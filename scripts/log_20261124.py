# -*- coding: utf-8 -*-
"""写 2026-11-24 早报运行日志 + 追加 logs/manifest.json。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
d = json.load(open(ROOT / "daily" / "2026-11-24.json", encoding="utf-8"))
p = {x["label"]: x for x in d["prices"]}

MAIL_TEXT = (
    "🌅 今日金价早报 | 2026 年 11 月 24 日 周二\n\n"
    "【金价快照 · 截至 09:12 亚市】\n"
    "· 招行积存金买入价（估算）" + p["招行积存金买入价"]["value"] + " 元/克，+0.73%\n"
    "· 上海金 AU9999 " + p["上海金 AU9999"]["value"] + " 元/克，+0.72%（基准 11-23 日盘收 781.40）\n"
    "· 美元汇率 " + p["美元汇率"]["value"] + "（11-24 中间价 09:15 前未发布，沿用 11-23 的 6.7120）\n"
    "· 伦敦金 XAUUSD " + p["伦敦金 XAUUSD"]["value"] + " 美元/盎司，+0.73%（昨收 3635.23）\n\n"
    "【昨夜大事】\n"
    "1. 威廉姆斯放鹰：为把通胀拉回 2%「仍有工作要做」，12 月加息 25bp 概率升到 99%、加 50bp 基本排除。\n"
    "2. 11 月标普全球 PMI 初值全线回落至四个月低位（综合 54.6、制造 54.5、服务 54.7），但仍在荣枯线上方。\n"
    "3. 黄仁勋复任英伟达 CEO，纳指 +6.51%、英伟达 +31.5%，AI 链恐慌退潮，金价跟着跳空高开。\n"
    "4. 美元指数冲上 104、收 104.32 创近 19 个月新高，2 年期美债 +4.7bp 报 4.696%，尾盘把金价从 3690 打回 3635。\n"
    "5. 伊朗称动用一切手段应对美国海上封锁，但油价先跌：WTI 80.17（-3.88%）、布伦特 89.33（-3.50%）。\n"
    "6. 三季度全球央行净购金 321 吨（同比 +42%）、中国连续 24 个月增持；金饰价回到 1078-1098 元/克。\n\n"
    "【趋势】短线中性 / 中线中性 / 长期偏多，当前建议：观望。\n"
    "超跌修复还没走完，但空间被美元锁住：3637 是多空线，站上 3660 才谈 3690，跌破 3612 就要去补 3571 的缺口。\n\n"
    "【买卖时机】\n"
    "买：回踩 3610-3620（约 779-781 元/克）分批试，跌破 3570 等 3560-3570（约 768-770 元/克），破 3535 停手。\n"
    "卖：冲 3685-3700（约 795-798 元/克）减一半，跌破 3600（约 777 元/克）止损，仓位别过三成。\n\n"
    "【今日学一招】昨晚那根「长上影线」，到底在告诉你什么？——影线记录的不是涨了多少，而是涨上去以后被卖回来了多少。\n\n"
    "网站：https://jerry-166.github.io/gold-price-briefing/"
)

steps = [
    {
        "num": 1,
        "name": "获取数据",
        "status": "success",
        "duration_ms": 86000,
        "result": (
            "伦敦金 3661.65（+0.73%，昨收 3635.23、今开 3630.52、高 3669.45、低 3619.71）；"
            "AU9999 787.00（+0.72%，基准 781.40、高 794.50 出自 11-23 夜盘）；T+D 786.74（+0.83%）；"
            "中间价 11-24 09:15 前未发布（中国货币网 lastDate 仍为 23/11/2026 9:15），沿用 11-23 的 6.7120；"
            "DXY 104.32（+0.44%）、2 年期美债 4.696%（+4.7bp）、10 年期 4.939%；COMEX 金 3634.40（+3.39%）；"
            "新闻六条均已取到原始 url"
        ),
        "source": "新浪财经 hq.sinajs.cn（hf_XAU / gds_AU9999 / gds_AUTD 实时接口）+ 中国货币网 ccpr.json + WebSearch",
    },
    {
        "num": 2,
        "name": "生成早报JSON",
        "status": "success",
        "duration_ms": 74000,
        "result": (
            "已写入 daily/2026-11-24.json（29 027 字节）；check_briefing.py 首轮报 advice 203 字超限，"
            "压缩到 184 字后 errors: 0 / OK；图表 labels 10-26…11-24 共 30 点，11-23 由早报快照 3605.0 回填为真实收盘 3635.2，"
            "events 整体 -1 后补 index 29；hero 790.2（昨日真实收盘折算 784.5，差 +5.7 元/克）"
        ),
    },
    {
        "num": 3,
        "name": "更新manifest",
        "status": "success",
        "duration_ms": 7000,
        "result": "已追加记录到 manifest.json（briefings 头部 2026-11-24 / 周二）",
    },
    {
        "num": 4,
        "name": "Git推送",
        "status": "success",
        "duration_ms": 46000,
        "result": "已提交并推送：b452992（早报+manifest）、7b4834d（构建脚本）；git rev-parse 与 ls-remote origin master 均为 7b4834d",
    },
    {
        "num": 5,
        "name": "发送邮件",
        "status": "success",
        "duration_ms": 61000,
        "result": (
            "已发送至 2132049351@qq.com（skip_confirmation 直发、一次 queued:true；sent 目录回读 "
            "created_at 2026-11-24T01:15:37Z = 09:15:37 CST）；底稿 .workbuddy/outbox/mail-2026-11-24-morning_briefing.html"
            "（17 621 字节 / maxline 832）"
        ),
        "outputs": [{"label": "邮件内容", "body": MAIL_TEXT}],
    },
]

log = {
    "date": "2026-11-24",
    "type": "morning_briefing",
    "status": "success",
    "summary": (
        "交易日版：伦敦金 3661.7（+0.73%）、AU9999 787.0（+0.72%）；"
        "中间价未发布沿用 6.7120；五步全部成功，邮件 09:15:37 送达"
    ),
    "timestamp": "09:16 CST",
    "steps": steps,
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": 274000,
        "email_sent": True,
        "git_pushed": True,
    },
}

raw = json.dumps(log, ensure_ascii=False, indent=2)
assert raw.count("%%") == 0
out = ROOT / "logs" / "2026-11-24-morning_briefing.json"
out.write_text(raw + "\n", encoding="utf-8")

mp = ROOT / "logs" / "manifest.json"
m = json.load(open(mp, encoding="utf-8"))
assert m["logs"][0]["date"] != "2026-11-24"
m["logs"].insert(0, {
    "date": "2026-11-24",
    "type": "morning_briefing",
    "status": "success",
    "summary": "交易日版：伦敦金 3661.7（+0.73%）、AU9999 787.0（+0.72%），中间价未发布沿用 6.7120；五步全成、邮件已送达",
})
raw2 = json.dumps(m, ensure_ascii=False, indent=2)
assert raw2.count("%%") == 0
mp.write_text(raw2 + "\n", encoding="utf-8")

print("log bytes", len(raw.encode("utf-8")))
print("logs head:", [x["date"] for x in m["logs"][:4]])
