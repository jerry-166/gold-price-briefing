# -*- coding: utf-8 -*-
"""写入 2026-10-27 运行日志 + buglog 留痕 + logs/manifest 追加。"""
import json, os, hashlib, subprocess, io

BASE = r"D:\workspace\每日金价资讯"
DATE = "2026-10-27"
BUG = os.path.join(BASE, ".buglog", "bugs")

B003 = os.path.join(BUG, "2026-09-08-briefing-scheduler-missed-days.md")
B006 = os.path.join(BUG, "2026-09-14-inspection-email-connector-down.md")
B012 = os.path.join(BUG, "2026-09-25-inspection-scheduler-silent-miss.md")
B013 = os.path.join(BUG, "2026-09-26-buglog-hook-misfire.md")
B016 = os.path.join(BUG, "2026-10-27-selfcheck-hardcoded-baseline.md")

# ---------- 1) BUG-003 延迟 ----------
t003 = """

- **2026-10-27（周二）延迟约 51 分钟**：会话起始 09:50:42（`<current_time>` 实测），首次命令 `date` 实测 09:50:55，全部步骤结束约 10:05。序列续记至 9/13-10/27 共 45 个日历日：…/约 46/约 100/约 67/**约 51**（回落到区间中低位，低于 10/26 的 67 分钟、高于 10/23 的 39 分钟），仍属「4-152 分钟极宽摆动」，未刷新任何边界。10/19-10/27 连续九个自然日、七个交易日全部产出，无缺跑、无提前触发。影响面：51 分钟延迟使伦敦金读数落在 09:46 的亚市实时价 4015.53（今开 4016.83、当日已走出 4003.70-4019.93 的 16 美元区间），若准点 09:00 取价会更贴近 4017 的昨收水平，当日方向（-0.04%）不受影响 → **建议 ②（定时提前至 07:00-07:30）继续维持**。第 ⑦ 条 in_progress 占位兜底本期未启用（会话单段连续完成），如实记为执行偏离。幂等检查前置：`daily/2026-10-27.json` 不存在、`logs/manifest.json` 头部无当日 morning_briefing 记录、`git log` 无当日早报提交 → 无中断残留（BUG-014 未复现）。前置缺口检查：上次早报 10/26（周一，success），10/27 为其后第一个交易日，其间无缺失交易日 → 无断档。
"""

# ---------- 2) BUG-006 邮件 ----------
t006 = """

- **2026-10-27（周二）恢复正常（第 13 次观察）**：ToolSearch 以精确名 `mcp__qq-mail__SendMessage` 一次命中；`SendMessage` 用标准写法（`to` 传对象数组）＋`body_format: HTML`＋`skip_confirmation: true` 直发，返回 `queued: true`、`email_sent: true`。形态序列：…→未注册(10/24)→正常(10/25)→正常(10/26)→**正常(10/27)**，为 10/16-10/18 之后**首次连续三日正常**（追平本 bug 历史最长正常窗口），但仍远低于「连续 5 个交易日正常」的升级判据 → **不构成修复证据**，severity 维持 major。
- **入参体积（经验续记）**：本期邮件底稿 **9 273 字节**（比 10/26 的 11 447 字节再缩 19%），一次投递成功，进一步印证「≤12 KB 可稳定投递」，且压线越低压越稳。
"""

# ---------- 3) BUG-012 巡检 ----------
t012 = """

- **2026-10-27 四维体检**：`inspection_noon` 最近产出 **10/26**（实际 14:18 落盘，较标称 14:00 延迟约 18 分钟、no_action）、`inspection_pm` 最近产出 **10/26**（22:00 准时、no_action）；两条线 10/26 同日产出，为 10/21 之后又一次「双线同日正常」，无「一起提前」「一起缺跑」镜像。10/27 的 14:00／22:00 尚未到点，不计异常。**连续零产出交易日数 0**，未达复合判据 → 不升级不降级；观察期自 10/15 起算已满 2 周窗口，**转入新一轮观察期（自 10/27 起算）**，升级仍须满足「连续 ≥5 个正常交易日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出」。
- **口径澄清**：10/26 早报的 buglog 条目写「双线最近产出均为 10/23」，那是该期 10:07 落笔时的真实状态（当日 14:00／22:00 未到），非记录错误；10/26 两条线随后均按时产出，故本期已纠正为 10/26。
"""

# ---------- 4) BUG-013 hook 误判 ----------
t013 = """

- **2026-10-27 第二十九次连续命中（9/26-10/27）**：hook 再次透传自动化提示词全文 → 判误判、未按字面建档。附带误报本期出现两类形态：①把 `scripts/check_briefing.py` 的两次编辑弱提示为「正在修 bug」——**本次该提示是对的**，该脚本确有真实缺陷（硬编码上一日汇率与价位 token，日更必报 7 条假错），已独立建档为 **BUG-016**，这是首次出现「弱提示指向真缺陷」的反例，说明弱提示不可一律忽略，需逐条判内容；②把 `scripts/build_20261027.py` 的 `%` 格式化 `ValueError` 修复弱提示为 bug 修复，实为写作前未预判字面 `%` 的正常返工（10/23 已固化的经验：正文一律 f-string 或 `{{TOKEN}}` + `str.replace`，不用 `%`）。双重复核已执行（逐文件 `grep -c` 计数＋五文件字节数/SHA-1 ＋ index 哈希，均写入 `logs/2026-10-27-morning_briefing.json` 的 `buglog_verification`）。
"""

# ---------- 5) BUG-016 新档 ----------
new016 = """# BUG-016 自检脚本硬编码上一日的汇率与价位 token，日更必产生假错警报

- **ID**: BUG-016
- **日期**: 2026-10-27
- **严重度**: minor
- **状态**: fixed
- **影响面**: 每日早报的提交前自检（`scripts/check_briefing.py`）、自检结论的可信度

## 现象

2026-10-27 对 `daily/2026-10-27.json` 运行 `scripts/check_briefing.py`，报 **7 条 error**：

```
- hero mismatch 867.1 vs 867.2
- token missing in plan/advice: 3940-3950
- token missing in plan/advice: 4018-4025
- token missing in plan/advice: 4060-4087
- token missing in plan/advice: 868-869
- token missing in plan/advice: 877-882
- token missing in plan/advice: 842
```

产物本身没有问题（`json.load` 通过、结构完整、价位经独立脚本复算全部命中），7 条全部为假错。

## 根因

1. 脚本把 `rate = 6.7162` 直接写死为 10/26 的中间价，而当日中间价已变为 6.7171 → hero 复算偏差 0.1 元 → 报 mismatch。
2. 脚本把 10/26 那期的价位 token（`3975-3985`、`3940-3950`、`4018-4025`、`4060-4087`、`868-869`、`877-882`、`842`）写死成核对清单，而这些价位每天随行情移动 → 每天必然少 6 条。
3. 更深一层：**自检脚本把「当期临时数据」当成了「校验规则」**。规则应当是「价位区间必须能由当日汇率复算且与 advice 一致」，而不是「必须出现昨天那串数字」。假错一旦成为日常，真错就会被淹没——这与 BUG-011（引号校验假阳性）属同一类缺陷：**校验器自身逻辑错误，比被校验对象更危险**。

## 修复

`scripts/check_briefing.py` 改为**通用版**，不再依赖任何日期常量：

- 汇率从产物自身提取：正则 `中间价[^0-9]{0,6}(\\d\\.\\d{4})` 读 `prices[2].source`，再用它复算 hero；
- 价位改**双向配对复算**：正则抓出所有「美元区间（约 ¥ 区间 元/克）」，两端分别用当日汇率正算比对（容差 0.6 元/克），不再核对固定 token；
- `plan.buy/sell` 的每一档美元区间必须出现在 `trend.advice`（一致性约束，而非固定清单）；
- 新增精度校验（金价 ≤2 位小数、汇率必须 2 位、change 必须 2 位）、`**` 字面加粗残留校验、labels 去重与严格递增校验。

## 验证

同一次运行：修复前 7 error；修复后先收敛到 1 条真错（`4030-4040 → 870.3-872.5` 而正文写 871-873，人工写错），改正为 `870-873` 后 **0 error / OK**。说明新校验器既能自动适配每日汇率，也确实抓得住人工笔误。
"""


def append(path, text):
    with io.open(path, "a", encoding="utf-8") as f:
        f.write(text)


append(B003, t003)
append(B006, t006)
append(B012, t012)
append(B013, t013)
with io.open(B016, "w", encoding="utf-8") as f:
    f.write(new016)

# ---------- 6) index.md：计数器 + 表格行 + 本期观察 ----------
idx = os.path.join(BASE, ".buglog", "index.md")
s = io.open(idx, encoding="utf-8").read()
s = s.replace("Open: 11 | Fixed: 4 | Total: 15", "Open: 11 | Fixed: 5 | Total: 16")
row016 = ("| BUG-016 | 自检脚本硬编码上一日汇率与价位 token，日更必报 7 条假错（10/27 首次定位；"
          "已改为从产物自身提取汇率、价位双向配对复算） | minor | fixed |\n")
if "| BUG-016 |" not in s:
    s = s.replace("\n\n## 2026-10-23（周五）观察更新", row016 + "\n## 2026-10-23（周五）观察更新", 1)

section = """## 2026-10-27（周二）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 51 分钟（会话起始 09:50:42、首次 `date` 09:50:55 实测），序列 45 个日历日 …/约 100/约 67/约 51，回落至区间中低位，仍属「4-152 分钟极宽摆动」；10/19-10/27 连续九个自然日、七个交易日无缺跑、无提前 |
| BUG-006 | **恢复正常（第 13 次观察）**：ToolSearch 精确名一次命中，`SendMessage` 标准写法返回 `queued: true`、`email_sent: true`；形态序列 正常(10/25)→正常(10/26)→正常(10/27)，为 10/16-10/18 后**首次连续三日正常**，追平历史最长窗口但仍低于 5 日判据，不构成修复证据；邮件底稿 9 273 字节（较昨日再缩 19%） |
| BUG-012 | `inspection_noon`/`inspection_pm` 最近产出均为 10/26（14:18／22:00，双线同日正常）；10/27 未到点不计；**连续零产出交易日数 0**，未达复合判据；观察期自 10/15 起满 2 周，转入新一轮（自 10/27 起算） |
| BUG-013 | 第 29 次连续命中，判误判跳过建档；附带弱提示本期**首次指向真缺陷**（check 脚本硬编码）→ 已独立建档 BUG-016，说明弱提示需逐条判内容而非一律忽略；另一条为 `%` 格式化返工的正常迭代 |
| BUG-016 | **新增（fixed）**：自检脚本硬编码 10/26 的汇率 6.7162 与 7 个价位 token → 本期报 7 条假错（product 本身无误）；已改为通用版（汇率从 `prices[2].source` 提取、价位双向配对复算、精度与 `**` 残留校验），复跑 0 error |

"""
if "## 2026-10-27（周二）观察更新" not in s:
    s = s.rstrip("\n") + "\n\n" + section
io.open(idx, "w", encoding="utf-8").write(s)

# ---------- 7) 复核凭据 ----------
def cred(path):
    raw = open(path, "rb").read()
    txt = raw.decode("utf-8")
    return {
        "file": os.path.relpath(path, BASE).replace("\\", "/"),
        "grep_c_2026_10_27": txt.count("2026-10-27"),
        "bytes": len(raw),
        "sha1": hashlib.sha1(raw).hexdigest(),
    }


files = [B003, B006, B012, B013, B016]
verification = {
    "checked_at": "2026-10-27 09:58 CST",
    "method": "逐文件 grep -c 等价计数（utf-8 文本 count）＋ 字节数 ＋ SHA-1；另校验 index.md 与 bugs/ 内容一致",
    "files": [cred(p) for p in files],
    "index_md": cred(idx),
    "index_counter": "Open: 11 | Fixed: 5 | Total: 16",
    "index_has_016_row": "| BUG-016 |" in io.open(idx, encoding="utf-8").read(),
    "index_has_today_section": "## 2026-10-27（周二）观察更新" in io.open(idx, encoding="utf-8").read(),
}
assert all(f["grep_c_2026_10_27"] >= 1 for f in verification["files"]), verification
assert verification["index_has_016_row"] and verification["index_has_today_section"]

# ---------- 8) 运行日志 ----------
email_text = """🌅 今日金价早报 | 2026年10月27日 周二

【金价快照】
· 招行积存金（估算）867.2 元/克  ▼0.04%
· 上海金 AU9999      863.1 元/克  ▲0.20%
· 人民币中间价        6.7171      调贬 9 个基点
· 伦敦金 XAUUSD     4015.5 美元/盎司  ▼0.04%

【一句话】金价昨天从三个月低点爬回 4000 上方（收 4016.97、+0.48%），今天没接着冲，全天只在 4003-4020 这 16 美元里磨。油价连跌两天给了喘息，但 12 月加息这把刀还悬着。

【昨夜大事】
1. 美联储：本周（10/27-28）按兵不动 89.5%、加息仅 10.5%；但 12 月加息 25bp 还有 73.9%、加 50bp 8.4%，年内至少再加一次合计 82.3%。「这次不加」已被吃进价格，压金价的是「12 月还要加」。
2. 中东：沙特、土耳其、巴基斯坦高官齐聚德黑兰斡旋，传「5 日互让协议」（重开霍尔木兹换解除封锁）；同时美媒称美军已备好新一轮打击，可能在 11 月 3 日中期选举后 96 小时内动手——一边谈一边备战，油价难痛快跌。
3. 油价：WTI 主力跌 1.96% 报 101.25、布伦特主力跌 1.39% 报 110.15，能源通胀预期缓和，金价才有底气收复 4000。
4. 机构与实物：汇丰把 2026 年均价预测从 4560 下调到 4490 美元；国内金饰回落到 1192-1205 元/克、投资金条重返 878 元/克的「8 字头」，赤峰黄金三季度净利同比 -41.84%。

【趋势】
短期 震荡（-0）—— 4000 收复但 4030 上方套牢盘还在，决议前是 4000-4030 箱体，反弹是修复不是反转
中期 偏弱（-1）—— 12 月加息 73.9%-80%、2 年期美债还在往上，方向看周四 PCE
长期 偏强（+1）—— 央行连续 23 个月购金、三季度 ETF 净流入创纪录，配置盘没走
建议：观望。别追高也别急着抄底，明晚决议、周四 PCE 连着来，等尘埃落定再动手。

【买卖时机】
买：4000-4005 美元（约 864-865 元/克）先上 3 成 → 3975-3985（858-861）再加 3 成（3975.58 与 3978.01 双底）→ 3943-3950（851-853）用最后一份钱（近一年低点）
卖：4030-4040 美元（约 870-873 元/克）减半（昨日高点 4029.78）→ 4060-4080（877-881）全部止盈；止损：收盘破 3975（约 858）减半、破 3943（约 851）清仓；站上 4100（约 885）并站稳则空头结构破，别再做空。
（按中间价 6.7171 折算，仅供参考，不构成投资建议。）

【今日学一招】同一分钟两个网站差 14 美元：一个报现货、一个报期货
09:46 伦敦金现货 4015.5、COMEX 12 月期金 4029.2，差 13.7 美元。现货是「马上交割的实物金」，期货是「12 月才交割的合约」，多出来的 10-15 美元叫基差，= 仓储保险 + 资金利息 + 12 月前的涨价预期，利率越高这笔越贵。所以算涨跌幅要用现货、看市场押注才看期货，两者不能混着比。

完整早报与 30 日走势图：https://jerry-166.github.io/gold-price-briefing/"""

log = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "success",
    "summary": (
        "周二早报（触发 09:50:42／延迟约 51 分钟）五步全部成功、邮件正常发送（queued:true）："
        "金 4015.5(-0.04%)、AU9999 863.1(+0.20%)、中间价 6.7171(调贬 9 基点)、积存金估算 867.2；"
        "主线「4000 收复、16 美元窄缝等决议」——昨日自三个月低位 3975 反弹、收 4016.97(+0.48%)，今日仅在 4003.70-4019.93 磨；"
        "油价连跌两日（WTI 主力 101.25／-1.96%、布伦特 110.15／-1.39%）是唯一支撑，12 月加息仍 73.9%-80%、年内再加一次 82.3%；"
        "国内同步修复、内盘折价收窄至约 4 元/克；短 0/中 -1/长 1、action=watch；teach 讲「现货 vs 期货基差」。"
    ),
    "timestamp": "09:50 CST",
    "gap_check": {
        "last_briefing_date": "2026-10-26",
        "missed_trading_days": [],
        "consecutive_missed_days": 0,
        "note": (
            "上一期早报 10-26（周一）正常产出，本期为其后第一个自然日、第一个交易日，其间无缺失交易日 → 无断档。"
            "幂等检查前置：daily/2026-10-27.json 不存在、logs/manifest.json 头部无当日 morning_briefing 记录、"
            "git log 无当日早报提交 → 无中断残留（BUG-014 未复现）。巡检体检：inspection_noon 与 inspection_pm 最近产出均为 10-26"
            "（14:18／22:00），双线同日正常、连续零产出交易日数 0（BUG-012 未达升级判据）。"
        ),
    },
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 5,
        "failed_steps": 0,
        "total_duration_ms": 612000,
        "email_sent": True,
        "git_pushed": True,
    },
    "steps": [
        {
            "num": 1, "name": "获取数据", "status": "success", "duration_ms": 196000,
            "result": (
                "NeoData 首次返回 TOKEN_MISSING → connect_cloud_service 取凭证 → --save-token 后续查成功："
                "AU9999 862.00（+0.07%，昨结 861.41、今开 864.00，行情时间 09:52）、中间价 2 位记 6.72／+9 基点、"
                "伦敦金 AUUSDO.LIFFE 4029.20（-0.23%，昨结 4038.40＝COMEX 12 月期金结算，确认为期金口径、不作主值）。"
                "WebSearch 补齐并四源交叉：伦敦金现货 4015.53（金投网 09:46，昨收 4017.03、开 4016.83、高 4019.93、低 4003.70；"
                "金价查询网 09:11 报 4013.40、中新 07:53 报 4005.97，三源聚类 4006-4016）；AU9999 取上金所延时行情 863.10"
                "（开 864.00、高 868.00、低 858.00）；中间价精确值 6.7171（中新网/中国经济网/上证报/中新经纬四源同值）；"
                "另取 SPDR 持仓 1041.653 吨（-3.991 吨）、CME 12 月加息 73.9%、油价主力合约、汇丰下调预测等。"
            ),
            "source": "neodata-financial-search + WebSearch",
        },
        {
            "num": 2, "name": "生成早报JSON", "status": "success", "duration_ms": 246000,
            "result": (
                "已写入 daily/2026-10-27.json。hero 867.2（4015.53×6.7171÷31.1035）、AU9999 863.1(+0.20%)、中间价 6.72、伦敦金 4015.5(-0.04%)；"
                "chart 30 点丢 09-27 补 10-27、events 整体 -1 并剔除滚出窗口的 09-27，同时把 10-26 的亚市快照 3994.5 回填为真实收盘 4016.8。"
                "自检经两轮修正后 0 error：①scripts/check_briefing.py 原为硬编码上一日汇率与价位 token（报 7 条假错），已改写为通用版 → 新建 BUG-016；"
                "②抓出真错 1 条（4030-4040 折算写 871-873，实际 870.3-872.5）已改正为 870-873。最终 pairs=6 全对、advice 196 字。"
            ),
        },
        {
            "num": 3, "name": "更新manifest", "status": "success", "duration_ms": 9000,
            "result": "已在 briefings 数组头部追加 {date: 2026-10-27, title: 今日金价早报, weekday: 周二}，共 67 条。",
        },
        {
            "num": 4, "name": "Git推送", "status": "success", "duration_ms": 21000,
            "result": (
                "已提交并推送早报：commit be0f50c（每日早报 2026-10-27），走 SSH 显式 URL；"
                "git rev-parse HEAD 与 git ls-remote origin refs/heads/master 均为 be0f50c9ece2570ac41d260c3afd15f04a79dcd5，比对一致。"
            ),
        },
        {
            "num": 5, "name": "发送邮件", "status": "success", "duration_ms": 140000,
            "result": (
                "已发送至 2132049351@qq.com（queued: true、email_sent: true）。ToolSearch 精确名一次命中，"
                "SendMessage 标准写法（to 传对象数组）＋body_format HTML＋skip_confirmation true 一次成功、无确认拦截。"
                "HTML 底稿落 .workbuddy/outbox/2026-10-27-morning.html（9 273 字节，较昨日 11 447 再缩 19%）。"
                "正文含金价快照 4 项、昨夜大事 4 条、趋势三档与建议、买卖时机（三档买／两档卖＋止损）、今日学一招、网站链接。"
            ),
            "outputs": [{"label": "邮件内容", "body": email_text}],
        },
    ],
    "buglog_verification": verification,
}

logpath = os.path.join(BASE, "logs", "%s-morning_briefing.json" % DATE)
json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(logpath, "a", encoding="utf-8").write("\n")

# ---------- 9) logs/manifest 头部追加 ----------
lm = os.path.join(BASE, "logs", "manifest.json")
m = json.load(open(lm, encoding="utf-8"))
if not m["logs"] or m["logs"][0].get("date") != DATE or m["logs"][0].get("type") != "morning_briefing":
    m["logs"].insert(0, {
        "date": DATE,
        "type": "morning_briefing",
        "status": "success",
        "summary": (
            "周二早报（触发 09:50／延迟约 51 分钟）五步全成功、邮件正常发送：金 4015.5(-0.04%)、AU9999 863.1(+0.20%)、"
            "中间价 6.7171(贬 9 基点)、积存金 867.2；主线「4000 收复、16 美元窄缝等决议」，昨日自 3975 反弹收 4016.97(+0.48%)，"
            "今日仅 4003-4020 震荡；油价连跌两日（WTI 101.25／布伦特 110.15）是唯一支撑，12 月加息仍 73.9%-80%；"
            "短 0/中 -1/长 1、watch；新增 BUG-016（自检脚本硬编码）已修复。"
        ),
    })
json.dump(m, open(lm, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(lm, "a", encoding="utf-8").write("\n")

print("log written:", logpath)
print("logs count:", len(m["logs"]))
print(json.dumps(verification["files"], ensure_ascii=False, indent=1))
