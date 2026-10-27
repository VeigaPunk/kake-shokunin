# ExecSourceLive

Claim C3 live re-open. Fetched 2026-10-27 UTC with `curl -sL --compressed`, UA `Mozilla/5.0 (X11; Linux x86_64; kake-r60-ExecSourceLive-livecheck)`. Evidence (hashes, no bodies): `.ufo/waves/round-60/w1/ExecSourceLive.files/live-hashes.json`. Comparison used the round-59 counter's article-block rules (`class="devsite-article-body` .. `<devsite-content-footer`, `<script>`/`<style>`/`<aside>`/`<nav>`/`<devsite-feedback>`/`<devsite-thumb-rating>` stripped, whitespace collapsed).

## FETCHES:

| row | URL | HTTP | retained bytes/sha256 | live bytes/sha256 | bytes equal | `Last updated` (retained = live) |
|---|---|---|---|---|---|---|
| S426 | .../crawlers-fetchers/verify-google-requests | 200 | 69789 / 8df9d4ad…f0879 | 69789 / e7388021…1c | no | 2026-03-20 UTC |
| S427 | .../crawlers-fetchers/overview-google-crawlers | 200 | 74477 / d70ce6f5…2175 | 74477 / e7152c48…e5 | no | 2026-06-12 UTC |
| S428 | .../crawlers-fetchers/google-user-triggered-fetchers | 200 | 76197 / 0f296b86…53b2 | 76197 / f5402ad6…0545c | no | 2026-08-19 UTC |
| S429 | .../search/docs/crawling-indexing/robots/intro | 200 | 178797 / 423d99c5…9edd | 178793 / 820d0356…d23 | no | 2025-12-10 UTC |

No redirects on any fetch (effective URL = request URL). Every `Last updated` sits inside `<devsite-content-footer` and matches between retained and live.

## TEXT-NODE DIFF:

Zero article-text differences on all four pages. Collapsed text-node multisets (retained vs live): S426 161=161, S427 203=203, S428 349=349, S429 137=137; nodes only-retained = 0, nodes only-live = 0 per page. All byte deltas are outside the article block: per-request `script nonce=` values, reordering of `dimensionN` keys in the `<script type="application/json" analytics>` blob, an app_loader nonce tail, and (S429 only) whitespace/attribute-line reordering of `data-label`/`aria-label` attributes in header/footer chrome — the 4-byte size delta. So every C5 quote against a retained body remains a substring of a live text node, page-unique status unchanged [INFERENCE: uniqueness across all four pages was verified for the retained bodies only this run; live bodies carry identical node sets].

## S426->S428 LINK:

Confirmed on both retained and live bodies: 6 `href` occurrences matching `user-triggered-fetchers`, of which 2 point at the category page `/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers`, both with anchor text "User-triggered fetchers". The other 4 hrefs are IP-range JSON (`/static/crawling/ipranges/user-triggered-fetchers[|-google].json`, anchor texts `user-triggered-fetchers.json`, `user-triggered-fetchers-google.json`, `User-triggered fetchers (users)`, `User-triggered fetchers (Google)`). The lane-found S428 derivation ("linked from the S426 page's category table") is live-true.

## POSTURE BY CATEGORY:

S427's article block states a robots.txt posture for exactly two of its three categories:
- Common crawlers — "They always respect robots.txt rules for automatic crawls." (article node, both bodies)
- Special-case crawlers — the AdsBot example: "ignores the global robots.txt user agent (* ) with the ad publisher's permission."
- User-triggered fetchers — NO robots.txt statement; the section only says they "are part of tools and product functions where the end user triggers a fetch" (example Google Site Verifier, "acts on the request of a user").

Only two article nodes on the page contain `robots` — both above, identical retained and live. This confirms R59-D4's substance: S425's `scope` cell ("the three crawler categories and their robots.txt posture") overstates the page, and S427's corrected scope (common + special-case only) matches the live page.

VERDICT: All four pages re-verified live 2026-10-27: article text nodes identical to retained bodies, `Last updated` unchanged (S426 2026-03-20, S427 2026-06-12, S428 2026-08-19, S429 2025-12-10), S426 still links the S428 category page (2 hrefs, anchor "User-triggered fetchers"), and S427 states robots.txt posture for common + special-case crawlers only — no posture for user-triggered fetchers.
