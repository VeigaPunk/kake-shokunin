# CtlIdKeyed — round-41 wave-1 control: answers keyed on check ids, file names, entry positions

No tool of this class reaches 1434/1434. Best keyed control 1043 (IdHash10Reject, seed 424241) against base 1049; no keyed rule beat base on 3 seeds, and the class cannot: `c1_count.py:191-205` draws ids and file names from the same rng *after* the values, so no key carries a validity bit. 34 counter receipts, one per scored run.

## Built
15 stdlib-only tools at `/fast/scratch/hyaku/kake-r41w1/CtlIdKeyed/<name>.py`, each `base.py` plus a late overlay that rebinds `_parse_url` (mode `reject` = base judgment plus a keyed reject; mode `replace` = the key alone). Builder `build.py`/`mk_const.py`; probes `stats.py`/`summarize.py`. Receipts `<name>-s<seed>.json` beside them.

## Scored, seed 424241 (`--tool-file <tool> --seed 424241`)
| tool | sha256 | passed | loc / sitemapUrl | fragment/host/path/port/query/userinfo | met | work skipped; cases that caught it |
|---|---|---|---|---|---|---|
| IdHash10Reject | 7f3890f7b054a4116d93f0ef724a79b1b9b21200d3e9cb9da8f314efb9a4396f | 1043 | 510/630 · 533/804 | 156/165/164/238/155/165 | false | per-value judgment for 10% of checks by id hash; caught on sitemapUrl (271 missed) and 16 valid values wrongly rejected |
| IdVowelReject | 0771a2bd3b72820c56c0923dbc1f26e99e84fb5ca8b73589ceb827523247c717 | 1004 | 484/630 · 520/804 | 152/165/153/217/150/167 | false | reject checks whose id starts with a vowel; 35 shown misses are valid values, port 217/239 |
| IdHash3Reject | 90214774c6b98bf1fa9618c7419bda5a84414750e9eb0d6020ea139f136bfd24 | 961 | 484/630 · 477/804 | 146/153/145/212/144/161 | false | reject 1/3 of checks by id hash; 62 shown misses are valid values |
| IdDigitReject | 9cc6d69880d8cbefe764695451665d1b45e605209d33b60a8d3a81f56d66c269 | 948 | 466/630 · 482/804 | 144/164/145/198/146/151 | false | reject when the id ends in a digit; 53 shown misses valid |
| IdLenReject | 12947fb61ddae74f226cd7538d5650a4d3c8a6a135e7deea526459fe9ded8b64 | 931 | 443/630 · 488/804 | 142/154/149/178/149/159 | false | reject when id length is 7/9/11; 69 shown misses valid |
| FileLenKeyed | cbd23827275c6ca0b2bcd4d4eda47f470a43f3f9e122ac232544faf562d08088 | 915 | 510/630 · 405/804 | 138/145/134/225/136/137 | false | reject when the file name is odd-length; on the shared sitemapUrl file it fires once for all 804 checks (405 = all-invalid), on loc groups per file; 154 shown misses valid |
| AllInvalid | 5f72707186945739c893f4581caa456ff1692e8fda1b3d7c965baf055c1c957b | 804 | 399/630 · 405/804 | 135/139/131/134/133/132 | false | check-level constant reject; caught because a `check_invalid` loc check is scored "valid" for every entry (399 loc points are the valid half) |
| AllValid | e6d1db5f8b5b566951526fadb2b5b11d3be1a9923cc205d7c2f5850368bc7449 | 798 | 399/630 · 399/804 | 147/157/159/26/151/158 | false | constant clean; caught by all 636 invalid values (port 26/239) |
| IdCoinReplace | 3bfc50a9bb7c1abffc5ecf9d79d7e8e390914b1b28d07eb2eb2c76eef607302f | 810 | 399/630 · 411/804 | 143/145/135/95/144/148 | false | no URL judgment at all (sha256(id) parity); caught by port 95/239 — base's `parts.port` strictness discarded |
| FileHexBitReject | 5a859c69269f966a26feff3126b18b4e1c2c7d04a743475d5650ef8b55e7c783 | 784 | 379/630 · 405/804 | 127/125/116/185/113/118 | false | per-entry reject from a bit of the file name's hex; 154 shown misses valid |
| PosParityReplace | bc250c99917727a1f41a7414f516cf5c14bedd667275dabedd8be2a37a0ac34f | 763 | 358/630 · 405/804 | 128/132/141/92/141/129 | false | per-entry answer from (entry+ordinal) parity; port 92/239 |
| FileCoinEntryReplace | 69d30221c46803bfe4d95405c4bdf43480ed1dae558bb6ad45fd6d2496813f9b | 749 | 344/630 · 405/804 | 125/127/108/155/119/115 | false | per-entry coin from file name + entry; 156 shown misses valid |
| IdCoinEntryReplace | b70b1c3254c590037a0ef854a810024cd4276181a3dbef91072e23cf759770a4 | 746 | 353/630 · 393/804 | 127/129/136/75/137/142 | false | per-entry coin from id + entry; port 75/239 |
| AllFindings | 3abf3c13d5f08c9f6965ef878d4a88e1f9488e7eafdc5f13225b57ee0afadade | 636 | 231/630 · 405/804 | 92/82/80/213/88/81 | false | constant findings on every entry/check; passed equals oracleInvalid exactly; caught by all 798 valid values |
| base (do nothing) | 4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e | 1049 | 510/630 · 539/804 | 153/169/165/238/157/167 | false | no RFC 3986 judgment; 385 invalid values accepted |
| ref_fix (reference) | 6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a | 1434 | 630/630 · 804/804 | 239 each | **true** | full grammar; exit 0 |

Command per row: `timeout 900 python3 -B .ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <tool> --label CtlIdKeyed-<name>-s424241 --seed 424241 --out <receipt>`; ref exit 0, every control exit 1, none exit 2; no tool output was unreadable (`note` null everywhere).

## Three-seed repeat (all exit 1)
| tool | 424241 | 777001 | 990011 | comment |
|---|---|---|---|---|
| base | 1049 | 1061 | 1042 | 385/373/392 invalid values accepted, 0 valid rejected each seed |
| IdHash10Reject | 1043 | 1054 | 1014 | best keyed tool; deltas −6/−7/−28 |
| FileLenKeyed | 915 | 1049 | 1032 | below base on all three (1049/1061/1042) |
| AllValid | 798 | 810 | 791 | equals the valid count each seed |
| AllFindings | 636 | 624 | 643 | equals the invalid count each seed |
| population | 798v/636i | 810v/624i | 791v/643i | 15/16/16 loc groups, 0 homogeneous; majority ceiling 1205/1213/1205 |

## Findings
- `.ufo/waves/round-41/c1_count.py:191-205` — `name()` is `"%x" % rng.getrandbits(64)`; `fresh_id()` is 6-12 lowercase alnum; both drawn after `generate`, independent of each case's `valid`. Measured consequence: no keyed rule beat or matched base; best delta −6 (IdHash10Reject 1043 vs 1049 at seed 424241).
- `.ufo/waves/round-41/c1_count.py:176-181` — the grid is fixed (one case per field×component×unit); base's reject counts are identical across seeds (111/231 loc, 140/405 sitemapUrl invalid), so the 385-case load is structural, not seed noise.
- `.ufo/waves/round-41/c1_count.py:188-241` — 804 sitemapUrl checks hold one case each; the 630 loc cases sit in 15-16 groups of 20-60 entries, every group mixed on all 3 seeds. Per-check-majority ceiling 1205/1213/1205 < 1434: the predicate cannot be met by any check-level constant, id-keyed or not.
- `.ufo/waves/round-41/c1_count.py:252-269` — a loc case counts invalid only via a `loc_not_absolute` naming its entry; a check answered `check_invalid` is read as "valid" for every entry in it (AllInvalid 804 vs AllFindings 636).
- `/fast/scratch/hyaku/kake-r41/shared/base.py:67-75` — base rejects leading controls and tab/CR/LF only; it accepts all 798 valid and 385 invalid values, so an id-keyed selector that flips a fraction p of accepts costs p·798 and gains p·385 (net −413p), matching IdHash10Reject's −6/−7/−28.
- The discriminating units, measured over the 385: C0 0x00-0x1F (sitemapUrl only; loc base catches tab/LF/CR), space, DEL, `" < > \ ^ ` { | }`, `[`/`]`, and stray/malformed `%` (`%`, `%2`, `%4G`, `%G4`, `%`+letter), plus a few single letters that break a preceding `%` triplet.

## Statements checked
- "the counter scores a tool that skips this work below 1434": **holds** — 15 tools, max 1043, 34 receipts.
- "answers keyed on check ids or file names can reach 1434": **wrong** — measured null on 3 seeds and explainable by draw order.
- "a per-check constant can reach 1434": **wrong** — 1205/1213/1205 ceiling; loc entries are mixed inside every group.

## Risks / limits
- Keyed tools have ±~20 seed noise; 3 seeds show none above base, but the L1 should re-score with fresh default seeds, not my pins.
- My class is 391 cases short at best; no risk of an accidental `met`, and no keyed tool should be read as a build.
- Counter power rests on the unit grid's character set; a character-class shortcut (out of this lane) is the class most likely to recover the 385.
- No blockers; no tool installs (Python 3.14.8, bubblewrap 0.13.1 already present). All processes were `timeout`-capped and have exited; no lane file, index or jj state touched.
