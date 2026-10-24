# CarryLedger — r26 `statements.json` carry-forward audit (round 27, wave 1)

Seat: `KakeR27.CarryLedger` (leaf reviewer; read-only). Axis: **freshness**. Milestone: `r27-full-citing-set`.
Checked 2026-10-21. Frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`; lane head `9ba102d4a0175c927adb54a005464ce2aa722099`.

Scope: the **r26 ledger only** — `.ufo/waves/round-26/statements.json` (sha256 `c2026376832ad4e4114d1bc19abeec4fcbdbd0fea3dbb102ab8a5c2eb18c95ce`) — checked against its own citing paths, its own seat reports, and the independently enumerated 57-pair baseline. No new source claim, no old gate execution, no r24 stopped work touched, no live-lane or sibling file edited, no tool installed.

---

## V1 — The 41 records and 313 units reproduce exactly; the pair set is clean

**Verdict: PASS (reproduced).** Recomputed from the committed blob, not from the counter's own output:

- 41 entries, 41 unique `(row,file)` keys — **no duplicate pair**.
- `sum(statements)` = **313**; `sum(stale)` = 7; `sum(reclassified)` = 4; `sum(seatUnverifiable)` = 6. Matches `corpus/lessons/round-26.md:144` "Final ledger: 313 units, 7 STALE corrections, 4 reclassified tags," / "6 UNVERIFIABLE units" and `corpus/lessons/round-26-verifier-spotcheck.md:40` "**41 unique (row,file) pairs**, sums **313 statements / 7 stale / 4 reclassified / 6 seatUnverifiable**".
- Every pair's file exists at the frozen base; every `stale + reclassified` equals the physical `[r26-recheck S0NN STALE]` tags in that file. Verified for all 41 pairs: **zero mismatches**. Total physical r26 tags = 11 = 7 accepted + 4 reclassified, so "Eleven physical tags are not eleven accepted STALE judgments" holds.
- Every pair's `report` path resolves on disk — except 14 entries whose `report` is the string `"L1 KakeR26-2"` (no file), carrying **34 of the 313 units** (10.9% of the total). These are the `w2Adjudication.changes` "round-20 correction lines … (34 row-statement units, all HOLD, judged by the L1 against retained bytes; gap found by w2/CounterCritic.md)" rows.
- Independent re-derivation of those 34 units from corpus bytes only: for each of the 14 pairs, the ledger `statements` value equals the number of `r20-correction` lines in that file that name that row (e.g. `S001`×publish-channels = lines 58,60 → 2; `S001`×sitemap-orphan-audit = lines 120–127 → 8; `S005`×ghp-subpath-spotcheck = line 95 → 1). All 14 reconcile exactly; total 34.

## V2 — Baseline 57 reproduced independently, and the 16 missing pairs decompose exactly

**Verdict: PASS (reproduced) — the frozen 57/41/16 split is honest.**

Two independent enumerators (literal `S\d{3,}` + dash-range expansion; and a dash-only variant, and a `to`/`through` variant) over `corpus/knowledge` at the frozen base, intersected with the 32-row population, both yield **57** pairs with identical sets. 41 are r26-carried; 16 missing — set-equal to `c1-before.json` `missing` and to `c2-oracle.json` `expectedPairs` (verified by set comparison, both directions empty).

Composition of the 16, by mechanism — this is the part the ledger does not record:

| # | mechanism | pairs |
|---|---|---|
| 12 | **range-only** (no literal `S…` token outside the range text) | `S001`–`S006`×`static-canonical-preflight.md` (from the `S001–S006` group at line 54); `S003`,`S005`×`sitemap-orphan-audit.md` (from `S001-S006` at line 2); `S004`,`S006`×`publish-channels.md` (from `S001-S007` at line 2); `S022`,`S023`×`static-canonical-preflight.md` (from `S020-S027` at line 2) |
| 4 | **literal token, r26-authored retrieval provenance** | `S008`×`crawl-scope-per-host.md`, `×ghp-custom-domain.md`, `×ghp-etag-anatomy.md`, `×static-canonical-preflight.md` — each occurrence is the phrase “S008 via `manifest-retry.json`” in the r26 recheck paragraph |

The 4 `S008` pairs are **new since r26**: at base `97404de` the literal count is 43, at `83528f7` it is 47 — r26's own appended recheck paragraphs introduced them. They are also *not* claim citations: r26 itself wrote the rebuttal at `ghp-served-set.md:95` — “The words “S008 via `manifest-retry.json`” in the recheck paragraph name the round's retry, not a source of this entry”. A pair whose only occurrence is retrieval provenance is arguably not a citing pair at all; the r27 ledger treats it as one (conservatively), which enlarges the denominator, not the claim.

**Uncertain:** whether the 12 range-only pairs should count as obligations. `contract.json` fixes the rule (“literal S +3-or-more digits and ranges with S at both ends separated by hyphen/en-dash/em-dash/../to/through; intersect r26 inherited32-row population… Historical metadata and r26 EOF prose are INCLUDED”), so the 57 is the declared denominator and I do not dispute it. I note only that 12 of 57 arise from ranges and 4 from provenance prose, so 41 of 57 are literal-citation pairs.

## V3 — Statement-level UNVERIFIABLE is a separate axis from pair-level adjudication

**Verdict: the r26 ledger's 313 is *not* a decided-statement count, and the two r26 records disagree about what their own `statements` field means.**

The ledger's `statements` field is not one convention across the 41 pairs:

- **S001**×`ghp-served-set.md`: `statements: 28` **includes** its 4 UNVERIFIABLE units (report: `{"statements":28,"hold":21,"stale":3,"unverifiable":4}` → 21+3+4 = 28).
- **S033**×`static-canonical-preflight.md`: `statements: 6` **excludes** its 3 UNVERIFIABLE units (report: “S033-attributed units: 9. Decided: 6 (HOLD 6, STALE 0). UNVERIFIABLE: 3 (rows 2, 4, 9)”). r26's own falsify wave recorded this asymmetry — `w2/FalsifyS033.md:207`: “the ledger's `statements: 6` is the *decided* count, not the 9 units the seat enumerated. The same pattern holds for S007”.
- **S007**×`ghp-custom-domain.md`: `statements: 20` excludes its 1 UNVERIFIABLE unit (report line 8: “20 decided statements, 20 HOLD, 0 STALE. 1 statement UNVERIFIABLE and not counted”), and the ledger records `seatUnverifiable: 0` for it.

Full reconciliation of the 313 against the seat reports’ own attributions (each report’s declared count, `UncoveredS024S025.md`’s S-1…S-4 rows, and the 14 L1 rows’ 34 line-derived units):

| pair | ledger `statements` | report-attributed | delta | why |
|---|---|---|---|---|
| S001×ghp-served-set.md | 28 | 28 | 0 | 28 **includes** its 4 UNVERIFIABLE units |
| S007×ghp-custom-domain.md | 20 | 21 | −1 | report: “20 decided … 1 statement UNVERIFIABLE and not counted” |
| S033×static-canonical-preflight.md | 6 | 9 | −3 | report: “attributed units: 9. Decided: 6” |
| S025×static-canonical-preflight.md | 1 | 2 | −1 | report enumerates S-3 (:72, implicit) and S-4 (:143-146, literal `S025`); the ledger records 1 |
| all other 37 pairs | = | = | 0 | ledger and report agree |
| **total** | **313** | **318** | **−5** | |

Consequences, all arithmetic on committed bytes:

1. **Decided statements inside the 313 = 310, not 313 and not 307.** The published aggregates “313 statement units” (`corpus/lessons/round-26.md:144`) and “313 statements” (`round-26-verifier-spotcheck.md:40`) are true as *ledger sums* but do not equal the decided-statement count. S033's 3 and S007's 1 are already outside the 313; S001's remaining 3 sit *inside* it; S025’s implicitly-attributed unit is outside it.
2. **S025’s ledger count of 1 omits a HOLD unit the seat enumerated** (S-3, `static-canonical-preflight.md:72`, “template descendants cannot supply a document-head canonical”). The corpus line 72 carries no literal `S025` token (only line 144 does), so the pair has one explicit citation and one implicit reliance; the ledger kept the explicit one and dropped the implicit one. This is the same “explicit vs attributed” seam as S007/S033, and it means one r26 HOLD unit is not counted anywhere.
3. **Seat-attributed UNVERIFIABLE units = 8; ledger-carried = 6.** 4 (S001) + 3 (S033) + 1 (S007) = 8 units across 3 pairs; `seatUnverifiable` sums to 6 across 2 pairs. `strict-c1-disposition.json` and `pairs.json` `r26CarriedMeaning` both name **six** units in **two** pairs (“S001 ghp-served-set3 and S033 preflight3”) — one unit (S007’s `ghp-custom-domain.md:54-55` Markdown-representation statement) is invisible in the ledger and in every carried-forward total. The committed corpus discloses **no** UNVERIFIABLE unit for S007 at all (`grep -i unverifiable` on the frozen `ghp-custom-domain.md` → 0 hits), and the r26 lesson names only the four v3.0.1 statements (`corpus/lessons/round-26.md:61`), of which `ghp-served-set.md:94` already corrects to three. So the honest carried number is **7 units in 3 pairs** (3 + 3 + 1), or 8 if the pre-falsify S001 count of 4 is used.
4. `count_c1.py` (strict, `9ba102d`) now derives undecided pairs from `seatUnverifiable > 0` only, so it reports exactly the two pairs r26 recorded and cannot see S007. Its `carriedUnverifiableUnits: 6` inherits the ledger gap; it is right about what it reads, but the corpus it reads is incomplete.

**This is the honesty defect the strict disposition is right to refuse to discharge.** Two r26 pairs with unresolved units are correctly *not* counted decided; a third pair (S007) with an unresolved unit is counted decided because the ledger lost it. The fix belongs in the ledger’s `seatUnverifiable` field (S007 → 1), not in the counter.

## V4 — Carry-forward as “r26 adjudications”: what is and is not carried

**Verdict: the carry-forward is honest at pair level and lossy at unit level.**

Carried correctly: all 41 pair records, their statement counts, their STALE/reclassified counts and their correction tags. The r26 corpus bytes are untouched at the frozen base; the four corpus files carrying r26 corrections still carry exactly the 11 physical tags.

Carried with loss: (a) the mixed `statements` convention above (V3); (b) S007’s single UNVERIFIABLE unit; (c) the 14 pairs’ per-pair adjudication artifact — no `w1`/`w2` report file exists for them, so their 34 HOLD units are attested only by the corpus EOF paragraph plus `w2Adjudication.changes` plus `w2/CounterCritic.md:62-65`. I re-derived all 34 from corpus bytes (V1), so the substance is sound; the *audit trail* is one hop shorter than for the other 27 pairs.

Also note r26’s ledger correctly separates *row* verdicts from *pair* verdicts: every r26 row has a HOLD receipt (`.ufo/waves/round-26/rechecks/S0NN.json`), and `measure-final.json` shows `decided 32, hold 32` — rows, not pairs. The 32-row row-level result and the 41-pair statement ledger are different claims; r27 must not merge them.

## V5 — Freshness of the r26 source bytes the carry-forward rests on

**Verdict: the r26 bytes are unchanged, but r27’s own re-fetch moved the HTML chrome, not the text.** Not an r26 defect; it bounds what r27 can claim.

- r27 re-fetched S001–S006 into `.ufo/waves/round-27/fetched/` (manifest sha256 `d3b0b1ca215bfa6d89edf639b2b87475d668fdf73cbf0ddf089c87e11d043781`, 8 payloads). For S002, S003, S004, S005, S006 the **raw sha256 differs** from r26’s retained payloads (e.g. S003 r26 `aa758b4a…` → r27 `f42d48b5…`), yet the **extracted text views are byte-identical** for every row/index compared (S001-1/2, S002-1/2, S003-1, S004-1, S005-1, S006-1). The diffs are GitHub asset-hash/URL churn in the HTML shell. S001-1 and S001-2 raw bytes are unchanged.
- Consequence for the carry-forward: the r26 HOLD verdicts still rest on the same *text*, so nothing in the r26 ledger is invalidated; but r27 must not claim byte identity with r26 for S002–S006, and any r27 quote must be checked against the **r27** payload (which it is: `count_c1.py` reads `fetched/manifest.json` at the measured revision and re-hashes the gzipped body).

## V6 — Two independent cross-checks that do **not** support a clean C1 today

Reported as facts for the parent; neither is a new source claim and neither retries stopped work.

1. **The C2 gate currently in the working tree does not reproduce the frozen oracle.** `scripts/citing_set.py` (uncommitted, sha256 `790d732799510c69cd870ae89a331a2178ce84d6d98cbda13cb50a0aa5f05b92`, mtime 18:17) reports **57** `unadjudicated_citing_pair` findings against the frozen snapshot where the oracle expects **16**; `python3 -B scripts/citing_set_selftest.py` reports `verdict failed, cases 29, failed 23`. Root cause is localized: in `evaluate()`, the citing set is keyed by `(row_key, file)` pairs while `ledger_present` holds only `row_key`, so `if key in ledger_present` (`scripts/citing_set.py:483`) never matches an adjudicated pair. Changing that one comparison to test the `(row_key, file)` pair makes the frozen run yield **exactly the oracle's 16** (verified in a scratch copy: detected 16, expected 16, extra ∅, missed ∅) and makes **29/29** fixture cases pass. This is the C2 seat’s file and my lane’s write scope forbids editing it — reported, not touched.
2. **The strict C1 arithmetic now published.** `count_c1.py` at `9ba102d` reports at the frozen base: `citingPairs 57, reviewedPairs 41, decided 39, r26CarriedFullyDecidedPairs 39, carriedUnverifiableUnits 6, findings 2` (`carried_unverifiable` on S001×ghp-served-set, S033×static-canonical-preflight). With the current worktree ledger (18 new pair records) the strict simulation gives `pairs 58, reviewed 58, decided 56, missing 2` — the same two pairs remain undecided by strict status. Consistent with `strict-c1-disposition.json`; note its stated expectation “candidate56/58 strictly decided alongside58/58 reviewed” matches what I measured. The carried **57** is a *review-coverage* count; `decided` is 39 at base and 56 at the worktree ledger, and six (seven counting S007) units are still explicit unknowns.

---

## Residual risk / verification gaps

- **S007’s one UNVERIFIABLE unit** is the largest carry-forward gap: absent from `statements.json`, absent from every carried-forward unit total, absent from the committed corpus, present only in `w1/PairS007GhpCustomDomain.md:8,41`. Any strict total derived from the ledger understates unresolved units by at least one. L1 must decide whether to correct the ledger (r26 file is frozen; correcting it would need an r27 record, not an r26 rewrite) or to disclose 7 units / 3 pairs explicitly.
- **S025’s second HOLD unit** (report S-3, `static-canonical-preflight.md:72`) is counted in neither the ledger nor the corpus. It is a HOLD, so it does not affect the STALE/unknown counts — but it is one of the 5 units by which report-attributed (318) exceeds ledger (313), and any r27 statement that repeats “313 units” without qualification inherits the loss.
- The r26 ledger’s mixed `statements` convention (V3) means **313 has no single referent**. A future reader comparing r26’s 313 to r27’s ledger totals will mis-compare. Recommend the r27 ledger state the decided-unit count (310) and the attributed-unit count (318) separately from the raw ledger sum (313).
- I verified the 34 unit-less-pair L1 attributions from corpus bytes only; I did **not** re-adjudicate their HOLD verdicts against source bytes (that was r26’s w2 seat’s work and is out of my scope).
- Range-only vs literal citation obligations: contract-fixed, but the 12/4 split above should travel with the 57 so the number is interpretable later.
- The C2 gate defect in V6 is a working-tree observation at 18:17; if that file changed after my check, re-verify before acting. My scratch copies live under `/fast/scratch/hyaku/kake-r27/CarryLedger/` (no `/tmp`, no `/dev/shm`).

## Tooling

None installed, upgraded or removed. No pacman / uv / npm / cargo transaction; all pacman transactions remain PAUSED host-wide and untouched. Read-only tooling used: `read`, `grep`, `git show`/`ls-tree`/`cat-file`/`diff`/`status`/`log`, and Python 3 stdlib (regex enumeration, `json`, `gzip`, `hashlib`, `difflib`) in memory. One `git diff`/`git log`/`git status` inspection of lane state was read-only; no commit, push, jj/git mutation, or branch operation was performed.

## Evidence index

- `.ufo/waves/round-26/statements.json` (sha256 `c2026376…`) — 41 pairs / 313 units / 7 stale / 4 reclassified / 6 seatUnverifiable.
- `.ufo/waves/round-26/w1/PairS001GhpServedSet.md:12` “28 statements. 21 HOLD. 3 STALE … 4 UNVERIFIABLE”; `:97` JSON `{"statements":28,…,"unverifiable":4}`.
- `.ufo/waves/round-26/w1/PairS033StaticCanonicalPrefl.md:39` “S033-attributed units: 9. Decided: 6 … UNVERIFIABLE: 3 (rows 2, 4, 9)”.
- `.ufo/waves/round-26/w1/PairS007GhpCustomDomain.md:8` “20 decided statements, 20 HOLD, 0 STALE. 1 statement UNVERIFIABLE and not counted”; `:41` the L54-55 Markdown-representation unit.
- `.ufo/waves/round-26/w2/FalsifyS033.md:207` “the ledger's `statements: 6` is the *decided* count, not the 9 units the seat enumerated.”
- `.ufo/waves/round-26/w2/FalsifyS007.md:120` on `seatUnverifiable: 0`.
- `.ufo/waves/round-26/w2/CounterCritic.md:62-65` (the four files’ citing lines), `:147` (the unjudged citing set).
- `.ufo/waves/round-26/w2/UncoveredS024S025.md:18-21` (S024 S-1/S-2 STALE; S025 S-3/S-4 HOLD → 2 + 2 units, ledger records 2 + 1).
- `corpus/lessons/round-26.md:61` “UNVERIFIABLE: four upload-pages-artifact v3.0.1 statements …”; `:144` “Final ledger: 313 units, 7 STALE corrections, 4 reclassified tags, 6 UNVERIFIABLE units.”
- `corpus/lessons/round-26-verifier-spotcheck.md:40` “41 unique (row,file) pairs … 313 statements / 7 stale / 4 reclassified / 6 seatUnverifiable.”
- `corpus/knowledge/ghp-served-set.md:94` “covers three statements … not four”; `:95` the “S008 via `manifest-retry.json`” provenance rebuttal.
- `.ufo/waves/round-27/count_c1.py` (strict, `9ba102d`) → `decided 39`, `carriedUnverifiableUnits 6`, 2 `carried_unverifiable` findings; `frozen_input_changed` guards on `statements.json`, `population.json`, `c1-before.json`.
- `.ufo/waves/round-27/strict-c1-disposition.json` — the strict reading of contract 10/13 and the six-unit/two-pair scope.
- `.ufo/waves/round-27/c2-oracle.json` (sha256 `1d038205…`) — 16 expected pairs; `.ufo/waves/round-27/frozen/ledger.json` == r26 `statements.json` (sha256 identical), 28 pinned sha256 files all matching their frozen copies.
- `scripts/citing_set.py:483` and `scripts/citing_set_selftest.py` — V6 gate finding (scratch-only reproduction).

Report: .ufo/waves/round-27/w1/CarryLedger.md
