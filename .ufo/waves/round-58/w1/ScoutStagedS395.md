# ScoutStagedS395

Sources: staged row `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` line 115 (S395); staged entry `.../knowledge/corpus/knowledge/baidu-crawler-identification.md`; retained body `sources/S423.html` (sha256 8b8aef60…, 29007 B, fetched 2026-10-26, from `receipts.json`); page text via `span_tools.py window S423` / `check S423`. All quote checks below were run with `span_tools.py check` (in_text_node=True unless noted). Page-side claims about S409 (2017 announcement) come from the lane registry row only, not from S423.

## STAGED ROW:
| cell | staged value | check |
|---|---|---|
| id/title/url | S395, 搜索问答剧场【五】“百度蜘蛛”全面解析, `articleinfo?id=3457` | SUPPORTED. Page title line: `搜索问答剧场 【五】“百度蜘蛛”全面解析` (title has a space after 搜索问答剧场; the staged title has none — cosmetic). Contract renumbers S395 -> S423. |
| kind/tier | docs / A | SUPPORTED (operator's own platform page, 搜索资源平台). |
| scope | "operator's own crawler inventory and its identification procedure — the Baidu-side counterpart to the Yahoo name list the lane could not reach, and to the address-based identification both operators publish" | Page supports "crawler inventory + identification procedure" (UA strings for 移动/PC/小程序; 方式二 DNS). The Yahoo clause is lane history, not on the page (unsupported by S423; not a page claim). "Address-based identification both operators publish" is not checkable from S423 (Yahoo not on page). Drop Yahoo clause from a registry scope. |
| anchor | `§ 【抓取篇】→「第一步：DNS反查IP」段末句 (the page prints no revision stamp — pinned by the quoted clause and the access date)` | PARTLY WRONG. (a) `【抓取篇】` exists (1u/5c) and `第一步：DNS反查IP` exists (5u/11c, a `<b>` in the 方式二 paragraph, under Q2) — both resolve. The path skips Q2 and 方式二 but is not false. (b) "段末句": the clause `非*.baidu.com或*.baidu.jp即为冒充。` is the last sentence of the first paragraph of 第一步 (`<p>…即为冒充。</p>`), but 第一步 continues with the ①②③ platform items, the last of which repeats the same clause with `&nbsp;` separators — ambiguous as "段末" of the whole step. (c) "no revision stamp": the page DOES print `发布日期：2022-08-19` (check: 4u/15c, unique). It prints no 更新/修订 date. So "no revision stamp" is true only as "no update date"; the anchor must carry 发布日期 2022-08-19 instead of implying the page is undated. |
| teaches | agent names Baiduspider/2.0 and "listed among them" Baiduspider-render/2.0; two ways: UA and a DNS reverse lookup, hostname under *.baidu.com / *.baidu.jp, other = impersonation | MOSTLY SUPPORTED. Both names appear in UA lists (`Baiduspider-render/2.0` count_in_body 3, unique=False — too repeated to be a quote anchor). Two ways: `A：有两个方式可以判断百度蜘蛛。`; 方式一 UA, 方式二 `双向DNS解析认证`. Gap: the page's 方式二 is bidirectional — reverse lookup THEN forward lookup (第二步：对域名运行正向DNS查找 ... IP地址不一致即为冒充); the row says only "reverse lookup", omitting the forward confirmation that actually decides the verdict. |
| status/opened | mined / 2026-10-24 | Contract: both rows opened 2026-10-26 (re-fetched). Update to 2026-10-26 when landing as S423. |
| recheck | `grep -F -c '非*.baidu.com或*.baidu.jp即为冒充。'` -> 1 | RE-RAN on retained body: 1. Clause is a raw substring of one text node, 6u/28c, unique=True. SAFE quote. |
| used-by | corpus/knowledge/baidu-crawler-identification.md | Contract names the landed entries `baidu-spider-identification.md` (cites S423) — name differs; fix at landing. |

## STAGED ENTRY:
Front-matter: `source:` mirrors the row anchor, so carries the same "no revision printed" defect and the 2026-10-24 date; `recheck` same as row (verified 1).

| # | staged sentence (abridged) | verdict | page evidence / source |
|---|---|---|---|
| 1 | "Three rounds of this lane tried to get an operator's crawler user-agent names ... Yahoo! JAPAN ... only when rendered. Baidu's page carries the same material in bytes a plain GET returns" | OTHER (lane history; Yahoo = other rows S418/S419 era). Last half partly checkable: the retained body was fetched by plain HTTP (`receipts.json` userAgent kake-shokunin-round58, status 200) and contains the UA strings, so "plain GET returns" is supported by the receipt, not by the page text. |
| 2 | "answers a publisher's actual question — is this request really Baiduspider? — with two methods: user agent, and DNS reverse lookup" | SUPPORTED: `2、Q：如何才能识别当前抓取是正确的百度蜘蛛？` / `有两个方式可以判断百度蜘蛛。` Omits that method two is reverse+forward. |
| 3 | "hostname must be under `*.baidu.com` or `*.baidu.jp`, and one that is not is an impersonation" | SUPPORTED: `非*.baidu.com或*.baidu.jp即为冒充。` (but note forward-confirmation step not mentioned: reverse hostname alone is not the page's full verdict). |
| 4 | "`Baiduspider/2.0` is the ordinary crawler" | SUPPORTED as a name (移动/PC UAs carry `Baiduspider/2.0`); "ordinary" is the entry's gloss, page says only `Baiduspider也叫百度蜘蛛，是百度搜索引擎的一个自动程序，它的作用是访问互联网上的网页，建立索引数据库`. |
| 5 | "`Baiduspider-render/2.0` is a separate, named agent" | SUPPORTED in the narrow sense: appears as the UA token in a mobile UA, the PC UA and the 小程序 UA (`...Baiduspider-render/2.0;Smartapp;...`). "separate" is an inference: the page never describes it as distinct, it only lists the UA. |
| 6 | "...that fetches a page's CSS, JavaScript and images" | UNSUPPORTED. Article block contains no occurrence of CSS, JavaScript, 图片, 渲染, 脚本 (window shows none; the css/javascript hits in the raw HTML are page chrome outside the article). The page never states what the render agent fetches. The function claim has no source on S423. |
| 7 | "the same agent the platform's 2017 announcement introduced" | FROM ANOTHER PAGE: S409 (`ziyuan.baidu.com/wiki/1021`, 发布日期 2017-06-07; registry says render UA introduced March 2017). S423 contains no 2017 and no date other than 2022-08-19. Cross-page identity (same UA name) is an [INFERENCE] stitching; must be cited to S409, not S423. |
| 8 | "sitting in the operator's inventory as one crawler among several" | PARTLY: the page lists UA strings across three channels; "inventory" is a gloss; "among several" holds only as Baiduspider/2.0 + -render/2.0 (two names). |
| 9 | "A publisher blocking by user agent must allow both" | UNSUPPORTED as stated. Page says only: `若网站需要百度蜘蛛抓取一定不要做任何封禁` (9u/9c) and lists `封禁百度UA` as a common block; no sentence mentions allowing the render UA specifically. |
| 10 | "What this page does not say is whether the render agent executes the script it fetches" | Absence claim, consistent with the page (no execute/render text in the article). Safe as [INFERENCE] absence; but premise "it fetches script" is itself unsupported (row 6). |
| 11 | "It has a section on crawling and a section on crawl frequency, and no rendering section" | WRONG as to sections. The page's two section headers are `【抓取篇】` and `【封禁篇】` (crawl and BLOCKING). Crawl frequency is Q4 inside 抓取篇 (`抓取频次过高 ... 【抓取频次】工具调整频次`), not a section. "No rendering section" is true. |
| 12 | "Baidu fetches your JavaScript with an agent it names" | UNSUPPORTED (same as row 6); the page names the agent but never says it fetches JavaScript. |
| 13 | "and asks you not to block it" | UNSUPPORTED for the render agent. Page says `若网站需要百度蜘蛛抓取一定不要做任何封禁` about 百度蜘蛛 generically (Q3, under 抓取篇), conditioned on `若网站需要...抓取`; it does not mention -render or JavaScript. Generic "don't block Baiduspider if you want crawling" is supported; "asks you not to block it [the render agent that fetches JS]" is not. |
| 14 | "fetch-versus-execute question stays open" | framing; fine given page silence, but rests on rows 6/12. |

## REFUSED LINES:
- "...`Baiduspider-render/2.0` ... that fetches a page's CSS, JavaScript and images" (sentence 6) — no support in S423.
- "the same agent the platform's 2017 announcement introduced" (7) — from S409, not S423; refuse unless cited to S409 with the 2017-06-07 date.
- "A publisher blocking by user agent must allow both." (9) — no page sentence.
- "It has a section on crawling and a section on crawl frequency" (11) — factually wrong; sections are 抓取篇 / 封禁篇.
- "Baidu fetches your JavaScript with an agent it names, and asks you not to block it." (12/13) — fetch half unsupported; "asks not to block it" attaches a generic Q3 sentence to the render agent.
- Row anchor `(the page prints no revision stamp — pinned by the quoted clause and the access date)` and entry front-matter "no revision printed" — the page prints `发布日期：2022-08-19`; say "publication date 2022-08-19, no update date" instead.
- Row scope clause "Baidu-side counterpart to the Yahoo name list the lane could not reach, and to the address-based identification both operators publish" — Yahoo content is not on S423.
- Section label `【抓取篇】→「第一步：DNS反查IP」段末句` — resolvable but ambiguous (see anchor cell); replace with `§ 【抓取篇】Q2 方式二 第一步：DNS反查IP, first paragraph (发布日期 2022-08-19)`.

## SAFE LINES:
Quotes (all `check S423` in_text_node=True, within ceilings, count_in_body=1, unique=True):
- `非*.baidu.com或*.baidu.jp即为冒充。` — 6u/28c (recheck grep -c = 1 on retained body).
- `一定不要做任何封禁` — 9u/9c (Q3; supports only generic "do not block Baiduspider if you want it to crawl").
- `发布日期：2022-08-19` — 4u/15c (date anchor).
- `访问互联网上的网页，建立索引数据库` — 16u/17c (what Baiduspider does).
- `第一步：DNS反查IP` — 5u/11c; `【抓取篇】` — 3u/5c (locators).
- NOT usable as quotes: `Baiduspider-render/2.0` (count_in_body 3, not unique); the page title (count 3).
Paraphrases safe to keep: the page gives two ways to identify Baiduspider (UA; two-step reverse-then-forward DNS); the UA lists carry `Baiduspider/2.0` and `Baiduspider-render/2.0` across 移动, PC, 小程序 channels; reverse hostname must be `*.baidu.com`/`*.baidu.jp`, else impersonation; forward lookup must return the original IP, else impersonation; page does not say what the render agent fetches or executes (absence, [INFERENCE] from article text).
Unrun: no live re-fetch of the page (retained body only); S409 content beyond its registry row not read.

VERDICT: S423 supports the identification procedure and the 非*.baidu.com clause, but five staged sentences (render agent fetches CSS/JS/images, 2017 link, must-allow-both, crawl-frequency section, asks not to block it) are unsupported or from S409, and "no revision stamp" is wrong (发布日期：2022-08-19 is printed).
