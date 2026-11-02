# -*- coding: utf-8 -*-
"""写 2026-11-02 早报运行日志 + 日志清单。"""
import json, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(io.open(os.path.join(BASE, "daily", "2026-11-02.json"), encoding="utf-8"))
ver = json.load(io.open(os.path.join(BASE, ".workbuddy", "tmp", "verify_20261102.json"), encoding="utf-8"))

# 邮件正文（纯文本摘要，用于日志留档）
L = []
L.append("今日金价早报 · 2026年11月2日 周一")
L.append("")
L.append("【金价快照】")
for pr in d["prices"]:
    L.append("%s：%s %s（%+.2f%%）" % (pr["label"], pr["value"], pr["unit"], pr["change"]))
L.append("")
L.append("【昨夜与今晨大事】")
for i, n in enumerate(d["news"], 1):
    L.append("%d. [%s] %s" % (i, n["tag"], n["title"]))
    L.append("   " + n["explain"])
    L.append("   来源：%s %s" % (n["source"], n["url"]))
L.append("")
L.append("【趋势判断】短期 %d / 中期 %d / 长期 %d，建议 %s" % (
    d["trend"]["shortVal"], d["trend"]["midVal"], d["trend"]["longVal"], d["trend"]["action"]))
L.append(d["trend"]["advice"])
L.append("")
L.append("【买卖时机】")
L.append("买入：" + d["plan"]["buy"]["price"])
L.append(d["plan"]["buy"]["trigger"])
L.append("卖出：" + d["plan"]["sell"]["price"])
L.append(d["plan"]["sell"]["trigger"])
L.append("提示：" + d["plan"]["note"])
L.append("")
L.append("【今日学一招】" + d["teach"]["title"])
import re
for i, it in enumerate(re.findall(r"<li>(.*?)</li>", d["teach"]["body"], re.S), 1):
    L.append("%d. %s" % (i, it))
L.append("")
L.append("完整日报与 30 天走势图：https://jerry-166.github.io/gold-price-briefing/")
MAIL_TEXT = "\n".join(L)

STEPS = [
    (1, "获取数据", "success", 78000,
     "伦敦金 3909.85 美元/盎司（+0.86%，09:59 亚市实时）、上海金 AU9999 837.89 元/克（-1.97%）、"
     "人民币中间价 6.7146（较 10-30 调低 8 个基点）、积存金估算 844.1 元/克；另取 6 条新闻："
     "伊朗『两天计划』、油价跳水＋OPEC+ 12 月不增产、12 月加息定价 72%、AI 股灾流动性挤兑复盘、"
     "本周日程（中期选举＋非农＋冬令时）、中间价结束连升＋央行隔夜逆回购转主",
     "新浪财经 hf_XAU / gds_AU9999 实时接口（neodata-financial-search skill 本期未装载，按项目既定替代路径取数）＋ WebSearch 六轮交叉"),
    (2, "生成早报JSON", "success", 90000,
     "已写入 daily/2026-11-02.json；check_briefing.py 首次拦下 advice too long: 205，压缩至 188 字后二次运行 0 error、"
     "11 组价位复算全中、chart 30 点 / 30 events 齐整（丢 10-03 补 11-02）"),
    (3, "更新manifest", "success", 6000,
     "已追加记录到 manifest.json，briefings 头部为 2026-11-02，共 73 条（含去重保护）"),
    (4, "Git推送", "success", 26000,
     "commit 82599e9（每日早报 2026-11-02），SSH 推送 d15c5b3..82599e9，rev-parse 与 ls-remote 一致"),
    (5, "发送邮件", "success", 76000,
     "已发送至 2132049351@qq.com，SendMessage 返回 queued:true；正文 HTML 12 056 字符 / 17 358 字节、最长行 501 字符，"
     "skip_confirmation 直发无 42801 往返。发信前修掉 BUG-017（表格宽度被渲染成 width:100%%）",
     None),
]

steps = []
for row in STEPS:
    num, name, status, dur, result = row[:5]
    src = row[5] if len(row) > 5 else None
    s = {"num": num, "name": name, "status": status, "duration_ms": dur, "result": result}
    if src:
        s["source"] = src
    if num == 5:
        s["outputs"] = [{"label": "邮件内容", "body": MAIL_TEXT}]
    steps.append(s)

log = {
    "date": "2026-11-02",
    "type": "morning_briefing",
    "status": "success",
    "summary": "周一复市：伦敦金亚市反弹至 3909.85（+0.86%）、AU9999 837.89（-1.97%，仍在补周五夜盘）、"
               "中间价 6.7146 调低 8 点、积存金估 844.1；伊朗『两天计划』带动油价跳水近 2%，"
               "推送与邮件均成功（email_sent:true），触发延迟约 59 分钟。",
    "timestamp": "10:04 CST",
    "steps": steps,
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": sum(s["duration_ms"] for s in steps),
        "email_sent": True,
        "git_pushed": True,
    },
    "buglog_verification": {
        "method": "逐文件 grep -c '2026-11-02' ＋ 字节数 ＋ SHA-1；index.md 同步校验章节与链接；stats.json 计数器校验",
        "bugs": ver,
        "note": "BUG-013 第 35 次误判；BUG-017 本期新增并修复。BUG-012 的 14:00/22:00 未到点，按规则不判缺跑。",
    },
}

OUT = os.path.join(BASE, "logs", "2026-11-02-morning_briefing.json")
io.open(OUT, "w", encoding="utf-8").write(json.dumps(log, ensure_ascii=False, indent=2))

# 日志清单
LM = os.path.join(BASE, "logs", "manifest.json")
m = json.load(io.open(LM, encoding="utf-8"))
m["logs"] = [x for x in m["logs"] if not (x["date"] == "2026-11-02" and x["type"] == "morning_briefing")]
m["logs"].insert(0, {
    "date": "2026-11-02",
    "type": "morning_briefing",
    "status": "success",
    "summary": "周一复市版：伦敦金 3909.85（+0.86%，亚市超跌反抽但均线全在头上）、AU9999 837.89（-1.97%）、"
               "中间价 6.7146 调低 8 点、积存金估 844.1；伊朗两天计划→油价跳水→加息预期松为今日主线；"
               "推送与邮件均成功（email_sent:true），触发延迟约 59 分钟。",
})
io.open(LM, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=2))

print("log written", OUT)
print("logs total", len(m["logs"]), "head", m["logs"][0]["date"], m["logs"][0]["type"])
print("total_duration_ms", log["summary_stats"]["total_duration_ms"])
print("mail_text chars", len(MAIL_TEXT))
