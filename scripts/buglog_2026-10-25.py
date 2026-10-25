# -*- coding: utf-8 -*-
"""写入 2026-10-25 期 buglog 条目（BUG-003/006/012/013）并更新 index.md。"""
import io, os, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(BASE, ".buglog", "bugs")

entries = {
    "2026-09-08-briefing-scheduler-missed-days.md": """
- **2026-10-25（周日）延迟约 100 分钟**：会话起始 10:40:23（`<current_time>` 实测），首次命令 `date` 实测 10:40:32，全部步骤结束约 10:47。序列续记至 9/13-10/25 共 43 个日历日：…/152/约 24/约 39/约 46/约 100，回到区间中高位（4-152 分钟极宽摆动内），未刷新上界但已高于前三日（39/46/100）。10/19-10/25 连续七个自然日、五个交易日全部产出，无缺跑、无提前触发。第 ⑦ 条 in_progress 占位兜底本期未启用（会话单段连续完成），如实记为执行偏离。**归档勘误**：本期核查发现 10-23、10-24 两期的 BUG-003 延迟条目被误追加进 `2026-09-05-briefing-scheduler-missed-days.md`（该文件 frontmatter 为 `id: BUG-002`，主题亦为调度器缺陷），本条目起回归本文件；两处历史条目内容本身无误、仅归档位置错位，故不追改历史文件，只在此留痕，后续一律写入本文件。
""",
    "2026-09-14-inspection-email-connector-down.md": """
- **2026-10-25（周日）恢复正常（第 11 次观察）**：ToolSearch 以精确名 `mcp__qq-mail__SendMessage` 一次命中（昨日 10/24 为「三组精确名＋两组关键词全部零命中」形态），`mcp__qq-mail__GetMe` 返回 scopes 含 `mail:send`、日配额 2000，随后 `SendMessage` 用标准写法（`to` 传对象数组）＋`body_format: HTML`＋`skip_confirmation: true` 一次成功、返回 `queued: true`，`email_sent: true`。形态序列 …→未注册(10/22)→正常(10/23)→未注册(10/24)→正常(10/25)，隔日抖动第四次出现。本日成功不构成修复证据（10/16-10/18 三日正常后第 4 日即复发已证伪，10/21-10/22 连续两日失效后 10/23 即恢复），severity 维持 major。
""",
    "2026-09-25-inspection-scheduler-silent-miss.md": """
- **2026-10-25（周日）四维体检**：`inspection_noon` 与 `inspection_pm` 最近产出均为 **10/23**（双线同日 `no_action`），10/24（周六）两线零产出（`ls logs/ | grep -c 2026-10-24-inspection` ＝ 0），但 10/24 为周末非交易日，按既有口径**不计入「连续零产出交易日数」**，该数回落为 **0**（10/23 双线均有产出）。当日 10/25（周日）亦为非交易日，14:00／22:00 未到不计异常。布尔判据 `today_has_any_inspection_output` 不适用（未到点）。观察期自 10/15 起第 10 日，仍在 2 周窗口内；连续数 0 < 3，未达复合判据 → 不升级不降级。形态记录：10/23 双线同日按时落盘属「双线同步正常」，与「一起缺跑」「一起提前」「夜间合并触发」「单线提前」四种镜像形态并列，仍不能视为修复。
""",
    "2026-09-26-buglog-hook-misfire.md": """
- **2026-10-25 第二十七次连续命中**（9/26-10/25，除缺跑日外每个自动化会话均触发），hook 再次透传自动化任务提示词全文（以「你是金价早报自动化助手」开头、含「第一步/第二步」流程编号）→ 判为误判、未按字面建档，改为人工盘点本期真实异常（延迟约 100 分钟、邮件恢复正常、巡检双线停在校验窗口）并逐条留痕。附带误报本期形态：`scripts/build_2026-10-25.py` 被编辑 3 次（advice 205→205→197 字两次压缩、去除 `**` 加粗标记）被弱提示为在修 bug，实为自检返工；`scripts/mail_2026-10-25.py` 生成的 20 420 字节底稿改用 12 045 字节紧凑版重写（避免超长 HTML 直传）亦被弱提示。本期工具调用零失败、零报错、零用户纠正。双重复核已执行（逐文件 `grep -c` 计数 ＋ 四文件字节数/SHA-1 写入 `logs/2026-10-25-morning_briefing.json` 的 `buglog_verification`），index 与 bugs/ 已同步。
""",
}

for fn, text in entries.items():
    p = os.path.join(B, fn)
    with io.open(p, "a", encoding="utf-8") as f:
        f.write(text)
    print("appended", fn)

# index.md 追加观察更新表
idx = os.path.join(BASE, ".buglog", "index.md")
block = """
## 2026-10-25（周日）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 100 分钟（会话起始 10:40:23、首次 `date` 10:40:32 实测），序列 43 个日历日 …/约 39/约 46/约 100，回到区间中高位，仍属「4-152 分钟极宽摆动」；10/19-10/25 连续七个自然日、五个交易日无缺跑、无提前 |
| BUG-006 | **恢复正常（第 11 次观察）**：ToolSearch 精确名一次命中、`GetMe` 确认 `mail:send` 与配额 2000，`SendMessage` 标准写法返回 `queued: true`、`email_sent: true`；形态序列 未注册(10/24)→正常(10/25)，隔日抖动第四次，不构成修复证据 |
| BUG-012 | `inspection_noon`/`inspection_pm` 最近产出均为 10/23（双线同日 no_action）；10/24 为周六、`grep -c 2026-10-24-inspection` ＝ 0，按非交易日不计阈值，**连续零产出交易日数 0**，未达复合判据；观察期自 10/15 起第 10 日 |
| BUG-013 | 第 27 次连续命中，判误判跳过建档；附带误报为 build 脚本 advice 两次压缩＋去 `**` 标记、mail 底稿由 20 420 字节改 12 045 字节紧凑版；双重复核已执行 |
"""
with io.open(idx, "a", encoding="utf-8") as f:
    f.write(block)
print("index updated")

# 统计与哈希凭据
for fn in entries:
    p = os.path.join(B, fn)
    n = subprocess.run(["grep", "-c", "2026-10-25", p], capture_output=True, text=True)
    size = os.path.getsize(p)
    sha = subprocess.run(["sha1sum", p], capture_output=True, text=True).stdout.split()[0]
    print("%s hits=%s bytes=%d sha1=%s" % (fn, n.stdout.strip(), size, sha))
