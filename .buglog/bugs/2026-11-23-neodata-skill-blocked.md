---
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
