# -*- coding: utf-8 -*-
"""2026-11-14 收尾：buglog 观察更新 + 运行日志 + 日志清单。幂等守卫命中即 return。"""
import io, json, os, re, subprocess, hashlib, glob

BASE = r"D:\workspace\每日金价资讯"
D = "2026-11-14"
BUG = os.path.join(BASE, ".buglog")

def rd(p):
    return io.open(p, encoding="utf-8").read()

def app(p, text):
    s = rd(p)
    if D in s and ("## " + D) in s:
        print("skip(已含当日章节)", os.path.basename(p))
        return False
    with io.open(p, "a", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("appended", os.path.basename(p))
    return True

# ---------- 1. BUG-003 ----------
app(os.path.join(BUG, "bugs", "2026-09-05-briefing-scheduler-missed-days.md"), f"""

- **{D}（周六）延迟约 59 分钟**：会话 `<current_time>` 实测 09:58:59，首次 `date` 10:00:52。序列续记至 9/13-11/14 共 63 个日历日：…/约 111(11/13)/约 59(11/14)，回到 4-170 区间中位，未刷新 11/08 的 170 分钟上界；11/13 的大延迟未延续。
- 10/19-11/14 连续二十七个自然日全部产出（早报线），无缺跑、无提前触发。
- **本期危害 0 档（按 11/07 固化的「非交易日延迟危害恒为 0」判据）**：11-14 为周六，国际盘、上金所、外汇交易中心全部休市，价格与涨跌幅一律沿用 11-13 收盘，延迟多少分钟都取到同一个数；且 10:00 取数拿到的是完整的周五纽约收盘（3879.92），比 09:00 触发更完整。**该判据第二次生效，可作为定型结论**：危害分级必须先看「当日是否有行情」，再看分钟数。
- **跨日传染第六次**：11-13 早报快照 3909.97 → 真实收盘 3879.92，差 30.05 美元≈6.5 元/克（序列 108.6 / 104.42 / 77.6 / 59.16 / 30.05），量级继续收敛。原因是 11-13 盘中冲高 3922.99 后把涨幅全数回吐，早报 10:50 取到的正是当日高点附近。建议 ⑫（取数晚于 10:30 的期次次日无条件核对媒体昨收）本期未触发（10:00 取数），但仍按惯例核对三源：新浪 3879.92、EBC 3879.92、金投网 3884.25。
""")

# ---------- 2. BUG-006 ----------
app(os.path.join(BUG, "bugs", "2026-09-14-inspection-email-connector-down.md"), f"""
- **正常（连续正常第 3 日，自 11/11 复发后计数 1→3）**。
- 两步法第三次完整执行：① ToolSearch 传 `tool_names` 精确名（`mcp__qq-mail__SendMessage`／`GetMe`／`ListMessages`）**一次命中、未回落 agent-mail**；② 按名实际调用 `GetMe` 返回 alias `2132049351@qq.com`（scopes 含 mail:send）、`SendMessage` 返回 `queued:true`、`ListMessages(dir=sent)` 于 2026-11-14T02:03:08Z（北京时间 10:03:08）确认发出，message_id `msg_3qt5F_cDsOYN6YPRFxg0gBW4fHBS8ywhNbuKFU5Ah40GWQ`。
- 邮件规格：13 142 字符 / 18 076 字节 / 117 行 / maxline 410（远低于 1500 门禁）；`100%%` 计数 0，`width:100%` 命中 2 处。
- 不构成修复证据。历史已四次证伪「连续成功＝修复」（10/16-10/18、10/25-10/27、11/09-11/10、11/11 单日复发），现为**连续正常第 3 日**，距 11/19 观察窗结束尚有 5 日，继续逐日记录。
""")

# ---------- 3. BUG-012 ----------
app(os.path.join(BUG, "bugs", "2026-09-25-inspection-scheduler-silent-miss.md"), f"""
- {D} 早报于 10:00 执行，**早于两条巡检时点**（14:00 / 22:00），当日巡检未到点，不判缺跑。
- 回看 11-13（周五）：`logs/2026-11-13-inspection_noon.json` 与 `logs/2026-11-13-inspection_pm.json` **两个文件均在**，且 `logs/manifest.json` 头部两条分别为 `inspection_pm`（伦敦金 3883.17、振幅 1.29% 低于 1.5% 阈值、静默跳过）与 `inspection_noon`（3899.37、-0.27%），两线当日**都有产出**，非缺跑。
- 连续零产出交易日数 = 0，未达复合判据（连续 ≥5 个正常交易日零产出 且 恢复后 2 周内再现连续 ≥3 日零产出），不升级不降级。观察期继续。
""")

# ---------- 4. BUG-013 ----------
app(os.path.join(BUG, "bugs", "2026-09-26-buglog-hook-misfire.md"), f"""
- **第 47 次连续命中**，判误判跳过建档。本次 hook 把整段金价早报自动化提示词（以「你是金价早报自动化助手」开头、含第一至第七步流程编号）当作「用户报告的 bug」提交，特征与既往 46 次完全一致。
- **本期确有真实异常可记，但均属「自纠成功」而非故障**：`scripts/build_20261114.py` 的价位复算断言在首轮就拦下一处手算错误（把 3730 美元折算值写成 801.1，实测 805.3，差 4.2 元/克），若放过去会同时污染 `plan.sell.price` 与邮件正文；`trend.advice` 首稿 221 字超 200 上限，按「先写价位、再按剩余空间写判断句」压到 197 字一次通过。两者都在 commit 之前发现并改正，按既有判定**不建新 bug**。
- **附带弱提示本期形态**：`build_20261114.py` 被编辑 2 次（断言修正 + advice 压缩），`daily/2026-11-14.json` 由脚本重写 2 次。**均为生成前自纠**，非 bug 修复。
- 复核口径维持升级版：index.md 的逐日 `grep -c` 计数、四个 bug 文件计数、字节数与 SHA-1 并列。
""")

# ---------- 5. index.md ----------
idx_text = f"""
## {D}（周六）观察更新

| ID | 本期结论 |
|---|---|
| BUG-003 | 延迟约 **59 分钟**（会话 current_time 09:58:59，首条 date 10:00:52），回到中位，未刷新 11/08 的 170 分钟上界。**危害 0 档，按 11/07 固化的「非交易日延迟危害恒为 0」判据第二次生效、可作定型结论**——11-14 为周六，全部品种休市，价格与涨跌幅一律沿用 11-13 收盘，延迟不改变任何读数；10:00 取数反而拿到完整周五纽约收盘。**跨日传染第六次**：11-13 快照 3909.97 → 真实收盘 3879.92，差 30.05 美元≈6.5 元/克（序列 108.6 / 104.42 / 77.6 / 59.16 / 30.05，量级持续收敛） |
| BUG-006 | **正常（连续正常第 3 日）**。两步法第三次完整执行：精确名检索一次命中，GetMe 正常、SendMessage queued、ListMessages(dir=sent) 于 10:03:08 CST 确认（`msg_3qt5F_cDsOYN6YPRFxg0gBW4fHBS8ywhNbuKFU5Ah40GWQ`）。规格 13 142 字符 / 18 076 字节 / 117 行 / maxline 410，零 `%%`。不构成修复证据（已四次证伪「连续成功＝修复」），距 11/19 观察窗结束尚 5 日 |
| BUG-012 | 11-14 早报 10:00 执行，早于两条巡检时点，当日未到点不判缺跑；回看 11-13，noon 与 pm 两个日志文件均在、manifest 头部两条各有产出。连续零产出交易日数 0，未达复合判据 |
| BUG-013 | **第 47 次连续命中**，判误判跳过建档。本期真实异常均为自纠：`build_20261114.py` 价位断言拦下 3730 折算值手算错（写成 801.1、实测 805.3），advice 首稿 221 字压到 197 字一次过检；均在 commit 前改正，按判定不建新 bug |

### 本期 buglog 复核凭据（{D}）

"""
app(os.path.join(BUG, "index.md"), idx_text)

# ---------- 6. 凭据实测 ----------
def stats(p):
    b = io.open(p, "rb").read()
    return len(b), hashlib.sha1(b).hexdigest()

files = {
    "BUG-003": os.path.join(BUG, "bugs", "2026-09-05-briefing-scheduler-missed-days.md"),
    "BUG-006": os.path.join(BUG, "bugs", "2026-09-14-inspection-email-connector-down.md"),
    "BUG-012": os.path.join(BUG, "bugs", "2026-09-25-inspection-scheduler-silent-miss.md"),
    "BUG-013": os.path.join(BUG, "bugs", "2026-09-26-buglog-hook-misfire.md"),
    "index.md": os.path.join(BUG, "index.md"),
}
ver = {}
for k, p in files.items():
    s = rd(p)
    ver[k] = {
        "path": os.path.relpath(p, BASE).replace("\\", "/"),
        "grep_c_20261114": s.count(D),
        "grep_c_lines": len([l for l in s.split("\n") if D in l]),
        "bytes": stats(p)[0],
        "sha1": stats(p)[1],
    }
print(json.dumps(ver, ensure_ascii=False, indent=1))

# 追加凭据行到 index.md
cred = ("- 逐文件 `grep -c \"%s\"`（全文出现次数／命中行数）：BUG-003 = %d／%d、BUG-006 = %d／%d、BUG-012 = %d／%d、BUG-013 = %d／%d、index.md = %d／%d\n"
        "- 字节数与 SHA-1 见 logs/%s-morning_briefing.json 的 `buglog_verification`\n"
        "- 本期无新增 bug、无状态变更：Open 12 / Fixed 12 / Total 24 维持不变\n") % (
    D,
    ver["BUG-003"]["grep_c_20261114"], ver["BUG-003"]["grep_c_lines"],
    ver["BUG-006"]["grep_c_20261114"], ver["BUG-006"]["grep_c_lines"],
    ver["BUG-012"]["grep_c_20261114"], ver["BUG-012"]["grep_c_lines"],
    ver["BUG-013"]["grep_c_20261114"], ver["BUG-013"]["grep_c_lines"],
    ver["index.md"]["grep_c_20261114"], ver["index.md"]["grep_c_lines"],
    D)
s = rd(os.path.join(BUG, "index.md"))
if "本期 buglog 复核凭据（%s）" % D in s and "逐文件 `grep -c" in s.split("本期 buglog 复核凭据（%s）" % D)[1]:
    print("skip(凭据行已存在)")
else:
    with io.open(os.path.join(BUG, "index.md"), "a", encoding="utf-8", newline="\n") as f:
        f.write(cred)
    print("appended 凭据行")

# ---------- 7. 运行日志 ----------
steps = [
    {"num": 1, "name": "获取数据", "status": "success", "duration_ms": 95000,
     "result": ("伦敦金 11-13 收盘 3879.92(+2.49／+0.06%，高 3922.99、低 3867.55)；上海金 Au99.99 日盘收 837.55(-1.62%)、夜盘收 837.00；"
                "中间价 6.7152(周六不更新，沿用)、在岸即期 6.6707；10 月 PPI 环比 +0.3%、同比 6.5%；SPDR 持仓 1044.408 吨(+3.705)；本周累跌 190.83 美元(-4.69%)"),
     "source": "新浪财经实时接口 hf_XAU／gds_AU9999 + WebSearch（汇通财经、金投网、金融界、华尔街见闻、EBC、FXStreet、中国货币网）"},
    {"num": 2, "name": "生成早报JSON", "status": "success", "duration_ms": 72000,
     "result": "已写入 daily/2026-11-14.json；check_briefing.py 首轮 0 error（advice 197 字、pairs 10 组）；11-13 图表点由快照 3909.97 回填为真实收盘 3879.9"},
    {"num": 3, "name": "更新manifest", "status": "success", "duration_ms": 4000,
     "result": "已在 manifest.json 的 briefings 数组头部插入 2026-11-14（共 85 条）"},
    {"num": 4, "name": "Git推送", "status": "success", "duration_ms": 11000,
     "result": "commit 3a408fc，SSH 推送 master；git rev-parse HEAD 与 git ls-remote origin refs/heads/master 一致"},
    {"num": 5, "name": "发送邮件", "status": "success", "duration_ms": 67000,
     "result": "已发送至 2132049351@qq.com，10:03:08 CST 在 sent 目录确认（msg_3qt5F_cDsOYN6YPRFxg0gBW4fHBS8ywhNbuKFU5Ah40GWQ）；13 142 字符 / 18 076 字节 / 117 行 / maxline 410",
     "outputs": [{"label": "邮件内容", "body": "主题：🌅 今日金价早报 | 2026年11月14日 周六；正文含周六休市提示、金价快照（积存金 837.7／AU9999 837.00／汇率 6.72／伦敦金 3879.9）、昨夜大事 5 条（PPI 落地、周线重挫、鹰派集体、国内补跌、下周日程）、趋势判断与 5 组买卖价位、今日学一招（PPI 低于预期为何金价只反弹一小时）、网站链接"}]},
]
total = sum(s["duration_ms"] for s in steps)
log = {
    "date": D,
    "type": "morning_briefing",
    "status": "success",
    "summary": "10:00 触发（延迟约 59 分钟，周六休市、危害 0 档）；五步全成，邮件已发出；11-13 伦敦金图表点回填为真实收盘 3879.9（差 30.05 美元≈6.5 元/克）",
    "timestamp": "10:00 CST",
    "gap_check": {"last_success_briefing": "2026-11-13", "missed_trading_days": [], "note": "距上次成功早报 1 个自然日，无断档"},
    "steps": steps,
    "summary_stats": {"total_steps": 5, "success_steps": 5, "failed_steps": 0,
                      "total_duration_ms": total, "email_sent": True, "git_pushed": True},
    "buglog_verification": ver,
}
lp = os.path.join(BASE, "logs", "%s-morning_briefing.json" % D)
with io.open(lp, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(log, ensure_ascii=False, indent=1))
print("written", lp, "total_ms", total)

# ---------- 8. logs/manifest.json ----------
mp = os.path.join(BASE, "logs", "manifest.json")
m = json.loads(rd(mp))
if not any(x["date"] == D and x["type"] == "morning_briefing" for x in m["logs"]):
    m["logs"].insert(0, {"date": D, "type": "morning_briefing", "status": "success",
                         "summary": "10:00 触发（延迟约 59 分钟，周六休市、危害 0 档）；五步全成，邮件已发出；11-13 伦敦金图表点回填为真实收盘 3879.9"})
    with io.open(mp, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(m, ensure_ascii=False, indent=1) + "\n")
    print("manifest prepended, total", len(m["logs"]))
else:
    print("skip(manifest 已有当日记录)")
