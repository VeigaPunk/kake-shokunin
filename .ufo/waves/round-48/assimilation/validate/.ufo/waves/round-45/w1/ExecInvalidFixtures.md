# ExecInvalidFixtures — C1 BEFORE receipts

Axes: operability and freshness. Implemented the three invalid-receipt fixtures, retained their v1 outputs, and ran the honest real-counter control. Used `.ufo/waves/round-45/w1/ScoutReceiptShape.md` for the committed receipt schema. Its finding that `caughtBy` is derived in the audit summary—not a raw counter-receipt field—is reflected in each fixture README.

## Result

**PASS against the named BEFORE-v1 attacks:** all three invalid fixtures returned `ok=true` / were certified witnessed by frozen `c44_audit.py`, as expected for the baseline. The exit-2 fixture had summary row `exit=2`; tool-absent had `note="tool absent"`, all 21 runs false and `exit=1`; stale-planted had row and build exits `-9` while its pre-run receipts supplied witness/build credit. The honest real-counter control returned `ok=true` for `--expect not-met`, with row `exit=1`, `error=null`, and a fresh run receipt. All four driver invocations themselves exited 0.

## Exact driver commands

Working directory: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

```sh
python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-45/fixtures/counter-error/controls.tsv --counter .ufo/waves/round-45/fixtures/counter-error/fake_counter.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --workers 1 --out .ufo/waves/round-45/verification/hardening/before/counter-error/out-v1/summary.json
python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-45/fixtures/tool-absent/controls.tsv --counter .ufo/waves/round-45/fixtures/tool-absent/fake_counter.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --workers 1 --out .ufo/waves/round-45/verification/hardening/before/tool-absent/out-v1/summary.json
python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-45/fixtures/stale-planted/controls.tsv --counter .ufo/waves/round-45/fixtures/stale-planted/fake_counter.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --workers 1 --out .ufo/waves/round-45/verification/hardening/before/stale-planted/out-v1/summary.json
python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-45/fixtures/honest/controls.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes v5 --expect not-met --build-rev 020bc457 --build-runs 3 --workers 1 --out .ufo/waves/round-45/verification/hardening/before/honest/out-v1/summary.json
```

Each command's stdout was saved as `stdout` and copied to `summary.txt`; the generated `out-v1/summary.json` was copied to the class-level `summary.json`. The shell reported `driver_exit=0` for each invocation.

## Decisive stdout (trailing padding elided; captured files retain exact output)

Counter-error:

```text
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=15363b71eaa0
  ctl1                 G5         met=False caught=G5,G7
  witnessed-by-class ctl1 caughtBy=G5,G7
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
```

Tool-absent:

```text
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=c697435a11e7
  ctl1                 G5         met=False caught=A,B,C,D,E,F,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,T1,T2,T3,T4,T5
  witnessed-by-class ctl1 caughtBy=A,B,C,D,E,F,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,T1,T2,T3,T4,T5
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
```

Stale-planted:

```text
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=18e3bcfda602
  ctl1                 G5         met=False caught=G2,G4,G9
  witnessed-by-class ctl1 caughtBy=G2,G4,G9
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
```

Honest real-counter control:

```text
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=5cedaa3b9f91
  ctl1                 G5         met=False caught=G5,G7
  witnessed-by-class ctl1 caughtBy=G5,G7
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
```

## Retained receipt evidence

- Summary JSON fields: counter-error `{ok:true, row.exit:2, row.met:false, caughtBy:[G5,G7]}`; tool-absent `{ok:true, row.exit:1, row.met:false, caughtBy:[A,B,C,D,E,F,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,T1,T2,T3,T4,T5]}`; stale-planted `{ok:true, row.exit:-9, row.met:false, caughtBy:[G2,G4,G9], build exits:[-9,-9,-9]}`; honest `{ok:true, row.exit:1, row.met:false, error:null, build exits:[0,0,0]}`.
- Tool-absent receipt readback: `met=false`, `note="tool absent"`, `toolSha256=null`, `equalRuns="0/21"`, 21 runs, `allFalse=true`, `allAbsent=true`.
- Honest real receipt readback: `met=false`, `note=null`, `seed=225637986974148`, `classesMode="v5"`, `toolFile` points to the copied fixture source, `equalRuns="19/21"`. The honest output directory was not preplanted.
- Counter-error receipt source readback: `met=false`, `seed=224408754848177`, `note=null`, `equalRuns="19/21"`, class runs G1–G10, false runs `[G5,G7]`; the fake wrote those committed bytes and exited 2.
- `cmp -s` confirmed byte-exact receipt copies: counter-error control and build fixture receipts; tool-absent template and build receipt; stale-planted control and all three build fixtures plus the pre-run output receipts. The copied control source and all four `ctl1.py` files hash to `00ece64886137a23b1b6a8e7f7795885d2e23ae3c1c2a0dfdb8f05f085503238`.

## Files written

- `.ufo/waves/round-45/fixtures/counter-error/`: `README.md`, `controls.tsv`, `ctl1.py`, `fake_counter.py`, `control-receipt.json`, `build-receipt.json`.
- `.ufo/waves/round-45/fixtures/tool-absent/`: `README.md`, `controls.tsv`, `ctl1.py`, `fake_counter.py`, `control-template.json`, `build-receipt.json`.
- `.ufo/waves/round-45/fixtures/stale-planted/`: `README.md`, `controls.tsv`, `ctl1.py`, `fake_counter.py`, `tools/ctl1.json`, `build-1.json`, `build-2.json`, `build-3.json`.
- `.ufo/waves/round-45/fixtures/honest/`: `README.md`, `controls.tsv`, `ctl1.py`.
- For each of `counter-error`, `tool-absent`, `stale-planted`, and `honest`, `.ufo/waves/round-45/verification/hardening/before/<class>/`: `summary.json`, `summary.txt`, `stdout`; and `out-v1/summary.json`, `out-v1/build-1.json`, `out-v1/build-2.json`, `out-v1/build-3.json`, `out-v1/tools/ctl1.json`.
- `.ufo/waves/round-45/w1/ExecInvalidFixtures.md` (this report).

No blockers. No installs; no build, lint, formatter, or unrelated tests were run. The only driver runs were the four explicitly requested v1 commands; v2 was not run.
