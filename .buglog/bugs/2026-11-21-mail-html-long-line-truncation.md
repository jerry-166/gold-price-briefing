---
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
