# RerunControls — re-score of retained C1 controls and the independent implementation (round 37, wave 2)

Seat: KakeR37.RerunControls (leaf). Sandbox: `/fast/scratch/hyaku/kake-r37w2/RerunControls/`
(clone at `79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c`, `TMPDIR` inside the sandbox; GIT_DIR,
GIT_WORK_TREE and GIT_INDEX_FILE unset). No lane file was written except this report. No tools
were installed. No network access. No processes are left running (`pgrep -fa sealed_count` found none).

## What I attacked
1. The committed receipts `verification/control-*.json` and `independent-selftest-reference.json`
   were scored by the L1 with `--key-file /fast/scratch/hyaku/kake-r37/private/cases.json`
   (`verification/score_control.sh:12`). I re-scored every file with the revealed key instead
   (`--key-revision 424aa248`) to see whether the private key and the revealed key give the same
   results.
2. Whether the sha256 of each retained file matches the hash its seat report gives.
3. The control figures in SCORECARD.md, lines 1908-1915 and 1994-1996.

## Commands (run in the clone; counter sha256 `2ebb39b5…0e3`, the same as `counterSha256` in every receipt)
- `timeout 900 python3 -B .ufo/waves/round-37/sealed_count.py --root $C --tool-file $C/<file> --key-revision 424aa248`
  for the 6 `retained/controls/*-robots_audit.py` files and `retained/independent/independent_robots_audit.py`,
  all 7 in parallel. I ran the whole set twice (`out/` and `out2/`) because the counter randomizes ids and
  file names. Exit codes: 1 for the five controls that do not meet the target, 0 for Shortcut-followup
  and independent. Both runs gave identical exit codes and identical perCase lists. stderr was empty.
- A python comparison of `passed`, `met`, `perCase` (compared id by id), `toolSha256`, `counterSha256`,
  `error` and the key set between each receipt and my re-run. I also hashed the file with `hashlib`.
- `sha256sum retained/controls/*`; `rg` for 64-hex hashes in `ctl/*.md`; `cmp` on the two Junk files (exit 0).

## Result table
| control | committed passed (exit) | re-run passed (exit) | perCase diff | file sha256 = receipt = seat report | match |
|---|---|---|---|---|---|
| CtlC1AllFalse | 4, met false (1) | 4, met false (1) | none (only g1-g4 pass) | `7bb59c7a…825a` = `ctl/CtlC1AllFalse.md:11` | yes |
| CtlC1ConstantClean | 0, false (1) | 0, false (1) | none | `96c8e739…618b` = `ctl/CtlC1ConstantClean.md:10` | yes |
| CtlC1Junk | 0, false (1) | 0, false (1) | none | `4c23062f…b33e` = `ctl/CtlC1Junk.md:11` | yes |
| CtlC1NaiveReader | 20, false (1) | 20, false (1) | none (b1-b4 and e1-e4 fail) | `fdc64538…3491` = `ctl/CtlC1NaiveReader.md:11` | yes |
| CtlC1NoReader | 0, false (1) | 0, false (1) | none | `4a4dfc5d…73e3` = `ctl/CtlC1NoReader.md:5` | yes |
| CtlC1Shortcut-followup | 28, met true (0) | 28, met true (0) | none | `61724ead…6f7d` = `ctl/CtlC1NoReader-shortcut.md:4` | yes |
| independent_robots_audit | 28, met true (0) | 28, met true (0) | none | `3400abd5…bdb8` = `w1/ExecRobotsSelftest.md:10` (in `a5ae028`) | yes |

## Verdicts
- "Controls under the same counter: constant clean 0; junk 0; no-reader 0; all-false 4; stock
  parser 20; shortcut follow-up 28" (SCORECARD.md:1994-1996, table at 1908-1915): **holds**. I
  reproduced each figure with the revealed key, twice, with identical perCase lists. So the private
  key file and the revealed key at `424aa248` score all seven tools the same way.
- "The stock parser passes every case of (a), (c), (d), (f), (g) and none of (b), (e)" (SCORECARD.md:1917-1918):
  **holds**. It fails exactly b1-b4 and e1-e4.
- "Every do-nothing, junk, constant, all-false and no-reader control at or below 4" (SCORECARD.md:1965): **holds** (0/0/0/4).
- "Independent blind implementation scores 28 of 28" (SCORECARD.md:1987-1988): **holds**. Its
  sha256 is the one the ExecRobotsSelftest seat reported. It imports only stdlib (json, os, re, stat,
  sys, urllib.parse; lines 31-36), not `scripts/robots_audit.py`. A difflib line ratio against the
  landed tool (`5eb767ec…cabae`) is 0.169, with 25 shared non-blank lines longer than 20 characters.
  That supports independence but does not prove the seat was blind. [INFERENCE]
- Every control's sha256 matches its seat report: **holds** for all six controls.
- The AllFalse seat predicted at most 4 of 28, coming only from (g) (`ctl/CtlC1AllFalse.md:24`):
  **confirmed**. The ConstantClean seat predicted 0 of 28 (`ctl/CtlC1ConstantClean.md:30`): **confirmed**.

## Findings (by severity)
- None at high or medium severity in this scope.
- Low, freshness: `ctl/CtlC1Junk.md:11-12` gives one sha256 for two differently named deliverables
  (`robots_audit.py` and `source_recheck_junk.py`), and both are retained. `cmp` shows the files are
  byte-identical, so the report is accurate, but a reader could take it for a copy-paste slip. The
  duplicate `retained/controls/CtlC1Junk-source_recheck_junk.py` is unused by any C1 receipt.
- Low, freshness: the measured tip `79d3c78` cites wave-1 seat reports that are not in its tree.
  Examples: `corpus/lessons/round-37.md:36` cites `w1/ScoutReopenS011.md`, and the independent
  file's provenance hash is only in `w1/ExecRobotsSelftest.md:10`. `git ls-tree 79d3c78
  .ufo/waves/round-37/` has no `w1/`. The reports landed in the child commit `a5ae028`
  ("wave-1 seat reports"), so the tip alone does not resolve those pointers.

## Residual risk and verification gaps
- The Shortcut-followup reaching 28 of 28 is disclosed (SCORECARD.md:1949-1972). I did not re-check
  its claim that it scores 20 without the six rule patches. That is outside this item.
- I did not run the robots selftest against these tools, and I did not re-score the ablation tools
  (`sealed/ablation-tools/`). Both are outside this item.
- I did not attempt to verify that the controls and the independent seat were blind to the key.
