import io, os

APP = {}

APP['.buglog/bugs/2026-09-05-briefing-scheduler-missed-days.md'] = """
- **2026-10-24（周六）延迟约 46 分钟**：会话起始 09:45:44（`<current_time>` 实测），首次命令 09:46:00 `date` 实测，全部步骤结束 09:51:40 实测。序列续记至 9/13-10/24 共 41 个日历日：…/152/约 24/约 39/约 46，仍落在 4-152 分钟区间中低位，未刷新上界。10/19-10/24 连续六个自然日、五个交易日全部产出，无缺跑、无提前触发。第 ⑦ 条 in_progress 占位兜底本期未启用（会话单段连续完成），如实记为执行偏离。
"""

APP['.buglog/bugs/2026-09-14-inspection-email-connector-down.md'] = """
- **2026-10-24（周六）第十次复发，形态回到「工具未注册」**：`connector-status` 显示 qq-mail 为 connected、agent-mail 为 connected，但会话工具索引中**不存在任何 `mcp__qq-mail__*` 工具**——①以精确名 `mcp__qq-mail__SendMessage` / `mcp__qq-mail__send_mail` / `mcp__qq-mail__SendMail` 三选一检索，只命中 `mcp__agent-mail__SendMessage`；②以关键词「发送邮件 收件人 主题 正文 HTML」「QQ邮箱 SMTP 发信」检索，只返回 agent-mail 的 GetMessage/ReplyMessage 与无关工具，零 qq-mail 候选。`mcp__agent-mail__GetMe` 返回 `Agent 邮箱尚未开通`、`status: not_bound` → 双通道同时失效，无降级路径。`email_sent: false`、status partial，完整 HTML 落 `.workbuddy/outbox/2026-10-24-morning.html`（14 445 字节）＋主题文本，待人工补发。
- **形态序列更新（10/6 起）**：未注册(10/6)→未注册(10/10)→正常(10/12)→正常(10/13)→未注册(10/14)→-32602(10/15)→正常(10/16-10/18)→未注册(10/19)→正常(10/20)→未注册(10/21-10/22)→正常(10/23)→**未注册(10/24)**。10/23 的单日成功次日即告失效，再次印证「单日/连续三日正常都不构成修复证据」；本次同时是「未注册」形态第 7 次出现，「正常↔未注册」的隔日抖动已连续出现三次（10/19-10/20、10/21-10/22-10/23、10/23-10/24）。
- **severity 维持 major**：本 bug 已连续影响主线 10 次，且从未出现「连续 5 个交易日正常」的最长窗口新纪录（现纪录仍为 10/16-10/18 的连续三次）；建议宿主侧优先排查 deferred tools 索引装载层为何间歇性丢失 qq-mail 命名空间。
"""

APP['.buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md'] = """
- **2026-10-24（周六）四维体检**：`inspection_noon` 最近产出 2026-10-23（`no_action`）、`inspection_pm` 最近产出 2026-10-23（`no_action`）——两线在 10/23 **同时恢复正常**，且均按标称时点落盘（无提前/延后证据）。10/22 两线零产出（`ls logs/ | grep -c 2026-10-22-inspection`＝0，当日为正常交易日，已如实留痕）。**连续零产出交易日数回落至 1**（仅 10/22），未达复合判据（连续 ≥5 日 且 恢复后 2 周内再现连续 ≥3 日），不升级不降级；观察期自 10/15 起算仍在 2 周窗口内（第 9 日）。
- 10/24 为周六，14:00 / 22:00 两条巡检尚未到点，不计异常。
- **镜像形态计数更新**：已观察到四种——「一起缺跑」（10/08-10/09、10/12-10/13）、「一起提前」（10/17）、「一起延后到夜间合并触发」（10/20、10/21）、「单线提前」（10/23）。10/23 两线同日同形态（均 no_action、均按时点）为少见的一次「双线正常」，仅 1 日，不作修复判据。
"""

APP['.buglog/bugs/2026-09-26-buglog-hook-misfire.md'] = """
- **2026-10-24 第二十六次连续命中**（9/26-10/24，第 41 个日历日）：hook 再次把整段自动化任务提示词（以「你是金价早报自动化助手」开头、含「第一步/第二步」流程编号）透传为「用户报告了一个 bug」，判为误判、**未按字面建档**。
- **附带误报本期形态**：①对 `scripts/_build_20261024.py` 的 2 次编辑给出「通常表示你在修复一个 bug」弱提示——实为把 plan.note 里一处编造的「4900 亿级别杠杆止损盘」改为事实性表述（属内容纠错，非 bug 修复）；②对 `scripts/_log_20261024.py` 的 2 次编辑再给同类弱提示——实为 `os.popen('date')` 在 Windows 下返回 GBK 字节导致 `UnicodeDecodeError` 后删除该行（该行输出本未被使用），属脚本自身缺陷的即时修正，已在本条留痕。
- **双重复核已执行**：(a) 逐文件 `grep -c "2026-10-24"` 计数＋字节数/SHA-1 写入 `logs/2026-10-24-morning_briefing.json` 的 `buglog_verification`；(b) 校验 `.buglog/index.md` 的结论与 `.buglog/bugs/` 实际内容一致。
"""

for path, text in APP.items():
    assert os.path.exists(path), path
    with io.open(path, 'a', encoding='utf-8') as f:
        f.write(text)
    print('appended', path, os.path.getsize(path), 'bytes')
