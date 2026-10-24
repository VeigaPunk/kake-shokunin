# RerunW1TallyV1 — wave-1 counter-v1 tally re-check

Statement under test (SCORECARD.md:2757-2764): "15 of 141 wave-1 receipts meet counter v1,
all from live seats." Verdict: **holds** on every checked clause.

## Checks run (repo /home/vgpnk/Projects/shokunin/kake-shokunin, HEAD eae5ae2)

1. `ls .ufo/waves/round-41/verification/w1/*.json | wc -l` → **141** (exit 0).
2. `jq -s 'map(select(.met))|length' verification/w1/*.json` → **15** (exit 0).
   Meeting labels: w1-MutStructure-m08_scheme_leading_digit, -m07_query_hash,
   -m06_path_question, -m03_empty_host, w1-MutRepertoireAdd-M05-port-letter,
   w1-MutPlacement-strip, -locLong16, -first2048, w1-CtlRawBytes-V3_decode_probe,
   w1-CtlNoUserinfoPort-no-port-v2, w1-CtlNoPct-terminal_pct,
   w1-CtlGeneratorShape-v1_shape, w1-CtlConstantFamily-delimiter_proxy,
   w1-CtlCharsetProxy-charset_pct_rules, w1-CtlAllowList-v11_charset_netloc_brackets.
   Matches the SCORECARD table exactly (2768-2773).
3. sha256 of all 10 sampled `controls/w1/<Seat>/<tool>.py` == `toolSha256` in the
   receipts → copies unchanged since L1 scoring.
4. Re-score: `timeout 850 prlimit --as=4000000000 python3 -B c1_count.py --root .
   --tool-file <tool> --label <receipt label> --seed <recorded seed> --out <sandbox>`.
   Receipts record the L1's random seeds; rerunning at the same seed reproduces the
   exact case set, so `passed` is directly comparable.

| label | receipt passed | rerun passed | rerun met | rerun exit |
|---|---|---|---|---|
| w1-MutStructure-m03_empty_host | 1434 | 1434 | true | 0 |
| w1-MutPlacement-strip | 1434 | 1434 | true | 0 |
| w1-CtlAllowList-v11_charset_netloc_brackets | 1434 | 1434 | true | 0 |
| w1-CtlGeneratorShape-v1_shape | 1434 | 1434 | true | 0 |
| w1-CtlNoPct-terminal_pct | 1434 | 1434 | true | 0 |
| w1-CtlAllowList-v1_strict | 854 | 854 | false | 1 |
| w1-CtlConstantFamily-empty_stdout | 0 | 0 | false | 1 |
| w1-CtlIdKeyed-AllValid | 791 | 791 | false | 1 |
| w1-CtlNoReader-no_reader_all_valid | 1193 | 1193 | false | 1 |
| w1-MutRepertoireAdd-M12-fragment-space | 1433 | 1433 | false | 1 |

5/5 meeting re-met, 5/5 non-meeting identical `passed`; toolSha256 identical in all
rerun receipts. Rerun artifacts: /fast/scratch/hyaku/kake-r41w2/RerunW1TallyV1/.

## Dead/refused seats

`w1-dispatch-log.txt` lines 1-2: 37 spawned at 09:47:43Z, 37 returned at 10:03:28Z,
**0 dead, 0 refused, 0 cancelled**. `w1-dispatch.json` counts {spawn:37, resume:0};
registry members = 37, all `"kind":"spawn"`. Python set diff: all 22 receipt-bearing
seats and all 10 met-bearing seats are registry members; no receipt seat is absent
("receipt seats not in registry: NONE"). The log carries no per-seat status field —
dead/refused exists only as the log's settle line — but nothing contradicts it, and
every met receipt maps to a spawned seat. **No receipt belongs to a dead or refused seat.**

## Per-statement verdict

- "15 of 141 receipts meet" → holds (141 files, 15 met; exact label set confirmed).
- "all from live seats" → holds (0 dead/0 refused recorded; all met seats spawned).
- Counter reproducibility → holds for all 10 sampled tools (byte-identical tools,
  same seed ⇒ same `passed`, same `met`, same exit class 0/1).

## Environment / installs

None needed: bwrap  (/usr/bin/bwrap), python3 3.14.8, jq already installed; oracle
wheel abnf-2.9.1 sha-matched inside the counter. No tools installed or updated.

Residual risk: re-score sampled 10/141 receipts (5 met + 5 not-met); the other 131
rely on the same verified mechanism. Determinism shown only at recorded seeds.
