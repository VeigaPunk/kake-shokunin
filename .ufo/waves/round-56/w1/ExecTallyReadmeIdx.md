# ExecTallyReadmeIdx

Claim C1 (calibration), row `readme-index-counter` (SKILL.md line 1233 at base). Independent derivation
in scratch clones only; no lane file written except this report, no lane git/jj mutation, no pacman,
no tool installs needed.

Scratch repos (both verified `git -C <dir> rev-parse --show-toplevel` == dir):
- `D=/tmp/tmp.wSg6nvN5Nj` — clone of the lane, checked out at `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`.
- `D2=/tmp/tmp.TWe51eXRlW` — same, plus one extra commit `d7b2620c1b574471b27f6fdee0bc1326cd30fe3e`
  (`-c user.name=selftest -c user.email=selftest@local`) touching the five paths named in the ticket.

## RUNS:

Command in `$D` (script documents **no** env pin; no `os.environ`/`getenv`/`KAKE_*` read anywhere in it):

    python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest

| run | exit | wall | last 3 stdout lines (stdout is exactly 1 line) | stderr |
|---|---|---|---|---|
| 1 | 0 | 9.82 s | `c55 readme-index selftest: 44/44` | empty |
| 2 | 0 | 12.09 s | `c55 readme-index selftest: 44/44` | empty |

Reproducible: identical tally both runs; the only line printed is the tally (fail lines print only on
failure). `git -C $D status --porcelain` empty after both runs — the selftest writes only into
`tempfile.mkdtemp()` sandbox repos and `shutil.rmtree`s each one.

Cross-check with the round-56 counter's own parser and per-row measure on `$D` (imported read-only,
`PYTHONDONTWRITEBYTECODE=1`):

- `c56_selftally.parse_tally("c55 readme-index selftest: 44/44\n")` -> `(44, 44)`.
- `c56_selftally.measure($D, BASE_REV, pop=[readme-index-counter row])` -> exit 1, problems
  `["claim_ne_observed"]`, facts `claim=35, observed="44/44", exit=0`, wall 27.9 s.
- `blob(HEAD)` == `blob(BASE_REV)` == `1a65be474aab47ac1e002f5a893fdda4de0071a6` -> no `tool_changed`.

So at the base revision the row is a genuine mismatch: claim 35, observed total 44.

## WHAT N COUNTS:

The printed `N` is `len(cases)`, i.e. the number of `case(...)` registrations in `selftest()` — 44 of
them, all names unique (`grep -c '^    case('` = 44; unique case names = 44). Each case builds **one**
generated sandbox repo (`_fixture`: `git init` in a `mktemp -d`, base commit of the knowledge tree, tip
commit of README + tree, optional post-commit worktree edit / tip-knowledge override / deletion) and
calls `measure()` once. So the denominator counts *fixture repos (cases)*; the numerator counts cases
whose exit code and asserted facts matched. It is **not** the count of checks: each case asserts one
exit code plus, where given, an `expect` dict of up to 2–3 facts.

The literal `N = 46` inside `selftest()` is unrelated to the printed number: it is the per-fixture
population (46 generated `knowledge/e<i>.md` entries and 46 coverage-map rows) and is never printed.
The counter-visible integer is therefore 44, and the row's Self-test cell states **35** — it does not
equal 44 (nor 46). Provenance of the stale 35: `git log` on the script shows `2bda8e4` (v2) had 35
`case(` lines, `faf9abe` (v2.1) has 44; the receipt was later regenerated in `64c0ce1` to `44/44`, but
the SKILL.md cell was never re-stated.

The cell also contradicts its own receipt: `git show HEAD:.ufo/waves/round-55/controls/c1-selftest-v2.txt`
ends with `c55 readme-index selftest: 44/44`.

## HEAD DEPENDENCE:

**None.** Every git read in the selftest targets the sandbox repo, never the enclosing clone:

- `open(` appears only at lines 245 and 258, both writing fixture files under `os.path.join(d, rel)`.
- `git ... rev-parse HEAD` (line 250) is `git -C d` on the fixture repo, used as that fixture's tip.
- `selftest()` calls `measure(d, tip, base)` — the fixture's own tip/base — so the module constant
  `BASE_REV = fcaf4b85…` is overridden and never resolved in the clone.
- No `os.environ`/`getenv`, no `git show` against the clone, no worktree read of `corpus/`, `SKILL.md`
  or `.ufo/waves/` anywhere in the selftest path. Its "fixtures" are in-code literals (`ents`, `rows`,
  `readme()`); the only file it takes from the clone is the script itself, which the interpreter loads.

Extra-commit rerun in `$D2` (HEAD = `d7b2620`, +1 registry row with `(999 fixtures)` in SKILL.md,
+`<!-- extra -->` in `corpus/SOURCES.md` and `corpus/README.md`, +`corpus/knowledge/archive/extra-r56.md`,
+`.ufo/waves/round-56/extra/note.json`):

    python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest
    -> "c55 readme-index selftest: 44/44", EXIT=0, WALL=13534 ms

Tally unchanged (44/44) and no failure: the selftest is invariant under later commits to
`corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/`, `SKILL.md` and new
`.ufo/waves/round-56/` files. A later commit that rewrites **the script itself** is the only thing that
can move the tally, and the counter catches that separately as `tool_changed`.

## REPLACEMENT CELL:

Exact new Self-test cell (5th cell of row `readme-index-counter`; command first in backticks, all other
prose of the cell preserved verbatim, only the integer changed 35 -> 44):

```
`python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` (44 fixtures, generated sandbox repos; receipt `.ufo/waves/round-55/controls/c1-selftest-v2.txt`)
```

Checked against the counter's POP entry for this row, `r"\((\d+) (?:fixtures|checks)"`, using the
counter's own helpers on the base SKILL.md row with this cell substituted:

- `re.findall(rx, cell)` -> `['44']` (old cell -> `['35']`); no other integer in the cell matches, so
  `claim = 44 == observed total 44`.
- `documented_command(...)` -> `['python3', '-B', '.ufo/waves/round-55/c55_readme_index.py', '--selftest']`
  (allowed by `run_command`: argv[0] `python3`, no env prefix needed).
- `selftest_cell(...)` resolves to the new cell; `_is_selftest_span` true via `--selftest`.

"44 fixtures" is the accurate noun: the 44 printed units are 44 generated sandbox repos (cases), each
one fixture repo.

## RISKS:

- The row's other cells stay untouched; only the tally integer is wrong. If the wave instead re-pins
  the script, the tally must be re-derived (35 was a v2 artifact; v2.1 = 44, and `faf9abe`'s blob equals
  the base blob, so no rewrite has happened since).
- No env pin is documented and the selftest does not scrub inherited env. Measured: with
  `GIT_DIR=/nonexistent` the run dies inside `_fixture` (`git init` returns 1, uncaught
  `CalledProcessError`), exit 1. The round-56 counter inherits `os.environ` (adds only
  `PYTHONDONTWRITEBYTECODE=1`), so a hostile `GIT_DIR`/`GIT_WORK_TREE`/`GIT_OBJECT_DIRECTORY` in the
  operator's environment would turn this row into `selftest_failed`/unevaluable. Not observed in the
  two clean runs; worth a pin if the counter is ever run under a git hook or `git -C` alias wrapper.
- `TIMEOUT = 300` in the counter vs ~10–14 s observed here: ample, but the host is loaded; the
  per-row measure probe took 27.9 s end to end (clone + run).
- `N = 46` in the selftest is a fixture *population* and must not be mistaken for the tally; the floor
  `knowledge_files >= 46` in the predicate and this `N` are the same number by design, not by accident.
- Cleanup: both scratch clones are under `/tmp` (`tmp.wSg6nvN5Nj`, `tmp.TWe51eXRlW`); nothing in the
  lane was written except this report. No tool was installed or upgraded (pacman untouched).

VERDICT: Observed tally for `readme-index-counter` is 44/44 (exit 0, ~10 s, twice), the row claims 35, and the selftest is HEAD-independent (44/44 unchanged after an extra commit touching corpus/SKILL.md/.ufo/waves/round-56) — replace the cell with `(44 fixtures, generated sandbox repos; receipt …c1-selftest-v2.txt)`.
