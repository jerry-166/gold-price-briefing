# Buglog 索引

Open: 5 | Fixed: 2 | Total: 7

| ID | Title | Severity | Status |
|---|---|---|---|
| BUG-001 | 金价早报自动化重复触发（当日已成功后再次运行） | major | open |
| BUG-002 | 金价早报调度器连续多日未触发（9/1-9/4缺失、9/5延迟至16:20） | major | open |
| BUG-003 | 金价早报调度器再次缺跑（9/6-9/7缺失、9/8延迟30分钟；9/13-9/15连续三日延迟） | major | open |
| BUG-004 | 无人值守巡检中 git push 因凭据无法交互输入而失败 | major | fixed |
| BUG-005 | 午后巡检误标为 inspection_pm 并延迟触发，污染晚间巡检日志与 manifest | major | fixed |
| BUG-006 | 金价巡检预警邮件无法发送（mail connector 不可用） | major | open |
| BUG-007 | NeoData 上海金 AU9999 返回字段异常（今开价明显不合理），且与上金所公开口径存在 2 元/克偏差 | minor | open |
