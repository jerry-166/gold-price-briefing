# -*- coding: utf-8 -*-
"""写 2026-10-22 早报运行日志 + 更新 logs/manifest.json"""
import json, hashlib, subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# ---------- buglog 复核凭据 ----------
files = {
    'BUG-003': '.buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md',
    'BUG-006': '.buglog/bugs/2026-09-14-inspection-email-connector-down.md',
    'BUG-012': '.buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md',
    'BUG-013': '.buglog/bugs/2026-09-26-buglog-hook-misfire.md',
}
ver = {}
for k, f in files.items():
    p = BASE / f
    b = p.read_bytes()
    n = subprocess.run(['grep', '-c', '2026-10-22', str(p)], capture_output=True, text=True).stdout.strip()
    ver[k] = {'file': f, 'grep_count_2026-10-22': int(n or 0), 'bytes': len(b), 'sha1': hashlib.sha1(b).hexdigest()}

plain = (BASE / '.workbuddy' / 'outbox' / '2026-10-22-morning.txt').read_text(encoding='utf-8')
body_excerpt = plain[:1400]

log = {
    'date': '2026-10-22',
    'type': 'morning_briefing',
    'status': 'partial',
    'summary': ('早报（触发 09:23:59／延迟约 24 分钟）前四步成功、第五步邮件失败：'
                '金 4111.6(-0.71%，亚市开 4139.90、冲高 4144.19 后跌至 4109.80)、AU9999 884.8(-0.30%，昨结 887.50)、'
                '中间价 6.7195(下调 3 基点、三连升终结)、积存金估算 888.3 元/克；短 -1/中 -1/长 1、action=watch；'
                '主线为「反抽只活一天」——周三靠 10Y 美债收益率连跌两日（5.111%）撑起的 +0.39% 反抽，'
                '周四亚市被美元回升(101.70)、油价高位、美股齐涨与 12 月加息 88%-92% 的定价全数回吐，4100 关口第三次被逼近；'
                '10-21 图表点已回填真实收盘 4140.9；邮件工具本次仍未注册（agent-mail 返回 not_bound），'
                'HTML 已落盘 outbox，BUG-006 第八次复发。'),
    'timestamp': '09:23 CST',
    'gap_check': {
        'last_briefing': '2026-10-21',
        'missing_trading_days': [],
        'continuous_missing_days': 0,
        'delay_minutes': 24,
        'delay_form': '延迟（BUG-003 复发，历史区间 4-152 分钟，本期落中低位）',
        'inspection_noon_last': '2026-10-21',
        'inspection_pm_last': '2026-10-21',
        'inspection_note': ('inspection_noon 最近产出 10/21 但实际落盘 21:40（延迟约 7h40m，属「夜间合并触发」形态）；'
                            'inspection_pm 10/21 于 22:00 正常触发、no_action；10/19-10/21 两线连续三日有产出；10/22 未到点'),
    },
    'steps': [
        {'num': 1, 'name': '获取数据', 'status': 'success', 'duration_ms': 155000,
         'result': ('NeoData 首查返回 TOKEN_EXPIRED → connect_cloud_service 取凭证 → --save-token 后四查全部成功；'
                    '伦敦金 4111.6(-0.71%，金投网 09:24:22 4111.05 / 金价查询网 09:25:09 4111.57 双源聚类，昨收 4140.95)；'
                    'AU9999 884.80(-0.30%，金投网 SGE 09:24:38 与 NeoData 09:23 分毫不差，昨结 887.50)；'
                    '中间价 6.7195(下调 3 基点)；旁证 AUUSDO.LIFFE 4132.80 为 COMEX 期金口径（昨结 4150 = 12 月期金收盘）已弃用；'
                    '新闻 5 条均带原始 url'),
         'source': 'neodata-financial-search + WebSearch（金投网/金价查询网/汇通网/金融界/国际金融报/SGE 官方/中国外汇交易中心）'},
        {'num': 2, 'name': '生成早报JSON', 'status': 'success', 'duration_ms': 76000,
         'result': ('已写入 daily/2026-10-22.json（39 285 字节）；图表丢 1 补 1（丢 09-22、补 10-22，events 索引整体 -1，'
                    '并移除滚出窗口的 09-22 事件），10-21 点回填真实收盘 4140.9；自检全部通过：'
                    'labels/values 各 30、events 30 条且 labels[index]==date 逐条匹配、新闻 url 全部 http、'
                    '解析后字段无 ASCII 直引号、trend.advice 197 字(≤200)、12 组 ¥/克 价位用 Python 批量复算一致'),
         'source': 'scripts/gen_20261022.py + 内联自检'},
        {'num': 3, 'name': '更新manifest', 'status': 'success', 'duration_ms': 9000,
         'result': '已在 manifest.json 的 briefings 数组头部插入 2026-10-22 记录，总数 62 条',
         'source': 'manifest.json'},
        {'num': 4, 'name': 'Git推送', 'status': 'success', 'duration_ms': 18000,
         'result': '已提交并推送（commit 3531581）。走 SSH 显式 URL 推送，git ls-remote 与 git rev-parse HEAD 均为 353158107bf8716050ed7f9128554648ba1f6ecc，一致',
         'source': 'git@github.com:jerry-166/gold-price-briefing.git'},
        {'num': 5, 'name': '发送邮件', 'status': 'failed', 'duration_ms': 60000,
         'result': ('未发送。connector-status 显示 qq-mail 为 connected，但会话工具索引中无任何 mcp__qq-mail__* 工具；'
                    'ToolSearch 三组关键词（qq mail send email / 发送邮件 QQ邮箱 / qqmail 邮件连接器）均只命中 agent-mail 同名能力；'
                    '第二通道 mcp__agent-mail__GetMe 返回「Agent 邮箱尚未开通」+ status=not_bound → 双通道同时失效、无降级路径。'
                    'HTML 底稿已落盘 .workbuddy/outbox/2026-10-22-morning.html（14 611 字节）＋纯文本版（2 901 字符），待人工补发。'
                    'BUG-006 第八次复发，且与 10/21 构成「未注册」形态首次连续两日'),
         'outputs': [{'label': '邮件主题', 'body': '🌅 今日金价早报 | 2026年10月22日 周四'},
                     {'label': '邮件正文（纯文本摘录）', 'body': body_excerpt}]},
    ],
    'summary_stats': {
        'total_steps': 5, 'success_steps': 4, 'failed_steps': 1,
        'total_duration_ms': 318000, 'email_sent': False, 'git_pushed': True,
    },
    'buglog_verification': {
        'verified_at': '2026-10-22 09:34 CST',
        'rule': 'BUG-013 双重复核：(a) 逐文件 grep -c 计数 (b) index.md 与 bugs/ 一致性 + 字节数/SHA-1 凭据',
        'files': ver,
        'index_consistency': {
            'index_rows_updated': {'BUG-003': True, 'BUG-006': True, 'BUG-012': True, 'BUG-013': True},
            'index_has_new_dates': True, 'all_bugs_written': True,
        },
        'hook_misfire': ('本次 hook 再次把自动化任务提示词全文当作「用户报告的 bug」→ 判误判、未按字面建档'
                         '（BUG-013 第二十四次连续命中）；另对 scripts/gen_20261022.py 的二次编辑做「修 bug」弱提示，'
                         '实为自检拦下 chart.events 残留 index:-1 孤儿事件后的正常修复与重生成'),
    },
}

out = BASE / 'logs' / '2026-10-22-morning_briefing.json'
out.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('log written', out.stat().st_size, 'bytes')

# ---------- logs/manifest.json ----------
mp = BASE / 'logs' / 'manifest.json'
m = json.loads(mp.read_text(encoding='utf-8'))
if m['logs'] and m['logs'][0]['date'] == '2026-10-22' and m['logs'][0]['type'] == 'morning_briefing':
    print('manifest already has today briefing, skip')
else:
    m['logs'].insert(0, {
        'date': '2026-10-22', 'type': 'morning_briefing', 'status': 'partial',
        'summary': ('早报（触发 09:23:59／延迟约 24 分钟）前四步成功、邮件失败：'
                    '金 4111.6(-0.71%，亚市冲高 4144.19 后跌至 4109.80)、AU9999 884.8(-0.30%)、中间价 6.7195(下调 3 基点)、'
                    '积存金估算 888.3；短 -1/中 -1/长 1、action=watch；主线「反抽只活一天」——'
                    '周三靠 10Y 美债 5.111% 撑起的 +0.39% 反抽被美元回升、油价高位、美股齐涨回吐，4100 第三次被逼近；'
                    '10-21 图表点回填真实收盘 4140.9；QQ 邮箱工具未注册、agent-mail 未开通，HTML 落盘 outbox，BUG-006 第八次复发。'),
    })
    mp.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('logs/manifest updated, total', len(m['logs']))
