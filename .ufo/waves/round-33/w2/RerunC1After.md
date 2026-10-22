# Wave-2 report — KakeR33.RerunC1After (falsify, C1 after-measurement re-run)

Seat: leaf. Axis: operability. Scope: re-run `.ufo/waves/round-33/c1_code_probe.py`
at four revs in my own clone, compare with L1 receipts, probe the counter's
mutation mechanics for overstatement. No finding that overturns C1; the claim
reproduces exactly.

## Setup

- Clone: `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r33/w2/RerunC1After/clone`; `checkout -q 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` (exit 0).
- `TMPDIR=/fast/scratch/hyaku/kake-r33/w2/RerunC1After/tmp`; `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset for all git/python runs.
- Command shape per rev `r`: `python3 -B .ufo/waves/round-33/c1_code_probe.py --repo <clone> --rev <r>`.

## Observed results (my runs)

| rev | exit | met/of | guard_ok | pristine | reworded | m3 | recoded |
|---|---|---|---|---|---|---|---|
| b1752a2480aa86fc27536dd6e7d27a91b52bed12 | 0 | 4/4 | true | 0/[] | 0/[] | 1/[P6] | 1/[P6] |
| e4903817669aa411e424006bb342b345e143ab20 | 0 | 4/4 | true | 0/[] | 0/[] | 1/[P6] | 1/[P6] |
| 1cf452eafb028785ce9fa154887178864e22ab71 | 0 | 4/4 | true | 0/[] | 0/[] | 1/[P6] | 1/[P6] |
| 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0 | 0 | 4/4 | true | 0/[] | 0/[] | 1/[P6] | 1/[P6] |

(`0/[]` = exit 0, no failing specs; `1/[P6]` = exit 1 failing only
`P6-commit-before-init`. `guardMatches` = 1 and benign 45 cases/0 failed at all revs.)

Per-variant sha256s reproduced identically (e.g. at e490381+: pristine
`88b47f6b…`, reworded `3596d20b…`, m3 `4c8a35fb…`, recoded `b1ce11b5…`).

## Diff vs receipts

- `c1-after-b1752a2.json`, `c1-at-e490381.json`, `c1-at-1cf452e.json`: every
  field compared — rev, runnerSha256, hostileSha256, guardMatches, benign,
  guard_ok, per-variant applicable/sha256/exit/specs/failing, expectations,
  met — identical. No differences.
- `0a0acfb` has no named receipt; its output is field-identical to
  `c1-at-1cf452e.json` (expected: tip only changes SCORECARD/LOG).
- Extra (out of scope, cheap): `--rev 5777d5af79cac1ebf9144b348a9d274099e77338`
  → exit 0, met 2/4, guard_ok true; pristine 0/[], reworded 1/[P6],
  m3 1/[P6], recoded not applicable. Matches `c1-before-5777d5a.json`'s
  declared before-contrast ("Before at base: met 2").

## Mutation-mechanics check (does the counter measure what it claims?)

- Guard is the declared two-line shape: `scripts/citing_set_selftest.py:401-402`
  `if step["op"] == "git_commit" and not initialized:` then one `raise` line
  carrying `"setup_commit_before_init"` and `needs an earlier 'git_init'`.
  Apply-time re-check at `:528-529` carries `"setup_commit_without_repo"`.
- P6 spec `scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json:23`
  carries `reason_code` and NO `reason_contains`; `codeChecks` is ANDed into
  `passed` at `citing_set_hostile_selftest.py:228-232`. So P6 keys on the
  structured code, not message text — claim verified, not just reported.
- `reworded` passes ⇒ a changed message does not fail P6 (the code is what is
  checked). `recoded` fails P6 ⇒ the check compares the literal, not merely
  "some code present" or "a code-shaped field".
- Probe mutation is surgical: `replace_in_guard` (probe `:83-93`) edits only the
  raise line inside the single GUARD match; m3 deletes only the guard block.
  Confirmed empirically: m3/recoded fail ONLY P6, P1–P5 stay true.
- Receipt identity across revs is coherent: runner sha changes b1752a2
  (`ca814fd7…`) → e490381+ (`88b47f6b…`, the e490381 "runner repairs" commit);
  hostile sha changes e490381 (`c222f227…`) → 1cf452e+ (`70def109…`, the
  "hostile hardening" commit). No silent drift.

## Residual risk / not verified

- Probe exits 0 regardless of `met` (exit 2 only on error); consumers must read
  `met`/`guard_ok` from stdout JSON — receipts do this, so no defect in lane use.
- GUARD regex requires the raise-call to fit one line (probe `:51-53`); a
  refactor to a multi-line call makes the probe error out (safe-fail direction).
- Run once per rev; determinism supported by bit-identical agreement with the
  L1's earlier independent runs.
- Tooling: none installed (python3 + git already present); pacman untouched.
