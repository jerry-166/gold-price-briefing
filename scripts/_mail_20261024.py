import io, os, json

d = json.load(io.open('daily/2026-10-24.json', encoding='utf-8'))
p = {x['label']: x for x in d['prices']}
hero, au, fx, lon = p['招行积存金买入价'], p['上海金 AU9999'], p['美元汇率'], p['伦敦金 XAUUSD']

def color(v):
    return '#c0392b' if v > 0 else ('#1e8449' if v < 0 else '#666')

def chg(v):
    s = ('+' if v > 0 else '') + ('%.2f' % v) + '%'
    return '<span style="color:%s;font-weight:600">%s</span>' % (color(v), s)

news_html = ''
for n in d['news']:
    news_html += (
        '<div style="margin:0 0 14px">'
        '<div style="font-size:12px;color:#8a6d3b;background:#fdf6e3;display:inline-block;padding:2px 8px;border-radius:10px;margin-bottom:6px">%s</div>'
        '<div style="font-size:15px;font-weight:600;color:#1a1a1a;line-height:1.5;margin-bottom:4px">%s</div>'
        '<div style="font-size:13px;color:#555;line-height:1.75">%s</div>'
        '<div style="font-size:12px;color:#999;margin-top:3px">来源：<a href="%s" style="color:#3c6e9e;text-decoration:none">%s 原文</a></div>'
        '</div>'
    ) % (n['tag'], n['title'], n['explain'], n['url'], n['source'])

teach_items = d['teach']['body'].replace('<b>', '<b style="color:#1a1a1a">')

html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#f4f1ea;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif">
<div style="max-width:640px;margin:0 auto;background:#ffffff">

  <div style="background:linear-gradient(135deg,#8a6d3b 0%,#c9a227 100%);padding:26px 24px;color:#fff">
    <div style="font-size:12px;opacity:.85;letter-spacing:2px">GOLD DAILY BRIEFING</div>
    <div style="font-size:24px;font-weight:700;margin-top:6px">🌅 今日金价早报</div>
    <div style="font-size:13px;opacity:.9;margin-top:6px">2026 年 10 月 24 日 星期六 · 第 64 期</div>
  </div>

  <div style="background:#fff5f5;border-left:4px solid #c0392b;padding:12px 16px;margin:16px 24px 0;font-size:13px;color:#7b241c;line-height:1.7">
    <b>⚠️ 4000 破了，而且是收在下面</b>：周五现货金盘中跌破 4000（7 月 29 日以来首次），最低 3975.698 创三个月新低，纽约尾盘收 <b>3995.5（-0.72%）</b>，全周累跌 4.07%。<b>今天周六休市，价格停在周五收盘，正好用来定下周一开盘前的计划。</b>
  </div>

  <div style="background:#eef4fb;border-left:4px solid #3c6e9e;padding:12px 16px;margin:10px 24px 0;font-size:12.5px;color:#20496e;line-height:1.7">
    📅 <b>今日休市提示</b>：国际盘、上金所、外汇交易中心均停，本次报价与涨跌幅<b>沿用 10 月 23 日收盘口径</b>，不是今天的新变动。周一 09:15 公布新中间价，节后开盘可能跳空，杠杆品种建议降仓。
  </div>

  <div style="padding:20px 24px 4px">
    <div style="font-size:17px;font-weight:700;color:#1a1a1a;border-bottom:2px solid #c9a227;padding-bottom:8px">金价快照</div>
  </div>
  <div style="padding:12px 24px 0">
    <table style="width:100%;border-collapse:collapse;font-size:14px">
      <tr style="background:#faf8f3">
        <td style="padding:12px;border-bottom:1px solid #eee"><b>招行积存金买入价</b><div style="font-size:11px;color:#999;margin-top:2px">估算值，实际以银行挂牌为准</div></td>
        <td style="padding:12px;border-bottom:1px solid #eee;text-align:right;font-size:20px;font-weight:700;color:#c0392b">¥{{HERO}}<div style="font-size:11px;color:#999;font-weight:400">元/克</div></td>
        <td style="padding:12px;border-bottom:1px solid #eee;text-align:right;width:70px">{{HERO_CHG}}</td>
      </tr>
      <tr>
        <td style="padding:12px;border-bottom:1px solid #eee"><b>上海金 AU9999</b></td>
        <td style="padding:12px;border-bottom:1px solid #eee;text-align:right;font-size:18px;font-weight:600">¥{{AU}}<div style="font-size:11px;color:#999;font-weight:400">元/克</div></td>
        <td style="padding:12px;border-bottom:1px solid #eee;text-align:right">{{AU_CHG}}</td>
      </tr>
      <tr>
        <td style="padding:12px;border-bottom:1px solid #eee"><b>伦敦金 XAUUSD</b></td>
        <td style="padding:12px;border-bottom:1px solid #eee;text-align:right;font-size:18px;font-weight:600">${{LON}}<div style="font-size:11px;color:#999;font-weight:400">美元/盎司</div></td>
        <td style="padding:12px;border-bottom:1px solid #eee;text-align:right">{{LON_CHG}}</td>
      </tr>
      <tr>
        <td style="padding:12px;border-bottom:1px solid #eee"><b>美元人民币中间价</b></td>
        <td style="padding:12px;border-bottom:1px solid #eee;text-align:right;font-size:18px;font-weight:600">{{FX}}</td>
        <td style="padding:12px;border-bottom:1px solid #eee;text-align:right">{{FX_CHG}}</td>
      </tr>
    </table>
    <div style="font-size:12px;color:#888;line-height:1.7;margin-top:8px;background:#fafafa;padding:10px 12px;border-radius:6px">
      积存金＝伦敦金 3995.5 × 中间价 6.7180 ÷ 31.1035 ＝ <b>863.0 元/克</b>。昨天早报的 867.5 是 09:33 的亚市<b>快照</b>（当时 4016.3），而金价当天下午跌破 4000、美盘最低 3975.698、收 3995.5，所以「一天跌 4.5 元」里几乎全部来自快照与真实收盘的落差（20.8 美元 ≈ 4.5 元/克），汇率这两天都是 6.7180、贡献为 0。按在岸即期（6.6704）折算只有约 856.9 元/克，与按中间价折算差 6.1 元，属口径差不是算错。上金所 Au9999 的 864.0 比积存金估算高 1.0 元，因为那是周五 15:30 日盘收盘、当时现货还在 4000 上方。
    </div>
  </div>

  <div style="padding:24px 24px 4px">
    <div style="font-size:17px;font-weight:700;color:#1a1a1a;border-bottom:2px solid #c9a227;padding-bottom:8px">昨夜大事</div>
  </div>
  <div style="padding:12px 24px 0">{{NEWS}}</div>

  <div style="padding:24px 24px 4px">
    <div style="font-size:17px;font-weight:700;color:#1a1a1a;border-bottom:2px solid #c9a227;padding-bottom:8px">趋势判断</div>
  </div>
  <div style="padding:12px 24px 0">
    <table style="width:100%;border-collapse:collapse;font-size:13px;text-align:center">
      <tr>
        <td style="padding:10px;background:#fdecea;border-radius:6px 0 0 6px;width:33.3%"><div style="color:#999;font-size:11px">短期</div><div style="font-size:16px;font-weight:700;color:#c0392b;margin-top:4px">看跌 ↓</div></td>
        <td style="padding:10px;background:#fdecea;width:33.3%"><div style="color:#999;font-size:11px">中期</div><div style="font-size:16px;font-weight:700;color:#c0392b;margin-top:4px">偏空寻底 ↓</div></td>
        <td style="padding:10px;background:#eafaf1;border-radius:0 6px 6px 0;width:33.3%"><div style="color:#999;font-size:11px">长期</div><div style="font-size:16px;font-weight:700;color:#1e8449;margin-top:4px">看多 ↑</div></td>
      </tr>
    </table>
    <div style="font-size:14px;color:#333;line-height:1.85;margin-top:14px">{{SHORT}}</div>
    <div style="background:#fffdf5;border:1px dashed #c9a227;border-radius:8px;padding:12px 14px;margin-top:12px;font-size:14px;color:#5b4b1e;line-height:1.8">
      <b>一句话操作建议：</b>{{ADVICE}}
    </div>
  </div>

  <div style="padding:24px 24px 4px">
    <div style="font-size:17px;font-weight:700;color:#1a1a1a;border-bottom:2px solid #c9a227;padding-bottom:8px">买卖时机</div>
  </div>
  <div style="padding:12px 24px 0">
    <div style="border-left:3px solid #1e8449;padding:10px 14px;background:#f4faf6;border-radius:0 6px 6px 0;margin-bottom:12px">
      <div style="font-size:14px;font-weight:700;color:#1e8449;margin-bottom:4px">🟢 什么价位买</div>
      <div style="font-size:13px;color:#333;line-height:1.8">{{BUY_T}}</div>
      <div style="font-size:12px;color:#1e8449;margin-top:6px;font-weight:600">{{BUY_P}}</div>
    </div>
    <div style="border-left:3px solid #c0392b;padding:10px 14px;background:#fdf5f5;border-radius:0 6px 6px 0">
      <div style="font-size:14px;font-weight:700;color:#c0392b;margin-bottom:4px">🔴 什么价位卖</div>
      <div style="font-size:13px;color:#333;line-height:1.8">{{SELL_T}}</div>
      <div style="font-size:12px;color:#c0392b;margin-top:6px;font-weight:600">{{SELL_P}}</div>
    </div>
    <div style="font-size:12px;color:#999;line-height:1.7;margin-top:10px">{{NOTE}}</div>
  </div>

  <div style="padding:24px 24px 4px">
    <div style="font-size:17px;font-weight:700;color:#1a1a1a;border-bottom:2px solid #c9a227;padding-bottom:8px">今日学一招 · {{TEACH_T}}</div>
  </div>
  <div style="padding:12px 24px 0;font-size:13.5px;color:#333;line-height:1.85">{{TEACH_B}}
    <div style="font-size:11px;color:#999;margin-top:8px">参考：{{TEACH_S}}</div>
  </div>

  <div style="padding:24px 24px 20px">
    <a href="https://jerry-166.github.io/gold-price-briefing/" style="display:block;text-align:center;background:#8a6d3b;color:#fff;text-decoration:none;padding:13px;border-radius:8px;font-size:14px;font-weight:600">查看完整早报与历史走势 →</a>
    <div style="text-align:center;font-size:11px;color:#aaa;line-height:1.8;margin-top:14px">
      数据来源：上海黄金交易所 · 中国外汇交易中心 · 金投网 · 每日经济新闻 · 国际金融报 · 中国基金报 · 汇通网 · FX168 · 上观新闻 · 21 经济网<br>
      本邮件为自动化生成的行情资讯，所有内容仅供参考，不构成投资建议。市场有风险，投资需谨慎。<br>
      © 2026 每日金价资讯
    </div>
  </div>

</div></body></html>"""

repl = {
    '{{HERO}}': hero['value'], '{{HERO_CHG}}': chg(hero['change']),
    '{{AU}}': au['value'], '{{AU_CHG}}': chg(au['change']),
    '{{LON}}': lon['value'], '{{LON_CHG}}': chg(lon['change']),
    '{{FX}}': fx['value'], '{{FX_CHG}}': chg(fx['change']),
    '{{NEWS}}': news_html,
    '{{SHORT}}': d['trend']['short'],
    '{{ADVICE}}': d['trend']['advice'],
    '{{BUY_T}}': d['plan']['buy']['trigger'], '{{BUY_P}}': d['plan']['buy']['price'],
    '{{SELL_T}}': d['plan']['sell']['trigger'], '{{SELL_P}}': d['plan']['sell']['price'],
    '{{NOTE}}': d['plan']['note'],
    '{{TEACH_T}}': d['teach']['title'], '{{TEACH_B}}': teach_items, '{{TEACH_S}}': d['teach']['source'],
}
for k, v in repl.items():
    html = html.replace(k, v)

os.makedirs('.workbuddy/outbox', exist_ok=True)
out = '.workbuddy/outbox/2026-10-24-morning.html'
io.open(out, 'w', encoding='utf-8').write(html)
print('written', out, len(html), 'bytes')

subject = '🌅 今日金价早报 | 2026年10月24日 周六'
io.open('.workbuddy/outbox/2026-10-24-subject.txt', 'w', encoding='utf-8').write(subject)
print(subject)
