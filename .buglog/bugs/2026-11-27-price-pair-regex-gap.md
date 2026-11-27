---
id: BUG-037
title: check_briefing 的价位配对正则不认「（积存金约 X-Y 元/克）」写法，复算校验被静默跳过
severity: minor
status: open
found_at: 2026-11-27
tags: [check, regex, price-pair, silent-skip]
---

# BUG-037 价位配对正则漏匹配

## 现象

`daily/2026-11-27.json` 首轮自检报：

```
advice len = 193 | rate = 6.7075 | pairs = 4
errors: 1
  - paired 价位 too few: 4
```

但文案里实际有 6 组「美元区间（约 ¥区间 元/克）」，只认出 4 组。

## 根因

`scripts/check_briefing.py` 第 104 行：

```python
pairs = re.findall(r"(\d{3,4})-(\d{3,4})[^（(0-9]{0,10}[（(]\s*约?\s*(\d{3})-(\d{3})\s*元/克[）)]", blob)
```

`[（(]\s*约?\s*` 要求左右括号后紧跟（或只跟空白后的）「约」字。本期 `plan.buy.price`
写作 `3570-3590 美元/盎司（积存金约 770-774 元/克）`，括号与「约」之间多了「积存金」三字
→ 该组不匹配。`plan.sell.price` 同理。

## 危害

表面只是「pairs 少于 5」这条计数报错，容易当成阈值问题去凑数；**真正的风险是反向的**：
只要把 `plan.price` 改写成带前缀的句式，`plan.buy.price` 里的价位就完全逃过校验，
即使美元价与 ¥/克折算对不上也会 `errors: 0` 通过 —— 约束静默失效。

本期处置是改文案（`（约 770-774 元/克，积存金口径同此）`）绕过，未动校验脚本。

## 待修

把正则改为「括号后允许任意非数字前缀」：

```python
r"(\d{3,4})-(\d{3,4})[^（(0-9]{0,10}[（(][^0-9（）()]{0,8}(\d{3})-(\d{3})\s*元/克[）)]"
```

并补一条自检：`plan.buy.price` / `plan.sell.price` 中的每组价位都必须出现在 `pairs` 里，
否则直接报「价位未被复算」而非仅报组数不足。
