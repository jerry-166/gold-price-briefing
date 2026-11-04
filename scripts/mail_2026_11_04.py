# -*- coding: utf-8 -*-
"""把当日 JSON 渲染成邮件 HTML（纯 f-string，不用 % 格式化，规避 BUG-017/018）。"""
import json, io, re, os

d = json.load(io.open("daily/2026-11-04.json", encoding="utf-8"))
p = d["prices"]
hero, au, fx, spot = p[0], p[1], p[2], p[3]
up = "#c0392b"
down = "#1e8449"


def tone(v):
    return up if v > 0 else (down if v < 0 else "#555")


def arrow(v):
    return "▲" if v > 0 else ("▼" if v < 0 else "—")


rows = ""
for it in p:
    rows += (
        f'<tr><td style="padding:9px 4px;border-bottom:1px solid #f0ece5;color:#333;font-size:14px">{it["label"]}</td>'
        f'<td style="padding:9px 4px;border-bottom:1px solid #f0ece5;text-align:right;font-size:15px;font-weight:700;color:#1a1a1a">{it["value"]}'
        f'<span style="font-size:11px;font-weight:400;color:#999"> {it["unit"]}</span></td>'
        f'<td style="padding:9px 4px;border-bottom:1px solid #f0ece5;text-align:right;font-size:13px;font-weight:700;color:{tone(it["change"])}">'
        f'{arrow(it["change"])} {abs(it["change"]):.2f}%</td></tr>' + chr(10)
    )

news_html = ""
for i, n in enumerate(d["news"][:5], 1):
    news_html += (
        f'<div style="margin:0 0 14px">'
        f'<span style="display:inline-block;background:#fdf3e3;color:#b7791f;font-size:11px;padding:2px 7px;border-radius:3px;margin-right:6px">{n["tag"]}</span>'
        f'<span style="font-size:14px;font-weight:700;color:#1a1a1a">{n["title"]}</span>'
        f'<div style="font-size:13px;color:#555;line-height:1.75;margin-top:5px">{n["explain"]}</div>'
        f'<div style="font-size:11px;color:#aaa;margin-top:3px">来源：{n["source"]}</div>'
        f'</div>' + chr(10)
    )

note_parts = hero["note"].split("实际以银行挂牌为准。")[1].split("。")
note_short = "。".join(note_parts[:2]) + "。"
t = d["trend"]
tv = {"-1": ("偏空", down), "0": ("中性", "#b7791f"), "1": ("偏多", up)}
plan = d["plan"]

html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#f7f5f1;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif">
<div style="max-width:640px;margin:0 auto;background:#ffffff">

  <div style="background:linear-gradient(135deg,#1f2a37,#374151);padding:26px 24px;color:#fff">
    <div style="font-size:12px;letter-spacing:2px;color:#e8c88a">GOLD DAILY BRIEF</div>
    <div style="font-size:22px;font-weight:700;margin-top:8px">🌅 今日金价早报 · 2026年11月4日 周三</div>
    <div style="font-size:13px;color:#c9d1d9;margin-top:8px">早盘 3951.4 涨 0.54%，但 3964-3966 已三次冲高失败</div>
  </div>

  <div style="padding:22px 24px 6px">
    <div style="font-size:15px;font-weight:700;color:#1a1a1a;border-left:3px solid #c9a227;padding-left:9px;margin-bottom:12px">金价快照</div>
    <table style="width:100%;border-collapse:collapse">{rows}</table>
    <div style="font-size:12px;color:#8a8a8a;line-height:1.7;margin-top:10px;background:#fbfaf7;padding:10px 12px;border-radius:6px">
      积存金 {hero["value"]} 元/克是按 3951.39 美元 × 中间价 6.7180 ÷ 31.1035 估算的。{note_short}
    </div>
  </div>

  <div style="padding:18px 24px 6px">
    <div style="font-size:15px;font-weight:700;color:#1a1a1a;border-left:3px solid #c9a227;padding-left:9px;margin-bottom:12px">昨夜到今晨的大事</div>
    {news_html}
  </div>

  <div style="padding:12px 24px 6px">
    <div style="font-size:15px;font-weight:700;color:#1a1a1a;border-left:3px solid #c9a227;padding-left:9px;margin-bottom:12px">趋势判断</div>
    <table style="width:100%;border-collapse:collapse;font-size:13px">
      <tr><td style="padding:7px 0;color:#666;width:64px">短期</td><td style="padding:7px 0;color:{tv[str(t["shortVal"])][1]};font-weight:700;width:52px">{tv[str(t["shortVal"])][0]}</td><td style="padding:7px 0;color:#444;line-height:1.6">{t["short"]}</td></tr>
      <tr><td style="padding:7px 0;color:#666">中期</td><td style="padding:7px 0;color:{tv[str(t["midVal"])][1]};font-weight:700">{tv[str(t["midVal"])][0]}</td><td style="padding:7px 0;color:#444;line-height:1.6">{t["mid"]}</td></tr>
      <tr><td style="padding:7px 0;color:#666">长期</td><td style="padding:7px 0;color:{tv[str(t["longVal"])][1]};font-weight:700">{tv[str(t["longVal"])][0]}</td><td style="padding:7px 0;color:#444;line-height:1.6">{t["long"]}</td></tr>
    </table>
    <div style="font-size:13px;color:#333;line-height:1.8;background:#f7f5f1;padding:12px 14px;border-radius:6px;margin-top:10px">{t["advice"]}</div>
  </div>

  <div style="padding:18px 24px 6px">
    <div style="font-size:15px;font-weight:700;color:#1a1a1a;border-left:3px solid #c9a227;padding-left:9px;margin-bottom:12px">什么价位买、什么价位卖</div>
    <div style="border:1px solid #e8e4dc;border-radius:8px;padding:14px 16px;margin-bottom:12px">
      <div style="font-size:14px;font-weight:700;color:{down};margin-bottom:6px">买入：分三档挂单，别追</div>
      <div style="font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:6px">{plan["buy"]["price"]}</div>
      <div style="font-size:13px;color:#555;line-height:1.8">{plan["buy"]["trigger"]}</div>
    </div>
    <div style="border:1px solid #e8e4dc;border-radius:8px;padding:14px 16px;margin-bottom:12px">
      <div style="font-size:14px;font-weight:700;color:{up};margin-bottom:6px">卖出与止损：反弹是减仓机会</div>
      <div style="font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:6px">{plan["sell"]["price"]}</div>
      <div style="font-size:13px;color:#555;line-height:1.8">{plan["sell"]["trigger"]}</div>
    </div>
    <div style="font-size:12px;color:#8a8a8a;line-height:1.7">{plan["note"]}</div>
  </div>

  <div style="padding:14px 24px 6px">
    <div style="font-size:15px;font-weight:700;color:#1a1a1a;border-left:3px solid #c9a227;padding-left:9px;margin-bottom:12px">今日学一招：{d["teach"]["title"]}</div>
    <div style="font-size:13px;color:#333;line-height:1.9;background:#fbfaf7;padding:14px 16px;border-radius:6px">{d["teach"]["body"]}</div>
    <div style="font-size:11px;color:#aaa;margin-top:6px">参考：{d["teach"]["source"]}</div>
  </div>

  <div style="padding:22px 24px 30px;text-align:center;border-top:1px solid #f0ece5;margin-top:20px">
    <a href="https://jerry-166.github.io/gold-price-briefing/" style="display:inline-block;background:#1f2a37;color:#fff;text-decoration:none;font-size:13px;padding:11px 26px;border-radius:6px">查看看板与历史走势 →</a>
    <div style="font-size:11px;color:#aaa;margin-top:14px;line-height:1.7">本邮件由自动化程序每日 09:00 生成，数据来自上海黄金交易所、中国外汇交易中心与公开行情接口。<br>所有内容仅供参考，不构成投资建议。</div>
  </div>

</div>
</body></html>'''

os.makedirs(".workbuddy/outbox", exist_ok=True)
out = ".workbuddy/outbox/2026-11-04-morning.html"
io.open(out, "w", encoding="utf-8").write(html)
print("written", out, len(html), "chars", len(html.encode("utf-8")), "bytes")
print("double-pct check:", html.count("100%%"))
print("width hits:", re.findall(r"width:100[^;\"']*", html)[:3])
