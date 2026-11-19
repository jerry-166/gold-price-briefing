---
id: BUG-026
title: JSON 生成脚本里「未被 % 格式化的字符串」写了 `%%`，daily JSON 产物残留 6 处 `%%`
severity: minor
status: fixed
found_at: 2026-11-19
tags: [percent-family, build-script, check-gap]
---

# BUG-026 JSON 产物残留字面量 `%%`

## 现象

`scripts/build_20261119.py` 生成 `daily/2026-11-19.json` 后，产物中 `prices[2].source`（美元汇率）与
`prices[3].source`（伦敦金）共残留 **6 处** `%%`，例如：

- `美元数值上升 0.01%%`
- `（−14.09／−0.38%%，昨收 3724.67`
- `日内振幅 53.78 美元／1.44%%）`
- `（−3.23%%，盘中低 3719.84`
- `现货白银 44.61（−1.01%%，昨收 45.06）`
- `一度报 3741（+0.44%%）`

`scripts/check_briefing.py` **未报错**（0 errors / OK），`%%` 会直接上站、读者在网页上看到双百分号。

## 根因

同一文件内存在两种字符串：

1. **参与 `%` 格式化的**（如 `prices[1].source` 末尾有 `% (HERO, ...)`）——这类里写 `%%` 才正确，会被折叠成 `%`；
2. **纯拼接、不参与格式化的**（`prices[2].source`、`prices[3].source` 全程没有 `% (...)`）——这类里写 `%%` 会**原样输出**。

本期把 `prices[1]` 的写法复制到 `prices[2]/[3]` 后，忘了它们没有 `%` 运算，于是 `%%` 全部漏进产物。
属**百分号家族第六代**，与 BUG-017（HTML 字面量行写 `%%`）同根同因，但首次发生在 **构建 JSON 的脚本** 而非拼 HTML 的脚本，
且首次出现「自检脚本查不出来」的检测缺口。

## 修复

1. 逐条把 6 处 `%%` 改为 `%`（用一次性替换脚本 + `assert s.count(a)==1` 保证唯一命中）。
2. 重新生成并加产物级门禁：

```
python -c "raw=open('daily/YYYY-MM-DD.json',encoding='utf-8').read(); print(raw.count('%%'))"
```

必须为 0 才算通过。

## 遗留建议

把 `%%` 残留检查并入 `scripts/check_briefing.py`：在 `walk()` 里对每个字符串加
`if '%%' in o: errs.append('literal %% in ' + path)`。
本期未改 check 脚本（避免在交付窗口动管线），已记入待办。

## 凭据

- 修复前：`raw.count('%%') == 6`；修复后：`raw.count('%%') == 0`，`check_briefing.py` OK。
- 涉及的字符串位置由 `re.finditer('%%', raw)` 逐条打印确认，非肉眼扫描。
