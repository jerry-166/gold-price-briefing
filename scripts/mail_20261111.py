# -*- coding: utf-8 -*-
"""生成 2026-11-11 早报邮件 HTML。全文 f-string / 字符串拼接，禁用 % 格式化（BUG-017/018/019/021/023）。
每条新闻与每个 tr 末尾显式换行（BUG-024），并打印 chars/bytes/lines/maxline 门禁。
"""
import json, os

DATE = "2026-11-11"
WD = "周三"
d = json.load(open(f"daily/{DATE}.json", encoding="utf-8"))
NL = chr(10)

p = {x["label"]: x for x in d["prices"]}
hero, au, fx, spot = d["prices"][0], d["prices"][1], d["prices"][2], d["prices"][3]

C_RED = "#c0392b"   # 涨（中国习惯：红涨绿跌）
C_GRN = "#1e8449"


def chg(v):
    """涨跌幅着色文本。"""
    if v > 0:
        return f'<span style="color:{C_RED};font-weight:600;">+{v:.2f}%</span>'
    if v < 0:
        return f'<span style="color:{C_GRN};font-weight:600;">{v:.2f}%</span>'
    return f'<span style="color:#666;font-weight:600;">0.00%</span>'


rows = []
rows.append(
    f'<tr><td style="padding:11px 8px;border-bottom:1px solid #eee;font-size:14px;color:#333;">招行积存金（估算）</td>'
    f'<td style="padding:11px 8px;border-bottom:1px solid #eee;text-align:right;font-size:17px;font-weight:700;color:{C_RED};">¥{hero["value"]}</td>'
    f'<td style="padding:11px 8px;border-bottom:1px solid #eee;text-align:right;font-size:14px;">{chg(hero["change"])}</td></tr>' + NL
)
rows.append(
    f'<tr><td style="padding:11px 8px;border-bottom:1px solid #eee;font-size:14px;color:#333;">上海金 AU9999</td>'
    f'<td style="padding:11px 8px;border-bottom:1px solid #eee;text-align:right;font-size:17px;font-weight:700;color:{C_GRN};">¥{au["value"]}</td>'
    f'<td style="padding:11px 8px;border-bottom:1px solid #eee;text-align:right;font-size:14px;">{chg(au["change"])}</td></tr>' + NL
)
rows.append(
    f'<tr><td style="padding:11px 8px;border-bottom:1px solid #eee;font-size:14px;color:#333;">伦敦金 XAUUSD</td>'
    f'<td style="padding:11px 8px;border-bottom:1px solid #eee;text-align:right;font-size:17px;font-weight:700;color:{C_RED};">${spot["value"]}</td>'
    f'<td style="padding:11px 8px;border-bottom:1px solid #eee;text-align:right;font-size:14px;">{chg(spot["change"])}</td></tr>' + NL
)
rows.append(
    f'<tr><td style="padding:11px 8px;border-bottom:1px solid #eee;font-size:14px;color:#333;">美元中间价</td>'
    f'<td style="padding:11px 8px;border-bottom:1px solid #eee;text-align:right;font-size:17px;font-weight:700;color:#333;">{fx["value"]}</td>'
    f'<td style="padding:11px 8px;border-bottom:1px solid #eee;text-align:right;font-size:14px;">{chg(fx["change"])}</td></tr>' + NL
)
price_rows = "".join(rows)

news_html = []
for i, n in enumerate(d["news"], 1):
    news_html.append(
        f'<div style="margin:0 0 14px 0;padding:12px 14px;background:#fbfbfb;border-left:3px solid #d4af37;border-radius:4px;">' + NL
        + f'<div style="font-size:12px;color:#8a6d3b;font-weight:700;margin-bottom:5px;">{i}. [{n["tag"]}]</div>' + NL
        + f'<div style="font-size:14px;font-weight:700;color:#222;line-height:1.55;margin-bottom:6px;">{n["title"]}</div>' + NL
        + f'<div style="font-size:13px;color:#555;line-height:1.75;">{n["explain"]}</div>' + NL
        + f'<div style="font-size:11px;color:#999;margin-top:6px;">来源：{n["source"]}</div>' + NL
        + '</div>' + NL
    )
news_block = "".join(news_html)

kn_html = []
for k in d["knowledge"]:
    kn_html.append(
        f'<div style="margin:0 0 12px 0;">' + NL
        + f'<div style="font-size:13px;font-weight:700;color:#222;">[{k["cat"]}] {k["title"]}</div>' + NL
        + f'<div style="font-size:12.5px;color:#555;line-height:1.7;margin-top:3px;">{k["detail"]}</div>' + NL
        + '</div>' + NL
    )
kn_block = "".join(kn_html)

teach_body = d["teach"]["body"].replace("<ol>", '<ol style="margin:6px 0 0 0;padding-left:20px;">').replace(
    "<li>", '<li style="font-size:13px;color:#444;line-height:1.8;margin-bottom:8px;">'
)

subject = f"🌅 今日金价早报 | 2026年11月11日 周三"

html = (
    '<div style="max-width:640px;margin:0 auto;padding:22px 18px;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Microsoft YaHei,sans-serif;background:#f5f5f5;">' + NL
    + '<div style="background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.08);">' + NL
    + '<div style="background:linear-gradient(135deg,#1a1a2e 0%,#3d2b1f 100%);padding:24px 22px;text-align:center;">' + NL
    + '<div style="font-size:20px;font-weight:700;color:#f4d35e;letter-spacing:1px;">今日金价早报</div>' + NL
    + f'<div style="font-size:12px;color:#c9b99a;margin-top:6px;">2026 年 11 月 11 日 · 周三 · 11:50 亚市</div>' + NL
    + '</div>' + NL
    + '<div style="padding:18px 20px 6px 20px;">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#222;border-left:4px solid #d4af37;padding-left:9px;margin-bottom:10px;">金价快照</div>' + NL
    + '<table style="width:100%;border-collapse:collapse;margin-bottom:6px;">' + NL
    + price_rows
    + '</table>' + NL
    + '<div style="font-size:11.5px;color:#888;line-height:1.6;margin-top:8px;">' + NL
    + '⚠️ 昨天早报上的 887.6 元/克是按 11-10 上午 11:48 的快照算的，当晚 CPI 超预期把金价砸了 2.61%，真实收盘只折算 870.9 元/克。'
    + '所以别看数字从 887.6 掉到 874.2 就以为又跌了一大截——按收盘对收盘算，今天其实是涨 0.38%。' + NL
    + '</div>' + NL
    + '</div>' + NL
    + '<div style="padding:10px 20px 6px 20px;">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#222;border-left:4px solid #d4af37;padding-left:9px;margin-bottom:10px;">昨夜大事</div>' + NL
    + news_block
    + '</div>' + NL
    + '<div style="padding:10px 20px 6px 20px;">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#222;border-left:4px solid #d4af37;padding-left:9px;margin-bottom:10px;">趋势建议</div>' + NL
    + '<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:10px;">' + NL
    + f'<tr><td style="padding:7px 0;width:64px;color:#666;">短线</td><td style="padding:7px 0;color:#333;">{d["trend"]["short"]}</td></tr>' + NL
    + f'<tr><td style="padding:7px 0;color:#666;">中期</td><td style="padding:7px 0;color:#333;">{d["trend"]["mid"]}</td></tr>' + NL
    + f'<tr><td style="padding:7px 0;color:#666;">长线</td><td style="padding:7px 0;color:#333;">{d["trend"]["long"]}</td></tr>' + NL
    + '</table>' + NL
    + f'<div style="background:#fff8e6;border:1px solid #f0d78c;border-radius:6px;padding:12px 14px;font-size:13px;color:#5a4a1f;line-height:1.8;">{d["trend"]["advice"]}</div>' + NL
    + '</div>' + NL
    + '<div style="padding:14px 20px 6px 20px;">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#222;border-left:4px solid #d4af37;padding-left:9px;margin-bottom:10px;">买卖时机</div>' + NL
    + '<div style="background:#f0f8f2;border-radius:6px;padding:12px 14px;margin-bottom:10px;">' + NL
    + '<div style="font-size:13.5px;font-weight:700;color:#1e8449;margin-bottom:5px;">买入 · 等回踩别追</div>' + NL
    + f'<div style="font-size:13px;color:#333;line-height:1.75;">{d["plan"]["buy"]["trigger"]}</div>' + NL
    + f'<div style="font-size:12px;color:#1e8449;font-weight:600;margin-top:6px;">参考价位：{d["plan"]["buy"]["price"]}</div>' + NL
    + '</div>' + NL
    + '<div style="background:#fdf0ee;border-radius:6px;padding:12px 14px;margin-bottom:10px;">' + NL
    + '<div style="font-size:13.5px;font-weight:700;color:#c0392b;margin-bottom:5px;">卖出 · 反弹分批止盈</div>' + NL
    + f'<div style="font-size:13px;color:#333;line-height:1.75;">{d["plan"]["sell"]["trigger"]}</div>' + NL
    + f'<div style="font-size:12px;color:#c0392b;font-weight:600;margin-top:6px;">参考价位：{d["plan"]["sell"]["price"]}</div>' + NL
    + '</div>' + NL
    + f'<div style="font-size:11.5px;color:#888;line-height:1.6;">{d["plan"]["note"]}</div>' + NL
    + '</div>' + NL
    + '<div style="padding:14px 20px 6px 20px;">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#222;border-left:4px solid #d4af37;padding-left:9px;margin-bottom:10px;">今日学一招</div>' + NL
    + f'<div style="font-size:14px;font-weight:700;color:#8a6d3b;margin-bottom:4px;">{d["teach"]["title"]}</div>' + NL
    + teach_body + NL
    + f'<div style="font-size:11px;color:#999;margin-top:8px;">参考：{d["teach"]["source"]}</div>' + NL
    + '</div>' + NL
    + '<div style="padding:14px 20px 6px 20px;">' + NL
    + '<div style="font-size:15px;font-weight:700;color:#222;border-left:4px solid #d4af37;padding-left:9px;margin-bottom:10px;">再多懂一点</div>' + NL
    + kn_block
    + '</div>' + NL
    + '<div style="padding:16px 20px 22px 20px;text-align:center;border-top:1px solid #eee;margin-top:10px;">' + NL
    + '<a href="https://jerry-166.github.io/gold-price-briefing/" style="display:inline-block;padding:11px 26px;background:#1a1a2e;color:#f4d35e;text-decoration:none;border-radius:22px;font-size:13px;font-weight:600;">查看完整日报与历史图表 →</a>' + NL
    + '<div style="font-size:11px;color:#aaa;margin-top:12px;line-height:1.7;">数据来源：新浪财经 · 上海黄金交易所 · 中国外汇交易中心 · 汇通财经 · 金十数据' + NL
    + '<br>本邮件仅供参考，不构成投资建议</div>' + NL
    + '</div>' + NL
    + '</div>' + NL
    + '</div>' + NL
)

os.makedirs(".workbuddy/outbox", exist_ok=True)
outp = f".workbuddy/outbox/mail-{DATE}.html"
open(outp, "w", encoding="utf-8").write(html)

lines = html.split(NL)
maxline = max(len(x) for x in lines)
print("subject:", subject)
print("chars", len(html), "| bytes", len(html.encode("utf-8")), "| lines", len(lines), "| maxline", maxline)
print("bad_100pw", html.count("100%%"))
print("width100_occurrences", html.count("width:100%"))
print("outfile", outp)
assert maxline <= 1500, f"maxline too long: {maxline}"
assert "100%%" not in html
print("GATE OK")
