import json

manifest_path = r"D:\workspace\每日金价资讯\logs\manifest.json"
with open(manifest_path, encoding="utf-8") as f:
    data = json.load(f)

entry = {
    "date": "2026-11-10",
    "type": "inspection_noon",
    "status": "no_action",
    "summary": "午后巡检：伦敦金 XAUUSD $4124.24/oz，较早报($4110.25)+0.34%、日内较昨收-0.40%、振幅约0.93%，远低于1.5%阈值；午后延续CPI前回落+双顶叙事，无美联储紧急声明或全新突发，静默跳过。"
}

data["logs"].insert(0, entry)

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("prepended inspection_noon; total logs:", len(data["logs"]))
