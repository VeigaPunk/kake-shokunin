# ExecTallyCitation

Claim C1 (calibration) — independent derivation of the observed selftest tally for SKILL.md
gate-registry row `commit-citation-lint` (line 1199 at base), plus the replacement Self-test cell
checked against the counter's claim regex. No lane file was created or modified; only this report.

## RUNS:

Scratch clone: `D=/tmp/tmp.B8T1IS9rOO`, `git clone -q --no-checkout <lane> "$D"`, `git -C "$D"
checkout -q e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`. Verified `git -C "$D" rev-parse
--show-toplevel` = `/tmp/tmp.B8T1IS9rOO` and `rev-parse HEAD` = `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`.

Command, cwd `$D`: `python3 -B scripts/citation_lint.py --selftest`. No env pin: the script reads no
env var for any decision (only `env = dict(os.environ)` as a pass-through to child `git`, line 200);
the counter itself sets `PYTHONDONTWRITEBYTECODE=1`.

- RUN 1 — rc=0, wall 105 ms, last 3 lines:
  ```
    PASS  mutant E (no ellipsis rule) overreaches on digest prefixes (diverges)
    PASS  adjudication ledger suppresses named token/file only
  selftest: 9/9 passed
  ```
- RUN 2 — rc=0, wall 95 ms, last 3 lines: byte-identical to RUN 1 (same three lines, `9/9 passed`).
- Full output: 9 `PASS` lines, 0 `FAIL`, header `citation_lint --selftest`, trailer
  `selftest: 9/9 passed`.
- Counter cross-check (read-only; counter run from the lane path with `--root "$D" --revision
  e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`): `commit-citation-lint: claim=8 observed=9/9 MISMATCH
  claim_ne_observed`; overall `tally_mismatches=7 rows_checked=10 met=False`, EXIT=1, 62.4 s — the
  contract's do-nothing control line reproduced exactly.

## WHAT N COUNTS:

`total = len(passed) + len(failures)` (script line 322-324): N is the number of **named assertions
(checks)** the selftest evaluates, and N=9 at base. It is not a fixture count, not a mutant count and
not a unit-check count. The 9 assertions:

1. planted dead citations flagged (2/2) — one assertion, two dead short tokens
2. planted dead full-40-hex token flagged (1/1)
3. resolving commit not flagged
4. no false positives on the exclusion classes
5. mutant F (no resolution) false-green on dead token (diverges)
6. mutant G (no context filter) overreaches on plain hex (diverges)
7. mutant H (no digest exclusion) flags the sha256 token (diverges)
8. mutant E (no ellipsis rule) overreaches on digest prefixes (diverges)
9. adjudication ledger suppresses named token/file only

The material it asserts over is an in-memory dict of 14 `SCORECARD.md` lines + 3 `LOG.md` lines (17
fixture lines) evaluated by `scan()` against a throwaway repo the selftest `git init`s in its own
`TemporaryDirectory`. So "fixtures"=17, "mutants"=4, "assertions"=9: only the last is what prints.

Equality with the row's cell: the cell at base states `(8/8;` → **does not equal 9**. The 8 is the
round-47 receipt's pasted stdout (`.ufo/waves/round-47/verification/selftest-citation-lint.txt`, 8
PASS lines, `tool_sha256: 3c78a0a8…`). The 9th assertion ("dead full-40-hex") landed afterwards in
round-48 commit `af7b217` (`scripts/citation_lint.py | 16 ++++++++++++++--`), and the receipt was
never re-issued (only commit touching that receipt path: `846138c`, round-47). Current script sha256
`0beba6478ce4e840b9220d9414c3d9ca888747267599e8a345b4eb67bf211235`, git blob `87252709fc65…`.

## HEAD DEPENDENCE:

Grep inventory of `scripts/citation_lint.py`:

- `rev-parse HEAD` — line 209 only, on the temp repo the selftest just created (`git init -q` in
  `TemporaryDirectory(prefix="kake-r46-citelint-")`), to get a token that resolves. Not the clone's HEAD.
- `git show` — none.
- `open(` — line 94 (`read_population`), line 114 (`load_adjudications`), both main-path only; line
  343 (`--json` output write). None reachable from `--selftest`.
- `environ` — line 200 only, `env = dict(os.environ)`, passed to child `git` calls; no branch on it.
- Imports — stdlib only (`argparse, json, os, re, shlex, shutil, subprocess, sys, tempfile`,
  plus local `pathlib`); no lane module, no `corpus/` path literal is opened.

Conclusion: the selftest reads nothing from the clone's HEAD or working tree beyond its own script
file, so `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/`, `SKILL.md` and new
`.ufo/waves/round-56/` files cannot move the tally.

Proof (extra commit): `D2=/tmp/tmp.7fvZqQVwh3`, clone + checkout of base, then one extra commit
`c1bb35f` made with `git -C "$D2" -c user.name=selftest -c user.email=selftest@local commit`
touching 5 files, +11 lines: `SKILL.md` (extra registry row `probe-extra-registry-row` inserted after
the citation row), `corpus/SOURCES.md` (+1 probe line), `corpus/README.md` (+1 probe line), new
`corpus/knowledge/probe-extra.md`, new `.ufo/waves/round-56/probe-extra.txt`. Rerun at `c1bb35f`:
rc=0, `selftest: 9/9 passed`, 9 PASS lines, identical to base. Control at `HEAD~1` (base content):
rc=0, 9/9. **Tally unchanged; selftest does not fail.**

Related, not HEAD: the `dict(os.environ)` pass-through makes the selftest non-hermetic against
ambient `GIT_*`. `GIT_DIR=<scratch>/probe.git python3 -B scripts/citation_lint.py --selftest` →
`fatal: this operation must be run in a work tree`, uncaught `CalledProcessError` traceback from line
207 (`git add f.txt`), exit 1, and a repo was created at `$GIT_DIR` (HEAD/config/objects/refs) — a
write outside the temp dir and no `A/B` line, which `parse_tally` cannot read (counter would exit 2,
unevaluable). With a clean env (`env -i PATH=/usr/bin:/bin HOME=<empty> GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_SYSTEM=/dev/null`) it passes 9/9.

## REPLACEMENT CELL:

Exact replacement for the row-1199 Self-test cell (only `8/8` → `9/9`; command first, all other prose
unchanged):

```
`python3 -B scripts/citation_lint.py --selftest` (9/9; receipt `.ufo/waves/round-47/verification/selftest-citation-lint.txt` names tool path + sha256 + tally)
```

Checked against the counter: POP entry `("commit-citation-lint", "scripts/citation_lint.py",
r"\((\d+)/\d+;")`; `re.findall` on this cell → `[9]`, sum 9 == observed denominator 9, so
`claim_ne_observed` clears; A==B (9/9) and rc=0 clear `selftest_failed`; `documented_command`
shlexes the backticked span to `['python3','-B','scripts/citation_lint.py','--selftest']` (first word
`python3`), and `_is_selftest_span` matches on `--selftest` in the script's own cell, so the row reads
`OK`. Verified base cell under the same regex captures `[8]` (sum 8), i.e. today's mismatch is exactly
one integer.

Caveat the counter does not test: the named round-47 receipt records 8/8, so a `9/9` cell citing it is
self-contradictory prose. Honest variant if wave 1 re-issues the receipt (9 PASS lines, sha256
`0beba6478ce4e840b9220d9414c3d9ca888747267599e8a345b4eb67bf211235`, exit=0):

```
`python3 -B scripts/citation_lint.py --selftest` (9/9; receipt `.ufo/waves/round-56/verification/selftest-citation-lint.txt` names tool path + sha256 + tally)
```

Both pass the regex identically (captured `[9]`); the choice is about prose truth, not the predicate.

## RISKS:

1. Stale receipt: round-47 receipt says 8/8 with `tool_sha256 3c78a0a8…`; the tool is now
   `0beba647…` and prints 9/9 (9th check added in `af7b217`). Any critic diffing cell against receipt
   will flag it; re-issuing the receipt in W1 is the clean fix.
2. Do not "fix" the row by editing `scripts/citation_lint.py`: the counter's `tool_changed` compares
   the script blob at the measured revision to `BASE_REV`'s, so a script edit converts the row from
   `claim_ne_observed` to `tool_changed` (still a mismatch).
3. `dict(os.environ)` pass-through: a harness exporting `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`
   makes this selftest crash with a traceback, write outside its temp dir, and the counter returns
   exit 2 (tally unparsable) rather than a pass. Out of a prose seat's scope.
4. Claim summation: the regex captures *every* `(N/M;` in the cell and the counter compares the sum to
   the observed denominator, so adding a second parenthetical tally to this cell (e.g. `(2/2;`) would
   sum to 11 and re-open the mismatch.
5. Class defect, not one row: N counts assertions, and the registry has no coupling to the selftest's
   assertion count, so any future added check silently falsifies the cell (as round 48 did). The
   counter only pins the script blob, so this recurrence is invisible until the tally drifts.
6. Wall time 95-105 ms per run on the loaded host, both runs identical; the counter's 300 s timeout is
   not a factor. `__pycache__` under `.ufo/waves/round-56/` is not mine — every invocation used `-B`
   and cwd outside the lane; `git status -- scripts/` in the lane is clean.

VERDICT: observed tally for commit-citation-lint is 9/9 (rc=0 twice, HEAD-independent, proven by an extra-commit rerun); the row's 8/8 is stale — replace with `(9/9;` and re-issue the receipt.
