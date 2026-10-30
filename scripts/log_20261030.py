# -*- coding: utf-8 -*-
"""写 2026-10-30 早报日志 + buglog 条目。"""
import json, os, io, hashlib, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

D = "2026-10-30"
TS = "09:44:30"

# ---------- 1. buglog 四条 ----------
bug_entries = {
    ".buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md": (
        "- **2026-10-30（周五）延迟约 44 分钟**：触发时刻 09:44:30（`<current_time>` 实测），"
        "首次命令 `date` 实测 09:44:38，全部步骤结束约 09:49。距标称 09:00 延迟 44 分钟，"
        "落在「4-275 分钟极宽摆动」的中低位，介于 10/29 的 20 分钟与 10/28 的 275 分钟之间，"
        "摆动仍无收敛迹象。序列续记至 9/13-10/30 共 48 个日历日：…/约 67/约 51/275/约 20/**约 44**。"
        "10/19-10/30 连续十二个自然日、十个交易日全部产出，无缺跑、无提前触发。"
        "影响面：44 分钟延迟使伦敦金读数落在 09:41:00 的亚市 4003.96，当日已走出"
        "「开 4023.79 → 高 4026.24 → 低 3996.50（一度跌破 4000）→ 回到 4003.96」的完整行程，"
        "方向（-0.43%）未被扭曲；但需注意 09:00 准点时的读数约为 4020-4024（等于平盘附近），"
        "**延迟把「平盘」放大成了「跌 0.43%」，方向虽同、幅度已被放大**，与 10/28 的 275 分钟同属"
        "「延迟改变幅度」而非「延迟改变方向」。故建议 ②（定时提前至 07:00-07:30）继续维持，"
        "宿主侧仍应核查该 9:00 定时器的投递链路。第 ⑦ 条 in_progress 占位兜底本期未启用"
        "（会话单段连续完成、无中断），如实记为执行偏离。幂等检查前置：`daily/2026-10-30.json` 不存在、"
        "`logs/manifest.json` 头部无当日 morning_briefing 记录、`git log` 无当日早报提交 → 无中断残留"
        "（BUG-014 未复现）。前置缺口检查：上次早报 10/29（周四，success），10/30 为其后第一个交易日，"
        "其间无缺失交易日 → 无断档。\n"
    ),
    ".buglog/bugs/2026-09-14-inspection-email-connector-down.md": (
        "- **2026-10-30（周五）正常，第 15 次观察**：`mcp__qq-mail__GetMe` 一次命中（scope 含 `mail:send`、"
        "日配额 2000、主别名 2132049351@qq.com），`SendMessage` 用标准写法（`to` 传对象数组）＋"
        "`body_format: HTML` ＋ `skip_confirmation: true` 一次成功返回 `queued: true`，未触发 42801 令牌往返；"
        "已在已发送箱核实 `msg_cIeV17lN6JWoKZlVTt0lCYhNvgLDq-VczlXJ1StnY3zt-A`（2026-10-30T01:48:41Z ＝ "
        "09:48:41 CST）。邮件底稿 10 276 字节（最长行 419 字符，满足「每条新闻独立成行、单行 < 2000 字符」"
        "的回读约束）。形态序列 正常(10/29)→正常(10/30)，连续正常计数 2，距「连续 ≥5 日」门槛仍有 3 日；"
        "鉴于 10/19 与 10/28 均出现「连续三日正常→第 4 日复发」，本期成功不构成任何改善证据。"
        "另：本次未出现 auth-required 标记，无需走 10/28 建立的「授权→reconnect→GetMe→SendMessage」SOP。\n"
    ),
    ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md": (
        "- **2026-10-30（周五）体检：两线连续三日正常**：`logs/manifest.json` 头部三条为 "
        "`2026-10-29 inspection_pm partial`、`2026-10-29 inspection_noon no_action`、"
        "`2026-10-29 morning_briefing success`，再往下为 10/28 的 noon+pm 与 10/27 的 noon+pm —— "
        "即 **10/27、10/28、10/29 连续三个交易日两条线均有产出**，连续零产出交易日数 0，未达复合判据"
        "（连续 ≥5 日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出），不升级不降级。"
        "其中 10/29 晚间巡检为 `partial` 波动型预警（日内振幅约 1.65% 超 1.5% 阈值，已发邮件），"
        "属正确触发而非故障。10/30 的 noon（14:00）与 pm（22:00）尚未到点，不计异常。"
        "观察期自 10/27 起算已满 3 日；形态库维持五种（一起缺跑／一起提前／夜间合并触发／单线提前／正常）。\n"
    ),
    ".buglog/bugs/2026-09-26-buglog-hook-misfire.md": (
        "- **2026-10-30 第 32 次连续命中**（9/26-10/30）：hook 再次透传自动化任务提示词全文 → 判误判、"
        "未按字面建档。本期附带误报为 `scripts/build_20261030.py` 的「2 次编辑」弱提示 —— 实为"
        "`_meta.updated` 由初稿硬编码的 09:52 改为 `date` 实测的 09:47（当时实际 09:47，初稿写到了未来时间），"
        "属正常自检返工，非 bug 修复。本期工具调用零失败、零报错、零用户纠正。双重复核已执行："
        "逐文件 `grep -c \"2026-10-30\"` 计数与四文件字节数/SHA-1 已写入 "
        "`logs/2026-10-30-morning_briefing.json` 的 `buglog_verification`，index 与 bugs/ 已同步。\n"
    ),
}

for path, text in bug_entries.items():
    with io.open(path, "a", encoding="utf-8") as f:
        f.write("\n" + text)

# ---------- 2. index.md 追加观察段 ----------
index_block = """
## 2026-10-30（周五）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 44 分钟（09:44:30 触发、09:44:38 首次 `date` 实测），序列 48 个日历日 …/275/约 20/约 44，落在「4-275 分钟极宽摆动」中低位，摆动无收敛；10/19-10/30 连续十二个自然日、十个交易日无缺跑无提前。**本期延迟把「平盘」放大成「跌 0.43%」**：09:00 准点时读数约在 4020-4024（近平盘），09:41 取到 4003.96，方向不变但幅度被放大 |
| BUG-006 | **正常（第 15 次观察）**：`GetMe` 一次命中、`SendMessage` 标准写法＋`skip_confirmation` 直发返回 `queued: true`，已发送箱核实 `msg_cIeV17lN6JWoKZlVTt0lCYhNvgLDq-VczlXJ1StnY3zt-A`；底稿 10 276 字节（最长行 419 字符）。序列 正常(10/29)→正常(10/30)，连续计数 2，距「连续 ≥5 日」门槛仍有 3 日 |
| BUG-012 | 两线 10/27、10/28、10/29 **连续三个交易日均有产出**（10/29 noon 为 no_action、pm 为 partial 波动型预警，振幅约 1.65% 正确触发），连续零产出交易日数 0，未达复合判据；10/30 的 14:00／22:00 未到点不计 |
| BUG-013 | 第 32 次连续命中，判误判跳过建档；附带误报为 `build_20261030.py` 的「2 次编辑」——实为 `_meta.updated` 由 09:52 改为实测 09:47；双重复核已执行 |
"""
with io.open(".buglog/index.md", "a", encoding="utf-8") as f:
    f.write(index_block)

# ---------- 3. 复核凭据 ----------
def sha1(p):
    return hashlib.sha1(open(p, "rb").read()).hexdigest()

def nbytes(p):
    return os.path.getsize(p)

def gcount(p, kw):
    try:
        return open(p, encoding="utf-8").read().count(kw)
    except Exception:
        return -1

bug_files = [
    ".buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md",
    ".buglog/bugs/2026-09-14-inspection-email-connector-down.md",
    ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md",
    ".buglog/bugs/2026-09-26-buglog-hook-misfire.md",
]
ver = {}
for p in bug_files:
    ver[os.path.basename(p)] = {
        "date_hits": gcount(p, D),
        "bytes": nbytes(p),
        "sha1": sha1(p),
    }
ver[".buglog/index.md"] = {
    "date_hits": gcount(".buglog/index.md", D),
    "bytes": nbytes(".buglog/index.md"),
    "sha1": sha1(".buglog/index.md"),
}
ver["_note"] = ("date_hits 为文件中 2026-10-30 出现次数（应各为 1 或以上）；"
                "index 的 date_hits 同时包含观察段标题与本表；哈希用于下期比对是否被改写")

print(json.dumps(ver, ensure_ascii=False, indent=2))

# ---------- 4. 运行日志 ----------
EMAIL_BODY_SUMMARY = (
    "主题：🌅 今日金价早报 | 2026年10月30日 周五。正文含：金价快照（积存金 864.3 元/克 -0.43%、"
    "AU9999 858.1 元/克 -0.82%、汇率 6.71 -0.01%、伦敦金 4004.0 美元/盎司 -0.43%）；"
    "昨夜大事五条（PCE 同比 3.6%/核心 3.1% 创四个月新高＋Q3 GDP 3.4%；12 月加息 83% 但美元美债齐跌；"
    "中间价 6.7138 在岸升破 6.66；美国与欧洲合计释放 8200 万桶储备压油价；纳指跌 1.38% 但钱进美债不进黄金）；"
    "趋势建议（短 0／中 -1／长 1）；买卖时机（买 3990-4000／3975-3985／3943-3950，"
    "卖 4030-4040／4070-4082，止损 3975／3943）；今日学一招「季度通胀降温 vs 月度通胀加速」；"
    "底部附站点链接。HTML 底稿 10 276 字节，落 .workbuddy/outbox/2026-10-30-morning.html。"
)

log = {
    "date": D,
    "type": "morning_briefing",
    "status": "success",
    "summary": "五步全部成功：数据取自新浪实时接口＋SGE 延时行情＋上海证券报中间价，早报与日志均已推送，邮件已发送至 2132049351@qq.com",
    "timestamp": "09:44 CST",
    "steps": [
        {"num": 1, "name": "获取数据", "status": "success", "duration_ms": 98000,
         "result": ("伦敦金 4003.96 美元/盎司（-0.43%，09:41，开 4023.79／高 4026.24／低 3996.50，"
                    "亚市一度跌破 4000）；AU9999 858.14 元/克（-0.82%，昨收 865.26）；"
                    "中间价 6.7138（调升 9 个基点）；昨夜 PCE＋GDP 双超预期等 5 条新闻与 3 条机构观点"),
         "source": "WebSearch（汇通财经／新华财经／上海证券报／证券时报／金融界）＋ 新浪财经实时接口 ＋ SGE 延时行情"},
        {"num": 2, "name": "生成早报JSON", "status": "success", "duration_ms": 82000,
         "result": "已写入 daily/2026-10-30.json（自检 0 error，advice 183 字，11 组价位复算全中）"},
        {"num": 3, "name": "更新manifest", "status": "success", "duration_ms": 6000,
         "result": "已追加记录到 manifest.json 的 briefings 头部"},
        {"num": 4, "name": "Git推送", "status": "success", "duration_ms": 18000,
         "result": "已提交 8380b13 并推送，ls-remote 与 rev-parse 一致"},
        {"num": 5, "name": "发送邮件", "status": "success", "duration_ms": 61000,
         "result": "已发送至 2132049351@qq.com（queued:true，msg_cIeV17lN6JWoKZlVTt0lCYhNvgLDq-VczlXJ1StnY3zt-A）",
         "outputs": [{"label": "邮件内容", "body": EMAIL_BODY_SUMMARY}]},
    ],
    "summary_stats": {
        "total_steps": 5, "success_steps": 5, "failed_steps": 0,
        "total_duration_ms": 265000, "email_sent": True, "git_pushed": True,
    },
    "data_snapshot": {
        "london_xauusd": "4004.0 USD/oz (-0.43%)",
        "au9999": "858.1 CNY/g (-0.82%)",
        "usd_cny_mid": "6.7138 (+9bp)",
        "hero_cumulative_gold": "864.3 CNY/g",
        "prev_close": "4021.1（汇通 4021.13／新浪 4021.23／国际金融报 4021.74）",
    },
    "gap_check": {
        "last_briefing_date": "2026-10-29",
        "last_briefing_status": "success",
        "missed_trading_days": [],
        "conclusion": "10/30 为 10/29 之后第一个交易日，其间无缺失交易日 → 无断档",
    },
    "health_check": {
        "inspection_noon_recent": "2026-10-29（no_action）",
        "inspection_pm_recent": "2026-10-29（partial，波动型预警，振幅约 1.65%）",
        "consecutive_zero_output_trading_days": 0,
        "conclusion": "两线 10/27-10/29 连续三个交易日有产出，未达复合判据，不升级不降级",
    },
    "idempotency_check": {
        "daily_exists_before": False,
        "logs_manifest_head_has_today": False,
        "git_log_has_today": False,
        "conclusion": "无中断残留，BUG-014 未复现",
    },
    "buglog_verification": ver,
    "notes": [
        "伦敦金改由新浪财经 hf_XAU 实时接口取数（09:41:00），与本项目历史口径（金投网实时页）聚类一致，"
        "多源交叉 4003.34／4005.61／4006.23 均落在 4003-4006。",
        "10-29 图表点由昨日 09:14 快照 4054.09 回填为真实收盘 4021.1，同时把 10-29 事件文案改写为全日走势"
        "（原为亚市快照描述），否则图表与事件自相矛盾。",
        "AU9999 涨跌基准取昨日（10/29）收盘 865.26，不是昨日早报的 870.6（那是 09:20 的早盘读数）。",
        "口径差逐日重算：按中间价 6.7138 折算 864.3 元/克，比按市场即期（在岸夜盘 6.6612）折算高 6.8 元/克，"
        "为近月最大，主因人民币升至 2022 年 6 月以来最强、中间价与市场价差拉大。",
        "邮件底稿最长行 419 字符，满足 Read 回读不截断（< 2000 字符）的前提，但本期为「手写紧凑版直接入参」，"
        "未走回读链路。",
    ],
}

json.dump(log, open("logs/%s-morning_briefing.json" % D, "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

# ---------- 5. logs/manifest.json ----------
lm = json.load(open("logs/manifest.json", encoding="utf-8"))
lm["logs"].insert(0, {
    "date": D, "type": "morning_briefing", "status": "success",
    "summary": ("4000 关口亚市被砸穿一次（最低 3996.50）又拉回，伦敦金 4003.96（-0.43%）、AU9999 858.1（-0.82%）、"
                "中间价 6.7138（+9 基点）、积存金估 864.3；昨夜 PCE 同比 3.6%/核心 3.1% 创四个月新高、Q3 GDP 3.4% 超预期，"
                "12 月加息概率 83% 但美元美债齐跌；邮件已发"),
})
json.dump(lm, open("logs/manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("log + logs/manifest written")
