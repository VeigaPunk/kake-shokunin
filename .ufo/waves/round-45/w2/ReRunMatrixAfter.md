# C1 after-receipt matrix rerun

Axes: operability (primary) and freshness of the generated evidence.

## Attack and result

Re-ran the named `after` matrix against an isolated scratch copy of its required inputs so the lane remained read-only. The scratch root was `/fast/scratch/hyaku/kake-r45/ReRunMatrixAfter`; it used the current round-45 drivers, round-44 counter/audit, fixtures, controls and class modules, retained round-41 real-run data, plus a read-only `.git` symlink for the counter's frozen-revision reads.

Command (working directory: `/fast/scratch/hyaku/kake-r45/ReRunMatrixAfter`):

```text
python3 -B .ufo/waves/round-45/c45_matrix.py --stage after
```

Verbatim command output:

```text
stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3
MATRIX_AFTER_PASS
```

The command returned exit 0 (tool-reported elapsed time: 221.16 s). **PASS** against the named attack: all requested after-stage measurements matched. The fresh scratch receipt records `invalid_accepted=0`, `rejections_named=3`, `named_classes=["counter_error", "stale_receipt", "tool_absent"]`, `honest_witnessed=27`, and `honest_build_met=3`. Each fixture rejected (`exit=1`, `ok=false`) with its respective named class. The honest leg records `exit=0`, `valid=true`, no problems, 27 witnessed, and 3/3 builds met. The copied driver SHA-256 is `f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076`; receipt `ran_at_ns=1792814493861754957`.

Additional retained evidence: the honest summary at `verification/honest-regression/after-v5-v2.json` has `ok=true` and verdict `witnessed 27/27 notMet=27 build met 3/3`.

## Files and scope

- Repository file written: `.ufo/waves/round-45/w2/ReRunMatrixAfter.md` (this report), the only lane file written.
- Scratch inputs copied under `/fast/scratch/hyaku/kake-r45/ReRunMatrixAfter`: `.ufo/waves/round-45/{c45_matrix.py,c45_audit.py,fixtures/**}`, `.ufo/waves/round-44/{c44_audit.py,c44_count_v5.py,controls-27.tsv,classes/*.py,controls-r43/*.py}`, and `.ufo/waves/round-41/realrun/**`. `.git` is a symlink to the lane's repository metadata, used for read-only `git show` lookups.
- Matrix-generated scratch outputs: `.ufo/waves/round-45/verification/matrix/after.json`; `.ufo/waves/round-45/verification/honest-regression/after-v5-v2.json`; honest cohort `runs/after/honest-cd6092296bd6/{after-v5-v2.json,build-1.json,build-2.json,build-3.json,run-manifest.json,tools/*.json}`; and fixture cohorts `runs/after/{counter-error-89a7ada4b647,tool-absent-f8ce74e3ba0d,stale-planted-ea98cbf7c8a5}/` with their generated summary, manifest, build and tool receipts.

No lane evidence was rewritten, no tool was installed, and no unrun portion remains.