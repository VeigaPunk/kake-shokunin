# CitingSweep06 — blind citing-set data-walk: ghp-custom-domain.md + ghp-etag-anatomy.md

Seat: KakeR27.CitingSweep06 (leaf, read-only findings). Round 27, wave 1, milestone r27-full-citing-set; axis freshness.
Targets, exactly: `corpus/knowledge/ghp-custom-domain.md`, `corpus/knowledge/ghp-etag-anatomy.md`.
Revisions: frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
Ordering: manual census completed first; parser/oracle comparison only afterwards. No network, no source or public-site
evaluation, no tool installs, no production edits. Scratch: `/fast/scratch/hyaku/kake-r27/CitingSweep06/census.json`.

## 0. Identity (base = declarations = worktree, byte-identical)

| path | lines/bytes | sha256 | git blob @base = @decl | frozen/expected.json |
|---|---|---|---|---|
| corpus/knowledge/ghp-custom-domain.md | 62 / 4475 | `65dd561af5cc7b189ae97caf67a52aa85ff794dc11c164cf07d2e0f91a7b19b6` | `dda34134c435fb701b81f251fc7a52d463f1432d` | match |
| corpus/knowledge/ghp-etag-anatomy.md | 70 / 5806 | `fa71ecd60370f81ec9d5ec596cc04483221392b9901068b4e92cef881a801d95` | `650387046beccbc1c2c92686c1fd65783fb3d20b` | match |

`git status --porcelain` for both paths is empty; `git diff 83528f7..be375d9 -- corpus/knowledge` is empty.

## 1. Manual census — every S-id reference (14 + 22 tokens)

Legend: G = grouped list, L = literal standalone, E = filename-embedded (`Pre…S0NN…`), P = placeholder glob (not a source id).
Word counts are `split()` counts of the located span; spans longer than 25 words are clipped (…).

### ghp-custom-domain.md — 14 tokens, 9 lines, 4 unique ids, 0 embedded, 0 ranges

| line | form | id(s) | scope | located support (≤25 words) |
|---|---|---|---|---|
| 1 | G header | S003, S005, S007 | provenance header; one source group for the entry, but the single URL is S005's managing-a-custom-domain page | `source: S003, S005, S007 (corpus/SOURCES.md) — https://docs.github.com/…managing-a-custom-domain… §Configuring an apex domain` (clipped) |
| 18 | L bullet | S005 | Source checks: §Configuring an apex domain, step 4 quote | `S005, Configuring an apex domain, step 4: "no CNAME file is created, and any existing CNAME file is ignored"` (19w) |
| 20 | L, same bullet | S005 | S005 recommendation: domain verification, wildcard warning | `S005 recommends domain verification and warns against wildcard DNS records.` (11w) |
| 22 | L bullet | S003 | Source checks: custom-workflow NOTE quote | `S003, custom-workflow NOTE: "A CNAME file in your repository file does not automatically add or remove a custom domain."` (19w) |
| 25 | L bullet | S007 | Source checks: Get a Pages site response schema | `S007, Get a Pages site response schema: cname is string-or-null and build_type is legacy, workflow, or null` (17w) |
| 32 | L | S005 | Falsifier: branch mode writes a root CNAME | `branch mode, S005 says saving the custom domain writes a root CNAME file.` (14w) |
| 52 | L | S007 | Post-review correction r20: quote-format erratum | `S007 quote-format erratum: the earlier gate's "cname: required, string or null" is a schema transcription` (15w) |
| 57 | L | S007 | same section: field claim supported by S007 schema | `field claim remains supported by S007 §Get a GitHub Pages site, response schema` (12w) |
| 62 | G + L + P | S003, S005, S007, S008; `S0NN` | Round-26 EOF recheck provenance: three rows via manifest.json, S008 via manifest-retry.json; receipts glob is not an id | `Rows S003, S005 and S007 were re-fetched by one public GET each (.ufo/waves/round-26/fetched/manifest.json, S008 via manifest-retry.json)` (16w) |

Token totals: S003 ×3, S005 ×5, S007 ×5, S008 ×1. Occurrences on distinct scopes: header, 8 body lines, EOF note.

### ghp-etag-anatomy.md — 22 tokens, 10 lines, 3 unique ids, 6 embedded, 0 ranges

| line | form | id(s) | scope | located support (≤25 words) |
|---|---|---|---|---|
| 1 | G header | S009, S010 | provenance header; the single URL is S009's nginx source; S010's RFC URL is absent (r26 reclassified precision note) | `source: S009, S010 (corpus/SOURCES.md) — https://raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c §ngx_http_set_etag` (10w) |
| 22 | L bullet | S009 | Source checks: file lines 1708–1710, release-1.28.0 | `S009, src/http/ngx_http_core_module.c:1708-1710, release-1.28.0 source` (4w) |
| 24 | L bullet | S010 | Source checks: §8.8.3 quote | `S010 §8.8.3: "An entity tag is an opaque validator for differentiating between multiple representations of the same resource."` (18w) |
| 25 | L, same bullet | S010 | §8.8.1 paraphrase (weak-validator condition) | `S010 §8.8.1 notes: "a representation's modification time… might be a weak validator" when changed twice within that second` (19w) |
| 60 | G + L + P | S009, S010, S008; `S0NN` | Round-26 EOF recheck provenance: two rows via manifest.json, S008 via manifest-retry.json | `Rows S009 and S010 were re-fetched by one public GET each (.ufo/waves/round-26/fetched/manifest.json, S008 via manifest-retry.json)` (15w) |
| 62 | L + E | S010 ×2, S009 ×1, E:S010 | r26 STALE marker: locator correction for line 1 | `[r26-recheck S010 STALE] Locator correction for line 1: the URL there is S009's nginx source only.` (17w) |
| 64 | L + E | S010 ×1, E:S010, E:S009 | r26 STALE marker: §8.8.1 paraphrase condition | `[r26-recheck S010 STALE] Lines 25-28 paraphrase the §8.8.1 condition as "when changed twice within that second".` (18w) |
| 68 | L + E | S010 ×2, E:S010 | falsify-wave adjudication: reclassified precision note | `Line 1 lists several source ids before one URL… The S010 URL stays as given there.` (18w) |
| 69 | E only | E:S010 (`Correction4S010.md`) | precision note on the §8.8.1 paraphrase | `the block's paraphrase drops "if it is possible for" (w2/Correction4S010.md)` (10w) |
| 70 | L + E | S009 ×2, E:S009 | S009 note: pin and anchors hold; line move not evidence | `S009 note (HOLD, not STALE): the release-1.28.0 pin and its anchors hold byte-for-byte.` (16w) |

Token totals: S009 ×8, S010 ×13, S008 ×1. Embedded tokens: L62 PairS010, L64 PairS010 + PairS009, L68 Correction3S010,
L69 Correction4S010, L70 Rejection13S009 (6). **No id in this file is embedded-only** — S009/S010 also appear standalone.

Alternate-form sweep over both files: 0 hits for `S-014`/`S 014`, lowercase `sNNN`, 4+ digits, slash lists, and
`S…to/through…S` ranges. The only non-grammar token is the receipt glob `S0NN` (L62 custom, L60 etag). `S014`, `S019`,
`S035` occur nowhere in either file.

## 2. Pairs, population, obligations

- Population membership: S003, S005, S007, S008 (custom) and S008, S009, S010 (etag) are all in the frozen 32-row set.
  Citing pairs from these files: **4 + 3 = 7**.
- Frozen57 (independent recomputation, frozen grammar, 26 knowledge files, 9 non-empty): crawl-scope 4, custom-domain 4,
  etag-anatomy 3, served-set 6, subpath-spotcheck 2, publish-channels 7, sitemap-orphan-audit 6, speedrun 3, preflight 22.
  All 7 target pairs are inside frozen57.
- Carried r26 decisions: 5/7 — (S003, custom) 13 statements; (S005, custom) 17, seatStale 3 / stale 0 with L1 disposition;
  (S007, custom) 20; (S009, etag) 13; (S010, etag) 9, seatStale 2 / stale 1, `reclassified:1`.
- Missing: 2/7 — **(S008, ghp-custom-domain.md)** and **(S008, ghp-etag-anatomy.md)**. Both are in `c1-before.json`
  16-missing and in `c2-oracle.json` `expectedPairs`; they are 2 of the 16, not dismissed metadata. S008 is the GNU tar
  row; the only located claim is the EOF fetch-provenance parenthetical, not a tar-content claim.
- **Additional obligation from these two files: none.** Every manual pair is already in frozen57; no pair is excluded as
  metadata. If any had been outside frozen57, it would be named here as an obligation.
- Live monotone growth (outside targets): `discovered-pairs.json` (untracked, mtime 2026-10-21T20:05:52Z, sha256
  `45e95683a6811675cc41e4f9b8a2b95e938bb112b1225a33d18d6ebad93703fb`) adds (S013, `ghp-served-set.md`). Denominator
  57→58, missing 16→17; target pairs stay 7. Corpus-wide embedded-only scan found two tokens: S013 (in population,
  admitted by that discovery) and `S404` in `free-read-verbs.md` (the `S404_SHA256` constant, out of population, not a
  source row).
- Outside-population bucket, recorded separately: **zero** S014/S019/S035 references in either target. The population's
  three gaps are exactly S014, S019, S035.

## 3. Parser comparison (performed after the census)

- `count_c1.py` HEAD blob `5e7a24d8fa909ec1c6d331f8cf31b17a9421314e`; `RANGE` line 4, `LITERAL` line 5
  (`\bS(\d{3,})\b`); population filter line 28. Token coverage on targets: custom 14/14; etag 16/22 — the 6 E tokens are
  invisible to `LITERAL` (no word boundary before `S` inside `PairS…`/`Correction…S…`), but the id **set** is unchanged,
  so pair output is identical (4 / 3).
- Independent reproduction at base and at `be375d9`: population 32, citingPairs 57, decided 41, missing 16, findings `[]`.
  `missing` set equals `c1-before.json` `missing` equals `c2-oracle.json` `expectedPairs` exactly (set equality, 16/16);
  r26 statements pairs = frozen ledger pairs = 41. `c1-before.json` sha256 `af55d0a4…`, blob `8fb5df27`, unmodified;
  `c2-oracle.json` sha256 `1d038205…`, blob `0ed63c34`, unmodified. Both are unmodified HEAD blobs.
- Out-of-population literals are silently filtered (line 28), never enumerated; no such token exists in these targets.
- Working-tree `count_c1.py` is being edited concurrently: +12 inserted lines vs HEAD (monotone union of decided +
  `c1-before` missing, outside-population raise, `decided.discard(key)` on a fresh override, `group_source_required`
  for preflight S001–S006, `--selftest` dispatch). Regex lines 4–5 unchanged. Observed sha256 `7489865d…` at 20:07Z
  (was `7ebb3f36…` at 20:05Z; mtime 17:05:14−03:00): the working copy is not a stable byte identity; the HEAD blob is.
- Consequence for these files: the r27 fetch manifest holds rows S001–S006 only (8 entries). A `kind:"source"` fresh
  override for S007/S009/S010/S008 would hit `source_missing` and, under the new discard rule, regress a decided pair
  to missing. S003/S005 are fetchable this round (S003-1, S005-1); S008 retry bytes are r26-tracked.

## 4. Evidence integrity

- Both target sha256 values equal `frozen/expected.json`; blobs and bytes are identical at base, declarations, worktree.
- S008 provenance artifact verifies: `manifest-retry.json` row S008, index 1, attempt 2, status 200, bytes 512359,
  sha256 `93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084`; decompressing
  `S008-1-retry.raw.gz` reproduces exactly that digest and length. The main r26 manifest's S008 entry is the failed
  first attempt (status null, TimeoutError, bytes 0, empty-string sha256), so the EOF parenthetical is precise.
- Neither target contains an `[r27-recheck … STALE]` marker (0 matches); any r27 STALE verdict for these pairs must add one.

## 5. Uncertainties

- The S008 pair's support is fetch provenance only. A HOLD must not be worded as GNU-tar support; `kind:"source"` is
  impossible without an r27 S008 fetch (absent from the r27 manifest), while the artifact route via
  `manifest-retry.json` is available.
- Grouped-header URL mismatch exists in both files (custom L1 attaches S003/S007 to S005's URL; etag L1 attaches S010 to
  S009's URL). r26 treated that header shape as HOLD/reclassified; this seat neither re-adjudicates nor asserts STALE.
- Pair granularity is file-level: S005's 5 tokens and S010's 13 tokens span distinct scopes that collapse into one pair;
  any adjudication must cover each scope separately.
- Embedded filename references are a real citation shape (the S013 discovery proves it can grow the denominator) but add
  no pair in these two files; `LITERAL` alone is not a complete citation-form detector.
- Counts here are snapshots: the counter and `discovered-pairs.json` were edited by others during this walk; no
  source/public-site evaluation was performed, per lane bounds.

## Verdict (scope-limited, factual)

- Census complete: custom-domain 14 tokens / 4 ids; etag 22 tokens / 3 ids; 0 ranges, 0 grouped ranges, 0 other
  spellings, 0 S014/S019/S035.
- These two files contribute **7** citing pairs: 5 carried r26 decisions, **2 undecided S008 pairs**, both already in the
  frozen 16; no additional inherited32-row obligation exists in these files.
- Manual census, `count_c1.py` id sets, `c1-before.json` 16-list, `c2-oracle.json`, and the frozen ledger agree within
  this scope; the only parser gap is filename-embedded tokens, which change no pair here.
- Live denominator is 58/17 after the (S013, ghp-served-set.md) discovery; the frozen oracles remain the historical
  57/16 by design.
- Only write: this report. No production/source/ledger/Git edits, no installs.

Report path (relative to repo root): `.ufo/waves/round-27/w1/CitingSweep06.md`
