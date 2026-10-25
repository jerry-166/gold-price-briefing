import io, os, json, datetime

d = json.load(io.open('daily/2026-10-23.json', encoding='utf-8'))
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
    <div style="font-size:13px;opacity:.9;margin-top:6px">2026 年 10 月 23 日 星期五 · 第 63 期</div>
  </div>

  <div style="background:#fff5f5;border-left:4px solid #c0392b;padding:12px 16px;margin:16px 24px 0;font-size:13px;color:#7b241c;line-height:1.7">
    <b>⚠️ 昨夜金价闪崩 116 美元</b>：从日内高 4143.89 直落 4020.95，收 4024.6（-2.71%），创两个半月新低，4100、4050 两道关口一日尽失。<b>今日亚市 4016.3（-0.21%），4000 是最后一道防线。</b>
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
      积存金＝伦敦金 4016.3 × 中间价 6.7180 ÷ 31.1035 ＝ 867.5 元/克。昨日早报的 888.3 是 09:24 的亚市<b>快照</b>（当时 4111.6），而金价当天美盘一路砸到 4020.95、收 4024.6，所以「一天跌 20.8 元」里约 18.8 元来自快照与真实收盘的落差，真正的续跌只有约 1.8 元，汇率升值还帮忙拉低约 0.2 元。按即期汇率（6.6727）折算只有约 861.6 元/克，与按中间价折算差 5.9 元，属口径差不是算错。
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
      数据来源：上海黄金交易所 · 中国外汇交易中心 · 金投网 · 金价查询网 · 汇通网 · 上海证券报 · 每日经济新闻 · 同花顺<br>
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
for k,v in repl.items():
    html = html.replace(k, v)

os.makedirs('.workbuddy/outbox', exist_ok=True)
out = '.workbuddy/outbox/2026-10-23-morning.html'
io.open(out, 'w', encoding='utf-8').write(html)
print('written', out, len(html), 'bytes')

subject = '🌅 今日金价早报 | 2026年10月23日 周五'
io.open('.workbuddy/outbox/2026-10-23-subject.txt', 'w', encoding='utf-8').write(subject)
print(subject)
