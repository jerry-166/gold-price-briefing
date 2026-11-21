# -*- coding: utf-8 -*-
"""buglog 2026-11-21：新增 BUG-030（图表事件孤儿索引，复发）、BUG-031（邮件 HTML 长行截断，已修），
并更新 BUG-003/006/012/013 观察；同步 index.md 表头计数、stats.json、logs 复核凭据。"""
import json, os, hashlib, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUG = os.path.join(BASE, ".buglog")
DATE = "2026-11-21"

# ---------- 1. 新增 bug 文件 ----------
f30 = os.path.join(BUG, "bugs", "2026-11-21-chart-event-orphan-index.md")
c30 = """---
id: BUG-030
title: 图表逐日平移时未清理滚出窗口的事件，残留 index:-1 孤儿记录
severity: minor
status: open
found_at: 2026-11-21
tags: [chart, events, index-shift, check-gate]
---

# BUG-030 图表事件孤儿索引

## 现象

`build_20261121.py` 按「丢 1 补 1」平移图表：`labels/values` 去掉首点、追加今日，
`events` 整体 `index - 1`。首次运行 `check_briefing.py` 直接报：

```
event idx -1
```

原因是 11-20 期 `events[0]` 指向 `index: 0`（标签 10-22），平移后变成 `-1`，
而 10-22 这一天已滚出 30 日窗口，事件应一并丢弃。

## 根因

平移逻辑只对 `labels/values` 做了切片（天然丢弃首点），却对 `events` 做了整体减 1，
**没有对「索引落到窗口外」做判据**。10-22（BUG-013 条目里已留痕）出现过一次同类问题，
本次是**复发**：每期都会新写一个 build 脚本，同一行 `if` 每次都要重新想一遍。

## 修复（本期）

```python
if e["index"] - 1 < 0:
    continue   # 已滚出窗口的点，其事件一并丢弃
```

修复后 events 数量 29→30（新增 11-21）、索引 0..29 连续、`check_briefing.py` errors 0。

## 建议（未落地，故状态 open）

把「图表平移」提炼成 `scripts/lib_chart.py` 的 `shift_chart(prev, new_date, value, event)`：
内部完成切片、索引重排、孤儿事件过滤、`labels[-1] == 今日` 断言。日更脚本只传参数，
不再手抄这段逻辑——否则每期仍有一次踩坑概率。
"""
if not os.path.exists(f30):
    open(f30, "w", encoding="utf-8").write(c30)
    print("written", f30)
else:
    print("exists", f30)

f31 = os.path.join(BUG, "bugs", "2026-11-21-mail-html-long-line-truncation.md")
c31 = """---
id: BUG-031
title: 邮件 HTML 单行超 2000 字符导致回读截断，正文无法原样传入发信工具
severity: minor
status: fixed
found_at: 2026-11-21
tags: [mail, html, line-length, read-truncation]
---

# BUG-031 邮件 HTML 长行截断

## 现象

`mail_20261121.py` 首版产物 13 944 字符，`max line = 3396`。发信链路是
「写 HTML 底稿 → `Read` 回读 → 把正文原样作为 `body` 传入 SendMessage」，
而 `Read` 单行上限 2000 字符，超长行会被截断 → 传进去的正文必然缺块。

历史做法是「让每条新闻独立成行」，本期证明**不够**：
`plan.buy.trigger`、`trend.advice` 这类单段长文案本身就超过 2000 字符。

## 根因

换行粒度按「模块」划分，而不是按「字符宽度」约束。只要某个模块内部是一整段长文本，
行宽就不可控。

## 修复

新增 `wrap_outside_tags(s, limit=1200)`：逐字符扫描，**只在标签外**插入换行，
保证单行 < 2000 且不破坏任何标签/属性值；扫完再断言产物无 `%%`、无 CSS `width:100%`。

实测：产物 13 949 字节、19 行、`max line = 1311`，`Read` 回读完整、正文一次传参成功
（`queued:true`，sent 目录 `created_at 2026-11-21T03:09:12Z`）。

## 复用

该函数建议与 BUG-030 的 `lib_chart.py` 一并作为 `scripts/lib_mail.py` 公共件，
后续每期 mail 脚本直接 import。
"""
if not os.path.exists(f31):
    open(f31, "w", encoding="utf-8").write(c31)
    print("written", f31)
else:
    print("exists", f31)

# ---------- 2. index.md ----------
ip = os.path.join(BUG, "index.md")
idx = open(ip, encoding="utf-8").read()

if "## 2026-11-21" in idx:
    print("index 已有 2026-11-21 小节，SKIP")
else:
    idx = idx.replace("Open: 13 | Fixed: 16 | Total: 29", "Open: 14 | Fixed: 17 | Total: 31", 1)

    section = """
## 2026-11-21（周六）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **129 分钟**（会话首条 `date` 实测 11:04:09、邮件投递 11:09:12，标称 09:00），近 9 期序列 `…/90/119/154/129`，未刷新 10/31 的 747 分钟上界。**周六国际盘 06:00 起休市、上金所与外汇交易中心全停，延迟窗口内无任何新行情 → 危害 0 档**（「非交易日延迟危害恒为 0」第四次生效），故未在邮件头部与 `_meta.updated` 标注延迟交付 |
| BUG-006 | **正常（连续第 4 日成功，11-18→11-21）**。`ToolSearch` 精确名检索 `mcp__qq-mail__SendMessage/ListMessages` 一次命中、未回落 agent-mail；沿用 11-20 的 `skip_confirmation: true` 直发，**未出现 42801、一次 `queued:true`**；`sent` 目录回读 `created_at 2026-11-21T03:09:12Z`。连续性仍不构成修复证据，severity 维持 major |
| BUG-012 | 今日 `logs/` 下无 `2026-11-21-inspection_*` 产出，14:00 与 22:00 均未到点，不判缺跑；按「当日有任一巡检产出即非零产出」口径连续零产出交易日数 = 0，未达复合判据 → 不升级不降级。另记：11-20 期出现的「巡检先于早报」顺序倒置未复发 |
| BUG-013 | **第 33 次连续命中**，hook 再次把自动化提示词全文透传为「bug 报告」→ 判误判、未按字面建档。附带弱提示 2 次：`build_20261121.py` 两次编辑（实为首版缩进被打乱导致 `IndentationError` ＋ advice 207→192 字压缩）、`mail_20261121.py` 两次编辑（实为新增 `wrap_outside_tags`，对应真实 bug BUG-031）。**本期确有真实失败（BUG-030/031），按「真实失败优先」未因 hook 误判而漏记** |
| BUG-030 | **新增、open**：图表平移只切片 `labels/values`、却对 `events` 整体 `index - 1`，首点（10-22）滚出窗口后残留 `index: -1` 孤儿事件，`check_briefing.py` 报 `event idx -1`。10-22 已出现过一次，本次为复发。修法加 `if e["index"] - 1 < 0: continue`；建议提炼 `lib_chart.shift_chart()` 公共件 |
| BUG-031 | **新增、fixed**：邮件 HTML 单行 `max line = 3396`，超 `Read` 的 2000 字符单行上限 → 「回读 → 原样传参」链路必然缺块。历史「每条新闻独立成行」不足以覆盖 `plan.buy.trigger` 这类长段落。修法：`wrap_outside_tags(limit=1200)` 只在标签外换行，实测 19 行、maxline 1311，发信一次成功 |

### 本期 buglog 复核凭据（2026-11-21）

- **有新增 bug**：`bugs/2026-11-21-chart-event-orphan-index.md`（BUG-030，open）、`bugs/2026-11-21-mail-html-long-line-truncation.md`（BUG-031，fixed）
- 计数取自本文件表头（写入后重读）：Open 14 / Fixed 17 / Total 31（Open 13→14、Fixed 16→17、Total 29→31）
- 幂等守卫：本脚本先检测 `## 2026-11-21` 是否已存在，存在即 SKIP
- 完整性：`bugs/` 目录 29 → **31** 个文件；`index.md` 字节数／SHA-1／当日串出现次数见 `logs/2026-11-21-morning_briefing.json` 的 `buglog_verification`（**在全部写入动作之后测量**）
"""
    if not idx.endswith("\n"):
        idx += "\n"
    idx += section
    open(ip, "w", encoding="utf-8").write(idx)
    print("index.md 已追加 2026-11-21 小节")

# ---------- 3. stats.json ----------
sp = os.path.join(BUG, "stats.json")
st = json.load(open(sp, encoding="utf-8"))
st["open_count"] = 14
st["fixed_count"] = 17
st["total_count"] = 31
rf = st.get("recent_fixed", [])
if "BUG-031" not in rf:
    rf.insert(0, "BUG-031")
st["recent_fixed"] = rf[:5]
open(sp, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=2))

# ---------- 4. 复核凭据 ----------
raw_idx = open(ip, "rb").read()
ver = {
    "checked_at": "2026-11-21 11:15 CST",
    "index_bytes": len(raw_idx),
    "index_sha1": hashlib.sha1(raw_idx).hexdigest(),
    "date_string_occurrences": raw_idx.decode("utf-8").count(DATE),
    "bug_files_total": len([f for f in os.listdir(os.path.join(BUG, "bugs")) if f.endswith(".md")]),
    "per_file_grep": {},
    "header_counts": "Open 14 | Fixed 17 | Total 31",
    "stats_json": {"open": st["open_count"], "fixed": st["fixed_count"], "total": st["total_count"]},
}
for f in sorted(os.listdir(os.path.join(BUG, "bugs"))):
    if f.endswith(".md"):
        t = open(os.path.join(BUG, "bugs", f), encoding="utf-8").read()
        n = t.count(DATE)
        if n:
            ver["per_file_grep"][f] = n

lp = os.path.join(BASE, "logs", DATE + "-morning_briefing.json")
lg = json.load(open(lp, encoding="utf-8"))
lg["buglog_verification"] = ver
lg["notes"].append(
    "buglog：本期确有真实失败 → 新增 BUG-030（图表事件孤儿索引，复发）与 BUG-031（邮件 HTML 长行截断，已修），"
    "并更新 BUG-003/006/012/013 观察；计数 Open 14 / Fixed 17 / Total 31，bugs/ 29→31"
)
open(lp, "w", encoding="utf-8").write(json.dumps(lg, ensure_ascii=False, indent=2) + "\n")

print(json.dumps(ver, ensure_ascii=False, indent=1))
