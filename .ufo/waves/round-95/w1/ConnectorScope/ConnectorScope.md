# ConnectorScope — round 95 seat report

Seat: ConnectorScope (connector, leaf member, read-only). Wave: round-95 w1. Lane: kake-shokunin.
Deliverable: `overlaps.md` (same directory). Verdict line: `CONNECTOR overlaps=12 contested=8`

Path note: the seat spec names `.ufo/waves/round-95/w1/ConnectorScope.md`. The hard bounds limit writes to `.ufo/waves/round-95/w1/ConnectorScope/`, so this report and `overlaps.md` are written there. The L1 should move or re-point the Report trailer.

## Scope and what was read

Instrument classes this round lands (from `freeze.md` and `c2-contract-v2.md`): a strict self-assessment counter (E1–E5, content-pinned identity), a conditional-request contract-v2 counter with a mutant-equivalence kill rule, and registry rows for prior counters (R94-9).

Sibling files opened (committed bytes, HEAD named in `overlaps.md`):
- kumitate-shokunin: `scripts/gate-mutants.mjs`, `scripts/counter-pins.mjs`, `corpus/knowledge/receipt-age-on-the-compare-path.md`, `corpus/knowledge/counter-receipt-source-binding.md`, `SKILL.md` (gate registry rows 589–627), `.ufo/waves/round-40/build/ConnSiblingOverlap.md` (prior connector precedent, read only).
- kotodama-shokunin: `corpus/knowledge/verification/gate-frozen-run-standard.md`, `corpus/knowledge/verification/gate-battery-surface-verification.md`, `tools/gates/` listing.
- chousa-shokunin: `corpus/evidence/round79/selfcheck-v2.py`, `corpus/evidence/round34/self-audit.py`, `corpus/evidence/round62/controls/` listing (`null-counter.py`, `path-keyed-counter.py`, `c1v2-before.txt`), `corpus/evidence/round79/` listing, `corpus/QUALITY.md` lines 880 and 1054, `SKILL.md` lines 53, 91–94, 118, 175, `corpus/README.md` line 9.
- tabi-shokunin: `scripts/check-selfassessment.mjs`, `scripts/check-gate-mutants.mjs`, `scripts/check-measurement-binding.mjs`, `scripts/check-freshness.mjs`, `corpus/knowledge/network-evidence-rung.md`, `corpus/evidence/round-24/c2-measurements.json`, `SKILL.md` registries (lines 1555–1849, 2479–2627).
- kake-shokunin (own tree): `scripts/conditional_eval.py` (header), `corpus/knowledge/cache-current-age.md`, `corpus/knowledge/conditional-request-evaluation.md`, `corpus/QUALITY.md` lines 1769–1830 (Round 90, Round 92 criteria), `corpus/lessons/round-94.md`, `corpus/lessons/round-94-verifier-spotcheck.md`, `SKILL.md` 181–240, `.ufo/waves/round-95/c95_selfassess.py` (header), `.ufo/waves/round-95/w1/ConnectorScope/`. The round-94 ConnectorScope report (`.ufo/waves/round-94/w1/ConnectorScope.md`) was NOT opened; its one-line outcome is only as summarised in `corpus/lessons/round-94.md` `## Wave review and Routed` ("two terms overlap in principle only; four sibling lanes cited, not absorbed").
- Fleet: `PROTOCOL.md` lines 375–392 (§Gate standard), `PROTOCOL-APPENDIX.md` rows "Gate standard" and "Registry home", `AXES.md` line 15 (calibration).

## Findings

1. **Self-assessment counter class is shared across four lanes.** Closest instances: tabi `check-selfassessment.mjs` (calibration of claims against observed state) and chousa `round79/selfcheck-v2.py` (registry-row, Mistakes-row and criteria path checks with digest-validated repair lines). Chousa's QUALITY criterion 146 already documents the R94-3 gaming class. Kake should cite that criterion, not port the code. (Overlap rows 1–2, both CONTESTED.)
2. **Mutant kill and equivalence are defined two ways in the fleet.** Kumitate K43 requires rerun stability; tabi's benign-mutant catalogue declares equivalence at authoring time; kake R94-4 requires digest-pinned equivalence receipts for survivors. No fleet rule decides between them. This is a fleet-level question for the L1 or the protocol owner; kake's C2 should state its default and not adopt another lane's (overlap rows 4–5, CONTESTED).
3. **Do-nothing and forger controls are a shared method rule.** Chousa's round-62 controls (`null-counter.py`, `path-keyed-counter.py`) and kake's QUALITY "Round 90" criterion encode the same admission test independently. Cite as independent discovery (row 3, CONTESTED).
4. **Quote verification overlaps chousa's source-hierarchy gate.** Chousa `tools/quote-reopen.py` and kake's S477/S478 located-quote checks use the same ≤25-word exact-substring rule. Kake has no committed quote gate; the L1 should decide whether one belongs to chousa (row 9, CONTESTED).
5. **Instrument binding and registry pins.** Tabi `check-measurement-binding.mjs` and kumitate `counter-pins.mjs` bind counter bytes to measurements and registries. Kake's R94-8 and R94-9 work is the same discipline without a machine check. Cite, do not import (rows 6–7, CONTESTED).
6. **Province-local, not absorbed.** Tabi `check-freshness.mjs` (local plugin bytes), tabi `network-evidence-rung.md` (304 wire observation) and kumitate `receipt-age-on-the-compare-path.md` (receipt-day age; cites the same RFC 9111 §4.2.3 section as kake `cache_current_age.py`, under a different source row S237 vs S462) do not overlap kake's publisher-side semantics in subject or code (rows 10–12, PROVINCE-LOCAL).
7. **Frozen-run standard is fleet policy.** Kotodama `gate-frozen-run-standard.md` restates PROTOCOL §Gate standard "Two evidences". Kake complies. No action (row 8).

## Routed-defect coverage

Per `overlaps.md` §Routed defects: R94-3 is covered in principle by chousa QUALITY 146. R94-4 has two contrasting fleet instruments. R94-8 and R94-9 have sibling analogues (tabi measurement binding, kumitate counter-pins, PROTOCOL registry-home clause). R94-1, R94-2, R94-5 and R94-6 have no sibling match in the opened files. R94-7 is partly covered by sibling batteries but is not substituted by them.

## Doctrine scan (merge/kake/doctrine)

Not scanned: `merge/kake/doctrine/` is absent. `find /home/vgpnk/Projects/shokunin -maxdepth 4 -type d \( -name doctrine -o -name merge \)` returned no output; `find … -maxdepth 6 -type d -name doctrine` returned no output; `kake-shokunin/merge` → ENOENT. The round-95 freeze's assimilation note (`.ufo/waves/round-95/assimilation/collisions`, ids S312/S329/S367/S372–S374/S390/S409) refers to a package that is not in this tree. The L1 should confirm where the merge package lives before any doctrine comparison.

## Checks and receipts

- `sha256sum` on `c95_selfassess.py` and `c95_conditional.py` — rc 0; both digests match the spec and `controls/instrument-sha256.txt`.
- Sibling reads: `git -C <lane> show HEAD:<path>`, `git -C <lane> grep … HEAD`, `git -C <lane> ls-tree --name-only HEAD <dir>` — each printed the expected content (output observed; per-command rc not captured explicitly).
- Absence checks (doctrine, merge): `find` and `ls` returned no matches / ENOENT (output observed).
- No counter was executed. No sibling file was written. No git mutation was run.

## Tooling

No tools installed or upgraded. Read-only shell and grep only.

## Hygiene

Scratch root `/fast/scratch/hyaku/kake-r95/ConnectorScope/` was created and holds nothing; it is removed before yield. The w1 seat directory holds `overlaps.md` and this report only.

## Verdict

CONNECTOR overlaps=12 contested=8
