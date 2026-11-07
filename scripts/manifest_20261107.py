# -*- coding: utf-8 -*-
import json
p = "manifest.json"
d = json.load(open(p, encoding="utf-8"))
items = d["briefings"]
today = {"date": "2026-11-07", "title": "今日金价早报", "weekday": "周六"}
items = [x for x in items if x["date"] != "2026-11-07"]
d["briefings"] = [today] + items
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("briefings", len(d["briefings"]), "head", d["briefings"][0])
