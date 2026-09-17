---
id: BUG-006
title: 金价巡检预警邮件无法发送（mail connector 不可用）
status: open
severity: major
source: user-review
reported_at: 2026-09-14T22:05:00
---

## 金价巡检预警邮件无法发送（mail connector 不可用）

### 现象
2026-09-14 22:00 晚间巡检触发预警（XAUUSD 振幅约 2.34% 超 1.5% 阈值，status=partial），需发送预警邮件至 2132049351@qq.com。
- 调用 `mcp__agent-mail__SendMessage`（skip_confirmation=true）返回 `"Agent 邮箱尚未开通 / not_bound"`，拒绝发送。
- 改走 qq-mail MCP，但 `mcp__qq-mail__*` 工具未进入工具索引（"Still connecting; call WaitForMcpServers"），`DeferExecuteTool` 报 `"not found in the deferred tools index"`，无法发送。
最终日志如实记录"邮件发送失败，需人工补发"，git push 成功（commit 0bc4039），但收件人未收到预警。

### 根因分析
两个邮件通道在执行时刻均不可用：
1. **agent-mail connector**：connector-status 显示 connected，但用户邮箱未绑定（not_bound），SendMessage 直接拒绝。此前（9/12）依赖 agent-mail skip_confirmation 成功发送，本次绑定状态已丢失。
2. **qq-mail connector**：connector-status 显示 connected，但 MCP server 工具未加载到工具索引，DeferExecuteTool 调用即报 not found。
巡检自动化对"触发即发邮件"有硬依赖，却未做双通道可用性校验与兜底，任一通道失效即导致预警静默丢失。

### 修复过程
- 将 `inspection_pm.json` / `manifest.json` 的 summary 由原"邮件已发"更正为"邮件发送失败，需人工补发"，避免记录虚假的发送成功。
- 日志已 git push（commit 0bc4039 → master）。
- 待用户恢复任一邮件通道后人工补发预警，或在 connector 恢复后对本次巡检补发。

### 复发记录（2026-09-17 22:00）
预警再次触发（XAUUSD 振幅约 2.91% 超 1.5% 阈值，status=partial），邮件仍无法发出，复现 9/14 完全相同根因：
- `mcp__agent-mail__GetMe` 返回 `"Agent 邮箱尚未开通 / not_bound"`（connector-status 显示 connected，但账号实际未绑定）。
- qq-mail connector 在 connector-status 显示 connected，但 `mcp__qq-mail__*` 工具仍未进入工具索引（仅 `mcp__agent-mail__*` 可用），无可用发送通道。
- 结论：双邮件通道在执行时刻均不可用，与 BUG-006 根因一致，属未修复的反复故障。
- 本次处置：日志 summary 标记"⚠️预警邮件发送失败（双邮件通道不可用），需人工补发"，并回写 `alert_triggered: true`；manifest 同步记 partial。待用户恢复任一通道后人工补发 9/17 晚间预警。

### 经验教训
- 巡检自动化应在发送前探测 agent-mail / qq-mail 任一通道可用性；任一可用即发，全不可用则日志必须标记 `email_delivered: false` 而非 success，杜绝静默丢预警。
- 建议在 automation 内增加邮件发送兜底/重试与状态回写字段，避免预警漏发。
- 定期巡检 connector 绑定状态，agent-mail 解绑后需重新开通；不要假设"上次能发这次就能发"。
