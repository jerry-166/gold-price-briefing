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

- **2026-10-12（周一）— 复发（10/10 之后第二次），形态与 10/10 完全一致**：早报第 5 步「发送邮件」**失败**，且会话开局的 `connector-status` 仍显示 agent-mail 与 qq-mail **均为 connected**（与 10/10 相同，即状态层与工具层不一致的现象稳定复现）：
  - ① `mcp__qq-mail__*` 工具**未进入会话工具索引**：先按语义检索「qq mail 发送邮件／send email QQ邮箱」，返回的 10 条结果**全部是 `mcp__agent-mail__*`**（含 SendMessage、ListMessages 等）；再按名称逐一试探 `mcp__qq-mail__SendMessage`、`mcp__qq-mail__send_message`、`mcp__qq-mail__send_email`、`mcp__qq-mail__SendEmail`、`mcp__qq-mail__send`，命中结果仍**只有 agent-mail 两个工具**，qq-mail 组完全不存在。
  - ② `mcp__agent-mail__GetMe` 直接返回「Agent 邮箱尚未开通……当前请勿重试」，`{"_agentmail_meta":{"status":"not_bound"}}` —— 与 10/6、10/10 两次的 `not_bound` 完全一致。
  - ③ 本地 SMTP 兜底（`scripts/send_email.py`）依赖 `config/email.json`，该文件不存在且被 `.gitignore` 排除，仍不可用。
  - ④ 本次处置：`logs/2026-10-12-morning_briefing.json` 记 `status: partial`、`email_sent: false`（`steps[4].status = failed`），`logs/manifest.json` 同步记 partial，**绝不写「已发送」**；邮件 HTML 已完整落盘于 `.workbuddy/outbox/2026-10-12-email.html`，**需人工补发至 2132049351@qq.com**。
  - ⑤ 形态结论更新：故障序列为「9/14、9/17 → 10/6（首次波及早报主线）→ 10/7-10/9 间歇正常三日 → **10/10、10/12 连续两次复发**」。10/7-10/9 的连续成功已可确认只是间歇期，**该 bug 已可定性为「长期未修复、间歇性可用」**，严重级维持 major。两次复发之间的间隔缩短至**一个自然日**（10/10 → 10/12，中间 10/11 为周末但当日工具可用、曾发送成功），说明可用窗口并不稳定。
  - ⑥ 建议 ⑦ 再次强化：**应在进入步骤 5 之前先做一次轻量通道探测**（例如一次 ToolSearch 语义检索），若两个通道的工具均不在索引中，直接跳过发送、立即落盘 `email_sent:false` 并生成待补发邮件文件，不在不可用通道上白耗时间（本次探测约耗 30 秒，较 10/10 的约 65 秒已因流程熟练而缩短）。

- **2026-10-14（周三）— 复发（10/10、10/12 之后第三次），形态与两次完全一致**：早报第 5 步「发送邮件」**失败**，会话开局的 `connector-status` 本次显示 **agent-mail `connected`、qq-mail `connecting`**（与 10/10、10/12 的「两条均 connected」略有差异，但结果相同——状态层与工具层依旧不一致）：
  - ① `mcp__qq-mail__*` 工具**未进入会话工具索引**：先按名称试探 `mcp__qq-mail__SendMessage`、`mcp__qq-mail__send_message`，未命中；再以「qq mail 发送邮件」「QQ邮箱 SendMessage」「mail qq connector send」「QQ邮箱 发送邮件 send mail」等关键词做语义检索，返回结果**全部是 `mcp__agent-mail__*`**（SendMessage／ReplyMessage／DeleteMessage／ForwardMessage 等），qq-mail 组完全不存在。
  - ② `mcp__agent-mail__GetMe` 直接返回「Agent 邮箱尚未开通。请引导用户在上方开通面板中完成开通……当前请勿重试」，`{"_agentmail_meta":{"status":"not_bound"}}` —— 与 10/6、10/10、10/12 三次的 `not_bound` 完全一致。
  - ③ 本次按 MCP 连接规范**首次正式发起连接请求**（`workbuddy_request_mcp_connection`，servers=[`qq-mail`]，capability＝「发送每日金价早报邮件至 2132049351@qq.com」），结果为 **`skipped`**（无人值守会话中用户未响应/未连接），符合预期——该动作在无人值守场景下不构成有效兜底，其价值在于**把「连接层不可用」这一事实显式留痕**，而非解决发送。
  - ④ 本地 SMTP 兜底（`scripts/send_email.py`）依赖 `config/email.json`，该文件不存在且被 `.gitignore` 排除，仍不可用。
  - ⑤ 本次处置：`logs/2026-10-14-morning_briefing.json` 记 `status: partial`、`email_sent: false`（`steps[4].status = failed`），`logs/manifest.json` 同步记 partial，**绝不写「已发送」**；邮件 HTML 已完整落盘于 `.workbuddy/outbox/2026-10-14-email.html`，**需人工补发至 2132049351@qq.com**。
  - ⑥ 形态结论更新：故障序列为「9/14、9/17 → 10/6（首次波及早报主线）→ **10/7-10/9 间歇正常三日** → 10/10、10/12 → **10/13 正常一日** → **10/14 复发**」。**可用窗口已缩短到「隔日可用」甚至更短**（10/13 成功、10/14 即失败），与 10/7-10/9 的「连续三日可用」形成鲜明对比，进一步确认该 bug 属**长期未修复、间歇性可用**，严重级维持 major。**「连续一次成功」与「连续三次成功」都不构成修复证据，必须逐日如实记录成败**（本次即为此结论的正面案例：10/13 成功并未延续到 10/14）。
  - ⑦ 建议 ⑦ 更新：**建议在进入步骤 5 之前，统一先做「一次 ToolSearch + 一次 `mcp__agent-mail__GetMe` 轻量探测」**；若两边都不可用，立即跳过发送、落盘 `email_sent:false` 并生成待补发邮件文件。本次该探测连同 `workbuddy_request_mcp_connection` 合计约耗 90 秒，虽较前两次略长，但**换来了「连接层不可用」的显式凭据**（此前只能记录「工具不在索引」），对后续定位宿主/连接器侧问题有价值。

  - ⑧ **2026-10-14 14:02 补记（同日重发成功）**：09:40 首次自动发送失败后，**用户在 14:02 手动触发「重新发送」**。此时会话重开，`mcp__qq-mail__SendMessage` **已正常进入工具索引**，用同一份底稿（`.workbuddy/outbox/2026-10-14-email.html`，仅把底部补发说明改为「原定 09:00 自动发送失败、14:02 手动重发」）重发成功，**服务端返回 `queued: true`**，收件人 2132049351@qq.com；`logs/2026-10-14-morning_briefing.json` 的 `status` 由 partial 修正为 success，并**保留 `steps[4].status=failed` 与新增 `resend` 字段**以留全时间线（不改写历史）。**新形态证据：同一自然日内 09:40 失败、14:02 成功——说明该故障的连接层/工具注册层在数小时内即可自行恢复，可用窗口比此前判断的更短也更随机。** 但「上午没发出」本身就是主线任务的实际损失（当日早报未能按时送达），且下次自动运行同样可能撞上不可用窗口，**BUG-006 维持 open、severity major 不变**；建议仍维持「进入步骤 5 前先探测、失败即落盘 `email_sent:false` 并生成待补发文件」的兜底流程，并在若条件允许时把「自动重试一次（间隔数小时）」列为候选改进项。


- **2026-10-15（周四）— 第五次复发，形态再次变化，故障点前移到服务端入参校验层（补记）**：早报第 5 步「发送邮件」**失败**（`logs/2026-10-15-morning_briefing.json` 记 `status: partial`、`email_sent: false`；底稿落盘 `.workbuddy/outbox/2026-10-15-email.txt`）。
  - ① **与历次的根本差异**：本次 `mcp__qq-mail__*` **已正常进入会话工具索引**（不再是「工具未注册」），工具可以取到 schema、可以调用。
  - ② **但连续三次调用均返回同一错误**：`MCP error -32602 check input schema type error field_name: to schema_type: array field_type: object`。分别尝试了「`to` 传对象数组（`[{email: ...}]`）」、「`to` 传字符串数组」、「加与不加 `skip_confirmation`」三种写法，**报错完全一致** → 判定为**服务端入参 schema 校验异常**，而非调用写法问题。
  - ③ `mcp__agent-mail__GetMe` 仍返回 **not_bound**，第二条通道依旧不可用。
  - ④ **形态结论更新**：「可用窗口」的表述已不再准确——故障形态第三次质变：`未注册`（10/6、10/10、10/12）→ `注册但服务端校验失败`（10/15）。即 **『工具在、但调用即失败』**，故障点从「工具注册层」前移到「服务端入参校验层」。severity 维持 major。
- **2026-10-16（周五）— 未复现（第二十次记录，发送一次成功）**：进入步骤 5 前按既定流程先做**通道可用性探测**——
  - ① **探测一（工具注册）**：按名称检索 `mcp__qq-mail__SendMessage` / `mcp__qq-mail__GetMe`，**两者均正常返回 schema** → 注册层通畅。
  - ② **探测二（真实调用）**：`mcp__qq-mail__GetMe` **一次成功**，返回主别名 `alias_A9yF9wF5eP0o6Tc1uUpRq71T8H09`（`2132049351@qq.com`、`is_primary: true`）、scope `alias:read / mail:read / mail:send`、rate limit（10 次/分钟、200 次/小时、日配额 2000）、附件约束（单个 1 MiB、合计 3 MiB、最多 3 个）→ **授权层与凭证层完全正常**。
  - ③ **发送结果**：`mcp__qq-mail__SendMessage` 使用**文档记载的标准写法**——`to` 为**对象数组** `[{email: 2132049351@qq.com}]`、`body_format: HTML`、`body` 为完整 HTML、`skip_confirmation: true` → **一次成功，服务端返回 `queued: true`**（`POST /v1/aliases/alias_A9yF9wF5eP0o6Tc1uUpRq71T8H09/messages/send`）。主题：`🌅 今日金价早报 | 2026年10月16日 周五`。
  - ④ **关键新证据（本 bug 迄今最有诊断价值的一条）**：**10/15 报 schema error 的那一种写法（`to` 传对象数组）在 10/16 完全可用** → 直接证明 10/15 的 `-32602` 是**服务端侧瞬时/版本性异常**，而不是「调用写法不对」。修复方向由此明确：**不需要改调用写法，需要宿主/连接器侧修复入参校验的稳定性**。同时说明「工具在、但调用即失败」这一形态的**窗口最短可至约 1 个自然日**（10/15 全天失败 → 10/16 上午即恢复）。
  - ⑤ **仍不构成修复证据**：故障序列为「10/06 → 10/07-10/09 间歇正常 → 10/10 → 10/12 → 10/13 正常 → 10/14 复发 → 10/15 复发（新形态）→ **10/16 正常**」。**「隔日可用」「连续成功」均已被反复证伪为修复证据，必须逐日如实记录成败**，severity 维持 major、status 维持 open。

- **2026-10-17（周六）— 未复现，连续第二日成功**：`mcp__qq-mail__SendMessage` 使用文档记载的标准写法（`to` 传对象数组 `[{email: 2132049351@qq.com}]`、`body_format: HTML`、`skip_confirmation: true`）**一次成功，返回 `queued: true`**（`POST /v1/aliases/alias_A9yF9wF5eP0o6Tc1uUpRq71T8H09/messages/send`）。主题：`🌅 今日金价早报 | 2026年10月17日 周六`。会话开局的 `connector-status` 显示 agent-mail 与 qq-mail 均为 **connected**，且 `mcp__qq-mail__*` 工具正常进入工具索引。
- **本期无需触发任何兜底**：未调用 `workbuddy_request_mcp_connection`、未落 `.workbuddy/outbox/` 人工补发件，`email_sent: true` 为真实发送结果。
- **仍不构成修复证据**：故障序列完整为「10/06 → 10/07-10/09 间歇正常 → 10/10 → 10/12 → 10/13 正常 → 10/14 复发 → 10/15 复发（新形态：工具在、调用即 -32602）→ 10/16 正常 → **10/17 正常**」。**「连续两次成功」在此 bug 历史上已被证伪过（10/07-10/09 曾连续三日正常，随后 10/10 即复发）**，故 severity 维持 **major**、status 维持 **open**，须逐日如实记录成败。
- 可用窗口观察：10/15 的「工具在、调用即失败」形态最短约 1 个自然日即恢复（10/16 上午），本期延续正常。**若本周内（10/19-10/23）仍连续成功，可考虑在 10/24 后再评估是否降级为 minor，但不得提前宣布修复。**

- **2026-10-18（周日）— 未复现（补记，连续第三日成功）**：`mcp__qq-mail__SendMessage` 标准写法一次成功、返回 `queued: true`。**本条为 10/19 期补记**——10/18 期只在 automation memory 与 logs 中记录了成功，未写入本文件，违反「逐日如实记录成败」的既定要求；已于 10/19 补录，使故障序列完整可追溯。
- **2026-10-19（周一）— 第六次复发，回到最初的「工具未注册」形态**：早报第 5 步「发送邮件」**失败**（`logs/2026-10-19-morning_briefing.json` 记 `status: partial`、`email_sent: false`；底稿已落盘 `.workbuddy/outbox/2026-10-19-email.html`，20 144 字节（落盘含标签换行拆分，压缩后 20 144 字节（落盘含标签换行拆分，压缩后 12 890 字节）））。
  - ① **会话开局 `connector-status` 显示 qq-mail 为 connected**，`list_installed_plugins` 返回 `qq-mail@workbuddy-connector-plugins-official`、`bound: true`、`enabled: true`、`status: connected` → **绑定层与启用层均正常**。
  - ② **但工具未进入会话索引**：按名称检索 `mcp__qq-mail__SendMessage` / `mcp__qq-mail__GetMe` 均无匹配（返回的是 agent-mail 的同名能力），直接以 `mcp__qq-mail__SendMessage` 调用返回 `Tool "mcp__qq-mail__SendMessage" not found in the deferred tools index`。又用关键词「qq_mail / 发送邮件 / QQ邮箱连接器」做三轮模糊检索，命中的全部是 agent-mail 工具 → 判定为 **MCP 工具注册层故障**，即 10/6、10/10、10/12 的原始形态，而非 10/15 的「工具在、调用即 -32602」形态。
  - ③ **第二通道同样不可用**：`mcp__agent-mail__GetMe` 返回 `Agent 邮箱尚未开通`（`_agentmail_meta.status = not_bound`）→ 双通道同时失效，无降级路径。
  - ④ **未做任何假发送**：既未改写 `email_sent`、也未用其它渠道冒充 QQ Mail 发出，HTML 底稿按既定流程落 `.workbuddy/outbox/` 待人工补发；`logs` 与 `logs/manifest` 均如实记 partial。
  - ⑤ **形态序列更新**：`未注册`（10/6、10/10、10/12）→ `注册但 -32602`（10/15）→ `正常`（10/16、10/17、10/18 连续三日）→ **`未注册`（10/19）**。**10/16-10/18 的「连续三次成功」已是本 bug 历史上最长的正常窗口，第 4 日即复发 → 再次证伪「连续成功＝修复」，severity 维持 major、status 维持 open**，并把「最长正常窗口 ≈ 3 日」写入观察基线。

**2026-10-20（周二）— 恢复正常，形态回到「一次调用即成功」**：`mcp__qq-mail__SendMessage` 经 ToolSearch 按名检索**一次命中**（既非 10/19 的「工具未注册」，亦非 10/15 的「调用即 -32602」），以标准写法（`to` 传对象数组）＋`body_format: HTML`＋`skip_confirmation: true` 直发，返回 `{"data": {"queued": true, "_hints": {...POST /v1/aliases/alias_A9yF9wF5eP0o6Tc1uUpRq71T8H09/messages/send}}}` → **邮件已入队、判定发送成功**（`email_sent: true`）；HTML 底稿同步落 `.workbuddy/outbox/2026-10-20-morning-briefing.html`（14 197 字节）留档备查。**形态序列更新**：`未注册`（10/6、10/10、10/12）→ `注册但 -32602`（10/15）→ `正常`（10/16、10/17、10/18）→ `未注册`（10/19）→ **`正常`（10/20）**。**本日成功不构成修复证据**——10/16-10/18 曾连续三日正常、第 4 日即复发已证伪一次；severity 维持 major、status 维持 open，「最长正常窗口 ≈ 3 日」观察基线维持不变，本期为复发后第 1 日恢复。

**2026-10-21（周三）— 第七次复发，回到「工具未注册」形态，双通道同时失效**：早报第 5 步「发送邮件」**失败**（`logs/2026-10-21-morning_briefing.json` 记 `status: partial`、`email_sent: false`；HTML 底稿落 `.workbuddy/outbox/2026-10-21-morning.html`，11 665 字节）。
  - ① `connector-status` 显示 qq-mail 为 connected；`list_installed_plugins` 返回 `qq-mail@workbuddy-connector-plugins-official`、`bound: true`、`enabled: true`、`status: connected` → 绑定层、启用层均正常。
  - ② 但工具未进入会话索引：以 `mcp__qq-mail__send_mail` / `mcp__qq-mail__SendMessage` / `qq_mail_send` 三个候选名做精确检索，只回落到 agent-mail 的同名能力；再以关键词「qq」「邮箱发送」做两轮模糊检索，返回 `No matching tools found` → 判定为 **MCP 工具注册层故障**（10/6、10/10、10/12、10/19 的同一形态），非 10/15 的「工具在、调用即 -32602」形态。
  - ③ 第二通道同样不可用：`mcp__agent-mail__SendMessage` 返回「Agent 邮箱尚未开通」＋ `_agentmail_meta.status = not_bound` → 双通道同时失效、无降级路径。
  - ④ 未做任何假发送：`email_sent` 保持 false，未用其它渠道冒充 QQ Mail 发出，HTML 按既定流程落 `.workbuddy/outbox/` 待人工补发。
  - ⑤ 形态序列更新：`未注册`（10/6、10/10、10/12）→ `-32602`（10/15）→ `正常`（10/16、10/17、10/18）→ `未注册`（10/19）→ `正常`（10/20）→ **`未注册`（10/21）**。10/20 的单日正常如预期未能延续，**「恢复正常」再次被证伪，severity 维持 major、status 维持 open**。
  - ⑥ 本次新增可操作线索：本会话中 agent-mail 与 qq-mail **同时**不可用，而 ToolSearch 对 qq-mail 关键词**完全没有候选返回**（连 agent-mail 都不再被模糊匹配命中），提示故障可能发生在「deferred tools 索引装载」这一更上游的位置，而非连接器本身；建议下次复现时先记录 ToolSearch 的原始返回，再判断是否值得提交宿主侧排查。
