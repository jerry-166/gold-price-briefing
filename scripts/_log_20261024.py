import json, io, os

log = {
    "date": "2026-10-24",
    "type": "morning_briefing",
    "status": "partial",
    "summary": "周六休市早报：5 步中 4 步成功，QQ 邮箱工具未注册、agent-mail 未开通导致邮件未发送（email_sent: false），HTML 已落盘待人工补发",
    "timestamp": "09:45 CST",
    "steps": [
        {
            "num": 1, "name": "获取数据", "status": "success", "duration_ms": 248000,
            "result": "伦敦金 10-23 纽约尾盘收 3995.5 美元/盎司（-0.72%，三源聚类 3995.38/3995.54/3995.63，盘中低 3975.698 创三个月新低、7 月 29 日以来首破 4000）；上金所 Au99.99 收 864.00 元/克（-1.85%，昨结 880.30，高 883.98/低 856.01，加权均价 863.44）；中间价 6.7180（-15 基点，周六无新定价，在岸 6.6704）。今日周六休市，价格与涨跌幅全部沿用 10-23 收盘口径。新闻 5 条（FOMC 前瞻/霍尔木兹油轮触雷/PMI 与密歇根信心/机构目标价分歧/人民币中间价），均带原始 url。",
            "source": "neodata-financial-search + WebSearch（金投网、每经、国际金融报、SGE 官方、金融界、中国基金报、汇通网、FX168、上观新闻、21 经济网）+ NeoData AU9999.SHG / USDCNY.FX 交叉校验"
        },
        {
            "num": 2, "name": "生成早报JSON", "status": "success", "duration_ms": 196000,
            "result": "已写入 daily/2026-10-24.json（41934 字节）。自检全部通过：labels/values 各 30、events 30 条且逐条日期与索引对齐、无 index<0 孤儿事件、news 5 条 url 均以 http 开头、解析后字段值无 ASCII 直引号、trend.advice 恰好 200 字（≤200）、hero 积存金 863.0 = 3995.5×6.7180÷31.1035 复算一致、plan 全部 ¥/克 价位用 Python 批量复算。图表滚动：丢 09-24、补 10-24，events 索引整体 -1；10-23 一点由昨日亚市快照 4016.3 回填为真实收盘 3995.5，10-24 休市与周五同值。",
        },
        {
            "num": 3, "name": "更新manifest", "status": "success", "duration_ms": 9000,
            "result": "已在 manifest.json 的 briefings 数组头部插入 2026-10-24 记录（共 64 期）",
        },
        {
            "num": 4, "name": "Git推送", "status": "success", "duration_ms": 46000,
            "result": "已提交并推送：早报 3752b94、元数据修正 eb52f5e（均走 SSH，git rev-parse 与 ls-remote 均为 eb52f5e，一致）",
        },
        {
            "num": 5, "name": "发送邮件", "status": "failed", "duration_ms": 212000,
            "result": "未发送至 2132049351@qq.com（email_sent: false）。QQ 邮箱连接器状态 connected，但本次会话工具索引中不存在任何 mcp__qq-mail__* 工具，多组关键词检索只命中 agent-mail 同名能力；mcp__agent-mail__GetMe 返回 not_bound（『Agent 邮箱尚未开通』）→ 双通道同时失效。HTML 已落盘 .workbuddy/outbox/2026-10-24-morning.html（14445 字节）＋主题文本，待人工补发。",
            "outputs": [{"label": "邮件内容", "body": "🌅 今日金价早报 | 2026年10月24日 周六 ｜ 金价快照：积存金估算 863.0 元/克（-0.72%）、上金所 Au9999 864.0（-1.85%）、伦敦金 3995.5 美元/盎司（-0.72%）、中间价 6.72（-0.02%）；顶部标注今日休市、沿用 10-23 收盘口径。昨夜大事 5 条，全部带原文链接。趋势：短 -1 / 中 -1 / 长 1，action=watch。买卖时机：买 3970-3985（857-861 元/克）/3940-3960（851-855）/3900-3920（843-847）三档；卖 4030-4050（870-875）/4075-4100（880-886）分批减，站回 4120（890）停手；止损 3960（855）/3920（847）。今日学一招：整数关口一破为什么跌得特别快（止损磁吸与流动性踩踏）。底部附站点链接。"}]
        },
    ],
    "summary_stats": {
        "total_steps": 5, "success_steps": 4, "failed_steps": 1,
        "total_duration_ms": 711000, "email_sent": False, "git_pushed": True
    },
    "gap_check": {
        "previous_briefing": "2026-10-23",
        "days_since": 1,
        "missed_trading_days": [],
        "note": "10/19-10/24 连续六个自然日、五个交易日全部产出，无断档。"
    },
    "inspection_check": {
        "inspection_noon_last": "2026-10-23",
        "inspection_pm_last": "2026-10-23",
        "consecutive_zero_output_trading_days": 1,
        "note": "10-22 两线零产出，10-23 两线均恢复正常（noon/pm 各一条 no_action）；连续零产出交易日数回落至 1，未达 BUG-012 复合升级判据（连续 ≥5 日 + 恢复后 2 周内再现连续 ≥3 日）。10-24 为周六，两条巡检未到点。"
    },
}

os.makedirs('logs', exist_ok=True)
p = 'logs/2026-10-24-morning_briefing.json'
io.open(p, 'w', encoding='utf-8').write(json.dumps(log, ensure_ascii=False, indent=2) + '\n')
print('written', p, os.path.getsize(p), 'bytes')

m = json.load(io.open('logs/manifest.json', encoding='utf-8'))
assert m['logs'][0]['date'] == '2026-10-23'
m['logs'].insert(0, {
    "date": "2026-10-24",
    "type": "morning_briefing",
    "status": "partial",
    "summary": "周六休市早报：金价沿用 10-23 收盘（伦敦金 3995.5、AU9999 864.0、中间价 6.7180），JSON/manifest/git 三步成功，邮件因工具未注册+邮箱未开通未发送",
})
io.open('logs/manifest.json', 'w', encoding='utf-8').write(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
print('logs head:', [(x['date'], x['type'], x['status']) for x in m['logs'][:3]])
print("done")
