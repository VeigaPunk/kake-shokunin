# Round 26 W1 — FetchCritic: fetch provenance attack

Seat: `KakeR25.FetchCritic-6` (critic, read-only). Axes judged: **freshness**, **operability**.
Inputs: `.ufo/waves/round-26/fetch_sources.py`, `source_text.py`, `fetched/manifest.json`, `fetched/manifest-retry.json`, `population.json`, `contract.json`, `fetched/*.raw.gz`, `fetched/text/*.txt`.
Tools installed or updated: none (I used the existing `python3` 3.14.8 and `curl` 8.23.0).

## Verdict

The manifest is **sound as a byte-retention record**. Every recorded sha256 and byte count reproduces from the gzip files. Every `content-length` that was sent matches. Every text view equals `text_of(gunzip(raw))` for the effective fetch. `population.json` agrees with the effective fetches for all 32 rows. No redirects occurred, and no body arrived content-encoded.

The manifest does **not** by itself prove the following. Receipts and the judge must not read it as proving them:

1. That HTML pages are reproducible.
2. That a mutable reference (a tag name, `/3/`, Living Standard) points at the version the row names.
3. That any `.txt` RFC row is current in status. A `.txt` RFC cannot show "Updated by".
4. How the S008 retry was produced.

These are tradeoffs to record in receipts, not defects that block C1. The two operability defects listed under "Smallest safe corrections" can be fixed by appending.

## Local evidence (all computed from retained bytes, nothing written)

| Check | Result |
|---|---|
| sha256 and byte count against gunzip for all 35 entries (34 in manifest, plus 1 retry) | 35/35 match |
| `content-length` against bytes, where the header was sent | all match. 13 entries are chunked with `null` length (GitHub release HTML, rfc-editor, debugbear, and the failed S008) |
| `finalUrl != url` | 0/35 |
| body starts with gzip magic `1f8b` | 0/35 |
| `text/*.txt` against `text_of(gunzip(raw), content-type)` | 34/34 MATCH. `S008-1.txt` derives from `S008-1-retry.raw.gz` |
| `population.json` fetches against effective manifest (retry supersedes) | 32 rows, 0 mismatches |
| duplicate sha | `21c1cdce…7232a` is shared by S028-1 and S033-1 |
| S008 retry etag `"9b668bb3c441a095e7c39a7baa7f88a93599ab4c"` | equals the locally computed git blob SHA-1 of the retry body |

## Findings by issue

### 1. Dynamic pages (freshness)
- **GitHub release HTML (S002)** is server-rendered but per-request. The raw bytes carry `nonce="`, `request-id`, `authenticity_token`, `data-turbo` and `visitor`. The etag is weak (`W/"64eea914…"`). The page has volatile text: "11 commits to main since this release".
- **docs.github.com (S003–S007, S015)** is a Next.js render (`__NEXT_DATA__`, `"buildId"`). It sends no etag and no last-modified, so there is no server-side change signal at all. The content is in the static HTML: S007's text view holds `build_type` and `protected_domain_state` twice each, and the raw bytes hold six of each. That makes these pages decidable by quote, not by sha.
- **Google Search Central (S013, S021, S022)** has `nonce`. Its `Last-Modified` header and the visible "Last updated 2026-07-08 / 2026-07-10 / 2026-08-21 UTC" both match the row anchors.
- **WHATWG (S023–S025, S030, S031)** has `Last-Modified: Tue, 20 Oct 2026` and the visible "Living Standard — Last Updated 20 October 2026", which matches the S030/S031 anchors.
- **Proves:** these exact bytes were served at `fetchedAt`. **Does not prove:** a later GET gives the same sha. For HTML rows, sha is a retention identifier, not a freshness comparator. Freshness has to be decided by a verbatim quote at the anchor, which is what the receipt contract already requires.

### 2. Redirects and `finalUrl` (operability)
- `urllib` follows 3xx silently and records only the last URL. It does not record the hop chain or the 3xx status. All 35 entries have `finalUrl == url`, so no redirect is in evidence.
- The `HTTPError` branch (`fetch_sources.py` line 42) records the *requested* `url` as `finalUrl`, not `error.geturl()`. A redirect-then-404 would therefore record a false `finalUrl`. This was not triggered, because every status is 200 apart from the S008 timeout, which has `status: null`.
- **Fragments:** `urllib` splits `#fragment` off before sending and `geturl()` re-appends it. So `finalUrl` ending in `#section-8.8` proves nothing about the anchor. I checked anchor ids directly in the raw bytes:
  - S010 has `id="section-8.8"`.
  - WHATWG uses unquoted ids, for example `id=link-type-canonical>`. Searching for the quoted form returns a false "missing".
  - `link-type-canonical`, `the-base-element`, `the-template-element`, `start-tags` and `parsing-main-inforeign` are all present.

### 3. Compression (operability)
- `fetch_sources.py` sends no `Accept-Encoding`, and `urllib` does not decode. `HEADERS` omits `content-encoding` and `vary`, so the manifest cannot show which encoding was served.
- I inferred identity encoding from evidence: no body has gzip magic, every declared `content-length` equals the decoded bytes, and the S002 re-fetch returned `content-encoding: None`.
- The sha is over the identity representation. For static resources that is encoding-invariant: re-fetch 1 below received `content-encoding: gzip` and still decoded to the same sha.

### 4. User-agent variance (freshness)
- The sole UA was `kake-shokunin-source-recheck/26 (+GET only)`. Re-fetch 1, using curl's default UA plus `--compressed`, returned **identical** bytes for RFC 9110 txt.
- UA variance is not shown to matter for static resources, and it is untested for GitHub, Google, docs.github.com and debugbear. [INFERENCE] A non-browser UA could receive a reduced or bot variant of a dynamic page. The text views do contain the substantive content (release notes, field names, "Last updated"), so no row is UNVERIFIABLE for this reason.

### 5. 60 s timeout and the single S008 retry (operability, provenance)
- `timeout=60` in `urllib` is a per-blocking-socket-operation timeout, not a total deadline. The first S008 attempt started at 15:09:36.04Z, and S009 started at 15:10:38.38Z, so the attempt took about 62 s and ended in `TimeoutError: The read operation timed out`. The manifest still carries that attempt with `bytes: 0` and the empty-body sha `e3b0c442…b855`, with no pointer to the retry.
- **Provenance gap:** `manifest-retry.json` claims "single retry with 240s timeout". `fetch_sources.py` hardcodes `timeout=60` and only writes `manifest.json`. No retained script, command line or log produced the retry. The "retry supersedes" rule exists only in `population.json` (`fetched/S008-1-retry.raw.gz`) and in the W1 dispatch specs, not in the fetcher.
- **Mitigation (strong):** the retry body is content-addressed. Its git blob SHA-1 equals the server etag `9b668bb3…599ab4c`. `Last-Modified` equals `Date` (cgit generates it per request) and should be ignored.
- **Proves:** the bytes are blob `9b668bb3` as served for `?id=cfdb891…`. **Does not prove:** that the blob sits at `doc/tar.texi` in `cfdb891`. That is the server's assertion; it is not verified locally.

### 6. Duplicated RFC 9110 URL (S028/S033), plus S010 (freshness, duplicate authority)
- S028 and S033 are two GETs of one immutable resource with identical sha `21c1cdce…`. S028's row-pinned prefix `21c1cdce…7232a` matches, and so does S029's `3102dae4…b2d683`.
- Counting S028 and S033 as two independent freshness confirmations would be a duplicate authority. Each row is valid for its own section scope, but the evidence is one document.
- S010 is the HTML rendering of the same RFC, with a different etag (`W/"0d9f5fb8…"`).
- **Strongest counterexample to `.txt` rows as freshness evidence:** an RFC's `.txt` is immutable, so equal sha only shows the text was not altered. It cannot show status changes.
  - The retained `.txt` files (S028/S033, S029, S032, S034) carry no "Updated by" or "Obsoleted by" metadata.
  - The rfc-editor HTML does carry status. S010's HTML has only "Obsoleted by This Document" table text and no "Updated by"; the same holds for S011 and S020. S010 therefore covers RFC 9110's status for S028/S033. S029, S032 and S034 have no retained status evidence.
  - [INFERENCE, not from retained bytes] RFC 3339 (S032) is updated by RFC 9557, and RFC 3986 (S029) has later updating RFCs. Whether either affects the row's teaches cannot be decided from the retained bytes. It needs a status read such as `https://www.rfc-editor.org/info/rfc3339` and `/info/rfc3986`. I did not fetch these because my three-fetch budget was spent.

### 7. GitHub release HTML vs API (S002)
- The HTML contains the full tag commits: `7b1f4a764d45c48632c6b24a0339c27f5614fb0b` twice in S002-1 and `fc324d3547104276b827a68afc52ff2a11cc49c9` twice in S002-2. It also holds the release-notes body.
- The REST API (re-fetch 3) returns `target_commitish: "main"` and **no** 40-hex commit. The API alone therefore cannot support the row's "release tags 7b1f4a7… and fc324d3…" anchor. **HTML is the right authority for the tag-to-commit anchor.**
- The API is the better *byte-stable* carrier for the notes body: 2709 bytes of JSON, containing the identical sentence "hidden files (specifically dotfiles) will not be included in the artifact".
- Operability: the unauthenticated API showed `x-ratelimit-remaining: 45` of 60 per hour, a budget shared by every lane on this host.

### 8. Mutable references the manifest cannot pin (freshness)
- **S009** fetches tag name `release-1.28.0`, while the row pins commit `481d28cb…`. The manifest does not prove tag-to-commit. The body's git blob is `92c3eae8a153ae016412e829d7debb447223e3f1`, which can be compared against a tree listing; I did not do that.
- **S026/S027:** `/3/` is a floating alias. The text reads "Python 3.15.1 documentation", while the rows say "Python 3.15". `Last-Modified` is 2026-10-21 13:04, so the sha will change on every docs rebuild.
- **S016:** `Last-Modified: Wed, 13 Aug 2025`, unchanged since before the row opened. The bytes list `"jekyll":"3.10.0"`.

### 9. Line-number anchors versus text views (operability; affects every row seat)
- `source_text.normalize` collapses all whitespace, so every `text/*.txt` file is a single line. Line anchors (S001 lines 17–20 and 37–39, S008 lines 8478–8617, S009 lines 1682 and 1708–1710) **cannot be observed in the text views**. A receipt's `anchorObserved` for those rows must cite raw-byte line numbers.
- Raw checks:
  - S009 line 1682 is `ngx_http_set_etag(ngx_http_request_t *r)`, and lines 1708–1710 contain the `"\"%xT-%xO\""` sprintf.
  - S008 lines 8478 and 8617 are `@end menu` and the `@item Inclusion` table row, with the section's `Controlling Pattern-Matching` heading at line 8481.
- **S001 lines 17–20 hold `include-hidden-files` only in fetch index 2** (main `5f327015`). In index 1 (v4.0.0 `7b1f4a76`), lines 17–20 are `outputs: artifact_id`. A receipt with `fetchIndex: 1` would mis-anchor. Row seats must use index 2 for this anchor.

## Re-fetches (3 of 3 allowed, plain GET, bodies held in memory only, nothing saved)

| # | URL | Method | Outcome |
|---|---|---|---|
| 1 | `https://www.rfc-editor.org/rfc/rfc9110.txt` (S028/S033) | curl 8.23.0 default UA, `--compressed`, 2026-10-21T15:29:51Z, 0.3 s | HTTP/2 200, `content-encoding: gzip`, decoded 502941 bytes, sha `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, **identical** to the manifest. The etag is now strong (`"7c9fc…"`) where it was weak (`W/"7c9fc…"`); only the weak marker differs with encoding |
| 2 | `https://github.com/actions/upload-pages-artifact/releases/tag/v4.0.0` (S002-1) | urllib with the fetcher's exact UA, 15:29:51Z, 0.6 s | 200, no redirect, `content-encoding` None, 200869 bytes (was 200830), sha `55fff4e6…d052` **differs** from `455adcec…334f`, etag `W/"bda724ae…"` was `W/"64eea914…"`. The text view is word-for-word identical (3482 against 3483 chars, whitespace only), and the key sentence is present |
| 3 | `https://api.github.com/repos/actions/upload-pages-artifact/releases/tags/v4.0.0` | urllib, same UA, `Accept: application/vnd.github+json`, 15:29:52Z, 0.3 s | 200, 2709 bytes, sha `a4d7f2ee836c2dfdbcc97f7be78e4e6cc70eb6a821147188cdfb80d5d60fd9d7`, `tag_name` v4.0.0, `target_commitish` main, `published_at` 2025-08-14T19:21:06Z, body contains the dotfile sentence, no 40-hex commit |

## What the manifest proves and does not

| Proves | Does not prove |
|---|---|
| These exact bytes were served once, at `fetchedAt` (the start time), with the recorded status and 5 headers | That re-fetching reproduces the sha for HTML rows (S002 was disproved within 20 minutes) |
| The body is the identity representation (inferred: no gzip magic, content-length matches) | Which encoding or `vary` the server negotiated; `content-encoding` is not recorded |
| No redirect landed elsewhere (`finalUrl == url`) | The redirect hop chain, or fragment and anchor existence |
| S028/S029 bytes are identical to what was opened (pinned sha prefixes match) | RFC status currency for `.txt` rows (S029, S032, S034); S028/S033 are covered only through S010's HTML |
| S008's retry body is a specific git blob | How the retry was run (no code retained); that the blob is in `cfdb891` |
| Retention integrity: manifest, gz, text and population agree | Tag-to-commit for S009, the version behind `/3/` for S026/S027, or two independent confirmations from S028 and S033 |

## Smallest safe corrections (append-only, no rewrite of retained bytes)
1. **Operability, provenance.** Append the exact retry command or script to the round directory, or a `retry` note in `manifest-retry.json` naming the code path and its 240 s timeout. Until then, record in receipts and the judge that the S008 retry is unretained-code provenance, mitigated by blob-etag equality.
2. **Operability.** The judge or counter should resolve effective fetches as "retry supersedes same row and index", which the spec already does. It should never read `manifest.json` alone for S008, because that yields an empty body.
3. **Freshness.**
   - Receipts for HTML rows should cite a quote and the anchor, never sha equality.
   - Receipts for S028 and S033 count as **one** document confirmation.
   - Receipts for S029 and S032, and for S034 to a lesser degree, should state that the `.txt` bytes cannot establish RFC status. They should be HOLD only on content-at-anchor, with status currency explicitly outside what the manifest proves. Alternatively, L1 can add one status GET per RFC in a later fetch.
4. **Row seats.** For S001, S008 and S009, `anchorObserved` must cite raw-byte line numbers, and S001's lines 17–20 anchor must use `fetchIndex: 2`.
5. **Fetcher hygiene (future rounds; not needed for r26).**
   - Add `content-encoding` and `vary` to `HEADERS`.
   - Record `error.geturl()` in the `HTTPError` branch.
   - Record completion time next to `fetchedAt`.

Impacted axes: freshness (findings 1, 4, 6, 8), operability (findings 2, 3, 5, 9). No defect found forces the canonical judge to reject C1, provided receipts follow corrections 2–4.
