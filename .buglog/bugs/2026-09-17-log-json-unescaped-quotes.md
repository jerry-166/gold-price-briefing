---
id: BUG-009
title: 早报运行日志 JSON 因正文内联 ASCII 直双引号未转义而解析失败
status: fixed
severity: minor
source: automation-hook
reported_at: 2026-09-17T10:40:00+08:00
fixed_at: 2026-09-17T10:45:00+08:00
files:
  - path: logs/2026-09-17-morning_briefing.json
    line: 46
    root_cause: "在 step5 的 outputs[].body（邮件正文摘要）里，直接用 ASCII 直双引号 `\"` 包裹中文引文（如 沃什表态\"通胀太高……\"），该引号与 JSON 字符串定界符同字符，未加反斜杠转义，提前终止了字符串"
    fix: "把正文内的 ASCII 直引号改为中文全角引号 “ ”，并在提交前用 python -c json.load 校验；后续写作规范：JSON 字符串内引用中文内容一律用 “ ” 或 『 』，禁用 ASCII 直引号"
tags: [automation, json, encoding]
related_bugs: []
---

## 早报运行日志 JSON 因正文内联 ASCII 直双引号未转义而解析失败

### 现象
- 2026-09-17 早报流程 step6 写入 `logs/2026-09-17-morning_briefing.json` 后，按惯例用 `python -c "json.load(...)"` 做结构校验，报错：
  `json.decoder.JSONDecodeError: Expecting ',' delimiter: line 46 column 425 (char 1951)`
- 出错位置在 `steps[4].outputs[0].body`（邮件正文摘要）中，紧邻 `②沃什鹰派表态"通胀太高且持续太久"、"今夏数据未显示基本趋势显著改善"` 这段文字。
- 由于 JSON 已损坏，`git add logs/ && git commit` 这一命令链因前置校验失败而未执行，日志与 logs/manifest.json 的推送被阻塞（后续修复后重跑成功，commit 7ab3389）。

### 根因分析
- **字符同形冲突**：JSON 规范只承认 ASCII 直双引号 `U+0022` 作为字符串定界符。邮件正文里为标注「沃什原话」使用了同字符的直双引号，解析器在该处认为字符串已结束，紧随其后的 `通胀太高且持续太久` 就不再是合法 JSON 值，于是报 `Expecting ',' delimiter`。
- **为什么这次才暴露**：此前几日的日志 `body` 字段均为叙述性文字，未出现引号包裹的引语；本次恰好要摘录沃什记者的原话（"通胀太高了，并且已经持续了太长时间"），第一次引入内联引号，触发了这个潜伏问题。
- **更深层原因**：写 JSON 时用的是「自然语言写作」的直觉（中文里习惯直接加 `"`），而非「序列化」的直觉（应让序列化库决定转义）。当我用 Write 工具直接手写 JSON 文本时，就丢失了 `json.dumps` 的自动转义保护。
- 同类风险点：`daily/YYYY-MM-DD.json` 的 `explain`/`detail`/`title` 字段同样大量包含中文引语，本次恰好未用到 ASCII 直引号（用了 『』和 →），属于**侥幸未中**，属同一类隐患。

### 修复过程
1. 用 `io.open(...).read()` 定位到具体行与列（line 46 / char 1951），确认只有两处引号问题：
   - `沃什鹰派表态"通胀太高且持续太久"、"今夏数据未显示基本趋势显著改善"`
   - `"美元强+收益率高"是黄金最难受的组合`
2. 用正则 `.{18}".{18}` 全量扫描文件，确认除 JSON 结构引号外已无残留 ASCII 直引号，避免漏改。
3. 通过 Edit 将上述两处的 ASCII `"` 替换为中文全角 `“ ”`。
4. 重新执行 `json.load` 校验通过（`log OK 2026-09-17 morning_briefing success {...}`），随后 `git add logs/ && git commit && git push` 成功。

### 经验教训
- **手写 JSON 一律禁用 ASCII 直双引号引中文**：需要引用中文内容时用 `“ ”`、`『 』` 或 `→` 串联；只有 `json.dumps` 生成的输出才可以自动转义。这条应固化为早报/巡检流程的写作规范。
- **写入即校验，校验失败即阻断提交**：本次因为校验排在 `git commit` 之前，损坏的日志没有进入仓库，这是正确姿势，应当保持（命令链 `python -c json.load && git add && git commit && git push`）。
- **不要只改报错点**：报错会停在第一个错误，后面往往还有同类问题。定位到错误行后，应当用正则/脚本全量扫描一次同类字符，一次性改完。
- 更彻底的做法：考虑改为「先用 Python dict 构造数据，再用 `json.dump(..., ensure_ascii=False)` 落盘」，从根上消除手写 JSON 的转义风险。
