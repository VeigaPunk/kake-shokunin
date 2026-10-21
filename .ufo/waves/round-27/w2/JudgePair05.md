# JudgePair05 — (S004, corpus/knowledge/publish-channels.md) — r27 fresh falsification

Seat `KakeR27.JudgePair05` (leaf, read-only, no dispatch). Axis: **freshness**. Measured revision `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (HEAD == frozen candidate, verified). Attacked item: `.ufo/waves/round-27/pairs.json` `{row:S004, file:corpus/knowledge/publish-channels.md}`, `kind=artifact`, `verdict=HOLD`, `evidence=corpus/SOURCES.md`.
**Verdict: HOLD CONFIRMED at its own scope** (historical opening-date metadata) — not STALE, not UNVERIFIABLE. One material dissent (§4); one actionable precision gap for L1 (§5-R1).

## 1. Citing sentence and the scope it actually asserts for S004

`corpus/knowledge/publish-channels.md` (bytes identical at base 83528f7 and candidate, sha256 `18042de41ae254a0e4138a6a1cfe6e4bdaa2bbf59b4c1de0181bca9f1bca73be`) has **no literal `S004`** (`git show ac46a74:corpus/knowledge/publish-channels.md | grep -n S004` → exit 1). The pair exists only through the C1 range expansion of line 2:

> `verified-at: 2026-09-26 (...) and 2026-09-28 (...); round-20 corrections 2026-10-19 (S001-S007 opened that day) — historical-not-live-reverified; no live domain recheck performed`

**Declared expectation before reading further:** S004's scoped proposition is only the parenthetical predicate *"opened that day"* (2026-10-19) — opening-date provenance, not content support. **Observed:** line 1 `source: S001, S002, S003, S005 and S007 in corpus/SOURCES.md support the EOF round-20 corrections`; lines 58–61 cite only S001/S002/S003/S005/S007; line 84 (r26 EOF) `The round-20 correction lines in this entry cite S001, S002, S003, S005 and S007 (lines 58-61)`. S004 and S006 are excluded from the file's own support set. Agrees with the declaration.

## 2. Artifact evidence for the asserted scope (independent historical artifacts)

**Declared expectation:** ≥3 independent in-repo records carry S004 + `2026-10-19`. **Observed** at candidate: `corpus/SOURCES.md:12` (S004 row: `Configuring the upload-pages-artifact action; fetched 2026-10-19` … `| mined | 2026-10-19 | 90d |`); `corpus/lessons/round-20.md:206` (S004 row: `fetched 2026-10-19`); `.ufo/round-20/resume/sources-gate.md` (`## S004 — Using custom workflows with GitHub Pages` → `- Accessed: 2026-10-19`); `corpus/SOURCES.md:105` `No source ids are void: all S001-S018 were opened.`
Ledger binding (byte-level; other seats' axis, re-checked): the pairs.json `contains` string is present verbatim in `corpus/SOURCES.md` at the candidate, starting at the S004 row head `| S004 | GitHub Docs: Using custom workflows with GitHub Pages —` and carrying the `| mined | 2026-10-19 | 90d |` cells; no other registry row shares that prefix (row-unique here, though count_c1.py:113 tests only substring).

## 3. Liveness of the cited source (corroboration, not the pair's scope)

**Declared expectation:** r27 fetch row S004/index 1 = status 200, received digest `9ee0766a…`, retained public text still carrying S004's artifact-shape teaching and anchor. **Observed** (`fetched/manifest.json`, `fetched/text/S004-1.txt`): status 200, fetchedAt 2026-10-21T19:59:55Z, receivedSha256 `9ee0766a2fb78e5af104bbc97dfe32ba09ebd8f2d68df1ed2d49efc081a5f53a`, 141818 received bytes → 6052 retained public-text bytes; retained text contains `compressed gzip archive containing a single tar file`, `under 10GB in size`, `should not contain any symbolic or hard links`, `Configuring the upload-pages-artifact action` (all True). No drift → no freshness basis for STALE.

## 4. Dissent addressed (strongest counter-argument)

**Counter-reading:** `corpus/knowledge/sitemap-orphan-audit.md:2` has a near-identical band (`r20 S001-S006 quote corrections 2026-10-19`) and the wave judged `(S005, sitemap-orphan-audit.md)` **STALE** (`[r27-recheck S005 STALE] The band over-attributes this entry's quote corrections to S005.`). If a line-2 band is always the entry's support set, publish-channels' `S001-S007` over-includes S004/S006 (entry set = S001/S002/S003/S005/S007) → this pair should be STALE.
**Why I reject the transfer (four grounds, all verified at candidate):**
1. *Band predicate* — sitemap's band modifies "quote corrections" (content claim); here the band sits in a parenthetical with predicate "opened that day" inside the `verified-at:` field.
2. *The candidate's own ruling for the same construct* — `static-canonical-preflight.md` line 2 band `(S020-S027)` beside `verified-at: 2026-10-20` was appended by this candidate: "The line2 S020–S027 metadata band records historical opening dates, including S022 and S023, not fresh round27 observations or individual support for every body claim. Their registry/round22 records support the dates." → (S022),(S023) HOLD at date scope. publish-channels' band is the same construction, more explicit ("opened that day").
3. *The wave's STALE rulings target bands bound to content claims* — preflight line 54 `(S001–S006, ghp-served-set.md)` attached to the manifest recommendation → S005 STALE; sitemap line 2 band → S005 STALE; `ghp-served-set` "S004 steps 4-5 upload static files and deploy" → S004 STALE. publish-channels line 2's band binds to no content claim in this file (lines 1/84 exclude S004).
4. *Topical coherence of S001–S007* — exactly the GitHub-Pages mechanism rows (upload-pages-artifact action.yml, releases, publishing source, custom workflows, custom domain, Jekyll, Pages REST API); S008–S018 are tar/nginx/HTTP/robots/sitemap/own-work/Astro/Firefox rows (SOURCES.md:16–26), and SOURCES.md:105 records all S001–S018 opened that day. The range is a plausible consulted Pages group, not a claim that all seven support the corrections.

Residual: the file never states which reading is intended; it is self-contradictory only under the rejected reading.

## 5. Findings / residual risk

- **R1 (actionable, low; L1's call):** publish-channels.md is byte-identical base→candidate (`18042de4…`) and carries **no** `r27-recheck` marker, while the three STALE files and preflight's line-2 band got clarifying notes. The append-only note proposed in `w1/Pair05A.md §7` (band = opened batch; S004/S006 are batch members, not support) is admissible and **cannot enlarge the C1 denominator** (S004/S006 already pair with this file: the line-2 range plus the two r27 pairs). It changes file bytes → needs a new commit and re-measurement; Main/L1 decision, not mine.
- **R2 (scope honesty, non-blocking):** 2026-10-19 is corpus self-attestation (registry + r20 gate + r20 lesson); the 2026-10-21 re-fetch corroborates liveness, not the past date. HOLD is *at date scope* and must not be restated as a fresh r27 external source observation of S004.
- **R3 (registry routing; disclosed, not a defect):** r27 added `corpus/knowledge/publish-channels.md` to S004's `used-by` although the entry uses no S004 content; `corpus/lessons/round-27.md` discloses it ("that includes historical metadata and rejected-attribution discussions, not an assertion that every use is admitted platform support").
- **R4 (flip risk):** `(S006, publish-channels.md)` shares this construction and reading. If Main adopts the support-set reading, BOTH rows must flip to STALE and both need appended `[r27-recheck S0NN STALE]` markers; the HOLD is load-bearing on the §4 reading.

## 6. Consumer-command verification (expectation declared first)

**Declared:** `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a74…` → **exit 1** (not clean: 3 carried-UNVERIFIABLE pairs must stay undecided), citingPairs 58, reviewedPairs 58, decided 55, knownUnverifiableUnits 7, knownUnverifiablePairs 3, missing = those 3, my row `HOLD, valid true`.
**Observed** (TMPDIR=/fast/scratch/hyaku/kake-r27/JudgePair05): exit **1**; 58 / 58 / **55**; 7 units; 3 pairs; findings S001/ghp-served-set (3), S007/ghp-custom-domain (1), S033/static-canonical-preflight (3); missing = those 3; my outcome `{S004, corpus/knowledge/publish-channels.md, HOLD, valid:true}`; all 18 outcomes valid. **Matches declaration exactly.** C1 stays UNPROVABLE: 55/58 strictly decided alongside 58/58 reviewed — review coverage is not supported status (contract:10/13).

## 7. Method, limits, hygiene

Read-only: no source/docs/registry/ledger edits, no commit/index/remote change, no build/lint/formatter, no tool install (none needed; no pacman transaction attempted — pacman PAUSED). Scratch only under `/fast/scratch/hyaku/kake-r27/JudgePair05/` (C1 JSON + stderr). No r24/r26 stopped work executed or rephrased; no live site, account, credential, property or publication operation; the only network-derived material is the already-committed r27 retained public text of S004. No external fetch by this seat.
