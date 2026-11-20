# -*- coding: utf-8 -*-
"""生成早报邮件 HTML（2026-11-20）。每条新闻独立成行，避免 Read 单行 2000 字符截断。"""
import json, io, os

d = json.load(open("daily/2026-11-20.json", encoding="utf-8"))
P = {p["label"]: p for p in d["prices"]}
GREEN = "#0f9d58"   # 中式配色：下跌用绿
RED = "#d93025"

site = "https://jerry-166.github.io/gold-price-briefing/"


def chg(v):
    return ("+" if v > 0 else "") + f"{v:.2f}%"


def color(v):
    return RED if v > 0 else (GREEN if v < 0 else "#666")


rows = []
for key in ["招行积存金买入价", "上海金 AU9999", "美元汇率", "伦敦金 XAUUSD"]:
    p = P[key]
    tag = "（估算）" if key == "招行积存金买入价" else ""
    rows.append(
        f'<tr><td style="padding:8px 6px;border-bottom:1px solid #eceef2;font-size:14px;color:#333">{key}{tag}</td>'
        f'<td style="padding:8px 6px;border-bottom:1px solid #eceef2;font-size:15px;font-weight:bold;color:#111;text-align:right">{p["value"]}</td>'
        f'<td style="padding:8px 6px;border-bottom:1px solid #eceef2;font-size:12px;color:#888">{p["unit"]}</td>'
        f'<td style="padding:8px 6px;border-bottom:1px solid #eceef2;font-size:14px;font-weight:bold;text-align:right;color:{color(p["change"])}">{chg(p["change"])}</td></tr>'
    )
price_rows = "\n          ".join(rows)

news_blocks = []
for i, n in enumerate(d["news"], 1):
    news_blocks.append(
        f'<div style="margin:0 0 14px 0">'
        f'<div style="font-size:15px;font-weight:bold;color:#111;line-height:1.5">'
        f'<span style="display:inline-block;background:#eef3ff;color:#2b5bd7;font-size:11px;padding:1px 6px;border-radius:3px;margin-right:6px;vertical-align:2px">{n["tag"]}</span>{n["title"]}</div>'
        f'<div style="font-size:13px;color:#444;line-height:1.75;margin-top:6px">{n["explain"]}</div>'
        f'<div style="font-size:11px;color:#999;margin-top:4px">来源：{n["source"]} · <a href="{n["url"]}" style="color:#2b5bd7;text-decoration:none">原文</a></div>'
        f'</div>'
    )
news_html = "\n        ".join(news_blocks)

t = d["trend"]
teach = d["teach"]
plan = d["plan"]


def tt(key):
    """把「偏空：xxx」拆成「加粗结论 + 说明」，避免出现两个冒号。"""
    txt = t[key]
    if "：" in txt:
        head, rest = txt.split("：", 1)
        c = RED if head == "偏多" else (GREEN if head == "偏空" else "#666")
        return f'<span style="font-weight:bold;color:{c}">{head}</span>：{rest}'
    return txt

html = f"""<div style="background:#f4f5f7;padding:20px 12px;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:640px;margin:0 auto;background:#ffffff;border-radius:10px;overflow:hidden">
    <tr><td style="padding:22px 24px 14px 24px;background:#111418">
      <div style="color:#ffffff;font-size:20px;font-weight:bold;letter-spacing:0.5px">金价早报 · 2026年11月20日 周五</div>
      <div style="color:#b9bec7;font-size:12px;margin-top:8px">生成于 11:34 CST（标称 09:00，延迟约 154 分钟）· 8 个交易日连破 5 道整数关</div>
    </td></tr>
    <tr><td style="padding:20px 24px 6px 24px">
      <div style="font-size:16px;font-weight:bold;color:#111;border-left:3px solid {RED};padding-left:8px;margin-bottom:12px">金价快照</div>
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse">
          {price_rows}
      </table>
      <div style="font-size:12px;color:#777;line-height:1.7;margin-top:10px">
        积存金按伦敦金 × 中间价 6.7131 ÷ 31.1035 估算，实际以银行挂牌为准。昨日早报的 800.8 是 11-19 上午 11:00 快照，11-19 纽约真实收盘折算只有 782.35 元/克，别拿 800.8 直接减今天的数——那会多算 18.5 元/克。
      </div>
    </td></tr>
    <tr><td style="padding:16px 24px 6px 24px">
      <div style="font-size:16px;font-weight:bold;color:#111;border-left:3px solid #2b5bd7;padding-left:8px;margin-bottom:12px">昨夜大事</div>
        {news_html}
    </td></tr>
    <tr><td style="padding:6px 24px">
      <div style="font-size:16px;font-weight:bold;color:#111;border-left:3px solid #f0a500;padding-left:8px;margin-bottom:10px">趋势与建议</div>
      <div style="font-size:13px;color:#333;line-height:1.9">
        <div>短期：{tt("short")}</div>
        <div>中期：{tt("mid")}</div>
        <div>长期：{tt("long")}</div>
      </div>
      <div style="background:#fafbfc;border:1px solid #eceef2;border-radius:6px;padding:12px;margin-top:10px;font-size:13px;color:#333;line-height:1.8">{t["advice"]}</div>
    </td></tr>
    <tr><td style="padding:14px 24px 4px 24px">
      <div style="font-size:16px;font-weight:bold;color:#111;border-left:3px solid {GREEN};padding-left:8px;margin-bottom:10px">现在该干嘛</div>
      <div style="border:1px solid #e6f4ea;background:#f3fbf6;border-radius:6px;padding:12px;margin-bottom:10px">
        <div style="font-size:13px;font-weight:bold;color:{GREEN};margin-bottom:6px">什么时候买</div>
        <div style="font-size:13px;color:#333;line-height:1.8">{plan["buy"]["trigger"]}</div>
        <div style="font-size:12px;color:#666;margin-top:6px">参考价位：{plan["buy"]["price"]}</div>
      </div>
      <div style="border:1px solid #fdecea;background:#fef7f6;border-radius:6px;padding:12px;margin-bottom:10px">
        <div style="font-size:13px;font-weight:bold;color:{RED};margin-bottom:6px">什么时候卖 / 止损</div>
        <div style="font-size:13px;color:#333;line-height:1.8">{plan["sell"]["trigger"]}</div>
        <div style="font-size:12px;color:#666;margin-top:6px">参考价位：{plan["sell"]["price"]}</div>
      </div>
      <div style="font-size:11px;color:#999;line-height:1.7">{plan["note"]}</div>
    </td></tr>
    <tr><td style="padding:14px 24px 4px 24px">
      <div style="font-size:16px;font-weight:bold;color:#111;border-left:3px solid #7b5cd6;padding-left:8px;margin-bottom:10px">今日学一招</div>
      <div style="font-size:14px;font-weight:bold;color:#333;margin-bottom:6px">{teach["title"]}</div>
      <div style="font-size:13px;color:#444;line-height:1.85">{teach["body"]}</div>
      <div style="font-size:11px;color:#999;margin-top:6px">参考：{teach["source"]}</div>
    </td></tr>
    <tr><td style="padding:18px 24px 24px 24px;border-top:1px solid #eceef2">
      <div style="font-size:12px;color:#666;line-height:1.8">完整版（含 30 天走势图与知识库）：<a href="{site}" style="color:#2b5bd7;text-decoration:none;font-weight:bold">{site}</a></div>
      <div style="font-size:11px;color:#aaa;margin-top:8px">本邮件由自动化程序生成，数据来自公开行情与媒体报道，仅供参考，不构成投资建议。</div>
    </td></tr>
  </table>
</div>"""

os.makedirs(".workbuddy/outbox", exist_ok=True)
out = ".workbuddy/outbox/mail-2026-11-20.html"
io.open(out, "w", encoding="utf-8").write(html)
lines = html.split("\n")
print("chars", len(html), "bytes", len(html.encode("utf-8")), "lines", len(lines), "maxline", max(len(x) for x in lines))
print("check 100%% == 0 :", html.count("100%%"), "| css width:100% :", html.count("width:100%"))
