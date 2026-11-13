# -*- coding: utf-8 -*-
import json, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, 'daily', '2026-11-13.json'), encoding='utf-8'))
T = []
a = T.append

def color(c):
    return '#d93025' if c > 0 else ('#0b8043' if c < 0 else '#5f6368')

def arrow(c):
    return '▲' if c > 0 else ('▼' if c < 0 else '—')

a('<!DOCTYPE html><html><head><meta charset="utf-8"></head>')
a('<body style="margin:0;padding:0;background:#f5f5f7;">')
a('<div style="max-width:640px;margin:0 auto;padding:18px 14px;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,PingFang SC,Microsoft YaHei,sans-serif;color:#1f2328;font-size:15px;line-height:1.75;">')

a('<div style="background:#fff;border-radius:14px;padding:22px 20px 18px;box-shadow:0 1px 4px rgba(0,0,0,0.06);">')
a('<div style="font-size:12px;letter-spacing:2px;color:#b8860b;font-weight:600;">GOLD DAILY · 2026-11-13</div>')
a('<h1 style="margin:6px 0 4px;font-size:23px;font-weight:700;color:#1f2328;">今日金价早报</h1>')
a('<div style="color:#6b7280;font-size:13px;">2026年11月13日 星期五 · 09:00 推送</div>')
a('</div>')

# 一句话
a('<div style="background:#fff8e6;border-left:4px solid #e0a800;border-radius:8px;padding:14px 16px;margin:12px 0;">')
a('<div style="font-weight:700;margin-bottom:4px;">一句话看今天</div>')
a('<div>金价连跌三天砸到 3852 刷新年内低点后，今早 V 型抢回 3900——但这是超跌反弹，不是反转。今晚 21:30 美国 PPI 是总开关。</div>')
a('</div>')

# 快照
a('<div style="background:#fff;border-radius:14px;padding:18px 20px;margin:12px 0;box-shadow:0 1px 4px rgba(0,0,0,0.06);">')
a('<div style="font-size:17px;font-weight:700;margin-bottom:10px;">📊 金价快照</div>')
a('<table style="width:100%;border-collapse:collapse;font-size:14px;">')
for i, p in enumerate(d['prices']):
    bg = '#fffdf5' if p.get('hero') else '#fff'
    a('<tr style="background:' + bg + ';">')
    a('<td style="padding:10px 6px;border-bottom:1px solid #eee;color:#4b5563;">' + p['label'] + '</td>')
    a('<td style="padding:10px 6px;border-bottom:1px solid #eee;text-align:right;font-weight:700;font-size:16px;">' + p['value'] + ' <span style="font-size:11px;color:#9ca3af;font-weight:400;">' + p['unit'] + '</span></td>')
    a('<td style="padding:10px 6px;border-bottom:1px solid #eee;text-align:right;width:78px;color:' + color(p['change']) + ';font-weight:600;">' + arrow(p['change']) + ' ' + ('%+.2f' % p['change']) + '%</td>')
    a('</tr>')
a('</table>')
a('<div style="margin-top:12px;font-size:13px;color:#6b7280;background:#fafafa;border-radius:8px;padding:10px 12px;">' + d['prices'][0]['note'].split('③')[0].replace('三层说明：①', '⚠️ 口径提醒：①') + '</div>')
a('</div>')

# 昨夜大事
a('<div style="background:#fff;border-radius:14px;padding:18px 20px;margin:12px 0;box-shadow:0 1px 4px rgba(0,0,0,0.06);">')
a('<div style="font-size:17px;font-weight:700;margin-bottom:12px;">🌙 昨夜大事</div>')
for n in d['news']:
    a('<div style="margin-bottom:14px;padding-bottom:12px;border-bottom:1px dashed #eaeaea;">')
    a('<div style="margin-bottom:5px;"><span style="display:inline-block;background:#f1f5f9;color:#475569;font-size:11px;padding:2px 7px;border-radius:4px;margin-right:7px;">' + n['tag'] + '</span><span style="font-weight:700;">' + n['title'] + '</span></div>')
    a('<div style="font-size:13.5px;color:#4b5563;">' + n['explain'] + '</div>')
    a('<div style="font-size:12px;color:#9ca3af;margin-top:4px;">来源：<a href="' + n['url'] + '" style="color:#9ca3af;">' + n['source'] + '</a></div>')
    a('</div>')
a('</div>')

# 趋势
tr = d['trend']
def label(v):
    return '看涨' if v > 0 else ('看跌' if v < 0 else '看平')
a('<div style="background:#fff;border-radius:14px;padding:18px 20px;margin:12px 0;box-shadow:0 1px 4px rgba(0,0,0,0.06);">')
a('<div style="font-size:17px;font-weight:700;margin-bottom:12px;">🧭 趋势判断</div>')
a('<table style="width:100%;border-collapse:collapse;font-size:14px;">')
for nm, v, t in (('短期', tr['shortVal'], tr['short']), ('中期', tr['midVal'], tr['mid']), ('长期', tr['longVal'], tr['long'])):
    a('<tr>')
    a('<td style="padding:8px 6px;border-bottom:1px solid #eee;width:52px;color:#6b7280;">' + nm + '</td>')
    a('<td style="padding:8px 6px;border-bottom:1px solid #eee;width:56px;font-weight:700;color:' + color(v) + ';">' + label(v) + '</td>')
    a('<td style="padding:8px 6px;border-bottom:1px solid #eee;color:#4b5563;font-size:13.5px;">' + t + '</td>')
    a('</tr>')
a('</table>')
a('<div style="margin-top:12px;background:#f0f7ff;border-radius:8px;padding:12px 14px;font-size:14px;">' + tr['advice'] + '</div>')
a('</div>')

# 买卖时机
pl = d['plan']
a('<div style="background:#fff;border-radius:14px;padding:18px 20px;margin:12px 0;box-shadow:0 1px 4px rgba(0,0,0,0.06);">')
a('<div style="font-size:17px;font-weight:700;margin-bottom:12px;">🎯 买卖时机</div>')
a('<div style="background:#fef2f2;border-radius:10px;padding:14px;margin-bottom:12px;">')
a('<div style="font-weight:700;color:#b91c1c;margin-bottom:6px;">什么时候买</div>')
a('<div style="font-size:14px;color:#4b5563;margin-bottom:8px;">' + pl['buy']['trigger'] + '</div>')
a('<div style="font-size:14px;font-weight:700;">参考价：' + pl['buy']['price'] + '</div>')
a('</div>')
a('<div style="background:#f0fdf4;border-radius:10px;padding:14px;margin-bottom:12px;">')
a('<div style="font-weight:700;color:#15803d;margin-bottom:6px;">什么时候卖</div>')
a('<div style="font-size:14px;color:#4b5563;margin-bottom:8px;">' + pl['sell']['trigger'] + '</div>')
a('<div style="font-size:14px;font-weight:700;">参考价：' + pl['sell']['price'] + '</div>')
a('</div>')
a('<div style="font-size:12.5px;color:#9ca3af;">' + pl['note'] + '</div>')
a('</div>')

# 学一招
te = d['teach']
tb = te['body'].replace('<ol>', '').replace('</ol>', '').replace('<li>', '').replace('</li>', '|SPLIT|')
a('<div style="background:#fff;border-radius:14px;padding:18px 20px;margin:12px 0;box-shadow:0 1px 4px rgba(0,0,0,0.06);">')
a('<div style="font-size:17px;font-weight:700;margin-bottom:8px;">💡 今日学一招</div>')
a('<div style="font-weight:700;color:#b8860b;margin-bottom:8px;">' + te['title'] + '</div>')
for i, seg in enumerate([s for s in tb.split('|SPLIT|') if s.strip()]):
    a('<div style="font-size:14px;color:#4b5563;margin-bottom:7px;"><span style="color:#b8860b;font-weight:700;">' + str(i + 1) + '.</span> ' + seg.strip() + '</div>')
a('<div style="font-size:12px;color:#9ca3af;margin-top:6px;">参考：' + te['source'] + '</div>')
a('</div>')

# 页脚
a('<div style="text-align:center;padding:16px 0 8px;font-size:13px;color:#6b7280;">')
a('<a href="https://jerry-166.github.io/gold-price-briefing/" style="display:inline-block;background:#b8860b;color:#fff;text-decoration:none;padding:10px 22px;border-radius:22px;font-weight:600;">查看完整早报与 30 日金价走势 →</a>')
a('<div style="margin-top:12px;font-size:12px;color:#9ca3af;">本邮件由自动化程序生成，数据来自公开行情与媒体报道，仅供参考，不构成投资建议。</div>')
a('</div>')

a('</div></body></html>')

html = ''.join(T)
os.makedirs(os.path.join(BASE, '.workbuddy', 'outbox'), exist_ok=True)
hp = os.path.join(BASE, '.workbuddy', 'outbox', '2026-11-13-morning-briefing.html')
io.open(hp, 'w', encoding='utf-8').write(html.replace('><', '>\n<'))
print('written', hp, len(html), 'bytes')
print('check 100%:', html.count('100%%'), '| width100 hits:', html.count('width:100%'))
