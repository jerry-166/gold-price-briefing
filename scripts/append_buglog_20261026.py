# -*- coding: utf-8 -*-
"""为 2026-10-26 早报追加 buglog 条目（独立脚本，避免 bash 吞反引号）。"""
import io, os, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGS = os.path.join(ROOT, ".buglog", "bugs")

BUG003 = """

- **2026-10-26（周一）延迟约 67 分钟**：会话起始 10:07:17（`<current_time>` 实测），首次命令 `date` 实测 10:08:21，全部步骤结束约 10:14。序列续记至 9/13-10/26 共 44 个日历日：…/约 39/约 46/约 100/**约 67**（回落到区间中位，低于昨日 100 分钟、高于 10/23 的 39 分钟），仍属「4-152 分钟极宽摆动」，未刷新任何边界。10/19-10/26 连续八个自然日、六个交易日全部产出，无缺跑、无提前触发。影响面：67 分钟延迟使伦敦金读数落在 10:05:35 的亚市实时价 3994.46（今开 3995.14、当日已走出 3978.01-4003.99 的约 26 美元振幅），若准点 09:00 取价会更贴近 3995 的开盘水平，当日方向（-0.03%）不受影响、仅细节不同 → **建议 ②（定时提前至 07:00-07:30）继续维持**。第 ⑦ 条 in_progress 占位兜底本期未启用（会话单段连续完成），如实记为执行偏离。幂等检查前置：`daily/2026-10-26.json` 不存在、`logs/manifest.json` 头部无当日 morning_briefing 记录、`git log` 无当日早报提交 → 无中断残留（BUG-014 未复现）。前置缺口检查：上次早报 10/25（周日，success），10/26 为其后第一个交易日，其间无缺失交易日 → 无断档。
"""

BUG006 = """

- **2026-10-26（周一）恢复正常（第 12 次观察）**：ToolSearch 以精确名 `mcp__qq-mail__SendMessage`、`mcp__qq-mail__GetMe` 一次命中；`GetMe` 返回 scopes 含 `mail:send`、日配额 2000、单附件上限 1 MB；`SendMessage` 用标准写法（`to` 传对象数组）＋`body_format: HTML`＋`skip_confirmation: true` 直发，返回 `queued: true`、`email_sent: true`。形态序列：…→未注册(10/24)→正常(10/25)→**正常(10/26)**，为 10/16-10/18 之后**第二次出现连续两日正常**（10/26 为第 2 日），仍远低于「连续 5 个交易日正常」的升级判据，**不构成修复证据**，severity 维持 major。
- **入参体积经验（固化）**：脚本自动生成的全量 HTML 在 10/25 为 20 420 字节（过长，需重写）、紧凑版 12 045 字节可用；本期手写紧凑版 **11 447 字节 / 8 329 字符**直传入参一次成功。结论：邮件正文入参控制在 ≤12 KB 量级可稳定投递，且不必先生成全量再改写，直接按紧凑版标准生产即可。
"""

BUG012 = """

- **2026-10-26（周一）双线仍停在 10/23，休市日不计阈值**：`ls logs/ | grep inspection` 最近产出为 `2026-10-23-inspection_noon.json` 与 `2026-10-23-inspection_pm.json`（双线同日 no_action、按时点落盘）；`grep -c 2026-10-24-inspection` ＝ 0、`grep -c 2026-10-25-inspection` ＝ 0，但 10/24 为周六、10/25 为周日，均非交易日，按既有口径不计入连续零产出交易日数 → **连续零产出交易日数 0**，未达复合升级判据（连续 ≥5 个正常交易日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出），不升级不降级。今日 14:00／22:00 两条线尚未到点，待观察；观察期自 10/15 起第 11 日，仍在 2 周窗口内。
"""

BUG013 = """

- **2026-10-26（周一）第 28 次连续命中**：会话开头的 `[Buglog] 用户报告了一个 bug` 再次附上整段自动化任务提示词（以「你是金价早报自动化助手」开头、含第一至第七步流程编号、无异常现象与期望行为），按既有判据判为**任务指令而非缺陷报告**，已跳过建档；另对 `scripts/build_20261026.py`、`scripts/mail_20261026.py`、`scripts/check_briefing.py` 三个新脚本的创建做「修 bug」弱提示，实为常规迭代（新建生成／校验脚本），不计入。双重复核已执行：逐文件 `grep -c "2026-10-26"` ＋ 字节数/SHA-1 写入 `logs/2026-10-26-morning_briefing.json` 的 `buglog_verification`。
"""

TARGETS = [
    ("2026-09-08-briefing-scheduler-missed-days.md", BUG003),
    ("2026-09-14-inspection-email-connector-down.md", BUG006),
    ("2026-09-25-inspection-scheduler-silent-miss.md", BUG012),
    ("2026-09-26-buglog-hook-misfire.md", BUG013),
]

for name, text in TARGETS:
    p = os.path.join(BUGS, name)
    with io.open(p, "r", encoding="utf-8") as f:
        cur = f.read()
    if "2026-10-26" in cur:
        print("skip (already)", name)
        continue
    with io.open(p, "a", encoding="utf-8") as f:
        f.write(text)
    print("appended", name)

INDEX = os.path.join(ROOT, ".buglog", "index.md")
section = """
## 2026-10-26（周一）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 67 分钟（会话起始 10:07:17、首次 `date` 10:08:21 实测），序列 44 个日历日 …/约 39/约 46/约 100/约 67，回落至区间中位，仍属「4-152 分钟极宽摆动」；10/19-10/26 连续八个自然日、六个交易日无缺跑、无提前 |
| BUG-006 | **恢复正常（第 12 次观察）**：ToolSearch 精确名一次命中、`GetMe` 确认 `mail:send` 与配额 2000，`SendMessage` 返回 `queued: true`、`email_sent: true`；形态序列 正常(10/25)→正常(10/26)，为 10/16-10/18 后第二次连续两日正常，仍不构成修复证据。另固化「入参 ≤12 KB」经验（本期 11 447 字节） |
| BUG-012 | `inspection_noon`/`inspection_pm` 最近产出均为 10/23；10/24（周六）、10/25（周日）非交易日不计阈值，**连续零产出交易日数 0**，未达复合判据；观察期自 10/15 起第 11 日 |
| BUG-013 | 第 28 次连续命中，判误判跳过建档；附带误报为三个新脚本（build／mail／check）的正常创建；双重复核已执行 |
"""
with io.open(INDEX, "r", encoding="utf-8") as f:
    idx = f.read()
if "2026-10-26（周一）观察更新" in idx:
    print("index skip")
else:
    with io.open(INDEX, "a", encoding="utf-8") as f:
        f.write(section)
    print("index appended")

print("\n--- verification ---")
for name, _ in TARGETS:
    p = os.path.join(BUGS, name)
    with io.open(p, "r", encoding="utf-8") as f:
        s = f.read()
    b = s.encode("utf-8")
    n = s.count("2026-10-26")
    print("%s  grep_count=%d bytes=%d sha1=%s" % (name, n, len(b), hashlib.sha1(b).hexdigest()))

b = idx.encode("utf-8")
print(".buglog/index.md  grep_count=%d bytes=%d sha1=%s" % (idx.count("2026-10-26"), len(b), hashlib.sha1(b).hexdigest()))
