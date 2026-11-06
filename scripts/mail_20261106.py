# -*- coding: utf-8 -*-
"""生成 2026-11-06 早报邮件 HTML。"""
import json, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(io.open(os.path.join(BASE, "daily", "2026-11-06.json"), encoding="utf-8"))
OUT = os.path.join(BASE, ".workbuddy", "outbox")
if not os.path.isdir(OUT):
    os.makedirs(OUT)
PATH = os.path.join(OUT, "2026-11-06-morning.html")

GOLD = "#B8860B"
DARK = "#1a1a1a"
GRAY = "#666666"
RED = "#C62828"
GREEN = "#2E7D32"
BG = "#FFFDF7"

TAGTYPE = {"fed": ("#7B1FA2", "美联储"), "geo": ("#E65100", "地缘"),
           "fx": ("#1565C0", "汇率"), "data": ("#00695C", "数据")}


def pct_cell(ch):
    if ch > 0:
        return '<td style="padding:9px 10px;text-align:right;font-size:14px;color:%s;font-weight:bold;">+%.2f%%</td>' % (RED, ch)
    if ch < 0:
        return '<td style="padding:9px 10px;text-align:right;font-size:14px;color:%s;font-weight:bold;">%.2f%%</td>' % (GREEN, ch)
    return '<td style="padding:9px 10px;text-align:right;font-size:14px;color:%s;">0.00%%</td>' % GRAY


# ---------- 价格表 ----------
price_rows = []
for p in d["prices"]:
    if p.get("hero"):
        name = '%s <span style="font-size:11px;color:%s;background:#FFF3D6;padding:1px 5px;border-radius:3px;">重点</span>' % (p["label"], GOLD)
    else:
        name = p["label"]
    price_rows.append(
        '<tr style="border-bottom:1px solid #F0EBDD;">'
        '<td style="padding:9px 10px;font-size:14px;color:%s;">%s</td>' % (DARK, name)
        + '<td style="padding:9px 10px;text-align:right;font-size:16px;font-weight:bold;color:%s;">%s <span style="font-size:11px;font-weight:normal;color:%s;">%s</span></td>' % (DARK, p["value"], GRAY, p["unit"])
        + pct_cell(p["change"])
        + '</tr>'
    )

# ---------- 新闻 ----------
news_rows = []
for i, n in enumerate(d["news"], 1):
    color, _ = TAGTYPE.get(n["tagType"], ("#555555", ""))
    news_rows.append(
        '<table role="presentation" style="width:100%%;border-collapse:collapse;margin:0 0 14px 0;">'
        '<tr><td style="padding:0;">'
        '<div style="font-size:12px;color:%s;font-weight:bold;margin-bottom:4px;">第 %d 条 · <span style="background:%s;color:#ffffff;padding:1px 6px;border-radius:3px;">%s</span> · <span style="color:%s;font-weight:normal;">%s</span></div>'
        '<div style="font-size:15px;font-weight:bold;color:%s;line-height:1.55;margin-bottom:5px;">%s</div>'
        '<div style="font-size:13px;color:#444444;line-height:1.75;">%s</div>'
        '</td></tr></table>' % (color, i, color, n["tag"], GRAY, n["source"], DARK, n["title"], n["explain"])
    )

# ---------- 趋势 ----------
def trend_row(label, text, val):
    if val > 0:
        arrow, c, word = "▲", RED, "偏多"
    elif val < 0:
        arrow, c, word = "▼", GREEN, "偏空"
    else:
        arrow, c, word = "◆", GRAY, "中性"
    return (
        '<tr style="border-bottom:1px solid #F0EBDD;">'
        '<td style="padding:8px 10px;font-size:13px;color:%s;white-space:nowrap;vertical-align:top;">%s</td>' % (GRAY, label)
        + '<td style="padding:8px 10px;font-size:13px;color:%s;font-weight:bold;white-space:nowrap;vertical-align:top;">%s %s</td>' % (c, arrow, word)
        + '<td style="padding:8px 10px;font-size:13px;color:#444444;line-height:1.7;">%s</td>' % text
        + '</tr>'
    )

trend_rows = [
    trend_row("短期（1-2 周）", d["trend"]["short"], d["trend"]["shortVal"]),
    trend_row("中期（1-3 月）", d["trend"]["mid"], d["trend"]["midVal"]),
    trend_row("长期（1 年+）", d["trend"]["long"], d["trend"]["longVal"]),
]

ACTION = {"buy": "可以买", "hold": "继续持有", "watch": "先观望"}
act = ACTION.get(d["trend"]["action"], "先观望")

buy, sell, pnote = d["plan"]["buy"], d["plan"]["sell"], d["plan"]["note"]

html = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F4F1E8;">
<table role="presentation" style="width:100%%;border-collapse:collapse;background:#F4F1E8;">
<tr><td align="center" style="padding:18px 10px;">
<table role="presentation" style="width:100%%;max-width:620px;border-collapse:collapse;background:%(BG)s;border-radius:10px;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;">

<tr><td style="background:linear-gradient(135deg,#8C6D1F,#C9A227);padding:22px 24px;">
<div style="font-size:20px;font-weight:bold;color:#ffffff;letter-spacing:0.5px;">🌅 今日金价早报</div>
<div style="font-size:13px;color:#F5E9C8;margin-top:6px;">2026 年 11 月 6 日 周五 · 09:00</div>
</td></tr>

<tr><td style="padding:20px 24px 6px 24px;">
<div style="font-size:15px;font-weight:bold;color:%(GOLD)s;border-left:3px solid %(GOLD)s;padding-left:9px;">一句话说今天</div>
<div style="font-size:14px;color:#333333;line-height:1.8;margin-top:9px;">%(LEAD)s</div>
</td></tr>

<tr><td style="padding:16px 24px 4px 24px;">
<div style="font-size:15px;font-weight:bold;color:%(GOLD)s;border-left:3px solid %(GOLD)s;padding-left:9px;margin-bottom:10px;">金价快照</div>
<table role="presentation" style="width:100%%;border-collapse:collapse;background:#ffffff;border:1px solid #EFE9D8;border-radius:8px;">
<tr style="background:#FAF6EA;">
<th style="padding:8px 10px;text-align:left;font-size:12px;color:%(GRAY)s;font-weight:normal;">品种</th>
<th style="padding:8px 10px;text-align:right;font-size:12px;color:%(GRAY)s;font-weight:normal;">最新价</th>
<th style="padding:8px 10px;text-align:right;font-size:12px;color:%(GRAY)s;font-weight:normal;">涨跌</th>
</tr>
%(PRICE_ROWS)s
</table>
<div style="font-size:11px;color:%(GRAY)s;line-height:1.7;margin-top:8px;">%(HERO_NOTE)s</div>
</td></tr>

<tr><td style="padding:18px 24px 2px 24px;">
<div style="font-size:15px;font-weight:bold;color:%(GOLD)s;border-left:3px solid %(GOLD)s;padding-left:9px;margin-bottom:12px;">昨夜大事</div>
%(NEWS_ROWS)s
</td></tr>

<tr><td style="padding:8px 24px 2px 24px;">
<div style="font-size:15px;font-weight:bold;color:%(GOLD)s;border-left:3px solid %(GOLD)s;padding-left:9px;margin-bottom:6px;">趋势怎么看</div>
<table role="presentation" style="width:100%%;border-collapse:collapse;">
%(TREND_ROWS)s
</table>
<div style="font-size:13px;color:#333333;line-height:1.8;background:#FFF8E6;border-radius:6px;padding:11px 13px;margin-top:12px;">
<span style="font-weight:bold;color:%(GOLD)s;">当前动作：%(ACT)s</span><br>%(ADVICE)s
</div>
</td></tr>

<tr><td style="padding:18px 24px 2px 24px;">
<div style="font-size:15px;font-weight:bold;color:%(GOLD)s;border-left:3px solid %(GOLD)s;padding-left:9px;margin-bottom:10px;">买卖时机</div>
<table role="presentation" style="width:100%%;border-collapse:collapse;">
<tr><td style="padding:0 0 10px 0;">
<div style="background:#F1F8F1;border-left:3px solid %(GREEN)s;border-radius:0 6px 6px 0;padding:11px 13px;">
<div style="font-size:13px;font-weight:bold;color:%(GREEN)s;margin-bottom:5px;">什么时候买</div>
<div style="font-size:13px;color:#333333;line-height:1.75;">%(BUY_TRIG)s</div>
<div style="font-size:12px;color:%(GREEN)s;margin-top:6px;font-weight:bold;">参考价位：%(BUY_PRICE)s</div>
<div style="font-size:12px;color:%(GRAY)s;margin-top:3px;">为什么：%(BUY_REASON)s</div>
</div></td></tr>
<tr><td style="padding:0 0 10px 0;">
<div style="background:#FDF2F2;border-left:3px solid %(RED)s;border-radius:0 6px 6px 0;padding:11px 13px;">
<div style="font-size:13px;font-weight:bold;color:%(RED)s;margin-bottom:5px;">什么时候卖 / 止损</div>
<div style="font-size:13px;color:#333333;line-height:1.75;">%(SELL_TRIG)s</div>
<div style="font-size:12px;color:%(RED)s;margin-top:6px;font-weight:bold;">参考价位：%(SELL_PRICE)s</div>
<div style="font-size:12px;color:%(GRAY)s;margin-top:3px;">为什么：%(SELL_REASON)s</div>
</div></td></tr>
</table>
<div style="font-size:11px;color:%(GRAY)s;line-height:1.7;">%(PLAN_NOTE)s</div>
</td></tr>

<tr><td style="padding:16px 24px 2px 24px;">
<div style="font-size:15px;font-weight:bold;color:%(GOLD)s;border-left:3px solid %(GOLD)s;padding-left:9px;margin-bottom:9px;">今日学一招：%(TEACH_TITLE)s</div>
<div style="font-size:13px;color:#333333;line-height:1.85;background:#ffffff;border:1px solid #EFE9D8;border-radius:8px;padding:12px 14px;">%(TEACH_BODY)s</div>
<div style="font-size:11px;color:%(GRAY)s;margin-top:6px;">来源：%(TEACH_SRC)s</div>
</td></tr>

<tr><td style="padding:16px 24px 6px 24px;">
<div style="font-size:15px;font-weight:bold;color:%(GOLD)s;border-left:3px solid %(GOLD)s;padding-left:9px;margin-bottom:9px;">今日知识点</div>
%(KNOW_ROWS)s
</td></tr>

<tr><td style="padding:20px 24px 24px 24px;text-align:center;border-top:1px solid #EFE9D8;">
<div style="font-size:13px;color:%(GRAY)s;line-height:1.8;">数据与图表都在站上，打开看 30 天走势<br><a href="https://jerry-166.github.io/gold-price-briefing/" style="color:%(GOLD)s;font-weight:bold;text-decoration:none;">jerry-166.github.io/gold-price-briefing</a></div>
<div style="font-size:11px;color:#999999;margin-top:10px;line-height:1.7;">本邮件由自动化流程生成，所有价格与观点仅供参考，不构成投资建议。<br>数据源：新浪财经、上海黄金交易所、中国外汇交易中心、新华财经、中金在线、汇通网</div>
</td></tr>

</table></td></tr></table></body></html>
"""

know_rows = []
for k in d["knowledge"]:
    know_rows.append(
        '<div style="margin-bottom:11px;padding:10px 12px;background:#ffffff;border:1px solid #EFE9D8;border-radius:8px;">'
        '<div style="font-size:13px;font-weight:bold;color:%s;margin-bottom:4px;">[' % DARK + k["cat"] + '] ' + k["title"] + '</div>'
        '<div style="font-size:13px;color:#555555;line-height:1.7;">' + k["detail"] + '</div>'
        '<div style="font-size:11px;color:%s;margin-top:4px;">来源：' % GRAY + k["source"] + '</div>'
        '</div>'
    )

vals = {
    "BG": BG, "GOLD": GOLD, "GRAY": GRAY, "DARK": DARK, "RED": RED, "GREEN": GREEN,
    "LEAD": "昨晚金价冲到 4146.77 的两周高点又被砸回来，收 4088.80（+0.67%），留了根长上影——不是没人买，是美股 AI 股灾逼得有人卖黄金去补保证金。今早 4076.76（-0.29%），多空都在等今晚 21:30 的 10 月非农。",
    "PRICE_ROWS": "\n".join(price_rows),
    "NEWS_ROWS": "\n".join(news_rows),
    "TREND_ROWS": "\n".join(trend_rows),
    "KNOW_ROWS": "\n".join(know_rows),
    "HERO_NOTE": d["prices"][0]["note"],
    "ADVICE": d["trend"]["advice"],
    "ACT": act,
    "BUY_TRIG": buy["trigger"], "BUY_PRICE": buy["price"], "BUY_REASON": buy["reason"],
    "SELL_TRIG": sell["trigger"], "SELL_PRICE": sell["price"], "SELL_REASON": sell["reason"],
    "PLAN_NOTE": pnote,
    "TEACH_TITLE": d["teach"]["title"],
    "TEACH_BODY": d["teach"]["body"],
    "TEACH_SRC": d["teach"]["source"],
}

html = html % vals
io.open(PATH, "w", encoding="utf-8").write(html)

lines = html.split(chr(10))
print("written", PATH)
print("chars", len(html), "bytes", len(html.encode("utf-8")), "lines", len(lines))
print("max line", max(len(x) for x in lines))
print("double pct left:", html.count("100%%"))
