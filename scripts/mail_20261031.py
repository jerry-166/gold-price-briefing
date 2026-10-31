# -*- coding: utf-8 -*-
"""生成 2026-10-31（周六）早报邮件 HTML 底稿"""
import json, io, os, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, 'daily', '2026-10-31.json'), encoding='utf-8'))
p = {x['label']: x for x in d['prices']}


def chg(v):
    if v < 0:
        return '<span style="color:#0a8f4d;font-weight:600;">%+.2f%%</span>' % v
    if v > 0:
        return '<span style="color:#c62828;font-weight:600;">%+.2f%%</span>' % v
    return '<span style="color:#888;font-weight:600;">0.00%</span>'


rows = ''
for lab in ['招行积存金买入价', '上海金 AU9999', '伦敦金 XAUUSD', '美元汇率']:
    it = p[lab]
    mark = ' ★' if it.get('hero') else ''
    rows += ('\n<tr><td style="padding:9px 8px;border-bottom:1px solid #eee;color:#333;">%s%s</td>'
             '<td style="padding:9px 8px;border-bottom:1px solid #eee;text-align:right;font-weight:700;color:#1a1a1a;">%s</td>'
             '<td style="padding:9px 8px;border-bottom:1px solid #eee;color:#666;font-size:13px;">%s</td>'
             '<td style="padding:9px 8px;border-bottom:1px solid #eee;text-align:right;">%s</td></tr>\n'
             % (lab, mark, it['value'], it['unit'], chg(it['change'])))

news_html = ''
for n in d['news']:
    news_html += ('\n<div style="margin:0 0 14px 0;padding-left:10px;border-left:3px solid #d4a017;">'
                  '<div style="font-size:13px;color:#b8860b;font-weight:600;margin-bottom:3px;">%s</div>'
                  '<div style="font-size:15px;color:#1a1a1a;font-weight:600;line-height:1.5;margin-bottom:4px;">%s</div>'
                  '<div style="font-size:14px;color:#555;line-height:1.65;">%s</div>'
                  '<div style="font-size:12px;color:#999;margin-top:4px;">来源：%s</div></div>\n'
                  % (n['tag'], n['title'], n['explain'], n['source']))

teach_body = d['teach']['body'].replace('<ol>', '<ol style="margin:6px 0 0 0;padding-left:20px;">')
teach_body = teach_body.replace('<li>', '<li style="margin-bottom:10px;line-height:1.7;">')

SUMMARY = ('周五夜里一根大阴线：金价跌 3.61% 收 3875.19，跌破 3900、创一年新低，白银更狠跌 5.82% 失守 50 美元。'
           '导火索是霍尔木兹油轮遇袭把布伦特推上 117.64、12 月加息预期升到 72%；'
           '真正把金价砸穿的是美股崩盘——纳指跌 2.86%、英特尔跌 28.58%，杠杆账户要补保证金，把黄金当提款机卖了。'
           '今天周六休市，盘面数字全是周五收盘的，别急着动手，周一先看能不能收回 3900。')

HTML = '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f5f7;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;">
<div style="max-width:640px;margin:0 auto;background:#ffffff;">
<div style="background:linear-gradient(135deg,#1f2937 0%%,#374151 100%%);padding:26px 24px;color:#fff;">
<div style="font-size:13px;letter-spacing:2px;color:#d4a017;font-weight:600;">GOLD DAILY · 2026</div>
<h1 style="margin:8px 0 4px 0;font-size:23px;font-weight:700;">🌅 今日金价早报</h1>
<div style="font-size:14px;color:#c9cdd4;">2026年10月31日 星期六 · 周六休市 · 价格取周五收盘</div>
</div>
<div style="padding:22px 24px 0 24px;">
<div style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:12px;">金价快照</div>
<table style="width:100%%;border-collapse:collapse;font-size:14px;">
%s</table>
<div style="margin-top:10px;font-size:12px;color:#999;line-height:1.6;">★ 积存金为估算值（伦敦金×中间价÷31.1035），实际以银行挂牌为准。AU9999 取周五夜盘收盘，按交易所规则归属下一交易日（11 月 2 日 周一）。</div>
</div>
<div style="margin:20px 24px 0 24px;padding:14px 16px;background:#fffbf0;border:1px solid #f0e0b0;border-radius:8px;">
<div style="font-size:14px;color:#8a6d1f;line-height:1.7;">
<b>一句话看懂今天：</b>%s
</div></div>
<div style="padding:22px 24px 0 24px;">
<div style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:12px;">昨夜今晨大事</div>
%s</div>
<div style="padding:6px 24px 0 24px;">
<div style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:12px;">趋势怎么看</div>
<div style="font-size:14px;color:#333;line-height:1.9;">
<div><b>短期（1-2 周）：</b>%s</div>
<div><b>中期（1-3 月）：</b>%s</div>
<div><b>长期（半年以上）：</b>%s</div>
</div>
<div style="margin-top:12px;padding:14px 16px;background:#f3f6ff;border-left:4px solid #3b5bdb;border-radius:4px;font-size:14px;color:#2b3a67;line-height:1.75;">
<b>操作建议：</b>%s
</div>
</div>
<div style="padding:22px 24px 0 24px;">
<div style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:12px;">什么价位买 / 什么价位卖</div>
<div style="font-size:14px;color:#333;line-height:1.8;margin-bottom:14px;padding:14px 16px;background:#f0f9f2;border-radius:8px;">
<div style="font-weight:700;color:#0a8f4d;margin-bottom:6px;">✅ 买入：分批接，别一次赌底</div>
<div style="margin-bottom:6px;">%s</div>
<div style="font-size:13px;color:#666;"><b>参考价位：</b>%s</div>
</div>
<div style="font-size:14px;color:#333;line-height:1.8;margin-bottom:14px;padding:14px 16px;background:#fdf0f0;border-radius:8px;">
<div style="font-weight:700;color:#c62828;margin-bottom:6px;">⚠️ 卖出 / 止盈：反弹是减仓机会</div>
<div style="margin-bottom:6px;">%s</div>
<div style="font-size:13px;color:#666;"><b>参考价位：</b>%s</div>
</div>
<div style="font-size:12px;color:#999;line-height:1.7;">%s</div>
</div>
<div style="padding:22px 24px 0 24px;">
<div style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:10px;">📚 今日学一招：%s</div>
<div style="font-size:14px;color:#333;">%s</div>
<div style="margin-top:8px;font-size:12px;color:#999;">参考：%s</div>
</div>
<div style="margin:24px 24px 0 24px;padding:18px 20px;background:#1f2937;border-radius:8px;text-align:center;">
<a href="https://jerry-166.github.io/gold-price-briefing/" style="color:#d4a017;text-decoration:none;font-size:15px;font-weight:600;">👉 打开网站看完整版（含 30 日走势图）</a>
<div style="color:#9ca3af;font-size:12px;margin-top:8px;">每日 09:00 更新 · 数据来源已在网站逐条标注</div>
</div>
<div style="padding:18px 24px 26px 24px;font-size:11px;color:#aaa;line-height:1.7;text-align:center;">
本邮件由自动化程序生成，所有价格与新闻均标注来源。内容仅供参考，不构成投资建议。<br>
伦敦金 10-30 纽约尾盘收盘（新浪财经实时接口）· AU9999 10-30 夜盘收盘 02:30（上金所）· 中间价 10-30 中国外汇交易中心（周六沿用）<br>
本期为延迟补发：原定 09:00 触发，实际生成于 TODAYNOW，内容已改用周五真实收盘价。
</div>
</div></body></html>''' % (
    rows, SUMMARY,
    news_html,
    d['trend']['short'], d['trend']['mid'], d['trend']['long'], d['trend']['advice'],
    d['plan']['buy']['trigger'], d['plan']['buy']['price'],
    d['plan']['sell']['trigger'], d['plan']['sell']['price'],
    d['plan']['note'],
    d['teach']['title'], teach_body, d['teach']['source'],
)

HTML = HTML.replace('TODAYNOW', datetime.datetime.now().strftime('%H:%M'))

os.makedirs(os.path.join(BASE, '.workbuddy', 'outbox'), exist_ok=True)
out = os.path.join(BASE, '.workbuddy', 'outbox', '2026-10-31-morning.html')
with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write(HTML)
print('bytes', len(HTML.encode('utf-8')), 'chars', len(HTML))
print('longest_line', max(len(l) for l in HTML.split('\n')))
print('path', out)
