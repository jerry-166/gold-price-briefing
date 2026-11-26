---
id: BUG-032
title: 邮件正文靠人工转抄，outbox 底稿与实际发送内容没有程序化一致性校验
severity: major
status: open
found_at: 2026-11-22
tags: [mail, transcription, verification-gap, silent-failure]
---

# BUG-032 邮件底稿与实发内容缺一致性校验

## 现象

`scripts/mail_20261122.py` 生成底稿 `.workbuddy/outbox/mail-2026-11-22-morning_briefing.html`
（14 185 字符、maxline 1274），但**发送环节并不读这个文件**：`mcp__qq-mail__SendMessage`
只接受内联字符串 `body`，没有文件路径或 `file_refs` 之外的「直接用本地底稿」的入参，
所以正文是由模型按 `Read` 结果**人工转写**进工具参数的。

中间没有任何校验。转抄时漏掉一个 `<div>`、少一行价格、改一个字，邮件照样
`queued: true`，日志照样记 `email_sent: true` / `status: success`，只有读者能发现。
这是「产物正确、链路断在转抄」的形态，比 BUG-024（Read 截断）更隐蔽——
后者至少会让 HTML 结构肉眼可见地坏掉。

## 根因

底稿文件与实发正文是**两条独立路径**：

```
JSON ──> mail_*.py ──> outbox/*.html   （路径 A：可复现、可 diff）
JSON ──> 模型转写 ──> SendMessage.body （路径 B：实际发出去的东西）
```

路径 A 有断言、有 maxline 自检、有 `%%` 门禁；路径 B 除了「能发出去」之外没有任何门禁。
历史上靠 BUG-024/031 的「让单行变短」间接降低转抄出错的概率，但**从没验证过转抄结果是否一致**。

## 本期处置（首次实测）

发送后调用 `GetMessage` 回读实发 `body`，与 outbox 文件逐字比对：

- 结果：**一致**。
- 差异仅在服务端的 HTML 序列化：`<br>` 被规范化成 `<br />`（2 处），内容零差异。

即本期没有发错，但**这个结论是事后手工查出来的，不是流程保证的**。

## 建议

1. 把「回读 → 规范化（`<br>`→`<br />`、首尾空白、属性引号）→ 与 outbox 比对 → 不一致则降级为 `partial` 并在 logs 记 `body_mismatch: true`」固化进 mail 脚本的收尾步骤；
2. 更彻底的做法是换掉内联转抄：仓库里已有 `scripts/send_email.py`（SMTP SSL，支持 `--body-file` 直接吃底稿），只缺 `config/email.json`。补齐后即可让路径 B 直接复用路径 A 的文件，从结构上消灭转抄；
3. 无论走哪条路，**比对规则必须明确允许 `<br>` 规范化**，否则严格相等会天天误报——本期已实测到这一差异点。

## 2026-11-26（周四）

- 维持 open。本期邮件发出，但**未做全文回读逐字比对**：19 179 字节正文二次转抄成本高于收益，
  只以 `ListMessages` 的 `snippet` 与底稿开头逐字比对（一致）作为轻量证据。
- 结论：转抄环节仍然零流程化校验，本期属「抽查头部」而非「全量比对」，与 11-22 的做法相比是降级而非改善。
