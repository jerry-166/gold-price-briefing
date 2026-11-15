# -*- coding: utf-8 -*-
"""更新 manifest.json：briefings 数组头部插入 2026-11-15。"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "manifest.json")
m = json.load(open(p, encoding="utf-8"))
assert m["briefings"][0]["date"] == "2026-11-14", m["briefings"][0]
assert all(b["date"] != "2026-11-15" for b in m["briefings"])
m["briefings"].insert(0, {"date": "2026-11-15", "title": "今日金价早报", "weekday": "周日"})
json.dump(m, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("briefings head:", m["briefings"][:2], "count", len(m["briefings"]))
