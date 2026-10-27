# ConnCrossClaim

Cross-claim coupling scan: evaluated `contract.md` (§ Causal separability, §§ Claims C1/C2/C3) against base `9f07731a`, commit `eaa9177`, and wave-1 peer implementations. Supporting artifacts: `.ufo/waves/round-61/w1/ConnCrossClaim.files/` (`coupling_matrix.json`, `extra_member_proof.txt`).

SEPARABILITY:
The contract's § Causal separability paragraph asserts claim independence ("C1 reads only git history... C2 reads only... C3 reads only... neither touches C1's surface"), but analysis reveals four major breakdowns:
1. `neither touches C1's surface` is FALSE under the frozen C1 surface definition (`every receipt file committed at the measured revision under .ufo/waves/round-<N>/control[s]/*.{txt,json}`). The round-61 receipt rule (contract line 18) mandates receipts land in `.ufo/waves/round-61/controls/`. In commit `eaa9177`, `census-before.txt` and `population-144.txt` were already committed there, and wave measurement receipts (e.g. `after-c2-header-cases-t1.txt`) will land there. Both `ExecC1Tool2` (`head.err`: `population_rule_extra`) and `ExecC1Counter` confirm these match the pattern and trigger `extra_member` false reds.
2. `C3 reads only... neither touches C1's surface` ignores C3 Condition C6 (`rows not in the due set are byte-identical to base`). Because C2 appends S430–S433 to `corpus/SOURCES.md`, C3's counter directly reads C2's rows. A naive non-due set equality check breaks C3.
3. The paragraph omits that all three claims mutate `corpus/lessons/round-61.md`. C3 counter conditions C3 and C5 mandate parsing lesson Gate lines; syntax or formatting faults in C1's mistake rows or C2's Gate lines can fail C3.
4. The paragraph asserts C1 reads `SCORECARD.md`/`SKILL.md`, but omits that C2 adds a capability row to `SCORECARD.md` upon demonstration, and both C1 and C2 append rows to `SKILL.md`'s gate registry.

SHARED WEAKNESSES:
1. Lesson file bottleneck: `corpus/lessons/round-61.md` is a single shared integration sink. C3's hard counter conditions (C3, C5) depend on strict parsing of this file, creating a cascading failure route if C1 or C2 edits disrupt markdown structure.
2. Remote RFC 9110 endpoint & census coupling: C3 live-fetches S010 (`rfc9110.html#section-8.8`) and C2 sources S433 (`rfc9110.html`). Both hit `www.rfc-editor.org` on 2026-10-27 with userAgent `round61`. Both share the canonical URL with existing S088, incrementing census W04 warnings from 15 to 16. Upstream connectivity issues or rate limiting would break C2 and C3 simultaneously.
3. Unified measured revision (`<rev>`): All three counters evaluate the same commit tip. Because no partial admission exists, an unhandled disclosure in C1, a missing capture receipt in C2, or a quote mismatch in C3 blocks the entire round.
4. Non-controls receipt asymmetry: C2 capture receipts (`capture/<id>/response.json`) feed both counter case R3 and the round report, but live outside `controls/` and are thus completely unmonitored by C1 lineage tracking.

INTERACTIONS:
1. C1 ↔ C2:
   - Controls namespace collision: Any C2 run receipts committed to `.ufo/waves/round-61/controls/` trigger `extra_member` under C1.
   - SCORECARD parsing: C2 capability row addition must not disrupt C1 counter's `scores_held == 3` regex (10/10/2).
   - SKILL.md table concurrency: C1 (receipt_lineage, lineage_cases) and C2 (response_snapshot, header_audit) both append gate rows.
2. C2 ↔ C3:
   - Registry concurrency: C2 appends S430–S433 at end of `corpus/SOURCES.md`; C3 edits S001–S010 in place (lines 9–18).
   - Condition C6 logic: C3 counter must explicitly permit appended rows beyond base registry length while enforcing byte-identity on base rows S011–S429.
   - Due-set isolation: S430–S433 opened date `2026-10-27` guarantees they do not perturb C3 Condition C1's oldest-opened derivation (`2026-10-19`).
   - S433/S010 duplicate URL: Both map to RFC 9110, triggering census W04 warning (retained exit 0).
3. C1 ↔ C3:
   - C3 isolates bodies and receipts in `.ufo/waves/round-61/recheck/`, cleanly avoiding C1's population path rule; however, C3 counter receipts in `controls/` collide with C1.
4. C1 ↔ C2 ↔ C3:
   - Convergence in `corpus/lessons/round-61.md` and the final commit `<rev>`.

AMENDMENTS:
1. Amendment A (C1 Historical Scope Boundary): Amend C1 surface definition in `contract.md` to: `every receipt file committed at the measured revision under .ufo/waves/round-<N>/control[s]/ for N < 61`. Exclude round 61's own control files from triggering `extra_member`.
2. Amendment B (C3 Condition C6 Append Semantics): Clarify Condition C6 as: `rows present at base outside the due set are byte-identical; rows absent at base are strictly appended with IDs > max base ID`.
3. Amendment C (Separability Declaration): Expand § Causal separability to enumerate shared files (`corpus/lessons/round-61.md`, `SKILL.md`, `SCORECARD.md`) and declare cross-claim invariants.
4. Connector Bounded Proposal (Synthesis across proposals):
   - Evidence: `ExecC1Tool2/head.err` and `ExecC1Counter.md` prove `census-before.txt` and `population-144.txt` trigger `population_rule_extra` under current C1 rules. `ExecC3Pins.md` and `ScribeC2Rows.md` demonstrate clean readiness on their individual surfaces.
   - Affected Axes: Calibration (C1), Operability (C2), Freshness (C3).
   - Proposed Move: Enforce a strict round-boundary partition: C1 counter v1 pins historical population frozen at rounds `< 61` (144 members); round-61 controls are excluded from C1's `extra_member` check until round 62; C3 Condition C6 evaluates registry diff as `base_rows \ due_set == rev_rows \ due_set \ appended_rows`; and separate `corpus/lessons/round-61.md` Gate lines into dedicated subheadings (`## Gate / C2` and `## Gate / C3`).
   - Risks: Round 61's own receipts are not lineage-checked during round 61; mitigated by inheriting them into round 62's frozen historical population.
   - Verification: `python3 scripts/receipt_lineage.py --revision <rev>` exits 0 with `receipts=144 undisclosed=0 extra=0`; C3 counter exits 0 with `conditions_passed == 6 of 6`; census exits 0 with W04=16.

VERDICT: C1, C2, and C3 have 4 critical unseparated couplings (round-61 controls namespace collision, SOURCES.md C6 delta logic, shared lesson parsing, and SCORECARD/SKILL table edits); resolved by scoping C1 to rounds < 61 and formalizing C6 append semantics.
