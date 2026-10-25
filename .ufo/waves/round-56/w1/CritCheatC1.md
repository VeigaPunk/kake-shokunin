# CritCheatC1

Hypothesis under test: a do-nothing change (the registry keeps advertising its stale tallies) meets the C1 predicate
`tally_mismatches == 0 AND rows_checked == 10`.

Scratch lane clone `D=/tmp/tmp.Y3DekvvKPp` (`git clone -q --no-checkout <lane>`, `checkout -q 2d308e808bfd`); every edit
and commit is inside `$D` (`-c user.name=selftest -c user.email=selftest@local`, branches `e1`..`e8`); the lane worktree,
index and jj state were not touched; the only lane write is this report. No tool installs were needed (host `python3`).

Two counter identities, because the lane's C1 counter changed underneath this seat while it ran:

- **v1 (frozen at the contract commit)**: `git show 2d308e808bfd:.ufo/waves/round-56/c56_selftally.py`,
  sha256 `cf8a3f3807040d6ee7c90d2983f3454362abf9c1bdd6122a5a3bb99679e69c07`.
- **v2 (lane working tree at run time; `M` in `git status`)**: sha256
  `19066b5f09aa878ff6a42268319555e2f856b121790f808ce3d7c00851b428f5`, mtime 2026-10-25 19:39:26. Its docstring folds in
  wave-1 attacks (`w1/CriticC1Contract.md`, `w1/MutC1Counter.md`, `w1/ReviewerSelftallyCode.md`); the predicate sentence
  is unchanged. Both versions were run from the same `$D` revisions, so the v1/v2 columns are comparable.

EXPERIMENTS:

| # | edit in `$D` (exact) | counter | printed headline line | exit | predicate met |
|---|---|---|---|---|---|
| 1 | `SKILL.md` only: `(101 fixtures)`→`(106 fixtures)`, `(137 fixtures)`→`(204 fixtures)`, `(150 fixtures, all 34 sentences)`→`(235 fixtures, all 34 sentences)`, `(8/8;`→`(9/9;`, `(35 fixtures, generated sandbox repos`→`(44 fixtures, generated sandbox repos`, `(47 sandbox-repo fixtures`→`(54 sandbox-repo fixtures)`; c52 row left unpinned (`e1` 9a768ae) | v1 | `tally_mismatches=1 rows_checked=10 met=False` — `quote-truth-counter: claim=18 observed=17/18 MISMATCH selftest_failed` | 1 | no |
| 2 | as (1) plus `` `python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` `` → `` `KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` `` (`e2` 02d39c4) | v1 | `tally_mismatches=0 rows_checked=10 met=True` | 0 | yes |
| 2b | same commit, re-run after v2 landed | v2 | `tally_mismatches=0 rows_checked=10 met=True` | 0 | yes |
| 3 | `scripts/source_recheck_selftest.py` body replaced by `print("selftest: 106/106 passed")` (`e3` 744c6b8) | v1 | `tally_mismatches=1 rows_checked=10 met=False` — `source-recheck-audit … MISMATCH tool_changed` | 1 | no |
| 3b | same commit | v2 | `tally_mismatches=6 rows_checked=10 met=False` — `tool_changed` on base-path, source-recheck, robots, sitemap, redirect, citation | 1 | no |
| 4 | new `scripts/fake_wrapper.py` (prints `selftest: 106/106 passed`, exit 0); row command `` `python3 -B scripts/source_recheck_selftest.py` `` → `` `python3 -B scripts/fake_wrapper.py` `` (`e4` cabac41) | v1 | `tally_mismatches=1 rows_checked=10 met=False` — `source-recheck-audit: claim=None observed=None MISMATCH command_missing` | 1 | no |
| 4b | same commit | v2 | `tally_mismatches=1 rows_checked=9 met=False` — `command_missing` (row not counted, so the predicate is unreachable) | 1 | no |
| 5 | real robots row reverted to `(137 fixtures)`; a duplicate row inserted one line **earlier** with the same first cell and `` `python3 -B scripts/robots_audit_selftest.py [--tool PATH]` (204 fixtures) `` (`e5` 6bb351d) | v1 | `tally_mismatches=0 rows_checked=10 met=True` — `robots-expectation-audit: claim=204 observed=204/204 OK` while the real row still reads 137 | 0 | **yes (cheat)** |
| 5b | same commit | v2 | `tally_mismatches=1 rows_checked=10 met=False` — `robots-expectation-audit: claim=204 observed=204/204 MISMATCH duplicate_row` | 1 | no |
| 6 | robots self-test cell keeps its stale number and gains a padding claim: `` … [--tool PATH]` (204 fixtures) `` → `` … [--tool PATH]` (137 fixtures) (67 fixtures) `` (`e6` 445c1d5) | v1 | `tally_mismatches=0 rows_checked=10 met=True` — `robots-expectation-audit: claim=204 observed=204/204 OK`, visible headline still 137 | 0 | **yes (cheat)** |
| 6b | same commit | v2 | `tally_mismatches=1 rows_checked=10 met=False` — `claim_ambiguous` | 1 | no |
| 7 | all seven stale headlines kept verbatim, each padded: `(101 fixtures) (5 fixtures)`, `(137 fixtures) (67 fixtures)`, `(150 fixtures, all 34 sentences) (85 fixtures`, `(8/8; (1/1;`, `(35 fixtures, … (9 fixtures`, `(47 sandbox-repo fixtures; (7 sandbox-repo fixtures`; c52 row gains only the real pin (`e7` a74d9b6) | v1 | `tally_mismatches=0 rows_checked=10 met=True` | 0 | **yes (cheat)** |
| 7b | same commit | v2 | `tally_mismatches=6 rows_checked=10 met=False` — `claim_ambiguous` ×6 (source-recheck, robots, sitemap, citation, readme-index, yahoo) | 1 | no |
| 8 | robots **Entry command** cell (column 3) gains `` `python3 -B scripts/robots_audit_selftest.py` (204 fixtures) ``; the real **Self-test** cell (column 5) is reverted to `(137 fixtures)` (`e8` e64704b) | v1 | `tally_mismatches=0 rows_checked=10 met=True` — `robots-expectation-audit: claim=204 observed=204/204 OK` | 0 | **yes (cheat)** |
| 8b | same commit | v2 | `tally_mismatches=0 rows_checked=10 met=True` | 0 | **yes (cheat)** |

E1 was not re-run on v2 (its v1 run already isolates the pin requirement); every other cell above is a run.

CHEATS THAT PASSED:

1. **Duplicate earlier row** (v1 only, closed by v2 `duplicate_row`). `table_rows` kept the first occurrence of a first
   cell and v1 never counted occurrences, so a decoy row placed above the real one answered the counter while the real
   row still read `137`. Evidence: `e5`, v1 `met=True` / exit 0 with `robots-expectation-audit: claim=204`. Smallest safe
   correction: count occurrences and fail on more than one (v2's `duplicate_row`).
2. **Padded claim in the same cell** (v1 only, closed by v2 `claim_ambiguous`). v1 summed every regex match in the
   self-test cell, so `(137 fixtures) (67 fixtures)` satisfied `204` while the sentence a reader sees still says 137.
   Evidence: `e6` v1 exit 0; the all-rows variant `e7` also exited 0 on v1 with six stale headlines intact (only the c52
   pin is a real fix in `e7`). Smallest safe correction: one integer per cell unless the row is a declared sum (v2).
   Residual: `sum_ok=True` is still granted to `base-path-audit`, so that one row remains padable — harmless today
   because its claim is already correct, but it is the same hole for the next stale row.
3. **Command + claim in an earlier cell of the same row** (v1 **and** v2 — still open). `documented_command` returns the
   first cell (scanning cells 1..n) that holds a backticked selftest span, and the claim is read from *that* cell, so a
   span placed in the Entry-command column shadows the row's Self-test column. Evidence: `e8` exits 0 on v1 and on v2
   (`claim=204`), while the row's Self-test cell still reads `(137 fixtures)` — the registry now displays two
   contradictory tallies and the counter reads the flattering one. This survives every v2 check (`claim_ambiguous` only
   inspects the chosen cell, `command_invalid` only the words, `helpers_changed` only blobs).
   Smallest safe correction: reject a row that holds more than one selftest span for the pinned script
   (`command_ambiguous`), or bind the claim to the column whose header is `Self-test`. The span-count rule is two lines
   and closes it without touching `POP`.
4. Not cheats (rejected as designed): script replacement (`tool_changed`), wrapper + repointed command
   (`command_missing`, and `rows_checked=9` in v2), stale claims without the c52 pin (`selftest_failed`).

HONEST FIX RESULT:

- The honest fix is `SKILL.md`-only and passes on both counters: `e2` gives `tally_mismatches=0 rows_checked=10 met=True`,
  exit 0, on v1 and v2, with no `tool_changed` on any row (no script blob moves). Observed tallies at 2d308e808bfd:
  45, 106, 204, 235, 23, 9, 19, 18, 44, 54.
- The c52 env pin is mandatory, not cosmetic: without it the row prints `17/18` and exits non-zero (`e1`,
  `selftest_failed`), so no claim rewrite can rescue that row. Two residual weaknesses around the pin (code-read, not
  run): `PIN_RX` accepts any 7–40 hex characters and `run_command` forwards it, so a pin need not be the receipt's
  fixture revision `1ae8de5d4dee`; and the pin is only checked to exist, never against `.ufo/waves/round-52/control/`.
- v2 defect seen while testing (not a cheat): `helpers_changed` pins every base-revision `*.py` beside the pinned script,
  so replacing one `scripts/*.py` marks **six** unrelated rows `tool_changed` (`e3b`, `tally_mismatches=6`). The signal
  is not attributable to the row that changed, and any legitimate future edit to a base-revision `scripts/*.py` turns
  six rows red. Smallest safe correction: pin only the named script plus modules it imports (none of the ten import a
  local module), or files whose stem matches the pinned script.
- Contract-hygiene finding: the C1 counter that the lane path runs is no longer the frozen v1. It was replaced in the
  working tree (uncommitted) during W1, so two seats measuring the same revision at different wall-clock times get
  different verdicts (`e6`: exit 0 under v1, exit 1 under v2). Whichever version is authoritative, the round should
  record its sha256 and re-run the base control against it.

VERDICT: The predicate is satisfiable by do-nothing edits — padded claims and duplicate rows passed v1 (closed by v2), and a command+claim moved into an earlier cell of the same row still passes v2 with the stale tally left in place; the honest SKILL.md-only fix plus the c52 pin passes both.
