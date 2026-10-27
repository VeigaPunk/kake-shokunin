# Calibration axis floor check

## Observed

- `SCORECARD.md` lines 3–7 says kake owns **operability + freshness**, with **calibration** added as an evidence-backed sub-axis; depth/coverage/adjacency are outside scored ownership.
- Axis table lines 15–19 gives scores operability 10, freshness 10, calibration 2. Thus calibration is uniquely lowest among the three owned axes (2 < 10); no tie or inference about non-owned axes is needed.
- `SCORECARD.md` lines 103–115 has a `Retired` section. Its visible retired item is the free-read-verb audit sub-surface; line 114 explicitly says the two original owned axes are not retired. No evidence in the inspected axis declarations or retirement passage indicates calibration itself is retired.
- The SCORECARD round-59 history says C1 works calibration as the lowest-scoring non-retired axis (lines 4420–4424); round-60 says the same (4490–4492); round-61 records calibration C1 and its failed distinctness/control result (4505–4513). These are consistent with the axis table and show the calibration workstream has not been labeled retired in these records.
- Frozen round-62 contract `.ufo/waves/round-62/contract.md` lines 5–7 explicitly targets “calibration (lowest owned non-retired axis; score 2)” and the C1 claim addresses the round-61 S432 disagreement through a quality gate and citation correction. It therefore targets the independently verified lowest owned non-retired axis.

## Commands / evidence

- `read /home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md:1-23` — axis ownership and scores.
- `grep` for `calibration|retired|Planned` in SCORECARD found the explicit round-59/60/61 calibration targeting/history; the retirement-specific section was read at SCORECARD lines 103–115.
- `read /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/contract.md:1-12` — frozen C1 axis and claim.

## Judgment / bounds

**Pass, high confidence:** calibration is owned, score 2 versus 10/10 for the other owned axes, and not shown as retired; the claim targets it. This is an axis/status check only. No claim/counter/criterion/score or lane source was changed, and no counter was run. I did not establish live external axis status beyond the inspected SCORECARD history.