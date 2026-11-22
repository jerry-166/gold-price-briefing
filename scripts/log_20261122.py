# -*- coding: utf-8 -*-
"""写 2026-11-22 早报运行日志 + 更新 logs/manifest.json。"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = "2026-11-22"

MAIL_BODY = """🌅 今日金价早报 | 2026 年 11 月 22 日 周日（周日休市版）

【金价快照 · 沿用 11-20 纽约收盘】
· 招行积存金买入价（估算）762.9 元/克，-2.49%
· 上海金 AU9999 755.0 元/克，-1.24%（基准 11-20 日盘收 764.50）
· 伦敦金 XAUUSD 3534.6 美元/盎司，-2.49%
· 美元人民币中间价 6.7131，0.00%（周末不更新）

【一句话】周末两天价格不动，现货金停在 3534.6 美元、周跌 8.91%，盘中最低 3502.73，3500 只差一步没破。
今天没有新行情，但信息不少——Kitco 调查 15 位分析师 9 人看跌，周一 06:00 开盘就会给出 3500 这道关的答案。

【昨夜大事与下周看点】
1. 东方金诚瞿瑞：3500 是「减速带」不是「终点站」——止跌不创新低只是第一步，收复 3600-3700 才算减速，收复 3800 且实际利率/美元/持仓不再恶化才算阶段性修复。
2. Kitco 周度调查：15 位分析师 9 人看跌下周、4 人看涨、2 人中性，散户看跌升至 46%。
3. 下周四个开关：11-23 制造业 PMI 初值；11-24 凌晨威廉姆斯讲话＋消费者信心；11-25 核心 PCE＋褐皮书＋Q3 GDP＋耐用品＋初请；11-26 感恩节纽交所全休、贵金属提前收市。
4. 美元指数周五收 103.87、单周 +0.44%、周线四连涨，盘中逼近 104。
5. 卓创资讯：后续核心变量仍是中东局势，最坏情形下黄金或承压至明年中旬。
6. 高盛三个数字别混用：2026 年底 4150、2027 年底 4650、2028 年底前重回 5600。

【趋势判断】短期 偏空｜中期 中性｜长期 偏多　操作基调：watch（观察，不追不抄）

【买卖时机】
买入：周一 06:00 国际盘重开、09:00 后银行才调挂牌价，先别抢开盘那一下。看 3500（约 755 元/克）守不守；守住且 1 小时图不再创新低、站上 3530 再下第一笔，破 3500 就等 3420-3440（约 738-742 元/克）。
　价位：3480-3500（约 751-755 元/克）第一批，3420-3440（约 738-742 元/克）第二批。
卖出：反弹到 3590-3620（约 775-781 元/克）先减一半，跌破 3420（约 738 元/克）止损离场。
一句话建议：加息预期没松、美元四周连涨，周一 3500 就是答案，别追也别急抄；仓位别超三成。
风险提示：以上价位只是参考坐标，不构成投资建议；周末休市，周一开盘可能直接跳空。

【今日学一招】一群分析师都看空的时候，为什么反而要小心？
①Kitco 每周五给分析师发问卷，本周 15 人 9 人看跌、散户看跌 46%，这是一致预期被量化的样子，记录的是情绪不是价格；
②一致预期错在已变成仓位——人人看空时看空的观点多半已卖成现金，继续跌需要「新的卖家」，所以极端一致常对应短线反弹，本质是仓位拥挤度指标；
③但它只对短线有效，中期由实际利率和美元决定，正确用法是「人人看空时不要追空、也别满仓抄底」。

【延伸】高盛三个时间尺度｜下周四个开关｜金饰需求同比 -17% 但央行净购 321 吨｜3500 三重身份

完整图表与历史早报：https://jerry-166.github.io/gold-price-briefing/"""

steps = [
    {
        "num": 1,
        "name": "获取数据",
        "status": "success",
        "duration_ms": 108000,
        "result": (
            "伦敦金 3534.64（-2.49%，昨收 3625.01，高 3636.63/低 3502.73）、AU9999 755.01（-1.24%，基准 764.50）、"
            "T+D 756.00（-1.05%）、沪金主力 756.50、中间价 6.7131（周末不更新）、美元指数 103.87（周涨 0.44%）；"
            "周日国际盘/上金所/外汇交易中心全休，价格沿用 11-20 收盘。另获 6 条新消息：瞿瑞「3500 是减速带」、"
            "Kitco 调查 9/15 看跌、下周四个开关、美元周线四连涨、中东仍是核心变量、高盛三个目标价口径"
        ),
        "source": (
            "新浪实时接口 hf_XAU / gds_AU9999 / gds_AUTD + WebSearch 交叉验证"
            "（neodata-financial-search skill 本地未安装，已如实改走实时接口 + 搜索，未假装调用）"
        ),
    },
    {
        "num": 2,
        "name": "生成早报JSON",
        "status": "success",
        "duration_ms": 20000,
        "result": "已写入 daily/2026-11-22.json（26 868 字节，30 个图表点 + 30 条 events，advice 180 字），check_briefing.py 自检 0 错误",
    },
    {
        "num": 3,
        "name": "更新manifest",
        "status": "success",
        "duration_ms": 6000,
        "result": "已追加记录到 manifest.json（briefings 92 → 93，头部为 2026-11-22 周日）",
    },
    {
        "num": 4,
        "name": "Git推送",
        "status": "success",
        "duration_ms": 12000,
        "result": "已提交并推送，commit 68f66db，git rev-parse HEAD 与 git ls-remote origin master 一致",
    },
    {
        "num": 5,
        "name": "发送邮件",
        "status": "success",
        "duration_ms": 70000,
        "result": "已发送至 2132049351@qq.com（skip_confirmation 直发，一次 queued:true；sent 目录回读 created_at 2026-11-22T01:57:04Z = 09:57:04 CST）",
        "outputs": [{"label": "邮件内容", "body": MAIL_BODY}],
    },
]

log = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "success",
    "summary": "周日休市版：沿用 11-20 收盘（伦敦金 3534.6、-2.49%），重点转向下周 PCE 与 3500 关口，五步全成功、邮件已送达",
    "timestamp": "09:57 CST",
    "steps": steps,
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": 216000,
        "email_sent": True,
        "git_pushed": True,
    },
}

assert sum(s["duration_ms"] for s in steps) == log["summary_stats"]["total_duration_ms"], "耗时合计不符"
path = os.path.join(BASE, "logs", DATE + "-morning_briefing.json")
raw = json.dumps(log, ensure_ascii=False, indent=2)
assert raw.count("%%") == 0
with open(path, "w", encoding="utf-8") as f:
    f.write(raw + "\n")
print("written", path, len(raw), "bytes")

# ---- logs/manifest.json ----
mp = os.path.join(BASE, "logs", "manifest.json")
m = json.load(open(mp, encoding="utf-8"))
assert m["logs"][0]["date"] == "2026-11-21", m["logs"][0]["date"]
assert not any(x["date"] == DATE and x["type"] == "morning_briefing" for x in m["logs"]), "已有今日记录"
m["logs"].insert(0, {
    "date": DATE,
    "type": "morning_briefing",
    "status": "success",
    "summary": "周日休市版：沿用 11-20 收盘（伦敦金 3534.6、-2.49%），下周 PCE 与 3500 关口是焦点，邮件已送达",
})
mraw = json.dumps(m, ensure_ascii=False, indent=2)
assert mraw.count("%%") == 0
with open(mp, "w", encoding="utf-8") as f:
    f.write(mraw + "\n")
print("logs manifest", len(m["logs"]), "head", m["logs"][0])
