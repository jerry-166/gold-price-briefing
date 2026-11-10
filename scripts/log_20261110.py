# -*- coding: utf-8 -*-
"""写入 2026-11-10 早报运行日志。"""
import json, sys, os, hashlib, time
sys.stdout.reconfigure(encoding="utf-8")

DATE = "2026-11-10"
d = json.load(open("daily/" + DATE + ".json", encoding="utf-8"))

B = {}
for p in [
    ".buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md",
    ".buglog/bugs/2026-09-14-inspection-email-connector-down.md",
    ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md",
    ".buglog/bugs/2026-09-26-buglog-hook-misfire.md",
    ".buglog/index.md",
]:
    raw = open(p, "rb").read()
    B[os.path.basename(p)] = {"bytes": len(raw), "sha1": hashlib.sha1(raw).hexdigest()}

durations = [164000, 11800, 14300, 10200, 56000]

mail_body = (
    "【主题】🌅 今日金价早报 | 2026年11月10日 周二\n"
    "【快照】积存金(估算) 887.6 元/克 -0.77%｜上海金 AU9999 882.00 元/克 +0.11%｜"
    "伦敦金 XAUUSD 4110.25 美元/盎司 -0.74%｜中间价 6.72 -0.03%\n"
    "【一句话】隔夜油价崩 6% 把金价推上 4140，今早冲到 4146 又被打回来。4146 是两道顶，4100 是生命线，今晚 21:30 CPI 才是裁判——现在别追高。\n"
    "【昨夜大事】①今晚 21:30 美国 10 月 CPI 只有环比没有同比，预期 0.3%｜"
    "②特朗普称没必要再打伊朗＋美伊核谈重启，油价一夜跌 6% 创三个月新低｜"
    "③12 月加息 25bp 概率 84.2%，巴尔金、古尔斯比连夜放鹰｜"
    "④美元指数跌 0.61% 到 101.66，人民币中间价调升 21 个基点｜"
    "⑤内盘折价消失：即期汇率折算 881.5，上海金 882.0，基本贴平。\n"
    "【趋势】短期震荡 0｜中期偏空 -1｜长期偏多 +1｜操作：先看不动（watch）\n"
    "【买卖时机】买：4100-4084（约 885-882 元/克）买三成，4055-4045（约 876-874 元/克）再加三成；"
    "卖：4146-4160（约 895-898 元/克）减三分之一，4180-4200（约 903-907 元/克）再减三分之一，"
    "破 4010-4000（约 866-864 元/克）认错离场。\n"
    "【今日学一招】今晚的 CPI 为什么没有「同比」——2025 年 10 月政府停摆缺基期，只发环比不发同比。\n"
    "【底部】https://jerry-166.github.io/gold-price-briefing/\n"
    "【HTML】落盘 .workbuddy/outbox/mail_2026-11-10.html（10 264 字符 / 14 276 字节 / 70 行 / 最长行 498 字符）"
)

log = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "success",
    "summary": "延迟 168 分钟触发；三项核心数据与 5 条新闻全部取到，已生成早报 JSON、回填 11-09 真实收盘、更新 manifest 并推送，邮件 11:52:50 确认落地。",
    "timestamp": "11:52 CST",
    "trigger_note": "原定 09:00，实际 11:48:36 触发，延迟约 168 分钟；同日 22:00 晚间巡检于 11:40 提前触发，两条线呈倒序（巡检先、早报后）。",
    "steps": [
        {
            "num": 1,
            "name": "获取数据",
            "status": "success",
            "duration_ms": durations[0],
            "result": "伦敦金 4110.25(-0.74%，昨收 4140.94)、AU9999 882.00(+0.11%，基准 881.00)、中间价 6.7167(调升 21bp)、积存金估算 887.6；旁证 COMEX 主力 4119.03、T+D 881.70、DXY 101.6664、WTI 12 月 85.64、布伦特 1 月 91.45；新闻 5 条含原始 url。",
            "source": "新浪财经 hq.sinajs（hf_XAU/gds_AU9999/gds_AUTD/USDCNY/DINIW）+ WebSearch（中宏网/中国经济网/中新网/汇通财经/金价查询网/FXStreet/汇通网）",
        },
        {
            "num": 2,
            "name": "生成早报JSON",
            "status": "success",
            "duration_ms": durations[1],
            "result": "已写入 daily/2026-11-10.json；check_briefing.py 首轮报 advice 237 字超限，两次收敛至 191 字后 0 error 通过；图表 30 点、events 30 条，11-09 点已由 4120.9 回填为 4140.9。",
        },
        {
            "num": 3,
            "name": "更新manifest",
            "status": "success",
            "duration_ms": durations[2],
            "result": "已追加记录到 manifest.json（briefings 头部，共 81 条）。",
        },
        {
            "num": 4,
            "name": "Git推送",
            "status": "success",
            "duration_ms": durations[3],
            "result": "已提交并推送（80d9ee0，SSH）；git ls-remote 与 git rev-parse 均为 80d9ee0934ed，一致。",
        },
        {
            "num": 5,
            "name": "发送邮件",
            "status": "success",
            "duration_ms": durations[4],
            "result": "已发送至 2132049351@qq.com；GetMe 正常、SendMessage 返回 queued、ListMessages(dir=sent) 于 11:52:50 CST 确认（msg_AEPpZ_1STNcA55caGGYmSZ4356WNnAhc96cXvcIkZmhECQ）。生成脚本三条门禁通过：maxline 498≤1500、字面双百分号计数为 0、width 100 百分比写法合法。",
            "outputs": [{"label": "邮件内容", "body": mail_body}],
        },
    ],
    "data_snapshot": {
        "london_gold": {"value": 4110.25, "prev_close": 4140.94, "open": 4138.05, "high": 4146.43, "low": 4108.51, "change_pct": -0.74},
        "au9999": {"value": 882.00, "base": 881.00, "open": 881.00, "high": 888.50, "low": 880.00, "change_pct": 0.11},
        "usdcny_mid": {"value": 6.7167, "prev": 6.7188, "bps": 21, "change_pct": -0.03},
        "hero_saving_gold": {"value": 887.6, "prev_true_close_equiv": 894.5, "change_pct": -0.77},
        "cross_check": {"comex_main": 4119.035, "au_td": 881.70, "dxy": 101.6664, "wti_dec": 85.637, "brent_jan": 91.450, "spot_fx": 6.6708},
    },
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": sum(durations),
        "email_sent": True,
        "git_pushed": True,
    },
    "buglog_verification": {
        "date_grep_count": {
            "2026-09-08-briefing-scheduler-missed-days.md": 3,
            "2026-09-14-inspection-email-connector-down.md": 1,
            "2026-09-25-inspection-scheduler-silent-miss.md": 2,
            "2026-09-26-buglog-hook-misfire.md": 3,
        },
        "file_bytes_and_sha1": B,
        "index_counts": {"open": 12, "fixed": 12, "total": 24, "note": "本期无新增 bug、无状态变更"},
        "notes": "BUG-003 第 5 次延迟 ≥100 分钟（1 档危害）、BUG-006 连续正常第 2 日、BUG-012 新增「巡检抢占早报时点」倒序形态、BUG-013 第 25 次误判。advice 237→214→191 与 manifest 脚本改 argv 属生成前自纠，按判定不计入 bug 修复。",
    },
    "_meta": {"written_at": time.strftime("%Y-%m-%d %H:%M:%S")},
}

p = "logs/" + DATE + "-morning_briefing.json"
with open(p, "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
print("written", p, "total_duration_ms", sum(durations))
print("sha1 sample", B[".buglog/index.md"])
