# -*- coding: utf-8 -*-
"""生成 2026-11-12 早报邮件 HTML。全文 f-string 拼接，零百分号格式化。"""
import json, os, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, "daily", "2026-11-12.json"), encoding="utf-8"))
NL = chr(10)

CLR_UP = "#c62828"
CLR_DOWN = "#2e7d32"

def fmt(lbl, val, unit, chg):
    if chg > 0:
        arrow, c = "▲", CLR_UP
    elif chg < 0:
        arrow, c = "▼", CLR_DOWN
    else:
        arrow, c = "—", "#555555"
    return (
        f'<tr>'
        f'<td style="padding:9px 8px;border-bottom:1px solid #eeeeee;color:#333333;font-size:14px">{lbl}</td>'
        f'<td style="padding:9px 8px;border-bottom:1px solid #eeeeee;text-align:right;font-size:15px;font-weight:600;color:#1a1a1a">{val} <span style="font-size:12px;color:#888888;font-weight:400">{unit}</span></td>'
        f'<td style="padding:9px 8px;border-bottom:1px solid #eeeeee;text-align:right;font-size:14px;font-weight:600;color:{c}">{arrow} {abs(chg):.2f}%</td>'
        f'</tr>' + NL
    )

rows = ""
for p in d["prices"]:
    rows += fmt(p["label"], p["value"], p["unit"], p["change"])

news_html = ""
for i, n in enumerate(d["news"], 1):
    news_html += (
        f'<div style="margin:0 0 16px 0;padding:0 0 0 10px;border-left:3px solid #d4af37">'
        f'<div style="font-size:13px;color:#a8842c;font-weight:600;margin-bottom:4px">[{n["tag"]}]</div>'
        f'<div style="font-size:15px;color:#1a1a1a;font-weight:600;line-height:1.5;margin-bottom:5px">{n["title"]}</div>'
        f'<div style="font-size:13.5px;color:#555555;line-height:1.75">{n["explain"]}</div>'
        f'<div style="font-size:12px;color:#999999;margin-top:4px">来源：{n["source"]}</div>'
        f'</div>' + NL
    )

t = d["trend"]
plan = d["plan"]

html = (
    '<div style="max-width:640px;margin:0 auto;background:#f7f7f5;padding:0 0 24px 0;'
    'font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Microsoft YaHei,sans-serif">' + NL
    + '<div style="background:linear-gradient(135deg,#1a1a1a,#3d3527);padding:26px 24px;text-align:center">' + NL
    + '<div style="color:#d4af37;font-size:12px;letter-spacing:3px">DAILY GOLD BRIEFING</div>' + NL
    + '<div style="color:#ffffff;font-size:23px;font-weight:700;margin-top:8px">今日金价早报</div>' + NL
    + '<div style="color:#bbbbbb;font-size:13px;margin-top:6px">2026 年 11 月 12 日 · 周四</div>' + NL
    + '</div>' + NL
    + '<div style="background:#ffffff;padding:20px 22px;margin:0">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:12px;border-left:4px solid #d4af37;padding-left:9px">金价快照</div>' + NL
    + '<table style="width:100%;border-collapse:collapse">' + NL + rows + '</table>' + NL
    + '<div style="font-size:12px;color:#888888;line-height:1.7;margin-top:12px;padding:10px;background:#faf9f6;border-radius:4px">'
    + d["prices"][0]["note"].replace("三层说明：", "关于积存金这个数字：") + '</div>' + NL
    + '</div>' + NL
    + '<div style="background:#ffffff;padding:20px 22px;margin:14px 0 0 0">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:14px;border-left:4px solid #d4af37;padding-left:9px">昨夜大事</div>' + NL
    + news_html
    + '</div>' + NL
    + '<div style="background:#ffffff;padding:20px 22px;margin:14px 0 0 0">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:12px;border-left:4px solid #d4af37;padding-left:9px">趋势怎么走</div>' + NL
    + f'<div style="font-size:13.5px;color:#444444;line-height:1.9"><b>短线：</b>{t["short"]}</div>' + NL
    + f'<div style="font-size:13.5px;color:#444444;line-height:1.9"><b>中期：</b>{t["mid"]}</div>' + NL
    + f'<div style="font-size:13.5px;color:#444444;line-height:1.9"><b>长期：</b>{t["long"]}</div>' + NL
    + f'<div style="margin-top:12px;padding:12px;background:#fdf8e8;border-radius:4px;font-size:13.5px;color:#5d4a10;line-height:1.8"><b>一句话建议：</b>{t["advice"]}</div>' + NL
    + '</div>' + NL
    + '<div style="background:#ffffff;padding:20px 22px;margin:14px 0 0 0">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:12px;border-left:4px solid #d4af37;padding-left:9px">现在该干嘛（什么价位买 / 什么价位卖）</div>' + NL
    + f'<div style="margin-bottom:14px"><div style="font-size:14px;font-weight:700;color:#2e7d32;margin-bottom:5px">买 · {plan["buy"]["price"]}</div>'
    + f'<div style="font-size:13.5px;color:#555555;line-height:1.75">{plan["buy"]["trigger"]}</div></div>' + NL
    + f'<div style="margin-bottom:14px"><div style="font-size:14px;font-weight:700;color:#c62828;margin-bottom:5px">卖 · {plan["sell"]["price"]}</div>'
    + f'<div style="font-size:13.5px;color:#555555;line-height:1.75">{plan["sell"]["trigger"]}</div></div>' + NL
    + f'<div style="font-size:12px;color:#999999;line-height:1.7;padding-top:10px;border-top:1px dashed #dddddd">{plan["note"]}</div>' + NL
    + '</div>' + NL
    + '<div style="background:#ffffff;padding:20px 22px;margin:14px 0 0 0">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:10px;border-left:4px solid #d4af37;padding-left:9px">今日学一招</div>' + NL
    + f'<div style="font-size:14.5px;font-weight:600;color:#1a1a1a;margin-bottom:8px">{d["teach"]["title"]}</div>' + NL
    + f'<div style="font-size:13.5px;color:#555555;line-height:1.8">{d["teach"]["body"]}</div>' + NL
    + f'<div style="font-size:12px;color:#999999;margin-top:8px">参考：{d["teach"]["source"]}</div>' + NL
    + '</div>' + NL
    + '<div style="text-align:center;padding:22px 20px 0 20px">' + NL
    + '<a href="https://jerry-166.github.io/gold-price-briefing/" style="display:inline-block;background:#1a1a1a;color:#d4af37;text-decoration:none;padding:11px 26px;border-radius:24px;font-size:14px;font-weight:600">查看完整早报与历史走势 →</a>' + NL
    + '<div style="font-size:11px;color:#aaaaaa;margin-top:14px;line-height:1.7">本邮件由自动化程序生成，数据来自公开行情与媒体报道，仅供参考，不构成投资建议。</div>' + NL
    + '</div>' + NL
    + '</div>'
)

html = html.replace("<ol>", '<ol style="margin:6px 0 0 0;padding-left:20px">').replace(
    "<li>", '<li style="margin-bottom:8px">')

out = os.path.join(BASE, ".workbuddy", "outbox")
os.makedirs(out, exist_ok=True)
p = os.path.join(out, "mail-2026-11-12.html")
open(p, "w", encoding="utf-8").write(html)

lines = html.split(NL)
print("chars", len(html), "bytes", len(html.encode("utf-8")), "lines", len(lines), "maxline", max(len(x) for x in lines))
print("has_double_pct", html.count("100%%"))
print("gates_ok", max(len(x) for x in lines) <= 1500 and html.count("100%%") == 0)
print("path", p)
