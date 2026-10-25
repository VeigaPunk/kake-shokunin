# ExecTallyQuoteR55

Claim C1 (calibration), seat ExecTallyQuoteR55. Row: `SKILL.md` gate-registry line 1234 at base
`e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`, name `yahoo-robots-quote-truth-counter`, pinned script
`.ufo/waves/round-55/c55_quote_truth.py` (blob `1c4688c75028adf09112d7e82fc7856c2982786a`, identical at
`e48354b7` and at lane HEAD `6b3df99`). Every run below is in a scratch clone under `/tmp`; the lane was
read-only for this seat (no lane write, no git/jj mutation, no `pacman`). No tool installs were needed;
`/usr/bin/time` is absent on the host, so wall times come from `date +%s%N` around the command.

## RUNS:

- Clone A: `D=$(mktemp -d)` -> `/tmp/tmp.aulDqDGgXf`;
  `git clone -q --no-checkout /home/vgpnk/Projects/shokunin/kake-shokunin "$D"`,
  `git -C "$D" checkout -q e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`.
  `git -C "$D" rev-parse --show-toplevel` = `/tmp/tmp.aulDqDGgXf`; `rev-parse HEAD` =
  `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`.
- Command, exactly as the row documents it (no env pin added; the script documents `KAKE_R55_SELFTEST_REV`
  only as an *alternative revision* pin, not a requirement):
  `cd $D && python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest`.
- Run 1: exit **0**, wall **5.895 s**, stderr 0 bytes. stdout is exactly **one** line, so "last 3 lines"
  is that line:
  `c55 quote-truth selftest: 54/54 (fixture revision e48354b7c26b)`
- Run 2: exit **0**, wall **6.844 s**, stderr 0 bytes, stdout byte-identical to run 1 (`diff` clean):
  `c55 quote-truth selftest: 54/54 (fixture revision e48354b7c26b)`
- Post-run `git -C "$D" status --porcelain` empty after both runs: `-B` plus `tempfile.mkdtemp` sandboxes
  (removed in `finally`) leave no file in the clone.
- Pin sanity (documented `KAKE_R55_SELFTEST_REV` path): `KAKE_R55_SELFTEST_REV=6b3df99d694f59d44504604da1a55a9fe1e9be75`
  -> exit 0, wall 4.741 s, `c55 quote-truth selftest: 54/54 (fixture revision 6b3df99d694f)`.
- Observed tally at the base revision: **54/54, exit 0** (`A == B`), stable across runs and across the
  round-56 spec commit (same 156-row registry).

## WHAT N COUNTS:

- The script prints `passed/total` with `total = len(cases) + len(unit_checks)` (line ~847). N = **54**
  decomposes as **51 sandbox-repo fixtures + 3 unit-rule checks**.
- `cases` = 51: 50 `@case(...)` decorators plus the initial `cases = {"pass": ...}` entry. Each case is one
  3-commit `mktemp -d` git repo built by `_build()` from the committed round-55 evidence with one mutation
  applied, then scored by `run_checks` on exit code. A case counts **once**, however many of C1–C8 it trips.
  By expected exit: 47 expect 1, 1 expects 2 (`fail_bad_receipts`), 3 expect 0 (`pass`,
  `pass_gate_extra_short_quote`, `pass_census_relative_argv`).
- `unit_checks` = 3: halfwidth kana one per character; non-BMP CJK counted; latin tokens per word.
- So N counts **cases (fixture repos) + unit checks**; it is not a mutants count and not an assertion count.
- The row's Self-test cell states `(47 sandbox-repo fixtures ... plus 3 unit-rule checks)`. The counter's
  claim regex `\((\d+) (?:sandbox-repo )?(?:fixtures|checks)` captures **47** (implied total 47+3 = 50).
  47 != 54: the claim is off by 4, and 47 happens to equal the count of *exit-1-expecting cases*, not the
  fixture count. The receipt the cell itself cites, `.ufo/waves/round-55/controls/c2-selftest.txt`, already
  reads `c55 quote-truth selftest: 54/54 (fixture revision 64c0ce12ffe3)` — the cell contradicts its own
  receipt. (Corroboration only: `.ufo/waves/round-56/controls/base-c1-selftally.txt` records
  `claim=47 observed=54/54 MISMATCH claim_ne_observed` for this row; my 54 is derived from my own two runs.)

## HEAD DEPENDENCE:

Every byte the selftest reads comes from `git show <rev>:<path>` (rev = `HEAD`, or `KAKE_R55_SELFTEST_REV`
when set); `os.getcwd()` is used only for `git rev-parse HEAD`. There is **no working-tree read** — the only
`open()` in the file is a *write* into the `mktemp -d` sandbox — so a dirty tree cannot change the tally, but
a later *commit* can. The only environment variable consulted is `KAKE_R55_SELFTEST_REV` (lines 594, 597).

Files read at the measured revision (from `keys` in `selftest()` plus `run_checks`):

1. `corpus/SOURCES.md`
2. `corpus/lessons/round-55.md`
3. `.ufo/waves/round-55/sources/receipts.json`
4. `.ufo/waves/round-55/assimilation/pre-append/corpus/SOURCES.md` (MIRROR)
5. `.ufo/waves/round-55/assimilation/mirror-pin.json`
6. `.ufo/waves/round-55/assimilation/validate/corpus/SOURCES.md`
7. `.ufo/waves/round-55/assimilation/validate/census-argv.txt`
8. `.ufo/waves/round-55/assimilation/validate/census-stdout.txt`
9. `.ufo/waves/round-55/assimilation/validate/census-exit.txt`
10. `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md`
11. `corpus/knowledge/yahoo-japan-robots-pattern-syntax.md`
12. `corpus/knowledge/yahoo-japan-robots-txt-basics.md`
13. `.ufo/waves/round-55/assimilation/validate/corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md`
14. `.ufo/waves/round-55/assimilation/validate/corpus/knowledge/yahoo-japan-robots-pattern-syntax.md`
15. `.ufo/waves/round-55/assimilation/validate/corpus/knowledge/yahoo-japan-robots-txt-basics.md`
16. `.ufo/waves/round-55/sources/S372.html`
17. `.ufo/waves/round-55/sources/S373.html`
18. `.ufo/waves/round-55/sources/S418.html`

Plus two history reads that are not at the measured revision: `corpus/SOURCES.md` at the script's own
constant `BASE_REV = fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d` (the round-55 base, *not* the round-56 base),
and the MIRROR blob at its add-commit (`git log --diff-filter=A ... <rev> -- <MIRROR>`).

Never read: `corpus/README.md`, `SKILL.md`, any `corpus/knowledge/` file outside the three adopted entries,
anything under `.ufo/waves/round-56/`.

Extra-commit rerun, proven in scratch clones (each a fresh clone of the lane at `e48354b7`, commit made with
`-c user.name=selftest -c user.email=selftest@local`, selftest re-run from the clone root):

- **Commit A** `/tmp/tmp.PT6b2CjICP` @ `d2b895f9c9c6` — benign paths: a line in `corpus/README.md`, a new
  `corpus/knowledge/zz-probe-extra-knowledge.md`, an extra `SKILL.md` gate-registry row
  (`| probe-counter | ... (9 fixtures) |`, a name outside `POP`), and `.ufo/waves/round-56/zz-probe-note.md`.
  Result: **54/54, exit 0**, wall 6.043 s — tally unchanged.
- **Commit B** (on top of A) @ `421f5b52043e` — appended two well-formed registry rows S419/S420 to
  `corpus/SOURCES.md` (156 -> 158 rows). Result: **51/54, exit 1**, wall 4.524 s. Failing cases: `pass`,
  `pass_census_relative_argv`, `pass_gate_extra_short_quote`, each with
  `C7_validate_before_append: validated scratch registry is not byte-equal to the landed registry`,
  `C8_mirror_bytes: registry rows 158 != mirror rows 155 + 1`, and
  `C8_mirror_bytes: append-only: measured registry minus new rows, used-by restored, != mirror bytes`.
- **Commit C** `/tmp/tmp.8JDV9WvYJU` @ `f1751d8ce56d` — one harmless prose line appended to the *adopted*
  entry `corpus/knowledge/yahoo-japan-robots-txt-basics.md`. Result: **51/54, exit 1**, wall 4.251 s:
  `C7_validate_before_append: S418: validated scratch entry differs from the landed entry` on the same three
  pass cases.

So the row's number is a function of HEAD, not of the frozen round-55 state: new files under
`corpus/knowledge/`, `corpus/README.md`, `SKILL.md` prose/rows and `.ufo/waves/round-56/` are inert; an
**edit** to one of the three adopted entries is fatal (C7 byte-equality); **any append to
`corpus/SOURCES.md` is fatal**, because C8 requires `len(registry rows) == len(MIRROR rows) + 1` and requires
the MIRROR bytes to equal the fixed `fcaf4b85` registry (155 rows). Only the c55 script blob is pinned by the
counter (`tool_changed` otherwise), so the evidence files are free to drift under it.

## REPLACEMENT CELL:

Self-test cell (5th cell) of row `yahoo-robots-quote-truth-counter`, keeping the documented command first and
every other clause of the cell as written, with the count corrected and the decomposition made explicit:

```
`python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` (54 checks: 51 sandbox-repo fixtures built from the committed round-55 evidence at `HEAD` or `KAKE_R55_SELFTEST_REV`, plus 3 unit-rule checks; receipt `.ufo/waves/round-55/controls/c2-selftest.txt`)
```

Checked against the counter (imported `c56_selftally.py` read-only and ran its own functions on this cell):
`documented_command` -> `['python3','-B','.ufo/waves/round-55/c55_quote_truth.py','--selftest']`;
`selftest_cell` resolves to this cell; the POP regex for the row yields exactly one capture, **54**
(claim = 54); `parse_tally` on the observed line -> `(54, 54)`. No other `(N fixtures|checks)` match exists in
the cell, so the sum cannot double-count.

This 54 is the tally at a **156-row** registry (`e48354b7`, and lane HEAD `6b3df99`). It is not what the same
command prints at a 158-row registry (51/54) — see RISKS 1–2.

## RISKS:

1. **Contract conflict, C1 vs C2 (blocker for this row).** C2's After state is "registry 158 rows"; commit B
   proves that at 158 rows this row's documented selftest prints 51/54 and exits 1. `measure()` appends
   `selftest_failed` when `code != 0 or tally[0] != tally[1]`, so **no integer in the cell can make the row
   green** at 158 rows, and `tally_mismatches == 0` is unreachable. Patching the script is not an escape:
   `measure()` also appends `tool_changed` unless the script blob equals its base blob. Updating the
   round-55 MIRROR/pin is not an escape either: C8's first check requires the MIRROR bytes to equal the
   fixed `fcaf4b85` registry. The only states that keep this row green are registries of exactly 156 rows.
   Resolution is the L1's call (relax `measure`'s exit-0 requirement for this row, exclude it, or land the
   two rows elsewhere); I did not act on it.
2. If the build lands 158 rows and the cell says `(54 ...)`, the counter reports
   `selftest_failed,claim_ne_observed` for this row; if it says `(51 ...)`, it reports
   `selftest_failed` alone. Both keep C1 at `tally_mismatches >= 1`.
3. The cell's cited receipt already reads 54/54, so the base `47` was never sourced from it; cell-vs-receipt
   contradiction exists at base and survives any integer-only fix.
4. Tally is HEAD-dependent (probes B, C). Any later wave that appends to `corpus/SOURCES.md` or edits one of
   the three adopted entries silently changes this row's number; the round-56 registry append is exactly
   such a wave.
5. Wall time: 51 sandbox repos cost 4.3–6.8 s here on a loaded host, far inside the counter's `TIMEOUT=300`;
   `measure()` additionally clones the whole lane once per invocation (~5 s warm), which is the dominant cost
   of the counter, not of this selftest.
6. Unrun: the full `c56_selftally.py --root ... --revision ...` sweep (10 rows) — out of this seat's scope
   (single row) and already receipted at base; nothing else reported here is inferred.

VERDICT: Row `yahoo-robots-quote-truth-counter` observes 54/54 (exit 0, two identical runs at `e48354b7`) but claims 47 -> replace the cell with `(54 checks: 51 sandbox-repo fixtures ... plus 3 unit-rule checks)`; the same command cannot pass at the 158-row registry C2 requires (51/54, exit 1), so C1 for this row is unsatisfiable as frozen.
