NOT MET — C1: three live-seat controls of the frozen "keyed fast path" class (expanded static host tables, answered without the URI check) MEET counter v4 with 11/11 equal runs and all five timing ratios ≤ 1.50, while judging values differently from the round-41 tool (differential + CLI witnesses below). Frozen kill rule (1) — "any live-seat control receipt meeting v4 means C1 is NOT MET" — therefore fires; reported, not relabelled.

## What the counter misses (mechanism)
Counter v4's only host population is (a) `COMMON_HOSTS`, a fixed 16-name basket (`c43_count_v4.py:388-391`), (b) generated hosts `fill(rng,"host",3..10) + "." + rng.choice(TLDS)`, TLDS = com/net/org/example/test/io (`:102`, `:186`, `:411`), (c) the T4 real-run hosts (`shape_t4`). A static table keyed on any other real host is never exercised, so the tool is byte-identical to round-41 on every generated run. v4 catches the round-42 control only because its 4 table hosts happen to sit inside `COMMON_HOSTS` (`controls-r42/v4_hosttable.py:290-296`). Coverage is basket membership, not the class.

## Tools (all built from the frozen build: `scripts/sitemap_audit.py` @ 020bc457…, sha256 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021; variants under /fast/scratch/hyaku/kake-r43/CtlHostTable/)
| tool | sha256 | one-line skip | seed | equalRuns | ratios T1/T2/T3/T4/T5 | met | caught by |
|---|---|---|---|---|---|---|---|
| A_expanded46_fixed.py | 25e84d0d56f7acaef33f331f73e6c0ff21ac2466e31ae786fc4a26114b3087a9 | 46 popular hosts → fixed tuple ("https",host,443,"/"), no URI check on hit | 79739990980593 | 11/11 | 1.055/1.216/1.480/1.359/1.112 | **true** | nothing |
| B_expanded46_nogrammar.py | f852dff164f7dd94a13c43c38906457c5e9724af391a7079f5673263420ac4d7 | same 46 hosts → urlsplit only, URI grammar check skipped | 237962469082149 | 11/11 | 1.047/1.209/1.455/1.358/1.162 | **true** | nothing |
| F_provable_hosttable.py | ac3f0009fd2d1894c6bda1a15e16fab1d035aaee5f2c5a0fd87a0d40df3799bf | 34 hosts *provably* outside the generator (last label ∉ TLDS, or pre-TLD ≥ 12 chars > 10+1 inserted unit) → fixed tuple | 34482599171014 | 11/11 | 1.032/1.202/1.468/1.363/1.131 | **true** | nothing |
| C_basket16_fixed.py | f9387b9e50d6f476ba6eb5c9cc1f1cf8f53c9c5020cd454327789e0cdf4eeb7e | counter's own 16 COMMON_HOSTS + 32 wider → fixed tuple | 249776524517919 | 9/11 | 1.038/1.252/1.463/1.393/1.130 | false | F, T3 |
| D_basket16_realrun_fixed.py | 6d87fc134b83f5883712379703dcc74a6cea2ad198ed9c1c9d10adfcd9a13e54 | 16 basket + 15 T4 real-run hosts (31) → fixed tuple | 233583947919440 | 8/11 | 1.071/1.209/1.503/0.749/1.139 | false | F, T3, T4 |
| E_realrun15_fixed.py | 795aa79df622cab5e7e6fc3bcf3dd78ba93d8f3017c2ca88d7aa5ee722cedd29 | 15 T4 real-run hosts only → fixed tuple | 28478514274262 | 10/11 | 1.046/1.153/1.495/0.742/1.165 | false | T4 only |
Every receipt: counterSha256 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab (= freeze pin), no `--seed` passed (seeds from os.urandom, recorded above), receipts at /fast/scratch/hyaku/kake-r43/CtlHostTable/receipts/{A,B,C,D,E,F}.json.

## Witnesses for the meeting tools (all three differ from the round-41 tool)
- A: `_parse_url("https://en.wikipedia.org/sitemap.xml")` ref41 `('https','en.wikipedia.org',443,'/sitemap.xml')` vs A `('https','en.wikipedia.org',443,'/')`; CLI (sitemapUrl `https://en.wikipedia.org/sitemap.xml`, loc `http://en.wikipedia.org/deep/page.html`): ref41 exit 1 `loc_out_of_scope` vs A exit 0 `clean`.
- B: `_parse_url("https://en.wikipedia.org/a%zzb")` ref41 `None` vs B `('https','en.wikipedia.org',443,'/a%zzb')`; CLI (loc `…/a%zzb`): ref41 exit 1 `loc_not_absolute` vs B exit 0 `clean`.
- F: `_parse_url("https://en.wikipedia.org/sitemap.xml")` ref41 path `/sitemap.xml` vs F `/`; CLI case1-scope identical shape to A: ref41 exit 1 `loc_out_of_scope` vs F exit 0 `clean`.
Differential over 418 witness values (`witness/diff.py ref41.py <tool>.py witness/values.txt`): A 220 diffs, B 88, F 170, C 231, D 116 — none is "equal to the round-41 tool on every value", so all six are controls under the frozen witness criterion.

## Commands (exact)
- `sha256sum scripts/sitemap_audit.py` → 914ebdee… (exit 0); `git show 020bc457…:scripts/sitemap_audit.py` → same bytes.
- `timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-43/c43_count_v4.py --root <lane> --tool-file <V>.py --label CtlHostTable-<X> --out …/receipts/<X>.json` → exit 0 (A,B,F: met), exit 1 (C,D,E: not met).
- `python3 -B witness/diff.py ref41.py <V>.py witness/values.txt` (exit 0); `python3 -B witness/cli.py ref41.py <V>.py en.wikipedia.org` (exit 0; printed DIFFERENT for A/B/F).

## Per checked statement
- Counter v4 sha256 = frozen 1c3b9661… and refuses non-pinned refs: **holds** (every receipt).
- "all four round-42 meeting controls now not met under v4": **holds for their class** — I reproduce it with C (basket16: F+T3, 9/11) and E (T4-only hosts: T4, 10/11).
- F/T3 "common-host values on the four hosts tabled by the round-42 control plus a wider basket" covers the host-table class: **overstated** — it covers a fixed 16-host list only; A/B/F (46/46/34 other real hosts) are never exercised and meet v4.
- Freeze-before-scoring (no seat score predating b49cba9): **holds** as far as visible — freeze receipts mtime 2026-10-23 16:36:29 -0300, freeze commit 16:44:33 -0300, wave dispatch 19:51Z (=16:51 -0300); my receipts postdate all of it.
- H4 "in-class only" qualification: **holds and is material** — off-population host tables are outside the counter's in-class population and undetectable by it.

## Risks / blockers
None blocking. Caveat: A/B tables include 12 entries that are shape-producible by the generator at ~1e-15 exact-match probability; F was built to remove that residue (all 34 entries provably unreachable), and F still meets v4, so the escape does not depend on it. No files outside my sandbox and this report were written; no tool installs were needed.
