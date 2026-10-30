# -*- coding: utf-8 -*-
"""2026-10-29 早报 buglog 追加"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGS = os.path.join(BASE, '.buglog', 'bugs')

def append(fn, text):
    p = os.path.join(BUGS, fn)
    s = io.open(p, encoding='utf-8').read()
    if '2026-10-29' in s:
        print('SKIP (already)', fn); return
    if not s.endswith('\n'):
        s += '\n'
    s += '\n' + text + '\n'
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print('APPENDED', fn, len(text))

append('2026-09-08-briefing-scheduler-missed-days.md',
"""- **2026-10-29（周四）延迟约 20 分钟**：触发时刻 09:20:04（`<current_time>` 实测），首次命令 `date` 实测 09:24:53，全部步骤结束约 09:26。距标称 09:00 延迟 20 分钟，落在「4-275 分钟极宽摆动」的低位段，为本月以来第二低位（仅次于 10/02 的 4 分钟），较 10/28 的 275 分钟大幅回落。序列续记至 9/13-10/29 共 47 个日历日：…/约 51/**275**/**约 20**。10/19-10/29 连续十一个自然日、九个交易日全部产出，无缺跑、无提前触发。影响面：20 分钟延迟使伦敦金读数落在 09:14:55 的亚市早盘 4054.09，当日刚走出开 4066.60／高 4068.88／低 4036.14 的约 33 美元区间，方向（-0.33%）未被延迟扭曲，属可接受范围；但需注意前一日 10/28 曾出现 275 分钟量级，摆动幅度并无收敛迹象 → **建议 ②（定时提前至 07:00-07:30）继续维持，且宿主侧仍应核查该 9:00 定时器的投递链路**。第 ⑦ 条 in_progress 占位兜底本期未启用（会话单段连续完成、无中断），如实记为执行偏离。幂等检查前置：`daily/2026-10-29.json` 不存在、`logs/manifest.json` 头部无当日 morning_briefing 记录、`git log` 无当日早报提交 → 无中断残留（BUG-014 未复现）。前置缺口检查：上次早报 10/28（周三，success，邮件于 13:47 补发成功），10/29 为其后第一个交易日，其间无缺失交易日 → 无断档。""")

append('2026-09-14-inspection-email-connector-down.md',
"""- **2026-10-29 正常（第 14 次观察）**：`ToolSearch` 以精确名 `mcp__qq-mail__SendMessage`／`GetMe` 一次命中，`SendMessage` 标准写法（`to` 传对象数组、`body_format: HTML`、`skip_confirmation: true`）直发返回 `queued: true`，未触发 42801 confirmation_token 往返；`email_sent: true`。形态序列：正常(10/25)→正常(10/26)→正常(10/27)→复发-未注册(10/28)→**正常(10/29)**。10/28 的复发再次印证「正常窗口 ≤3 日不构成改善证据」的升级判据（10/25-10/27 连续三日正常，第 4 日即复发）；本期恢复为单日正常，连续性归零重新计数，**距「连续 ≥5 日正常」的疑似修复门槛仍有 4 日**。另记：10/28 已把本 bug 定性修正为「OAuth 过期 → status=auth-required → 连接器 MCP 工具整体不进 deferred tools 索引」，本期 `connector-status` 显示 qq-mail 为 connected，与定性一致。""")

append('2026-09-25-inspection-scheduler-silent-miss.md',
"""- **2026-10-29 四维体检：两条线最近产出均为 10/28，连续零产出交易日数 0，未达复合判据 → 不升级不降级**。`inspection_noon` 最近产出 10/28（实际 14:05，较标称 14:00 延迟约 5 分钟）、`inspection_pm` 最近产出 10/28（实际 22:00，准点触发，`no_action`，自述伦敦金 4049.93、日内振幅约 1.06% 低于 1.5% 阈值）；`ls logs/ | grep -c 2026-10-28-inspection` ＝ 2，两条线同日双产出。10/29 的 14:00／22:00 均未到点，不计异常。布尔判据 `today_has_any_inspection_output`：10/28 = true。观察期自 10/15 起算仍在 2 周窗口末段（10/29 为第 11 个交易日），当前无新的连续零产出段，复合判据第二项（恢复后 2 周内再现连续 ≥3 日零产出）未被触发。""")

append('2026-09-26-buglog-hook-misfire.md',
"""- **2026-10-29 第三十一次连续命中（9/26-10/29）**：hook 再次把自动化任务提示词全文（以「你是金价早报自动化助手」开头、含第一步至第七步流程编号）透传为「用户报告的 bug」，判为 BUG-013 误判，未按字面建档，改为人工盘点本期真实异常（仅 BUG-003 延迟 20 分钟属常态摆动、BUG-006 恢复正常）后逐条留痕。附带误报本期形态：①`scripts/build_20261029.py` 被编辑 2 次 → 弱提示「正在修 bug」，实为 `prices[2].value` 由 float 改字符串（自检脚本 `check_briefing.py` 对 float 调 `.split()` 抛 TypeError）与汇率精度 4 位改 2 位（自检规则要求），属正常修改非缺陷修复；②`scripts/mail_20261029.py` 被编辑 2 次 → 弱提示，实为把新闻块拆行以便回读全文（Read 单行截断）时误插裸换行导致 `SyntaxError: unterminated string literal`，随即修正，属工具链适配非产品缺陷。双重复核已执行：逐文件 `grep -c "2026-10-29"` 计数与字节数／SHA-1 写入 `logs/2026-10-29-morning_briefing.json` 的 `buglog_verification`。""")
