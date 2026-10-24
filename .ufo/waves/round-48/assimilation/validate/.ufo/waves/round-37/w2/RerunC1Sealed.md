# RerunC1Sealed — re-derive C1's measured result from committed bytes (r37 wave 2, falsify)

Attacked: SCORECARD.md "Round 37 — measured results" C1 row (SCORECARD.md:1980-1986 at 79d3c780),
its receipts `.ufo/waves/round-37/verification/c1-*.json`, the key pin, and the tool hash/provenance.

## Setup
Sandbox `/fast/scratch/hyaku/kake-r37w2/RerunC1Sealed/clone` (git clone of the lane, checkout
79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c, GIT_* unset, TMPDIR=sandbox/tmp). Counter = the clone's
committed `.ufo/waves/round-37/sealed_count.py`, sha256 `2ebb39b5…0cf0e3` (same at 202d625a, the
only commit that touches it; same as the lane working tree). No tools installed or updated.

Command, per revision R, all 7 in parallel, each under `timeout 900`:
`python3 -B .ufo/waves/round-37/sealed_count.py --root <clone> --revision R --key-revision 424aa248`
Stdout was byte-compared with `cmp` against `verification/c1-keyrev-at-R.json`. For 424aa248 the
receipt is the full-hash file name. Stderr was empty for every run.

## Per-revision result
| Revision | passed | met | exit (ours / receipt .exit) | byte-identical |
|---|---|---|---|---|
| 9dbc88bb | 28 | true | 0 / 0 | yes |
| 621fb528 | 0 | false | 1 / 1 | yes |
| 202d625a | 0 | false | 1 / 1 | yes |
| 4b089da6 | 0 | false | 1 / 1 | yes |
| ccc3b2b9 | 0 | false | 1 / 1 | yes |
| 528a6d02 | 0 | false | 1 / 1 | yes |
| 424aa248 | – | – | 2 / 2 ("key visible at the measured revision") | yes |

Also byte-identical: `verification/c1-at-9dbc88bb.json` (exit 0) and `verification/c1-at-621fb528.json`.
A repeat run at 9dbc88bb was byte-identical again (exit 0), and so was a `--key-file` run with the
key extracted from 424aa248 compared against `c1-at-9dbc88bb.json` (exit 0). The output is
deterministic.

## Hashes
- Key: `git show 424aa248:.ufo/waves/round-37/sealed/cases.json | sha256sum` gives
  `93ad9ee64db63b661b408e678f2c6f3d665b7f5c88ef1f977433dbceee8c0a90`. That equals `KEY_SHA256`
  (sealed_count.py:49) and the abbreviated pin `93ad9ee6…0a90` in the declaration text
  (SCORECARD.md:1777, present at 202d625a) and in the measured results (SCORECARD.md:1976). The key
  holds 28 cases and 44 runs. Its blob appears nowhere in the 9dbc88bb or 528a6d02 trees.
- Tool: `git show 9dbc88bb:scripts/robots_audit.py | sha256sum` gives
  `5eb767ec68a649145102619ed13754428bef489e432ed50eb20e9e50542cabae`. That matches `toolSha256` in the
  receipt, the abbreviation `5eb767ec…cabae` (SCORECARD.md:1986, lessons/round-37.md:18), the hash
  stated in `w1/ExecRobotsTool.md:11`, the wave-1 sandbox file
  `/fast/scratch/hyaku/kake-r37w1/ExecRobotsTool/robots_audit.py`, and the file at 79d3c780. The
  9dbc88bb commit (parent 528a6d02) adds only that file: 578 lines, mode 100755. That is consistent
  with "landed unedited". Nothing touches it between 9dbc88bb and 79d3c780.

## Verdicts
- C1 "passed 28 of 28 at 9dbc88bb, met; exit 0": **holds**. Reproduced byte-for-byte.
- C1 "Before: passed 0 of 28 at 621fb528, 202d625a, 4b089da6, ccc3b2b9, 528a6d02": **holds, but the
  zero is vacuous**. `scripts/robots_audit.py` is absent at all five revisions (`git cat-file -e`
  fails), so every receipt shows `toolPresent: false` and `toolSha256: null`. The before value
  measures "no tool", not a weaker tool. The scorecard does not say so in the row. Severity: low.
  The control receipts (stock parser 20, ablations 16–24) carry the discriminating evidence.
- "Measuring the reveal commit is refused with exit 2": **holds**.
- "Key sha256 equal to the pin; counter, key and target unchanged since 202d625a": **holds**.
  `git log -- sealed_count.py` shows only 202d625. The 202d625a blob has the same sha256.
- "Tool is ExecRobotsTool's file, sha256 5eb767ec…cabae": **holds** on bytes. Provenance gap
  (low): `w1/ExecRobotsTool.md` is **not in the measured tip 79d3c780**. `git ls-tree 79d3c780
  .ufo/waves/round-37/` has no `w1/`. The w1 reports land in child commit a5ae0280 ("wave-1 seat
  reports", 12 s later). The report at a5ae0280 has sha256 `194e360b…b147`, the same as the working
  tree. So the tip's SCORECARD cites a wave-1 report that the tip itself does not contain. The
  wave-2 brief's `git show 79d3c780:<path>` reading of w1/ fails.
- "The build was also measured before the reveal with the key file (`c1-at-9dbc88bb.json`)":
  **unverifiable from bytes**. The counter's output records neither the key source nor a timestamp.
  The `--key-file` and `--key-revision` outputs are byte-identical, and that receipt was first
  committed in the reveal commit 424aa24 itself. Nothing committed shows it predates the reveal.
  This changes nothing about the result, because the key is pinned by sha256 either way.

## Residual risk / gaps
- I did not re-audit the counter's jail or judge logic, the controls, the ablations or the selftest.
  Those are out of this item.
- Runs used the host's `/usr/bin/python3` and `bwrap`. The versions were not recorded in the receipts
  and not compared.
- No processes remain (pgrep empty). Sandbox outputs: `/fast/scratch/hyaku/kake-r37w2/RerunC1Sealed/out/`.
