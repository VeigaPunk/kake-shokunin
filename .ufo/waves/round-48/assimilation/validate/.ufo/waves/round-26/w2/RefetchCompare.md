# RefetchCompare — live refetch of all 34 population URLs, receipt-quote persistence

- Seat: `KakeR26-2.RefetchCompare` (critic, leaf). Axis: **freshness**. Milestone: r26-recheck-falsify. Checked 2026-10-21T16:28:57–16:29:00Z.
- Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
- Lane root: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

## Verdict: AGREE

I refetched every recorded population URL once, regenerated text with the committed helper, and could not make any receipt quote disappear. Every one of the 32 receipt quotes still occurs in today's live text, and every SHA-256 / Last-Modified value asserted in a receipt `reason` matches the live response. No counterexample found; no correction needed.

## Method (exactly what ran)

1. Read the 34 fetch records from `.ufo/waves/round-26/fetched/manifest.json`, with `manifest-retry.json` superseding S008 index 1 (the documented 60 s timeout retry).
2. One plain public GET per record, in memory only: `urllib.request`, `User-Agent: kake-shokunin-source-recheck/26 (+GET only)` (the same UA `fetch_sources.py` uses), no credentials, cookies, forms or auth. Bodies were never written to disk.
3. Text regenerated with the committed `.ufo/waves/round-26/source_text.py`: `text = normalize(text_of(body, live_content_type))`.
4. Quote test mirrors `measure.py:273-276` `quote_in_text`: `re.search(r"(?<!\w)" + re.escape(normalize(quote)) + r"(?!\w)", text)`.
5. Population coverage re-derived from `corpus/SOURCES.md` with `fetch_sources.py`'s own row/URL rule (`EXCLUDED = {S014, S019, S035}`): 32 rows → 34 (row, index, url) records, and the manifest URL set is **exactly equal** to that set (no URL added, dropped or substituted). 34 records cover 33 distinct URLs because S028 and S033 both record `rfc9110.txt`.

## Result: 34/34 live fetches succeed, 32/32 receipt quotes persist

All 34 returned HTTP 200 with `finalUrl` identical to the recorded URL (no redirect, no consent/login page). Quote column is "receipt quote occurs word-bounded in today's text"; `-` means that fetch carries no receipt quote (S001 idx 1 and S002 idx 2 are cited only in `reason`/`anchorObserved`).

| row | idx | receipt fi | HTTP | live bytes | live sha == retained sha | live text == retained text | quote occurs |
|---|---|---|---|---|---|---|---|
| S001 | 1 | – | 200 | 2,529 | yes | yes | – |
| S001 | 2 | 2 | 200 | 2,895 | yes | yes | **yes** |
| S002 | 1 | 1 | 200 | 200,910 (+80 B) | no | yes | **yes** |
| S002 | 2 | – | 200 | 205,120 (+85 B) | no | yes | – |
| S003 | 1 | 1 | 200 | 154,136 | yes | yes | **yes** |
| S004 | 1 | 1 | 200 | 141,818 | yes | yes | **yes** |
| S005 | 1 | 1 | 200 | 240,439 | yes | yes | **yes** |
| S006 | 1 | 1 | 200 | 138,096 | yes | yes | **yes** |
| S007 | 1 | 1 | 200 | 453,447 | yes | yes | **yes** |
| S008 | 1 | 1 | 200 | 512,359 | yes (retry) | yes | **yes** |
| S009 | 1 | 1 | 200 | 147,410 | yes | yes | **yes** |
| S010 | 1 | 1 | 200 | 1,187,554 | yes | yes | **yes** |
| S011 | 1 | 1 | 200 | 82,367 | yes | yes | **yes** |
| S012 | 1 | 1 | 200 | 45,292 | yes | yes | **yes** |
| S013 | 1 | 1 | 200 | 191,341 (same length) | no | yes | **yes** |
| S015 | 1 | 1 | 200 | 88,733 (same length) | no | yes | **yes** |
| S016 | 1 | 1 | 200 | 1,287 | yes | yes | **yes** |
| S017 | 1 | 1 | 200 | 187,320 | yes | yes | **yes** |
| S018 | 1 | 1 | 200 | 55,919 | yes | yes | **yes** |
| S020 | 1 | 1 | 200 | 18,428 | yes | yes | **yes** |
| S021 | 1 | 1 | 200 | 194,799 (same length) | no | yes | **yes** |
| S022 | 1 | 1 | 200 | 178,056 (same length) | no | yes | **yes** |
| S023 | 1 | 1 | 200 | 381,019 | yes | yes | **yes** |
| S024 | 1 | 1 | 200 | 333,092 | yes | yes | **yes** |
| S025 | 1 | 1 | 200 | 276,128 | yes | yes | **yes** |
| S026 | 1 | 1 | 200 | 55,260 | yes | yes | **yes** |
| S027 | 1 | 1 | 200 | 119,730 | yes | yes | **yes** |
| S028 | 1 | 1 | 200 | 502,941 | yes | yes | **yes** |
| S029 | 1 | 1 | 200 | 141,811 | yes | yes | **yes** |
| S030 | 1 | 1 | 200 | 89,196 | yes | yes | **yes** |
| S031 | 1 | 1 | 200 | 826,255 | yes | yes | **yes** |
| S032 | 1 | 1 | 200 | 35,064 | yes | yes | **yes** |
| S033 | 1 | 1 | 200 | 502,941 | yes | yes | **yes** |
| S034 | 1 | 1 | 200 | 28,360 | yes | yes | **yes** |

- **Receipt quotes checked: 32/32. Occurring: 32/32. Absent: 0.**
- The six raw-digest differences are transient bytes only: S002 index 1/2 grew by 80/85 bytes of GitHub release-page hydration, and S013/S015/S021/S022 are byte-length-identical with a different digest (regenerated nonce/asset markers). In every case `normalize(text_of(live))` is **character-identical** to `normalize(text_of(retained))` — 34/34 text equality.
- All 34 committed `fetched/text/*.txt` views reproduce exactly from the retained `.raw.gz` under the current `source_text.py` (34/34), so the comparison baseline is the same text the receipts were written against.

### Negative control (the test can fail)

On S012's live text, the unmodified quote matches (`True`); `Sitemap → Sitemapx` and `determines → defines` both return `False`. The word-bounded matcher is not vacuously passing.

## Supplementary checks that also hold

- **Pinned/immutable sources are byte-identical today.** Live SHA-256 equals the retained digest for S001 both copies (`4524ed61…`, `e8ce828a…`), S008 retry (`93281a63…`), S009, S010, S011, S012, S016 (`0a713bab…`, unchanged since 2025-08-13), S017, S018, S020, S023–S034.
- **Every body digest asserted in a receipt `reason` matches the live bytes:** S004 `5c15ef2d…`, S005 `dc89eecd…`, S007 `4f4449ba…`, S008 `93281a63…`, S026 `d92217e0…`, S028 `21c1cdce…7232a`, S029 `3102dae4…`, S031 `a11dcf17…`, S033 `21c1cdce…`, S034 `61a5378f…`.
- **Every Last-Modified claim matches the live header:** S012 `Thu, 15 Dec 2022 10:54:02 GMT`; S013 `Wed, 08 Jul 2026 15:47:49 GMT`; S021 `Fri, 10 Jul 2026 10:12:15 GMT`; S022 `Fri, 21 Aug 2026 11:28:27 GMT`; S024/S025 `Tue, 20 Oct 2026 12:58:32 GMT`; S026 `Wed, 21 Oct 2026 13:04:30 GMT`; S027 `13:04:29 GMT`; S030/S031 `Tue, 20 Oct 2026 12:58:33 GMT`.
- **41 curated anchor strings from `reason`/`anchorObserved` checked; all resolve.** Three initial misses were my attribution error, not defects: S017's CNAME sentence belongs to the S005 custom-domain page and is present there verbatim (and absent from S017 by design — that is the contradiction the row teaches); S021/S022 footers render `Last updated 2026-07-10 UTC` / `2026-08-21 UTC`, matching the claimed dates.
- **S001's reason survives line-level checking:** live S001-2 raw lines 17-20 carry `include-hidden-files … default: "false"`, and the `.git`/`.github` pair is unconditional at lines 37-38, 55-56, 73-74 (3 boundary-counted `.git`, 3 `.github`). S001-1 still has no `include-hidden-files` and hard-codes `--exclude=".[^/]*"` exactly 3 times.
- **Quote specificity still holds today:** no receipt quote occurs word-bounded in any non-group row's live text (group `{S010,S028,S033}` excluded, as the amendment allows).

## Limits of this check (no verdict impact)

- My GETs landed at 2026-10-21T16:28:57–16:29:00Z, **~78–80 minutes after** the retained fetches (`15:09:32.237330Z` … `15:11:01.972009Z`). This establishes same-day reproducibility of every quote; it does not establish multi-day persistence.
- `docs.github.com` responses came back CDN-cached (`age: 4763`, `x-cache: MISS, HIT` on S003–S006; `age: 950/24/11/0` elsewhere), so my copy could be the same edge object the author received around 15:09Z. The pages' own old `Last-Modified` values and the unchanged text still support each receipt, but the CDN does bound how independent this recheck is of the author's fetch.
- Disclosed deviation: I issued one reachability probe GET to the S034 URL just before the batch, i.e. **35 requests over 34 records / 33 distinct URLs**. There were no retries, no reruns and no partial results folded in.
- S001 idx 1 and S002 idx 2 carry no receipt quote, so there is no quote expectation there; both still returned 200 and produced text identical to the retained text, and S002 idx 2 still carries `feat: add include-hidden-files input @jonchurch (#137)`.
- Observation, no severity: S001's receipt quote `(those starting with a dot) in the artifact. Excludes.git and.github regardless.` matches only under the contract's normalization — raw S001-2 line 18 reads `Excludes .git and .github`. `measure.py:273-276` compares normalized quote to normalized text by design, so this is contract-conforming, not a defect.

No tools were installed or upgraded; `python3` (stdlib only) was already present, and no package transaction was attempted under the host-wide pacman pause. Nothing outside this report file was written; no corpus, script, fleet, sibling-lane or Git state was touched.

```json
{"target":".ufo/waves/round-26/fetched/manifest.json (34 live refetch records / 32 receipt quotes)","verdict":"AGREE","severity":"none"}
```
