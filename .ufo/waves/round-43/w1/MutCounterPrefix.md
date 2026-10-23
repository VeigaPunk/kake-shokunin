KILLED — all four one-member weakenings of the round-43 shared-prefix class still reject the 32-prefix table control (9/11 to 10/11 equal, met false). No survivor, so no survivor witness; the item's expectation that the control MEETS every weakening is wrong.

Axes: operability measured; freshness not exercised. Leaf mutation probe only; no lane source changed, no round verdict.
Control: 32-code-point result table (first value seen with a prefix answers every later one). Two independent builds, both FAIL unweakened v4 with timing inside limit:
- D/ctl_build42_p32.py sha256 06ad5a7e5c99ff215ddf3a81e966c78aa7323c7729015bbf12b5feec989b3705 (`build42.py` sha256 914ebdee7bcb… plus `_parse_url` memo on `value[:32]`, sha check by diff); receipts base_v4.json (seed 218330596634026, 7/11, unequal A,D,F,T3), s_v4.json (seed 430043, 8/11, F,T2,T3), ratios ≤1.412.
- D/frozen v2_prefix32.py sha256 eadf5df4b5c26059429a5dbffd2d87bcdbca6f460ba982c81360736e6856aa0f (the L1 control, `.ufo/waves/round-43/controls-r42/v2_prefix32.py`); s_freeze_v4.json seed 430043, 8/11, F,T2,T3, ratios ≤1.451; freeze receipt 7/11 at seed 202843337434829 (SCORECARD.md:3227).
- A third, round-41-based control was built first and discarded: it fails only on cost (T1 4.559, T5 9.847 vs round-40), the same timing-only rejection as the freeze's ref41-base — so its equality evidence is inconclusive, not used.
Expected detector: a counter that keeps the count refuses the control (not met). Observed: every mutant refuses.
Command (each, exit 1 = not met): `timeout 900 prlimit --as=8000000000 -- python3 -B <counter> --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <control> --label <label> [--seed 430043] --out D/<receipt>.json`. All 18 scored counter invocations exited 1 (18 receipts, every met=false); sanity invocations of ref41/build42/control on a cut-40 pair exited 1/1/0.
D = /fast/scratch/hyaku/kake-r43/MutCounterPrefix. Frozen counter bytes untouched (sha256 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab); PREDICATE AST-equal in all four mutants.
| Mutant | sha256 | One-member change | Receipts (control, seed, equalRuns, unequal runs, met) | Verdict |
|---|---|---|---|---|
| D/m16.py | f1dced1a4abefa02873076020a7cb9349934218698ee2ed6e77fc5092d7e0708 | `c43_count_v4.py:450` `cut = rng.randint(36, 44)` -> `cut = 16` | ctl_build42_p32 seed 142054259508706 10/11 F; seed 430043 9/11 F,T2; frozen control seed 430043 9/11 F,T2; all met false | KILLED |
| D/m24.py | 2a9760055ac0292ae18923adc702ba28eb47e922a88c3064168aaf119d6f63ed | same line -> `cut = 24` | ctl_build42_p32 seed 51478373704840 9/11 F,T2; seed 430043 9/11 F,T2; frozen control seed 430043 9/11 F,T2; met false | KILLED |
| D/mfdrop.py | aea0289f51e958a4749f66dae07d760e56c70419d93deb62ce1779566098e4f2 | `:471-473` standalone F prefixpair loop deleted; `:477` pairfile `a3,b3 = prefix_pair` -> `fold_pair` | seed 107858610368298 8/11 F,T2,T3; seed 430043 8/11 F,T2,T3; frozen control 8/11 F,T2,T3; met false | KILLED |
| D/mt3drop.py | eb793f1bab01a2655370be68ad3a389d5f9f7026cf909b15c5e73176db1f64ce | `:795-798` T3 prefix-pair branch deleted (rolls fall through to long_value) | seed 199741923724591 9/11 F,T2; seed 430043 9/11 F,T2; frozen control 9/11 F,T2; met false | KILLED |
Witnesses (why no survivor): cut 16/24 removes the intended collision (0/200 generated pairs share `value[:32]`; v4: 200/200), and T3 falls equal for both (s_m16, s_m24), so the named class loses its T3 catch — yet rejection survives on
- F: `layout_f` (c43_count_v4.py:543-556) gives each pair a sitemapUrl sharing the value's host and first path segment, so a 32-prefix table reuses the sitemapUrl parse for the loc. Traced with `D/dbg_ctl.py` (scan cache + collision log) on an m16 F run: 17 of 1,220 checks differ; example key `hTTps://t6v~+aCs.example:012214/`, cached path `/sitemap.xml`, fresh `/uor2h`. mfdrop has no prefixpair in F at all and F is still unequal, so this catch is independent of the mutated member.
- T2: seed-dependent (unequal at 430043/51478373704840, equal at 142054259508706), and cut-40 sanity pair shows the class itself: bad `https://a.com/x*30%`, good `https://a.com/x*30abc`; control returns exit 0 and drops `loc_not_absolute` where ref41 exits 1.
Per checked statement:
- "PREDICATE byte-identical in every version" — holds (AST compare, all four).
- "32-prefix table control FAILS unweakened v4" — holds (7/11 and 8/11, the failure is equality, not cost).
- "Control must MEET every weakening" — wrong: 4/4 mutants stay not met; the class is load-bearing only through T3's guaranteed ≥36>32 collision, and v4 has two other catch channels.
- SCORECARD.md:3227 "v2_prefix32 by E, F, T2, T3 (7/11)" — overstated as a per-run claim: at a different seed my equivalent control is caught by A,D,F,T3; the run set moves with the seed, only the not-met verdict was stable in the four baseline scorings.
No tool installs or upgrades. Scratch bounded (<1 MB); no background processes left.
