# Falsify S016 — round-26 C1 freshness recheck (receipt HOLD)

Seat: `KakeR26-2.FalsifyS016` (leaf member — no subagent dispatch). Milestone `r26-recheck-falsify`. Axis: **freshness**.
Target: `.ufo/waves/round-26/rechecks/S016.json` (verdict HOLD) and the SOURCES row `corpus/SOURCES.md:24`.

Goal: try to show the receipt is WRONG — (a) the quote does not ground this row's `teaches` (page chrome / neighbouring clause instead), (b) the `anchorObserved` is mislocated in the raw bytes, (c) content or version changed in a way the receipt missed.

**Verdict: AGREE** — the receipt survives every falsification attempt I ran. Severity of residual observations: low; **no change to the receipt is required**.

## What the row claims (the ground truth under attack)

`corpus/SOURCES.md:24` (identical in base `97404de4` and candidate `e28312b1`; the only SOURCES.md delta in this round is the appended round-26 note at line 76):

```
| S016 | GitHub Pages dependency versions — https://pages.github.com/versions.json | dataset | A | Dependency versions in the public GitHub Pages build catalog | JSON keys jekyll and github-pages; fetched 2026-10-19 | At fetch time the dataset lists Jekyll 3.10.0 and the github-pages gem 232 | queued | 2026-10-19 | 90d | — |
```

- teaches: *“At fetch time the dataset lists Jekyll 3.10.0 and the github-pages gem 232”* → two load-bearing values: `jekyll` = `3.10.0`, `github-pages` = `232`.
- anchor: *“JSON keys jekyll and github-pages; fetched 2026-10-19”* → two named JSON keys.

Receipt under attack (`rechecks/S016.json:1-10`), byte-identical in the worktree and at candidate `e28312b1` (both sha256 `d6b10708a7a49a401c46f40e8ec026b7c01a710c9f16179d1533fc1a25291564`); absent at base `97404de4` (round-26 added it):

```json
{"id":"S016","verdict":"HOLD","fetchIndex":1,
 "quote":"\"jekyll\":\"3.10.0\",\"jekyll-sass-converter\":\"1.5.2\",\"kramdown\":\"2.4.0\"",
 "anchorObserved":"Single-line JSON object: key `jekyll` is the first key (byte 2); `jekyll-sass-converter` and `kramdown` follow. The same object's `github-pages` key reads `\"232\"`, and `ruby`:`\"3.3.4\"` sits beside it; no headings or sections exist in a JSON body.",
 "reason":"At the 2026-10-21 re-fetch the catalog still lists `jekyll` 3.10.0 and `github-pages` 232 exactly as the row teaches, with the same JSON-key anchor intact, so scope (public GitHub Pages build-catalog dependency versions), anchor and teaches all still hold; the served object is also unchanged since before the row's 2026-10-19 fetch, so there is no drift window.",
 "correction":null}
```

## Attack 1 — Does the quote ground THIS row's teaches (not page chrome, not a neighbouring clause)? → NO DEFECT

Retained bytes `fetched/S016-1.raw.gz` (decompressed 1 287 B, sha256 `0a713bab52e15579fda7f76e71da0283e8260e217e448fd56d704801212c4542`) and the committed text view `fetched/text/S016-1.txt` are **byte-identical** (both 1 287 B, same sha256) — the view is the body plus its single trailing `\n`:

```
{"jekyll":"3.10.0","jekyll-sass-converter":"1.5.2","kramdown":"2.4.0",…,"ruby":"3.3.4","github-pages":"232","html-pipeline":"2.14.3",…,"nokogiri":"1.16.7"}
```

- The quote is the **opening of the JSON object itself**, byte offset 1 of the raw body (`raw.find(b'"jekyll"') == 1`), not a page header, nav or sidebar — there is no chrome in a JSON body.
- It carries the row's first load-bearing value verbatim: `"jekyll":"3.10.0"`.
- Word-bounded, unique: `re.search(r"(?<!\w)" + re.escape(normalize(quote)) + r"(?!\w)", text)` → **match span (1, 69)**, one occurrence; `grep -lF '"jekyll":"3.10.0","jekyll-sass-converter":"1.5.2","kramdown":"2.4.0"' .ufo/waves/round-26/fetched/text/*.txt` → **only `S016-1.txt`** (satisfies the contract-amendment row-specificity rule; S016 is in no document group).
- Counter rule (`.ufo/waves/round-26/measure.py:386-392`): `tokens = len(re.findall(r"[^\W_]+", quote)) = 14 ≥ 6`; `words = len(quote.split()) = 1 ≤ 25` → passes `quote_word_count` and `quote_not_in_text`.
- The **second** load-bearing value (`github-pages` = `232`) is **not contiguous** with the quote — it sits 39 keys later at raw byte 1185 (`"ruby":"3.3.4","github-pages":"232"`). It is therefore asserted in prose (`anchorObserved`, `reason`) rather than inside the quote. I verified the value directly in the parsed object: `json.loads(raw)` → 47 keys, `d["jekyll"] == "3.10.0"`, `d["github-pages"] == "232"`, `d["ruby"] == "3.3.4"`.
  This is a **weakness of form, not of verdict**: the anchor cell itself names the two keys (`JSON keys jekyll and github-pages`), the anchorObserved states both observed values with their location, and a contiguous quote spanning byte 1→1185 would be a 1 184-byte span (one whitespace “word”, ~236 tokens) — that would satisfy the amended token rule but not the spec's “6-25 words”. The amendment explicitly anticipated this body: *“S016 is a whitespace-free JSON body”* (`contract-amendment.json:12`). No contiguous quote can carry both taught values in a proportionate span, so the seat's choice (quote the head, document the tail) is the correct trade-off, not a mis-grounding.

## Attack 2 — Is `anchorObserved` correct in the raw bytes? → NO DEFECT

Every locator in `anchorObserved` was checked against `fetched/S016-1.raw.gz` (offsets 0-based):

| claim | raw evidence | verdict |
|---|---|---|
| “Single-line JSON object” | `raw.count(b'\n') == 1` (trailing LF only); 1 287 B, one JSON object | ✓ |
| “key `jekyll` is the first key (byte 2)” | `raw[0:3] == b'{"j'` → `{`=0, `"`=1, `j`=2; `json.loads(raw)` first key = `jekyll` | ✓ |
| “`jekyll-sass-converter` and `kramdown` follow” | offsets 19 and 51, in that order, immediately after | ✓ |
| “`github-pages` key reads `\"232\"`” | offset 1185 → `"github-pages":"232"` | ✓ |
| “`ruby`:`\"3.3.4\"` sits beside it” | `ruby` at 1170, `github-pages` at 1185 → `"ruby":"3.3.4","github-pages":"232"` (adjacent) | ✓ |
| “no headings or sections exist in a JSON body” | single flat object, no markup | ✓ |

The SOURCES row’s anchor “JSON keys jekyll and github-pages” still resolves: both keys exist in the 2026-10-21 body, unchanged.

## Attack 3 — Did content or version change in a way the receipt missed? → NO DEFECT

1. **Independent live GET** (one plain GET of the URL already in `corpus/SOURCES.md`, `curl 8.23.0`, 2026-10-21 ~16:28 UTC) — body sha256 **`0a713bab52e15579fda7f76e71da0283e8260e217e448fd56d704801212c4542`, content-length 1287 — byte-identical to the retained wave bytes** (`fetched/manifest.json:301-317`, `sha256` and `bytes` fields). `jekyll` still `3.10.0`, `github-pages` still `232`. No version drift, no content drift, no drift window.
2. **Round-26 population pin agrees**: `population.json` S016 → `sha256 0a713bab…c4542`, `file fetched/S016-1.raw.gz`; `manifest.json` S016 index 1 → same sha256, status 200, `error: null`, `fetchedAt 2026-10-21T15:10:41.481034+00:00`; the committed blob at `e28312b1` for `S016-1.raw.gz` hashes `77b2ab695e5da8efbd6748b461bab76d2008a660a8eb92839d317f1cef3f972f`, identical to the worktree file. The receipt’s `fetchIndex: 1` is the row’s only population fetch.
3. **Receipt shape**: exactly the 7 required keys (`id, verdict, fetchIndex, quote, anchorObserved, reason, correction`), `id == "S016"`, `verdict == "HOLD"`, non-empty `reason`, non-empty `anchorObserved`, `correction: null` (required for HOLD by `measure.py:396-398`). Row-level verdicts across all 32 receipts: `HOLD 32`, `STALE 0`, `UNVERIFIABLE 0` — matching the round-26 note at `corpus/SOURCES.md:76`.
4. **No stale adjudication owed for this row**: `grep -rn "S016" corpus/` → only `SOURCES.md:24`, `SOURCES.md:65` (round-20 gate note) and `corpus/lessons/round-20.md:218`. The registry row’s `used-by` is `—`, and `statements.json` `pairs` contains **no S016 entry** (all 25 pairs point at `corpus/knowledge/*.md` files; S016 is cited by no knowledge entry). So no `[r26-recheck S016 STALE]` block is required or expected, and none exists (`grep -rn "r26-recheck S016" corpus/` → no matches). Consistent.

## Residual observations (low severity; none requires changing the receipt)

**R1 — the receipt’s *supporting* stability argument leans on a header that is not stable (evidence in `w1/RowS016.md`, not in the receipt).** The wave receipt cites `last-modified: Wed, 13 Aug 2025 12:02:55 GMT` / `etag: "689c7eef-507"` (`fetched/manifest.json:307-311`). My independent GET at 16:28:33 UTC returned `etag: "689c7eee-507"` and `last-modified: Wed, 13 Aug 2025 12:02:54 GMT` — **one second earlier** — while `content-length: 1287` and the body sha256 were identical. Both etags are `<hex-mtime>-<hex-len>` (0x689c7eef → 2025-08-13 12:02:55 UTC, 0x507 = 1287), so the *validator* changed between two same-day requests for the same unchanged bytes (different CDN edge: `x-github-edge-region: brazilsouth`, `x-cache: MISS`). Consequence: the w1 caveat’s inference “the bytes were already stable across both access dates” is sound only if it rests on the **body digest**, not on ETag/Last-Modified equality. The receipt itself (`rechecks/S016.json`) cites neither header — it asserts content stability, and that assertion is independently confirmed above. Minimal correction: none to the receipt; the w1 caveat line may be tightened to say “body sha256 identical across both 2026-10-21 fetches” instead of citing ETag stability.

**R2 — `corpus/lessons/round-20.md:218` renders the pair as if adjacent and space-separated:** `` `"jekyll": "3.10.0", "github-pages": "232"` ``. In the actual body the keys are 1 184 bytes apart and written without spaces (`"jekyll":"3.10.0"`, separately `"github-pages":"232"`). The two *values* are exactly right and the line’s date (`fetched 2026-10-19`) is a historical record, so under the round-26 rule (`statements.json:rule` — “Historical dates … are not stale”; “quote fidelity” bites only when a statement’s substance misquotes) this is a presentation normalization, not a stale statement; the w1 caveats already flagged it as such. `corpus/lessons/round-20.md` is a lessons file, not a `corpus/knowledge/*` entry, and the ledger has no S016 pair, so no `[r26-recheck S016 STALE]` block is owed. Residual risk: a reader could take that cell for a literal contiguous fragment of the dataset. Fix would be an EOF block in `corpus/lessons/round-20.md` — **not required by the contract** (append-only, knowledge-entry scope) and not requested by my item; recorded here only so the reviewer sees it was considered and rejected as a basis for DISAGREE.

**R3 — byte-offset nit in the w1 report (not in the receipt).** `w1/RowS016.md` says the quote was “taken verbatim from the text view starting at byte 2”; the quote string itself begins at byte 1 (its leading `"`), byte 2 being the `j` of `jekyll`. The receipt’s own wording (“key `jekyll` is the first key (byte 2)”) is correct as written. Cosmetic only.

## Verification gaps / limits of this attack

- I did not re-derive the 2026-10-19 body: no bytes from that date are retained in the lane, so “unchanged since before the row’s 2026-10-19 fetch” rests on (a) the origin `last-modified` date 2025-08-13 preceding the row’s open, (b) the corpus’s own 2026-10-19 record of the same two values (`corpus/lessons/round-20.md:218`), and (c) identical body bytes across two independent 2026-10-21 fetches (wave fetch + my GET). The teach values are unchanged under all three.
- Per the lane bounds I did not read, run, retry or re-route round-24 material, did not probe any property, did not use a browser, and did not touch the corpus, scripts, fleet repo, sibling lanes, or the lane Git index/jj. Only my report file was written.
- I did not run `measure.py` (my item names only the receipt, the SOURCES row, the retained bytes and one GET), so the counter’s own verdict for S016 is asserted from reading `measure.py:341-404` plus my manual replay of its quote rules (token/word counts, word-bounded match, cross-row uniqueness) — all of which I ran directly and all of which pass.

## Process note / bound compliance

- Tools used, none installed or updated: `curl 8.23.0` (system package, OpenSSL 3.6.5), `python3 3.14.8`, `gzip`, `sha256sum`, `grep`. No pacman/uv/cargo/npm transaction was performed; the host-wide pacman pause was therefore untouched.
- One plain public GET of `https://pages.github.com/versions.json` (a documentation URL already listed in `corpus/SOURCES.md`) was made for the drift comparison. It was written to a temporary path and deleted immediately after the digest/length comparison; no copy was retained and no corpus, script or wave file was modified by it. All other checks ran on the committed retained bytes.
- Files written by me: this report only (`.ufo/waves/round-26/w2/FalsifyS016.md`).

```json
{"target":".ufo/waves/round-26/rechecks/S016.json","verdict":"AGREE","severity":"low"}
```
