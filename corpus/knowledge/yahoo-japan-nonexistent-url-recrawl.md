source: S420 — https://info-search.yahoo.co.jp/archives/002857.php — § 存在しないウェブページが巡回される (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002857.php' | grep -F -c 'クローラーはエラーページとみなさず、'` -> 1 (curl arm 1 and the same grep against the retained round-56 body 1, 2026-10-25)
ground: per-engine crawl hygiene — what the operator says the crawler does with an error page returned under a success status, the status it asks for instead, and the meta-tag fallback where that status cannot be set

# The crawler does not treat a 200 OK error page for a nonexistent URL as an error page

The lane holds the status layer on the Google side (`crawl-error-status-table.md`, S286) and the refusal file's own rules (`yahoo-japan-robots-txt-refusal-rules.md`, S372). This page is the operator's own rule for a URL that has no page [S420].

## The condition the page names

The condition is an attempt to display a web page that does not exist. The page names no cause and states no exclusion of a page that was once published and then removed — that case has its own operator page (S419), and S420's words do not exclude it [INFERENCE]:

> "存在しないウェブページを表示しようとしたときに、"

(rendered: when a web page that does not exist is about to be displayed — 表示しようとした is an attempt to display; the page names no cause such as a typo or a renamed route.) What the server answers:

> "サーバーが「HTTP 200 OK」"

(rendered: the server, with the status `HTTP 200 OK` — the value sits inside the quote). The verb sits between this span and the next, outside both quotes:

> "のステータスを返して"

(rendered: returns the status — 返して, the connective form, so the clause continues into the next span.) The configuration behind it:

> "エラーページを表示する設定にしていると、"

(rendered: where it is configured to display an error page — 設定にしていると closes the whole sentence into a conditional about a server configuration, not a standing rule; the object is the error page's display, the setting is the server's.)

## What the crawler is said to do

> "クローラーはエラーページとみなさず、"

(rendered: the crawler does not regard it as an error page — みなさず is a treatment, not a finding about the body.)

> "巡回を続けます"

(rendered: it continues the crawl — stated flatly: `python3 -B .ufo/waves/round-56/span_tools.py window S420 | grep -o -F -e 可能性 -e 頻度 -e 間隔 | wc -l` -> 0, 2026-10-25: no possibility hedge, no interval and no frequency.) [INFERENCE] the lane reads this shape — a success status in front of an error page — as what the industry calls a soft 404; the page does not use the term and the reading is the lane's, not the operator's.

## The status the page asks for instead

> "存在しないウェブページを表示しようとしたときには、"

(rendered: when a web page that does not exist is about to be displayed — the same condition, now the topic of the instruction.)

> "サーバーが「HTTP 404 Not Found」"

(rendered: the server answers with the status `HTTP 404 Not Found` — the second and last status value the page names.)

> "のステータスを返すように設定を行ってください"

(rendered: configure the server to return that status — 行ってください is a request addressed to the site's operator.)

The request is to make the setting, not to check one: the deletion page S419 asks the publisher to check whether that status is configured, S420 asks for it to be set. Both pages name the same two status values and no other [S420].

## Where that setting cannot be made

The sentence goes on with また (also), adding a fallback to the 404 request for the case where such a setting cannot be made. The clause that states that condition and the head of the error page's HTML is the same on the deletion page, and its scope, its qualifiers and the S372 substitute are read once in `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` (§ The fallback where that setting cannot be made). S420 differs only in the phrase for the setting itself:

> "メタタグを使ったインデックス拒否の設定"

(rendered: an index refusal set with a meta tag — S419's phrase is インデックスへの登録拒否, registration in the index.) The page names no tag name and no tag value (`python3 -B .ufo/waves/round-56/span_tools.py window S420 | grep -c -E 'noindex|name=|content='` -> 0, 2026-10-25; the raw body holds `name=` eight times as the page's own HTML attributes, so the sweep runs on the article text). [INFERENCE] the page does not compare this condition with the no-root-access condition of S372.

## The deletion page S419, as far as both pages state it

Both bodies state a server answering 200 OK for a page that should not be served, the crawler continuing, the 404 status as the answer asked for, and the meta-tag fallback in the error page's HTML head. What differs on the two bodies: S419's subject is a deleted URL and it states the continuing crawl as a possibility; S420's subject is a request for a page that does not exist and it states the continuation without that qualifier; S419 asks the publisher to check the 404 setting, S420 asks for the setting to be made; S419's fallback phrase names インデックスへの登録拒否, S420's names インデックス拒否. Neither body names a crawler product or user agent, a crawl interval, or what the index does with the page; the only agent word on either is クローラー (`python3 -B .ufo/waves/round-56/span_tools.py window S419 | grep -o -F クローラー | wc -l` and the same for S420 print 1 each, and `grep -o -E 'Googlebot|Slurp|Bingbot'` on both bodies prints nothing, 2026-10-25) [S419][S420].

## The lane's Google-side entries

`crawl-error-status-table.md` admits one Googlebot sentence — crawling scales back when server trouble is detected — and claims no soft-404 remedy from it; S420 states a remedy for one shape of server answer, for one operator. `crawl-budget-consequences.md` holds Google's budget statements; S420 says nothing about crawl budget, crawl rate or a robots block. The contrast is between what each source states, not between the engines' behaviour.

## Quote classes

Every quotation above is a raw substring of the retained body `.ufo/waves/round-56/sources/S420.html` (sha256 `a860d4f3…`, 7332 bytes, HTTP 200 in `.ufo/waves/round-56/sources/receipts.json`), sits inside the article block, and is at most 25 units under the counter's `units()` (`.ufo/waves/round-56/c56_quote_truth.py`: one unit per CJK character in the kana/kanji ranges, so CJK punctuation costs 0, plus one per non-CJK whitespace token) and at most 40 characters. One span — `サーバーが「HTTP 404 Not Found」` — also occurs on the deletion page S419 (shared remedy wording); the other nine are page-unique (`python3 -B .ufo/waves/round-56/span_tools.py check S420 '<span>'` prints `count_in_page=1` and `in_content=True` for all ten and `in_other_adopted_body=True` for that one, 2026-10-25).

## What this entry does not establish

- No URL was served and no crawl was observed; every statement is about what the page says [S420].
- No status other than the two the page names: no 3xx, no 410, no 5xx; no redirect rule (`redirect-rewrite-rules.md` is a different surface).
- No index outcome: the page says the crawler continues and names an index refusal only as a fallback setting.
- No crawler name or user agent in the article block: the only ユーザーエージェント in the retained body is the anchor text of a sidebar link to another page (`python3 -B .ufo/waves/round-56/span_tools.py window S420 | grep -c -F ユーザーエージェント` -> 0, `grep -o -F ユーザーエージェント .ufo/waves/round-56/sources/S420.html | wc -l` -> 1, 2026-10-25).
- No claim that the meta-tag fallback has the 404 answer's effect [INFERENCE]; the page does not compare them.
- No claim about the per-link attribute (`yahoo-japan-rel-nofollow-semantics.md`).
- The page prints 更新日 2010年11月24日; this entry reports the body fetched 2026-10-25 and makes no claim about the live documentation today.

Scope note: a claim about what the operator's documentation states on one page of its info centre; no URL was served under test, no crawl was observed, and no server setting was changed.
