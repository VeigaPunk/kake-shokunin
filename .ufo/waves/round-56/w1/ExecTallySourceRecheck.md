# ExecTallySourceRecheck

Claim C1 (calibration), row `source-recheck-audit`, `SKILL.md:1067` at base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`.
Every run below happened in a `mktemp -d` clone; the lane was read-only for me (only this report is written).

RUNS:

Clone (call it D): `git clone -q --no-checkout <lane> "$D" && git -C "$D" checkout -q e48354b7…`; `git -C "$D" rev-parse --show-toplevel` = `/tmp/tmp.ts7nmSzEgt`, `rev-parse HEAD` = `e48354b7…`. Ran in `$D`:
`python3 -B scripts/source_recheck_selftest.py` (no env pin: the script documents only `[--tool PATH]`; it
sets `PYTHONDONTWRITEBYTECODE=1` and `setdefault("LC_ALL", "C.UTF-8")` for the child itself).

- RUN1: exit **0**, wall **8698 ms**. Last 3 lines — the output is a *single* line, so last 3 = last 1:
  `{"cases": 106, "failed": 0, "failures": [], "passed": 106, "passedOverTotal": "106/106", "selftest": "kake-r36-source-recheck-selftest", "tool": "/tmp/tmp.ts7nmSzEgt/scripts/source_recheck.py", "verdict": "clean"}`
- RUN2: exit **0**, wall **7850 ms**; byte-identical to RUN1 (`cmp` → IDENTICAL, same `tool` path).
- `git -C "$D" status --porcelain` after both runs: empty (nothing written; `-B` respected, no `__pycache__`).
- Control, no repo at all: copied `scripts/` into a fresh `mktemp -d` with no `.git` and ran the same
  command there → exit 0, wall 7456 ms, `"passedOverTotal": "106/106"`; directory still holds only `scripts/`.
  So the run needs neither `.git` nor any other lane file.

WHAT N COUNTS:

N is **fixtures (= cases)**, not checks, mutants or unit checks. `main()` prints `cases = len(FIXTURES)`,
`passedOverTotal = "%d/%d" % (passed, cases)`, and loops once per fixture; each fixture is one black-box
subprocess run of the tool in its own temp case dir (`run_case`), judged on exit code, verdict, projected
findings and `checksEvaluated`. There is no separate unit-check block in this script (the string `unit`
does not occur), unlike the round-55 counters' "+ 3 unit-rule checks". `MIN_FIXTURES = 40` is a floor only.
Fixture registration: 106 `add(` calls; families a=8 b=13 c=12 d=7 e=8 f=17 g=28 o=4 u=4 v=5 (`--list`
gives 106 names; `u01–u04` are usage-error fixtures, still fixtures).
**The row's Self-test cell states `(101 fixtures)`; the observed tally is 106/106.** Not equal.
The counter's regex for this row (`POP`, `c56_selftally.py`) is `\((\d+) fixtures\)`; applied to the cell it
captures `[101]`, claim = 101, while `parse_tally` on the real output gives `(106, 106)` → `claim_ne_observed`.

HEAD DEPENDENCE:

Greps over `scripts/source_recheck_selftest.py`: no `rev-parse`, no `HEAD`, no `git show`, no git
subprocess; `os.environ` appears only in `tool_environment()` (copies the ambient env to the child,
adds `PYTHONDONTWRITEBYTECODE=1`, `setdefault LC_ALL`); `rglob` (`snapshot`) only walks the per-run temp
work dir; `SCORECARD.md`/`corpus`/`.ufo`/`SKILL` occur only as docstring prose, never as a read.
Files read from the checked-out tree beyond its own script: **exactly one** — `scripts/source_recheck.py`,
via `DEFAULT_TOOL = HERE / "source_recheck.py"` (`HERE = Path(__file__).resolve().parent`). It is not
imported or inspected, it is executed once per fixture (the docstring's "never reads the tool" means
black-box, not "does not touch the file"). Everything else is inline fixture data materialized into temp dirs.

Extra-commit proof (second clone D2 = `/tmp/tmp.6nzA6o2ciK`, base + one commit `f9e7fdf`, made with
`git -C "$D2" -c user.name=selftest -c user.email=selftest@local commit`; toplevel verified = `$D2`):
touched an extra registry row appended to `SKILL.md`, appended lines to `corpus/SOURCES.md` and
`corpus/README.md`, added `corpus/knowledge/probe-extra.md`, added `.ufo/waves/round-56/probe-extra.txt`
(`.ufo/waves/round-56/` does not exist at base). Rerun: exit **0**, **106/106**, wall 6465 ms; output
identical to the base run except the `tool` path string (different clone dir). Those five paths cannot
change the tally and cannot make the selftest fail.

Sensitivity control (same D2, next commit `7c14cc1`): changed `"version": REPORT_VERSION` →
`"version": 2` in `scripts/source_recheck.py` → exit **1**, tally **4/106**, 102 failures
`version mismatch: expected 1, observed 2`, wall 6177 ms. So the tally is a function of the selftest
script's own bytes plus the tool-under-test bytes, and of nothing else in the tree.

REPLACEMENT CELL:

Exact cell text (the only change is the integer; the backticked command stays first, the cell has no
other prose):

    `python3 -B scripts/source_recheck_selftest.py` (106 fixtures)

Checked against the counter, end to end: in scratch clone D3 (`/tmp/tmp.ERh5b5drLW`, base + commit
`59dc93d` holding exactly that cell) `c56_selftally.measure(D3, 59dc93d, pop=[("source-recheck-audit",
"scripts/source_recheck_selftest.py", r"\((\d+) fixtures\)")], base_rev=BASE_REV, expected=1)` returned
exit **0** with `claim=106 observed=106/106 problems=[]`. The same call on the base revision with today's
cell returned exit **1**, `claim=101 observed=106/106 problems=["claim_ne_observed"]`. `blob()` of
`scripts/source_recheck_selftest.py` at base and at the worktree are the same (`4093335f57b52171c11e604e1346140d758b1f6b`),
so `tool_changed` does not fire and the row's only remaining problem is the stale integer.

RISKS:

- The counter compares the selftest blob to `BASE_REV`: any later edit to
  `scripts/source_recheck_selftest.py` (even a comment, or one added fixture) re-breaks the row via
  `tool_changed`, and would also invalidate 106. Cell and blob must move together.
- The tally also depends on `scripts/source_recheck.py` bytes (demonstrated 4/106). A tool edit that
  changes a report field or an exit code changes the observed N without touching the selftest.
- `parse_tally` keeps the **last** matching line; today the output is one JSON line, so first and last
  agree. A future trailing line containing `a/b` plus "pass"/"selftest" would override it.
- Wall time was 6.2–8.7 s per run on this loaded host, well inside the counter's `TIMEOUT = 300`, but the
  counter re-runs the row on every measure (no caching).
- Inherited environment reaches the child unchanged (`LC_ALL` is only a `setdefault`). Not observed to
  affect the tally (git-free plain-dir run reproduced 106/106), but only these three contexts were run.
- Line 1067 holds the row at base and at worktree `6b3df99` (`git diff e48354b… -- SKILL.md
  scripts/source_recheck*.py` is empty), so the edit target is unambiguous.
- No installs were needed (system `python3`); no pacman was run; nothing outside this report was written
  in the lane.

VERDICT: Observed selftest tally for `source-recheck-audit` is 106/106, exit 0, on two identical base-clone runs (and in a git-free copy); the row's `(101 fixtures)` is wrong — replacing it with `(106 fixtures)` yields claim=106 = observed and clears the counter's only finding for this row.
