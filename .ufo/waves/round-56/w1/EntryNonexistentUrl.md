# EntryNonexistentUrl

ENTRY:

```markdown
source: S420 — https://info-search.yahoo.co.jp/archives/002857.php — § 存在しないウェブページが巡回される (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002857.php' | grep -F -c 'クローラーはエラーページとみなさず、'` -> 1 on the retained round-56 body (2026-10-25; the curl arm was not run this round)
ground: per-engine crawl hygiene — what the operator says the crawler does with an error page returned under a success status, the status it asks for instead, and the meta-tag fallback where that status cannot be set

# An error page answered with HTTP 200 OK is not read as an error page

The lane holds the status layer on the Google side (`crawl-error-status-table.md`, S286) and the refusal file's own rules (`yahoo-japan-robots-txt-refusal-rules.md`, S372). This page is the operator's own rule for a URL that has no page [S420].

## The condition the page names

The condition is a request for a page that does not exist, not a page once published and removed:

> "存在しないウェブページを表示しようとしたときに、"

(rendered: when a web page that does not exist is about to be displayed — 表示しようとした is an attempt to display; the page names no cause such as a typo or a renamed route.) What the server answers:

> "サーバーが「HTTP 200 OK」"

(rendered: the server answers with the status `HTTP 200 OK` — the value sits inside the quote, the noun ステータス just after it.) The configuration behind it:

> "エラーページを表示する設定にしていると、"

(rendered: where the server is configured to display an error page — the object is the error page's display, the setting is the server's.)

## What the crawler is said to do

> "クローラーはエラーページとみなさず、"

(rendered: the crawler does not regard it as an error page — みなさず is a treatment, not a finding about the body.)

> "巡回を続けます"

(rendered: it continues the crawl — stated flatly: the page has no 可能性, no interval and no frequency.) [INFERENCE] the lane reads this shape — a success status in front of an error page — as what the industry calls a soft 404; the page does not use the term and the reading is the lane's, not the operator's.

## The status the page asks for instead

> "存在しないウェブページを表示しようとしたときには、"

(rendered: when a web page that does not exist is about to be displayed — the same condition, now the topic of the instruction.)

> "サーバーが「HTTP 404 Not Found」"

(rendered: the server answers with the status `HTTP 404 Not Found` — the second and last status value the page names.)

> "のステータスを返すように設定を行ってください"

(rendered: configure the server to return that status — 行ってください is a request addressed to the site's operator.)

The request is to make the setting, not to check one: the deletion page S419 asks the publisher to check whether that status is configured, S420 asks for it to be set. Both pages name the same two status values and no other [S420].

## Where that setting cannot be made

> "このような設定ができない場合には、"

(rendered: where such a setting cannot be made — このような points back at the 404 setting just requested.)

> "エラーページのHTMLの&lt;head&gt;に、"

(rendered: in the head of the error page's HTML — the entity is quoted as the raw body writes it.)

> "メタタグを使ったインデックス拒否の設定"

(rendered: an index refusal set with a meta tag)

> "を行ってください"

(rendered: please do that setting — the request verb closes the sentence.)

The page names no tag name and no tag value [S420]. `yahoo-japan-robots-txt-refusal-rules.md` (S372) carries the same fallback for a different condition — a site with no root write access for the refusal file; here the condition is a server that cannot be made to answer 404. [INFERENCE] the page does not compare the two conditions.

## The deletion page S419, as far as both pages state it

Both bodies state a server answering 200 OK for a page that should not be served, the crawler continuing, the 404 status as the answer asked for, and the meta-tag fallback in the error page's HTML head. What differs on the two bodies: S419's subject is a deleted URL and it states the continuing crawl as a possibility; S420's subject is a request for a page that does not exist and it states the continuation without that qualifier; S419 asks the publisher to check the 404 setting, S420 asks for the setting to be made; S419's fallback phrase names インデックスへの登録拒否, S420's names インデックス拒否. Neither body names a crawler, an interval, or what the index does with the page [S420].

## The lane's Google-side entries

`crawl-error-status-table.md` admits one Googlebot sentence — crawling scales back when server trouble is detected — and claims no soft-404 remedy from it; S420 states a remedy for one shape of server answer, for one operator. `crawl-budget-consequences.md` holds Google's budget statements; S420 says nothing about crawl budget, crawl rate or a robots block. The contrast is between what each source states, not between the engines' behaviour.

## Quote classes

Every quotation above is a raw substring of the retained body (sha256 `a860d4f3…`, 7332 bytes, HTTP 200 in `receipts.json`), sits inside the article block, and is at most 25 units (one unit per CJK character, one per non-CJK whitespace token). Four spans — `サーバーが「HTTP 404 Not Found」`, `このような設定ができない場合には、`, `エラーページのHTMLの&lt;head&gt;に、` and `を行ってください` — also occur on the deletion page S419; the other eight are page-unique.

## What this entry does not establish

- No URL was served and no crawl was observed; every statement is about what the page says [S420].
- No status other than the two the page names: no 3xx, no 410, no 5xx; no redirect rule (`redirect-rewrite-rules.md` is a different surface).
- No index outcome: the page says the crawler continues and names an index refusal only as a fallback setting.
- No crawler name or user agent in the article block: the only ユーザーエージェント in the retained body is a sidebar link title to another page.
- No claim that the meta-tag fallback has the 404 answer's effect [INFERENCE]; the page does not compare them.
- No claim about the per-link attribute (`yahoo-japan-rel-nofollow-semantics.md`).
- The page prints 更新日 2010年11月24日; this entry reports the body fetched 2026-10-25 and makes no claim about the live documentation today.

Scope note: a claim about what the operator's documentation states on one page of its info centre; no URL was served under test, no crawl was observed, and no server setting was changed.
```

GATE LINE:

- S420 — https://info-search.yahoo.co.jp/archives/002857.php — accessed 2026-10-25 — § 存在しないウェブページが巡回される (更新日 2010年11月24日) — quote: "クローラーはエラーページとみなさず、" (17 units; raw substring of the retained body, sha256 a860d4f33181302d7ab467f5a0b21f2008916bb6dc6def69e69df5b54c630209, 7332 bytes, HTTP 200)

COVERAGE ROW:

| Yahoo! JAPAN non-existent URL crawl handling (r56) | `knowledge/yahoo-japan-nonexistent-url-recrawl.md` (S420) | error page served with HTTP 200 OK is not read as an error page, the crawl continues; HTTP 404 Not Found requested instead; meta-tag index-refusal fallback where that setting cannot be made |

REGISTRY ROW:

| S420 | Yahoo!検索 インフォセンター — 存在しないウェブページが巡回される — https://info-search.yahoo.co.jp/archives/002857.php | docs | A | **What the crawler does with an error page returned under a success status** — the operator's own rule for a URL that has no page: the answer its server gives, the crawl that follows, the status asked for instead, and the meta-tag fallback where that status cannot be set | § 存在しないウェブページが巡回される (更新日 2010年11月24日) | An error page returned with HTTP 200 OK at a URL that has no page is not read as an error page and the crawl continues; the page asks for HTTP 404 Not Found instead, and where that setting cannot be made for an index-refusal meta tag in the error page's HTML head; it names no crawler, no interval and no index outcome | mined | 2026-10-25 | 180d | corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md |

S419 is another seat's cell and S367 is a held row (used-by extension only), so this seat emits no row for either; S367 = none — held row.

UNIT COUNTS (span_tools.py check S420, the counter's units(); all <= 25): 23u `存在しないウェブページを表示しようとしたときに、`; 7u `サーバーが「HTTP 200 OK」`; 19u `エラーページを表示する設定にしていると、`; 17u `クローラーはエラーページとみなさず、`; 7u `巡回を続けます`; 24u `存在しないウェブページを表示しようとしたときには、`; 8u `サーバーが「HTTP 404 Not Found」`; 22u `のステータスを返すように設定を行ってください`; 16u `このような設定ができない場合には、`; 9u `エラーページのHTMLの&lt;head&gt;に、`; 19u `メタタグを使ったインデックス拒否の設定`; 8u `を行ってください`. Gate quote 17u.

UNIQUE SPANS (page-unique to S420 per span_tools: count 1 in S420, absent from S367 and S419): 23u `存在しないウェブページを表示しようとしたときに、`; 7u `サーバーが「HTTP 200 OK」`; 19u `エラーページを表示する設定にしていると、`; 17u `クローラーはエラーページとみなさず、`; 7u `巡回を続けます`; 24u `存在しないウェブページを表示しようとしたときには、`; 22u `のステータスを返すように設定を行ってください`; 19u `メタタグを使ったインデックス拒否の設定`. Eight, above the required three. Not page-unique (shared with S419, quoted for fidelity only): 8u `サーバーが「HTTP 404 Not Found」`; 16u `このような設定ができない場合には、`; 9u `エラーページのHTMLの&lt;head&gt;に、`; 8u `を行ってください`.

RECHECK RUN: `grep -F -c 'クローラーはエラーページとみなさず、' .ufo/waves/round-56/sources/S420.html` printed `1`. The curl arm was not run (no network fetch by this seat). sha256 of the retained body `a860d4f33181302d7ab467f5a0b21f2008916bb6dc6def69e69df5b54c630209`, 7332 bytes, matching `sources/receipts.json` (HTTP 200, fetched 2026-10-25T22:02:42+00:00).

OMITTED:

- The page's `<title>`, meta description, breadcrumb, sidebar category list, the 個別リンクURL widget and the footer — outside the article block (`content_window` = `<h2` .. `個別リンクURL`); no quote may sit there.
- The staged candidate's quote `サーバーが「HTTP 404 Not Found」のステータスを返すように設定を行ってください`: measured 29 units, over the 25 ceiling; replaced by the 8u status span plus the 22u request span.
- The staged candidate's inferences (that both pages are one rule in two places, that a success-served error page is a permanent crawl target, that the triggers are typos/renamed routes/retired campaigns): not stated by S420, so not carried; the route-cause list is absent from the body.
- The staged id S376, its `opened 2026-10-24` and its `soft-404` file name: superseded by this row's S420, the round date, and the landed file name; the term soft 404 appears only as an `[INFERENCE]`-tagged lane reading, never in quotes.
- The page's two sidebar link titles that name other crawl pages (including the user-agent page): listed as links, not carried as content.

VERDICT: S420 entry drafted and quote-true — 12 quoted spans all raw substrings of the retained body, in-content, <= 25 units, 8 page-unique; registry row 11 cells, gate line and coverage row supplied; recheck grep arm printed 1, curl arm unrun.
