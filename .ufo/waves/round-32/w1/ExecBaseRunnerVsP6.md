# KakeR32.ExecBaseRunnerVsP6 — P6 spec vs older runners (wave 1, operability)

Target: does the new P6 spec discriminate by the load-time guard, or merely track a runner revision?
Advisory input for the L1, not a judgment on the round.

## Setup

Sandbox `/fast/scratch/hyaku/kake-r32/w1/ExecBaseRunnerVsP6/` (clone/, tmp/, runners), TMPDIR
exported there. No installs, no pacman transactions. Lane untouched except this report file.
Runners exported read-only via `git show <rev>:scripts/citing_set_selftest.py`; sha256: pre-repair
`f1ffb81738c92c0537b99b30970143ab9419f990` = `9f2d1ecb…e14d3`; base `a0b0dffcd95b2215f638a5ff7591dd4fde325d27`
and tip `285abcad632e3c1c57bb402232e7d218054db383` = `7c95a18e…8b8969` (base and tip are byte-identical).

## Commands and exit codes

Hostile selftest (all runs): `python3 -B clone/scripts/citing_set_hostile_selftest.py --root <root> --tmpdir <tmp> --runner <r>`.

1. `git clone -q <lane> clone` ; `git -C clone checkout -q 285abcad...` — exit 0, HEAD 285abca.
2. Base runner, full tip spec set (`--root clone --tmpdir tmp/run-base --runner runner_a0b0dff.py`) — **exit 0**.
3. Pre-repair runner, full tip spec set (`--runner runner_f1ffb817.py`) — **exit 1** (90 s; P4 hits RUN_TIMEOUT).
4. P6 only (`root_p6only` = tip clone copy holding only P6-commit-before-init): pre-repair runner **exit 1**; base runner **exit 0** (run 2's P6 row).
5. P6 only, mutant m3 = base runner minus the 2 load-time guard lines (`runner_mutant_m3.py`, sha256 `c4cacd0d…7320`) — **exit 1**; full tip spec set under m3 — **exit 1**, only P6 fails.
6. Isolation: pre-repair runner + **only** the load-time guard added (`runner_pre_plus_guard.py`, sha256 `c195a069…62a5`), P6 only — **exit 0**.
7. P6 with `reason_contains` deleted from the spec (`root_p6_norc`): base runner **exit 0**, mutant m3 **exit 0**.
8. Benign fixtures on base runner: `python3 -B clone/scripts/citing_set_selftest.py --root root_p6only --fixtures root_p6only/scripts/fixtures/citing-set --tmpdir tmp/benign --timeout 60` — **exit 0**, cases 45, failed 0, meetsContractMinimum true.

## Per-spec results, full tip spec set

| spec | base a0b0dff (== tip) | pre-repair f1ffb817 |
|---|---|---|
| P1-selftest-argv | PASS (exit 1, canary false) | FAIL (exit 1, **canary true**) |
| P2-fixture-dot-git | PASS (exit 1, victim unchanged) | FAIL (exit 0, **victim mutated**) |
| P3-commit-without-init | PASS (exit 1, victim unchanged) | FAIL (exit 0, **victim mutated**) |
| P4-expected-json-guard | PASS (exit 1) | FAIL (exit None, **timed out**) |
| P5-symlinked-case | PASS (exit 1) | FAIL (exit 0) |
| P6-commit-before-init | **PASS** (exit 1, h6 reason "case.json setup op 'git_commit' needs an earlier 'git_init'", reasonChecks h6 true) | **FAIL** (exit 0, reasons {}, **victim mutated**, reasonChecks h6 false) |

Acceptance met: P6 fails on the pre-repair runner and passes on the base runner. The base runner
also leaves the 45 benign fixtures clean (run 8).

## The surprise: the pre-repair runner does not refuse P6 — it accepts it and writes to the victim

P6 failing there is **not** a refusal-with-different-wording: that runner has no load-time guard
*and* no apply-time re-check, so it **runs the hostile setup**. Replaying P6 by hand against
`runner_f1ffb817.py` (exit 0, `verdict clean`, `passed true`, rows `00-benign`/`h0-control`/`h6` all
`ok true`, `failures []`) shows case h6 counted as a **passing** case. The victim's HEAD moved
`5c245630…f0fedc` → `6899f53b…82e7` ("probe") and its tree then listed
`tmp/citing-set-selftest/cases/h6/case.json` etc.: the pre-repair runner sets neither
`GIT_CEILING_DIRECTORIES` nor a pinned `--git-dir`/`--work-tree`, so `git add -A` + `git commit`
walked up into the victim repository and committed there. Same mechanism behind P2/P3 (victim
mutated) and P1 (canary true: the planted script ran). P6's failure signal there is `exit 0` +
`victimUnchanged false`, not a wrong reason string.

## Isolation: the load-time guard alone is what P6 pins

- Pre-repair runner + only the load-time guard → P6 **PASSES** (exit 0, reason "case.json setup op
  'git_commit' needs an earlier 'git_init'", victimUnchanged true); the victim no longer mutates.
- Base runner minus the load-time guard (mutant m3) → P6 **FAILS** (exit 1), h6 reason "case setup
  failed: git_commit needs the repository created by git_init" — the apply-time re-check refuses it,
  but with different wording. Full suite under m3: P1–P5 pass, only P6 fails (matches the L1
  receipt `.ufo/waves/round-32/verification/c1-after-2f2f12d.json`).
- Deleting `reason_contains` from the P6 spec makes **both** base and mutant m3 pass P6 (run 7):
  the new spec key is load-bearing for the m3 kill, since refusal by the apply-time layer is not
  enough — only the load-time layer's wording counts.

## Evidence pointers

- P6 spec `scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json`; load-time guard
  base runner `scripts/citing_set_selftest.py` lines 362–363, absent in `f1ffb817` (its
  `load_case_setup` ends at the `mkdir`/`fifo` path checks); apply-time re-check base lines 488–490;
  hostile selftest `scripts/citing_set_hostile_selftest.py` (`reason_contains` in CASE_KEYS, line ~86).
- Hardening absent from `f1ffb817`: base `git_env` sets `GIT_CEILING_DIRECTORIES`; `git_command`
  pins `--git-dir=`/`--work-tree=`. Round-31 container work `f1ffb817` predates: `c88b97e`, `9a7f5be`.

## Risks / not verified

- P6 cannot distinguish the load-time guard from the apply-time re-check by shape alone; only the
  `reason_contains` wording does. A reworded load-time message would fail P6 on a correct runner.
- P6 on the pre-repair runner fails via victim mutation, so it detects the whole round-31
  containment layer; the mutant-m3 row is the P6-specific signal.
- I did not re-run the L1's `c1_m3_probe.py` counter itself; I reproduced its mutant logic directly
  in the sandbox and got the same P1–P5 pass / P6 fail split. No live web properties contacted;
  nothing outside the lane working tree written. Tooling: none installed or updated.
