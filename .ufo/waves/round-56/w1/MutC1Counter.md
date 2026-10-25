# MutC1Counter

Method: copied `.ufo/waves/round-56/c56_selftally.py` to scratch `/tmp/mutc1-ng3zmrjd` (pristine sha256
`cf8a3f380704…9c07`, unchanged after the run — original never edited). Detector = `python3 -B <copy> --selftest`
(13 sandbox cases + 7 unit checks). Baseline on pristine copy: exit 0, `c56 selftally selftest: 20/20` — detector
valid. Each mutant is one exact-count string substitution on a fresh copy; 16 mutants run.

## MUTANTS:

| id | single-point change | selftest result | evidence (first failing case) |
|---|---|---|---|
| M01 | `claim != tally[1]` → `claim > tally[1]` | KILLED (exit 1, 19/20) | `do_nothing_stale_count` got 0 problems, wanted `claim_ne_observed` |
| M02 | `tool_changed` check dropped (`problems.append` → `pass`) | KILLED (exit 1, 19/20) | `tool_replaced_by_fake_print` got 0 problems, wanted `tool_changed` |
| M03 | `claim = sum(nums)` → `nums[0]` | SURVIVED (exit 0, 20/20) | no case separates first-claim from summed claims |
| M04 | `if code != 0 or tally[0] != tally[1]` → `if code != 0` | KILLED (exit 1, 19/20) | `tally_not_equal_pass_fail` reported only `tool_changed`, wanted `selftest_failed` |
| M05 | `_is_selftest_span` returns `True` always | KILLED (exit 1, 18/20) | `command_swapped_to_other_script` ran beta as alpha, wanted `command_missing` |
| M06 | `documented_command` drops leading `VAR=value` word | KILLED (exit 1, 18/20) | `pass` case: beta ran without `PIN=1` → `selftest_failed`; also `env_prefix_split` unit |
| M07 | `parse_tally` returns first match instead of last | SURVIVED (exit 0, 20/20) | every fixture output holds a single tally line |
| M08 | `met = mism == 0 and len(results) == expected` → `mism == 0` | KILLED (exit 1, 19/20) | `population_one_short` exited 0, wanted 1 |
| M09 | `table_rows` last occurrence wins (dup-key guard removed) | SURVIVED (exit 0, 20/20) | no fixture has a duplicated row name |
| M10 | `blob(root, base_rev, script)` → `blob(root, rev, script)` | KILLED (exit 1, 19/20) | `tool_replaced_by_fake_print` got 0 problems, wanted `tool_changed` |
| M11 | `return (0 if met else 1)` → `(1 if met else 0)` | KILLED (exit 1, 8/20) | `pass` case exited 1, wanted 0 |
| M12 | `TimeoutExpired` → append OK row + `continue` | SURVIVED (exit 0, 20/20) | no fixture reaches the timeout path (TIMEOUT=300) |
| M13 | `clone = clone_at(root, rev)` → `clone = root` (no clone) | SURVIVED (exit 0, 20/20) | every case measures tip == worktree HEAD, so running in root is equivalent |
| M14 | `command_missing` problem dropped (row reported OK) | KILLED (exit 1, 19/20) | `command_swapped_to_other_script` got 0 problems, wanted `command_missing` |
| M15 | `_is_selftest_span` drops `--selftest`/`*selftest*` marker | KILLED (exit 1, 19/20) | unit `entry_command_not_selftest` failed |
| M16 | row regex `^ {0,3}\|` → `^\|` (space tolerance removed) | SURVIVED (exit 0, 20/20) | all fixture tables start at column 0 |

Mutant copies with sha256 (12-hex) kept in scratch: M01 `1c9a49e0b3f3`, M02 `fdddb49e4be4`, M03 `0f18e5b39a5f`,
M04 `e57863a92b1c`, M05 `ef3e2d0c1a2a`, M06 `3fbd0a10a1b7`, M07 `1a7d5a9d0bd2`, M08 `f9d80de62b4d`,
M09 `77f9c33bb373`, M10 `6688ce6a35f8`, M11 `8d6971fb46b4`, M12 `7f8e65584d0f`, M13 `08a17c76fd2b`,
M14 `6e57bdff4672`, M15 `d4b52f79ceef`, M16 `b5c9f1eb1a49`. Scratch is disposable; nothing outside it and this
report was written.

## SURVIVORS:

- **M03 (first claim only):** cases only use multi-claim cells whose sum AND first item both differ from the
  observed total (`(2)(2)(1)` → 5 or 2, both ≠ 4). No case where claims split into groups summing exactly to
  the observed total, so first-only is indistinguishable from summing.
- **M07 (first tally match):** every fixture script prints exactly one `A/B` line, so first/last coincide. No
  multi-tally output exercises the last-match-wins rule in `parse_tally`.
- **M09 (last table row wins):** no fixture repeats a row name, so first-wins vs last-wins never diverges; the
  "first occurrence wins" contract is untested.
- **M12 (timeout swallowed):** all fixture selftests return instantly; the `TimeoutExpired` branch is never
  reached, so converting it into a pass is invisible.
- **M13 (clone skipped):** every case measures `tip`, which IS the sandbox worktree HEAD, so running the
  documented command in the measured root gives identical bytes. The "clone and check out the measured
  revision" guarantee is untested.
- **M16 (indented table rejected):** all fixture tables are flush-left; the `^ {0,3}\|` tolerance for indented
  (still valid Markdown) tables is untested.

## PROPOSED FIXTURES:

All six were executed against both pristine and mutant copies (same sandbox mechanism as the selftest cases);
each is a `cases.append(...)`-style addition. "pristine" line = case passes as honest control; "mutant" line =
case assertion would fail → selftest exit != 0 → kill.

- **F03 kills M03** — case `claims_split_across_groups`, `want=0`.
  Skill: `| alpha | `python3 -B t/alpha_selftest.py` (2 fixtures) (2 fixtures) |` + standard beta row. Scripts:
  alpha prints `selftest: 4/4 passed`, beta = `FAKE_ENV`. Pristine: claim 2+2=4, exit 0. M03: claim 2 ≠ 4 →
  false `claim_ne_observed`, exit 1.
- **F07 kills M07** — case `last_tally_line_wins`, `want=0`.
  Alpha script: `print("stage1 selftest: 3/3 passed")` then `print("selftest: 4/4 passed")`. Skill unchanged
  (`(4 fixtures)`). Pristine: last match 4/4, exit 0. M07: first match 3/3 → false `claim_ne_observed`, exit 1.
- **F09 kills M09** — case `first_table_row_wins`, `want=0`.
  Skill table lists `alpha` twice: first `(4 fixtures)` (correct), then a stale `| alpha | ... (9 fixtures) |`;
  beta row last. Scripts unchanged. Pristine: first row wins, claim 4 = observed 4/4, exit 0. M09: claim 9 ≠ 4,
  exit 1.
- **F12 kills M12** — case `timeout_is_unevaluable`, `want=2, sub="timeout"`, with the case harness setting
  `c56_selftally.TIMEOUT = 1` around the call (selftest may patch the module constant).
  Alpha script: `import time; time.sleep(30)` then print `selftest: 4/4 passed`. Pristine: exit 2 with
  `["timeout"]`. M12: alpha reported OK, beta OK → exit 0 (predicate falsely met).
- **F13 kills M13** — case `measures_checked_out_revision`, `want=0`; needs the case harness to support
  measuring a rev that is not HEAD (three-commit sandbox: `base` = good scripts; `tip1` = skill + good scripts;
  then commit broken alpha `print("selftest: 2/3 passed")` as `tip2` = HEAD; call `measure(d, tip1, ...)`).
  Pristine: clone checks out tip1, runs 4/4 alpha → exit 0. M13: runs the tip2 worktree → observed 2/3 →
  `selftest_failed` + `claim_ne_observed`, exit 1.
- **F16 kills M16** — case `indented_table_rows`, `want=0`.
  Skill text: the entire standard two-row table indented by two spaces (valid Markdown, ≤3 spaces). Pristine:
  rows found, exit 0. M16: both rows `row_missing`, exit 1.

Coverage finding only: the six survivors are gaps in the selftest's fixture matrix, not defects in the frozen
v1 contract; no source change made or proposed here.

VERDICT: 16 mutants run against the C1 selftest — 10 killed, 6 survived (M03 first-claim, M07 first-tally,
M09 last-row, M12 timeout-swallow, M13 no-clone, M16 no-indent-tolerance); all 6 killed by fixtures provided
and executed here; original c56_selftally.py byte-identical (sha256 cf8a3f38…9c07 before and after).
