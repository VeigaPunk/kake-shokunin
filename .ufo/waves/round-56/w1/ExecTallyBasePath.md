# ExecTallyBasePath

Claim C1 (calibration) — SKILL.md gate-registry row `base-path-audit`, line 726 at base
`e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`. Row text in the lane worktree is byte-identical to the
base blob (diff empty), so the replacement below applies at either revision.

## RUNS:

Scratch clone `D=$(mktemp -d /tmp/etbp-XXXXXX)` = `/tmp/etbp-Th46aF`;
`git clone -q --no-checkout <lane> "$D"` then `git -C "$D" checkout -q e48354b7…`;
`git -C "$D" rev-parse HEAD` → `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`;
`git -C "$D" rev-parse --show-toplevel` → `/tmp/etbp-Th46aF` (matches `$D`).

Command, exactly as the row documents it, `cwd=$D`, no env pin added (the script documents none; it
pins `PYTHONDONTWRITEBYTECODE=1` for the child tool itself at line 158 and defaults `LC_ALL=C.UTF-8`
only when unset):

```
python3 -B scripts/base_path_selftest.py
```

| run | exit | wall | last 3 lines (stdout JSON tail + stderr tally) |
|---|---|---|---|
| 1 | 0 | 2.29 s | `  ]` / `}` / `45/45 fixtures passed` |
| 2 | 0 | 2.71 s | `  ]` / `}` / `45/45 fixtures passed` |

Both runs produced byte-identical stdout+stderr (empty `diff`). No `__pycache__`, no `*.pyc`, no new
files in the clone (`git status --porcelain` empty after both runs). No files created in the lane.

## WHAT N COUNTS:

N is **fixtures**, i.e. case directories: `case_dirs = sorted(p for p in fixtures.iterdir() if p.is_dir()
and (p/"expected.json").exists())`, then `summary["cases"] = passed + failed` and the stderr line is
`"%d/%d fixtures passed" % (passed, total)`. Each fixture = one `scripts/base_path_audit.py` process run,
compared on exit code, `verdict`, and the matched finding tuples (`reason` plus `element`/`attribute`/
`value`/`page`/`resolved` when pinned), plus `pagesChecked`/`referencesChecked` when the fixture pins
them. It counts neither checks, mutants, nor unit checks.

Composition at base, measured by listing `scripts/fixtures/base-path/`: 45 case dirs, 132 files,
tree sha256[:16] `49dc2922b3020e82`.

- 30 matrix fixtures: `D1`–`D14` (14), `I1`–`I8` (8), `K1`–`K7` (7), `U1` (1).
- 15 round-29 regression fixtures: dir names `X01-duplicate-json-key` … `X15-same-scheme-single-slash-relative`,
  `expected.json` `id` equal to the dir name, so the `X01`–`X15` ids the row names exist.

The row's Self-test cell states "30 matrix fixtures plus 15 round-29 regression fixtures `X01`–`X15`".
The counter's claim regex for this row, `(\d+) (?:matrix |round-29 regression )?fixtures`, applied to
that cell captures `[30, 15]`, sum **45**, which equals the observed total 45. So at base the claim
already equals the observation — but only as a sum of two component counts; the cell never states the
total the command actually prints, which is what makes the row unreadable as a self-assessment and what
a single added `fixtures` token would silently break (see RISKS).

Hard floor: `MIN_DEFAULT_CASES = 45` — when the default fixture path resolves and holds fewer than 45
case dirs, the run is `could-not-evaluate` (exit 2), not a smaller tally (measured, below).

## HEAD DEPENDENCE:

Grep over `scripts/base_path_selftest.py` and `scripts/base_path_audit.py`: no `git` call, no
`rev-parse HEAD`, no `git show`, no `HEAD` string. The only environment read is `os.environ` at line 157,
copied into the child tool's environment (plus forced `PYTHONDONTWRITEBYTECODE=1`, `LC_ALL` default);
no env value selects a revision or a path.

Files read beyond its own script:

- `scripts/base_path_audit.py` — `DEFAULT_TOOL = HERE/"base_path_audit.py"` (line 50).
- `scripts/fixtures/base-path/` — `DEFAULT_FIXTURES` (line 51): `iterdir()` for case dirs, each
  `<case>/expected.json`, and whatever each fixture's `manifest.json` names inside that case dir (the
  tool walks case-relative components with `os.open(..., dir_fd=...)`).
- `sys.executable` (line 231, `--python` default) — the interpreter, not a repo file.

Nothing under `corpus/`, `SKILL.md`, or `.ufo/` is read. The runner reads the **working tree beside the
script**, not HEAD.

Extra-commit proof (second scratch clone `D2=/tmp/etbp2-vACU3B`, toplevel verified == `$D2`, base then
one commit `4f5955f` via `git -C "$D2" -c user.name=selftest -c user.email=selftest@local commit`):

```
 .ufo/waves/round-56/probe.json     | 1 +     (round-56/ did not exist at base; last wave was round-55)
 .ufo/waves/round-56/probe.md       | 1 +
 SKILL.md                           | 1 +     (extra registry row zz-probe-audit, 99-fixture claim)
 corpus/README.md                   | 2 ++
 corpus/SOURCES.md                  | 2 ++
 corpus/knowledge/zz-probe-extra.md | 3 +++
```

Rerun twice on that commit: exit 0, `45/45 fixtures passed`, wall 2.31 s / 2.16 s. Full stdout+stderr
diffed against the base-revision run: identical except the absolute `"tool"`/`"fixtures"` paths in the
JSON summary (empty diff once those two lines are dropped).

Tree-vs-HEAD probes in the same clone (uncommitted, then restored; tree clean afterwards):
adding one case dir (`X16-probe-extra`, copy of `X09`) → `46/46`, exit 0; deleting one case dir → exit 2,
`could-not-evaluate: only 44 fixtures, expected at least 45`.

Answer: no later commit touching `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/`,
`SKILL.md`, or new files under `.ufo/waves/round-56/` changes the tally or fails the selftest. The
tally moves only with `scripts/fixtures/base-path/` (or with `scripts/base_path_audit.py`), and — since
the working tree is what is read — an *uncommitted* fixture edit also moves it while HEAD is unchanged.

## REPLACEMENT CELL:

Exact Self-test cell text (en dash U+2013 between `X01` and `X15` retained; command first in backticks;
remaining prose unchanged; total stated once):

```
`python3 -B scripts/base_path_selftest.py` over `scripts/fixtures/base-path/` (45 fixtures: 30 matrix cases plus 15 round-29 regression cases `X01`–`X15`), comparing exit, verdict and reason tuples
```

Whole-row line to land (line 726), same cell substituted, all other cells untouched:

```
| base-path-audit | gate (offline static project-site base-path policy) | `python3 -B scripts/base_path_audit.py --manifest <dir>/manifest.json` | 0 clean; 1 failed-policy (`outside_base_path`); 2 could-not-evaluate (`input_invalid`, `page_outside_base_path`); 64 usage | `python3 -B scripts/base_path_selftest.py` over `scripts/fixtures/base-path/` (45 fixtures: 30 matrix cases plus 15 round-29 regression cases `X01`–`X15`), comparing exit, verdict and reason tuples | frozen matrix `.ufo/waves/round-29/c2-matrix.json` sha256 `75c08f64…`, counted by `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision <commit>` | none (reads local files, no network, no writes) | kake |
```

Checked with the counter's own functions (module `.ufo/waves/round-56/c56_selftally.py` imported
read-only, no run of the other nine rows):

- `documented_command` → `['python3', '-B', 'scripts/base_path_selftest.py']` (command still first and
  still a selftest span); `selftest_cell` → this cell.
- POP regex `(\d+) (?:matrix |round-29 regression )?fixtures` → matches `[45]`, sum **45** = observed
  total `B` of `45/45` → no `claim_ne_observed`, and no `claim_missing`.

## RISKS:

- The claim regex sums every `<N> fixtures` token in the cell. The naive form that keeps the split in
  "fixtures" wording — `(45 fixtures: 30 matrix fixtures plus 15 round-29 regression fixtures …)` —
  measures **90** (matches `[45,30,15]`) and would make this row `claim_ne_observed`. Hence the split is
  written as "cases" (the script's own vocabulary: `summary["cases"]`). If a later round wants both the
  total and the split in "fixtures" wording, the counter's POP entry needs a total-only anchor first —
  a counter change, not a doc change.
- The 45 is a literal floor (`MIN_DEFAULT_CASES = 45`) separate from the fixture tree: adding a fixture
  moves the tally to 46 (cell must move with it), while deleting one below 45 turns the run into exit 2
  rather than a smaller tally. Two constants, one file — they can drift.
- The selftest passes the ambient environment through to the tool under test (inherited `PYTHONPATH`,
  a pre-set `LC_ALL`, etc.); I added no pin because the script documents none. Under a polluted env the
  child tool could in principle behave differently; the tally itself is env-independent in this run
  (two identical runs, ambient env).
- Timing headroom is large (2.16–2.71 s vs the counter's `TIMEOUT = 300`) even on the loaded host.
- Scope: all runs in `/tmp` scratch clones; lane worktree, lane jj state and lane Git index untouched; no
  installs needed, no pacman run.

VERDICT: base-path-audit observes 45/45 fixtures (exit 0, twice, 2.29 s / 2.71 s); N counts fixture case dirs (30 matrix + 15 X01–X15) and equals the row's summed claim 45; no HEAD/corpus/SKILL/.ufo read, proven by an extra-commit rerun at 45/45; replacement cell `…(45 fixtures: 30 matrix cases plus 15 round-29 regression cases `X01`–`X15`), …` yields claim 45 under the POP regex.
