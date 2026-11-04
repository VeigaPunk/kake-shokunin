# ReviewCounter — frozen C1 independent attack

Axes: calibration 2 HOLD; freshness 10 HOLD. Scope: finite C1 ledger/source agreement, not C2 arithmetic or outside admission. Read-only production review; no predicate, target or frozen bytes changed.

## Findings by severity

### Low — C1 has an unnecessary C2-fixture startup dependency

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/count.py:11-12` eagerly loads both expected-ledger.json and age-cases.json, before claim selection. C1's predicate and runtime branch (lines 18-27, 54-61) do not use CASES, any receipt, any C2 result, or the C2 tool. Thus there is **no receipt/C2-output dependency**, but asserting complete C2 independence would be inaccurate: absence or malformed JSON in the C2 fixture prevents C1 from producing its result.

Bounded scratch probe copied the frozen counter and ledger oracle unchanged, omitted age-cases.json, and invoked C1 with the real explicit root/freeze: exit 1, no JSON stdout, FileNotFoundError at line 12. Receipt: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewCounter/startup-dependency.json`. This is not a failure at the intact frozen tree, whose fixture exists. Recommendation for a future authorized counter: load C2 cases only in C2 branch; do not amend this frozen instrument.

## Predicate result and source truth

No mismatch found between the eight expected rows and the three committed source tables. Independent reads used git show at freeze, not fleet/live source paths. All snapshot SHA-256 values equal the expected rows:

- Round 84: `80f48887b1e5f2e9d7d54adcce19d8b935f77fc0b236620abac3335b730dfda9`; table lines 73-75: admit/mined, reject, reject; agreement agree for all three.
- Round 85: `948c316831d0c71927e6a29501f05037b3faa940a251984ed28ca8f0eee2ce71`; table lines 71-72: admit, reject; agree for both.
- Round 86: `47499686bc976564c43174fdeeae2219e0db2351c571678ba35caff0a34de42b`; table lines 89-91: admit (A), admit (A), reject proposition; agree for all three.

Table paths are `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/snapshots/round-{84,85,86}-verifier-spotcheck.md`. Expected normalized `admit`/`reject` correctly preserve these source decisions; Markdown bolding on round-86 agree does not change meaning. Full extracted rows and digests: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewCounter/source-checks.json`.

The exact counter measures parsed row equality against a fixed expected ledger plus snapshot-byte integrity, **not independently performed self-assessment or live source truth**. Scratch `copied_oracle_without_assessment` passes with zero mismatches, using only a deep copy of expected rows and frozen source bytes. A writer can copy correct claims without doing assessment; false provenance/process claims can therefore accompany a green tally. Conversely, changing an actual assessed decision or outside-agreement field fails. This disclosed finite-limit is consistent with contract lines 8-17, not a newly discovered violation. Digests authenticate identity relative to frozen expected values, not historical authorship or truth of the underlying reports. No network truth checks were attempted.

## Authorized executions and exact exits

Commands executed concurrently, from explicit scratch cwd:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --work /fast/scratch/hyaku/kake-r87/ReviewCounter/count --selftest
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 86ca7803fd964db7ae2a628c7e9048741c78a45f --claim c1 --work /fast/scratch/hyaku/kake-r87/ReviewCounter/count
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 58fee726102aa89ad2c1fa9f697869de3a212510 --claim c1 --work /fast/scratch/hyaku/kake-r87/ReviewCounter/count
```

Results: selftest exit 0, 6/6; base exit 1, population 8/mismatches 8/met false; freeze exit 1, population 8/mismatches 8/met false. Both revisions genuinely lack `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/gate-agreement-ledger.json` (git show exit 128), so neither is an after-integration success measurement. Base missing8 is an absence baseline, not eight observed false decisions.

Independent scratch JSON mutants exercised `ledger_errors` directly, using source reads from the frozen commit:

| Mutant | Mismatches | Predicate |
|---|---:|---|
| empty | 8 | fails |
| missing one row | 1 | fails |
| outside=disagree | 1 | fails |
| wrong source hash | 1 | fails |
| duplicate expected row | 2 | fails |
| extra unrelated row | 1 | fails |
| tampered snapshot reader | 8 | fails |
| copied oracle without assessment | 0 | passes |

These are function-level predicate results, not separate CLI process exits. Duplicate yields two because its matching key has multiplicity two and length exceeds population by one; mismatch counts are penalties, not universally bounded to eight.

Exact driver invocation: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewCounter/review.py`, exit 0. Retained driver and JSON receipts describe all subprocess argument vectors, stdout/stderr and exits. Receipts are under `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ReviewCounter/`: commands.json, mutants.json, source-checks.json, immutable-inputs.json, startup-dependency.json. Read-only diff command `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --stat 86ca7803fd964db7ae2a628c7e9048741c78a45f 58fee726102aa89ad2c1fa9f697869de3a212510` exited 0 and showed 13 new wave-input/control files, no ledger artifact.

## Immutability, residual risk and verification gaps

The three snapshots, expected ledger, contract, count.py and age cases all read successfully from freeze; each current worktree file was byte-equal to its committed frozen counterpart at review. Committed source reads remain revision-addressed through count.py lines 14-16 and 52-53. One caveat: the executed counter loads its expected oracle from its own worktree directory, not automatically from --revision. This review explicitly established equality to frozen bytes, so that did not change the observed score. It is not a claim that mutable host files can never change later.

LSP device unavailable: `read xd://lsp` returned “No such tool”; no status/references/definition/diagnostics endpoint was available. Structural inspection and direct execution were the fallback, not semantic LSP proof. No candidate integrated ledger was scored because the assignment names base and freeze only; all reachable frozen-target checks were completed. Canonical runtime rerouting/resume continuity and saturation machinery are not touched by this C1-only diff. No general calibration, universal no-harm, closure, or outside admission recommendation is inferred.

No builds/lints, broader tests, provider probes, model calls, services, installs, repository mutations or clones. Python stdlib only. Scratch was explicitly created and removed after receipts were retained (both driver and additional startup probe printed scratch_removed true). No scratch or full-lane mirror remains.

Self-evaluation: accuracy 4 (reproducible finite observations, no live-source truth claim); completeness 4 (requested mutations/source/base/freeze covered, integrated carrier intentionally outside assigned revisions); clarity 4 (explicit operational versus logical C2 dependency); actionability 4 (future branch-local load recommendation, frozen target retained); conciseness 4 (long commands retained for reproduction). Overall 4.0/5. Highest-impact improvement applied: distinguish missing-row baseline and copied-oracle pass from truthful assessment. User agreement expected because limits are explicit.

Report: .ufo/waves/round-87/w1/ReviewCounter.md
