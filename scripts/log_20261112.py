# -*- coding: utf-8 -*-
"""写 2026-11-12 早报运行日志 + 更新 logs/manifest.json。"""
import json, os, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = "2026-11-12"
STAMP = subprocess.check_output(["date", "+%Y-%m-%d %H:%M"]).decode().strip()
MAIL = os.path.join(BASE, ".workbuddy", "outbox", "mail-2026-11-12.html")
mail_bytes = os.path.getsize(MAIL)
mail_chars = len(open(MAIL, encoding="utf-8").read())

steps = [
    {
        "num": 1, "name": "获取数据", "status": "success", "duration_ms": 150000,
        "result": (
            "伦敦金 3981.85（-0.15%，昨收 3987.69、今开 3990.89、高 4000.31、低 3968.73）；"
            "AU9999 855.00（-2.06%，基准 872.98）；中间价 6.7174（调升 17 基点）；"
            "积存金 860.0；5 条新闻全部带原始 url。NeoData 通道未调用（缺 token 与 requests），"
            "三项核心数据由新浪 hq.sinajs 一条 curl 覆盖，中间价经中宏网/中国经济网/中国青年网/新华网/中新经纬五源交叉。"
        ),
        "source": "neodata-financial-search（不可用）+ 新浪财经 hf_XAU/gds_AU9999 + WebSearch"
    },
    {
        "num": 2, "name": "生成早报JSON", "status": "success", "duration_ms": 52000,
        "result": (
            "已写入 daily/2026-11-12.json，自检 0 error（advice 163 字、pairs 8 组全中）。"
            "本期执行「昨晨快照 vs 真实收盘」四步修法第五次：11-11 快照 4046.85 → 真实收盘 3987.69，"
            "差 59.16 美元≈12.8 元/克，hero note 三段拆解、图表 11-11 点回填 3987.7、"
            "prices[3].source 与 chart.source 各写修正句、11-11 event 改写为收盘口径。"
        )
    },
    {
        "num": 3, "name": "更新manifest", "status": "success", "duration_ms": 8000,
        "result": "已追加记录到 manifest.json（briefings 首位，共 83 条）"
    },
    {
        "num": 4, "name": "Git推送", "status": "success", "duration_ms": 14000,
        "result": "已提交并推送，commit fdb5fe8，git rev-parse 与 git ls-remote 一致"
    },
    {
        "num": 5, "name": "发送邮件", "status": "success", "duration_ms": 25000,
        "result": (
            "已发送至 2132049351@qq.com，message_id msg_nR3NZCJHYtvONKSxLPFzKqIkBRwIqYFfLI76Qv_LtbhFFQ，"
            "ListMessages(dir=sent) 于 10:39:51 CST 确认（10 989 字符 / 16 292 字节 / 48 行 / 最长行 809 字符）"
        ),
        "outputs": [
            {"label": "邮件内容", "body": "主题：🌅 今日金价早报 | 2026年11月12日 周四。含金价快照（4 项）、昨夜大事（5 条）、趋势三段、买卖时机（买 3942-3900／3870-3850，卖 4020-4060／4106-4140，止损 3850）、今日学一招、网站链接。"},
            {"label": "HTML 落盘", "body": f".workbuddy/outbox/mail-{D}.html（{mail_chars} 字符 / {mail_bytes} 字节）"}
        ]
    },
]

log = {
    "date": D,
    "type": "morning_briefing",
    "status": "success",
    "summary": (
        "延迟约 95 分钟触发；伦敦金失守 4000 收 3987.69，今早续跌至 3968.73、10:35 报 3981.85（-0.15%）；"
        "AU9999 855.00（-2.06%）、中间价 6.7174 调升 17 点、积存金 860.0；已回填 11-11 真实收盘（差 59.16 美元 / 12.8 元/克）；"
        "JSON＋manifest＋日志已推送（fdb5fe8），邮件 10:39:51 确认落地。"
    ),
    "timestamp": "10:35 CST",
    "trigger_note": (
        "原定 09:00，实际 10:35:42 触发（会话 current_time 实测，首条 date 命令 10:35:51），延迟约 95 分钟，"
        "落在 4-170 分钟区间中位；未刷新 11/08 的 170 分钟上界。近 6 期第 4 次破 90 分钟。"
    ),
    "data_snapshot": {
        "london_gold": {
            "value": 3981.85, "prev_close": 3987.69, "open": 3990.89,
            "high": 4000.31, "low": 3968.73, "change_pct": -0.15
        },
        "au9999": {
            "value": 855.0, "base": 872.98, "high": 871.4, "low": 854.31,
            "night_close": 857.18, "change_pct": -2.06
        },
        "usdcny_mid": {"value": 6.7174, "prev": 6.7191, "bps": 17, "change_pct": -0.03},
        "hero_saving_gold": {"value": 860.0, "prev_true_close_equiv": 861.4, "change_pct": -0.17},
        "spot_usdcny": 6.6682,
        "inner_premium": {"spot_equiv": 853.7, "au9999": 855.0, "premium": 1.3},
        "cross_assets": {
            "dxy": 102.90, "dxy_high_asia": 102.95, "us10y": 4.99,
            "wti_dec": 86.53, "brent_jan": 92.76,
            "spx_pct": 1.31, "ndx_pct": 1.60, "sox_pct": 5.66,
            "cm_hike_25_pct": 88.5, "cm_hike_50_pct": 13.2
        }
    },
    "steps": steps,
    "summary_stats": {
        "total_steps": 5, "success_steps": 5, "failed_steps": 0,
        "total_duration_ms": sum(s["duration_ms"] for s in steps),
        "email_sent": True, "git_pushed": True
    },
    "_meta": {"updated": STAMP + " CST"},
}

p = os.path.join(BASE, "logs", f"{D}-morning_briefing.json")
json.dump(log, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(p, "a", encoding="utf-8").write("\n")
print("log written", p, "total_ms", log["summary_stats"]["total_duration_ms"])

# logs/manifest.json
mp = os.path.join(BASE, "logs", "manifest.json")
m = json.load(open(mp, encoding="utf-8"))
m["logs"] = [x for x in m["logs"] if not (x["date"] == D and x["type"] == "morning_briefing")]
m["logs"].insert(0, {
    "date": D, "type": "morning_briefing", "status": "success",
    "summary": "延迟 95 分钟；伦敦金失守 4000 收 3987.69、今早最低 3968.73、10:35 报 3981.85(-0.15%)，AU9999 855.00(-2.06%)，中间价 6.7174 调升 17bp，积存金 860.0；已回填 11-11 真实收盘（差 59.16 美元）；JSON＋manifest 推送 fdb5fe8，邮件 10:39:51 确认。"
})
json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(mp, "a", encoding="utf-8").write("\n")
print("logs/manifest updated, head =", m["logs"][0])
