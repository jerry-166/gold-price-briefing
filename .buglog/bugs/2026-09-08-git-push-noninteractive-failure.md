---
id: BUG-004
title: 无人值守巡检中 git push 因凭据无法交互输入而失败
status: fixed
severity: major
source: user-review
reported_at: 2026-09-08T21:35:00
fixed_at: 2026-09-11T14:08:00+08:00
files:
  - path: .workbuddy/memory/automations/automation-1784188108172
    root_cause: "remote 为 https 协议，无人值守环境无交互凭据；9/11 午后巡检时 git 全局 insteadOf(SSH) 改写丢失，git push 再次失败"
    fix: "巡检 automation 的 push 改为显式 SSH URL（git push git@github.com:jerry-166/gold-price-briefing.git master），不再依赖 https 交互凭据；已验证成功 d73fa1b..dde2b4d"
tags: [git, automation, credentials]
---

## 无人值守巡检中 git push 因凭据无法交互输入而失败

### 现象
2026-09-08 PM 巡检自动化执行 `git push` 时报错：
`fatal: could not read Username for 'https://github.com': terminal prompts disabled`
重试后进程挂起 9 分钟无任何输出，最终被终止。本地 commit（e747514）成功，但远端 master 落后 1 个提交。

### 根因分析
remote 使用 https://github.com/... 协议，credential helper 为 `helper-selector`。无人值守（自动化/非交互 shell）环境下，helper 无法弹出凭据选择框、也无法读取终端输入，导致认证失败；重试时 git 卡在等待凭据的网络请求上。

### 修复过程
（待修复）临时处置：commit 已保留在本地，失败情况已写入 automation memory，待下次交互会话手动 push。

### 经验教训
- 自动化任务中的 git push 不应依赖交互式凭据。可选方案：
  1. remote 改为 SSH；
  2. 使用带 PAT 的 https URL（凭据存入 credential manager，非交互可读）；
  3. push 加超时与失败重试上限，失败时明确记录并在下次人工会话补偿。
- 无人值守流程应对 git push 增加显式超时（如 60s），避免整次自动化被挂起拖长。

### 补充（2026-09-08 22:00 巡检验证）
- **已验证可用绕过方案**：本沙箱环境 `ssh -o BatchMode=yes -T git@github.com` 返回 `Hi jerry-166! ... authenticated`，即 SSH 钥匙可用、已认证为仓库 owner。
- 22:00 巡检改用 `git push git@github.com:jerry-166/gold-price-briefing.git master` 直接以 SSH URL 推送，**成功**（`a7a5370..e1c94c9 master -> master`），无需改动用户本地持久 remote 配置（其仍为 https + helper-selector，在用户本机交互环境正常）。
- 结论：无人值守会话可临时用 `git push git@github.com:<owner>/<repo>.git <branch>` 走 SSH 完成推送；`git fetch origin` 后本地 origin/master 跟踪即同步。建议将「优先尝试 SSH URL 推送」写入巡检 automation 的固定流程作为兜底。

## 根因修复落实（2026-09-11 午后巡检）

- **已落实修复**：2026-09-11 14:08 推送时，发现全局 `url."git@github.com:".insteadOf` 已丢失（前次 9/10 设的 SSH 改写不再存在），plain `git push` 再次失败。重新设置 insteadOf 后推送成功；并进一步将 automation-1784188108172 的 push 命令改为**显式 SSH URL** `git push git@github.com:jerry-166/gold-price-briefing.git master`，使其不再依赖 https 交互凭据或易丢失的 insteadOf 全局配置。
- **验证**：本次午后巡检 `git add logs/ && git commit && git push <SSH URL>` 成功（`d73fa1b..dde2b4d master -> master`）。早报 automation 此前已用 SSH URL 推送成功，故两类推送均不再受 https 凭据阻塞。
- **经验**：无人值守 push 必须自检鉴权方式；insteadOf 全局配置在沙箱中不保证跨会话持久，应把 SSH URL 直接写进 automation 的 push 命令作为最稳方案。
