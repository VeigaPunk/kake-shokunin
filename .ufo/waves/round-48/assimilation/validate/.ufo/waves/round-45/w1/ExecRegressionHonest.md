# C1 honest-cohort regression — driver v2

Axes: operability and freshness.

## Result

**Blocked at the stated prerequisite; regression not run.** The assigned driver path `.ufo/waves/round-45/c45_audit.py` was absent at inspection. The round-45 directory listing contained `w1-taskcall.json`, `w1-run.stderr`, `w1-plan.json`, `w1-plan.stderr`, `w1-spec.json`, `make_w1_spec.py`, and `w1/`, but not `c45_audit.py`. Per the assignment, I did not wait for another seat or substitute another driver.

Requested command (not executed):

```text
python3 -B .ufo/waves/round-45/c45_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --workers 4 --out .ufo/waves/round-45/verification/honest-regression/after-v5-v2.json
```

**AUDIT line:** none; no audit ran. **Exit code:** N/A (not run). The requested text table was not generated. Decisive prerequisite evidence:

```text
Path '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_audit.py' not found.
```

## Frozen v1 comparison reference

Read-only receipt `.ufo/waves/round-44/verification/claim/after-final/after-v5.json` reports:

- `witnessed`: 27
- Build runs 1–3: each `exit: 0`, `met: true` (3/3)
- `counterSha256`: `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc`
- `ok`: true
- `verdict`: `witnessed 27/27 notMet=27 build met 3/3`

No v2 receipt exists from this attempt, so v2 summary fields/counter SHA could not be diffed against v1. Kill rule 4 is **not evaluated** (neither a pass nor a divergence failure); rerun requires the assigned v2 driver artifact.

## Files written

- `.ufo/waves/round-45/w1/ExecRegressionHonest.md` — this report.

No tools were installed. The requested audit and its text-table capture remain unrun.