# -*- coding: utf-8 -*-
"""生成 2026-11-10 早报邮件 HTML（纯 f-string，无 % 格式化）。"""
import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")

DATE = "2026-11-10"
d = json.load(open(f"daily/{DATE}.json", encoding="utf-8"))

BRAND = "#b8860b"
INK = "#1f2328"
MUTE = "#6b7280"
LINE = "#e5e7eb"
BG = "#faf7f0"

p = {x["label"]: x for x in d["prices"]}


def arrow(ch):
    return "🔺" if ch > 0 else ("🔻" if ch < 0 else "➖")


def color(ch):
    return "#c0392b" if ch > 0 else ("#1e8449" if ch < 0 else MUTE)


def row(label, value, unit, ch, note=""):
    c = color(ch)
    return (
        f'<tr>'
        f'<td style="padding:10px 12px;border-bottom:1px solid {LINE};color:{INK};font-size:14px">{label}</td>'
        f'<td style="padding:10px 12px;border-bottom:1px solid {LINE};text-align:right;color:{INK};'
        f'font-size:16px;font-weight:700;white-space:nowrap">{value}'
        f'<span style="font-size:11px;font-weight:400;color:{MUTE}"> {unit}</span></td>'
        f'<td style="padding:10px 12px;border-bottom:1px solid {LINE};text-align:right;color:{c};'
        f'font-size:14px;font-weight:600;white-space:nowrap">{arrow(ch)} {ch:+.2f}%</td>'
        f'</tr>'
    )


L = []
L.append(f'<div style="background:{BG};padding:24px 12px;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\','
         f'\'PingFang SC\',\'Microsoft YaHei\',sans-serif">')
L.append('<div style="max-width:640px;margin:0 auto;background:#ffffff;border:1px solid '
         + LINE + ';border-radius:14px;overflow:hidden">')

# 头部
L.append('<div style="background:linear-gradient(135deg,#fff8e6 0%,#fdf2d6 100%);'
         'padding:22px 22px 18px;border-bottom:3px solid '
         + BRAND + '">')
L.append('<div style="font-size:12px;letter-spacing:2px;color:' + BRAND + ';font-weight:700">DAILY GOLD BRIEFING</div>')
L.append(f'<div style="font-size:22px;font-weight:800;color:{INK};margin-top:6px">'
         f'🌅 今日金价早报 · 2026年11月10日 周二</div>')
L.append(f'<div style="font-size:12px;color:{MUTE};margin-top:8px">'
         f'本期生成于 11:52（原定 09:00，任务延迟约 168 分钟），以下为 11:48 亚市盘中读数</div>')
L.append('</div>')

L.append('<div style="padding:20px 22px 4px">')

# 一句话结论
L.append(f'<div style="background:#fff8e6;border-left:4px solid {BRAND};padding:12px 14px;'
         f'border-radius:0 8px 8px 0;font-size:14px;color:{INK};line-height:1.7">'
         f'<b>一句话：</b>隔夜油价崩 6% 把金价推上 4140，今早冲到 4146 又被打回来。'
         f'4146 是两道顶，4100 是生命线，今晚 21:30 CPI 才是裁判——现在别追高。</div>')

# 金价快照
L.append(f'<div style="font-size:15px;font-weight:800;color:{INK};margin:20px 0 8px">'
         f'📊 金价快照</div>')
L.append('<table style="width:100%;border-collapse:collapse;border:1px solid ' + LINE + ';border-radius:8px">')
L.append(row("招行积存金买入价（估算）", p["招行积存金买入价"]["value"], "元/克", p["招行积存金买入价"]["change"]))
L.append(row("上海金 AU9999", p["上海金 AU9999"]["value"], "元/克", p["上海金 AU9999"]["change"]))
L.append(row("伦敦金 XAUUSD", p["伦敦金 XAUUSD"]["value"], "美元/盎司", p["伦敦金 XAUUSD"]["change"]))
L.append(row("美元人民币中间价", p["美元汇率"]["value"], "USD/CNY", p["美元汇率"]["change"]))
L.append('</table>')
L.append(f'<div style="font-size:11px;color:{MUTE};margin-top:8px;line-height:1.7">'
         f'积存金＝伦敦金×中间价÷31.1035 估算，实际以招行 App 挂牌为准。'
         f'注：昨天早报的 890.2 元/克是按 09:48 快照算的，昨天真实收盘 4140.94 折算应为 894.5，'
         f'差的 4.3 元今天已补正，所以今天与你记忆里的数字相比只跌 0.26%，真实变化是 -0.77%。</div>')

# 昨夜大事
L.append(f'<div style="font-size:15px;font-weight:800;color:{INK};margin:22px 0 8px">'
         f'🌙 昨夜大事</div>')
for n in d["news"]:
    L.append(f'<div style="margin-bottom:12px;padding-left:12px;border-left:3px solid #f0d79a">')
    L.append(f'<div style="font-size:11px;color:{BRAND};font-weight:700;margin-bottom:3px">'
             f'【{n["tag"]}】{n["source"]}</div>')
    L.append(f'<div style="font-size:14px;font-weight:700;color:{INK};line-height:1.6">{n["title"]}</div>')
    L.append(f'<div style="font-size:13px;color:#444;line-height:1.75;margin-top:4px">{n["explain"]}</div>')
    L.append('</div>')

# 趋势建议
t = d["trend"]
L.append(f'<div style="font-size:15px;font-weight:800;color:{INK};margin:22px 0 8px">'
         f'🧭 趋势判断</div>')
L.append('<table style="width:100%;border-collapse:collapse;font-size:13px;color:' + INK + '">')
for name, key, val in (("短期", "short", t["shortVal"]), ("中期", "mid", t["midVal"]), ("长期", "long", t["longVal"])):
    tag = "偏多" if val > 0 else ("偏空" if val < 0 else "震荡")
    tc = color(val)
    L.append(f'<tr><td style="padding:8px 0;width:52px;color:{MUTE}">{name}</td>'
             f'<td style="padding:8px 0"><span style="color:{tc};font-weight:700">{tag}</span>　'
             f'<span style="color:#333;line-height:1.6">{t[key]}</span></td></tr>')
L.append('</table>')
act = {"hold": "持有观望", "buy": "可以买入", "watch": "先看不动"}[t["action"]]
L.append(f'<div style="margin-top:8px;font-size:13px;color:{INK};background:#f6f8fa;padding:10px 12px;'
         f'border-radius:8px;line-height:1.8"><b>操作方向：{act}</b><br>{t["advice"]}</div>')

# 买卖时机
pl = d["plan"]
L.append(f'<div style="font-size:15px;font-weight:800;color:{INK};margin:22px 0 8px">'
         f'🎯 买卖时机</div>')
L.append(f'<div style="background:#f4faf4;border:1px solid #cfe8cf;border-radius:10px;padding:13px 14px;margin-bottom:10px">')
L.append(f'<div style="font-size:14px;font-weight:800;color:#1e8449;margin-bottom:6px">✅ 什么价位买</div>')
L.append(f'<div style="font-size:13px;color:{INK};line-height:1.8">'
         f'<b>参考价位：</b>{pl["buy"]["price"]}<br>'
         f'<b>怎么操作：</b>{pl["buy"]["trigger"]}<br>'
         f'<b>理由：</b>{pl["buy"]["reason"]}</div>')
L.append('</div>')
L.append(f'<div style="background:#fdf5f4;border:1px solid #f0d2cd;border-radius:10px;padding:13px 14px">')
L.append(f'<div style="font-size:14px;font-weight:800;color:#c0392b;margin-bottom:6px">⚖️ 什么价位卖</div>')
L.append(f'<div style="font-size:13px;color:{INK};line-height:1.8">'
         f'<b>参考价位：</b>{pl["sell"]["price"]}<br>'
         f'<b>怎么操作：</b>{pl["sell"]["trigger"]}<br>'
         f'<b>理由：</b>{pl["sell"]["reason"]}</div>')
L.append('</div>')
L.append(f'<div style="font-size:11px;color:{MUTE};margin-top:10px;line-height:1.7">⚠️ {pl["note"]}</div>')

# 今日学一招
te = d["teach"]
L.append(f'<div style="font-size:15px;font-weight:800;color:{INK};margin:22px 0 8px">'
         f'📚 今日学一招：{te["title"]}</div>')
L.append(f'<div style="background:#f8f9fb;border-radius:10px;padding:14px 16px;font-size:13px;'
         f'color:{INK};line-height:1.85">{te["body"]}</div>')
L.append(f'<div style="font-size:11px;color:{MUTE};margin-top:8px">来源：{te["source"]}</div>')

# 底部
L.append('</div>')
L.append(f'<div style="border-top:1px solid {LINE};background:#fbfbfb;padding:16px 22px;text-align:center">')
L.append(f'<a href="https://jerry-166.github.io/gold-price-briefing/" '
         f'style="display:inline-block;background:{BRAND};color:#fff;text-decoration:none;'
         f'font-size:13px;font-weight:700;padding:10px 22px;border-radius:20px">'
         f'👉 打开网站看完整图表与历史早报</a>')
L.append(f'<div style="font-size:11px;color:{MUTE};margin-top:10px;line-height:1.7">'
         f'https://jerry-166.github.io/gold-price-briefing/<br>'
         f'数据来源：新浪财经 · 中国外汇交易中心 · 汇通财经 · 金价查询网 · CME FedWatch<br>'
         f'本邮件由自动化程序生成，所有内容仅供参考，不构成投资建议。</div>')
L.append('</div>')
L.append('</div>')
L.append('</div>')

html = chr(10).join(L)
out = ".workbuddy/outbox/mail_2026-11-10.html"
open(out, "w", encoding="utf-8").write(html)

lines = html.split(chr(10))
print("written", out)
print("chars", len(html), "bytes", len(html.encode("utf-8")), "lines", len(lines),
      "maxline", max(len(x) for x in lines))
print("gate_100pct_double", html.count("100%%"))
m = re.search(r"width:100[^;]*", html)
print("width_token", m.group(0) if m else "none")
