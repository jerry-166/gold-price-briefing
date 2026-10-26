# -*- coding: utf-8 -*-
"""早报 JSON 自检（结构 + 内容 + 一致性）。"""
import json, re, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "daily/2026-10-26.json"
DATE = PATH.split("/")[-1].replace(".json", "")
d = json.load(open(PATH, encoding="utf-8"))

errs = []

# 1 基础
assert d["date"] == DATE, d["date"]
assert d["updateTime"] == "09:00"
assert d["_meta"]["updated"].startswith(DATE)

# 2 图表
labels, values = d["chart"]["labels"], d["chart"]["values"]
if not (len(labels) == len(values) == 30):
    errs.append("chart len %d/%d" % (len(labels), len(values)))
if labels[-1] != DATE[5:]:
    errs.append("labels[-1]=%s" % labels[-1])
for i, e in enumerate(d["chart"]["events"]):
    if not (0 <= e["index"] < len(labels)):
        errs.append("event idx %s" % e["index"])
    elif labels[e["index"]] != e["date"]:
        errs.append("event date mismatch idx=%d %s vs %s" % (e["index"], e["date"], labels[e["index"]]))
idx = [e["index"] for e in d["chart"]["events"]]
if idx != sorted(idx) or len(set(idx)) != len(idx):
    errs.append("events not strictly increasing")

# 3 新闻 url
for n in d["news"]:
    if not n.get("url", "").startswith("http"):
        errs.append("bad url: " + n["title"][:20])
    if n["tagType"] not in ("fed", "geo", "fx", "data"):
        errs.append("bad tagType: " + n["tagType"])

# 4 dataSources 域名
for s in d["_meta"]["dataSources"]:
    host = re.sub(r"^https?://", "", s["url"]).split("/")[0]
    if not host or "." not in host:
        errs.append("bad ds host: " + s["url"])

# 5 解析后字符串里的 ASCII 引号
def walk(o, path=""):
    if isinstance(o, str):
        if '"' in o:
            errs.append("ASCII quote in " + path)
        if "`" in o:
            errs.append("backtick in " + path)
    elif isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, "%s[%d]" % (path, i))

walk(d)

# 6 advice 字数
adv = re.sub(r"<[^>]+>", "", d["trend"]["advice"])
if len(adv) > 200:
    errs.append("advice too long: %d" % len(adv))

# 7 hero 复算
rate = 6.7162
p = float(d["prices"][3]["value"])
hero = round(p * rate / 31.1035, 1)
if abs(hero - float(d["prices"][0]["value"])) > 0.1:
    errs.append("hero mismatch %s vs %s" % (hero, d["prices"][0]["value"]))

# 8 价位一致性：advice / plan / note 中的 ¥/克 必须能由美元价复算
def cny(usd):
    return round(usd * rate / 31.1035, 1)

checks = {3975: 858.3, 3985: 860.5, 3940: 850.8, 3950: 852.9, 3900: 842.1,
          4018: 867.6, 4025: 869.1, 4060: 876.7, 4087: 882.5, 4120: 889.6, 3943: 851.4}
for usd, exp in checks.items():
    if abs(cny(usd) - exp) > 0.15:
        errs.append("cny mismatch %s -> %s (exp %s)" % (usd, cny(usd), exp))

blob = d["trend"]["advice"] + d["plan"]["buy"]["trigger"] + d["plan"]["sell"]["trigger"] + d["plan"]["buy"]["price"] + d["plan"]["sell"]["price"]
for token in ["3975-3985", "3940-3950", "4018-4025", "4060-4087", "858-861", "851-853", "868-869", "877-882", "842"]:
    if token not in blob:
        errs.append("token missing in plan/advice: " + token)

# 9 必填
for k in ["prices", "news", "trend", "plan", "teach", "knowledge", "chart"]:
    if not d.get(k):
        errs.append("missing " + k)
for v in ["shortVal", "midVal", "longVal"]:
    if d["trend"][v] not in (-1, 0, 1):
        errs.append("bad " + v)
if d["trend"]["action"] not in ("hold", "buy", "watch"):
    errs.append("bad action")
if not d["teach"]["body"].startswith("<ol>") or d["teach"]["body"].count("<li>") != 3:
    errs.append("teach body format")

print("advice len =", len(adv))
print("errors:", len(errs))
for e in errs:
    print("  -", e)
print("OK" if not errs else "FAIL")
