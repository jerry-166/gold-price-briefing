# -*- coding: utf-8 -*-
"""写 logs/2026-11-04-morning_briefing.json 与 logs/manifest.json（追加头部）。"""
import json, io, re, os

DATE = "2026-11-04"
d = json.load(io.open("daily/%s.json" % DATE, encoding="utf-8"))
p = d["prices"]

lines = []
lines.append("【金价快照】")
for it in p:
    lines.append("%s %s %s（%+.2f%%）" % (it["label"], it["value"], it["unit"], it["change"]))
lines.append("")
lines.append("【昨夜到今晨的大事】")
for i, n in enumerate(d["news"], 1):
    lines.append("%d. [%s] %s" % (i, n["tag"], n["title"]))
    lines.append("   " + n["explain"])
    lines.append("   来源：%s %s" % (n["source"], n["url"]))
lines.append("")
lines.append("【趋势判断】")
t = d["trend"]
lines.append("短期：%s" % t["short"])
lines.append("中期：%s" % t["mid"])
lines.append("长期：%s" % t["long"])
lines.append("建议：%s" % t["advice"])
lines.append("")
lines.append("【什么价位买、什么价位卖】")
lines.append("买入：%s" % d["plan"]["buy"]["price"])
lines.append(d["plan"]["buy"]["trigger"])
lines.append("卖出：%s" % d["plan"]["sell"]["price"])
lines.append(d["plan"]["sell"]["trigger"])
lines.append(d["plan"]["note"])
lines.append("")
lines.append("【今日学一招】%s" % d["teach"]["title"])
lines.append(re.sub(r"<[^>]+>", " ", d["teach"]["body"]).replace("  ", " ").strip())
lines.append("")
lines.append("看板：https://jerry-166.github.io/gold-price-briefing/")
body_text = "\n".join(lines)

steps = [
    {"num": 1, "name": "获取数据", "status": "success", "duration_ms": 114000,
     "result": "伦敦金 3951.39（昨收 3930.09、高 3964.68、低 3919.85）、Au99.99 848.50（昨收 840.01）、"
               "中间价 6.7180（调贬 30 点）、离岸 6.6725、美元指数 101.36、WTI 95.53、布伦特 103.25、COMEX 12 月期金 3972.7；"
               "新闻 7 条（美军空袭格什姆岛、油价先涨后跌、JOLTS 超预期、世界黄金协会双调整、中期选举计票、德商银行看多、今日日程）",
     "source": "neodata-financial-search（未用，改走实时接口）＋ 新浪财经 hf_XAU/gds_AU9999/gds_AUTD/hf_CL/hf_OIL ＋ 东方财富 push2 ＋ WebSearch"},
    {"num": 2, "name": "生成早报JSON", "status": "success", "duration_ms": 120000,
     "result": "已写入 daily/2026-11-04.json；check_briefing.py 0 error（advice 190 字、12 组价位复算全中）；"
               "执行「昨晨快照 vs 真实收盘」四步修法：11-03 图表点 3944.1→3930.1、hero note 单列、prices[3].source 与 chart.source 各写修正句"},
    {"num": 3, "name": "更新manifest", "status": "success", "duration_ms": 18000,
     "result": "已追加 2026-11-04 记录至 manifest.json 头部，briefings 共 75 条"},
    {"num": 4, "name": "Git推送", "status": "success", "duration_ms": 15000,
     "result": "commit a93b69f 已推送（ls-remote 与 rev-parse 一致）；另追加修正提交 32a4492（油价改先涨后跌口径）"},
    {"num": 5, "name": "发送邮件", "status": "success", "duration_ms": 74000,
     "result": "已发送至 2132049351@qq.com，ListMessages(dir=sent) 于 09:53:54 CST 确认（msg_gedgfwswplVf8eci…），正文 11 081 字符 / 15 754 字节",
     "outputs": [{"label": "邮件内容", "body": body_text}]},
]

total = sum(s["duration_ms"] for s in steps)

log = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "success",
    "summary": "早报全流程 5/5 成功：伦敦金 3951.4(+0.54%)、Au99.99 848.5(+1.01%)、中间价 6.7180、积存金 853.5；已推送并完成邮件投递",
    "timestamp": "09:48 CST（触发）／09:53 CST（邮件送达）",
    "steps": steps,
    "summary_stats": {
        "total_steps": 5, "success_steps": 5, "failed_steps": 0,
        "total_duration_ms": total, "email_sent": True, "git_pushed": True,
    },
}

io.open("logs/%s-morning_briefing.json" % DATE, "w", encoding="utf-8").write(
    json.dumps(log, ensure_ascii=False, indent=2))

# logs/manifest.json 头部追加
mp = "logs/manifest.json"
m = json.load(io.open(mp, encoding="utf-8"))
item = {"date": DATE, "type": "morning_briefing", "status": "success",
        "summary": "早报 5/5 成功：3951.4(+0.54%)、Au9999 848.5、中间价 6.7180，邮件已发"}
if m["logs"][0].get("date") == DATE and m["logs"][0].get("type") == "morning_briefing":
    print("logs/manifest already has today morning, replace")
    m["logs"][0] = item
else:
    m["logs"].insert(0, item)
io.open(mp, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=2))

print("log written, total_ms", total, "body chars", len(body_text))
print("logs/manifest head", m["logs"][0])
