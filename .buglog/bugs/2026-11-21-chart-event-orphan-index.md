---
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
