---
id: BUG-029
title: 邮件底稿文件名未区分任务类型，同日巡检与早报互相覆盖（巡检未发出的底稿被早报覆盖）
severity: minor
status: open
found_at: 2026-11-20
tags: [outbox, naming-collision, unattended]
---

# BUG-029 邮件底稿同日同名互相覆盖

## 现象

2026-11-20 是「巡检先于早报」的异常日：

1. **11:29** 晚间巡检（`inspection_pm`，提前约 10.5 小时触发）因 qq-mail 未装载，邮件未发出，
   按既有约定把 HTML 底稿落到 `.workbuddy/outbox/mail-2026-11-20.html` 待人工补发；
2. **11:35** 早报的 `mail_20261120.py` 也把底稿写到**同一路径** `.workbuddy/outbox/mail-2026-11-20.html`，
   且是 `io.open(out, "w")` 直接覆盖 —— **巡检那份待补发底稿当场被抹掉**。

结果：当日 outbox 里只剩早报那一份，巡检的预警邮件正文已不可恢复（只剩 `logs/2026-11-20-inspection_pm.json`
里的纯文本 `summary`，HTML 排版丢失）。

## 根因

底稿命名规则是 `mail-<日期>.html`，**只编码了日期、没有编码任务类型**。
在「一天只跑一个任务」的常态下不出问题；一旦出现同一天两个任务都发信失败（或「巡检先于早报」这种顺序倒置），
后写的那份必然覆盖前一份。属于**无人值守场景下的静默数据丢失**：没有任何报错，日志里也看不出来。

## 修复建议（未实施，本期仅留痕）

1. 底稿文件名加上类型后缀：`mail-2026-11-20-morning.html` / `mail-2026-11-20-inspection_pm.html`；
2. 写盘前做存在性检查：目标文件已存在且非本次任务写入 → 追加 `-2` 序号而不是覆盖；
3. 在 `logs/*.json` 里记录 `outbox_path`，便于事后对账「哪份底稿属于哪次执行」。

## 凭据

- `logs/2026-11-20-inspection_pm.json`：`status: partial`、`timestamp: 11:29 CST`、`email_sent: false`，
  自述底稿路径为 `.workbuddy/outbox/mail-2026-11-20.html`
- 同路径在 11:35 被 `scripts/mail_20261120.py` 以写模式打开并覆盖（脚本内 `io.open(out, "w", encoding="utf-8")`），
  覆盖后的文件规格为 12 484 字符／17 510 字节／62 行（早报那封）
- `.buglog/.edit_counts.json` 与 outbox 目录均不在 git 跟踪范围内，因此覆盖动作无 git 凭据，只能由两处日志的时间先后推定
