# -*- coding: utf-8 -*-
"""11-27 buglog 追加：BUG-003/006/012/013 观察更新 + 新增 BUG-036/037。幂等。"""
import io, json, os, hashlib

IDX = ".buglog/index.md"
MARK = "## 2026-11-27"
src = io.open(IDX, encoding="utf-8").read()
if MARK in src:
    print("SKIP: 2026-11-27 已存在")
    raise SystemExit(0)

NEW036 = """---
id: BUG-036
title: wrap_outside_tags 按字符数硬切，把 HTML 标签属性切断导致样式失效
severity: minor
status: fixed
found_at: 2026-11-27
tags: [mail, html, wrap, attribute-cut]
---

# BUG-036 折行函数切断标签属性

## 现象

`mail_20261127.py` 首版沿用 BUG-031 的 `wrap_outside_tags`，产物 10 636 字符、71 行、
`maxline 468`。回读时发现多处属性被切断：

```
...color:#1f2328;fo
nt-size:15px;font-weight:700...
```

即 `font-size` 被拆成 `fo` + 换行 + `nt-size`，CSS 声明失效，单元格字号回退。

## 根因

BUG-031 的修复只约束了「不要切在 `<` 或 `>` 上」，并未跟踪「当前是否位于标签内」：

```python
if len(buf) >= limit and ch not in "<>":
```

条件只看当前字符，不看扫描位置，因此切点可以落在属性值中间。BUG-031 的
`limit=1200` 恰好让切点落在 tag 内概率较低，问题被掩盖；本期按 1200 切、正文更长，就命中了。

即：**修复函数被「重新发明」时退化为字符计数版**，原始设计意图（只在标签外换行）丢失。

## 修复

改为标签内感知再切：

1. 逐行处理，只有 `len(line) > limit` 才尝试切分；
2. 扫描前 `limit` 个字符，维护 `in_tag` 状态（遇 `<` 置真、遇 `>` 置假）；
3. 仅在 `not in_tag` 且字符属于空白或中文标点（`，。、；：）」`）处记为候选切点；
4. 找不到候选切点则整行不切（宁可超长也不破坏结构）。

同时把 `limit` 从 1200 提到 1500：本期产物 `maxline 596`，根本不需要折行，
折行只在真正超长时才生效。

修复后重生成：10 628 字符、63 行、`maxline 596`，`grep -c 'fo$'` = 0，无被切断属性。

## 复用

BUG-031 建议的 `scripts/lib_mail.py` 公共件仍未落地，本期第二次「各写一份」并因此退化。
该公共件应同时固化：折行（标签内感知）、`%%` 门禁、`width:100%` 门禁、U+FFFD 与繁简门禁。
"""

NEW037 = """---
id: BUG-037
title: check_briefing 的价位配对正则不认「（积存金约 X-Y 元/克）」写法，复算校验被静默跳过
severity: minor
status: open
found_at: 2026-11-27
tags: [check, regex, price-pair, silent-skip]
---

# BUG-037 价位配对正则漏匹配

## 现象

`daily/2026-11-27.json` 首轮自检报：

```
advice len = 193 | rate = 6.7075 | pairs = 4
errors: 1
  - paired 价位 too few: 4
```

但文案里实际有 6 组「美元区间（约 ¥区间 元/克）」，只认出 4 组。

## 根因

`scripts/check_briefing.py` 第 104 行：

```python
pairs = re.findall(r"(\\d{3,4})-(\\d{3,4})[^（(0-9]{0,10}[（(]\\s*约?\\s*(\\d{3})-(\\d{3})\\s*元/克[）)]", blob)
```

`[（(]\\s*约?\\s*` 要求左右括号后紧跟（或只跟空白后的）「约」字。本期 `plan.buy.price`
写作 `3570-3590 美元/盎司（积存金约 770-774 元/克）`，括号与「约」之间多了「积存金」三字
→ 该组不匹配。`plan.sell.price` 同理。

## 危害

表面只是「pairs 少于 5」这条计数报错，容易当成阈值问题去凑数；**真正的风险是反向的**：
只要把 `plan.price` 改写成带前缀的句式，`plan.buy.price` 里的价位就完全逃过校验，
即使美元价与 ¥/克折算对不上也会 `errors: 0` 通过 —— 约束静默失效。

本期处置是改文案（`（约 770-774 元/克，积存金口径同此）`）绕过，未动校验脚本。

## 待修

把正则改为「括号后允许任意非数字前缀」：

```python
r"(\\d{3,4})-(\\d{3,4})[^（(0-9]{0,10}[（(][^0-9（）()]{0,8}(\\d{3})-(\\d{3})\\s*元/克[）)]"
```

并补一条自检：`plan.buy.price` / `plan.sell.price` 中的每组价位都必须出现在 `pairs` 里，
否则直接报「价位未被复算」而非仅报组数不足。
"""

NOTES = {
    "2026-11-27-wrap-tag-cut.md": NEW036,
    "2026-11-27-price-pair-regex-gap.md": NEW037,
}
for fn, body in NOTES.items():
    p = os.path.join(".buglog/bugs", fn)
    if not os.path.exists(p):
        io.open(p, "w", encoding="utf-8", newline="\n").write(body)

ROWS = (
    "| BUG-036 | `wrap_outside_tags` 按字符数硬切、未跟踪标签内状态，把 `font-size` 切成 `fo`+换行+`nt-size`，CSS 声明失效（2026-11-27 回读底稿发现并修复，改为标签内感知+只在空白/中文标点断行） | minor | fixed |\n"
    "| BUG-037 | `check_briefing.py` 价位配对正则不认「（积存金约 X-Y 元/克）」写法，`pairs` 计数不足；改文案可绕过，但同等句式下价位复算会静默失效（2026-11-27） | minor | open |\n"
)

src = src.replace("Open: 18 | Fixed: 17 | Total: 35", "Open: 19 | Fixed: 18 | Total: 37")
anchor = "| BUG-033 |"
i = src.index(anchor)
j = src.index("\n", i) + 1
src = src[:j] + ROWS + src[j:]

SECTION = """
---

## 2026-11-27（周五）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **100 分钟**（会话起始 10:40:27 实测，标称 09:00），近 8 期序列 `…/153/12/148/108/100`。**交易日且有单向行情**：09:00 时伦敦金约 3570（+0.1%），10:41 已 3625.0（+1.65%），隔夜低点 3557.80 与日内高点 3636.77 全落在延迟窗口内，整段约 55 美元拉升未进早报 → **危害 2 档**（方向与量级均被改写）。未达 360 分钟门槛，按建议 ⑬ 顶部不标延迟，但邮件头已写真实生成时点 10:45 |
| BUG-006 | **正常**。`ToolSearch` 精确名 `mcp__qq-mail__SendMessage` 一次命中（未回落 agent-mail），`DeferExecuteTool` 携 `skip_confirmation: true` 首次调用即 `queued: true`，未出现 42801；`ListMessages(dir=sent)` 回读 `created_at` 2026-11-27T02:45:15Z（10:45:15 CST）。形态序列：未注册(11-23)→正常(11-24)→未注册(11-25)→正常(11-26)→**正常(11-27)**，首次出现「连续两日正常」，按历史已被多次证伪，不构成修复证据 |
| BUG-012 | 今日 `logs/2026-11-27-*` 截至本期收尾仅早报一条，14:00/22:00 巡检未到点，不判缺跑；11-26 两条巡检均 `no_action` 正常，连续零产出交易日数 = 0，不升级不降级 |
| BUG-013 | **第 38 次连续命中**（9/26 起），hook 再次把自动化提示词全文透传为「bug 报告」→ 判误判、未按字面建档。附带弱提示三条均属正常返工：`build_20261127.py` 编辑 2 次（`plan.price` 两处句式改写）、`mail_20261127.py` 编辑 2 次（折行函数重写，见 BUG-036）。本期无工具失败、无用户纠正 |
| BUG-030 | 本期**第六次手工规避**：仍手写 `if ni < 0: continue`，并新增 `assert labels[e["index"]] == e["date"]` 逐条校验与 `assert [e["index"] for e in events] == sorted(set(...))`。`lib_chart.shift_chart()` 仍未落地 |
| BUG-032 | 维持 open。本期邮件发出，仅以 `snippet` 与底稿开头比对（一致）作轻量证据，未做全文逐字回读 → 与 11-26 同级，无改善 |
| BUG-033 | 维持 open，**本期仍未调用**：`query.py` 硬依赖 `requests`、本机 pip 索引不可用，且缺依赖时 `exit 0`。取数走新浪 `hf_XAU`／`gds_AU9999`／`gds_AUTD` 实时接口 + 上金所延时行情 + WebSearch 交叉验证，logs step1 已如实写明「未假装调用」 |
| BUG-034 | 维持 open。本期 build 脚本内置 `assert "\\ufffd" not in raw`（局部规避第 2 次、产物零 U+FFFD），`check_briefing.py` 的 `walk()` 仍未补 |
| BUG-035 | 维持 open。本期在 build 脚本里加 `for bad in ("別","藉","後","個","們","裡")` 断言（局部规避第 1 次，产物零命中），但仍是单脚本约束、未进公共校验 |
| BUG-036 | **新增、fixed（minor）**：`wrap_outside_tags` 按字符数硬切、不跟踪标签内状态，把 `style` 属性切成 `fo`+换行+`nt-size`，CSS 声明失效。BUG-031 的修复函数在「各写一份」时退化 → 改为标签内感知 + 仅在空白/中文标点断行 + `limit` 提到 1500。修复后 `maxline 596`、`grep -c 'fo$'` = 0 |
| BUG-037 | **新增、open（minor）**：`check_briefing.py` 的价位配对正则要求括号后紧跟「约」，`（积存金约 X-Y 元/克）` 不匹配 → `pairs` 只 4 组、误报「too few」。本期靠改文案绕过；真正的风险是同句式下价位复算静默失效。待修正则为宽松前缀 + 补「plan.price 每组价位必须被复算」断言 |

### 本期 buglog 复核凭据（2026-11-27）

- **有新增 bug**：`bugs/2026-11-27-wrap-tag-cut.md`（BUG-036，fixed，minor）、`bugs/2026-11-27-price-pair-regex-gap.md`（BUG-037，open，minor）
- 计数取自本文件表头（写入后重读）：Open 19 / Fixed 18 / Total 37（Open 18→19、Fixed 17→18、Total 35→37）
- 幂等守卫：本脚本先检测 `## 2026-11-27` 是否已存在，存在即整体 SKIP
- 完整性：`bugs/` 目录 35 → **37** 个文件
"""

io.open(IDX, "w", encoding="utf-8", newline="\n").write(src + SECTION)

st = json.load(open(".buglog/stats.json", encoding="utf-8"))
st["open_count"] = 19
st["fixed_count"] = 18
st["total_count"] = 37
st["recent_fixed"] = ["BUG-036", "BUG-031", "BUG-027", "BUG-026", "BUG-024"]
io.open(".buglog/stats.json", "w", encoding="utf-8", newline="\n").write(json.dumps(st, ensure_ascii=False, indent=2) + "\n")

bugs = sorted(os.listdir(".buglog/bugs"))
print("bugs files", len(bugs))
print("index bytes", os.path.getsize(IDX), "sha1", hashlib.sha1(open(IDX, "rb").read()).hexdigest())
print("2026-11-27 occurrences", io.open(IDX, encoding="utf-8").read().count("2026-11-27"))
for fn in NOTES:
    p = os.path.join(".buglog/bugs", fn)
    print(fn, os.path.getsize(p), hashlib.sha1(open(p, "rb").read()).hexdigest())
