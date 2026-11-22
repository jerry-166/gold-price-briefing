# -*- coding: utf-8 -*-
"""11-22 更新站点 manifest：briefings 头部插入今日记录。"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(BASE, "manifest.json")
m = json.load(open(p, encoding="utf-8"))
assert m["briefings"][0]["date"] == "2026-11-21", m["briefings"][0]["date"]
assert not any(b["date"] == "2026-11-22" for b in m["briefings"]), "已存在今日记录"
m["briefings"].insert(0, {"date": "2026-11-22", "title": "今日金价早报", "weekday": "周日"})
raw = json.dumps(m, ensure_ascii=False, indent=2)
assert raw.count("%%") == 0
with open(p, "w", encoding="utf-8") as f:
    f.write(raw + "\n")
print("briefings", len(m["briefings"]), "head", m["briefings"][0])
