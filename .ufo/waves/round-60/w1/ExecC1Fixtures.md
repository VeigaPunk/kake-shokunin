# ExecC1Fixtures

Independent C1 fixture harness, authored only from `contract.md` § Claim C1 (no other seat's counter read). Deliverable:
`.ufo/waves/round-60/w1/ExecC1Fixtures.files/c60_gate_status_fixtures.py` (stdlib only; runs any
`python3 -B <counter> --root <fixture> --revision <sha> --work <dir>`).

Fixture model: each case is a real `git init -b main` repo in scratch with two commits. Commit 1 (PIN) writes every member at its pin-time body plus noise files; commit 2 (TIP, the measured revision) writes differing member bodies, SKILL.md, SCORECARD.md, symlinks, deletions. The pin sha is real and an ancestor of the tip, so `historical`/`never met` Kind cells can carry a genuine 40-hex pin. A dangling `commit-tree` commit (no parent, no branch) supplies a guaranteed non-ancestor 40-hex for `pin_not_ancestor`. Toy members are `sys.exit(k)` one-liners; probes assert substituted argv/env (e.g. `argv == git rev-parse HEAD`, `--rev <sha>`, `<scratch>` is an existing abs dir, `<fleet root>` literal). SKILL.md rows carry the real 8-cell registry shape (`| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |`), `Verdict map` = `` `0=met`; `1=not met`; `2=unevaluable`; `64=usage` ``. SCORECARD.md carries `| Axis | Score | Evidence pointer | Last change |` = 10/10/2.

Pass rule per case: observed exit == expected exit AND every expected class token present in stdout+stderr AND no other class token present (per-case `allow` relaxations for contract-silent neighbors). Class tokens checked verbatim: `unregistered duplicate_row row_incomplete unpinned pin_not_ancestor command_unparsable live_not_green historical_but_green historical_not_green_at_pin never_met_but_green` and predicate token `scores_held`.

CASES: (54; id — fixture delta — expected exit — expected class)

- `met_baseline` — 28 live members, all green — 0 — (none)
- `met_subdir_member` — `round-53/exec-quality-gate/...` moved to `round-53/sub/c53_gate_truth.py` — 0 — none (one-level `[a-z0-9-]+` subdir counts)
- `met_boundary_noise` — 28 members + 12 committed non-members (`round-47/*`, `round-5/*`, `round-60/*`, `round-53/a/b/`, `round-53/under_score/`, `c53_UPPER.py`, `*.PY`, `c53_.py`, `scripts/c53_*`) — 0 — none (counting noise breaks `members==28` or adds `unregistered`)
- `met_phantom_row` — extra row for uncommitted `c53_ghost.py` — 0 — none (population is committed paths, not rows)
- `member_symlink` — a member path committed as a symlink to a blob — 0 — none [AMBIGUITY A5]
- `unregistered` — one member's row dropped — 1 — `unregistered`
- `duplicate_row` — member row appended twice — 1 — `duplicate_row`
- `row_incomplete_cells` — 6-cell row — 1 — `row_incomplete`
- `row_incomplete_vmap` — 8 cells, `Verdict map` = `0:`/`1:` (no `0=`/`1=`) — 1 — `row_incomplete`
- `met_vmap_control` — literal `0=`/`1=` vmap — 0 — none
- `fenced_row_unregistered` — member's only row inside a fenced block — 1 — `unregistered`
- `commented_row_unregistered` — member's only row inside `<!-- -->` — 1 — `unregistered`
- `indented_row_unregistered` — member's only row 4-space indented — 1 — `unregistered`
- `wrong_table_unregistered` — member's row in a table whose first three cells are `A|B|C` — 1 — `unregistered`
- `wrong_cell_unregistered` — row's `Entry command` names `round-99/c99_ghost.py` — 1 — `unregistered`
- `label_default_live` — Kind `gate` (no label word) — 0 — none
- `label_nevermet_hyphen` — Kind `gate (never-met hyphen variant)` — 0 — none (`never-met` ≠ `never met` → live)
- `kind_both_words_hist_wins` — Kind contains `historical {pin}` AND `never met` — 0 — none (contract order ⇒ historical; allows `never_met_but_green` under the other reading)
- `live_not_green` — live member exits 1 — 1 — `live_not_green`
- `live_exit2_not_green` — live member exits 2 — 1 — `live_not_green`
- `live_timeout_not_green` — live member exits 124 (timeout stand-in; real 1800 s timeout untested) — 1 — `live_not_green`
- `historical_met` — historical+pinned, green at pin, red at tip — 0 — none
- `historical_first_hex_pin` — Kind carries `{pin}` then `{side}` (two 40-hex) — 0 — none (first hex is the pin; allows `pin_not_ancestor`,`historical_not_green_at_pin` for a last-hex reader)
- `historical_but_green` — historical label, member green at tip — 1 — `historical_but_green` (R59-D1 control twin)
- `historical_not_green_at_pin` — historical+pinned, red at pin — 1 — `historical_not_green_at_pin`
- `unpinned_historical` — `historical` word, no 40-hex — 1 — `unpinned` (allows `historical_not_green_at_pin`,`pin_not_ancestor` for counters that probe a missing pin)
- `pin_not_ancestor` — Kind hex = dangling non-ancestor commit — 1 — `pin_not_ancestor` (allows `historical_not_green_at_pin` if e_P is still attempted)
- `never_met_clean` — `never met`+pinned, red at pin and tip — 0 — none
- `never_met_but_green_tip` — never met, green at tip — 1 — `never_met_but_green`
- `never_met_but_green_pin` — never met, green at pin — 1 — `never_met_but_green`
- `unpinned_never_met` — `never met` word, no 40-hex — 1 — `unpinned`
- `command_unparsable_quote` — unbalanced quote in command — 1 — `command_unparsable`
- `command_unparsable_sh` — `sh <path>` — 1 — `command_unparsable`
- `command_unparsable_bashwrap` — `bash -c 'python3 <path>'` — 1 — `command_unparsable`
- `command_no_backtick` — path in plain text, no backtick span — 1 — `command_unparsable` (allows `unregistered`) [AMBIGUITY A3]
- `command_echo_span` — first span `echo <path>`, second span `python3 -B <path>` — 1 — `command_unparsable` (first span containing the path wins)
- `placeholder_commit` / `placeholder_rev` / `placeholder_revision` / `placeholder_tip` — each placeholder must substitute the measured revision — 0 — none
- `placeholder_scratch` — `--work <scratch>` must substitute an existing abs dir — 0 — none
- `placeholder_fleet_root` — `<fleet root>` → literal `/home/vgpnk/Projects/shokunin` — 0 — none
- `bracket_kept` — `[--rev <rev>]` kept (all placeholders known, brackets stripped) — 0 — none
- `bracket_dropped` — `[--bogus]` dropped whole — 0 — none
- `bracket_dropped_partial` — `[--rev <rev> --bogus]` dropped whole — 0 — none
- `env_words_literal` — `NAME=value NAME2=ok python3 -B <path>` env must reach the member — 0 — none
- `env_words_substituted` — `FLAG=<rev>` before `python3` — 0 — none (allows `command_unparsable`) [AMBIGUITY A4]
- `extra_args_ok` — trailing `--root . --jobs 2 --json` pass through — 0 — none
- `score_cal_mutant` — calibration 2→10 — 1 — `scores_held` (R59-D2)
- `score_op_mutant` — operability 10→9 — 1 — `scores_held`
- `score_row_missing` — calibration row absent — 1 — `scores_held` (allows `unevaluable`→exit 2 is NOT allowed; see A6) — expected exit 1, token `scores_held`
- `unevaluable_no_skill` — SKILL.md absent at tip — 2 — none
- `unevaluable_no_scorecard` — SCORECARD.md absent at tip — 2 — none
- `unevaluable_bad_rev` — `--revision` names a commit not in the repo — 2 — none

HARNESS SELF-CHECK:
`--selfcheck` writes `counter_always0.py` (`sys.exit(0)`) and `counter_always1.py` (`sys.exit(1)`) into the scratch work dir and runs all 54 cases against each. Observed (transcript `ExecC1Fixtures.files/selfcheck.txt`):

- `counter_always0.py`: **24/54** — passes exactly the 24 expected-exit-0 cases; fails every exit-1/exit-2 case on exit code.
- `counter_always1.py`: **0/54** — fails all 24 exit-0 cases on exit code and all 27 exit-1/2 cases on missing class tokens (its output contains no class names).
- Self-check exit code 0 (the discrimination assertion held). The harness discriminates: an always-green counter can only score the met cases; an always-red counter can never score because class tokens are required, not just the exit code.

CONTRACT AMBIGUITIES:
- **A1 e_P cwd/tree.** "the same command also runs with the pin substituted" — the clone is only ever detached at the measured revision, so the executed member file is the TIP-tree body with the pin passed as an argument (the real rows' `--revision <commit>`). Fixtures implement this reading; `pin_body` additionally equals the intended pin-run exit wherever both readings can agree, so a "run the pin-tree file" counter passes the same cases. Where the readings provably diverge (tip body `argv`-dependent AND pin body different), the contract reading is used.
- **A2 Kind containing both `historical` and `never met`.** Class list order puts `historical` first; fixture `kind_both_words_hist_wins` expects the historical branch but tolerates a `never_met_but_green` print under the alternative reading.
- **A3 Entry-command cell with NO backtick span containing the path.** `command_unparsable` expected (no command can be derived); `unregistered` allowed ("contains m's path" arguably fails).
- **A4 Placeholder inside an env word value** (`FLAG=<rev>`): substitution expected to apply inside values; `command_unparsable` tolerated.
- **A5 Non-blob member paths** (symlink): regex is on committed paths, not types — fixture expects the member still counts (python3 resolves the link); a blob-only counter exits 1 here (flagged, not resolved).
- **A6 `Verdict map` cell identity**: fixtures assume the cell is identified by the header position of a matching table, matching real-lane rows.
- **A7 `<scratch>` freshness**: fixture accepts any existing absolute dir; "a fresh scratch dir" implies it is created (and empty) per run — a counter that reuses one dir across members still passes this fixture.
- **A8 Timeout**: real 1800 s timeout is only simulated by member exit 124 (`live_timeout_not_green`); the actual `TimeoutExpired` path is untestable within the wave budget.
- **A9 `score_row_missing`**: contract requires the three axis rows to hold 10/10/2; a missing row ⇒ scores_held==2 ⇒ not met ⇒ exit 1 with `scores_held`. An alternative exit-2 ("table unreadable") reading is flagged but not allowed.
- **A10 Output format for classes**: the contract never names an output format; the harness requires the class token verbatim in stdout+stderr (consistent with the C2 contract's `kind path` convention and the backticked class names in the text). A counter printing only `mismatches == 1` fails class cases — flagged as the single most likely false-negative source for w2.

Files: `c60_gate_status_fixtures.py` (harness, 818 lines), `counter_always0.py`, `counter_always1.py` (generated probes), `selfcheck.txt` (transcript). No installs; git 2.56.0 + python 3.14.8 only. Scratch `/fast/scratch/hyaku/kake-r60/ExecC1Fixtures` deleted at exit.

VERDICT: harness delivered — 54 fixture cases covering every C1 clause; self-check discriminates (always0 24/54, always1 0/54); 10 contract ambiguities flagged for the C1 counter author.
