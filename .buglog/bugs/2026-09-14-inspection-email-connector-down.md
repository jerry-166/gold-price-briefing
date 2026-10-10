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

### 复发记录（2026-10-06 早报，首次波及主线任务）
早报邮件（收件人 2132049351@qq.com）发送失败，根因与 9/14、9/17 完全一致，**但这是第一次落在「每日唯一必发邮件」的主线任务上**（此前两次都只影响巡检预警）：
- `mcp__agent-mail__GetMe` / `ListMessages` 返回「Agent 邮箱尚未开通 / not_bound」（connector-status 仍显示 connected，账号实际未绑定）。
- `mcp__qq-mail__*` 工具未进入工具索引：逐一试探 `mcp__qq-mail__GetMe`、`mcp__qq-mail__ListMessages`、`mcp__qqmail__ListMessages` 三个候选名，`DeferExecuteTool` 均报 `not found in the deferred tools index`；`ToolSearch` 以 mail / 邮箱 / email 为关键词检索，只返回 `mcp__agent-mail__*` 一组，**qq-mail MCP 工具在本会话中完全不存在**。
- 环境线索：本机 `~/.workbuddy` 下 `.skill-list-cache.json`、`.legacy-localstorage-migration.done`、`.playwright-driver-node-reuse.done` 的时间戳均为 **2026-10-06 11:46**，与早报会话被中断的时刻重合，推测**应用在 11:46 前后完成了一次版本更新/重启，可能重置了邮箱绑定状态、并导致 qq-mail 的 MCP 工具未能重新注册**（与 BUG-014 同源）。
- 本次处置：`logs/2026-10-06-morning_briefing.json` 记 `status: partial`、`email_sent: false`，`logs/manifest.json` 同步记 partial，**绝不写「已发送」**；今日早报邮件需人工补发。
- 结论：**双邮件通道的环境级不可用已从「巡检偶发」升级为「跨任务、跨场景的常态」**（9/14、9/17、10/6 三次复现）。任务侧兜底只有「如实记 false + 明示人工补发」；根治需在连接器侧重新完成 agent-mail 绑定，或让 qq-mail 的 MCP server 重新注册工具。
- **2026-10-07（周三）— 本期未复现（正向记录）**：会话开局时 `connector-status` 显示 agent-mail 与 qq-mail **均为 connected**；步骤 5 用 QQ Mail `SendMessage`（`body_format=HTML`、`skip_confirmation=true`）一次发送成功，返回 `queued:true`，日志记 `email_sent: true`。**该次成功发生在 10/6 应用更新（11:46）重启之后的次日，说明「工具未注册」并非永久性损坏——支持前述「更新/重启导致绑定或 MCP 工具临时丢失」的推断；但仍须继续逐日观察，不因此判定已修复。**
- **2026-10-08（周四）— 本期未复现（连续第二日）**：开局 `connector-status` 同样显示 agent-mail 与 qq-mail 均为 connected；步骤 5 通过 `ToolSearch` 一次即取到 `mcp__qq-mail__SendMessage` 的工具 schema（**未再出现 10/6 那种「三个候选名逐一试探均 not found」的情况**），`body_format=HTML` + `skip_confirmation=true` 直接发送成功、返回 `queued:true`，日志记 `email_sent: true`、`git_pushed: true`。**这是 9/14 以来该问题首次出现「连续两日未复现」**，与 10/7 合并观察，10/6 的应用更新所致损坏可初步判定为**已自愈**；但鉴于该 bug 曾在「偶发—复发—常态」之间反复，**仍建议继续逐日留痕至 10/14 之后再决定是否降级**。
- **2026-10-09（周五）— 本期未复现（连续第三日；补记）**：会话开局 `connector-status` 同样显示 agent-mail 与 qq-mail 均为 connected，步骤 5 通过 QQ Mail `SendMessage`（`body_format=HTML`、`skip_confirmation=true`）一次发送成功、返回 `queued:true`，日志记 `email_sent: true`。（**本条为事后补记**：10/9 期实际未在本文件落盘，见下述 10/10 复发的第 ⑥ 点。）

- **2026-10-10（周六）— 双通道同时失效，复发并再次波及主线任务（10/6 以来首次）**：早报第 5 步「发送邮件」**失败**，根因与 9/14、9/17、10/6 三次完全一致：
  - ① `mcp__agent-mail__SendMessage` / `ListMessages` 返回「**Agent 邮箱尚未开通 / not_bound**」（`{"_agentmail_meta":{"status":"not_bound"}}`），而会话开局的 connector-status 仍显示 agent-mail **connected**。
  - ② `mcp__qq-mail__*` 工具**未进入本次会话的工具索引**：按名称逐一试探 `mcp__qq-mail__SendMessage`、`mcp__qq-mail__send_message`、`mcp__qq-mail__send_email`、`mcp__qq-mail__SendEmail`、`mcp__qq-mail__send_mail` 均无命中；以「发送邮件／邮箱／mail」为关键词做检索，返回的 10 条结果**全部是 `mcp__agent-mail__*`**，qq-mail 组完全不存在。
  - ③ **与前三期不同的新线索：连接器侧状态其实是「正常」的。** 直接检查本机连接器状态文件可见 `connector-states.v3.json` 中 `qq-mail` 属于 `enabled` 且 `userDisabled=false`；`.credentials.v3.json` 中该账号的 OAuth 凭证**仍存在且可用**（serverName `qq-mail`、serverUrl `https://api.mail.qq.com/mcp`、scope 含 `alias:read mail:read mail:send`、`accessTokenRecoverable: true`）。也就是说，**故障点不在「账号绑定」或「授权」，而在「MCP 工具未被注册进会话工具索引」这一层**——这修正了 10/6 期「更新/重启重置了绑定状态」的推断：绑定与授权自 10/6 起从未丢失，丢的是工具注册。
  - ④ 本地 SMTP 兜底通道亦不可用：项目 `scripts/send_email.py` 依赖 `config/email.json`，该文件既不存在、又被 `.gitignore` 排除（从未入库），故无第三条通道。
  - ⑤ 本次处置：`logs/2026-10-10-morning_briefing.json` 记 `status: partial`、`email_sent: false`（steps[4].status = failed），`logs/manifest.json` 同步记 partial，**绝不写「已发送」**；邮件 HTML 已完整备好落盘于 `.workbuddy/outbox/2026-10-10-email.html`，**需人工补发至 2132049351@qq.com**。
  - ⑥ **「10/6 的应用更新所致损坏已自愈」的初步判定被推翻**。10/7-10/9 连续三日成功只是间歇期；该故障的形态为「**偶发→复发→常态→间歇→复发**」，属**长期未修复**，严重级维持 major。另须留痕：**10/9 期的本文件（BUG-006）与 BUG-012、BUG-013 三处 buglog 更新均未实际落盘**，仅 BUG-003 写入成功——即「buglog 声明与产物脱节」再次发生，10/9 日志 notes ⑩ 声称已用 `grep` 复核落盘但实证为空（详见 BUG-013 附项）。
  - ⑦ 新增建议：**自动化应在进入步骤 5 之前先做一次通道可用性探测**（例如一次轻量工具检索），若两个通道的工具均不在索引中，则直接跳过发送、立即落盘 `email_sent:false` 并生成待补发邮件文件，避免在不可用通道上白耗时间（本次通道排查耗去约 65 秒）。根治仍需宿主/连接器侧修复 qq-mail MCP server 的工具注册——可向维护方反馈：**connector 状态显示 connected、OAuth scope 齐全，但工具未进入 agent 工具索引**。
