import json, io

log = {
  "date": "2026-10-23",
  "type": "morning_briefing",
  "status": "success",
  "summary": "早报全流程成功（触发 09:38:29／延迟约 39 分钟）：金价 4016.3（-0.21%，昨收 4024.56，亚市 4011.83-4032.66 低位磨底）、AU9999 863.6（-1.90%，昨结 880.30）、中间价 6.7180（升 15 基点，在岸 6.6727 创 2022 年 6 月以来新高）、积存金估算 867.5；主线为「黑色星期四破位、4000 保卫战」——10/22 美盘自日内高 4143.89 闪崩至 4020.95、收 4024.6（-2.71%），中东油袭推布伦特上 113 美元→通胀→12 月加息 74.8%-91%，AI 股灾令 10Y 美债收益率单日暴跌 19.3bp 反而分流了避险资金；短 -1/中 -1/长 1、action=watch；10-22 图表点由亚市快照 4111.6 回填真实收盘 4024.6；邮件发送成功（email_sent: true、queued: true），BUG-006 第 9 次观察恢复正常。",
  "timestamp": "09:38 CST（触发）／09:45 CST（完成）",
  "gap_check": {
    "previous_morning_briefing": "2026-10-22",
    "gap_trading_days": 0,
    "missed_trading_days": [],
    "verdict": "10/19-10/23 连续五个交易日全部产出，无缺跑、无提前触发"
  },
  "steps": [
    {"num": 1, "name": "获取数据", "status": "success", "duration_ms": 126000,
     "result": "伦敦金 10/23 亚市 4016.3（金投网 09:33 报 4016.26／-8.30／-0.21%，昨收 4024.56、今开 4023.20、最高 4032.66、最低 4011.83）；10/22 真实收盘 4024.6（同花顺 4024.33／金融界 4024.16／上证报 4025.33／每经 4028.58 四源聚类）；AU9999 863.60（-1.90%，昨结 880.30，09:32:44 金投网 SGE 行情，开 874.50、高 883.98、低 862.01）；中间价 6.7180（升 15 基点，财联社/界面/每经/腾讯四源一致）；新闻 5 条含原始 url；NeoData 首次查询返回 TOKEN_EXPIRED，经 connect_cloud_service 取凭证后 --save-token 续期成功（AUUSDO.LIFFE 4029.40 作 COMEX 期金旁证）",
     "source": "neodata-financial-search + WebSearch（金投网／金价查询网／SGE 官方／中国外汇交易中心／汇通网／上海证券报／每经／同花顺／界面新闻）"},
    {"num": 2, "name": "生成早报JSON", "status": "success", "duration_ms": 110000,
     "result": "已写入 daily/2026-10-23.json：hero 867.5 元/克、AU9999 863.6、汇率 6.7180、伦敦金 4016.3；trend 短-1/中-1/长1、action=watch，advice 198 字；plan 买入三档 4000-4012／3960-3980／3920-3940 美元（864-866／855-860／847-851 元/克），卖出 4050-4058／4080-4100 美元，止损 4000／3960；teach 讲「避险资产的排队顺序」；knowledge 3 条；chart 30 点、丢 09-23 补 10-23、events 索引 -1 并剔除孤儿事件，10-22 点由 4111.6 回填为 4024.6；自检（长度/索引/日期比对/url/ASCII 引号遍历）全部通过",
     "source": "scripts/_build_20261023.py"},
    {"num": 3, "name": "更新manifest", "status": "success", "duration_ms": 2000,
     "result": "已追加记录到 manifest.json，briefings 头部为 2026-10-23 周五，总数 63"},
    {"num": 4, "name": "Git推送", "status": "success", "duration_ms": 4000,
     "result": "早报提交 5924322「每日早报 2026-10-23」已推送；git rev-parse HEAD 与 git ls-remote origin refs/heads/master 均为 59243225faeae73e5137025162153c259c7f8349，比对一致"},
    {"num": 5, "name": "发送邮件", "status": "success", "duration_ms": 55000,
     "result": "已发送至 2132049351@qq.com（mcp__qq-mail__SendMessage 返回 queued: true，body_format HTML，skip_confirmation true，一次成功，无确认拦截）",
     "outputs": [
       {"label": "邮件内容", "body": "主题：今日金价早报 | 2026年10月23日 周五。正文含：①顶部红色警示框「昨夜金价闪崩 116 美元」；②金价快照表（积存金 867.5 元/克 -0.21%／AU9999 863.6 -1.90%／伦敦金 4016.3 -0.21%／中间价 6.7180 -0.02%）＋口径说明（888.3→867.5 的三层拆解：快照落差 18.8 元、续跌 1.8 元、汇率 -0.2 元）；③昨夜大事 5 条（加息 75%-91%／10Y 美债 -19.3bp 钱进债不进金／初请 19.4 万／中间价 6.7180 在岸四年新高／沙特撤侨地缘反成利空）；④趋势三档（短-1/中-1/长1）＋一句话操作；⑤买卖时机（买 4000-4012／3960-3980／3920-3940 美元＝864-866／855-860／847-851 元/克；卖 4050-4058／4080-4100 美元＝875-877／881-886 元/克；止损 4000／3960 美元＝864／855 元/克）；⑥今日学一招「同样是避险，为什么钱涌进美债却把黄金砸了 2.8%」三点；⑦底部网站链接 https://jerry-166.github.io/gold-price-briefing/ 与免责声明。HTML 底稿另存 .workbuddy/outbox/2026-10-23-morning.html（13 765 字节）"}
     ]}
  ],
  "summary_stats": {
    "total_steps": 5, "success_steps": 5, "failed_steps": 0,
    "total_duration_ms": 297000, "email_sent": True, "git_pushed": True
  },
  "health_check": {
    "note": "巡检两条线分开统计，且不以「历史读数相同」充当「持续正常」证据",
    "inspection_noon": {"last_output": "2026-10-21", "actual_time": "21:40（标称 14:00，延迟约 7h40m，属夜间合并触发）", "today": "未到点"},
    "inspection_pm": {"last_output": "2026-10-23", "actual_time": "09:29（标称 22:00，提前 12h31m）", "status": "partial（波动型预警；按「10/22 收 4024.6 → 当前 4015.8」口径振幅仅约 0.2%，其自述 -3.09% 系基准取错，见 BUG-015）"},
    "zero_output_trading_days": 1,
    "zero_output_days": ["2026-10-22"],
    "verdict": "连续零产出 1 个交易日 < 复合判据阈值（连续 >=5 且恢复后 2 周内再现连续 >=3）→ 不升级不降级；本期新增第四种镜像形态「单线提前」"
  },
  "buglog_verification": {
    "method": "逐文件 grep -c '2026-10-23' 计数 + 字节数 + SHA-1，写入本字段作为凭据",
    "bugs/2026-09-05-briefing-scheduler-missed-days.md": {"grep_c": 1, "bytes": 3156, "sha1": "29cfa88ec70567c0a441c1f0bbb25a9cd2623592"},
    "bugs/2026-09-14-inspection-email-connector-down.md": {"grep_c": 1, "bytes": 30310, "sha1": "2499f0056a9cb369ea30737f28f13db2d3e07802"},
    "bugs/2026-09-25-inspection-scheduler-silent-miss.md": {"grep_c": 2, "bytes": 44569, "sha1": "dadefdfa669692571226f4b96bf14806c6fea80c"},
    "bugs/2026-09-26-buglog-hook-misfire.md": {"grep_c": 3, "bytes": 44308, "sha1": "970faebb797736dec5bfeae5e7a0d4877ad4db9c"},
    "bugs/2026-10-23-inspection-close-price-basis-error.md": {"grep_c": 3, "bytes": 2727, "sha1": "17d59be506c0762cd2cb69fa18e7b711d2e4c16b"},
    "index_consistency": "index.md 已追加「2026-10-23（周五）观察更新」小节并新增 BUG-015 行，Open/Fixed/Total 计数同步为 11/4/15"
  }
}

with io.open('logs/2026-10-23-morning_briefing.json', 'w', encoding='utf-8') as f:
    json.dump(log, f, ensure_ascii=False, indent=2)

m = json.load(io.open('logs/manifest.json', encoding='utf-8'))
m['logs'].insert(0, {
    "date": "2026-10-23",
    "type": "morning_briefing",
    "status": "success",
    "summary": "早报（触发 09:38:29／延迟约 39 分钟）五步全部成功、邮件恢复发送（queued:true）：金 4016.3(-0.21%，昨收 4024.56，亚市 4011.83-4032.66 磨底)、AU9999 863.6(-1.90%)、中间价 6.7180(升 15 基点)、积存金估算 867.5；主线「黑色星期四破位、4000 保卫战」——10/22 美盘从 4143.89 闪崩至 4020.95 收 4024.6(-2.71%)，中东油袭推布伦特上 113 美元→通胀→12 月加息 74.8%-91%，AI 股灾令 10Y 美债收益率单日跌 19.3bp 反成分流；短 -1/中 -1/长 1、action=watch；10-22 图表点回填真实收盘 4024.6；新增 BUG-015（巡检误用日内高点作昨收）。"
})
with io.open('logs/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(m, f, ensure_ascii=False, indent=2)

print('logs written; total', len(m['logs']))
print(json.dumps(m['logs'][0], ensure_ascii=False)[:100])
