# -*- coding: utf-8 -*-
"""写 2026-11-09 早报运行日志 + logs/manifest 更新"""
import json, os, io, sys, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, 'daily', '2026-11-09.json'), encoding='utf-8'))
p = {x['label']: x for x in d['prices']}

mail_txt = """金价快照（2026-11-09 09:48 亚市）
- 招行积存金买入价（估算）：890.2 元/克，+1.26%
- 上海金 AU9999：885.30 元/克，+1.29%（基准 11-06 夜盘收 874.00）
- 伦敦金 XAUUSD：4120.95 美元/盎司，+1.23%（昨收 4070.75）
- 美元中间价：6.7188，+0.03%（调贬 20 个基点）

一句话：特朗普周日五度表态“极不可能”对伊动武 → 油价盘初跌逾 1%（布伦特 97.26）→ 通胀预期降温，
金价反手低开高走、收复 4100 冲到 4120.95。这波涨的不是避险，是“通胀降温→美联储不必更鹰”这条线。
但 12 月加息概率已到 81%，上方 4125-4146 是上周冲高失败区，周二 21:30 的 CPI 才是本周裁判。

昨夜今晨大事：①特朗普淡化对伊动武，战争溢价继续回吐；②10 月非农 16.5 万远超预期 6.5 万，
12 月加息概率 72.8%→81%；③周二 21:30 美国 10 月 CPI（只发环比，缺同比基期）、周五 PPI；
④布伦特单周暴跌 13.32% 创 2020 年以来最大周跌幅。

趋势：短期偏多（+1）／中期偏空（-1）／长期偏多（+1），动作 watch。

买卖：买入 4085-4100 美元（约 882-886 元/克）、4030-4050 美元（约 870-875 元/克）；
卖出 4146-4160 美元（约 896-899 元/克）、4200-4225 美元（约 907-913 元/克）；
收盘破 4060（约 877 元/克）止损离场。

今日学一招：同一件事、两个开关——中东缓和了，黄金为什么反而涨？
网站：https://jerry-166.github.io/gold-price-briefing/"""

log = {
    'date': '2026-11-09',
    'type': 'morning_briefing',
    'status': 'success',
    'summary': '伦敦金收复 4100 报 4120.95(+1.23%)，积存金估算 890.2 元/克(+1.26%)，邮件已发',
    'timestamp': '09:52 CST',
    'steps': [
        {
            'num': 1, 'name': '获取数据', 'status': 'success', 'duration_ms': 130000,
            'result': ('伦敦金 4120.95(+1.23%，09:48 亚市；昨收 4070.75、开 4066.57、高 4125.12、低 4054.25)、'
                       'AU9999 885.30(+1.29%，基准 874.00)、中间价 6.7188(调贬 20 点)、COMEX 主力 4132.38(旁证)、'
                       'T+D 885.15；新闻 6 条源（汇通/新浪/腾讯/新华/华尔街见闻/每经）全部带原始 url。'
                       'NeoData 未调用（连续第六期），新浪 hq.sinajs 一条 curl 覆盖三项核心数据'),
            'source': 'sina hq.sinajs.cn + WebSearch（6 源交叉）'
        },
        {
            'num': 2, 'name': '生成早报JSON', 'status': 'success', 'duration_ms': 62000,
            'result': '已写入 daily/2026-11-09.json；check_briefing.py 自检 0 error（advice 197 字、10 组价位全中、汇率 2 位）'
        },
        {
            'num': 3, 'name': '更新manifest', 'status': 'success', 'duration_ms': 4000,
            'result': '已追加记录到 manifest.json，briefings 共 80 条，头部 2026-11-09/周一'
        },
        {
            'num': 4, 'name': 'Git推送', 'status': 'success', 'duration_ms': 12000,
            'result': 'commit 79a3e74「每日早报 2026-11-09」，SSH 推送成功，rev-parse 与 ls-remote 一致'
        },
        {
            'num': 5, 'name': '发送邮件', 'status': 'success', 'duration_ms': 58000,
            'result': '已发送至 2132049351@qq.com，09:52:35 CST ListMessages(sent) 确认，message_id msg_XnFi0d7PKZ6fumrW1-KaFoBoj5tm50LtT4cX55SzGhr7eg',
            'outputs': [{'label': '邮件内容', 'body': mail_txt}]
        }
    ],
    'summary_stats': {
        'total_steps': 5, 'success_steps': 5, 'failed_steps': 0,
        'total_duration_ms': 266000, 'email_sent': True, 'git_pushed': True
    }
}

out = os.path.join(BASE, 'logs', '2026-11-09-morning_briefing.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
print('written', out)

# logs/manifest
mp = os.path.join(BASE, 'logs', 'manifest.json')
m = json.load(open(mp, encoding='utf-8'))
entry = {'date': '2026-11-09', 'type': 'morning_briefing', 'status': 'success',
         'summary': '伦敦金收复 4100 报 4120.95(+1.23%)，积存金 890.2 元/克，邮件已发'}
if m['logs'][0]['date'] != '2026-11-09':
    m['logs'].insert(0, entry)
json.dump(m, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('logs head', m['logs'][0], 'count', len(m['logs']))
