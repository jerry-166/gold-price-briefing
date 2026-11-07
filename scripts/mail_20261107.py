# -*- coding: utf-8 -*-
"""生成 2026-11-07 早报邮件 HTML。用法：python scripts/mail_20261107.py"""
import json, os

d = json.load(open("daily/2026-11-07.json", encoding="utf-8"))
p = {x["label"]: x for x in d["prices"]}
hero = p["招行积存金买入价"]
au = p["上海金 AU9999"]
fx = p["美元汇率"]
spot = p["伦敦金 XAUUSD"]

UP = "#c0392b"
DOWN = "#1e8449"
FLAT = "#7f8c8d"


def col(ch):
    if ch > 0:
        return UP
    if ch < 0:
        return DOWN
    return FLAT


def arrow(ch):
    if ch > 0:
        return "▲"
    if ch < 0:
        return "▼"
    return "—"


L = []
A = L.append

A('<!DOCTYPE html>')
A('<html><head><meta charset="utf-8"></head>')
A('<body style="margin:0;padding:0;background:#f4f5f7;">')
A('<div style="max-width:640px;margin:0 auto;padding:24px 16px;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;color:#22272e;font-size:15px;line-height:1.75;">')

A('<div style="background:linear-gradient(135deg,#1f2d3d,#3d4f66);border-radius:14px;padding:22px 22px 18px;color:#fff;">')
A('<div style="font-size:13px;letter-spacing:2px;opacity:.75;">GOLD BRIEFING · 2026 年 11 月 7 日 周六</div>')
A('<div style="font-size:24px;font-weight:700;margin-top:6px;">🌅 今日金价早报</div>')
A('<div style="font-size:14px;opacity:.88;margin-top:8px;">周六休市，价格沿用周五纽约收盘。非农 16.5 万砸出 4026，又被买回 4070——这周多空各打一枪。</div>')
A('</div>')

# 快照
A('<div style="background:#fff;border-radius:14px;padding:6px 18px 14px;margin-top:14px;">')
A('<div style="font-size:16px;font-weight:700;padding:14px 0 6px;border-bottom:1px solid #eef0f3;">📊 金价快照</div>')
A('<table style="width:100%;border-collapse:collapse;font-size:14px;">')
rows = [
    ("招行积存金（估算）", hero["value"] + " 元/克", hero["change"], "按中间价折算，实际以挂牌为准"),
    ("上海金 AU9999", au["value"] + " 元/克", au["change"], "夜盘收盘，归属 11-09"),
    ("伦敦金 XAUUSD", spot["value"] + " 美元/盎司", spot["change"], "周五纽约收盘"),
    ("美元中间价", fx["value"] + " USD/CNY", fx["change"], "周六不公布，沿用 11-06"),
]
for name, val, ch, memo in rows:
    c = col(ch)
    A('<tr>')
    A('<td style="padding:10px 0;border-bottom:1px solid #f2f4f7;">' + name + '<br><span style="color:#8a94a6;font-size:12px;">' + memo + '</span></td>')
    A('<td style="padding:10px 0;border-bottom:1px solid #f2f4f7;text-align:right;font-weight:700;">' + val + '</td>')
    A('<td style="padding:10px 0 10px 12px;border-bottom:1px solid #f2f4f7;text-align:right;color:' + c + ';font-weight:700;white-space:nowrap;">' + arrow(ch) + ' ' + ("%.2f" % ch) + '%</td>')
    A('</tr>')
A('</table>')
A('<div style="background:#f8f9fb;border-radius:10px;padding:12px 14px;margin-top:12px;font-size:13px;color:#5b6573;line-height:1.7;">'
  '一句话解释数字为什么这么“别扭”：昨天早报的 880.4 是 09:23 的盘中快照，周五真实收盘只有 4070.75，差 1.3 元/克。所以今天 879.1 比 880.4 只低 1.3 元，这 1.3 元是把昨天记高的补回去，不是今天又跌了。</div>')
A('</div>')

# 昨夜大事
A('<div style="background:#fff;border-radius:14px;padding:6px 18px 14px;margin-top:14px;">')
A('<div style="font-size:16px;font-weight:700;padding:14px 0 6px;border-bottom:1px solid #eef0f3;">🌙 昨夜大事</div>')
for n in d["news"]:
    A('<div style="padding:12px 0;border-bottom:1px solid #f4f6f8;">')
    A('<div style="font-size:12px;color:#8a94a6;">【' + n["tag"] + '】</div>')
    A('<div style="font-weight:700;margin-top:2px;">' + n["title"] + '</div>')
    A('<div style="color:#4a5666;font-size:14px;margin-top:4px;">' + n["explain"] + '</div>')
    A('<div style="font-size:12px;color:#9aa4b2;margin-top:4px;">来源：' + n["source"] + '</div>')
    A('</div>')
A('</div>')

# 趋势
t = d["trend"]
A('<div style="background:#fff;border-radius:14px;padding:6px 18px 14px;margin-top:14px;">')
A('<div style="font-size:16px;font-weight:700;padding:14px 0 6px;border-bottom:1px solid #eef0f3;">🧭 趋势判断 <span style="font-size:12px;color:#8a94a6;font-weight:400;">（观望 watch）</span></div>')
trends = [("短期 1-2 周", t["short"], t["shortVal"]), ("中期 1-3 月", t["mid"], t["midVal"]), ("长期 1 年以上", t["long"], t["longVal"])]
for name, txt, val in trends:
    c = col(val)
    tag = {1: "偏多", 0: "中性", -1: "偏空"}[val]
    A('<div style="padding:10px 0;border-bottom:1px solid #f4f6f8;">')
    A('<div style="font-weight:700;color:' + c + ';">' + name + ' · ' + tag + '</div>')
    A('<div style="color:#4a5666;font-size:14px;margin-top:2px;">' + txt + '</div>')
    A('</div>')
A('</div>')

# 买卖时机
b = d["plan"]["buy"]
s = d["plan"]["sell"]
A('<div style="background:#fff;border-radius:14px;padding:6px 18px 14px;margin-top:14px;">')
A('<div style="font-size:16px;font-weight:700;padding:14px 0 6px;border-bottom:1px solid #eef0f3;">🎯 买卖时机</div>')
A('<div style="padding:12px 0;border-bottom:1px solid #f4f6f8;">')
A('<div style="font-weight:700;color:#1e8449;">买入 · 分两笔</div>')
A('<div style="color:#4a5666;font-size:14px;margin-top:4px;">' + b["trigger"] + '</div>')
A('<div style="background:#eef8f1;border-radius:8px;padding:8px 12px;margin-top:6px;font-size:13px;color:#1e8449;">参考价位：' + b["price"] + '</div>')
A('</div>')
A('<div style="padding:12px 0;border-bottom:1px solid #f4f6f8;">')
A('<div style="font-weight:700;color:#c0392b;">卖出 / 止盈 · 分批</div>')
A('<div style="color:#4a5666;font-size:14px;margin-top:4px;">' + s["trigger"] + '</div>')
A('<div style="background:#fdeeec;border-radius:8px;padding:8px 12px;margin-top:6px;font-size:13px;color:#c0392b;">参考价位：' + s["price"] + '</div>')
A('</div>')
A('<div style="color:#8a94a6;font-size:13px;padding:10px 0 0;">' + d["plan"]["note"] + '</div>')
A('</div>')

# 学一招
A('<div style="background:#fff;border-radius:14px;padding:6px 18px 14px;margin-top:14px;">')
A('<div style="font-size:16px;font-weight:700;padding:14px 0 6px;border-bottom:1px solid #eef0f3;">📚 今日学一招：' + d["teach"]["title"] + '</div>')
A('<div style="color:#4a5666;font-size:14px;padding-top:10px;">' + d["teach"]["body"] + '</div>')
A('<div style="color:#9aa4b2;font-size:12px;padding-top:6px;">参考：' + d["teach"]["source"] + '</div>')
A('</div>')

A('<div style="text-align:center;padding:20px 0 6px;font-size:13px;color:#8a94a6;">')
A('网页版（含 30 日走势图）<br>')
A('<a href="https://jerry-166.github.io/gold-price-briefing/" style="color:#2f6feb;text-decoration:none;">https://jerry-166.github.io/gold-price-briefing/</a>')
A('</div>')
A('<div style="text-align:center;font-size:12px;color:#b3bac4;padding-bottom:8px;">以上内容仅供参考，不构成投资建议。金价有波动，买入需谨慎。</div>')
A('</div></body></html>')

html = "\n".join(L)
os.makedirs(".workbuddy/outbox", exist_ok=True)
out = ".workbuddy/outbox/2026-11-07-morning.html"
open(out, "w", encoding="utf-8").write(html)
print("chars", len(html), "bytes", len(html.encode("utf-8")), "lines", len(L))
print("maxline", max(len(x) for x in L))
print("dblpct", html.count("100%%"), "widths", html.count("width:100%"))
