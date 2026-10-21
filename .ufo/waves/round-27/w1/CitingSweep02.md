# CitingSweep02 — blind citing-set data-walk (2 files)

Seat: KakeR27.CitingSweep02 (leaf, read-only). Milestone r27-full-citing-set; axis freshness.
Targets: `corpus/knowledge/crawl-scope-per-host.md`, `corpus/knowledge/drift-detection.md`.
Measured revision `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations
`be375d90afc6fc7aca369ab3cf5247bf460aeed2`. `git diff --stat` across both files between those
two commits is empty; hashes equal the frozen pins in `.ufo/waves/round-27/frozen/expected.json`.

## Method (census performed before any parser/oracle comparison)

1. Read both files end-to-end (57 + 116 = 173 lines) and hand-enumerated every source-id form:
   provenance header, body source checks, EOF append-only notes, HTML comments.
2. Re-scanned with three independent regexes: frozen `\bS(\d{3,})\b`, frozen range pattern
   (`S…` + `-`/`–`/`—`/`..`/`to`/`through` + `S…`), and a loose alternate-form pattern
   `(?i)\bS[\s_-]?\d{2,}\b` (catches `S-011`, `S 011`, 2-digit forms). Cross-checked line bytes.
3. Only then replicated `count_c1.py`'s pair construction at base and diffed against my census,
   `c1-before.json`, and the frozen 16.
4. Verified the EOF note's *local* provenance claims against r26 retained artifacts. No
   source/public-site evaluation was performed (out of scope by ticket).

## Manual census — every reference occurrence

`corpus/knowledge/crawl-scope-per-host.md` — 57 lines, sha256 `aea5d1579b1cec8c…09af691`.

| Line | Form | Ids | Scope |
|---|---|---|---|
| 1 | grouped literal list | S011, S012, S013 | `source:` provenance header; authority pointer to `corpus/SOURCES.md` for the whole entry |
| 27 | literal | S011 | body `**Source checks**`; anchors §2.3 / §2.3.1.3 / §2.3.1.4 |
| 30 | literal | S012 | body source check; Sitemap-file-location quote |
| 33 | literal | S013 | body source check; Sitemap-best-practices quote |
| 57 | grouped literal list + literal | S011, S012, S013, **S008** | EOF `## Round-26 source recheck`, append-only metadata note |

Exact EOF text: “Rows S011, S012 and S013 were re-fetched by one public GET each
(`…/manifest.json`, S008 via `manifest-retry.json`)” — 20 words. **S008 is a cross-document
reference**: SOURCES.md:16 defines S008 as the GNU tar pattern-matching row (own source:
`https://cgit.git.savannah.gnu.org/.../doc/tar.texi`), unrelated to robots/sitemap claims.
No ranges and no alternate forms exist in this file. L57's `rechecks/S0NN.json` is a template
placeholder, not a digit id; the frozen regex correctly does not enumerate it.

`corpus/knowledge/drift-detection.md` — 116 lines, sha256 `cffb82b35849a8b5…f4129c`.

| Line | Form | Ids | Scope |
|---|---|---|---|
| 1 | literal | S019 | `source:` provenance header; explicitly “Metadata authority only: S019 in corpus/SOURCES.md, not platform verification” |

No other S-id, range, or alternate form in the file (grep of `S\d{2,}` finds only L1; no `S014`,
no `S035`). S019 resolves to a real row: SOURCES.md:27 “own-work: publishing corpus contract
audit — scripts/corpus-contract.mjs …” — so the header's self-description is accurate, and the
id is not dangling.

## Distinct citing pairs from this slice

In inherited-32 population (population.json = S001–S034 minus S014/S019):

1. `(S008, corpus/knowledge/crawl-scope-per-host.md)` — L57 only — **MISSING/undecided at base**.
2. `(S011, corpus/knowledge/crawl-scope-per-host.md)` — L1 + L27 + L57 — decided in r26.
3. `(S012, corpus/knowledge/crawl-scope-per-host.md)` — L1 + L30 + L57 — decided in r26.
4. `(S013, corpus/knowledge/crawl-scope-per-host.md)` — L1 + L33 + L57 — decided in r26.

Outside the inherited population (recorded separately, NOT counted):

5. `(S019, corpus/knowledge/drift-detection.md)` — L1, provenance/metadata scope. Excluded by
   construction, matching SOURCES.md:79 “the 32 previously opened external rows (S001–S034 minus
   own-work S014/S019)”. Named here so a future population widening starts from this pair.

S014 and S035 do not appear in either file.

## Parser / `c1-before.json` / frozen-16 comparison (done after census)

- Replicated `count_c1.py` pair construction at `83528f7`: **citingPairs 57**, decided 41,
  missing **16**. Pairs contributed by my two files: exactly the four in-population pairs above;
  `drift-detection.md` contributes zero (S019 removed by population intersection).
- The computed 16 match `c2-oracle.json` `expectedPairs` and `c1-before.json` `missing`
  element-for-element in row/file and sorted order: **16/16, 0 divergence**, 0 extra, 0 absent.
- My slice's only parser/census delta is the documented population filter on S019 — not a miss.
- `frozen/expected.json` pins both target hashes; working-tree hashes match, so the frozen
  snapshot and current bytes are identical (no silent drift during the wave).
- `discovered-pairs.json` is absent, so the monotone discovery channel is empty and the
  denominator is currently the minimum 57.

## EOF-note provenance verified locally (not a source verdict)

- r26 `fetched/manifest.json`: S011 idx1 HTTP 200, 82,367 B, sha `bbaa2806…`; S012 idx1 200,
  45,292 B, sha `5e757059…`; S013 idx1 200, 191,341 B, sha `492e22cf…` → “one public GET each” is true.
- S008 main attempt: `status: null`, `TimeoutError`, 0 B (`e3b0c442…`, empty); retry row
  `(row S008, index 1, attempt 2, status 200)` in `manifest-retry.json` → “S008 via
  manifest-retry.json” is true.
- Receipts `r26/rechecks/{S008,S011,S012,S013}.json` all exist.

Conclusion: L57 is a truthful provenance note. Its S008 reference is metadata-scope only and
cannot support any crawl-scope host/path proposition; adjudicating `(S008, crawl-scope-per-host.md)`
as HOLD must be scoped to the note, not the entry claim.

## Additional obligations (monotone)

- **None newly discovered.** These files add no inherited-32 pair beyond the frozen four;
  `(S008, crawl-scope-per-host.md)` is already frozen obligation, so the denominator need not grow
  for this slice.
- Future/conditional pair, not counted: `(S019, drift-detection.md)` if the population ever
  widens beyond S001–S034 minus S014/S019.
- No range/alternate form was found that the frozen regexes could miss, so no hidden pair exists
  in this slice.

## Parser-semantics observations (outside my two files; not adjudicated here)

- `count_c1.py` builds `decided` from every r26 `statements.json` pair with no verdict filter:
  `decided={(p['row'],p['file']) for p in old}`. Six carried pairs hold nonzero counters:
  S001/ghp-served-set (stale 1, unverif 3), S003/ghp-served-set (stale 2),
  S010/ghp-etag-anatomy (stale 1), S021/static-canonical-preflight (stale 1),
  S024/static-canonical-preflight (stale 2), S033/static-canonical-preflight (unverif 3).
- In-file `[r26-recheck … STALE]` corrections do exist for S001, S003, S010, S021, S024
  (`ghp-served-set.md:85,87,93`; `ghp-etag-anatomy.md:62,64`;
  `static-canonical-preflight.md:186,198,199`), so their carriage is not obviously fail-open.
  S033's row carries `seatUnverifiable: 3` with no STALE marker and is still counted decided;
  whether a carried-UNVERIFIABLE pair satisfies C1's “durable HOLD or supported STALE” is an L1
  call, not mine.
- This question does not touch my three decided pairs: statements.json records S011 20 stmts,
  S012 11, S013 14 with `stale 0`, `seatUnverifiable 0`.

## Residual uncertainties

- `(S008, crawl-scope-per-host.md)` remains undecided: no r27 `pairs.json` exists and
  `.ufo/waves/round-27/fetched/` holds only S001–S006 as of 17:01, so any r27 adjudication of
  S008 must lean on r26-retained bytes (`S008-1-retry.raw.gz`) or re-fetch; r26 is the only
  retained evidence I could verify.
- The gate's `citation_range_invalid` and range-span rules are untested by this slice: no range
  form occurs in either target, so range handling is not evidenced here either way.
- Scope of the one undecided pair is inherently inferential: the only possible support is that the
  r26 recheck happened, which is metadata, not a crawl-scope claim.

## Evidence / boundaries

- Commands: `git show <rev>:<file>` + three-regex census; parser replication from
  `count_c1.py` source; `sha256sum` of working and frozen copies; JSON reads of
  `round-26/{population,statements}.json`, `round-26/fetched/{manifest,manifest-retry}.json`;
  `ls` of `round-26/rechecks/` and `round-27/fetched/`.
- Written only this report under `.ufo/waves/round-27/w1/`; scratch none needed beyond an empty
  mkdir. No repo edits, no grade, no installs, no pacman. No tool versions to record.
- Blindness note: manual census and parser comparison were recorded separately above; the manual
  result was fixed before the parser was run (census: 4 in-population pairs + 1 excluded pair;
  parser (same 4, 57 total, 16 missing)).
