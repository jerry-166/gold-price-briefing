# -*- coding: utf-8 -*-
"""生成 2026-11-08 早报邮件 HTML（每条新闻独立成行，便于回读直传）。"""
import json, os, re

d = json.load(open("daily/2026-11-08.json", encoding="utf-8"))
p = {x["label"]: x for x in d["prices"]}

def col(ch):
    return "#c0392b" if ch > 0 else ("#1e8449" if ch < 0 else "#666")

def arrow(ch):
    return "▲" if ch > 0 else ("▼" if ch < 0 else "—")

rows = []
for key in ["招行积存金买入价", "上海金 AU9999", "美元汇率", "伦敦金 XAUUSD"]:
    it = p[key]
    rows.append(
        '<tr><td style="padding:7px 0;color:#444;font-size:14px">' + it["label"] + '</td>'
        '<td style="padding:7px 0;text-align:right;font-size:15px;font-weight:600;color:#1b1b1b">'
        + it["value"] + ' <span style="font-size:12px;font-weight:400;color:#888">' + it["unit"] + '</span></td>'
        '<td style="padding:7px 0;text-align:right;font-size:13px;color:' + col(it["change"]) + '">'
        + arrow(it["change"]) + " " + ("%.2f" % abs(it["change"])) + '%</td></tr>'
    )

news_html = []
for n in d["news"]:
    news_html.append(
        '<div style="margin:0 0 14px 0">'
        '<div style="font-size:13px;color:#b8860b;font-weight:600;margin-bottom:3px">【' + n["tag"] + '】</div>'
        '<div style="font-size:14px;font-weight:600;color:#1b1b1b;line-height:1.5;margin-bottom:3px">' + n["title"] + '</div>'
        '<div style="font-size:13px;color:#555;line-height:1.7">' + n["explain"] + '</div>'
        '<div style="font-size:12px;color:#999;margin-top:3px">来源：' + n["source"] + ' · <a href="' + n["url"] + '" style="color:#999">原文</a></div>'
        '</div>'
    )

t = d["trend"]
plan = d["plan"]

html = f'''<div style="max-width:640px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;background:#faf7f2;padding:22px;border-radius:10px">
<div style="text-align:center;padding-bottom:14px;border-bottom:2px solid #e8d9b5">
<div style="font-size:20px;font-weight:700;color:#1b1b1b">🌅 今日金价早报</div>
<div style="font-size:13px;color:#8a7a55;margin-top:6px">2026 年 11 月 8 日 周日 · 休市版</div>
</div>

<div style="background:#fff8e7;border-left:4px solid #d4a017;padding:10px 12px;margin:16px 0;font-size:13px;color:#6b5a2e;line-height:1.6">
今天周日，伦敦金、上金所、外汇交易中心全部休市，盘面没有新价格。下面所有数字都是 <b>周五（11-06）收盘口径</b>，涨跌幅一并沿用、不归零，不是数据没刷新。
</div>

<div style="font-size:15px;font-weight:700;color:#1b1b1b;margin:18px 0 8px">金价快照</div>
<table style="width:100%;border-collapse:collapse;background:#fff;border-radius:8px;padding:6px 14px">
{''.join(rows)}
</table>
<div style="font-size:12px;color:#999;margin-top:6px;line-height:1.6">积存金为估算值（伦敦金 × 中间价 6.7168 ÷ 31.1035），实际以银行挂牌为准；按周五在岸即期 6.6711 折算约 873.1 元/克，与中间价口径差 6.0 元。</div>

<div style="font-size:15px;font-weight:700;color:#1b1b1b;margin:22px 0 10px">周末都发生了啥</div>
{''.join(news_html)}

<div style="font-size:15px;font-weight:700;color:#1b1b1b;margin:22px 0 8px">趋势判断</div>
<div style="background:#fff;border-radius:8px;padding:14px;font-size:13px;color:#444;line-height:1.8">
<div style="margin-bottom:8px"><b>短期（震荡）</b>：{t["short"]}</div>
<div style="margin-bottom:8px"><b>中期（偏空）</b>：{t["mid"]}</div>
<div><b>长期（偏多）</b>：{t["long"]}</div>
</div>

<div style="font-size:15px;font-weight:700;color:#1b1b1b;margin:22px 0 8px">现在该干嘛</div>
<div style="background:#fff;border-radius:8px;padding:14px;font-size:13px;color:#444;line-height:1.75">
<div style="margin-bottom:10px"><span style="background:#e8f5e9;color:#2e7d32;padding:2px 8px;border-radius:4px;font-weight:600">买入</span> {plan["buy"]["trigger"]}<br><span style="color:#888">参考价位：</span>{plan["buy"]["price"]}</div>
<div><span style="background:#fdecea;color:#c0392b;padding:2px 8px;border-radius:4px;font-weight:600">卖出</span> {plan["sell"]["trigger"]}<br><span style="color:#888">参考价位：</span>{plan["sell"]["price"]}</div>
</div>
<div style="font-size:12px;color:#999;margin-top:8px;line-height:1.6">{plan["note"]}</div>

<div style="font-size:15px;font-weight:700;color:#1b1b1b;margin:22px 0 8px">今日学一招：{d["teach"]["title"]}</div>
<div style="background:#fff;border-radius:8px;padding:14px;font-size:13px;color:#444;line-height:1.8">{d["teach"]["body"]}</div>

<div style="text-align:center;margin-top:26px;padding-top:16px;border-top:1px solid #e8d9b5">
<a href="https://jerry-166.github.io/gold-price-briefing/" style="display:inline-block;background:#d4a017;color:#fff;text-decoration:none;padding:10px 22px;border-radius:6px;font-size:14px">查看完整日报与 30 天走势图 →</a>
<div style="font-size:12px;color:#999;margin-top:12px;line-height:1.7">数据来源：新浪财经实时行情、上海黄金交易所、中国外汇交易中心<br>本邮件由自动化任务生成，仅供参考，不构成投资建议</div>
</div>
</div>'''

html = html.replace("><", ">\n<")
os.makedirs(".workbuddy/outbox", exist_ok=True)
out = ".workbuddy/outbox/2026-11-08-morning-briefing.html"
open(out, "w", encoding="utf-8").write(html)
print("written", out, len(html), "bytes")
print("100%% count =", html.count("100%%"))
print([x for x in re.findall(r"width:100[^;\"]*", html)])
