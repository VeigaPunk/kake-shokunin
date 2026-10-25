# ExecSelftestC1

Seat: falsify wave 2, C1 selftest and its registry row. Lane `kake-shokunin`; measured revision
`a450e43e696d032e3ac308383f6b3394e0c92860` in my own `mktemp -d` clone (`git rev-parse --show-toplevel` == `$D`).
Lane tree, index and jj untouched; only this report written. No tool installed (nothing needed).

## RUNS:

All runs executed in the clone at `a450e43`, cwd = clone root, with the counter's own fixed environment
(`env -i PATH HOME LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1`), which is the environment `run_command`
imposes (`c56_selftally.py:201-214`).

| # | command | result | exit |
|---|---|---|---|
| R1 | `python3 -B .ufo/waves/round-56/c56_selftally.py --selftest` | `c56 selftally selftest: 47/47` | 0 |
| R2 | same, second run | `c56 selftally selftest: 47/47` | 0 |
| R3 | same, at lane tip `7ad7db51dfcf` (no diff of counter or `SKILL.md` between `a450e43` and tip) | `47/47` | 0 |
| R4 | `KAKE_R56_SELFTEST_REV=3691e9689a0358fc671d948d39dae3546ba5c01d python3 -B .ufo/waves/round-56/c56_quote_truth.py --selftest` (the C2 row's documented command) | `c56 quote-truth selftest: 67/67 (fixture revision 3691e9689a03)` | 0 |
| R5 | same C2 command with the pin omitted (default = HEAD `a450e43`) | `67/67 (fixture revision a450e43e696d)` | 0 |
| R6 | `measure()` of the committed counter with an extended population of the two new rows (probe, not a lane run) | both rows `tool_changed`, observed `47/47` and `67/67`, exit 1 | 1 |

Per-run wall time ~3 s, against `TIMEOUT = 300` (`c56_selftally.py:58`); no timeout risk on this host.

## COUNT DERIVATION:

Independent count by AST over `selftest()` (`c56_selftally.py:350-461`), not by trusting the printed denominator:

- `add(...)` case calls (`c56_selftally.py:367` closure; registered at `cases` line 365): **32**, all 32 names distinct, no duplicate.
- `unit` dict entries (`c56_selftally.py:432-446`): **15** keys, all distinct (a duplicate key would silently collapse the denominator; none).
- `total = len(cases) + len(unit)` (`c56_selftally.py:460`) = 32 + 15 = **47**, equal to the printed denominator in R1/R2/R3.

So the registry row's integer 47 is arithmetically true: 32 sandbox-repo cases + 15 unit checks, every one load-bearing
(see MUTATION SWEEP).

For the C2 row I ran the same derivation: `cases` is seeded with `"pass"` (`c56_quote_truth.py:651`) plus **63** distinct
`@case(...)` decorators = **64** fixtures, and `unit_checks` (`c56_quote_truth.py:910-912`) = **3** entries; `total`
(`c56_quote_truth.py:934`) = 67, equal to R4/R5. The cell's decomposition "64 … plus 3 unit-rule checks" is literally true.

## NEW ROW CHECKS:

Hand-applied the committed C1 counter's documented-command rule (`documented_command` `c56_selftally.py:147-162`,
`command_problem` `:164-171`, claim extraction `:274-281`) to the two rows of
`SKILL.md:1243` "Round 56 gate registry additions", by importing the counter module and feeding it the
`SKILL.md` blob at `a450e43` (so the rule applied is the shipped code, not my reading of it).

| fact | `selftest-tally-counter` (`SKILL.md:1253`) | `yahoo-crawl-handling-quote-truth-counter` (`SKILL.md:1254`) |
|---|---|---|
| row occurrences in `SKILL.md` | 1 (no `duplicate_row`) | 1 |
| `Self-test` column index | 4 of 8 cells | 4 of 8 |
| backticked command found there | `python3 -B .ufo/waves/round-56/c56_selftally.py --selftest` | `KAKE_R56_SELFTEST_REV=3691e9689a03… python3 -B .ufo/waves/round-56/c56_quote_truth.py --selftest` |
| `command_problem` | `None` (valid) | `None` (valid); pin accepted by `PIN_RX` (`c56_selftally.py:59`) |
| claim extracted | `['47']` → 47, exactly one | `['67']` → 67, exactly one under the population's anchored regexes |
| observed tally | `47/47` (R1/R2/R3), exit 0 | `67/67` (R4), exit 0 |
| claimed number true? | **yes** | **yes** |

Both Self-test cells state a number their documented command prints. Caveats that the L1 should carry:

- **Wording (C1 row).** `(47 checks, generated sandbox repos)` attributes all 47 to sandbox repos; only 32 are sandbox cases,
  15 are unit checks that build no repo. The C2 row splits its number explicitly ("64 … plus 3 unit-rule checks"), so the
  registry convention exists and the C1 cell under-describes its own selftest. The counter cannot see this: its claim regex
  captures only the integer, so the qualifier is outside C1's calibration.
- **Claim-regex sensitivity (C2 row).** The cell contains three numerals (67, 64, 3). With the population's anchored style
  `\((\d+) (?:sandbox-repo )?(?:fixtures|checks)` the cell yields one claim (`67`); with the same regex *without* the `\(`
  anchor it yields two (`67`, `64`) → `claim_ambiguous`. If these rows are ever added to `POP`, the anchor is mandatory.
- **Neither new row is in `POP`** (`c56_selftally.py:62-76`, ten names, none of them these). So the C1 predicate
  `rows_checked == 10` does not cover the registry's own two newest rows, and their Self-test claims are uncalibrated
  except by this hand-check. Adding them is structurally blocked today: R6 shows `helpers_changed` (`:216-224`) returns the
  round-56 script itself as changed for both rows, because `.ufo/waves/round-56/` does not exist at `BASE_REV`
  `e48354b7c26b` (verified with `git cat-file -e e48354b7c26b:.ufo/waves/round-56` → absent). Both rows would be
  `tool_changed` mismatches under the current base pin, regardless of a true tally.
- **C2 pin currency.** The pinned revision's evidence is byte-identical to `a450e43`
  (`git diff --stat 3691e96 a450e43 -- .ufo/waves/round-56/sources .ufo/waves/round-56/controls corpus/SOURCES.md
  corpus/lessons/round-56.md corpus/knowledge/yahoo-japan-*` → empty), and the unpinned run (R5) also prints 67/67, so the
  pin is a fixed point, not a stale fixture set.

## MUTATION SWEEP:

Fourteen single-string mutants of `c56_selftally.py`, each written to a `mktemp -d` copy and run with `--selftest`
(lane bytes never touched): **12 killed, 2 survived**.

Killed (tally dropped, exit 1): accept-any-command `43/47`; drop `duplicate_row` `45/47`; drop `claim_ne_observed`
`45/47`; drop `helpers_changed` `45/47`; drop the `nclaims` ambiguity branch `45/47`; first-tally-wins `46/47`;
helper scan off (`names = []`) `46/47`; env pin not applied `40/47`; `_is_selftest_words` always true `45/47`;
drop `claim_missing` `45/47`; drop `selftest_failed` `45/47`; helper scan short-circuited `45/47`.

Survivors (47/47, exit 0):

1. **S1 — predicate term `checked`.** Replacing `checked = sum(1 for r in results if r["checked"])` in `measure`
   (`c56_selftally.py:296`) with `checked = len(results)` leaves 47/47. Analysis: `met` requires `mism == 0`, and every row
   appended with `checked: False` (`row_missing`, `command_missing`, `command_invalid`) also carries a problem, so the two
   computations agree whenever the exit code is 0; `render` (`:303`) recomputes its own `checked` for the printed line.
   Demonstrated on a 9-of-10-row sandbox repo: real and mutant print the same `tally_mismatches=10 rows_checked=8`, exit 1.
   **Equivalent mutant, no predicate impact** — but the case named `rows_checked_counts_found_rows_only`
   (`:404`, extra assertion `:423`) asserts the per-row flags, not `measure`'s term, so the name overstates coverage.
2. **S2 — pin *name* allowlist.** Loosening `PIN_RX` (`:59`) to `[A-Z0-9_]+=[0-9a-f]{7,40}` leaves 47/47, because the
   `pin_not_in_allowlist` case (`:396`) uses `OTHER=1`, whose value fails the hex-length rule, not the name rule: measured,
   real and mutant both reject `OTHER=1`, and only the mutant accepts `OTHER=deadbeef`
   (`command_problem(["OTHER=deadbeef",…])` → `None` under the mutant, a rejection under the real counter). The shipped
   counter is **not** bypassed — I confirmed it rejects `PYTHONPATH=deadbeef` as a pin word and that a
   `deadbeef/sitecustomize.py` payload therefore never executes — but the selftest would not notice a regression that
   accepted any `NAME=<7-40 hex>` pin, and such a pin is injected into the child environment by `run_command`
   (`:200-214`). This is the concrete gap behind the contract's looser disclosure ("a helper outside the pinned script's
   directory is not pinned").

## FINDINGS FOR THE L1:

- **F1 (attacks `SKILL.md:1253` Self-test cell).** Claim "47 checks" is true (R1-R3) and its decomposition is 32 sandbox
  cases + 15 unit checks (`c56_selftally.py:365-460`). The qualifier "generated sandbox repos" is imprecise for 15 of the 47;
  a wording fix would align it with the C2 row's "64 … plus 3 unit-rule checks". No number changes.
- **F2 (attacks `SKILL.md:1254` Self-test cell).** Claim "67 checks: 64 … plus 3" is true (R4: 67/67, exit 0; AST: 63 `@case`
  + `"pass"` = 64, `unit_checks` = 3).
- **F3 (attacks the C1 population, `c56_selftally.py:62-76`).** The registry's two round-56 rows are outside `POP`; the
  frozen predicate's `rows_checked == 10` therefore says nothing about them, and R6 shows they cannot be added while the tool
  pin stays anchored at `BASE_REV` (`.ufo/waves/round-56/` absent at `e48354b7c26b`). If coverage is wanted, the population
  needs a per-row base pin or a self-exclusion rule; that is a contract change, not a code fix.
- **F4 (attacks `pin_not_in_allowlist`, `c56_selftally.py:396`).** S2: the case tests the value shape, not the name
  allowlist. A one-line fixture (`OTHER=deadbeef`) would close it and raise the selftest to 48 checks — which would then
  require updating the `SKILL.md:1253` claim, so it must be a coordinated change, not a silent one.
- **F5 (attacks `rows_checked_counts_found_rows_only`, `c56_selftally.py:404/423`).** S1: the case name claims coverage of
  `measure`'s `rows_checked` term but asserts only the per-row `checked` flags. Harmless today (equivalent mutant), worth a
  comment or a renamed case rather than a new fixture.
- **F6 (attacks C2 fixture pin).** Pin `3691e9689a03` is content-identical to `a450e43` on every evidence key the selftest
  reads, and the unpinned run also gives 67/67 (R4/R5); the pin is honest and currently redundant.

## VERDICT: Both new registry rows' Self-test claims are true (C1 47/47 twice at `a450e43`, C2 67/67 pinned, both exit 0) and both commands are valid under the counter's documented-command rule; the 47 is 32 sandbox + 15 unit checks, 12 of 14 mutants killed, and the surviving pin-name mutant plus the two rows' absence from `POP` are reported as calibration gaps for the L1.
