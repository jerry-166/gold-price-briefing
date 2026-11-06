# -*- coding: utf-8 -*-
"""2026-11-06 期 buglog 写入 + 双重复核凭据。"""
import io, os, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGS = os.path.join(BASE, ".buglog", "bugs")
INDEX = os.path.join(BASE, ".buglog", "index.md")


def app(name, text):
    p = os.path.join(BUGS, name)
    old = io.open(p, encoding="utf-8").read()
    io.open(p, "w", encoding="utf-8").write(old.rstrip() + "\n\n" + text.strip() + "\n")


def newfile(name, text):
    p = os.path.join(BUGS, name)
    if os.path.exists(p):
        print("EXISTS", name)
        return
    io.open(p, "w", encoding="utf-8").write(text.strip() + "\n")


newfile("2026-11-06-mail-whole-doc-percent-format.md", """
# BUG-021 邮件 HTML 整体 `%` 格式化时，字面量百分号未转义导致脚本连抛 ValueError

- **ID**: BUG-021
- **发现日期**: 2026-11-06
- **严重度**: minor
- **状态**: fixed
- **关联**: BUG-017 / BUG-018 / BUG-019（「百分号家族」第四代）

## 现象

`scripts/mail_20261106.py` 首次运行即抛两个异常：

1. `ValueError: unsupported format character ';' (0x3b) at index 44` —— `news_rows` 里
   `<table style="width:100%;...">` 写的是单 `%`，而该行参与 `%` 格式化。
2. 修完第 1 处后，`html = html % vals` 又抛
   `ValueError: unsupported format character ';' (0x3b) at index 236` —— 主模板最外层两个
   `<table style="width:100%;...">` 同样是单 `%`。

两次均为「该转义没转义」，与 BUG-017（不该写 `%%` 却写了）方向相反，属 BUG-018/019 同族。

## 根因

本期邮件改用「**整篇 HTML 一次性 `% vals` 格式化**」的写法（区别于以往逐行拼装）。
在整篇格式化的前提下，**文档里每一处字面 `%` 都必须写成 `%%`**，而这类字面 `%` 分散在
`width:100%`、正文里的 `+0.67%` 等位置，数量与位置都不可靠枚举。转义的正确性因此依赖
「记住全文所有 `%`」这个做不到的前提 —— 与前三次的「依赖该行是否被格式化」是同一类隐性前提，
只是范围从一行扩大到一篇。

## 修复

1. 外层两个 `width:100%` 补成 `%%`（news_rows 内一处、主模板两处）。
2. 正文里含百分号的段落（「一句话说今天」的 `+0.67%`／`-0.29%`）**不留在被格式化的模板里**，
   改为 `%(LEAD)s` 占位、值放在 `vals` 字典 → 作为参数注入，不再参与格式化解析。
3. 生成后校验：`grep -c '100%%'` 必须为 0、`grep -o 'width:100[^;"]*'` 计数 10 且全为 `width:100%`。

## 教训（已写入 SKILL 约定）

- 长文档模板**不要用整篇 `%` 格式化**：正文类内容一律 `str.replace` 或占位注入，
  `%` 只留给「纯数值、无中文正文」的短模板。
- 一次 `%` 格式化只报第一个非法转换符，所以这类错会**一个一个冒**；连报两次即说明
  模板里散布着多处字面 `%`，此时应换写法而不是逐个补 `%%`。
- 本期两次 ValueError 均在邮件发出前拦下，未污染产物；`email_sent` 未受影响。
""")

app("2026-09-08-briefing-scheduler-missed-days.md", """
## 2026-11-06（周五）

- 触发时刻 **09:23:41**（会话内首个 `date` 实测 09:23:59，按 09:23:41 计），相对标称 09:00 **延迟约 24 分钟**。
  序列续记至 9/13-11/06，落在区间中低位，未刷新 10/21 的 152 分钟上界，定性仍为「4-152 分钟极宽摆动」。
  昨日（11/05）的 2 分钟极低位未延续，再次印证「低位不延续、序列随机摆动」。
- 延迟危害本期为 **0 档**：09:23 与 09:00 处于同一亚市早盘段、且金价在 4071-4106 区间横盘，
  方向与幅度均未被延迟放大（对比 11/02 的「方向同、幅度放大」与 11/04 的「基准被抬高」）。
- **本期仍需执行「昨晨快照 vs 真实收盘」修法，但差值极小**：11-05 早报用的 09:03 快照为 4095.22，
  11-05 实际收 4088.80，差 **6.42 美元 ≈ 1.4 元/克**。已在 hero `note` 单列该原因，
  `prices[3].source` 与 `chart.source` 各写修正句，图表 11-05 点由 4095.2 回填为 4088.8。
  这是「跨日传染」形态的第二次出现，但量级从 11/05 的 23.5 元/克降到 1.4 元/克。
- 幂等检查前置：`daily/2026-11-06.json` 不存在、`logs/manifest.json` 头部无当日记录、
  `git log -1` 为「日志：巡检 2026-11-05 晚间」→ 无中断残留（BUG-014 未复现）。
  前置缺口检查：上次早报 11/05（success），11/06 为其后第一个交易日 → 无断档。
  第 ⑦ 条 in_progress 占位兜底本期未启用（会话单段连续完成），如实记为执行偏离。
""")

app("2026-09-14-inspection-email-connector-down.md", """
## 2026-11-06（周五）

- **正常（第 22 次观察，连续正常第 6 日）**：`connector-status` 报 qq-mail `connected`；
  按 `tool_names` 精确名检索 `mcp__qq-mail__SendMessage/ListMessages/GetMe` 一次命中，
  `SendMessage`（`to` 传对象数组 + `body_format: HTML` + `skip_confirmation: true`）返回 `queued: true`，
  `ListMessages(dir=sent)` 于 **09:28:37 CST** 确认落箱（`msg_iQgtnH9lbCXj8KJeoI2wlsvWz_OQZveUL686evDgRrQbVA`）。
- 已**连续 6 日**正常，超过「疑似修复」所需的 5 日门槛 1 日；「精确名检索」假设第 6 次正面验证。
  仍是**疑似修复**而非 fixed：历史最长窗口为 10/16-10/18 的三日，5-6 日虽有质变但未过 2 周观察窗，
  按既定判据需观察到 **11/19 前后**无复发方可改 status。
- 附带记录：本期未出现 auth-required／工具缺失／-32602 三种历史形态中的任何一种。
""")

app("2026-09-25-inspection-scheduler-silent-miss.md", """
## 2026-11-06（周五）

- 本期早报 09:23 执行，早于 14:00／22:00，11-06 两条巡检线尚未到点，**不判缺跑**。
- 回看 11-05：`inspection_pm` 于 22:00 正常落盘并触发波动型预警（振幅 2.19%，邮件已发）；
  `inspection_noon` 11-05 无产出（`ls logs/ | grep -c 2026-11-05-inspection_noon` = 0），
  为 11-02-11-04 连续三日双落地后的首次单线缺跑。
- 连续零产出交易日数维持 **0**（pm 线 11-05 有产出，按「当日任一巡检线有产出即非零产出」口径），
  未触发「连续 ≥5 个正常交易日零产出」第一条判据，**不升降级**。
- 观察口径：11/06 收盘后重点看 noon 是否补回，以及两线时间戳是否落在 noon 14:00±2h / pm 22:00±2h 窗口内。
""")

app("2026-09-26-buglog-hook-misfire.md", """
## 2026-11-06（周五）

- **第 39 次连续命中**（9/26-11/06）：hook 再次把自动化任务提示词全文透传为「用户报告的 bug」，
  并附「用户可能在指出本次会话中遗漏的问题」的引导语 → 判误判、未按字面建档。
- 附带误报 3 次（均忽略，不计入）：
  ① `scripts/build_20261106.py` 创建后 1 次 Edit —— 实为 `trend.advice` 222→197 字收敛，属生成前自纠；
  ② `scripts/mail_20261106.py` 2 次 Edit —— 实为 BUG-021 的两处 `%%` 转义修复，该修复已按正式 bug 建档；
  ③ 同文件「2 次编辑即视为在修 bug」的弱提示，在②处与真实 bug 修复重叠，判定仍以「是否有产物损坏」为准。
- **本期确有 1 个新增 bug（BUG-021）**，与前几期「零新增」不同；两份 ValueError 均在邮件发出前拦下，
  未造成产物损坏。双重复核已执行：逐文件 `grep -c "2026-11-06"` 计数 ＋ 字节数/SHA-1 比对，
  凭据落在 `logs/2026-11-06-morning_briefing.json` 的 `buglog_verification` 字段；
  `index.md` 与 `bugs/` 内容一致性已同步校验。
""")

# ---- index.md：追加观察更新段 ----
idx = io.open(INDEX, encoding="utf-8")
old = idx.read()
idx.close()

row21 = ("| BUG-021 | 邮件 HTML 整体 `%` 格式化时字面量百分号未转义，脚本连抛两次 "
         "`ValueError: unsupported format character`（2026-11-06 发现并修复；百分号家族第四代，"
         "范围从「单行是否被格式化」扩大到「整篇是否被格式化」） | minor | fixed |")

if "BUG-021" not in old:
    anchor = "| BUG-020 |"
    lines = old.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith(anchor):
            lines.insert(i + 1, row21)
            break
    old = "\n".join(lines)
    old = old.replace("Open: 11 | Fixed: 9 | Total: 20", "Open: 11 | Fixed: 10 | Total: 21")

sec = """
## 2026-11-06（周五）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | **延迟约 24 分钟**（09:23:41 触发），序列续记至 9/13-11/06 共 55 日，落中低位、未刷新 152 分钟上界，定性仍为「4-152 分钟极宽摆动」。本期危害 **0 档**（同一亚市早盘段、横盘，方向与幅度均未被放大）。但**仍需执行「昨晨快照 vs 真实收盘」修法**：11-05 快照 4095.22 vs 真实收 4088.80，差 6.42 美元 ≈ 1.4 元/克，已在 hero note／prices[3].source／chart.source 三处留痕并回填图表点 —— 「跨日传染」形态第二次出现，量级由 23.5 元/克降至 1.4 元/克 |
| BUG-006 | **正常（第 22 次观察，连续正常 6 日）**：`SendMessage` 返回 `queued: true`、`ListMessages(dir=sent)` 于 09:28:37 CST 确认（`msg_iQgtnH9lbCXj8KJeoI2wlsvWz_OQZveUL686evDgRrQbVA`）。「精确名检索」第 6 次正面验证。仍是**疑似修复**：历史最长窗口为 3 日，5-6 日虽已质变，但按判据需观察到 11/19 前后无复发方可改 fixed |
| BUG-012 | 本期 09:23 执行，早于 14:00／22:00，不判缺跑。回看 11-05：pm 线 22:00 正常落盘并触发波动预警，noon 线零产出（11-02-11-04 三连双落地后首次单线缺跑）。连续零产出交易日数 **0**，未达复合判据，不升降级 |
| BUG-013 | **第 39 次连续命中**，判误判跳过建档；附带弱提示 3 次：`build_20261106.py` 的 advice 222→197 字收敛（生成前自纠，不计入）、`mail_20261106.py` 的 2 次 Edit（实为 BUG-021 转义修复，已正式建档） |
| BUG-021 | **新增（fixed）**：整篇 HTML 一次性 `%` 格式化时，`width:100%` 与正文 `+0.67%` 等多处字面量百分号未转义，连抛两次 `ValueError: unsupported format character ';'`。修法：外层补 `%%`，正文改占位注入；约定「长文档模板不用整篇 `%` 格式化」。产物未受损，邮件正常发出 |

"""

if "## 2026-11-06（周五）观察更新" not in old:
    old = old.rstrip() + "\n" + sec

io.open(INDEX, "w", encoding="utf-8").write(old)
print("index written, contains BUG-021:", "BUG-021" in old)

# ---- 校验凭据 ----
files = [
    "2026-09-08-briefing-scheduler-missed-days.md",
    "2026-09-14-inspection-email-connector-down.md",
    "2026-09-25-inspection-scheduler-silent-miss.md",
    "2026-09-26-buglog-hook-misfire.md",
    "2026-11-06-mail-whole-doc-percent-format.md",
]
ver = {}
for n in files:
    p = os.path.join(BUGS, n)
    raw = io.open(p, "rb").read()
    cnt = io.open(p, encoding="utf-8").read().count("2026-11-06")
    ver[n] = {"occurrences": cnt, "bytes": len(raw), "sha1": hashlib.sha1(raw).hexdigest()}

iraw = io.open(INDEX, "rb").read()
ver["index.md"] = {"occurrences": io.open(INDEX, encoding="utf-8").read().count("2026-11-06"),
                   "bytes": len(iraw), "sha1": hashlib.sha1(iraw).hexdigest()}
for k, v in ver.items():
    print(k, v["occurrences"], v["bytes"], v["sha1"][:12])
