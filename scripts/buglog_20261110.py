# -*- coding: utf-8 -*-
"""追加 2026-11-10 早报期观测到 4 个长期 bug 文件。"""
import io, sys, hashlib, os
sys.stdout.reconfigure(encoding="utf-8")

D = "2026-11-10"
H = "## " + D + "（周二）早报期观测"

b003 = """
""" + H + """
- 触发时刻 **11:48:36**（会话内首个 `date` 实测），相对标称 09:00 **延迟约 168 分钟**。
  序列续记至 9/13-11/10，落在 10/21 的 152 分钟与 11/08 的 170 分钟之间，**未刷新上界**，
  定性仍为「4-170 分钟极宽摆动」。这是近 5 期内第 3 次超过 100 分钟（11/07 130、11/08 170、11/10 168），
  「高位段聚集」现象再添一例，但仍不足以判定趋势性恶化。
- 延迟危害本期为 **1 档（幅度被改变、不涉方向）**：09:00 前后金价约 4138-4140、11:48 读数为 4110.25，
  早 3 小时取数会把今日记成「基本平盘」，实际是 -0.74% 的回落。
- **本期必须执行「昨晨快照 vs 真实收盘」修法**：11-09 早报的 4120.95 为 09:48 快照，当日实际收 4140.94，
  差 **20.0 美元 ≈ 4.3 元/克**。四步已全部执行：媒体取真实收盘、hero `note` 单列该原因、
  图表 11-09 点由 4120.9 回填 4140.9、`prices[3].source` 与 `chart.source` 各写修正句。此为「跨日传染」第三次。
- 幂等检查前置：`daily/2026-11-10.json` 不存在、`logs/manifest.json` 头部为当日 `inspection_pm`、
  `git log -1` 为「日志：巡检 2026-11-10 晚间」→ 无早报残留（BUG-014 未复现）。
  注意本期顺序反常：**22:00 的晚间巡检先在 11:40 提前触发、早报反而后到**，与 BUG-012 的「提前触发」形态叠加。
"""

b006 = """
""" + H + """
- **未复现，连续正常第 2 日**（11-08 复发后重新计数）。`GetMe` 一次成功（alias 主地址、scope 含 mail:send、
  日配额 2000），`SendMessage` 按标准写法（`to` 传对象数组）＋`body_format:HTML`＋`skip_confirmation:true` 一次返回 queued:true，
  `ListMessages(dir=sent)` 于 **11:52:50 CST** 确认落地（`msg_AEPpZ_1STNcA55caGGYmSZ4356WNnAhc96cXvcIkZmhECQ`）。
- 「精确名检索」（ToolSearch 传 `tool_names`）第 9 次验证通过，仍未出现关键词检索假阴性。
- 依历史规律（10/16-10/18 曾连续 3 日正常、第 4 日即复发），两日正常不构成修复证据，观察期继续。
"""

b012 = """
""" + H + """
- **新增形态：同日内「巡检先、早报后」的倒序触发**。`logs/2026-11-10-inspection_pm.json` 于 11:40 落盘
  （标称 22:00，提前约 10 小时 20 分），早报直到 11:48 才启动——两条线不再是镜像同步，而是「巡检抢占早报时点」。
- `inspection_noon` 最近产出停在 11-09（14:15 落盘）；11-10 的 14:00 未到，不计异常。
- 按复合判据（连续 ≥5 日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出）：当前连续零产出交易日数 0，不升级不降级。
"""

b013 = """
""" + H + """
- **第二十五次连续命中**（9/26 起），hook 再次透传自动化提示词全文 → 判误判、未按字面建档。
- 附带弱提示本期两次：`build_20261110.py` 被 Edit 3 次（实为 `trend.advice` 237→214→191 字自检返工，
  属生成前自纠）、`manifest_20261110.py` 被 Edit 2 次（实为把写死的 status 改成 argv 入参）——均忽略。
- 双重复核本期已执行：逐文件 `grep -c "2026-11-10"` 计数与四文件字节数/SHA-1 写入
  `logs/2026-11-10-morning_briefing.json` 的 `buglog_verification`；index.md 计数维持 Open 12 / Fixed 12 / Total 24（本期无新增、无状态变更）。
"""

files = {
    ".buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md": b003,
    ".buglog/bugs/2026-09-14-inspection-email-connector-down.md": b006,
    ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md": b012,
    ".buglog/bugs/2026-09-26-buglog-hook-misfire.md": b013,
}

for p, block in files.items():
    with io.open(p, "a", encoding="utf-8") as f:
        f.write(block)
    print("appended", p)
