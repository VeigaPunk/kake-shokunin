# ExecC2SeedSweep

Seat scope: attack item "Claim C2 gate determinism" for round-59 w1. Read-only attack: run the frozen
version-1 counter `.ufo/waves/round-59/c59_resolver_cases.py` against the **base** revision
`fd6303ce5c14b3f892dec586297a942ab6e4193b` of lane `kake-shokunin` under many seeds and hostile
environments, recording whether the per-case verdict vector is seed-independent and whether the counter
leaves scratch behind. No after-state was scored (counters are VERSION 1; wave 1 attacks before any claim
is measured). No lane, sibling-lane, jj-state or Git-index mutation was performed by this seat.
Environment: Python 3.14.8, Linux, host loaded; lane root verified with `git rev-parse --show-toplevel`.
All scratch under `/fast/scratch/hyaku/kake-r59/ExecC2SeedSweep/`, removed after the receipts were
copied into `.ufo/waves/round-59/w1/ExecC2SeedSweep.files/seed-sweep-receipts.txt`. No tool was
installed (none needed); no pacman transaction was run.

## RUNS:

Command form (the assignment's form, absolute paths):

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/c59_resolver_cases.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision fd6303ce5c14b3f892dec586297a942ab6e4193b \
  --work /fast/scratch/hyaku/kake-r59/ExecC2SeedSweep/w [--seed N]
```

Required runs — all six, plus four environment variants (all with `--work` under this seat's scratch).
Every run below printed `C2 resolver-cases 13/21 met=False` and exited 1:

| run | seed | elapsed |  | run | seed | elapsed |
| --- | --- | --- | --- | --- | --- | --- |
| seed1 | 1 | 1.04 s |  | gitdir_seed59 (`GIT_DIR=/nonexistent`) | 59 | 1.07 s |
| seed2 | 2 | 1.13 s |  | notmp_seed59 (`TMPDIR` unset) | 59 | 1.10 s |
| seed59 | 59 | 1.14 s |  | gitdir_noseed | random (`1138799550`) | 1.07 s |
| seed1000 | 1000 | 1.14 s |  | notmp_noseed | random (`1207855084`) | 1.07 s |
| seed424242 | 424242 | 1.14 s |  | | | |
| noseed | random (`2273235102`) | 1.13 s |  | | | |

Per-case PASS/FAIL, **identical in every run listed above** (seed 59 shown; the other nine are
byte-identical after normalising fixture ids, fixture commit hashes and the counter's own work-dir path).
`rc` = the case's tool exit code; `c/r/d` = its `ids_cited ids_resolved dangling` triple; `D` = a
`DANGLING S…` line was printed.

```
K1_fenced_heading_before_registry                     PASS rc=1 2/1/1 D
K2_backtick_fence_inside_registry                     PASS rc=1 2/1/1 D
K3_tilde_fence_inside_registry                        PASS rc=1 2/1/1 D
K4_non_ascii_path_at_revision                         PASS rc=1 2/1/1 D  cited-by=corpus/knowledge/中文.md
K5_git_quoted_path_at_revision                        PASS rc=1 2/1/1 D  cited-by=corpus/knowledge/a"b.md
K6_fenced_low_id_dangles_registered_high_id_resolves  PASS rc=1 2/1/1 D  low id dangles, high id resolves
K7_newline_path_at_revision                           PASS rc=1 2/1/1 D  cited-by=corpus/knowledge/line | break.md
K8_html_comment_row_is_not_registered                 FAIL rc=0 2/2/0
K9_setext_heading_ends_registry                       FAIL rc=0 2/2/0
K10_in_lane_symlinked_dir_is_read                     FAIL rc=0 1/1/0
K11_revision_symlink_resolved_in_tree                 FAIL rc=1 2/1/1 D  cited-by=corpus/knowledge/odd.md
K12_registry_outside_lane_is_unevaluable              FAIL rc=0 2/2/0
K13_non_utf8_path_at_revision                         FAIL rc=2 unevaluable: cannot read corpus/knowledge/bad<ff>.md
K14_non_toplevel_root_is_unevaluable                  FAIL rc=0 2/2/0
P1_three_space_row_resolves                           PASS rc=0 1/1/0
P2_row_after_closed_fence_resolves                    PASS rc=0 2/2/0
P3_four_space_line_is_code                            PASS rc=1 2/1/1 D
P4_committed_sibling_owns                             PASS rc=1 2/1/1 D  owners=alpha-shokunin url-match=alpha-shokunin
P5_absent_fleet_is_unevaluable                        PASS rc=2 fleet root <work>/c59-rc-*/no-such-fleet not a dir
P6_tool_selftest                                      FAIL rc=0 tool selftest tally 59/59 < the counter's floor 66
P7_real_lane_green                                    PASS rc=0 108/108/0
```

The failing set at the base revision is exactly the eight the contract names: **K8, K9, K10, K11, K12,
K13, K14 (the seven disclosed round-58 routes) and P6** (tool selftest tally 59 < the counter's floor
66). K1–K7 and P1–P5, P7 pass. The `13/21 met=False` score matches the committed base control
`controls/base-c2-resolver-cases.txt` exactly: a normalised diff of its per-case lines against my
seed-59 capture is empty, and its header line is identical. Timing, single-run wall clock, seed 59,
serial, host loaded: n=9 → min 1.218 s, median 1.352 s, max 1.459 s; in parallel batches each run took
1.03–1.14 s; a 120-seed sweep at P=10 completes in ≈ 20 s.

## DETERMINISM:

**Seed-independent — confirmed.** The per-case verdict vector is byte-identical across every run.

- Required seeds (1, 2, 59, 1000, 424242) and the unseeded run: identical vector; score line
  `13/21 met=False`, exit 1 in all six.
- Widening beyond the required set (so the property is not a coincidence of five seeds): 30 further
  sequential seeds (3, 4, 5, 6, 11, 12, 13, 17, 23, 29, 31, 37, 41, 43, 47, 53, 61, 67, 71, 73, 79, 83,
  89, 97, 101, 103, 107, 109, 113, 127) and 120 pseudo-random seeds (`random.Random(99)`) — every one
  returned `13/21 met=False`, exit 1, and the same verdict-vector digest (`sha256` of "case-name
  verdict" pairs, first 16 hex: `a3212b71629bc2d0`; the full-output digest after normalising fixture
  ids / fixture SHAs / the work-dir path: `ca8359c53a7055f3`).
- Total measuring invocations performed this seat: **180** (each produced a score line). Distinct
  score lines across all 180 captured outputs: one — `C2 resolver-cases 13/21 met=False` (180×).
  Distinct exit codes: one — 1. (Further non-measuring invocations exercised the error paths and
  `--selftest`; see below.)
- Same seed repeated three times in a row: identical full-output digest. The counter's seed echo is
  stable for a given `--seed` and is printed for unseeded runs (three unseeded runs printed
  `2273235102`, `1138799550`, `1207855084` — the seed is random per run, the verdict vector is not).

**Environment-independent — confirmed.** `GIT_DIR=/nonexistent` and `TMPDIR` unset each leave the
verdict vector and the score line unchanged, at seed 59 and at a random seed. Two stronger variants
were also checked: `GIT_DIR` pointed at the lane's *real* `.git`, and `GIT_DIR=/nonexistent` together
with `GIT_WORK_TREE=/nonexistent GIT_INDEX_FILE=/nonexistent/index` — both still `13/21 met=False`,
exit 1, same digest. This is expected from the code: the counter's `env()` (line 55) and the tool's
`_spawn()` (line 70) both strip every `GIT_*` variable before spawning git.

Further environment probes, all giving the same `13/21 met=False` / exit 1 and the same digest:
`LC_ALL=C LANG=C TZ=Asia/Tokyo`; `HOME` unset; cwd `/`; three concurrent runs sharing one `--work`
parent; `--root` with a trailing slash; `--revision fd6303ce` (short sha) and `--revision HEAD`
(resolved to the lane tip `cb685273…`; P7 stays `ids_cited=108`).

Error paths (the counter's own kill rule), each leaving no scratch behind: unresolvable revision → exit
2; `--root` below a repository toplevel → exit 2; `--root` at a repo whose revision has no
`scripts/id_resolver.py` → exit 2 with `0/21 met=False`, `tool_present FAIL`; missing `--revision` →
exit 64; unknown flag → exit 64. `--selftest` is still the version-1 stub: it prints
`c59 resolver-cases selftest: version 1 stub (not yet ported); exit 2` and exits 2 — consistent with
the contract's statement that wave 1 ports the round-58 cheat-class selftest before data.

The only per-run stdout variation is cosmetic and expected: the fixture ids (`S###`), the fixture commit
SHAs quoted in the K13/P5 notes, and the counter's own `c59-rc-*` directory name. No verdict, exit
code, count or ordering changed.

**Risk noted, not a defect of this seat's scope:** the counter's `--seed` only drives the *fixture id
draw* (`random.Random(SEED).sample(range(100,10000), 20)`); it does not permute case order, fixture
content or expectation strings. The sweep therefore proves invariance to the id draw (and exercises the
id-magnitude-sensitive case K6 across seeds), but does **not** prove invariance to a permuted case
order or different fixture shapes — that is the fixture generator's property, covered by the counter's
own selftest (still a stub).

## HYGIENE:

- **The counter removes its work dir.** The counter creates `<--work>/c59-rc-XXXXXXXX` and deletes it
  in a `finally` block. After every one of the 180 runs: **0** leftover `c59-rc-*` directories under
  this seat's scratch, **0** under `/tmp`, **0** inside the `--work` parent after the run. The
  `--work` *parent* is the caller's and is left in place (the counter creates it if missing — verified
  with `--work <…>/new/deep`); only the `c59-rc-*` child is removed. This matches the contract
  requirement that the counter remove its work dir.
- **The tool removes its own scratch.** The tool's `--selftest` uses
  `tempfile.mkdtemp(prefix="idresolver-selftest-")` and removes it in a `finally`. After all runs:
  **0** leftover `idresolver-selftest-*` directories under this seat's scratch and **0** in `/tmp`.
- **TMPDIR unset.** With `TMPDIR` unset and no `--work`, the counter's parent falls back to
  `tempfile.gettempdir()` = `/tmp`; sampling `/tmp` mid-run showed 1–2 transient `c59-rc-*` /
  `idresolver-selftest-*` entries during the run and **0** afterwards. With `TMPDIR` set to a scratch
  directory, the same transient entries appeared there and were cleaned. Nothing outside the counter's
  own work dir survives a run.
- **Fixture repos.** The only fixture repository this seat created was one throwaway repo under this
  seat's scratch, to exercise the "tool absent at the revision" path; its toplevel was asserted with
  `git rev-parse --show-toplevel` before the first commit and it was committed only with
  `-c user.name=selftest -c user.email=selftest@local`. No commit was made in the lane, a sibling
  lane, or anywhere else.
- **Lane untouched by this seat.** `git status --porcelain` in the lane shows only pre-existing
  wave-59 artefacts and modifications made by *other* seats (`c59_axis_evidence.py`,
  `c59_quote_truth.py`); this seat ran no `git add/commit/stash/checkout/reset/pull/push` and no jj
  mutation, and wrote only its own report file plus `ExecC2SeedSweep.files/`. Scratch removed after
  the receipts were copied into `.ufo/waves/round-59/w1/ExecC2SeedSweep.files/seed-sweep-receipts.txt`.
- **Credentials / private material.** None read, none written; no tokens, no `op://` refs, no private
  URLs appear in this report or in the receipts. The counter's own fixture URLs are `example.invalid`.

**Bottom line for the L1:** the C2 gate is deterministic and hygienic at the base revision — the same
21-case verdict vector (13/21; eight failures: K8–K14 + P6) under 180 invocations spanning 160+ seeds,
four hostile environments, four error paths and concurrent execution, with zero scratch leakage. No
seed-dependent false green and no seed-dependent false red was found. The one gap I could not close
from this seat: the counter's own `--selftest` remains the version-1 stub, so cheat-class detection is
not yet asserted by the counter itself.

VERDICT: C2 gate at base revision is seed- and environment-deterministic (identical 13/21 verdict
vector, exit 1, across 180 invocations / 160+ seeds / GIT_DIR and TMPDIR hostility) and leaks zero
scratch; no seed-dependent false green or false red found.
