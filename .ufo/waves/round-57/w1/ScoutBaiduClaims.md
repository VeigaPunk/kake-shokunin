# ScoutBaiduClaims

Method: read both staged entries (`baidu-dead-link-taxonomy.md` = S403, `baidu-spider3-dead-link-recognition.md` = S408), the retained bodies S421/S422 (article text via `span_tools.py window`, re-split into sentences in a scratch copy under /tmp; nothing written in the lane except this file), plus raw-HTML greps. No source edits, no tool installs. Page text is quoted as the page writes it, with inline tags removed. Frontmatter checks that ran: S421 recheck string count = 1 in S421.html; S422 recheck string count = 1 in S422.html; S421 date 2022-09-09 and S422 date 2016-06-30 are both in `<p class="info-item-time">` (outside the `span_tools` window, which starts at the article body). S422 `<h1>` = 百度搜索Spider3.0升级对站点有什么好处 (title tag: 搜索资讯 category). S422 contains no "404" and no "200" anywhere.

## S421 CLAIMS: (staged S403, `baidu-dead-link-taxonomy.md`; page = 搜索问答剧场【六】“死链”常见问题解析, 2022-09-09)

| # | Staged claim (prose sentence) | Mark | Page text / what the page says |
|---|---|---|---|
| 1 | Operator's definition of a dead link is wider than the HTTP status a server returns | SUPPORTED | §一、了解死链 → 1、死链都有哪些类型？ A：「死链一般是指页面已经无效，无法对用户提供任何有价值信息的页面。包括协议死链和内容死链。」 Content kind is defined by a normal server status (item 2). |
| 2 | Dead link = page already invalid, can give the user no valuable information | SUPPORTED | Same A: sentence. Page hedges with 一般是指 ("generally refers to"); staged drops the hedge. |
| 3 | The taxonomy splits it in two | SUPPORTED | 「包括协议死链和内容死链」 |
| 4 | Protocol dead link: TCP/HTTP status says so; 403, 404, 503 common | SUPPORTED | 「（1）协议死链：页面的TCP协议状态/HTTP协议状态明确表示的死链，常见的如403、404、503状态等。」 |
| 5 | Content dead link: normal status, content changed to non-existent / deleted / needs permission | SUPPORTED | 「（2）内容死链：服务器返回状态是正常的，但内容已经变更为不存在、已删除或需要权限等与原内容无关的信息页面。」 Staged omits 与原内容无关 (an information page unrelated to the original content). |
| 6 | "The page states the consequence plainly: the content kind returns HTTP 200 and cannot be set to 404" | SUPPORTED (quote); "consequence" framing is staged's | Where: same Q1 answer, directly after item (2), as its own sentence: 「内容死链，服务器端返回HTTP状态码200，无法设置为404。」 The page gives it as a bare statement; it does not say what follows from it, and says nothing about whether any checker can or cannot see such pages. |
| 7 | "That single clause is why the taxonomy matters to a publisher" | INFERENCE | Editorial; no sentence on why it matters. |
| 8 | A page gone but answering 200 is, by the operator's definition, a dead link | SUPPORTED | Follows from items (2) + 已删除 + the 200 sentence above. |
| 9 | "no crawler, monitor or link checker that reads status codes alone can see it" | INFERENCE | Not stated. Page Q4 only says discovery tools are 抓取异常工具 and 爬虫软件 ("可以爬取全站所有链接并分析页面状态") and never says they miss content dead links. |
| 10a | Symptom: page "crawls cleanly, ranks as a live URL" | INFERENCE | No crawl or ranking statement about content dead links. (Page §3 (2)(3) speaks of dead links shown in results and affecting site evaluation, but of dead links generally.) |
| 10b | ...and sends a visitor to an empty or permission-gated screen | SUPPORTED | 「内容已经变更为不存在、已删除或需要权限等…信息页面」; 「无法对用户提供任何有价值信息」 |
| 11 | "The remedy is on the publisher's side and is not a status code" | WRONG (as a reading of the page) | The page states no remedy specific to content dead links. Every remedy it does state is a status code: §一 Q2 (1) 「发现后需要及时做404处理」; §二 Q2 第一步 「页面设置404，一定是404页面」; §三 Q1 「【死链提交】工具仅识别404，请一定设置为404；若存在非404资源，可能会影响整个文件生效情况」. "Publisher's side" is INFERENCE (all remedies are on the site side, unsurprisingly). |
| 12a | "the path has to be removed from the site's internal links" | INFERENCE | Not on the page. |
| 12b | "or the route has to be made to answer a real 404" | WRONG (literal) / in tension | Page: content dead link 「无法设置为404」. The page recommends 404 only for the protocol/invalid-resource case (see 11). Staged remedy is the opposite of the literal sentence it quotes one paragraph earlier. |
| 13 | "The same distinction governs what to do with a link that points at such a page" | INFERENCE | Nothing on handling links that point at such a page. |
| 14 | Operator's framing: link dead because of what the reader would find, not what the server said | INFERENCE (partly grounded) | Grounded only in the definition (no valuable information; content changed). The phrase "what the reader would find" is not on the page. |

## S422 CLAIMS: (staged S408, `baidu-spider3-dead-link-recognition.md`; page = 百度搜索Spider3.0升级对站点有什么好处, 2016-06-30; section heading 『死链处理更及时—被黑低质页面全屏蔽』)

| # | Staged claim | Mark | Page text / what the page says |
|---|---|---|---|
| 1 | Round-15 taxonomy: protocol = status code says so (403/404/503); content = normal answer, content gone; operator says it cannot be set to 404 | SUPPORTED (by S421, not S422) | See S421 rows 4, 5, 6. S422 never mentions 404, 200 or a status code. |
| 2 | "Read on its own, that reads like a gap in what any checker can see" | INFERENCE | Inherits S421 row 9. |
| 3 | "The operator's spider-3.0 announcement closes the loop from the other side" | INFERENCE | Page is an article under 搜索资讯 on ziyuan.baidu.com, opening 「近期百度搜索最大的动作应该就是百度Spider3.0升级了」 (hedged commentary voice; 百度工程师 is cited third-hand only for the link-submission advice). It is dated 2016-06-30, six years before the 2022 taxonomy page, and predates it; it neither responds to nor knows the taxonomy. |
| 4 | Crawler "runs a new dead-link recognition model that identifies protocol dead links and most content dead links" | SUPPORTED | 「在死链处理方面，Spider3.0启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页」. Staged omits 跳转死链 (redirect dead links) and 低质网页 (low-quality pages); "most" (大多数) is kept in this sentence but lost in claim 6. |
| 5a | Heading promises faster handling | SUPPORTED (wording) | Heading 『死链处理更及时—被黑低质页面全屏蔽』 = "dead-link handling more timely — hacked low-quality pages fully blocked". 更及时 = more timely/prompt. |
| 5b | "...rather than mere detection" | INFERENCE | The heading draws no detection/handling contrast; the contrast is staged's. |
| 6 | "the content dead link that answers 200 is visible to this crawler: invisible to a status-code check, not to the search engine" | INFERENCE | Page says the model identifies "大多数" (most) content dead links; it does not say content dead links answer 200 (S422 has no 200), nor mention status-code checks. "Is visible" overstates "most". |
| 7 | "if you want the best processing result, a protocol dead link is the best choice" (operator's preference) | SUPPORTED (text); attribution is INFERENCE | 「当然，如果你要追求最佳处理效果，协议死链是最好的选择。」 Scope: it sits in the dead-link handling paragraph, directly after the sentence about handling of dead links submitted via 站长平台; 处理效果 = handling result, no mention of ranking or index. No reason given. Voice is the article's; page does not label it "the operator's preference". |
| 8 | "which is the practical form of the taxonomy" | INFERENCE | S422 does not define or mention the taxonomy; the link is cross-page and cross-date (2016 vs 2022). |
| 9 | "A 404 is not merely more honest than a 200 that lies; it is the kind the operator says its systems handle best" | INFERENCE | S422 has no "404". 404 as a protocol dead link comes only from S421 (404 listed beside 403, 503). "Honest/lies" is editorial. The page says 协议死链, not 404. |
| 10 | Page "does not say a recognised dead link is removed from the index" | SUPPORTED (literal), with a caveat | No sentence on removal from 索引 for dead links (索引 appears only in 「索引展现时效性提升」). Caveat: the page does say previously 「站点通过站长平台提交死链，处理速度可能非常慢，甚至快照在一段时间内仍然存在，但是Spider3.0更新后，大约几天内就可以处理掉了」, and the heading says 全屏蔽 (fully blocked) for hacked low-quality pages. Both imply the snapshot goes away once handled, for submitted dead links. |
| 11 | "the timing it quotes concerns handling, not ranking" | SUPPORTED for 「大约几天内就可以处理掉了」; scope trap otherwise | The dead-link section's only timing is 大约几天 for handling of submitted dead links. The 10天/40%~80% sentence (「索引展现时效性提升，原来是10天左右，现在提升40%~80%不等！」) is in the earlier 链接抓取和建库 section and is about index display timeliness, not dead links; it is also not "handling". The staged text quotes no number, so "the timing it quotes" is ambiguous. |

## SUMMARY:
- S421 entry (16 rows): SUPPORTED 8 (1, 2, 3, 4, 5, 6, 8, 10b), INFERENCE 6 (7, 9, 10a, 12a, 13, 14), WRONG 2 (11 remedy "not a status code"; 12b "route made to answer a real 404").
- S422 entry (13 rows incl. 5a/5b split): SUPPORTED 6 (1, 4, 5a, 7, 10, 11), INFERENCE 6 (2, 3, 5b, 6, 8, 9), WRONG 0.
- Frontmatter: dates 2022-09-09 / 2016-06-30, sections, and both recheck strings verified against the retained bodies (counts 1/1).
- Dates: neither prose states a date. The S422 entry frames a 2016 page as the "other side" of a 2022 taxonomy ("closes the loop", "counterpart"), which the pages do not. The two pages also give different timings for dead-link processing (2016: 大约几天; 2022 submit tool: 「死链提交后一般生效周期为1-2周」), not reconciled in either entry.

## PAGE FACTS THE STAGED ENTRIES OMIT:
- S421 §三 Q1: the 死链提交 tool 「仅识别404」; non-404 entries in a file may affect the whole file taking effect (「请一定设置为404」); 「请勿使用该工具提交非死链内容，避免影响正常页面的搜索展现效果」. Directly cuts against "remedy is not a status code".
- S421 §一 Q2 (1): 「发现后需要及时做404处理」 (for wrongly added content links, e.g. maliciously added spam pages).
- S421 §一 Q3: dead links cost management effort; many dead links shown in results hurt access experience; 百度蜘蛛 「会定期检测网站页面内容价值，若存在大量死链，可能会影响网站整体评价，从而不能更好的进行网站抓取和展现」, which is a site-evaluation effect that S422's "not ranking" framing should not be read to deny.
- S421 §一 Q4: finding dead links = 抓取异常工具 in the platform (shows recent dead links, exportable) and crawler software that analyses page status.
- S421 §二/§三: tool steps (404 page, file in site root, sitemap-format file, no directory-level or index-type submissions, effect 1-2 weeks).
- S421 content-dead-link wording includes 「与原内容无关的信息页面」 (an information page unrelated to the original content); staged drops it.
- S422: the model also covers 跳转死链 (redirect dead links) and 低质网页; scope is 「大多数」 content dead links, not all.
- S422 heading ends 「被黑低质页面全屏蔽」 (hacked low-quality pages fully blocked); the staged entry quotes only the first half.
- S422 baseline: the comparison is between submitting dead links via 站长平台 in earlier versions (slow, snapshot might persist) and Spider3.0 (about a few days). It concerns submitted dead links, not self-recognised ones.
- S422 does discuss ranking elsewhere (「收录时间越近的排名会越靠前…排名不可能简单的跟发布时间有关」), so "page does not speak of ranking" holds only for the dead-link section.
- S422 date and title live in the page header (`info-item-time`, `<h1>`), outside the `span_tools` window; the window text for S422 begins mid-CSS and does not show them.

VERDICT: S421 entry 8 supported / 6 inference / 2 wrong (remedy "not a status code" and "make the route answer 404" contradict the page); S422 entry 6 supported / 6 inference / 0 wrong, with 2016-vs-2022 framing and the 10-day/40-80% scope as the traps.
