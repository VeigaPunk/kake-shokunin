# ReviewCounterCode — c42_count.py review (wave 1, operability)

Scope: full read of `.ufo/waves/round-42/c42_count.py` (616 ln, sha256 `7bfc32c5e76d…dd2a6` — matches SCORECARD),
docstring vs code, SCORECARD §"Round 42 — C1 counter candidate", plus the two sanctioned runs. No tool installs.

## Commands (exact, with exit codes)
- `sha256sum .ufo/waves/round-42/c42_count.py /fast/scratch/hyaku/kake-r42/shared/{tip41,base40}.py`
  → `7bfc32c5…`, `50287ac6…`, `4de35f8c…` — all three identities match the declared ones. exit 0.
- `timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-42/c42_count.py --root <repo> --tool-file
  /fast/scratch/hyaku/kake-r42/shared/tip41.py --label ReviewCounterCode-tip41 --seed 42901
  --out /fast/scratch/hyaku/kake-r42w1/ReviewCounterCode/tip41-42901.json` → **exit 1** (163 s wall for both runs).
- Same with `base40.py`, label `ReviewCounterCode-base40`, same seed → **exit 1**.
- Read `verification/pre/donothing-tip-42001.json` (L1 receipt cross-check).

## Counter results for every tool I scored
- tip41 (`50287ac6…`): equalRuns **8/8**, equalValues 3290, ratios T1 5.563, T2 2.808, T3 1.333, T4 1.217,
  T5 10.147 → **not met** (receipt `…/ReviewCounterCode/tip41-42901.json`). Same band as SCORECARD seeds
  42001/42002 (T1 5.35–5.37, T5 8.87–9.35; T5 10.147 slightly above both recorded seeds, same shape).
- base40 (`4de35f8c…`): equalRuns **3/8**, ratios 0.963–1.019 → **not met** (its own noise band; SCORECARD band
  0.968–1.054). Receipt `…/ReviewCounterCode/base40-42901.json`.
- Both runs same seed → identical ref41 output hashes per run key (A `2618fed5…`, B `89be58f5…`, C `d1318f86…`):
  generation is seed-deterministic.

## Findings by severity
1. **LOW — receipt-void path with wrong exit code** (`c42_count.py:508-515`, `:606-612`): `finish()` writes
   `--out` unguarded. If `open(a.out)` raises (bad dir/permissions), the call at `:612` is outside the try →
   unhandled exception, process exit 1 ("not met") with **no receipt**; same from the except-handler calls at
   `:609`/`:611`. Violates docstring line 6 "a receipt is written in every case" and the exit-2 contract.
   Reachable only with an unwritable `--out` path; every evaluation outcome itself does write a receipt.
2. **LOW — ratio rounding at the limit** (`:594`, `:603`): ratio rounded to 3 decimals *before* the `<= 2.0`
   test; a true ratio in (2.0, 2.0005] is recorded as 2.0 and passes. ≤0.05% effect; decision-relevant only for
   a candidate sitting exactly on the limit. Unrounded medians are in the receipt (`base40Cpu`/`candCpu`), so the
   L1 can recompute — no silent distortion.
3. **LOW (fairness note)** (`:578-579`): alternating order starts with base40 in reps 0/2/4 — cold-cache cost
   lands on base40 slightly more often. One warm-up per rep, far below the observed 0.96–10.1 ratio spread; no
   action.
4. **THEORETICAL — stdout beyond 256 MiB never compared** (`:474`, `:65`, `:447-448`): equality compares at most
   OUT_CAP bytes; a writer exceeding the cap dies by SIGXFSZ. If both tools exceeded it on an equality run,
   equal signal exits + equal truncated prefixes could fake an "equal". Unreachable with these tools/shapes
   (outputs are audit reports), and timing ratios still gate `met`. No code change needed; documenting the bound.

## Statement verdicts (docstring + SCORECARD)
- Predicate text = `PREDICATE` constant `:52-54` = SCORECARD sentence: **holds**.
- Exit codes 0/1/2: **holds** (`:606-612`).
- "a receipt is written in every case": **overstated** — true for all evaluation outcomes, false under `--out`
  write failure (finding 1).
- Equality = exit code + full stdout bytes, first run and all 5 timing reps: **holds** (`:570-571`, `:585-586`,
  `:590`); receipts carry per-run output hashes and CPU samples.
- `met` ⟺ 8/8 equal ∧ 5 ratios present ∧ all ≤ 2.0: **holds** (`:603-604`); missing timing line, timeout, absent
  candidate, zero base40 median all yield no ratio → **not met** (`:466-469`, `:479-486`, `:572-574`, `:591-596`).
  **No path found where a failure becomes `met`.**
- CPU = user+system of tool and every descendant via child-subreaper runner reaping orphans before the last
  timing line: **holds** (RUNNER `:413-425`: subreaper `:415`, reap loop `:418-422`, RUSAGE_CHILDREN `:423`,
  write-after-reap `:424`). Last-line-wins read (`:480-486`) defeats any tool-side timing-file prepending
  (tool fd closed `:416`; timing file outside the sandbox binds); a killed runner leaves cpu None → not met.
  Fails safe.
- "caching by value cannot help": **holds** (random token heads every value); cross-rep caching is impossible —
  case dir is read-only inside the sandbox (`:456` `--ro-bind cd work`), `/tmp` tmpfs is fresh per bwrap call
  (`:455`), each rep a new sandbox. Label/seed/id/name keying: label recorded only, all sandbox names random
  (`:440-445`, `:554`). Realrun copied into the case dir and verified (`:393-406`), not read from inside.
  I found **no seam** for the SCORECARD measurement-skip classes in these bytes.
- Sandbox claims (absolute bwrap, OSError→exit 2 `:471-472`,`:518-519`; stdin /dev/null; stderr discarded;
  RLIMIT_FSIZE 256 MiB; AS 4 GiB `:447-448`; bwrap env PATH only `:464`; LANG inside `:459`; 600 s timeout
  `:64`,`:466-469`; SHA256SUMS-verified T4): **holds**.
- Shape/size claims (A 1434 = 6×(99+6) + 6×(128+6); B 1200; C 600+40+16; T1/T2 20,000; T3 50,000; T5 48 checks,
  40 defects, window 64): **holds** — my `equalValues` 3290 matches; `candRepsEqual`, `base40Cpu`, `candCpu`
  present per timing run.
- Do-nothing reproduction (tip41 8/8 not met, high T1/T5; base40 3/8, noise-band ratios): **holds** on seed 42901.

## Residual risk / verification gaps
- Measurement-skip resistance is verified by code reading plus two sanctioned runs only; I did not execute
  control/mutant tools against the counter (out of my sanctioned run set).
- The bwrap fd-passing chain (pass_fds → runner) confirmed only empirically (both runs produced timing lines).
- Findings 1, 2, 4 are unexercised; severity judged from code paths.
- Note for the freeze: exit codes 2 on equality runs A/B are the tools' own behaviour (candExit == ref41Exit == 2
  in every receipt), not a counter artifact.
