# ReviewHostileContract — C1 interface contract vs routed text (kake r31 w1)

Axes: operability (contract fidelity, zero breakage of the 45 committed cases), completeness
(nothing routed dropped or weakened). Method: text compare of the C1 contract (L1 context,
landed a16602a) against `corpus/lessons/round-30-verifier-spotcheck.md:145-170` and `:250-262`,
plus `history://HyakuCloseKake30.RunnerSandboxHold` (readable, parked), plus head bytes of gate
and runner and all committed `case.json`.

## Coverage of the five routed gaps (spotcheck.md:250-262)

| Routed | Contract | Verdict |
|---|---|---|
| N1 refuse `--selftest` and any argv outside an allowlist | argv allowlist; `--selftest` name is not a prefix of root/revision/population/ledger, so refused with `case.json argv refused: --selftest`; "the gate is never started for that case" | covered, and stronger (refusal precedes gate start, which also closes hold-N4's delegation vector) |
| N2 refuse fixture `.git` for every setup op | `.git` entry at any depth (file/dir/symlink) refuses the whole case, with or without case.json, before any copy or setup | covered, stronger than per-op refusal; `git_init` before `git_commit` covered under N3 below |
| N3 pin `GIT_CEILING_DIRECTORIES` and `--git-dir`/`--work-tree` | every setup Git command runs with `GIT_CEILING_DIRECTORIES=<work>/..` and explicit `--git-dir=<work>/.git --work-tree=<work>`; `git_commit` with no earlier `git_init` refused | covered verbatim |
| N5 `expected.json` with `O_NOFOLLOW`, regular-file check, size cap | `os.open(O_RDONLY\|O_NOFOLLOW\|O_NONBLOCK\|O_NOCTTY)`, fstat regular ≤ 1048576, bounded read, never block on FIFO, reason names expected.json | covered, stronger (nonblock/noctty); cap value unconstrained by routed text |
| N6 symlinked case is a failure, not a silent skip | non-dot symlink in the fixture dir → `symlinked case directory refused`, run exits 1 even with `--min-cases 0` | covered |
| "Add a fixture or counter probe for each" | hostile selftest P1-selftest-argv, P2-fixture-dot-git, P3-commit-without-init, P4-expected-json-guard, P5-symlinked-case; benign base `01-single-literal-clean` exists in the tree; exit 1 required against base runner f1ffb81 | covered |

No routed requirement is dropped or weakened. Contract additions beyond routed text (never
starting the gate on argv refusal; exit 1 even with `--min-cases 0`) are tightenings.

## Findings

- LOW — F1, allowlist admits one argparse-ambiguous token. The gate parser
  (`gate.py:820-831`, exported at a16602a) defines exactly `--root --revision --population
  --ledger --json --selftest` (+`-h/--help`), `StoreOnce` on the four valued options,
  `parse_args` (gate.py:882). The only name that is a prefix of two allowed names and of no
  other option is `r` (root, revision). The contract admits `--r`; argparse rejects it as
  ambiguous, so a future case using it would fail as an ordinary gate failure instead of the
  contract's argv-refusal path. No committed case uses `--r`; no case breaks today. Suggested
  one-clause fix: "and is unambiguous among the four names".
- INFO — F2, option VALUES are unrestricted. `--root=/`, `--ledger=<absolute path>` etc. pass
  the allowlist (name allowed, value free-form) and argparse last-wins lets case argv override
  the runner's own values (runner.py:450-463). Impact bounded: the N1 refusal closes the
  `--selftest` delegation (gate.py:858-868 forwards extras to a nested runner), gate git calls
  strip inherited git env, and findings echo ids/reasons, not file content. The routed text
  does not demand value rules, so this is a decision to state, not a routed drop.
- INFO — F3, wording: `symlinked case directory refused` also fires for a non-dot symlinked
  FILE (e.g. a symlinked expected.json). Stricter than routed N6 (cases only); only the reason
  string says "directory". Cosmetic.
- INFO — F4, numbering: hostile probe P4 maps to routed gap N5 (P5→N6); the P/N offset invites
  misreading in the SCORECARD. No text change required beyond awareness.
- STATE — the contract requires committed specs at `scripts/fixtures/citing-set-hostile/<case>/hostile.json`;
  that directory does not exist at a16602a (ls-tree empty). The build must add it; contract is
  internally consistent (specs are read by the hostile selftest, not the runner).

## Committed case.json inventory (all 8 of 45; the other 37 have no case.json)

Exported via `git archive a16602a961da...`; contents read in full.

- 30-document-not-regular-file: setup `[{op: fifo, path: population.json}]`; no argv.
- 33-corpus-empty: setup `[{op: mkdir, path: corpus/knowledge}]`; no argv.
- 36-revision-not-found: argv `["--revision", "no-such-revision"]`; setup `git_init`, `git_commit` (message "fixture").
- 37-root-not-repository-top-level: root `"sub"`, argv `["--revision", "HEAD"]`; setup `git_init`, `git_commit`.
- 42-repeated-population-option: argv `["--population", "population.json"]`; no setup.
- 43-repeated-ledger-equals-form: argv `["--ledger=ledger.json"]`; no setup.
- 44-repeated-root-abbreviated: argv `["--roo", "."]`; no setup.
- 45-repeated-revision-abbreviated: argv `["--revision", "HEAD", "--rev", "HEAD"]`; setup `git_init`, `git_commit`.

Contract-rule check against these 45:
- argv allowlist: tokens `--revision`, `--rev` (prefix of revision, unique), `--roo` (prefix of
  root, unique), `--population`, `--ledger` (equals form, name `ledger`); values `HEAD`,
  `no-such-revision`, `population.json`, `ledger.json`, `.` — every token admissible; none is
  `--r` (F1). StoreOnce repeats (42, 43, 45) are per-token legal, gate refusal is the expected
  outcome under test. PASS.
- git_commit ordering: 36, 37, 45 each have `git_init` earlier in the same list. PASS.
- N2 `.git` rule: zero entries named `.git` in the committed fixtures. PASS.
- N6 symlink rule: zero symlinks (all 188 entries mode 100644). PASS.
- N5 guard: all expected.json regular; max committed expected.json = 168 bytes
  (largest fixture file overall 1375 B) ≪ 1048576. PASS.
- Cases 30 and 33 need fifo/mkdir setup ops, which the contract keeps. PASS.
So no contract rule breaks any of the 45 committed cases. This also confirms the round-30
ruling's inventory (spotcheck.md:163-166) — same eight cases, same ops, same argv spellings.

## Commands run (all from /home/vgpnk/Projects/shokunin/kake-shokunin, exit 0)

1. `git rev-parse HEAD` → a16602a961da5d6e75cfa09a1118a416ad01225b (matches claims).
2. `git show a16602a...:scripts/citing_set.py > $SANDBOX/gate.py` (916 lines); same for
   `citing_set_selftest.py` (635 lines) — analyzed via grep/read on sandbox copies.
3. `git ls-tree a16602a... scripts/fixtures/citing-set/` → 45 case dirs;
   `git ls-tree -r --name-only ... | grep -c case.json` → 8;
   `git ls-tree a16602a... scripts/fixtures/citing-set-hostile` → empty.
4. `git ls-tree -r -l ... | sort -k4 -nr | head` → max 1375 B; mode census `188 × 100644`.
5. `git archive a16602a... scripts/fixtures/citing-set | tar -x -C $SANDBOX` then
   `find ... -name case.json | sort` → the 8 paths above; read × 8.
6. `find $SANDBOX/scripts/fixtures/citing-set \( -name .git -o -type l -o -type p \) | wc -l` → 0;
   max expected.json 168 B; 188 files.
7. One earlier loop (`git cat-file -e` per case.json) exited 0 with no output (temp-shell
   artifact); superseded by the archive export, which is the authoritative inventory.

## Residual risk and verification gaps

- Static review of contract text and committed bytes only; the repaired runner does not exist
  at a16602a, so no behavior (exit codes, summary JSON, P1-P5 outcomes) was executed. The C1
  counter (`c1_sandbox_probes.py`) and hostile selftest run are the L1's checks.
- Hold-only items NOT routed into defect 1 remain open by routing and are not contract
  regressions: N4 nested-run timeout (practical vector closed by N1 refusal), N7 corpus-root
  lstat final component, N8 uncaught decode/recursion errors, N10-N12.
- F2 (free-form values) is the one place a hostile fixture still steers the gate inside the
  contract as written; rated INFO per routed scope, decision belongs to the L1.
- Installs: none.

Report: .ufo/waves/round-31/w1/ReviewHostileContract.md
