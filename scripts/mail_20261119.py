# -*- coding: utf-8 -*-
"""生成 2026-11-19 早报邮件 HTML，落 .workbuddy/outbox/ 并打印行数/长度自检"""
import json, os, io

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, 'daily', '2026-11-19.json'), encoding='utf-8'))
OUT = os.path.join(BASE, '.workbuddy', 'outbox', 'mail-2026-11-19.html')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

RED = '#c0392b'
GREEN = '#1e8e5a'
GREY = '#6b7280'
DARK = '#1f2937'
LINE = '#e5e7eb'


def color(v):
    return RED if v > 0 else (GREEN if v < 0 else GREY)


def arrow(v):
    return '▲' if v > 0 else ('▼' if v < 0 else '—')


L = []
A = L.append

A('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>')
A('<body style="margin:0;padding:0;background:#f3f4f6;">')
A('<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f3f4f6;padding:20px 0;">')
A('<tr><td align="center">')
A('<table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:640px;background:#ffffff;border-radius:10px;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',\'PingFang SC\',\'Microsoft YaHei\',sans-serif;">')

# 头部
A('<tr><td style="background:linear-gradient(135deg,#b45309,#d97706);padding:22px 24px;">')
A('<div style="font-size:21px;font-weight:700;color:#ffffff;letter-spacing:1px;">🌅 今日金价早报</div>')
A('<div style="font-size:13px;color:#fde68a;margin-top:6px;">2026年11月19日 周四 · 数据截至 11:00 CST</div>')
A('</td></tr>')

# 快照
A('<tr><td style="padding:20px 24px 4px;">')
A('<div style="font-size:15px;font-weight:700;color:%s;border-left:4px solid #d97706;padding-left:8px;">金价快照</div>' % DARK)
A('</td></tr>')
A('<tr><td style="padding:10px 24px 0;">')
A('<table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-size:14px;">')
for p in d['prices']:
    c = color(p['change'])
    bg = '#fffbeb' if p.get('hero') else '#ffffff'
    weight = '700' if p.get('hero') else '500'
    A('<tr style="background:%s;">' % bg)
    A('<td style="padding:11px 10px;border-bottom:1px solid %s;color:%s;font-weight:%s;">%s</td>' % (LINE, DARK, weight, p['label']))
    A('<td align="right" style="padding:11px 10px;border-bottom:1px solid %s;color:%s;font-weight:700;font-size:16px;">%s <span style="font-size:11px;font-weight:400;color:%s;">%s</span></td>' % (LINE, DARK, p['value'], GREY, p['unit']))
    A('<td align="right" style="padding:11px 10px;border-bottom:1px solid %s;color:%s;font-weight:700;white-space:nowrap;">%s %.2f%%</td>' % (LINE, c, arrow(p['change']), p['change']))
    A('</tr>')
A('</table>')
A('<div style="font-size:12px;color:%s;line-height:1.7;padding:8px 0 0;">%s</div>' % (GREY, d['prices'][0]['note']))
A('</td></tr>')

# 昨夜大事
A('<tr><td style="padding:22px 24px 4px;">')
A('<div style="font-size:15px;font-weight:700;color:%s;border-left:4px solid #d97706;padding-left:8px;">昨夜大事</div>' % DARK)
A('</td></tr>')
A('<tr><td style="padding:6px 24px 0;">')
for n in d['news']:
    A('<div style="padding:12px 0;border-bottom:1px solid %s;">' % LINE)
    A('<div style="font-size:12px;color:#ffffff;background:#b45309;display:inline-block;padding:2px 8px;border-radius:10px;">%s</div>' % n['tag'])
    A('<div style="font-size:14px;font-weight:700;color:%s;line-height:1.55;margin-top:7px;">%s</div>' % (DARK, n['title']))
    A('<div style="font-size:13px;color:#374151;line-height:1.8;margin-top:6px;">%s</div>' % n['explain'])
    A('<div style="font-size:12px;color:%s;margin-top:6px;">来源：<a href="%s" style="color:#2563eb;text-decoration:none;">%s</a></div>' % (GREY, n['url'], n['source']))
    A('</div>')
A('</td></tr>')

# 趋势
A('<tr><td style="padding:22px 24px 4px;">')
A('<div style="font-size:15px;font-weight:700;color:%s;border-left:4px solid #d97706;padding-left:8px;">趋势判断</div>' % DARK)
A('</td></tr>')
A('<tr><td style="padding:8px 24px 0;">')
A('<table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-size:13px;border-collapse:collapse;">')
for lab, key, vkey in (('短期（1-2周）', 'short', 'shortVal'), ('中期（1-3月）', 'mid', 'midVal'), ('长期（1年以上）', 'long', 'longVal')):
    v = d['trend'][vkey]
    tag = '偏多' if v > 0 else ('偏空' if v < 0 else '中性')
    c = color(v)
    A('<tr>')
    A('<td style="padding:8px 0;vertical-align:top;width:96px;"><span style="color:%s;font-weight:700;white-space:nowrap;">%s %s</span></td>' % (c, tag, arrow(v)))
    A('<td style="padding:8px 0;color:#374151;line-height:1.65;">%s</td>' % d['trend'][key])
    A('</tr>')
A('</table>')
A('<div style="margin-top:10px;padding:12px 14px;background:#fffbeb;border-radius:8px;font-size:13px;color:#78350f;line-height:1.85;">%s</div>' % d['trend']['advice'])
A('</td></tr>')

# 买卖时机
A('<tr><td style="padding:22px 24px 4px;">')
A('<div style="font-size:15px;font-weight:700;color:%s;border-left:4px solid #d97706;padding-left:8px;">买卖时机</div>' % DARK)
A('</td></tr>')
A('<tr><td style="padding:8px 24px 0;">')
A('<table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-size:13px;border-collapse:collapse;">')
A('<tr><td style="padding:12px 14px;background:#fef2f2;border-radius:8px 8px 0 0;border-left:3px solid #c0392b;">')
A('<div style="font-weight:700;color:#c0392b;font-size:14px;">买入：等这两个位置</div>')
A('<div style="color:#374151;line-height:1.8;margin-top:6px;">%s</div>' % d['plan']['buy']['trigger'])
A('<div style="color:#7f1d1d;font-weight:700;margin-top:8px;line-height:1.7;">参考价位：%s</div>' % d['plan']['buy']['price'])
A('<div style="color:#6b7280;font-size:12px;margin-top:4px;line-height:1.7;">%s</div>' % d['plan']['buy']['reason'])
A('</td></tr>')
A('<tr><td style="padding:12px 14px;background:#f0fdf4;border-left:3px solid #1e8e5a;margin-top:8px;">')
A('<div style="font-weight:700;color:#1e8e5a;font-size:14px;">卖出 / 止盈</div>')
A('<div style="color:#374151;line-height:1.8;margin-top:6px;">%s</div>' % d['plan']['sell']['trigger'])
A('<div style="color:#14532d;font-weight:700;margin-top:8px;line-height:1.7;">参考价位：%s</div>' % d['plan']['sell']['price'])
A('<div style="color:#6b7280;font-size:12px;margin-top:4px;line-height:1.7;">%s</div>' % d['plan']['sell']['reason'])
A('</td></tr>')
A('</table>')
A('<div style="margin-top:10px;font-size:12px;color:#92400e;line-height:1.75;background:#fffbeb;padding:10px 12px;border-radius:8px;">⚠️ %s</div>' % d['plan']['note'])
A('</td></tr>')

# 今日学一招
A('<tr><td style="padding:22px 24px 4px;">')
A('<div style="font-size:15px;font-weight:700;color:%s;border-left:4px solid #d97706;padding-left:8px;">今日学一招</div>' % DARK)
A('</td></tr>')
A('<tr><td style="padding:8px 24px 0;">')
A('<div style="background:#f9fafb;border-radius:8px;padding:14px 16px;">')
A('<div style="font-size:14px;font-weight:700;color:%s;line-height:1.6;">%s</div>' % (DARK, d['teach']['title']))
A('<div style="font-size:13px;color:#374151;line-height:1.9;margin-top:8px;">%s</div>' % d['teach']['body'].replace('<ol>', '<ol style="margin:0;padding-left:20px;">').replace('<li>', '<li style="margin-bottom:8px;">'))
A('<div style="font-size:12px;color:%s;margin-top:8px;">参考：%s</div>' % (GREY, d['teach']['source']))
A('</div>')
A('</td></tr>')

# 页脚
A('<tr><td style="padding:24px 24px 26px;">')
A('<div style="border-top:1px solid %s;padding-top:16px;font-size:12px;color:%s;line-height:1.9;">' % (LINE, GREY))
A('<div>完整版含 30 日走势图与知识点：<a href="https://jerry-166.github.io/gold-price-briefing/" style="color:#2563eb;text-decoration:none;font-weight:600;">jerry-166.github.io/gold-price-briefing</a></div>')
A('<div style="margin-top:6px;">数据口径：伦敦金取新浪财经 hf_XAU 实时价，AU9999 取上金所延时行情，汇率取中国外汇交易中心中间价。以上内容仅供参考，不构成投资建议。</div>')
A('</div>')
A('</td></tr>')

A('</table></td></tr></table></body></html>')

html = '\n'.join(L)
open(OUT, 'w', encoding='utf-8').write(html)

lines = html.split('\n')
print('path', OUT)
print('chars', len(html), 'bytes', len(html.encode('utf-8')), 'lines', len(lines), 'maxline', max(len(x) for x in lines))
print('bad_percent', html.count('%%'), 'width100_css', html.count('width:100%'))
