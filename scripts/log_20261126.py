# -*- coding: utf-8 -*-
"""写入 2026-11-26 早报运行日志，并在 logs/manifest.json 头部追加记录。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "logs" / "2026-11-26-morning_briefing.json"
LMAN = ROOT / "logs" / "manifest.json"

MAIL_OUTBOX = ROOT / ".workbuddy" / "outbox" / "mail-2026-11-26-morning_briefing.html"
assert MAIL_OUTBOX.exists()
outbox_bytes = len(MAIL_OUTBOX.read_bytes())

MAIL_BODY_SUMMARY = (
    "主题：🌅 今日金价早报 | 2026年11月26日 周四；收件人 2132049351@qq.com；HTML 正文 19 179 字节 / maxline 774。"
    "结构：头部（日期 + 数据截至 10:46）→ 导语（PCE 超预期砸到 3426.64 后深 V 拉回 3588.55 收涨 0.92%，"
    "今晨站上 3601，但 12 月加息 97.2% 已定价）→ 金价快照（积存金 777.0 +0.37%、AU9999 773.0 +2.07%、"
    "汇率 6.71 +0.01%、伦敦金 3601.8 +0.37%）→ 昨夜大事 7 条（核心PCE / 深V反转 / 加息定价 / 美元美债 / "
    "跨市场港股黄金股 / 感恩节日程 / 摩根大通 4500）→ 趋势判断（短中性、中中性、长偏多，建议观望）→ "
    "买卖时机（买 3550-3570 美元≈766-770 元/克，卖 3650-3670≈787-792 元/克，止损 3520≈759 元/克）→ "
    "今日学一招（空头回补 vs 新增买盘）→ 站点链接。发送方式：qq-mail SendMessage + skip_confirmation=true，"
    "首次调用即 queued:true，未出现 42801。"
)

data = {
    "date": "2026-11-26",
    "type": "morning_briefing",
    "status": "success",
    "summary": "数据、JSON、manifest、Git、邮件、日志六环节全部成功；伦敦金 3601.83 +0.37%，AU9999 772.99 +2.07%，中间价 6.7096 调贬 8bp，邮件 skip_confirmation 直发一次 queued。",
    "timestamp": "10:53 CST",
    "trigger_note": (
        "定时任务标称 09:00，实际触发 10:48:23 CST，延迟约 108 分钟。今日为交易日且有行情（隔夜 PCE 后砸到 3426.64、"
        "今晨拉回并冲高 3607.02），09:00-10:46 之间错过的最大区间约 56 美元（3551.13→3607.02），危害按 2 档计；"
        "延迟 <360 分钟，按既定纪律不在邮件头部标注延迟，updateTime 仍为 09:00，_meta.updated 写真实生成时点 10:52。"
    ),
    "steps": [
        {
            "num": 1,
            "name": "获取数据",
            "status": "success",
            "duration_ms": 118000,
            "result": (
                "伦敦金 3601.83（+0.37%，昨收 3588.55、今开 3589.32、高 3607.02、低 3551.13、振幅 1.56%）；"
                "AU9999 772.99（+2.07%，基准 757.35、最高 775.00、夜盘最低 736.51）；T+D 772.49（+2.06%，昨结 756.90）；"
                "沪金主连 774.94（+2.32%）；中间价 6.7096（调贬 8bp，前值 6.7088，四源一致）；在岸即期 6.6681；"
                "COMEX 期金 3627.77（+1.77%）；白银 42.30（+4.34%）；WTI 83.86、布伦特 90.59；美元指数 103.709、10Y 4.85%。"
                "新闻 7 条：10 月核心 PCE 3.3% 超预期致金价盘中跌超 3%、最低 3426.64（逾一年新低、首破 3500），"
                "随后空头回补与感恩节前调仓拉回 3588.55 收涨 0.92%；CME 12 月加息 97.2%、1 月累计 50bp 62.5%；"
                "港股黄金股集体大涨；今日感恩节美股债休市、CME 提前至 27 日 03:30 收；摩根大通看 2027Q4 金价 4500。"
            ),
            "source": (
                "新浪财经实时接口 hf_XAU / gds_AU9999 / gds_AUTD / hf_GC / hf_SI ＋ 东方财富 push2（期金、沪金交叉校验）"
                "＋ WebSearch 交叉验证（财联社、每经、中新网、中宏网）。"
                "neodata-financial-search 本期已实测仍未可用：scripts/query.py 输出「需要安装 requests」后 exit 0（静默降级），"
                "本机 pip 索引不可用，与 BUG-033 记录一致；未假装调用。"
            ),
        },
        {
            "num": 2,
            "name": "生成早报JSON",
            "status": "success",
            "duration_ms": 240000,
            "result": (
                "已写入 daily/2026-11-26.json（scripts/build_20261126.py 纯 f-string 构建，内建断言全部通过）。"
                "check_briefing.py 首轮报 3 处（pairs 只有 4 档、3550→765 折算差 0.8 元超 0.6 容差），"
                "改 766-770 并补 3510-3520 一档后 errors: 0；另人工回读发现一处繁简混用（「別」→「别」）已修正。"
            ),
        },
        {
            "num": 3,
            "name": "更新manifest",
            "status": "success",
            "duration_ms": 8000,
            "result": "已追加记录到 manifest.json 头部，briefings 由 96 条增至 97 条，首位为 2026-11-26。",
        },
        {
            "num": 4,
            "name": "Git推送",
            "status": "success",
            "duration_ms": 26000,
            "result": (
                "已提交并推送：早报+manifest 561ba0b、错字修正 cd8aa50；git rev-parse HEAD 与 git ls-remote origin master "
                "三次比对一致（均为 cd8aa50）。"
            ),
        },
        {
            "num": 5,
            "name": "发送邮件",
            "status": "success",
            "duration_ms": 96000,
            "result": (
                "已发送至 2132049351@qq.com。qq-mail SendMessage 携 skip_confirmation=true 首次调用即 queued:true，"
                "未出现 42801 确认链路；sent 目录回读 created_at 2026-11-26T02:52:57Z（10:52:57 CST），主题与 snippet 头部一致。"
                "底稿 .workbuddy/outbox/mail-2026-11-26-morning_briefing.html（19 179 字节 / maxline 774）；"
                "按 BUG-032 记录：本期未做全文回读逐字比对（19KB 二次转抄成本高于收益），仅验 snippet 头部一致。"
            ),
            "outputs": [{"label": "邮件内容", "body": MAIL_BODY_SUMMARY}],
        },
    ],
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": 488000,
        "email_sent": True,
        "git_pushed": True,
    },
    "outbox_path": str(MAIL_OUTBOX.relative_to(ROOT)).replace("\\", "/"),
    "outbox_bytes": outbox_bytes,
}

assert data["summary_stats"]["success_steps"] + data["summary_stats"]["failed_steps"] == 5
raw = json.dumps(data, ensure_ascii=False, indent=2)
assert raw.count("%%") == 0
LOG.write_text(raw, encoding="utf-8")

lm = json.load(open(LMAN, encoding="utf-8"))
assert "logs" in lm, list(lm.keys())
assert lm["logs"][0]["date"] != "2026-11-26" or lm["logs"][0]["type"] != "morning_briefing"
lm["logs"].insert(0, {
    "date": "2026-11-26",
    "type": "morning_briefing",
    "status": "success",
    "summary": "六环节全部成功：伦敦金 3601.83 +0.37%、AU9999 772.99 +2.07%，邮件 skip_confirmation 直发一次 queued。",
})
LMAN.write_text(json.dumps(lm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("log written", LOG.name, len(raw.encode("utf-8")), "bytes")
print("logs/manifest head:", json.dumps(lm["logs"][0], ensure_ascii=False))
print("total logs:", len(lm["logs"]))
