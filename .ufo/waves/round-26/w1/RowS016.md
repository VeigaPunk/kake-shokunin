# RowS016 — round 26 freshness recheck

Seat: `KakeR25.RowS016-6`. Row: `corpus/SOURCES.md:24` (S016, tier A, kind dataset, cadence 90d, used-by —).
Source re-fetched this round: `#1 https://pages.github.com/versions.json` — HTTP 200, fetchedAt `2026-10-21T15:10:41Z`, body sha256 `0a713bab52e15579fda7f76e71da0283e8260e217e448fd56d704801212c4542` (1,287 B, 47 keys), gz file sha256 `77b2ab695e5da8efbd6748b461bab76d2008a660a8eb92839d317f1cef3f972f`; `gzip -dc` of the retained gz is byte-identical to `fetched/text/S016-1.txt`.

```json
{"id":"S016","verdict":"HOLD","fetchIndex":1,"quote":"\"jekyll\":\"3.10.0\",\"jekyll-sass-converter\":\"1.5.2\",\"kramdown\":\"2.4.0\"","anchorObserved":"Single-line JSON object: key `jekyll` is the first key (byte 2); `jekyll-sass-converter` and `kramdown` follow. The same object's `github-pages` key reads `\"232\"`, and `ruby`:`\"3.3.4\"` sits beside it; no headings or sections exist in a JSON body.","reason":"At the 2026-10-21 re-fetch the catalog still lists `jekyll` 3.10.0 and `github-pages` 232 exactly as the row teaches, with the same JSON-key anchor intact, so scope (public GitHub Pages build-catalog dependency versions), anchor and teaches all still hold; the served object is also unchanged since before the row's 2026-10-19 fetch, so there is no drift window.","correction":null}
```

Caveats (≤10 lines):

- Living dataset URL, no commit/tag pin: this is a content-drift plus availability test. Drift risk is low because the response's `last-modified: Wed, 13 Aug 2025 12:02:55 GMT` and `etag: "689c7eef-507"` (0x507 = 1,287 B) predate the row's 2026-10-19 fetch, so the bytes were already stable across both access dates.
- Row cells quoted from `corpus/SOURCES.md:24`; nothing in the row needed changing. No correction text and no `[r26-recheck S016 STALE]` block required.
- Anchor contains a historical access date ("fetched 2026-10-19"); that statement remains true of the original open. This round's recheck date is 2026-10-21, not a correction to the anchor.
- Quote-count note: the body is a single-line JSON object with no whitespace, so the quote is six comma-separated key:value tokens (contiguous, taken verbatim from the text view starting at byte 2); a whitespace-based word counter would read the whole line as one word.
- Second load-bearing value (`github-pages`:`"232"`) is not contiguous with the quoted head; it was verified directly in the same parsed object (47 keys) and is cited in `anchorObserved`/`reason`.
- Unrelated to freshness: `corpus/lessons/round-20.md:218` renders the same pair as `"jekyll": "3.10.0", "github-pages": "232"` (spaces added). That is a presentation normalization of an unchanged value, not dataset drift.
- No tools installed or updated; no builds/tests/linters run; no browsers or property probes — only the retained round-26 bytes, the manifest, and the row line.
- Remaining unknown: none for this row; the verdict is decidable from retained bytes.
