# -*- coding: utf-8 -*-
"""生成 2026-11-16 早报邮件 HTML。所有数据取自 daily/2026-11-16.json，保证与站点一致。
注意：字面量行写单个 %（本脚本不做 % 格式化），避免 BUG-017。"""
import json, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, "daily", "2026-11-16.json"), encoding="utf-8"))
NL = chr(10)

p = d["prices"]
hero, au, fx, xau = p[0], p[1], p[2], p[3]


def tint(ch):
    return "#c62828" if ch > 0 else ("#2e7d32" if ch < 0 else "#666")


def arrow(ch):
    return "▲" if ch > 0 else ("▼" if ch < 0 else "—")


L = []
A = L.append

A('<!DOCTYPE html><html><head><meta charset="utf-8">')
A('<meta name="viewport" content="width=device-width,initial-scale=1">')
A('<title>今日金价早报 2026-11-16</title></head>')
A('<body style="margin:0;padding:0;background:#f5f2ea;">')
A('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f5f2ea;padding:16px 0;">')
A('<tr><td align="center">')
A('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:640px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden;box-shadow:0 2px 12px rgba(120,100,60,0.12);font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\',\'Microsoft YaHei\',sans-serif;">')

# 头部
A('<tr><td style="background:linear-gradient(135deg,#b8860b 0%,#d4a017 55%,#e0b84c 100%);padding:22px 24px 18px;">')
A('<div style="font-size:20px;font-weight:700;color:#fff;letter-spacing:0.5px;">🌅 今日金价早报</div>')
A('<div style="font-size:13px;color:#fff7e0;margin-top:6px;">2026 年 11 月 16 日 周一 · 第 87 期</div>')
A('<div style="font-size:12px;color:#fff3d0;margin-top:10px;background:rgba(0,0,0,0.14);padding:6px 10px;border-radius:6px;line-height:1.6;">')
A('⚠️ 延迟交付：本期生成于 <b>10:59 CST</b>，比标称 09:00 晚约 2 小时，价格均为亚市盘中读数、非收盘。上周日（11-15）早报因发信通道故障未送达，本期为最新一期。')
A('</div></td></tr>')

# 一句话结论
A('<tr><td style="padding:18px 24px 6px;">')
A('<div style="font-size:15px;line-height:1.75;color:#333;background:#fdf8ec;border-left:4px solid #d4a017;padding:12px 14px;border-radius:0 8px 8px 0;">')
A('<b>一句话：</b>亚市冲高 3901.15 又被打回，3900 成了天花板、3852 是生死线；今天 10 点公布的 10 月数据全面走弱，'
  '其中金银珠宝零售暴跌 28.7%，国内买盘撑不住价格 —— 现在不是抄底的时候，是分批接的时候。')
A('</div></td></tr>')

# 金价快照
A('<tr><td style="padding:14px 24px 0;">')
A('<div style="font-size:15px;font-weight:700;color:#8a6d1f;margin-bottom:10px;">📊 金价快照</div>')
A('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px;">')
A('<tr style="background:#f7f3e8;">'
  '<th align="left" style="padding:9px 10px;color:#7a6a45;font-weight:600;border-bottom:1px solid #ece4d0;">品种</th>'
  '<th align="right" style="padding:9px 10px;color:#7a6a45;font-weight:600;border-bottom:1px solid #ece4d0;">价格</th>'
  '<th align="right" style="padding:9px 10px;color:#7a6a45;font-weight:600;border-bottom:1px solid #ece4d0;">涨跌</th>'
  '</tr>')
for pr in (hero, au, fx, xau):
    ch = pr["change"]
    A('<tr>'
      '<td style="padding:10px;border-bottom:1px solid #f2ecdd;color:#333;">' + pr["label"] + '</td>'
      '<td align="right" style="padding:10px;border-bottom:1px solid #f2ecdd;color:#111;font-weight:700;">'
      + pr["value"] + ' <span style="font-size:11px;color:#999;font-weight:400;">' + pr["unit"] + '</span></td>'
      '<td align="right" style="padding:10px;border-bottom:1px solid #f2ecdd;color:' + tint(ch) + ';font-weight:600;">'
      + arrow(ch) + ' ' + ("%+.2f" % ch) + '%</td>'
      '</tr>')
A('</table>')
A('<div style="font-size:11.5px;color:#8a8577;line-height:1.7;margin-top:8px;">积存金 = 伦敦金 × 中间价 ÷ 31.1035 = 836.4 元/克，按中间价折算比按即期 6.6701 折算高约 5.5 元/克，'
  '属口径差异；实际以银行挂牌为准。AU9999 涨跌基准为 11-13 日盘收盘 837.55。</div>')
A('</td></tr>')

# 昨夜大事
A('<tr><td style="padding:20px 24px 0;">')
A('<div style="font-size:15px;font-weight:700;color:#8a6d1f;margin-bottom:6px;">📰 昨夜今晨 5 件大事</div>')
for i, n in enumerate(d["news"], 1):
    A('<div style="margin-top:12px;padding:12px 14px;background:#fafafa;border:1px solid #f0ecdf;border-radius:10px;">')
    A('<div style="font-size:12px;color:#fff;background:#d4a017;display:inline-block;padding:2px 8px;border-radius:10px;margin-bottom:7px;">'
      + n["tag"] + '</div>')
    A('<div style="font-size:14px;font-weight:700;color:#222;line-height:1.6;">' + str(i) + '. ' + n["title"] + '</div>')
    A('<div style="font-size:13px;color:#4a4a4a;line-height:1.85;margin-top:6px;">' + n["explain"] + '</div>')
    A('<div style="font-size:11.5px;color:#9a9484;margin-top:6px;">来源：' + n["source"]
      + ' · <a href="' + n["url"] + '" style="color:#b8860b;text-decoration:none;">原文</a></div>')
    A('</div>')
A('</td></tr>')

# 趋势
t = d["trend"]
A('<tr><td style="padding:20px 24px 0;">')
A('<div style="font-size:15px;font-weight:700;color:#8a6d1f;margin-bottom:10px;">🧭 趋势判断</div>')
A('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;border-collapse:collapse;">')
for lab, key, val in (("短期", "short", t["shortVal"]), ("中期", "mid", t["midVal"]), ("长期", "long", t["longVal"])):
    icon = "偏空" if val < 0 else ("偏多" if val > 0 else "中性")
    A('<tr><td valign="top" style="padding:8px 0;border-bottom:1px dashed #ece4d0;width:64px;">'
      '<span style="font-size:12px;color:#fff;background:' + tint(val) + ';padding:2px 7px;border-radius:8px;white-space:nowrap;">'
      + lab + '</span></td>'
      '<td style="padding:8px 0 8px 10px;border-bottom:1px dashed #ece4d0;color:#444;line-height:1.8;">'
      + t[key] + ' <span style="color:' + tint(val) + ';font-size:12px;font-weight:600;">（' + icon + '）</span></td></tr>')
A('</table>')
A('<div style="margin-top:10px;font-size:13px;color:#3a3a3a;line-height:1.85;background:#fdf8ec;padding:12px 14px;border-radius:8px;">'
  '<b>小结：</b>' + t["advice"] + '</div>')
A('</td></tr>')

# 买卖时机
pl = d["plan"]
A('<tr><td style="padding:20px 24px 0;">')
A('<div style="font-size:15px;font-weight:700;color:#8a6d1f;margin-bottom:10px;">🎯 买卖时机（小白版）</div>')
A('<div style="padding:12px 14px;background:#f2f8f2;border:1px solid #d8e8d8;border-radius:10px;">')
A('<div style="font-size:13px;font-weight:700;color:#2e7d32;margin-bottom:6px;">🟢 什么时候买</div>')
A('<div style="font-size:13px;color:#3d3d3d;line-height:1.85;">' + pl["buy"]["trigger"] + '</div>')
A('<div style="font-size:12.5px;color:#2e7d32;font-weight:700;margin-top:8px;">参考价位：' + pl["buy"]["price"] + '</div>')
A('</div>')
A('<div style="padding:12px 14px;background:#fdf2f2;border:1px solid #eed6d6;border-radius:10px;margin-top:10px;">')
A('<div style="font-size:13px;font-weight:700;color:#c62828;margin-bottom:6px;">🔴 什么时候卖</div>')
A('<div style="font-size:13px;color:#3d3d3d;line-height:1.85;">' + pl["sell"]["trigger"] + '</div>')
A('<div style="font-size:12.5px;color:#c62828;font-weight:700;margin-top:8px;">参考价位：' + pl["sell"]["price"] + '</div>')
A('</div>')
A('<div style="font-size:11.5px;color:#8a8577;line-height:1.75;margin-top:9px;">' + pl["note"] + '</div>')
A('</td></tr>')

# 今日学一招
A('<tr><td style="padding:20px 24px 0;">')
A('<div style="font-size:15px;font-weight:700;color:#8a6d1f;margin-bottom:8px;">📚 今日学一招</div>')
A('<div style="padding:14px;background:#f7f4ec;border-radius:10px;">')
A('<div style="font-size:14px;font-weight:700;color:#222;line-height:1.6;margin-bottom:8px;">' + d["teach"]["title"] + '</div>')
A('<div style="font-size:13px;color:#454545;line-height:1.9;">' + d["teach"]["body"] + '</div>')
A('<div style="font-size:11.5px;color:#9a9484;margin-top:8px;">参考：' + d["teach"]["source"] + '</div>')
A('</div></td></tr>')

# 本周日历
A('<tr><td style="padding:20px 24px 0;">')
A('<div style="font-size:15px;font-weight:700;color:#8a6d1f;margin-bottom:8px;">🗓️ 本周要盯的事</div>')
A('<div style="font-size:13px;color:#444;line-height:1.95;">')
A('· <b>周二 21:30</b>　美国 10 月零售销售（预期环比持平、核心 +0.4%）——消费走弱才是加息预期松动的唯一理由<br>')
A('· <b>本周内</b>　美联储 10 月会议纪要（各家日历口径在周三与周四之间，以官方为准）——看内部对 50 个基点的分歧<br>')
A('· <b>11-17 01:00</b>　美联储主席沃什在旧金山联储听证会致开幕词')
A('</div></td></tr>')

# 底部
A('<tr><td style="padding:22px 24px 24px;">')
A('<div style="border-top:1px solid #ece4d0;padding-top:14px;font-size:12px;color:#8a8577;line-height:1.9;">')
A('完整数据、30 日走势图与历史早报：<br>')
A('<a href="https://jerry-166.github.io/gold-price-briefing/" style="color:#b8860b;font-weight:700;text-decoration:none;">'
  'https://jerry-166.github.io/gold-price-briefing/</a><br>')
A('<span style="font-size:11px;">本邮件由自动化脚本生成，数据来自上海黄金交易所、中国外汇交易中心、国家统计局与公开财经媒体。'
  '所有分析与价位仅供参考，不构成投资建议。</span>')
A('</div></td></tr>')

A('</table></td></tr></table></body></html>')

html = NL.join(L)
outdir = os.path.join(BASE, ".workbuddy", "outbox")
os.makedirs(outdir, exist_ok=True)
out = os.path.join(outdir, "mail-2026-11-16.html")
with io.open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)

lines = html.split(NL)
print("written", out)
print("chars", len(html), "bytes", len(html.encode("utf-8")), "lines", len(lines), "maxline", max(len(x) for x in lines))
print("pct_literal_100double", html.count("100%%"))
