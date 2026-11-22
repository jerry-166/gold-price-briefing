# -*- coding: utf-8 -*-
"""生成 2026-11-22 早报邮件 HTML（每条新闻独立成行 + 标签外换行，不用 % 格式化）。"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, "daily", "2026-11-22.json"), encoding="utf-8"))

p = d["prices"]
hero, au, fx, xau = p[0], p[1], p[2], p[3]

TAG_COLOR = {"fed": "#b3261e", "geo": "#8a5a00", "fx": "#1b5e20", "data": "#37474f"}
TAG_BG = {"fed": "#fdecea", "geo": "#fff6e0", "fx": "#e8f5e9", "data": "#eceff1"}


def chg_html(c):
    if c > 0:
        return '<span style="color:#c62828;font-weight:600;">' + ("+%.2f" % c) + "%</span>"
    if c < 0:
        return '<span style="color:#2e7d32;font-weight:600;">' + ("%.2f" % c) + "%</span>"
    return '<span style="color:#757575;font-weight:600;">0.00%</span>'


rows = []
for label, val, unit, change in [
    ("招行积存金买入价（估算）", hero["value"], "元/克", hero["change"]),
    ("上海金 AU9999", au["value"], "元/克", au["change"]),
    ("伦敦金 XAUUSD", xau["value"], "美元/盎司", xau["change"]),
    ("美元人民币中间价", fx["value"], "—", fx["change"]),
]:
    rows.append(
        '<tr>'
        '<td style="padding:9px 10px;border-bottom:1px solid #eee;font-size:14px;color:#333;">' + label + "</td>"
        '<td style="padding:9px 10px;border-bottom:1px solid #eee;font-size:16px;font-weight:700;color:#111;text-align:right;">' + val + "</td>"
        '<td style="padding:9px 10px;border-bottom:1px solid #eee;font-size:12px;color:#888;text-align:right;">' + unit + "</td>"
        '<td style="padding:9px 10px;border-bottom:1px solid #eee;font-size:13px;text-align:right;">' + chg_html(change) + "</td>"
        "</tr>"
    )
price_rows = "\n".join(rows)

news_rows = []
for n in d["news"]:
    tc, tb = TAG_COLOR[n["tagType"]], TAG_BG[n["tagType"]]
    news_rows.append(
        '<div style="margin:0 0 14px 0;padding:0 0 12px 0;border-bottom:1px dashed #e6e6e6;">'
        '<div style="margin:0 0 6px 0;">'
        '<span style="display:inline-block;padding:2px 8px;border-radius:10px;background:' + tb + ";color:" + tc + ';font-size:11px;font-weight:600;margin-right:6px;">' + n["tag"] + "</span>"
        '<span style="font-size:14px;font-weight:700;color:#1a1a1a;">' + n["title"] + "</span>"
        "</div>"
        '<div style="font-size:13px;line-height:1.75;color:#555;">' + n["explain"] + "</div>"
        '<div style="font-size:11px;color:#999;margin-top:4px;">来源：<a href="' + n["url"] + '" style="color:#8a6d3b;text-decoration:none;">' + n["source"] + "</a></div>"
        "</div>"
    )
news_blocks = "\n".join(news_rows)

kn_rows = []
for k in d["knowledge"]:
    kn_rows.append(
        '<div style="margin:0 0 10px 0;font-size:13px;line-height:1.7;color:#444;">'
        '<span style="color:#8a6d3b;font-weight:600;">[' + k["cat"] + "]</span> " + k["title"]
        + '<div style="color:#666;font-size:12px;margin-top:2px;">' + k["summary"] + "</div>"
        "</div>"
    )
kn_blocks = "\n".join(kn_rows)

trend_items = [
    ("短期", d["trend"]["short"], d["trend"]["shortVal"]),
    ("中期", d["trend"]["mid"], d["trend"]["midVal"]),
    ("长期", d["trend"]["long"], d["trend"]["longVal"]),
]
tr_rows = []
for name, text, val in trend_items:
    arrow = "偏空" if val < 0 else ("偏多" if val > 0 else "中性")
    color = "#2e7d32" if val < 0 else ("#c62828" if val > 0 else "#757575")
    tr_rows.append(
        '<tr>'
        '<td style="padding:8px 10px;font-size:13px;color:#333;white-space:nowrap;border-bottom:1px solid #f0f0f0;">' + name + "</td>"
        '<td style="padding:8px 10px;font-size:13px;color:' + color + ';font-weight:600;white-space:nowrap;border-bottom:1px solid #f0f0f0;">' + arrow + "</td>"
        '<td style="padding:8px 10px;font-size:13px;line-height:1.7;color:#444;border-bottom:1px solid #f0f0f0;">' + text + "</td>"
        "</tr>"
    )
trend_rows = "\n".join(tr_rows)

WEB = "https://jerry-166.github.io/gold-price-briefing/"
title = "🌅 今日金价早报 | 2026年11月22日 周日"

html = (
    '<div style="margin:0;padding:0;background:#f5f5f5;">'
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f5f5f5;">'
    "<tr><td align=\"center\" style=\"padding:18px 10px;\">"
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
    'style="max-width:640px;background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.06);">'

    # 头部
    "<tr><td style=\"padding:22px 22px 14px 22px;background:linear-gradient(135deg,#3e2b12,#7a5a2e);\">"
    '<div style="font-size:12px;color:#f0d9b5;letter-spacing:2px;">GOLD BRIEFING · 周日休市版</div>'
    '<div style="font-size:22px;font-weight:700;color:#fff;margin-top:6px;">今日金价早报</div>'
    '<div style="font-size:12px;color:#e6d3b8;margin-top:6px;">2026 年 11 月 22 日 周日 · 数据口径：11-20 纽约收盘（国际盘休市至周一 06:00）</div>'
    "</td></tr>"

    # 一句话
    "<tr><td style=\"padding:16px 22px 6px 22px;\">"
    '<div style="font-size:14px;line-height:1.8;color:#333;">'
    "周末两天价格不动：现货金停在 <b>3534.6 美元</b>、周跌 <b>8.91%</b>，盘中最低 3502.73，3500 只差一步没破。"
    "今天没有新行情，但信息不少——Kitco 调查 15 位分析师 9 人看跌，<b>周一 06:00 开盘就会给出 3500 这道关的答案</b>。"
    "</div>"
    "</td></tr>"

    # 快照表
    "<tr><td style=\"padding:10px 22px 4px 22px;\">"
    '<div style="font-size:13px;font-weight:700;color:#7a5a2e;margin-bottom:6px;">金价快照</div>'
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">'
    + price_rows +
    "</table>"
    '<div style="font-size:11px;color:#999;line-height:1.6;margin-top:6px;">'
    "积存金为估算值（伦敦金 × 中间价 ÷ 31.1035），实际以银行挂牌为准；周日国际盘、上金所、外汇交易中心全休，价格与昨日同值、非数据未刷新。"
    "AU9999 取 11-20 夜盘收（归 11-23 交易日），涨跌幅基准为 11-20 日盘收 764.50，与伦敦金的时段不对齐，两个数不能直接比。"
    "</div>"
    "</td></tr>"

    # 盘外动静
    "<tr><td style=\"padding:16px 22px 4px 22px;\">"
    '<div style="font-size:13px;font-weight:700;color:#7a5a2e;margin-bottom:10px;">昨夜大事与下周看点（周末盘外）</div>'
    + news_blocks +
    "</td></tr>"

    # 趋势
    "<tr><td style=\"padding:6px 22px 4px 22px;\">"
    '<div style="font-size:13px;font-weight:700;color:#7a5a2e;margin-bottom:6px;">趋势判断</div>'
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">'
    + trend_rows +
    "</table>"
    "</td></tr>"

    # 买卖
    "<tr><td style=\"padding:14px 22px 4px 22px;\">"
    '<div style="font-size:13px;font-weight:700;color:#7a5a2e;margin-bottom:8px;">现在该干嘛：什么价位买、什么价位卖</div>'
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
    '<tr><td style="padding:0 0 10px 0;">'
    '<div style="background:#f1f8f2;border-left:4px solid #2e7d32;padding:10px 12px;border-radius:0 8px 8px 0;">'
    '<div style="font-size:13px;font-weight:700;color:#1b5e20;margin-bottom:4px;">买入时机</div>'
    '<div style="font-size:13px;line-height:1.75;color:#333;">' + d["plan"]["buy"]["trigger"] + "</div>"
    '<div style="font-size:13px;line-height:1.75;color:#1b5e20;font-weight:600;margin-top:5px;">价位：' + d["plan"]["buy"]["price"] + "</div>"
    "</div></td></tr>"
    '<tr><td style="padding:0 0 10px 0;">'
    '<div style="background:#fdf0ef;border-left:4px solid #c62828;padding:10px 12px;border-radius:0 8px 8px 0;">'
    '<div style="font-size:13px;font-weight:700;color:#8e1b16;margin-bottom:4px;">卖出 / 止盈止损</div>'
    '<div style="font-size:13px;line-height:1.75;color:#333;">' + d["plan"]["sell"]["trigger"] + "</div>"
    '<div style="font-size:13px;line-height:1.75;color:#8e1b16;font-weight:600;margin-top:5px;">价位：' + d["plan"]["sell"]["price"] + "</div>"
    "</div></td></tr></table>"
    '<div style="font-size:12px;line-height:1.7;color:#8a6d3b;background:#fffaf0;padding:9px 12px;border-radius:8px;">'
    "一句话建议：" + d["trend"]["advice"] + "</div>"
    '<div style="font-size:11px;color:#999;margin-top:6px;">' + d["plan"]["note"] + "</div>"
    "</td></tr>"

    # 今日学一招
    "<tr><td style=\"padding:16px 22px 4px 22px;\">"
    '<div style="background:#f7f4ee;border-radius:10px;padding:14px;">'
    '<div style="font-size:13px;font-weight:700;color:#7a5a2e;margin-bottom:6px;">今日学一招 · ' + d["teach"]["title"] + "</div>"
    '<div style="font-size:13px;line-height:1.8;color:#444;">' + d["teach"]["body"] + "</div>"
    '<div style="font-size:11px;color:#999;margin-top:6px;">参考：' + d["teach"]["source"] + "</div>"
    "</div>"
    "</td></tr>"

    # 延伸
    "<tr><td style=\"padding:14px 22px 4px 22px;\">"
    '<div style="font-size:13px;font-weight:700;color:#7a5a2e;margin-bottom:8px;">再多看三条</div>'
    + kn_blocks +
    "</td></tr>"

    # 页脚
    "<tr><td style=\"padding:16px 22px 22px 22px;border-top:1px solid #f0f0f0;\">"
    '<div style="font-size:12px;line-height:1.8;color:#777;">'
    '完整图表与历史早报：<a href="' + WEB + '" style="color:#7a5a2e;font-weight:600;text-decoration:none;">' + WEB + "</a><br>"
    "数据来源：新浪财经、上海黄金交易所、中国外汇交易中心、澎湃新闻、联合早报、证券时报、腾讯新闻。<br>"
    "本邮件为自动化生成的信息整理，不构成任何投资建议。"
    "</div></td></tr>"

    "</table></td></tr></table></div>"
)


def wrap_outside_tags(s, limit=1200):
    """在标签之外插入换行，保证单行 < 2000 字符（Read 回读不被截断），不破坏 HTML。"""
    out, buf_len, in_tag = [], 0, False
    for ch in s:
        out.append(ch)
        buf_len += 1
        if ch == "<":
            in_tag = True
        elif ch == ">":
            in_tag = False
        elif ch == "\n":
            buf_len = 0
        if buf_len >= limit and not in_tag:
            out.append("\n")
            buf_len = 0
    return "".join(out)


html = wrap_outside_tags(html)

outbox = os.path.join(BASE, ".workbuddy", "outbox")
os.makedirs(outbox, exist_ok=True)
path = os.path.join(outbox, "mail-2026-11-22-morning_briefing.html")
with open(path, "w", encoding="utf-8") as f:
    f.write(html)

assert html.count("%%") == 0, "邮件残留 %%"
assert "width:100%" not in html, "邮件用了 CSS width:100%"
print("subject:", title)
print("html bytes:", len(html), "chars:")
print("max line:", max(len(x) for x in html.split("\n")))
print("outbox:", path)
