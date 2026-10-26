# ExecRelabelDiffs

Seat: round-57 W1, claim C1 sub-question — did the six historical receipt relabels change any
counter RESULT? Read-only over the lane (git show/log/ls-tree + one scratch clone); no lane file,
index or jj state touched. Only this report was written.
Environment: python3 3.14.8, git 2.56.0, host loaded (each run given a long timeout, no retries).
No tool installed or upgraded (pacman never invoked).

METHOD. Scratch clone `D=/tmp/tmp.9Psk3xu2KE`
(`git clone -q --no-checkout /home/vgpnk/Projects/shokunin/kake-shokunin $D`;
`git -C $D rev-parse --show-toplevel` = `$D`). Per case: `git -C $D checkout -q <rev>` then
`python3 -B $D/<counter> --root $D --revision <rev>`. The receipt body is compared mechanically
against `git -C <lane> show HEAD:<receipt>` after dropping `revision:` and `EXIT=` lines (the
round-52 receipts carry a doubled `EXIT=0` capture line; a single re-run prints the counter's one
`EXIT=0`). 12 runs total (both revisions for each of the six receipts); every run exit 0.

## PER RECEIPT

| # | path (under `.ufo/waves/`) | claimed-at (pre-relabel) | relabelled-to | relabel commit | re-run at old rev | re-run at new rev | body equal |
|---|---|---|---|---|---|---|---|
| 1 | `round-52/control/c1-ledger-real.txt` | `3a50ae43` | `1ae8de5d` | `a4a890c` | `3/3 met=True`, L1/L2/L3 PASS, exit 0 | identical | **yes** |
| 2 | `round-52/control/c2-quote-real.txt` | `3a50ae43` | `1ae8de5d` | `a4a890c` | `8/8 met=True`, C1–C8 PASS, exit 0 | identical | **yes** |
| 3 | `round-55/controls/after-c1-readme-index.txt` | `faf9abe8` | `64c0ce12` | `955e3d7` | `index_mismatches=0 knowledge_files=49 met=True`; `unindexed=0 multi=0 thin=0 duplicate=0 head_changed=0 deleted=0 dangling=0 coverage_rows=51`, exit 0 | identical | **yes** |
| 4 | `round-55/controls/after-c2-quote-truth.txt` | `faf9abe8` | `64c0ce12` | `955e3d7` | `8/8 met=True`, C1–C8 PASS, exit 0 | identical | **yes** |
| 5 | `round-56/controls/after-c1-selftally.txt` | `f8438a28` | `4cb225fb` | `ad06cb8` | `tally_mismatches=0 rows_checked=10 met=True`, 10 rows OK, exit 0 | identical | **yes** |
| 6 | `round-56/controls/after-c2-quote-truth.txt` | `f8438a28` | `4cb225fb` | `ad06cb8` | `8/8 met=True`, C1–C8 PASS, exit 0 | identical | **yes** |

Mechanical result (one line per run, `body_equal` = re-run stdout body vs committed receipt body):

```
r52-c1 @3a50ae43 exit=0 body_equal=True rerun_lines=4  receipt_lines=4
r52-c2 @3a50ae43 exit=0 body_equal=True rerun_lines=9  receipt_lines=9
r52-c1 @1ae8de5d exit=0 body_equal=True rerun_lines=4  receipt_lines=4
r52-c2 @1ae8de5d exit=0 body_equal=True rerun_lines=9  receipt_lines=9
r55-c1 @faf9abe8 exit=0 body_equal=True rerun_lines=2  receipt_lines=2
r55-c2 @faf9abe8 exit=0 body_equal=True rerun_lines=9  receipt_lines=9
r55-c1 @64c0ce12 exit=0 body_equal=True rerun_lines=2  receipt_lines=2
r55-c2 @64c0ce12 exit=0 body_equal=True rerun_lines=9  receipt_lines=9
r56-c2 @f8438a28 exit=0 body_equal=True rerun_lines=9  receipt_lines=9
r56-c1 @f8438a28 exit=0 body_equal=True rerun_lines=11 receipt_lines=11
r56-c2 @4cb225fb exit=0 body_equal=True rerun_lines=9  receipt_lines=9
r56-c1 @4cb225fb exit=0 body_equal=True rerun_lines=11 receipt_lines=11
```

RELABEL DIFFS (each commit touches exactly the two receipt paths, one line each; no other line of
either receipt is in the hunk):

- `a4a890c` (round 52, `--stat`: `c1-ledger-real.txt 2 +-`, `c2-quote-real.txt 2 +-`)
  ```
  -  revision: 3a50ae4321e64856229c7cd0d39d3557b204d489
  +  revision: 1ae8de5d4dee8300624b0db2a94497ff905942c5
  ```
  (same single-line swap in both files; `git show a4a890c -- <the two paths>`)
- `955e3d7` (round 55, `--stat`: the two receipts + `c2-selftest.txt`, `LOG.md`, `SCORECARD.md`, 5 files / 5 +-)
  ```
  -  revision: faf9abe81d1ef5925733f756a918527483073fe8
  +  revision: 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6
  ```
- `ad06cb8` (round 56, `--stat`: the two receipts + `c2-selftest.txt`, `w2/MutC2Selftest.md`, `LOG.md`, `SCORECARD.md`, 6 files / 16 + 17 -)
  ```
  -  revision: f8438a282d5946b386812d784cc617edcbc9201d
  +  revision: 4cb225fb032b04166fb0232bc98a7bcce72675ec
  ```

COUNTER IDENTITY ACROSS EACH PAIR (blob at old vs new rev): five of six counters are the same blob
(`c52_wave_ledger` 93891e1, `c52_quote_truth` 1bd6e78, `c55_readme_index` 1a65be4, `c55_quote_truth`
1c4688c, `c56_selftally` 4b6942f). `c56_quote_truth.py` **changed** (`6dcb050` → `c48aa2c`,
+67 lines, selftest fixtures only — `git diff f8438a28 4cb225fb -- …/c56_quote_truth.py` is a single
insertion block inside `selftest()`), and it still prints the identical 8/8 body at both labels.

WHAT CHANGED BETWEEN EACH PAIR (why body invariance is not vacuous):
- `3a50ae43`→`1ae8de5d`: baselines.json + the ten round-52 control receipts only (no corpus bytes).
- `faf9abe8`→`64c0ce12`: reviewer repairs to `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md`
  (4 lines) and `corpus/lessons/round-55.md` (6 lines), the round-55 receipts, SCORECARD/LOG/settlement.
- `f8438a28`→`4cb225fb`: `c56_quote_truth.py` (selftest), `SKILL.md` (2 lines: pin/counts), `contract.md`,
  round-56 receipts, SCORECARD/LOG/settlement, two w2 reports.

## STATEMENTS THAT NAME THE REVISION

Round 52 (no LOG section exists for round 52 — `LOG.md` jumps `:1977` "## Round 50" → `:2114` "## Round 54";
round-52 `w1/` holds only `swarm-registry.json`):
- `SCORECARD.md:4242-4243` — "Measured revision `1ae8de5d4dee8300624b0db2a94497ff905942c5`; every receipt below lives under `.ufo/waves/round-52/control/`."
  (`git log -S1ae8de5d4dee -- SCORECARD.md` = `a4a890c`, i.e. the pin and the relabel land in one commit;
  the SCORECARD at `1ae8de5d` has no round-52 measured section at all.)
- receipts: `round-52/control/c1-ledger-real.txt:5`, `round-52/control/c2-quote-real.txt:10` — `revision: 1ae8de5d…`

Round 55:
- `SCORECARD.md:4299-4300` — "measured commit `64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6`."
  (`git log -S64c0ce12ffe3 -- SCORECARD.md` = `955e3d7`, the relabel commit.)
- `LOG.md:2166` — "after `0`, exit 0 at `64c0ce1`." (`git log -S64c0ce1 -- LOG.md` = `955e3d7`.)
- receipts: `round-55/controls/after-c1-readme-index.txt:3`, `round-55/controls/after-c2-quote-truth.txt:10` — `revision: 64c0ce12…`
  (`round-55/settlement.md` names no revision hash.)

Round 56:
- `SCORECARD.md:4323-4324` — "measured content commit `4cb225fb032b04166fb0232bc98a7bcce72675ec`."
  (`git log -S4cb225fb032b -- SCORECARD.md` = `ad06cb8`, the relabel commit.)
- `LOG.md:2187` — "after `0`, exit 0 at `4cb225fb032b04166fb0232bc98a7bcce72675ec`."
  (`git log -S4cb225fb032b -- LOG.md` = `ad06cb8`, the relabel commit; `LOG.md:2185` carries the
  `KAKE_R52_SELFTEST_REV=1ae8de5d4dee` pin, introduced by `4cb225f`.)
- receipts: `round-56/controls/after-c1-selftally.txt:12`, `round-56/controls/after-c2-quote-truth.txt:10` — `revision: 4cb225fb…`
- prior finding restated: `corpus/lessons/round-56-verifier-spotcheck.md:95-97` — the receipts "were committed
  in `4cb225f` with `revision: f8438a282d59…`; `ad06cb8` edited that line to `4cb225fb…`", so "the report's
  'After (`4cb225fb`)' column is therefore not a run over" that revision.

## FINDINGS / RISKS

1. **All six relabels are result-neutral.** At both the old and the new label each counter prints exactly
   the PASS/FAIL/measure lines the committed receipt carries (12/12 mechanical body equality, all exit 0).
   So the relabel never changed what a receipt asserts about the measured tree; it changed the claim about
   *when/where* the run happened.
2. **Structural pattern (not asked, but material to C1):** every relabel moved the pin from the revision that
   was actually measured (the parent) to the receipt's **own introducing commit** — `1ae8de5d` introduced
   `c1-ledger-real.txt`/`c2-quote-real.txt`, `64c0ce12` introduced the two round-55 `after-*` files,
   `4cb225fb` introduced the two round-56 `after-*` files. The round-57 C1 frozen form requires a *strict
   ancestor* of the introducing commit for the new receipts, so the historical relabelled form would not be
   admissible for a new receipt even though its body is true at the new label.
3. Round-52 is the only pair where the SCORECARD pin and the relabel landed in the same commit (`a4a890c`);
   for rounds 55/56 the SCORECARD/LOG pins likewise landed in the relabel commit itself. No committed window
   was found in which SCORECARD/LOG named a revision the receipt did not carry.
4. `c56_quote_truth.py` changed between `f8438a28` and `4cb225fb` (selftest-only, +67 lines) yet the gate body
   is byte-identical — the added fixtures did not alter the measured result.
5. Duplicate relabel objects exist under jj keep refs, not reachable from `master`: `c7a6935` (parent
   `64c0ce12`, same diff as `955e3d7`) and `99254b4` (parent `4cb225fb`, same diff as `ad06cb8`). Recorded
   as retained evidence only; the `master` history carries `955e3d7`/`ad06cb8`.
6. Limitation: this seat verifies *body equality of the printed result at both labels*, not that any run
   occurred at the relabelled revision at the time of the relabel — no such evidence exists in the history,
   which is exactly the round-56 verifier defect.
7. Nothing installed, no pacman, no lane index/jj mutation; scratch clone `/tmp/tmp.9Psk3xu2KE` remains under
   `/tmp` and is not part of the lane.

VERDICT: None of the six relabels changed a counter result — all twelve re-runs (old and new label) reproduce the committed receipt bodies exactly, exit 0; the relabels misstate run provenance (each new pin is the receipt's own introducing commit), not the measured outcome.
