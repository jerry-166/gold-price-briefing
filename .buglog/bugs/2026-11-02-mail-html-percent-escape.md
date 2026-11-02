---
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
