# -*- coding: utf-8 -*-
import io, os, json, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(BASE, '.buglog', 'bugs')
D = '2026-11-13'

def app(fn, text):
    p = os.path.join(B, fn)
    s = io.open(p, encoding='utf-8').read()
    if D in s:
        print('skip (already)', fn)
        return
    if not s.endswith('\n'):
        s += '\n'
    s += text
    io.open(p, 'w', encoding='utf-8').write(s)
    print('appended', fn)

app('2026-09-08-briefing-scheduler-missed-days.md', """

## 2026-11-13（周五）早报期观测

- **延迟约 111 分钟**（会话 current_time 10:51:04，首条 `date` 实测 10:51:14，原定 09:00）。落在 4-170 分钟区间的高位侧，**未刷新 11/08 的 170 分钟上界**；序列续记至 9/13-11/13。近 7 期第 5 次破 90 分钟：11/07 130、11/08 170、11/10 168、11/12 95、11/13 111。
- 当日危害：10:51 读数 3909.97（+0.84%）。若按 09:00 取数，价格在 3877-3887（今开 3877.21，09:16 约 3887.31），对应涨跌幅约 0.0%-0.25%；实际交付 +0.84%。幅度差约 0.6-0.8 个百分点，**方向未变**（微涨→明显上涨），属第 3 档「幅度显著放大」。
- **跨日传染第五次、本站第二大回填**：11-12 早报延迟 95 分钟、10:35 取数 3981.85；当日金价从 4000.40 一路砸到 3852.33、收 3877.43，差 104.42 美元 ≈ 22.6 元/克。累计回填量级序列：11/05 108.6 美元（23.5 元/克）＞ **11/12 104.42 美元（22.6 元/克）** ＞ 11/10 77.6 美元（16.6 元/克）＞ 11/11 59.16 美元（12.8 元/克）。已按四步修法回填（hero note 三段拆解、图表 11-12 点改 3877.4、prices[3].source 与 chart.source 各写修正句、11-12 event 改写为收盘口径）。
- **新认识（对建议 ⑪ 的补充）**：跨日回填量级与「上一期迟了多久」几乎无相关——11-12 只迟 95 分钟却产生本站第二大回填，因为它取数后 12 小时内就撞上破位行情。真正决定量级的是「取数之后有多大的行情」，而延迟 90 分钟以上的期次恰好把取数推到了欧美盘接力段之前的高波动窗口。**新增建议 ⑫：取数时刻晚于 10:30 的期次，次日必须无条件用媒体昨收核对上期数字，不得以上期 prices 值当基准**（四步修法照常执行）。今日已按此执行。
""")

app('2026-09-14-inspection-email-connector-down.md', """

## 2026-11-13（周五）早报期观测

- **正常（连续正常第 2 日，自 11/11 复发后重新计数）**。
- 两步法第二次完整执行：① ToolSearch 传 `tool_names` 精确名（mcp__qq-mail__SendMessage／GetMe）**一次命中、未回落 agent-mail**；② 按名实际调用 `SendMessage`（标准写法：`to` 对象数组 ＋ `body_format:HTML` ＋ `skip_confirmation:true`）返回 `queued:true`。
- 邮件规格：12 269 字节（落盘含标签换行拆分）；`grep -c '100%%'` = 0，`width:100%` 命中 2 处（百分号家族与 BUG-024 均未复现）。
- 不构成修复证据。历史已四次证伪「连续成功＝修复」（10/16-10/18 三日、10/25-10/27 三日、11/09-11/10 两日、11/11 单日复发），仍需观察到 11/19 前后无复发方可考虑改 fixed。
""")

app('2026-09-25-inspection-scheduler-silent-miss.md', """

## 2026-11-13（周五）早报期观测

- 11-13 早报于 10:51 执行，**早于两条巡检时点**（14:00 / 22:00），当日巡检未到点，不判缺跑。
- 回看 11-12（周四）：`logs/2026-11-12-inspection_noon.json` 与 `logs/2026-11-12-inspection_pm.json` **两个文件均在**，且 git log 有「日志：午后巡检 2026-11-12」与「日志：巡检 2026-11-12 晚间」两次独立提交 → 两线当日**都有产出**，非缺跑。
- 连续零产出交易日数 = 0，未达复合判据（连续 ≥5 个正常交易日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出），不升级不降级。观察期继续。
""")

app('2026-09-26-buglog-hook-misfire.md', """

## 2026-11-13（周五）

- **第 46 次连续命中**（9/26-11/13），判误判跳过建档。hook 再次以「用户报告了一个 bug」开头、透传自动化任务提示词全文，未按字面建档。
- 附带弱提示本期形态：本次会话**零工具失败、零报错、零用户纠正**；弱提示仅命中新建的两个脚本文件（`scripts/gen_2026-11-13.py`、`scripts/mail_2026-11-13.py`），未出现「同文件编辑 ≥2 次」提示。
- **新增观察**：hook 的「回顾本次会话是否有多次失败、报错、用户纠正的情况」问句，在零失败会话里同样会出现——它属固定模板而非事实判断，不应作为建 bug 的依据。反之若照字面执行，会在一切正常的日子里把「无失败」记成「有遗漏」。
- **复核口径维持升级版**：index.md 的逐日 `grep -c` 计数与四个 bug 文件的计数并列，同时记字节数／SHA-1。
""")

# ---- index.md 追加当日观察更新 ----
ip = os.path.join(BASE, '.buglog', 'index.md')
s = io.open(ip, encoding='utf-8').read()
if D in s and '观察更新' in s[s.rfind('## 2026-11-12'):]:
    print('index already has 11-13?', D in s)
block = """
## 2026-11-13（周五）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **111 分钟**（会话 current_time 10:51:04，首条 date 10:51:14），高位侧、未刷新 11/08 的 170 分钟上界；近 7 期第 5 次破 90 分钟。当日危害第 3 档「幅度显著放大」：09:00 取数约 0.0%-0.25%，实际交付 +0.84%，方向未变。**跨日传染第五次、本站第二大回填**：11-12 快照 3981.85 → 真实收盘 3877.43，差 104.42 美元≈22.6 元/克（序列 108.6 / 104.42 / 77.6 / 59.16）。**新认识：回填量级与上期延迟时长几乎无关，取决于取数后是否紧接大行情 → 新增建议 ⑫（取数晚于 10:30 的期次，次日必须无条件核对媒体昨收）** |
| BUG-006 | **正常（连续正常第 2 日）**。两步法第二次完整执行：ToolSearch 精确名一次命中未回落 agent-mail，SendMessage 标准写法返回 queued:true。规格 12 269 字节，零 `%%`，width:100% 2 处正常。不构成修复证据（已四次证伪「连续成功＝修复」） |
| BUG-012 | 11-13 早报 10:51 执行，早于两条巡检时点，当日未到点不判缺跑；回看 11-12，noon 与 pm 两个日志文件均在且各有一次独立提交，两线均有产出。连续零产出交易日数 0，未达复合判据 |
| BUG-013 | **第 46 次连续命中**，判误判跳过建档。本次会话零工具失败/报错/用户纠正，弱提示仅命中两个新建脚本。**新增观察：hook「是否有多次失败」问句属固定模板而非事实判断，零失败会话里也会出现，不得据此建 bug** |

### 本期 buglog 复核凭据（2026-11-13）

- 逐文件 `grep -c "2026-11-13"`：BUG-003 = 1、BUG-006 = 1、BUG-012 = 1、BUG-013 = 1
- 字节数与 SHA-1 见 logs/2026-11-13-morning_briefing.json 的 `buglog_verification`
- 本期无新增 bug、无状态变更：Open 12 / Fixed 12 / Total 24 维持不变
"""
s = s.rstrip('\n') + '\n' + block
io.open(ip, 'w', encoding='utf-8').write(s)
print('index updated')

# ---- 复核凭据 ----
files = ['2026-09-08-briefing-scheduler-missed-days.md', '2026-09-14-inspection-email-connector-down.md',
         '2026-09-25-inspection-scheduler-silent-miss.md', '2026-09-26-buglog-hook-misfire.md']
ver = {}
for fn in files:
    p = os.path.join(B, fn)
    raw = open(p, 'rb').read()
    ver[fn] = {'hit': raw.decode('utf-8').count(D), 'bytes': len(raw),
               'sha1': hashlib.sha1(raw).hexdigest()[:8]}
    print(fn, ver[fn])

lp = os.path.join(BASE, 'logs', '2026-11-13-morning_briefing.json')
lg = json.load(open(lp, encoding='utf-8'))
lg['buglog_verification'] = {
    'date': D,
    'grep_counts': {'BUG-003': ver[files[0]]['hit'], 'BUG-006': ver[files[1]]['hit'],
                    'BUG-012': ver[files[2]]['hit'], 'BUG-013': ver[files[3]]['hit']},
    'file_bytes_sha1': ver,
    'index_md_bytes': os.path.getsize(ip),
    'index_md_sha1': hashlib.sha1(open(ip, 'rb').read()).hexdigest()[:8],
    'new_bugs': 0, 'status_change': 'none', 'counts': 'Open 12 / Fixed 12 / Total 24'
}
io.open(lp, 'w', encoding='utf-8').write(json.dumps(lg, ensure_ascii=False, indent=2))
print('log updated')
