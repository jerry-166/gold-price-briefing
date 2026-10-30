# -*- coding: utf-8 -*-
"""2026-10-29 早报运行日志 + index.md 观察更新"""
import json, io, os, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = '2026-10-29'

# ---------- index.md 观察更新 ----------
idx = os.path.join(BASE, '.buglog', 'index.md')
s = io.open(idx, encoding='utf-8').read()
section = """
## 2026-10-29（周四）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 20 分钟（09:20:04 起始实测、09:24:53 收尾），序列 47 日 …/约 51/275/约 20，为本月第二低位；10/19-10/29 连续十一日、九个交易日无缺跑无提前。注意前一日 275 分钟，摆动无收敛迹象 |
| BUG-006 | **正常（第 14 次观察）**：ToolSearch 精确名一次命中、`SendMessage` 标准写法直发返回 `queued: true`、无需 confirmation_token 往返；形态序列 正常×3（10/25-10/27）→ 复发（10/28）→ 正常（10/29）。连续正常计数重新从 1 起算，距「连续 ≥5 日」门槛仍有 4 日 |
| BUG-012 | 两线最近产出均为 10/28（noon 14:05 延迟 5 分钟、pm 22:00 准点 no_action），连续零产出交易日数 0，未达复合判据；`grep -c 2026-10-28-inspection` ＝ 2 |
| BUG-013 | 第 31 次连续命中，判误判跳过建档；附带误报为两个新脚本的正常迭代（自检验证 float 值、汇率精度改 2 位、邮件 HTML 拆行改动导致的临时 SyntaxError）；双重复核已执行 |
"""
if '2026-10-29（周四）观察更新' not in s:
    if not s.endswith('\n'):
        s += '\n'
    s += section
    io.open(idx, 'w', encoding='utf-8', newline='\n').write(s)
    print('index.md updated')
else:
    print('index.md already has 10-29 section')

# ---------- 复核凭据 ----------
files = ['2026-09-08-briefing-scheduler-missed-days.md',
         '2026-09-14-inspection-email-connector-down.md',
         '2026-09-25-inspection-scheduler-silent-miss.md',
         '2026-09-26-buglog-hook-misfire.md']
ver = {'date_marker': DATE, 'per_file': []}
for f in files:
    p = os.path.join(BASE, '.buglog', 'bugs', f)
    b = open(p, 'rb').read()
    txt = b.decode('utf-8')
    ver['per_file'].append({
        'file': f,
        'grep_count': txt.count(DATE),
        'bytes': len(b),
        'sha1': hashlib.sha1(b).hexdigest(),
    })
ib = open(idx, 'rb').read()
ver['index_md'] = {'bytes': len(ib), 'sha1': hashlib.sha1(ib).hexdigest(),
                   'has_2026_10_29_section': '2026-10-29（周四）观察更新' in ib.decode('utf-8')}
st = json.load(open(os.path.join(BASE, '.buglog', 'stats.json'), encoding='utf-8'))
ver['stats'] = st

# ---------- 运行日志 ----------
STEP = [
    {'num': 1, 'name': '获取数据', 'status': 'success', 'duration_ms': 106000,
     'result': ('伦敦金 4054.09 美元/盎司（09:14:55 金投网，-13.25／-0.33%，昨收 4067.34）；'
                'AU9999 870.6 元/克（上金所延时行情 09:20，基准 10/28 收盘 868.99，+0.19%）；'
                '中间价 6.7147（调升 18 基点，四源同值）；新闻 5 条（美联储 10:2 维持利率、沃什取消前瞻指引、'
                '今晚 20:30 GDP+PCE+初请、胡塞袭击沙特炼油厂推油价、人民币中间价续升）'),
     'source': '金投网 + 上海黄金交易所 + WebSearch（证券时报/汇通财经/每日经济新闻/同花顺/东方财富）'},
    {'num': 2, 'name': '生成早报JSON', 'status': 'success', 'duration_ms': 62000,
     'result': '已写入 daily/2026-10-29.json（自检 0 error；ASCII 引号 0 处；chart 30/30、events 30 条日期索引逐条对齐）'},
    {'num': 3, 'name': '更新manifest', 'status': 'success', 'duration_ms': 8000,
     'result': '已追加记录到 manifest.json（briefings 头部插入 2026-10-29，共 69 条）'},
    {'num': 4, 'name': 'Git推送', 'status': 'success', 'duration_ms': 22000,
     'result': '已提交并推送 f401d95，git ls-remote 与 rev-parse 一致（SSH 通道）'},
    {'num': 5, 'name': '发送邮件', 'status': 'success', 'duration_ms': 91000,
     'result': '已发送至 2132049351@qq.com（queued: true，skip_confirmation 直发，未触发 confirmation_token 往返）',
     'outputs': [{'label': '邮件内容',
                  'body': ('主题：🌅 今日金价早报 | 2026年10月29日 周四\n'
                           '金价快照：积存金估算 875.2 元/克（-0.33%）｜AU9999 870.6（+0.19%）｜'
                           '伦敦金 4054.1 美元（-0.33%）｜中间价 6.71（调升 18 基点）\n'
                           '昨夜今晨：美联储 10:2 维持 3.75%-4%（两张反对票主张加息）／沃什取消前瞻指引并削减明年议息次数／'
                           '今晚 20:30 三季度 GDP＋9 月 PCE＋初请三雷同发／胡塞导弹袭击沙特拉斯塔努拉炼油厂推油价回 100 上方\n'
                           '趋势：短 0／中 -1／长 1，action=watch\n'
                           '买卖时机：买 4036-4040（871-872 元/克）／4010-4020（866-868）／3990-4000（861-864）；'
                           '卖 4082-4085（881-882）／4100-4110（885-887）；止损收盘破 4036、破 3990 离场\n'
                           '今日学一招：美联储『不预告下一步』为什么对金价是坏消息（前瞻指引退场 → 波动搬到数据日）\n'
                           '底部链接：https://jerry-166.github.io/gold-price-briefing/')}],
     },
]

log = {
    'date': DATE,
    'type': 'morning_briefing',
    'status': 'success',
    'summary': ('触发 09:20:04（延迟约 20 分钟）；数据/JSON/manifest/Git/邮件五步全部成功，'
                '伦敦金 4054.09、AU9999 870.6、中间价 6.7147，邮件 queued:true'),
    'timestamp': '09:20 CST',
    'steps': STEP,
    'summary_stats': {
        'total_steps': 5, 'success_steps': 5, 'failed_steps': 0,
        'total_duration_ms': 289000, 'email_sent': True, 'git_pushed': True,
    },
    'gap_check': {
        'last_morning_briefing': '2026-10-28',
        'last_status': 'success',
        'missed_trading_days': [],
        'note': '上次早报 10/28（周三）全部成功，10/29 为其后第一个交易日，其间无缺失交易日 → 无断档',
    },
    'health_check': {
        'inspection_noon_last': '2026-10-28',
        'inspection_pm_last': '2026-10-28',
        'consecutive_zero_output_trading_days': 0,
        'note': ('两条线 10/28 同日双产出（noon 14:05、pm 22:00 准点 no_action），未达 BUG-012 复合升级判据；'
                 '未用历史读数相同当作「持续正常」的证据'),
    },
    'scheduler': {
        'nominal': '09:00', 'actual': '09:20:04', 'delay_minutes': 20,
        'form': '延迟（正常触发）', 'note': '落在 4-275 分钟极宽摆动区间低位；前一日 10/28 为 275 分钟',
    },
    'buglog_verification': ver,
    'notes': {
        'idempotency': 'daily/2026-10-29.json 事前不存在、logs/manifest.json 头部无当日记录、git log 无当日早报提交 → 无中断残留',
        'chart_roll': '丢 09-29、补 10-29；10-28 由亚市快照 4035.0 回填为真实收盘 4067.3，事件文案同步改写为全日「先跌后涨」；events 索引整体 -1 并剔除 index<0 的 09-29（本期恰为 index 0）',
        'hero_layers': '875.2 = 871.3(昨晨估算) + 7.0(昨晨快照 4035.0 → 真实收盘 4067.3) - 2.9(今日盘中 -13.25 美元) - 0.2(人民币升值 18bp)；口径差：中间价折算比市场即期约高 6 元/克',
        'deviation': '第 ⑦ 条 in_progress 占位兜底未启用（会话单段连续完成、无中断），如实记录',
    },
}

out = os.path.join(BASE, 'logs', DATE + '-morning_briefing.json')
with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('log written', out, len(open(out, 'rb').read()), 'bytes')
