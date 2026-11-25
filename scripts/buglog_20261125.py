# -*- coding: utf-8 -*-
"""追加 2026-11-25 期 buglog（幂等）：新增 BUG-034 + index 段落 + stats。"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BL = ROOT / ".buglog"
BUGS = BL / "bugs"
IDX = BL / "index.md"

NEW_FILE = BUGS / "2026-11-25-fffd-gate-gap.md"
BUG034 = """---
id: BUG-034
title: 早报产物级门禁存在字形缺口，无法发现正文中的 U+FFFD 替换字符
status: open
severity: minor
source: ai-detected
reported_at: 2026-11-25T11:30:00
tags: [validation, encoding, gold-briefing]
related_bugs: [BUG-026, BUG-028, BUG-011]
---

## 早报产物级门禁存在字形缺口，无法发现正文中的 U+FFFD 替换字符

### 现象

2026-11-25 早报构建脚本 `scripts/build_20261125.py` 里，`chart.events` 第 28 条的长中文文案中出现了单字乱码：
「盘中最�3546.00」，其中「」位置是一个 U+FFFD 替换字符（写脚本时被截断/替换的「低」字）。
该乱码是在成稿前人工回读脚本源码时发现的，已用一次 Edit 修正为「盘中最低 3546.00」，产物未受影响。

### 根因分析

本项目已有三道关卡，但都不覆盖字形完整性：

1. `json.load` 只校验 JSON 语法，U+FFFD 在语法上完全合法；
2. `scripts/check_briefing.py` 的 `walk()` 只检查 ASCII 双引号、反引号、字面 `**`（BUG-009/011 的产物），
   以及 `%%` 门禁（BUG-026/028 的产物），**没有对 U+FFFD 或任何控制字符做断言**；
3. 文案字段长（本次单条 events 文案约 600 字），人眼回读时也容易漏掉一个字的位置。

即：故障类别是「非法字符」而不是「非法定界符」，而现有门禁是按「定界符」设计的，属于覆盖维度的缺口。
另外，脚本是手写长中文文案、再跑脚本产出 JSON 的工作流，乱码产生在「写脚本」这一步，一旦没被发现就会原样进产物并上站。

### 修复过程

本次为**临时规避**：靠人工回读脚本源码发现并 Edit 修正，未改校验器。
建议的彻底修复（未落地）：在 `check_briefing.py` 的 `walk()` 里增加一条断言，遍历所有字符串字段，
若包含 `\\ufffd` 或 C0/C1 控制字符（`\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f`）即报错，并打印字段路径：

```python
if "\\ufffd" in o:
    errs.append("U+FFFD in " + path)
if any(ord(c) < 32 and c not in "\\n\\t" for c in o):
    errs.append("control char in " + path)
```

### 经验教训

- 门禁的覆盖维度要按「故障类别」列清单，而不是按「历史踩过的坑」逐个补：
  目前已有「定界符类」（引号/反引号）、「格式化类」（%%）、「结构类」（index/日期对齐），
  缺「字符集类」（替换字符、控制字符、零宽字符）。建议把这三类合并成一次 `walk()` 全量断言。
- 手写长中文文案时，凡是产出后还要经过 render 的字段，优先用 `.format()`/f-string 拼短句，
  减少一次性粘贴长串的机会；写完立刻跑一次门禁，不要等自检环节。
"""


def sha1(p):
    return hashlib.sha1(Path(p).read_bytes()).hexdigest()


idx = IDX.read_text(encoding="utf-8")
if "## 2026-11-25（周三）观察更新" in idx:
    print("SKIP: 2026-11-25 section already exists")
    raise SystemExit(0)

if not NEW_FILE.exists():
    NEW_FILE.write_text(BUG034, encoding="utf-8")
    print("created", NEW_FILE.name)

section = """
## 2026-11-25（周三）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **148 分钟**（会话首次 `date` 实测 11:27:53，标称 09:00），近 7 期序列 `…/53/153/12/148`。**今日为交易日且盘中有双向行情**（07 时前后冲高 3574.84、10:05 探低 3533.67、11:27 报 3551.40），延迟窗口内的两个极值点都没抓到 → **危害 2 档（有行情且错过关键时点）**。未达 360 分钟标注门槛，按建议 ⑬ 不在顶部标延迟交付 |
| BUG-006 | **复发**（11-24 单日成功后的次日失败）。`connector-status` 显示 qq-mail 为 connected，但 `ToolSearch` 精确名检索 4 组（`mcp__qq-mail__SendMessage`、`mcp__qq-mail__ListMessages`、`mcp__qq-mail__send_mail`、`mcp__qq-mail__send_message` / `SendMail`）全部回落 `mcp__agent-mail__*`；`DeferExecuteTool mcp__qq-mail__SendMessage` 返回 `Tool "mcp__qq-mail__SendMessage" not found in the deferred tools index`；兜底 `mcp__agent-mail__GetMe` 返回 `{"status":"not_bound"}` 并提示「当前请勿重试」→ **双通道同时失效、无降级路径**，`email_sent: false`、status partial，HTML 底稿落 `.workbuddy/outbox/mail-2026-11-25-morning_briefing.html`（18 823 字节／maxline 761，零双百分号、零 CSS `width:100%`）待人工补发。形态序列：正常(11-18~11-22 五日)→未注册(11-23)→正常(11-24)→**未注册(11-25)**，隔日抖动再次出现，severity 维持 major |
| BUG-012 | 今日 `logs/2026-11-25-*` 仅早报一条，14:00/22:00 两条巡检均未到点，不判缺跑；11-24 两条巡检均正常产出（`inspection_noon` = no_action、`inspection_pm` = partial 波动型预警并送达），连续零产出交易日数 = 0，不升级不降级 |
| BUG-013 | **第 36 次连续命中**（9/26 起），hook 再次把自动化提示词全文透传为「bug 报告」→ 判误判、未按字面建档。附带弱提示一条属正常开发：`build_20261125.py` 编辑 2 次＝①修正手写文案里的 U+FFFD 乱码（另立 BUG-034）②`advice` 219→193 字压缩；另 `manifest.json` / `daily/2026-11-25.json` 各被脚本重写一次，属幂等重建，非 bug 修复 |
| BUG-030 | 本期**第四次手工规避**：`build_20261125.py` 仍手抄 `if ev["index"] - 1 < 0: continue`，并沿用 `assert labels[ev["index"]] == ev["date"]` 逐条比对兜底。建议的 `lib_chart.shift_chart()` 仍未落地 |
| BUG-032 | 维持 open。本期邮件未发出，转抄环节不存在，无一致性校验可做；底稿与实发本应同源的问题依旧，最短路径仍是「让发信工具直接吃本地底稿」，而 qq-mail 的 `SendMessage` 只吃内联 body，结构上做不到 |
| BUG-033 | 维持 open，**本期第二次未调用**：`query.py` 依赖 `requests` 缺失、`pip install requests` 因本地索引不可用而失败，且缺依赖时脚本 `exit 0`（静默降级）。本期取数仍走「新浪实时接口 + WebSearch 交叉验证」，logs step1 的 `source` 已如实写明「未假装调用」 |
| BUG-034 | **新增、open（minor）**：`check_briefing.py` 的 `walk()` 只校验 ASCII 引号/反引号/字面 `**` 与 `%%`，**不校验 U+FFFD 与控制字符**；本期构建脚本的长中文文案里出现过一处 U+FFFD（「盘中最低」的「低」被替换），靠人工回读源码发现、成稿前已修正，产物未受影响。建议在 `walk()` 内补 `\\ufffd` 与控制字符断言 |

### 本期 buglog 复核凭据（2026-11-25）

- **有新增 bug**：`bugs/2026-11-25-fffd-gate-gap.md`（BUG-034，open，minor）
- 计数取自本文件表头（写入后重读）：Open 17 / Fixed 17 / Total 34（Open 16→17、Total 33→34；无 fixed 变动）
- 幂等守卫：本脚本先检测 `## 2026-11-25` 是否已存在，存在即整体 SKIP
- 完整性：`bugs/` 目录 33 → **34** 个文件
"""

idx = idx.rstrip("\n") + "\n" + section
idx = idx.replace("Open: 16 | Fixed: 17 | Total: 33", "Open: 17 | Fixed: 17 | Total: 34", 1)
IDX.write_text(idx, encoding="utf-8")

stats = json.load(open(BL / "stats.json", encoding="utf-8"))
stats["open_count"] = 17
stats["total_count"] = 34
stats["recent_fixed"] = stats.get("recent_fixed", [])
(BL / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("buglog updated")
print("index bytes", IDX.stat().st_size, "sha1", sha1(IDX)[:12])
print("bugs count", len(list(BUGS.glob("*.md"))))
print("grep 2026-11-25 in index:", IDX.read_text(encoding="utf-8").count("2026-11-25"))
print("grep BUG-034 in index:", IDX.read_text(encoding="utf-8").count("BUG-034"))
print("stats", json.dumps({k: stats[k] for k in ("open_count", "fixed_count", "total_count")}, ensure_ascii=False))
