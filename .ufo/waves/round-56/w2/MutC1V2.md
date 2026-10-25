# MutC1V2

Mutation probe of `.ufo/waves/round-56/c56_selftally.py` (C1 v2) at lane tip `a450e43e696d032e3ac308383f6b3394e0c92860`. All work in a throwaway clone `/tmp/mutc1v2-FxUw` (`git clone -q --no-checkout` + `git -C … checkout -q a450e43e…`); the lane repo, its jj/Git state, and sibling lanes were never touched. Detector: `python3 -B .ufo/waves/round-56/c56_selftally.py --selftest` (~3 s per run), executed on pristine, on each mutant, and on restored bytes.

- Baseline pristine: exit 0, `c56 selftally selftest: 47/47` — detector valid.
- 24 single-point mutants (13 assigned + 11 supplementary); each target string asserted to occur exactly once before substitution; bytes restored and sha256-verified after every run.
- Pristine sha256 before = after = `591d2701debc26b343fec55603c994f2686a7760b6828c0ac3eb4eddda1d5dc1`.
- Result: 16 KILLED, 8 SURVIVED (all survivors exit 0 with 47/47).

## MUTANTS:

Line refs are `.ufo/waves/round-56/c56_selftally.py` at `a450e43e`. "FF" = first failing selftest case.

| ID | Single-point mutation (site) | Verdict | FF |
|---|---|---|---|
| M01 | drop `duplicate_row` (:245) | KILLED | duplicate_row_earlier: exp 1 `duplicate_row`, got 1 w/ `command_missing` |
| M02 | `len(nums) != nclaims` → `<` (:260) | KILLED | two_claims_junk_sum_is_ambiguous: exp 1 `claim_ambiguous`, got 0 |
| M03 | `helpers_changed` checks only the script (:220) | KILLED | helper_beside_script_changed: exp 1 `tool_changed`, got 0 |
| M04 | header column ignored, `idx = 1` (:153) | SURVIVED | — |
| M05 | env scrub removed, `**os.environ` (:203) | KILLED | env_pin_removed: exp 1 `selftest_failed`, got 0 |
| M06 | `PIN_RX` → `.*` (:59) | SURVIVED | — |
| M07 | `command_problem` never fails (:169 `if False:`) | KILLED | fake_command_c_shadowing_honest: exp 1 `command_invalid`, got 2 `tally_unparsable` |
| M08 | `parse_tally` first match wins (:180 `found = found or …`) | KILLED | pass_last_tally_line_wins: exp 0, got 1 `claim_ne_observed` |
| M09 | `rows_checked` by table lookup (:296) | SURVIVED | — |
| M10 | timeout → row passes (:273-274) | KILLED | timeout_is_unevaluable: exp 2 `timeout`, got 0 |
| M11 | clone skipped, `clone_at` returns root (:186) | SURVIVED | — |
| M12 | table split on every pipe (:116) | SURVIVED | — |
| M13 | unanchored selftest tally rx (:80, `^\s*` → `\s*`) | SURVIVED | — |
| M14 | claim vs `tally[0]` (:287) | SURVIVED | — |
| M15 | `selftest_failed` drops exit-code cond (:285) | SURVIVED | — |
| M16 | `_strip_brackets` disabled (:129) | KILLED | unit: brackets_stripped |
| M17 | `_is_selftest_words` drops script membership (:144) | KILLED | command_swapped_to_other_script: exp `command_missing`, got `command_invalid` |
| M18 | `clone_at` keeps dir on failure (:195) | KILLED | unit: clone_cleanup_on_failure |
| M19 | `met` ignores `checked == expected` (:297) | KILLED | population_one_short: exp 1, got 0 |
| M20 | `documented_command` takes first parseable span (:159) | KILLED | command_swapped_to_other_script: exp `command_missing`, got `command_invalid` |
| M21 | `row_missing` problem dropped (:242) | KILLED | row_deleted: exp `row_missing`, absent |
| M22 | `command_problem` pin loop dropped (:167) | KILLED | pass: exp 0, got 1 (beta `command_invalid`) |
| M23 | `run_command` drops pin injection (:206) | KILLED | pass: exp 0, got 1 (beta `selftest_failed` 2/3) |
| M24 | `documented_command` header-None guard dropped (:151) | KILLED | crash: TypeError from `enumerate(None)` path |

## SURVIVORS:

- **M04 — header column ignored** (`documented_command` :153 pinned to cell 1). `command_in_other_column_shadows_selftest_cell` (:401) still fails under the mutant because beta's missing command preserves exit 1 and the `command_missing` substring; nothing asserts *alpha* resolved to the Self-test cell. Real coverage gap — the Self-test-column binding is untested.
- **M06 — `PIN_RX` widened to `.*`** (:59). The selftest always overrides `pin_rx=TEST_PIN` (`measure(d, tip, …, pin_rx=TEST_PIN)` :417), so the production allowlist regex is dead in every test path; `command_problem` :167 and `run_command` :206 only ever see `PIN=1`. Real coverage gap — the shipped `KAKE_R5[0-9]…` pattern is untested (harness wiring defect, not contract defect).
- **M09 — `rows_checked` by table lookup** (:296). Equivalent mutant: every `checked: false` append (:242, :248, :249-region, command_invalid) carries ≥1 problem, so `mism == 0` ⇒ all results `checked: true` ⇒ lookup count == checked count; `met` (:297) is unchanged on every input. No behavioral fixture can kill it; note that measure-local `checked` is redundant with `mism` for the exit gate (render/main recompute their own).
- **M11 — clone skipped** (`clone_at` :186 returns root). Every case's sandbox worktree equals the tip commit, so running in root is indistinguishable; `_clone_cleans_up` still passes (no dir is ever created). Coverage gap — "measure committed bytes, not the worktree" is untested.
- **M12 — split on every pipe** (:116). The only escaped-pipe case, `pass_escaped_pipe_in_later_cell` (:376), puts `\|` in a separate later row whose mis-split is harmless; no case has `\|` inside the measured row's own cells. Coverage gap.
- **M13 — unanchored selftest tally rx** (:80). No case prints a prefixed `selftest: A/B` noise line after the true tally; `parse_date_is_not_a_tally`/`parse_dash_name_line` stay non-matching even unanchored. Coverage gap — the v2 "tally line must be anchored" guarantee is untested.
- **M14 — claim compared to `tally[0]`** (:287). Exit-code-equivalent on all current cases: when A≠B the row already carries `selftest_failed`, and both `claim_ne_observed` cases (:377, :378) have A==B=4 so `tally[0]` differs from the claim. The problem-list difference is never asserted. Killable with a stronger fixture.
- **M15 — `selftest_failed` drops exit-code condition** (:285). No case exits non-zero with an equal tally A/B, so `code != 0` is untested. Coverage gap.

## PROPOSED FIXTURES:

Each is a concrete selftest addition that kills its survivor (verified by reasoning against the mutant's control flow; not run — probe scope is detection only).

- F1 (M04): unit — `documented_command((["alpha", "`python3 -B a/b.py --root X`", "`python3 -B a/b.py --selftest` (3 fixtures)"], ["name", "entry command", "self-test"]), "a/b.py")` must equal `(["python3","-B","a/b.py","--selftest"], <third-cell text>)`. Mutant returns the entry-command words.
- F2 (M06): units exercising the DEFAULT `pin_rx` — `command_problem(["KAKE_R52_SELFTEST_REV=abc1234","python3","-B","a/b.py"], "a/b.py", []) is None` and `command_problem(["OTHER=1","python3","-B","a/b.py"], "a/b.py", []) is not None`. Under `.*` the first call degrades to `command_invalid`.
- F3 (M11): in the `pass` sandbox, after the tip commit, overwrite `t/alpha_selftest.py` in the worktree (uncommitted) with a fake printing `selftest: 9/9`; `measure(d, tip)` must still exit 0 (clean clone yields committed 4/4). Mutant observes 9/9 → `claim_ne_observed`.
- F4 (M12): case with an escaped pipe inside alpha's own Self-test cell — `a_cell = "ops \\| notes `python3 -B t/alpha_selftest.py` (4 fixtures)"`, want=0. Every-pipe split mis-locates the cell → `command_missing`.
- F5 (M13): alpha prints `selftest: 4/4 passed` then `>>> selftest: 9/9 (see run log)`; want=0. Anchored rx rejects the prefixed line; unanchored rx adopts 9/9 (last match wins) → `claim_ne_observed`.
- F6 (M14): alpha script `print("selftest: 4/9 passed")` + `sys.exit(1)`, `a_cell` claim `(4 fixtures)`, want=1, and assert `"claim_ne_observed" in json.dumps(results)`. Original flags it (4 ≠ total 9); mutant's claim == `tally[0]` == 4 → absent.
- F7 (M15): alpha script `print("selftest: 4/4 passed")` + `sys.exit(1)`, claim 4, want=1, sub `selftest_failed`. Mutant sees A==B → no problem → exit 0.
- M09: no behavioral fixture exists (equivalent mutant, see above); if `rows_checked` is meant to be independently observable from `measure`, return it in the results payload rather than deriving it in three places.

## RESTORATION EVIDENCE:

- After every mutant run the pristine bytes were rewritten and sha256 re-verified inside the driver (assert on mismatch).
- Final: `git -C /tmp/mutc1v2-FxUw status --porcelain` → empty; `git rev-parse HEAD` → `a450e43e696d032e3ac308383f6b3394e0c92860`; `sha256sum` → `591d2701debc26b343fec55603c994f2686a7760b6828c0ac3eb4eddda1d5dc1`; restored copy re-ran `--selftest` → exit 0, 47/47.
- Lane writes: this report file only. No pacman/tool installs were needed.

VERDICT: 24 mutants vs C1-v2 selftest — 16 KILLED, 8 SURVIVED (M04 M06 M09 M11 M12 M13 M14 M15); 6 are real selftest coverage gaps with fixtures proposed (M09 equivalent, M06 is a harness-wiring gap leaving the production PIN_RX untested).
