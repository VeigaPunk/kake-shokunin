# ExecRegistry — round 85, wave 1

Axes: registry discoverability, exit-map accuracy, retained reproducibility; preserve frozen semantics and production read-only scope.

## Deliverable

Three exact eight-column candidate SKILL rows are in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ExecRegistry/registry-rows.md`. L1 alone may integrate them after WAVE-DONE. Each row names the actual command, CLI exits, isolated selftest, persisted expectations/receipt, write scope, and owner kake. The two counters are explicitly historical frozen round-84 instruments; the classifier is explicitly experimental. None grants publishing approval, field-specific Referrer-Policy correctness, independent closure, or full D84 closure.

Production files were read only. No VCS mutations, network requests, installs, dispatch, or external-state changes. No LSP tool is exposed in this seat; CLI/exit inspection used direct source reads rather than claiming symbol-index coverage.

## Executed commands and retained evidence

All subprocesses used cwd `/fast/scratch/hyaku/kake-r85/ExecRegistry` and TMPDIR equal to that directory, with Python bytecode disabled. Each JSON receipt below retains exact argv, cwd, TMPDIR, exit, stdout and stderr; controls also retain their complete SKILL fixture. Absolute command prefixes are retained in the receipts, not abbreviated executable instructions here.

| Receipt basename | Invocation | Observed result |
|---|---|---|
| selftest-defect-queue.json | python3 -B, absolute round-84/c84_defect_queue.py, --selftest | exit 0; 8/8 passed |
| selftest-policy-values.json | python3 -B, absolute round-84/c84_policy_values.py, --selftest | exit 0; 4/4 passed |
| selftest-policy-value-class.json | python3 -B, absolute scripts/policy_value_class.py, --selftest --work /fast/scratch/hyaku/kake-r85/ExecRegistry/classifier | exit 0; 15/15 passed |
| c1-base.json | python3 -B, absolute round-85/count.py, --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7 --claim c1 --work /fast/scratch/hyaku/kake-r85/ExecRegistry/baseline | exit 1; complete=0/3, missing=3 |
| dummy-complete.json | same frozen counter, --claim c1, scratch-only SKILL root and work | exit 0; complete=3/3, missing=0 |
| dummy-missing-cell-1.json through dummy-missing-cell-8.json | same frozen counter, each scratch fixture blanks the named cell in all three otherwise-complete dummy rows | all exit 1; complete=0/3, missing=3 |

All receipt files are under `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ExecRegistry/`. `source-digests.json` retains SHA256 for the inspected contract, counter and three instruments. No other checks were run. Candidate integration/counting is left to L1; the reported 3/3 positive control is deliberately dummy data, not an integrated candidate measurement.

## Findings, defects and limits

1. Both round-84 counters use plain argparse: unknown/malformed options exit **2**, not the docstrings' blanket usage=64. Missing --root explicitly returns 64; --help returns 0. c84_defect_queue returns 2 for an invalid root, but missing files at an existing root ordinarily become failed predicates (exit 1). c84_policy_values has explicit unevaluable returns 2, but uncaught export/I/O/conversion exceptions are not uniformly normalized. Rows document these distinctions; no unassigned CLI probes were run.
2. policy_value_class handles parse errors as 64, caught input errors as 1, and successful printing as 0 even for policy-changed or policy-unclassified. A selftest failure also returns 1. Its selftest is 15 checks, not 15 independent HTTP-field semantics cases: twelve generic cases, canonicalization, unchanged verdict, corrupt retained-body rejection.
3. c84_policy_values --selftest covers only four parser/offline canaries. It neither runs the full capture matrix nor establishes the semantic validity of the frozen Referrer-Policy reordered expectation. That expectation remains in the frozen JSON; no rewrite or semantic upgrade is proposed here.
4. The existing persisted `after-c1-v2.txt` names C1v2 and row_named checks; the inspected c84_defect_queue source prints C1v1 and lacks those row_named conjuncts. Its D3 uses a settled connector output as row evidence, and D4 uses positive W04 count equality rather than the contract's prose row requirements. Therefore the v2 historical receipt is not represented as proof of the inspected source. The candidate row points to the current selftest receipt and identifies historical bounded scope, not current queue closure.
5. The complete dummy rows pass because count.py checks syntactic discoverability, not executable commands, valid persisted proof paths, or semantic adequacy. Every one of the eight missing-cell controls fails. This matches the frozen C1 scope but is not full registry gate conformance. In particular, selftest success is not independent acceptance.
6. Historical counters may turn red as frozen input populations change; this is not by itself a production regression. Neither round-84 counter was rerun normally in this seat. No revision-specific green status is newly asserted.

## Handoff and cleanup

Only the candidate rows, JSON receipts, digest manifest, and this report were written beneath the assigned deliverable paths. All generated fixtures were scratch-only; receipts preserve their inputs before scratch removal. The exact scratch directory was removed before terminal handoff. Installs: none. Assimilation: none. Blockers: none within the assigned scope.

L1 should integrate the candidate rows, then run the frozen C1 counter at its integrated revision and apply the independent semantic review. No C2 decoder work or complete D84-queue claim is made by this seat.

Self-evaluation (advisory, not judging): accuracy 4 (CLI exception normalization is source-inspected, not exhaustively exercised); completeness 4 (integration is intentionally L1-only); clarity 4 (long absolute command cells trade readability for reproducibility); actionability 4 (ready rows still require L1 integration); conciseness 4 (receipts hold detailed execution data). Mean 4.0. Improvement: L1's post-integration check should bind the integrated rows to its final revision. The user should agree these limits match the assigned boundary.

Report: .ufo/waves/round-85/w1/ExecRegistry.md
