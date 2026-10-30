# -*- coding: utf-8 -*-
"""生成 2026-10-29 早报邮件 HTML 底稿"""
import json, io, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, 'daily', '2026-10-29.json'), encoding='utf-8'))
p = {x['label']: x for x in d['prices']}

def chg(v):
    if v < 0:
        return f'<span style="color:#0a8f4d;font-weight:600;">{v:+.2f}%</span>'
    if v > 0:
        return f'<span style="color:#c62828;font-weight:600;">{v:+.2f}%</span>'
    return '<span style="color:#888;font-weight:600;">0.00%</span>'

rows = ''
for lab in ['招行积存金买入价', '上海金 AU9999', '伦敦金 XAUUSD', '美元汇率']:
    it = p[lab]
    mark = ' ★' if it.get('hero') else ''
    rows += (f'<tr><td style="padding:9px 8px;border-bottom:1px solid #eee;color:#333;">{lab}{mark}</td>'
             f'<td style="padding:9px 8px;border-bottom:1px solid #eee;text-align:right;font-weight:700;color:#1a1a1a;">{it["value"]}</td>'
             f'<td style="padding:9px 8px;border-bottom:1px solid #eee;color:#666;font-size:13px;">{it["unit"]}</td>'
             f'<td style="padding:9px 8px;border-bottom:1px solid #eee;text-align:right;">{chg(it["change"])}</td></tr>')

news_html = ''
for n in d['news'][:4]:
    news_html += ('\n' + f'<div style="margin:0 0 14px 0;padding-left:10px;border-left:3px solid #d4a017;">'
                  f'<div style="font-size:13px;color:#b8860b;font-weight:600;margin-bottom:3px;">{n["tag"]}</div>'
                  f'<div style="font-size:15px;color:#1a1a1a;font-weight:600;line-height:1.5;margin-bottom:4px;">{n["title"]}</div>'
                  f'<div style="font-size:14px;color:#555;line-height:1.65;">{n["explain"]}</div></div>' + '\n')

teach_body = d['teach']['body'].replace('<ol>', '<ol style="margin:6px 0 0 0;padding-left:20px;">')
teach_body = teach_body.replace('<li>', '<li style="margin-bottom:10px;line-height:1.7;">')

HTML = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f5f7;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;">
<div style="max-width:640px;margin:0 auto;background:#ffffff;">
<div style="background:linear-gradient(135deg,#1f2937 0%,#374151 100%);padding:26px 24px;color:#fff;">
<div style="font-size:13px;letter-spacing:2px;color:#d4a017;font-weight:600;">GOLD DAILY · 2026</div>
<h1 style="margin:8px 0 4px 0;font-size:23px;font-weight:700;">🌅 今日金价早报</h1>
<div style="font-size:14px;color:#c9cdd4;">2026年10月29日 星期四 · 第 30 期连续日更</div>
</div>
<div style="padding:22px 24px 0 24px;">
<div style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:12px;">金价快照</div>
<table style="width:100%;border-collapse:collapse;font-size:14px;">
{rows}
</table>
<div style="margin-top:10px;font-size:12px;color:#999;line-height:1.6;">★ 积存金为估算值（伦敦金×中间价÷31.1035），实际以银行挂牌为准。</div>
</div>
<div style="margin:20px 24px 0 24px;padding:14px 16px;background:#fffbf0;border:1px solid #f0e0b0;border-radius:8px;">
<div style="font-size:14px;color:#8a6d1f;line-height:1.7;">
<b>一句话看懂今天：</b>美联储凌晨按兵不动，但两张反对票是“要加息”、10 年期美债站上 5.02%，
决议落地反而成了闷局——金价冲高 4068 就回头，一度砸到 4036。今晚 20:30 的 PCE 才是这周真正的雷。
</div></div>
<div style="padding:22px 24px 0 24px;">
<div style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:12px;">昨夜今晨大事</div>
{news_html}
</div>
<div style="padding:6px 24px 0 24px;">
<div style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:12px;">趋势怎么看</div>
<div style="font-size:14px;color:#333;line-height:1.9;">
<div><b>短期（1-2 周）：</b>{d["trend"]["short"]}</div>
<div><b>中期（1-3 月）：</b>{d["trend"]["mid"]}</div>
<div><b>长期（半年以上）：</b>{d["trend"]["long"]}</div>
</div>
<div style="margin-top:12px;padding:14px 16px;background:#f3f6ff;border-left:4px solid #3b5bdb;border-radius:4px;font-size:14px;color:#2b3a67;line-height:1.75;">
<b>操作建议：</b>{d["trend"]["advice"]}
</div>
</div>
<div style="padding:22px 24px 0 24px;">
<div style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:12px;">什么价位买 / 什么价位卖</div>
<div style="font-size:14px;color:#333;line-height:1.8;margin-bottom:14px;padding:14px 16px;background:#f0f9f2;border-radius:8px;">
<div style="font-weight:700;color:#0a8f4d;margin-bottom:6px;">✅ 买入：分批接，别一次赌底</div>
<div style="margin-bottom:6px;">{d["plan"]["buy"]["trigger"]}</div>
<div style="font-size:13px;color:#666;"><b>参考价位：</b>{d["plan"]["buy"]["price"]}</div>
</div>
<div style="font-size:14px;color:#333;line-height:1.8;margin-bottom:14px;padding:14px 16px;background:#fdf0f0;border-radius:8px;">
<div style="font-weight:700;color:#c62828;margin-bottom:6px;">⚠️ 卖出 / 止盈：反弹是减仓机会</div>
<div style="margin-bottom:6px;">{d["plan"]["sell"]["trigger"]}</div>
<div style="font-size:13px;color:#666;"><b>参考价位：</b>{d["plan"]["sell"]["price"]}</div>
</div>
<div style="font-size:12px;color:#999;line-height:1.7;">{d["plan"]["note"]}</div>
</div>
<div style="padding:22px 24px 0 24px;">
<div style="font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:10px;">📚 今日学一招：{d["teach"]["title"]}</div>
<div style="font-size:14px;color:#333;">{teach_body}</div>
<div style="margin-top:8px;font-size:12px;color:#999;">参考：{d["teach"]["source"]}</div>
</div>
<div style="margin:24px 24px 0 24px;padding:18px 20px;background:#1f2937;border-radius:8px;text-align:center;">
<a href="https://jerry-166.github.io/gold-price-briefing/" style="color:#d4a017;text-decoration:none;font-size:15px;font-weight:600;">👉 打开网站看完整版（含 30 日走势图）</a>
<div style="color:#9ca3af;font-size:12px;margin-top:8px;">每日 09:00 更新 · 数据来源已在网站逐条标注</div>
</div>
<div style="padding:18px 24px 26px 24px;font-size:11px;color:#aaa;line-height:1.7;text-align:center;">
本邮件由自动化程序生成，所有价格与新闻均标注来源。内容仅供参考，不构成投资建议。<br>
伦敦金 09:14:55 金投网 · AU9999 09:20 上金所 · 中间价 09:15 中国外汇交易中心
</div>
</div></body></html>'''

os.makedirs(os.path.join(BASE, '.workbuddy', 'outbox'), exist_ok=True)
out = os.path.join(BASE, '.workbuddy', 'outbox', '2026-10-29-morning.html')
with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write(HTML)
print('bytes', len(HTML.encode('utf-8')), 'chars', len(HTML))
print('path', out)
