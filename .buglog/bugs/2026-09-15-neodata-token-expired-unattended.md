---
id: BUG-008
title: NeoData 技能令牌过期（TOKEN_EXPIRED），无人值守巡检无法以 NeoData 为优先数据源
status: open
severity: minor
source: automation-hook
reported_at: 2026-09-15T14:02:00+08:00
related_bugs: [BUG-007]
---

## NeoData 技能令牌过期（TOKEN_EXPIRED），无人值守巡检无法以 NeoData 为优先数据源

### 现象
- 2026-09-15 14:00 午后巡检执行价格查询时，调用 `neodata-financial-search` 技能脚本 `scripts/query.py`，首跑即返回 `TOKEN_EXPIRED`，未能取得任何伦敦金报价。
- 同日早报（09:33）尚能经 NeoData 取数成功，至 14:00（间隔约 4.5h）即过期，明显短于技能文档所述 12h 缓存有效期，疑似缓存凭据在两次运行间被清空或该次缓存写入时即为临近过期值。
- 本次巡检被迫降级到与早报同口径的**金投网现货 XAUUSD**（任务既定权威备用源），数据正确性未受影响；但技能要求的「金融数据必须优先使用 NeoData」硬规则在无人值守场景下被绕过。

### 根因分析
- **凭据缓存生命周期不稳定**：`neodata-financial-search` 依赖本地缓存 token（标称 12h），但在 daily 自动化多次触发之间缓存未稳定保活，导致后续运行读取到已失效 token。无人值守场景无法像交互会话那样自动走 `connect_cloud_service` 重新获取（需 IDE 桌面会话在线，自动化环境未必可用）。
- 巡检任务把 NeoData 列为「优先数据源」，却未对「取数失败」设计自动续期或静默降级到备用源的显式分支，一旦 NeoData 不可用就只剩人工兜底。

### 修复过程
- 本次为「带疑继续」：NeoData 取数失败后，按任务既定口径改用金投网现货 XAUUSD（与早报同口径、可比），并在 `steps[0].result` 与 `source` 字段显式注明「NeoData 令牌过期未取数」，未中断巡检链路。
- 尚未实现自动续期。

### 经验教训
- **无人值守取数要内置「主源失败→备用源」的硬降级分支**：对每日定时巡检这类非交互任务，不应假设主数据源凭据长期有效；应在脚本层捕获 `TOKEN_EXPIRED`，先尝试 `connect_cloud_service` 续期一次，失败则自动落到任务约定的备用源（如金投网/金价查询网），并在日志标注降级原因。
- 对「NeoData 优先」类规则，在自动化 prompt 中应补一句：「若 NeoData 取数失败/超时，允许以金投网现货为准，并在 result 注明偏差」，把本次的人工判断固化为规则，避免每次都靠临场判断。
- 可顺带向数据源侧反馈凭据缓存 TTL 与实际失效不一致的问题（标称 12h 实际约 4–5h 失效）。
