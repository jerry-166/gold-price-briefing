# -*- coding: utf-8 -*-
"""向 buglog 各 bug 文件追加 2026-10-22 留痕"""
from pathlib import Path

B = Path(__file__).resolve().parent.parent / '.buglog' / 'bugs'

BUG003 = """

**2026-10-22（周四）— 第二十四期留痕（延迟形态，未缺跑、未提前）**：会话触发时刻 **09:23:59 CST**（automation 提示词注入时间，会话内首个 `date` 实测 09:26:32）→ **延迟约 24 分钟**，落在历史区间中低位，未刷新任何上界。延迟序列续记至 9/13-10/22 共 39 日：…/67/41/约 50/152/**约 24**。**定性维持「4-152 分钟极宽摆动」**；本期为本周第四个交易日连续产出（10/19、10/20、10/21、10/22），无缺跑、无提前触发。影响面：24 分钟的延迟使伦敦金读数取到 09:24:22 的亚市实时价 4111.05（今开 4139.90，当日已下探至 4109.80），若准点 09:00 取价则会更接近 4139.90 的开盘水平——延迟对口径的影响仍可观测，**建议 ②（定时提前至 07:00-07:30）继续维持**。第 ⑦ 条「in_progress 占位兜底」本期**未启用**（会话单段连续完成、无中断），如实记为执行偏离。幂等检查前置：`daily/2026-10-22.json` 不存在、`logs/manifest.json` 头部无当日 morning_briefing 记录、`git log` 无当日早报提交 → 无中断残留（BUG-014 未复现）。前置缺口检查：上次早报 10/21（partial／邮件失败但数据与推送成功），10/22 为其后第一个交易日，其间无缺失交易日 → 无断档。
"""

BUG006 = """

**2026-10-22（周四）— 第八次复发，连续第二日「工具未注册」形态，双通道同时失效**：早报第 5 步「发送邮件」**失败**（`logs/2026-10-22-morning_briefing.json` 记 `status: partial`、`email_sent: false`；HTML 底稿落 `.workbuddy/outbox/2026-10-22-morning.html`，14 611 字节；另存纯文本版 2 901 字符便于人工补发）。
  - ① `connector-status` 显示 qq-mail 为 connected；但会话工具索引中**没有任何 `mcp__qq-mail__*` 工具**。
  - ② ToolSearch 以三组关键词检索（「qq mail send email」「发送邮件 QQ邮箱」「qqmail 邮件连接器 / QQ Mail connector send html email」），**命中的全部是 `mcp__agent-mail__*` 的同名能力**，`mcp__qq-mail__SendMessage` 始终无候选 → 判定为 **MCP 工具注册层故障**（10/6、10/10、10/12、10/19、10/21 的同一形态），非 10/15 的「工具在、调用即 -32602」形态。
  - ③ 第二通道同样不可用：`mcp__agent-mail__GetMe` 返回「Agent 邮箱尚未开通」＋ `_agentmail_meta.status = not_bound` → 双通道同时失效、无降级路径（与 10/21 完全一致）。
  - ④ 未做任何假发送：`email_sent` 保持 false，未用其它渠道冒充 QQ Mail 发出，HTML 按既定流程落 `.workbuddy/outbox/` 待人工补发。
  - ⑤ 形态序列更新：`未注册`（10/6、10/10、10/12）→ `-32602`（10/15）→ `正常`（10/16、10/17、10/18）→ `未注册`（10/19）→ `正常`（10/20）→ **`未注册`（10/21、10/22 连续两日）**。**本期首次出现「未注册」形态连续两日**，说明该形态并非单日抖动；severity 维持 major、status 维持 open。
  - ⑥ 线索延续：ToolSearch 对 qq-mail 关键词仍然零候选，故障点继续指向「deferred tools 索引装载」这一上游环节，而非连接器绑定/授权层。
"""

BUG012 = """

- **2026-10-21 / 10-22 体检**：`inspection_noon` 最近产出 10-21（实际落盘 21:40，标称 14:00 → **延迟约 7h40m**，属「延迟到夜间合并触发」形态）；`inspection_pm` 最近产出 10-21（22:00 正常触发、`no_action`）。10/19-10/21 两条线连续三日均有产出，为本 bug 观察期内少见的连续正常段，但**形态曾在「提前触发／静默缺跑／正常／夜间合并触发」之间切换过至少三次，连续三日正常仍不足以判定修复**。10-22 两条线尚未到点。
"""

BUG013 = """

- **2026-10-22（周四）第二十四次连续命中**（9/26-10/22）：hook 再次把自动化任务提示词全文当作「用户报告的 bug」透传（原文以「你是金价早报自动化助手」开头、含「第一步/第七步」流程编号、无异常现象也无期望行为），按既定判别流程判为**误判、未按字面建档**，改为人工盘点本期真实异常（BUG-003 延迟约 24 分钟、BUG-006 第八次复发且「未注册」形态首次连续两日、BUG-012 巡检链路体检）并逐条留痕。
- 附带误报本期形态：对 `scripts/gen_20261022.py` 的第二次编辑被弱提示为「正在修复 bug」——实际是真缺陷修复：初版脚本把 `events` 索引整体 -1 后未剔除降至 -1 的过期事件（09-22 点已滚出 30 日窗口），导致 `chart.events` 残留 `index: -1` 的孤儿记录；已在脚本中加入 `if e['index'] - 1 < 0: continue` 并重新生成，校验 `all(labels[e['index']] == e['date'])` 通过。属自检环节拦下的产物缺陷（BUG-010 类），非调度类 bug，故不单独立档。
- **双重复核已执行**：写入后逐文件 `grep -c "2026-10-22" .buglog/bugs/*.md` 计数，并把四个受影响 bug 文件的字节数与 SHA-1 写入 `logs/2026-10-22-morning_briefing.json` 的 `buglog_verification` 字段；`index.md` 四行结论同步追加本期内容。
"""

for name, text in [
    ('2026-09-08-briefing-scheduler-missed-days.md', BUG003),
    ('2026-09-14-inspection-email-connector-down.md', BUG006),
    ('2026-09-25-inspection-scheduler-silent-miss.md', BUG012),
    ('2026-09-26-buglog-hook-misfire.md', BUG013),
]:
    p = B / name
    s = p.read_text(encoding='utf-8')
    if '2026-10-22' in s:
        print('skip (already)', name)
        continue
    if not s.endswith('\n'):
        s += '\n'
    p.write_text(s + text, encoding='utf-8')
    print('appended', name, p.stat().st_size, 'bytes')
