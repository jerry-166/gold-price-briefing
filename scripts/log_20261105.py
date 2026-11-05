# -*- coding: utf-8 -*-
"""写入 2026-11-05 早报运行日志"""
import io, json, os

BASE = r'D:/workspace/每日金价资讯'
OUT = os.path.join(BASE, 'logs', '2026-11-05-morning_briefing.json')

mail_body = (
    '主题：🌅 今日金价早报 | 2026年11月05日 周四\n'
    '收件人：2132049351@qq.com ｜ message_id：msg_WOck2_ycC9mqyLbgyN3yNZ1YENwX6EPgg9Y__T3myB6eQA ｜ 确认时间 09:07 CST\n'
    '正文要点：一句话（选举→美元跌→金价单日+3.29%，但属情绪修复别追高）｜快照表（积存金 884.5 +0.87%、AU9999 878.0 +1.65%、汇率 6.72 0.00%、伦敦金 4095.2 +0.87%）｜'
    '⚠ 31 元里 23.5 元是补昨天记低的（昨晨快照 3951.39 vs 真实收盘 4060.01，真实涨幅仅 7.6 元）｜昨夜五件事（中期选举、油价崩 9%、ADP 8.6 万推高 12 月加息至 81.5%、民主党拿下参议院堵死重塑美联储、机构警告或看 3500）｜'
    '趋势（短中性/中偏空/长看多，观望别追高）｜买卖时机（买 4050-4060 约 875-877、3980-4000 约 860-864；卖 4120-4140 约 890-894、4180-4200 约 903-907；止损破 4020 约 868）｜'
    '今日学一招（加息概率 81.5% 为何金价还能涨 3%：两张价签）｜网站链接。HTML 13 098 字节 / 152 行 / 最长行 260 字符。'
)

log = {
    'date': '2026-11-05',
    'type': 'morning_briefing',
    'status': 'success',
    'summary': '延迟约 2 分钟（观察期最低），选举反弹第二日金价 4095.2 美元、积存金 884.5 元/克；邮件已发，日志与 buglog 已提交。',
    'timestamp': '09:08 CST',
    'steps': [
        {
            'num': 1, 'name': '获取数据', 'status': 'success', 'duration_ms': 100000,
            'result': '伦敦金 4095.22（+0.87%，昨收 4060.01、开 4064.10、高 4096.80、低 4057.76，行情时间戳 09:03:00）；AU9999 878.00（+1.65%，昨收 863.79）；T+D 879.50；中间价 6.7180（11-04 值，今日 9:15 未公布，四源同值确认）；新闻 5 条（中期选举/油价崩/ADP 与加息概率/参议院易手/机构警告）。',
            'source': '新浪财经 hf_XAU＋gds_AU9999＋gds_AUTD、中国货币网、WebSearch（汇通财经/华尔街见闻/中宏网/经济日报）',
        },
        {
            'num': 2, 'name': '生成早报JSON', 'status': 'success', 'duration_ms': 150000,
            'result': '已写入 daily/2026-11-05.json；图表丢 10-07 补 11-05、events 整体 -1（原 index 0 已剔除，无孤儿事件），11-04 点由早盘快照 3951.39 回填为真实收盘 4060.0 并改写事件文案。check_briefing.py 一次 0 error、6 组价位复算全中（首次 3 error：advice 215 字超限＋sell 价位未进 advice，两次收敛至 198 字后通过）。',
        },
        {
            'num': 3, 'name': '更新manifest', 'status': 'success', 'duration_ms': 12000,
            'result': '已追加记录到 manifest.json，briefings 由 75 条增至 76 条，头部为 2026-11-05/周四。',
        },
        {
            'num': 4, 'name': 'Git推送', 'status': 'success', 'duration_ms': 45000,
            'result': '已提交并推送，commit e147d18「每日早报 2026-11-05」，rev-parse 与 ls-remote 均为 e147d182ec994ae4754db3c728dee678eff7efb4。',
        },
        {
            'num': 5, 'name': '发送邮件', 'status': 'success', 'duration_ms': 95000,
            'result': '已发送至 2132049351@qq.com，queued:true，ListMessages(dir=sent) 于 09:07 CST 确认入已发送箱。',
            'outputs': [{'label': '邮件内容', 'body': mail_body}],
        },
    ],
    'summary_stats': {
        'total_steps': 5, 'success_steps': 5, 'failed_steps': 0,
        'total_duration_ms': 402000, 'email_sent': True, 'git_pushed': True,
    },
    'data_notes': [
        '伦敦金取 web 实时口径（hf_XAU），昨收 4060.01 与汇通 4059.92、网易/华尔街见闻 4060.01 一致；NeoData 未调用（本期 python requests 缺失、query.sh 不存在，sina 接口已覆盖三项核心数据）。',
        'AU9999 取上金所延时行情 878.00（09:03:26），昨收 863.79 为 11-04 收盘，涨跌幅分母用该值（+1.65%），不用 11-04 早报的盘中 848.50。',
        '中间价 6.7180 为 11-04 中国外汇交易中心公布值（中宏网/经济日报/中国货币网/中新网四源同值），今日 9:15 才公布新值，故涨跌幅记 0.00；在岸即期收 6.6770、离岸 6.6652。',
        '积存金 884.5 = 4095.22 × 6.7180 ÷ 31.1035；按在岸即期 6.6770 折算为 879.1，口径差 5.4 元/克。',
        'hero 三层拆解：①昨日快照 3951.39 → 真实收盘 4060.01 差 108.62 美元 ＝ 23.5 元/克（补昨日记低）②真实的国际金续涨 35.21 美元 ＝ 7.6 元/克 ③汇率两日同为 6.7180、贡献 0。23.5+7.6 ＝ 31.1 ≈ 实差 31.0 元。',
        '技术面自算：MA5 3938.0、MA10 3973.2、MA20 4032.3（11-04 已回填），布林上轨 4223.5、中轨 4032.3、下轨 3841.1；今日 4095.2 已站上全部三条均线，为 10-30 破位以来首次。',
    ],
    'buglog_verification': {
        'note': '本期无新增/修复 bug，Open/Fixed/Total 维持 11/9/20；四条观察更新已逐条写入并用 grep -c 与哈希复核。',
        'entries': [
            {'id': 'BUG-003', 'file': '.buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md', 'grep_c': 2, 'bytes': 69262, 'sha1': 'e9329e298aa1d09a5fbcd2712878314552f9a8b9'},
            {'id': 'BUG-006', 'file': '.buglog/bugs/2026-09-14-inspection-email-connector-down.md', 'grep_c': 1, 'bytes': 49814, 'sha1': '5441c43a4f4a32b4372c20d197dd464949808ef7'},
            {'id': 'BUG-012', 'file': '.buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md', 'grep_c': 1, 'bytes': 54938, 'sha1': '43b28b1525fb8450abdab20bf238a47c774e739f'},
            {'id': 'BUG-013', 'file': '.buglog/bugs/2026-09-26-buglog-hook-misfire.md', 'grep_c': 2, 'bytes': 55806, 'sha1': '78b89f189b961a32668f0b78034816c910f71973'},
        ],
        'index_md': {'file': '.buglog/index.md', 'bytes': 43854, 'sha1': 'b3a2aebbc41041be48b86266acb4ce1cfd37d518', 'section': '## 2026-11-05（周四）观察更新'},
    },
}

with io.open(OUT, 'w', encoding='utf-8') as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
print('written', OUT, os.path.getsize(OUT))
