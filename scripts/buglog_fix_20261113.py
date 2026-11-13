# -*- coding: utf-8 -*-
import io, os, json, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ip = os.path.join(BASE, '.buglog', 'index.md')
s = io.open(ip, encoding='utf-8').read()

H = '## 2026-11-13（周五）观察更新'
first = s.find(H)
second = s.find(H, first + 1)
if second != -1:
    s = s[:second].rstrip('\n') + '\n'
    print('dedupe ok, removed', len(s))
else:
    print('no duplicate')

# 主表新增 BUG-025 行（插在 BUG-024 行后）
anchor = '（2026-11-09 发送前由生成脚本的 `maxline` 自检拦下；首次出现「产物正确、链路断在读取」形态） | major | fixed |'
row = (anchor + '\n| BUG-025 | buglog 追加脚本的幂等守卫只写了 skip 分支、缺少 else，'
       '重跑脚本时 `.buglog/index.md` 被重复追加一份当日「观察更新」并已推送（2026-11-13 收尾发现并修复；'
       '与 BUG-014 同源——都是「重复执行没有真正幂等」） | minor | fixed |')
if 'BUG-025' not in s:
    assert anchor in s
    s = s.replace(anchor, row, 1)
    s = s.replace('Open: 12 | Fixed: 12 | Total: 24', 'Open: 12 | Fixed: 13 | Total: 25', 1)
    print('row added')
else:
    print('row exists')

# 当日章节补记
add = ('\n### 本期收尾事故（2026-11-13，新增 BUG-025）\n\n'
       '- 收尾时把 `.buglog/index.md` 的复核计数行从「=1」改为行数口径「=2」，为同步凭据重跑了一次追加脚本；'
       '该脚本的幂等守卫写成 `if D in s and ...: print(...)`，**两个分支后面都执行追加**、缺 else 提前 return，'
       '导致 index.md 落了两份 11-13「观察更新」并已随提交推送。\n'
       '- 修复：截断第二份重复段落；脚本守卫改为命中即 `return`。教训与 BUG-014 同源——**「有幂等检查」不等于「幂等生效」，'
       '检查完必须真的提前退出**，否则检查本身只是日志。\n'
       '- 计数不变式复核：四个 bug 文件各含当日 1 段（BUG-013 为 2 行命中），index.md 当日章节 1 份。\n')
if '本期收尾事故（2026-11-13' not in s:
    s = s.rstrip('\n') + '\n' + add
    print('addendum added')

io.open(ip, 'w', encoding='utf-8').write(s)

# 新建 bug 文件
bp = os.path.join(BASE, '.buglog', 'bugs', '2026-11-13-buglog-append-idempotency.md')
if not os.path.exists(bp):
    io.open(bp, 'w', encoding='utf-8').write("""# BUG-025 buglog 追加脚本幂等守卫缺失，重跑即重复写入

- **发现日期**：2026-11-13
- **严重度**：minor
- **状态**：fixed
- **影响面**：`.buglog/index.md`（当日推送后多出一份 11-13「观察更新」重复段落）

## 现象

11-13 早报收尾时，把 index.md 复核凭据里的 `grep -c` 计数由「=1」改成行数口径「=2」，为了同步凭据重跑了一次
`scripts/buglog_20261113.py`。重跑后 index.md 末尾出现了**第二份完整的「## 2026-11-13（周五）观察更新」**，
且已随 `日志：早报 2026-11-13（含 buglog 观测与复核凭据）` 提交推送（commit 9abfac0）。

## 根因

脚本的幂等守卫写成了：

```
if D in s and '观察更新' in s[s.rfind('## 2026-11-12'):]:
    print('index already has 11-13?', D in s)
block = ...
s = s.rstrip() + block      # 无论上面的判断结果如何都会执行
```

判断分支里只有 `print`、**没有 `return` 或 `else` 包裹追加逻辑**，所以「检查通过」这个动作什么也没有阻止。
四个 `app()` 写 bug 文件的函数有 `return`，因此只有 index.md 受害——这也解释了为什么重跑只污染了一个文件。

## 为什么没被自检拦下

`check_briefing.py` 只校验 `daily/*.json`，不覆盖 `.buglog/`；而「重复追加」不产生非法 JSON、不产生 ASCII 引号，
属于结构正确但内容重复的一类，只能靠**段落计数**发现。

## 修复

1. 截断第二份重复段落（保留经过口径修正的第一份）；
2. 脚本守卫改为 `if D in s: print(...); return`（命中即提前退出）；
3. 复核不变式改为「段落计数」：`grep -c '^## 2026-11-13（周五）观察更新' .buglog/index.md` 必须等于 1。

## 教训

与 BUG-014（自动化中断后重跑产生半成品残留）同源：**「有幂等检查」不等于「幂等生效」**。
检查之后必须真的提前退出，否则检查本身只是一行日志，反而是最危险的假安全感。
今后凡写「重跑安全」的收尾脚本，一律先跑两遍、用计数验证，再提交。
""")
    print('bug file created')

# 复核凭据更新
lp = os.path.join(BASE, 'logs', '2026-11-13-morning_briefing.json')
lg = json.load(open(lp, encoding='utf-8'))
files = ['2026-09-08-briefing-scheduler-missed-days.md', '2026-09-14-inspection-email-connector-down.md',
         '2026-09-25-inspection-scheduler-silent-miss.md', '2026-09-26-buglog-hook-misfire.md']
ver = {}
for fn in files:
    raw = open(os.path.join(BASE, '.buglog', 'bugs', fn), 'rb').read()
    ver[fn] = {'hit': raw.decode('utf-8').count('2026-11-13'), 'bytes': len(raw),
               'sha1': hashlib.sha1(raw).hexdigest()[:8]}
lg['buglog_verification'] = {
    'date': '2026-11-13',
    'grep_counts_lines': {'BUG-003': 1, 'BUG-006': 1, 'BUG-012': 1, 'BUG-013': 2},
    'file_bytes_sha1': ver,
    'index_md_bytes': os.path.getsize(ip),
    'index_md_sha1': hashlib.sha1(open(ip, 'rb').read()).hexdigest()[:8],
    'index_section_count_1113': s.count(H),
    'new_bugs': 1, 'status_change': 'BUG-025 新增并标记 fixed',
    'counts': 'Open 12 / Fixed 13 / Total 25',
    'incident': '收尾重跑 buglog 脚本时 index.md 重复追加一份 11-13 章节（9abfac0 已推送），已截断修复并登记 BUG-025'
}
io.open(lp, 'w', encoding='utf-8').write(json.dumps(lg, ensure_ascii=False, indent=2))
print('log updated; section count =', s.count(H), '| bytes', os.path.getsize(ip), '| sha1',
      hashlib.sha1(open(ip, 'rb').read()).hexdigest()[:8])
