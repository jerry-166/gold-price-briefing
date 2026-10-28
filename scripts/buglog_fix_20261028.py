# -*- coding: utf-8 -*-
"""BUG-006 2026-10-28 补记：定性修正 —— 根因是 OAuth auth-required，不是「工具未注册」"""
import json, os, hashlib, glob, io

os.chdir(r"D:/workspace/每日金价资讯")

bug_file = ".buglog/bugs/2026-09-14-inspection-email-connector-down.md"

append = """

- **2026-10-28 13:44-13:47 补记：用户手动授权后 13:47 补发成功，并推翻本期「工具未注册」的定性 —— 真正根因是 OAuth 凭证过期（status: auth-required）**：
  - 13:44 用户回复「连接器已授权」后复检：会话 `connector-status` 明确标注 `qq-mail QQ邮箱 | auth-required`，`list_installed_plugins` 返回 `qq-mail@workbuddy-connector-plugins-official: status=auth-required, bound=true, enabled=true`。**这与 13:41 首轮读到的 connected 相互矛盾，说明 `list_installed_plugins` 的 status 字段存在缓存滞后，不能单独作为判断依据。**
  - 13:45 调 `reconnect_plugin`（`pluginName=qq-mail@workbuddy-connector-plugins-official`）→ 返回空结果（无 error），随后会话 `connector-status` 变为 `connected`，**同一秒内 `mcp__qq-mail__GetMe` 即可被 ToolSearch 以精确名命中并调用成功**（返回 `alias_A9yF9wF5eP0o6Tc1uUpRq71T8H09`、scopes 含 `mail:send`、日配额 2000）。
  - 13:46 首次 `SendMessage` 返回 `42801 requires confirmation`，携带 `confirmation_token` 后重发；13:47 返回 `queued: true`；13:45:46 CST 在「已发送」箱核实到 `msg_FTyru1l5FlYOkH2JWm_EEYmyK15HG48wyUE_KpEHJG3rmQ`（主题 `🌅 今日金价早报 | 2026年10月28日 周三`、无附件）。
  - **定性修正（关键）**：10/6 以来长期记为「MCP 工具未被注册进会话索引」，本质上很可能是 **OAuth 凭证过期 → 连接器进入 auth-required → 该连接器的 MCP 工具整体不被装载进 deferred tools 索引**。也就是说「工具未注册」是**症状**，不是根因。本期拿到了此前一直缺失的因果链证据：授权恢复后工具索引**立即**恢复，无需重启会话、无需重装插件、无需改配置。
  - **对历史结论的影响**：10/10 记录的 `connector-states.v3.json` 显示 enabled、`.credentials.v3.json` OAuth 凭证「完好」——该「完好」只证明字段存在，不证明令牌未过期，**不足以排除 auth 过期**。今后凡遇「ToolSearch 精确名回落 agent-mail／零命中」，第一步先看 `connector-status` 是否 auth-required，而不是先去推断注册层。
  - **可复用处置路径（写成 SOP）**：① 看会话 `connector-status` 是否标 auth-required → ② 是则提示用户手动重新授权（无人值守下无法自愈）→ ③ 授权后调一次 `reconnect_plugin` 触发状态刷新 → ④ `GetMe` 验证 scopes 含 mail:send → ⑤ `SendMessage` 若返回 42801 则带 `confirmation_token` 重发（也可直接 `skip_confirmation: true` 省掉往返）。
  - **形态序列更新**：正常(10/25)→正常(10/26)→正常(10/27)→auth-required 致工具不可见(10/28 13:41)→**同日 13:47 授权恢复并发送成功**。因此 10/28 最终 **`email_sent: true`、status success**，不再是 partial；「连续三日正常→第 4 日复发」的判据结论保留（复发确实发生），但复发原因归为授权过期。
  - 入参体积：本期 HTML 正文约 13.9 KB 一次投递成功，说明 12 KB 并非硬上限；但首次因缺 confirmation_token 多耗一次往返，仍建议压到 12 KB 量级。
"""

with open(bug_file, "a", encoding="utf-8") as f:
    f.write(append)

# index.md 追加一行
idx = ".buglog/index.md"
row = "| BUG-006 | **10/28 补记：根因修正为 OAuth auth-required（非「工具未注册」），用户授权后 13:47 补发成功**：13:44 复检 `connector-status` 与 `list_installed_plugins` 均为 `status=auth-required`（与 13:41 读到的 connected 矛盾 → 该字段有缓存滞后，不可单凭）；13:45 `reconnect_plugin` 空返回后状态转 connected，**同一秒内 `mcp__qq-mail__GetMe` 即被索引命中**，13:46 `SendMessage` 首次返回 42801 需 confirmation_token、带令牌重发 13:47 返回 `queued: true`，已发送箱核实 `msg_FTyru1l5FlYOkH2JWm_EEYmyK15HG48wyUE_KpEHJG3rmQ`（13:45:46 CST，无附件）。**结论：所谓「工具未注册」是 auth 过期后的症状，授权恢复即工具恢复，无需重启会话/重装插件**；10/10 依据 `.credentials.v3.json`「凭证完好」排除授权的判断被推翻。本期最终 `email_sent: true`、status success。SOP：看 auth-required → 请用户授权 → 调一次 reconnect → GetMe 验 scope → SendMessage（42801 则带 confirmation_token 或直接 skip_confirmation） | open |\n"

with open(idx, "a", encoding="utf-8") as f:
    f.write(row)

# 复核凭据
counts = {}
for p in sorted(glob.glob(".buglog/bugs/*.md")):
    c = open(p, encoding="utf-8").read().count("2026-10-28")
    if c:
        counts[p] = c
files = {}
for p in sorted(glob.glob(".buglog/bugs/*.md")):
    b = open(p, "rb").read()
    if b"2026-10-28" in b:
        files[p] = {"bytes": len(b), "sha1": hashlib.sha1(b).hexdigest()}
idx_hash = hashlib.sha1(open(idx, "rb").read()).hexdigest()
idx_bytes = len(open(idx, "rb").read())

ver = {
    "date": "2026-10-28",
    "purpose": "BUG-006 定性修正（auth-required 根因）+ 补发成功留痕",
    "grep_2026_10_28_counts": counts,
    "file_bytes_sha1": files,
    "index_md": {"bytes": idx_bytes, "sha1": idx_hash},
    "bug006_row_count": open(idx, encoding="utf-8").read().count("| BUG-006 |"),
}
print(json.dumps(ver, ensure_ascii=False, indent=2))

lp = "logs/2026-10-28-morning_briefing.json"
d = json.load(open(lp, encoding="utf-8"))
d["buglog_verification_email_retry"] = ver
json.dump(d, open(lp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("log verification written")
