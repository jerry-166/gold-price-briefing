# -*- coding: utf-8 -*-
"""2026-10-21 期 buglog 归档：BUG-003 / BUG-006 / BUG-012 / BUG-013 复发留痕 + index 同步 + 复核凭据。"""
import io
import json
import hashlib
import re
from pathlib import Path

BASE = Path('.')
B = BASE / '.buglog' / 'bugs'

b003 = B / '2026-09-08-briefing-scheduler-missed-days.md'
b006 = B / '2026-09-14-inspection-email-connector-down.md'
b012 = B / '2026-09-25-inspection-scheduler-silent-miss.md'
b013 = B / '2026-09-26-buglog-hook-misfire.md'

E003 = """
- **2026-10-21（周三）— 延迟复发，且刷新区间上界**：早报实际触发 **11:32**（会话内首次 `date` 实测 `2026-10-21 11:32:32`，起始即触发时刻，无需估算），距标称 09:00 **延迟 152 分钟**——**首次突破 10/10 的 133 分钟，区间定性改写为「4-152 分钟极宽摆动」**。延迟序列续记至 9/13-10/21 共 38 日：…/78/67/41/约 50/**152**。本期为本周连续第三个交易日产出（10/19、10/20、10/21），无缺跑、无提前触发。第 ⑦ 条「in_progress 占位兜底」本期**未启用**（会话单段连续完成、无中断），如实记为执行偏离。
- 影响面：快照时点从 09:4x 前移到 11:26，伦敦金读数 4119.64 已包含亚市早盘「下探 4106.23 后回升」的完整过程，与 09:00 口径不可直接横向比较；已在 `prices.source` 与 automation memory 中标注真实快照时间。
"""

E006 = """
**2026-10-21（周三）— 第七次复发，回到「工具未注册」形态，双通道同时失效**：早报第 5 步「发送邮件」**失败**（`logs/2026-10-21-morning_briefing.json` 记 `status: partial`、`email_sent: false`；HTML 底稿落 `.workbuddy/outbox/2026-10-21-morning.html`，11 665 字节）。
  - ① `connector-status` 显示 qq-mail 为 connected；`list_installed_plugins` 返回 `qq-mail@workbuddy-connector-plugins-official`、`bound: true`、`enabled: true`、`status: connected` → 绑定层、启用层均正常。
  - ② 但工具未进入会话索引：以 `mcp__qq-mail__send_mail` / `mcp__qq-mail__SendMessage` / `qq_mail_send` 三个候选名做精确检索，只回落到 agent-mail 的同名能力；再以关键词「qq」「邮箱发送」做两轮模糊检索，返回 `No matching tools found` → 判定为 **MCP 工具注册层故障**（10/6、10/10、10/12、10/19 的同一形态），非 10/15 的「工具在、调用即 -32602」形态。
  - ③ 第二通道同样不可用：`mcp__agent-mail__SendMessage` 返回「Agent 邮箱尚未开通」＋ `_agentmail_meta.status = not_bound` → 双通道同时失效、无降级路径。
  - ④ 未做任何假发送：`email_sent` 保持 false，未用其它渠道冒充 QQ Mail 发出，HTML 按既定流程落 `.workbuddy/outbox/` 待人工补发。
  - ⑤ 形态序列更新：`未注册`（10/6、10/10、10/12）→ `-32602`（10/15）→ `正常`（10/16、10/17、10/18）→ `未注册`（10/19）→ `正常`（10/20）→ **`未注册`（10/21）**。10/20 的单日正常如预期未能延续，**「恢复正常」再次被证伪，severity 维持 major、status 维持 open**。
  - ⑥ 本次新增可操作线索：本会话中 agent-mail 与 qq-mail **同时**不可用，而 ToolSearch 对 qq-mail 关键词**完全没有候选返回**（连 agent-mail 都不再被模糊匹配命中），提示故障可能发生在「deferred tools 索引装载」这一更上游的位置，而非连接器本身；建议下次复现时先记录 ToolSearch 的原始返回，再判断是否值得提交宿主侧排查。
"""

E012 = """
- **2026-10-21（周三）四维体检**：`inspection_noon` 与 `inspection_pm` 最近产出均为 **2026-10-20**，两条线连续无产出交易日数 = 0（10/21 的 14:00／22:00 未到，不计异常）；`ls logs/ | grep inspection` 最新两条为 `2026-10-20-inspection_noon.json` 与 `2026-10-20-inspection_pm.json`。**新增观察点：10/20 两条巡检的落盘时间分别为 23:47 与 23:50**（远晚于标称 14:00／22:00，且两者间隔仅 3 分钟），与 10/17「一起提前」、10/20 早间「pm 提前 12 小时」并列，构成第三种镜像形态——**「一起延后到夜间合并触发」**。无论提前还是延后，两条线仍同步受调度器作用，与既有结论一致。按复合判据当前连续数 0 < 3，不升级不降级；观察期自 10/15 起算仍在 2 周窗口内（至 10/29）。
"""

E013 = """
- **2026-10-21（周三）第二十三次连续命中**（9/26-10/21）：hook 再次透传自动化任务提示词全文作为「用户报告的 bug」，按既定判别流程判为**误判、未按字面建档**，改为人工盘点本期真实异常（BUG-003 延迟 152 分钟刷新上界、BUG-006 第七次复发）并逐条留痕。
- 附带误报本期形态：①把 `scripts/gen_20261021.py` 的两次编辑（`trend.advice` 209→191 字压缩、4155 折算值 897→898 修正）弱提示为「正在修复 bug」——实为正常自检返工，忽略；②「同一文件被编辑 ≥2 次」在 `scripts/selfcheck_20261021.py` 上同样触发（期望值由 897 改为 898），属同一类正常迭代。
- **双重复核已执行**（BUG-013 既定要求）：(a) 逐文件 `grep -c "2026-10-21" .buglog/bugs/*.md` 计数；(b) 四个受影响 bug 文件的字节数与 SHA-1 写入 `logs/2026-10-21-morning_briefing.json` 的 `buglog_verification` 字段，并校验 `index.md` 结论与 `bugs/` 实际内容一致。
"""

for path, text in [(b003, E003), (b006, E006), (b012, E012), (b013, E013)]:
    s = io.open(path, encoding='utf-8').read()
    if '2026-10-21' in s:
        print('skip (already has 10-21):', path.name)
        continue
    io.open(path, 'a', encoding='utf-8').write(text)
    print('appended:', path.name)

# ---- index.md 同步 ----
ip = BASE / '.buglog' / 'index.md'
idx = io.open(ip, encoding='utf-8').read()

adds = {
    'BUG-003': '；**10/21 延迟 152 分钟（会话起始 11:32:32 实测），首次突破 10/10 的 133 分钟，区间改写为「4-152 分钟极宽摆动」**',
    'BUG-006': '；**10/21 第七次复发、回到「工具未注册」形态，且 ToolSearch 对 qq-mail 关键词返回零候选（故障点疑在 deferred tools 索引装载层）；agent-mail 仍 not_bound，双通道同时失效，`email_sent: false`、status partial，HTML 落 `.workbuddy/outbox/2026-10-21-morning.html`（11 665 字节）待人工补发；10/20 的单日正常未能延续 → 「恢复正常」再次证伪**',
    'BUG-012': '；**10/21 体检：两条线最近产出均为 10/20、连续无产出交易日数 0，未达复合判据；新增第三种镜像形态——10/20 两条巡检分别于 23:47／23:50 落盘，呈「一起延后到夜间合并触发」，与「一起缺跑」「一起提前」并列**',
    'BUG-013': '；**10/21 第二十三次连续命中，判误判跳过建档；附带误报为 advice 压缩（209→191 字）与 4155 折算修正（897→898）被弱提示为修 bug；双重复核已执行（逐文件 `grep -c` ＋ 四文件字节数/SHA-1 写入 logs 的 `buglog_verification`），index 与 bugs/ 已同步**',
}

for bid, extra in adds.items():
    # 在该行最后一个 " | major | open |" / " | minor | open |" 之前插入
    pattern = re.compile(r'^(\| ' + bid + r' \|.*?)(\s*\|\s*(?:major|minor|trivial)\s*\|\s*open\s*\|\s*)$', re.M | re.S)
    m = pattern.search(idx)
    if not m:
        print('INDEX ROW NOT FOUND', bid)
        continue
    if '10/21' in m.group(1):
        print('index skip', bid)
        continue
    idx = idx[:m.start()] + m.group(1).rstrip() + extra + ' |' + m.group(2).lstrip(' |').rstrip() + idx[m.end():]
    # 简化：直接重建该行尾部
idx = re.sub(r'\s*\|\s*(major|minor|trivial)\s*\|\s*open\s*\|\s*$', lambda mm: ' | ' + mm.group(1) + ' | open |', idx, flags=re.M)
io.open(ip, 'w', encoding='utf-8').write(idx)
print('index updated')

# ---- stats.json ----
sp = BASE / '.buglog' / 'stats.json'
st = json.load(io.open(sp, encoding='utf-8'))
ids = [re.search(r'^id: (BUG-\d+)', io.open(f, encoding='utf-8').read(), re.M).group(1)
       for f in sorted(B.glob('*.md'))]
opened = sum(1 for f in sorted(B.glob('*.md'))
             if re.search(r'^status: open', io.open(f, encoding='utf-8').read(), re.M))
st['total_count'] = len(ids)
st['open_count'] = opened
st['fixed_count'] = len(ids) - opened
io.open(sp, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2))
print('stats:', st)
