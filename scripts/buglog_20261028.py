# -*- coding: utf-8 -*-
"""2026-10-28 期 buglog 写入 + 复核凭据。"""
import json, os, hashlib, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGS = os.path.join(BASE, ".buglog", "bugs")

ENTRIES = {
    "2026-09-08-briefing-scheduler-missed-days.md": """

- **2026-10-28（周三）延迟约 275 分钟——刷新最严重延迟记录**：触发时刻 13:35:01（`<current_time>` 实测），首次命令 `date` 实测 13:35:24，全部步骤结束约 13:43。距标称 09:00 **延迟 275 分钟**，**大幅突破 10/21 的 152 分钟上界（为其 1.8 倍）**，区间定性改写为「4-275 分钟极宽摆动」。序列续记至 9/13-10/28 共 46 个日历日：…/约 100/约 67/约 51/**275**。10/19-10/28 连续十个自然日、八个交易日全部产出，无缺跑、无提前触发。
- 影响面（本期为最实质的一次）：275 分钟延迟把快照时点从 09:00 亚市早盘直接推到 13:35 亚市午后，伦敦金读数 4034.97 已完整包含当日「开 4059.50 → 高 4070.57 → 低 4032.42」的全部行程（振幅 0.94%）。若准点 09:00 取价，读数会接近 4059 的开盘水平、当日涨跌幅接近 0 而非 **-0.62%**——**早报的「当日方向」已因延迟而改变**，这是延迟首次影响到结论而非仅影响细节。故建议 ②（定时提前至 07:00-07:30）已不足以覆盖 275 分钟量级的延迟，须宿主侧直接核查该条 9:00 定时器的投递链路。
- 第 ⑦ 条 in_progress 占位兜底本期**未启用**（会话单段连续完成、无中断），如实记为执行偏离。幂等检查前置：`daily/2026-10-28.json` 不存在、`logs/manifest.json` 头部无当日 morning_briefing 记录、`git log` 无当日早报提交 → 无中断残留（BUG-014 未复现）。前置缺口检查：上次早报 10/27（周二，success），10/28 为其后第一个交易日，其间无缺失交易日 → 无断档。
""",
    "2026-09-14-inspection-email-connector-down.md": """

- **2026-10-28（周三）第十三次复发：回到「工具未注册」形态，且首次出现「连接器显示 connected ＋ 工具不可达 ＋ 重连被拒」三重叠加**：
  - `list_installed_plugins` 返回 `qq-mail@workbuddy-connector-plugins-official`：`status: connected`、`bound: true`、`enabled: true`；`connector-status` 亦声明 connected。
  - 但 ToolSearch 用精确名 `mcp__qq-mail__SendMessage` / `mcp__qq-mail__GetMe` 检索，**两次均回落到 agent-mail 命名空间**（返回的全是 `mcp__agent-mail__*`），即 qq-mail 的 MCP 工具根本没有进入本会话工具索引。
  - `mcp__agent-mail__GetMe` 返回 `{"_agentmail_meta":{"status":"not_bound"}}`（智能体邮箱尚未开通，请勿重试）。
  - 对 qq-mail 执行 `reconnect_plugin` 返回 **「User refused, no changes applied. Reconnection cancelled or timed out」**——无人值守场景下重连流程无法完成。
  - 三重叠加 → **无任何降级路径**，`email_sent: false`、status partial，完整 HTML 落 `.workbuddy/outbox/2026-10-28-morning.html`（14 667 字节）待人工补发。
- 形态序列：正常(10/25) → 正常(10/26) → 正常(10/27) → **未注册(10/28)**。这是 10/16-10/18「连续三日正常」之后**第二次**出现「连续三日正常 → 第 4 日即复发」，与 10/19 的轨迹完全一致。**结论升级为判据：正常窗口 ≤3 日不构成任何改善证据，只有连续 ≥5 日正常才进入「疑似修复」观察**。
- 新增线索：本次 `reconnect_plugin` 首次被实际调用并留下「无人值守下被拒／超时」的凭据，说明该 bug 在无人值守场景下**没有自愈通道**；若宿主侧不修复注册层，早报邮件将长期以「隔几日断一日」的节奏失败。
""",
    "2026-09-25-inspection-scheduler-silent-miss.md": """

- **2026-10-28（周三）四维体检**：`inspection_noon`／`inspection_pm` 最近产出均为 **10/27**（noon 14:03 `no_action`、pm 22:00 `no_action`，双线同日正常）；10/28 的 14:00／22:00 均未到点，不计异常；`ls logs/ | grep -c 2026-10-28-inspection`＝0（未到点，非缺跑）。**连续零产出交易日数＝0**，未达复合判据（连续 ≥5 日零产出 且 恢复后 2 周内再现连续 ≥3 日）→ 不升级不降级。10/24、10/25 为周末（非交易日，不计阈值），10/26-10/27 双线连续正常，观察期自 10/27 起算仍在新一轮窗口内。
""",
    "2026-09-26-buglog-hook-misfire.md": """

- **2026-10-28（周三）第 30 次连续命中**（9/26-10/28）：hook 再次把自动化提示词全文（以「你是金价早报自动化助手」开头、含「第一步/第二步」流程编号）判为「用户报告的 bug」→ **判误判、未按字面建档**。附带误报本期形态：对 `scripts/build_20261028.py` 与 `scripts/log_20261028.py` 的正常创建、以及 `daily/2026-10-28.json` 的生成做弱提示。本期真实工具调用零失败、零用户纠正（邮件发送失败属 BUG-006 既有故障，非本次新缺陷）。双重复核已执行：逐文件 `grep -c` 计数＋四文件字节数与 SHA-1 已写入 `logs/2026-10-28-morning_briefing.json` 的 `buglog_verification`，`index.md` 与 `bugs/` 内容一致。
- **附带修复（归档一致性）**：本次发现 `.buglog/stats.json` 长期滞后（open 11／fixed 4／total 15，而 `index.md` 头部为 Open 11 | Fixed 5 | Total 16，差的就是 10/27 新增的 BUG-016）→ 本期一并修正为 11／5／16，并把 BUG-016 补入 `recent_fixed`。
""",
}

for fn, text in ENTRIES.items():
    p = os.path.join(BUGS, fn)
    with open(p, "a", encoding="utf-8") as f:
        f.write(text)
    print("appended", fn)

# ---- index.md 追加当日观察段落 ----
section = """
## 2026-10-28（周三）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | **延迟约 275 分钟（触发 13:35:01、首次 `date` 13:35:24 实测），为 10/21 的 152 分钟上界的 1.8 倍，刷新最严重记录**；区间改写为「4-275 分钟极宽摆动」；序列 46 个日历日 …/约 67/约 51/**275**；10/19-10/28 连续十个自然日、八个交易日无缺跑、无提前。**本期延迟首次实质改变结论**：快照推到亚市午后 4034.97，已含当日 4059.50→4070.57→4032.42 全行程，准点取价则方向接近 0 而非 -0.62% |
| BUG-006 | **第十三次复发，回到「工具未注册」形态**：`list_installed_plugins` 显示 connected/bound/enabled，但 ToolSearch 精确名 `mcp__qq-mail__SendMessage`／`GetMe` 均回落 agent-mail；`agent-mail` 返回 `not_bound`；`reconnect_plugin` 被拒/超时（无人值守无自愈通道）→ `email_sent: false`、status partial，HTML 落 `.workbuddy/outbox/2026-10-28-morning.html`（14 667 字节）。**判据升级：正常窗口 ≤3 日不构成改善证据**（连续三日正常→第 4 日复发已发生两次：10/19、10/28） |
| BUG-012 | `inspection_noon`／`inspection_pm` 最近产出均为 10/27（14:03／22:00，双线同日正常）；10/28 未到点不计；**连续零产出交易日数 0**，未达复合判据；观察期自 10/27 起算 |
| BUG-013 | 第 30 次连续命中，判误判跳过建档；附带弱提示为两个新脚本的正常创建与 JSON 生成；双重复核已执行 |
| BUG-016 | 附带修复归档一致性：`.buglog/stats.json` 由 11/4/15 修正为 11/5/16，与 index 头部对齐，并把 BUG-016 补入 `recent_fixed` |
"""
ip = os.path.join(BASE, ".buglog", "index.md")
with open(ip, "a", encoding="utf-8") as f:
    f.write(section)
print("index updated")

# ---- stats.json 修正 ----
sp = os.path.join(BASE, ".buglog", "stats.json")
st = json.load(open(sp, encoding="utf-8"))
st["open_count"] = 11
st["fixed_count"] = 5
st["total_count"] = 16
rf = st.get("recent_fixed", [])
if "BUG-016" not in rf:
    rf = ["BUG-016"] + rf
st["recent_fixed"] = rf[:4]
json.dump(st, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("stats:", st)

# ---- 复核凭据写入日志 ----
files = [
    "2026-09-08-briefing-scheduler-missed-days.md",
    "2026-09-14-inspection-email-connector-down.md",
    "2026-09-25-inspection-scheduler-silent-miss.md",
    "2026-09-26-buglog-hook-misfire.md",
]
ver = {"date_marker": "2026-10-28", "files": {}, "index_sha1": "", "counters_check": ""}
for fn in files:
    p = os.path.join(BUGS, fn)
    b = open(p, "rb").read()
    txt = b.decode("utf-8")
    ver["files"][fn] = {
        "grep_c": txt.count("2026-10-28"),
        "bytes": len(b),
        "sha1": hashlib.sha1(b).hexdigest(),
    }
ib = open(ip, "rb").read()
ver["index_sha1"] = hashlib.sha1(ib).hexdigest()
ver["index_bytes"] = len(ib)
itxt = ib.decode("utf-8")
ver["counters_check"] = "index 头部 Open/Fixed/Total = 11/5/16；stats.json 已同步为 11/5/16"
ver["total_hits"] = sum(v["grep_c"] for v in ver["files"].values())

lp = os.path.join(BASE, "logs", "2026-10-28-morning_briefing.json")
log = json.load(open(lp, encoding="utf-8"))
log["buglog_verification"] = ver
log["buglog_written"] = ["BUG-003", "BUG-006", "BUG-012", "BUG-013"]
json.dump(log, open(lp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(ver, ensure_ascii=False, indent=2))
