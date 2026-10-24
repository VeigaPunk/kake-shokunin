# W1 ReviewC1ProbeCode — attack on `.ufo/waves/round-32/c1_m3_probe.py`

Sandbox: `/fast/scratch/hyaku/kake-r32/w1/ReviewC1ProbeCode/` (clone of the lane, all runs there,
`TMPDIR` set to sandbox `tmp/`). Probe file unchanged 5b32cc7→96d49d6 (`git diff` empty), so all
findings apply to current HEAD. No tools installed.

## Verdict
Core counting is correct: the probe reproduces both committed receipts exactly and its three runs
are all pinned to the `git archive` export. Three low-severity defects found; none flips the
declared C1 result at the pinned revs.

## Reproduction (all exit 0, ~6 s total)
- `python3 -B clone/.ufo/waves/round-32/c1_m3_probe.py --rev 2f2f12deb0fe… --repo clone`
  → killed 1, guard_ok true, pristine 0, mutant 1 (P1–P5 true, P6 false only), benign 45/0 failed,
  runnerSha256 `7c95a18e4621…` — field-identical to `verification/c1-after-2f2f12d.json`.
- `… --rev a0b0dffcd95b…` → killed 0, guard_ok true, mutant P1–P5 true — matches
  `verification/c1-before-a0b0dff.json`.
- runnerSha256 equals `git show <rev>:scripts/citing_set_selftest.py | sha256sum` at both revs
  (runner identical a0b0dff→2f2f12d). No `.gitattributes` tracked at 5b32cc7 → no export-ignore
  risk. Benign count at rev: 45 case dirs. `GUARD.subn` = 1 at rev; `n != 1` exits 2 (fail-closed).
  Mutant source compiles (`compile()` OK) → no crash-kill path at this rev.

## Findings (by severity)

### F1 — LOW: docstring says "a kill only counts with guard_ok true"; code never gates
`c1_m3_probe.py` docstring (~line 19) vs `out["killed"] = 1 if m_exit == 1 else 0` (~line 100):
`killed` is computed unconditionally. Synthetic repro in my sandbox clone (rev `35433163f4aa`,
NOT a lane rev; built by corrupting `scripts/fixtures/citing-set/01-single-literal-clean/expected.json`
on top of 2f2f12d so the benign run fails):
`python3 -B clone/.ufo/waves/round-32/c1_m3_probe.py --rev HEAD --repo clone` → exit 0,
`killed: 1, guard_ok: False` (pristine 1, benign exit 1 / 1 failed). A consumer reading `killed`
alone would overclaim. Receipts unaffected: both have guard_ok true. Fix: `killed = 1 if (m_exit == 1 and guard_ok) else 0`.

### F2 — LOW: error paths escape the documented exit contract (0 or 2)
`run()` does not catch `subprocess.TimeoutExpired`: demo
`m.run(['sleep','5'], timeout=1)` (module imported from the probe) → TimeoutExpired escapes →
traceback, exit 1. Same for `git archive … check=True` (CalledProcessError) and tar extract errors
on a bad export — documented as "could not run" → exit 2, actually crash exit 1. Rev resolution
alone is handled (exit 2, verified by code read). Practical impact small (900 s timeout, local
archive); a hang mid-round yields a misleading traceback instead of a JSON object with exit 2.

### F3 — LOW (latent, not live at pinned revs): `killed=1` means only "mutant run exited 1"
Hostile harness exit 1 also covers non-target failures:
- broken runner: `python3 -B clone/scripts/citing_set_hostile_selftest.py --root clone --tmpdir
  tmp/a2 --runner /bin/true` → exit 1, all six specs false (a2.json);
- harness infra error: `… --tmpdir "$PWD/tmp/a1file"` (tmpdir exists as file) → uncaught
  traceback, exit 1 (a1.err).
So a crashing mutant, or an infra failure confined to the mutant run (e.g. disk full), scores
killed=1. Not live for m3 here: mutation is surgical (subn==1 enforced; mutant compiles; receipts
show P1–P5 still pass under the mutant, so the mutant runner ran normally). Stricter counter could
require exactly P6 false and `compile()` the mutant.

### F4 — NOTE (confirmed correct, mechanism attribution): the m3 kill is a reason differential
Extracted by running the hostile harness directly on a 2f2f12d export
(`git archive 2f2f12d | tar -x -C exp-2f2f12d`) with the m3 runner vs its own runner:
- mutant P6: passed False, runner exit 1, reasons `{"h6": "case setup failed: git_commit needs the
  repository created by git_init"}` (execution-time check, runner ~line 490), reasonChecks false;
- pristine P6: passed True, reasons `{"h6": "case.json setup op 'git_commit' needs an earlier
  'git_init'"}` (load guard), reasonChecks true.
So with the guard deleted, h6 is still refused — by the later execution-time check — and it is
P6's `reason_contains` that makes pristine/mutant observably differ. The probe answers its question
truthfully; claim wording should not imply h6 would go undetected without the guard. This matches
the wave-1 docstring repair (df31d30 "runner docstring names P6/m3 layer probe").

## Verified clean
- All three probe runs execute only against the export: hostile loads specs from
  `<export>/scripts/fixtures/citing-set-hostile` (SPEC_DIR), benign from
  `<export>/scripts/fixtures/citing-set`; `--runner` mutant is the surgically edited export source.
- guard_ok inputs sound: runner EXIT_OK=0 only with zero failures (runner lines 129–131, 740–756);
  hostile exits 0 iff every spec passed, 2 on load errors (hostile ~line 245, 233–237).
- CASE_KEYS includes `reason_contains` from 2f2f12d on (line 84); P6 is the only reason-gated spec
  (P1–P5 specs have no `reason_contains`).
- Receipt revs resolve; probe JSON schema/fields match receipts field-for-field.

## Residual risk / not verified
- Did not run or audit the C2 counter (out of scope); did not audit P1–P5 spec internals.
- Timeout path shown at unit level only; no >900 s full-probe hang test.
- F1's synthetic rev exists only in my sandbox clone, never in the lane.
- Lane moved during review (HEAD now 96d49d6 with wave-1 repairs); probe unchanged, re-run at HEAD
  not done (findings are code-level, file identical).
