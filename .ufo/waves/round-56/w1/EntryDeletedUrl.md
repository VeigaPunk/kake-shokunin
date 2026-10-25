# EntryDeletedUrl

Seat EntryDeletedUrl — claim C2, row S419. Lane bounds observed: this report is the only file written; no lane entry,
registry, README, jj state or git index touched; no subagent dispatched. Everything below was re-grounded in the retained
body `.ufo/waves/round-56/sources/S419.html` (7428 bytes, sha256
`6172d5d108d0c31d25244659516fc7fc81472c924ef35a51afc964cdd3a4a5c8`, HTTP 200, `sources/receipts.json`), read with
`span_tools.py window S419` and lines 100–108 raw. The shokuknow staged candidate was reference only: none of its S375 id,
`opened` date, quotes, section label or "practical reading" prose is carried; the heading and the three sentences were
re-derived from the body.

ENTRY:

```markdown
source: S419 — https://info-search.yahoo.co.jp/archives/002856.php — § 削除したウェブページが巡回され続ける (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002856.php' | grep -F -c 'クローラーは削除されたウェブページと認識できず、'` -> 1 (2026-10-25: the grep form against the retained round-56 body prints 1; the curl arm was not run this round)
ground: per-engine crawl hygiene — what a success status on a deleted URL does to the crawl, the 404 check the page asks for, and the head meta-tag fallback it names where that setting cannot be made

# A deleted URL that still answers 200 OK is a page the crawler cannot drop

The lane holds what an error status does to crawling on Googlebot's side (`corpus/knowledge/crawl-error-status-table.md`, S286) and what a robots block does to the crawl budget (`corpus/knowledge/crawl-budget-consequences.md`, S273/S274). Neither says what a success status on a removed page does. This page states that failure and its two remedies in three sentences [S419].

## The condition, and a possibility rather than a certainty

> "削除したURLのウェブページにアクセスしたときに"
> "「HTTP 200 OK」のステータスを返すように"
> "サーバーが設定されている場合、"

(rendered: in the case where the server is configured, when the web page of a deleted URL is accessed, to return the status "HTTP 200 OK" — the condition is a server setting, and the status is named with its reason phrase, 200 OK.)

> "クローラーは削除されたウェブページと認識できず、"
> "そのウェブページを巡回し続ける可能性があります"

(rendered: the crawler cannot recognise it as a deleted web page, and there is a possibility that it keeps crawling that web page). The consequence is stated as 可能性があります, a possibility; the page does not say the crawl always continues [S419].

## The check the page asks for

> "削除されたウェブページが巡回され続けるときには、"
> "サーバーが「HTTP 404 Not Found」のステータスを返すように"
> "設定されているかを確認してください"

(rendered: when a deleted web page continues to be crawled, confirm whether the server is configured to return the status "HTTP 404 Not Found"). The verb is 確認してください, please confirm: the page asks the publisher to check the setting, not to change it, and the second status is named with its reason phrase, 404 Not Found [S419].

## The fallback where that setting cannot be made

> "また、このような設定ができない場合には、"
> "エラーページのHTMLの&lt;head&gt;に、"
> "メタタグを使ったインデックスへの登録拒否"
> "の設定を行ってください"

(rendered: also, in the case where such a setting cannot be made, make a setting, by means of a meta tag, in the head of the error page's HTML, that refuses registration in the index). Three qualifiers hold the remedy's scope: このような設定ができない場合には (where such a setting cannot be made — the fallback is conditional), エラーページのHTMLの head (the tag belongs in the error page's own head, not in the page that used to exist at the URL), and メタタグを使った (by means of a meta tag). The remedy text names no tag name, no content value and no attribute [S419]; [INFERENCE] `noindex` and `name="robots"` are the lane's candidate values, not the page's words.

The same substitute appears on the operator's robots page, `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md` (S372): a site that cannot place robots.txt is told to set index-registration refusal with a meta tag, and that page names no value either. [S419] adds the location — the error page's head — and still no value.

## What the lane's Google-side entries state, and what this page does not

`corpus/knowledge/crawl-error-status-table.md` records one admitted Googlebot sentence: crawling is scaled back when the servers are detected to have trouble (S286). [S419] states no rate effect and no trigger: its stated outcome is a continued crawl, and it gives no rate, no frequency and no duration [INFERENCE the page's silence is recorded here, not filled].

`corpus/knowledge/crawl-budget-consequences.md` records Google's statement that a robots block does not hand the spared fetches to other pages unless the capacity limit is already hit (S273), and that an emergency backoff reduces the crawl rate across the whole hostname (S274). [S419] names no block and no budget: its two remedies are a response status and a head meta tag, not a robots.txt record, so it neither agrees nor disagrees with those sentences.

The meta tag is a page-level head setting; `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` (S374) covers a link-level attribute, and [S419] names no link attribute. Neither remedy is a redirect: `corpus/knowledge/redirect-rewrite-rules.md` covers publisher-side redirect configuration (S050, S135), and [S419] proposes no redirect for a deleted URL.

## What this entry does not establish

- No tag name, content value, attribute or syntax for the meta-tag fallback; no statement that any crawler honours it [S419].
- No statement that the 404 is to come from the server configuration or from the application: the page's subject is サーバー, the server, and its sentence asks whether that server is so configured.
- Nothing about how long a continued crawl lasts, at what rate it runs, or when it stops; no crawl-budget or crawl-rate statement; nothing about redirects, canonicals or a removal tool.
- Nothing about a URL that never existed: that is the sibling page 存在しないウェブページが巡回される (002857.php, row S420), not this one.
- Nothing about any live property: no URL was deleted, no response was served under test, and no crawl was observed.

## Quote classes

Each quotation is a raw substring of `.ufo/waves/round-56/sources/S419.html` (sha256 `6172d5d1…`, 7428 bytes, HTTP 200 in `.ufo/waves/round-56/sources/receipts.json`), occurs once in that body, and is at most 25 units (one unit per CJK character, one per non-CJK whitespace token). Four spans also occur on the sibling S420 body — `サーバーが「HTTP 404 Not Found」のステータスを返すように`, `また、このような設定ができない場合には、`, `エラーページのHTMLの&lt;head&gt;に、`, `の設定を行ってください` — because the two pages share the remedy wording; those four are unique within S419, not across the round's three adopted bodies. HTML entities stay as written (`&lt;head&gt;`). Renderings keep the page's qualifiers: 設定されている場合, 可能性があります, 確認してください, このような設定ができない場合には, エラーページ.

Scope note: a claim about what the operator's documentation states on one page of its info centre; no URL was deleted or served under test for this lane, and no crawl was observed.
```

GATE LINE:

- S419 — https://info-search.yahoo.co.jp/archives/002856.php — accessed 2026-10-25 — § 削除したウェブページが巡回され続ける (更新日 2010年11月24日) — quote: "クローラーは削除されたウェブページと認識できず、" (23 units; raw substring of the retained body, sha256 6172d5d108d0c31d25244659516fc7fc81472c924ef35a51afc964cdd3a4a5c8, 7428 bytes, HTTP 200)

COVERAGE ROW:

| Per-engine crawl hygiene (Yahoo! JAPAN) | `knowledge/yahoo-japan-deleted-url-recrawl.md` (S419) | deleted URL status 200 OK vs 404 Not Found check, error-page head meta tag with unnamed value, possibility and cannot-be-configured qualifiers |

REGISTRY ROW:

| S419 | Yahoo!検索 インフォセンター — 削除したウェブページが巡回され続ける — https://info-search.yahoo.co.jp/archives/002856.php | docs | A | **A deleted URL answered with 200 OK stays in the crawl** — the operator's diagnosis that a success status hides a deletion from the crawler, the 404 check it asks for, and the head meta-tag fallback where that setting cannot be made | § 削除したウェブページが巡回され続ける (更新日 2010年11月24日) | deletion becomes visible to the crawler through the response status; a 200 OK on a removed page leaves it crawled, and the page offers a 404 check plus an unnamed index-refusal meta tag in the error page's head | mined | 2026-10-25 | 180d | corpus/knowledge/yahoo-japan-deleted-url-recrawl.md |

S367: none — held row. S420: not this seat.

UNIT COUNTS (unit rule: one per CJK character, one per non-CJK whitespace token; each verified with `span_tools.report`):

1. 削除したURLのウェブページにアクセスしたときに — 21
2. 「HTTP 200 OK」のステータスを返すように — 14
3. サーバーが設定されている場合、 — 14
4. クローラーは削除されたウェブページと認識できず、 — 23 (gate quote)
5. そのウェブページを巡回し続ける可能性があります — 23
6. 削除されたウェブページが巡回され続けるときには、 — 23
7. サーバーが「HTTP 404 Not Found」のステータスを返すように — 19
8. 設定されているかを確認してください — 17
9. また、このような設定ができない場合には、 — 18
10. エラーページのHTMLの&lt;head&gt;に、 — 9
11. メタタグを使ったインデックスへの登録拒否 — 20
12. の設定を行ってください — 11

All twelve: raw substring True, in-content True, count_in_page 1, <= 25 units. Spans 7, 9, 10, 12 also occur in S420's
body (shared remedy wording, disclosed in the entry); 1–6, 8, 11 are page-unique across S367/S419/S420.

UNIQUE SPANS (`span_tools.py spans S419` returned four: 23u 削除したURLのウェブページにアクセスしたときに「HTTP 200 OK」,
23u クローラーは削除されたウェブページと認識できず、, 23u そのウェブページを巡回し続ける可能性があります, 23u
削除されたウェブページが巡回され続けるときには、). Used and page-unique: spans 1, 2, 3, 4, 5, 6, 8, 11 above. The gate
quote is span 4 — page-unique, 23 units, raw, count 1.

RECHECK RUN:

- Header form: `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002856.php' | grep -F -c 'クローラーは削除されたウェブページと認識できず、'`
- Executed (grep form, retained body only): `grep -F -c 'クローラーは削除されたウェブページと認識できず、' .ufo/waves/round-56/sources/S419.html` → printed `1`.
- Spot check: `grep -F -c 'メタタグを使ったインデックスへの登録拒否' …/S419.html` → `1`. `sha256sum` → `6172d5d1…a5c8` and `wc -c` → 7428, both matching `receipts.json`. The curl arm was **not** run; no live-fetch count is claimed.

OMITTED:

- The page's own `<meta name="robots" content="index,follow,noarchive,noodp" />` and meta description: info-centre chrome, not the remedy (remedy text is lines 104–106).
- The `個別リンクURL` input block and module markup: navigation; the URL is carried in the header, gate line and registry row.
- Related-links list (002854, 002855, 002857) and カテゴリ一覧 nav: link furniture. 002857 is named in prose as row S420; the other two get no row and no new S-id.
- The 更新日 2010年11月24日 line: carried in header and registry anchor cell, not quoted (it also occurs in S367/S420 bodies, so not page-unique).
- The staged candidate's "practical reading" paragraph (soft-deleted URL still paying crawl cost): the page states a continued crawl and a possibility, not a cost; the only reading kept is the [INFERENCE]-tagged candidate tag values.
- Nothing from S367/S420/S387/S388/S389 bodies is quoted.

VERDICT: S419 entry drafted quote-true from the retained body (12 spans, max 23 units, 8 page-unique, 4 shared with S420 and disclosed), with gate line, 11-cell registry row and coverage row; this report is the only file written.
