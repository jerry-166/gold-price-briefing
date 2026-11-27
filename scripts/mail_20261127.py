# -*- coding: utf-8 -*-
"""11-27 早报邮件 HTML：纯 f-string，无 % 格式化；按行输出、标签外折行防单行超长。"""
import io, json, re, textwrap

D = json.load(open("daily/2026-11-27.json", encoding="utf-8"))
OUT = ".workbuddy/outbox/mail-2026-11-27-morning_briefing.html"

UP = "#c0392b"
DOWN = "#1e8449"
INK = "#1f2328"
MUTED = "#6b7280"

def sign(v):
    return f"+{v}" if v > 0 else f"{v}"

def arrow(v):
    return "▲" if v > 0 else ("▼" if v < 0 else "—")

def row(label, value, unit, chg):
    color = UP if chg > 0 else (DOWN if chg < 0 else MUTED)
    return (
        "          <tr>"
        f"<td style=\"padding:8px 10px;border-bottom:1px solid #eceff3;color:{INK};font-size:14px\">{label}</td>"
        f"<td style=\"padding:8px 10px;border-bottom:1px solid #eceff3;color:{INK};font-size:15px;font-weight:700;text-align:right\">{value}<span style=\"font-size:11px;color:{MUTED};font-weight:400\"> {unit}</span></td>"
        f"<td style=\"padding:8px 10px;border-bottom:1px solid #eceff3;color:{color};font-size:13px;text-align:right;white-space:nowrap\">{arrow(chg)} {sign(chg)}%</td>"
        "</tr>"
    )

price_rows = "\n".join(
    row(p["label"], p["value"], p["unit"], p["change"]) for p in D["prices"]
)

PICK = [D["news"][0], D["news"][1], D["news"][2], D["news"][3], D["news"][4]]
news_blocks = []
for n in PICK:
    news_blocks.append(
        f"        <p style=\"margin:0 0 6px 0;font-size:14px;font-weight:700;color:{INK};line-height:1.55\">"
        f"<span style=\"display:inline-block;padding:1px 6px;margin-right:6px;border-radius:3px;background:#f1f5f9;color:#475569;font-size:11px;font-weight:400\">{n['tag']}</span>"
        f"{n['title']}</p>"
    )
    news_blocks.append(
        f"        <p style=\"margin:0 0 16px 0;font-size:13px;color:#374151;line-height:1.75\">{n['explain']}</p>"
    )
news_html = "\n".join(news_blocks)

t = D["trend"]
trend_rows = "\n".join([
    f"          <tr><td style=\"padding:6px 10px;font-size:13px;color:{MUTED};white-space:nowrap;vertical-align:top\">短期</td><td style=\"padding:6px 10px;font-size:13px;color:{INK};line-height:1.7\">{t['short']}</td></tr>",
    f"          <tr><td style=\"padding:6px 10px;font-size:13px;color:{MUTED};white-space:nowrap;vertical-align:top\">中期</td><td style=\"padding:6px 10px;font-size:13px;color:{INK};line-height:1.7\">{t['mid']}</td></tr>",
    f"          <tr><td style=\"padding:6px 10px;font-size:13px;color:{MUTED};white-space:nowrap;vertical-align:top\">长期</td><td style=\"padding:6px 10px;font-size:13px;color:{INK};line-height:1.7\">{t['long']}</td></tr>",
])

plan = D["plan"]

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN"><body style="margin:0;padding:0;background:#f5f6f8">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f5f6f8;padding:18px 0">
    <tr><td align="center">
      <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff;border:1px solid #e5e8ee;border-radius:8px">
        <tr><td style="padding:22px 26px 14px 26px;border-bottom:1px solid #eceff3">
          <div style="font-size:19px;font-weight:700;color:{INK};line-height:1.5">今日金价早报 · 2026 年 11 月 27 日 周五</div>
          <div style="margin-top:6px;font-size:12px;color:{MUTED};line-height:1.6">生成于 10:45 CST（计划 09:00）｜伦敦金亚市盘中读数 3625.0 美元/盎司</div>
        </td></tr>
        <tr><td style="padding:16px 26px 6px 26px">
          <div style="font-size:13px;font-weight:700;color:{INK};margin-bottom:8px">一、金价快照</div>
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{price_rows}
          </table>
          <p style="margin:10px 0 0 0;font-size:12px;color:{MUTED};line-height:1.7">积存金为估算值（伦敦金 × 中间价 6.7075 ÷ 31.1035），实际以银行挂牌为准；昨日基准已按 11-26 真实收盘 3566.26 回填，不是早报快照。</p>
        </td></tr>
        <tr><td style="padding:14px 26px 6px 26px">
          <div style="font-size:13px;font-weight:700;color:{INK};margin-bottom:10px">二、昨夜今晨大事</div>
{news_html}
        </td></tr>
        <tr><td style="padding:6px 26px 6px 26px">
          <div style="font-size:13px;font-weight:700;color:{INK};margin-bottom:8px">三、趋势判断（当前建议：观望）</div>
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fafbfc;border:1px solid #eef1f5;border-radius:6px">
{trend_rows}
          </table>
        </td></tr>
        <tr><td style="padding:14px 26px 6px 26px">
          <div style="font-size:13px;font-weight:700;color:{INK};margin-bottom:8px">四、买卖时机</div>
          <p style="margin:0 0 8px 0;font-size:13px;color:{INK};line-height:1.75"><span style="color:{DOWN};font-weight:700">买入</span>　{plan['buy']['trigger']}</p>
          <p style="margin:0 0 4px 0;font-size:12px;color:{MUTED};line-height:1.7">参考价位：{plan['buy']['price']}</p>
          <p style="margin:0 0 12px 0;font-size:12px;color:{MUTED};line-height:1.7">理由：{plan['buy']['reason']}</p>
          <p style="margin:0 0 8px 0;font-size:13px;color:{INK};line-height:1.75"><span style="color:{UP};font-weight:700">卖出</span>　{plan['sell']['trigger']}</p>
          <p style="margin:0 0 4px 0;font-size:12px;color:{MUTED};line-height:1.7">参考价位：{plan['sell']['price']}</p>
          <p style="margin:0 0 12px 0;font-size:12px;color:{MUTED};line-height:1.7">理由：{plan['sell']['reason']}</p>
          <p style="margin:0;padding:10px 12px;background:#fff8f0;border-left:3px solid #f0b27a;font-size:12px;color:#8a5a2b;line-height:1.7">{plan['note']}</p>
        </td></tr>
        <tr><td style="padding:14px 26px 6px 26px">
          <div style="font-size:13px;font-weight:700;color:{INK};margin-bottom:8px">五、今日学一招：{D['teach']['title']}</div>
          <div style="font-size:13px;color:#374151;line-height:1.8">{D['teach']['body']}</div>
        </td></tr>
        <tr><td style="padding:16px 26px 22px 26px;border-top:1px solid #eceff3">
          <p style="margin:0 0 6px 0;font-size:12px;color:{MUTED};line-height:1.7">完整版（含 30 日走势图、知识点、买卖计划）：<a href="https://jerry-166.github.io/gold-price-briefing/" style="color:#2563eb;text-decoration:none">jerry-166.github.io/gold-price-briefing</a></p>
          <p style="margin:0;font-size:11px;color:#9aa3af;line-height:1.7">数据来源：新浪财经、上海黄金交易所、中国外汇交易中心、21 世纪经济报道、金十期货、中金在线、汇通财经。本邮件仅供信息参考，不构成投资建议。</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body></html>
"""

# 标签外折行，控制单行长度（BUG-031）：只在标签外、且落在空白/中文标点处断开
def _split_line(line, limit):
    pieces, rest = [], line
    while len(rest) > limit:
        in_tag, cut, depth = False, -1, 0
        for i, ch in enumerate(rest[:limit]):
            if ch == "<":
                in_tag = True
            elif ch == ">":
                in_tag = False
            elif not in_tag and ch in (" ", "，", "。", "、", "；", "：", "）", "」"):
                cut = i + 1
        if cut <= 0:
            break
        pieces.append(rest[:cut])
        rest = rest[cut:]
    pieces.append(rest)
    return pieces


def wrap_outside_tags(html, limit=1500):
    out = []
    for line in html.split("\n"):
        out.extend(_split_line(line, limit))
    return "\n".join(out)

HTML = wrap_outside_tags(HTML)
assert HTML.count("%%") == 0
assert "\ufffd" not in HTML
for bad in ("別", "藉", "後", "個", "們"):
    assert bad not in HTML, bad

io.open(OUT, "w", encoding="utf-8", newline="\n").write(HTML)
lines = HTML.split("\n")
print("path", OUT)
print("chars", len(HTML), "lines", len(lines), "maxline", max(len(x) for x in lines))
print("width100%% count", HTML.count("100%%"), "| style100% count", HTML.count("width:100%"))
