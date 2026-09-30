# Buglog 索引

Open: 9 | Fixed: 4 | Total: 13

| ID | Title | Severity | Status |
|---|---|---|---|
| BUG-001 | 金价早报自动化重复触发（当日已成功后再次运行） | major | open |
| BUG-002 | 金价早报调度器连续多日未触发（9/1-9/4缺失、9/5延迟至16:20） | major | open |
| BUG-003 | 金价早报调度器异常（9/13-9/30「延迟」与「静默缺跑」交替；**9/23、9/27、9/28 三日缺跑，其中 9/27-9/28 为首次连续两日缺跑**；**9/30 延迟 115 分钟刷新迄今最长记录**，区间上界由 88 推至 115 分钟） | major | open |
| BUG-004 | 无人值守巡检中 git push 因凭据无法交互输入而失败 | major | fixed |
| BUG-005 | 午后巡检误标为 inspection_pm 并延迟触发，污染晚间巡检日志与 manifest | major | fixed |
| BUG-006 | 金价巡检预警邮件无法发送（mail connector 不可用） | major | open |
| BUG-007 | NeoData 上海金 AU9999 报价异常（9/15字段矛盾、9/17水平偏离官方5元/克），处理策略已转为官方源优先 | minor | open |
| BUG-008 | NeoData 技能令牌过期（TOKEN_EXPIRED），无人值守巡检无法以 NeoData 为优先数据源 | minor | open |
| BUG-009 | 早报运行日志 JSON 因正文内联 ASCII 直双引号未转义而解析失败 | minor | fixed |
| BUG-010 | 早报 JSON 与运行日志中手工录入内容出现笔误（来源 URL 域名错误、价位数字转录错误） | minor | fixed |
| BUG-011 | 提交前自检脚本用 ASCII 直引号扫描中文正文，产生大量假阳性（正则本身即含未转义引号） | minor | open |
| BUG-012 | 巡检定时任务频繁零产出（9/18-9/24 连续七日、9/27-9/28 再次静默；**9/29 晚间巡检恢复正常触发**，但 **inspection_noon 自 9/18 起持续零产出已满 12 个自然日**）；「晚间巡检」9/25、9/26 提前约12小时触发后于 9/27 转为完全静默 | major | open |
| BUG-013 | Buglog hook 把自动化任务提示词误判为「用户报告的 bug」，会污染 buglog（**9/26、9/29、9/30 连续三期中三次稳定复现**；「同文件编辑≥2次」亦会误报「正在修 bug」，9/30 因 advice 字数压缩被触发） | minor | open |
