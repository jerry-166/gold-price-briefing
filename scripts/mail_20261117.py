# -*- coding: utf-8 -*-
"""生成 2026-11-17 早报邮件 HTML"""
import json, os, io

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, 'daily', '2026-11-17.json'), encoding='utf-8'))
OUT = os.path.join(BASE, '.workbuddy', 'outbox', 'mail-2026-11-17.html')

UP = '#c0392b'
DOWN = '#1e8e3e'
GREY = '#6b7280'

def clr(ch):
    if ch > 0:
        return UP
    if ch < 0:
        return DOWN
    return GREY

def sign(ch):
    return ('+' if ch > 0 else '') + ('%.2f' % ch) + '%'

rows = []
for p in d['prices']:
    star = '★ ' if p.get('hero') else ''
    rows.append(
        '<tr>'
        '<td style="padding:9px 10px;border-bottom:1px solid #eee;font-size:14px;color:#111;">' + star + p['label'] + '</td>'
        '<td style="padding:9px 10px;border-bottom:1px solid #eee;text-align:right;font-size:15px;font-weight:700;color:#111;">' + p['value'] + ' <span style="font-size:12px;font-weight:400;color:#6b7280;">' + p['unit'] + '</span></td>'
        '<td style="padding:9px 10px;border-bottom:1px solid #eee;text-align:right;font-size:14px;font-weight:700;color:' + clr(p['change']) + ';">' + sign(p['change']) + '</td>'
        '</tr>'
    )

news_html = []
for n in d['news']:
    news_html.append(
        '<div style="margin:0 0 14px 0;">'
        '<div style="font-size:13px;color:#8a6d3b;background:#fdf6e3;display:inline-block;padding:2px 8px;border-radius:10px;margin-bottom:5px;">' + n['tag'] + '</div>'
        '<div style="font-size:15px;font-weight:700;color:#111;line-height:1.55;margin-bottom:4px;">' + n['title'] + '</div>'
        '<div style="font-size:13px;color:#374151;line-height:1.75;">' + n['explain'] + '</div>'
        '<div style="font-size:12px;color:#9ca3af;margin-top:4px;">来源：' + n['source'] + '　<a href="' + n['url'] + '" style="color:#2563eb;text-decoration:none;">原文</a></div>'
        '</div>'
    )

t = d['trend']
def trend_line(label, text, val):
    col = DOWN if val < 0 else (UP if val > 0 else GREY)
    word = '偏空' if val < 0 else ('偏多' if val > 0 else '中性')
    return ('<tr>'
            '<td style="padding:8px 10px;border-bottom:1px solid #eee;font-size:13px;color:#111;white-space:nowrap;vertical-align:top;">' + label + '</td>'
            '<td style="padding:8px 10px;border-bottom:1px solid #eee;font-size:13px;color:' + col + ';white-space:nowrap;vertical-align:top;font-weight:700;">' + word + '</td>'
            '<td style="padding:8px 10px;border-bottom:1px solid #eee;font-size:13px;color:#374151;line-height:1.7;">' + text + '</td>'
            '</tr>')

teach = d['teach']['body'].replace('<ol>', '<ol style="padding-left:20px;margin:6px 0;">')
teach = teach.replace('<li>', '<li style="margin-bottom:9px;line-height:1.8;">')

H = []
H.append('<!DOCTYPE html>')
H.append('<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>')
H.append('<body style="margin:0;padding:0;background:#f3f4f6;">')
H.append('<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f3f4f6;padding:18px 10px;">')
H.append('<tr><td align="center">')
H.append('<table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:640px;background:#ffffff;border-radius:12px;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,\'PingFang SC\',\'Microsoft YaHei\',sans-serif;">')

# 头部
H.append('<tr><td style="background:linear-gradient(135deg,#b8860b 0%,#8b5e00 100%);padding:22px 20px;">')
H.append('<div style="font-size:12px;color:rgba(255,255,255,0.82);letter-spacing:1px;">GOLD BRIEFING · 每日金价</div>')
H.append('<div style="font-size:22px;font-weight:700;color:#ffffff;margin-top:6px;">🌅 今日金价早报｜2026年11月17日 周二</div>')
H.append('<div style="font-size:12px;color:rgba(255,255,255,0.78);margin-top:8px;">报价时点 11-17 13:17 CST　·　今日延迟交付（标称 09:00，实际约 13:27 生成，延迟约 257 分钟）</div>')
H.append('</td></tr>')

# 一句话结论
H.append('<tr><td style="padding:18px 20px 4px 20px;">')
H.append('<div style="font-size:15px;line-height:1.8;color:#111;background:#fff8e6;border-left:4px solid #d4a017;border-radius:6px;padding:12px 14px;">')
H.append('<b>一句话：</b>今早金价探底 3843.45 后拉回 3875，但冲到 3879.90、差 0.1 美元没摸到 3880 就被打回——<b>3880 站不上，反弹都只能算修复</b>；3850 已破，下一道真防线在 3800。')
H.append('</div></td></tr>')

# 快照
H.append('<tr><td style="padding:20px 20px 0 20px;">')
H.append('<div style="font-size:17px;font-weight:700;color:#111;margin-bottom:10px;">💰 金价快照</div>')
H.append('<table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">')
H.append('<tr style="background:#fafafa;">'
         '<th align="left" style="padding:8px 10px;font-size:12px;color:#6b7280;border-bottom:1px solid #e5e7eb;">品种</th>'
         '<th align="right" style="padding:8px 10px;font-size:12px;color:#6b7280;border-bottom:1px solid #e5e7eb;">价格</th>'
         '<th align="right" style="padding:8px 10px;font-size:12px;color:#6b7280;border-bottom:1px solid #e5e7eb;">日涨跌</th>'
         '</tr>')
H.extend(rows)
H.append('</table>')
H.append('<div style="font-size:12px;color:#6b7280;line-height:1.75;margin-top:10px;background:#f9fafb;border-radius:6px;padding:10px 12px;">')
H.append('<b>口径提醒：</b>昨日早报的积存金 836.4 是当天 10:59 的盘中快照，而 11-16 纽约真实收盘 3856.24 折算只有 832.3 元/克（差 4.1 元）。今天 836.4 与昨晨数字一样是巧合，从真实收盘算起的真实涨幅约 +4.0 元/克。'
         '积存金按中间价 6.7132 折算，比按在岸即期 6.6642 折算的约 830.3 元/克高约 6.1 元，属口径差异。实际以银行挂牌为准。')
H.append('</div></td></tr>')

# 昨夜大事
H.append('<tr><td style="padding:22px 20px 0 20px;">')
H.append('<div style="font-size:17px;font-weight:700;color:#111;margin-bottom:12px;">🌙 昨夜大事</div>')
H.extend(news_html)
H.append('</td></tr>')

# 趋势
H.append('<tr><td style="padding:6px 20px 0 20px;">')
H.append('<div style="font-size:17px;font-weight:700;color:#111;margin-bottom:10px;">📊 趋势判断</div>')
H.append('<table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">')
H.append(trend_line('短期（1-2 周）', t['short'], t['shortVal']))
H.append(trend_line('中期（1-3 月）', t['mid'], t['midVal']))
H.append(trend_line('长期（6 月+）', t['long'], t['longVal']))
H.append('</table>')
H.append('<div style="font-size:12px;color:#6b7280;margin-top:8px;">动作建议：<b>观望（watch）</b>　·　今晚 21:30 零售销售、周四凌晨 3:00 FOMC 纪要是两个变盘点</div>')
H.append('</td></tr>')

# 买卖时机
pl = d['plan']
H.append('<tr><td style="padding:22px 20px 0 20px;">')
H.append('<div style="font-size:17px;font-weight:700;color:#111;margin-bottom:10px;">🎯 买卖时机</div>')
H.append('<div style="background:#fef2f2;border-radius:8px;padding:12px 14px;margin-bottom:10px;">')
H.append('<div style="font-size:14px;font-weight:700;color:#991b1b;margin-bottom:6px;">买入（分批，别一次打完）</div>')
H.append('<div style="font-size:13px;color:#374151;line-height:1.8;">' + pl['buy']['trigger'] + '</div>')
H.append('<div style="font-size:13px;color:#991b1b;font-weight:700;margin-top:6px;">参考价位：' + pl['buy']['price'] + '</div>')
H.append('</div>')
H.append('<div style="background:#f0fdf4;border-radius:8px;padding:12px 14px;margin-bottom:10px;">')
H.append('<div style="font-size:14px;font-weight:700;color:#166534;margin-bottom:6px;">卖出 / 止盈 / 止损</div>')
H.append('<div style="font-size:13px;color:#374151;line-height:1.8;">' + pl['sell']['trigger'] + '</div>')
H.append('<div style="font-size:13px;color:#166534;font-weight:700;margin-top:6px;">参考价位：' + pl['sell']['price'] + '</div>')
H.append('</div>')
H.append('<div style="font-size:12px;color:#6b7280;line-height:1.75;">⚠️ ' + pl['note'] + '</div>')
H.append('</td></tr>')

# 今日学一招
H.append('<tr><td style="padding:22px 20px 0 20px;">')
H.append('<div style="font-size:17px;font-weight:700;color:#111;margin-bottom:8px;">🎓 今日学一招：' + d['teach']['title'] + '</div>')
H.append('<div style="font-size:13px;color:#374151;">' + teach + '</div>')
H.append('<div style="font-size:12px;color:#9ca3af;margin-top:6px;">参考：' + d['teach']['source'] + '</div>')
H.append('</td></tr>')

# 底部
H.append('<tr><td style="padding:24px 20px 26px 20px;text-align:center;border-top:1px solid #eee;margin-top:20px;">')
H.append('<a href="https://jerry-166.github.io/gold-price-briefing/" style="display:inline-block;background:#b8860b;color:#ffffff;text-decoration:none;font-size:14px;font-weight:700;padding:11px 26px;border-radius:24px;">查看完整早报与 30 日图表 →</a>')
H.append('<div style="font-size:12px;color:#9ca3af;margin-top:14px;line-height:1.8;">数据来源：新浪财经实时行情 · 上海黄金交易所 · 中国外汇交易中心 · 央视财经 · 汇通财经 · 财联社<br>'
         '本邮件为自动生成的信息整理，所有价格与观点仅供参考，不构成投资建议。</div>')
H.append('</td></tr>')

H.append('</table>')
H.append('</td></tr></table>')
H.append('</body></html>')

html = chr(10).join(H)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

lines = html.split(chr(10))
maxline = max(len(x) for x in lines)
print('file', OUT)
print('chars', len(html), 'bytes', len(html.encode('utf-8')), 'lines', len(lines), 'maxline', maxline)
print('pct100', html.count('100%%'), 'css100', html.count('width:100%'))
assert maxline <= 1500, maxline
assert '100%%' not in html
