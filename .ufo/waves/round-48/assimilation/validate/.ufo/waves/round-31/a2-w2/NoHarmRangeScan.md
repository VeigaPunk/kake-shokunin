# NoHarmRangeScan — no-harm scan over the round-31 range

Seat: KakeR31a2.NoHarmRangeScan (wave 2, falsify). Range scanned:
`f1ffb81738c92c0537b99b30970143ab9419f990 .. fde133ab48086bb9a06911b4ab045e2ad9086347`
(4 commits: a16602a declare, c88b97e C1, b801ac8 strict supplement, fde133a C2 entry).
Sandbox: `/fast/scratch/hyaku/kake-r31/a2-w2/NoHarmRangeScan/` (clone at fde133a; artifacts: `numstat.txt`, `selftest.diff`, `selftest-run.json`).

## Method

`git diff --numstat <base> <tip>` (62 files), `git diff --summary`, `git diff --name-status` (no D/R/C entries, no mode changes), fixture-shape scan of `scripts/fixtures/citing-set/` (45 cases), and a live run of the repaired runner over the existing fixtures.

## Files with removed lines

Exactly one file in the whole range removes lines: `scripts/citing_set_selftest.py` (+123/-15, hunk diff saved at `selftest.diff`). It is executable code, not an append-only document, so the standard is "superseding edit, not silent loss". Every removed line, with verdict:

1. Docstring lines `git_commit stage everything and commit (Git identity is set by the runner; / the environment is isolated: inherited GIT_* variables are / dropped and GIT_CONFIG_GLOBAL is pinned to /dev/null)` — replaced by an expanded docstring that adds the git_init-first rule, GIT_CEILING_DIRECTORIES and --git-dir/--work-tree pinning. Verdict: superseded documentation, more precise. NO HARM.
2. `def git_env():` / `"""Isolated environment for setup Git commands."""` — replaced by `git_env(work_dir)` which still drops GIT_* and pins GIT_CONFIG_GLOBAL, and additionally sets GIT_CEILING_DIRECTORIES to the copy's parent (blocks enclosing-repo discovery, N3). Sole caller updated (diff line `env = git_env(work_dir)`). Verdict: superseded. NO HARM.
3. `run_command(["git", "-c", "core.hooksPath=/dev/null", "init", "-q"], ...)` and the two git_commit `run_command([... "add", "-A"], ...)` / `["git", ... "commit", ...]` lines — replaced by `git_command(work_dir, ...)` which keeps `core.hooksPath=/dev/null` and adds `--git-dir=<copy>/.git --work-tree=<copy>`, plus a `git_commit` guard requiring a real (non-symlink) `.git` dir inside the copy (N2/N3). Verdict: superseded, strictly stronger. NO HARM.
4. `expected_file = case_dir / "expected.json"` + `raw = expected_file.read_text(encoding="utf-8")` + `except OSError ... row["reason"] = "expected.json unreadable: %s"` — replaced by `read_expected(case_dir)` using O_NOFOLLOW/O_NONBLOCK/O_NOCTTY, fstat regular-file and 1 MiB size checks (N5). Failure path still sets `row["reason"]` and returns the case failed. Verdict: superseded. NO HARM.
5. Case-discovery predicate `path.is_dir() and not path.is_symlink() and not path.name.startswith(".")` — replaced by `(path.is_symlink() or path.is_dir()) and not path.name.startswith(".")` so symlinked case dirs are enumerated and then failed explicitly in `run_case` (`"symlinked case directory refused"`) instead of silently skipped (N6). Verdict: superseded, implements the refusal. NO HARM.

## Append-only documents

SOURCES.md (+7), LOG.md (+33), QUALITY.md (+29), SKILL.md (+63), PROVINCE.md (+14), README.md (+10), SCORECARD.md (+101), corpus/lessons/round-31.md (new), corpus/knowledge/render-static-sites.md (+23), corpus/knowledge/render-web-services.md (new): all 0 removed lines in numstat. Verdict: append-only discipline intact. NO HARM.

## Invariants checked

- SHONEN.md: unchanged (zero diff in range).
- corpus/knowledge/: only render-static-sites.md modified and render-web-services.md created; the other 28 entries byte-identical.
- No file deleted, renamed, copied or mode-changed anywhere in the range (name-status shows only A/M; summary shows only `create mode`).
- Existing-fixture regression probe (no harm from new refusals): scanned all 45 cases in `scripts/fixtures/citing-set/` — zero symlinks, zero `.git` entries, zero `.git` setup paths, zero git_commit-without-git_init, all expected.json regular files ≤ 1 MiB; the only `argv` tokens starting with `-` are allowlisted gate options (`--revision`, `--population`, `--ledger=...`, `--roo`, `--rev` — prefixes of `root`/`revision` and of no valueless option, accepted by `argv_refusal`).
- Live run in sandbox: `TMPDIR=<sandbox>/tmp python3 -B scripts/citing_set_selftest.py --root . --tmpdir <sandbox>/tmp/selftest` → exit 0, `verdict clean`, `passed true`, `cases 45`, `failedCases 0`, `failures []` (`selftest-run.json`). The containment rewrite did not break any existing case.

## Verdict

No harm found in the range. The only removed lines (15, all in `scripts/citing_set_selftest.py`) are superseding edits required by the C1 containment repair; each replaced by strictly stronger code, and the repaired runner still passes all 45 pre-existing fixture cases.

Not verified: behavior of the base runner (I reviewed only the landed range, base state read via diff context); semantics of the counter scripts themselves (other seats attack those).

Tooling: none installed (git + python3 only; pacman transactions paused per bounds).
