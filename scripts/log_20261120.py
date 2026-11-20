# -*- coding: utf-8 -*-
"""写运行日志 logs/2026-11-20-morning_briefing.json 并前置到 logs/manifest.json。"""
import json, io, os

d = json.load(open("daily/2026-11-20.json", encoding="utf-8"))
P = {p["label"]: p for p in d["prices"]}

plain = []
plain.append("金价早报 · 2026年11月20日 周五（生成 11:34 CST，标称 09:00，延迟约 154 分钟）")
plain.append("")
plain.append("金价快照")
for k in ["招行积存金买入价", "上海金 AU9999", "美元汇率", "伦敦金 XAUUSD"]:
    p = P[k]
    plain.append("%s：%s %s，%+.2f%%" % (k, p["value"], p["unit"], p["change"]))
plain.append("")
plain.append("昨夜大事")
for i, n in enumerate(d["news"], 1):
    plain.append("%d. [%s] %s" % (i, n["tag"], n["title"]))
    plain.append("   %s" % n["explain"])
    plain.append("   来源：%s %s" % (n["source"], n["url"]))
plain.append("")
t = d["trend"]
plain.append("趋势与建议")
plain.append("短期：%s" % t["short"])
plain.append("中期：%s" % t["mid"])
plain.append("长期：%s" % t["long"])
plain.append("建议：%s" % t["advice"])
plain.append("")
plain.append("现在该干嘛")
plain.append("买入：%s" % d["plan"]["buy"]["trigger"])
plain.append("买入参考：%s" % d["plan"]["buy"]["price"])
plain.append("卖出：%s" % d["plan"]["sell"]["trigger"])
plain.append("卖出参考：%s" % d["plan"]["sell"]["price"])
plain.append("风险提示：%s" % d["plan"]["note"])
plain.append("")
plain.append("今日学一招：%s" % d["teach"]["title"])
plain.append("官网：https://jerry-166.github.io/gold-price-briefing/")
body_text = "\n".join(plain)

steps = [
    {
        "num": 1,
        "name": "获取数据",
        "status": "success",
        "duration_ms": 78000,
        "result": (
            "伦敦金 3533.97（-2.51%，昨收 3625.01，高 3636.63／低 3517.33）；AU9999 759.95（-5.23%，基准 11-19 日盘 801.93）；"
            "黄金 T+D 758.70（-5.41%）；中间价 6.7131（调贬 3bp）、在岸即期 6.6715；现货白银 41.55（-3.03%）；"
            "COMEX 12 月期金 3533.7（昨结 3685.50）；美元指数 103.85-103.90；LPR 1Y 3.0%／5Y 3.5% 连续 18 个月不变"
        ),
        "source": "新浪财经 hf_XAU／gds_AU9999／gds_AUTD／fx_susdcny 实时接口 + 东方财富 push2（GC00Y、UDI）+ WebSearch 交叉验证（金投网、汇通财经、澎湃、新华财经、中新经纬、格林大华）",
    },
    {
        "num": 2,
        "name": "生成早报JSON",
        "status": "success",
        "duration_ms": 112000,
        "result": (
            "已写入 daily/2026-11-20.json（28 041 字符）；check_briefing.py 一次通过：advice 185 字、pairs 11、errors 0、OK；"
            "图表丢 1 补 1（10-22～11-20），11-19 点回填为真实收盘 3625.0、新增 11-20 点 3534.0，events 同步 -1 并新增末位。"
            "过程含一次失败重写：% 格式化的 note 里夹带字面百分号（−2.51%）抛 TypeError，改用 .format 后通过"
        ),
    },
    {
        "num": 3,
        "name": "更新manifest",
        "status": "success",
        "duration_ms": 4000,
        "result": "已追加 2026-11-20 记录到 manifest.json 头部，briefings 90 → 91 条",
    },
    {
        "num": 4,
        "name": "Git推送",
        "status": "success",
        "duration_ms": 11000,
        "result": "已提交并推送：commit 441e776（每日早报 2026-11-20），git rev-parse HEAD 与 git ls-remote origin refs/heads/master 一致",
    },
    {
        "num": 5,
        "name": "发送邮件",
        "status": "success",
        "duration_ms": 62000,
        "result": (
            "已发送至 2132049351@qq.com，SendMessage 返回 queued:true，sent 目录回读确认 created_at 2026-11-20T03:36:57Z（11:36:57 CST），"
            "message_id msg_tGDlHB3Nes6jhJmLGOn2-nJD9yx3aHTxCLFsiO7zUHGS9w；HTML 底稿 12 484 字符／17 510 字节／62 行／maxline 909，零双百分号字面量、零 CSS width:100%"
        ),
        "outputs": [{"label": "邮件内容", "body": body_text}],
    },
]

log = {
    "date": "2026-11-20",
    "type": "morning_briefing",
    "status": "success",
    "summary": (
        "五步全成；伦敦金 3533.97（-2.51%）8 天连破 5 道整数关、本周累跌 8.9%，AU9999 759.95（-5.23%），"
        "中间价 6.7131 调贬 3bp；12 月加息 96.4% 定价＋美股崩盘＋美元 19 个月新高；标称 09:00、实际 11:32 触发延迟约 154 分钟，邮件已发"
    ),
    "timestamp": "11:32 CST（触发）／11:34 CST（生成）／11:36:57 CST（邮件）",
    "steps": steps,
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": 267000,
        "email_sent": True,
        "git_pushed": True,
    },
    "notes": [
        "延迟约 154 分钟（会话 current_time 11:32:23、首条 date 实测 11:32:30，标称 09:00）；09:00 前后伦敦金约 3590-3597，"
        "11:32 已 3533.97，延迟窗口内又跌约 60 美元（≈13 元/克）并击穿 3600、3550 两道关，按「是否覆盖当日关键价格窗口」判据记危害 1 档；"
        "updateTime 仍固定 09:00，真实生成时点已写入 _meta.updated（2026-11-20 11:34 CST）与邮件头部（建议 ⑬）",
        "neodata-financial-search skill 本地未安装（plugins/cache/**/finance-data 与 skills/finance-data 下均无 query.py）→ 取数全程走"
        "「新浪实时接口 + 东方财富 push2 + WebSearch 交叉验证」，未假装调用，step1 的 source 已如实写明",
        "今日 11:29 已有 logs/2026-11-20-inspection_pm.json（pm 线提前约 10.5 小时触发，且发生在早报之前），"
        "与本期早报 11:32 触发构成「巡检先于早报」的异常先后顺序，已记入 BUG-012 观察",
        "跨日折算用 FXP=6.7128（11-19 中间价）算昨日收盘积存金 782.35，今日 762.74 → -19.61 元/克（-2.51%），"
        "伦敦金贡献 -19.65、汇率贡献 +0.03，hero note 三段已按此写；昨日快照 800.8 与真实收盘折算差 18.45 元/克（跨日传染第九次）",
        "邮件改用 skip_confirmation:true 直发，未再出现 42801 确认链路，一次 queued:true；HTML 打点用 width=\"100%\" 属性，彻底规避 BUG-017 家族",
    ],
    "buglog_verification": {},
}

# 幂等：同日期同类型已存在则跳过
out = "logs/2026-11-20-morning_briefing.json"
if os.path.exists(out):
    old = json.load(open(out, encoding="utf-8"))
    if old.get("summary_stats", {}).get("email_sent") is True:
        print("SKIP exists", out)
        raise SystemExit

raw = json.dumps(log, ensure_ascii=False, indent=2)
assert raw.count("%%") == 0, "%% in log"
io.open(out, "w", encoding="utf-8").write(raw + "\n")
print("written", out, len(raw))

mf = json.load(open("logs/manifest.json", encoding="utf-8"))
if mf["logs"] and mf["logs"][0].get("date") == "2026-11-20" and mf["logs"][0].get("type") == "morning_briefing":
    print("log manifest already has today morning_briefing")
else:
    mf["logs"].insert(0, {
        "date": "2026-11-20",
        "type": "morning_briefing",
        "status": "success",
        "summary": log["summary"],
    })
    io.open("logs/manifest.json", "w", encoding="utf-8").write(json.dumps(mf, ensure_ascii=False, indent=2) + "\n")
    print("log manifest prepended, total", len(mf["logs"]))
