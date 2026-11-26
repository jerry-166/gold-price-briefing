# -*- coding: utf-8 -*-
"""写入 2026-11-26 期 buglog（新增 BUG-035，更新 003/006/012/013/030/032/033/034）。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUGS = ROOT / ".buglog" / "bugs"
IDX = ROOT / ".buglog" / "index.md"
STATS = ROOT / ".buglog" / "stats.json"
LOGDIR = ROOT / "logs"

BEFORE = len(list(BUGS.glob("*.md")))

BUG_FILES = {
    "BUG-003": BUGS / "2026-09-08-briefing-scheduler-missed-days.md",
    "BUG-006": BUGS / "2026-09-14-inspection-email-connector-down.md",
    "BUG-012": BUGS / "2026-09-25-inspection-scheduler-silent-miss.md",
    "BUG-013": BUGS / "2026-09-26-buglog-hook-misfire.md",
    "BUG-030": BUGS / "2026-11-21-chart-event-orphan-index.md",
    "BUG-032": BUGS / "2026-11-22-mail-body-no-consistency-check.md",
    "BUG-033": BUGS / "2026-11-23-neodata-skill-blocked.md",
}

# ---------- 新增 bug 文件：BUG-035 ----------
NEW_BUG = BUGS / "2026-11-26-traditional-chars-gate-gap.md"
NEW_BUG.write_text(
    """# BUG-035：`check_briefing.py` 不校验繁简混用，手写长文案里的繁体字只能靠人工回读发现

- **日期**：2026-11-26
- **严重度**：minor
- **状态**：open
- **发现场景**：11-26 早报（`scripts/build_20261126.py` 构建 `daily/2026-11-26.json` 与邮件底稿）

## 现象

本期 `news[5].explain`（今日日程条目）手写文案里出现「也**別**在薄盘里挂市价单」——「別」是繁体字，
简体应为「别」。`check_briefing.py` 报 `errors: 0`、`build_20261126.py` 内建的 `walk()` 断言（ASCII 引号／反引号／
字面 `**`）与 `%%` 门禁、U+FFFD 断言全部通过，漏检的是「字符集正确性」这一维度。
最终由人工逐行回读邮件底稿时发现，`sed` 替换后重建、重生成底稿、补一个修正提交（cd8aa50）才收口。

## 根因

现有三道门禁各自覆盖的维度：

| 门禁 | 覆盖 | 不覆盖 |
|---|---|---|
| `check_briefing.py` 的 `walk()` | ASCII 直双引号、反引号、字面 `**` | 繁简混用、U+FFFD、控制字符 |
| 构建脚本 `raw.count("%%") == 0` | 双百分号（BUG-026/028） | 同上 |
| 构建脚本 `assert "\\ufffd" not in raw`（本期新增，BUG-034 的局部规避） | U+FFFD | 繁简混用 |

即：字形层面的错误（繁体字、异体字、全角半角混用）完全没有自动化拦截，只能靠人眼。
而本项目的文案是每期手写的长中文段落（note／explain／teach／advice），正是繁简混用的高发区
——尤其「別／别」「後／后」「裡／里」「着／著」这类输入法联想容易带出的字。

## 修复建议

在 `check_briefing.py` 的 `walk()` 里增加一个**常用繁体字黑名单**断言（成本最低、误报最低）：

```python
TRAD = "別後裡來說時對開關實現點為與這個們還過發現經濟國價漲跌週年華東車馬長門問間"
for ch in TRAD:
    if ch in s:
        bad.append(f"traditional char {ch!r} in {path}")
```

更彻底的方案是引入 `opencc`（简繁转换）对整串做 `t2s` 后比对，不一致即报错；
但该项目无第三方依赖预算（参见 BUG-033 的 `requests` 教训），黑名单法更契合。

## 影响

- 产物层面：11-26 期的繁体字已修正，站点与邮件最终内容正确，无读者可见影响。
- 流程层面：多消耗一次「重建 + 重生成底稿 + 追加提交」的返工，且修正提交已推送到远端、历史留下两条 commit。

## 关联

- BUG-034（U+FFFD 门禁缺口）：同一类问题——字形层面的错误没有自动化门禁，都靠人工回读兜住。
- 两期连续出现同类问题（11-25 的 U+FFFD、11-26 的繁体字），说明「人工回读」这条兜底正在被高频依赖，
  应当合并成一个「字符集门禁」一并补齐。
""",
    encoding="utf-8",
)

# ---------- 更新既有 bug 文件 ----------
def append(path, text):
    old = path.read_text(encoding="utf-8")
    marker = text.strip().split("\n")[0].strip()
    if marker in old:
        return False
    path.write_text(old.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")
    return True


append(BUG_FILES["BUG-003"], """
## 2026-11-26（周四）

- 延迟约 **108 分钟**（会话首次 `date` 实测 10:48:23，标称 09:00）；近 8 期序列 `…/153/12/148/108`。
- **今日为交易日且有行情**：隔夜 PCE 后砸到 3426.64、今晨拉回并冲高 3607.02，09:00-10:46 之间错过的最大区间约 56 美元（3551.13→3607.02）→ **危害 2 档**。
- 未达 360 分钟标注门槛，按建议 ⑬ 不在邮件头部标延迟；`updateTime` 仍 09:00、`_meta.updated` 写真实 10:52。
""")

append(BUG_FILES["BUG-006"], """
## 2026-11-26（周四）

- **正常**。`ToolSearch` 以精确名 `mcp__qq-mail__SendMessage` 一次命中（未回落 agent-mail），
  `DeferExecuteTool` 携 `skip_confirmation: true` 首次调用即 `queued: true`，未出现 42801 确认链路。
- `ListMessages(dir=sent)` 回读 `created_at` 2026-11-26T02:52:57Z（10:52:57 CST），主题与 snippet 头部一致。
- 形态序列：正常(11-24)→未注册(11-25)→**正常(11-26)**，隔日抖动第 4 次出现，不构成修复证据，severity 维持 major。
""")

append(BUG_FILES["BUG-012"], """
## 2026-11-26（周四）

- 今日 `logs/2026-11-26-*` 仅早报一条（本脚本执行时 14:00/22:00 两条巡检均未到点），不判缺跑。
- 11-25 两条巡检均正常产出，连续零产出交易日数 = 0，不升级不降级。
""")

append(BUG_FILES["BUG-013"], """
## 2026-11-26（周四）

- **第 37 次连续命中**（9/26 起）：hook 再次把自动化提示词全文透传为「bug 报告」→ 判误判、未按字面建档。
- 附带弱提示两条均属正常开发返工：①`scripts/build_20261126.py` 编辑 3 次＝修 `labels[0]` 断言位置（切片后判据写错）
  ＋`advice` 209→190 字压缩＋繁简混用修正（另立 BUG-035）；②`scripts/mail_20261126.py` 编辑 2 次＝替换日期与导语。
- 本期无「工具失败计数虚报」，hook 只报了编辑次数。
""")

append(BUG_FILES["BUG-030"], """
## 2026-11-26（周四）

- 本期**第五次手工规避**：`build_20261126.py` 仍手抄 `if ev["index"] - 1 < 0: continue`，
  并沿用 `assert labels[ev["index"]] == ev["date"]` 逐条比对兜底，另加 `assert len(events) == 30`、`events[-1]["index"] == 29`。
- 建议的 `lib_chart.shift_chart()` 仍未落地，第 5 次记账。
""")

append(BUG_FILES["BUG-032"], """
## 2026-11-26（周四）

- 维持 open。本期邮件发出，但**未做全文回读逐字比对**：19 179 字节正文二次转抄成本高于收益，
  只以 `ListMessages` 的 `snippet` 与底稿开头逐字比对（一致）作为轻量证据。
- 结论：转抄环节仍然零流程化校验，本期属「抽查头部」而非「全量比对」，与 11-22 的做法相比是降级而非改善。
""")

append(BUG_FILES["BUG-033"], """
## 2026-11-26（周四）

- 维持 open，**本期第三次实测仍未调用成功**：`query.py "伦敦金现货价格XAUUSD最新价"` 输出「需要安装 requests」后 `exit 0`；
  `python -c "import requests"` 仍 ImportError。
- 本期取数改走「新浪实时接口 hf_XAU/gds_AU9999/gds_AUTD ＋ 东方财富 push2 ＋ WebSearch 交叉验证」，
  logs step1 的 `source` 已如实写明「未假装调用」。
""")

append(BUGS / "2026-11-25-fffd-gate-gap.md", """
## 2026-11-26 复检（BUG-034）

- 本期在 `build_20261126.py` 内**已内置** `assert "\\ufffd" not in raw`，属局部规避第 1 次，产物零 U+FFFD。
- 但 `check_briefing.py` 的 `walk()` **仍未补** U+FFFD／控制字符断言 → 约束只存在于单个 build 脚本里，
  下一个不抄这行断言的脚本仍会漏。建议与 BUG-035 一并合并为「字符集门禁」补进 `walk()`。维持 open。
""")

# ---------- 更新 index.md ----------
idx = IDX.read_text(encoding="utf-8")
assert "## 2026-11-26" not in idx, "already written"

idx = idx.replace("Open: 17 | Fixed: 17 | Total: 34", "Open: 18 | Fixed: 17 | Total: 35", 1)

new_row = (
    "| BUG-035 | **新增、open（minor）**：`check_briefing.py` 不校验繁简混用。本期 `news[5].explain` 手写文案出现「別」（应为「别」），"
    "`check_briefing.py` 报 `errors: 0`、build 脚本的 `walk()`／`%%` 门禁／U+FFFD 断言全部通过，字形维度零拦截，靠人工回读底稿发现后 `sed` 修正"
    "（追加提交 cd8aa50）。与 BUG-034 同属「字形层面没有自动化门禁」，建议合并补一个字符集门禁（常用繁体字黑名单，或 `opencc t2s` 不一致即报错；"
    "按 BUG-033 教训不建议引入第三方依赖） | minor | open |"
)
anchor = "| BUG-034 |"
pos = idx.index(anchor)
end = idx.index("\n", pos)
idx = idx[:end + 1] + new_row + "\n" + idx[end + 1:]

NOW = len(list(BUGS.glob("*.md")))
section = """
---

## 2026-11-26（周四）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **108 分钟**（会话首次 `date` 实测 10:48:23，标称 09:00），近 8 期序列 `…/53/153/12/148/108`。**今日为交易日且盘中有双向行情**（隔夜 PCE 后砸到 3426.64、今晨拉回并冲高 3607.02），09:00-10:46 之间错过的最大区间约 56 美元 → **危害 2 档**。未达 360 分钟标注门槛，按建议 ⑬ 不在顶部标延迟 |
| BUG-006 | **正常**。`ToolSearch` 精确名 `mcp__qq-mail__SendMessage` 一次命中（未回落 agent-mail），`DeferExecuteTool` 携 `skip_confirmation: true` 首次调用即 `queued: true`，未出现 42801；`ListMessages(dir=sent)` 回读 `created_at` 10:52:57 CST 一致。形态序列：正常(11-24)→未注册(11-25)→**正常(11-26)**，隔日抖动第 4 次，不构成修复证据 |
| BUG-012 | 今日 `logs/2026-11-26-*` 仅早报一条，14:00/22:00 巡检未到点，不判缺跑；11-25 两条巡检均正常，连续零产出交易日数 = 0，不升级不降级 |
| BUG-013 | **第 37 次连续命中**（9/26 起），hook 再次把自动化提示词全文透传为「bug 报告」→ 判误判、未按字面建档。附带弱提示两条属正常返工：`build_20261126.py` 编辑 3 次（`labels[0]` 断言位置、`advice` 209→190 字、繁简修正另立 BUG-035）、`mail_20261126.py` 编辑 2 次（日期与导语替换） |
| BUG-030 | 本期**第五次手工规避**：仍手抄 `if ev["index"] - 1 < 0: continue`，另加 `assert len(events) == 30`、`events[-1]["index"] == 29`、逐条 `labels[ev["index"]] == ev["date"]`。`lib_chart.shift_chart()` 仍未落地 |
| BUG-032 | 维持 open。本期邮件发出，但**未做全文回读逐字比对**：19 179 字节正文二次转抄成本高于收益，只以 `snippet` 与底稿开头比对（一致）作轻量证据 → 相比 11-22 的全文比对是降级而非改善 |
| BUG-033 | 维持 open，**本期第三次实测仍未成功**：`query.py` 报「需要安装 requests」后 `exit 0`，`import requests` 仍 ImportError。取数改走新浪实时接口＋东财 push2＋WebSearch，logs step1 已如实写明「未假装调用」 |
| BUG-034 | 维持 open。本期 `build_20261126.py` 已内置 `assert "\\ufffd" not in raw`（局部规避第 1 次、产物零 U+FFFD），但 `check_briefing.py` 的 `walk()` 仍未补 → 约束只存在于单个脚本里 |
| BUG-035 | **新增、open（minor）**：`check_briefing.py` 不校验繁简混用。本期手写文案出现「別」（应为「别」），三道门禁全过、靠人工回读底稿发现，`sed` 修正后追加提交 cd8aa50。建议与 BUG-034 合并为「字符集门禁」 |

### 本期 buglog 复核凭据（2026-11-26）

- **有新增 bug**：`bugs/2026-11-26-traditional-chars-gate-gap.md`（BUG-035，open，minor）
- 计数取自本文件表头（写入后重读）：Open 18 / Fixed 17 / Total 35（Open 17→18、Total 34→35；无 fixed 变动）
- 幂等守卫：本脚本先检测 `## 2026-11-26` 是否已存在，存在即整体 SKIP
- 完整性：`bugs/` 目录 %d → **%d** 个文件
""" % (BEFORE, NOW)

# 复核凭据：逐文件 grep -c 计数 + 字节数/SHA-1（BUG-013 双重复核要求）
verif = {"date": "2026-11-26", "bugs_count_before": BEFORE, "bugs_count_after": NOW, "files": {}}
for name, path in list(BUG_FILES.items()) + [("BUG-034", BUGS / "2026-11-25-fffd-gate-gap.md"),
                                             ("BUG-035", NEW_BUG)]:
    data = path.read_bytes()
    verif["files"][name] = {
        "file": path.name,
        "bytes": len(data),
        "sha1": hashlib.sha1(data).hexdigest(),
        "hits_2026_11_26": data.decode("utf-8").count("2026-11-26"),
    }

IDX.write_text(idx + section, encoding="utf-8")

stats = json.loads(STATS.read_text(encoding="utf-8"))
stats["open_count"] = 18
stats["fixed_count"] = 17
stats["total_count"] = 35
STATS.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 追加到当日日志（buglog_verification 字段）
logp = LOGDIR / "2026-11-26-morning_briefing.json"
log = json.loads(logp.read_text(encoding="utf-8"))
verif["index_bytes"] = len(IDX.read_bytes())
verif["index_sha1"] = hashlib.sha1(IDX.read_bytes()).hexdigest()
verif["counts"] = {"open": 18, "fixed": 17, "total": 35}
log["buglog_verification"] = verif
logp.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

# 结论自检：index 的 BUG-035 行与 bugs/ 实际内容是否一致
assert "BUG-035" in IDX.read_text(encoding="utf-8")
assert "2026-11-26" in NEW_BUG.read_text(encoding="utf-8")
print("bugs dir:", BEFORE, "->", NOW)
print("counts: Open 18 / Fixed 17 / Total 35")
for k, v in verif["files"].items():
    print(f"  {k}: {v['file']} {v['bytes']}B sha1={v['sha1'][:12]} hits={v['hits_2026_11_26']}")
