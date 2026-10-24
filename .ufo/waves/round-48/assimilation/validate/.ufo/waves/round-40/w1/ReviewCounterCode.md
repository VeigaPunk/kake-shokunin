# ReviewCounterCode — attack on the frozen r40 C1 counter (wave 1)

Axes: operability (can the counter be made to pass a wrong tool / fail a right one), freshness (does it still measure the declared C1). No tools installed. No tools scored as controls; the two tools below were scored as run-matrix ground truth.
Counter sha256 `6d73b8f498a29a5a86c9a7f1ce5d87cd135c40f1b634d869d14659cc10bee8d8` = SCORECARD pin; frozen selftest sha `99ee9bbf…93351db` = pin. Lane HEAD has moved to `12211cc5` (sibling commits); base runs pinned `--revision f043c721…` explicitly.

## Runs (`timeout 1200 python3 -B .ufo/waves/round-40/c1_count.py --root <lane> …`, receipts + logs in `/fast/scratch/hyaku/kake-r40w1/ReviewCounterCode/`)
- base `f043c721`, seed 40001 → passed 10, E 4/9 U 3/13 R 3/8, selftest exit 0 "PASS 150/150", met false, EXIT=1
- base `f043c721`, random seed 209225254507129 → identical totals, EXIT=1 (matches SCORECARD "Before" exactly at both seeds)
- ref_fix seed 1701 → passed 30, E 9/9 R 8/8 U 13/13, selftest 150/150, met true, EXIT=0
- ref_fix random seed 167157884336518 → same, met true, EXIT=0
- ref_fix seed 1701 rerun → rows identical (receipts differ only in `label`); different seeds give different hosts/dirs/ids (`w5y34gpkd` vs `wok87j6ze`), same-seed replay exact. toolSha base `6d86c8ce…`, ref `03a8fba4…` — both match SCORECARD.

## Findings
- **F1 MEDIUM — cannot-evaluate collapses to not-met with no receipt.** `c1_count.py:237` (`git rev-parse --verify` unguarded), `:263` and `:278` (only `TimeoutExpired` is caught, `:265`/`:284`), `:219` (`finish`'s own `open`). Repro 1: `python3 -B .ufo/waves/round-40/c1_count.py --root . --revision 0000000000000000000000000000000000000000 --out badrev.json` → `CalledProcessError` traceback, EXIT=1, no receipt, no stdout summary. Repro 2 (PATH without bwrap, git symlinked): `FileNotFoundError: 'bwrap'`, EXIT=1, no receipt. Exit 2 is reachable only for selftest-fetch/sha failures. A scorer keying on exit alone records "not met" for an unevaluable run and loses the audit receipt. Not exploitable to pass a wrong tool.
- **F2 LOW — judge normalisation lenience, false-accept only.** `c1_count.py:170`: `doc.get("version") != 1` accepts `"version": true` (True==1) and `1.0`; `json.loads` makes duplicate keys last-wins (`{"version":9,"version":1}` passes). `norm` `:152-158` accepts list-form findings (`[["loc_not_absolute",1]]`) and `entry: true` ≡ 1 (verified at witness level: U1 with entry `true` → "match"; E1 dup-verdict → "match"). Sentence 33 is stricter than the judge, but every mutant still needs correct exit, verdict, id, status, error and finding set per case — no declared work is skipped, so no control class gains.
- **F3 LOW — misleading failure diagnostics.** `:184-186` mismatch message prints only status/error/findings, never `id`; the R6 "echo int id" probe fails correctly but reports `got error/check_invalid/[] want error/check_invalid/[]`. Receipt `why` fields can look identical for different defects (audit friction, verdicts unaffected).
- **F4 INFO — regression half is unsandboxed.** `:278` runs the tool directly (no bwrap) in the tempdir that still holds all 30 witness case dirs; a tool can detect selftest context (real tempdir argv[0] + inherited env vs sandbox argv `/tool/tool.py --manifest /work/manifest.json` + clearenv — probe verified env is exactly PATH/LANG/PYTHONHASHSEED, cwd /work). No scoring shortcut found: the predicate still requires a genuine 30/30 and 150/150. SCORECARD's unqualified "The tool runs in bubblewrap" is overstated for this half.
- **F5 INFO — receipt rows carry no random token** (labels static; `why` strings exclude ids/hosts), so rows are byte-identical across seeds by construction. Don't misread cross-seed row equality as seed not applied — the manifests do differ (verified).

## Per attacked statement
- Seed handling — **holds**: per-seed variation + exact replay + receipted seed.
- Sandbox argv — **holds** for witnesses: bwrap load-bearing (absent → crash), argv/cwd/env as declared, no label/seed/revision visible to the tool.
- Judge — **holds** against work-skipping: status-flip, id-wrong, false-positive, verdict case, prefix junk, BOM, array doc, NaN, unhashable finding code, check reorder (multi-check R5/R6) all fail; single-check witnesses can't expose reorder (no-op). Overstated only per F2 leniences.
- Selftest summary parsing — **holds**: frozen selftest prints exactly one `PASS n/total` (`selftest_frozen.py:1054`), exit 1 on any failure/coverage gap; counter demands exit 0 and exact "PASS 150/150" (`:286`); per-case `FAIL` lines can't spoof (`PASS `-with-slash preferred, bare `FAIL` summary ≠ target).
- Exit mapping — **overstated**: 0/1 verified on the normal paths; 2 not reachable for environment/tool-absent-at-revision failures (F1).
- Freshness — **holds**: counter and selftest shas match pins; base before-totals reproduce exactly at two seeds; ref_fix meets 30/30+150/150 at two seeds (no counter-detection in its diff: plain control-char guard, NUL check, duplicate-id ordering).

Verification gaps: network isolation cited from `--unshare-all` argv, not empirically tested; no bwrap-escape fuzzing; the 150 selftest fixtures trusted via sha pin, not re-audited. No control meeting the predicate was found or needed — this seat did not build one.
