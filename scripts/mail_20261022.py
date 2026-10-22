# -*- coding: utf-8 -*-
"""生成 2026-10-22 早报邮件 HTML（QQ 邮件未注册时落盘 outbox）"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
d = json.loads((BASE / 'daily' / '2026-10-22.json').read_text(encoding='utf-8'))
by = {p['label']: p for p in d['prices']}
g = by['伦敦金 XAUUSD']
a = by['上海金 AU9999']
fx = by['美元汇率']
h = by['招行积存金买入价']

rows = ''
for p in d['prices']:
    c = p['change']
    color = '#c0392b' if c > 0 else ('#1e8449' if c < 0 else '#7f8c8d')
    sign = '+' if c > 0 else ''
    star = ' ★' if p.get('hero') else ''
    rows += (
        '<tr>'
        '<td style="padding:9px 8px;border-bottom:1px solid #eee;font-size:14px;color:#333">%s%s</td>'
        '<td style="padding:9px 8px;border-bottom:1px solid #eee;text-align:right;font-size:16px;font-weight:600;color:#1a1a1a">%s <span style="font-size:11px;color:#999;font-weight:400">%s</span></td>'
        '<td style="padding:9px 8px;border-bottom:1px solid #eee;text-align:right;font-size:14px;font-weight:600;color:%s">%s%.2f%%</td>'
        '</tr>'
    ) % (p['label'], star, p['value'], p['unit'], color, sign, c)

news_html = ''
for n in d['news']:
    news_html += (
        '<div style="margin:0 0 14px 0;padding:0 0 12px 0;border-bottom:1px dashed #e5e5e5">'
        '<div style="font-size:12px;color:#b8860b;font-weight:600;margin-bottom:4px">【%s】</div>'
        '<div style="font-size:14px;color:#1a1a1a;font-weight:600;line-height:1.55;margin-bottom:6px">%s</div>'
        '<div style="font-size:13px;color:#555;line-height:1.7">%s</div>'
        '<div style="font-size:11px;color:#aaa;margin-top:5px">来源：<a href="%s" style="color:#aaa;text-decoration:none">%s</a></div>'
        '</div>'
    ) % (n['tag'], n['title'], n['explain'], n['url'], n['source'])

t = d['trend']
def arrow(v):
    return '偏空 ↓' if v < 0 else ('偏多 ↑' if v > 0 else '中性 →')

act = {'hold': '持有观望', 'buy': '可以买', 'watch': '先看着，别急'}.get(t['action'], t['action'])

html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>今日金价早报</title></head>
<body style="margin:0;padding:0;background:#f4f2ee;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif">
<div style="max-width:600px;margin:0 auto;background:#ffffff">

  <div style="background:linear-gradient(135deg,#1c1c1c 0%%,#3d3226 100%%);padding:26px 24px;text-align:center">
    <div style="font-size:12px;letter-spacing:3px;color:#c9a961">GOLD DAILY</div>
    <div style="font-size:23px;color:#fff;font-weight:700;margin-top:8px">今日金价早报</div>
    <div style="font-size:13px;color:#c9a961;margin-top:6px">2026 年 10 月 22 日 · 周四</div>
  </div>

  <div style="padding:20px 24px 4px">
    <div style="background:#fdf8ef;border-left:4px solid #c9a961;padding:12px 14px;font-size:13px;color:#5c4a2e;line-height:1.7">
      <b>一句话看今天：</b>昨收 4140.95、今晨跌到 4111 附近（-0.71%%），昨天那根反抽只活了一天就被打回。
      4100 关口本周第三次被逼到墙角，守得住是双底，守不住就是新一轮下探。<b>现在不追涨、不追跌，等 4100 附近给信号。</b>
    </div>
  </div>

  <div style="padding:16px 24px 8px">
    <div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:10px">📊 金价快照</div>
    <table style="width:100%%;border-collapse:collapse">%s</table>
    <div style="font-size:11px;color:#999;margin-top:8px;line-height:1.6">
      ★ 积存金为估算值：伦敦金 × 人民币中间价 ÷ 31.1035，实际以银行挂牌为准。涨跌幅基准为上一交易日收盘/昨结。
    </div>
  </div>

  <div style="padding:16px 24px 4px">
    <div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:12px">🌙 昨夜今晨大事</div>
    %s
  </div>

  <div style="padding:16px 24px 4px">
    <div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:10px">🧭 趋势判断</div>
    <table style="width:100%%;border-collapse:collapse;font-size:13px">
      <tr style="background:#fafafa">
        <td style="padding:9px 10px;color:#666;width:32%%">短期（1-2 周）</td>
        <td style="padding:9px 10px;font-weight:600;color:#1e8449">%s</td>
      </tr>
      <tr>
        <td style="padding:9px 10px;color:#666">中期（1-3 月）</td>
        <td style="padding:9px 10px;font-weight:600;color:#1e8449">%s</td>
      </tr>
      <tr style="background:#fafafa">
        <td style="padding:9px 10px;color:#666">长期（1 年+）</td>
        <td style="padding:9px 10px;font-weight:600;color:#c0392b">%s</td>
      </tr>
      <tr>
        <td style="padding:9px 10px;color:#666">现在该干嘛</td>
        <td style="padding:9px 10px;font-weight:700;color:#b8860b">%s</td>
      </tr>
    </table>
    <div style="font-size:11px;color:#999;margin-top:8px;line-height:1.6">
      中期偏空的四个理由：12 月加息概率 88%%-92%%、实际利率仍高、美元有加息+避险双重支撑、短线投机资金还在退。
      长期看多的三个理由：央行购金（上半年全球 345 吨、中国连续 23 个月增持）、矿产供给增速仅 1%%。长多不等于短不跌。
    </div>
  </div>

  <div style="padding:16px 24px 4px">
    <div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:10px">💰 买卖时机</div>
    <div style="background:#f0f7f2;border-left:4px solid #1e8449;padding:13px 14px;margin-bottom:10px">
      <div style="font-size:14px;font-weight:700;color:#1e8449;margin-bottom:6px">买：等 4100 附近，分三档</div>
      <div style="font-size:13px;color:#333;line-height:1.8">
        ① 首仓 1/3：回踩 <b>4100-4106 美元/盎司</b>（约 <b>886-887 元/克</b>）——两次「碰一下就弹」的实盘低点<br>
        ② 加仓 1/3：跌到 <b>4073-4080 美元</b>（约 <b>880-881 元/克</b>）——10 月 14 日 CPI 夜低点，触及即反弹<br>
        ③ 兜底 1/3：跌到 <b>4060-4066 美元</b>（约 <b>877-878 元/克</b>）——10 月最低点，本月最便宜的位置
      </div>
      <div style="font-size:12px;color:#666;margin-top:8px">纪律：下探半小时内能收回 4106 上方才动手，直接击穿就往下一档等。</div>
    </div>
    <div style="background:#fdf0ee;border-left:4px solid #c0392b;padding:13px 14px;margin-bottom:8px">
      <div style="font-size:14px;font-weight:700;color:#c0392b;margin-bottom:6px">卖：反弹就减，破位就走</div>
      <div style="font-size:13px;color:#333;line-height:1.8">
        ① 止盈 1/3：<b>4131-4144 美元</b>（约 <b>892-895 元/克</b>）——今日高点 4144.19，本周反复熄火地带<br>
        ② 再减 1/3：<b>4155-4165 美元</b>（约 <b>898-900 元/克</b>）；收盘站稳 4200（约 907 元/克）才停手<br>
        ③ 止损：日线收盘破 <b>4100 美元</b>（约 886 元/克）先减 1/3；有效跌破 <b>4066 美元</b>（约 877 元/克）先清仓
      </div>
    </div>
    <div style="font-size:11px;color:#999;line-height:1.6">
      换算基准：4111.6 × 6.7195 ÷ 31.1035 ≈ 888.3 元/克。以上仅供参考，不构成投资建议。下周 10/27-28 美联储议息 + PCE 才是方向牌，杠杆品种请降仓。
    </div>
  </div>

  <div style="padding:18px 24px 4px">
    <div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:10px">📚 今日学一招</div>
    <div style="background:#f7f7f5;padding:14px 16px;border-radius:4px">
      <div style="font-size:14px;font-weight:700;color:#3d3226;margin-bottom:8px">%s</div>
      <div style="font-size:13px;color:#444;line-height:1.85">%s</div>
    </div>
  </div>

  <div style="padding:20px 24px 24px;text-align:center">
    <a href="https://jerry-166.github.io/gold-price-briefing/" style="display:inline-block;background:#3d3226;color:#fff;text-decoration:none;padding:11px 26px;border-radius:4px;font-size:14px">查看完整早报与 30 日走势图 →</a>
    <div style="font-size:11px;color:#bbb;margin-top:14px;line-height:1.7">
      数据来源：金投网、金价查询网、上海黄金交易所、中国外汇交易中心、汇通网、国际金融报、NeoData<br>
      本邮件由自动化程序生成，仅供参考，不构成任何投资建议。
    </div>
  </div>

</div>
</body></html>""" % (
    rows, news_html,
    arrow(t['shortVal']), arrow(t['midVal']), arrow(t['longVal']), act,
    d['teach']['title'], d['teach']['body'],
)

out = BASE / '.workbuddy' / 'outbox' / '2026-10-22-morning.html'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html, encoding='utf-8')
print('written', out, out.stat().st_size, 'bytes')

# 供日志记录的纯文本正文（去掉标签）
import re
plain = re.sub(r'<[^>]+>', '', html)
plain = re.sub(r'\n\s*\n+', '\n', plain).strip()
(BASE / '.workbuddy' / 'outbox' / '2026-10-22-morning.txt').write_text(plain, encoding='utf-8')
print('plain chars', len(plain))
