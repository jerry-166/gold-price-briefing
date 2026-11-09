# BUG-024 `''.join()` 抹掉换行，邮件 HTML 变成 2202 字符单行，触发 Read 2000 字符截断

- **ID**: BUG-024
- **发现日期**: 2026-11-09
- **严重度**: major
- **状态**: fixed
- **关联**: 无（新形态）

## 现象

`scripts/mail_20261109.py` 生成邮件 HTML 后打印统计：

```
chars 10580 bytes 14935
lines 69 maxline 2202
```

`maxline` 为 2202，超过 Read 工具 2000 字符的单行截断上限。若照常 `Read` 该文件再传给
`SendMessage` 的 `body`，正文会在 2000 字符处被截断 —— 邮件会变成**半截 HTML**（标签不闭合、
后半段内容全部丢失），而脚本本身不会报任何错，`SendMessage` 也会正常 queued。

本期在发送前发现了该风险（生成脚本自带 `maxline` 打印），改为 `chr(10).join()` 后
`maxline` 降到 576，再读取发送，未造成实际事故。

## 根因

邮件 HTML 由 4 个片段拼成：`price_rows`（4 行表格）、`news_html`（4 条新闻）、
`trend_html`（3 段趋势）、主模板。前三个片段用 `''.join(...)` 拼接列表元素：

```python
price_rows = ''.join(price_rows)
news_html = ''.join(news_html)
```

每个列表元素是一段 **不含换行的单行 f-string**（HTML 标签天然连写），`''.join()` 于是把
4 条新闻的完整标签串成**一整行 2202 字符**。

关键点在于：**HTML 对空白不敏感，所以"一行写完"在浏览器/邮件客户端里完全正常**，
脚本输出、`chars`、`bytes` 统计全部正常，唯一会出问题的是**中间环节 —— 需要把文件内容
读进内存再当参数传给工具时**。而 Read 的 2000 字符单行截断是静默的（截断后不含任何标记），
下游拿到的字符串依然"看起来像 HTML"。

这是本项目第一次出现「生成正常、传输截断」的故障形态：**产物正确，链路断在读取**。

## 修复

三处 `''.join(...)` 改为 `chr(10).join(...)`：

```python
price_rows = chr(10).join(price_rows)
news_html = chr(10).join(news_html)
trend_html = chr(10).join([...])
```

并在生成脚本末尾固化三条自检，作为发送前的门禁：

```python
print('lines', html.count(chr(10)) + 1, 'maxline', max(len(x) for x in html.split(chr(10))))
```

- `maxline <= 1500` 才允许进入"读取→发送"环节；
- `100%% count == 0`（百分号家族门禁）；
- `chars/bytes` 记录进日志，供次日比对体积突变。

修复后 `maxline` 2202 → 576，`lines` 69 → 77，`chars` 10580 → 10588（仅多 8 个换行符，内容不变）。

## 教训

- **凡"生成文件 → Read 读回 → 作为工具入参"的链路，都必须保证单行 < 2000 字符**。
  这条约束与 HTML 本身无关，是传输层的限制，但 HTML 恰好最容易踩中（标签连写、无自然换行）。
- 拼接 HTML 片段时**默认用换行符 join**，不要用空串。空串 join 的唯一好处是省几个字节，
  代价是把整篇文档压成一行，任何按行读取的下游都会被截断。
- 生成脚本应在末尾**主动打印 `maxline`**。本次能在发送前拦下来，完全是因为 11/07 起养成的
  「打印 chars/bytes/lines/maxline」习惯 —— 若只看 `chars 10580`，是无法发现截断风险的。
- 静默截断比报错更危险：`SendMessage` 收到半截 HTML 仍返回 `queued`，
  事后只能靠比对字节数（`ListMessages` 的 size）才能察觉，成本极高。
