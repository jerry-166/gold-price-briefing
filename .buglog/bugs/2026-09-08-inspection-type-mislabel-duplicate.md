---
id: BUG-005
title: 午后巡检误标为 inspection_pm 并延迟触发，污染晚间巡检日志与 manifest
status: fixed
severity: major
source: automation-hook
reported_at: 2026-09-08T22:00:00+08:00
fixed_at: 2026-09-11T14:10:00+08:00
files:
  - path: .workbuddy/memory/automations/automation-1784188108172
    root_cause: "14:00 午后巡检 automation 提示词把输出文件名/type 硬编码为 inspection_pm，与 22:00 晚检(inspection_pm)冲突"
    fix: "将 automation 输出改为 inspection_noon（文件名与 type 均修正），并加'勿与22:00晚检混淆'约束；9/11 午后巡检已以 inspection_noon 落库"
tags: [automation, logging, data-integrity]
---

## 午后巡检误标为 inspection_pm 并延迟触发，污染晚间巡检日志与 manifest

### 现象
- 2026-09-08 22:00 晚间巡检（inspection_pm）自动化按计划执行，但发现 `logs/2026-09-08-inspection_pm.json` 与 `logs/manifest.json` 中已存在一条 `date=2026-09-08, type=inspection_pm` 记录，其 summary 为「午后巡检（14:00定时，21:17延迟执行）」。
- 即：本应 14:00 运行的「午后巡检（inspection_noon）」实际在 21:17 才触发，且**写入了 inspection_pm 的文件与 manifest 类型**，而非 inspection_noon。
- 后果：晚间 22:00 的 inspection_pm 运行时，当日 pm 文件已存在，必须覆盖重写才能产出权威记录；manifest 中 9/8 出现「午后巡检」内容却挂在 inspection_pm 类型下，索引口径错乱。

### 根因分析
- 两个独立问题叠加：
  1. **调度延迟**：inspection_noon（14:00）自动化未在准点执行，积压触发被延迟到 21:17 才补发（与 BUG-002/003 同类调度器延迟，但首次出现在巡检类任务上）。
  2. **类型串写（核心缺陷）**：该延迟运行的午后巡检在写日志时使用了 `type: "inspection_pm"`，应为 `type: "inspection_noon"`、文件 `logs/YYYY-MM-DD-inspection_noon.json`。疑似该 automation 的提示词/模板把文件名与 type 硬编码成 pm，未随触发时段区分。
- 缺少「同日同 type 已存在则自检」的幂等保护，导致晚间巡检无法提前识别这是脏数据。

### 修复过程
- 本次 22:00 巡检：检测到 pm 文件已被 21:17 误写，遂以权威的 22:00 数据**覆盖** `logs/2026-09-08-inspection_pm.json`，并将 manifest 中该条 9/8 inspection_pm 记录 summary 原地更新为 22:00 结果（避免重复追加同 date+type 行）。
- 根因修复待落实：需修正 inspection_noon automation 的输出文件名/type 为 inspection_noon；并给所有巡检 automation 增加幂等检查（运行前若发现当日对应 date+type 已存在，先比对 timestamp，避免误覆盖/误追加）。

### 经验教训
- 多个同类定时任务（早报/午后/晚间）必须靠 `type` 字段与文件名严格区分，提示词中不要硬编码 pm，应按触发时段参数化。
- 巡检类 automation 开头应加幂等自检：扫描 manifest 与 logs 是否已存在当日同 type 且 status 已落库，存在则判断是脏数据还是重复触发，再决定覆盖/跳过/追加。
- manifest 索引应保持「一 date 一 type 一行」的唯一性，同一天同 type 只允许一条，更新而非追加。

## 根因修复落实（2026-09-11 午后巡检）

- **已落实修复**：2026-09-11 14:04 实际执行的午后巡检，识别到 `logs/2026-09-11-inspection_pm.json` 已被 08:58 提前触发的 22:00 晚检占用，故本次严格以 `inspection_noon` 写入 `logs/2026-09-11-inspection_noon.json`，并在 manifest 顶部追加 `type: inspection_noon` 行，未触碰晚间巡检数据。
- **提示词根因修复**：已更新 automation-1784188108172 的 prompt，将输出文件名与 type 从 `inspection_pm` 改为 `inspection_noon`，并新增「本巡检为 14:00 午后巡检，日志类型固定为 inspection_noon；22:00 晚检使用 inspection_pm，切勿混淆或覆盖」约束。后续 14:00 运行将天然隔离，不再与晚检冲突。
- **残留建议**：各巡检 automation 仍宜加运行前幂等自检（扫描 manifest 是否已存在当日同 type 且已落库），作为额外保险。
