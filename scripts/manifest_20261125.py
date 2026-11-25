# -*- coding: utf-8 -*-
"""在 manifest.json 的 briefings 数组头部插入今日记录（幂等）。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "manifest.json"
d = json.load(open(P, encoding="utf-8"))

rec = {"date": "2026-11-25", "title": "今日金价早报", "weekday": "周三"}
arr = [x for x in d["briefings"] if x.get("date") != rec["date"]]
arr.insert(0, rec)
d["briefings"] = arr

raw = json.dumps(d, ensure_ascii=False, indent=2)
assert raw.count("%%") == 0
P.write_text(raw + "\n", encoding="utf-8")
print("manifest head:", json.dumps(d["briefings"][:3], ensure_ascii=False))
print("total:", len(d["briefings"]))
