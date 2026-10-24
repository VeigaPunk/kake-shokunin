# MutV2GateFinal — rebuilt spec mutants vs FINAL `c45_audit.py`

Seat `kake-r45.MutV2GateFinal` (mutation-tester), lane `kake-shokunin`, round-45 wave 2.
Axes: **operability** (does the shipped self-test still kill the named defects on the bytes that
actually ship?) · **freshness** (do the rebuilt mutants match the current receipt-gate shape?).

Scratch: `/fast/scratch/hyaku/kake-r45/MutV2GateFinal/` (all copies + detectors).
Report: this file. No other lane path was written.

## Target and why it moved

```text
$ sha256sum .ufo/waves/round-45/c45_audit.py
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  .ufo/waves/round-45/c45_audit.py
$ stat -c '%s bytes mtime=%y' .ufo/waves/round-45/c45_audit.py
20320 bytes mtime=2026-10-24 00:38:48.540162098 -0300
```

w1 (`MutDriverV2Spec`) mutated `5a342e29c7e872d992cfedc26de849c010d197bb82162e007a61a55d915c7051`.
The final bytes are `f3c3171b…` and they **add `_selftest_cohort()`** (an end-to-end probe that
runs `main()` against a fake counter in four modes: `counter-error`, `tool-absent`, `stale`,
`honest`). w1's `mutants/v2/m*.py` are built on the superseded snapshot, so they cannot answer the
question. I rebuilt every mutant as a scratch byte-copy of the final file with anchor-exact,
single-occurrence edits (`make_mutants.py` asserts each anchor occurs exactly once, so a silent
no-op mutant is impossible), then re-ran the **shipped** `--selftest` on each.

## The rebuilt mutants (single-point, diffs verified)

| id | mutation | final-bytes anchor | sha256 |
|---|---|---|---|
| m1 | exit gate removed | `if exit_code not in (0, 1): return False, "counter_error"` | `3332d2296f1c9bef…` |
| m2 | note gate removed | `if receipt.get("note") == "tool absent": … "tool_absent"` | `154365c8e74f6065…` |
| m3 | freshness window removed | `in_window = lower_ns <= receipt_mtime_ns <= upper_ns` → `True` | `885ee0e6c09f9463…` |
| m4 | counter-sha binding removed | `if receipt.get("counterSha256") != counter_sha: … "stale_receipt"` | `ee2863935d087232…` |
| m5 | invalid rows counted as not-met | `not_met_rows` drops `row_valid(row)` | `83b784d276f50ace…` |
| m6 | build-count pin removed | `count_ok = …` → `True` **and** `expectation_ok`'s `len(build) != build_runs` check | `899deac49183ebe2…` |
| m7 | seed gate removed (extra) | `if "seed" not in receipt or receipt["seed"] is None: …` | `ef6b09bfe8245be6…` |
| m8 | **control** row builder ignores validity | `error=validity_error, _valid=valid)` → `error=None, _valid=True)` | `8eef81d5ef03c0a3…` |
| m9 | window neutered at control call site | `(mtime_ns, started_ns - EPS, finish_ns + EPS)` → `(mtime_ns, 0, 2**62)` | `4a9147c2257b95a6…` |
| m10 | **build** row builder ignores validity | `"error": validity_error, "_valid": valid}` → `"error": None, "_valid": True}` | `1b01079b2efee1d8…` |

Pristine copy `pristine_final.py` sha256 = `f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076`
(byte-identical to the lane file; diff-verified by hash, not by eye).

## Decisive output 1 — shipped `--selftest` on pristine and on every mutant

```text
$ python3 -B run_selftest.py
pristine_final.py  selftest_exit=0  SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
mutants/m1.py      selftest_exit=1  assert receipt_validity(receipt, 2, in_window, "counter-sha") == (False, "counter_error")
mutants/m2.py      selftest_exit=1  assert receipt_validity(dict(receipt, note="tool absent"), 1, in_window,
mutants/m3.py      selftest_exit=1  assert receipt_validity(receipt, 1, (111, 90, 110), "counter-sha") == (False, "stale_receipt")
mutants/m4.py      selftest_exit=1  assert receipt_validity(dict(receipt, counterSha256="other-sha"), 1, in_window,
mutants/m5.py      selftest_exit=1  assert not not_met_rows([error_row])
mutants/m6.py      selftest_exit=1  assert not expectation_ok("witnessed", [class_divergence, mixed_divergence],
mutants/m7.py      selftest_exit=1  assert receipt_validity({"counterSha256": "counter-sha", "note": None}, 1,
mutants/m8.py      selftest_exit=1  assert summary["ok"] is False and summary["witnessed"] == 0, (mode, summary["witnessed"])
mutants/m9.py      selftest_exit=1  assert summary["ok"] is False and summary["witnessed"] == 0, (mode, summary["witnessed"])
mutants/m10.py     selftest_exit=0  SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
```

Every m1–m7 kill is the **intended** assertion (the `assert` line shown is the last one executed),
not an incidental traceback. m8/m9 are killed by the **new cohort**, and the assert message names
the defect: `('counter-error', 1)` / `('stale', 1)` = an invalid class produced `witnessed=1` while
the cohort requires 0.

The lane file itself, run directly (temp dirs only, lane bytes read-not-written):

```text
$ python3 -B .ufo/waves/round-45/c45_audit.py --selftest
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
LANE_SELFTEST_EXIT=0
```

## Decisive output 2 — the cohort extension alone (`_selftest_cohort` imported and called)

This isolates the wave-2 addition from the older unit asserts, so the verdict on "the selftest was
extended for exactly this" is not inflated by pre-existing assertions:

```text
$ for f in pristine_final.py mutants/m8.py mutants/m10.py mutants/m9.py mutants/m3.py; do
    python3 -B cohort_only.py "$f"; echo "$f exit=$?"; done      # (harness prints exit)
COHORT PASS pristine_final.py | exit=0
COHORT KILL m8.py: AssertionError: ('counter-error', 1) | exit=1
COHORT PASS m10.py | exit=0
COHORT KILL m9.py: AssertionError: ('stale', 1) | exit=1
COHORT KILL m3.py: AssertionError: ('stale', 1) | exit=1
```

So the extension genuinely covers: control-row unwiring (m8), call-site window neutering (m9), and
window removal at the predicate (m3) — a real improvement over w1, where all three survived.

## The finding: m10 survives the shipped selftest

`m10` unwires the validity gate from **`build_build_row()`** and the shipped `--selftest` still
prints PASS and exits 0. This is not an equivalent mutant — it restores exactly the C1 defect on
the build path and certifies invalid build receipts. Probe (fresh isolated cohort, control receipt
valid + genuine class witness; each build receipt is well-formed, sha-correct, seeded, in-window,
but `exit=2` with `met=True`; run with `--build-rev deadbeef --build-runs 3`):

```text
$ python3 -B build_probe.py pristine_final.py mutants/m10.py mutants/m8.py
pristine_final.py  exit=1 ok=False build_met=0/3 errors=['counter_error', 'counter_error', 'counter_error']
   AUDIT kake-r45 classes=v5 classKeys=G1,…,G10 witnessed=1/1 notMet=1 build_met=0/3 ok=False counter=513af9225c0f
m10.py             exit=0 ok=True build_met=3/3 errors=[None, None, None]
   AUDIT kake-r45 classes=v5 classKeys=G1,…,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=513af9225c0f
m8.py              exit=1 ok=False build_met=0/3 errors=['counter_error', 'counter_error', 'counter_error']
   AUDIT kake-r45 classes=v5 classKeys=G1,…,G10 witnessed=1/1 notMet=1 build_met=0/3 ok=False counter=513af9225c0f
```

Pristine refuses (`build_met=0/3`, three `counter_error` rows, exit 1). m10 prints
`build_met=3/3 ok=True` and exits 0 **from exit-2 receipts** — C1's "invalid receipt accepted" is
back on the build path with a green selftest. (m8 is killed here too, because the control gate is
also exercised by this probe; the distinguishing case is m10.)

Cause, verbatim in the final bytes — the cohort subprocess argv never supplies build flags, so
`score_build`/`build_build_row` never run inside `--selftest`:

```text
$ grep -n 'subprocess.run(' -A5 .ufo/waves/round-45/c45_audit.py     # cohort call sites
279:        p = subprocess.run(
280-            [sys.executable, "-B", me, "--root", root, "--controls",
281-             os.path.join(tmp, "controls.tsv"), "--counter", fake_path,
282-             "--classes", "v5", "--expect", "witnessed", "--out",
283-             os.path.join(cohort, "summary.json")],
...
296:    p = subprocess.run(
297-            [sys.executable, "-B", me, "--root", root, "--controls",
298-             os.path.join(tmp, "controls.tsv"), "--counter", fake_path,
299-             "--classes", "v5", "--expect", "not-met", "--out",
300-             os.path.join(cohort, "summary.json")],
```

`build_build_row` has exactly one caller (`score_build` inside `main()`, reached only when
`--build-rev` **and** `--build-runs` are set), and the shipped selftest never sets them. In real
runs (honest cohort, `c45_matrix.py --stage before|after`) the build receipts are valid, so the
gate never fires there either: m10 has no able-to-fail detector anywhere in the shipped surface.
The docstring's claim "the selftest drives it directly" is true of `build_control_row` only.

## Verdict on the named attack

| named attack | detector | result | verdict |
|---|---|---|---|
| exit gate removed (m1) | shipped `--selftest` | exit 1, intended assert | **KILLED** |
| note gate removed (m2) | shipped `--selftest` | exit 1, intended assert | **KILLED** |
| freshness window removed (m3) | shipped `--selftest` / cohort | exit 1 (unit assert; cohort also kills `('stale',1)`) | **KILLED** |
| counter-sha binding removed (m4) | shipped `--selftest` | exit 1, intended assert | **KILLED** |
| invalid rows as not-met (m5) | shipped `--selftest` | exit 1, `assert not not_met_rows([error_row])` | **KILLED** |
| build-count pin removed (m6) | shipped `--selftest` | exit 1, `expectation_ok(..., build_runs=3)` assert | **KILLED** |
| honest bytes | shipped `--selftest` | exit 0, PASS | **GREEN** |
| m8 control builder ignores gate | cohort extension | exit 1, `('counter-error', 1)` | **KILLED** (extension works) |
| m10 build builder ignores gate | cohort extension | exit 0, PASS | **SURVIVED (coverage gap)** |

**Pass** on the six-mutant requirement (6/6 killed on the final bytes; honest 0). **Fail / partial**
on the stated "m8/m10 class is now covered": the extension kills m8 but **not** the build-row twin
m10, which remains behaviourally refuted out-of-tree (`build_met=3/3 ok=True` from `counter_error`
receipts) while the shipped selftest stays green. This is a detector-coverage finding, not a
contract change: the repair is to add a build-flag cohort leg (e.g. `--build-rev X --build-runs 2`
with a fake counter that returns exit 2 for `--revision` runs) and assert `build_met==0` / exit 1.

## Restoration evidence

The lane file was never edited; every run above read it or scratch copies. Before and after:

```text
$ sha256sum .ufo/waves/round-45/c45_audit.py /fast/scratch/hyaku/kake-r45/MutV2GateFinal/pristine_final.py
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  .ufo/waves/round-45/c45_audit.py
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  /fast/scratch/hyaku/kake-r45/MutV2GateFinal/pristine_final.py
$ stat -c '%s bytes mtime=%y' .ufo/waves/round-45/c45_audit.py
20320 bytes mtime=2026-10-24 00:38:48.540162098 -0300   # unchanged across the whole run
```

Post-run lane `--selftest` exit 0 (above). w1's superseded mutant directory is untouched:
`mutants/v2/m10.py` still `fbebcd931281ed68…` (w1 bytes, mutation of `5a342e29…`), distinct from my
rebuilt `1b01079b2efee1d8…` against `f3c3171b…`.

## Files written (all)

Lane:
- `.ufo/waves/round-45/w2/MutV2GateFinal.md` (this report)

Scratch `/fast/scratch/hyaku/kake-r45/MutV2GateFinal/`:
- `pristine_final.py` — byte copy of lane `c45_audit.py` @ `f3c3171b…`
- `make_mutants.py` — anchor-exact, single-occurrence generator (fails `ANCHOR-FAIL`/`NOOP-FAIL`)
- `mutants/m1.py` … `mutants/m10.py` — 10 single-point mutants (hashes in the table above)
- `run_selftest.py` — shipped `--selftest` sweep
- `cohort_only.py` — imports the copy and calls `_selftest_cohort()` alone
- `build_probe.py` — invalid-build-receipt probe (non-equivalence proof for m10)

No pip/npm/cargo/pacman install was made; all detectors are stdlib CPython 3.14.8
(`python3 --version` → `Python 3.14.8`). No git/jj command was run. No file outside the paths
listed above was written.
