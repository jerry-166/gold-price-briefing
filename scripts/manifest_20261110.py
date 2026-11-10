# -*- coding: utf-8 -*-
"""更新 manifest.json 与 logs/manifest.json（追加今日早报记录）。"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")

DATE = "2026-11-10"

m = json.load(open("manifest.json", encoding="utf-8"))
if m["briefings"] and m["briefings"][0]["date"] == DATE:
    print("manifest already has", DATE)
else:
    m["briefings"].insert(0, {"date": DATE, "title": "今日金价早报", "weekday": "周二"})
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    print("manifest prepended", DATE, "total", len(m["briefings"]))

lm = json.load(open("logs/manifest.json", encoding="utf-8"))
STATUS = sys.argv[1] if len(sys.argv) > 1 else "success"
SUMMARY = sys.argv[2] if len(sys.argv) > 2 else ""
if lm["logs"] and lm["logs"][0]["date"] == DATE and lm["logs"][0]["type"] == "morning_briefing":
    print("logs.manifest already has", DATE)
else:
    lm["logs"].insert(0, {
        "date": DATE,
        "type": "morning_briefing",
        "status": STATUS,
        "summary": SUMMARY,
    })
    with open("logs/manifest.json", "w", encoding="utf-8") as f:
        json.dump(lm, f, ensure_ascii=False, indent=2)
    print("logs.manifest prepended", DATE, "total", len(lm["logs"]))
