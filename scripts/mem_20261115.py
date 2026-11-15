# -*- coding: utf-8 -*-
"""追加 2026-11-15 期摘要到自动化记忆与项目日志（append-only）。"""
import io, os

ROOT = r"D:/workspace/每日金价资讯"
MEM_AUTO = os.path.join(ROOT, ".workbuddy/memory/automations/automation-1784188098041/memory.md")
MEM_DAY = os.path.join(ROOT, ".workbuddy/memory/2026-11-15.md")

AUTO = """

### 2026-11-15（周日）— partial（4/5，邮件未发出）
- 触发 **20:39:51**（会话 current_time 实测），延迟约 **700 分钟**——仅次于 10/31 的 747 分钟，为历史第二大值，未刷新上界。**延迟跨过整个交易日**：早报在晚间交付，标称 09:00 与交付时点相差 11.6 小时。
- 数据：伦敦金 11-13 收 **3879.92**(+2.49／+0.06%，高 3922.99、低 3867.55)，周日无新成交；AU9999 夜盘收 **837.00**（日盘 837.55、-1.62%）、T+D 836.29、沪金主力 839(-2.5%)、沪银 11985(-4.1%)；中间价 **6.7152**（周末不更新）、在岸即期 6.6707；积存金 **837.7**。旁证 COMEX 3887.6(+0.06%)、DXY 103.4 附近、10Y 5.13%-5.15%。
- 主叙事：**周末静止 + 两个底座反向**——本周累跌 190.83 美元(-4.69%)、周低 3852.48 创逾一年新低；实物端金饰四天跌 77 元（1164-1178）、上海小克重金条售罄柜台挤满人，而 SPDR 9 日减 18.53 吨、CFTC 多头 25.3→21.6 万张；CME 12 月加 25bp 84.7%／50bp 15.3%（50bp 定价一周内从 0 升到 15.3%）；62% 分析师看空下周、最悲观看 3800。趋势短 -1/中 -1/长 1、action=watch。
- **本期无跨日回填**（无新收盘），为连续第二个「零回填」周末日。hero note 明写「与昨日早报同值不是没刷新」+ 明日 11-16 夜盘归属提醒。
- commit：早报 `2fe2efd`、日志+buglog+脚本 `6a3c336`（SSH，两次 rev-parse 与 ls-remote 一致）。
- **邮件：失败（email_sent:false）— BUG-006 复发**，11/12-11/14 连续正常 3 日后中断。证据组合：精确名检索两次均回落 agent-mail、关键词检索同样、按名调用 not found、插件列表却 connected/bound/enabled 三真。**reconnect_plugin 返回 User refused（无人值守无人确认）→ 自愈路径对定时任务实际是断的**；备用 agent-mail 未开通(not_bound)。HTML 落 `.workbuddy/outbox/mail-2026-11-15.html`（11 315 字符／16 961 字节／70 行／maxline 561）待人工补发。
- 经验：
  - **BUG-003 新建议 ⑬**：延迟 >360 分钟的期次，交付物（邮件头部／`_meta.updated`）必须显式标注「延迟交付 + 真实生成时点」，否则读者会把晚间读数当晨间读数。本期已在邮件头部标「生成于 20:50、延迟约 700 分钟」。
  - **「非交易日危害恒为 0」判据第三次生效**，可作定型：危害分级先看当日是否有行情，再看分钟数。
  - **BUG-006 两条新结论**：①「connected+bound+enabled 三真 + 精确名检索回落」= 索引未装载，是第 3 种可复现证据组合；② reconnect 需人机交互，自动化时段无法自愈 → 发信通道必须与 MCP 解耦（人工前置确认或改 SMTP）。
  - **周末巡检不是必跑**：107 条巡检记录中落在周六/周日的仅 3 条（10-17 两条、11-07 一条），故 11-14 两线零产出不计入「连续零产出交易日」——这是 BUG-012 判据的一个重要分母修正。
  - advice 首稿 208 字超限、压到 196 字后 pairs 10 组一次过检（「先写 5 组价位、再按剩余空间写判断句」第 5 次生效）。
  - hook 第 48 次把自动化提示词误判为 bug 报告（BUG-013）；本期真实故障是 BUG-006 复发，按「真实失败优先」正常建档。弱提示命中 build_20261115.py 编辑 2 次（advice 压缩），属自纠不计入修复。
- buglog：BUG-003（700 分钟、危害 0 档、新形态「延迟跨整个交易日」、建议 ⑬）、BUG-006（复发、连续正常归零、两条新结论）、BUG-012（周末巡检非必跑、当日 noon 零产出属倒序形态）、BUG-013（第 48 次）四条已写入并同步 index.md；复核凭据（逐文件 grep -c 1/2/1/1、index 4；字节 9 568/59 498/60 743/65 179，index 68 910；各 SHA-1）落在 logs/2026-11-15-morning_briefing.json 的 `buglog_verification`；Open 12 / Fixed 12 / Total 24 维持。
"""

DAY = """# 2026-11-15（周日）

## 金价早报（20:39 触发，延迟约 700 分钟，partial）
- 生成 daily/2026-11-15.json（周日休市，价格与涨跌幅沿用 11-13 收盘：伦敦金 3879.9、AU9999 837.00、中间价 6.72、积存金 837.7）。
- check_briefing.py 0 error（advice 196 字、pairs 10 组）；图表丢 10-16 补 11-15，events 索引 -1。
- manifest.json briefings 头部插入 11-15（86 条）；logs 侧写 logs/2026-11-15-morning_briefing.json 与 logs/manifest.json（191 条）。
- 提交：2fe2efd（早报）、6a3c336（日志+buglog+脚本），SSH 推送并校验远端一致。
- 邮件未发：qq-mail 工具未进 deferred 索引、reconnect 被取消、agent-mail 未开通；HTML 在 .workbuddy/outbox/mail-2026-11-15.html 待人工补发。
- 脚本新增：build_20261115.py / mail_20261115.py / manifest_20261115.py / log_20261115.py / buglog_20261115.py。
"""

for path, text in ((MEM_AUTO, AUTO), (MEM_DAY, DAY)):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        s = io.open(path, encoding="utf-8").read()
    else:
        s = ""
    if "2026-11-15" in s and path == MEM_AUTO and "2026-11-15（周日）" in s:
        print("skip (already)", path)
        continue
    if path == MEM_DAY and s:
        print("skip (exists)", path)
        continue
    s = s.rstrip("\n") + "\n" + text
    io.open(path, "w", encoding="utf-8").write(s)
    print("appended", path, len(s))
