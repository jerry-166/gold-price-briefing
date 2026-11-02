# -*- coding: utf-8 -*-
"""生成 2026-11-02 早报邮件 HTML（紧凑版，每条新闻独立成行，便于回读直传）。"""
import json, io, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(io.open(os.path.join(BASE, "daily", "2026-11-02.json"), encoding="utf-8"))
OUT = os.path.join(BASE, ".workbuddy", "outbox", "2026-11-02-morning.html")

C = {
    "gold": "#B8860B", "red": "#C0392B", "green": "#1E8449",
    "ink": "#1f2328", "sub": "#57606a", "line": "#e5e7eb", "bg": "#faf8f3",
}


def chg(v, unit=""):
    if v > 0:
        return '<span style="color:%s">▲ %+.2f%s</span>' % (C["red"], v, unit)
    if v < 0:
        return '<span style="color:%s">▼ %.2f%s</span>' % (C["green"], v, unit)
    return '<span style="color:%s">0.00%s</span>' % (C["sub"], unit)


P = []
P.append('<div style="background:%s;padding:22px 20px 16px;border-bottom:3px solid %s;">' % (C["bg"], C["gold"]))
P.append('<div style="font-size:12px;color:%s;letter-spacing:2px;">GOLD DAILY BRIEF</div>' % C["sub"])
P.append('<div style="font-size:21px;font-weight:700;color:%s;margin-top:6px;">今日金价早报 · 2026年11月2日 周一</div>' % C["ink"])
P.append('</div>')

P.append('<div style="padding:18px 20px 4px;">')
P.append('<div style="font-size:14px;font-weight:700;color:%s;border-left:3px solid %s;padding-left:8px;margin-bottom:10px;">金价快照</div>' % (C["ink"], C["gold"]))
P.append('<table style="width:100%;border-collapse:collapse;font-size:13px;">')
for pr in d["prices"]:
    bg = "background:#fffbf0;" if pr.get("hero") else ""
    star = " ⭐" if pr.get("hero") else ""
    P.append('<tr style="%s"><td style="padding:7px 4px;border-bottom:1px solid %s;color:%s;">%s%s</td>'
             '<td style="padding:7px 4px;border-bottom:1px solid %s;text-align:right;font-weight:700;color:%s;">%s</td>'
             '<td style="padding:7px 4px;border-bottom:1px solid %s;text-align:right;font-size:12px;">%s</td>'
             '<td style="padding:7px 4px;border-bottom:1px solid %s;text-align:right;font-size:11px;color:%s;">%s</td></tr>'
             % (bg, C["line"], C["ink"], pr["label"], star, C["line"], C["ink"], pr["value"],
                C["line"], chg(pr["change"], "%"), C["line"], C["sub"], pr["unit"]))
P.append('</table>')
P.append('<div style="font-size:11px;color:%s;margin-top:6px;line-height:1.7;">积存金为估算值（伦敦金×中间价÷31.1035），实际以银行挂牌为准。</div>' % C["sub"])
P.append('</div>')

P.append('<div style="padding:16px 20px 4px;">')
P.append('<div style="font-size:14px;font-weight:700;color:%s;border-left:3px solid %s;padding-left:8px;margin-bottom:10px;">昨夜与今晨大事</div>' % (C["ink"], C["gold"]))
for n in d["news"]:
    P.append('<div style="margin-bottom:12px;padding-bottom:10px;border-bottom:1px dashed %s;">' % C["line"])
    P.append('<div style="font-size:13px;font-weight:700;color:%s;line-height:1.6;"><span style="background:%s;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;margin-right:6px;">%s</span>%s</div>' % (C["ink"], C["gold"], n["tag"], n["title"]))
    P.append('<div style="font-size:12px;color:%s;line-height:1.8;margin-top:4px;">%s</div>' % (C["sub"], n["explain"]))
    P.append('</div>')

P.append('<div style="padding:4px 20px 4px;">')
P.append('<div style="font-size:14px;font-weight:700;color:%s;border-left:3px solid %s;padding-left:8px;margin-bottom:10px;">趋势判断</div>' % (C["ink"], C["gold"]))
P.append('<table style="width:100%;border-collapse:collapse;font-size:13px;">')
for lbl, k, vk in (("短期", "short", "shortVal"), ("中期", "mid", "midVal"), ("长期", "long", "longVal")):
    val = d["trend"][vk]
    mark = "偏强 ▲" if val > 0 else ("偏弱 ▼" if val < 0 else "中性 —")
    col = C["red"] if val > 0 else (C["green"] if val < 0 else C["sub"])
    P.append('<tr><td style="padding:7px 4px;border-bottom:1px solid %s;width:56px;font-weight:700;color:%s;">%s</td>'
             '<td style="padding:7px 4px;border-bottom:1px solid %s;width:64px;color:%s;font-size:12px;">%s</td>'
             '<td style="padding:7px 4px;border-bottom:1px solid %s;color:%s;line-height:1.7;font-size:12px;">%s</td></tr>'
             % (C["line"], C["ink"], lbl, C["line"], col, mark, C["line"], C["sub"], d["trend"][k]))
P.append('</table>')
P.append('<div style="margin-top:10px;padding:11px 12px;background:%s;border-radius:5px;font-size:13px;color:%s;line-height:1.8;">%s</div>' % (C["bg"], C["ink"], d["trend"]["advice"]))
P.append('</div>')

P.append('<div style="padding:16px 20px 4px;">')
P.append('<div style="font-size:14px;font-weight:700;color:%s;border-left:3px solid %s;padding-left:8px;margin-bottom:10px;">买卖时机（仅供参考）</div>' % (C["ink"], C["gold"]))
for key, lbl, col in (("buy", "分批买入", C["red"]), ("sell", "分批止盈", C["green"])):
    b = d["plan"][key]
    P.append('<div style="margin-bottom:12px;border-left:3px solid %s;padding-left:10px;">' % col)
    P.append('<div style="font-size:13px;font-weight:700;color:%s;margin-bottom:4px;">%s｜%s</div>' % (col, lbl, b["price"]))
    P.append('<div style="font-size:12px;color:%s;line-height:1.8;">%s</div>' % (C["sub"], b["trigger"]))
    P.append('<div style="font-size:12px;color:%s;margin-top:3px;">理由：%s</div>' % (C["ink"], b["reason"]))
    P.append('</div>')
P.append('<div style="font-size:11px;color:%s;line-height:1.7;margin-top:4px;">%s</div>' % (C["sub"], d["plan"]["note"]))
P.append('</div>')

body = d["teach"]["body"]
items = re.findall(r"<li>(.*?)</li>", body, re.S)
P.append('<div style="padding:16px 20px 4px;">')
P.append('<div style="font-size:14px;font-weight:700;color:%s;border-left:3px solid %s;padding-left:8px;margin-bottom:8px;">今日学一招：%s</div>' % (C["ink"], C["gold"], d["teach"]["title"]))
P.append('<div style="background:#fffdf6;border:1px solid #f0e6cc;border-radius:5px;padding:12px;font-size:12px;color:%s;line-height:1.85;">' % C["ink"])
for i, it in enumerate(items, 1):
    P.append('<div style="margin-bottom:6px;"><b>%d.</b> %s</div>' % (i, it))
P.append('</div>')
P.append('</div>')

P.append('<div style="padding:18px 20px 22px;text-align:center;border-top:1px solid %s;margin-top:14px;">' % C["line"])
P.append('<div style="font-size:12px;color:%s;line-height:1.9;">完整日报与 30 天走势图：<br><a href="https://jerry-166.github.io/gold-price-briefing/" style="color:%s;font-weight:700;text-decoration:none;">jerry-166.github.io/gold-price-briefing</a></div>' % (C["sub"], C["gold"]))
P.append('<div style="font-size:11px;color:%s;margin-top:8px;line-height:1.7;">数据来源：新浪财经实时行情、上海黄金交易所、中国外汇交易中心、财联社、汇通网、金融界。<br>本邮件为自动化生成，仅供参考，不构成投资建议。</div>' % C["sub"])
P.append('</div>')

html = ('<div style="max-width:600px;margin:0 auto;background:#ffffff;border:1px solid %s;'
        'border-radius:8px;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\','
        '\'PingFang SC\',\'Microsoft YaHei\',sans-serif;">\n' % C["line"]) + "\n".join(P) + "\n</div>"

io.open(OUT, "w", encoding="utf-8").write(html)
raw = html.encode("utf-8")
print("written", OUT, len(raw), "bytes", len(html), "chars")
print("maxline", max(len(x) for x in html.split("\n")))
