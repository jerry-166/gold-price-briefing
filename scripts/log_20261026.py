# -*- coding: utf-8 -*-
"""写入 2026-10-26 早报运行日志并更新 logs/manifest.json。"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAIL_TEXT = """🌅 今日金价早报 | 2026年10月26日 周一

【金价快照】
· 招行积存金（估算）862.5 元/克  ▼0.03%
· 上海金 AU9999      858.4 元/克  ▼0.65%
· 美元汇率（中间价）  6.7162      调升 18 个基点
· 伦敦金 XAUUSD     3994.5 美元/盎司  ▼0.03%

【一句话】4000 得而复失，盘初冲高 4003.99 被打回、最低 3978.01，随后回到 3994 一线，全天振幅只有 0.65%。

【昨夜与今晨】
1. 加息：本周 10/27-28 美联储开会，北京时间 29 日凌晨出结果。CME 最新定价：这次不动 90%、加息 10%；但 12 月至少加一次仍有 76.2%。刀没撤，所以每次反弹都被摁回。
2. 地缘：以军 25 日空袭加沙、特朗普再提「小规模史诗怒火行动」、伊朗称备好打波斯湾海底光缆。但这次避险没救金价——冲突推高油价、油价推高通胀、通胀逼加息，反而是压制。
3. 油价：亚市早盘 WTI 跌 1.58% 至 101.81、布伦特跌 1.20% 至 110.36，通胀担忧稍缓，金价才从 3978 捞回 4000 上方。现在金价的「方向盘」握在油价手里。
4. 汇率：中间价升 18 个基点报 6.7162，叠加国内多头砍仓（沪金主力 -1.04%），上海金跌 0.65%，比国际盘跌得多。
5. 数据：周四（10/29）不止美联储——美国三季度 GDP 初值与 9 月 PCE 同日落地，是 12 月加息的最后一块拼图。

【趋势判断】短期 ↓ / 中期 ↓ / 长期 ↑，操作建议：观望
4000 得而复失，日线均线全空、RSI 37 还没到极端，本周四美联储与 PCE 落地前不宜押方向。

【什么时候买】
分三档：① 回踩 3975-3985 美元（约 858-861 元/克）先上 3 成，这是上周五低点与今日低点叠在一起的位置；② 跌到 3940-3950 美元（约 851-853 元/克）再加 3 成，3943 是近一年低点；③ 真到 3900 美元（约 842 元/克）才动剩下的钱，整数关口破位只适合小仓试。

【什么时候卖】
① 反弹 4018-4025 美元（约 868-869 元/克）先减一半，MA10 与 MA20 共振压力；② 4060-4087 美元（约 877-882 元/克）全部止盈；止损：收盘破 3975（约 858 元/克）减半、破 3943（约 851）清仓；站回 4120（约 890）上方说明空头结构破了，别再空。

【今日学一招】同一天国际金价只跌 0.03%、国内却跌 0.65%：这 4 块钱差价是谁拿走的？
上海金 ≈ 伦敦金 × 汇率 ÷ 31.1035 + 溢价。按中间价算今天应是 862.5 元/克，上金所实报 858.40，少掉的 4 块就是「内盘溢价」被抹掉了。溢价由国内实物买盘、人民币升贬预期、国内投机盘仓位决定——今天沪金主力跌 1.04%，是国内多头在砍仓，溢价自然收缩。所以看到「国际跌一点、国内跌很多」别急着怀疑数据错，先看溢价。

【风险提示】以上价位按中间价 6.7162 折算，实际以银行/交易所挂牌为准；仅供参考，不构成投资建议。周四美联储与 PCE 前后波动会明显放大，务必轻仓。

完整早报与 30 日走势图：https://jerry-166.github.io/gold-price-briefing/"""

steps = [
    {
        "num": 1,
        "name": "获取数据",
        "status": "success",
        "duration_ms": 168000,
        "result": "NeoData 首次返回 TOKEN_EXPIRED → connect_cloud_service 取凭证 → --save-token 后续查成功：AU9999 858.40（-0.65%，昨结 864.00、今开 865.00，行情时间 10:07）、中间价 6.7162（NeoData 2 位记 6.72／-18 基点）。WebSearch 补齐并交叉：伦敦金 3994.46 美元/盎司（10:05:35 读写，-1.08／-0.03%，开 3995.14、高 4003.99、低 3978.01、昨收 3995.54，另上证报亚市早盘 3988.72、金融界 08:30 报 4003.4、金投黄金网 09:30 报 3987.60，四源同段聚类）；中间价四源同值（中国新闻网／中国经济网／上证报／证券时报）；行情侧：美元指数 101.65(-0.16%)、10Y 美债 4.995%(金十 5.007%)、WTI 101.81(-1.58%)、布伦特 110.36(-1.20%)、CME 10 月不动 90%／12 月至少加一次 76.2%、SPDR 持仓 1041.65 吨(10/24)；新闻 6 条均带原始 url。NeoData AUUSDO.LIFFE 为 COMEX 期金口径，未采信、仅作旁证。",
        "source": "neodata-financial-search + WebSearch",
    },
    {
        "num": 2,
        "name": "生成早报JSON",
        "status": "success",
        "duration_ms": 90000,
        "result": "已写入 daily/2026-10-26.json。hero 862.5（3994.46×6.7162÷31.1035）、AU9999 858.4、中间价 6.72、伦敦金 3994.5；chart 30 点丢 09-26 补 10-26、events 整体 -1 并剔除孤儿（09-26 滚出窗口）；自检 scripts/check_briefing.py 报 0 error（结构／图表长度／events 日期逐条比对／url／dataSources 域名／解析后字符串反引号与 ASCII 引号／advice 175 字／hero 复算／11 个价位逐一复算／plan 与 advice token 一致性）。",
    },
    {
        "num": 3,
        "name": "更新manifest",
        "status": "success",
        "duration_ms": 12000,
        "result": "已追加 {date: 2026-10-26, title: 今日金价早报, weekday: 周一} 至 briefings 数组头部，共 66 条。",
    },
    {
        "num": 4,
        "name": "Git推送",
        "status": "success",
        "duration_ms": 25000,
        "result": "已提交并推送：早报提交 0859aba（git rev-parse HEAD 与 git ls-remote refs/heads/master 均为 0859aba47c38dd8711fb3f25e1056a806a30a0ea，比对一致，走 SSH 显式 URL）。",
    },
    {
        "num": 5,
        "name": "发送邮件",
        "status": "success",
        "duration_ms": 80000,
        "result": "已发送至 2132049351@qq.com（queued: true）。ToolSearch 精确名一次命中，GetMe 返回 scopes 含 mail:send、日配额 2000，SendMessage 标准写法（to 传对象数组）＋body_format HTML＋skip_confirmation true 一次成功、无确认拦截。正文含金价快照 4 项、今晨大事 5 条、趋势三档与建议、买入三档／卖出两档＋止损、今日学一招、底部站点链接；HTML 底稿 11 447 字节（8 329 字符）落 .workbuddy/outbox/2026-10-26-morning.html。",
        "outputs": [{"label": "邮件内容", "body": MAIL_TEXT}],
    },
]

total = sum(s["duration_ms"] for s in steps)

log = {
    "date": "2026-10-26",
    "type": "morning_briefing",
    "status": "success",
    "summary": "周一早报（触发 10:07:17／延迟约 67 分钟）五步全部成功、邮件正常发送（queued:true）：金 3994.5(-0.03%)、AU9999 858.4(-0.65%)、中间价 6.7162(升 18 基点)、积存金估算 862.5；主线「4000 得而复失、30 美元窄缝拉锯」——亚市盘初冲高 4003.99 被打回、最低 3978.01，早盘油价回落 1.2-1.6% 才把金价捞回 4000 上方；12 月加息定价仍 76.2%（10 月不动 90%），周四（10/29）美联储＋PCE＋三季度 GDP 同日落地；国内补跌更明显（沪金主力 -1.04%、内盘溢价收缩约 4 元/克）；短 -1/中 -1/长 1、action=watch；teach 讲「内盘溢价为何让国内跌得比国际多」。",
    "timestamp": "10:07 CST",
    "gap_check": {
        "last_briefing_date": "2026-10-25",
        "missed_trading_days": [],
        "consecutive_missed_days": 0,
        "note": "上一期早报 10-25（周日）正常产出，本期为其后第一个自然日；10-25 为周日非交易日，无缺失交易日，无断档。幂等检查前置：daily/2026-10-26.json 不存在、logs/manifest.json 头部无当日 morning_briefing 记录、git log 无当日早报提交 → 无中断残留（BUG-014 未复现）。",
    },
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": total,
        "email_sent": True,
        "git_pushed": True,
    },
    "steps": steps,
    "buglog_verification": {
        "hook_misfire": "hook 再次把自动化任务提示词判为「用户报告的 bug」（BUG-013 第 28 次连续命中），已判别跳过、未按字面建档；另对 build／mail／check 三个新脚本的正常创建做弱提示，不计入",
        "entries_written": [
            "BUG-003：延迟约 67 分钟，序列 44 个日历日 …/约 39/约 46/约 100/约 67",
            "BUG-006：恢复正常（第 12 次观察），queued:true，形态序列 正常(10/25)→正常(10/26)，不构成修复证据；另固化「入参 ≤12 KB」经验",
            "BUG-012：双线最近产出 10/23，10/24-10/25 为非交易日不计阈值，连续零产出交易日数 0",
            "BUG-013：第 28 次连续命中，附带误报为三个新脚本的正常创建",
        ],
        "grep_counts": {
            ".buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md": 2,
            ".buglog/bugs/2026-09-14-inspection-email-connector-down.md": 1,
            ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md": 1,
            ".buglog/bugs/2026-09-26-buglog-hook-misfire.md": 3,
            ".buglog/index.md": 1,
        },
        "file_hashes": {
            ".buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md": "bytes=56315 sha1=52767e0c31697c261c42d9aa13095828eedff130",
            ".buglog/bugs/2026-09-14-inspection-email-connector-down.md": "bytes=33701 sha1=d82dec842be08c5c1ce6de16ff8af5f2171f8a45",
            ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md": "bytes=47069 sha1=19b573e93e47c83de287426ac52a1cea28ccde98",
            ".buglog/bugs/2026-09-26-buglog-hook-misfire.md": "bytes=46994 sha1=4bf6133ecf34cd1da303bd9f8c5d4fa509ea4bbf",
            ".buglog/index.md": "bytes=24111 sha1=a1f40b5edd1f83bc6fc6d4e1614ded079a40a3d8",
        },
        "file_location_check": "写前按 grep -l \"^id: BUG-00X\" 逐个定位，四个目标文件与预期一一对应，未出现 10/25 发现的归档漂移（BUG-003 未再误入 frontmatter 为 BUG-002 的 2026-09-05 文件）",
    },
    "health_check": {
        "inspection_noon_last_output": "2026-10-23",
        "inspection_pm_last_output": "2026-10-23",
        "today_has_any_inspection_output": "not_applicable（今日 14:00／22:00 两条线尚未到点）",
        "consecutive_zero_output_trading_days": 0,
        "note": "ls logs/ | grep inspection 最近两条为 2026-10-23-inspection_noon / _pm（双线同日 no_action）；10/24 周六、10/25 周日均非交易日，按既有口径不计入连续零产出交易日数 → 计数 0，未达 BUG-012 复合升级判据，不升级不降级。观察期自 10/15 起第 11 日。",
    },
}

lp = os.path.join(ROOT, "logs", "2026-10-26-morning_briefing.json")
with io.open(lp, "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
print("written", lp, "total_ms", total)

mp = os.path.join(ROOT, "logs", "manifest.json")
m = json.load(io.open(mp, encoding="utf-8"))
if m["logs"][0]["date"] == "2026-10-26" and m["logs"][0]["type"] == "morning_briefing":
    print("manifest already has today")
else:
    m["logs"].insert(0, {
        "date": "2026-10-26",
        "type": "morning_briefing",
        "status": "success",
        "summary": "周一早报（触发 10:07／延迟约 67 分钟）五步全成功、邮件正常发送：金 3994.5(-0.03%)、AU9999 858.4(-0.65%)、中间价 6.7162(升 18 基点)、积存金 862.5；主线「4000 得而复失、30 美元窄缝拉锯」，盘初冲高 4003.99 被打回、最低 3978.01，早盘油价回落才捞回 4000；12 月加息仍 76.2%，周四 FOMC＋PCE＋Q3 GDP；国内补跌更狠（沪金主力 -1.04%）；短 -1/中 -1/长 1、watch。",
    })
    json.dump(m, io.open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("manifest updated, count", len(m["logs"]))
