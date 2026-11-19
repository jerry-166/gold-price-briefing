# -*- coding: utf-8 -*-
"""追加 2026-11-19 的 buglog 观察小节 + 更新表头计数（幂等：小节已存在即跳过）"""
import os, json, hashlib, io

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(BASE, '.buglog', 'index.md')
STATS = os.path.join(BASE, '.buglog', 'stats.json')
DAY = '2026-11-19'

s = io.open(IDX, encoding='utf-8').read()

if ('## ' + DAY) in s:
    print('SKIP: 当日小节已存在')
else:
    section = io.open(os.path.join(BASE, 'scripts', '_section_20261119.md'), encoding='utf-8').read()
    if not s.endswith('\n'):
        s += '\n'
    s = s + '\n' + section
    io.open(IDX, 'w', encoding='utf-8').write(s)
    print('appended', DAY)

# 表头计数：BUG-026/027 当日 fixed → Fixed 13→15，Total 25→27，Open 不变
s = io.open(IDX, encoding='utf-8').read()
old = 'Open: 12 | Fixed: 13 | Total: 25'
new = 'Open: 12 | Fixed: 15 | Total: 27'
if old in s:
    s = s.replace(old, new, 1)
    io.open(IDX, 'w', encoding='utf-8').write(s)
    print('header updated ->', new)
elif new in s:
    print('header already updated')
else:
    print('WARN: header pattern not found')

raw = io.open(IDX, 'rb').read()
print('index bytes', len(raw), 'sha1', hashlib.sha1(raw).hexdigest()[:12], 'day_count', raw.decode('utf-8').count(DAY))

st = {'open_count': 12, 'fixed_count': 15, 'total_count': 27,
      'recent_fixed': ['BUG-027', 'BUG-026', 'BUG-024', 'BUG-023', 'BUG-022']}
io.open(STATS, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2))
print('stats written')
