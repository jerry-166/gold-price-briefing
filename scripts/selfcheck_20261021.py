# -*- coding: utf-8 -*-
"""早报自检：结构 + 引号 + 价位一致性 + 换算复算。"""
import json
import re

D = 'daily/2026-10-21.json'
d = json.load(open(D, encoding='utf-8'))

assert d['date'] == '2026-10-21' and d['weekday'] == '周三'
ch = d['chart']
assert len(ch['labels']) == len(ch['values']) == 30, (len(ch['labels']), len(ch['values']))
assert max(e['index'] for e in ch['events']) < 30
for e in ch['events']:
    assert ch['labels'][e['index']] == e['date'], (e['date'], ch['labels'][e['index']])
assert all(n['url'].startswith('http') for n in d['news'])
assert d['trend']['action'] in ('hold', 'buy', 'watch')

adv = re.sub(r'<[^>]+>', '', d['trend']['advice'])
print('advice len(no tags) =', len(adv))
assert len(adv) <= 200

DQ = chr(34)
bad = []
def walk(o, p=''):
    if isinstance(o, str):
        if DQ in o:
            bad.append(p)
    elif isinstance(o, dict):
        for k, v in o.items():
            walk(v, p + '.' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, p + '[' + str(i) + ']')
walk(d)
print('ASCII double-quote in text fields:', len(bad), bad[:5])
assert not bad

R = 6.7192
cny = lambda usd: usd * R / 31.1035
checks = {
    'hero 4119.64': (round(cny(4119.64), 1), 890.0),
    '4100': (round(cny(4100)), 886),
    '4106': (round(cny(4106.23)), 887),
    '4073': (round(cny(4073.30)), 880),
    '4080': (round(cny(4080)), 881),
    '4060': (round(cny(4060)), 877),
    '4066': (round(cny(4066.30)), 878),
    '4131': (round(cny(4131.79)), 893),
    '4140': (round(cny(4140)), 894),
    '4155': (round(cny(4155)), 898),
    '4165': (round(cny(4165)), 900),
    '4200': (round(cny(4200)), 907),
}
for k, (got, exp) in checks.items():
    print(f'{k}: calc={got} expect={exp} {"OK" if got == exp else "MISMATCH"}')
    assert got == exp, (k, got, exp)

print('instance diff:', round(cny(4119.64) - cny(4119.64) * 0 - (4119.64 * 6.6791 / 31.1035), 1))
print('change:', round((4119.64 / 4124.70 - 1) * 100, 2))
print('ALL CHECKS PASSED')
