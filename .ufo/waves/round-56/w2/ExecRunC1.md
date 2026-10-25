# ExecRunC1

Attack on claim C1 (calibration: `SKILL.md` registry self-test tallies vs the tallies the documented
commands print) **as measured**, at the revision under attack
`a450e43e696d032e3ac308383f6b3394e0c92860`, base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`,
round date 2026-10-25. Frozen predicate: `met: tally_mismatches == 0 AND rows_checked == 10`.

All runs happened in my own clone `D=/tmp/execrunc1.bFY31g`
(`git clone -q --no-checkout <lane> "$D" && git -C "$D" checkout -q a450e43e…`),
`git -C "$D" rev-parse --show-toplevel` = `/tmp/execrunc1.bFY31g`, `HEAD` = `a450e43e…` verified before
and after every batch; `git -C "$D" status --porcelain` empty after all runs. No lane file, lane index,
jj state or sibling lane was touched; this report is the only file I wrote. Counter source read at
`.ufo/waves/round-56/c56_selftally.py` (POP at :63-75, `run_command` at :200-213).

## COUNTER RUNS:

Command, verbatim, `D=/tmp/execrunc1.bFY31g`:
`python3 -B .ufo/waves/round-56/c56_selftally.py --root "$D" --revision a450e43e696d032e3ac308383f6b3394e0c92860`

| run | extra args | exit | wall | stdout md5 | tally line |
|---|---|---|---|---|---|
| run1 | — | **0** | ~28 s (see note) | `92060ce2eaab0276b9588f1e530f36dd` | `tally_mismatches=0 rows_checked=10 met=True` |
| run2 | — | **0** | ~28 s (see note) | `92060ce2eaab0276b9588f1e530f36dd` | identical |
| run3 | `--json` | **0** | ~28 s (see note) | `7e4fd91ebbebf64e6b534fccbcc1e6fb` | `"tally_mismatches": 0, "rows_checked": 10, "met": true` |
| timed re-pair a | — | **0** | **29.232 s** | `92060ce2…` | identical to run1 |
| timed re-pair b | — | **0** | **28.504 s** | `92060ce2…` | identical to run1 |
| counter `--selftest` | — | **0** | 2.572 s | — | `c56 selftally selftest: 47/47` |
| base run | `--revision e48354b7…` | **1** | 25.713 s | — | `tally_mismatches=7 rows_checked=10 met=False` |

- **Run1 and run2 are byte-identical** (`cmp` clean, same md5); the timed re-pair reproduced the same
  bytes a third and fourth time. Stderr was empty (0 bytes) on every run.
- The first batch of three runs totalled 84.35 s wall; `bc` is not installed on this host, so that batch
  carries no per-run split — the 29.232 s / 28.504 s pair above is the per-run timing evidence.
- run3 `--json` rows: all ten `"problems": []`, `"checked": true`, every `"exit": 0`; claims
  45/106/204/235/23/9/19/18/44/54 and observed `45/45 106/106 204/204 235/235 23/23 9/9 19/19 18/18 44/44 54/54`.
  Top-level `"exit": 0`, `"met": true`, `"schema": "kake-r56-c1-selftally-v1"`.
- The counter's own selftest at the tip passes 47/47 (the count the contract's §Counter versions declares);
  I did not judge whether those 47 checks are mutant-killing — that is the mutation seat's term, not mine.

## RECOUNT TABLE:

Counter-free recount. I extracted each row's `Self-test` cell myself from
`git show a450e43e…:SKILL.md` (my own parser, no import of the counter; cells at lines 726, 1067, 1093,
1128, 1198, 1199, 1215, 1216, 1233, 1234; each row name occurs exactly once in the file), read the
documented command and claimed number by eye, then ran the command **exactly as written** in the same
clone with my inherited environment and captured the printed tally line.

| row (SKILL.md line) | claimed | documented command I ran | printed | exit | agree |
|---|---|---|---|---|---|
| base-path-audit (:726) | 45 (`30 matrix` + `15 round-29 regression`) | `python3 -B scripts/base_path_selftest.py` | `45/45 fixtures passed` (**stderr**) | 0 | **yes** |
| source-recheck-audit (:1067) | 106 | `python3 -B scripts/source_recheck_selftest.py` | `"passedOverTotal": "106/106"` (JSON) | 0 | **yes** |
| robots-expectation-audit (:1093) | 204 | `python3 -B scripts/robots_audit_selftest.py` | `"passedOverTotal": "204/204"` (JSON) | 0 | **yes** |
| sitemap-file-audit (:1128) | 235 | `python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` | `PASS 235/235` | 0 | **yes** |
| redirect-expectation-audit (:1198) | 23 (of 23) | `python3 -B scripts/redirect_audit.py --selftest` | `selftest: 23/23 passed` | 0 | **yes** |
| commit-citation-lint (:1199) | 9 (current; cell also names the historical `8/8`) | `python3 -B scripts/citation_lint.py --selftest` | `selftest: 9/9 passed` | 0 | **yes** |
| wave-evidence-ledger (:1215) | 19 | `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest` | `c52 ledger selftest: 19/19` | 0 | **yes** |
| quote-truth-counter (:1216) | 18 | `KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` | `c52 quote-truth selftest: 18/18 (fixture revision 1ae8de5d4dee)` | 0 | **yes** |
| readme-index-counter (:1233) | 44 | `python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` | `c55 readme-index selftest: 44/44` | 0 | **yes** |
| yahoo-robots-quote-truth-counter (:1234) | 54 | `KAKE_R55_SELFTEST_REV=64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` | `c55 quote-truth selftest: 54/54 (fixture revision 64c0ce12ffe3)` | 0 | **yes** |

Recount wall times (ms): 1406, 4043, 4551, 5452, 102, 49, 1045, 560, 5863, 1991.
**10 of 10 agree with the counter's per-row `claim`/`observed` and with the registry cells.**

Side checks on the same cells:
- The `quote-truth-counter` pin is load-bearing, exactly as the cell's prose says: run **without**
  `KAKE_R52_SELFTEST_REV` at tip, the selftest exits **1** with
  `FAIL C8_mirror_bytes: registry rows 158 != mirror rows 145 + 3`. The documented command carries the
  pin, so the claim is not affected.
- The ambient environment contains no `KAKE_*` variable, so my inherited-env recount and the counter's
  fixed environment (`PATH/HOME/LANG/PYTHONDONTWRITEBYTECODE`, `.ufo/waves/round-56/c56_selftally.py:200-213`)
  are the same measurement here — no host-exported pin can be rescuing a row, and no row needs one
  beyond the two documented pins.

## BASE DIFF:

`python3 -B .ufo/waves/round-56/c56_selftally.py --root "$D" --revision e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`
→ exit **1**, 25.713 s. `diff -u .ufo/waves/round-56/controls/base-c1-selftally-v2.txt <stdout>` → **rc 0,
byte-identical**, trailing `EXIT=1` line included. Reproduced base mismatches: 7 —
source-recheck-audit `101≠106`, robots-expectation-audit `137≠204`, sitemap-file-audit `150≠235`,
commit-citation-lint `8≠9`, quote-truth-counter `18 vs 17/18 selftest_failed`, readme-index-counter
`35≠44`, yahoo-robots-quote-truth-counter `47≠54`; `base-path-audit`, `redirect-expectation-audit` and
`wave-evidence-ledger` already OK at base. This matches the contract's declared before-state (7 of 10,
claimed `101/137/150/8/18/35/47`) and the frozen do-nothing control. Note also that
`controls/base-c1-selftally.txt` (v1) and `controls/base-c1-selftally-v2.txt` are byte-identical files.

## DISAGREEMENTS:

**None.** Every element of the frozen predicate holds on the measured bytes:
`tally_mismatches=0`, `rows_checked=10`, `met=True`, exit 0, twice byte-identically and once as JSON;
the counter-free recount agrees on all ten rows with exit 0 each; the base run reproduces the v2 control
byte-for-byte at exit 1. C1's before (7 → after 0) is real as measured, not inferred from the counter.

Observations that are **not** predicate failures and that I hand to the L1 as context:
1. `base-path-audit` prints its tally (`45/45 fixtures passed`) on **stderr**; stdout is a JSON matrix
   listing with no tally. The counter merges stderr (`stderr=STDOUT`, `c56_selftally.py:211-212`), so the
   measurement is right, but a human following the row with `2>/dev/null` would see no tally.
2. `commit-citation-lint`'s cell carries two numbers — `9/9` current and `8/8` historical. The claim regex
   `\((\d+)/\d+;` matches only `(9/9;` because the historical number is written `then-tally 8/8;` without
   the parenthesised form. By eye the cell is unambiguous (9 is the current selftest), so this is a
   regex-fragility note, not a wrong claim.
3. `base-path-audit`'s claim is the sum of two prose integers (30 + 15); the counter's `nclaims=2` sum rule
   covers it. The printed total is what agrees, so the decomposition itself is unverified by the counter.
4. Concurrency hygiene: while I ran, other seats' `/tmp/c56-tally-*` clones came and went (5 present at
   19:58, 2 at 19:59 — both older than my first run, from killed seats). The counter clones per row into
   its own `mkdtemp` and removes it (`c56_selftally.py:185-195, 294`), and **none of my runs left a
   directory behind**, so parallel seats do not collide on this counter.
5. Not run by me, deliberately: any judgement of whether these ten selftests are *good* (mutant-killing),
   the ~20 fixture-count mentions outside the ten rows, and helper pinning beyond the pinned script's own
   directory — the contract already excludes those from C1's predicate; they belong to the mutation and
   code-review seats.

VERDICT: C1 confirmed as measured — 0/10 mismatches, `rows_checked=10`, `met=True`, exit 0, twice byte-identically plus a JSON run, all ten tallies independently reproduced by hand-run documented commands at exit 0, and the base run reproduces `controls/base-c1-selftally-v2.txt` byte-for-byte at exit 1; no disagreement found.
