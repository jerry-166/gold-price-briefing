# Buglog 索引

Open: 6 | Fixed: 4 | Total: 10

| ID | Title | Severity | Status |
|---|---|---|---|
| BUG-001 | 金价早报自动化重复触发（当日已成功后再次运行） | major | open |
| BUG-002 | 金价早报调度器连续多日未触发（9/1-9/4缺失、9/5延迟至16:20） | major | open |
| BUG-003 | 金价早报调度器再次缺跑（9/6-9/7缺失；9/13-9/19连续七日延迟、峰值74分钟；9/20回落至7分钟） | major | open |
| BUG-004 | 无人值守巡检中 git push 因凭据无法交互输入而失败 | major | fixed |
| BUG-005 | 午后巡检误标为 inspection_pm 并延迟触发，污染晚间巡检日志与 manifest | major | fixed |
| BUG-006 | 金价巡检预警邮件无法发送（mail connector 不可用） | major | open |
| BUG-007 | NeoData 上海金 AU9999 报价异常（9/15字段矛盾、9/17水平偏离官方5元/克），处理策略已转为官方源优先 | minor | open |
| BUG-008 | NeoData 技能令牌过期（TOKEN_EXPIRED），无人值守巡检无法以 NeoData 为优先数据源 | minor | open |
| BUG-009 | 早报运行日志 JSON 因正文内联 ASCII 直双引号未转义而解析失败 | minor | fixed |
| BUG-010 | 早报 JSON 与运行日志中手工录入内容出现笔误（来源 URL 域名错误、价位数字转录错误） | minor | fixed |

