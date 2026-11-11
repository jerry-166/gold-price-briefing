# -*- coding: utf-8 -*-
"""写 2026-11-11 早报运行日志 + 更新 logs/manifest.json。全部 f-string，禁用 % 格式化。"""
import json, datetime, os

DATE = "2026-11-11"
OUT = f"logs/{DATE}-morning_briefing.json"
MAIL_HTML = f".workbuddy/outbox/mail-{DATE}.html"

mail_sent = False
mail_note = (
    "失败：QQ Mail 连接器工具未进入 deferred tools 索引。三次精确名检索（mcp__qq-mail__SendMessage / GetMe）均回落 agent-mail 命名空间，"
    "直接调用返回 Tool not found；list_installed_plugins 同时显示 qq-mail status=connected、bound=true、enabled=true，"
    "即连接器自报已连接但 MCP 工具链未注册，属 BUG-006 形态。邮件 HTML 已落盘待人工补发。"
)

email_body = (
    f"主题：🌅 今日金价早报 | 2026年11月11日 周三（HTML 版已落盘 {MAIL_HTML}）\n\n"
    "【金价快照 11-11 11:50 亚市】\n"
    "招行积存金（估算）874.2 元/克 +0.38%\n"
    "上海金 AU9999 869.0 元/克 -1.63%\n"
    "伦敦金 XAUUSD 4046.85 美元/盎司 +0.35%\n"
    "美元中间价 6.7191 +0.04%（调贬 24 个基点）\n\n"
    "【昨夜大事】\n"
    "1. 美国 10 月 CPI 全面超预期：环比 +0.4%（预期 0.3%）、核心 +0.3%（预期 0.2%），连续第三个月 ≥0.4%；"
    "美元 102.25（+0.59%）、10 年期美债 4.994%（+13.1bp）、2 年期 4.748%（+19.5bp）；金价失守 4100，最低 4013.53，收 4032.73（-2.61%）。\n"
    "2. 12 月加息 25 个基点已被完全定价，加息 50 个基点的概率从零升到 10%-11.8%，明年 1 月再加息概率约 60%。\n"
    "3. 机构分歧：高盛下调 2026 年底目标 4650→4150；瑞银维持 4600/5000/5400；渣打维持超配、3 个月 4350、12 个月 4700。中国金币集团发风险提示。\n"
    "4. 霍尔木兹三艘油轮爆炸，但美方淡化动武、卡塔尔争取两周谈判时间 → 布伦特盘中破 90（8 月来首次）、WTI 85.49，地缘溢价退潮。\n"
    "5. 国内集中补跌：Au99.99 跌 1.63%、T+D 跌 1.54%，按即期 6.6805 折算国际金 869.2 与上海金 869.0 贴平，价差收敛到 3 元内。\n\n"
    "【趋势】短线 0 震荡 / 中期 -1 偏空 / 长期 +1 偏多，动作：观望。\n"
    "【买卖】买：4013-4000（约 867-864 元/克）三成，3950-3930（约 853-849 元/克）再加三成；"
    "卖：4100-4120（约 886-890 元/克）减三成，4146-4160（约 896-899 元/克）再减三成；破 3910-3900（约 845-842 元/克）离场。\n"
    "【今日学一招】CPI 只差 0.1 个百分点，金价为什么能跌掉 3%——机会成本与「完全定价」的重新定价。\n\n"
    "网站：https://jerry-166.github.io/gold-price-briefing/"
)

log = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "partial",
    "summary": (
        "延迟约 50 分钟触发；三项核心数据与 5 条新闻全部取到，已生成早报 JSON、回填 11-10 真实收盘（差 77.6 美元）、"
        "更新 manifest 并推送（084b98d）；邮件失败——QQ Mail 工具未注册，HTML 已落盘待人工补发。"
    ),
    "timestamp": "11:49 CST",
    "trigger_note": "原定 09:00，实际 11:49:59 触发（会话 current_time 实测），延迟约 50 分钟，落在 4-170 分钟区间的中低位；未刷新 11/08 的 170 分钟上界。",
    "data_snapshot": {
        "london_gold": {
            "value": 4046.85,
            "prev_close": 4032.73,
            "open": 4035.41,
            "high": 4052.49,
            "low": 4026.55,
            "overnight_low": 4013.53,
            "change_pct": 0.35,
        },
        "au9999": {
            "value": 869.0,
            "base": 883.42,
            "open": 876.0,
            "high": 878.6,
            "low": 862.05,
            "change_pct": -1.63,
        },
        "usdcny_mid": {
            "value": 6.7191,
            "prev": 6.7167,
            "bps": -24,
            "change_pct": 0.04,
        },
        "hero_saving_gold": {
            "value": 874.2,
            "prev_true_close_equiv": 870.9,
            "change_pct": 0.38,
        },
        "cross_check": {
            "comex_main": 4055.78,
            "au_td": 869.2,
            "shfe_main": 866.0,
            "silver_spot": 51.54,
            "dxy": 102.25,
            "us10y": 4.994,
            "wti_dec": 85.49,
            "brent_jan": 91.07,
            "spot_fx": 6.6805,
        },
    },
    "steps": [
        {
            "num": 1,
            "name": "获取数据",
            "status": "success",
            "duration_ms": 95000,
            "result": (
                "新浪 hf_XAU/gds_AU9999/gds_AUTD 一条 curl 取到三项核心行情；中间价 6.7191（调贬 24 基点，中宏网/新华网/中国经济网/中国青年网四源同值）；"
                "WebSearch 四轮取到 CPI 数据、加息定价、机构目标价与地缘/油价；补充 SGE 延时行情与金价查询网交叉校验。"
            ),
            "source": "neodata 通道本期未调用（缺 requests/token，连续第六期）＋ 新浪财经接口 ＋ WebSearch",
        },
        {
            "num": 2,
            "name": "生成早报JSON",
            "status": "success",
            "duration_ms": 80000,
            "result": (
                f"已写入 daily/{DATE}.json（44 466 字节）；图表丢 1 补 1、11-10 点回填 4110.3→4032.7、events 整体 -1 并新增 11-11；"
                "check_briefing.py 终轮 0 error（advice 196 字、10 组价位全中）。"
            ),
        },
        {
            "num": 3,
            "name": "更新manifest",
            "status": "success",
            "duration_ms": 7000,
            "result": "已追加记录到 manifest.json（briefings 头部，共 82 条）。",
        },
        {
            "num": 4,
            "name": "Git推送",
            "status": "success",
            "duration_ms": 6000,
            "result": "已提交 084b98d 并推送（SSH），git rev-parse 与 git ls-remote 两点一致。",
        },
        {
            "num": 5,
            "name": "发送邮件",
            "status": "failed",
            "duration_ms": 35000,
            "result": mail_note,
            "error": "qq-mail MCP tool not registered in deferred tools index (BUG-006)",
            "outputs": [{"label": "邮件内容", "body": email_body}],
        },
    ],
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 4,
        "failed_steps": 1,
        "total_duration_ms": 223000,
        "email_sent": mail_sent,
        "git_pushed": True,
    },
    "_meta": {
        "written_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "outbox": MAIL_HTML if os.path.exists(MAIL_HTML) else None,
        "outbox_bytes": os.path.getsize(MAIL_HTML) if os.path.exists(MAIL_HTML) else 0,
    },
}

json.dump(log, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("written", OUT, os.path.getsize(OUT), "bytes")

# logs/manifest.json
mp = "logs/manifest.json"
m = json.load(open(mp, encoding="utf-8"))
m["logs"] = [x for x in m["logs"] if not (x["date"] == DATE and x["type"] == "morning_briefing")]
m["logs"].insert(0, {
    "date": DATE,
    "type": "morning_briefing",
    "status": "partial",
    "summary": (
        "延迟 50 分钟；伦敦金 4046.85(+0.35%) 自隔夜低 4013.53 反抽，AU9999 869.0(-1.63%) 补跌，中间价 6.7191 调贬 24bp，积存金 874.2；"
        "已回填 11-10 真实收盘 4032.7；JSON＋manifest 已推送 084b98d；邮件失败（BUG-006），HTML 落盘待补发。"
    ),
})
json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("logs/manifest.json updated, len", len(m["logs"]), "head", m["logs"][0]["date"], m["logs"][0]["type"])
