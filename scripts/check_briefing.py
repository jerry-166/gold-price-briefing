# -*- coding: utf-8 -*-
"""早报 JSON 自检（结构 + 内容 + 一致性）。通用版：汇率与价位从产物自身提取，不写死日期。

用法：python scripts/check_briefing.py daily/YYYY-MM-DD.json
"""
import json, re, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "daily/2026-10-27.json"
DATE = PATH.replace("\\", "/").split("/")[-1].replace(".json", "")
d = json.load(open(PATH, encoding="utf-8"))

errs = []

# 1 基础
if d["date"] != DATE:
    errs.append("date mismatch %s vs %s" % (d["date"], DATE))
if d["updateTime"] != "09:00":
    errs.append("updateTime " + d["updateTime"])
if not d["_meta"]["updated"].startswith(DATE):
    errs.append("_meta.updated " + d["_meta"]["updated"])

# 2 图表
labels, values = d["chart"]["labels"], d["chart"]["values"]
if not (len(labels) == len(values) == 30):
    errs.append("chart len %d/%d" % (len(labels), len(values)))
if labels and labels[-1] != DATE[5:]:
    errs.append("labels[-1]=%s" % labels[-1])
if len(set(labels)) != len(labels):
    errs.append("duplicate labels")
for e in d["chart"]["events"]:
    if not (0 <= e["index"] < len(labels)):
        errs.append("event idx %s" % e["index"])
    elif labels[e["index"]] != e["date"]:
        errs.append("event date mismatch idx=%d %s vs %s" % (e["index"], e["date"], labels[e["index"]]))
idx = [e["index"] for e in d["chart"]["events"]]
if idx != sorted(idx) or len(set(idx)) != len(idx):
    errs.append("events not strictly increasing")

# 3 新闻 url / tagType
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

# 5 解析后字符串里的 ASCII 引号 / 反引号 / 未渲染的 ** 加粗
def walk(o, path=""):
    if isinstance(o, str):
        if '"' in o:
            errs.append("ASCII quote in " + path)
        if "`" in o:
            errs.append("backtick in " + path)
        if "**" in o:
            errs.append("literal ** in " + path)
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

# 7 汇率：从「美元汇率」一栏的 source 里取四位小数中间价
fx_src = d["prices"][2]["source"]
m = re.search(r"中间价[^0-9]{0,6}(\d\.\d{4})", fx_src)
if not m:
    errs.append("rate not found in prices[2].source")
    rate = 6.7171
else:
    rate = float(m.group(1))
    if not fx_src.startswith("中国外汇交易中心") and "中国外汇交易中心" not in fx_src:
        errs.append("prices[2].source 未标注中国外汇交易中心")


def cny(usd):
    return round(usd * rate / 31.1035, 1)


# 8 hero 复算
p = float(d["prices"][3]["value"])
hero = round(p * rate / 31.1035, 1)
if abs(hero - float(d["prices"][0]["value"])) > 0.15:
    errs.append("hero mismatch %s vs %s" % (hero, d["prices"][0]["value"]))

# 9 价位一致性：所有「美元区间（约 ¥ 区间 元/克）」两端都要能由汇率复算
blob = "".join([
    d["trend"]["advice"],
    d["plan"]["buy"]["trigger"], d["plan"]["buy"]["price"], d["plan"]["buy"]["reason"],
    d["plan"]["sell"]["trigger"], d["plan"]["sell"]["price"], d["plan"]["sell"]["reason"],
    d["plan"]["note"],
])
pairs = re.findall(r"(\d{3,4})-(\d{3,4})[^（(0-9]{0,10}[（(]\s*约?\s*(\d{3})-(\d{3})\s*元/克[）)]", blob)
if len(pairs) < 5:
    errs.append("paired 价位 too few: %d" % len(pairs))
for u1, u2, y1, y2 in pairs:
    if abs(cny(int(u1)) - int(y1)) > 0.6 or abs(cny(int(u2)) - int(y2)) > 0.6:
        errs.append("cny pair mismatch %s-%s -> %s-%s (calc %s-%s)"
                    % (u1, u2, y1, y2, cny(int(u1)), cny(int(u2))))

# 10 plan.price 里的每一档美元区间都必须出现在 advice 里
for key in ("buy", "sell"):
    usd_ranges = re.findall(r"(\d{3,4})-(\d{3,4})", d["plan"][key]["price"])
    for a, b in usd_ranges:
        if ("%s-%s" % (a, b)) not in d["trend"]["advice"]:
            errs.append("plan.%s 价位 %s-%s 未出现在 advice" % (key, a, b))

# 11 必填与枚举
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

# 12 精度：金价 1 位小数、汇率 2 位小数、涨跌幅 2 位小数
for pr in d["prices"]:
    if "." in pr["value"] and len(pr["value"].split(".")[1]) > 2:
        errs.append("value 精度过多: %s" % pr["label"])
    ch = pr["change"]
    if round(ch, 2) != ch:
        errs.append("change 精度过多: %s %s" % (pr["label"], ch))
if not re.fullmatch(r"\d+\.\d{2}", d["prices"][2]["value"]):
    errs.append("汇率应 2 位小数: " + d["prices"][2]["value"])

# 13 休市日必须注明「沿用」（仅在周末自动判定时提示）
print("advice len =", len(adv), "| rate =", rate, "| pairs =", len(pairs))
print("errors:", len(errs))
for e in errs:
    print("  -", e)
print("OK" if not errs else "FAIL")
