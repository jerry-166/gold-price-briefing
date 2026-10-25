# -*- coding: utf-8 -*-
import json, io, re, sys

DATE = "2026-10-25"
d = json.load(io.open("daily/%s.json" % DATE, encoding="utf-8"))
errs = []

assert d["date"] == DATE
assert d["weekday"] == "周日"
assert d["updateTime"] == "09:00"

# 图表
ch = d["chart"]
if not (len(ch["labels"]) == len(ch["values"]) == 30):
    errs.append("chart 长度不符: %d/%d" % (len(ch["labels"]), len(ch["values"])))
for e in ch["events"]:
    if not (0 <= e["index"] < 30):
        errs.append("event 索引越界 %s" % e)
    elif ch["labels"][e["index"]] != e["date"]:
        errs.append("event 日期错位 idx=%d %s != %s" % (e["index"], e["date"], ch["labels"][e["index"]]))
if len(ch["events"]) != 30:
    errs.append("events 数量 %d" % len(ch["events"]))
if ch["labels"][-3:] != ["10-23", "10-24", "10-25"]:
    errs.append("末尾日期 %s" % ch["labels"][-3:])
if ch["values"][-3:] != [3995.5, 3995.5, 3995.5]:
    errs.append("末尾值 %s" % ch["values"][-3:])
idx = [e["index"] for e in ch["events"]]
if idx != sorted(idx) or len(set(idx)) != len(idx):
    errs.append("events 索引非严格递增/有重复")

# 新闻
for n in d["news"]:
    if not n.get("url", "").startswith("http"):
        errs.append("news url 非法: %s" % n.get("title"))
    if n.get("tagType") not in ("fed", "geo", "fx", "data"):
        errs.append("tagType 非法: %s" % n.get("tagType"))
if len(d["news"]) < 4:
    errs.append("news 少于 4 条")

# dataSources
for s in d["_meta"]["dataSources"]:
    if not s["url"].startswith("http"):
        errs.append("dataSource url 非法: %s" % s["name"][:20])
    if "chinanet" in s["url"]:
        errs.append("域名笔误 chinanet")

# 数字自洽
prices = {p["label"]: p for p in d["prices"]}
hero = prices["招行积存金买入价"]
calc = 3995.5 * 6.7180 / 31.1035
if abs(float(hero["value"]) - round(calc, 1)) > 0.05:
    errs.append("hero 折算不符: %s vs %.2f" % (hero["value"], calc))
if prices["伦敦金 XAUUSD"]["value"] != "3995.5":
    errs.append("伦敦金值不符")
if prices["上海金 AU9999"]["value"] != "864.0":
    errs.append("AU9999 值不符")
if len(d["prices"]) != 4:
    errs.append("prices 数量 %d" % len(d["prices"]))
if sum(1 for p in d["prices"] if p.get("hero")) != 1:
    errs.append("hero 标记数不为 1")

# trend / plan 一致性
for k in ("short", "mid", "long", "action", "advice"):
    if k not in d["trend"]:
        errs.append("trend 缺字段 " + k)
for k in ("shortVal", "midVal", "longVal"):
    if d["trend"][k] not in (-1, 0, 1):
        errs.append("trend.%s 取值非法" % k)
if d["trend"]["action"] not in ("hold", "buy", "watch"):
    errs.append("action 非法")
adv = re.sub(r"<[^>]+>", "", d["trend"]["advice"])
if len(adv) > 200:
    errs.append("advice 超长 %d" % len(adv))
for token in ["3970-3985", "3940-3960", "3900-3920", "4030-4050", "4075-4100", "4120", "3960", "3920", "857-861", "851-855", "842-847", "870-875", "880-886", "890", "855", "847"]:
    if token not in d["trend"]["advice"]:
        errs.append("advice 缺价位 " + token)
    if token not in d["plan"]["buy"]["price"] + d["plan"]["sell"]["price"]:
        errs.append("plan 缺价位 " + token)

# teach
if "<ol>" not in d["teach"]["body"] or d["teach"]["body"].count("<li>") != 3:
    errs.append("teach body 结构不符")

# ASCII 直引号只在解析后的字符串里检查
def walk(o, path=""):
    if isinstance(o, str):
        if '"' in o:
            errs.append('ASCII 引号 @ %s: %s' % (path, o[:40]))
        if "'" in o:
            errs.append("ASCII 单引号 @ %s: %s" % (path, o[:40]))
    elif isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + "[%d]" % i)
walk(d)

print("ERRORS:" if errs else "ALL CHECKS PASSED")
for e in errs:
    print(" -", e)
sys.exit(1 if errs else 0)
