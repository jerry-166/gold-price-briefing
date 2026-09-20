---
id: BUG-010
title: 早报 JSON 与运行日志中手工录入内容出现笔误（来源 URL 域名错误、价位数字转录错误）
status: fixed
severity: minor
source: ai-review
reported_at: 2026-09-20T09:10:00+08:00
fixed_at: 2026-09-20T09:12:00+08:00
files:
  - path: daily/2026-09-20.json
    root_cause: "手工录入 _meta.dataSources 时把中国货币网域名 chinamoney.org.cn 误写为 chinanet.org.cn（少一个 m、多一个 n 的相邻键位混淆）。该字段是站点展示的『数据来源』可点击链接，域名错误会导致读者点击后 404，属会随产物发布出去的可见缺陷。"
    fix: "写入后回读文件，用 python -c 逐项检查 dataSources 的 url 是否可解析、域名是否与来源名匹配，发现后立即 Edit 修正为 https://www.chinamoney.org.cn/chinese/bkccpr/。"
  - path: logs/2026-09-20-morning_briefing.json
    root_cause: "在 step 5 的 result 描述里转录买卖时机价位时，把 4330 误写为 4310（数字相邻键位笔误）。同一份事实在同一文件内出现了两个版本，读者对照 plan 字段时会发现自相矛盾。"
    fix: "提交前用 python -c 读回日志 JSON，比对 step 5 result 中的价位区间与 daily JSON 的 plan.buy.price 是否一致，发现后 Edit 修正为 4330-4345。"
tags: [data-quality, json, manual-entry]
related_bugs: [BUG-009]
---

## 早报 JSON 与运行日志中手工录入内容出现笔误（来源 URL 域名错误、价位数字转录错误）

### 现象
- 生成 `daily/2026-09-20.json` 时，`_meta.dataSources` 中「中国货币网·人民币汇率中间价公告」的 url 写成了 `https://www.chinanet.org.cn/chinese/bkccpr/`，正确应为 `https://www.chinamoney.org.cn/chinese/bkccpr/`。
- 生成 `logs/2026-09-20-morning_briefing.json` 时，step 5（发送邮件）的 `result` 描述里把买卖时机写为「4310-4345 买」，而同一批次 `daily/2026-09-20.json` 的 `plan.buy.price` 是「4330-4345」。
- 两处均在提交前自查发现并修复，未随 commit `ea81299` / `fa9c9c5` 发布出去。

### 根因分析
- 两处属同一类根因：**早报产物中的大量字段（来源 URL、价位区间、日期、数值）由模型手工转录，缺乏生成后的机械校验环节**。
- 旧的校验脚本只做 `json.load()` 语法校验（用于拦截 BUG-009 那类转义问题），能保证「JSON 合法」，但完全不校验「内容正确」——一个合法的 JSON 里可以同时存在错误的域名和自相矛盾的数字。
- 触发条件：单次早报需要转录 20+ 条 dataSources URL 和 10+ 个价位数字，键位相邻（m/n、0/3）的转录错误在长文本中不受语法校验约束。

### 修复过程
1. 写入 `daily/2026-09-20.json` 后用脚本回读，检查 `dataSources[].url` 的域名与来源名是否匹配，命中 chinanet → Edit 改为 chinamoney。
2. 写入 `logs/2026-09-20-morning_briefing.json` 后用脚本回读，提取 step 5 `result` 中的价位区间，与 `daily` 的 `plan.buy.price` / `plan.sell.price` 做交叉比对，命中 4310 → Edit 改为 4330。
3. 两处修复后均重新执行 `json.load()` 校验通过，再进入 git 提交。

### 经验教训
- **JSON 语法校验 ≠ 内容校验**。早报链路的提交流程应从「只校验能否 parse」升级为「parse + 关键字段一致性校验」两个环节。
- 建议固化一个提交前自检清单（可脚本化）：
  - `dataSources[].url` 域名与来源名匹配、不含明显错拼（重点域名白名单：chinamoney.org.cn / sge.com.cn / chinanews.com.cn / cnfin.com 等）；
  - `prices[].value` 与 `trend`/`plan`/`teach`/`knowledge` 正文中引用的同一数字一致；
  - `plan.buy.price` / `plan.sell.price` 的区间与 logs step 5 `result` 描述一致；
  - `hero` 积存金估算值 = 伦敦金 × 汇率 ÷ 31.1035 且四舍五入到 1 位小数；
  - `chart.labels.length == chart.values.length`，且 `events[].index < labels.length`。
- 这类笔误的性质与 BUG-009（转义导致的语法错误）互补：BUG-009 是「写坏了 JSON」，本条是「JSON 没坏但内容是错的」，两者需在提交前分别拦截。
