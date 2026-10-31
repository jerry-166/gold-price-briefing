# -*- coding: utf-8 -*-
"""2026-10-31 期 buglog 写入：BUG-003 / BUG-006 / BUG-012 / BUG-013。"""
import io, os, hashlib, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BL = os.path.join(BASE, '.buglog')

E003 = """
- **2026-10-31（周六）延迟约 747 分钟，观察期首次以「小时」计、上界改写为 4-747 分钟**：会话起始 21:27:29（`<current_time>` 实测），首次 `date` 实测 21:27:36。原定 09:00 → 21:27 相隔约 12 小时 27 分 ＝ 747 分钟，把此前 10/28 创下的 275 分钟上界一次性推高 2.7 倍。序列续记至 9/13-10/31 共 49 个日历日：…/约 20(10/29)/约 44(10/30)/约 747(10/31)。
- **关键新形态：早上 09:00 完全零产出，当晚才补跑**——21:27 之前 `daily/2026-10-31.json` 与 `logs/2026-10-31-morning_briefing.json` 均不存在，仓库内最新产物停在 10/30（`git log -1` 为 c511e29 日志：巡检 2026-10-30 晚间）。这不是 BUG-002 式的「当日已成功后再次运行」，而是**唯一一次触发就迟到了 12.5 小时**，属「静默缺跑 ＋ 超长延迟」的复合形态；按 BUG-014 口径它没有半成品残留，是一次干净的迟到。
- **反面印证一条**：正因为迟到 12.5 小时，本期反而成为近月最准确的一期——09:00 只能拿到亚市快照（当时约 4020 附近，方向会被写成平盘），而 21:27 拿到的是周五真实收盘 3876.69，因此本期无需执行「昨晨快照 → 真实收盘」的图表回填（10-30 点一次到位）。这再次说明 BUG-003 的核心危害不在「晚」而在「早」：越晚越准，越准越说明 09:00 本就不该是取数时点。
- 建议（续前 ⑦ 条）：早报若在 16:00 之后才触发，应自动改用「当日真实收盘」口径并在邮件显著标注，本期已这么做（邮件底部注明「延迟补发、内容已改用周五真实收盘价」）。
"""

E006 = """
- **2026-10-31 第十六次复发（形态：双通道同时「未注册／未绑定」）**：`connector-status` 显示 agent-mail `connected`、qq-mail `connecting`；实测 `mcp__agent-mail__GetMe` 返回 `{"_agentmail_meta":{"status":"not_bound"}}`（Agent 邮箱尚未开通），ToolSearch 以 `qq mail send email`、`qq`、`qqmail send_message` 三组关键词检索均只命中 agent-mail，`mcp__qq-mail__*` 未进工具索引 → 无任何降级路径。`email_sent: false`、status `partial`，完整 HTML 底稿落 `.workbuddy/outbox/2026-10-31-morning.html`（15 283 字节、最长行 693 字符）待人工补发。
- 序列：正常(10/29) → 正常(10/30) → 复发(10/31)，连续正常计数由 2 归零，距「连续 ≥5 日」门槛再退 5 日。
- **新增判据冲突证据**：`connector-status` 报告 agent-mail 为 `connected`，而 `GetMe` 同一会话内返回 `not_bound`；结合 10/28 记录的「status 字段缓存滞后」，再次确认宿主侧状态字段不能作为可用性凭据，必须以一次真实调用（`GetMe` / `SendMessage`）为准。
"""

E012 = """
- **2026-10-31（周六）四维体检**：`ls logs/ | grep -c '2026-10-31-inspection'` ＝ 0，两条线当日零产出；周六为非交易日，不计入连续阈值，但如实留痕。最近产出：`inspection_noon` 10/30、`inspection_pm` 10/30（10/30 晚间巡检为 partial 波动型预警）。
- 当日「是否有任何产出」布尔判据：早报已在 21:27 补跑（见 BUG-003），故 today_has_any_output ＝ true；连续零产出交易日数 ＝ 0，未达复合判据（连续 ≥5 个正常交易日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出），不升级不降级。
- 补充观察：本期两条巡检线不是「缺跑」而是「未被调度器触碰到」——与早报的 747 分钟超长延迟同源，疑为宿主侧同一时段（10/31 白天）调度整体未生效，建议与 BUG-003 合并观察。
"""

E013 = """
- **2026-10-31 第三十三次连续命中**：hook 再次把自动化任务提示词全文透传为「用户报告的 bug」，判误判、未按字面建档。
- 附带误报本期形态：`scripts/build_20261031.py` 的多次编辑被弱提示为「在修 bug」——实为 `trend.advice` 226 → 220 → 196 字的三次压缩（自检拦下「too long」）与 3730 折算值 806 → 805 的修正，均属正常自检返工。
- 双重复核已执行：逐文件 `grep -c "2026-10-31"` 计数、四文件字节数与 SHA-1 全部写入 `logs/2026-10-31-morning_briefing.json` 的 `buglog_verification`；index.md 本期结论与 bugs/ 实际内容已同步。
"""

IDX = """
## 2026-10-31（周六）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | **延迟约 747 分钟（12 小时 27 分），观察期首次以「小时」计，上界由 275 改写为 4-747 分钟**：会话起始 21:27:29 实测。新形态为「早上 09:00 完全零产出、当晚补跑」，仓库内在 21:27 之前无 10/31 任何产物。序列 49 个日历日 …/约 20(10/29)/约 44(10/30)/约 747(10/31)。反面印证：因迟到 12.5 小时，本期直接拿到周五真实收盘 3876.69，无需做「昨晨快照 → 真实收盘」回填，为近月最准确一期 |
| BUG-006 | **第十六次复发（第 16 次观察，形态：双通道同时不可用）**：agent-mail `GetMe` 返回 `not_bound`、`mcp__qq-mail__*` 未进工具索引（三组关键词检索均只命中 agent-mail）→ `email_sent: false`、status partial，HTML 底稿 15 283 字节落 `.workbuddy/outbox/2026-10-31-morning.html` 待人工补发。连续正常计数由 2 归零。另留证：`connector-status` 报 connected 与 `GetMe` 报 not_bound 并存，状态字段不可作可用性凭据 |
| BUG-012 | 两线 10/31 零产出（`grep -c 2026-10-31-inspection` ＝ 0），周六非交易日不计阈值；最近产出均为 10/30。当日有产出（早报 21:27 补跑），连续零产出交易日数 0，未达复合判据，不升级不降级。疑与 BUG-003 同源（宿主侧 10/31 白天调度整体未生效） |
| BUG-013 | 第 33 次连续命中，判误判跳过建档；附带误报为 `build_20261031.py` 的三次 advice 压缩（226→220→196 字）与 806→805 折算修正；双重复核已执行（逐文件 `grep -c` ＋ 字节数/SHA-1 写入 logs 的 `buglog_verification`） |
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
    print('%-52s bytes=%d sha1=%s cnt1031=%d' % (
        rel, len(raw), hashlib.sha1(raw).hexdigest(),
        io.open(path, encoding='utf-8').read().count('2026-10-31')))
