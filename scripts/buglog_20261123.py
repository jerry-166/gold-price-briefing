# -*- coding: utf-8 -*-
"""2026-11-23 buglog：新增 BUG-033（neodata 技能被 requests 依赖卡死）+ 追加当日观察更新。
幂等守卫：检测到 '## 2026-11-23' 已存在即整体 SKIP（BUG-025 教训：skip 分支必须收尾，不能半途而废）。
"""
import hashlib
import io
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGDIR = os.path.join(BASE, ".buglog", "bugs")
INDEX = os.path.join(BASE, ".buglog", "index.md")
STATS = os.path.join(BASE, ".buglog", "stats.json")
DATE = "2026-11-23"

NEW_BUG = """---
id: BUG-033
title: neodata-financial-search 技能就位但跑不起来（缺 requests 依赖且 pip 源不可用），任务提示词的第一取数路径长期不可执行
severity: minor
status: open
found_at: 2026-11-23
tags: [data-source, dependency, silent-degradation]
---

# BUG-033 neodata 技能被 requests 依赖卡死

## 现象

任务提示词第一步明确要求「调用 neodata-financial-search skill 查询伦敦金 / 中间价 / AU9999」。
2026-11-23 实测：技能已不在 `plugins/cache`，而是落在
`~/.workbuddy/skills-marketplace/skills/neodata-financial-search/`，`SKILL.md` 与 `scripts/query.py` 齐全，
token 缓存 `~/.workbuddy/.neodata_token` 也存在（不再是 BUG-008 的 TOKEN_EXPIRED 形态）。

但 `python scripts/query.py --query "伦敦金现货XAUUSD最新价和涨跌幅"` 直接输出：

```
需要安装 requests: pip install requests
```

按提示补装 `python -m pip install requests` 后返回：

```
ERROR: Could not find a version that satisfies the requirement requests (from versions: none)
ERROR: No matching distribution found for requests
```

即**当前环境的 pip 源不可用**，无法补依赖。技能因此完全不可执行。

## 根因

技能脚本硬依赖第三方包 `requests`，而宿主环境既没预装、也装不上。
`query.py` 把「缺依赖」处理成打印提示后正常退出（`exit 0`），不抛异常、不返回非零码，
对自动化链路而言是**静默降级**——如果调用方只看退出码，会误以为查询成功、拿到空结果。

## 影响

- 早报/巡检的「第一取数路径」实际长期不可用，每期都要临时改走「新浪实时接口 hf_XAU / gds_AU9999 + WebSearch」。
  这条替代路径本身可用（11-17 起已验证多次），所以**产物质量未受影响，但流程与提示词脱节**。
- 每期都要在 logs 的 `step1.source` 里解释一遍「为什么没用 neodata」，属重复劳动，且有「假装调用」的合规风险。

## 建议修法

1. 优先级最高：把 `query.py` 的 HTTP 层从 `requests` 换成标准库 `urllib.request`（只用到 POST + JSON + Bearer，
   标准库完全够用），一次性消除外部依赖；
2. 或者让缺依赖时 `exit 1` 并在 stderr 输出明确错误码，避免调用方把「没结果」当「没数据」；
3. 若坚持用 requests，需在技能安装流程里自带依赖（vendored 或 wheels 离线目录），不能依赖在线 pip 源。

## 本期处置

如实记录为「未调用成功」，`logs/2026-11-23-morning_briefing.json` 的 `step1.source` 已写明
「脚本就位且 token 存在，但运行缺 requests 依赖、本地 pip 源不可用，install 失败 → 改走实时接口 + 搜索，未假装调用」。
"""

OBS = """## 2026-11-23（周一）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **153 分钟**（会话首次 `date` 实测 11:33:39，标称 09:00），近 6 期序列 `…/154/129/53/153`，在 11-22 的 53 分钟低位后**重新跳回 100 分钟以上**，仍属「4-747 分钟极宽摆动」区间。**今日为交易日且盘中有大行情**（06:00 跳空高开至 3559.83、09:20 冲高 3630.32、11:33 报 3605.04），延迟窗口内已错过开盘位置与冲高段 → **危害 2 档（有行情且错过关键时点）**，与周末期的「危害 0 档」形成对照。未达 360 分钟标注门槛，按建议 ⑬ 不在顶部标延迟交付 |
| BUG-006 | **复发**（连续 5 日成功后的第 6 日失败）。`connector-status` 显示 qq-mail 为 connected，但 `ToolSearch` 精确名检索 4 组（`mcp__qq-mail__SendMessage`、`mcp__qq-mail__ListMessages`、`mcp__qq-mail__send_mail`、`mcp__qq-mail__send_email`）全部回落 `mcp__agent-mail__*`；`DeferExecuteTool mcp__qq-mail__SendMessage` 直接返回 `Tool "mcp__qq-mail__SendMessage" not found in the deferred tools index`；兜底 `mcp__agent-mail__GetMe` 返回 `{"status":"not_bound"}` 并提示「请在开通面板完成开通，当前请勿重试」→ **双通道同时失效、无降级路径**，`email_sent: false`、status partial，HTML 底稿落 `.workbuddy/outbox/mail-2026-11-23-morning_briefing.html`（14 788 字节／maxline 1314，零双百分号、零 CSS `width:100%`）待人工补发。形态序列：未注册(10-19)→正常(10-20)→未注册(10-21/22)→…→正常(11-18~11-22 五日)→**未注册(11-23)**。11-22 的「连续 5 日正常」再次被证伪为修复证据 |
| BUG-012 | 今日 `logs/` 下无 `2026-11-23-inspection_*` 产出，14:00 与 22:00 均未到点，不判缺跑；连续零产出交易日数 = 0，按复合判据不升级不降级 |
| BUG-013 | **第 35 次连续命中**（9/26 起），hook 再次把自动化提示词全文透传为「bug 报告」→ 判误判、未按字面建档。附带弱提示两条均属正常开发：①`build_20261123.py` 编辑 2 次＝`advice` 204→198 字压缩 + `_meta.updated` 占位符填真实时间；②`log_20261123.py` 编辑 1 次＝清单摘要笔误「交易所版」→「交易日版」 |
| BUG-030 | 本期**第三次手工规避**：`build_20261123.py` 仍手抄 `if e["index"] - 1 < 0: continue`，另加 `assert labels[e["index"]] == e["date"]` 逐条比对兜底。建议的 `lib_chart.shift_chart()` 仍未落地 |
| BUG-032 | 维持 open。本期邮件未发出，转抄环节不存在，故无一致性校验可做。**但本期实测否掉了建议的兜底路径：`config/` 目录根本不存在，`scripts/send_email.py` 一运行就会在「配置文件不存在」处 `return 1`，所以「补齐 config/email.json 改走 SMTP」不是补个文件的事，还需要 SMTP 授权码等人工输入** |
| BUG-033 | **新增、open**：neodata-financial-search 技能已落 `skills-marketplace`（SKILL.md 与 `scripts/query.py` 齐全）、token 缓存也在，但 `query.py` 运行即报「需要安装 requests」，`pip install requests` 又因本地索引无此包而失败 → 第一取数路径实际不可执行，且脚本缺依赖时 `exit 0`，属静默降级。建议把 HTTP 层改标准库 `urllib.request`，彻底去掉外部依赖 |

### 本期 buglog 复核凭据（2026-11-23）

- **有新增 bug**：`bugs/2026-11-23-neodata-skill-blocked.md`（BUG-033，open）
- 计数取自本文件表头（写入后重读）：Open 16 / Fixed 17 / Total 33（Open 15→16、Total 32→33；无 fixed 变动）
- 幂等守卫：本脚本先检测 `## 2026-11-23` 是否已存在，存在即整体 SKIP
- 完整性：`bugs/` 目录 32 → **33** 个文件；`index.md` 字节数／SHA-1／当日串出现次数已写入 `logs/2026-11-23-morning_briefing.json` 的 `buglog_verification`（在全部写入动作之后测量）
"""

idx = io.open(INDEX, encoding="utf-8").read()

if "## 2026-11-23" in idx:
    print("SKIP: 2026-11-23 观察更新已存在，幂等退出")
else:
    # 1) 新增 bug 文件
    bugpath = os.path.join(BUGDIR, "2026-11-23-neodata-skill-blocked.md")
    io.open(bugpath, "w", encoding="utf-8").write(NEW_BUG)
    print("written", bugpath)

    # 2) 表头计数
    idx = idx.replace("Open: 15 | Fixed: 17 | Total: 32", "Open: 16 | Fixed: 17 | Total: 33", 1)

    # 3) 表格追加 BUG-033 行（插在 BUG-032 行之后）
    lines = idx.split("\n")
    row = (
        "| BUG-033 | neodata-financial-search 技能就位但跑不起来（缺 requests 依赖且 pip 源不可用），"
        "任务提示词的第一取数路径长期不可执行；`query.py` 缺依赖时 `exit 0`，属静默降级（2026-11-23） | minor | open |"
    )
    out, done = [], False
    for ln in lines:
        out.append(ln)
        if not done and ln.startswith("| BUG-032 |"):
            out.append(row)
            done = True
    assert done, "未找到 BUG-032 表格行，插入失败"
    idx = "\n".join(out)

    # 4) 末尾追加当日观察更新
    idx = idx.rstrip("\n") + "\n\n" + OBS
    io.open(INDEX, "w", encoding="utf-8").write(idx)

    # 5) stats.json
    st = json.load(io.open(STATS, encoding="utf-8"))
    st["open_count"] = 16
    st["total_count"] = 33
    io.open(STATS, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=2) + "\n")
    print("stats", st["open_count"], st["fixed_count"], st["total_count"])

# ---- 复核凭据（在全部写入动作之后测量） ----
nb = len([f for f in os.listdir(BUGDIR) if f.endswith(".md")])
raw = io.open(INDEX, encoding="utf-8").read()
ver = {
    "date": DATE,
    "new_bug": "BUG-033",
    "bugs_dir_count": nb,
    "index_bytes": len(raw.encode("utf-8")),
    "index_sha1": hashlib.sha1(raw.encode("utf-8")).hexdigest(),
    "date_string_occurrences": raw.count(DATE),
    "header_line": raw.split("\n")[2],
    "consistency": {
        "bugs_with_date": sum(
            1 for f in os.listdir(BUGDIR) if f.startswith(DATE) or DATE in io.open(os.path.join(BUGDIR, f), encoding="utf-8").read()[:400]
        ),
        "index_has_section": "## 2026-11-23" in raw,
    },
}
print(json.dumps(ver, ensure_ascii=False, indent=2))

# 写入当日报表日志
lp = os.path.join(BASE, "logs", DATE + "-morning_briefing.json")
lg = json.load(io.open(lp, encoding="utf-8"))
lg["buglog_verification"] = ver
io.open(lp, "w", encoding="utf-8").write(json.dumps(lg, ensure_ascii=False, indent=2) + "\n")
print("log updated", lp)
