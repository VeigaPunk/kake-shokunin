source: S423 — https://ziyuan.baidu.com/college/articleinfo?id=3457 — § 2、Q：如何才能识别当前抓取是正确的百度蜘蛛？ (发布日期 2022-08-19) — fetched 2026-10-26
verified-at: 2026-10-26
recheck: 180d — `curl -fsSL --compressed 'https://ziyuan.baidu.com/college/articleinfo?id=3457' | grep -F -c '若百度蜘蛛抓取频次过高，造成网站服务异常，可以通过'` -> 1 (grep against the retained body 1, 2026-10-26)
ground: per-engine crawl hygiene — how Baidu's own operator says a publisher tells a genuine Baiduspider request from an impostor, and what it says sustains and relieves heavy crawling

# Baidu's own page gives two tests for a genuine Baiduspider request, and names three UA channels

The operator's article prints its title (the fifth episode of its 搜索问答剧场 Q&A series, on 百度蜘蛛; the exact title is in the
S423 registry row) and the line
`发布日期：2022-08-19`, and answers four questions under the body heading `【抓取篇】` (one
occurrence in the body: `span_tools.py check S423 '【抓取篇】'` -> count_in_body 1, raw substring,
2026-10-26) [S423].

## What Baiduspider is said to be

> "也叫百度蜘蛛"

(rendered: it is also called 百度蜘蛛 — Baidu spider). The sentence names the thing and its job [S423]:

> "是百度搜索引擎的一个自动程序，它的作用是"

(rendered: it is an automatic program of the Baidu search engine, and its function is [S423])

> "访问互联网上的网页，建立索引数据库"

(rendered: to visit pages on the internet and build the index database), so that users can find
site-related content through Baidu search [S423]. The page states purpose, not capability: nothing
here says what script, if any, the program executes.

## Method one: the user-agent string

> "方式一：查看UA信息"

(rendered: method one — inspect the UA information). A wrong UA is treated as decisive [S423]:

> "如果UA信息不对，可以直接判断为非百度搜索的蜘蛛"

(rendered: if the UA information is not right, one can directly judge it to be a spider that is not
Baidu search's). The page then fixes the channel split [S423]:

> "UA分为移动、PC"

(rendered: the UA is divided into mobile, PC), and the next node adds 小程序 (Mini Program) [S423]:

> "这三个渠道UA分别如下："

(rendered: the UAs of these three channels are as follows:).

The three channel blocks print the full strings verbatim, at 186 to 219 characters each — far past
this lane's quotation ceilings — so the entry names their distinguishing tokens instead:
`Baiduspider/2.0` in the mobile and PC forms, and `Baiduspider-render/2.0` in one mobile form, the
PC form, and the Mini Program form, which appends `Smartapp` [S423]. The page presents these as
strings a publisher compares against. It does **not** say what the render-named agent fetches,
executes, or is to be allowed, and this entry asserts none of that.

## Method two: reverse DNS, then forward DNS

> "方式二：双向DNS解析认证"

(rendered: method two — two-way DNS resolution authentication). The steps are printed in order [S423]:

> "第一步：DNS反查IP"

(rendered: step one — reverse-look-up the IP by DNS). The developer resolves the logged IP address
backward, and the crawler's hostname must carry one of two suffixes [S423]:

> "非*.baidu.com或*.baidu.jp即为冒充"

(rendered: anything that is not `*.baidu.com` or `*.baidu.jp` is an impersonation — 冒充). The
per-platform commands are given as examples [S423]:

> "可以使用host ip命令反解ip来判断是否来自Baiduspider的抓取"

(rendered: on linux one can use the `host ip` command to reverse-resolve the ip to judge whether it
comes from Baiduspider's crawling) [S423];

> "可以使用nslookup ip命令反解ip"

(rendered: on Windows, or the IBM OS/2 platform, one can use the `nslookup ip` command to
reverse-resolve the ip) [S423];

> "可以使用dig"

(rendered: on mac os one can use the `dig` command to reverse-resolve the ip) [S423].

> "第二步：对域名运行正向"

(rendered: step two — run a forward DNS lookup on the domain name) [S423]. The forward lookup
closes the test [S423]:

> "IP地址一致可确认spider来自百度搜索引擎"

(rendered: if the IP address is the same, the spider can be confirmed to come from the Baidu search
engine) [S423],

> "IP地址不一致即为冒充"

(rendered: if the IP address is not the same, it is an impersonation).

## Q3: whether the crawler keeps coming

> "一般会的"

(rendered: generally it will). The condition the page states is fresh material [S423]:

> "若网站持续生产新资源、更新内容等，蜘蛛会持续抓取的"

(rendered: if the site keeps producing new resources and updating content and so on, the spider
will keep crawling). The same answer adds a reminder, addressed to a site that wants that
crawling [S423]:

> "一定不要做任何封禁"

(rendered: do not apply any block), and offers a log check — inspect the site's access logs — so that
someone maliciously impersonating Baiduspider to crawl the site frequently can be guarded against [S423]:

> "及时判断正确的百度蜘蛛"

(rendered: judge the correct 百度蜘蛛 in time). The page does not define 封禁 here; its own
blocking section (【封禁篇】) refers the reader to the operator's separate unblocking article, which the lane carries as
`corpus/knowledge/baidu-spider-unblocking.md`; this entry quotes nothing from that section.

## Q4: causes of heavy crawling, and the tool named for it

The answer gives two candidate causes; the first is fresh material awaiting the crawl [S423]:

> "新生产资源、更新内容"

(rendered: newly produced resources, updated content). The second is that an impersonator may be
crawling, and for that the page refers the reader back to its Q2 identification method [S423].
Where the frequency itself is the problem, the remedy named is a platform tool [S423]:

> "若百度蜘蛛抓取频次过高，造成网站服务异常，可以通过"

(rendered: if Baiduspider's crawl frequency is too high and causes the site's service to be
abnormal, one can, through [S423])

> "【抓取频次】工具"

(rendered: the crawl-frequency tool of the Search Resource Platform), adjust the frequency [S423].
The page states no numbers: no default rate, no ceiling, no effect time for an adjustment.

## What this entry does not establish

- It does not establish what the render-named agent fetches or executes. The page lists the token
  and no rendering behaviour; the fetch-versus-execute question is left open here.
- It does not establish that the two UA strings per channel are exhaustive or still current beyond
  the 2022-08-19 printing, nor that a UA match alone proves a genuine crawler — the page's second
  method exists because a string can be copied.
- It does not establish any rate, budget, or timing for a 抓取频次 adjustment, nor how long a
  blocked object stays unfetched.
- It establishes nothing about other operators' identity tests. Related lane entries, by path:
  `corpus/knowledge/crawler-identity.md` (general identity material),
  `corpus/knowledge/robots-txt-rules.md` (refusal rules),
  `corpus/knowledge/baidu-friendly-crawl-guidance.md` (this operator's crawl hygiene), and
  `corpus/knowledge/js-rendering-queue.md` (another operator's render phase).

## Quote classes

Every quotation above is an exact raw substring of one text node of the article block in the
retained body `S423.html` (29007 bytes, HTTP 200, sha256
`8b8aef60bd7e315799e9a97dadfd02a5982f8c7e17b9d4064a6fc3913a0736ec`), each within 25 units and 40
characters, page-unique in both retained bodies. None is a rendered-text reconstruction; where the
page's inline markup splits a sentence, the entry says so rather than joining nodes. The UA strings
are named by token in backticks, not quoted, because they exceed the quotation ceiling.

Scope note: this entry records what the operator's page states, and nothing more; no crawl was
observed and no Baidu behaviour was measured.
