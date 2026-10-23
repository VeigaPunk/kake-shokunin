# CtlCharTable — component-blind ASCII table (r41 wave 1, operability)

No tool of this class reaches the target. Best: **1336/1434** (counter v2), **1320/1434** (counter
v1, mean 1303). It skips the component repertoires and percent-triplet syntax; the counter catches
that on 98-148 cases per run, so it does separate this control from the repair.
## Built (stdlib only, `/fast/scratch/hyaku/kake-r41w1/CtlCharTable/`)
`ctl_char_table.py` `45b28cc74ba7b6e9f851fc31819c364001ea22e622a5a293d7eddb844986d0c2` —
`shared/base.py` with its 2-line URL guard replaced by a 128-entry `_ASCII_VALID = bytes(...)`;
`_parse_url` rejects a value when any ASCII code point has a clear bit, then the unchanged `urlsplit`
parse runs (+21/-2). Code points >0x7F keep round-39 behaviour. Table = 85 allowed
(`! #.. / 0..9 : ; = ? @ A..Z [ ] _ a..z ~`); denied = 0x00-0x20, `"`, `<`, `>`, `\`, `^`, `` ` ``,
`{`, `|`, `}`, 0x7F. Skips: one bit for every component, no percent-triplet check.
Ablations `t_nobracket.py` `a8ce026b…` (83, drops `[ ]`), `t_printable.py` `5691d410…` (94, all
0x21-0x7E), `t_nopct.py` `a5e64064…` (84, drops `%`). No tool installed or upgraded; no lane file
touched (reads and read-only `git` only).
## Commands (`--root /home/vgpnk/Projects/shokunin/kake-shokunin`, each capped `timeout 300`)
    python3 -B .ufo/waves/round-41/c1_count.py    --tool-file ctl_char_table.py --label CtlCharTable-seed414141    --seed 414141 --out seed-v1.json  # exit 1
    python3 -B .ufo/waves/round-41/c1_count_v2.py --tool-file ctl_char_table.py --label CtlCharTable-v2-seed414141 --seed 414141 --out seed-v2.json  # exit 1
    same shape seedless: 10 v1 runs, 3 v2, 2 per ablation, ref_fix/base anchors; ref_fix exit 0, mine exit 1
## Receipts (`passed`; `byField` = loc/sitemapUrl; byComponent for the seeded pair; `met`)
| tool | v1 `c1_count.py` `2acc443a…` | v2 `c1_count_v2.py` `f5a39361…` |
|---|---|---|
| `ctl_char_table.py` 85 | 1286-1320, mean 1303 (n=10), met false; seed 414141 = **1301**, 564/630, 737/804, frag 212/239 host 217/239 path 212/239 port 239/239 query 210/239 ui 211/239 | 1333, 1333, 1336, met false; seed 414141 = **1307**, 568/630, 739/804, frag 208/239 host 218/239 path 212/239 port 239/239 query 211/239 ui 219/239 |
| `t_printable.py` 94 | 1207, 1210, met false | 1228, 1243, met false |
| `t_nobracket.py` 83 | 1269, 1271, met false | 1278, 1279, met false |
| `t_nopct.py` 84 | 771, 778, met false | not run |
| base.py anchor | 1043, 1048, met false | not run |
| ref_fix.py anchor | **1434, 1434, met true, exit 0** | **1434, met true, exit 0** |

Skipped work and who caught it — `ctl_char_table.py`: per-component repertoires plus percent-triplet
syntax; 101 misses on the v2 seedless run: percent triplets 48 (`%` 20, `%4G` 10, `%G4` 10, `%2` 7,
`%41` 1), inserts landing inside an existing `%XX` triplet 34 (`/cbs%9?D/`, `n8%jB`, `q7d1%KAc`),
`[` outside a host 12, `#` ending a fragment 5, `@` in userinfo 2. `t_printable.py`: also the nine
never-legal printables (`"<>\^`{|}`), 12 more per component. `t_nobracket.py`: the IPv6-literal
brackets, losing the ~120 bracket-bearing host values. `t_nopct.py`: `%`, so every percent-bearing
valid value is rejected (530 misses). Port is 239/239 in every run — `urlsplit` raises on a
non-numeric port (`base.py:67-88`), so the counter gives this control that component for free.
## Findings
`c1_count.py:118` (`i = rng.randint(1, len(text) - 1)`) is v1's interior-only insertion;
`c1_count_v2.py:1-8` records v1 was killed because a wave-1 control accepting a trailing `%` met it —
both counters are in the lane and this control fails both. `c1_count.py:37` `CASES = 1434` and the
630/804 split hold in all 16 receipts; `c1_count.py:252-266` reads only `loc_not_absolute` /
`check_invalid`, as described. The tuning surface is flat near the optimum: 85 -> 1303/1334; dropping
`[ ]` costs 32-34 (v1) / 55-56 (v2); the nine never-legal printables cost ~95; dropping `%` costs
530. `[ ]` must stay — the only non-base characters that pay, carrying the IPv6-literal host values.
Family ceiling ~1334/1434: ~82 of its ~100 misses are percent-triplet blindness (invisible to a
per-character table by construction), plus ~19 from `[`, `#`, `@` trade-offs.
## Statement checks
- "counter `c1_count.py` sha256 `2acc443a…`" — **holds** (`2acc443af334…`); "base tool scores 1049"
  — **holds** within seed noise (1043, 1048 here); "reference repair scores 1434" — **holds** (2/2
  v1, 1/1 v2, exit 0); "1434 cases, 630 loc + 804 sitemapUrl" — **holds** in every receipt.
- "a per-character table control cannot reach 1434" — **holds**: best 1336, 98-148 misses.
- "`c1_count.py` is the counter that scores this wave" — **overstated**: `c1_count_v2.py`
  (`f5a39361…`, same 1434/630/804 shape) sits beside it with a v1-kill note, and my tool scores 1303
  (v1) vs 1334 (v2); the wave should name the binding counter before freezing the claim.
## Risks
`[ ]` is a deliberate bet (+55 on v2): every bracket injected outside a host is a miss. Non-ASCII is
untouched (round-39 `urlsplit` behaviour) and untested — the counter generates none. Seed noise ±15
on v1, ±5 on v2, so single receipts must not be read as the mean.
