# -*- coding: utf-8 -*-
"""写入 2026-11-17 早报运行日志与 logs/manifest 摘要"""
import json, os, io, collections, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(BASE, 'logs', '2026-11-17-morning_briefing.json')
MAN = os.path.join(BASE, 'logs', 'manifest.json')

MAIL_HTML = os.path.join(BASE, '.workbuddy', 'outbox', 'mail-2026-11-17.html')
mail_html = io.open(MAIL_HTML, encoding='utf-8').read()

log = collections.OrderedDict()
log['date'] = '2026-11-17'
log['type'] = 'morning_briefing'
log['status'] = 'partial'
log['summary'] = ('数据、早报 JSON、manifest、Git 推送全部成功；QQ Mail 工具未装载（BUG-006 复发）导致邮件未发出，'
                  '邮件 HTML 已落 .workbuddy/outbox/mail-2026-11-17.html 待人工补发')
log['timestamp'] = '13:17-13:26 CST'
log['trigger_delay_minutes'] = 257
log['gap_check'] = collections.OrderedDict([
    ('last_morning_briefing', '2026-11-16'),
    ('last_status', 'success'),
    ('gap_days', 0),
    ('missed_trading_days', []),
    ('inspection_noon_last', '2026-11-16（no_action）'),
    ('inspection_pm_last', '2026-11-16（partial，波动预警）'),
    ('note', '早报链路无断档；午后/晚间巡检两条线最近产出日均 2026-11-16，11-14/11-15 为周末不计分母')
])
log['delay_impact'] = ('本期延迟 257 分钟且当日有行情，危害判据命中「延迟区间覆盖当日关键价格窗口」（11-16 新增第三条判据）：'
                       '09:00 时伦敦金约 3855（日内 -0.03%，方向接近持平），13:17 已反弹到 3875.12（+0.49%）——'
                       '方向由「持平/微跌」翻为「上涨」，约 20 美元的日内反弹全部发生在延迟窗口内。按分钟数分级为 1 档。')
log['steps'] = [
    collections.OrderedDict([
        ('num', 1), ('name', '获取数据'), ('status', 'success'), ('duration_ms', 278000),
        ('result', ('伦敦金 3875.12（+18.88／+0.49%，昨收 3856.24、开 3858.88、高 3879.90、低 3843.45）；'
                    'AU9999 832.45（+2.96／+0.36%，基准 11-16 日盘收盘 829.49，开 830.00、高 836.88、低 825.01）；'
                    '中间价 6.7132（调升 9 个基点）；积存金估算 836.4；旁证 COMEX 主力 3877.6（+0.64%）、T+D 831.87、'
                    '沪金主力 828.26、沪银主力 11207、DXY 103.58、10Y 5.124%、2Y 4.821%、'
                    'WTI 12 月 85.72（-3.21%）、布伦特 1 月 92.44（-3.55%）。'
                    '本次取数走「新浪 hf_XAU/gds_ 实时接口 + WebSearch 交叉验证」；neodata-financial-search skill 本地未安装脚本，未调用。')),
        ('source', '新浪财经实时行情 + 上海黄金交易所 + 中国外汇交易中心/中国新闻网 + WebSearch（汇通财经/财联社/央视财经/中金在线）')
    ]),
    collections.OrderedDict([
        ('num', 2), ('name', '生成早报JSON'), ('status', 'success'), ('duration_ms', 120000),
        ('result', '已写入 daily/2026-11-17.json；图表丢 10-18 补 11-17（events 索引 -1），11-16 点由快照 3874.6 回填为真实收盘 3856.2；check_briefing.py 首轮 0 error（advice 200 字、pairs 15 组）')
    ]),
    collections.OrderedDict([
        ('num', 3), ('name', '更新manifest'), ('status', 'success'), ('duration_ms', 30000),
        ('result', '已在 briefings 数组头部插入 {date:2026-11-17, weekday:周二}，共 88 条')
    ]),
    collections.OrderedDict([
        ('num', 4), ('name', 'Git推送'), ('status', 'success'), ('duration_ms', 30000),
        ('result', 'commit 2111a79「每日早报 2026-11-17」；SSH 推送成功，git rev-parse HEAD 与 git ls-remote refs/heads/master 均为 2111a79')
    ]),
    collections.OrderedDict([
        ('num', 5), ('name', '发送邮件'), ('status', 'failed'), ('duration_ms', 70000),
        ('result', ('未发送 —— BUG-006 复发：ToolSearch 精确名检索 mcp__qq-mail__SendMessage/GetMe/ListMessages 全部回落 agent-mail 命名空间，'
                    '关键词检索同样回落；list_installed_plugins 显示 qq-mail connected/bound/enabled 三真（索引未装载的第 3 种证据组合）；'
                    '备用 agent-mail GetMe 返回 not_bound；reconnect_plugin 返回 User refused（无人值守无人确认）。'
                    '邮件 HTML 已落 .workbuddy/outbox/mail-2026-11-17.html（13 879 字符／19 605 字节／70 行／maxline 929／零 100%%）待人工补发')),
        ('outputs', [collections.OrderedDict([('label', '邮件内容'), ('body', mail_html)])])
    ])
]
log['summary_stats'] = collections.OrderedDict([
    ('total_steps', 5), ('success_steps', 4), ('failed_steps', 1),
    ('total_duration_ms', 537000), ('email_sent', False), ('git_pushed', True)
])
log['buglog_verification'] = collections.OrderedDict([
    ('note', '本期 buglog 在日志之后单独写入，凭据见 .buglog/index.md 的「本期 buglog 复核凭据」小节')
])

with io.open(LOG, 'w', encoding='utf-8') as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
    f.write('\n')

man = json.load(io.open(MAN, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
if man['logs'][0]['date'] != '2026-11-17':
    man['logs'].insert(0, collections.OrderedDict([
        ('date', '2026-11-17'), ('type', 'morning_briefing'), ('status', 'partial'),
        ('summary', '数据/JSON/manifest/推送全部成功；QQ Mail 工具未装载，邮件未发出（HTML 已落 outbox 待人工补发）')
    ]))
with io.open(MAN, 'w', encoding='utf-8') as f:
    json.dump(man, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('log written', LOG)
print('logs total', len(man['logs']), man['logs'][0])
print('mail html sha1', hashlib.sha1(mail_html.encode('utf-8')).hexdigest())
