MET — 5 of 9 shared-prefix-cache controls met counter v4 (11/11 equal, ratios ≤ 1.47) and each
diverges from the round-41 tool on a witness, so each is a control; under the frozen kill rule
"any live-seat control meeting v4" that means C1 is NOT MET (L1 to rule). The blind spot is one
code point wide: caches keyed on the first N code points are caught for N ≤ 44 and missed for
N ≥ 45, because the counter's only shared-prefix class tops out at a 44-code-point cut
(`c43_count_v4.py:450` `cut = rng.randint(36, 44)`).

Seat kake-r43-w1-CtlPrefixCache. Base `scripts/sitemap_audit.py` @020bc457 (sha `914ebdee…`),
counter `c43_count_v4.py` sha `1c3b9661…`. Command (no --seed; os.urandom seed in receipt):
`timeout 900 prlimit --as=8000000000 -- python3 -B <repo>/.ufo/waves/round-43/c43_count_v4.py
 --root <repo> --tool-file /fast/scratch/hyaku/kake-r43/CtlPrefixCache/<n>.py --label CtlPrefixCache-<n> --out <n>.json`
Skip: a module-global `_PREFIX_CACHE` wraps `_parse_url` (renamed `_parse_url_scan`); noreval reuses
the first parse for any value sharing the first N cp (tail never read); weakreval reuses it after a
cheap tail well-formedness check (tail content never compared); reval reuses only on identical tail.

| file /fast/scratch/hyaku/kake-r43/CtlPrefixCache/ | sha256 | skip | seed | equalRuns | ratios T1/T2/T3/T4/T5 | met | caught by |
|---|---|---|---|---|---|---|---|
| `p16_noreval.py` | `40d118573b78…` | 16 cp none | 212063442214382 | 3/11 | 1.05/0.91/1.30/0.70/1.09 | false | A,B,C,D,E,F + T2,T3 reps |
| `p24_noreval.py` | `28238b0ab9dc…` | 24 cp none | 32264098028907 | 6/11 | 1.04/0.87/1.33/0.69/1.06 | false | B,D,F + T2,T3 reps |
| `p32_noreval.py` | `db50cc51027c…` | 32 cp none | 97980567091280 | 8/11 | 1.06/0.95/1.42/0.71/1.10 | false | F + T2,T3 reps |
| `p36_noreval.py` | `327f3093cd1b…` | 36 cp none | 92898020256209 | 9/11 | 1.04/1.19/1.44/0.70/1.04 | false | F + T3 reps |
| `p40_noreval.py` | `b29d26047707…` | 40 cp none | 29357229475160 | 9/11 | 1.03/1.23/1.46/0.82/1.07 | false | F + T3 reps |
| `p44_noreval.py` | `dbec0e69b391…` | 44 cp none | 185484641100860 | 9/11 | 1.02/1.26/1.40/1.01/1.21 | false | F + T3 reps |
| `p45_noreval.py` | `164aa4d5902b…` | 45 cp none | 157897586892236 | 11/11 | 1.07/1.26/1.46/1.06/1.17 | **true** | nothing |
| `p46_noreval.py` | `442c84ea8aaa…` | 46 cp none | 246453014200990 | 11/11 | 1.06/1.22/1.47/1.10/1.22 | **true** | nothing |
| `p48_noreval.py` | `4e5064fccdac…` | 48 cp none | 190339581916698 | 11/11 | 1.05/1.25/1.42/1.11/1.19 | **true** | nothing |
| `p64_noreval.py` | `678fec6dc61f…` | 64 cp none | 186734228306336 | 11/11 | 1.04/1.16/1.45/1.33/1.12 | **true** | nothing |
| `p16_reval.py` | `fb391b4581bf…` | 16 cp exact tail | 67984378148720 | 11/11 | 1.14/1.19/1.47/1.31/1.35 | true* | nothing |
| `p24_reval.py` | `e234f283d4c9…` | 24 cp exact tail | 8731700520366 | 11/11 | 1.20/1.24/1.34/1.31/1.13 | true* | nothing |
| `p48_reval.py` | `b76749ff9682…` | 48 cp exact tail | 92023601898405 | 11/11 | 1.17/1.35/1.40/1.41/1.19 | true* | nothing |
| `p24_weakreval.py` | `c67bad5957f4…` | 24 cp weak tail | 70642802506666 | 9/11 | 1.03/0.99/1.42/0.74/1.14 | false | F + T2 reps |
| `p48_weakreval.py` | `4905148a5cc2…` | 48 cp weak tail | 275074208186561 | 11/11 | 1.05/1.22/1.46/1.20/1.18 | **true** | nothing |

\* met honestly: prefix + identical tail is the whole value (an exact memo), no divergent witness
exists, not controls. Witnesses (verified locally `python3 -B`; base42 == ref41 on each, so the
divergence is the cache's): noreval N∈{45,46,48,64} — locs `https://www.example.com/` + `a`×(N−24)
+ `/good` then same head + `%zz`, smu `https://www.example.com/sitemap.xml`: ref41 `_parse_url(bad)`
= `None`, variant returns good's tuple; CLI ref41 exit 1 `loc_not_absolute` entry 2 vs variant
exit 0 `clean`. weakreval 48 — smu `…<head48>/docs/sitemap.xml`, locs `…<head48>/docs/ok`,
`…<head48>/other/no` (head48 = `https://www.example.com/`+`a`×24): ref41 exit 1 `loc_out_of_scope`
entry 2 (loc2's real path not under `…/docs/`); variant exit 0 `clean` — loc2 inherits the
sitemapUrl's cached parse.

Why blind at ≥45 (seed-4242 corpus, XML-decoded, ref41 `_parse_url`): `prefix_pair`
(`c43_count_v4.py:443-456`) is the only class built for this attack; its cut `rng.randint(36,44)`
can never emit a pair sharing ≥45 cp, and F's `prefixpair` units (`:472`) plus T3's 3% prefix pairs
(`:796-799`) both draw it. Census `analyze2.py`: finding-relevant divergent groups exist at w≤44
(F 441@16→16@44; T3 3171@16→52@44; T2 74@32; A–E at w16-40) and ZERO at w≥45 in every generated
run. T4 has 2423 colliding groups at 48 cp and 86 at 64 cp, all path-tail-only (postgresql.org doc
pages) under a `/` sitemap directory, so no finding flips; verified: every variant's CLI output on
`.ufo/waves/round-41/realrun/` is byte-identical to ref41's (exit 1, sha `2ffbea3a…`).

Statements: "the predicate certifies the tool keeps every round-41 judgment" — WRONG (five controls
meet it while misjudging witnesses). The header's shared-prefix class (`c43_count_v4.py:4-5,444-446`)
— OVERSTATED: sized for the round-42 32-cp control, invisible ≥45 cp. "Values are distinct … so
caching by value cannot help" (`:33`) — HOLDS for whole-value caching (reval memo pays 1.1-1.4×
overhead, keeps every judgment); does not extend to prefix caching. Files: 15 variants + receipts,
builders, analyzers, witnesses under `/fast/scratch/hyaku/kake-r43/CtlPrefixCache/`; this report.
No tool installed/upgraded; no repo/jj/git write outside this report; no network. Risk: one seed
per met verdict, but ≥45-cp blindness is structural (cut ≤ 44; T4 retained).
