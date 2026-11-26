# -*- coding: utf-8 -*-
"""生成 2026-11-26 早报邮件 HTML 底稿。用 f-string，不用 % 格式化。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
d = json.load(open(ROOT / "daily" / "2026-11-26.json", encoding="utf-8"))
OUT = ROOT / ".workbuddy" / "outbox" / "mail-2026-11-26-morning_briefing.html"
OUT.parent.mkdir(parents=True, exist_ok=True)

p = {x["label"]: x for x in d["prices"]}
hero = p["招行积存金买入价"]
au = p["上海金 AU9999"]
fx = p["美元汇率"]
xau = p["伦敦金 XAUUSD"]


def color(v):
    return "#c0392b" if v > 0 else ("#1e8449" if v < 0 else "#666")


def arrow(v):
    return "▲" if v > 0 else ("▼" if v < 0 else "—")


def chg_txt(v):
    return f"{v:+.2f}%"


def wrap_outside_tags(html, limit=1200):
    """只在标签外换行，避免邮件客户端/Read 单行截断。"""
    out = []
    buf = ""
    in_tag = False
    for ch in html:
        buf += ch
        if ch == "<":
            in_tag = True
        elif ch == ">":
            in_tag = False
        if not in_tag and len(buf) >= limit and ch in "。；：、，）":
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf)
    return "\n".join(out)


TREND_ROWS = [
    ("短线", d["trend"]["short"], d["trend"]["shortVal"]),
    ("中线", d["trend"]["mid"], d["trend"]["midVal"]),
    ("长线", d["trend"]["long"], d["trend"]["longVal"]),
]
TREND_WORD = {1: "偏多", 0: "中性", -1: "偏空"}
ACTION_WORD = {"hold": "持有", "buy": "买入", "watch": "观望"}

rows_price = ""
for it in d["prices"]:
    tag = "（估算）" if it.get("hero") else ""
    rows_price += (
        f'<tr><td style="padding:9px 0;border-bottom:1px solid #eee;font-size:13px;color:#333">{it["label"]}{tag}</td>'
        f'<td style="padding:9px 0;border-bottom:1px solid #eee;text-align:right;font-size:15px;font-weight:600;color:#1a1a1a">'
        f'{it["value"]}&nbsp;<span style="font-size:11px;color:#888;font-weight:400">{it["unit"]}</span></td>'
        f'<td style="padding:9px 0;border-bottom:1px solid #eee;text-align:right;font-size:13px;color:{color(it["change"])};width:74px">'
        f'{arrow(it["change"])} {chg_txt(it["change"])}</td></tr>\n'
    )

news_html = ""
for i, n in enumerate(d["news"], 1):
    news_html += (
        f'<div style="margin:0 0 16px 0">'
        f'<span style="display:inline-block;background:#f6efe2;color:#8a6d3b;font-size:11px;padding:2px 7px;border-radius:3px">{n["tag"]}</span>'
        f'<div style="font-size:14px;font-weight:600;color:#1a1a1a;margin:6px 0 5px;line-height:1.6">{i}. {n["title"]}</div>'
        f'<div style="font-size:13px;color:#555;line-height:1.75">{n["explain"]}</div>'
        f'<div style="font-size:11px;color:#999;margin-top:4px">来源：{n["source"]} · '
        f'<a href="{n["url"]}" style="color:#b8860b;text-decoration:none">原文</a></div></div>\n'
    )

trend_html = ""
for name, txt, val in TREND_ROWS:
    trend_html += (
        f'<tr><td style="padding:7px 0;font-size:13px;color:#666;width:52px;vertical-align:top">{name}</td>'
        f'<td style="padding:7px 0;font-size:13px;color:{color(val)};width:52px;vertical-align:top">{TREND_WORD[val]}</td>'
        f'<td style="padding:7px 0;font-size:13px;color:#333;line-height:1.7">{txt}</td></tr>\n'
    )

BODY = f'''<div style="margin:0;padding:0;background:#f4f1ea">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f4f1ea;padding:18px 0">
<tr><td align="center">
<table width="640" cellpadding="0" cellspacing="0" border="0" style="width:640px;max-width:640px;background:#ffffff;border-radius:8px;overflow:hidden;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif">

<tr><td style="background:#1a1a1a;padding:22px 26px">
<div style="font-size:11px;color:#b8860b;letter-spacing:2px">GOLD PRICE BRIEFING</div>
<div style="font-size:21px;color:#ffffff;font-weight:600;margin-top:6px">🌅 今日金价早报 · 2026年11月26日 周四</div>
<div style="font-size:12px;color:#999;margin-top:6px">更新 09:00 · 数据截至 10:46 亚市 · 面向小白的大白话解读</div>
</td></tr>

<tr><td style="padding:22px 26px 6px">
<div style="font-size:13px;color:#666;line-height:1.75">昨夜是名副其实的过山车：21:30 美国 10 月核心 PCE 同比 <b>3.3%</b> 高出预期 0.1 个百分点、创 2023 年 11 月以来最高，金价一度跌超 3%，最低砸到 <b>3426.64</b>——2025 年 9 月以来第一次跌破 3500，创逾一年新低；随后逢低买盘与感恩节前空头回补把价格拉回 <b>3588.55</b>，收涨 0.92%。今早亚市站上 <b>3601</b>、最高摸到 3607。但要看清：CME 显示 <b>12 月加息概率已到 97.2%</b>，这波是修复、不是转向。今天感恩节美股债休市、盘口薄，别用大仓位赌方向。</div>
</td></tr>

<tr><td style="padding:10px 26px 4px">
<div style="font-size:12px;color:#b8860b;font-weight:600;letter-spacing:1px;margin-bottom:4px">金价快照</div>
<table width="100%" cellpadding="0" cellspacing="0" border="0">{rows_price}</table>
<div style="font-size:11px;color:#999;line-height:1.7;margin-top:8px">注：积存金为按中间价折算的估算值，实际以银行挂牌为准；昨早报写的 766.0 是 11:27 盘中快照，按 11-25 真实收盘 3588.55 折算应为 774.0，本期已回填，所以今天与 774.0 的 +3.0 元/克才是干净差额。AU9999 的涨跌幅把夜盘一并计入（夜盘最低 736.51），与伦敦金的日内涨幅不能直接相减。</div>
</td></tr>

<tr><td style="padding:18px 26px 4px">
<div style="font-size:12px;color:#b8860b;font-weight:600;letter-spacing:1px;margin-bottom:10px">昨夜大事</div>
{news_html}</td></tr>

<tr><td style="padding:14px 26px 4px">
<div style="font-size:12px;color:#b8860b;font-weight:600;letter-spacing:1px;margin-bottom:8px">趋势判断 · 当前建议：{ACTION_WORD[d["trend"]["action"]]}</div>
<table width="100%" cellpadding="0" cellspacing="0" border="0">{trend_html}</table>
<div style="margin-top:10px;padding:12px 14px;background:#faf7f0;border-radius:6px;font-size:13px;color:#333;line-height:1.8">{d["trend"]["advice"]}</div>
</td></tr>

<tr><td style="padding:20px 26px 4px">
<div style="font-size:12px;color:#b8860b;font-weight:600;letter-spacing:1px;margin-bottom:10px">买卖时机</div>
<table width="100%" cellpadding="0" cellspacing="0" border="0">
<tr><td style="padding:12px 14px;background:#fdf6f5;border-radius:6px 6px 0 0;border-left:3px solid #c0392b">
<div style="font-size:13px;font-weight:600;color:#c0392b;margin-bottom:5px">买入 · {d["plan"]["buy"]["price"]}</div>
<div style="font-size:13px;color:#444;line-height:1.75">{d["plan"]["buy"]["trigger"]}</div>
<div style="font-size:12px;color:#888;margin-top:5px">为什么：{d["plan"]["buy"]["reason"]}</div></td></tr>
<tr><td style="padding:12px 14px;background:#f4f8f5;border-radius:0 0 6px 6px;border-left:3px solid #1e8449;border-top:1px solid #fff">
<div style="font-size:13px;font-weight:600;color:#1e8449;margin-bottom:5px">卖出 · {d["plan"]["sell"]["price"]}</div>
<div style="font-size:13px;color:#444;line-height:1.75">{d["plan"]["sell"]["trigger"]}</div>
<div style="font-size:12px;color:#888;margin-top:5px">为什么：{d["plan"]["sell"]["reason"]}</div></td></tr>
</table>
<div style="font-size:11px;color:#999;line-height:1.7;margin-top:8px">{d["plan"]["note"]}</div>
</td></tr>

<tr><td style="padding:20px 26px 4px">
<div style="font-size:12px;color:#b8860b;font-weight:600;letter-spacing:1px;margin-bottom:8px">今日学一招</div>
<div style="font-size:14px;font-weight:600;color:#1a1a1a;margin-bottom:7px">{d["teach"]["title"]}</div>
<div style="font-size:13px;color:#444;line-height:1.85">{d["teach"]["body"]}</div>
<div style="font-size:11px;color:#999;margin-top:6px">参考：{d["teach"]["source"]}</div>
</td></tr>

<tr><td style="padding:20px 26px 26px">
<table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td align="center" style="padding:14px;background:#faf7f0;border-radius:6px">
<a href="https://jerry-166.github.io/gold-price-briefing/" style="font-size:13px;color:#b8860b;text-decoration:none;font-weight:600">查看完整日报与 30 日走势图 →</a>
<div style="font-size:11px;color:#999;margin-top:5px">jerry-166.github.io/gold-price-briefing</div>
</td></tr></table>
<div style="font-size:11px;color:#aaa;line-height:1.7;margin-top:14px;text-align:center">本邮件由自动化程序生成，所有价位与判断仅供参考，不构成投资建议。<br>行情波动剧烈时请以交易平台实时报价为准。</div>
</td></tr>

</table></td></tr></table></div>'''

html = wrap_outside_tags(BODY)
OUT.write_text(html, encoding="utf-8")

maxline = max(len(x) for x in html.split("\n"))
print("bytes", len(html.encode("utf-8")), "| maxline", maxline)
print("path", OUT)
assert "100%%" not in html
assert html.count("width:100%") == 0
print("grep 100%% ->", html.count("100%%"))
