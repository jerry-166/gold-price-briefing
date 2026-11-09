# -*- coding: utf-8 -*-
"""生成 2026-11-09 早报邮件 HTML（f-string 拼接，无 % 格式化）"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, 'daily', '2026-11-09.json'), encoding='utf-8'))

p = {x['label']: x for x in d['prices']}
hero = p['招行积存金买入价']
au = p['上海金 AU9999']
fx = p['美元汇率']
xau = p['伦敦金 XAUUSD']

GOLD = '#b8860b'
RED = '#c62828'
GREEN = '#2e7d32'


def arrow(ch):
    return '▲' if ch > 0 else ('▼' if ch < 0 else '—')


def color(ch):
    return RED if ch > 0 else (GREEN if ch < 0 else '#666')


rows = [
    (hero['label'], hero['value'], '元/克', hero['change'], True),
    (au['label'], au['value'], '元/克', au['change'], False),
    (xau['label'], xau['value'], '美元/盎司', xau['change'], False),
    (fx['label'], fx['value'], 'USD/CNY', fx['change'], False),
]

price_rows = []
for label, val, unit, ch, is_hero in rows:
    bg = '#fffbea' if is_hero else '#ffffff'
    weight = '700' if is_hero else '400'
    price_rows.append(
        f'<tr style="background:{bg};">'
        f'<td style="padding:10px 12px;border-bottom:1px solid #eee;font-size:14px;color:#333;font-weight:{weight};">{label}</td>'
        f'<td style="padding:10px 12px;border-bottom:1px solid #eee;text-align:right;font-size:16px;font-weight:700;color:#222;">{val}'
        f' <span style="font-size:12px;color:#999;font-weight:400;">{unit}</span></td>'
        f'<td style="padding:10px 12px;border-bottom:1px solid #eee;text-align:right;font-size:14px;font-weight:700;color:{color(ch)};">{arrow(ch)} {abs(ch):.2f}%</td>'
        f'</tr>'
    )
price_rows = chr(10).join(price_rows)

news_html = []
for n in d['news'][:4]:
    news_html.append(
        f'<div style="margin:0 0 14px 0;padding:0 0 0 10px;border-left:3px solid {GOLD};">'
        f'<div style="font-size:13px;color:{GOLD};font-weight:700;margin-bottom:4px;">【{n["tag"]}】{n["title"]}</div>'
        f'<div style="font-size:13px;color:#555;line-height:1.7;">{n["explain"]}</div>'
        f'<div style="font-size:12px;color:#999;margin-top:3px;">来源：{n["source"]}</div>'
        f'</div>'
    )
news_html = chr(10).join(news_html)

t = d['trend']


def trend_line(label, txt, val):
    tag = {1: ('偏多', RED), 0: ('震荡', '#666'), -1: ('偏空', GREEN)}[val]
    return (
        f'<div style="margin-bottom:10px;">'
        f'<span style="display:inline-block;padding:1px 7px;border-radius:3px;background:{tag[1]};color:#fff;font-size:12px;font-weight:700;">{label} {tag[0]}</span>'
        f'<div style="font-size:13px;color:#555;line-height:1.7;margin-top:5px;">{txt}</div>'
        f'</div>'
    )


trend_html = chr(10).join([trend_line('短期', t['short'], t['shortVal']), trend_line('中期', t['mid'], t['midVal']), trend_line('长期', t['long'], t['longVal'])])

plan = d['plan']

html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f1ea;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f1ea;padding:20px 0;">
<tr><td align="center">
<table width="640" cellpadding="0" cellspacing="0" style="max-width:640px;background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.06);">

<tr><td style="background:linear-gradient(135deg,#2c2620 0%,#4a3f30 100%);padding:26px 24px;">
<div style="font-size:20px;font-weight:700;color:#f5d78e;letter-spacing:1px;">🌅 今日金价早报</div>
<div style="font-size:13px;color:#c9bda8;margin-top:6px;">2026年11月09日 周一 · 09:50 CST</div>
</td></tr>

<tr><td style="padding:22px 24px 6px 24px;">
<div style="font-size:15px;font-weight:700;color:#2c2620;margin-bottom:12px;">📊 金价快照</div>
<table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #eee;border-radius:6px;overflow:hidden;">
{price_rows}
</table>
<div style="font-size:12px;color:#888;line-height:1.7;margin-top:10px;">{hero["note"]}</div>
</td></tr>

<tr><td style="padding:18px 24px 6px 24px;">
<div style="background:#fffbea;border:1px solid #f0e2b8;border-radius:6px;padding:14px 16px;">
<div style="font-size:14px;font-weight:700;color:#7a5c00;margin-bottom:6px;">一句话看懂</div>
<div style="font-size:13px;color:#5a4a20;line-height:1.8;">特朗普周日五度表态“极不可能”对伊动武 → 油价盘初跌逾 1%（布伦特 97.26）→ 通胀预期降温，金价反手低开高走、收复 4100 冲到 4120.95（+1.23%）。<strong>这波涨的不是避险，是“通胀降温→美联储不必更鹰”这条线。</strong>但 12 月加息概率已经到 81%，上方 4125-4146 是上周冲高失败区，周二 21:30 的 CPI 才是本周裁判。</div>
</div>
</td></tr>

<tr><td style="padding:18px 24px 0 24px;">
<div style="font-size:15px;font-weight:700;color:#2c2620;margin-bottom:12px;">🗞 昨夜今晨大事</div>
{news_html}
</td></tr>

<tr><td style="padding:14px 24px 0 24px;">
<div style="font-size:15px;font-weight:700;color:#2c2620;margin-bottom:12px;">🧭 趋势怎么看</div>
{trend_html}
</td></tr>

<tr><td style="padding:14px 24px 0 24px;">
<div style="font-size:15px;font-weight:700;color:#2c2620;margin-bottom:12px;">💰 现在该干嘛</div>
<div style="border:1px solid #e8e8e8;border-radius:6px;padding:14px 16px;margin-bottom:10px;">
<div style="font-size:14px;font-weight:700;color:{RED};margin-bottom:6px;">买入 · {plan["buy"]["price"]}</div>
<div style="font-size:13px;color:#555;line-height:1.8;">{plan["buy"]["trigger"]}</div>
<div style="font-size:12px;color:#999;margin-top:6px;">理由：{plan["buy"]["reason"]}</div>
</div>
<div style="border:1px solid #e8e8e8;border-radius:6px;padding:14px 16px;margin-bottom:10px;">
<div style="font-size:14px;font-weight:700;color:{GREEN};margin-bottom:6px;">卖出 / 止盈 · {plan["sell"]["price"]}</div>
<div style="font-size:13px;color:#555;line-height:1.8;">{plan["sell"]["trigger"]}</div>
<div style="font-size:12px;color:#999;margin-top:6px;">理由：{plan["sell"]["reason"]}</div>
</div>
<div style="font-size:12px;color:#999;line-height:1.7;">{plan["note"]}</div>
</td></tr>

<tr><td style="padding:18px 24px 0 24px;">
<div style="background:#f7f5f0;border-radius:6px;padding:16px;">
<div style="font-size:15px;font-weight:700;color:#2c2620;margin-bottom:8px;">🎓 今日学一招：{d["teach"]["title"]}</div>
<div style="font-size:13px;color:#555;line-height:1.9;">{d["teach"]["body"]}</div>
<div style="font-size:12px;color:#999;margin-top:8px;">参考：{d["teach"]["source"]}</div>
</div>
</td></tr>

<tr><td style="padding:22px 24px 26px 24px;text-align:center;">
<a href="https://jerry-166.github.io/gold-price-briefing/" style="display:inline-block;padding:10px 24px;background:{GOLD};color:#fff;text-decoration:none;border-radius:4px;font-size:14px;font-weight:700;">查看完整日报与历史走势 →</a>
<div style="font-size:12px;color:#aaa;margin-top:14px;line-height:1.7;">本邮件由自动化脚本生成，数据来源：新浪财经、中国外汇交易中心、上海黄金交易所、汇通财经等。<br>仅供参考，不构成投资建议。</div>
</td></tr>

</table>
</td></tr>
</table>
</body></html>'''

outdir = os.path.join(BASE, '.workbuddy', 'outbox')
os.makedirs(outdir, exist_ok=True)
out = os.path.join(outdir, 'gold-20261109.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print('written', out)
print('chars', len(html), 'bytes', len(html.encode('utf-8')))
print('lines', html.count(chr(10)) + 1, 'maxline', max(len(x) for x in html.split(chr(10))))
print('100%% count', html.count('100%%'))
print('has width:100%', 'width:100%' in html)
