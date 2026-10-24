# C1 matrix wall-clock sizing

**Axis:** operability — after-stage wall time must be below 120 s while retaining every planted witness class and rejecting all three controls.

## Measurement

No valid C46 matrix wall time was obtained. The requested invocation was attempted once at revision `ded938d2f23aba265d1acf1fdd4b3ab028020037`:

```text
$ TIMEFORMAT='wall_s=%3R'; time python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision ded938d2f23aba265d1acf1fdd4b3ab028020037 --stage after
python3: can't open file '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/c46_matrix.py': [Errno 2] No such file or directory

real	0m0.006s
user	0m0.007s
sys	0m0.003s
```

The 0.006 s is only the failed file-open attempt, **not** matrix runtime. The `c46_matrix.py` runner, `scripts/redirect_audit.py`, fixture directory, and controls directory were absent when inspected. The fixture design artifact was also not present, so the final witness-class count and row shape could not be read. No shrink/re-measure was possible.

The first timing wrapper tried `/usr/bin/time` and failed before invoking Python (`error: command not found: /usr/bin/time`, exit 127); the second attempt above used the shell `time` and reached Python.

## Retained prior evidence (not a C46 measurement)

The existing C45 report records this after-stage run:

```text
$ cd /fast/scratch/hyaku/kake-r45/AttackHonestIdentity/root && time python3 -B .ufo/waves/round-45/c45_matrix.py --stage after
stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3
MATRIX_AFTER_PASS

real	3m40.661s
BASELINE_EXIT=0
```

Source: `.ufo/waves/round-45/w2/AttackHonestIdentity.md:56-61`. This is a prior C45 27-witness honest-cohort result (220.661 s), not evidence for C46's runner or fixtures.

## Recipe and disposition

**C46 final recipe: not established; item fails measurement acceptance because the runner and inputs are missing.** Do not treat the 0.006 s failed invocation as meeting the 120 s budget.

Once the dependencies land, first time the full published after-stage matrix with every witness class and do-nothing/constant/junk controls. If that valid run is at least 120 s, a candidate shrink is one minimal manifest row per distinct witness class (the design assignment targets 14–18 classes), retaining all three controls, and running independent rows with four workers; then re-time the complete counter and accept only if its receipt still shows every witness class caught, all controls rejected, and wall time below 120 s. This is a contingency proposal, not an applied or measured recipe; current evidence does not establish that the runner supports parallel rows.
