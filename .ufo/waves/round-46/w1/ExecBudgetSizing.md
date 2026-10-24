# ExecBudgetSizing — C1 matrix wall-clock sizing

**Axis:** operability. **Result against the named <120 s after-stage budget: FAIL / unmeasurable.** The required runner and inputs were absent; the failed launch is not a matrix timing. No valid C46 recipe or shrink/re-measure was established.

## Decisive command evidence

Revision used: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD` → `ded938d2f23aba265d1acf1fdd4b3ab028020037`.

First wrapper attempt:

```text
$ /usr/bin/time -f 'wall_s=%e exit=%x' python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision ded938d2f23aba265d1acf1fdd4b3ab028020037 --stage after
error: command not found: /usr/bin/time
Command exited with code 127
```

After switching to shell `time`, the requested after-stage shape was attempted once:

```text
$ TIMEFORMAT='wall_s=%3R'; time python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision ded938d2f23aba265d1acf1fdd4b3ab028020037 --stage after
python3: can't open file '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/c46_matrix.py': [Errno 2] No such file or directory

real	0m0.006s
user	0m0.007s
sys	0m0.003s

Command exited with code 2
```

`real 0.006s` is a missing-file failure, not an observed matrix wall time. At inspection, `scripts/redirect_audit.py`, `.ufo/waves/round-46/fixtures/`, `.ufo/waves/round-46/controls/`, and the C46 fixture-design artifact were also absent. Per the independent-seat instruction I did not wait for another seat.

Prior, non-C46 evidence only: `.ufo/waves/round-45/w2/AttackHonestIdentity.md:56-61` records `stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3`, `MATRIX_AFTER_PASS`, and `real 3m40.661s` (220.661 s). It shows a previous C45 honest-cohort run over budget, but is not a C46 measurement.

A contingency proposal is recorded in `.ufo/waves/round-46/build/budget-sizing.md`: first time the complete C46 witness/control population; if a valid run is ≥120 s, try one minimal row per distinct witness class (design target 14–18 classes), retain all three controls, and run independent rows with four workers, then remeasure. This is not validated; current evidence does not show parallel-row support.

## Files written

- `.ufo/waves/round-46/build/budget-sizing.md`
- `.ufo/waves/round-46/w1/ExecBudgetSizing.md`

No tools were installed. No tests/builds/linters were run; the only execution was the explicitly requested timed matrix launch, which failed at file-open.
