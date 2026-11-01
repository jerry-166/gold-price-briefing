# -*- coding: utf-8 -*-
"""把 2026-11-01 记录追加到 manifest.json 头部。"""
import json, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, "manifest.json")
d = json.load(io.open(P, encoding="utf-8"))
b = d["briefings"]
if b and b[0]["date"] == "2026-11-01":
    print("already exists, skip")
else:
    b.insert(0, {"date": "2026-11-01", "title": "今日金价早报", "weekday": "周日"})
    io.open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    print("inserted, total", len(b))
