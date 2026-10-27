# CriticEntryOverreach

C3 overreach guard: statements the three new entries (S427 re-open, S428 user-triggered fetchers, S429 robots.txt intro)
must NOT make, each bounded by verified page wording. Every quoted span below was checked against the round-59 counter's
own article-block/text-node code (`c59_quote_truth.py` `text_segments`/`units`): 6..25 units, <= 160 chars, a substring
of one whitespace-collapsed text node inside `class="devsite-article-body` .. `<devsite-content-footer`, and page-unique
across all three bodies (verification script in `.files/overreach_check.py`, node dumps `.files/s427.txt`/`s428.txt`/`s429.txt`).

## MUST-NOT:

S427 (`overview-google-crawlers`, `Last updated 2026-06-12 UTC.`):
- MUST NOT attribute a robots.txt posture to user-triggered fetchers. The page states posture for common crawlers only —
  "They always respect robots.txt rules for automatic crawls." — and for special-case crawlers only via the AdsBot
  example. Its user-triggered text ("User-triggered fetchers are part of tools and product functions where the end user
  triggers a fetch.") never mentions robots.txt. (This was R59-D4; S427 `scope` may not repeat `their robots.txt posture`.)
- MUST NOT say "Google crawlers respect robots.txt" without the category bound — the "always respect" sentence sits
  inside the common-crawler bullet only; the same page names three categories ("Google's clients fall into three
  categories:") with different postures.
- MUST NOT say special-case crawlers "ignore robots.txt" — the page gives an example, not a rule: "Special-case
  crawlers are similar to common crawlers," used "where there's an agreement between the crawled site and the Google
  product about the crawl process" (the AdsBot case).
- MUST NOT say AdsBot ignores robots.txt unconditionally — it "ignores the global robots.txt user agent (" (`*`) only
  "with the ad publisher's permission." (5 units — under quote ceiling, cite as qualifier, see below.)
- MUST NOT state the 15MB crawl ceiling as absolute — "Google's crawlers and fetchers only crawl the first 15MB of a
  file" is bounded by "may have a smaller size limit (for example, 2MB), or specify a larger file size limit for a PDF
  than for HTML."
- MUST NOT say caching is universal or unsupported — "Individual Google crawlers and fetchers may or may not make use of
  caching"; only "Other HTTP caching directives aren't supported." beyond ETag/Last-Modified.

S428 (`google-user-triggered-fetchers`, `Last updated 2026-08-19 UTC.`):
- MUST NOT say "user-triggered fetchers ignore robots.txt" — the page's exact bounded claim is "Because the fetch was
  requested by a user, these fetchers generally ignore robots.txt rules" (this is the S426-vs-S428 wording gap the
  correction exists to fix; the correction quote must carry `generally ignore`).
- MUST NOT drop the causation — not "these fetchers can ignore robots.txt" free-standing; the page ties it to
  "Because the fetch was requested by a user,".
- MUST NOT generalize to fetchers "never follow robots.txt", nor extend the posture to crawlers — the page only says
  "these fetchers" (the user-triggered set).
- MUST NOT present the fetcher table as complete — "The list is not exhaustive, it only covers the requestors that are
  more likely to show up in log files".
- MUST NOT claim distinct technical properties — the page defers to the shared doc: the node boundary splits at "The
  general" + link + "of Google's crawlers also apply to the user-triggered fetchers." [INFERENCE: no valid single-node
  quote exists for that sentence; cite it unquoted or paraphrase.]

S429 (`robots/intro`, `Last updated 2025-12-10 UTC.`):
- MUST NOT say "robots.txt hides a page from Google" / "keeps a page out of Google" — the page's explicit limit: "it is
  not a mechanism for keeping a web page out of Google" and "A page that's disallowed in robots.txt can still be indexed
  if linked to from other sites." A blocked URL "can still appear in search results, but the search result won't have a
  description."
- MUST NOT say Google says other crawlers ignore robots.txt — the bounded claim is "While Googlebot and other
  respectable web crawlers obey the instructions in a robots.txt file, other crawlers might not." (might-not on others,
  obedience only asserted for "respectable" ones).
- MUST NOT say robots.txt enforces access — "The instructions in robots.txt files cannot enforce crawler behavior to
  your site;" and "it's up to the crawler to obey them."
- MUST NOT claim robots.txt works on all search engines — "robots.txt rules may not be supported by all search engines."
- MUST NOT claim one syntax fits every crawler — "each crawler might interpret the rules differently."
- MUST NOT present robots.txt as the primary purpose of the file for secrecy — "A robots.txt file is used primarily to
  manage crawler traffic to your site," (keeping a file off Google is secondary and "usually" + "depending on the file
  type:"); for security the page steers elsewhere: "if you want to keep information secure from web crawlers, it's
  better to use other blocking methods".

## QUALIFIERS TO KEEP:

Exact words that must survive in entry prose whenever these claims are made:
- `always` + `for automatic crawls` — S427 common crawlers (posture is scoped to automatic crawls, not every fetch).
- `with the ad publisher's permission` — S427 AdsBot carve-out (5 units, under the 6-unit quote floor: keep the words,
  don't wrap them as a double-quoted span).
- `generally` — S428: `generally ignore`, never bare `ignore`/`never obey`.
- `Because the fetch was requested by a user` — S428 causation clause.
- `may` — S429 `may not be supported`, `might not` obey, `might interpret ... differently`, `might still find and index`,
  `may attempt to crawl` (S427 IP ranges), `may affect how your site appears` (S427 response codes).
- `primarily` — S429 `used primarily to manage crawler traffic`.
- `usually` — S429 "usually to keep a file off Google" (1 unit — prose, not a quote).
- `not exhaustive` — S428 fetcher list bound.
- `By default` / `may` — S427 15MB and per-project limits.
- `respectable` — S429 obedience is asserted of `Googlebot and other respectable web crawlers` only.
- `depending on your goals and situation` / `cannot enforce` — S429 limits framing (the contract's required S429
  subject span is `cannot enforce`; S427's required Gate subject is `automatic crawls`; S428's is `generally ignore`).

VERDICT: Entries pass scrutiny iff S427 scopes robots.txt posture to common crawlers (`always`/`automatic crawls`) and the AdsBot permissioned carve-out, S428 keeps `generally ignore` + the user-request causation, and S429 keeps `cannot enforce`/`may not be supported`/`might not` plus the not-a-hiding-mechanism bound — any unqualified universal is overreach the w2 wave can falsify.
