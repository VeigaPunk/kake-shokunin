# AttackNotMetGate — C1 not-met half, driver v2 (`c45_audit.py`)

Wave: round-45 wave 2 (falsify). Lane: kake-shokunin. Axes: **operability** (does the driver's
not-met certification actually gate on receipt validity?) and **freshness** (no change was made to
the mtime/sha freshness predicates; the attack probes whether their verdict can be laundered into a
not-met pass).

Target: `c45_audit.py` sha256 `f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076`
(20320 bytes). All work in `/fast/scratch/hyaku/kake-r45/AttackNotMetGate/`; the lane file was
never written.

## Attack

Claim under test: an invalid receipt cannot be credited as **not-met**. Build a mutant that lets an
invalid receipt count as not-met (`not_met_rows` skipping validity) and a fixture whose only row is
invalid; the mutant must certify `--expect not-met` while the honest driver refuses; then the shipped
`--selftest` must kill the mutant.

Fixture: one control (`ctl.py`), one counter that writes an otherwise fully honest receipt
(`counterSha256` = self-sha, `seed` = 1, `met:false`, `runs:{"D":{"equal":false}}`, fresh mtime) and
then exits **2**. That is exactly one invalidity: `receipt_validity` → `(False, "counter_error")`.
`--expect not-met` over one row.

Two mutants were built from byte-identical pristine bytes:

- **M1 (named single-point weakening):** `not_met_rows` drops the `row_valid(row)` filter.
- **M2 (coherent not-met-trust weakening, 3 hunks, one defect theme "a met:false is not-met
  evidence regardless of receipt validity"):** M1 plus (a) the early validity guard in
  `expectation_ok` made conditional (`if expect != "not-met" and …`) and (b) the not-met branch
  counts `len(results)`/`len(not_met)` instead of the valid-row `total`.

Behavioral detector (bounded, same bytes for pristine/mutant/restored):

1. `python3 -B <driver> --selftest` → pristine must exit 0.
2. `python3 -B <driver> --root ./root --controls ./controls.tsv --counter ./counter/err_counter.py
   --classes v5 --expect not-met --out ./fixture-out/<tag>/summary.json` → pristine must exit **1**
   with `ok=false`, `notMet=0`.

## Verbatim evidence

### Baseline — pristine bytes

```
$ sha256sum .ufo/waves/round-45/c45_audit.py
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  .ufo/waves/round-45/c45_audit.py
$ sha256sum /fast/scratch/hyaku/kake-r45/AttackNotMetGate/c45_audit.pristine.py
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  .../c45_audit.pristine.py

$ python3 -B ./c45_audit.pristine.py --selftest
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
rc=0

$ python3 -B ./c45_audit.pristine.py --root ./root --controls ./controls.tsv \
    --counter ./counter/err_counter.py --classes v5 --expect not-met \
    --out ./fixture-out/honest/summary.json
AUDIT kake-r45 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=0/0 notMet=0 build_met=0/0 ok=False counter=64ce0a07a2d2
  ctl1                 legacy     met=False caught=D                      counter_error
rc=1   ok=False notMet=0 notMetNames=[] errors=['ctl1:counter_error'] controls=0
```

Baseline passes both detector legs: the honest driver **refuses** the invalid-only not-met cohort.

### M1 — only `not_met_rows` weakened

```
$ diff -u c45_audit.pristine.py c45_audit.m1_notmet_only.py
-def not_met_rows(rows):
-    return [row for row in rows if row_valid(row) and row.get("met") is False]
+def not_met_rows(rows):
+    return [row for row in rows if row.get("met") is False]

$ python3 -B ./c45_audit.m1_notmet_only.py --selftest
rc=1   AssertionError
    assert not not_met_rows([error_row])
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError

$ python3 -B ./c45_audit.m1_notmet_only.py --root ./root --controls ./controls.tsv \
    --counter ./counter/err_counter.py --classes v5 --expect not-met \
    --out ./fixture-out/m1/summary.json
AUDIT kake-r45 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=0/0 notMet=1 build_met=0/0 ok=False counter=64ce0a07a2d2
  ctl1                 legacy     met=False caught=D                      counter_error
rc=1   ok=False notMet=1 notMetNames=['ctl1'] errors=['ctl1:counter_error'] controls=0
```

M1 does **not** certify: the early validity guard in `expectation_ok` still forces `ok=False`
(defense in depth). But M1 leaks `notMet=1` / `notMetNames=['ctl1']` into the summary while
`controls=0` and `errors=['ctl1:counter_error']` — a self-inconsistent receipt. Shipped selftest
kills M1 at its direct function-level assert.

### M2 — coherent not-met-trust mutant

```
$ diff -u c45_audit.pristine.py c45_audit.m2_notmet_trust.mut.py
@@ not_met_rows
-    return [row for row in rows if row_valid(row) and row.get("met") is False]
+    return [row for row in rows if row.get("met") is False]
@@ expectation_ok
-    if any(not row_valid(row) for row in results) or any(not row_valid(row) for row in build):
+    if expect != "not-met" and (
+            any(not row_valid(row) for row in results) or any(not row_valid(row) for row in build)):
         return False
@@ expectation_ok tail
-    return expect == "not-met" and total == expected_rows and len(not_met) == total
+    return expect == "not-met" and len(results) == expected_rows and len(not_met) == len(results)

$ python3 -B ./c45_audit.m2_notmet_trust.py --root ./root --controls ./controls.tsv \
    --counter ./counter/err_counter.py --classes v5 --expect not-met \
    --out ./fixture-out/m2/summary.json
AUDIT kake-r45 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=0/0 notMet=1 build_met=0/0 ok=True counter=64ce0a07a2d2
  ctl1                 legacy     met=False caught=D                      counter_error
rc=0   ok=True notMet=1 notMetNames=['ctl1'] errors=['ctl1:counter_error'] controls=0
```

**M2 certifies not-met on a cohort whose only row is invalid** (exit 0, `ok=True`, `notMet=1`) while
the same fixture against pristine bytes exits 1 (`ok=False`, `notMet=0`). Attack demonstrated.

```
$ python3 -B ./c45_audit.m2_notmet_trust.py --selftest
rc=1   AssertionError
    assert not not_met_rows([error_row])
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

Shipped `--selftest` **kills** M2 (rc=1) before the end-to-end cohort is even reached — the
error-row asserts at `selftest()` are the load-bearing kill.

### Restoration

Mutant scratch bytes were restored from pristine bytes; both detectors re-run on the restored bytes:

```
restored M2 path sha: f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076
pristine sha:        f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076
lane sha now:        f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076

RESTORED selftest rc=0 :: SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
RESTORED fixture rc=1 ok=False notMet=0 controls=0 errors=['ctl1:counter_error']
```

The lane `c45_audit.py` hash was unchanged across the mutation/restoration probe itself (verified
immediately after restore, `f3c3171b…`); no lane file other than this report was written by this
seat. A separate lane edit landed at 00:59:29 under another writer — see Drift below.

## Drift at tip during the probe (finding)

The lane driver changed under the probe (not by this seat; I wrote only this report). Baseline copy
was taken at 00:58 and matched the declared hash; at 00:59:29 the lane file became
`b61447e6…416660` (21904 bytes), adding an `-O` selftest guard and a `bad-build` selftest leg.

```
$ sha256sum .ufo/waves/round-45/c45_audit.py      # at probe start / after restore
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076
$ sha256sum .ufo/waves/round-45/c45_audit.py      # 00:59:29 drift, stable on recheck
b61447e64730dcdb1449fcb3002d0bc09e7ceb4d8be2c249c7f1604358416660
```

Replayed read-only against the drifted tip (`c45_audit.drift.pristine.py`, same 3 anchors):

```
$ python3 -B c45_audit.drift.pristine.py --selftest
Traceback (most recent call last):
  ...
  File ".../c45_audit.drift.pristine.py", line 333, in _selftest_cohort
    assert sum(1 for b in summary["build"] if b.get("met") is True) == 0, summary["build"]
AssertionError: [{'run': 1, 'exit': 2, 'met': True, 'seed': 1, 'equalRuns': None, 'ratios': None,
'receipt': 'build-1.json', 'error': 'counter_error'}, ... run 2/3 identical ...]
rc=1

$ python3 -B c45_audit.drift.m2.py --root ./root --controls ./controls.tsv \
    --counter ./counter/err_counter.py --classes v5 --expect not-met \
    --out ./fixture-out/drift-m2/summary.json
AUDIT kake-r45 ... notMet=1 build_met=0/0 ok=True ...
  ctl1                 legacy     met=False caught=D                      counter_error
rc=0   ok=True notMet=1 errors=['ctl1:counter_error'] controls=0
$ python3 -B c45_audit.drift.m2.py --selftest
rc=1   AssertionError  (kills the same not_met_rows assert as before)
$ python3 -B c45_audit.drift.pristine.py --root ./root ... --expect not-met ...
rc=1   ok=False notMet=0
```

Two operability findings at the drifted tip, both outside this seat's write scope:

1. **The drifted tip's shipped `--selftest` is RED** (rc=1). The newly added build-leg assert is
   defeated by `build_build_row`: an invalid build receipt (`counter_error`, exit 2) still carries
   its raw `met=True` claim into `summary["build"][*].met`. The top-level verdict stays safe
   (`row_valid` blocks `build_met`), but the summary row exposes an unmasked met claim and the new
   assert fails. This is exactly a build-leg twin of the not-met attack below: validity is enforced
   in the verdict, not at row materialization.
2. The not-met attack (M2) reproduces unchanged at the drifted tip: mutant certifies
   `ok=True notMet=1` on the invalid-only fixture while pristine refuses; `--selftest` still kills
   the mutant.

## Verdict

| Mutant | Named weakening | Certifies not-met on invalid-only fixture? | Shipped `--selftest` | Verdict |
|---|---|---|---|---|
| M1 | yes (`not_met_rows` loses validity) | **no** — early guard holds `ok=False`; only summary counters leak (`notMet=1`, `controls=0`) | rc=1 AssertionError | **killed** (behavior survived at verdict level; summary integrity did not) |
| M2 | yes + guard made not-met-exempt + not-met branch counts raw rows | **yes** — rc=0 `ok=True notMet=1` with `errors=['ctl1:counter_error']`, `controls=0` | rc=1 AssertionError | **killed** |

- Pass/fail on the named attack: the driver's top-level not-met verdict is not defeatable by the
  named single-point `not_met_rows` weakening — the `expectation_ok` early validity guard is the
  load-bearing check, and the named mutant is caught by `--selftest`. A coherent "trust met:false"
  mutant **does** certify an invalid receipt as not-met, and the shipped `--selftest` kills it.
- Operability finding: `not_met_rows` alone is not a gate; do not treat it as one in receipts. Its
  summary fields (`notMet`, `notMetNames`) are validity-independent only if the mutant exists — in
  shipped code they are filtered, but the verdict safety actually comes from `expectation_ok`'s
  leading guard.
- Freshness: untouched. The probe did not exercise mtime/sha laundering into not-met beyond using
  a fresh, self-sha-matching receipt; the sole invalidity was the counter exit code, which the
  driver correctly maps to `counter_error`.
- Fixture-contract observation: `load_counter` **executes** the counter module at import. A counter
  with import-time side effects hijacks the driver's own `--out` (first attempt wrote the receipt
  into `summary.json` and exited 2 silently). Scratch fixture counters here guard their body with
  `if __name__ == "__main__":`; no shipped behavior was re-run against this and it is not claimed as
  a driver defect.

Unrun: none material. No tool installs or upgrades were performed.

## Files written

Lane (only):
- `.ufo/waves/round-45/w2/AttackNotMetGate.md` (this report)

Scratch `/fast/scratch/hyaku/kake-r45/AttackNotMetGate/`:
- `c45_audit.pristine.py` (byte copy, sha `f3c3171b…0a076`)
- `c45_audit.m1_notmet_only.py` (mutant, sha `52d3eea8…87ef58`)
- `c45_audit.m2_notmet_trust.py` (restored to pristine bytes)
- `c45_audit.m2_notmet_trust.mut.py` (archived mutant, sha `22501a84…38dac8`)
- `c45_audit.drift.pristine.py` (read-only copy of drifted tip `b61447e6…416660`)
- `c45_audit.drift.m2.py` (M2 replay on drifted tip, sha `d2e6ffbf…a80921`)
- `root/ctl.py`, `controls.tsv`, `counter/err_counter.py`
- `fixture-out/{honest,m1,m2,restored,drift-m2,drift-pristine}/summary.json`, `selftest-pristine-out/`
