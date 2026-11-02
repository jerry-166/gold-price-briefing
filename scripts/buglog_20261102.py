# -*- coding: utf-8 -*-
"""2026-11-02 早报：buglog 追加 + 运行日志 + 日志清单。"""
import json, io, os, hashlib, subprocess, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(BASE, ".buglog", "bugs")
IDX = os.path.join(BASE, ".buglog", "index.md")
ST = os.path.join(BASE, ".buglog", "stats.json")

E003 = """
- **2026-11-02（周一）延迟约 59 分钟**：会话 `<current_time>` 实测 09:59:30，首次 `date` 09:59:35。序列续记至 9/13-11/02 共 51 个日历日：…/约 44(10/30)/约 747(10/31)/约 67(11/01)/约 59(11/02)，回落到 4-747 区间中低位，10/31 的极端值未复现（连续两日未复现）。10/19-11/02 连续十五个自然日、十一个交易日全部产出，无缺跑、无提前。**本期延迟的危害为「放大幅度型」的温和版**：09:00 准点的伦敦金约在 3881-3890（亚市刚开、贴近开盘价 3881.88），09:59 取到 3909.85，于是「涨约 0.3%」被写成「涨 0.86%」——方向没变但幅度放大约 2.8 倍，与 10/30（方向由平盘变下跌）和 10/28（方向被改变）并列，构成延迟影响的第三档「方向同、幅度放大」。
"""

E006 = """
- **2026-11-02（周一）恢复正常（第 18 次观察，连续正常 2 日）**：`GetMe` 返回 alias `2132049351@qq.com`、scopes 含 `mail:send`、日配额 2000；`SendMessage` 以 `body_format: HTML` ＋ `skip_confirmation: true` 直发，返回 `queued: true`，`email_sent: true`。正文 12 056 字符 / 17 358 字节、最长行 501 字符，一次投递无 42801 往返。**检索方式假设第二次验证成功**：本期继续只用 ToolSearch 的 `tool_names` 精确名（`mcp__qq-mail__SendMessage`、`mcp__qq-mail__GetMe`）检索，两个工具均一次命中、未出现「回落 agent-mail 命名空间」现象 → 「关键词检索拿不到 deferred tools 索引」的解释得到第 2 次正面支持（11/01、11/02 连续两期）。按判据仍需连续 ≥5 日正常才进入「疑似修复」观察，当前连续计数 2。
"""

E012 = """
- **2026-11-02（周一）**：`grep -c 2026-11-02-inspection` ＝ 0，但 14:00 与 22:00 两大触发点在本期早报执行时（10:03）均未到达，按「未到点不计异常」规则不判定缺跑。最近巡检产出仍为 `logs/2026-10-30-inspection_noon.json` 与 `2026-10-30-inspection_pm.json`（两线同日双产出）；10/31（周六）、11/01（周日）零产出属非交易日、不计阈值。连续零产出交易日数 ＝ 0，未达复合判据（连续 ≥5 日且恢复后 2 周内再现连续 ≥3 日），不升级不降级。**本期为 11/02 起新一周观察的第一天**，重点看 11/02-11/06 五个交易日的两线产出形态。
"""

E013 = """
- **2026-11-02（周一）第 35 次连续命中（9/26-11/02）**：hook 再次透传自动化任务提示词全文并声明「用户报告了一个 bug」，判误判、未按字面建档。附带误报本期两次：①`scripts/build_20261102.py` 的「2 次编辑」——实为 `trend.advice` 由 205 字压缩到 188 字（自检拦下 `advice too long: 205`，正常返工）；②`scripts/mail_20261102.py` 经 heredoc 两次改写 `width:100%%` → `width:100%`，该次确有真缺陷，已另立 **BUG-017** 单独立档，不混入本条。双重复核已执行（逐文件 `grep -c` ＋ 字节数/SHA-1 写入 logs 的 `buglog_verification`）。
"""

E017 = """---
id: BUG-017
title: 邮件 HTML 里用 % 格式化的转义双写百分号，导致表格宽度变成 width:100%%
severity: minor
status: fixed
first_seen: 2026-11-02
fixed_at: 2026-11-02
---

# BUG-017 邮件 HTML 的 CSS 百分号被双写成 %%

## 现象

2026-11-02 早报邮件底稿 `.workbuddy/outbox/2026-11-02-morning.html` 中，两处 `<table>` 的内联样式渲染为
`style="width:100%%;border-collapse:collapse;..."`，浏览器按非法值丢弃该声明，表格宽度退回 `auto`。

## 根因

`scripts/mail_20261102.py` 用列表逐段拼 HTML，其中两行写成：

```python
P.append('<table style="width:100%%;border-collapse:collapse;font-size:13px;">')
```

`%%` 是 **`%` 运算符**里的转义写法，只有在该字符串**真的被 `%` 格式化**时才会折叠成单个 `%`。
这两行**没有传格式化参数**，所以 `%%` 原样进了产物。同一脚本里其他行都带 `% (...)` 参数，`%%` 才会被正确折叠——
正因如此，肉眼看源码很难发现这两行是「多余的转义」。

## 修复

把两处改为单写 `width:100%`（这两行不做格式化，不需要转义）。已重新生成底稿并 `grep -o 'width:100[^;]*'` 验证，
输出为两条 `width:100%`。

## 教训

拼 HTML 的脚本里，**只要有一行是纯字面量、不参与 `%` 格式化，就不能沿用 `%%`**。更稳的做法是整篇改用 f-string
或 `str.format` 之外的方式（如 `"".join` ＋ 字母量），从根上避免两套转义规则混用。同类坑 10/27 已踩过一次
（`"…-0.04%…" % (...)` 抛 `ValueError: unsupported format character`），两次都是「正文含百分号」场景。

## 验证清单

- [x] 产物 `grep -c '100%%'` ＝ 0
- [x] 产物 `grep -o 'width:100[^;]*'` 输出两条 `width:100%`
- [x] 邮件 `SendMessage` 返回 `queued: true`
"""


def append(path, text):
    with io.open(path, "a", encoding="utf-8") as f:
        f.write(text)


append(os.path.join(B, "2026-09-05-briefing-scheduler-missed-days.md"), E003)
append(os.path.join(B, "2026-09-14-inspection-email-connector-down.md"), E006)
append(os.path.join(B, "2026-09-25-inspection-scheduler-silent-miss.md"), E012)
append(os.path.join(B, "2026-09-26-buglog-hook-misfire.md"), E013)
io.open(os.path.join(B, "2026-11-02-mail-html-percent-escape.md"), "w", encoding="utf-8").write(E017)

IDX_SEC = """
## 2026-11-02（周一）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | **延迟约 59 分钟**（会话 `<current_time>` 09:59:30 实测、首次 `date` 09:59:35），昨日 67 分钟延续，10/31 的 747 分钟极端值连续两日未复现。序列 51 个日历日 …/约 44(10/30)/约 747(10/31)/约 67(11/01)/约 59(11/02)。**新增危害第三档**：本期属「方向同、幅度放大」——09:00 准点约 3881-3890（贴近开盘 3881.88），09:59 取到 3909.85，「涨约 0.3%」被写成「涨 0.86%」，幅度放大约 2.8 倍；与 10/28（方向被改变）、10/30（平盘变下跌）并列 |
| BUG-006 | **恢复正常（第 18 次观察，连续正常 2 日）**：`GetMe` 正常（scopes 含 mail:send、日配额 2000）、`SendMessage` 返回 `queued: true`，`email_sent: true`，12 056 字符一次投递无 42801 往返。**「精确名检索」假设第 2 次正面验证**（11/01、11/02 连续两期均一次命中、未回落 agent-mail 命名空间），距「连续 ≥5 日」门槛仍差 3 日 |
| BUG-012 | 两线 11/02 尚未到点（14:00／22:00 均晚于本期 10:03 执行时刻），不判缺跑；最近产出仍为 10/30 两线双产出，10/31-11/01 属非交易日不计。连续零产出交易日数 0，未达复合判据。**11/02 起进入新一周观察，重点看 11/02-11/06 五个交易日的形态** |
| BUG-013 | 第 35 次连续命中，判误判跳过建档；附带误报两次：`build_20261102.py` 的 advice 205→188 字压缩（自检正常返工）、`mail_20261102.py` 的 `width:100%%` 修复（该次确有真缺陷，**已另立 BUG-017**）；双重复核已执行 |
| BUG-017 | **新增、fixed**：邮件 HTML 里两处 `<table>` 渲染为 `width:100%%`（`%` 运算符的转义写法被用在不做格式化的字面量上），浏览器丢弃该声明、表格退回 auto 宽度。已在发信前发现并修复，`grep -c '100%%'` ＝ 0、`grep -o 'width:100[^;]*'` 输出两条 `width:100%` |
"""

append(IDX, IDX_SEC)

st = json.load(io.open(ST, encoding="utf-8"))
st["open_count"] = 11
st["fixed_count"] = 6
st["total_count"] = 17
st["recent_fixed"] = ["BUG-017", "BUG-016", "BUG-010", "BUG-009"]
io.open(ST, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=2) + "\n")

# ---- 复核凭据 ----
FILES = {
    "BUG-003": os.path.join(B, "2026-09-05-briefing-scheduler-missed-days.md"),
    "BUG-006": os.path.join(B, "2026-09-14-inspection-email-connector-down.md"),
    "BUG-012": os.path.join(B, "2026-09-25-inspection-scheduler-silent-miss.md"),
    "BUG-013": os.path.join(B, "2026-09-26-buglog-hook-misfire.md"),
    "BUG-017": os.path.join(B, "2026-11-02-mail-html-percent-escape.md"),
}
ver = {}
for k, p in FILES.items():
    raw = io.open(p, encoding="utf-8").read()
    ver[k] = {
        "file": os.path.basename(p),
        "grep_c_2026_11_02": raw.count("2026-11-02"),
        "bytes": len(raw.encode("utf-8")),
        "sha1": hashlib.sha1(raw.encode("utf-8")).hexdigest(),
    }
idx_raw = io.open(IDX, encoding="utf-8").read()
ver["index.md"] = {
    "bytes": len(idx_raw.encode("utf-8")),
    "sha1": hashlib.sha1(idx_raw.encode("utf-8")).hexdigest(),
    "has_1102_section": "## 2026-11-02（周一）观察更新" in idx_raw,
    "bug017_linked": "BUG-017" in idx_raw,
}
ver["stats.json"] = json.load(io.open(ST, encoding="utf-8"))

MAIL_HTML = io.open(os.path.join(BASE, ".workbuddy", "outbox", "2026-11-02-morning.html"), encoding="utf-8").read()
ver["mail_html"] = {"chars": len(MAIL_HTML), "bytes": len(MAIL_HTML.encode("utf-8")),
                    "has_double_percent": "100%%" in MAIL_HTML}

print(json.dumps(ver, ensure_ascii=False, indent=1))
io.open(os.path.join(BASE, ".workbuddy", "tmp", "verify_20261102.json"), "w", encoding="utf-8").write(
    json.dumps(ver, ensure_ascii=False, indent=1))
