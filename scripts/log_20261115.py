# -*- coding: utf-8 -*-
"""写入 logs/2026-11-15-morning_briefing.json（含 buglog 复核凭据）。"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = "2026-11-15"

log = {
    "date": DATE,
    "type": "morning_briefing",
    "status": "partial",
    "summary": ("20:39 触发（延迟约 700 分钟，历史第二大值；周日休市、危害 0 档）；前四步全成并已推送（2fe2efd）；"
                "邮件未能发出——qq-mail 工具未装载、reconnect 在无人值守下被取消、备用 agent-mail 未开通（email_sent:false，HTML 已落 outbox）；"
                "价格与涨跌幅一并沿用 11-13 收盘，无跨日回填"),
    "timestamp": "20:39 CST",
    "gap_check": {
        "last_success_briefing": "2026-11-14",
        "missed_trading_days": [],
        "note": ("距上次成功早报 1 个自然日，无断档；11-14 为周六、11-15 为周日，均为非交易日。"
                 "巡检侧：11-13 两线均有产出；11-14 两线零产出但周末巡检历史仅 3/107 条、属非必跑，不计入连续零产出；"
                 "11-15 晚报 20:39 已过 noon 时点、未到 pm 时点。")
    },
    "steps": [
        {
            "num": 1,
            "name": "获取数据",
            "status": "success",
            "duration_ms": 356000,
            "result": ("伦敦金 11-13 纽约收盘 3879.92（+2.49／+0.06%，高 3922.99、低 3867.55），周日无新成交、读数未变；"
                       "AU9999 夜盘收 837.00（日盘 837.55，-1.62%）、T+D 836.29、沪金主力 839(-2.5%)、沪银 11985(-4.1%)；"
                       "中间价 6.7152（周末不更新，沿用）、在岸即期 6.6707；本周累跌 190.83 美元(-4.69%)、周低 3852.48 为逾一年新低；"
                       "周末消息：金饰四天跌 77 元（1164-1178）、小克重金条售罄、SPDR 9 日减 18.53 吨、CFTC 多头 25.3→21.6 万张、"
                       "CME 12 月加 25bp 84.7%／50bp 15.3%、62% 分析师看空下周、下周日程（周一沃什讲话＋国内社零、周二零售销售、周三 FOMC 纪要）"),
            "source": "新浪财经实时接口 hf_XAU／gds_AU9999／gds_AUTD ＋ 东方财富 GC00Y ＋ WebSearch（财闻、腾讯新闻、新浪财经、经济参考报、中新经纬、英为财情、金投网）"
        },
        {
            "num": 2,
            "name": "生成早报JSON",
            "status": "success",
            "duration_ms": 68000,
            "result": ("已写入 daily/2026-11-15.json；check_briefing.py 首轮 1 error（advice 208 字超限）→ 压缩到 196 字后 0 error、pairs 10 组全中；"
                       "图表正常日更丢 1 补 1（丢 10-16、补 11-15=3879.9，events 索引整体 -1、共 30 条，逐条日期比对通过）"),
        },
        {
            "num": 3,
            "name": "更新manifest",
            "status": "success",
            "duration_ms": 9500,
            "result": "已在 manifest.json 的 briefings 数组头部插入 2026-11-15（共 86 条）"
        },
        {
            "num": 4,
            "name": "Git推送",
            "status": "success",
            "duration_ms": 6916,
            "result": "commit 2fe2efd，SSH 推送 master；git rev-parse HEAD 与 git ls-remote origin refs/heads/master 一致（2fe2efd9…aa9ee3）"
        },
        {
            "num": 5,
            "name": "发送邮件",
            "status": "failed",
            "duration_ms": 54000,
            "result": ("未发出：ToolSearch 传 tool_names 精确名两次均回落 agent-mail 命名空间，按名调用 mcp__qq-mail__GetMe 报 not found in the deferred tools index，"
                       "而 list_installed_plugins 显示 qq-mail status=connected／bound=true／enabled=true；按指引 reconnect_plugin 返回 User refused（无人值守无人确认授权）；"
                       "备用 mcp__agent-mail__GetMe 返回 not_bound（邮箱未开通）。HTML 已落 .workbuddy/outbox/mail-2026-11-15.html（11 315 字符／16 961 字节／70 行／maxline 561，零 %%）待人工补发"),
            "outputs": [
                {
                    "label": "邮件内容",
                    "body": ("主题：🌅 今日金价早报 | 2026年11月15日 周日；正文含周日休市与延迟交付提示（生成于 20:50、延迟约 700 分钟）、"
                             "金价快照（积存金 837.7／AU9999 837.00／汇率 6.72／伦敦金 3879.9，并说明与昨日早报同值的原因）、"
                             "昨夜与周末大事 5 条（周线重挫、金饰四天跌 77 元、金条售罄与投资端反向、62% 分析师看空、下周两个开关）、"
                             "趋势判断与 5 组买卖价位、今日学一招（金店排长队为什么不等于金价要涨）、网站链接")
                }
            ]
        }
    ],
    "summary_stats": {
        "total_steps": 5,
        "success_steps": 4,
        "failed_steps": 1,
        "total_duration_ms": 494416,
        "email_sent": False,
        "git_pushed": True
    },
    "buglog_verification": {
        "BUG-003": {
            "path": ".buglog/bugs/2026-09-05-briefing-scheduler-missed-days.md",
            "grep_c_20261115": 1,
            "grep_c_lines": 1,
            "bytes": 9568,
            "sha1": "416a1f5b8ef376eeb512b5c5aa31d55acae698b2"
        },
        "BUG-006": {
            "path": ".buglog/bugs/2026-09-14-inspection-email-connector-down.md",
            "grep_c_20261115": 2,
            "grep_c_lines": 2,
            "bytes": 59498,
            "sha1": "9c3387345712bd0de2dd6996c7cd1c66441ab493"
        },
        "BUG-012": {
            "path": ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md",
            "grep_c_20261115": 1,
            "grep_c_lines": 1,
            "bytes": 60743,
            "sha1": "5f79f1184aa3d5f64a39c7ad2da6f1a57021f82f"
        },
        "BUG-013": {
            "path": ".buglog/bugs/2026-09-26-buglog-hook-misfire.md",
            "grep_c_20261115": 1,
            "grep_c_lines": 1,
            "bytes": 65179,
            "sha1": "4dd35eac07375b5370bbd939f6d8297194094f36"
        },
        "index.md": {
            "path": ".buglog/index.md",
            "grep_c_20261115": 4,
            "grep_c_lines": 3,
            "bytes": 68910,
            "sha1": "b0899b1eed7757f6bae3dc54552dc3190bea5582"
        }
    }
}

p = os.path.join(ROOT, "logs", DATE + "-morning_briefing.json")
assert not os.path.exists(p), "日志已存在，勿覆盖"
with open(p, "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=1)
print("written", p)
print("status", log["status"], "success", log["summary_stats"]["success_steps"], "/", log["summary_stats"]["total_steps"])
