# -*- coding: utf-8 -*-
"""向 .buglog/index.md 追加 2026-11-17 观察更新（带幂等守卫）"""
import io, os, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, '.buglog', 'index.md')
MARK = '## 2026-11-17（周二）观察更新'

txt = io.open(P, encoding='utf-8').read()
if MARK in txt:
    print('SKIP: 已存在当日小节，幂等守卫生效')
else:
    sec = []
    sec.append('')
    sec.append(MARK)
    sec.append('')
    sec.append('| ID | 本期结论 |')
    sec.append('|---|---|')
    sec.append('| BUG-003 | 延迟约 **257 分钟**（首条 `date` 实测 13:17:32，标称 09:00），'
               '介于 11-15 的 700 与 11-10 的 168 之间、未刷新 10/31 的 747 分钟上界；近 7 期第 5 次破 100 分钟。'
               '**危害 1 档，命中 11-16 新增的第三条判据「延迟区间是否覆盖当日关键价格窗口」**：09:00 时伦敦金约 3855'
               '（对昨收 3856.24 约 -0.03%，方向接近持平），13:17 已反弹到 3875.12（+0.49%）——'
               '**方向由「持平／微跌」翻为「上涨」，约 20 美元的日内反弹全部发生在延迟窗口内**；'
               '本期仍是「跨日传染第七次」：11-16 快照 3874.63 → 真实收盘 3856.24，差 18.39 美元≈4.0 元/克'
               '（序列 108.6／104.42／77.6／59.16／30.05／18.39，量级继续收敛） |')
    sec.append('| BUG-006 | **复发（11/16 成功后新序列第 1 日失败）**，`email_sent: false`、整期 partial。'
               '证据组合与 11-15 完全一致、第 3 种形态再次复现：①`ToolSearch` 精确名检索 `mcp__qq-mail__SendMessage/GetMe/ListMessages` '
               '全部回落 agent-mail 命名空间；②关键词检索同样只命中 agent-mail；'
               '③`list_installed_plugins` 显示 `qq-mail` connected/bound/enabled 三真；'
               '④备用 `mcp__agent-mail__GetMe` 返回 `not_bound`；'
               '⑤`reconnect_plugin` 返回 `User refused`（无人值守无人确认）。'
               '**「三真 + 精确名检索回落」第 3 次复现，「reconnect 在无人值守下不可用」第 2 次复现**，'
               'HTML 落 `.workbuddy/outbox/mail-2026-11-17.html`（13 879 字符／19 605 字节／70 行／maxline 929）待人工补发。'
               'severity 维持 major，不因单日成功而改状态 |')
    sec.append('| BUG-012 | 早报 13:17 执行，**已过 noon 标称 14:00 之前、未到 pm 时点** → 当日两条线均未到点，不判缺跑。'
               '回看体检：`inspection_noon` 最近产出 2026-11-16（no_action）、`inspection_pm` 最近产出 2026-11-16（partial，波动预警）；'
               '11-14／11-15 为周末零产出，按「周末巡检非必跑」不计入分母。连续零产出交易日数 = 0，未达复合判据 → 不升级不降级 |')
    sec.append('| BUG-013 | **第 30 次连续命中**，hook 再次透传自动化提示词全文 → 判误判、未按字面建档。'
               '附带弱提示：`scripts/build_20261117.py` 一次成稿后仅因 advice 字数边界（200 字）复核过一次，'
               '`mail_20261117.py` 一次通过 `maxline`/`%%` 门禁 → 属正常自检，不计入修复。'
               '**本期确有真实故障（BUG-006 复发），按「真实失败优先」正常建档，未因 hook 误判而漏记** |')
    sec.append('')
    sec.append('### 本期 buglog 复核凭据（2026-11-17）')
    sec.append('')
    sec.append('- 本期为 **index-only 更新**（无新增 bug、无状态变更），逐日观察直接记入本文件，不与 `bugs/` 产生分歧；'
               '计数取自本文件表头：**Open 12 / Fixed 13 / Total 25** 维持不变')
    sec.append('- 字节数与 SHA-1 见 `logs/2026-11-17-morning_briefing.json` 的 `buglog_verification`'
               '（**在全部写入动作之后测量**——11-14 期固化口径）')
    sec.append('- 幂等守卫：脚本先检测当日小节标题是否已存在，存在即 SKIP；11-13 期 BUG-025 的教训已内置')
    sec.append('')
    txt = txt.rstrip(chr(10)) + chr(10) + chr(10) + chr(10).join(sec)
    io.open(P, 'w', encoding='utf-8').write(txt)
    print('APPENDED')

io.open(P, 'w', encoding='utf-8').write(txt if txt.endswith(chr(10)) else txt + chr(10))
b = io.open(P, 'rb').read()
print('bytes', len(b))
print('sha1', hashlib.sha1(b).hexdigest())
print('grep date count', b.decode('utf-8').count('2026-11-17'), 'lines', b.decode('utf-8').count('2026-11-17' + chr(10)))
