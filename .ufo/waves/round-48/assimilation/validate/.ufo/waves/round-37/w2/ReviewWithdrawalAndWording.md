# ReviewWithdrawalAndWording — measured tip 79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c
Axes: operability (claim sizing / reproducibility); freshness only as lane context.
Recommendation only; no admission verdict, implementation edits, runtime invocation, or integration.

## Findings, highest severity first
1. MEDIUM — WRONG, SCORECARD.md:2009 evidence cell: “against 0 at base and at most 20 for the controls that skip rules”.
   The declared ablation controls skip rules and reach 24, not at most 20: verification/ablations/ablation-a_2xx.json, ablation-g_version.json and 29 others reach 24. All 34 range 16–24. Narrow this bound to named pre-follow-up public controls, or say 24 including ablations.
2. MEDIUM — WRONG, SCORECARD.md:1778–1779: “Every case of a bullet carries one check per listed rule of that bullet, and every case has at least one check that holds and one that does not.”
   Sealed cases.json:1, cases g1–g4 each have four input_invalid runs (nothing evaluated) and one one-check blocked run. None contains an evaluated hold-producing check. This directly falsifies the second conjunct; f2/f4 duplicate ids must not be mistaken for absence of a hold (their first duplicate-id check does hold).
   First conjunct is OVERSTATED if “listed rule” means the public contract: f cases contain no non-object/missing-id/empty-id checks; g has no >64-MiB or nonregular manifest run. Private reference/cases.py:23–28 lists selected ablations instead. Name that narrower list rather than every public rule.
3. LOW — OVERSTATED, SCORECARD.md:1940–1942: “and a snapshot set of 299 random manifests whose expectations were recorded from E1 (no contract reading) **32 of 32, met** (commit `da09e6c7` in the seat's sandbox; 398 fixtures valid on E1 and E2). A sourceless fixture set meets the counter, so the counter does not measure the claimed surface (contract-grounded fixtures).”
   The appended 299 expectations were recorded, but the final set retains 101 incumbent fixtures: 400 total, 398 valid. Initial replacement-only snapshot killed 27, not 32. retained/controls/c2/variants.json:38,49 explicitly disclaims human contract-blindness (embedded docstring exposed) and describes retention. Say “recorded-oracle additions to incumbent fixtures”; do not call the whole final set sourceless or the human contract-blind. This does not undermine conservative withdrawal.
4. LOW — WRONG literal identity, SCORECARD.md:1767–1770: “Frozen predicate, the same sentence here, in `.ufo/waves/round-37/sealed_count.py` (`PREDICATE`, `met = cases == 28 and passed >= 25`) and in every receipt's `predicate` field:” followed by “met: passed >= 25 of 28 sealed cases”.
   Code PREDICATE and all 178 C1 predicate-bearing JSON receipts contain exactly “passed >= 25 of 28 sealed cases”, without “met: ”. All ten C2 receipts likewise omit that display prefix. Logical target and normalized sentence identity HOLD; strict byte identity including the label does not. No observed predicate drift.
5. LOW — WRONG, SCORECARD.md:2001–2002: “Capability row "Offline robots.txt expectation audit" entered `## Capabilities` below. Axis ratings unchanged (10 → 10).”
   First sentence is wrong: the canonical ## Capabilities is at line 187 and lacks this row; the row is under ### Capabilities acquired in round 37 at 2005. Ratings sentence is unchanged, not a new saturation measurement.
6. LOW — OVERSTATED, SCORECARD.md:1785–1787: “On every run the counter replaces every check id and robots file name with fresh random ones, so no tool can key on ids, file names or labels; the tool runs in a bubblewrap jail that sees only /usr and the scratch directory.”
   sealed_count.py:166 also mounts /proc, /dev and tmpfs /tmp. Materialization preserves robots directory components and duplicate-id relationships; fresh strings do not prove the universal “no tool can key” statement. This is not evidence of a demonstrated successful shortcut.

## Withdrawal and claim-size sentence verdicts
- HOLDS as pre-build chronology, SCORECARD.md:1937: “C2 is withdrawn before any data.” Baseline/control data already existed; “before any build measurement” is the precise meaning supported by history, not literally before all data.
- HOLDS, SCORECARD.md:1945–1947: “The fixture repair for the five selftest survivors (routed defect 3) continues as non-claim work; its counter output is reported as evidence only. C1 is the round's only claim.”
  Withdrawal commit 4b089da6 precedes repair 528a6d02 and build 9dbc88bb. The measured-results claim table contains only C1; C2 27→32 is explicitly non-claim evidence at 1999–2000.
- HOLDS with the same chronology qualification, lesson:21–23: “C2 (declared at `202d625a`: the selftest fixture data kills the 32 round-36 mutants) was **withdrawn before any data**: a snapshot fixture set recorded from E1 on random inputs met its counter (32 of 32). Its fixture work continued as non-claim routed repair (below).” Snapshot composition/blindness qualifications above should propagate here.
- HOLDS, lesson:25–28: “Neither counter, the key nor the predicate changed after the declaration.” Counter hashes across all seven named revisions are singleton sets; revealed key equals declaration pin. No pre-reveal key bytes independently available to inspect.
- HOLDS with chronology qualification, LOG.md:1513–1516: “Control call (8 seats): C1 controls ≤ 20; C2's snapshot control met (32 of 32) → C2 withdrawn before data (`4b089da6`).” Here ≤20 is scoped to that public-control call, before the separately disclosed 28-point shortcut follow-up; not all ablations.
- HOLDS as a limitation, SCORECARD.md:2009: “the sealed cases certify the tested rules of (a)–(g), not every contract sentence”. The earlier row's “each check” describes intended tool behavior, not a quantified proof supplied by 28 cases. Counter judge (sealed_count.py:141–159) compares exit/verdict/findings only, not report version, checksEvaluated, usage exit 64, no-write behavior or all public-contract edges. Selftest is a separate instrument, not an enlargement of the frozen predicate.
- UNVERIFIABLE as a cited rule, SCORECARD.md:1943–1945: “Under the round rule a counter that a control meets is redesigned before data or the claim is dropped; no redesign that separates contract-grounded from recorded expectations was found in time, so C2 is not a claim of this round.” Declaration 1893–1894 says fixed before any build, not “or dropped”; no independently located rule authorizes that quoted branch. Withdrawing rather than claiming the result is nevertheless conservative.

## Reproduction and observed outputs
Exact bounded command (exit 0):
`timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w2/ReviewWithdrawalAndWording/tmp python3 -B /fast/scratch/hyaku/kake-r37w2/ReviewWithdrawalAndWording/audit_wording.py`
The retained script reads pinned objects with `timeout 60 git -C /home/vgpnk/Projects/shokunin/kake-shokunin show <revision>:<path>` and `ls-tree`/`log`; every successful subprocess is checked. No code under review is executed.
Observed: 178 C1 and 10 C2 predicate-bearing JSON files; zero code-to-receipt mismatches. C1 includes retained mutant outputs and the round-36 junk receipt; unrelated selftest/source/live JSON without predicate fields is not counted as counter output.
C1 counter hash: 2ebb39b585e2a35f16ff71397f2fb22477a7a3c0e95da4415a26b0430b0cf0e3.
C2 counter hash: d72e232e4d4f120b6b45139958c40e9364d44d3d902207c0705ac97c1b6d5cb6.
Key hash: 93ad9ee64db63b661b408e678f2c6f3d665b7f5c88ef1f977433dbceee8c0a90.
SCORECARD hash: 27eb050a667f5d26245faea4de700f1916bc2dde309248a546dc2fbd038badef.
Lesson hash: 0dcd067a8a7263e251cd159d9917a05949a61e95c9242de0a84483fa6a52b9be.
LOG hash: 14f91b459d661a3f46f083984dcdb824d8e0d4fdfd7bd23a32713bd9cc23b986.

## Residual risk / verification gaps
No counter rerun or live network check; receipt values are inspected, not independently reproduced runtime outcomes. Chronology establishes committed order, not private observation times. No saturation increase is measured or recommended.
LSP unavailable: `read xd://lsp` returned “No such tool”, mounted devices only ast_edit/debug; therefore no semantic references/definition/diagnostics claim. Text/object inspection is the fallback.
No resume/runtime/rerouting changes in scoped documentation; no resume_continuity_v1 conclusion. No installations, background processes, or lane writes beyond this report.
