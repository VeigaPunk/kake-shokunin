# ReviewInheritedLineage — Kake r44 w1, leaf seat (build + pre-freeze calibration)

Scope: re-verify the six inherited round-44 artifacts attempt 1 left uncommitted, and adjudicate
reuse vs discard for attempt 2. Lane lens: R44 build chair (operability). Member seat: no
subagent dispatch. All commands ran as the lane user from the lane repo root
`/home/vgpnk/Projects/shokunin/kake-shokunin`; no fleet/sibling edits; nothing outside the lane
repo was written except this report (named path), the scratch dir, and the scratch files below.

## Environment and provenance
- Branch state: `git status --porcelain -- .ufo/waves/round-44` → `?? .ufo/waves/round-44/`
  (the entire directory is untracked; the r43 dir is tracked, r44 is not). So every artifact
  below is inherited *uncommitted* from attempt 1, exactly as stated.
- `sha256sum .ufo/waves/round-43/c43_count_v4.py` =
  `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab` — matches the expected
  value. The v5 build input is the correct byte-for-byte r43 v4 counter.
- Scratch: `/fast/scratch/hyaku/kake-r44/ReviewInheritedLineage/` — `hashes-root.txt`,
  `hashes-controls.txt`, `probe-g5-seed42.txt` (all outputs below were also captured there).

## Per-artifact rows

| Artifact | sha256 | Re-derivation command + result | Verdict |
|---|---|---|---|
| `build_v5.py` | `783bb16fc53bddfd3f1576b8a272d9675d38389ffc94f3780a764ee688e34c07` | `python3 -B .ufo/waves/round-44/build_v5.py --check` → prints `current sha256: 5cedaa3b…` / `built   sha256: 5cedaa3b…`, `EXIT=0` | **reuse** (idempotent validator; deterministic byte-exact from r43 v4) |
| `c44_count_v5.py` | `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc` | the same `build_v5.py --check` (it rebuilds the module in memory from `c43_count_v4.py` and compares; printed sha matches disk) | **reuse** (re-derives identically; also the sha the freeze JSON pins) |
| `c44_audit.py` | `e88a0309825ef0e62e0dd64a41d1c66fdea27db29436c7b2fd200a1d6aa6e689` | no independent rebuild exists; observed live-rewritten mid-window (see finding F1) | **reuse with caution / freeze at label** (see F1) |
| `controls-27.tsv` | `233afa37d6ce85b0cbbedba8fe941de25f96d13773d3d388d68cbd9ab182eb57` | python: 27 rows; sha256 of all 27 `controls-r43/*.py` vs TSV `sha256` column → 0 mismatches | **reuse** |
| `controls-r43/` (27 tools) | per-file hashes in `hashes-controls.txt` (all match TSV; e.g. `portlen-v1…` `752a8de5…`, `repeat-depth-deep…` `7eb373f2…`) | `python3 -B -m py_compile .ufo/waves/round-44/controls-r43/*.py` → exit 0 (all parse) | **reuse** |
| `verification/freeze/control-v4blind.json` | `4957875178e5c1519b9f4584d115f9b8da94e2bb6e3eb31d2ca3c1696fc43158` | read-only; no rebuild exists | **discard as evidence / keep as provenance** (see F2) |

Class modules (`classes/`, required by v5 and by the probe): exist now — G1, G2, G3, G4,
G5, G6, G7, G8, G10 (`g1_longport_grammar.py … g10_headtail_windows.py`; all expose
`cases(rng, h)` and compile; hashes recorded at 20:10–20:11; **G9 is missing** — only a
placeholder `classes-placebo/g9_port_digits.py` exists (see F3); probe smoke on G5
(`--class G5 --tool-file …headtail-V1-prefix-cache64.py --seed 42`) ran end-to-end and
produced a semantic witness (exit 1: `equal: false`, ref41 vs candidate output sha
`4d4cdbfa…` vs `0b2dedd9…`, per-entry status divergence), so the probe/counter harness is
functional (see F4).

## Findings

### F1 — `c44_audit.py` is a moving target (operability)
`stat` mtimes: `c44_audit.py` `20:10:49` → `20:11:03` (final). At 20:10 it did **not parse**
(duplicate keyword on line 151), at 20:11 it compiles. The inherited audit driver is not a fixed
artifact to freeze; a peer is actively editing it. The verdict is reuse only if the L1 freezes
the *specific* byte (label + sha) of the audit run, not "the audit file" as a name.
`.ufo/waves/round-44/classes-placebo/` also exists (contains `g7_band_memos.py`,
`g9_port_digits.py` placebos — v4 skip-work scaffolding), which c44_audit.py does not use; a
clean freeze should decide whether it stays.

### F2 — `control-v4blind.json` proves less than the statement implies
It is a v4-mode audit receipt (`classesMode: v4`, `classRuns: []`, `ok: false`,
`verdict: "witnessed 2/27"`), dated 19:40 — before the wave's own runs (20:03+). Per-row
receipts (`tools/*.json`, 27 files, each ~5 KB) show 2 witnesses (buildscope-m5 D; repeat-depth-deep
C, `equalRuns 10/11`), 25 met, 0 errors. Crucially, **`"build": []`** — the held build
(revision 020bc457) was *not* scored by this receipt, so it proves at most that the v4 corpus
is (mostly) blind *for the current count file*, **not** the round's C1 (witness under v5) nor
the build-meets-v5 claim. Also the `tools/` directory is **not** empty (27 receipt files) — the
claim that it is empty does not hold for on-disk state; the freeze does not itself contain
control results under the `verification/freeze/` root, its receipts do. What it does not prove:
any v5 run, any build run, any verdict on the round-42 red controls, `ok=true` semantics at
freeze time (it is a knowing-witness baseline). If attempt 2 needs v4-blind as a gate, it must
re-run it against the frozen bytes; `ok=false` means, by the driver's own `expectation_ok`
("blind" → exit 0 iff witnessed == 0), the *current* file is **not** a passing "blind" gate (2 ≠ 0).

### F3 — G9 class module missing; v5 class runs cannot run today
`CLASS_MODULES` (build_v5.py, and the counter) requires all ten modules; `load_classes` raises
`CannotEvaluate("class module missing: …")` if any is absent. Current `classes/` has 9 of 10:
G1–G8 and G10; G9 `g9_port_digits.py` is absent (only the placebo, under `classes-placebo/`).
The v5 counting command (and `--classes v5`) therefore cannot pass today. G9 is assigned to a
live peer (ExecG9PortDigits "Reading inverted branch exact code"); the executor/W1 freeze must
decide whether G9 ships before freeze, or the class list shrinks.

### F4 — probe on G5 works (WITNESS expected, so okay)
The G5 probe produced a semantic divergence (exit 1, `equal: false`, candidate judged 2 of 4
entries clean where ref41 flagged `loc_not_absolute`). This is the *desired* witness behavior
for the control under test (headtail-V1 prefix-cache64); it confirms the counter+probe harness
is operational end-to-end. It is **not** evidence of a counter defect.

## Reuse / discard table
- **Reuse as-is:** `build_v5.py`, `c44_count_v5.py` (re-derive byte-exact), `controls-27.tsv`,
  `controls-r43/` (0 hash mismatches, all parse; these are the round-43 verified controls).
- **Reuse with condition:** `c44_audit.py` — freeze the exact bytes at label time; do not
  freeze "the audit file" while peers edit it (F1).
- **Discard for the claim:** `verification/freeze/control-v4blind.json` — it predates this
  attempt's freeze, carries no build rows, and does not support either claim (F2); keep it only
  as round history.
- **G9 class module** — required by v5; missing; must be supplied or the v5 class set must be
  re-scoped before freeze (F3).

## Verification gaps / risks
- The audit driver was mid-edit during this review; its final byte-level behavior (exit codes,
  `--expect` semantics, receipts) should be re-smoked by the main agent after freeze.
- `control-v4blind.json`/`tools/` are dated 19:40, before this wave's runs; if the claim wants a
  fresh v4-blind baseline, it must be re-run against the frozen artifacts.
- This review performed no full counter run (20+ min); only the probe (one class run), `--check`,
  py_compile, and receipt inspection were exercised.
- G9 absence is the only hard blocker for a v5 run today.

Report files written: this file; scratch: `hashes-root.txt`, `hashes-controls.txt`,
`probe-g5-seed42.txt` (`/fast/scratch/hyaku/kake-r44/ReviewInheritedLineage/`).
