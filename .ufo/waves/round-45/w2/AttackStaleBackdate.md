# AttackStaleBackdate — w2 falsify probe: does the stale-backdate fixture carry its own refusal?

Seat: kake-r45.AttackStaleBackdate (lane kake-shokunin, axes operability/freshness).
Date: 2026-10-24. Time-boxed probe; every number below was produced in this seat.

## Target and hypothesis

The after-stage matrix leg `stale-planted` (`c45_matrix.py:44`, `AFTER_STALE_FIXTURE =
"stale-backdate"`) rejects the fixture `.ufo/waves/round-45/fixtures/stale-backdate/fake_counter.py`
with the named class `stale_receipt`. The fixture's docstring asserts the refusal is the
run-window mtime branch ("BACKDATES its mtime 5 seconds ... Under driver v2 the receipt
fails the run-window mtime check").

Attack: build scratch variants of the fixture and run them under the **real, unmodified v2
driver** (`c45_audit.py`, sha256 `f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076`):

1. `v1_nobackdate.py` — shipped fixture minus the two `os.utime` backdate lines (fresh mtime).
   Predicted by tasking: v2 accepts it as a witness, exit 0 `ok=True`.
2. `v2_zerosh.py` — shipped fixture minus the backdate, but `counterSha256 = "0"*64`.
   Predicted: `stale_receipt` named via the **sha** branch, not mtime.

## Setup

Scratch: `/fast/scratch/hyaku/kake-r45/AttackStaleBackdate/` (all writes here; the lane tree was
read-only for this seat except this report). `--root` is the lane repo so the fixture's own
`controls.tsv` (ctl1, sha `00ece648…`, matches `ctl1.py`) is used unchanged. No tool installs.

Variants (full bytes, scratch only):
- `v1_nobackdate.py` — sole delta vs shipped fixture: `past = time.time() - 5; os.utime(out, (past, past))` removed.
- `v2_zerosh.py` — same delta plus `"counterSha256": "0" * 64` (self-sha replaced by zeroes; `met:False`, `caughtBy G2` shape kept).
- `v1b_buildmet.py` — attribution probe only: `v1` plus `met=True` when `--revision` is present (build receipts), because `expectation_ok("witnessed")` cannot pass otherwise (see Finding 1).

Baseline driver self-check (unmodified tree):
```
$ python3 -B .ufo/waves/round-45/c45_audit.py --selftest
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
```

## Commands (verbatim, run from `/home/vgpnk/Projects/shokunin/kake-shokunin`)

```
python3 -B .ufo/waves/round-45/c45_audit.py --root "$PWD" \
  --controls .ufo/waves/round-45/fixtures/stale-backdate/controls.tsv \
  --counter <VARIANT> --classes v5 --expect witnessed \
  --out /fast/scratch/hyaku/kake-r45/AttackStaleBackdate/out_<TAG>/summary.json \
  --build-rev 020bc457 --build-runs 3 --workers 1 --label <TAG>
```
plus one no-build run of variant 1 (no `--build-rev/--build-runs`).

## Decisive output

### Pristine fixture (control: refusal reproduced)
```
AUDIT pristine classes=v5 classKeys=G1,...,G10 witnessed=0/0 notMet=0 build_met=0/3 ok=False counter=77aa39c7eefa
  ctl1                 G5         met=False caught=G2                     stale_receipt
  build#1 met=False equal=None stale_receipt
  build#2 met=False equal=None stale_receipt
  build#3 met=False equal=None stale_receipt
EXIT=1
```

### Variant 1 — backdate removed (real v2 driver, same build shape as the matrix)
```
AUDIT mut-v1-nobackdate classes=v5 classKeys=G1,...,G10 witnessed=1/1 notMet=1 build_met=0/3 ok=False counter=797e20092151
  ctl1                 G5         met=False caught=G2
  witnessed-by-class ctl1 caughtBy=G2
  build#1 met=False equal=None
  build#2 met=False equal=None
  build#3 met=False equal=None
EXIT=1
```
Row-level summary: `rows=[{'name':'ctl1','exit':0,'met':False,'caughtBy':['G2'],'error':None}]`,
`errors=[]`, `witnessedNames=['ctl1']`, `build=[{met:False,error:None} x3]`.

Variant 1 without any build leg: `witnessed=1/1 notMet=1 build_met=0/0 ok=False`, `errors=[]`, `EXIT=1`.

### Variant 1b — backdate removed **and** build receipts met=True (attribution probe)
```
AUDIT mut-v1b-buildmet classes=v5 classKeys=G1,...,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=481f439cad95
  ctl1                 G5         met=False caught=G2
  witnessed-by-class ctl1 caughtBy=G2
  build#1 met=True equal=None
  build#2 met=True equal=None
  build#3 met=True equal=None
EXIT=0
```

### Variant 2 — zero self-sha, fresh mtime (real v2 driver)
```
AUDIT mut-v2-zerosh classes=v5 classKeys=G1,...,G10 witnessed=0/0 notMet=0 build_met=0/3 ok=False counter=e4f0cc9662ba
  ctl1                 G5         met=False caught=G2                     stale_receipt
  build#1 met=False equal=None stale_receipt
  build#2 met=False equal=None stale_receipt
  build#3 met=False equal=None stale_receipt
EXIT=1
```
`errors=['ctl1:stale_receipt','build#1:stale_receipt','build#2:stale_receipt','build#3:stale_receipt']`.

### Branch attribution (real driver module imported read-only; same receipt bytes and bounds)
Bounds: `lower = manifest.started_ns - MTIME_EPS_NS`, upper deliberately 1000 s above receipt
mtime so the window cannot be what rejects.
```
pristine     mtime-start=-4986.352 ms  in_window=0  ctl1_error=stale_receipt
v1_build     mtime-start=+11.108 ms    in_window=1  ctl1_error=None
v1_nobuild   mtime-start=+11.354 ms    in_window=1  ctl1_error=None
v2_build     mtime-start=+11.238 ms    in_window=1  ctl1_error=stale_receipt
v1b_build    mtime-start=+11.792 ms    in_window=1  ctl1_error=None

v1_build: rec.sha=797e20092151 true_sha=797e20092151 mtime_in_window=True actual=(True, None)  sha_fixed=(True, None)
v2_build: rec.sha=000000000000 true_sha=e4f0cc9662ba mtime_in_window=True actual=(False, 'stale_receipt') sha_fixed=(True, None)
v1b_build: rec.sha=481f439cad95 true_sha=481f439cad95 mtime_in_window=True actual=(True, None) sha_fixed=(True, None)
```
`sha_fixed` rewrites only `counterSha256` in the same receipt; the verdict flips to `(True, None)`,
so for variant 2 the **sha branch** is the sole rejector. For variant 1 the same `receipt_validity`
returns `(True, None)` on the untouched receipt, so the shipped fixture's `stale_receipt` really
does come from the mtime branch (pristine mtime is 4.99 s before run start).

## Findings

1. **Tasking's predicted observable for variant 1 is false as stated.** A faithful
   backdate-removal does **not** yield `exit 0 ok=True`; it yields `EXIT=1 ok=False` with
   `errors=[]` and `witnessed=1/1`. Cause is in the driver, not the fixture: `build_met(build,
   build_runs)` (`c45_audit.py`) returns `count_ok and bool(build) and all(row_valid and
   row["met"] is True …)` — an empty build is a failure, and the fixture writes `met:False` into
   every build receipt, so `expectation_ok("witnessed")` fails on the build leg regardless of mtime.
   Variant 1b (`build receipts met=True`, control receipt still `met:False` + `caughtBy G2`) is the
   first construction that reaches `EXIT=0 ok=True`, proving the driver can accept and that the
   backdate is what blocks *the class*, not the only thing blocking the *stage*.
2. **Verdict on the named attack — PASS, with a correction.** The refusal *class* is genuinely
   carried by the `os.utime` backdate: remove it and `ctl1.error` is `None`, the row is `_valid`,
   `witnessedNames=['ctl1']`, and the mtime is +11 ms inside the window. But the fixture is
   **over-determined**: even with a fresh mtime the after-stage leg still fails (`ok=False`,
   `EXIT=1`) because its build receipts declare `met=False`. So "the fixture's ability to fail the
   after stage" is *not* attributable to the backdate alone; the stage's `ok` signal would remain
   red if the mtime check were deleted. The matrix only stays honest because it also requires the
   *named* class to appear (`rejections_named == 3`), and that class is what disappears.
3. **Variant 2 — PASS.** Zero self-sha with an in-window mtime is named `stale_receipt` by the sha
   branch (`receipt_validity` → `(False,'stale_receipt')`, same bounds with the true sha →
   `(True,None)`), on the control row and all three build rows. The sha branch is independently
   load-bearing, as claimed.
4. **Operability notes (read, not run).** [INFERENCE] If the mtime branch in `receipt_validity`
   were deleted, the stale leg would still report `ok=False` (finding 2), so `invalid_accepted`
   would remain 0; the after stage would fail only via `rejections_named` dropping to 2 (the other
   two fixtures still name their classes). That is the sole detector for mtime-branch removal —
   worth knowing when reading a green `invalid_accepted=0`.
   Also: `stale-backdate/` is the only invalid-class fixture directory **without a README.md**
   (counter-error, stale-planted, tool-absent, honest all have one), and `c45_matrix.py` stages it
   under leg name `stale-planted`, so the after receipt records
   `verification/matrix/runs/after/stale-planted-47bd82ade247/summary.json` whose `counter` field is
   the `stale-backdate` fixture. Cosmetic, but it misdirects anyone auditing the after stage by
   directory name.

## Restoration / non-mutation evidence

The lane tree was never written by this probe (variants and outputs live only in scratch). Hashes
before the first run and after the last run are identical:
```
5e1b1d25c8ee4c0b132ace6e05126de442ca72ba10c91b8a42b528ff3eef6bbd  .../stale-backdate/controls.tsv
00ece64886137a23b1b6a8e7f7795885d2e23ae3c1c2a0dfdb8f05f085503238  .../stale-backdate/ctl1.py
77aa39c7eefa7b7cab366f42d141a49a72cea5060deca118e88a307b4cd9e129  .../stale-backdate/fake_counter.py
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  .../round-45/c45_audit.py
```
Mutant self-hashes (as computed by the driver's `counterSha256` check): v1 `797e20092151…`,
v2 `e4f0cc9662ba…`, v1b `481f439cad95…`.

## Verdict

- Variant 1 attack: **lands with correction** — v2 accepts the fresh-mtime receipt as a witness
  (`witnessed 1/1`, `error None`, mtime +11 ms in window), so the `stale_receipt` *class* is carried
  by the backdate; but `exit 0 ok=True` is **not** reproduced (`EXIT=1`), because `build_met`
  rejects the fixture's `met=False` build receipts. Fixture is over-determined as a stage-failure
  witness; tasking's expected exit code is falsified.
- Variant 2 attack: **passes** — zero self-sha is refused as `stale_receipt` through the sha branch
  with the mtime proven in-window.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2/AttackStaleBackdate.md` (this report)
- `/fast/scratch/hyaku/kake-r45/AttackStaleBackdate/v1_nobackdate.py`
- `/fast/scratch/hyaku/kake-r45/AttackStaleBackdate/v2_zerosh.py`
- `/fast/scratch/hyaku/kake-r45/AttackStaleBackdate/v1b_buildmet.py`
- `/fast/scratch/hyaku/kake-r45/AttackStaleBackdate/out_{pristine,v1_build,v1_nobuild,v2_build,v1b_build}/` (driver summaries, manifests, receipts)

Unrun: `c45_matrix.py --stage after` against a driver mutant (finding 4 is code-read inference, not
an executed probe; driver mutation belongs to the C1 gate seats).
