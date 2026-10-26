# ExecSpanTools

Claim C3, round-57 W1: characterisation of the two retained Baidu bodies for the counter and the scribes. Lane
`kake-shokunin`, base `28fa0b23e699303725aba2727094531f5e44494d`, round date 2026-10-25. Read-only on the lane:
nothing outside this report and `.ufo/waves/round-57/w1/ExecSpanTools.files/` was written; no git/jj mutation.
## SCRIPT:
`.ufo/waves/round-57/w1/ExecSpanTools.files/inspect.py` — my own python, byte-exact UTF-8-strict read (no newline
translation), replicating `c57_quote_truth.content_window()` = min offset of `class="article-info"` /
`class="zz_dldes_content` → first `class="footer"`. Captured outputs beside it: `inspect.out` (178 lines),
`window-S421.txt`, `window-S422.txt`, `spans-S421.txt`, `spans-S422.txt`, `s421-tail-skeleton.txt`.
Ran (all exit 0): `span_tools.py window S421|S422`; `span_tools.py spans S421` (75 spans) and `spans S422` (23);
`span_tools.py check` on four strings (receipts at the end); `inspect.py`.
## OFFSETS:
`char/byte`, byte = UTF-8 offset in the retained file.

| page | marker | n | char/byte offsets |
|---|---|---|---|
| S421 | `class="article-info"` | 1 | 9346/10018 |
| S421 | `class="zz_dldes_content` | 0 | — |
| S421 | `class="footer"` | 1 | 21828/26188 |
| S421 | `<h1` / `<strong` | 0 / 0 | — |
| S421 | `<h2` | 4 | 10033/11031, 14632/16934, 17881/20989, 21193/25197 |
| S421 | `<h3` | 20 | 9368/10040, 10099/11109, 11217/12553, 12723/14491, 13851/15941, 14876/17202, 15339/17797, 15652/18192, 15734/18274, 16328/19076, 16410/19158, 16713/19587, 16795/19669, 17323/20325, 17405/20407, 18142/21284, 18839/22179, 19335/22777, 19648/23144, 20285/23907 |
| S421 | `<title>` | 1 | 315/315 (inner text 322/322) |
| S421 | `发布日期` | 1 | 9443/10153 |
| S422 | `class="article-info"` | 0 | — |
| S422 | `class="zz_dldes_content` | 1 | 9247/9979 |
| S422 | `class="footer"` | 1 | 13061/16251 |
| S422 | `<h1` | 1 | 9060/9754 |
| S422 | `<h2` / `<h3` / `<strong` | 0 / 0 / 0 | — |
| S422 | `<title>` | 1 | 315/315 (inner text 322/322) |
| S422 | `发布日期` | 1 | 9222/9944 |

S421 = 34750 bytes / 30007 decoded chars / 450 lines; S422 = 27327 bytes / 23676 chars / 496 lines; neither has a BOM
or a trailing newline. Each marker occurs once per page, so `content_window` has no ambiguity
(`class="footer-info"` does not match `class="footer"`, which needs the closing quote after `footer`).
## TITLES AND DATES:
- S421 inner: `搜索问答剧场 【六】“死链”常见问题解析_搜索学堂_百度搜索资源平台` — 34 chars, 27 units, exactly one
  ASCII space (between `剧场` and `【六】`), no double space, no tab, no `&nbsp;`; raw is that inner inside
  `<title>…</title>` at byte 315.
- S422 inner: `百度搜索Spider3.0升级对站点有什么好处_搜索资讯_百度搜索资源平台` — 37 chars, 26 units, zero ASCII
  spaces; raw is that inner inside `<title>…</title>` at byte 315.
- S421 `发布日期：2022-09-09` at char 9443 / byte 10153, in `<p class="info-item-time">`, **inside** the article block.
  The bare title text also sits at 322 (`<title>`), 9245 (breadcrumb, pre-window) and 9391 (`<h3 class="info-title">`,
  in-window): 3 occurrences, not page-unique.
- S422 `发布日期：2016-06-30` at char 9222 / byte 9944 — 25 chars **before** the container at 9247, so **outside** the
  article block. The counter tests whole-body presence (`发布日期：<date> in body`), which passes, but the date line
  must not be quoted inside an entry span (it would fail `in_content`). The h1 text occurs at 322 (`<title>` prefix)
  and 9064 (the `<h1>`, pre-window): 2 occurrences.
## HEADINGS:
`char`/`byte` = opening tag; all rows are inside the S421 window. `pageN` = occurrences of the stripped text in the
body. `raw` = stripped text is a raw substring; `NO` means inline `<span>` wrappers split it, and the counter's anchor
test is `anchor in body`, so a `NO` heading cannot serve as `§ <heading>`. Neither page has a `<strong>` element.

| tag | char | byte | units | pageN | raw | text |
|---|---|---|---|---|---|---|
| h3 | 9368 | 10040 | 15 | 3 | yes | 搜索问答剧场 【六】“死链”常见问题解析 (`class="info-title"`) |
| h2 | 10033 | 11031 | 5 | 1 | yes | 一、了解死链 |
| h3 | 10099 | 11109 | 8 | 1 | yes | 1、死链都有哪些类型？ |
| h3 | 11217 | 12553 | 8 | 1 | yes | 2、Q：死链是如何产生的？ |
| h3 | 12723 | 14491 | 18 | 0 | NO | 3、Q：为什么要及时处理死链&nbsp;？不处理是否有影响？ |
| h3 | 13851 | 15941 | 13 | 0 | NO | 4、Q：如何发现网站中存在的死链接？ |
| h2 | 14632 | 16934 | 11 | 0 | NO | 二、教你如何处理死链页面 |
| h3 | 14876 | 17202 | 8 | 0 | NO | 1、Q：如何有效处理死链？ |
| h3 | 15339 | 17797 | 12 | 0 | NO | 2、Q：如何使用平台工具处理死链？ |
| h3 | 15734 | 18274 | 12 | 0 | NO | 第一步：处理的页面设置404页面 |
| h3 | 16410 | 19158 | 15 | 0 | NO | 第二步：将文件放置在网站根目录下 |
| h3 | 16795 | 19669 | 13 | 0 | NO | 第三步：登录百度搜索资源平台 |
| h3 | 17405 | 20407 | 9 | 0 | NO | 第四步：提交死链数据 |
| h2 | 17881 | 20989 | 14 | 0 | NO | 三、使用【死链提交】工具的注意事项 |
| h3 | 18142 | 21284 | 16 | 0 | NO | 1、【死链提交】工具可以识别403、500等无效数据吗？ |
| h3 | 18839 | 22179 | 20 | 0 | NO | 2、【死链提交】工具是否可以删除目录下所有链接（如：*.a.example.com）？ |
| h3 | 19335 | 22777 | 10 | 0 | NO | 3、工具支持索引型sitemap文件吗？ |
| h3 | 19648 | 23144 | 12 | 0 | NO | 4、提交数据的生效周期是什么？ |
| h3 | 20285 | 23907 | 9 | 1 | yes | ——什么是【搜索问答剧场】？ |
| h2 | 21193 | 25197 | 4 | 1 | yes | 推荐阅读 (`class="recommand-news-title"`, right sidebar, not article prose) |

Four further `h3` are empty (`<span><br></span>` only): char/byte 15652/18192, 16328/19076, 16713/19587, 17323/20325.
Anchor-safe S421 candidates (raw, in-window, page-unique, article prose): `一、了解死链` (5u, below the Gate 6-unit
floor), `1、死链都有哪些类型？`, `2、Q：死链是如何产生的？`, `——什么是【搜索问答剧场】？`. 18 of 24 headings are
span-split (`raw NO`).

S422 has one heading element: `h1` char 9060 / byte 9754, 14 units, pageN=2, raw yes, **outside** the window. Its
section markers are `『…』` bracket lines, all in-window and page-unique:

| char | byte | units | text |
|---|---|---|---|
| 10245 | 11253 | 17 | 『抓取、建库更快—提交的内容更容易被抓取』 |
| 10955 | 12559 | 16 | 『死链处理更及时—被黑低质页面全屏蔽』 |
| 11373 | 13307 | 17 | 『时效性内容更多—有内容站点的更多机遇』 |
| 12156 | 14938 | 18 | 『链接提交更好用—站点提交链接会更易收录』 |
## WINDOW CHECK:
- S421 window char [9346, 21828) = byte [10018, 26188), 12482 chars / 16170 bytes; stripped 2091 chars, unchanged with
  `<script>`/`<style>` removed (none inside). Prose nodes (≥20 CJK): 19 page / 15 inside / 4 outside, and the 4 are not
  article text — `<title>` string (322), `meta description` (4039), two IE-browser-warning strings in `<script>`
  (25311, 25381). **All article prose is inside**: first at 9840 (10636), last at 20322 (23972).
- S422 window char [9247, 13061) = byte [9979, 16251), 3814 chars / 6272 bytes; stripped 2015 chars, 1453 with
  `<script>`/`<style>` removed — **562 chars of CSS** (a `<style>` at 9282..9860) are inside the window and therefore
  "in content" for substring tests. Prose: 20 page / 16 inside / 4 outside (same four non-article kinds: 322, 4042,
  16522, 16592). **All article prose is inside**: first 9921 (10711), last 12631 (15723). The `<h1>` (9060) and the
  `发布日期` line (9222) are pre-window.
- Over-inclusion: S421 tail 20418..21828 (1410 chars) = `往期回顾` recap list (20418), empty pager (21063) and the
  `推荐阅读` sidebar (21143..21800), whose 7 titles each occur twice (`title=` attribute + link text) so the helper never
  offers them; S422 tail 12680..13061 (381 chars) = the bbs URL plus empty widget divs.
- Pre-window region: S421 char [0, 9346) = 9346 chars / 10018 bytes, stripped 340 chars; S422 [0, 9247) = 9247 chars /
  9979 bytes, stripped 357 chars — `<title>` text + breadcrumb + the same 42 nav labels + `回到顶部`, and for S422 the
  `发布日期：2016-06-30` line.
- Looser windows: from document char 0 the stripped window text grows to 2529 chars (S421, +438) / 1898 (S422, +445);
  from `<body>` (5177 / 5110) 2472 / 1838; from the first `<div>` (5184 / 5117) 2471 / 1837.
- Helper spans occurring before the window: **0 of 75** (S421) and **0 of 23** (S422) — no offered span is nav text.
- Pre-window text nodes at or above the 6-unit floor: S421 the `<title>` string (27u, n=1), `创作者小课堂` (6u),
  `流量与关键词` (6u), `我的溯源提交` (6u), `站点优化与维护` (7u), the info-title (15u, n=3); S422 the `<title>` string
  (26u, n=1), the same four nav labels, the h1 text (14u, n=2). The four nav labels occur once per body but in **both**
  bodies, so C5's cross-body clause excludes them even under a looser window. What a looser window newly admits: from
  char 0 the two `<title>` strings (27u / 26u, page-unique, absent from the other body) become in-content and would pass
  C5 — head metadata is kept out **only** by the lower bound at the article container; from `<body>` the `<title>` stays
  out. The S421 info-title and the S422 h1 (both raw) become "inside" under any looser bound, but neither is page-unique.
- Span placement among the helper's own candidates: S421 51 article-prose / 21 mid-sentence fragments / 3 from the
  `往期回顾` recap (`“站点关联主体”常见问题解析`, `“站点Logo”常见问题解析`, `“百度蜘蛛”全面解析`); S422 16 / 7 / 0.
  Fragments begin or end at a tag boundary (S421 `的TCP协议状态/HTTP协议状态明确表示的死链，`,
  `：服务器返回状态是正常的，但`; S422 `此次升级是把当前离线、`, `！索引展现时效性提升，原来是`,
  `有兴趣的站点可以参加：`): raw, unique, in-window, but cut clauses.
## STAGED RECHECK STRINGS:
| string | chars | units | ≤25u | ≤40ch | own body | other body | in window |
|---|---|---|---|---|---|---|---|
| `死链一般是指页面已经无效，无法对用户提供任何有价值信息的页面。` | 31 | 29 | no | yes | S421 n=1 @ char 10180 / byte 11212 | S422 n=0 | yes |
| `启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页` | 40 | 37 | no | yes (exactly 40) | S422 n=1 @ char 11102 / byte 12760 | S421 n=0 | yes |

Both occur exactly once, only in their own body, as raw substrings, with no HTML entity and no curly quote. **Both
exceed the 25-unit ceiling**, so neither staged string can be a Gate quote or an entry span; shorter in-window
candidates exist, e.g. S421 `协议死链和内容死链` (9u), `服务器端返回HTTP状态码200` (9u); S422 `在死链处理方面，` (7u),
`更新后，大约几天内就可以处理掉了` (15u), `『死链处理更及时—被黑低质页面全屏蔽』` (16u),
`当然，如果你要追求最佳处理效果，协议死链是最好的选择` (24u / 30 chars).
`span_tools.py check` receipts (verbatim `{units, raw_substring, in_content, count_in_page, in_other_adopted_body}`):
- `check S421 死链一般是指…页面。` → `29, True, True, 1, False`
- `check S422 启用了全新的死链识别模型…低质网页` → `37, True, True, 1, False`
- `check S422 『死链处理更及时—被黑低质页面全屏蔽』` → `16, True, True, 1, False`
- `check S421 一、了解死链` → `5, True, True, 1, False` (5u is below the 6-unit Gate floor)

Risks recorded, not remediated (outside this seat): the S421 window over-includes the recap list and the `推荐阅读`
sidebar; the S422 window includes 562 chars of CSS; the S422 date line is outside the window while its body-presence
test passes; 28 of the 98 helper spans are mid-sentence fragments. No tool install or upgrade was needed.

VERDICT: Both bodies are clean for C3 — all main prose lies inside `content_window` (S421 [10018,26188), S422 [9979,16251) bytes); S421 anchors must come from 4 raw-unique headings, S422's from a 『…』 line (its only h1 is pre-window, pageN=2); both staged recheck strings are unique to their own body but exceed the 25-unit ceiling (29u / 37u) and cannot be quoted.
