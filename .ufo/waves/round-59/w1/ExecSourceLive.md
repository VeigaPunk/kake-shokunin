# ExecSourceLive

Live re-open of the two C3 source pages (S425, S426) and comparison of their article-block text
nodes against the bodies retained in `.ufo/waves/round-59/sources/`.

Scratch: `/fast/scratch/hyaku/kake-r59/ExecSourceLive/` (bodies fetched there, deleted at end of run).
Hash receipts: `.ufo/waves/round-59/w1/ExecSourceLive.files/fetch-hashes.json` (hashes only, no bodies copied).
No lane state, no sibling lane, no Git index touched. Tools installed: none.

## FETCHES:

Command (both pages, UA `kake-shokunin-round59-recheck`, `--compressed`, `--max-time 60`):

    curl -sL --compressed -A kake-shokunin-round59-recheck --max-time 60 -o <out> \
         -w '%{http_code} %{url_effective} %{size_download}' <url>

| id | url | HTTP | final URL | live bytes | live sha256 |
|---|---|---|---|---|---|
| S425 | https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers | 200 | same as request (no redirect) | 74481 | `c8b73afbe72b4267ab230c0a5345e69210f42b98926fab61e32e2145072c67d3` |
| S426 | https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests | 200 | same as request (no redirect) | 69793 | `e4d471685dce8effc513167aa764802c0704986c8f2c9bad8408a27ec6a8b145` |

Retained bodies (unchanged, read-only) for comparison:

| id | retained path | retained bytes | retained sha256 | matches `sources/receipts.json` |
|---|---|---|---|---|
| S425 | `.ufo/waves/round-59/sources/S425.html` | 74477 | `ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa` | yes (bytes + sha256 + status 200 + effectiveUrl + fetchedAt 2026-10-27T01:21:22+00:00) |
| S426 | `.ufo/waves/round-59/sources/S426.html` | 69789 | `8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879` | yes (bytes + sha256 + status 200 + effectiveUrl + fetchedAt 2026-10-27T01:21:22+00:00) |

Whole-page sha256 therefore differs between retained and live (S425 +4 bytes, S426 +4 bytes); the
difference is outside the article block (see next section).

`Last updated` line (identical in retained and live, same line numbers):

- S425 line 1345: `<p>Last updated 2026-06-12 UTC.</p>` — corroborated by response header `last-modified: Fri, 12 Jun 2026 11:47:15 GMT`.
- S426 line 1274: `<p>Last updated 2026-03-20 UTC.</p>` — corroborated by response header `last-modified: Fri, 20 Mar 2026 14:21:12 GMT`.

Response `Date` headers: `Tue, 27 Oct 2026 01:47:51 GMT` (S425) and `Tue, 27 Oct 2026 01:47:52 GMT` (S426);
so the round's access date 2026-10-27 (UTC) still holds for this re-open.

Page `<title>` identical retained vs live:
- S425 `Google Crawler (User Agent) Overview | Google Crawling Infrastructure | Crawling infrastructure | Google for Developers`
- S426 `Verify Requests from Google Crawlers and Fetchers | Google Crawling Infrastructure | Crawling infrastructure | Google for Developers`

## TEXT-NODE DIFF:

Method: the C3 counter's own code, imported unmodified from
`.ufo/waves/round-59/c59_quote_truth.py` (`content_window`, `text_segments`, `article_headings`),
applied to (a) the raw retained body and (b) the live body, and also in the counter's exact
evaluation order (whole-body whitespace collapse first, then `text_segments`).

Article-block window (`class="devsite-article-body` .. `<devsite-content-footer`) is at the same
offsets in retained and live for both pages:

| id | window offsets (retained = live) | window bytes | window sha256 (retained = live) | byte-identical |
|---|---|---|---|---|
| S425 | 32092..45212 | 13120 = 13120 | `a3b00be0beccce8600c7bfd3394d0492e35e1f3732e1dc90b6ad0d70fd9d0658` | yes |
| S426 | 32091..40524 | 8433 = 8433 | `f49315862009e212a0be4ebe5c8ff0dadb29344a22c403011f79278c77ae097a` | yes |

Text-node comparison (the counter's `text_segments`, whitespace-collapsed):

| id | segments retained / live | collapsed non-empty retained / live | ordered lists equal | set equal | only-in-retained | only-in-live | `<h2>/<h3>` headings equal |
|---|---|---|---|---|---|---|---|
| S425 | 217 / 217 | 157 / 157 | **yes** | yes | **0** | **0** | yes |
| S426 | 165 / 165 | 90 / 90 | **yes** | yes | **0** | **0** | yes |

Result: **identical**. No differences at all in the article-block text nodes — same nodes, same
order, same collapsed text, same headings — for both pages, under both evaluation orders
(raw-body segmentation and counter-style whole-body-collapse-then-segmentation). Raw (uncollapsed)
segment lists are also identical.

Whole-page differences exist but lie entirely outside the article block: a `difflib` opcode scan
gives 74 (S425) / 87 (S426) differing hunks, of which **0** touch the article window (all hunks are
after the window end). They are session/boilerplate churn only: sign-in state blobs
(`"dimension5": "en"`, `"Signed out"` vs `Signed out`), a random nonce token, and the
`MiscFeatureFlags__*` / `Profiles__*` feature-flag list whose element order is randomized per
response, plus a re-ordered analytics id list. None of it is page prose.

Spot-check of the C5-relevant sentences in the live bodies (collapsed, article-block scoped):
`your logs may show visits from several IP addresses` — present once in S425, 0 in S426;
`The source IP address of the request.` — S425 once, S426 zero;
`The reverse DNS hostname of the source IP.` — S425 once, S426 zero;
`The HTTP` / `user-agent` / ` request header.` — the three-signal list nodes are present in live S425
at the same positions (nodes 197–203) as in retained. The counter's per-row topics
(`IP address` for S425, `reverse DNS` for S426) are in-content in both retained and live bodies.
The stale-sentence target string `user-agent string` occurs 0 times in either body, retained or
live — so the C3 correction cannot be quoting it from these pages.

## S425->S426 LINK:

`grep -n 'verify-google-requests'` on the **retained** S425 body
(`.ufo/waves/round-59/sources/S425.html`) — two hits:

    720:  <li class="devsite-nav-item"><a href="/crawling/docs/crawlers-fetchers/verify-google-requests"
    1284:  <a href="/crawling/docs/crawlers-fetchers/verify-google-requests">verify Google's crawlers and fetchers</a>.

Line 1284 is inside the article block (char offsets 44182–44292, window 32092..45212); line 720 is
site navigation outside the article block (offset 20719–20815). The anchor is relative
`/crawling/docs/crawlers-fetchers/verify-google-requests`, which resolves against the S425 page
URL to `https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests` —
exactly the S426 URL in `sources/receipts.json` and in the contract.

Surrounding retained lines 1281–1285 (identical in the live body, same line numbers):

    <p>
      Learn how to use these details to
      <a href="/crawling/docs/crawlers-fetchers/verify-google-requests">verify Google's crawlers and fetchers</a>.
    </p>

So the S426 provenance ("lane-found, linked from S425's 'Learn how to use these details to verify'
sentence") is confirmed against the retained body and holds in the live body as well (live S425 has
the identical href on the same line 1284).

## Notes / limits:

- No lane file other than this report and `.ufo/waves/round-59/w1/ExecSourceLive.files/fetch-hashes.json`
  was written; no `git`/`jj` mutation, no build/test/lint run.
- The counter `c59_quote_truth.py` was imported read-only to reuse its segmentation code; it was
  not executed as a scorer and no claim state was measured (no seat scores an after-state).
- C3 after-state truth of the English entries is not asserted here: this seat only re-opened the
  pages and compared the article blocks. Whether the drafted entries quote spans that survive these
  same text nodes is a separate check for the reviewer/critic seats.
- The live page is not byte-identical to the retained body (session/flag-list churn above), so any
  check that pins the *whole-file* sha256 of a re-fetch would fail by design; only the article
  block is stable, and it is byte-identical.

VERDICT: Both C3 pages re-open live (HTTP 200, no redirect) with byte-identical article blocks to the retained bodies (0 text-node differences, 0 differing hunks inside the window); only session/feature-flag boilerplate outside the article block differs, and S425's retained article body links to the S426 URL — C3's source retention and the S425->S426 provenance are re-confirmed live.
