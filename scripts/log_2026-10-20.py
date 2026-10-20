# -*- coding: utf-8 -*-
"""写入 2026-10-20 早报运行日志 + buglog 留痕（双重复核：grep -c 计数 + 字节数/SHA-1）"""
import json, io, os, hashlib, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUG = os.path.join(BASE, '.buglog', 'bugs')

# ---------------- 1. 各 bug 文件追加 10-20 条目 ----------------
APPEND = {
 '2026-09-08-briefing-scheduler-missed-days.md':
  '\n**2026-10-20（周二）— 第二十二期留痕（延迟形态，未缺跑、未提前）**：会话内首次 `date` 实测 **09:50:24 CST**，为本次会话第二个工具调用，会话起始按 09:50 估算 → **延迟约 50 分钟**（区间内中位偏低）。序列续记至 9/13-10/20 共 37 日：…/40/71/37/78/67/41/**约 50**。**定性维持「4-133 分钟极宽摆动」**；本期延迟 50 分钟导致取价时点落在亚市已运行约 50 分钟处（取到 4127.04，而非今开 4140.10），当日已打出 4115.55-4143.70 的 28 美元振幅，若准点 09:00 取价会更贴近开盘 → **建议 ②（定时提前至 07:00-07:30）继续维持**。**第 ⑦ 条 in_progress 占位兜底本期未启用**（会话单段连续完成、无中断），如实记为执行偏离。幂等检查前置：`daily/2026-10-20.json` 不存在、`logs/manifest.json` 头部无当日 morning_briefing 记录、`git log` 无当日早报提交 → 无中断残留（BUG-014 未复现）。前置缺口检查：上次早报 10/19（周一，partial／邮件失败但数据与推送成功），10/20 为其后第一个交易日，其间无缺失交易日 → 无断档。\n',

 '2026-09-14-inspection-email-connector-down.md':
  '\n**2026-10-20（周二）— 恢复正常，形态回到「一次调用即成功」**：`mcp__qq-mail__SendMessage` 经 ToolSearch 按名检索**一次命中**（既非 10/19 的「工具未注册」，亦非 10/15 的「调用即 -32602」），以标准写法（`to` 传对象数组）＋`body_format: HTML`＋`skip_confirmation: true` 直发，返回 `{"data": {"queued": true, "_hints": {...POST /v1/aliases/alias_A9yF9wF5eP0o6Tc1uUpRq71T8H09/messages/send}}}` → **邮件已入队、判定发送成功**（`email_sent: true`）；HTML 底稿同步落 `.workbuddy/outbox/2026-10-20-morning-briefing.html`（14 197 字节）留档备查。**形态序列更新**：`未注册`（10/6、10/10、10/12）→ `注册但 -32602`（10/15）→ `正常`（10/16、10/17、10/18）→ `未注册`（10/19）→ **`正常`（10/20）**。**本日成功不构成修复证据**——10/16-10/18 曾连续三日正常、第 4 日即复发已证伪一次；severity 维持 major、status 维持 open，「最长正常窗口 ≈ 3 日」观察基线维持不变，本期为复发后第 1 日恢复。\n',

 '2026-09-25-inspection-scheduler-silent-miss.md':
  '\n**2026-10-20（周二）— 提前触发形态再现，pm 线提前幅度创观察期纪录**：`logs/2026-10-20-inspection_pm.json` 已落盘（`logs/manifest.json` 头部自述为「晚间巡检（22:00定时，09:40提前触发）」）→ 相对名义 22:00 **提前约 12 小时 20 分钟**，属「提前触发」形态（非静默缺跑），且超过 10/17 的约 12 小时，为观察期内最大提前量。① **noon 线**：最近产出 10/19（`2026-10-19-inspection_noon.json`），10/20 的 14:00 未到 → 暂无新数据；② **pm 线**：10/19 pm **零产出**（`ls logs/ | grep -c 2026-10-19-inspection_pm` ＝ 0），10/20 pm 提前于 09:40 产出 → 「一起缺跑／一起提前」的同步镜像本期**只能部分成立**（pm 单线提前、noon 尚未到点，无法判定同步性），如实记录不推定；③ **连续零产出交易日数**：按「早报线有产出即当日非零产出」的既有口径，10/20 已有早报产出 → 当前连续数 = **0**，**未达复合判据**（连续 ≥5 个正常交易日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出，两项须同时满足）→ **不升级、不降级**，观察期自 10/15 起算仍在 2 周窗口内；④ 待办 ①②③④⑤⑥⑦⑧⑨⑩⑪ 全部维持。\n',

 '2026-09-26-buglog-hook-misfire.md':
  '- **2026-10-20 第二十二次连续命中（9/26-10/20）**：会话开局 hook 再次把自动化任务提示词全文当作「用户报告的 bug」透传（原文以「你是金价早报自动化助手」开头、含「第一步/第二步」流程编号、无异常现象也无期望行为），**判为误判、未按字面建档**；改为人工盘点本次会话真实异常（BUG-003 延迟约 50 分钟、BUG-006 本期恢复正常、BUG-012 pm 线提前约 12 小时 20 分），逐条写入对应 bug 文件。\n- **附带误报**：本期 hook 另在 `Edit` 操作后追问「同一文件被编辑 ≥2 次，通常表示在修复 bug」——实际为 `scripts/build_2026-10-20.py` 因 `trend.advice` 初稿 203 字超 200 上限而两次压缩（203→196→195）触发的正常自检返工，非修 bug。本期工具调用**零失败、零报错、零用户纠正**。\n- **双重复核（10/16 修订要求）本期已执行**：写入后以 `grep -c "2026-10-20" .buglog/bugs/*.md` 逐文件计数，并把四个 bug 文件的字节数与 SHA-1 写入 `logs/2026-10-20-morning_briefing.json` 的 `buglog_verification` 字段（见该文件）。\n- **index.md 与 bugs/ 一致性**：本期已把 10/20 结论同步追加到 `index.md` 的 BUG-003/006/012/013 四行末尾 → 本次未复现「声明与产物脱节」。\n',
}

for name, text in APPEND.items():
    p = os.path.join(BUG, name)
    with io.open(p, 'a', encoding='utf-8') as f:
        f.write(text)
    print('appended:', name)

# ---------------- 2. index.md 四行末尾同步 ----------------
INDEX_ADD = {
 9:  '；**10/20 延迟约 50 分钟（会话内首次 `date` 实测 09:50:24，起始按 09:50 估），序列续记至 9/13-10/20 共 37 日：…/78/67/41/约 50，定性仍为「4-133 分钟极宽摆动」；第 ⑦ 条 in_progress 占位兜底本期未启用（会话单段连续完成），如实记为执行偏离**',
 12: '；**10/20 恢复正常：`SendMessage` 经 ToolSearch 一次命中、标准写法直发，返回 queued:true，`email_sent: true`，HTML 底稿落 `.workbuddy/outbox/2026-10-20-morning-briefing.html`（14 197 字节）；形态序列 未注册(10/6/10/10/12)→-32602(10/15)→正常(10/16-10/18)→未注册(10/19)→正常(10/20)；本日成功不构成修复证据（10/16-10/18 三日正常后第 4 日即复发已证伪），severity 维持 major**',
 18: '；**10/20 四维体检：`inspection_pm` 于 09:40 提前触发（`logs/2026-10-20-inspection_pm.json` 已落盘、manifest 头部自述「22:00定时，09:40提前触发」），相对标称 22:00 提前约 12 小时 20 分、创观察期最大提前量；`inspection_noon` 最近产出 10/19、10/20 的 14:00 未到；10/19 pm 零产出（`grep -c 2026-10-19-inspection_pm`＝0）；按「早报线有产出即当日非零产出」口径连续零产出交易日数＝0，未达复合判据 → 不升级不降级，观察期自 10/15 起算仍在 2 周窗口内**',
 19: '；**10/20 第二十二次连续命中（9/26-10/20），hook 再次透传自动化提示词全文 → 判误判、未按字面建档；附带误报本期形态：把 `scripts/build_2026-10-20.py` 的 advice 203→196→195 字两次压缩（正常自检返工）弱提示为在修 bug，忽略；本期工具调用零失败、零报错、零用户纠正；双重复核已执行（逐文件 `grep -c` 计数＋四文件字节数/SHA-1 写入 logs 的 buglog_verification），index 与 bugs/ 已同步**',
}

ip = os.path.join(BASE, '.buglog', 'index.md')
lines = io.open(ip, encoding='utf-8').read().split('\n')
for ln, add in INDEX_ADD.items():
    i = ln - 1
    assert lines[i].rstrip().endswith('| major | open |') or '| open |' in lines[i], (ln, lines[i][-40:])
    # 插到最后一个 " | major | open |" 之前
    marker = ' | major | open |'
    if marker in lines[i]:
        j = lines[i].rfind(marker)
        lines[i] = lines[i][:j] + add + lines[i][j:]
    else:
        j = lines[i].rfind(' | open |')
        lines[i] = lines[i][:j] + add + lines[i][j:]
    print('index patched line', ln)
io.open(ip, 'w', encoding='utf-8').write('\n'.join(lines))

# ---------------- 3. 双重复核凭据 ----------------
files = ['2026-09-08-briefing-scheduler-missed-days.md',
         '2026-09-14-inspection-email-connector-down.md',
         '2026-09-25-inspection-scheduler-silent-miss.md',
         '2026-09-26-buglog-hook-misfire.md',
         '.buglog/index.md']
grep_counts, bytes_sha = {}, {}
for rel in files:
    p = os.path.join(BASE, rel) if rel.startswith('.buglog') else os.path.join(BUG, rel)
    data = io.open(p, 'rb').read()
    txt = data.decode('utf-8')
    key = rel if rel.startswith('.buglog') else '.buglog/bugs/' + rel
    grep_counts[key] = txt.count('2026-10-20')
    bytes_sha[key] = '%dB / %s' % (len(data), hashlib.sha1(data).hexdigest())
    print('verify:', key, grep_counts[key], bytes_sha[key])

assert all(v >= 1 for v in grep_counts.values()), grep_counts

# ---------------- 4. 写运行日志 ----------------
MAIL_BODY = '''🌅 今日金价早报 | 2026年10月20日 周二

【今日金价快照】
· 招行积存金买入价（估算）★ 891.7 ¥/克 -0.33%
· 上海金 AU9999 891.2 ¥/克 -1.08%
· 美元汇率 6.72 USD/CNY -0.01%
· 伦敦金 XAUUSD 4127.0 $/盎司 -0.33%

【昨夜与今晨大事】
1）加息定价更硬：CME 10 月维持不变 82.8%、加息 25bp 17.2%，但 12 月只剩 6.4% 不变、加息 25bp 77.8%、50bp 15.8%——年内至少再加一次 93.6%（昨日约 92%）。10 年期美债回升 5.141%、30 年期 5.477%。
2）AI 股反弹→美债被卖：费半 +1.6% 终结八连跌（此前累跌 15.7%、2008 年 10 月以来最长），纳指 +1.11%、标普 +0.41%、道指 -0.07%；上周躲进美债的避险钱回流股市，10Y 收益率从 5.081% 一夜修复到 5.141%，美元指数涨 0.22% 站到 102 附近。
3）地缘反噬：胡塞 48 小时六袭沙特（延布阿美设施、沙伊巴油田、利雅得与阿布哈机场），一艘油轮在霍尔木兹南部触水雷，内塔尼亚胡下令「推翻伊朗政权」；Kpler 称霍尔木兹油流由逾 2000 万桶/日崩至约 850 万桶/日 → 油价创一个月新高（WTI 盘中 99.71、布伦特 110.66）→ 通胀粘性 → 加息预期 → 反而压制金价。
4）俄油利好落空：美国能源部长赖特称「俄罗斯柴油尚未投放市场」，并称要让俄持续出口柴油、乌克兰局势必须改变 → 昨日「俄柴油 15-20 天进美国」的链条第一环断裂，油价不跌反涨。
5）经济暗线：美国住宅建筑商信心降至 14 年低点；高盛称对冲基金以十年来最快速度削减科技股持仓。今晚 20:30 美国 9 月新屋开工、营建许可、成屋签约销售为检验数据。
6）长线买盘仍在：世界黄金协会 8 月全球央行净购金 39 吨（中国 20、乌兹别克 8、波兰 8），中国连买 23 个月、储备 7747 万盎司，国内 13 只黄金主题 ETF 10 月净流入 64.18 亿元。业内定位为「底部区间」而非「硬地板」。

【趋势怎么看】短期 偏空 ↓｜中期 偏空 ↓｜长期 偏强 ↑（action = watch）
一句话：早盘探 4115.55 后回到 4127，箱体下沿 4130 失守、4100 未破，属破位待确认。仓位 8:2，积存金定额买、不加杠杆。

【现在该干嘛】
📥 买入时机：回踩 4115-4120 美元/盎司（约 889-890 元/克）买首档 1/3；4100-4105 美元（约 886-887 元/克）加二档 1/3；4073-4080 美元（约 880-882 元/克）买满兜底档。纪律：今天上午连跌时别挂单接刀，等 4100 附近出现跌不动的信号。
📤 卖出时机：反弹 4187-4200 美元/盎司（约 905-907 元/克）先减 1/3；收盘实体站稳 4235 美元（约 915 元/克）才谈继续持有，上方看 4300（约 929 元/克）；跌破 4100 美元（约 886 元/克）减 1/3，有效跌破 4073 美元（约 880 元/克）清仓观望。
换算基准：4127.04 × 6.7200 ÷ 31.1035 ≈ 891.7 元/克。按中间价折算比按在岸即期（约 6.6817）折算高约 5.2 元/克，属口径差。以上仅供参考，不构成投资建议。

【🎓 今日学一招】为什么「油轮触雷」这样的坏消息，最后会变成黄金的利空？——地缘风险传导到金价的三道关。要点：第一关油价（中东出事→供应受威胁→油价涨）、第二关通胀（油价涨→成本上移→通胀预期回升）、第三关利率（通胀预期回升→美联储不敢松手→加息预期变硬→持有不生息的黄金更贵）。三道关全过，「避险利多」就被「利率利空」吃掉。反转条件：油价涨到市场觉得过头开始回落，或美联储明确停止加息——看到「油价跌 + 金价涨」同时出现才是真信号。

查看完整日报与 30 日走势图 → https://jerry-166.github.io/gold-price-briefing/'''

LOG = {
 'date': '2026-10-20',
 'type': 'morning_briefing',
 'status': 'success',
 'summary': '早报（触发约 09:50／延迟约 50 分钟，BUG-003 复发）五步全部成功：数据→daily/2026-10-20.json→manifest(60 条)→git 推送(2e937bd)→QQ 邮件 queued:true（BUG-006 本期恢复正常）。行情：金价连续第二日走弱，亚市开 4140.10、早盘下探 4115.55，09:49 报 4127.04 美元/盎司(-0.33%)、日内高 4143.70；上金所 Au99.99 报 891.20 元/克(-1.08%，基准 10-19 日盘收盘 900.89)；人民币中间价 6.7200、升 8 个基点；hero 积存金估算 891.7 元/克（较昨晨 901.2 低 9.5 元，其中约 6.5 元为昨日亚市快照虚高、仅约 3.1 元为真实下跌）。趋势短 -1/中 -1/长 1、action=watch；核心叙事「箱体下沿 4130 失守、4100 未破，属破位待确认」。本期关键：昨日 10-19 真实收盘为 4140.90（非早报记录的 4170.87 亚市快照），已回填图表并单列在 hero note；下跌主因是 AI 股反弹→避险资金撤出美债→10Y 由 5.081% 修复至 5.141%→持金成本上升，而非地缘。',
 'timestamp': '09:54 CST',
 'steps': [
  {'num': 1, 'name': '获取数据', 'status': 'success', 'duration_ms': 158000,
   'result': '伦敦金现货取 web 亚市实时价 4127.04 美元/盎司(-0.33%)（金投网实时页 09:49:01，昨收 4140.90、今开 4140.10、最高 4143.70、最低 4115.55；交叉源 汇通 07:31 报 4135.69、金投网 09:19 报 4126.68(-0.34%)、中金在线金财报 4135 附近，指向 4126-4136 区间取 09:49 最新读数）；AU9999 取 SGE 官方延时行情 891.2 元/克(-1.08%，最高 898.0／最低 891.2／今开 897.0，基准 10-19 日盘收盘 900.89；国际金融报 891.20／-1.08%、金价查询网 892.60／-0.92%、金投网 888.50／-1.38% 三源交叉，官方值与平价锚 891.7 偏离仅 -0.06% 故取官方)；中间价 6.7200、较 10-19 的 6.7208 上调 8 个基点（中国新闻网／中国证券网／证券时报／金融界四源一致）；新闻 6 条全部带原始 url（CME 加息定价、美元与美债、地缘与油运、俄油落空、经济暗线、长线买盘）；另取到 10-19 真实收盘 4140.90（推翻昨日早报的亚市快照 4170.87）、美元指数 101.99(+0.20%)、10Y 5.141%／30Y 5.477%、美股三大指数、WTI 98.24／布伦特 109.19、Kpler 霍尔木兹油流 850 万桶/日、CME 12 月至少加一次 93.6%、世界黄金协会 8 月央行净购金 39 吨',
   'source': 'neodata-financial-search + WebSearch'},
  {'num': 2, 'name': '生成早报JSON', 'status': 'success', 'duration_ms': 42000,
   'result': '已写入 daily/2026-10-20.json（30 个 labels／30 个 values／30 条 events；丢 09-20、补 10-20＝4127.04，且 10-19 点由 4170.87 回填为真实收盘 4140.9；events 索引整体 -1 并新增 10-20 条目）。自检全部通过：labels 与 events 逐条日期比对一致、index 连续 0-29、解析后字符串无 ASCII 直/单引号、news 6 条 url 均以 http 开头且 tagType 全部合法、advice 去标签 195 字 ≤200、hero 与 plan 全部 ¥/克 价位 Python 批量复算（4115→889、4120→890、4100→886、4105→887、4073.3→880、4080→882、4187→905、4200→907、4235→915、4300→929、4127.04→891.66）。自检过程一处返工：advice 初稿 203 字超限，两次压缩至 195 字',
   'source': '本地生成脚本 scripts/build_2026-10-20.py'},
  {'num': 3, 'name': '更新manifest', 'status': 'success', 'duration_ms': 3000,
   'result': '已在 briefings 数组头部插入 2026-10-20（title=今日金价早报、weekday=周二），总条数由 59 增至 60；写入前已判断头部为 10-19 且无 10-20 重复记录，具备幂等性',
   'source': 'manifest.json'},
  {'num': 4, 'name': 'Git推送', 'status': 'success', 'duration_ms': 8000,
   'result': '已提交并推送：commit 2e937bd（每日早报 2026-10-20，2 files changed / 424 insertions），走 SSH（git@github.com:jerry-166/gold-price-briefing.git master）；git rev-parse HEAD 与 git ls-remote refs/heads/master 均为 2e937bdedec387d2dc6de63175567aa75e0a489d，远端确认为最新',
   'source': 'git'},
  {'num': 5, 'name': '发送邮件', 'status': 'success', 'duration_ms': 22000,
   'result': '已发送至 2132049351@qq.com：qq-mail 的 SendMessage 经 ToolSearch 一次命中（非 10/19 的「工具未注册」、亦非 10/15 的「-32602」），以标准写法（to 传对象数组）＋body_format=HTML＋skip_confirmation=true 直发，返回 queued:true（_hints 指向 POST /v1/aliases/alias_A9yF9wF5eP0o6Tc1uUpRq71T8H09/messages/send）；HTML 底稿同步落 .workbuddy/outbox/2026-10-20-morning-briefing.html（14 197 字节）。BUG-006 本期未复现，但按既有结论「单日/连续三日成功均不构成修复证据」，severity 维持 major',
   'outputs': [{'label': '邮件内容', 'body': MAIL_BODY}]},
 ],
 'summary_stats': {'total_steps': 5, 'success_steps': 5, 'failed_steps': 0,
                   'total_duration_ms': 233000, 'email_sent': True, 'git_pushed': True},
 'gap_check': {
  'last_successful_briefing': '2026-10-19',
  'is_next_trading_day': True,
  'missed_trading_days': [],
  'consecutive_missed_days': 0,
  'note': '上次早报 10/19（周一，status=partial：数据与推送成功、仅邮件失败），10/20 为其后第一个交易日，10/19→10/20 之间无缺失交易日 → 无断档、未在邮件/日志中标注缺失。'
 },
 'idempotency_check': {
  'daily_file_existed': False,
  'logs_manifest_head_date': '2026-10-20（头部为 inspection_pm 记录，无当日 morning_briefing）',
  'git_log_today_briefing_commit': False,
  'residual_from_interruption': False,
  'note': '三项前置幂等检查全部为「无残留」，按标准流程全量执行，BUG-014 本期未复现。manifest 头部虽已有 10-20 的 inspection_pm 记录，但 type 不同、不构成早报重复，已按类型判定而非仅按日期判定。'
 },
 'health_check': {
  'inspection_noon_last_output': '2026-10-19',
  'inspection_pm_last_output': '2026-10-20（09:40 提前触发）',
  'inspection_noon_actual_vs_nominal': '10-19 实际时点未核，10-20 的 14:00 未到',
  'inspection_pm_actual_vs_nominal': '09:40 vs 22:00（提前约 12 小时 20 分钟，创观察期最大提前量）',
  'today_has_any_inspection_output': True,
  'consecutive_zero_output_trading_days': 0,
  'consecutive_zero_output_detail': '按「早报线有产出即当日非零产出」的既有口径，10-20 已有早报产出 → 连续零产出交易日数 = 0；另 10-19 的 pm 线零产出（grep -c 2026-10-19-inspection_pm = 0）已记入 BUG-012。',
  'weekend_note': '10-18（周日）两条线零产出已在 10-19 期留痕；本期不涉及周末。',
  'escalation': '未达复合判据（连续 ≥5 个正常交易日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出，两项须同时满足）→ 不升级、不降级；观察期自 10-15 起算仍在 2 周窗口内。',
  'note': 'pm 线 09:40 提前触发属 BUG-012 的「提前触发」形态，且提前量超过 10-17 的约 12 小时；noon 线 14:00 未到，无法判定两条线是否同步，不推定。'
 },
 'buglog_verification': {
  'grep_counts': grep_counts,
  'grep_pattern': '2026-10-20',
  'file_bytes_and_sha1': bytes_sha,
  'index_vs_bugs_consistent': True,
  'note': '本期四条 bug（003 延迟约 50 分钟／006 恢复正常／012 pm 线提前触发／013 hook 第二十二次误判）均已写入对应 bugs/ 文件并在 index.md 四行末尾同步追加 10-20 结论；写入后逐文件 grep -c 均 ≥1（见 grep_counts），字节数与 SHA-1 见上，index 与 bugs/ 已核对一致。'
 },
 'notes': [
  '本期 hook 再次把自动化任务提示词全文当作「用户报告的 bug」透传，判为 BUG-013 误判、未按字面建档；改为人工盘点真实异常（BUG-003 延迟约 50 分钟／BUG-006 恢复／BUG-012 pm 提前触发）。本期实际零失败、零报错、零用户纠正。',
  '【本期最重要的口径修正】昨日（10-19）早报记录的 4170.87 是 09:40 的亚市快照，10-19 真实收盘为 4140.90（亚市低开 4160.59、欧盘高 4190.13、美盘尾低 4136.44，全天 -0.59%）。按 MEMORY 固化的四步修法执行：①基准改用真实收盘 → ②hero note 单列该原因 → ③chart 的 10-19 点回填 4140.9 → ④prices.source 与 chart.source 各写一句修正说明。因此 hero 的 901.2→891.7 中，约 6.5 元属昨日快照虚高、仅约 3.1 元为真实下跌。',
  'hero 三层原因：①昨日基准为亚市快照 4170.87，同一口径下（中间价 6.7208）折算 901.24，而按真实收盘 4140.90 折算仅 894.76 → 快照虚高 6.48 元/克；②真实收盘至今晨：伦敦金 4140.90→4127.04(-13.86 美元) 压约 3.0 元、中间价 6.7208→6.7200（升 8 基点）再压约 0.1 元，合计 -3.10 元；两项相加 9.58 元，与 901.2→891.7 的 -9.5 吻合；③按中间价折算 891.66，按在岸即期 6.6817 折算 886.48，相差 5.17 元/克，属口径差而非算错。',
  'AU9999 今日基准取 10-19 日盘收盘 900.89（非 10-16 的 901.57），因 10-19 为完整交易日、其夜盘按规则归属 10-20；SGE 官方 891.2 与平价锚 891.7 偏离 -0.06%，明显优于金投网的 888.50 与金价查询网的 892.60，故以官方为主口径。',
  '本期叙事主线与昨日反转：昨日「俄油解禁→油价跌→通胀缓→利多黄金」，今日被美国能源部长赖特「俄罗斯柴油尚未投放市场」直接推翻，油价反创一个月新高（WTI 盘中 99.71、布伦特 110.66）；下跌真正推手是「AI 股反弹→避险资金撤出美债→10Y 由 5.081% 修复至 5.141%→持金成本上升」，比地缘新闻更直接。已在 news②与 teach 中把这个传导链讲透。',
  'teach 本期选题「地缘风险传导到金价的三道关（油价→通胀→利率）」，承接 10-19 的「避险资产排队顺序」并避开 10-15 已讲过的「实际利率」；与 knowledge 的「跨市场联动—AI 股→美债→黄金」形成互补而非重复。',
  'NeoData 本期未调用（token 续期流程未触发），三路数据全部由 WebSearch 取到公开权威源；「伦敦金现货取 web」惯例继续有效，AU9999 以 SGE 官方为主口径。',
  'updateTime 固定写 09:00（定时口径），真实触发时间只记入本日志的 timestamp（09:54 CST，为完成时刻；触发约 09:50）。',
 ],
}

lp = os.path.join(BASE, 'logs', '2026-10-20-morning_briefing.json')
with io.open(lp, 'w', encoding='utf-8') as f:
    json.dump(LOG, f, ensure_ascii=False, indent=2)

# 自检：解析后字符串无 ASCII 直引号
def walk(o, path=''):
    bad = []
    if isinstance(o, dict):
        for k, v in o.items():
            bad += walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            bad += walk(v, path + '[%d]' % i)
    elif isinstance(o, str):
        for ch in ('"', "'"):
            if ch in o:
                bad.append((path, ch))
    return bad
print('written:', lp)
print('ASCII quote issues:', walk(LOG) or 'none')
print('advice/MAIL_BODY len:', len(MAIL_BODY))
