# CtlSkipR — wave 1 control report (round 40, C1)

Seat: KakeR40.CtlSkipR. Control class: partial repair that skips class R
(repeated-`id` rule); implement E and U exactly as the reference, leave R as base.

## Tool
- Path: `/fast/scratch/hyaku/kake-r40w1/CtlSkipR/ctl_skip_r.py`
- sha256: `fc3bd1708d672c723730d5d2902eeb348c5290dac0abdd5aa61d571fdbf51485`
- Built from base `f043c721…b508f8:scripts/sitemap_audit.py` + the reference's two
  E/U hunks, verbatim:
  - U: `_parse_url` leading-control/TAB/CR/LF guard, `ctl_skip_r.py:70-71`
    (matches `ref_fix.py:70-71`).
  - E: U+0000 → `xml_malformed` after BOM strip, `ctl_skip_r.py:189-190`
    (matches `ref_fix.py:191-192`).
  - R: left as base — `seen_ids.add(ident)` only after the isinstance gate
    (`ctl_skip_r.py:339-344`), so an earlier check that is invalid for a missing/
    non-string member never registers its id. This is the skipped declared work.

## Counter results (command used)
```
prlimit --as=4000000000 timeout 1200 python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/c1_count.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --tool-file /fast/scratch/hyaku/kake-r40w1/CtlSkipR/ctl_skip_r.py \
  --label CtlSkipR --seed <N> --out .../receipt-seed<N>.json
```
| seed | passed | E | U | R | selftest | met | exit |
|------|--------|----|----|----|----------|-----|------|
| 1 | 25/30 | 9/9 | 13/13 | 3/8 | PASS 150/150 | false | 1 |
| 2 | 25/30 | 9/9 | 13/13 | 3/8 | PASS 150/150 | false | 1 |

Receipts: `receipt-seed1.json`, `receipt-seed2.json` (same sandbox). Counter sha:
`6d73b8f498a29a5a86c9a7f1ce5d87cd135c40f1b634d869d14659cc10bee8d8` (unchanged).

## Findings
- Witnesses that caught the skip: R1–R5 (5 of 8). Fail text (both seeds, receipt rows):
  - R1, R2, R3, R4: `check 1: got clean/None/[] want error/check_invalid/[]`
    (repeat of an id whose first occurrence was invalid — missing `file`, missing
    `sitemapUrl`, `file: 7`, `sitemapUrl: null` — is judged clean).
  - R5: `check 2: got clean/None/[] want error/check_invalid/[]` (repeat after a
    first occurrence invalid for a missing member).
  - R6–R8 pass (int id vs str, non-object check, case-different id), meaning the
    counter's R set pins exactly the skipped shape, nothing else.
- E 9/9 and U 13/13 pass: the reference E/U implementation is faithfully reproduced;
  no other witness failed under either seed (hosts/ids random per run).
- Selftest 150/150: the R-skip is invisible to the round-39 regression (it only
  tests post-gate duplicates), so the counter's selftest half does not compensate
  for the missing class.

## Attacked statement
- **Holds.** "The C1 counter's power to reject a tool that skips this work": the
  counter rejects an R-skipper at 25/30 (exit 1, `met: false`) while the same tool
  passes E and U completely and the selftest. Every witness in class R that targets
  the skipped rule (R1–R5) fires; no tool can skip the rule and still reach 30/30,
  because R1–R5 each require the id of an earlier-invalid check to be registered —
  any mechanism that does this for all five invalid shapes is the declared repair.
  No control was found that meets the predicate; this control is a clean negative.

## Notes
- No tools installed; no lane mutation (report path is the only lane write);
  no network; no subagents (labrat only).
