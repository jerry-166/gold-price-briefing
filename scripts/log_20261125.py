# -*- coding: utf-8 -*-
"""写入 2026-11-25 早报运行日志 + 更新 logs/manifest.json（幂等）。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGDIR = ROOT / "logs"
DATE = "2026-11-25"

mail_body = (
    "【主题】🌅 今日金价早报 | 2026年11月25日 周三\n\n"
    "金价快照：积存金估算 766.0 元/克（-0.12%）、上海金 AU9999 763.3 元/克（-1.85%）、"
    "中间价 6.71（-0.03%，调升 23 个基点）、伦敦金 3551.4 美元/盎司（-0.12%）。\n"
    "昨夜大事：12 月加息 25bp 已完全定价（95%-97%）、1 月再加息 66%；美国 11 月消费者信心 103.3 远超预期 92.5；"
    "美股 AI 链二次跳水（英伟达 -5.9%、费半近 -8%、Anthropic 破发）触发保证金平仓；"
    "美元跌 0.48% 到 103.82、10 年期美债 4.928%，金价仍跌 2.15%；地缘升级但油价仍是三个月最低；"
    "国内金饰再破 1100（周大福 1068、周生生 1062）。\n"
    "趋势：短偏空／中中性／长偏多，建议观望。\n"
    "买卖：买 3500-3520（约 755-759 元/克）第一批、3450-3470（约 744-748 元/克）第二批；"
    "卖 3680-3700（约 794-798 元/克）分批止盈，跌破 3480（约 751 元/克）减一半。\n"
    "今日学一招：PCE 和 CPI 到底差在哪、为什么美联储只认 PCE。\n"
    "网站：https://jerry-166.github.io/gold-price-briefing/"
)

steps = [
    {
        "num": 1,
        "name": "获取数据",
        "status": "success",
        "duration_ms": 118000,
        "result": (
            "伦敦金 3551.40（-0.12%，昨收 3555.83、今开 3558.41、高 3574.84、低 3533.67）；"
            "AU9999 763.30（-1.85%，基准 11-24 日盘收 777.72、开 780.00、高 784.00、低 758.01）；"
            "T+D 762.86（-1.85%，昨结 777.21）；中间价 6.7088（调升 23 个基点，前值 6.7111）；"
            "11-24 纽约收盘 3555.83（-2.15%）；DXY 收 103.82（-0.48%）、2 年期美债 4.685%、10 年期 4.928%；"
            "现货白银 40.79（-5.12%）；WTI 1 月 82.05（+2.35%）、布伦特 1 月 91.40（+2.27%）；新闻七条均已取到原始 url"
        ),
        "source": (
            "新浪财经 hq.sinajs.cn（hf_XAU / gds_AU9999 / gds_AUTD 实时接口）+ 中国外汇交易中心/中宏网（中间价）"
            " + WebSearch（金投网、中金在线、新华财经、汇通网、中国经济网、每经、同花顺、SKN）；"
            "neodata-financial-search 仍未调用（BUG-033：query.py 依赖 requests 缺失、pip 索引不可用）"
        ),
    },
    {
        "num": 2,
        "name": "生成早报JSON",
        "status": "success",
        "duration_ms": 53000,
        "result": (
            "已写入 daily/2026-11-25.json（约 3.0 万字节）；check_briefing.py 首轮报 advice 219 字超限，"
            "压缩到 193 字后 errors: 0 / OK；图表 labels 10-27…11-25 共 30 点，11-24 由早报快照 3661.7 回填为"
            "真实收盘 3555.8（差 105.9 美元≈22.7 元/克），events 整体 -1 后补 index 29；"
            "hero 766.0（11-24 真实收盘折算 767.2，差 -1.2 元/克）"
        ),
    },
    {
        "num": 3,
        "name": "更新manifest",
        "status": "success",
        "duration_ms": 9000,
        "result": "已追加记录到 manifest.json（briefings 头部 2026-11-25 / 周三，共 96 条）",
    },
    {
        "num": 4,
        "name": "Git推送",
        "status": "success",
        "duration_ms": 8000,
        "result": "已提交并推送：d2d1409（早报+manifest）；git rev-parse 与 ls-remote refs/heads/master 均为 d2d1409",
    },
    {
        "num": 5,
        "name": "发送邮件",
        "status": "failed",
        "duration_ms": 52000,
        "result": (
            "失败（BUG-006 复发）：qq-mail 连接器状态为 connected，但 ToolSearch 以 4 组精确名检索全部回落 agent-mail 命名空间，"
            "DeferExecuteTool 直调 mcp__qq-mail__SendMessage 返回 not found in the deferred tools index；"
            "agent-mail GetMe 返回 not_bound。按纪律未重试、未谎报，底稿已落 outbox 待人工补发："
            ".workbuddy/outbox/mail-2026-11-25-morning_briefing.html（18 823 字节 / maxline 761）"
        ),
        "outputs": [{"label": "邮件内容", "body": mail_body}],
    },
]

log = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "partial",
    "summary": (
        "交易日版：伦敦金 3551.4（-0.12%）、AU9999 763.3（-1.85%）、中间价 6.7088（调升 23bp）；"
        "数据/JSON/manifest/git 四步成功，邮件因 qq-mail 工具未装载、agent-mail 未开通而失败，email_sent:false，底稿已落 outbox"
    ),
    "timestamp": "11:32 CST",
    "trigger_note": "标称 09:00、实际 11:27:53 触发，延迟约 148 分钟（BUG-003）；交易日且有行情，未超 360 分钟阈值，顶部不标延迟",
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

raw = json.dumps(log, ensure_ascii=False, indent=2)
assert raw.count("%%") == 0
p = LOGDIR / f"{DATE}-morning_briefing.json"
p.write_text(raw, encoding="utf-8")

mp = LOGDIR / "manifest.json"
lm = json.load(open(mp, encoding="utf-8"))
rec = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "partial",
    "summary": "伦敦金 3551.4（-0.12%）、AU9999 763.3（-1.85%）、中间价 6.7088（+23bp）；邮件通道故障，底稿待补发",
}
arr = [x for x in lm["logs"] if not (x.get("date") == DATE and x.get("type") == "morning_briefing")]
arr.insert(0, rec)
lm["logs"] = arr
raw2 = json.dumps(lm, ensure_ascii=False, indent=2)
assert raw2.count("%%") == 0
mp.write_text(raw2, encoding="utf-8")

print("log written:", p.name, "| total_duration_ms =", log["summary_stats"]["total_duration_ms"])
print("logs/manifest head:", json.dumps(lm["logs"][:3], ensure_ascii=False))
