# Review: c44_count_v5.py vs c43_count_v4.py — counter contract

Seat: ReviewCounterContract. Reviewed the frozen, uncommitted counter v5
`.ufo/waves/round-44/c44_count_v5.py` (1,124 lines) against the round-43 v4 it derives from,
`.ufo/waves/round-43/c43_count_v4.py` (1,075 lines), and the builder `.ufo/waves/round-44/build_v5.py`.
All paths under `/home/vgpnk/Projects/shokunin/kake-shokunin`. No files modified; no installs needed
(python3, diff, coreutils already present).

## (1) build_v5.py --check — verdict: sound

Command (from the lane root):

    $ python3 -B .ufo/waves/round-44/build_v5.py --check; echo "EXIT=$?"
    current sha256: 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
    built   sha256: 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
    EXIT=0

The bytes rebuilt from the committed v4 source equal the committed-in-workspace v5 file exactly.
`build_v5.py:128-137` applies eight anchor-unique replacements and exits non-zero if any anchor is
not unique (`:133-134`); `--check` (`:142-147`) compares `OUT.read_text()` against the rebuilt text
byte-for-byte. The extra `text.replace('"""Round-43 C1 counter', ...)` at `:136` is a no-op today —
`OLD_HEAD` already replaced the only docstring-prefixed occurrence; embedded provenance headers
inside the docstring carry no `"""` prefix. Harmless.

## (2) Diff scope — verdict: sound

`diff -u c43_count_v4.py c44_count_v5.py` yields exactly 8 hunks (62 insertions, 12 deletions).
Every hunk, with v5 line numbers:

| Hunk | v5 lines | Content | Verdict |
|---|---|---|---|
| `@@ -1,10 +1,14 @@` | 2-11 | Header: provenance sentence + description of the ten class runs and the blind spots they close | header only |
| `@@ -75,9 +79,9 @@` | 82-84 | `PREDICATE` sentence rewritten to name "the eleven v4 runs and the ten class runs" | predicate only |
| `@@ -91,6 +95,20 @@` | 98-110 | `CLASS_DIR` + `CLASS_MODULES` tuple (G1-G10 → `gN_*.py` filenames) | class wiring |
| `@@ -115,6 +133,27 @@` | 136-152 | `load_classes(root)` — loads each module via importlib, requires `cases`, raises `CannotEvaluate` on missing file/function | class wiring |
| `@@ -947,6 +986,9 @@` | 989-991 | `--classes {v5,v4}` argparse flag, default `v5` | flag |
| `@@ -954,7 +996,10 @@` | 999-1002 | receipt gains `classesMode` and `classRuns` fields; `toolSha256` moved to its own line | receipt record only — not consulted by `equal`/`met` logic |
| `@@ -998,9 +1043,11 @@` | 1046-1050 | `classes = load_classes(root) if a.classes == "v5" else {}`; runs list split: A-F, then `[(key,None) for key,_ in CLASS_MODULES if key in classes]`, then T1-T5 | class wiring / runs list |
| `@@ -1013,6 +1060,9 @@` | 1063-1065 | `elif key in classes:` branch — `units, n = classes[key].cases(rng, sys.modules[__name__])`, laid out by the existing `layout_f` | class wiring |

Nothing outside these hunks differs. Runs A-E still dispatch to `layout_cases` (`:1056-1059`),
F to `cases_f`/`layout_f` (`:1060-1062`), T4 to `shape_t4` (`:1066-1068`), T1/T2/T3/T5 to their
shape generators (`:1069-1071`) — identical code to v4 `:1009-1021`. The equality test
(`c_code == ref_code and c_out == ref_out`, `:1077`), the T-run REP loop and ratio computation
(`:1081-1104`), `equalRuns`/`equalValues` (`:1109-1110`), and the `met` conjunction
(`equal == len(runs) and len(ratios) == 5 and ratios_ok`, `:1111-1112`) are byte-identical to v4.
The class branch reuses `layout_f` and the same `box.run` comparison, so class runs inherit the
exact run-F equality semantics; `cases(rng, h)` receives `h = sys.modules[__name__]` (the counter
module itself), matching the documented class-module contract.
Equality/timing semantics of A-F and T1-T5: unchanged.

## (3) Predicate sentence vs code — verdict: sound

`PREDICATE` (`:82-84`): "the tool's exit code and output equal the round-41 tool's on every
generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the
five timing shapes is at most 2.0 times the round-40 tool's".

- "eleven v4 runs and the ten class runs" — runs list is A-F (6) + G1-G10 (10) + T1-T5 (5);
  every generated run gets `entry["equal"]` from the same `box.run` comparison (`:1072-1079`),
  and `met` requires `equal == len(runs)` (`:1112`). Consistent.
- "five timing shapes" / "median CPU" — `if key.startswith("T")` (`:1081`) runs `REPS = 5`
  reps (`:86`, `:1084`), alternating base40/cand order; ratio = `median(cand)/median(base)`
  (`:1100`). `ratios_ok` requires exactly 5 exact ratios (`:1111`).
- "2.0 times" — `RATIO_LIMIT = 2.0` (`:85`), enforced at `:1111`.
- "the round-40 tool's" — `BASE40_REV`/`BASE40_SHA` (`:90-91`), fetched and hash-pinned at
  `:1018-1022`, run as `paths["base40"]`. Unchanged from v4.

## (4) Run denominators — verdict: sound

Derived from the code by exec'ing the module and replaying lines 1046-1050 without bwrap/git:

    v5 runs: 21 ['A','B','C','D','E','F','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','T1','T2','T3','T4','T5']
    v4 runs: 11 ['A','B','C','D','E','F','T1','T2','T3','T4','T5']

`rec["equalRuns"]` formats `"%d/%d" % (equal, len(runs))` (`:1109`), so the denominators are
21 in v5 mode and 11 in v4 mode. `RATIO_LIMIT 2.0 REPS 5` confirmed live from the module.

## (5) `--classes v4` cannot produce class runs — verdict: sound

- `:1046` — `classes = load_classes(root) if a.classes == "v5" else {}`: in v4 mode
  `load_classes` is never called, so no class module is even opened/imported.
- `:1049` — `runs += [(key, None) for key, _ in CLASS_MODULES if key in classes]`: with
  `classes == {}` the filter admits nothing; zero class runs are generated.
- `:1063` — the `elif key in classes` dispatch is unreachable in v4 mode (no run key is in `{}`).
- `:1001` — `classRuns` receipt field is `[]` in v4 mode; `classesMode` records `"v4"`.

## Residual risk / nits (not defects)

- `load_classes` hard-requires all ten files under `.ufo/waves/round-44/classes/` and raises
  `CannotEvaluate` (exit 2) on any missing one (`:144-145`). At review time only five exist in the
  workspace (`g2,g4,g5,g6,g8`); wave-1 executors are still writing the rest. Expected mid-wave
  state, but any v5-mode invocation before all ten land exits 2 by design.
- `here = sys.modules[__name__]` at `:139` is an unused local (the branch at `:1064` repeats the
  expression instead). Dead line in a frozen file; zero semantic effect.
- In v5 mode the ten G runs consume `rng` between F and T1, so T1-T5 see a different RNG stream
  than the same seed would give in v4 mode. Inherent to appending runs; v4-mode stream is
  bit-identical to the v4 counter. Not a defect.

## Commands run (verbatim where decisive)

    python3 -B .ufo/waves/round-44/build_v5.py --check        → EXIT=0, sha256 match (above)
    diff -u .ufo/waves/round-43/c43_count_v4.py .ufo/waves/round-44/c44_count_v5.py   → 8 hunks (table above)
    python3 -B -c '<module replay of :1046-1050>'             → 21 / 11 run keys (above)
    glob .ufo/waves/round-44/classes/*                        → 5 of 10 modules present at review time

Overall: the v5 counter is a strict superset build — all five reviewed items **sound**; the only
discrepancy-class observations are the two nits above, neither of which changes equality or timing
semantics.
