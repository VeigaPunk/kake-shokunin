# counter-error fixture

`ctl1.py` is a byte copy of `.ufo/waves/round-44/controls-r43/headtail-V1-prefix-cache64.py`; `controls.tsv` carries the committed source SHA-256 and one G5 row.

`control-receipt.json` is copied byte-for-byte from `.ufo/waves/round-44/verification/claim/after-final/tools/headtail-V1.json`. The fake counter copies it unchanged to the requested receipt path and exits 2. Thus every top-level field (`predicate`, `met`, `ratioLimit`, `reps`, `revision`, `toolFile`, `label`, `seed`, `counterSha256`, `ref41Sha256`, `base40Sha256`, `classesMode`, `classRuns`, `toolSha256`, `equalRuns`, `equalValues`, `runs`, `ratios`, `ratiosExact`, `note`) and every nested run/ratio value has the committed frozen-counter receipt's provenance; none is synthesized or edited. The raw receipt has no `caughtBy` field: frozen `c44_audit.py` derives the summary's `caughtBy` from false `runs[*].equal` keys and `CLASS_MODULES`.

For the three build invocations, `build-receipt.json` is copied byte-for-byte from `.ufo/waves/round-44/verification/claim/after-final/build-1.json`; every receipt field is unchanged and real-counter sourced. The fake exits 0 for these build invocations so the fixture isolates the control-call exit-code defect.
