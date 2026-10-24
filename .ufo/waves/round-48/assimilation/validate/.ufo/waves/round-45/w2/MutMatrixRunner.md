# MutMatrixRunner — can c45_matrix.py fail?

Seat: `kake-r45.MutMatrixRunner` · wave 2 (falsify) · axes: operability, freshness.
Named attack: **c45_matrix.py able-to-fail**. Three mutants of the matrix driver, each run with
`--stage after` against a scratch lane. Verdicts: **M1 killed by the identity gate** (mutant PASS
where the honest runner FAILs), **M2 survives as an equivalent mutant** (the loosened `<=1` is dead
slack masked by `len(named)==3`), **M3 dies** (the SIGKILL fixture cannot name `stale_receipt`).

## Pinned bytes and source drift

| object | sha256 |
|---|---|
| `c45_matrix.py` at copy time (01:00:43, baseline for all mutants) | `ebcccd55dcf910f87c14be5b5f8c912731d323b78ad1695284cb4321f642c63b` |
| `c45_matrix.py` at lane tip when probed (01:03:05) | `2e8d9af9476736d2baaa994036c4479d87e454716621298e0ea760eef576fb6f` |
| `c45_audit.py` (v2 driver, unchanged) | `f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076` |
| `c44_count_v5.py` (real counter) | `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc` |
| `controls-27.tsv` | `a1f0e364dad5ff937666966a16622e6895591a2eb3db714d6ecf3f3948c31bf8` |

**Source drifted mid-wave**: between my copy and the probes another writer changed
`.ufo/waves/round-45/c45_matrix.py` from `ebcccd55…` to `2e8d9af9…`. The only delta is cosmetic leg
naming in `stage_fixtures` for the after stage (`("stale-planted")` → `("stale-backdate")`); the
fixture selected (`AFTER_STALE_FIXTURE = "stale-backdate"`), `invalid_accepted`, `named`, and the
honest checks are byte-identical. My lanes pin `ebcccd55…`; I did not re-run against the tip.

```diff
--- ebcccd55 c45_matrix.py
+++ 2e8d9af9 c45_matrix.py
@@ -74,8 +74,9 @@ def stage_fixtures(stage: str):
     stale = "stale-planted" if stage == "before" else AFTER_STALE_FIXTURE
+    stale_leg = "stale-planted" if stage == "before" else "stale-backdate"
     return [("counter-error", "counter-error"), ("tool-absent", "tool-absent"),
-            (stale, "stale-planted")]
+            (stale, stale_leg)]
```

## Scratch design (why lanes are mirrored)

`c45_matrix.py` derives `LANE = Path(__file__).resolve().parents[3]` and writes `verification/matrix/`
under it. Running a mutant in-tree would write into the frozen lane, so each mutant runs in
`/fast/scratch/hyaku/kake-r45/MutMatrixRunner/lane-<id>/` — a real directory at the same depth whose
`.git`, `scripts/`, `round-41/realrun/`, `round-44/classes/`, `round-44/controls-r43/`,
`round-45/c45_audit.py` and `round-45/fixtures/` are symlinks to the lane; only
`verification/{matrix,honest-regression}` and the counter copy are real. The matrix, driver, counter,
controls and fixtures bytes are therefore unchanged; `git -C <lane>` resolves `020bc457` and the
build leg reproduces `met=True 21/21` (see smoke test). No lane file was written.

## Mutants (exact diffs vs the pinned baseline)

Each mutant changes one behavior-bearing point; hashes are of the scratch copies.

```diff
### M1 lane-m1/c45_matrix.py  sha256 289674e57bed4a2b45e348e9a5cf7131e5fb4a0a09e714ca4ef2731e64c9e2dc
@@ -116,8 +116,6 @@ (run_honest_leg)
     if summary is None:
         problems.append("no summary written")
     else:
-        if summary.get("counterSha256") != sha256(COUNTER_V5):
-            problems.append("counter sha mismatch")
         if summary.get("controls") != 27:
             problems.append("controls != 27")

### M2 lane-m2/c45_matrix.py  sha256 cb584926b6d388ab2c8f8e789edbed50f8e9b3cd2d5b51f290f204e80b99bacd
@@ -174,7 +174,7 @@ (main)
     if args.stage == "before":
         passed = invalid_accepted == 3
     else:
-        passed = (invalid_accepted == 0 and len(named) == 3 and
+        passed = (invalid_accepted <= 1 and len(named) == 3 and
                   honest_witnessed == 27 and honest_build_met == 3)

### M3 lane-m3/c45_matrix.py  sha256 64af0da6d21b7b57a78baad7a1cbf67599500fb869b88860d9d2f33330ed858d
@@ -41,7 +41,7 @@
 BUILD_REVISION = "020bc457"
 ...
-AFTER_STALE_FIXTURE = "stale-backdate"
+AFTER_STALE_FIXTURE = "stale-planted"
```

Because M1's deletion is invisible on the clean lane, it was paired with a probe that makes the
honest runner fail exactly on identity: the lane's counter copy carries a scratch-only shim that
counts invocations under its parent and, on the 30th completion (27 controls + 3 builds), appends one
comment line to its own bytes after every receipt has already recorded its start-of-run
`counterSha256`. The unmutated matrix (`lane-driftbase`) and M1 (`lane-m1`) run the **same** drifted
counter. Both `/tmp/kake45-drift-<ppid>` state files read exactly `30` (one append per run).

## Decisive result 1 — M1: mutant PASS where the honest runner FAILS

Command (both concurrent, identical lane shape and counter bytes):

```sh
python3 -B lane-driftbase/.ufo/waves/round-45/c45_matrix.py --stage after
python3 -B lane-m1/.ufo/waves/round-45/c45_matrix.py --stage after
```

Verbatim stdout/exit (324 s wall):

```text
===DRIFTBASE
stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=0 honest_build_met=0
MATRIX_AFTER_FAIL
EXIT=1
===M1
stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3
MATRIX_AFTER_PASS
EXIT=0
===HASHES
293d516414ecf96944c50836f74945325a5932658f061465e914d1c25cb68e9f  lane-driftbase/.ufo/waves/round-44/c44_count_v5.py
293d516414ecf96944c50836f74945325a5932658f061465e914d1c25cb68e9f  lane-m1/.ufo/waves/round-44/c44_count_v5.py
```

The honest legs differ only by the deleted check. Receipts (`verification/matrix/after.json`,
honest block, verbatim):

```text
##### driftbase
honest {"build_met": 3, "cohort": ".../honest-2eeb8857d62a", "exit": 0,
        "problems": ["counter sha mismatch"], "summary": ".../after-v5-v2.json",
        "valid": false, "witnessed": 27}
##### m1
honest {"build_met": 3, "cohort": ".../honest-5458cd30f6e3", "exit": 0,
        "problems": [], "summary": ".../after-v5-v2.json",
        "valid": true, "witnessed": 27}
```

Both honest summaries, verbatim:

```text
counterSha256 d6ccb6a515f741e3b0a48e537d810fa2c501155a1db7fd22a33ecfafbd80031b
ok True witnessed 27 controls 27 errors [] build_met 3 verdict witnessed 27/27 notMet=27 build met 3/3
```

Post-leg counter file hash is `293d516414…` in both lanes while the driver-recorded start-of-leg
`counterSha256` is `d6ccb6a515…`; `errors []` and `witnessed 27` prove every receipt's own
self-hash matched the driver's value. So the only rejection the honest matrix has is identity drift,
and deleting that one check converts FAIL(1) into PASS(0) with `witnessed=27, build=3`.

**Verdict M1: KILLED as a mutation** — the honest runner fails the drifted-counter state, the mutant
certifies it. The identity gate is load-bearing for this state, not decorative. Reachability caveat:
identity can only diverge by a byte change after the driver hashed the same path it invoked; the
driver self-reports that hash, so ordinary fixtures cannot exercise the check (this is the same
narrowness `w1/CriticC1Predicate.md` called out against the frozen sentence).

## Decisive result 2 — M2: the `<=1` slack is dead, masked by `len(named)==3`

Fixture-only probe on the clean lane (honest leg **UNRUN**, see below):

```text
##### base
invalid_accepted 0 named ['counter_error', 'stale_receipt', 'tool_absent']
  counter-error counter-error exit 1 ok False classes ['counter_error']
  tool-absent tool-absent exit 1 ok False classes ['tool_absent']
  stale-planted stale-backdate exit 1 ok False classes ['stale_receipt']
##### m2
invalid_accepted 0 named ['counter_error', 'stale_receipt', 'tool_absent']
  counter-error counter-error exit 1 ok False classes ['counter_error']
  tool-absent tool-absent exit 1 ok False classes ['tool_absent']
  stale-planted stale-backdate exit 1 ok False classes ['stale_receipt']
```

To give the loosening a state it could actually accept, `lane-m2acc` replaces the stale-backdate fake
counter with a receipt-shaped forgery the v2 driver **accepts** (`exit 0`, in-window fresh receipt,
own sha, `met=False`, G2 divergence for controls; `met=True` for the three build calls). Same lane
carries both matrices; note that `c45_matrix_base.py` was copied after the mid-wave rename, so it is
the tip version (`2e8d9af9…`, leg key `stale-backdate`) while the M2 copy is the pinned baseline
(`cb584926…`, leg key `stale-planted`):

```text
##### c45_matrix_base.py (unmutated)
matrix_sha256 2e8d9af94767 invalid_accepted 1 named ['counter_error', 'tool_absent'] rejections_named 2
  counter-error counter-error exit 1 ok False classes ['counter_error']
  tool-absent tool-absent exit 1 ok False classes ['tool_absent']
  stale-backdate stale-backdate exit 0 ok True classes []
##### c45_matrix.py (M2, <=1)
matrix_sha256 cb584926b6d3 invalid_accepted 1 named ['counter_error', 'tool_absent'] rejections_named 2
  counter-error counter-error exit 1 ok False classes ['counter_error']
  tool-absent tool-absent exit 1 ok False classes ['tool_absent']
  stale-planted stale-backdate exit 0 ok True classes []
```

Both the honest matrix and M2 FAIL on this state: accepting a fixture always removes that fixture's
named class, so `invalid_accepted == 1` forces `len(named) == 2` and the `==3` conjunct fires
regardless of the `<=1` relaxation. The three fixtures are hard-coded one per class
(`stage_fixtures`), so no reachable after-stage state can have both one accepted invalid and three
named classes.

**Verdict M2: SURVIVED (equivalent on all reachable inputs)** — `<=1` is dead slack, not a false-PASS
path. This is a coverage finding: the bound itself is untested because the class-conjunction masks
it. It does **not** show the matrix cannot fail.

## Decisive result 3 — M3: dies, the SIGKILL fixture names the wrong class

Fixture-only probe (honest leg **UNRUN**):

```text
##### m3
invalid_accepted 0 named ['counter_error', 'tool_absent']
  counter-error counter-error exit 1 ok False classes ['counter_error']
  tool-absent tool-absent exit 1 ok False classes ['tool_absent']
  stale-planted stale-planted exit 1 ok False classes ['counter_error']
```

`stale-planted`'s fake counter `os.kill(signal.SIGKILL)`s every invocation, so `exit=-9` and
`receipt_validity` returns `counter_error` on its first branch (`if exit_code not in (0, 1)`), never
`stale_receipt`. `len(named)==2` is independent of the honest leg, so M3's `--stage after` cannot
print PASS; it would exit 1 even with `honest_witnessed=27, honest_build_met=3`.

**Verdict M3: KILLED (dies)** — the after-stage gate is sensitive to which stale fixture is wired.
Side finding: the SIGKILL fixture can never produce `stale_receipt` under v2; the backdate fixture is
the only mtime-branch witness, so the two fixtures are not interchangeable.

## Honest-runner baseline

A clean-lane full `--stage after` (unmutated matrix, unmodified counter) was **UNRUN**; the same
honest leg ran twice inside the drift pair on identical inputs and returned
`witnessed 27/27, controls 27, build 3/3, errors [], ok=True, exit 0` in both. Fixture-gate baseline
on the clean lane measured `invalid_accepted 0`, `named ['counter_error','stale_receipt','tool_absent']`.
The lane tip's own recorded `after.json` reports `MATRIX_AFTER_PASS` (`invalid_accepted=0`,
`rejections_named=3`, `honest_witnessed=27`, `honest_build_met=3`), consistent with these probes.

## Answer to the named attack

The matrix **is able to fail**: it fails on mid-leg counter-byte drift (honest `FAIL`, exit 1) and on
the SIGKILL-for-backdate fixture swap (`named=2`). The mutants split cleanly:

| mutant | scratch sha256 | `--stage after` | verdict |
|---|---|---|---|
| M1 identity check deleted | `289674e5…` | PASS, exit 0 (honest runner: FAIL, exit 1, `problems=["counter sha mismatch"]`) | killed by the drift probe; gate is load-bearing but reachable only by byte drift |
| M2 `invalid_accepted <= 1` | `cb584926…` | clean lane: same as base; accepted-invalid lane: FAIL (`named=2`) | survived as equivalent; slack masked, unexercised |
| M3 stale fixture → SIGKILL | `64af0da6…` | FAIL (`named=2`), independent of honest leg | died |

No mutant produced a false PASS that the honest matrix would reject. The residual coverage finding is
the `<=1` slack in M2 (and, symmetrically, the honest-leg checks other than identity are not
individually exercised by any fixture).

## Commands run (scratch root `/fast/scratch/hyaku/kake-r45/MutMatrixRunner`)

```sh
mkdir -p /fast/scratch/hyaku/kake-r45/MutMatrixRunner
# mirrored lanes lane-{base,driftbase,m1,m2,m3,m2acc}: symlink .git, scripts/sitemap_audit.py,
#   .ufo/waves/round-41/realrun, round-44/{classes,controls-r43}, round-45/{c45_audit.py,fixtures};
#   copy controls-27.tsv, c44_audit.py, c44_count_v5.py, c45_matrix.py
git -C lane-base rev-parse --verify '020bc457^{commit}'      # 020bc4574729ed674299f6cab02faac1582d9464
python3 -B .ufo/waves/round-44/c44_count_v5.py --root <lane> --classes v5 \
  --revision 020bc457 --out /tmp/probe-build.json            # met True, 21/21, 21.3 s
python3 -B probe_fixtures.py lane-{base,m2,m3}/.ufo/waves/round-45/c45_matrix.py
python3 -B probe_fixtures.py lane-m2acc/.ufo/waves/round-45/{c45_matrix_base.py,c45_matrix.py}
python3 -B lane-driftbase/.ufo/waves/round-45/c45_matrix.py --stage after   # FAIL exit 1
python3 -B lane-m1/.ufo/waves/round-45/c45_matrix.py --stage after          # PASS exit 0
```

## Files I wrote

Lane (only this report):
- `.ufo/waves/round-45/w2/MutMatrixRunner.md`

Scratch `/fast/scratch/hyaku/kake-r45/MutMatrixRunner/`:
- `probe_fixtures.py` (fixture-leg-only harness; imports a lane's `c45_matrix` and calls `run_fixture_leg`)
- `lane-m2acc/.ufo/waves/round-45/fixtures/stale-backdate/fake_counter.py` (accepted-invalid probe counter)
- `lane-{base,driftbase,m1,m2,m3,m2acc}/…` mirror trees (symlinks to lane inputs; per-lane
  `c45_matrix.py` copies, `c44_count_v5.py` copies, `verification/` output dirs)
- `lane-{driftbase,m1}/.ufo/waves/round-44/c44_count_v5.py` byte-drift shim (`_drift_probe`, 30th-invocation append)
- logs `log-driftbase.txt`, `log-m1.txt`, and `/tmp/probe-{ctl,build}.json`, `/tmp/kake45-drift-*`

Restoration: the lane was never mutated; no restore was required. Tools installed: none.
