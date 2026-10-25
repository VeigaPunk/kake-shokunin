# MutC1Counter

Round-55 W1 mutation probe of `.ufo/waves/round-55/c55_readme_index.py` (C1 counter) and its `--selftest`.
Method: original copied to a `mktemp -d` scratch dir; pristine copy baseline `--selftest` = exit 0 (`c55 readme-index selftest: 10/10`); 16 single-point mutants applied to scratch copies only (each old-string verified to occur exactly once), each run's `--selftest` executed; survivor kill-fixtures were then run for real against both pristine and mutant modules via `measure()`. Original file read-only throughout: sha256 `dfa4b37083dc3bc437daffac1db56428627c6013096d980b15dc69956f444660` identical before and after all runs; scratch dirs removed afterwards. No tool installs (stock python3/git). Selftest cases: pass, fail_unindexed, fail_thin_short, fail_thin_offtopic, fail_prefix_name, fail_dangling, pass_brace_expands, fail_brace_member_missing, fail_deleted_population, fail_no_section.

MUTANTS:

| id  | change (single point)                                                             | selftest result |
|-----|------------------------------------------------------------------------------------|-----------------|
| M01 | `FLOOR = 46` -> `FLOOR = 45`                                                        | exit 0, 10/10 — SURVIVED |
| M02 | boundary drop, first form (stray `r")"` left)                                       | exit 1, SyntaxError at line 107, selftest never ran — killed by crash only; superseded by M02b |
| M02b| boundary `(?![A-Za-z0-9_.-])` deleted cleanly from the row pattern                  | exit 1, 9/10, `FAIL fail_prefix_name: expected 1, got 0` — KILLED |
| M03 | thin overlap clause removed (`or not shared`)                                       | exit 1, 9/10, `FAIL fail_thin_offtopic: expected 1, got 0` — KILLED |
| M04 | `expand()` returns `[token]` unexpanded (brace expansion dead)                      | exit 1, 9/10, `FAIL pass_brace_expands: expected 0, got 1` — KILLED |
| M05 | token threshold `< 5` -> `< 6`                                                      | exit 0, 10/10 — SURVIVED |
| M06 | dangling detection disabled (`if not resolves(...)` -> `if False and ...`)          | exit 1, 8/10, `FAIL fail_dangling`, `FAIL fail_brace_member_missing` — KILLED |
| M07 | unindexed scan skips `.json` knowledge files                                        | exit 0, 10/10 — SURVIVED |
| M08 | `show()` reads working tree file instead of `git show rev:path`                     | exit 0, 10/10 — SURVIVED |
| M09 | section regex matches any `## ` heading (`^## .*?\s*\n(.*?)(?=^## \|\Z)`)           | exit 1, 9/10, `FAIL fail_no_section: expected 2, got 1` — KILLED |
| M10 | lane-root base `""` dropped from `BASES`                                            | exit 0, 10/10 — SURVIVED |
| M11 | word regex `{4,}` -> `{3,}` (4-letter words now count as overlap)                   | exit 0, 10/10 — SURVIVED |
| M12 | thin-overlap window `body[:1500]` -> `body` (whole file)                            | exit 0, 10/10 — SURVIVED |
| M13 | coverage rows slice `[2:]` -> `[1:]` (separator row kept as row)                    | exit 0, 10/10 — SURVIVED (exit-code-equivalent) |
| M14 | `"json"` removed from `EXTS` (json tokens never dangling-checked)                   | exit 0, 10/10 — SURVIVED |
| M15 | exit polarity flipped (`return (1 if met else 0)`)                                  | exit 1, 1/10 (9 cases flip) — KILLED |
| M16 | `and` -> `or` in `met` (population guard bypasses mismatches)                       | exit 1, 3/10 (7 cases flip) — KILLED |

KILLED: M02b, M03, M04, M06, M09, M15, M16 (7). SURVIVED: M01, M05, M07, M08, M10, M11, M12, M13, M14 (9). (M02 crash-kill is a mutant-construction artifact, not a selftest detection.)

SURVIVORS:

- M01 — root cause: the selftest derives its fixture population from the constant under test (`range(FLOOR)` for entries and rows), so lowering FLOOR just scales the whole suite down; every case stays green.
- M05 — no selftest coverage cell has 4-6 whitespace tokens while sharing a body word; the only 5-token cell (fail_thin_offtopic) also fails the overlap clause, so the threshold is not pinned between 5 and 6.
- M07 — all selftest knowledge files are `.md`; `.json` unindexed detection is untested.
- M08 — selftest fixtures commit clean worktrees, so worktree bytes always equal HEAD; committed-bytes-only reading is never pinned.
- M10 — every selftest token resolves under `corpus/`-prefixed bases; the lane-root base `""` is never exercised.
- M11 — every selftest cell that must pass overlap shares 5+ letter words, and the negative case shares none at all; words of length 4 are never the deciding overlap.
- M12 — selftest bodies are far under 1500 chars, so the slice window is never distinguishing.
- M13 — the separator row can never name a knowledge file or add a backticked token, so exit codes are identical on every expressible fixture; only the reported `coverage_rows` fact changes (verified 46 -> 47 on the pass fixture). This is a selftest blind spot: it asserts exit codes only, never `measure()` facts.
- M14 — no selftest token uses a `.json` extension; json dangling detection is untested.

PROPOSED FIXTURES: (all validated by running pristine vs mutant; form is "selftest case (files, expected)")

- M01: hardcode the population instead of deriving it from FLOOR — `entries`/`good_rows` built over literal `range(46)`; case `(entries46 minus e0.md, README with rows46 minus e0's row, 1)`. Verified: pristine 1, M01 mutant 0 (pass case with literal 46 stays 0 on both).
- M05: pass fixture with e0's coverage cell `Widget0 cache invalidation rules verbatim` (5 tokens, shares widget0/cache/invalidation/rules with the e0 body), expect 0. Verified: pristine 0, mutant 1.
- M07: pass fixture plus `corpus/knowledge/zz.json` (`{"note": "x"}`) with no README row, expect 1. Verified: pristine 1, mutant 0.
- M08: pass fixture committed, then a post-commit hook rewrites the worktree README so e1's coverage cell is `TBD`; expect 0 (HEAD is authoritative). Verified: pristine 0 (reads HEAD), mutant 1 (reads worktree). Needs the case harness to support a post-commit worktree edit.
- M10: pass fixture plus committed root-level `notes.txt` and section extra line `Ops runbook: `+"`notes.txt`"+`.`, expect 0. Verified: pristine 0, mutant 1 (dangling).
- M11: pass fixture with e0's coverage cell `just text here and more` (5 tokens, only <=4-letter words, shares `text` with the e0 body), expect 1 (thin: no 5+ letter shared word). Verified: pristine 1, mutant 0.
- M12: pass fixture with e0 body = H1 + `source: S900` + ~2.4k chars of filler (`filler block prose on unrelated matters` repeated) + trailing `zonkeys graze quietly beyond the window`, e0 coverage cell `entirely different note about zonkeys`, expect 1 (shared word lies only beyond offset 1500). Verified: pristine 1, mutant 0.
- M13: not killable by any exit-code fixture; kill requires asserting facts — e.g. run `--json` on the pass case and require `coverage_rows == 46` (mutant reports 47, verified). Recommended: extend selftest to compare key facts (`knowledge_files`, `coverage_rows`, `unindexed`/`thin`/`dangling` lists) on at least the pass case.
- M14: pass fixture with section extra line `Snapshot: `+"`data.json`"+`.` and no such file, expect 1. Verified: pristine 1, mutant 0.

Restoration evidence: no lane path other than this report was written; the script under test was only ever read (sha256 unchanged before/after, shown above); all mutants and fixtures lived in `mktemp -d` scratch dirs, now deleted. No subagent dispatch, no git/jj state changes, no pacman use.

VERDICT: 16 single-point mutants probed against `--selftest`: 7 KILLED (M02b boundary drop, M03 overlap clause, M04 brace expansion, M06 dangling, M09 section regex, M15 exit polarity, M16 met conjunction), 9 SURVIVED (M01 FLOOR self-reference, M05 threshold, M07/M14 extension gaps, M08 committed-bytes, M10 root base, M11 word floor, M12 1500 window, M13 facts blind spot); verified kill-fixtures delivered for 8 of 9 survivors, M13 requiring a facts assertion.
