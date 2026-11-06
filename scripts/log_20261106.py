# -*- coding: utf-8 -*-
"""写入 2026-11-06 早报运行日志 + 日志清单。"""
import json, io, os, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGS = os.path.join(BASE, ".buglog", "bugs")


def fstat(p):
    raw = io.open(p, "rb").read()
    return {"occurrences": io.open(p, encoding="utf-8").read().count("2026-11-06"),
            "bytes": len(raw), "sha1": hashlib.sha1(raw).hexdigest()}


ver_files = [
    "2026-09-08-briefing-scheduler-missed-days.md",
    "2026-09-14-inspection-email-connector-down.md",
    "2026-09-25-inspection-scheduler-silent-miss.md",
    "2026-09-26-buglog-hook-misfire.md",
    "2026-11-06-mail-whole-doc-percent-format.md",
]
ver = {}
for n in ver_files:
    ver[n] = fstat(os.path.join(BUGS, n))
ver["index.md"] = fstat(os.path.join(BASE, ".buglog", "index.md"))

mail_body = (
    "🌅 今日金价早报 | 2026年11月06日 周五\n\n"
    "【金价快照】积存金 880.4 元/克（-0.31%）｜上海金 AU9999 875.0 元/克（-1.03%）｜"
    "中间价 6.7168（+0.02%，调贬 12 点）｜伦敦金 4076.8 美元/盎司（-0.29%）\n\n"
    "【一句话说今天】昨晚金价冲到 4146.77 的两周高点又被砸回来，收 4088.80（+0.67%），留了根长上影——"
    "不是没人买，是美股 AI 股灾（纳指 -5.52%、VIX +69.66%）逼得有人卖黄金去补保证金。"
    "今早 4076.76，多空都在等今晚 21:30 的 10 月非农。\n\n"
    "【昨夜大事】① 今晚 21:30 非农，预期 6.5 万而 ADP 已 8.6 万，数据偏强则金价承压；"
    "② 霍尔木兹一艘油轮触雷起火，WTI 收 90.52（+2.72%）、布伦特 98.29（+3.88%），油价反弹打断通胀降温；"
    "③ 美股 AI 股灾，纳指 100 市值蒸发 2.3 万亿美元，流动性挤兑下黄金被动挨抛；"
    "④ 哈玛克、巴尔金连夜放鹰，12 月加息概率 CME 81.5%／部分期货口径 66%-69%；"
    "⑤ 中间价 6.7168 调贬 12 点。\n\n"
    "【趋势】短期中性（等非农）、中期偏空（利率天花板 4150-4170）、长期偏多（央行三季度净购金 321 吨）。"
    "当前动作：先观望。\n\n"
    "【买卖时机】买：回踩 4050-4060 美元（约 875-877 元/克）第一笔，3980-4000（约 860-864 元/克）第二笔；"
    "卖：4130-4150（约 892-896 元/克）卖三分之一，4180-4200（约 903-907 元/克）再卖一批；"
    "收盘破 4030-4040（约 870-872 元/克）离场。\n\n"
    "【今日学一招】非农凭什么一个晚上能让金价跳 100 美元？—— 强数据＝加息预期升＝美元美债涨＝持金成本升＝金价跌，"
    "看的是「跟 6.5 万预期差多少」。\n\n"
    "网站：https://jerry-166.github.io/gold-price-briefing/"
)

log = {
    "date": "2026-11-06",
    "type": "morning_briefing",
    "status": "success",
    "summary": "早报 5/5 全流程成功：伦敦金 4076.76（-0.29%）、AU9999 875.00（-1.03%）、中间价 6.7168、积存金 880.4 元/克；"
               "已推送 GitHub Pages 并向 2132049351@qq.com 发出邮件（连续第 6 日正常）。",
    "timestamp": "09:23:41 CST",
    "steps": [
        {"num": 1, "name": "获取数据", "status": "success", "duration_ms": 108000,
         "result": "伦敦金 4076.76（昨收 4088.80、开 4087.48、高 4106.79、低 4071.10，-0.29%）；AU9999 875.00（昨收 884.09、开 887.00，-1.03%）、T+D 874.70（-1.03%）；"
                   "中间价 6.7168（调贬 12 点）+ 在岸 6.6710／夜盘 6.6680／离岸 6.6652；DXY 101.60、COMEX 12 月期金 4103.0；"
                   "新闻 5 条（非农／霍尔木兹油轮／美股 AI 股灾／联储放鹰／中间价）均带原始 url。",
         "source": "新浪财经 hf_XAU/gds_AU9999/gds_AUTD + 东方财富 push2 + WebSearch（新华财经、中金在线、汇通网、同花顺）"},
        {"num": 2, "name": "生成早报JSON", "status": "success", "duration_ms": 46000,
         "result": "已写入 daily/2026-11-06.json；check_briefing.py 一次 0 error（11 组价位复算全中）；"
                   "图表 30 点、11-05 点由快照 4095.2 回填真实收盘 4088.8、events 整体 -1 并新增 11-06。",
         "source": "scripts/build_20261106.py + scripts/check_briefing.py"},
        {"num": 3, "name": "更新manifest", "status": "success", "duration_ms": 2000,
         "result": "已追加 2026-11-06 记录到 manifest.json 头部（briefings 76→77 条）。",
         "source": "脚本内联处理"},
        {"num": 4, "name": "Git推送", "status": "success", "duration_ms": 15000,
         "result": "已提交 df6c0e1「每日早报 2026-11-06」并推送 origin/master；rev-parse 与 ls-remote 均为 df6c0e13f94d929fc3bc586cb70ce216c9969db2。",
         "source": "git push via SSH"},
        {"num": 5, "name": "发送邮件", "status": "success", "duration_ms": 128000,
         "result": "已发送至 2132049351@qq.com，ListMessages(dir=sent) 于 09:28:37 CST 确认（msg_iQgtnH9lbCXj8KJeoI2wlsvWz_OQZveUL686evDgRrQbVA）；"
                   "HTML 15 870 字符 / 21 636 字节 / 96 行 / 最长行 817 字符，底稿落 .workbuddy/outbox/2026-11-06-morning.html。",
         "outputs": [{"label": "邮件内容", "body": mail_body}]},
    ],
    "summary_stats": {"total_steps": 5, "success_steps": 5, "failed_steps": 0,
                      "total_duration_ms": 299000, "email_sent": True, "git_pushed": True},
    "data_notes": [
        "本期为常规交易日，无周末／节假日沿用；11-06 图表点为 09:23 盘中快照，收盘后回填。",
        "执行「昨晨快照 vs 真实收盘」修法：11-05 早报用 09:03 快照 4095.22，实际收 4088.80，差 6.42 美元 ≈ 1.4 元/克；"
        "hero note 三段拆解、prices[3].source 与 chart.source 各写修正句、图表 11-05 点回填为 4088.8。",
        "国内溢价由升转折：11-05 收 884.09 相对应有价 883.0 升水 1.1 元；今日 875.00 相对 880.4 折价 5.4 元（-0.61%）。",
        "12 月加息概率存在口径分歧：CME 口径 81.5%（新华财经 11-05 收盘），部分利率期货口径已回落至 66%-69%（中金在线 11-06 早评），"
        "两处均已标注来源，未强行统一。",
        "COMEX 12 月期金收盘各源不一致（新华 4098.1/+0.62%、央视 4113.50/+0.99%、东方财富昨结 4113.5），故未写入 prices，仅在旁证中引用。",
        "NeoData 通道本期未调用：sina 接口一条 curl 已覆盖伦敦金／AU9999／T+D 三项，中间价用 WebSearch 五源交叉（证券时报、财联社、第一财经、同花顺同值 6.7168）。",
        "BUG-021 新增：mail 脚本整篇 % 格式化导致两次 ValueError，均在发货前拦下，邮件未受影响。",
    ],
    "buglog_verification": ver,
}

p = os.path.join(BASE, "logs", "2026-11-06-morning_briefing.json")
io.open(p, "w", encoding="utf-8").write(json.dumps(log, ensure_ascii=False, indent=2) + "\n")
print("written", p)

# logs/manifest.json
lp = os.path.join(BASE, "logs", "manifest.json")
m = json.load(io.open(lp, encoding="utf-8"))
print("keys", list(m.keys()))
entry = {"date": "2026-11-06", "type": "morning_briefing", "status": "success",
         "summary": "早报 5/5 成功：伦敦金 4076.76（-0.29%）、AU9999 875.0（-1.03%）、中间价 6.7168、积存金 880.4；已推送并发出邮件。"}
if m["logs"] and m["logs"][0].get("date") == "2026-11-06":
    print("ALREADY")
else:
    m["logs"].insert(0, entry)
    io.open(lp, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
    print("inserted, n=", len(m["logs"]))
print(json.dumps(m["logs"][:2], ensure_ascii=False))
