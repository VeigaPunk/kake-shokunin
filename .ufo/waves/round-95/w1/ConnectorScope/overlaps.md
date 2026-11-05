# ConnectorScope — round 95 sibling-overlap scan (read-only)

Method: committed trees only. Reads were `git -C <lane> show HEAD:<path>`, `git -C <lane> grep … HEAD`, `git ls-tree HEAD`, and plain `sed`/`grep` over the lane's working tree for the kake files. No sibling file was written; no git mutation was run.

Sibling HEADs at scan time: kumitate-shokunin `0bff4bab`, kotodama-shokunin `80614d0f`, chousa-shokunin `378fda82`, tabi-shokunin `58d84eda`, kake-shokunin freeze `8f638b59`.

Instrument digests verified before reading (`sha256sum`, rc 0): `.ufo/waves/round-95/c95_selfassess.py` = `8fd27d62…b193` (match); `.ufo/waves/round-95/c95_conditional.py` = `f09f8409…f312` (match). Both match `controls/instrument-sha256.txt`.

## Instrument classes this round lands

- **A. Strict self-assessment counter** — `c95_selfassess.py`: E1 Gate vocabulary, E2 QUALITY criteria→lesson paths, E3 knowledge `source:`/`verified-at:`/`recheck:` lines, E4 Mistakes table contiguity, E5 SKILL repo-path rows resolve to non-empty blobs; content-pinned identity (`frozen/c1-surfaces.json`); 20-route defect battery plus 5 admit routes plus the effectful-shadow route F1e.
- **B. Conditional-request contract v2 + mutant-equivalence kill rule** — `c95_conditional.py` over `scripts/conditional_eval.py`, `c2-contract-v2.md` C1–C5, 40-mutant population, equivalence receipts (`frozen/c2-equiv-receipts.json`, empty) under the R94-4 rule.
- **C. Registry rows for prior counters** — R94-9 rows in `SKILL.md` `### Owned freshness gate registry` (kake SKILL.md:208–213 currently holds only `freshness-sweep` and `c53_gate_truth.py`).

## Doctrine check (merge/kake/doctrine)

Not scanned: the path does not exist. `find /home/vgpnk/Projects/shokunin -maxdepth 4 -type d \( -name doctrine -o -name merge \)` printed nothing; `find /home/vgpnk/Projects/shokunin -maxdepth 6 -type d -name doctrine` printed nothing; `ls kake-shokunin/merge` → No such file or directory. Substitute read: kake `corpus/lessons/round-94.md` `## Routed` and fleet `PROTOCOL.md` §Gate standard (lines 375–392, read). See the coverage section of `ConnectorScope.md`.

## Overlap table

| # | Sibling artifact (path @ HEAD) | Class touched | Overlap in principle | Province-local or contested | One-line verdict |
|---|---|---|---|---|---|
| 1 | `tabi-shokunin/scripts/check-selfassessment.mjs` (SKILL.md:2627 registry row; `corpus/evidence/round-24/c2-measurements.json`) | A | Frozen-CASES calibration counter with a zero-mismatch predicate, a self-test that asserts exit and finding id, and a counter sha256 pinned in the registry. Same AXES.md calibration axis (AXES.md:15). | **Contested.** Tabi's m1/m3 compare SCORECARD/LOG tallies and uncommitted state against observed state; kake's E1–E5 audit corpus structure. The axis definition is fleet text, so the counter class is shared, not owned by either lane. | CONTESTED: report, do not absorb. The two counters measure different surfaces under one axis. |
| 2 | `chousa-shokunin/corpus/evidence/round79/selfcheck-v2.py` (registry row SKILL.md:175; QUALITY.md criteria 83 at :880 and 146 at :1054) | A (E2, E3, E4, E5 analogues) | S1 registry-row cell-count and S3 Mistakes-row erratum with `sha256(row)` digest are the closest match to kake E4/E5 and R94-3. S2 path-token resolution matches E2. Repair lines are digest-validated, which is the R94-3 identity rule. QUALITY.md:1054 already names the defect class: a repair accepted as set membership with no content check. | **Contested.** The checks read fleet-template documents (SKILL.md, QUALITY.md, lesson Mistakes tables) that every lane shares, not web-property semantics. | CONTESTED: cite chousa criterion 146 as precedent for R94-3; do not port the code. This is the most likely duplication. |
| 3 | `chousa-shokunin/corpus/evidence/round62/controls/null-counter.py`, `path-keyed-counter.py`, `c1v2-before.txt`; `corpus/evidence/round79/forge-battery.py` + `forgers/` | A/B (battery and do-nothing control) | "A counter exits 0 on a detection forger" (round 62): do-nothing and label-keyed controls, forgers that must be refused. Same admission rule as kake QUALITY "Round 90" (do-nothing control, one forgery per conjunct, positive fixture). | **Contested** (method rule). Both lanes independently adopted the same test; neither owns it. | CONTESTED: cite as independent discovery in the round-95 lesson; no code shared. |
| 4 | `kumitate-shokunin/scripts/gate-mutants.mjs` (contract `kumitate-gate-mutants-v2`, kill predicate K43; registry row SKILL.md:617; 43 frozen mutants) | B (mutant kill) | Frozen mutant population, kill predicate over a self-test run, survivors listed. Kill requires an immediate rerun with the same failing case names. | **Contested.** Kumitate's K43 requires rerun stability and says nothing about equivalence. Kake's C2 requires digest-pinned equivalence receipts for survivors and says nothing about rerun. Two fleet instruments define "killed" differently. | CONTESTED: a fleet-level kill-predicate decision is needed. Kake must not adopt either silently. |
| 5 | `tabi-shokunin/scripts/check-gate-mutants.mjs` + `scripts/gate-mutants.json` (fault vs benign catalogue; 12 self-test cases) | B (equivalence) | Benign-mutant class = equivalence declared at catalogue authoring time. Kake R94-4 = equivalence checked after survival, with a receipt. Same question, opposite default. | **Contested** (same question as row 4). | CONTESTED: record the default difference in the round-95 lesson; do not import the catalogue. |
| 6 | `tabi-shokunin/scripts/check-measurement-binding.mjs` (SKILL.md:1836 "Measurement-binding gate registry (C1)") | Instrument pinning | Binds each counted claim to counter blob sha256 at the measured revision, the revision's ancestry, and counted-input drift; `--reproduce` reruns. Kake's round-95 `controls/instrument-sha256.txt` pins bytes only; the base control names its revision in its output line. | **Contested** (instrument-binding discipline shared; tabi's check is stronger on ancestry and drift). Ancestry behaviour of kake's counter was not verified [INFERENCE]. | CONTESTED: a candidate for the R94-8 erratum wording; do not import. |
| 7 | `kumitate-shokunin/scripts/counter-pins.mjs` (contract `kumitate-counter-pins-v1`; `.ufo/pins/counter-pins.json`; registry row SKILL.md:627) | Registry of frozen counters | Machine check that registered counter bytes match pins. Kake's R94-9 adds registry rows but no machine pin check. | **Contested** (the registry-of-counters class is fleet-wide; kumitate's machine check is one implementation). | CONTESTED: note for the R94-9 registry rows; do not port. |
| 8 | `kotodama-shokunin/corpus/knowledge/verification/gate-frozen-run-standard.md` + `tools/check-gate-battery.py` (baseline never re-executed; pins checked) | Frozen-run pins | Digest-pinned frozen runs with committed expected verdict; "a digest proves the bytes, never the tool". | **Fleet standard, not contested.** Governed by fleet PROTOCOL.md §Gate standard "Two evidences" (PROTOCOL.md:~388). Kake already complies. | FLEET-STANDARD: cited, no overlap action. |
| 9 | `chousa-shokunin/tools/quote-reopen.py` + `corpus/evidence/round29/c1-count.py` (registry SKILL.md:91–92; `TOO_LONG` > 25 words, `VERBATIM`/`ABSENT`/`UNREACHABLE`) | Source hierarchy (quote verification) | Located-quote check: exact substring of a retained or fetched body, ≤25 words. Kake's S477/S478 quote checks (round-94 ScribeEntry; `corpus/SOURCES.md` 223–224; `round-94-verifier-spotcheck.md` §3) use the same ≤25-word rule. Kake has no committed quote gate. | **Contested.** Chousa owns source-hierarchy verification (task brief). Kake's quote checks are per-round scripts over RFC bodies. | CONTESTED: route to chousa or the fleet; do not build a second quote verifier in kake. |
| 10 | `tabi-shokunin/scripts/check-freshness.mjs` (SKILL.md:1559 `closeout-pin-witness` row; `scripts/freshness-witness.mjs`) | Freshness gate | Pinned-expected freshness gate with a witness and an expected-file table. | **Province-local.** Tabi's check compares local kimi-webbridge plugin file bytes against public copies (its `publicTargets` constant). Kake's `freshness-sweep.mjs` checks publisher-side web-property paths, sitemaps, GHP subpaths and probe history. Different subjects. | PROVINCE-LOCAL: no absorption. |
| 11 | `tabi-shokunin/corpus/knowledge/network-evidence-rung.md` (lines 24, 163: `HTTP/1.0 304 Not Modified` observed on the wire) and `corpus/evidence/w4-t41-network/run6-reval/` | Conditional request (C2 adjacency) | Both touch 304 revalidation. Tabi observes what a browser-driven fetch received. Kake's `scripts/conditional_eval.py` decides which status a recipient would answer over supplied values; no network, clock or cache store (contract scope). | **Province-local.** Crawler/browser wire observation versus publisher-side contract decision function. | PROVINCE-LOCAL: no absorption; cite tabi for the wire-truth boundary only. |
| 12 | `kumitate-shokunin/corpus/knowledge/receipt-age-on-the-compare-path.md` (+ `scripts/omp-census.mjs --max-age`; cites RFC 9111 §4.2.3 as S237) vs kake `corpus/knowledge/cache-current-age.md` + `scripts/cache_current_age.py` (RFC 9111 §4.2.3 as S462) | Conditional / cache age (C2 adjacency) | Same RFC section cited for an age threshold. Kumitate's `--max-age` gates receipt age in days against a wall clock for a compare verdict. Kake's is HTTP `current_age` arithmetic. | **Province-local.** Different subject; no shared code. Two source rows (S237, S462) cite the same section — a fleet source-registry observation, not a kake defect. | PROVINCE-LOCAL: no absorption; note the duplicate section in the source-registry census. |

## Counts

- Overlap candidates with an opened sibling artifact: **12** (rows 1–12).
- Contested: rows 1, 2, 3, 4, 5, 6, 7, 9 = **8**.
- Province-local: rows 10, 11, 12 = **3**.
- Fleet standard, not contested: row 8 = **1**.

Verdict line (for the L1): `CONNECTOR overlaps=12 contested=8`

## Routed defects (R94-1 … R94-9) against sibling coverage

Read-only check: which routed items a sibling instrument already covers, so the round-95 lesson can cite rather than re-derive.

- R94-1 (strict parse of Gate/Mistakes/source lines, symlink and `/tmp` rejection): no sibling match in the opened files. Chousa `selfcheck-v2.py` covers digest-validated repair lines, not these parse rules.
- R94-2 (effectful shadow, sys.path hygiene): no sibling match in the opened files. Kotodama `gate-battery-surface-verification.md` covers mirror isolation for the battery, not module shadowing.
- R94-3 (repair removing backticks): chousa QUALITY criterion 146 names the same gaming class (set-membership repair with no content check) → cite (row 2).
- R94-4 (equivalence check per survivor): rows 4 and 5 are the contrasting fleet instruments → contested.
- R94-5 (directory references need a blob): no sibling match in the opened files.
- R94-6 (empty list members): HTTP grammar, kake-only; no sibling instrument.
- R94-7 (battery over every rule class): rows 3 and 4 are sibling batteries; neither is a substitute for kake's battery.
- R94-8 (population base pin): row 6 is the sibling analogue (counter blob at measured revision).
- R94-9 (registry rows for prior counters): row 7 and the fleet PROTOCOL registry-home clause (PROTOCOL-APPENDIX.md "Registry home", row 14) → cite.

## Not run

No counter was executed (seat is read-only and the instruments are frozen). Tooling installed: none. Every verdict above rests on committed text read at the HEAD named above; no observed rc is claimed beyond the `sha256sum` check (rc 0).
