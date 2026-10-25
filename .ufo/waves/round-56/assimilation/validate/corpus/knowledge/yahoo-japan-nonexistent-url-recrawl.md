source: S420 — https://info-search.yahoo.co.jp/archives/002857.php — § 存在しないウェブページが巡回される (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002857.php' | grep -F -c 'クローラーはエラーページとみなさず、'` -> 1 (curl arm 1 and the same grep against the retained round-56 body 1, 2026-10-25)
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
