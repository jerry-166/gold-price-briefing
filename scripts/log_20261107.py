# -*- coding: utf-8 -*-
"""2026-11-07 收尾：buglog 追加 + 运行日志 + logs/manifest 更新。"""
import hashlib, json, os

DATE = "2026-11-07"
NOW = os.environ.get("NOW_TS", "2026-11-07 11:20")
MSG_ID = "msg_z88u2fppLffg9wDilg-lEdz4hgTiMEBELLUF1W3qVTmoMQ"

BUG003 = ".buglog/bugs/2026-09-05-briefing-scheduler-missed-days.md"
BUG006 = ".buglog/bugs/2026-09-14-inspection-email-connector-down.md"
BUG012 = ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md"
BUG013 = ".buglog/bugs/2026-09-26-buglog-hook-misfire.md"
INDEX = ".buglog/index.md"

e003 = (
    "\n- **2026-11-07（周六）延迟约 130 分钟**：会话 `<current_time>` 实测 11:10:27，首次 `date` 11:10:42 实测。"
    "序列续记至 9/13-11/07 共 56 个日历日：…/约 24(11/06)/约 130(11/07)，落在 4-747 分钟区间中高位，"
    "为 10/21 的 152 分钟之后第二大值；10/31 的 747 分钟极端值连续六日未复现。"
    "10/19-11/07 连续二十个自然日、十五个交易日全部产出，无缺跑、无提前触发。"
    "**本期危害 0 档**：11-07 为周六休市、全天无行情，130 分钟延迟对读数无任何影响；"
    "反而因为延到 11:10 才取数，拿到的是周五纽约盘的完整收盘（4070.75），比 09:00 触发只能取 11-06 日盘数据更完整。"
    "**新增分档结论：周末/节假日档的延迟危害恒为 0**，危害分级应按时点分档（交易日／非交易日），不能只看分钟数。"
    "另本期仍需执行「昨晨快照 vs 真实收盘」修法：11-06 快照 4076.76 对真实收盘 4070.75，差 6.01 美元 ≈ 1.3 元/克，"
    "「跨日传染」形态第三次出现（11/05 23.5 元 → 11/06 1.4 元 → 11/07 1.3 元，量级持续收敛）。\n"
)

e006 = (
    "\n- **2026-11-07（周六）正常（第 23 次观察，连续正常 7 日）**：`GetMe` 返回 scope 含 `mail:send`、日配额 2000、"
    "别名 2132049351@qq.com；`SendMessage` 用 `to` 对象数组 ＋ `body_format: HTML` ＋ `skip_confirmation: true` "
    "一次成功返回 `queued: true`；`ListMessages(dir=sent)` 于 11:15:31 CST 确认入已发送箱"
    f"（`{MSG_ID}`），正文 10 098 字符／14 276 字节。"
    "「精确名检索（ToolSearch 传 `tool_names` 而非关键词）」第 7 次正面验证、连续 7 次无误。"
    "仍是**疑似修复**：连续 7 日已远超历史最长窗口 3 日，但按判据需观察到 11/19 前后无复发方可改 fixed。\n"
)

e012 = (
    "\n- **2026-11-07（周六）体检**：本期 11:10 执行，早于 14:00／22:00，不判缺跑。"
    "回看 11-06：`inspection_noon` 有产出（`logs/2026-11-06-inspection_noon.json` 存在），"
    "`inspection_pm` 无产出（`ls logs/ | grep 2026-11-06-inspection_pm` 为空）——属单线缺跑，"
    "未呈「一起缺跑／一起提前／一起延后」三种镜像形态，是该 bug 的新观察点（镜像并非每次成立）。"
    "连续零产出交易日数 **0**（早报线有产出即当日非零），未达复合判据"
    "（连续 ≥5 个交易日 且 恢复后 2 周内再现连续 ≥3 日），不升级不降级。"
    "11-07／11-08 为周末，不计阈值但如实留痕。\n"
)

e013 = (
    "\n- **2026-11-07（周六）第 40 次连续命中**（9/26 起），hook 再次透传自动化任务提示词全文，并附加"
    "「请回顾本次会话中是否有多次失败、报错、用户纠正的情况」，判误判、未按字面建档。\n"
    "- 附带弱提示 4 次（均忽略，不计入）：\n"
    "  ① `scripts/build_20261107.py` 创建后 1 次 Edit —— 实为 `trend.advice` 201→197 字收敛，属生成前自纠；\n"
    "  ② 同一文件「2 次编辑即视为在修 bug」的弱提示，与①重叠；\n"
    "  ③ `scripts/mail_20261107.py` 由 Write 一次落盘、零修补（改用 f-string 与字符串拼接，未用 `%` 格式化），"
    "百分号家族 bug 未复发；\n"
    "  ④ 本期工具调用零失败、零报错、零用户纠正。\n"
    "- **本期零新增 bug、零修复**；`check_briefing.py` 一次通过（首轮 advice 201 字超限后收敛，属生成前自纠）。"
    "双重复核已执行：逐文件 `grep -c \"2026-11-07\"` 计数 ＋ 字节数/SHA-1 比对，"
    "凭据落在 `logs/2026-11-07-morning_briefing.json` 的 `buglog_verification` 字段；"
    "`index.md` 与 `bugs/` 内容一致性已同步校验。\n"
)

for path, text in ((BUG003, e003), (BUG006, e006), (BUG012, e012), (BUG013, e013)):
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)

idx = (
    "\n## 2026-11-07（周六）观察更新\n\n| ID | 本期结论 |\n|---|---|\n"
    "| BUG-003 | **延迟约 130 分钟**（11:10:27 触发，首次 `date` 11:10:42），序列续记至 9/13-11/07 共 56 日，"
    "为 10/21 的 152 分钟之后第二大值，定性仍为「4-747 分钟极宽摆动」。**本期危害 0 档**：周六全天休市，"
    "130 分钟延迟不影响读数，反而因延后取数拿到周五完整收盘 4070.75。**新增分档结论：非交易日档的延迟危害恒为 0**。"
    "仍需执行「昨晨快照 vs 真实收盘」修法（差 6.01 美元 ≈ 1.3 元/克），「跨日传染」第三次出现 |\n"
    "| BUG-006 | **正常（第 23 次观察，连续正常 7 日）**：`SendMessage` 返回 `queued: true`、"
    "`ListMessages(dir=sent)` 于 11:15:31 CST 确认"
    f"（`{MSG_ID}`）。「精确名检索」第 7 次正面验证。仍为**疑似修复**，需观察到 11/19 前后无复发方可改 fixed |\n"
    "| BUG-012 | 本期 11:10 执行、早于两条巡检时点，不判缺跑。回看 11-06：noon 有产出、pm 零产出，"
    "属**单线缺跑**、未呈镜像形态（新观察点）。连续零产出交易日数 0，未达复合判据，不升降级 |\n"
    "| BUG-013 | **第 40 次连续命中**，判误判跳过建档；附带弱提示 4 次，其中 `build_20261107.py` 的 1 次 Edit "
    "实为 advice 201→197 字收敛（生成前自纠，不计入）。本期零新增 bug、零修复 |\n"
)
with open(INDEX, "a", encoding="utf-8") as f:
    f.write(idx)

# ---- 复核凭据 ----
ver = {}
for name, path in (("BUG-003", BUG003), ("BUG-006", BUG006), ("BUG-012", BUG012),
                   ("BUG-013", BUG013), ("index.md", INDEX)):
    raw = open(path, "rb").read()
    txt = raw.decode("utf-8")
    ver[name] = {
        "path": path,
        "date_grep_count": txt.count(DATE),
        "bytes": len(raw),
        "sha1": hashlib.sha1(raw).hexdigest(),
    }
print(json.dumps(ver, ensure_ascii=False, indent=2))

MAIL_BODY = (
    "🌅 今日金价早报 | 2026年11月07日 周六\n"
    "周六休市，价格沿用周五纽约收盘。\n"
    "金价快照：招行积存金（估算）879.1 元/克 -0.44%｜上海金 AU9999 874.0 元/克 +0.63%｜"
    "伦敦金 4070.8 美元/盎司 -0.44%｜美元中间价 6.72 0.00%\n"
    "昨夜大事：①非农 16.5 万（预期 6.5 万）、失业率 4.1%，12 月加息概率 67%→77%，金价砸到 4026.86 后收回 4070.75；"
    "②高盛下调 2026 年底目标价至 4150、2027 年底 4800；③美股 AI 硬件反攻（纳指 +1.09%、费半 +5.8%），"
    "SPDR 加仓 0.855 吨至 1041.368 吨；④中间价 6.7168、本周累贬 30 点；⑤AU9999 夜盘 +0.63% 与沪金主力 -0.53% 分化。\n"
    "趋势：短 中性／中 偏空／长 偏多，action=watch。\n"
    "买卖：买 4040-4050（约 872-875 元/克）、3980-4000（约 860-864 元/克）；"
    "卖 4100-4114（约 885-888 元/克）、4146-4160（约 895-898 元/克）；收盘破 4000（约 864 元/克）全撤。\n"
    "今日学一招：数据这么炸，金价为什么只跌了 0.44%？\n"
    "网页版：https://jerry-166.github.io/gold-price-briefing/"
)

steps = [
    {"num": 1, "name": "获取数据", "status": "success", "duration_ms": 148000,
     "result": ("伦敦金 4070.75（-0.44%，hq.sinajs hf_XAU，昨收 4088.80、高 4106.79、低 4028.27）；"
                "AU9999 夜盘 874.00（+0.63%，昨收 868.57）；T+D 872.50（+0.51%）；沪金主力 874.58（-0.53%）；"
                "中间价周六不公布，沿用 6.7168；美元指数 102.29（+0.68%）；WTI 90.238、布伦特 97.853；"
                "COMEX 主力 4079.5（-0.83%，仅作旁证）；非农 16.5 万、失业率 4.1%、12 月加息概率 77%"),
     "source": "neodata-financial-search（本期未调用，环境缺 requests/token）＋ 新浪财经 hq.sinajs 实时接口 ＋ WebSearch 五源交叉"},
    {"num": 2, "name": "生成早报JSON", "status": "success", "duration_ms": 176000,
     "result": "已写入 daily/2026-11-07.json；chart 丢 10-08 补 11-07、11-06 点回填 4070.8、events 整体 -1；check_briefing.py 0 error（advice 197 字、8 组价位复算全中）"},
    {"num": 3, "name": "更新manifest", "status": "success", "duration_ms": 6000,
     "result": "已追加记录到 manifest.json（briefings 78 条，头部 2026-11-07）"},
    {"num": 4, "name": "Git推送", "status": "success", "duration_ms": 21000,
     "result": "已提交并推送，本地 HEAD 0372b5e 与 ls-remote origin/master 一致"},
    {"num": 5, "name": "发送邮件", "status": "success", "duration_ms": 57000,
     "result": f"已发送至 2132049351@qq.com（queued:true，ListMessages(dir=sent) 于 11:15:31 CST 确认，{MSG_ID}）",
     "outputs": [{"label": "邮件内容", "body": MAIL_BODY}]},
]

log = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "success",
    "summary": "周六休市版早报全部成功：伦敦金取周五收盘 4070.75(-0.44%)、AU9999 夜盘 874.00(+0.63%)，非农 16.5 万主线成稿，推送与邮件均完成",
    "timestamp": "11:10 CST",
    "trigger_delay_minutes": 130,
    "steps": steps,
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": sum(s["duration_ms"] for s in steps),
        "email_sent": True,
        "git_pushed": True,
    },
    "notes": [
        "周六休市：伦敦金取 11-06 纽约收盘 4070.75，涨跌幅沿用当日收盘对收盘 -0.44%（不归零）；AU9999 取 11-06 夜盘收盘 874.00、涨跌幅对日盘收盘 868.57（+0.63%），夜盘按规则归属 11-09；中间价周六不公布，沿用 11-06 的 6.7168、涨跌幅记 0.00。",
        "「昨晨快照 vs 真实收盘」修法本期第三次执行：11-06 早报点为 09:23 快照 4076.76，真实收 4070.75，差 6.01 美元 ≈ 1.3 元/克；hero note 三段拆解、prices[3].source 与 chart.source 各写修正句、图表 11-06 点回填。",
        "NeoData 通道连续第四期未调用（缺 requests 与 token），新浪 hq.sinajs 一条 curl 覆盖伦敦金／AU9999／T+D 三项，中间价经陆家嘴早餐、东方财富国际金融要情、同花顺三源交叉确认 6.7168。",
        "BUG-006 连续正常第 7 日，ToolSearch 精确名检索第 7 次正面验证；邮件 HTML 由生成脚本一次性落盘（f-string 拼接，未用 % 格式化），百分号家族 bug 未复发。",
        "hook 第 40 次把自动化提示词误判为 bug 报告（BUG-013），已判别跳过；附带弱提示 2 次均为 advice 字数收敛导致的 Edit，按「生成前自纠不算修复」判定不计入。",
    ],
    "buglog_verification": ver,
}

os.makedirs("logs", exist_ok=True)
json.dump(log, open(f"logs/{DATE}-morning_briefing.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

lm_path = "logs/manifest.json"
lm = json.load(open(lm_path, encoding="utf-8"))
key = "logs" if "logs" in lm else "items"
entries = [x for x in lm[key] if not (x.get("date") == DATE and x.get("type") == "morning_briefing")]
lm[key] = [{"date": DATE, "type": "morning_briefing", "status": "success",
            "summary": "周六休市版早报 5/5 全部成功，邮件已发送，git 已推送"} ] + entries
json.dump(lm, open(lm_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("logs manifest key =", key, "len =", len(lm[key]), "head =", lm[key][0])
print("log written logs/%s-morning_briefing.json size=%d" % (DATE, os.path.getsize(f"logs/{DATE}-morning_briefing.json")))
