# MutateC2 — KILLED; exact source restored

- Axes: operability (observable integrity rejection through real self-invocation); freshness (frozen-candidate/oracle identity).
- Attacked item: contract C2.frozenOracle snapshot integrity, not source-support semantics or strict C1 admission.
- Candidate: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.
- Observed isolated worktree: `/fast/scratch/hyaku/kake-r27/w2-mut4`, branch `kake-r27-w2mut4`, candidate base confirmed by `git worktree list --porcelain`.
- Only source edit: `.ufo/waves/round-27/c2_count.py:21` in that isolated worktree.
- Mutation: `if hashlib.sha256(data).hexdigest()!=digest:` → `if False and hashlib.sha256(data).hexdigest()!=digest:`. One snapshot-guard bypass; declaration/oracle guard unchanged.

## Independent expectations, declared before execution

`/fast/scratch/hyaku/kake-r27/MutateC2/probe-spec.json` was written before the pristine run and mutation.
- Pristine/restored: detector exit0, 3 cases, 0 failures; frozen omissions detected16/16 with zero false positives; snapshot alteration exit2/`snapshot_tampered`; rewritten expectedPairs exit2/`frozen_input_changed`.
- Mutant: detector exit1 with exactly snapshot case failing; changed snapshot incorrectly accepted exit0, detected16/16; expectedPairs rewrite still rejected by the unchanged declaration guard.
- Baseline failure would be inconclusive; a passing mutant would be survived. Neither occurred.

## Actual detector and commands

The unchanged `c2_count.py --selftest` invokes unchanged `oracle_selftest.py --kind c2`, which clones real candidate Git content and invokes the actual counter/gate subprocesses. No stub, echo, mocked gate, or rewritten fixture expectation was used.

```text
env TMPDIR=/fast/scratch/hyaku/kake-r27/MutateC2/tmp python3 -B /fast/scratch/hyaku/kake-r27/MutateC2/run_probe.py pristine
env TMPDIR=/fast/scratch/hyaku/kake-r27/MutateC2/tmp python3 -B /fast/scratch/hyaku/kake-r27/MutateC2/run_probe.py mutant
env TMPDIR=/fast/scratch/hyaku/kake-r27/MutateC2/tmp python3 -B /fast/scratch/hyaku/kake-r27/MutateC2/run_probe.py restored
```

Each recorder invocation runs `/usr/bin/python3 -B /fast/scratch/hyaku/kake-r27/w2-mut4/.ufo/waves/round-27/c2_count.py --selftest` inside bubblewrap with read-only host/source/object-store binds and network disabled. The selftest's hardcoded temporary root is mapped into this seat's `sandbox/`; explicit TMPDIR is this seat's `tmp/`. Exact sandbox argv is preserved in each `*.record.json`.
Only the existing detector's disposable clone creates fixture commits/index entries; isolated source-worktree refs/index and live sources are not written.
Actual boundary inputs: append `\nChanged snapshot.\n` to frozen `corpus/knowledge/static-canonical-preflight.md`; restore that clone file, then rewrite clone `c2-oracle.json` expectedPairs to `[]`.

## Actual stdout / exits

| Source phase | Detector exit; failed | frozen_missing_interior | snapshot_tampered | oracle_rewrite_not_blessed |
|---|---|---|---|---|
| Pristine | 0; 0/3 | exit0, passed=true, detected16, falsePositive0 | exit2, finding=snapshot_tampered, case passed=true | exit2, finding=frozen_input_changed, case passed=true |
| Mutant | 1; 1/3 | exit0, passed=true, detected16, falsePositive0 | **exit0, oracle passed=true, detected16, falsePositive0; case passed=false (expected2)** | exit2, finding=frozen_input_changed, case passed=true |
| Restored | 0; 0/3 | exit0, passed=true, detected16, falsePositive0 | exit2, finding=snapshot_tampered, case passed=true | exit2, finding=frozen_input_changed, case passed=true |

Every evaluated gate output above has gateExit1, citingPairs57, ledgerPairs41; the frozen expected red result is distinct from counter/selftest success. In pristine/restored snapshot rejection, output file is `corpus/knowledge/static-canonical-preflight.md`; rewrite rejection names `.ufo/waves/round-27/c2-oracle.json`. All captured outer and case stderr are empty.

## Hashes and restoration evidence

SHA-256 of isolated `c2_count.py`:
- Candidate blob / pristine: `913a797fdfcbd25d328c2291a14cb84620f4ebfe348d6fd1016415674b8ca055`.
- Mutant: `e864806211cd216cee3fa6c8c2e323843540d9bb645c8aaca30c1058370e830e`.
- Restored before restored detector: `913a797fdfcbd25d328c2291a14cb84620f4ebfe348d6fd1016415674b8ca055`.
- Exact-byte comparison after restored run: `git show ac46a7472d945a6d7ff135e4d7f07b0b6913d835:.ufo/waves/round-27/c2_count.py | cmp - .ufo/waves/round-27/c2_count.py` → exit0, no stdout.
- Unmodified selftest SHA-256, checked against candidate blob: `943db49c69dd908d0d56678dd4c9af231d00850a1aea092f90b441caafe3e460`.
- Actual gate SHA-256, checked against candidate blob: `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`.

Raw stdout retained under `/fast/scratch/hyaku/kake-r27/MutateC2/`:
- `pristine.stdout.json`: `1923abf910e048e9f76d1d7606f170348c46271ff2b2f4e74b634fd5ec0cc983`.
- `mutant.stdout.json`: `bd5bdd2d695de5d56e40e0bd8ada736f9c2789e2a2bdf69429b60e2ba55e10f7`.
- `restored.stdout.json`: `4b61d37e49eff9b5518542995c343a5279993cbf3ebeedcbfe0e33c4c11adabe`.
- Each phase also has `*.record.json` and empty `*.stderr.txt` (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

## Verdict and limits

**KILLED** by actual snapshot consumer self-invocation: pristine accepted the bounded detector, the bypass accepted altered snapshot bytes and made the detector fail, and exact restoration restored the expected rejection and detector success. No surviving mutant in this assigned probe.
ExpectedPairs rewrite was exercised as the unchanged-guard negative control; this does not claim both guards were disabled. No separate frozen/expected.json rewrite was added or claimed.
Contract C2's broad tamper wording names snapshot_tampered; the actual declaration/oracle rewrite finding is frozen_input_changed, as the existing real selftest expects. Outputs were not renamed or expectations weakened.
No C1 conclusion, source-semantic verdict, admission, integration, or shipping claim follows from this one killed mutant.
Tools used: existing Python 3.14.8 and bubblewrap 0.13.1; no installs/updates. No build/lint/formatter, network access, another runtime, or live source/docs/registry mutation.
