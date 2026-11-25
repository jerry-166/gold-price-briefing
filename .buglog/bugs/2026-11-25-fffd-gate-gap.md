---
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
「盘中最<U+FFFD>3546.00」（原文此处为一个 U+FFFD 替换字符），其中「」位置是一个 U+FFFD 替换字符（写脚本时被截断/替换的「低」字）。
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
若包含 `\ufffd` 或 C0/C1 控制字符（`\x00-\x08\x0b\x0c\x0e-\x1f`）即报错，并打印字段路径：

```python
if "\ufffd" in o:
    errs.append("U+FFFD in " + path)
if any(ord(c) < 32 and c not in "\n\t" for c in o):
    errs.append("control char in " + path)
```

### 经验教训

- 门禁的覆盖维度要按「故障类别」列清单，而不是按「历史踩过的坑」逐个补：
  目前已有「定界符类」（引号/反引号）、「格式化类」（%%）、「结构类」（index/日期对齐），
  缺「字符集类」（替换字符、控制字符、零宽字符）。建议把这三类合并成一次 `walk()` 全量断言。
- 手写长中文文案时，凡是产出后还要经过 render 的字段，优先用 `.format()`/f-string 拼短句，
  减少一次性粘贴长串的机会；写完立刻跑一次门禁，不要等自检环节。
