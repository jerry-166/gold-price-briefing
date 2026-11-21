# -*- coding: utf-8 -*-
"""写 2026-11-21 早报运行日志并更新 logs/manifest.json。"""
import json, os, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = "2026-11-21"
now = datetime.datetime.now()
ts = now.strftime("%H:%M") + " CST"

body = open(os.path.join(BASE, ".workbuddy", "outbox", "mail-2026-11-21-morning_briefing.html"), encoding="utf-8").read()

steps = [
    {
        "num": 1,
        "name": "获取数据",
        "status": "success",
        "duration_ms": 128000,
        "result": (
            "伦敦金 3534.64 美元/盎司（−2.49%，昨收 3625.01，高 3636.63／低 3502.73）；"
            "AU9999 夜盘收 755.01（−1.24%，基准 11-20 日盘收 764.50）；中间价 6.7131（11-20 公布，周六不更新）；"
            "新闻 6 条（保尔森/库克放鹰、TIPS 实际利率 2.95%、周五收盘 3537.87、中间价与美元指数、"
            "金饰十连跌与四家银行风险提示、大阪交易所熔断）"
        ),
        "source": "新浪财经 hf_XAU/gds_AU9999 实时接口 + WebSearch（中新经纬/每经/上海证券报/金投网/同花顺）+ 中国货币网；neodata-financial-search 本地未安装，未调用",
    },
    {
        "num": 2,
        "name": "生成早报JSON",
        "status": "success",
        "duration_ms": 96000,
        "result": "已写入 daily/2026-11-21.json（26 361 字节），check_briefing.py 零错误（advice 192 字、价位配对 8 处）；11-20 图表点按真实收盘回填 3534.6，11-21 与收盘同值",
    },
    {
        "num": 3,
        "name": "更新manifest",
        "status": "success",
        "duration_ms": 6000,
        "result": "已追加记录到 manifest.json（briefings 91→92 条，头部 2026-11-21 周六）",
    },
    {
        "num": 4,
        "name": "Git推送",
        "status": "success",
        "duration_ms": 14000,
        "result": "已提交 4b1e20a 并推送，git ls-remote 与 rev-parse 一致（2473ed8..4b1e20a master）",
    },
    {
        "num": 5,
        "name": "发送邮件",
        "status": "success",
        "duration_ms": 59000,
        "result": "已发送至 2132049351@qq.com，skip_confirmation 直发一次 queued:true，sent 目录回读 created_at 2026-11-21T03:09:12Z（11:09:12 CST）",
        "outputs": [{"label": "邮件内容", "body": body}],
    },
]

log = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "success",
    "summary": "周六休市版早报：沿用 11-20 纽约收盘（伦敦金 3534.6、−2.49%），AU9999 取夜盘收 755.0；JSON/图表/manifest/推送/邮件六步全部完成，延迟约 129 分钟但当日无新行情、危害 0 档",
    "timestamp": ts,
    "steps": steps,
    "notes": [
        "触发 11:04、邮件 11:09，标称 09:00 → 延迟约 129 分钟；周六国际盘 06:00 起休市、上金所与外汇交易中心全停，窗口内无新行情，危害 0 档，未在邮件头部标注延迟（updateTime 仍固定 09:00）",
        "媒体报周五纽约收盘 3537.87（−2.47%），与站内 hf_XAU 3534.64 差约 3 美元，已在 prices[3].source 与 chart.source 写明来源差异",
        "AU9999 涨跌幅 −1.24% 只覆盖 11-20 夜盘，与伦敦金 −2.49%（覆盖整个 11-20 交易日）时段不对齐，已在 source 说明，避免读者以为数据矛盾",
        "outbox 底稿按 BUG-029 规范命名 mail-2026-11-21-morning_briefing.html",
    ],
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": 303000,
        "email_sent": True,
        "git_pushed": True,
    },
    "outbox_path": ".workbuddy/outbox/mail-2026-11-21-morning_briefing.html",
}

p = os.path.join(BASE, "logs", DATE + "-morning_briefing.json")
raw = json.dumps(log, ensure_ascii=False, indent=2)
assert raw.count("%%") == 0
open(p, "w", encoding="utf-8").write(raw + "\n")
print("log written", p, len(raw), "bytes, timestamp", ts)

# logs/manifest.json
mp = os.path.join(BASE, "logs", "manifest.json")
m = json.load(open(mp, encoding="utf-8"))
rec = {"date": DATE, "type": "morning_briefing", "status": "success",
       "summary": "周六休市版：沿用 11-20 收盘（伦敦金 3534.6、−2.49%），五步全成功、邮件已送达"}
if m["logs"] and m["logs"][0]["date"] == DATE and m["logs"][0]["type"] == "morning_briefing":
    m["logs"][0] = rec
    print("manifest 已有今日早报记录，已覆盖")
else:
    m["logs"].insert(0, rec)
    print("manifest 已前插，总数", len(m["logs"]))
open(mp, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
print(m["logs"][:2])
