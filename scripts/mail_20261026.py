# -*- coding: utf-8 -*-
"""生成 2026-10-26 早报邮件 HTML（紧凑版）。"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, "daily", "2026-10-26.json"), encoding="utf-8"))

C = {"up": "#c62828", "down": "#2e7d32", "text": "#262626", "muted": "#8c8c8c",
     "line": "#ececec", "bg": "#faf9f7", "gold": "#a8763e"}


def chg(v):
    color = C["up"] if v > 0 else (C["down"] if v < 0 else C["muted"])
    arrow = "▲" if v > 0 else ("▼" if v < 0 else "—")
    return ('<span style="color:%s;font-weight:600">%s %.2f%%</span>' % (color, arrow, abs(v)))


rows = []
for p in d["prices"]:
    hero = p.get("hero")
    label = p["label"] + ("（估算）" if hero else "")
    rows.append(
        '<tr>'
        '<td style="padding:11px 0;border-bottom:1px solid %s;font-size:14px;color:%s">%s</td>'
        '<td style="padding:11px 0;border-bottom:1px solid %s;text-align:right;font-size:%s;font-weight:%s;color:%s">%s <span style="font-size:11px;color:%s;font-weight:400">%s</span></td>'
        '<td style="padding:11px 0;border-bottom:1px solid %s;text-align:right;font-size:13px;width:88px">%s</td>'
        '</tr>' % (C["line"], C["text"], label,
                   C["line"], "19px" if hero else "16px", "700" if hero else "600",
                   C["gold"] if hero else C["text"], p["value"], C["muted"], p["unit"],
                   C["line"], chg(p["change"]))
    )

news_html = []
for n in d["news"][:5]:
    news_html.append(
        '<div style="margin:0 0 14px;padding-left:10px;border-left:2px solid #e8e0d4">'
        '<div style="font-size:11px;color:%s;letter-spacing:1px;margin-bottom:4px">%s</div>'
        '<div style="font-size:14px;font-weight:600;color:%s;line-height:1.55;margin-bottom:5px">%s</div>'
        '<div style="font-size:13px;color:#595959;line-height:1.7">%s</div>'
        '<div style="font-size:11px;color:%s;margin-top:4px">来源：%s</div>'
        '</div>' % (C["gold"], n["tag"], C["text"], n["title"], n["explain"], C["muted"], n["source"])
    )

kn_html = []
for k in d["knowledge"][:3]:
    kn_html.append(
        '<div style="margin-bottom:12px">'
        '<div style="font-size:14px;font-weight:600;color:%s;line-height:1.5">%s</div>'
        '<div style="font-size:13px;color:#595959;line-height:1.7;margin-top:3px">%s</div>'
        '</div>' % (C["text"], k["title"], k["summary"])
    )

H = """<!DOCTYPE html>
<html><body style="margin:0;padding:0;background:%(bg)s">
<div style="max-width:600px;margin:0 auto;background:#fff;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif">

<div style="padding:26px 24px 20px;background:#fdfbf7;border-bottom:1px solid %(line)s">
  <div style="font-size:11px;letter-spacing:2px;color:%(gold)s;margin-bottom:6px">GOLD BRIEFING · 每日金价早报</div>
  <div style="font-size:22px;font-weight:700;color:%(text)s;line-height:1.35">2026 年 10 月 26 日 · 周一</div>
  <div style="font-size:13px;color:%(muted)s;margin-top:6px">4000 得而复失，多空在 30 美元窄缝里死磕</div>
</div>

<div style="padding:18px 24px">
  <div style="font-size:12px;color:%(muted)s;line-height:1.7;background:#f7f7f5;padding:11px 13px;border-radius:4px">
    本周是<span style="color:%(text)s;font-weight:600">超级央行周</span>：周四（10/29）凌晨美联储决议，同日美国三季度 GDP 初值与 9 月 PCE 一起落地。方向大概率要等这两件事给出，中间别押单边。
  </div>
</div>

<div style="padding:0 24px">
  <div style="font-size:13px;font-weight:700;color:%(gold)s;letter-spacing:1px;margin-bottom:4px">金价快照</div>
  <table style="width:100%%;border-collapse:collapse">%(rows)s</table>
  <div style="font-size:11px;color:%(muted)s;line-height:1.7;margin-top:8px">
    涨跌幅＝当前价 vs 上一交易日收盘/昨结；积存金为「伦敦金 × 中间价 6.7162 ÷ 31.1035」估算值，实际以银行挂牌为准。
  </div>
</div>

<div style="padding:22px 24px 0">
  <div style="font-size:13px;font-weight:700;color:%(gold)s;letter-spacing:1px;margin-bottom:12px">昨夜与今晨大事</div>
  %(news)s
</div>

<div style="padding:6px 24px 0">
  <div style="font-size:13px;font-weight:700;color:%(gold)s;letter-spacing:1px;margin-bottom:10px">趋势判断</div>
  <table style="width:100%%;border-collapse:collapse;font-size:13px;color:#595959;line-height:1.7">
    <tr><td style="padding:5px 10px 5px 0;width:52px;color:%(text)s;font-weight:600">短期</td><td>%(short)s</td></tr>
    <tr><td style="padding:5px 10px 5px 0;color:%(text)s;font-weight:600">中期</td><td>%(mid)s</td></tr>
    <tr><td style="padding:5px 10px 5px 0;color:%(text)s;font-weight:600">长期</td><td>%(long)s</td></tr>
  </table>
  <div style="margin-top:10px;font-size:13px;line-height:1.75;color:%(text)s;background:#fdf7ee;padding:12px 14px;border-radius:4px">%(advice)s</div>
</div>

<div style="padding:22px 24px 0">
  <div style="font-size:13px;font-weight:700;color:%(gold)s;letter-spacing:1px;margin-bottom:12px">什么时候买、什么时候卖</div>
  <div style="font-size:13px;line-height:1.8;color:#595959">
    <div style="margin-bottom:12px"><span style="color:%(up)s;font-weight:700">买入信号</span><br>%(buy)s</div>
    <div><span style="color:%(down)s;font-weight:700">卖出/止盈</span><br>%(sell)s</div>
  </div>
  <div style="font-size:11px;color:%(muted)s;line-height:1.7;margin-top:12px;padding-top:10px;border-top:1px solid %(line)s">%(note)s</div>
</div>

<div style="padding:22px 24px 0">
  <div style="font-size:13px;font-weight:700;color:%(gold)s;letter-spacing:1px;margin-bottom:10px">今日学一招</div>
  <div style="font-size:14px;font-weight:600;color:%(text)s;line-height:1.55;margin-bottom:8px">%(t_title)s</div>
  <div style="font-size:13px;color:#595959;line-height:1.8">%(t_body)s</div>
</div>

<div style="padding:22px 24px 0">
  <div style="font-size:13px;font-weight:700;color:%(gold)s;letter-spacing:1px;margin-bottom:10px">也值得知道</div>
  %(kn)s
</div>

<div style="padding:24px;margin-top:22px;background:#fdfbf7;border-top:1px solid %(line)s;text-align:center">
  <a href="https://jerry-166.github.io/gold-price-briefing/" style="display:inline-block;padding:10px 22px;background:%(gold)s;color:#fff;text-decoration:none;border-radius:4px;font-size:13px">查看完整早报与 30 日走势图</a>
  <div style="font-size:11px;color:%(muted)s;line-height:1.7;margin-top:14px">
    数据来源：金投网现货黄金 · 上海黄金交易所 · 中国外汇交易中心 · 新华财经 · 金十数据<br>
    本邮件由自动化流程生成，仅供参考，不构成投资建议。
  </div>
</div>

</div></body></html>"""

teach_body = d["teach"]["body"].replace("<ol>", '<ol style="padding-left:20px;margin:0">').replace(
    "<li>", '<li style="margin-bottom:9px">')

html = H % {
    "bg": C["bg"], "line": C["line"], "text": C["text"], "muted": C["muted"], "gold": C["gold"],
    "up": C["up"], "down": C["down"],
    "rows": "".join(rows), "news": "".join(news_html), "kn": "".join(kn_html),
    "short": d["trend"]["short"], "mid": d["trend"]["mid"], "long": d["trend"]["long"],
    "advice": d["trend"]["advice"],
    "buy": d["plan"]["buy"]["trigger"],
    "sell": d["plan"]["sell"]["trigger"],
    "note": d["plan"]["note"],
    "t_title": d["teach"]["title"], "t_body": teach_body,
}

os.makedirs(os.path.join(BASE, ".workbuddy", "outbox"), exist_ok=True)
out = os.path.join(BASE, ".workbuddy", "outbox", "2026-10-26-morning.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("bytes", len(html.encode("utf-8")), out)
