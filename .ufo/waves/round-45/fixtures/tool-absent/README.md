# tool-absent fixture

`ctl1.py` is a byte copy of `.ufo/waves/round-44/controls-r43/headtail-V1-prefix-cache64.py`; `controls.tsv` carries the committed source SHA-256 and one G5 row.

The control receipt starts from `control-template.json`, a byte-for-byte copy of `.ufo/waves/round-44/verification/claim/after-final/tools/headtail-V1.json`.

For the synthetic missing-tool result, these top-level fields remain copied from that receipt: `predicate`, `ratioLimit`, `reps`, `revision`, `label`, `seed`, `ref41Sha256`, `base40Sha256`, and `classesMode`; its `classRuns` list is retained. The fake counter sets `counterSha256` to its own file hash, `toolFile` to the invoked control path, `toolSha256` to null, `met` to false, `equalRuns` to `0/21`, `equalValues` to zero, `note` to `tool absent`, `ratios` to five null timing ratios, and `ratiosExact` to an empty object.

The `runs` map and all run keys are copied. For each run the template's `values`, `ref41Exit`, and `ref41OutSha256` remain; `equal` becomes false, `candExit` becomes `tool absent`, and `candOutSha256` is removed. Timing runs retain the copied `base40Cpu`, but get empty `candCpu` and `candRepsEqual=0/5`. Therefore `caughtBy` is not a raw receipt field: `c44_audit.py` derives it from the false run equalities and the fake counter's ten v5 class keys.

For build invocations, `build-receipt.json` is copied byte-for-byte from `.ufo/waves/round-44/verification/claim/after-final/build-1.json`; every build receipt field is unmodified real-counter output, and the fake exits 0. The control invocation writes the synthetic receipt and exits 1.
