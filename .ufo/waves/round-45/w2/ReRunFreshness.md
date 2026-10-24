# ReRunFreshness — C2 receipt re-run

Axis attacked: **freshness**.

## Result

**PASS for the three named measurements.** I ran the unchanged `c45_freshness.py` and its copied inputs in the required scratch directory so the run would not write outside my report in the lane. It returned exit 0 and produced the requested tuple. The scratch receipt was refreshed.

The canonical lane receipt was read before and after this scratch run. Its `ran_at_ns` changed from `1792813373796121529` to `1792814215829301560`; the post-run receipt has the same expected three measurements. I did not run the script against the lane or write that receipt, so I cannot attribute that canonical timestamp change to my invocation.

## Command and decisive output

Working directory: `/fast/scratch/hyaku/kake-r45/ReRunFreshness`

```sh
python3 -B .ufo/waves/round-45/c45_freshness.py
```

Verbatim stdout; process exit status 0:

```text
selftest_kills before=2/4 after=4/4
v4_predicate_names_class_runs before=true after=false
witness_split class_only=26 mixed=1 met=0
FRESHNESS_RAN_OK
```

The generated scratch `verification/freshness/freshness.json` records `selftest_kills={before:2,after:4,of:4}`, predicate `{before:true,after:false}`, and split `{class_only:26,mixed:1,met:0}`.

## Files written

Lane:
- `.ufo/waves/round-45/w2/ReRunFreshness.md` (this report; only lane file written by this seat)

Scratch copies and generated receipt under `/fast/scratch/hyaku/kake-r45/ReRunFreshness/`:
- `.ufo/waves/round-45/c45_freshness.py`
- `.ufo/waves/round-45/mutants/m1.py`, `m2.py`, `m3.py`, `m4.py`
- `.ufo/waves/round-45/mutants/m1_v2.py`, `m2_v2.py`, `m3_v2.py`, `m4_v2.py`
- `.ufo/waves/round-45/verification/v6v4/counter-v4.json`
- `.ufo/waves/round-45/verification/freshness/freshness.json` (generated)
- `.ufo/waves/round-44/verification/claim/v4-final/v4.json`
- `.ufo/waves/round-44/verification/claim/after-final/after-v5.json`

Tools installed or updated: none (`jq` was already available).

## Risk / limitation

The actual lane invocation is intentionally not claimed: `c45_freshness.py` writes its receipt into the lane, while this seat's lane write bound permits only its report. The canonical receipt's post-run contents and changed timestamp were observed, but the writer/invocation is unknown to this seat.
