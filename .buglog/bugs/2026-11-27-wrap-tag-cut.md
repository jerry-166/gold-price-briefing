---
id: BUG-036
title: wrap_outside_tags 按字符数硬切，把 HTML 标签属性切断导致样式失效
severity: minor
status: fixed
found_at: 2026-11-27
tags: [mail, html, wrap, attribute-cut]
---

# BUG-036 折行函数切断标签属性

## 现象

`mail_20261127.py` 首版沿用 BUG-031 的 `wrap_outside_tags`，产物 10 636 字符、71 行、
`maxline 468`。回读时发现多处属性被切断：

```
...color:#1f2328;fo
nt-size:15px;font-weight:700...
```

即 `font-size` 被拆成 `fo` + 换行 + `nt-size`，CSS 声明失效，单元格字号回退。

## 根因

BUG-031 的修复只约束了「不要切在 `<` 或 `>` 上」，并未跟踪「当前是否位于标签内」：

```python
if len(buf) >= limit and ch not in "<>":
```

条件只看当前字符，不看扫描位置，因此切点可以落在属性值中间。BUG-031 的
`limit=1200` 恰好让切点落在 tag 内概率较低，问题被掩盖；本期按 1200 切、正文更长，就命中了。

即：**修复函数被「重新发明」时退化为字符计数版**，原始设计意图（只在标签外换行）丢失。

## 修复

改为标签内感知再切：

1. 逐行处理，只有 `len(line) > limit` 才尝试切分；
2. 扫描前 `limit` 个字符，维护 `in_tag` 状态（遇 `<` 置真、遇 `>` 置假）；
3. 仅在 `not in_tag` 且字符属于空白或中文标点（`，。、；：）」`）处记为候选切点；
4. 找不到候选切点则整行不切（宁可超长也不破坏结构）。

同时把 `limit` 从 1200 提到 1500：本期产物 `maxline 596`，根本不需要折行，
折行只在真正超长时才生效。

修复后重生成：10 628 字符、63 行、`maxline 596`，`grep -c 'fo$'` = 0，无被切断属性。

## 复用

BUG-031 建议的 `scripts/lib_mail.py` 公共件仍未落地，本期第二次「各写一份」并因此退化。
该公共件应同时固化：折行（标签内感知）、`%%` 门禁、`width:100%` 门禁、U+FFFD 与繁简门禁。
