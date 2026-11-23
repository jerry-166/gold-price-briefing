# -*- coding: utf-8 -*-
"""写 2026-11-23 早报运行日志 + 更新 logs/manifest.json。"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = "2026-11-23"

MAIL_BODY = """🌅 今日金价早报 | 2026 年 11 月 23 日 周一（交易日 · 数据口径 11:33 亚市实时价）

【金价快照】
· 招行积存金买入价（估算）778.0 元/克，+1.98%
· 上海金 AU9999 775.5 元/克，+1.44%（基准 11-20 日盘收 764.50，含归属今日的周五夜盘）
· 伦敦金 XAUUSD 3605.0 美元/盎司，+1.99%（昨收 3534.64，今开 3559.83、高 3630.32、低 3554.42）
· 美元人民币中间价 6.7120，-0.02%（调升 11 个基点）

【一句话】国际盘一开就跳空：现货金从上周五 3534.6 直接跳到 3605（+1.99%），09:20 一度冲到 3630，
把上周跌掉的 9% 抢回来一截。国内跟涨慢一些：上海金 775.5 元/克（+1.44%）、积存金估算 778 元/克。
但这是超卖修复、不是反转——3600-3630 是上周套牢盘最密集的地方，今天就是在这里被顶回来的。

【昨夜大事与今天为什么涨】
1. 跳空反弹：06:00 重开即 3559.83，09:20 冲 3630.32（+2.7%），11:33 回落报 3605.04（+1.99%）。
2. 美财长贝森特警告美联储「别过度收紧」，交易员不再百分之百押 12 月加息；CME 显示按兵不动概率从 0 回升到 8.6%-11.4%，50bp 尾部预期从 15% 挤到 0。
3. 隔夜美股崩盘（道指 -1.93%、标普 -3.69%、纳指 -5.28%、费半 -10.73%、英伟达 -14.01%）→ 2 年期美债 -11.9bp 至 4.647%、10 年期 4.944%、美元指数退回 103.76。
4. 特朗普改口「重启对伊打击可能性相当小」、伊朗重申外交优先，中东溢价回摆。
5. 本周日程：今夜 22:45 美国 11 月 PMI 初值、明晨 05:00 威廉姆斯讲话、11-25 核心 PCE（预期 3.2%-3.3%）、11-26 感恩节休市。
6. 中金：2027 年 COMEX 中枢约 4300 美元；工建招等多家银行同步发布贵金属风险提示。

【趋势判断】短期 中性｜中期 中性｜长期 偏多　操作基调：watch（观察，不追高）

【买卖时机】
买入：别在 3600 上方追。回踩 3550-3570（约 766-770 元/克）不破 3535 分批进，缺口被吃掉就等 3480-3500（约 751-755 元/克）。
　价位：3550-3570（约 766-770 元/克）第一批，3480-3500（约 751-755 元/克）第二批。
卖出：冲 3660-3680（约 790-794 元/克）先减一半，跌破 3480（约 751 元/克）止损。
一句话建议：跌 9% 后的这波是超卖修复、不是反转，追高容易被套；仓位别超三成。
风险提示：价位按 11-23 中间价 6.7120 折算，仅供参考；今夜 PMI 与明晨威廉姆斯讲话，波动可能很大。

【今日学一招】今天图上那道 25 美元的「缺口」
①周五收 3534.64、周一开 3559.83，中间 3535-3559 一笔成交都没有，这就是跳空缺口——它是周末消息被一次性定价，不是价格上涨；
②缺口常被回补，因为那个区间没有换手成本、没人死守，但趋势行情里的突破缺口可以一年不补；
③看缺口不是「一定会补」，而是「补与不补代表强弱」：只补一半就拉起＝买方还强；整个缺口被吃掉并跌破 3535＝今天只是空头回补。

【延伸】中金 2027 中枢 4300｜摩根大通凯利「加一次就暂停」vs 沃勒 50bp｜今天的三道技术边界｜本周日程

完整图表与历史早报：https://jerry-166.github.io/gold-price-briefing/"""

steps = [
    {
        "num": 1,
        "name": "获取数据",
        "status": "success",
        "duration_ms": 420000,
        "result": (
            "伦敦金 3605.04（+1.99%，昨收 3534.64，今开 3559.83、高 3630.32、低 3554.42）、AU9999 775.50（+1.44%，基准 764.50）、"
            "T+D 774.97（+1.44%）、中间价 6.7120（调升 11 个基点）、美元指数 103.76（-0.10%）、COMEX 12 月期金 3604.7（+2.54%）、"
            "现货白银 42.58（+2.46%）；另获 6 条新消息：金价跳空高开冲 3630、贝森特警告美联储别过度收紧、2 年期美债 -11.9bp 与美元退回 103.76、"
            "特朗普改口与伊朗外交优先、本周 PCE/PMI/威廉姆斯日程、中金 2027 中枢 4300 与银行风险提示"
        ),
        "source": (
            "新浪实时接口 hf_XAU / gds_AU9999 / gds_AUTD + 东财 COMEX 旁证 + WebSearch 交叉验证"
            "（neodata-financial-search 脚本已在 skills-marketplace 就位且 token 存在，但运行缺 requests 依赖、"
            "本地 pip 源不可用，install 失败 → 如实改走实时接口 + 搜索，未假装调用）"
        ),
    },
    {
        "num": 2,
        "name": "生成早报JSON",
        "status": "success",
        "duration_ms": 130000,
        "result": "已写入 daily/2026-11-23.json（28 385 字节，30 个图表点 + events 索引整体 -1，advice 198 字），check_briefing.py 自检 0 错误（首轮 1 错：tagType 误用 fund，改 data 后通过）",
    },
    {
        "num": 3,
        "name": "更新manifest",
        "status": "success",
        "duration_ms": 5000,
        "result": "已追加记录到 manifest.json（briefings 93 → 94，头部为 2026-11-23 周一）",
    },
    {
        "num": 4,
        "name": "Git推送",
        "status": "success",
        "duration_ms": 18000,
        "result": "已提交并推送，commit 2d2108d（父 744fb75），远端 refs/heads/master 已更新",
    },
    {
        "num": 5,
        "name": "发送邮件",
        "status": "failed",
        "duration_ms": 150000,
        "result": (
            "未发送。qq-mail 连接器状态为 connected，但 tools 精确名检索（SendMessage/ListMessages/send_mail/send_email）"
            "全部回落到 agent-mail 命名空间，DeferExecuteTool 直接调用 mcp__qq-mail__SendMessage 返回 not found in the deferred tools index；"
            "agent-mail 兜底亦失败（GetMe 返回 not_bound，提示需人工开通）。HTML 底稿已落 .workbuddy/outbox/mail-2026-11-23-morning_briefing.html 待人工补发。"
            "属 BUG-006 复发（第 3 种证据组合：connected+bound+enabled 三真 + 精确名检索回落）。"
        ),
        "outputs": [{"label": "邮件内容（未投递，底稿见 outbox）", "body": MAIL_BODY}],
    },
]

log = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "partial",
    "summary": (
        "交易日版：伦敦金跳空高开报 3605.0（+1.99%），AU9999 775.5（+1.44%）、中间价 6.7120，主体四步全部成功；"
        "邮件通道故障未发送（qq-mail 工具未进索引、agent-mail 未开通），HTML 底稿已落 outbox 待人工补发。"
        "另：本次触发延迟 153 分钟（11:33 vs 标称 09:00），当日有行情（亚市 09:20 高点 3630.32），快照时点已错过开盘与冲高段，属有危害的延迟但未达 360 分钟标注门槛。"
    ),
    "timestamp": "11:57 CST",
    "steps": steps,
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 4,
        "failed_steps": 1,
        "total_duration_ms": sum(s["duration_ms"] for s in steps),
        "email_sent": False,
        "git_pushed": True,
    },
}

assert sum(s["duration_ms"] for s in steps) == log["summary_stats"]["total_duration_ms"], "耗时合计不符"
assert log["summary_stats"]["success_steps"] + log["summary_stats"]["failed_steps"] == 5
path = os.path.join(BASE, "logs", DATE + "-morning_briefing.json")
raw = json.dumps(log, ensure_ascii=False, indent=2)
assert raw.count("%%") == 0, "日志残留 %%"
with open(path, "w", encoding="utf-8") as f:
    f.write(raw + "\n")
print("written", path, len(raw), "bytes")

# ---- logs/manifest.json ----
mp = os.path.join(BASE, "logs", "manifest.json")
m = json.load(open(mp, encoding="utf-8"))
assert m["logs"][0]["date"] == "2026-11-22", m["logs"][0]["date"]
assert not any(x["date"] == DATE and x["type"] == "morning_briefing" for x in m["logs"]), "已有今日记录"
m["logs"].insert(0, {
    "date": DATE,
    "type": "morning_briefing",
    "status": "partial",
    "summary": "交易日版：伦敦金跳空高开 3605.0（+1.99%）、AU9999 775.5（+1.44%）；四步成功，邮件通道故障未发、底稿落 outbox 待补发",
})
mraw = json.dumps(m, ensure_ascii=False, indent=2)
assert mraw.count("%%") == 0, "清单残留 %%"
with open(mp, "w", encoding="utf-8") as f:
    f.write(mraw + "\n")
print("logs manifest", len(m["logs"]), "head", m["logs"][0])
