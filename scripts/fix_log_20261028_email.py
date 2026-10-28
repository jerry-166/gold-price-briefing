# -*- coding: utf-8 -*-
"""补发邮件成功后，修正 2026-10-28 早报日志与 logs/manifest.json。"""
import json, io, subprocess, hashlib, os

os.chdir(r"D:/workspace/每日金价资讯")

p = "logs/2026-10-28-morning_briefing.json"
d = json.load(open(p, encoding="utf-8"))

step5 = d["steps"][-1]
old_result = step5["result"]
step5["status"] = "success"
step5["duration_ms"] = step5["duration_ms"] + 53000
step5["result"] = (
    "已发送至 2132049351@qq.com（13:47 补发成功，SendMessage 返回 queued=true）。"
    "首轮 13:41 失败：qq-mail 连接器状态 auth-required、mcp__qq-mail__* 未注册进工具索引、"
    "agent-mail 返回 not_bound、reconnect 被拒。用户随后手动授权，13:45 工具索引恢复、"
    "GetMe 返回 alias_A9yF9wF5eP0o6Tc1uUpRq71T8H09（scopes 含 mail:send），"
    "13:46 首次调用返回 42801 需确认令牌，带 confirmation_token 重发成功。"
)
step5.setdefault("outputs", [])

d["status"] = "success"
d["summary"] = "数据、JSON、manifest、Git 全部成功；邮件首轮因连接器鉴权失败，用户授权后于 13:47 补发成功"

d["summary_stats"]["success_steps"] = 5
d["summary_stats"]["failed_steps"] = 0
d["summary_stats"]["total_duration_ms"] = d["summary_stats"]["total_duration_ms"] + 53000
d["summary_stats"]["email_sent"] = True

d["email_retry"] = {
    "first_attempt": "13:41 失败（连接器 auth-required / 工具未注册 / agent-mail not_bound / reconnect 被拒）",
    "reauthorized_by_user": "13:44 用户确认连接器已授权，13:45 状态转为 connected",
    "resend": "13:47 补发成功，SendMessage 返回 queued=true",
    "root_cause": "QQ 邮箱远程 MCP（https://api.mail.qq.com/mcp）OAuth 授权过期，需用户手动重新授权；授权后工具索引自动恢复，无需重启会话",
    "note": "首轮失败事实保留在 step5.result 与 buglog BUG-006 记录中，未删除",
}
d["step5_first_failure"] = old_result

json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("log updated:", d["status"], d["summary_stats"])

# logs/manifest.json
mp = "logs/manifest.json"
m = json.load(open(mp, encoding="utf-8"))
hit = 0
for r in m["logs"]:
    if r.get("date") == "2026-10-28" and r.get("type") == "morning_briefing":
        r["status"] = "success"
        r["summary"] = "数据/JSON/manifest/Git 全部成功；邮件首轮鉴权失败，授权后 13:47 补发成功"
        hit += 1
print("manifest patched rows:", hit)
json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
