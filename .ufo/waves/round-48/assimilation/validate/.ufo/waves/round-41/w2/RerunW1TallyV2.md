# Kake R41 wave 2 — RerunW1TallyV2 (falsify seat)

Axes: operability (counter+tool machinery runs and re-scores reproducibly), freshness (claims match receipts as they exist now).
No tools installed (nothing needed; counter needs only python3+bwrap, both present). No lane mutations outside this report; receipts written to sandbox `/fast/scratch/hyaku/kake-r41w2/KakeR41.RerunW1TallyV2/`.

## Target statement (SCORECARD.md:2812-2814)
"Scores of the wave-1 tools under v2: `verification/w1v2/` — 10 of 141 meet: `terminal_pct`, `v1_shape`, `strip`, `delimiter_proxy` and `m07_query_hash` now fail."

## Check 1 — count of `verification/w1v2/*.json`
- `find .ufo/waves/round-41/verification/w1v2 -maxdepth 1 -name '*.json' | wc -l` → **141**, exit 0.
- Tally script (sandbox `tally.py`, `python3 tally.py`, exit 0): **met=true: 10, met=false: 131, other: 0**. The 10 files with `passed=1434` are exactly the 10 with `met=true`.
- Integrity: all 141 receipts have `counterSha256` equal to the sha256 of the current `.ufo/waves/round-41/c1_count_v2.py`, `cases=1434`, and `oracleSha256=cdcac127…0917` (the value pinned in the counter). Zero mismatches.
- **Statement "10 of 141 meet": HOLDS.**

## Check 2 — the five named tools fail
Stored receipts (all `met=false`, `note=null`, i.e. judged, not errored):
- `verification/w1v2/CtlNoPct__terminal_pct.json` — passed 1433/1434 (sitemapUrl 803/804)
- `verification/w1v2/CtlGeneratorShape__v1_shape.json` — passed 1365/1434 (loc 601/630)
- `verification/w1v2/MutPlacement__strip.json` — passed 1429/1434 (sitemapUrl 799/804)
- `verification/w1v2/CtlConstantFamily__delimiter_proxy.json` — passed 1414/1434 (loc 619/630)
- `verification/w1v2/MutStructure__m07_query_hash.json` — passed 1433/1434 (sitemapUrl 803/804)

### Re-score: counter v2, two fresh seeds per tool (10 runs, all from lane root)
Command form: `prlimit --as=4000000000 timeout 900 python3 -B .ufo/waves/round-41/c1_count_v2.py --root . --tool-file .ufo/waves/round-41/controls/w1/<fam>/<tool>.py --label w2-<tool>-s<seed> --seed <seed> --out <sandbox receipt>`

| tool | seed | passed/cases | loc | sitemapUrl | met | exit |
|---|---|---|---|---|---|---|
| CtlNoPct/terminal_pct | 412701 | 1431/1434 | 628/630 | 803/804 | false | 1 |
| CtlNoPct/terminal_pct | 412702 | 1430/1434 | 628/630 | 802/804 | false | 1 |
| CtlGeneratorShape/v1_shape | 413701 | 1352/1434 | 583/630 | 769/804 | false | 1 |
| CtlGeneratorShape/v1_shape | 413702 | 1363/1434 | 594/630 | 769/804 | false | 1 |
| MutPlacement/strip | 414701 | 1428/1434 | 630/630 | 798/804 | false | 1 |
| MutPlacement/strip | 414702 | 1430/1434 | 630/630 | 800/804 | false | 1 |
| CtlConstantFamily/delimiter_proxy | 415701 | 1419/1434 | 621/630 | 798/804 | false | 1 |
| CtlConstantFamily/delimiter_proxy | 415702 | 1421/1434 | 626/630 | 795/804 | false | 1 |
| MutStructure/m07_query_hash | 416701 | 1433/1434 | 630/630 | 803/804 | false | 1 |
| MutStructure/m07_query_hash | 416702 | 1432/1434 | 629/630 | 803/804 | false | 1 |

All 10 runs: exit 1 (= "not met"), `met=false`, `note=null` (no timeout, no bwrap error, no cannot-evaluate). Each run ~2 s wall. Fresh-seed failure rates track the stored receipts (e.g. v1_shape 1352–1365, delimiter_proxy 1414–1421, m07 1432–1433): the failures are systematic, not seed luck.
- **Statement "`terminal_pct`, `v1_shape`, `strip`, `delimiter_proxy`, `m07_query_hash` fail (under v2): HOLDS.**

## Findings
1. **[low] SCORECARD.md:2813-2815** — the enumeration of the 10 still-meeting tools ("the two allow-list-plus-delimiter tools, `V3_decode_probe`, the two length-gated mutants and the equivalent mutants") accounts for 9; the 10th is `CtlNoUserinfoPort__no-port-v2.json` (met=true, a control-class receipt), which the description does not clearly cover. Count (10 of 141) is correct; the descriptive roster is incomplete. Outside my assigned statement; flagging as information for the next round.
2. No severity ≥ medium found in scope.

## Per-statement verdicts
- "under counter v2, 10 of 141 meet" — **holds** (141 receipts, 10 met / 131 not met, integrity-clean).
- "`terminal_pct`, `v1_shape`, `strip`, `delimiter_proxy`, `m07_query_hash` fail" — **holds** (stored receipts met=false and 10/10 fresh-seed re-scores fail, exit 1, no errors).

## Residual risk / verification gaps
- Receipt provenance is supported only by embedded `counterSha256`/`oracleSha256`/`cases` plus internal consistency (passed histogram ↔ met flags); I did not re-run the other 136 receipts. The five assigned tools were re-executed directly and behave as recorded.
- Fresh seeds are explicit (412701/412702, 413701/413702, 414701/414702, 415701/415702, 416701/416702); I cannot prove no earlier run used them, only that they are unused by the stored wave-1 receipts (whose seeds are 13–15-digit values) and my own batch.
- Not checked (out of scope for this seat): `verification/pre/v2-*.json` build/reference scores, selftest, realrun byte-equality.
