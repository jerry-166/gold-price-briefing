# -*- coding: utf-8 -*-
"""写入 2026-10-31 早报运行日志与日志清单。"""
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(BASE, 'logs', '2026-10-31-morning_briefing.json')
LM = os.path.join(BASE, 'logs', 'manifest.json')

EMAIL_BODY = (
    "主题：🌅 今日金价早报 | 2026年10月31日 周六\n"
    "收件人：2132049351@qq.com\n"
    "状态：未发送 —— 双通道均不可用（qq-mail 的 MCP 工具未进入会话工具索引；"
    "agent-mail 返回 not_bound），按 BUG-006 规则如实记 email_sent:false。\n"
    "完整 HTML 底稿：.workbuddy/outbox/2026-10-31-morning.html（15 283 字节），待人工补发。"
)

log = {
    "date": "2026-10-31",
    "type": "morning_briefing",
    "status": "partial",
    "summary": "伦敦金周五收盘 3876.69（-3.59%）跌破 3900 创一年新低、AU9999 夜盘 833.0（-2.55%）、中间价周六沿用 6.7138、积存金估 836.8；数据与推送 4 步成功，邮件双通道同时不可用。",
    "timestamp": "21:27 CST（原定 09:00，延迟约 747 分钟，为观察期最大延迟）",
    "date_note": "本期为周六休市版：伦敦金取 10 月 30 日纽约尾盘收盘、AU9999 取 10 月 30 日夜盘收盘（按交易所规则归属 11 月 2 日）、中间价沿用 10 月 30 日值、涨跌幅不作归零（汇率记 0.00）。",
    "steps": [
        {"num": 1, "name": "获取数据", "status": "success", "duration_ms": 105000,
         "result": "新浪实时接口拿到伦敦金 3876.69（昨收 4021.23、-3.59%、高 4026.24／低 3870.05）与上金所 AU9999 夜盘 833.00（昨结 854.76、-2.55%）、T+D 831.10；四轮 WebSearch 补齐周四收盘媒体聚类（3875.19／3875.55）、AU9999 日盘收盘 854.76（-1.21%）、油价（WTI 104.12／+2.08%、布伦特 117.64／+2.4%）、美股（纳指 -2.86%、费半 -7.2%、英特尔 -28.58%）、FedWatch 12 月加息 72%、金饰克价 1161-1165。中间价 6.7138 周六无新值，沿用周五。",
         "source": "neodata-financial-search 未使用（AUUSDO 为 COMEX 口径、AU9999 与中间价已由官方源覆盖）；实际取数：新浪财经 hf_XAU／gds_AU9999 实时接口 + WebSearch（中新经纬、每日经济新闻、央广网、新华财经、中国证券网、汇通财经、北京青年报）"},
        {"num": 2, "name": "生成早报JSON", "status": "success", "duration_ms": 105000,
         "result": "已写入 daily/2026-10-31.json：4 条价格、5 条新闻（均带原文 url）、trend 短 -1／中 -1／长 1、action=watch、plan 三档买入（3800-3830／3730-3760／3650-3680）＋两档止盈（3960-3990／4010-4040）、chart 30 点。图表丢 10-01 补 10-31，10-30 点由昨晨快照 4004.0 回填为真实收盘 3876.7、事件文案同步改写。check_briefing.py 一次通过（0 error、advice 196 字、11 组价位复算全中）。"},
        {"num": 3, "name": "更新manifest", "status": "success", "duration_ms": 4000,
         "result": "已追加记录到 manifest.json（briefings 头部，共 71 条）"},
        {"num": 4, "name": "Git推送", "status": "success", "duration_ms": 12000,
         "result": "已提交并推送：040c94d 每日早报 2026-10-31（c511e29..040c94d，SSH 通道）"},
        {"num": 5, "name": "发送邮件", "status": "failed", "duration_ms": 60000,
         "result": "未发送：ToolSearch 三组关键词（qq mail send email／qq／qqmail send_message）均只命中 agent-mail，mcp__qq-mail__* 未进会话工具索引；agent-mail GetMe 返回 not_bound。BUG-006 第十六次复发，双通道同时失效。",
         "outputs": [{"label": "邮件内容", "body": EMAIL_BODY}]}
    ],
    "summary_stats": {
        "total_steps": 5, "success_steps": 4, "failed_steps": 1,
        "total_duration_ms": 302000, "email_sent": False, "git_pushed": True
    },
    "buglog_verification": {
        "date_stamp": "2026-10-31",
        "per_file_grep_c": {
            ".buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md": 3,
            ".buglog/bugs/2026-09-14-inspection-email-connector-down.md": 2,
            ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md": 2,
            ".buglog/bugs/2026-09-26-buglog-hook-misfire.md": 3,
            ".buglog/index.md": 3
        },
        "bytes": {
            ".buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md": 64029,
            ".buglog/bugs/2026-09-14-inspection-email-connector-down.md": 42509,
            ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md": 51184,
            ".buglog/bugs/2026-09-26-buglog-hook-misfire.md": 51510,
            ".buglog/index.md": 32866
        },
        "sha1": {
            ".buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md": "cec9cc670469129bbcf4ee6da3e23a058ec9de02",
            ".buglog/bugs/2026-09-14-inspection-email-connector-down.md": "db9001a4c1042fb30ab58f0173861091d73ae4ac",
            ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md": "99be254a7c5bda2ca003acdbf82bb44d93664b92",
            ".buglog/bugs/2026-09-26-buglog-hook-misfire.md": "1420a5400b9b4261231d7ecff3a1e052f66f707b",
            ".buglog/index.md": "7afcff30c29e19a71ed65e5aa3daf1c6eb809b43"
        },
        "note": "BUG-003／006／012／013 四条已写入并同步 index.md；本期为 hook 第 33 次误判（透传自动化提示词），未按字面建档。"
    }
}

with io.open(LOG, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(log, f, ensure_ascii=False, indent=2)
    f.write('\n')

m = json.load(io.open(LM, encoding='utf-8'))
m['logs'] = [x for x in m['logs'] if not (x['date'] == '2026-10-31' and x.get('type') == 'morning_briefing')]
m['logs'].insert(0, {
    "date": "2026-10-31",
    "type": "morning_briefing",
    "status": "partial",
    "summary": "周六休市版：伦敦金 3876.69（-3.59%）跌破 3900 创一年新低、AU9999 夜盘 833.0（-2.55%）、积存金估 836.8；数据与推送成功，邮件双通道同时不可用（email_sent:false）。触发延迟约 747 分钟，为观察期最大。"
})
with io.open(LM, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(m, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('log written', LOG)
print('logs count', len(m['logs']))
print(json.load(io.open(LOG, encoding='utf-8'))['status'])
