# ExecRegress

Regression sweep of previously committed counters/gates at the round-57 build. Tip read:
`4b8c73050470ada9e6583f3b12d659d1bed6a17f` (clone `D=/tmp/execregress.m5WKq3`, `git -C $D rev-parse HEAD` = that
revision, `--show-toplevel` = `$D`). Base: `28fa0b23e699303725aba2727094531f5e44494d` (clone
`B=/tmp/execregress-base.9NuZfr`, same checks). All eight scripts are **byte-identical** between base and tip
(`git diff --stat 28fa0b2 4b8c730 -- <the 8 paths>` is empty, exit 0), so any result difference is data-driven.
Every row below is *confirmed by running* the named command in that clone; no base re-run was skipped.

## TABLE:

| # | command (run with `cwd=$D`, `--root $D`) | base `28fa0b2` | tip `4b8c730` | changed |
|---|---|---|---|---|
| 1 | `python3 -B .ufo/waves/round-55/c55_readme_index.py` | `C1 readme-index index_mismatches=0 knowledge_files=52 met=True` · `unindexed=0 multi=0 thin=0 duplicate=0 head_changed=0 deleted=0 dangling=0 coverage_rows=54` · EXIT=0 | `C1 readme-index index_mismatches=0 knowledge_files=54 met=True` · same zero line, `coverage_rows=56` · EXIT=0 | verdict no; counts +2 files/+2 coverage rows |
| 2 | `python3 -B .ufo/waves/round-56/c56_selftally.py` (37 s measured, under the 600 s cap) | `C1 selftest-tally tally_mismatches=0 rows_checked=10 met=True`, all 10 rows `OK` (`source-recheck-audit 106/106`, `robots 204/204`, …) · EXIT=0 | identical text, `revision: 4b8c730…` · EXIT=0 | no |
| 3 | `python3 -B .ufo/waves/round-56/c56_quote_truth.py` | `C2 quote-truth 8/8 met=True`, C1–C8 all PASS · EXIT=0 | `C2 quote-truth 6/8 met=False`, **C7_validate_before_append FAIL** (`validated scratch registry is not byte-equal to the landed registry`), **C8_mirror_bytes FAIL** (`registry rows 160 != mirror rows 156 + 2`; `append-only: measured registry minus new rows, used-by restored, != mirror bytes`); C1–C6 PASS · EXIT=1 | **YES** |
| 4 | `python3 -B scripts/citation_lint.py` | `{"adjudicated":31,…,"violations":0,"verdict":"clean"}` · EXIT=0 | same summary (`adjudicated` 31, `violations` 0, `verdict":"clean"`) · EXIT=0 | no |
| 5 | `node scripts/freshness-sweep.mjs --selftest` (node v24.21.0) | `selftest: 36/36 passed` · EXIT=0 | `selftest: 36/36 passed` · EXIT=0 | no |
| 6 | `python3 -B scripts/landed_check.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-56/kake.md --repo /home/vgpnk/Projects/shokunin/kake-shokunin --branch master` | `cited=11 landed=11 missing=0 unknown=0`, `suppressed 1 digest-labelled non-commit token(s)` · EXIT=0 | identical summary · EXIT=0 | no |
| 7 | `python3 -B scripts/source_recheck.py --selftest` | `usage: source_recheck.py --manifest PATH` · EXIT=64 | same · EXIT=64 | no (both are the usage path) |
| 7b | documented selftest instead (`SKILL.md:1067`): `python3 -B scripts/source_recheck_selftest.py` | `106/106 passed, verdict clean` · EXIT=0 | `106/106 passed, verdict clean` · EXIT=0 | no |
| 8 | `python3 -B scripts/robots_audit_selftest.py` (`SKILL.md:1093`, no args) | `204/204 passed, failed 0, verdict clean` · EXIT=0 | `204/204 passed, failed 0, verdict clean` · EXIT=0 | no |

Command 7 as assigned is not a valid invocation of the tool at either revision: `scripts/source_recheck.py` takes
only `--manifest PATH` (argparse usage → exit 64). The documented fixture selftest is
`scripts/source_recheck_selftest.py`, run as row 7b — the assignment's "or its documented selftest command" clause
was applied here.

## CHANGED:

**Only `c56_quote_truth` changes result: 8/8 met=True/EXIT=0 at base → 6/8 met=False/EXIT=1 at the tip.**

Cause (confirmed by running, not inferred): the round-56 counter freezes the registry at its own round. Its
`MIRROR` is `.ufo/waves/round-56/assimilation/pre-append/corpus/SOURCES.md` (156 rows, pin
`.ufo/waves/round-56/assimilation/mirror-pin.json`, `sourceRevision e48354b7…`) and `NEW_ROWS = ("S419","S420")`, so
C8 requires `len(rows) == 156 + 2 == 158` (`c56_quote_truth.py:535`) and C7 requires the landed registry to be
byte-equal to the round-56 validated scratch registry (`c56_quote_truth.py:499`). The round-57 build appended the two
Baidu rows, so `corpus/SOURCES.md` at the tip has 160 rows: `grep -c '^| S[0-9]'` on
`git show 4b8c730:corpus/SOURCES.md` = 160 vs base 158. Both failures are that growth and nothing else — the third
message (`c56_quote_truth.py:549`) fires because the append-only reconstruction only drops `S419`/`S420` and leaves
the two round-57 rows in the compared text.

No round-56 content regressed: C1–C6 PASS at the tip, including `C6_receipt_pins` for S419/S420 and `C5_quote_truth`.
The append itself is pure addition: `diff <(git show 28fa0b2:corpus/SOURCES.md) <(git show 4b8c730:corpus/SOURCES.md)`
is one hunk, 2 added lines, 0 removed lines (only the S421 and S422 rows, inserted at line 167). The round-57 own pin
is intact: `.ufo/waves/round-57/assimilation/pre-append/corpus/SOURCES.md` sha256
`010af7926a03788fa5f36371a0f9452ee3f3ee3c087977a455dc400bb3b5be81`, 158 rows, `sourceRevision 28fa0b2…`, equal to
`round-57/assimilation/mirror-pin.json` (verified by hashing the blob). So the historical counter is append-frozen, not
broken by a bad edit — and the base control stands: at base the same script is 8/8, and the committed round-56 receipt
`.ufo/waves/round-56/controls/after-c2-quote-truth.txt` pins `revision: 4cb225fb…` with `8/8 met=True`, `EXIT=0`.

What the L1 must do:
1. Do **not** read the tip `6/8` as a round-57 defect and do **not** re-run `c56_quote_truth` at the round-57 tip as
   evidence about round-56 claims. Round-56 quote-truth is a statement about `4cb225fb`
   (`.ufo/waves/round-56/controls/after-c2-quote-truth.txt`), where it is 8/8; round-57 freshness is owned by
   `.ufo/waves/round-57/c57_quote_truth.py`.
2. If any round-57 text (report prose, lesson, SCORECARD) asserts that the previously committed counters still pass at
   the round-57 tip, that sentence is false for `c56_quote_truth` and must be scoped to "growth-tolerant counters" or
   dropped. [INFERENCE] no such sentence was searched for me; the L1 should grep its own round-57 prose for
   "c56_quote_truth" / "round-56 counters".
3. If instead the L1 wants a tip-live round-56 gate, the only compliant route is a new counter version that accepts
   growth (e.g. `len(rows) == mirror_rows + NEW_ROWS + <rows added after round 56>` with an explicit post-round-56 row
   list), and per the contract's receipt discipline the run must land under a new file name — do not rewrite
   `controls/after-c2-quote-truth.txt` or its `revision:` line. That is a semantics change to a historical claim, so
   it is the L1's call, not a repair I should make. [INFERENCE] on the version-bump being the only route.
4. No repair is needed to the registry append or to the round-57 mirror pin: both are verified byte-clean above.
5. Rows 1 and 2 changed numbers only (`knowledge_files` 52→54, `coverage_rows` 54→56) with the same `met=True`/EXIT=0;
   no action. Rows 4–8 are byte-identical results and need no follow-up.

## UNRUN:

- `c56_quote_truth`'s own selftest and the c57 counters (`c57_receipt_pins.py`, `c57_idresolver_gate.py`,
  `c57_quote_truth.py`) were not run: outside this assignment's command list and owned by other seats.
- No run at `4cb225fb` (round-56's measured revision) to re-confirm its 8/8; the base run at `28fa0b2` plus the
  additive diff already localises the flip, and the committed receipt records that run.
- No network-dependent gate (`remap`, `sitemap-file-audit`, `source_recheck --manifest`) was exercised.
- None of the eight scripts was executed against the live lane working tree (which the L1 may be repairing); all runs
  were in the two scratch clones, so results describe revisions, not the working tree.
- No tool install or upgrade was needed (node v24.21.0, python 3.14.8 present); no pacman call was made.

VERDICT: Only `c56_quote_truth` changes result at `4b8c730` (8/8 EXIT=0 → 6/8 EXIT=1), and solely because the registry grew 158→160 rows past its round-56 mirror pin; the other seven commands are unchanged, and the round-57 append is a verified pure addition whose own pin is intact.
