---
id: BUG-028
title: `%` 格式化串里夹带字面百分号（`−2.51%`），build 脚本抛 `TypeError: not enough arguments for format string`
severity: minor
status: fixed
found_at: 2026-11-20
tags: [percent-family, build-script, hero-note]
---

# BUG-028 `%` 格式化串里夹带字面百分号导致 TypeError

## 现象

`scripts/build_20261120.py` 首次运行即抛错，产物未生成：

```
File "scripts/build_20261120.py", line 93, in <module>
    "note": (
TypeError: not enough arguments for format string
```

出错的是 `prices[0].note`（积存金 hero 说明）—— 该字段用 `) % HERO` 做一次占位符填充，
字符串里既有 `%.1f` 占位符，又有字面百分号 `（−2.51%）`。

最小复现（已实测）：

```
>>> "折算 %.1f 元/克（−2.51%）" % 762.7
TypeError: not enough arguments for format string
>>> "折算 %.1f 元/克（+0.03 元）" % 762.7      # 去掉字面百分号即正常
'折算 762.7 元/克（+0.03 元）'
```

注意报错形态：不是 `ValueError: unsupported format character`，而是 **`TypeError: not enough arguments`** ——
`%` 后面跟的全角右括号 `）` 被当成「又一个占位符的起始」，于是解释器认为实参不足。

## 根因

**百分号家族第七代**，与前六代的共同前提完全相同：**只要「字面百分号」和「占位符」同处一个被 `%` 格式化的字符串，就必然出错**。
本期的新形态是：出错的不是 HTML、不是未被格式化的 `source`（BUG-026），而是**被格式化的长中文 `note` 字段里写了一句涨跌幅说明**——
写 note 时脑子里想的是「给读者看 −2.51%」，但这段文本恰好落在 `%` 运算的左值位置。

## 修复

把该字段（以及同批出问题的 `prices[1].source`）从 `%` 格式化改为 `.format()`，占位符写作 `{}`：

```
"... = {} 元/克 ...".format(HERO)
```

`.format()` 只解析花括号，字面 `%` 原样保留，从根上不再有「是否被格式化」的隐性前提。
改完重跑，`check_briefing.py` 一次通过（advice 185 字、pairs 11、errors 0、OK）。

## 遗留建议

1. **新写的文案字段一律优先用 `.format()` / f-string**，把 `%` 格式化限制在「纯数字拼接」的短串里；
2. `check_briefing.py` 的 `walk()` 仍查不出 `%%`（BUG-026 的遗留缺口），建议并入：
   `if '%%' in o: errs.append('literal %% in ' + path)`；
3. 本轮已在 build 脚本内置产物级门禁 `assert raw.count('%%') == 0`，两次运行均生效。

## 凭据

- 报错原文：`TypeError: not enough arguments for format string`（build_20261120.py 第 93 行）
- 最小复现两例均已实测（见上），正反例对照确认触发条件就是字面百分号
- 修复后：`python scripts/build_20261120.py` → `written daily/2026-11-20.json 28041 chars`；
  `python scripts/check_briefing.py daily/2026-11-20.json` → `errors: 0` / `OK`
