# -*- coding: utf-8 -*-
"""2026-11-16 早报期 buglog 追加（幂等：命中即 return）。"""
import io, os, json, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(BASE, '.buglog', 'bugs')
D = '2026-11-16'


def app(fn, text):
    p = os.path.join(B, fn)
    s = io.open(p, encoding='utf-8').read()
    if D in s:
        print('skip (already)', fn)
        return
    if not s.endswith('\n'):
        s += '\n'
    s += text
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print('appended', fn)


app('2026-09-05-briefing-scheduler-missed-days.md', """

- **2026-11-16（周一）延迟约 119 分钟**：会话 `<current_time>` 实测 10:59:13，首次 `date` 10:59:22。序列续记至 9/13-11/16 共 65 个日历日：…/约 95(11/12)/约 111(11/13)/约 59(11/14)/约 700(11/15)/约 119(11/16)。落在历史区间 4-747 分钟的中高位，**未刷新上界**（119 < 747）。
- 10/19-11/16 连续二十九个自然日、早报线全部产出，无缺跑、无提前触发。
- **危害 1 档（交易日，方向被小幅改变）**：11-16 为周一、正常交易日。09:00 时点在亚市冲高段内（当日最高 3901.15 出现在早间），10:59 取数时已回落至 3874.63 → 按 09:00 交付约可报「平开微涨、冲击 3900」，实际交付「-0.14%、冲高失败」。差异幅度不足 0.5 个百分点，但结论句式从「冲击整数关」变成「整数关失败」，属 1 档而非 0 档。
- **跨日传染：本期为零（连续第三个零回填日，11-14/11-15/11-16）**。11-15 为周日、无新收盘，其图表点 3879.9 与 11-13 真实收盘一致，无需回填；11-16 当点为 10:59 实时读数，明日按纽约收盘回填。
- **建议 ⑬（延迟 >360 分钟须显式标注）本期未触发**（119 < 360）。但仍按惯例在邮件头部标注「生成于 10:59 CST、比标称 09:00 晚约 2 小时、价格为盘中读数非收盘」，`_meta.updated` 写 10:59 CST，`updateTime` 固定 09:00。
- **新增观察（危害分级的新维度）**：本期 119 分钟的实质影响不是「数字错」，而是「错过一个窗口」——09:00-11:00 之间金价完成了「冲 3901.15 → 回落 3874.63」的完整往返，早报在窗口结束时才落地，恰好只能报「失败」。**「延迟区间是否覆盖当日关键价格窗口」应作为危害分级的第三条判据**（前两条：当日是否有行情、跨日是否需回填）。
""")

app('2026-09-14-inspection-email-connector-down.md', """

## 2026-11-16（周一）早报期观测

- **恢复正常（11/15 失败后新序列第 1 日成功）**。email_sent = true，整期 status 记 success。
- **执行路径**：ToolSearch 传 `tool_names`（精确名）**一次命中** `mcp__qq-mail__SendMessage`／`GetMe`，未回落 agent-mail 命名空间 → `GetMe` 返回正常（scope 含 `mail:send`、日配额 2000）→ `SendMessage` 带 `body_format:HTML`＋`skip_confirmation:true` 一次成功返回 `queued:true` → `ListMessages(dir=sent)` 于 **11:03:57 CST** 确认落库（`msg_Y43_jSyMRnHKOuJzoTV59y8vFMoDLCQVRwR1UrPw87wXwA`，snippet 与产物首屏一致）。
- **「精确名检索 + 按名调用验证」两步法第 N 次完整执行、本次零失败**；邮件 HTML 规格 14 055 字符 / 19 078 字节 / 105 行 / maxline 477，零 `%%`、零 `width:100%` CSS 写法（改用 `width="100%"` 属性，从根上规避 BUG-017 家族）。
- **不构成修复证据**：本 bug 历史上「连续正常」已被多次证伪（最长 10/16-10/18 三日正常后第 4 日复发；11/12-11/14 三日正常后 11/15 复发）。当前新序列连续正常 1 日，severity 维持 major，观察窗继续。
""")

app('2026-09-25-inspection-scheduler-silent-miss.md', """

## 2026-11-16（周一）早报期体检

- 早报于 10:59 执行，**早于当日 noon（14:00）与 pm（22:00）两个时点** → 当日未到点，不判缺跑。
- 两条线最近产出均停在 **11-13**（`inspection_noon` 与 `inspection_pm` 各有 `logs/2026-11-13-inspection_*.json`，manifest 头部两条 status=no_action）。
- 11-14（周六）、11-15（周日）两线零产出：按 11/15 固化的分母修正（107 条巡检记录中落在周末的仅 3 条，**周末巡检非必跑**），**不计入「连续零产出交易日」**。
- 因此连续零产出交易日数 = 0（11-13 有产出，11-16 未到点），未达复合判据（连续 ≥5 个正常交易日零产出 且 恢复后 2 周内再现连续 ≥3 日）→ 不升级不降级。
- 镜像形态提示仍有效：两条线受同一调度器作用，会「一起缺跑／一起提前／一起夜间合并」，不可用单条线判断链路健康。
""")

app('2026-09-26-buglog-hook-misfire.md', """

- **2026-11-16 第二十九次连续命中（9/26-11/16）**：会话起始 hook 再次把自动化任务提示词全文透传为「用户报告了一个 bug」，判误判、未按字面建档。
- 附带误报本期形态：对 `scripts/build_20261116.py` 报「编辑 2 次，通常表示在修 bug」——实为 `trend.advice` 216→207→194 字两次压缩（自检拦下超 200 字后的正常收敛）；对 `scripts/mail_20261116.py` 报「编辑 2 次」——实为趋势标签由「🔴 偏空／🟢 偏多」改为纯文字（红绿 emoji 与中式涨跌配色相反，属生成前自纠）。两类均不计入修复。
- 本期真实故障为零（无报错、无重试、无用户纠正），故不新建 bug。双重复核已执行：逐文件 `grep -c` 计数 + 字节数/SHA-1 写入 logs 的 `buglog_verification`，index 与 bugs/ 已同步。
""")

# index.md 追加
idx = os.path.join(BASE, '.buglog', 'index.md')
s = io.open(idx, encoding='utf-8').read()
if '## 2026-11-16（周一）观察更新' in s:
    print('skip index')
else:
    s += """

## 2026-11-16（周一）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **119 分钟**（会话 current_time 10:59:13，首条 date 10:59:22），中高位、未刷新 10/31 的 747 分钟上界。**危害 1 档**：交易日，09:00 落在亚市冲高段内（当日最高 3901.15），10:59 取数已回落至 3874.63 → 交付句从「冲击 3900」变成「3900 失败」，幅度差不足 0.5 个百分点但方向结论不同。**跨日传染为零（连续第三个零回填日）**。**新增第三条危害判据：延迟区间是否覆盖当日关键价格窗口**——本期实质损失是「错过窗口」而非「数字错」 |
| BUG-006 | **正常（11/15 失败后新序列第 1 日成功）**。精确名检索一次命中、GetMe 正常、SendMessage queued、ListMessages(dir=sent) 于 11:03:57 CST 确认（`msg_Y43_jSyMRnHKOuJzoTV59y8vFMoDLCQVRwR1UrPw87wXwA`）。规格 14 055 字符 / 19 078 字节 / 105 行 / maxline 477，零 `%%`、零 `width:100%` CSS。不构成修复证据（连续正常已被多次证伪），severity 维持 major |
| BUG-012 | 早报 10:59 执行，早于 noon/pm 两个时点 → 当日未到点不判缺跑。两条线最近产出均为 11-13；11-14/11-15 周末零产出按「周末巡检非必跑」不计入。连续零产出交易日数 = 0，未达复合判据 |
| BUG-013 | **第 29 次连续命中**，判误判跳过建档。附带误报：build 脚本 advice 三次压缩（216→207→194）、mail 脚本趋势标签 emoji 改文字（红绿 emoji 与中式涨跌配色相反），均属生成前自纠，不计入修复。本期无真实故障 |

### 本期 buglog 复核凭据（2026-11-16）

- 逐文件 `grep -c "2026-11-16"`、字节数与 SHA-1 见 logs/2026-11-16-morning_briefing.json 的 `buglog_verification`（**在全部写入动作之后测量**）
- 本期无新增 bug、无状态变更：Open 12 / Fixed 13 / Total 25 维持不变（计数取自本文件表头，不照抄上期结论）
"""
    io.open(idx, 'w', encoding='utf-8', newline='\n').write(s)
    print('appended index.md')

# 测量凭据
files = {
    'BUG-003': '2026-09-05-briefing-scheduler-missed-days.md',
    'BUG-006': '2026-09-14-inspection-email-connector-down.md',
    'BUG-012': '2026-09-25-inspection-scheduler-silent-miss.md',
    'BUG-013': '2026-09-26-buglog-hook-misfire.md',
    'index': '../index.md',
}
ver = {}
for k, rel in files.items():
    p = os.path.join(B, rel) if rel != '../index.md' else idx
    raw = io.open(p, 'rb').read()
    txt = raw.decode('utf-8')
    ver[k] = {
        'file': os.path.basename(p),
        'occurrences': txt.count(D),
        'hit_lines': sum(1 for ln in txt.split('\n') if D in ln),
        'bytes': len(raw),
        'sha1': hashlib.sha1(raw).hexdigest(),
    }
print(json.dumps(ver, ensure_ascii=False, indent=2))
io.open(os.path.join(BASE, 'logs', '_buglog_ver_1116.json'), 'w', encoding='utf-8', newline='\n').write(
    json.dumps(ver, ensure_ascii=False, indent=2))
