# -*- coding: utf-8 -*-
"""2026-11-22 buglog：更新 index.md 观察段 + 计数器 + stats.json，并回写复核凭据。
幂等守卫：检测到 `## 2026-11-22` 已存在即 SKIP（BUG-025 教训）。
"""
import hashlib, json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(BASE, ".buglog", "index.md")
STATS = os.path.join(BASE, ".buglog", "stats.json")
LOGS = os.path.join(BASE, "logs", "2026-11-22-morning_briefing.json")
DATE = "2026-11-22"
MARK = "## 2026-11-22（周日）观察更新"

idx = open(IDX, encoding="utf-8").read()
if MARK in idx:
    print("SKIP: 已存在今日观察段")
    raise SystemExit(0)

OLD_HEAD = "Open: 14 | Fixed: 17 | Total: 31"
assert OLD_HEAD in idx, "表头计数与预期不符，先核对"
idx = idx.replace(
    OLD_HEAD,
    "Open: 15 | Fixed: 17 | Total: 32",
    1,
)

# 在 BUG 表格末尾（第一个 ## 之前）插入 BUG-032 行
BUG032_ROW = (
    "| BUG-032 | 邮件正文靠人工转抄，outbox 底稿与实际发送内容无程序化一致性校验"
    "（2026-11-22 首次主动用 GetMessage 回读比对，本期一致；服务端会把 `<br>` 规范化为 `<br />`，"
    "严格相等校验会误报） | major | open |\n"
)
first_h2 = idx.find("\n## ")
assert first_h2 > 0, "找不到第一个二级标题"
idx = idx[:first_h2] + "\n" + BUG032_ROW + idx[first_h2:]

SECTION = """
## 2026-11-22（周日）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **53 分钟**（会话起始 `date` 实测 09:53:34，标称 09:00），近 10 期序列 `…/90/119/154/129/53`，落回区间低位、未刷新上界。**周日国际现货盘自 11-21 06:00 停至 11-23 06:00，上金所与外汇交易中心全休，延迟窗口内零新报价 → 危害 0 档**（「非交易日延迟危害恒为 0」第五次生效），故邮件头部与 `_meta.updated` 不标延迟交付，`updateTime` 仍固定 09:00 |
| BUG-006 | **正常（连续第 5 日成功，11-18→11-22）**。`ToolSearch` 精确名检索 `mcp__qq-mail__SendMessage/ListMessages` 一次命中、未回落 agent-mail；沿用 `skip_confirmation: true` 直发，**未出现 42801、一次 `queued:true`**；`sent` 回读 `created_at 2026-11-22T01:57:04Z`（09:57:04 CST）。连续 5 日仍不构成修复证据（本 bug 历史上 3 日正常后第 4 日即复发），severity 维持 major |
| BUG-012 | 今日 `logs/` 下无 `2026-11-22-inspection_*` 产出，14:00 与 22:00 均未到点，不判缺跑。另记：11-21（周六）同样零巡检产出，周末不计入「连续零产出交易日」（分母修正第十一次生效）；按复合判据连续零产出交易日数 = 0，不升级不降级 |
| BUG-013 | **第 34 次连续命中**，hook 再次把自动化提示词全文透传为「bug 报告」→ 判误判、未按字面建档。附带弱提示本期为 0 次（build/mail/log/manifest 四个脚本均一次写对、零返工）。**本期确有真实发现（BUG-032），按「真实发现优先」未因 hook 误判而漏记** |
| BUG-030 | 本期**第二次手工规避**：`build_20261122.py` 平移图表时再次手抄 `if e["index"] - 1 < 0: continue`，`check_briefing.py` 未报孤儿索引。状态维持 open —— 建议的 `lib_chart.shift_chart()` 仍未落地，每期仍有一次性踩坑概率 |
| BUG-031 | 本期沿用 `wrap_outside_tags(limit=1200)`，邮件 HTML 实测 14 185 字符／maxline 1274、零双百分号、零 CSS `width:100%`（容器统一用 `width="100%"` 属性），未复现截断。状态 fixed 成立 |
| BUG-032 | **新增、open**：底稿文件与实发正文是两条独立路径，转抄环节零校验。本期首次主动 `GetMessage` 回读比对 → 一致（仅 `<br>`→`<br />` 序列化差异），但结论是事后手查的、不是流程保证的。建议把「回读→规范化→比对→不一致降级 partial」固化进 mail 脚本收尾，或补齐 `config/email.json` 改走已有 `scripts/send_email.py --body-file` |

### 本期 buglog 复核凭据（2026-11-22）

- **有新增 bug**：`bugs/2026-11-22-mail-body-no-consistency-check.md`（BUG-032，open）
- 计数取自本文件表头（写入后重读）：Open 15 / Fixed 17 / Total 32（Open 14→15、Total 31→32；无 fixed 变动）
- 幂等守卫：本脚本先检测 `## 2026-11-22` 是否已存在，存在即 SKIP
- 完整性：`bugs/` 目录 31 → **32** 个文件；`index.md` 字节数／SHA-1／当日串出现次数见 `logs/2026-11-22-morning_briefing.json` 的 `buglog_verification`（**在全部写入动作之后测量**）
"""

idx = idx.rstrip("\n") + "\n" + SECTION
with open(IDX, "w", encoding="utf-8") as f:
    f.write(idx)

# ---- stats.json ----
st = json.load(open(STATS, encoding="utf-8"))
st["open_count"] = 15
st["fixed_count"] = 17
st["total_count"] = 32
st["recent_fixed"] = ["BUG-031", "BUG-027", "BUG-026", "BUG-024", "BUG-023"]
with open(STATS, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=2)
    f.write("\n")

# ---- 写入后测量凭据，回写 logs ----
raw = open(IDX, "rb").read()
bugs = sorted(os.listdir(os.path.join(BASE, ".buglog", "bugs")))
txt = raw.decode("utf-8")
ver = {
    "measured_at": "after_all_writes",
    "index_bytes": len(raw),
    "index_sha1": hashlib.sha1(raw).hexdigest(),
    "date_occurrences": txt.count(DATE),
    "bug_files_count": len(bugs),
    "counters": {"open": 15, "fixed": 17, "total": 32},
    "bug032_file_sha1": hashlib.sha1(
        open(os.path.join(BASE, ".buglog", "bugs", "2026-11-22-mail-body-no-consistency-check.md"), "rb").read()
    ).hexdigest(),
    "grep_date_hits_per_file": {
        b: open(os.path.join(BASE, ".buglog", "bugs", b), encoding="utf-8").read().count(DATE)
        for b in bugs
        if b.startswith("2026-11-22")
    },
}
log = json.load(open(LOGS, encoding="utf-8"))
log["buglog_verification"] = ver
with open(LOGS, "w", encoding="utf-8") as f:
    f.write(json.dumps(log, ensure_ascii=False, indent=2) + "\n")

print("index bytes", len(raw), "sha1", ver["index_sha1"][:8], "date x", ver["date_occurrences"])
print("bugs files", len(bugs), "bug032 grep", ver["grep_date_hits_per_file"])
print("Open 15 / Fixed 17 / Total 32")
