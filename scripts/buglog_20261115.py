# -*- coding: utf-8 -*-
"""2026-11-15 早报期 buglog 追加（幂等：命中即 return，不再往下执行追加）。"""
import io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(BASE, '.buglog', 'bugs')
D = '2026-11-15'


def app(fn, text):
    p = os.path.join(B, fn)
    s = io.open(p, encoding='utf-8').read()
    if D in s:
        print('skip (already)', fn)
        return
    if not s.endswith('\n'):
        s += '\n'
    s += text
    io.open(p, 'w', encoding='utf-8').write(s)
    print('appended', fn)


app('2026-09-05-briefing-scheduler-missed-days.md', """

- **2026-11-15（周日）延迟约 700 分钟**：会话 `<current_time>` 实测 20:39:51，首次 `date` 20:39:56 实测。序列续记至 9/13-11/15 共 64 个日历日：…/约 81(11/03)/约 130(11/07)/约 170(11/08)/约 50(11/11)/约 95(11/12)/约 111(11/13)/约 59(11/14)/约 700(11/15)。落在 4-747 分钟区间的高位，**仅次于 10/31 的 747 分钟，为历史第二大值，未刷新上界**（700 < 747）。
- 10/19-11/15 连续二十八个自然日、早报线全部产出，无缺跑、无提前触发。
- **危害 0 档（「非交易日延迟危害恒为 0」判据第三次生效）**：11-15 为周日，国际盘、上金所、外汇交易中心全部休市，20:39 取到的读数与 09:00 完全同值（伦敦金 3879.92、AU9999 837.00、中间价 6.7152），延迟不改变任何一个数字。
- **本期无跨日传染**（当日无新收盘、无可回填点），为连续第二个「零回填」周末日（11-14、11-15）。
- **新形态：延迟跨过整个交易日 → 早报在晚间交付**。产物标称口径 09:00，实际交付 20:39，相差 11.6 小时，读者拿到时距下一交易日（11/16）开盘只剩约 12 小时；这与「延迟 1-2 小时」不是同一类问题——前者只影响快照时点，后者改变了交付场景（晨间阅读→睡前阅读）。
- **新增建议 ⑬：延迟 >360 分钟的期次，交付物（邮件头部／`_meta.updated`）必须显式标注「延迟交付 + 真实生成时点」**，避免读者把晚间读数当晨间读数。本期已在邮件头部写明「本期生成于 20:50（原定 09:00，任务延迟约 700 分钟）」、`_meta.updated` 写 20:50 CST，`updateTime` 仍固定 09:00（定时口径不变）。
""")

app('2026-09-14-inspection-email-connector-down.md', """

## 2026-11-15（周日）早报期观测

- **复发（11/12-11/14 连续正常 3 日后中断，新序列第 1 日失败）**。email_sent = false，整期 status 记 partial。
- **形态：MCP 工具未装载进 deferred tools 索引**，四重证据：① ToolSearch 传 `tool_names` 精确名（mcp__qq-mail__SendMessage／GetMe／ListMessages）**两次，两次都回落 agent-mail 命名空间**、只返回 mcp__agent-mail__*；② 关键词检索（qq-mail 发送邮件 / QQ邮箱 send message）同样只出 agent-mail；③ 按名调用 `DeferExecuteTool("mcp__qq-mail__GetMe")` → `not found in the deferred tools index`；④ `list_installed_plugins` 显示 `qq-mail@workbuddy-connector-plugins-official` status=connected、bound=true、enabled=true。
- **结论升级**：「connected ＋ bound ＋ enabled」三真 ＋ 精确名检索回落 agent-mail = 索引未装载，这是 BUG-006 的**第 3 种可复现证据组合**（前两种：工具 not found 单证、connector-status 显示 connecting 但工具不可用）。
- **新增限制：reconnect 在无人值守时段不可用**。按 connector-status 指引调用 `reconnect_plugin(qq-mail@workbuddy-connector-plugins-official)`，返回 `User refused, no changes applied. Reconnection cancelled or timed out.`——重连需要人机交互确认，自动化时段无人点「授权」，所以**这条自愈路径对定时任务实际上是断的**。
- **备用通道也不通**：`mcp__agent-mail__GetMe` 返回 `not_bound`（Agent 邮箱尚未开通），故本期无任何可用发信通道。
- 产物：HTML 落 `.workbuddy/outbox/mail-2026-11-15.html`（11 315 字符／16 961 字节／70 行／maxline 561；`grep -c '100%%'` = 0、`width:100%` 正常），待人工补发。
- **建议（新增）：把「发信」从 MCP 依赖里解耦**。要么在 09:00 前人工确认 qq-mail 工具已装载，要么改用可脚本化的 SMTP/第三方 API 直发，否则每天的发信成功率完全取决于宿主当天的工具索引状态，任务侧无法自愈。
""")

app('2026-09-25-inspection-scheduler-silent-miss.md', """

## 2026-11-15（周日）早报期观测

- 11-15 早报于 **20:39** 执行，晚于当日 `inspection_noon`（14:00）时点、早于 `inspection_pm`（22:00）时点 → 当日午后巡检零产出，属「早报延迟跨过巡检时点」的倒序形态（10/21 曾出现「巡检抢占早报时点」，方向相反）。
- 回看 11-14（周六）：`inspection_noon` 与 `inspection_pm` 两个文件均**不存在**。但历史统计显示周末巡检本就不是必跑：全部 107 条巡检记录中，落在周六/周日的仅 3 条（10-17 两条、11-07 一条），故 11-14 两线零产出**不计入「连续零产出交易日」**。
- 11-13（周五）：noon 与 pm 两文件均在、manifest 头部各有记录 → 两线均有产出（已核）。
- 连续零产出交易日数 = 0，未达复合判据（连续 ≥5 个正常交易日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出），不升级不降级。观察期继续。
""")

app('2026-09-26-buglog-hook-misfire.md', """

## 2026-11-15（周日）

- **第 48 次连续命中**（9/26-11/15），判误判跳过建档。hook 再次以「用户报告了一个 bug」开头、透传自动化任务提示词全文（含「第一步/第二步」流程编号与「你是金价早报自动化助手」开头），无异常现象、无期望行为，按判据不建 bug。
- **但本期确有真实故障**（BUG-006 复发：qq-mail 工具未装载 + reconnect 被取消 + 备用邮箱未开通），按「真实失败优先」正常建档，见 BUG-006 条目。
- 弱提示本期命中 1 次：`scripts/build_20261115.py` 被编辑 2 次（`trend.advice` 首稿 208 字超限、压到 196 字后一次过检）。属生成前自纠，**不计入修复**。
- 复核口径维持升级版：index.md 逐日 `grep -c` 计数 ＋ 四个 bug 文件计数并列，同时记字节数／SHA-1；**凭据一律在全部写入动作之后测量**（11-14 期固化）。
""")

# ---- index.md 追加当日观察更新 ----
ip = os.path.join(BASE, '.buglog', 'index.md')
s = io.open(ip, encoding='utf-8').read()
if '## 2026-11-15（周日）观察更新' in s:
    print('skip (already) index.md')
else:
    block = """
## 2026-11-15（周日）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **700 分钟**（会话 current_time 20:39:51，首条 date 20:39:56），**仅次于 10/31 的 747 分钟、为历史第二大值**，未刷新上界。**危害 0 档**（周日三市场全停、读数与 09:00 完全同值），「非交易日危害恒为 0」判据第三次生效。**本期无跨日传染**（无新收盘）。**新形态：延迟跨过整个交易日 → 早报晚间交付**，标称 09:00 与交付 20:39 相差 11.6 小时；**新增建议 ⑬：延迟 >360 分钟须在交付物显式标注延迟与真实生成时点**（本期邮件头部已标注） |
| BUG-006 | **复发（连续正常 3 日后中断，新序列第 1 日失败）**，email_sent=false、整期 partial。四重证据指向「工具未装载进 deferred 索引」：精确名检索两次均回落 agent-mail、关键词检索同样、按名调用 not found、插件列表却三真（connected/bound/enabled）。**新增两条结论：①「三真 + 检索回落」是第 3 种可复现证据组合；② reconnect_plugin 在无人值守时段不可用（返回 User refused / cancelled），这条自愈路径对定时任务实际是断的**。备用 agent-mail 亦未开通（not_bound）。HTML 落 outbox 待人工补发 |
| BUG-012 | 11-15 早报 20:39 执行，晚于 noon 时点、早于 pm 时点 → 当日午后巡检零产出，属「早报延迟跨过巡检时点」倒序形态。11-14（周六）两线零产出，但历史 107 条巡检记录中周末仅 3 条，周末非必跑 → 不计入连续零产出。连续零产出交易日数 0，未达复合判据 |
| BUG-013 | **第 48 次连续命中**，判误判跳过建档。本期真实故障为 BUG-006 复发，按「真实失败优先」正常建档。弱提示命中 build_20261115.py 编辑 2 次（advice 208→196 字压缩），属生成前自纠、不计入修复 |

### 本期 buglog 复核凭据（2026-11-15）

- 逐文件 `grep -c "2026-11-15"`（全文出现次数／命中行数）与字节数、SHA-1 见 logs/2026-11-15-morning_briefing.json 的 `buglog_verification`（**在全部写入动作之后测量**）
- 本期无新增 bug、无状态变更：Open 12 / Fixed 12 / Total 24 维持不变
"""
    s = s.rstrip('\n') + '\n' + block
    io.open(ip, 'w', encoding='utf-8').write(s)
    print('appended index.md')
