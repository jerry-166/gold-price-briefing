# -*- coding: utf-8 -*-
"""把 2026-11-20 观察更新追加到 .buglog/index.md（幂等），并更新表头计数。"""
import io, re, json, hashlib, os

IDX = ".buglog/index.md"
s = io.open(IDX, encoding="utf-8").read()

if "## 2026-11-20" in s:
    print("SKIP: 2026-11-20 section exists")
    raise SystemExit

section = """

## 2026-11-20（周五）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **154 分钟**（会话 `current_time` 11:32:23、首条 `date` 实测 11:32:30，标称 09:00），近 8 期序列 `…/257/90/119/154`，未刷新 10/31 的 747 分钟上界。**危害 1 档，第四次命中「延迟区间是否覆盖当日关键价格窗口」判据，且是量级最大的一次**：09:00 前后伦敦金约 3590-3597（07:40 低 3590.69、08:52 报 3591.19），11:32 已 3533.97 —— 延迟窗口内又跌约 60 美元（≈13 元/克），并**完成 3600、3550 两道整数关的击穿**；按分钟数（154）只算中高位，按窗口判据则是「错过关口破位」。跨日传染第九次：11-19 快照 3710.58 → 真实收盘 3625.01，差 85.57 美元≈18.5 元/克（序列 108.6／104.42／77.6／59.16／30.05／18.39／16.3／18.5，在收敛后再次回升，因 11-19 单日跌 2.66%） |
| BUG-006 | **正常（连续第 3 日成功，11-18→11-19→11-20）**。`ToolSearch` 精确名检索 `mcp__qq-mail__SendMessage/GetMe/ListMessages` 均一次命中、无回落 agent-mail；`GetMe` 正常返回 scope（含 mail:send）与主别名。**新观察：本期改用 `skip_confirmation: true` 直发，未再出现 42801 确认链路，一次返回 `queued:true`** —— 与 11-18/11-19「靠携 token 重试」并列，构成第二种可用的免交互发送路径。`sent` 目录回读确认 `created_at 2026-11-20T03:36:57Z`。HTML 规格 12 484 字符／17 510 字节／62 行／maxline 909，零双百分号、零 CSS `width:100%`（容器用 `width="100%"` 属性）。连续性仍不构成修复证据，severity 维持 major |
| BUG-012 | **新增第三种镜像形态的极端案例：巡检先于早报。** 今日 `logs/2026-11-20-inspection_pm.json` 于 **11:29** 落盘（`timestamp: 11:29 CST`、status partial、波动型预警），相对标称 22:00 **提前约 10.5 小时**；且该次巡检 **早于** 本期早报（11:32 触发）—— 同一调度器把「晚间巡检」排到了「早间早报」之前，顺序倒置为观察期首次。当日 `inspection_noon` 无产出、14:00 未到不判缺跑；按「当日有任一巡检产出即非零产出」口径连续零产出交易日数 = 0，未达复合判据 → 不升级不降级 |
| BUG-013 | **第 32 次连续命中**，hook 再次把自动化提示词全文透传为「bug 报告」→ 判误判、未按字面建档。附带弱提示本期 2 次：`scripts/log_20261120.py` 一次编辑（实为把文案里的双百分号改成中文表述以过产物门禁）被判为「在修 bug」；`build_20261120.py` 的 `.format` 改造属真实修复（见 BUG-028），已正常建档。**本期确有真实故障（BUG-028），按「真实失败优先」未因 hook 误判而漏记** |
| BUG-028 | **新增、fixed**：`build_20261120.py` 在**被 `%` 格式化的** `prices[0].note` 里夹带字面涨跌幅 `（−2.51%）`，首次运行即抛 `TypeError: not enough arguments for format string`（注意不是 `unsupported format character` —— 全角 `）` 被当成下一个占位符的起始）。**百分号家族第七代**，首次落在「被格式化的中文长文案字段」上。修法：该字段改用 `.format()`（`{}` 占位），从根上消除「该行是否被格式化」的隐性前提；最小正反例已实测记录。凭据：`build` 前置门禁 `raw.count('%%')==0` 两次均通过，`check_briefing.py` errors 0 / OK |

### 本期 buglog 复核凭据（2026-11-20）

- **有新增 bug**：新增 `bugs/2026-11-20-percent-literal-in-format-string.md`（BUG-028），status=fixed
- 计数取自本文件表头（写入后重读，非照抄上期）：Open 12 / Fixed 16 / Total 28（Fixed 15→16、Total 27→28 各 +1）
- 幂等守卫：`scripts/buglog_20261120.py` 先检测 `## 2026-11-20` 是否已存在，存在即 SKIP（BUG-025 教训内置）
- 完整性：`bugs/` 目录 27 → **28** 个文件；`index.md` 字节数与 SHA-1、当日串出现次数见 `logs/2026-11-20-morning_briefing.json` 的 `buglog_verification`（**在全部写入动作之后测量**）
"""

s = s.rstrip("\n") + section
s = s.replace("Open: 12 | Fixed: 15 | Total: 27", "Open: 12 | Fixed: 16 | Total: 28", 1)
io.open(IDX, "w", encoding="utf-8").write(s)
print("index updated")

# 统计凭据
files = sorted(os.listdir(".buglog/bugs"))
print("bugs files:", len(files))
rawi = io.open(IDX, "rb").read()
print("index bytes", len(rawi), "sha1", hashlib.sha1(rawi).hexdigest())
print("date occurrences", s.count("2026-11-20"))
