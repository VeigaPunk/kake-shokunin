# KakeR27.BindArtifact13 — byte/locator binding attack: S008 × corpus/knowledge/ghp-etag-anatomy.md

Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (explicit hash for every git read). Axis judged: freshness. Milestone r27-fresh-falsification. Leaf seat, no dispatch.
Scope: artifact identity/coordinates only for the ledger row
`{row S008, file corpus/knowledge/ghp-etag-anatomy.md, kind artifact, evidence .ufo/waves/round-26/fetched/manifest-retry.json, contains "\"file\": \"S008-1-retry.raw.gz\""}`.
Read-only on the project repo. No source/docs/registry edit, no commit/ref/index/jj change in the project repo (`git status --porcelain` shows only pre-existing untracked wave files; `git diff HEAD` empty; HEAD still `ac46a74`; no new reflog entry). Scratch only: `/fast/scratch/hyaku/kake-r27/BindArtifact13/` (TMPDIR there) plus a `--shared` **scratch clone** of the project repo at `.../BindArtifact13/clone` whose commits exist only there (L1 may delete). No installs, no network, no r24 material.

## 1. The binding holds: substring is byte-exact and located in the right row/record

Declared expectation before running: evidence path resolves at the candidate; the recorded `contains` occurs byte-exactly **once**; that occurrence lies **inside the record whose `row` is S008** (not another source's boilerplate); the record's own `file` field equals the asserted filename.

```
git cat-file blob ac46a74:.ufo/waves/round-26/fetched/manifest-retry.json
  sha256 84e83fb0cf5bf431eb029a9ab8cab69b661054e6e992b862e87b514786a65d1b   902 bytes
  json: 1 record  -> row S008, index 1, attempt 2, status 200, error null,
         fetchedAt 2026-10-21T15:11:01.972009+00:00, bytes 512359,
         sha256 93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084,
         file "S008-1-retry.raw.gz",
         reason "first attempt TimeoutError at 60s; single retry with 240s timeout"
  contains "\"file\": \"S008-1-retry.raw.gz\"" occurrences = 1, byte offset 783,
         context: ...6084",\n    "file": "S008-1-retry.raw.gz",\n    "reason": ...
  record containing that span: row S008   (0 records with any other row)
  record.file == asserted filename: True
```
Actual = declared. The evidence file is single-record, so substring and record coincide; the S008-1-retry filename cannot come from another row's boilerplate.

## 2. Independent hash recompute (no trust in the manifest's own fields)

Declared: gunzip of the retained blob must reproduce the manifest's `sha256` **and** `bytes`; the on-disk gzip file's own digest must be different from either (it names the received body, not the retained file).

```
gunzip(S008-1-retry.raw.gz)  -> 512359 bytes, sha256 93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084
  manifest sha256 matches recompute: True     manifest bytes matches recompute: True
retained gzip file itself: 150267 bytes, sha256 1d34183a2015d3648c62182642bf7e04c4c54d40c2cfb11522820c38e4d61dd2
```
Actual = declared. Blob ids for both r26 payloads are **identical at base `83528f7c`, declarations `be375d90`, and candidate `ac46a74`** (`S008-1-retry.raw.gz` = `0b03a05f…`, `manifest-retry.json` = `637e278d…`); the whole `.ufo/waves/round-26/fetched/` tree is byte-identical base↔candidate (`diff` of `git ls-tree` = empty). No frozen input was rewritten.

Corroboration of the asserted *retry* (the record's own claim) from an independent committed artifact: `manifest.json` holds exactly one S008 entry — `status null`, `error "TimeoutError: The read operation timed out"`, `bytes 0`, `sha256 e3b0c442…b855` (SHA-256 of empty) — and the retained first-attempt `S008-1.raw.gz` (blob `86e43ea3…`, 20 bytes) gunzips to **0 bytes**. So "first attempt timed out, one retry succeeded" is consistent across two separate committed files plus two retained payloads.

## 3. Historical date / base / evidence-filename asserted — all verified

- **Evidence filename**: `S008-1-retry.raw.gz` exists at candidate and at base with the same blob; it is the file named by the record itself.
- **Date**: citing file line 60 says "Round-26 source recheck (2026-10-21)"; manifest `fetchedAt` = `2026-10-21T15:11:01Z`. Consistent. The r27 `fetched/manifest.json` covers **only S001–S006** (8 records), so no fresh r27 S008 fetch exists — the ledger reason explicitly says the retry fact is "not a fresh S008 opening", and nothing in the record implies a current-source observation. Freshness claim is honest.
- **Base**: line 60's "Pointers labelled `at base cb807bc` stay base-scoped" — `cb807bc8d8bc94be1268e4741191bb3d5e518565` is an ancestor of the candidate. I read the base-scoped cited windows at cb807bc: `LOG.md:161-163` and `corpus/lessons/round-16.md:35-38` are byte-identical at base and candidate; `corpus/knowledge/publish-queue.md:255-261` at cb807bc **is** the ETag-anomaly block, and at candidate those lines have shifted — consistent with the base-scoped reading the file itself declares. (The cb807bc-vs-5009ecaa baseline ambiguity was already logged as low-severity in r26 `w2/Rejection07S013.md`; the S009/S010 pairs, not this pair, carry those pointers.)
- **Scope**: `corpus/SOURCES.md:16` (S008, GNU tar) has usedBy = `corpus/knowledge/ghp-served-set.md` only; this file's header (line 1) is `source: S009, S010`. The file contains **zero** word-boundary `tar` occurrences. So "not attribution of any platform claim to GNU tar" and "the named subject rows exclude S008" both check out.
- **Citation set**: literal token census at the candidate over the file with count_c1's own regexes → `S008`×1, `S009`×6, `S010`×9, **no ranges**. The single S008 occurrence is line 60, byte offset 3502 — inside the "## Round-26 source recheck" bullet. Its subject is "Rows S009 and S010"; S008 sits in the provenance parenthetical.
- **Ledger mechanics**: `count_c1.py` at the candidate → exit 1, citingPairs 58, reviewedPairs 58, decided **55/58**, knownUnverifiableUnits 7 in 3 pairs, `missing` = {S001/served-set, S007/custom-domain, S033/static}. The S008/etag outcome is `{'verdict':'HOLD','valid':True}`, absent from `missing` and from `findings`. This matches `frozen-candidate.json` strictC1 "55 strictly decided/58 reviewed, 7 known unknown units in 3pairs". The pair is one of the 16 frozen baseline-missing obligations (`c1-before.json` missing[] contains it); the original counter at `be375d90` reproduces 57/41/16 with it listed.

## 4. FINDINGS

**F1 (MEDIUM, counter-level, not a defect in this record): the artifact branch is not row-scoped.** `count_c1.py:113-115` checks `p['contains'] not in blob(p['evidence']).decode()` — substring over the **whole** evidence file, with no requirement that the match sit in the record for `p['row']`. Demonstrated in the scratch clone: re-pointing the S008/etag record at `.ufo/waves/round-26/fetched/manifest.json` (34 records) with `contains '"file": "S009-1.raw.gz"'` — S008 bound to **a different row's record** — still yields `valid: True`, decided 55/58, exit 0. A control with a generic `'"status": 200'` from the same evidence file also passes. Consequence: artifact-record row identity rests on the reviewer, not on the counter. **This pair is unaffected** (§1 proves the single-record coincidence), so no verdict changes here; but the counter cannot detect a mis-bound artifact row in any wave.
*Adjacent live instance (other seat's pair, reported for the integrator, not adjudicated by me):* the S005/sitemap-orphan-audit record's `contains` (`"supersededClaim": "Each deployment snapshots the entire checked-out tree."`) resolves to `/platformCorrections[10]` whose record's `sources` list is `["S001","S002","S004","S006"]` — S005 is not among them. The whole-file containment check cannot see that.

**F2 (LOW, mechanism): the artifact branch never re-reads the citing file.** Scratch clone: deleting the S008 token from `corpus/knowledge/ghp-etag-anatomy.md` entirely leaves the counter at decided 55/58 with the S008/etag row `valid: True` — the obligation survives its own citation because the pair set pins the baseline 57 as a minimum. Consistent with the frozen contract's "baseline 57 minimum, not maximum" rule, so this is design-observed rather than a break, but it means the artifact branch is one-directional (evidence-side only).

**F3 (LOW, evidence-path failure mode is global, not per-row):** a nonexistent `evidence` path raises inside `blob()` → whole counter exits **2** (`could-not-evaluate`, `{"error":"ValueError: missing …"}`), not a per-pair finding. Fail-closed, but one bad path aborts the whole measurement instead of isolating the bad row.

**F4 (LOW, coordinate wording shared across the four S008 rows):** the reason calls the mention "r26 **EOF** retrieval provenance". In this file the S008 mention is line 60 of 70 — inside `## Round-26 source recheck`, with ten further lines after it (S010 STALE corrections and a `### Round-26 falsify-wave adjudication` section). "EOF" is an imprecise locator descriptor here. Does not touch the HOLD verdict (the reason's substantive claims — retry manifest, no GNU-tar attribution, subject rows exclude S008 — are all verified above). The same reason string is reused verbatim for the other three S008 rows; in `static-canonical-preflight.md` the mention is at line 184 of 247, i.e. definitively not EOF, and that file's line 244 explicitly calls the line-184 span "historical artifact provenance only" — consistent with the verdict but inconsistent with the "EOF" wording.

**F5 (LOW, cross-wave digest-naming hazard, no effect on this pair):** in r26's `manifest-retry.json` (and `manifest.json`), `sha256`/`bytes` name the **decompressed received body** (S008: 512359 bytes). In r27's `fetched/manifest.json` the same field names denote the **retained public representation**, with `receivedSha256`/`receivedBytes` added for the body (S002/S003…: retained 3496 bytes vs received 200835 bytes). Same field names, opposite semantics across waves. The S008 ledger record asserts no digest, so it is unaffected; any future consumer reading an r26 manifest's `sha256` as "retained bytes" would mis-bind.

**F6 (INFORMATIONAL):** `strict-c1-disposition.json` pre-declared "[INFERENCE before execution] baseline 39/57 strictly decided alongside 41/57 reviewed"; the actual candidate counter at `be375d90` yields **38** strictly decided of 57. The 39 predates the third carried-unverifiable pair (`S007/ghp-custom-domain`, 1 unit) added by `carry-errata.json`; 41 − 3 = 38. Consistent, not a discrepancy in any measured pair.

## 5. Not claimed / residual risk
- I did not adjudicate semantic support of the S008 row against the GNU-tar source (separate reviewer lane), and did not verify the four sibling S008 rows' own files beyond the shared-reason wording note in F4.
- The `contains`-substring specificity requirement is not enforced by any counter (F1), so row-level artifact binding for the other 10 artifact rows in `pairs.json` rests on their seat's manual check; this seat verified only its own row (and incidentally S005's location, F1).
- `rechecks/S008.json` exists at the candidate (verdict HOLD, fetchIndex 1, quote present in the retained bytes at the asserted anchor lines 8587/8588/8602-8604/8618 — all independently confirmed in the decompressed payload), but that receipt is **not** the evidence cited by this ledger row; the cited evidence is the retry manifest itself, which is sufficient for the provenance claim actually made.
- r27 W1 reviews `w1/Pair13A.md` (blob `8f8380ec…`) and `w1/Pair13B.md` (blob `df37b64d…`) are tracked at the candidate, name this exact pair, and every hash/anchor they state for this row reproduced exactly under my independent recompute. Pair13A's "count_c1 57/41/16 at be375d9" is true of the counter **as it existed at be375d90**; the candidate's stricter counter reports 38 decided of 57 at that revision (F6).
- No build/lint/formatter run. No source edit in the project repo.
