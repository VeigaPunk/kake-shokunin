# ScoutClaimsAudit

Method: staged entries read from `shokuknow/merge/kake/knowledge/corpus/knowledge/` (yahoo-japan-link-target-crawl-restriction = staged S367, yahoo-japan-deleted-url-recrawl = staged S375 -> S419, yahoo-japan-soft-404-recrawl = staged S376 -> S420). Page text from `span_tools.py window` plus raw reads of `sources/S367.html`, `S419.html`, `S420.html` (grep of the HTML for headings, links, and the `個別リンクURL` field). No claim was tested against a live crawler. Lane-internal statements (what the lane already holds) are not page claims and are marked INFERENCE/lane-internal. Scope notes ("No page was submitted...") are disclaimers, not factual claims, and are not counted.

Page text that matters (verbatim):
- S367 body (no header): `リンク先ウェブページの巡回制限は、rel=&quot;nofollow&quot;属性を使った指定方法のほかに、HTMLのメタタグで指定する方法と、サーバーの設定で指定する方法があります。` (the attribute method is a link to archives/002851.php.)
- S367 § メタタグを使用する方法: `「このウェブページ内にあるリンク先ウェブページの巡回は拒否するが、このウェブページ自身はインデックスへの登録を許可する」という意味を持ちます` (for index,nofollow) and `「リンク先ウェブページの巡回を拒否し、ウェブページ自身のインデックスへの登録も拒否する」` (for noindex,nofollow).
- S367 § サーバーで設定する方法: `ウェブページをホスティングしているサーバーで、次のようなディレクティブ設定をします。` then `X-Robots-Tag: NOFOLLOW`. Nothing about index status.
- S419 (no sub-heading): `削除したURLのウェブページにアクセスしたときに「HTTP 200 OK」のステータスを返すようにサーバーが設定されている場合、クローラーは削除されたウェブページと認識できず、そのウェブページを巡回し続ける可能性があります。` / `...サーバーが「HTTP 404 Not Found」のステータスを返すように設定されているかを確認してください。` / `また、このような設定ができない場合には、エラーページのHTMLの&lt;head&gt;に、メタタグを使ったインデックスへの登録拒否の設定を行ってください。`
- S420 (no sub-heading): `存在しないウェブページを表示しようとしたときに、サーバーが「HTTP 200 OK」のステータスを返してエラーページを表示する設定にしていると、クローラーはエラーページとみなさず、巡回を続けます。` / `...サーバーが「HTTP 404 Not Found」のステータスを返すように設定を行ってください。また、このような設定ができない場合には、エラーページのHTMLの&lt;head&gt;に、メタタグを使ったインデックス拒否の設定を行ってください。`

## S367 CLAIMS:
| # | Staged sentence (short) | Mark | Page wording / note |
|---|---|---|---|
| 1 | Lane's crawl ground so far is S201/S192/S199/S200 (REP side); lane lacked the link-refusal half | INFERENCE (lane-internal) | Not a page claim; page says nothing about the lane. Not checked here. |
| 2 | The operator names three routes: attribute form, meta tag, server header | SUPPORTED (count implicit) | `rel=&quot;nofollow&quot;属性を使った指定方法のほかに、HTMLのメタタグで指定する方法と、サーバーの設定で指定する方法があります` — three methods enumerated; the page never says "three". Attribute route is only named and linked (002851), not described on this page. Server route is called `ディレクティブ設定`; the word "header" is the staged reader's gloss. |
| 3 | Quote `"X-Robots-Tag: NOFOLLOW"` | SUPPORTED | Located in § サーバーで設定する方法, `<pre>` block. grep -F -c = 1. |
| 4 | Meta-tag form carries the distinction; operator spells it out | SUPPORTED | § メタタグを使用する方法 gives both index,nofollow and noindex,nofollow with glosses. |
| 5 | `index,nofollow`: refuses link-target crawl while still allowing page to be indexed | SUPPORTED | `リンク先ウェブページの巡回は拒否するが、このウェブページ自身はインデックスへの登録を許可する`. Page says index registration is *permitted* (許可), not that the page is kept/guaranteed indexed. |
| 6 | `noindex,nofollow` refuses both, page's own indexing refused | SUPPORTED | `リンク先ウェブページの巡回を拒否し、ウェブページ自身のインデックスへの登録も拒否する`. |
| 7 | "The operator also states the same refusal can be applied to an individual link URL rather than the page's whole link set" | WRONG | The only occurrence of 個別リンクURL is the page-footer permalink field `<strong>個別リンクURL</strong>` containing the article's own URL (`https://info-search.yahoo.co.jp/archives/002852.php`). It is a site widget label meaning "permalink", not a refusal scope. The page makes no statement about per-link application; the only per-link-adjacent text is the bare mention of the rel="nofollow" method (linked to 002851). |
| 8 | A page wanting content crawled/indexed but not outbound links followed "into places it cannot vouch for" | INFERENCE | Page states no purpose or motive; "cannot vouch for" is absent. |
| 9 | "has three documented ways to say so" | INFERENCE (partly) | Three methods for restricting link-target crawl: supported (row 2). But X-Robots-Tag: NOFOLLOW is shown with no index/noindex counterpart and rel=nofollow's index effect is not on this page. |
| 10 | "the choice between them [the three routes] changes whether the page itself stays in the index" | INFERENCE (overreach) | The index/noindex choice exists only inside the meta tag (row 5/6). The page never says rel=nofollow or X-Robots-Tag: NOFOLLOW changes indexing, nor that the choice *between routes* does. "stays in the index" also exceeds 許可 (permit registration). |
| 11 | "A blanket noindex on such a page is the wrong instrument, and the operator's own page says so" | INFERENCE (attributed to the operator wrongly) | Page only shows noindex,nofollow as the form for refusing both; it never calls noindex wrong. Evaluation is the staged author's; "the operator's own page says so" is not stated. |

Also: S367's own `<meta name="robots">` is `index,follow,noarchive,noodp` (line 14), unrelated to the claim but an observed page fact.

## S419 CLAIMS:
| # | Staged sentence (short) | Mark | Page wording / note |
|---|---|---|---|
| 1 | Operator explains a recurring complaint in one page: URL removed, crawler keeps coming back | INFERENCE (partly) | Title `削除したウェブページが巡回され続ける` and `...巡回され続けるとき...` support the symptom; "recurring complaint" is not stated. |
| 2 | The diagnosis is the response status | SUPPORTED | Page ties it to the server being configured to return `「HTTP 200 OK」`. |
| 3 | Quote `クローラーは削除されたウェブページと認識できず、そのウェブページを巡回し続ける可能性があります` | SUPPORTED | First paragraph, grep -F -c = 1. Note the hedge `可能性があります` ("may"). |
| 4 | If server answers a deleted URL with a success status, crawler cannot tell the page is gone, so it keeps crawling it | INFERENCE (hedge dropped, status widened) | Page: `「HTTP 200 OK」...認識できず...巡回し続ける可能性があります` — "may continue", and only 200 OK is named. Staged prose says "success status" generally and "keeps crawling" unhedged. "Cannot tell" is SUPPORTED (`認識できず`). |
| 5 | Remedy is to answer with a not-found status instead | SUPPORTED | `サーバーが「HTTP 404 Not Found」のステータスを返すように設定されているかを確認してください` (phrased as "check that it is configured to return 404"). |
| 6 | Where server cannot be configured that way, put an index-refusal meta tag in the error page's head | SUPPORTED | `エラーページのHTMLの&lt;head&gt;に、メタタグを使ったインデックスへの登録拒否の設定を行ってください`. |
| 7 | "A deletion is only a deletion if the server stops answering with success" | INFERENCE | Editorial reading; page does not generalise. |
| 8 | "A soft-deleted URL — one the application still serves with a 200 — is still being crawled" | INFERENCE (overstated) | Page: 200 OK on deleted URL -> crawler *may* continue (`可能性`). Term "soft-deleted"/"application" absent; "is still being crawled" is a certainty the page does not give. |
| 9 | "the crawl cost of a removed page is still being paid" | INFERENCE | Page says nothing about crawl cost, budget or any price paid; it only says the crawler may keep visiting. (Header `ground:` line, "crawl budget", is also not on the page.) |

## S420 CLAIMS:
| # | Staged sentence (short) | Mark | Page wording / note |
|---|---|---|---|
| 1 | "This is the sibling of the deleted-URL case" | INFERENCE | Page never refers to the deleted-URL case. Observed only: S420 sidebar links to 002856 (S419) among 9 category-sidebar links; similar structure (200 OK -> keeps crawling; 404 or meta). The relation term is staged editorial. |
| 2 | It is about a URL that never existed | SUPPORTED | `存在しないウェブページを表示しようとしたときに` / title `存在しないウェブページが巡回される`. |
| 3 | Examples: typo in a link, a renamed route, a retired campaign page | INFERENCE (and inconsistent) | Page lists no causes. A renamed route / retired campaign page existed before, which is the deleted-URL case (S419), contradicting row 2's "never existed". |
| 4 | Error page served with success status is not read as an error page | SUPPORTED | `サーバーが「HTTP 200 OK」のステータスを返してエラーページを表示する設定にしていると、クローラーはエラーページとみなさず` |
| 5 | so the crawler keeps coming | SUPPORTED | `巡回を続けます` — unhedged here (contrast S419's `可能性があります`). |
| 6 | Remedy is the same status the deletion case asks for | SUPPORTED (404 in both) | S420 `「HTTP 404 Not Found」のステータスを返すように設定を行ってください`; S419 asks it as a check. "Same as deletion case" is a comparison the page does not draw. |
| 7 | Quote `サーバーが「HTTP 404 Not Found」のステータスを返すように設定を行ってください` | SUPPORTED | Second paragraph of S420, grep -F -c = 1. Same string is NOT in S419 (count 0; S419 ends `設定されているかを確認してください`). |
| 8 | Where server cannot be configured, index-refusal meta tag in error page's head | SUPPORTED | `エラーページのHTMLの&lt;head&gt;に、メタタグを使ったインデックス拒否の設定を行ってください`. |
| 9 | "Both pages together are the operator's statement of one rule in two places" | INFERENCE | Each page states its own case; no cross-statement of one rule. |
| 10 | "the crawl loop follows what the server answers, not what the site intends" | INFERENCE | Page wording: crawler recognises/treats a page as deleted or error based on status (`認識できず`, `エラーページとみなさず`). "Crawl loop", "site intends" are absent. Consistent in direction, not stated. |
| 11 | "A host that serves a styled error page with success status converts every mistake into a permanent crawl target" | INFERENCE (overstated) | Page: error page with 200 -> crawler `巡回を続けます`. "Styled", "every mistake", "permanent" absent. |
| 12 | "one for a URL removed, one for a URL never built — same defect with different triggers" | INFERENCE | Editorial synthesis of rows 1-3; page does not say "same defect". |

## SUMMARY:
Counting sentences of prose including the quote block; scope notes excluded; partly-supported rows counted by their dominant mark.
- S367: 11 claims — SUPPORTED 5 (rows 2,3,4,5,6); INFERENCE 5 (rows 1,8,9,10,11); WRONG 1 (row 7).
- S419: 9 claims — SUPPORTED 4 (rows 2,3,5,6); INFERENCE 5 (rows 1,4,7,8,9); WRONG 0.
- S420: 12 claims — SUPPORTED 6 (rows 2,4,5,6,7,8); INFERENCE 6 (rows 1,3,9,10,11,12); WRONG 0.
Flagged-term verdicts: "index,nofollow keeps the page indexable" -> page says index registration is *permitted* (SUPPORTED as "allows", INFERENCE as "stays in the index"); "three routes" -> three methods enumerated, numeral absent (SUPPORTED); "individual link URL" -> WRONG (permalink widget); "crawl loop follows what the server answers" -> INFERENCE; "crawl cost still being paid" -> INFERENCE (nothing on cost); "sibling of the deleted-URL case" -> INFERENCE (editorial; sidebar link only).

## PAGE FACTS THE STAGED ENTRIES OMIT:
- S367: the attribute route is `rel=&quot;nofollow&quot;`, linked to its own page 002851 and not explained here; the page gives no index/noindex statement for the rel and X-Robots-Tag routes; the server route is `ディレクティブ設定`; update date 2010-11-24 (staged cites it). The meta examples are written with HTML-entity quotes in the page source.
- S419: the trigger is specifically `HTTP 200 OK`; outcome is hedged (`可能性があります`); the remedy is to *check* 404 is configured (`確認してください`); the fallback meta tag is described as `インデックスへの登録拒否` (registration refusal).
- S420: the page is unhedged (`巡回を続けます`); the fallback meta wording is `インデックス拒否` (differs from S419's `インデックスへの登録拒否`); the pages are 2 adjacent entries in the same `クローラー` category; S419 and S420 are cross-linked only via the generic category sidebar.
- Neither S419 nor S420 mentions crawl budget/cost, soft deletes, typos, renames, campaigns, or permanence.
- Retained bodies fetched 2026-10-25; staged entries record fetch 2026-10-24 and recheck commands that still return 1 on the retained bodies (S367 grep X-Robots-Tag: NOFOLLOW = 1; S419 and S420 quote greps = 1).

VERDICT: S367 5 supported / 5 inference / 1 wrong (`individual link URL` is a permalink widget); S419 4/5/0 (hedge dropped, "crawl cost" unsupported); S420 6/6/0 (sibling/one-rule/styled-error/permanent claims are staged inference).
