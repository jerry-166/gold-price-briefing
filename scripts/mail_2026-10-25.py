# -*- coding: utf-8 -*-
"""生成 2026-10-25 早报邮件 HTML（周末版）。"""
import json, io, os

d = json.load(io.open("daily/2026-10-25.json", encoding="utf-8"))
P = {p["label"]: p for p in d["prices"]}

def arrow(v):
    return "▲" if v > 0 else ("▼" if v < 0 else "—")

def pct(v):
    return ("%+.2f%%" % v)

rows = []
for lab, unit in [("招行积存金买入价", "¥/克"), ("上海金 AU9999", "¥/克"), ("美元汇率", "USD/CNY"), ("伦敦金 XAUUSD", "$/oz")]:
    p = P[lab]
    color = "#c0392b" if p["change"] > 0 else ("#1e8449" if p["change"] < 0 else "#555")
    rows.append(
        '<tr><td style="padding:10px 12px;border-bottom:1px solid #f0e6d2;font-size:14px;color:#3a2f1b">%s%s</td>'
        '<td style="padding:10px 12px;border-bottom:1px solid #f0e6d2;text-align:right;font-size:16px;font-weight:700;color:#3a2f1b">%s <span style="font-size:11px;font-weight:400;color:#8a7a5c">%s</span></td>'
        '<td style="padding:10px 12px;border-bottom:1px solid #f0e6d2;text-align:right;font-size:13px;color:%s">%s %s</td></tr>'
        % (lab, ' <span style="background:#e8b400;color:#fff;font-size:10px;padding:1px 5px;border-radius:3px;margin-left:4px">主看</span>' if p.get("hero") else "",
           p["value"], unit, color, arrow(p["change"]), pct(p["change"])))

news_html = "".join(
    '<div style="margin-bottom:14px;padding-left:12px;border-left:3px solid #e8b400">'
    '<div style="font-size:13px;font-weight:700;color:#3a2f1b;margin-bottom:4px"><span style="background:#fdf3d4;color:#96700a;font-size:11px;padding:1px 6px;border-radius:3px;margin-right:6px">%s</span>%s</div>'
    '<div style="font-size:13px;line-height:1.75;color:#5a4b31">%s</div>'
    '<div style="font-size:11px;color:#a08c66;margin-top:4px">来源：%s　<a href="%s" style="color:#96700a">原文</a></div></div>'
    % (n["tag"], n["title"], n["explain"], n["source"], n["url"])
    for n in d["news"])

T = d["trend"]
PL = d["plan"]

html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f7f2e7;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif">
<div style="max-width:640px;margin:0 auto;background:#fffdf8">

  <div style="background:linear-gradient(135deg,#2c2416 0%,#4a3c20 100%);padding:26px 24px;text-align:center">
    <div style="font-size:12px;letter-spacing:3px;color:#d9bc72;margin-bottom:8px">GOLD DAILY · 周日休市</div>
    <div style="font-size:23px;font-weight:700;color:#fff">今日金价早报</div>
    <div style="font-size:13px;color:#c9b183;margin-top:8px">2026 年 10 月 25 日 周日 · 国际盘与上金所休市，价格沿用 10 月 23 日收盘</div>
  </div>

  <div style="padding:16px 24px 0">
    <div style="background:#fff8e1;border:1px solid #f0d894;border-radius:8px;padding:12px 14px;font-size:13px;line-height:1.7;color:#7a5f16">
      <b>周末提示</b>：今天没有新成交，表里的数字全部是周五（10/23）收盘口径，涨跌幅也是周五的，<b>不是今天又跌了 0.72%</b>。周末真正的增量在消息面（胡塞打沙特七处、伊朗点名海底光缆、路透 100 位经济学家全票预计 12 月加息），周一开盘可能跳空高开也可能冲高回落。<b>下周是三连击</b>：10/27-28 美联储议息（北京时间 10/29 凌晨 2 点公布）、10/29 三季度 GDP 初值与 9 月 PCE，同周还有加拿大、欧洲、日本央行开会 —— 杠杆品种务必降仓。
    </div>
  </div>

  <div style="padding:20px 24px 0">
    <div style="font-size:15px;font-weight:700;color:#3a2f1b;margin-bottom:10px">💰 金价快照</div>
    <table style="width:100%;border-collapse:collapse;background:#fffefb;border-radius:8px;overflow:hidden;border:1px solid #f0e6d2">
      __ROWS__
    </table>
    <div style="font-size:11px;color:#a08c66;margin-top:8px;line-height:1.6">积存金＝伦敦金×人民币中间价÷31.1035 估算（3995.5×6.7180÷31.1035＝863.0），实际以银行挂牌为准。按在岸即期 6.6704 折算会低约 6.1 元/克，属口径差。</div>
  </div>

  <div style="padding:24px 24px 0">
    <div style="font-size:15px;font-weight:700;color:#3a2f1b;margin-bottom:12px">📰 周末大事</div>
    __NEWS__
  </div>

  <div style="padding:24px 24px 0">
    <div style="font-size:15px;font-weight:700;color:#3a2f1b;margin-bottom:10px">🎯 趋势判断</div>
    <table style="width:100%;border-collapse:collapse;font-size:13px;color:#3a2f1b">
      <tr>
        <td style="padding:8px;background:#fdf3d4;border-radius:6px;text-align:center;width:33%"><div style="font-size:11px;color:#96700a">短期</div><div style="font-size:16px;font-weight:700;color:#1e8449">偏空</div></td>
        <td style="width:6px"></td>
        <td style="padding:8px;background:#fdf3d4;border-radius:6px;text-align:center;width:33%"><div style="font-size:11px;color:#96700a">中期</div><div style="font-size:16px;font-weight:700;color:#1e8449">偏空寻底</div></td>
        <td style="width:6px"></td>
        <td style="padding:8px;background:#fdf3d4;border-radius:6px;text-align:center;width:33%"><div style="font-size:11px;color:#96700a">长期</div><div style="font-size:16px;font-weight:700;color:#c0392b">看多</div></td>
      </tr>
    </table>
    <div style="font-size:13px;line-height:1.8;color:#5a4b31;margin-top:10px">__ADVICE__</div>
    <div style="background:#f6f2ea;border-radius:6px;padding:10px 12px;margin-top:10px;font-size:12px;line-height:1.7;color:#6b5b3d">
      <b>动作：观察为主</b>。破位后的第一个周末，超卖（RSI 28-32）只支持技术性反抽，不构成反转；下周会议与 PCE 落地前，仓位别超过五成。
    </div>
  </div>

  <div style="padding:24px 24px 0">
    <div style="font-size:15px;font-weight:700;color:#3a2f1b;margin-bottom:10px">📐 买卖时机</div>
    <div style="background:#eef7f0;border-radius:8px;padding:14px;margin-bottom:10px;border-left:4px solid #1e8449">
      <div style="font-size:13px;font-weight:700;color:#1e6b3a;margin-bottom:6px">买 —— 三档分批，等回踩站稳再下手</div>
      <div style="font-size:12px;line-height:1.75;color:#3a4f3f">__BUY__</div>
    </div>
    <div style="background:#fdeeee;border-radius:8px;padding:14px;border-left:4px solid #c0392b">
      <div style="font-size:13px;font-weight:700;color:#a03024;margin-bottom:6px">卖 —— 分批止盈，破位就走不留恋</div>
      <div style="font-size:12px;line-height:1.75;color:#4f3a3a">__SELL__</div>
    </div>
    <div style="font-size:11px;color:#a08c66;margin-top:8px;line-height:1.6">换算基准 6.7180。以上仅供参考，不构成投资建议。</div>
  </div>

  <div style="padding:24px 24px 0">
    <div style="font-size:15px;font-weight:700;color:#3a2f1b;margin-bottom:10px">🎓 今日学一招</div>
    <div style="background:#fffdf8;border:1px dashed #d9c79a;border-radius:8px;padding:14px">
      <div style="font-size:13px;font-weight:700;color:#96700a;margin-bottom:8px">__TEACH_TITLE__</div>
      <div style="font-size:12px;line-height:1.8;color:#5a4b31">__TEACH_BODY__</div>
    </div>
  </div>

  <div style="padding:24px;text-align:center">
    <a href="https://jerry-166.github.io/gold-price-briefing/" style="display:inline-block;background:#2c2416;color:#f0d894;text-decoration:none;padding:11px 26px;border-radius:6px;font-size:13px;font-weight:700">查看完整早报 · 历史数据</a>
    <div style="font-size:11px;color:#a08c66;margin-top:14px;line-height:1.7">每日 09:00 自动更新 · 数据来源：上海黄金交易所、中国外汇交易中心、央视财经、新浪财经、金投网<br>
    本邮件仅为信息汇总，不构成任何投资建议，投资需谨慎。</div>
  </div>
</div></body></html>"""

html = (html.replace("__ROWS__", "".join(rows))
            .replace("__NEWS__", news_html)
            .replace("__ADVICE__", T["advice"])
            .replace("__BUY__", PL["buy"]["trigger"])
            .replace("__SELL__", PL["sell"]["trigger"])
            .replace("__TEACH_TITLE__", d["teach"]["title"])
            .replace("__TEACH_BODY__", d["teach"]["body"]))

os.makedirs(".workbuddy/outbox", exist_ok=True)
op = ".workbuddy/outbox/2026-10-25-morning.html"
io.open(op, "w", encoding="utf-8").write(html)
print("html bytes", len(html.encode("utf-8")), "->", op)
