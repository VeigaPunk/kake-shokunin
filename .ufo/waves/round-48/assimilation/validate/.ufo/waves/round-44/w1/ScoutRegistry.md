# ScoutRegistry — controls-27.tsv verification

Axes checked: hash fidelity, path existence, round-43 seat-report presence, family/class arithmetic, byte identity against round-43 `l1-rescores` `toolSha256` where a receipt exists.

Verdict: **no row defect**. 27/27 sha256 match, 27/27 paths exist, 27/27 seat reports exist, family and class tallies each sum to 27. The candidate formula `5+3+4+5+3+2+1+4=27` is **not** this registry’s decomposition (the sum is 27, the grouping is not). Where an l1-rescore receipt exists (14/27), its `toolSha256` equals the file and column 5. The other 13 rows have no receipt in that directory; that is an evidence gap, not a byte mismatch.

No tools installed. Scratch dir created empty: `/fast/scratch/hyaku/kake-r44/ScoutRegistry/`. Only file written: this report.

## Commands

Working directory for `sha256sum`: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/controls-r43`.

```
sha256sum <the 27 control basenames listed in the TSV, in TSV order>
```

Independent cross-check (stdlib `hashlib.sha256` of each repo-relative path, `os.path.isfile` of `.ufo/waves/round-43/` + column 6, JSON `toolSha256` from every `l1-rescores/*.json`):

```
python3 -  # script body not saved; stdout reproduced below under Cross-check
```

Seat-file sizes (same ten distinct column-6 names):

```
python3 -c existence probe of the 10 distinct w1/*.md paths
```

## sha256sum (verbatim, 27 lines)

```
752a8de5baba3d14f8edb8e77052c0f8dd164f814c4c74c2922283abda5d7df6  portlen-v1-skip-grammar-6plus.py
e55e3bfb9a6e9f3523a9c1393e14a2defdadd2ae7c2b4104e12cd717a51e76f5  portlen-v5-abbrev-window-6plus.py
0fc6091351c1e080b90df1f96ef2558d9f5ada2dce473109d0fe805d07fe5889  buildscheme-M5-default-port-https80.py
870ba78489282ef8966c90e1ea87ce304b507715c10959a833393917dda89f4d  buildscope-m5-empty-path.py
272d02127daa0b6f35d29957b3ebb16a91a10ab01a73f3a10a3c28814de5412e  buildscope-m4-port-dropped.py
00ece64886137a23b1b6a8e7f7795885d2e23ae3c1c2a0dfdb8f05f085503238  headtail-V1-prefix-cache64.py
012527ff78763caf8e20bc244cf5c7d899436e026c06fb4e9e43809f700c10bf  headtail-V2-headtail-key48.py
56eda048b6bfcc4d569e23ddf4bf02261c960ceff110971357e0a93d52f615ea  headtail-V7-prefix-cache45.py
4e5064fccdac11262107d2005a6c88923a621e64b9d3c37787f7f78e66d2234b  prefixcache-p48-noreval.py
bec3fd0cc443ca914a14a0b450737ef8e1e9539691f929f66a913db776969df3  casememo-v3-validity-lower.py
5c9158fb9ca98b783768fda314fbba1ae481f04ef0e0017964a4d07ae9992063  casememo-v4-validity-lower-short.py
d41f0f1b06315604b03eb44e1b0a4609ac7340d8a566d9e6216a5f6fd52659f8  casememo-v7-value-lower-nonascii.py
29070eed5a2c54ffe1619973057a2383d4e671c4235a408af7db66f5016126fa  casememo-v8-value-casefold-nonascii.py
c3a8770e5d76a8a7e218f56a2e9776fa03746770745d78a00f65dd6382df83ec  repeat-ctl_len_memo_band.py
abf4984abb2b5fdd5e006b0d5b113ad1e9362362ec763724002254757416faf4  repeat-ctl_depth_memo_band.py
b9c7eda690cf0566c8a6f37e1b1472a16324bbfe86213a9556c68b5264c55c0e  repeat-ctl_defpos_memo_band.py
7eb373f22afee62fc5aa605c7216be37065283e9a0d7739dcbbc909dc463a9bc  repeat-ctl_depth_memo_deep.py
9d49f8c8dca8ddd7c78250a9b5c8de38a64431396736cb7cab87112376e72304  repeat-ctl_defpos_memo_late.py
25e84d0d56f7acaef33f331f73e6c0ff21ac2466e31ae786fc4a26114b3087a9  hosttable-A-expanded46-fixed.py
f852dff164f7dd94a13c43c38906457c5e9724af391a7079f5673263420ac4d7  hosttable-B-expanded46-nogrammar.py
ac3f0009fd2d1894c6bda1a15e16fab1d035aaee5f2c5a0fd87a0d40df3799bf  hosttable-F-provable.py
d09ad5fec5c9493f3c206ab1b1a33acf5e6ece344fe0e988a99bfa8749dab00d  portvalue-memo-digits.py
ed50b5742d3a2409f5b9e06bca28e2f9a8aeb8b533a0f123d70e63a072ddfd86  portvalue-memo-digits-67.py
1b34f83d4b45346dd22628064ffb5cda451ea9922b1168933b781648262df58b  portlen-v4-cache-portlen.py
68f3750025531d7815d6ec665432536abc3b0c78a036fdb49339e1f73bcbe87e  buildport-m6-default-branch.py
52fb29a7f74b5898d3eaf82933f0d530ea2d09862c46511b6ed5ded5faeee7c6  headtail-V4-longport-head64.py
35be7a24eae3d242710c95ffebddc2159793d6a0fae6ae37c08121af267cc07a  headtail-V8-longport-tail64.py
```

Each digest equals column 5 of the same row. `sha256sum` exiting with 27 lines also shows every path exists. Directory `controls-r43/` contains exactly these 27 files (no extra, no missing).

## 27-row table

Seat path checked as `.ufo/waves/round-43/` + column 6 (all ten distinct files are regular files).

| name | sha match | seat report | class |
|---|---|---|---|
| portlen-v1 | yes | yes (`w1/CtlPortLen.md`) | G1 |
| portlen-v5 | yes | yes (`w1/CtlPortLen.md`) | G1 |
| buildscheme-M5 | yes | yes (`w1/MutBuildScheme.md`) | G2 |
| buildscope-m5 | yes | yes (`w1/MutBuildScope.md`) | G3 |
| buildscope-m4 | yes | yes (`w1/MutBuildScope.md`) | G4 |
| headtail-V1 | yes | yes (`w1/CtlHeadTail.md`) | G5 |
| headtail-V2 | yes | yes (`w1/CtlHeadTail.md`) | G5 |
| headtail-V7 | yes | yes (`w1/CtlHeadTail.md`) | G5 |
| prefixcache-p48 | yes | yes (`w1/CtlPrefixCache.md`) | G5 |
| casememo-v3 | yes | yes (`w1/CtlCaseMemo.md`) | G6 |
| casememo-v4 | yes | yes (`w1/CtlCaseMemo.md`) | G6 |
| casememo-v7 | yes | yes (`w1/CtlCaseMemo.md`) | G6 |
| casememo-v8 | yes | yes (`w1/CtlCaseMemo.md`) | G6 |
| repeat-len-band | yes | yes (`w1/CtlRepeat.md`) | G7 |
| repeat-depth-band | yes | yes (`w1/CtlRepeat.md`) | G7 |
| repeat-defpos-band | yes | yes (`w1/CtlRepeat.md`) | G7 |
| repeat-depth-deep | yes | yes (`w1/CtlRepeat.md`) | G7 |
| repeat-defpos-late | yes | yes (`w1/CtlRepeat.md`) | G7 |
| hosttable-A | yes | yes (`w1/CtlHostTable.md`) | G8 |
| hosttable-B | yes | yes (`w1/CtlHostTable.md`) | G8 |
| hosttable-F | yes | yes (`w1/CtlHostTable.md`) | G8 |
| portvalue-digits | yes | yes (`w1/CtlPortValue.md`) | G9 |
| portvalue-digits-67 | yes | yes (`w1/CtlPortValue.md`) | G9 |
| portlen-v4 | yes | yes (`w1/CtlPortLen.md`) | G9 |
| buildport-m6 | yes | yes (`w1/MutBuildPort.md`) | G9 |
| headtail-V4 | yes | yes (`w1/CtlHeadTail.md`) | G10 |
| headtail-V8 | yes | yes (`w1/CtlHeadTail.md`) | G10 |

Seat-file probe (verbatim):

```
YES 10292 w1/CtlPortLen.md
YES 5120 w1/MutBuildScheme.md
YES 4364 w1/MutBuildScope.md
YES 6090 w1/CtlHeadTail.md
YES 5729 w1/CtlPrefixCache.md
YES 6411 w1/CtlCaseMemo.md
YES 9355 w1/CtlRepeat.md
YES 6027 w1/CtlHostTable.md
YES 6139 w1/CtlPortValue.md
YES 4643 w1/MutBuildPort.md
```

27 unique names, 27 unique sha256, 27 unique paths. Header is the comment line `# name	family	class	...` and is not a data row.

## Family and class arithmetic

Family and class are 1:1 on this TSV (each family is exactly one class). Ten families, ten classes, both sums 27.

Class order:

`G1:2 + G2:1 + G3:1 + G4:1 + G5:4 + G6:4 + G7:5 + G8:3 + G9:4 + G10:2 = 27`

Family order (same counts):

`portlen:2 + default_port:1 + empty_path:1 + port_scope:1 + prefix:4 + fold:4 + band:5 + host:3 + portdigit:4 + window:2 = 27`

By descending count:

`band 5 + fold 4 + portdigit 4 + prefix 4 + host 3 + portlen 2 + window 2 + default_port 1 + empty_path 1 + port_scope 1 = 27`

The candidate `5+3+4+5+3+2+1+4` is eight terms and does not equal either tally. Not recorded as a row defect: the TSV does not state that formula.

## Round-43 l1-rescore byte check

Directory: `.ufo/waves/round-43/verification/l1-rescores/`. 14 JSON receipts. Each `toolSha256` equals both the on-disk file and column 5 of exactly one row. Zero receipts point at a different row. Zero receipts disagree with the file.

| receipt | row | match |
|---|---|---|
| `CtlHeadTail-V1c.json` | headtail-V1 | yes (`00ece648…`) |
| `CtlHeadTail-V2b.json` | headtail-V2 | yes (`012527ff…`) |
| `CtlHeadTail-V4b.json` | headtail-V4 | yes (`52fb29a7…`) |
| `CtlHeadTail-V7c.json` | headtail-V7 | yes (`56eda048…`) |
| `CtlHostTable-A_expanded46_fixed.json` | hosttable-A | yes (`25e84d0d…`) |
| `CtlHostTable-B_expanded46_nogrammar.json` | hosttable-B | yes (`f852dff1…`) |
| `CtlHostTable-F_provable_hosttable.json` | hosttable-F | yes (`ac3f0009…`) |
| `p48_noreval.json` | prefixcache-p48 | yes (`4e5064fc…`) |
| `v3_memo_validity_lower.json` | casememo-v3 | yes (`bec3fd0c…`) |
| `v4_memo_validity_lower_short.json` | casememo-v4 | yes (`5c9158fb…`) |
| `v7_memo_value_lower_nonascii.json` | casememo-v7 | yes (`d41f0f1b…`) |
| `v8_memo_value_casefold_nonascii.json` | casememo-v8 | yes (`29070eed…`) |
| `v4_cache_portlen_with_path.json` | portlen-v4 | yes (`1b34f83d…`) |
| `v5_abbrev_window_6plus.json` | portlen-v5 | yes (`e55e3bfb…`) |

No `l1-rescores/*.json` for these 13 rows (comparison not possible from that directory; not a mismatch):

`portlen-v1`, `buildscheme-M5`, `buildscope-m5`, `buildscope-m4`, `repeat-len-band`, `repeat-depth-band`, `repeat-defpos-band`, `repeat-depth-deep`, `repeat-defpos-late`, `portvalue-digits`, `portvalue-digits-67`, `buildport-m6`, `headtail-V8`.

## Cross-check stdout (decisive lines)

```
data_rows 27
unique_names 27
unique_sha 27
unique_paths 27
disk_files 27
extra_on_disk []
missing_on_disk []
family_sum 27 n_families 10
family_terms 5+4+4+4+3+2+2+1+1+1
class_sum 27 n_classes 10
MISMATCHES 0
---RECEIPTS 14
---ROWS_WITH_RECEIPT 14
byte_mismatch_count 0
```

(`family_terms` is band, fold, portdigit, prefix, host, portlen, window, default_port, empty_path, port_scope.)

## Blockers

None.
