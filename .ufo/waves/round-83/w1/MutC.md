# MutC — round 83 wave w1

Mutation-tested both frozen round-83 counters. **16 property mutants (8 per counter), all killed**;
**2 comment-only controls, both survived** (harness falsification control). The committed counters,
the classifier tool and the control/junk builders were never written: every mutant is a copy under
`/fast/scratch/hyaku/kake-r83/MutC/cases/<case>/`.

## Method

Two axes are scored for every mutant, against byte-identical material:

1. **self** — the mutant counter's own `--selftest`;
2. **fixture** — a tree built for exactly the property the patch breaks.

`killed` = the tuple `(exit code, the counter's own verdict line)` differs from the pristine
counter's on either axis. The comparison line is the `C1v1 …` / `C2v1 …` line, not the trailing
`# control=` / `# problems=` diagnostics (see Harness defects, item 2). Pristine and mutant runs are
handed copies of the same fixture directory, and `sha_tree` equality is asserted per mutant
(`tree_identical=True` in all 16 scored rows), so a difference cannot come from the tree.

Counter bytes measured (sha256 of the file, recorded in `matrix/matrix-all.json`):
`c83_defect_queue.py` `9fdfe84fc80c2218754ef486c4a9b5ee7f8621da7c9bc1ade9f13d8e1e3a985a`;
`c83_drift_class.py` `f7bcaeb1abe9acc92f238a2355a4244fa1fac478a001e1fe6d1be919bfb76c0f`.

## Harness defects hit, disclosed, and fixed before scoring

1. **Fixture bug (D4 erratum window).** The first fixture builder quoted `C1_FLEET_LINES[:4]`, but the
   amendment commit removes only `C1_FLEET_LINES[1:]`; the retained first line was quoted as an
   "erratum", so the *base* fixture read `D4 open … quoted=3` and five "mutant closes the item"
   readings would have been `open=2→1` rather than `1→0`. Fixed to quote only removed lines
   (`[1:1+quotes]`); fixtures and cases were deleted and rebuilt from scratch (`rm -rf cases fixtures
   receipts`) before any row was scored. No row in this report comes from the flawed build.
2. **Comparison-line bug.** The scorer first compared each run's *last* stdout line. For the C2
   counter that line is `# control=verdict=… validator=3`, which is identical across many mutants and
   masked the verdict line entirely (C2-m7 would have been scored `survived` for this reason). Fixed
   to extract the `C2v1`/`C1v1` line; the whole matrix was re-run and is deterministic (below).
3. **Round-82's defect class (path resolution) was designed out.** The C2 counter's selftest resolves
   its tool as `Path(__file__).resolve().parents[3] / TOOL`. Each C2 mutant therefore sits at
   `/fast/scratch/hyaku/kake-r83/MutC/cases/<case>/lane/.ufo/waves/round-83/c83_drift_class.py`
   with the tool at `<case>/lane/scripts/header_change_class.py`, so `parents[3]` is `<case>/lane`.
   Positive evidence that the layout is correct rather than merely plausible: the pristine copy at
   that exact layout scores **9/9, exit 0**, and the comment-only control survives both axes. No
   mutant row is red for a missing tool.

## C1 — `c83_defect_queue.py`

Pristine controls: `--selftest` 9/9 exit 0; synthetic green tree `open=0 met=true` exit 0; synthetic
junk tree (six prose "closed" lines, no state carriers) `open=6 met=false` exit 1.

| mutant | change (one point) | fixture / property broken | pristine | mutant | verdict |
|---|---|---|---|---|---|
| C1-m1 | D1 drops `settled_share >= 0.25` | 9 settled, 2 attack → share 0.2222; pristine `D1 open … settled_share=0.2222` | `open=1 met=false`, exit 1 | `open=0 met=true`, exit 0 | **killed** (fixture); selftest 9/9 |
| C1-m2 | D2 ignores `bytes_basis` | accounting `bytes_basis="chars"`, byte values correct; pristine `D2 open bytes_basis='chars'` | `open=1 met=false`, 1 | `open=0 met=true`, 0 | **killed** (fixture); selftest 9/9 |
| C1-m3 | D4 quote threshold `>= 4` → `>= 1` | lesson quotes exactly 2 of 4 removed lines; pristine `D4 open … quoted=2` | `open=1 met=false`, 1 | `open=0 met=true`, 0 | **killed** (fixture); selftest 9/9 |
| C1-m4 | D3 drops `bound == population` | receipt `population=30 bound=29 mismatches=0 met=true`; pristine `D3 open bound=29 population=30` | `open=1 met=false`, 1 | `open=0 met=true`, 0 | **killed** (fixture); selftest 9/9 |
| C1-m5 | D1 drops the `settled_attack >= 2` floor | 4 settled, 1 attack → share 0.25; pristine `D1 open … settled_attack=1` | `open=1 met=false`, 1 | `open=0 met=true`, 0 | **killed** (fixture); selftest 9/9 |
| C1-m6 | D5 drops the per-name `rows_ok` check | killer prints only `distinguished=5/5`, no rows; pristine `D5 open … rows=no` | `open=1 met=false`, 1 | `open=0 met=true`, 0 | **killed** (fixture); selftest 9/9 |
| C1-m7 | derived size `len(str)` instead of UTF-8 bytes | 4 seats × `"é"*150` = 150 chars / 300 bytes, accounting records 300 | `open=0 met=true`, 0 | `D2 open mismatched=['Alfa', 'Bravo', 'Charlie']` (counter prints the first three), `open=1 met=false`, 1 | **killed** (fixture, green→red); selftest 9/9 |
| C1-m8 | `run()`: `met = True` | contract junk tree, six prose-closed items, no accounting/receipt/killer | `open=6 met=false`, 1 | `open=6 met=true`, **exit 0** | **killed** (fixture); selftest 9/9 |
| C1-m0 | comment-only (`# mutc harness control`) | green tree — must not move | `open=0 met=true`, 0 | `open=0 met=true`, 0 | **survived** (control) |

Deltas on the scored line for m1–m6 are `open 1→0`, `closed 5→6`, `met false→true`; m7 is the
reverse direction (`0→1`, `true→false`), which proves the UTF-8 conjunct is live and not tautological;
m8 moves only `met false→true` (exactly the contract's kill rule: a junk control that reads `met=true`
means C1 is not scored).

## C2 — `c83_drift_class.py`

Pristine controls: `--selftest` 9/9 exit 0; synthetic green tree `met=true` exit 0 (all flags 1,
`diffs=6`).

| mutant | change (one point) | fixture / property broken | pristine | mutant | verdict |
|---|---|---|---|---|---|
| C2-m1 | `tool_offline` returns `True` unconditionally | tool gains `import socket`; pristine `tool_offline=0` | `tool_offline=0 … met=false`, 1 | `tool_offline=1 … met=true`, 0 | **killed** both axes (selftest 8/9) |
| C2-m2 | `flags["control_ok"] = 1` (result computed, then discarded) | control B replaced by an identical copy of control A; pristine `control_ok=0`, control line `verdict=same-object validator=0` | `control_ok=0 … met=false`, 1 | `control_ok=1 … met=true`, 0 | **killed** both axes (8/9) |
| C2-m3 | `header_class` maps `validator` → `per-request` | only `ETag` moved on s1; pristine `validator=1 verdict=representation-changed` | `validator=1 verdict=representation-changed control_ok=1 … met=false`, 1 | `validator=0 verdict=same-object control_ok=0 … met=false`, 1 | **killed** both axes (8/9); line-level, met held by `control_ok` |
| C2-m4 | `met` drops `diffs > 0` | captures A and B identical (`diffs=0`, `verdict=same-object`, every other flag green) | `diffs=0 … met=false`, 1 | `diffs=0 … met=true`, 0 | **killed** (fixture only); selftest 9/9 |
| C2-m5 | `record_equal` reduced to `rc1 == 0` | committed record replaced by `summary surfaces=3 diffs=9 verdict=same-object` | `record_equal=0 … met=false`, 1 | `record_equal=1 … met=true`, 0 | **killed** both axes (8/9) |
| C2-m6 | `content-length` classified `per-request` | only `Content-Length` differs on s1 (5→6), body identical; pristine `representation=1 verdict=representation-changed` | `representation=1 … met=false`, 1 | `representation=0 verdict=same-object … met=true`, 0 | **killed** (fixture only); selftest 9/9 |
| C2-m7 | receipt gate drops `truncated is not False` | capture-B s1 receipt `truncated=true`; pristine `surfaces_b=2 receipts_ok=0 verdict=none determinism=0` | `surfaces_b=2 receipts_ok=0 … met=false`, 1 | `surfaces_b=3 receipts_ok=1 diffs=6 verdict=same-object … met=false`, 1 | **killed** (fixture only); selftest 9/9 — **line-level kill**, see finding 3 |
| C2-m8 | `flags["met"] = True or (…)` | identical captures; every other flag green | `diffs=0 … met=false`, 1 | `diffs=0 … met=true`, 0 | **killed** both axes (selftest 1/9) |
| C2-m0 | comment-only (`# mutc harness control`) | green tree — must not move | `met=true`, 0 | `met=true`, 0 | **survived** (control) |

## Findings

1. **The C1 counter's own selftest does not exercise its conjuncts.** All 8 C1 mutants survive
   `--selftest` at 9/9. The selftest pins exactly one instantiation per item and scores `evaluate()`
   (row booleans), never `run()` (the `met` aggregation). Consequences, each demonstrated above:
   the D1 fixture empties the only reviewer seat so *record-field equality* — not the `>=2` floor —
   is what turns it red (m5 survives); the D2 fixture changes a value rather than the basis (m2);
   the D4 fixture removes all quotes rather than some (m3); the D3 fixture fails `mismatches` (m4);
   the D5 fixture reduces the summary count (m6); and no fixture has non-ASCII output (m7). m8 is the
   structural case: a mutant confined to `run()` is invisible because `run()` is never scored.
   The counter is nonetheless correct — these are selftest coverage gaps, not property defects.
2. **C2's selftest is substantially stronger, with three named holes.** m1, m2, m3, m5 and m8 are
   killed by the embedded selftest (8/9, or 1/9 for m8). m4, m6 and m7 survive it because no fixture
   has (a) `diffs = 0`, (b) a `Content-Length`-only change, or (c) a truncated receipt. External
   fixtures kill all three.
3. **C2-m7 is a line-level kill, and that is a redundancy rather than a hole.** Deleting the
   counter's `truncated` check moves `surfaces_b 2→3`, `receipts_ok 0→1` and `verdict none→same-object`,
   but `met` stays `false` because `determinism` and `record_equal` also fail — the tool's
   `load_surface` performs the identical receipt validation, so any receipt defect the counter can see
   the tool sees too. `receipts_ok` can therefore never be the sole reason `met` flips. Defense in
   depth, but it means this conjunct is only observable in the printed line. (Analogous to round-82's
   `m3` "equivalent mutant — sha256 equality already implies equal length".)
4. **C2's validator property is guarded from both sides.** C2-m3 cannot reach `met=true` even in
   principle: the main captures require `validator == 0 ∧ verdict == same-object`, while the control
   pair requires `validator >= 1`; a classifier that stops counting validators fails one or the other.
   The same mutant is also caught by the selftest, so this is triple coverage.
5. **Determinism.** The full matrix was run twice from a clean build. `(exit code, verdict line)` for
   all 18 rows and all 17 pristine fixture readings are identical across runs. C2's fixtures are
   byte-identical across runs (sha256 equal for all 8); C1's non-junk fixtures differ only in the
   fixture fleet's commit hash, which changes with commit timestamps and is embedded in the lesson's
   D4 line — the `junk-prose-only` tree, which has no fleet reference, is byte-identical. Pristine
   and mutant trees within each run are equal (`tree_identical=True`, 16/16). Receipts:
   `matrix/matrix-run1.json` vs `matrix/matrix-all.json`, `run1.log`, `run2.log`.

## Commands and exit codes

All commands were run with `TMPDIR=/fast/scratch/hyaku/kake-r83/MutC/tmp`; absolute paths only.

| # | command | exit |
|---|---|---|
| 1 | `python3 -B /…/kake-shokunin/.ufo/waves/round-83/c83_defect_queue.py --selftest` | 0 (`selftest: 9/9 passed`) |
| 2 | `python3 -B /…/kake-shokunin/.ufo/waves/round-83/c83_drift_class.py --selftest --work /fast/scratch/…/tmp/c2-final` | 0 (`selftest: 9/9 passed`) |
| 3 | `python3 -B /fast/scratch/hyaku/kake-r83/MutC/mutc.py c1` | 0 |
| 4 | `python3 -B /fast/scratch/hyaku/kake-r83/MutC/mutc.py c2` | 0 |
| 5 | `python3 -B /fast/scratch/hyaku/kake-r83/MutC/mutc.py all` (clean build, run 1) | 0 |
| 6 | `python3 -B /fast/scratch/hyaku/kake-r83/MutC/mutc.py all` (run 2, determinism) | 0 |
| 7 | `git -C /…/kake-shokunin hash-object <file>` vs `git -C … rev-parse HEAD:<file>` for both counters and the tool | equal, all three |
| 8 | `git -C /…/kake-shokunin status --porcelain -- .ufo/waves/round-83 scripts/header_change_class.py` | no `M` rows; only untracked wave artefacts |
| 9 | `cp -a` of receipts into `.ufo/waves/round-83/w1/MutC/` | 0 |

Per-mutant detail (change, fixture, both runs, both axes) is in `matrix/matrix-all.json`; unified
diffs of each mutant against the frozen counter are in `diffs/`; the harness is `mutc.py`; pristine
item-level output for every fixture is `matrix/pristine-fixtures.txt`.

## Non-mutation / restoration evidence

The two counters and `scripts/header_change_class.py` in the lane are byte-identical to the freeze
commit `64b7199281e5457df0e08652977f698c4f34f46e` (blob hashes: `6a97b375…`, `17a2178f…`,
`d26c3e0d…`; `git log` for each path shows only that commit). No VCS mutation was issued: the fixture
fleet is a standalone `git init` under scratch whose `--show-toplevel` was asserted before its first
commit, and every later git call used `-C <fixture>`. All mutants lived under
`/fast/scratch/hyaku/kake-r83/MutC/`; that tree was deleted after the receipts were copied here
(`rm -rf /fast/scratch/hyaku/kake-r83/MutC`, verified absent below).

## Verdict

Both counters **die when the property they claim breaks**: 16/16 property mutants killed (C1 8/8,
C2 8/8), including every conjunct named in the tasking (`share`/attack floor, `bytes_basis`, D4 quote
count, D3 `bound==population`, D5 rows; `tool_offline`, `control_ok`, validator classification,
`diffs>0`, `record_equal`, representation class, `truncated`). The counter is **not** uniformly
defended by its own selftest: C1's selftest is blind to all 8 of its mutants (m1–m7 at conjunct
level, m8 at the `run()` aggregation the selftest never calls), and C2's is blind to 3 of 8 —
coverage finding for the C1 `selftest_ok` conjunct, not a claim failure, since the counters
themselves measure the property correctly on external fixtures. Harness integrity is demonstrated, not assumed: both comment-only controls
survive, the pristine counters read green on a synthetic green tree, and no row is red for a path or
syntax reason. Round-82's path-resolution defect does not recur (`parents[3]` layout with 9/9
pristine selftest at that layout).
