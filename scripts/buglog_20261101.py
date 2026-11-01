# -*- coding: utf-8 -*-
"""2026-11-01 期 buglog 写入：BUG-003 / BUG-006 / BUG-012 / BUG-013。"""
import io, os, hashlib, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BL = os.path.join(BASE, '.buglog')

E003 = """
- **2026-11-01（周日）延迟约 67 分钟，回落到「常规延迟」区间**：会话 `<current_time>` 为 10:07:19，首次 `date` 实测 10:07:56。原定 09:00 → 10:07 相隔约 67 分钟，序列续记至 9/13-11/01 共 50 个日历日：…/约 20(10/29)/约 44(10/30)/约 747(10/31)/约 67(11/01)。昨日 747 分钟的超长形态未复现，属单次极端值而非趋势。
- **本期再次印证「晚不等于错」这一结论的方向性，但结论需要修正一半**：周日三地休市，价格与结算价在周五就已固定，因此 67 分钟的延迟对数据准确性完全没有影响（本期无需任何图表回填，10-30 点一次到位、10-31 与 11-01 同值）。对比 10/31 的 747 分钟「反而最准」和 10/30 的 44 分钟「把平盘写成跌 0.43%」，可以得到更精确的表述：**延迟的危害程度 ＝ 延迟跨越的行情变动量**，在交易日等于「09:00 亚市快照与当日收盘之间的落差」，在周末恒为 0。所以 BUG-003 的严重性应按交易日/非交易日分档，而非单纯按分钟数排。
- 建议（续前 ⑧ 条）：非交易日的早报在 `_meta` 与邮件底部显式写「本期延迟 X 分钟，因休市对数据无影响」，避免读者把「迟到」误读成「数据不准」。本期已在邮件底部注明生成时刻 10:11。
"""

E006 = """
- **2026-11-01 恢复正常（第 17 次观察，连续正常 1 日）**：`connector-status` 报 qq-mail `connected`；实测三步全通——`GetMe` 返回 alias `2132049351@qq.com`（scopes: alias:read / mail:read / mail:send，日发送配额 2000）、`SendMessage` 返回 `{"queued":true}`、`ListMessages(dir=sent)` 在 02:11:29Z（＝北京时间 10:11:29）确认新邮件已在「已发送」目录。`email_sent: true`。
- **新增可用性诱因证据（重要）**：本期与昨日的关键差异不在「服务是否在线」，而在**工具检索方式**——10/31 用三组关键词（`qq mail send email` / `qq` / `qqmail send_message`）检索 ToolSearch，全部只命中 agent-mail；本期改用 `tool_names` 精确名检索（`mcp__qq-mail__SendMessage`、`mcp__qq-mail__GetMe`），一次命中并可直接调用。据此提出新假设：BUG-006 的一部分「工具未注册」现象，实为**关键词检索拿不到 deferred tools 索引**导致的假阴性，而非服务端真的未注册。建议后续每次先用精确名检索一次，仍失败再判定为服务端故障。
- 待验证：若精确名检索也失败，才可归入服务端/鉴权类。该假设需在后续 3 至 5 期内复现验证，暂不结案。
"""

E012 = """
- **2026-11-01（周日）四维体检**：`ls logs/ | grep -c '2026-11-01-inspection'` ＝ 0，两条巡检线当日零产出；11-01 为周日、非交易日，不计入连续阈值。最近产出仍为 `inspection_noon` / `inspection_pm` 的 10/30。
- 当日「是否有任何产出」布尔判据：早报已产出（本文件），故 today_has_any_output ＝ true；连续零产出**交易日**数 ＝ 0（10/31、11/01 均为非交易日）。未达复合判据（连续 ≥5 个正常交易日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出），不升级不降级。
- 待观察点：11/02（周一）是下一个正常交易日，若早报与两条巡检线在 11/02 全部零产出，则「恢复后连续零产出」计数从 0 起算，需重点盯 11/02-11/06 这一周。
"""

E013 = """
- **2026-11-01 第三十四次连续命中**：hook 再次把自动化任务提示词全文透传为「用户报告的 bug」，并额外附一句「用户可能在指出本次会话中遗漏的问题」，判误判、未按字面建档。本条为事实来源，逐日 `grep -c` 计数留证。
- 附带误报本期形态：`scripts/build_20261101.py` 的 3 次编辑被弱提示为「在修 bug」——实为 `trend.advice` 211 → 205 → 195 字的两次压缩（自检 `advice too long: 211` 拦下）与 `trend.long` 里「新疆以外柜台客流翻番」误写为「北京菜百与深圳水贝客流翻番」的措辞修正，均属正常自检返工，非缺陷修复。
- 双重复核已执行：逐文件 `grep -c "2026-11-01"` 计数、四文件字节数与 SHA-1 全部写入 `logs/2026-11-01-morning_briefing.json` 的 `buglog_verification`；index.md 本期结论与 bugs/ 实际内容已同步。
"""

IDX = """
## 2026-11-01（周日）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | **延迟约 67 分钟，回落到常规区间**（会话 10:07:19、首次 `date` 10:07:56），昨日 747 分钟的超长形态未复现、属单次极端值。序列 50 个日历日 …/约 44(10/30)/约 747(10/31)/约 67(11/01)。**口径修正**：延迟危害 ＝ 延迟跨越的行情变动量，交易日看「亚市快照与收盘落差」，非交易日恒为 0，故严重性应按交易日/非交易日分档而非按分钟排 |
| BUG-006 | **恢复正常（第 17 次观察，连续正常 1 日）**：`GetMe` 返回 alias 与 scopes 正常、`SendMessage` 返回 queued、`ListMessages(dir=sent)` 于 10:11:29 CST 确认入「已发送」。`email_sent: true`。**新假设**：昨日「工具未注册」疑为关键词检索拿不到 deferred tools 索引的假阴性——本期改用 `tool_names` 精确名检索一次即命中，建议后续先精确名检索再判服务端故障 |
| BUG-012 | 两线 11/01 零产出（`grep -c 2026-11-01-inspection` ＝ 0），周日非交易日不计阈值；当日有产出（早报），连续零产出交易日数 0，未达复合判据，不升级不降级。重点观察 11/02（周一）起的一周 |
| BUG-013 | 第 34 次连续命中，判误判跳过建档；附带误报为 `build_20261101.py` 的两次 advice 压缩（211→205→195 字）与 `trend.long` 措辞修正；双重复核已执行（逐文件 `grep -c` ＋ 字节数/SHA-1 写入 logs 的 `buglog_verification`） |
"""

TARGETS = [
    ("bugs/2026-09-08-briefing-scheduler-missed-days.md", E003),
    ("bugs/2026-09-14-inspection-email-connector-down.md", E006),
    ("bugs/2026-09-25-inspection-scheduler-silent-miss.md", E012),
    ("bugs/2026-09-26-buglog-hook-misfire.md", E013),
    ("index.md", IDX),
]

for rel, text in TARGETS:
    path = os.path.join(BL, rel)
    with io.open(path, 'a', encoding='utf-8', newline='\n') as f:
        f.write(text)
    raw = io.open(path, 'rb').read()
    print('%-52s bytes=%d sha1=%s cnt=%d' % (
        rel, len(raw), hashlib.sha1(raw).hexdigest(),
        io.open(path, encoding='utf-8').read().count('2026-11-01')))
