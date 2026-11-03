# -*- coding: utf-8 -*-
"""2026-11-03 期 buglog 更新：逐文件追加观察条目 + 重建 index 段落 + 同步 stats。"""
import io, os, json, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGS = os.path.join(BASE, ".buglog", "bugs")

APPEND = {
    "2026-09-05-briefing-scheduler-missed-days.md": (
        "\n- **2026-11-03（周二）延迟约 81 分钟**：会话 `<current_time>` 实测 10:21:00，首次 `date` 10:21:11。"
        "序列续记至 9/13-11/03 共 52 个日历日：…/约 67(11/01)/约 59(11/02)/约 81(11/03)，"
        "落在 4-747 区间中位，10/31 的极端值连续三日未复现。10/19-11/03 连续十六个自然日、十二个交易日全部产出，"
        "无缺跑、无提前。**本期延迟危害属「平盘变微跌」档**：09:00 前后现货约 3948-3950"
        "（金投网 09:50 报 3948.52、金价查询网 08:09 报 3950.19），对应涨跌幅 +0.04% 至 +0.09%，基本平盘；"
        "10:21 取到 3944.05、-0.06%，符号由「正/零」转为「负」。与 10/30 同型（平盘变下跌）但幅度极小，"
        "对结论无影响——两个时点的判断都是「观望、别追」。\n"
    ),
    "2026-09-14-inspection-email-connector-down.md": (
        "\n- **2026-11-03（周二）正常（第 19 次观察，连续正常 3 日）**：`GetMe` 返回 alias "
        "（alias_A9yF9wF5eP0o6Tc1uUpRq71T8H09）与 scopes（alias:read / mail:read / mail:send）、日配额 2000；"
        "`SendMessage` 标准写法（`to` 传对象数组 ＋ `body_format:HTML` ＋ `skip_confirmation:true`）一次返回 "
        "`queued: true`；`ListMessages(dir=sent, limit=3)` 于 10:26:17 CST 确认入「已发送」"
        "（message_id 以 msg_oOcBSW1 开头）。`email_sent: true`。"
        "**「精确名检索」假设第 3 次正面验证**（11/01、11/02、11/03 连续三期 `ToolSearch(tool_names=[…])` "
        "均一次命中，未回落 agent-mail 命名空间），距「连续 ≥5 日」门槛还差 2 日。"
        "仍不构成修复证据——历史上 10/16-10/18 曾连续三日正常、第 4 日即复发，"
        "「最长正常窗口 3 日」已被本期追平。\n"
    ),
    "2026-09-25-inspection-scheduler-silent-miss.md": (
        "\n- **2026-11-03（周二）体检**：本期执行时刻 10:21，早于 14:00／22:00 两条巡检的触发点，不判缺跑。"
        "最近产出：`inspection_pm` 为 11/02（22:06 落盘、波动型预警、邮件已发）、"
        "`inspection_noon` 为 11/02（14:16 落盘），两条线 11/02 双产出。"
        "按「早报线有产出即当日非零产出」口径，11/03 已由本期早报构成当日产出，"
        "连续零产出交易日数 0，未达复合判据 → 不升级不降级。"
        "新一周观察（11/02-11/06）第 2 个交易日，两线均正常。\n"
    ),
    "2026-09-26-buglog-hook-misfire.md": (
        "\n- **2026-11-03 第 36 次连续命中（9/26-11/03）**：hook 再次透传自动化提示词全文 → 判误判、未按字面建档。"
        "附带误报本期形态：①对 `scripts/build_20261103.py` 的 2 次编辑弱提示为「正在修 bug」——"
        "实为生成前的两处自纠（`round(3944.05,1)` 会得 3944.0，改为字面量 3944.1；"
        "`市场still在给加息定价` 的英文词残留改为「仍在」），且发生在脚本首次运行**之前**，不属 bug 修复；"
        "②`mail_20261103.py` 的 TypeError **确为真缺陷，已另立 BUG-018**。"
        "双重复核已执行（逐文件 `grep -c` 计数 ＋ 五个 bug 文件字节数/SHA-1 写入 logs 的 `buglog_verification`）。\n"
    ),
}

for fn, text in APPEND.items():
    p = os.path.join(BUGS, fn)
    with io.open(p, "a", encoding="utf-8") as f:
        f.write(text)
    print("appended", fn)

# index.md
IDX = os.path.join(BASE, ".buglog", "index.md")
block = """
## 2026-11-03（周二）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | **延迟约 81 分钟**（`<current_time>` 10:21:00 实测、首次 `date` 10:21:11），10/31 的 747 分钟极端值连续三日未复现。序列 52 个日历日 …/约 747(10/31)/约 67(11/01)/约 59(11/02)/约 81(11/03)。**本期危害属「平盘变微跌」档**：09:00 前后约 3948-3950（+0.04%~+0.09%），10:21 取 3944.05（-0.06%），符号由正/零转负；与 10/30 同型但幅度极小，两时点结论一致（观望） |
| BUG-006 | **正常（第 19 次观察，连续正常 3 日）**：`GetMe` 正常、`SendMessage` 一次返回 `queued: true`、`ListMessages(dir=sent)` 于 10:26:17 CST 确认入已发送，`email_sent: true`。**「精确名检索」假设第 3 次正面验证**，距「连续 ≥5 日」差 2 日；仍不构成修复证据（10/16-10/18 三日正常后第 4 日即复发，最长窗口 3 日已被追平） |
| BUG-012 | 本期 10:21 执行，早于 14:00／22:00，不判缺跑。11/02 两线双产出（noon 14:16、pm 22:06 且 pm 触发波动型预警并已发信）；11/03 由早报构成当日产出，连续零产出交易日数 0，未达复合判据，不升降级。新一周观察第 2 个交易日正常 |
| BUG-013 | 第 36 次连续命中，判误判跳过建档；附带误报两次：`build_20261103.py` 生成前的两处自纠（数值取整、英文词残留）被弱提示为修 bug；`mail_20261103.py` 的 TypeError 为真缺陷，**已另立 BUG-018**。双重复核已执行 |
| BUG-018 | **新增、fixed**：往已做 `%` 格式化的 HTML 行里插入字面百分号（「微跌 0.06%」），触发 `TypeError: not enough arguments for format string`，拼邮件中断。修法改为「0.06 个百分点」，从根上不引入百分号。属 BUG-017 的反向同源缺陷（该写不写 vs 不该写却写），累计第三次踩「正文含百分号」的坑 |
"""
with io.open(IDX, "a", encoding="utf-8") as f:
    f.write(block)
print("index appended")

# stats
SP = os.path.join(BASE, ".buglog", "stats.json")
st = json.load(io.open(SP, encoding="utf-8"))
st["fixed_count"] = st.get("fixed_count", 0) + 1
st["total_count"] = st.get("total_count", 0) + 1
st["recent_fixed"] = ["BUG-018"] + [x for x in st.get("recent_fixed", []) if x != "BUG-018"][:3]
with io.open(SP, "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=2)
print("stats", st)

# verification credentials
files = [
    "2026-09-05-briefing-scheduler-missed-days.md",
    "2026-09-14-inspection-email-connector-down.md",
    "2026-09-25-inspection-scheduler-silent-miss.md",
    "2026-09-26-buglog-hook-misfire.md",
    "2026-11-03-mail-percent-literal-in-formatted-line.md",
]
out = {}
for fn in files:
    p = os.path.join(BUGS, fn)
    raw = io.open(p, "rb").read()
    txt = raw.decode("utf-8")
    out[fn] = {
        "bytes": len(raw),
        "sha1": hashlib.sha1(raw).hexdigest(),
        "grep_2026_11_03": txt.count("2026-11-03"),
        "has_bug018": ("BUG-018" in txt),
    }
print(json.dumps(out, ensure_ascii=False, indent=1))
with io.open(os.path.join(BASE, ".buglog", "_verify_20261103.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
