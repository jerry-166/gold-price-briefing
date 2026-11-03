# -*- coding: utf-8 -*-
"""写 2026-11-03 早报运行日志 + 更新 logs/manifest.json。"""
import io, os, json, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS = os.path.join(BASE, "logs")
now = datetime.datetime.now()

VERIFY = json.load(io.open(os.path.join(BASE, ".buglog", "_verify_20261103.json"), encoding="utf-8"))

EMAIL_BODY_TAIL = (
    "邮件正文（HTML 摘要）：今日金价早报 · 2026年11月3日 周二｜"
    "金价快照：招行积存金（估）851.5 元/克 ▼-0.06%、上海金 AU9999 847.1 元/克 ▲+1.32%、"
    "美元中间价 6.71 ▲+0.01%、伦敦金 3944.1 美元/盎司 ▼-0.06%。"
    "昨夜大事：①油价一天崩 8%（布伦特 104.32/-8.08%、WTI 96.26/-7.55%），伊朗提两天重开霍尔木兹的条件、美国尚未接受，"
    "油价跌→通胀预期降→12 月加息定价自 80% 回落至 73%-74.9%，金价自 3870.25 反弹至 3965.98、收 3946.47（+1.80%）；"
    "②Kitco 调查华尔街 63% 看空、散户 53% 看多，3900-4000 成新战场；③美国 10 月 ISM 制造业 PMI 55.5 超预期但投入价格 77.9→75.2；"
    "④AU9999 补涨 1.32%，内盘溢价基本抹平。"
    "趋势：短期中性/中期偏弱/长期偏强，动作=观望。"
    "买卖时机：回踩 3880-3900 美元（约 838-842 元/克）上三成、3830-3850（约 827-831）补第二份、3760-3780（约 812-816）留最后一份；"
    "反弹 3990-4020 美元（约 861-868 元/克）减半、4040-4060（约 872-876）止盈；收盘破 3870（约 835）减仓、破 3840（约 829）离场。"
    "今日学一招：中期选举凭什么给黄金换剧本——看的不是谁赢，是实际收益率。"
    "底部链接：https://jerry-166.github.io/gold-price-briefing/"
)

log = {
    "date": "2026-11-03",
    "type": "morning_briefing",
    "status": "success",
    "summary": (
        "周二正常交易：伦敦金 10:21 报 3944.05（-0.06%）、AU9999 补涨 1.32% 至 847.10、"
        "中间价 6.7150 调贬 4 点、积存金估 851.5；昨夜油价崩 8% 是金价自一年低位反弹的总开关，"
        "本期把 11-02 图表点由早盘快照回填为真实收盘 3946.5。推送与邮件均成功（email_sent:true），触发延迟约 81 分钟。"
    ),
    "timestamp": now.strftime("%H:%M CST"),
    "steps": [
        {
            "num": 1,
            "name": "获取数据",
            "status": "success",
            "duration_ms": 168000,
            "result": (
                "伦敦金 3944.05（昨收 3946.47、开 3948.82、高 3964.31、低 3941.31，新浪 hf_XAU 10:21）；"
                "AU9999 847.10（昨收 836.08、开 836.00、高 849.99、低 834.00）；T+D 846.95；"
                "中间价 6.7150（调贬 4 点，中国经济网/中宏网/中新网三源一致）；离岸 6.6683；"
                "COMEX 12 月期金 3953.0（-0.42%）；油价布伦特 104.32(-8.08%)、WTI 96.26(-7.55%)；"
                "CME 12 月加息 74.9%；新闻 7 条（油价、和谈、加息、选举、Kitco 分歧、ISM、国内补涨），全部带原始 url"
            ),
            "source": "新浪财经 hf_XAU/gds_AU9999/gds_AUTD、东方财富 push2、同花顺期货通、汇通网、华尔街见闻、第一财经、金投网、金价查询网、WebSearch",
        },
        {
            "num": 2,
            "name": "生成早报JSON",
            "status": "success",
            "duration_ms": 96000,
            "result": "已写入 daily/2026-11-03.json（check_briefing.py 0 error，advice 197 字、价位配对 12 组全部复算通过、汇率 2 位小数）",
        },
        {
            "num": 3,
            "name": "更新manifest",
            "status": "success",
            "duration_ms": 5000,
            "result": "已在 briefings 头部追加 2026-11-03 记录，条数 73 → 74",
        },
        {
            "num": 4,
            "name": "Git推送",
            "status": "success",
            "duration_ms": 21000,
            "result": "commit 91e11da（每日早报 2026-11-03），SSH 推送成功；git rev-parse 与 git ls-remote 均为 91e11da，远端 master 一致",
        },
        {
            "num": 5,
            "name": "发送邮件",
            "status": "success",
            "duration_ms": 262000,
            "result": "已发送至 2132049351@qq.com（10:26:17 CST 入已发送箱，message_id msg_oOcBSW1…，12 631 字符 / 18 127 字节）；发信前修掉 BUG-018（格式化行裸百分号 TypeError），回归检查 width:100%% 计数 0、width:100% 两处",
            "outputs": [{"label": "邮件内容", "body": EMAIL_BODY_TAIL}],
        },
    ],
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": 552000,
        "email_sent": True,
        "git_pushed": True,
    },
    "buglog_verification": {
        "method": "逐文件 grep -c 2026-11-03 计数 + 字节数/SHA-1 双重复核；index.md 与 bugs/ 内容一致性人工比对",
        "bugs": ["BUG-003", "BUG-006", "BUG-012", "BUG-013", "BUG-018"],
        "files": VERIFY,
        "note": "五个 bug 文件均命中 2026-11-03（计数各 ≥1）；新建 BUG-018 文件 2 612 字节、含 BUG-018 标识；index.md 头部计数已同步为 Open 11 / Fixed 7 / Total 18，并把 BUG-017、BUG-018 补入 ID 表",
    },
}

p = os.path.join(LOGS, "2026-11-03-morning_briefing.json")
with io.open(p, "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
print("written", p)

mp = os.path.join(LOGS, "manifest.json")
m = json.load(io.open(mp, encoding="utf-8"))
entry = {
    "date": "2026-11-03",
    "type": "morning_briefing",
    "status": "success",
    "summary": "伦敦金 3944.05(-0.06%)、AU9999 847.10(+1.32%)补涨、中间价 6.7150 调贬 4 点、积存金估 851.5；油价崩 8% 驱动昨日反弹，11-02 图表点回填真实收盘 3946.5",
}
m["logs"] = [x for x in m.get("logs", []) if not (x.get("date") == "2026-11-03" and x.get("type") == "morning_briefing")]
m["logs"].insert(0, entry)
with io.open(mp, "w", encoding="utf-8") as f:
    json.dump(m, f, ensure_ascii=False, indent=2)
print("logs manifest head:", json.dumps(m["logs"][:2], ensure_ascii=False))
