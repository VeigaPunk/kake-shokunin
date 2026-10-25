# CriticJunkC1v2

Second falsify attack on claim C1 (calibration) **after** the version-2 fixes. Target: `c56_selftally.py` at the revision
under attack `a450e43e696d032e3ac308383f6b3394e0c92860` (blob identical to the current lane tip: `git diff --stat a450e43
HEAD -- .ufo/waves/round-56/c56_selftally.py SKILL.md` is empty), plus the v2 version list in `contract.md` §Counter versions.

Method: one commit per experiment, each on its own branch from `a450e43` in a `mktemp -d` clone of the lane (every edit and
commit stays in that throwaway clone; the change is quoted in full below so the L1 can reproduce it), then
`python3 -B .ufo/waves/round-56/c56_selftally.py --root <clone> --revision <experiment commit>`. No lane file, index or jj
state was touched.

Baseline at `a450e43`: `met=True tally_mismatches=0 rows_checked=10`, exit 0, 26 s wall — so every `met` below is a
regression from a green state, not a pre-existing red.

## EXPERIMENTS:

| # | change committed in the clone | attacks | exit | met | problem code(s) |
|---|---|---|---|---|---|
| E1 | decoy table `\| Name \| Self-test \|` + row `readme-index-counter … (99 fixtures)` inserted **before** the real table (`SKILL.md:1231`) | duplicate row names, `measure` reading `occ[0]` (`c56_selftally.py:246`) | 1 | no | `duplicate_row,claim_ne_observed` (claim read from the decoy = 99, observed 44/44) |
| E2a | honest span first, second span `python3 -B …/c55_readme_index.py --selftest --bogus` appended to the same Self-test cell | first-span-wins loop (`:157`) | 0 | **yes** | — |
| E2b | inert span first `python3 -c "print('ok')"`, honest span second | `_is_selftest_words` skip + first-span-wins (`:143-161`) | 0 | **yes** | — |
| E2c | fake span **naming the script** first (`… --selftest --bogus`), honest span second | `:157` + `command_problem` | 1 | no | `command_invalid` |
| E3 | new file `scripts/zz_extra_helper.py` beside the pinned scripts (absent at `BASE_REV`) | base-revision-closed pin set (`:219-220`) | 0 | **yes** (inert) | — |
| E4 | `KAKE_R52_SELFTEST_REV=e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6` prefixed to the `redirect-expectation-audit` command, a row that documents no pin | pin accepted by regex only (`:59`, `:167`, `:208`) | 0 | **yes** | — |
| E5 | `yahoo-robots-quote-truth-counter` pin `64c0ce12…` swapped to the base revision `e48354b7…` | pin value never compared to the row's claim (`:167`) | 0 | **yes** | — |
| E6a | `` `… --selftest ; true` `` inside the backticks | shlex keeps `;` as a token | 1 | no | `command_invalid` |
| E6b | `` `… --selftest \| cat` `` inside the backticks | markdown cell splitter (`table_rows`, `:106-131`) | 1 | no | `command_missing` (cell split into 9 vs 8 columns; span truncated) |
| E7 | readme table header `Self-test` renamed `Selftest` | header lookup `h.startswith("self-test")` (`:153`) | 1 | no | `command_missing` on **both** rows of that table (`rows_checked=8`) |
| E8 | fixture-only: `scripts/fixtures/base-path/D1-root-relative-stylesheet/` rewritten to a vacuous clean case (45 dirs kept) | `helpers_changed` pins only `*.py`, non-recursively (`:219-220`) | 0 | **yes** | — |

E8 verification outside the counter: in the clone at the E8 commit, `python3 -B scripts/base_path_selftest.py --case D1`
prints `6/6 fixtures passed`; the directory still named `D1-root-relative-stylesheet` now asserts `exit 0, findings []`.

## CHEATS THAT PASSED:

1. **E2a / E2b — a Self-test cell may document a second, unvalidated command.** `documented_command` (`:157`) returns the
   first span whose words name the pinned script and look like a selftest and never inspects the rest of the cell. So
   `… --selftest --bogus` (E2a) or `python3 -c "print('ok')"` (E2b) can sit in the cell indefinitely; both trees print
   `met=True`, all ten rows `OK`. The v2 text ("exactly one claim per cell") constrains *claims*, not *commands* — the row
   can advertise two commands and the registry then says something the counter never checked.
   Fix: R1.
2. **E4 — a pin on a row that documents none is accepted, and its value is never resolved.** `command_problem` (`:167`)
   skips any leading word matching `KAKE_R5[0-9]_SELFTEST_REV=[0-9a-f]{7,40}` and `run_command` (`:208`) exports it. Adding
   the base revision to `redirect-expectation-audit` (which names no pin, and whose selftest ignores the variable) still
   prints `met=True`. The v2 claim "the documented command must be exactly `[KAKE_R5N_SELFTEST_REV=<hex>] …`" is true
   syntactically but the hex is arbitrary: it need not resolve, need not be the measured revision, and need not be the
   value the round used. Fix: R2.
3. **E5 — the pinned revision can name a different tree state.** Swapping the r55 row's pin from
   `64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` to `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6` still prints `met=True`; the
   selftest run directly with that pin prints `c55 quote-truth selftest: 54/54 (fixture revision e48354b7c26b)`. The row's
   own words ("built from the committed round-55 evidence at the pinned revision") then describe a different tree than the
   round measured, and the counter cannot tell. This is the sharpest hole: the pin is part of what the row *claims*, and
   it is the one part v2 left unchecked. Fix: R2.
4. **E8 — fixture-only hollowing.** `helpers_changed` (`:219`) lists `*.py` only, non-recursively, at `BASE_REV`; the
   fixture trees the four `scripts/*_selftest.py` rows read (`scripts/fixtures/base-path/`, and the analogous trees for
   sitemap/robots/source-recheck) are not pinned at all. Replacing a defect fixture with a trivially-clean case keeps the
   count at 45, so `base-path-audit: claim=45 observed=45/45 OK` and the predicate is met while the fixture named for
   root-relative stylesheet resolution no longer tests it. The contract discloses "not that a gate's selftest is good", but
   v2's "every `*.py` beside the pinned script must be byte-identical" reads as a tool pin that the data files escape.
   Fix: R3.
5. **E3 — inert but shows the pin set is closed over base-revision names.** A new `*.py` beside the pinned scripts is
   invisible to `helpers_changed` (it only re-checks names present at `BASE_REV`), so any future helper added there is
   unpinned by construction. The assigned instance — a helper *imported* from outside the directory — does not exist today
   (see NOT RUN), so this commit reaches `met` without changing behaviour. Fix: R3 (same fix).

## RECOMMENDED CHANGES:

- **R1 (closes E2a/E2b).** In `documented_command` (`c56_selftally.py:157`), collect every span in the Self-test cell whose
  words name the script and are selftest-shaped; if more than one and they are not byte-identical, return a new
  `command_ambiguous` problem. Add two selftest cases (honest-first/fake-second, fake-first/honest-second) so the v2
  selftest count moves 47 → 49.
- **R2 (closes E4/E5).** Give every `POP` entry an `expected_pin`: `None` for the eight rows that document no pin, the
  exact documented string for `quote-truth-counter` (`KAKE_R52_SELFTEST_REV=1ae8de5d4dee`) and
  `yahoo-robots-quote-truth-counter` (`KAKE_R55_SELFTEST_REV=64c0ce12…`). Require `words[:i] == [expected_pin]` (or `i == 0`
  when `None`), and additionally `git rev-parse --verify <value>^{commit}` must succeed in `root`. Record the two allowed
  values in `contract.json` (`claims.C1.pins`) so the contract, not the row, is the authority.
- **R3 (closes E8/E3).** Replace `git ls-tree --name-only <base> <dir>/` with `git ls-tree -r --name-only <base> <dir>/`
  over **all** files, or pin the tree hash (`git rev-parse <rev>:<dir>`) of each row's fixture root against a value recorded
  in `contract.json`. The first is one flag; the second is stronger and cheap for `scripts/fixtures/base-path/`.
- **R4 (diagnosis, keeps E6a/E6b/E7 red).** `table_rows` (`:106-131`) splits on every unescaped `|`, including inside backticks, so
  E6b's cell silently becomes 9 columns and every later column of the row shifts; the row is caught but reported as
  `command_missing`. Split only outside code spans, emit `row_shape` when the cell count differs from the header, and emit
  a distinct `header_missing` when no header cell starts with `self-test` (E7 currently reports `command_missing` for a
  renamed header, which misnames the defect).
- **R5 (minor).** `table_rows` does not track fenced code blocks, so an illustrative table inside a fence that repeats a
  registry name is a false `duplicate_row`; and `measure:246` still runs the command for a row already flagged
  `duplicate_row` (E1 spent a full selftest run on a row it had already rejected).

## NOT RUN / RESIDUAL:

- **E3's assigned instance does not exist.** `grep -n '^from\|^import' scripts/*.py .ufo/waves/round-5*/c5*.py` over the ten
  pinned scripts shows stdlib-only imports (`argparse json os re shlex subprocess sys tempfile shutil hashlib posixpath
  datetime`); the tools are invoked by `subprocess` from the same directory. The disclosed "helper outside the pinned
  script's directory" limit is real but unreachable for these ten rows as written.
- **r52 pin swap not achievable among resolving revisions.** Only the documented `1ae8de5d4dee` prints 18/18; `e48354b7`,
  `2d308e80`, `6b3df99`, `a450e43`, `3691e96`, `d5afc48` all fail `C8_mirror_bytes`. E5 was therefore demonstrated on the
  r55 row, where `e48354b7` prints 54/54 and `d5afc48`/`3691e96`/`a450e43` fail.
- **Not run:** a revision whose round-55 evidence is hollowed so that the r55 selftest prints 54/54 trivially. It would
  require rewriting the whole retained-evidence set consistently; R2+R3 are the guards if someone tries.
- **Residual, unrun:** the counter fixes the environment except `PATH`/`HOME`/`LANG` and does not pass `-I`/`-S`
  (`:200-205`), so a `sitecustomize.py` in the inherited `HOME`'s user site — or a `python3` earlier on the inherited
  `PATH` — executes inside every selftest and can print any tally. Outside the tree-only threat model, but it means the
  "observed state" is only as clean as the caller's environment.

VERDICT: C1 v2 holds against table duplication, fake-first commands that name the script, `;`/`|` suffixes and header renames, but 5 behaviour-bearing one-commit trees reach `met` — two-command cells (E2a/E2b), an unvalidated pin on a no-pin row (E4), a pin naming a different tree state (E5) and a hollowed unpinned fixture (E8); R1-R3 close them.
