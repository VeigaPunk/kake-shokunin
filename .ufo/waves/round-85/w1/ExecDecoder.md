# ExecDecoder — round 85 w1

## Deliverable and axes

Candidate: `.ufo/waves/round-85/w1/ExecDecoder/referrer_policy_effective.py` (complete Python stdlib implementation; production unchanged).
Axes: field-order correctness, strict input/exit behavior, isolation, reproducible evidence. No registry/C1 or full D84-queue closure claim.

The decoder accepts stdin UTF-8 JSON lists containing only strings, traverses fields and comma-separated tokens in order, strips surrounding whitespace, and retains the last recognized case-sensitive policy token. All eight contract tokens are recognized. Empty/unknown tokens do not reset policy. Normal output is one JSON object containing only `effective`; no token produces the empty string. Invalid JSON, non-list input, non-string members, all objects (including duplicate-key objects), nonstandard JSON constants and invalid UTF-8 fail with exit 1 and no stdout. Invalid CLI usage exits 64. `--selftest` exercises actual subprocess exit codes and output with entirely in-memory fixtures, without fixture or live-tree writes.

## Executed checks and retained evidence

Both checks ran against the isolated minimal tree under `/fast/scratch/hyaku/kake-r85/ExecDecoder/tree`, with cwd `/fast/scratch/hyaku/kake-r85/ExecDecoder`, TMPDIR `/fast/scratch/hyaku/kake-r85/ExecDecoder/work`, and `PYTHONDONTWRITEBYTECODE=1`.

1. `python3 -B /fast/scratch/hyaku/kake-r85/ExecDecoder/tree/scripts/referrer_policy_effective.py --selftest`
   - Exit 0; stdout `selftest: 32/32 passed`; stderr empty.
   - Receipt: `.ufo/waves/round-85/w1/ExecDecoder/selftest.json`.
   - Coverage: every policy, ordered/reversed multi-field inputs, unknown preservation, case sensitivity, empties, malformed/trailing JSON, duplicate and nested objects, non-string types, invalid UTF-8, and usage errors.
2. `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/count.py --root /fast/scratch/hyaku/kake-r85/ExecDecoder/tree --claim c2 --work /fast/scratch/hyaku/kake-r85/ExecDecoder/work`
   - Exit 0; all case indices 0–9 report `matches=1`; final `C2 cases=10/10 met=true`; stderr empty.
   - Receipt: `.ufo/waves/round-85/w1/ExecDecoder/counter.json`.

## Limits, defects and handoff

- Counter invocation used its worktree mode against a minimal tree containing only the candidate; no revision claim or production integration is implied. This is author-side evidence, not independent closure.
- The mandated initial whole-file counter read exposed its frozen CASES before implementation. No additional lookup occurred, no counter outputs were hardcoded, and candidate logic implements the contract's general eight-token algorithm. This exposure means author blindness cannot be claimed.
- ExecTrial reports an independent retained-control reference trial: A effective `strict-origin`, B effective `no-referrer`; its scoped assignment does not run this candidate. This seat did not execute an additional retained-control candidate trial. L1 owns post-integration retained-trial verification and final closure.
- No LSP interface was exposed by the mounted tools; no supported symbol-reference operation was available. Candidate is standalone; no existing production caller is changed.
- No production files, VCS state, external services, credentials, sibling artifacts or PATH directories changed. No installs, network requests, build, lint or formatter runs. Assimilation: none.
- Receipts were retained before scratch removal. Cleanup command: `rm -rf /fast/scratch/hyaku/kake-r85/ExecDecoder`.

## Self-evaluation

Accuracy 4: 32/32 CLI assertions and 10/10 frozen witnesses, but author-side only. Completeness 4: scoped candidate and assigned checks complete; retained candidate trial belongs to L1. Clarity 4: exact commands and limitations retained; verbose report deliberately preserves provenance. Actionability 4: integration-ready candidate, but no integration authorization. Conciseness 4: implementation includes subprocess selftests rather than a separate fixture tree. Overall 4.0/5. Improvement: L1 independently validates integrated bytes and retained controls. User agreement expected on the bounded implementation, not a full-queue closure claim.

Report: .ufo/waves/round-85/w1/ExecDecoder.md
