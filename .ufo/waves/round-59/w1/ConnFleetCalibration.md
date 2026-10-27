# ConnFleetCalibration

LANES:
- kasegi-shokunin — 0 evidence cells, 0 dead pointers (no axis rows parsed).
- kengaku-shokunin — 21 evidence cells, 5 dead pointers.
- kumitate-shokunin — 2 evidence cells, 9 dead pointers.
- kotoba-shokunin — 2 evidence cells, 0 dead pointers.
- kagi-shokunin — 108 evidence cells, 18 dead pointers.
- kama-shokunin — 5 evidence cells, 1 dead pointer.

NOTE:
Counted first six sibling repos from MANIFEST roster order, excluding kake. Parsed committed `HEAD:SCORECARD.md` axis rows for operability/freshness/calibration and extracted pointers using `c59_axis_evidence.py:pointers()`. A pointer was dead when it used `/tmp/`, `~/`, or `/home/`, or its file portion failed `git -C <lane> cat-file -e HEAD:<path>`. No pointers/cells in rows absent from scorecards. Counts are dead pointer occurrences, including repetitions, rather than distinct paths. No tools installed.

VERDICT: Five sampled sibling lanes have 33 dead-pointer occurrences across 138 evidence cells; kasegi has no parsed axis rows.
