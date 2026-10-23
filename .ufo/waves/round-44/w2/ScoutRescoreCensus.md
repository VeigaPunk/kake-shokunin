# ScoutRescoreCensus — rescore-tally derive

Axes: freshness (this item), operability (local git/python only; no network, no installs).

Verdict: **PASS.** The named attack does not land. Independent distinct toolSha256 count is **14**. scripts/ledger_latest_check.py derive for rescore-tally is **14**. They are equal. Total top-level *.json files under the receipt directory is **14** (one hash each; no missing or duplicate toolSha256).

The SCORECARD quote is still 18 (SCORECARD.md:3393). That quote/derive mismatch is what the checker prints; it is not a census disagreement. Both this seat and the checker read the same 14 committed receipts.

No tools installed. Scratch dir created empty: /fast/scratch/hyaku/kake-r44/ScoutRescoreCensus/. Only file written: this report.

Master (also HEAD): 18cb2c28f47c3ec3732ffa06c456e61b3444b1a2. Working tree at run time: SCORECARD.md modified, scripts/ledger_latest_check.py untracked. Receipts were read with git show master:PATH, not the worktree.

## Commands

Working directory: /home/vgpnk/Projects/shokunin/kake-shokunin.

```
git ls-tree --name-only master .ufo/waves/round-43/verification/l1-rescores/
git rev-parse master
python3 -  # stdlib json + subprocess git show master:PATH; script not saved
python3 -B scripts/ledger_latest_check.py --root .
git ls-tree -r --name-only master .ufo/waves/round-43/verification/l1-rescores/ | wc -l
diff of non-recursive vs -r name lists
```

## ls-tree (verbatim, 30 lines)

```
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V1c.json
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V1c.log
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V2b.json
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V2b.log
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V4b.json
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V4b.log
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V7c.json
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V7c.log
.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-A_expanded46_fixed.json
.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-A_expanded46_fixed.log
.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-B_expanded46_nogrammar.json
.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-B_expanded46_nogrammar.log
.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-F_provable_hosttable.json
.ufo/waves/round-43/verification/l1-rescores/CtlHostTable-F_provable_hosttable.log
.ufo/waves/round-43/verification/l1-rescores/exits.txt
.ufo/waves/round-43/verification/l1-rescores/exits2.txt
.ufo/waves/round-43/verification/l1-rescores/p48_noreval.json
.ufo/waves/round-43/verification/l1-rescores/p48_noreval.log
.ufo/waves/round-43/verification/l1-rescores/v3_memo_validity_lower.json
.ufo/waves/round-43/verification/l1-rescores/v3_memo_validity_lower.log
.ufo/waves/round-43/verification/l1-rescores/v4_cache_portlen_with_path.json
.ufo/waves/round-43/verification/l1-rescores/v4_cache_portlen_with_path.log
.ufo/waves/round-43/verification/l1-rescores/v4_memo_validity_lower_short.json
.ufo/waves/round-43/verification/l1-rescores/v4_memo_validity_lower_short.log
.ufo/waves/round-43/verification/l1-rescores/v5_abbrev_window_6plus.json
.ufo/waves/round-43/verification/l1-rescores/v5_abbrev_window_6plus.log
.ufo/waves/round-43/verification/l1-rescores/v7_memo_value_lower_nonascii.json
.ufo/waves/round-43/verification/l1-rescores/v7_memo_value_lower_nonascii.log
.ufo/waves/round-43/verification/l1-rescores/v8_memo_value_casefold_nonascii.json
.ufo/waves/round-43/verification/l1-rescores/v8_memo_value_casefold_nonascii.log
```

Non-recursive and ls-tree -r name lists are identical (30 lines, diff empty, trees-identical). No nested JSON. Checker filter (parent equals l1-rescores and suffix .json in rescore_receipts) therefore sees the same 14 files.

## toolSha256 census (verbatim)

```
ls-tree lines=30 top_json=14
CtlHeadTail-V1c.json	'00ece64886137a23b1b6a8e7f7795885d2e23ae3c1c2a0dfdb8f05f085503238'
CtlHeadTail-V2b.json	'012527ff78763caf8e20bc244cf5c7d899436e026c06fb4e9e43809f700c10bf'
CtlHeadTail-V4b.json	'52fb29a7f74b5898d3eaf82933f0d530ea2d09862c46511b6ed5ded5faeee7c6'
CtlHeadTail-V7c.json	'56eda048b6bfcc4d569e23ddf4bf02261c960ceff110971357e0a93d52f615ea'
CtlHostTable-A_expanded46_fixed.json	'25e84d0d56f7acaef33f331f73e6c0ff21ac2466e31ae786fc4a26114b3087a9'
CtlHostTable-B_expanded46_nogrammar.json	'f852dff164f7dd94a13c43c38906457c5e9724af391a7079f5673263420ac4d7'
CtlHostTable-F_provable_hosttable.json	'ac3f0009fd2d1894c6bda1a15e16fab1d035aaee5f2c5a0fd87a0d40df3799bf'
p48_noreval.json	'4e5064fccdac11262107d2005a6c88923a621e64b9d3c37787f7f78e66d2234b'
v3_memo_validity_lower.json	'bec3fd0cc443ca914a14a0b450737ef8e1e9539691f929f66a913db776969df3'
v4_cache_portlen_with_path.json	'1b34f83d4b45346dd22628064ffb5cda451ea9922b1168933b781648262df58b'
v4_memo_validity_lower_short.json	'5c9158fb9ca98b783768fda314fbba1ae481f04ef0e0017964a4d07ae9992063'
v5_abbrev_window_6plus.json	'e55e3bfb9a6e9f3523a9c1393e14a2defdadd2ae7c2b4104e12cd717a51e76f5'
v7_memo_value_lower_nonascii.json	'd41f0f1b06315604b03eb44e1b0a4609ac7340d8a566d9e6216a5f6fd52659f8'
v8_memo_value_casefold_nonascii.json	'29070eed5a2c54ffe1619973057a2383d4e671c4235a408af7db66f5016126fa'
---
total_top_json 14
distinct_including_none 14
distinct_non_none 14
```

Each value is a non-empty string on a JSON object. Each hash appears once.

## Checker (verbatim)

```
rescore-tally MISMATCH quoted=18 derived=14 SCORECARD.md:3393
donothing-ratios MISMATCH quoted=T1 4.27, T5 8.68 derived=T1 4.21, T5 7.05 LOG.md:1661
build-ratio-range MISMATCH quoted=T1 1.00-1.02, T5 1.13-1.18 derived=T1 1.00-1.01, T5 1.11-1.22 LOG.md:1660
ledger-quotes: 3 figures, 3 mismatches
EXIT:1
```

Note: the live build-ratio-range line used an en dash (U+2013) between range endpoints. The line above uses an ASCII hyphen. The decisive rescore-tally line is byte-identical to the run: rescore-tally MISMATCH quoted=18 derived=14 SCORECARD.md:3393.

Derive kind in ledger_latest_check.py derive_values: distinct-tool-sha256 adds each non-empty string toolSha256 to a set and returns len(hashes). That length is 14, matching the independent set.

SCORECARD pattern (re-scored, digits, of the 27) matches once, line 3393, group 18.

## Numbers

| quantity | value |
|---|---|
| top-level json files | 14 |
| distinct toolSha256 | 14 |
| checker derive | 14 |
| SCORECARD quote | 18 |

## Blockers

None.