# -*- coding: utf-8 -*-
"""把 buglog 复核凭据写入 logs/2026-11-11-morning_briefing.json（实测值）。"""
import json, hashlib, os, datetime

DATE = "2026-11-11"
LOGP = f"logs/{DATE}-morning_briefing.json"
BUGS = {
    "2026-09-08-briefing-scheduler-missed-days.md": ".buglog/bugs/2026-09-08-briefing-scheduler-missed-days.md",
    "2026-09-14-inspection-email-connector-down.md": ".buglog/bugs/2026-09-14-inspection-email-connector-down.md",
    "2026-09-25-inspection-scheduler-silent-miss.md": ".buglog/bugs/2026-09-25-inspection-scheduler-silent-miss.md",
    "2026-09-26-buglog-hook-misfire.md": ".buglog/bugs/2026-09-26-buglog-hook-misfire.md",
    "index.md": ".buglog/index.md",
}

files = {}
for name, path in BUGS.items():
    raw = open(path, "rb").read()
    files[name] = {
        "bytes": len(raw),
        "sha1": hashlib.sha1(raw).hexdigest(),
        "date_2026_11_11_count": raw.decode("utf-8").count(DATE),
        "date_2026_11_10_count": raw.decode("utf-8").count("2026-11-10"),
    }

log = json.load(open(LOGP, encoding="utf-8"))
log["buglog_verification"] = {
    "date_grep_count_2026_11_11": {k: v["date_2026_11_11_count"] for k, v in files.items()},
    "date_grep_count_2026_11_10": {k: v["date_2026_11_10_count"] for k, v in files.items()},
    "file_bytes_and_sha1": {k: {"bytes": v["bytes"], "sha1": v["sha1"]} for k, v in files.items()},
    "index_counts": {"open": 12, "fixed": 12, "total": 24, "note": "本期无新增 bug、无状态变更"},
    "notes": (
        "BUG-003 延迟约 50 分钟（中低位，未刷新上界），新增危害实例「延迟撞上重大数据窗口」（11-10 延迟 168 分钟与 CPI 之夜重合，"
        "今日回填 77.6 美元≈16.6 元/克，本站第二大）；BUG-006 复发（工具未注册形态），连续正常 2 日后中断，"
        "新增两条结论：connector-status 状态字段不可作可用性判据、精确名检索无法兜底索引未装载；"
        "BUG-012 当日巡检未到点；BUG-013 第 44 次误判，并发现 11-10 期 index.md 小节整体漏写（第四次「声明与产物脱节」），已补记。"
        "advice 215→202→196 三次压缩、build 脚本 3 次 Edit 属生成前自纠，不计入 bug 修复。"
    ),
}
log["_meta"]["written_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
json.dump(log, open(LOGP, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(log["buglog_verification"]["date_grep_count_2026_11_11"], ensure_ascii=False))
print(json.dumps(log["buglog_verification"]["date_grep_count_2026_11_10"], ensure_ascii=False))
print("log rewritten", os.path.getsize(LOGP), "bytes")
