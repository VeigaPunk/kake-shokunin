# MutC1Counter — mutation probe of the C1 counter (round 70, W1)

Base `e5f6fd9e4c243d092160bc74e8bea24256087173`. Scratch clone at that revision; each fixture is
its own git repo under `/fast/scratch/hyaku/kake-r70/MutC1Counter/fx.*` (`rev-parse --show-toplevel`
verified equal to the fixture before the first commit; commits made with
`-c user.name=kake-seat -c user.email=seat@fixture`).

SUT: `.ufo/waves/round-70/w1/ExecC1Counter/c70_pointer_audit.py`, 12590 bytes, sha256
`3e4958fc1a2971c418ff42317ea6fe204e3c312353c37f7a85d71d37ae45a43e` (lane artifact; identical bytes
were first seen in ExecC1Counter-2's scratch clone at 16:38). Every verdict below was re-executed
against the lane artifact after it landed. No lane tracked file was edited; no tool was installed
(pacman paused host-wide; nothing was needed). An independent contract-faithful reference
(`ref_c70_pointer_audit.py`, retained) was used while the artifact was absent; it agreed with the lane
artifact on F1–F5, and its base run is retained as `receipt-ref-base.txt`.

## Assigned mutants (F1–F5, same bounded detector on each)

| # | Mutant in fixture bytes | Required behaviour | Actual (summary; exit) | Verdict |
|---|---|---|---|---|
| F1 | row first cell `/tmp/kake-r1` (line 11) for body token `/tmp/kake-r10` (line 5) | not annotated → `unannotated>=1`, exit 1 | `pointers=2 dangling=2 annotated=1 unannotated=1 met=false`; exit 1; `tmp unannotated line=5 token=/tmp/kake-r10`, `tmp annotated line=11 token=/tmp/kake-r1` | killed |
| F2 | exact-token row at line 12 inside `<!-- ... -->` (lines 9–13) | not annotated → exit 1 | `pointers=1 dangling=1 annotated=0 unannotated=1 met=false`; exit 1 | killed |
| F3 | exact-token row at line 11 under `## Pointer calibration (round 69)` (line 7) | not annotated → exit 1 | `pointers=1 dangling=1 annotated=0 unannotated=1 met=false`; exit 1 | killed |
| F4 | exact-token row at line 11 in `## Pointer calibration (round 70)`; resolving repo pointer `scripts/probe.sh` in body | annotated, `met=true`, exit 0 | `pointers=2 dangling=1 annotated=1 unannotated=0 met=true`; exit 0 | expected green: honest control passes |
| F5 | body token `.ufo/waves/round-70/ghost.md` (line 5) exists only in the working tree (`?? .ufo/`) | stays dangling at the revision → exit 1 | `pointers=1 dangling=1 annotated=0 unannotated=1 met=false`; exit 1; detail `repo unannotated line=5 token=.ufo/waves/round-70/ghost.md`; `git cat-file -e 02e1f59:.ufo/waves/round-70/ghost.md` → fatal `exists on disk, but not in '02e1f59...'` | killed |

No assigned mutant the design should reject was accepted: F1–F5 all produce the contract's expected
summary line and exit code.

## Pristine / mutated / restored cycle (F4 repo; smallest behaviour-bearing point = row's first cell)

| State | Revision | `SCORECARD.md` sha256 | Summary | Exit |
|---|---|---|---|---|
| pristine | `0d8afca46d4fa66aa74d94cbf44cfca0fffe14b3` | `c58deb6137e8c55e8646798166a605eb755d61fb1444da9218895a5af5454a04` | `pointers=2 dangling=1 annotated=1 unannotated=0 met=true` | 0 |
| mutated (cell → `/tmp/kake-r1`) | `9dc639b1d5d5782622be5667b8d29c888f378f44` | `4d8a9ec8c34203df1af450c5053eef99ffa3683cbdf344c076b5c059c78f55fb` | `pointers=3 dangling=2 annotated=1 unannotated=1 met=false` | 1 |
| restored (exact pristine bytes) | `5b669e41c3bf1a0524994fb4b6232786ab1814a6` | `c58deb6137e8c55e8646798166a605eb755d61fb1444da9218895a5af5454a04` | `pointers=2 dangling=1 annotated=1 unannotated=0 met=true` | 0 |

Restoration evidence: restored sha256 equals pristine sha256; the detector is green before, red only
while the mutation is committed, green again after exact-byte restore.

## Controls (same detector, lane artifact)

- Selftest: `python3 -B <SUT> --selftest --work /fast/scratch/hyaku/kake-r70/MutC1Counter/selftest-work`
  → cases a–e ok, `selftest 5/5`, exit 0.
- Do-nothing control at base: `--root <clone> --revision e5f6fd9e...` →
  `pointers=348 dangling=19 annotated=0 unannotated=19 met=false`, exit 1. Kill rule satisfied (base is
  not green). Danglers: 3 home, 8 repo, 8 tmp. Host-state note: `/tmp/kake-r16` exists on this host
  (created 15:50), so it resolves and is not in the dangling set; the contract's own host-state rule
  makes this set time-dependent.

## Adjacent probes (not in the assigned five; same detector, same scratch)

- F6 backticked first cell: row at line 11 `` | `/tmp/kake-r10` | ... `` → `annotated=0 unannotated=1`,
  exit 1. Strictness note, not a falsification: the section's row cells must be bare tokens; a
  backticked cell does not annotate, so the annotation section must not backtick the pointer cell.
- F7 row inside a fenced code block (lines 9–13; exact accepted line `fixtures/F7-SCORECARD.md:12`:
  `| /tmp/kake-r10 | historical: scratch-discipline cleanup (2026-11-03) |`) → `pointers=1 dangling=1
  annotated=1 unannotated=0 met=true`, exit 0. **Falsification candidate:** a fenced line is not a table
  row under CommonMark, so the frozen locus sentence (“a table row in that section”) does not grant this
  annotation; the counter strips only HTML comments (`annotation_cells` → `strip_comments`) and credits
  it. The frozen text is silent on fences (the analogous `append_guard` excludes comments and code
  spans), so this is named for the L1 to rule, not asserted as a contract change.

## Verdict and limits

- Assigned mutants F1–F5: 5/5 killed by the lane artifact; the four reject-cases are rejected and the
  honest case passes. F1 confirms exact-token first-cell matching; F2 comment-awareness; F3 section
  specificity; F5 revision bytes (not worktree).
- Surviving mutant: F7 only, named above with its exact line; it does not affect F1–F5.
- Probe bound: verdicts pin SUT sha256 `3e4958fc...`. If ExecC1Counter rewrites the artifact after this
  report, these receipts are stale and must be re-run.

## Reproduction

`python3 -B .ufo/waves/round-70/w1/ExecC1Counter/c70_pointer_audit.py --root <fixture> --revision <rev>`
per row; fixtures rebuilt by `build_fixtures.sh` (F1–F5) and by copying `fixtures/F6|F7-SCORECARD.md`
into a fresh `git init` repo and committing. Receipts: `receipt-counter-lane-artifact-fixtures.txt`,
`receipt-counter-mutate-restore.txt`, `receipt-counter-selftest-base.txt`, `receipt-counter-adjacent.txt`,
`receipt-counter-sha256.txt`; fixture bytes retained under `fixtures/`. Scratch
`/fast/scratch/hyaku/kake-r70/MutC1Counter` was removed after the runs.
