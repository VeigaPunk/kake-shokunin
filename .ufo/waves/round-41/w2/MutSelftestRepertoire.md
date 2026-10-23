# MutSelftestRepertoire — bounded mutation probe
Axes: operability (fixture sensitivity); freshness (exact landed-build provenance only).
Build: eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6; copied only its two scripts with read-only git archive. No lane source/index/state changed.
Checked statement: SCORECARD.md:2802-2804 reports PASS 198/198 at the build — holds on pristine and every restored copy.
Checked hypothesis: the 15 r41 fixtures kill this component-repertoire sample — wrong: 3/17 killed, 14/17 survived, 0 inconclusive. This hypothesis is not a quoted scorecard claim.
MEDIUM — scripts/sitemap_audit_selftest.py:876-950: all 198 fixtures, including all 15 additions, miss 14 behavior-changing userinfo/reg-name/query/fragment repertoire defects. This is a coverage finding, not a defect demonstrated in the pristine build.
Expected detector: unchanged full selftest must exit 1 when a mutant contradicts an exercised expectation; a survivor exits 0 despite its independently witnessed parser behavior change.
R=/fast/scratch/hyaku/kake-r41w2/MutSelftestRepertoire (all evidence and scratch writes stay here except this report).
Exact outer commands (each exit 0):
`timeout --kill-after=5s 900s prlimit --as=4000000000 --fsize=60000000 -- python3 -B /fast/scratch/hyaku/kake-r41w2/MutSelftestRepertoire/probe.py baseline`
`timeout --kill-after=5s 900s prlimit --as=4000000000 --fsize=60000000 -- python3 -B /fast/scratch/hyaku/kake-r41w2/MutSelftestRepertoire/probe.py mutated`
`timeout --kill-after=5s 900s prlimit --as=4000000000 --fsize=60000000 -- python3 -B /fast/scratch/hyaku/kake-r41w2/MutSelftestRepertoire/probe.py restored`
Inner detector: `timeout --kill-after=5s 150s prlimit --as=4000000000 --fsize=60000000 -- /usr/bin/python3 -B R/pristine/scripts/sitemap_audit_selftest.py --tool TOOL`; TOOL is R/pristine/scripts/sitemap_audit.py initially, then R/mutants/ID.py. Fully expanded argv, exits, stdout and stderr are retained in R/results/{baseline,mutated,restored}/*.json.
Pristine shared baseline: PASS 198/198, exit 0; all 17 slots had identical pristine bytes before mutation.
Pristine and restored tool SHA-256 (every slot): 0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf.
Unmodified selftest SHA-256 throughout: d8d2ba6cf3d8721e558cac42f44784101aaaddab8571a5364b8808cd4977c16d.
Restoration: exact original bytes restored in all 17 slots; each reran the identical full detector with PASS 198/198, exit 0, r41 15/15. Each witness also returned to its pristine output.
Every mutation is exactly one inserted/deleted ASCII character in one _URI_RE component; independently recorded one-edit diffs and SHA-256s are in R/mutation-diffs.json. Lines below refer to scripts/sitemap_audit.py.
Survivors first; PASS lines and exits are actual full-selftest outputs. The r41 column is passed additions / 15.
| ID | Single change @ line | Selftest PASS line | Exit | r41 | Verdict | Mutated SHA-256 |
|---|---|---|---:|---|---|---|
| U01 | userinfo + U+007C @79 | PASS 198/198 | 0 | 15/15 | survived | 3e2cf071e0cfcf956cbffd388c3146540e353be959b5924875389afd0a31c827 |
| U02 | userinfo + U+0020 @79 | PASS 198/198 | 0 | 15/15 | survived | 7b91ff3a0832e8b1d6c375fd09004b35778c7b2d62d35e81db058d5c1c91d74e |
| H01 | reg-name + U+007C @81 | PASS 198/198 | 0 | 15/15 | survived | 3ad1c92e574bf45e75dd0b83da6af6136983c67e8fc46f955c57480fffc3428d |
| H02 | reg-name + U+005E @81 | PASS 198/198 | 0 | 15/15 | survived | 5cf5bdeb0913be53326880b9202c148ca2073b7fd2ff8158485ed29b8af7a488 |
| H03 | reg-name + U+0060 @81 | PASS 198/198 | 0 | 15/15 | survived | da78dfde5322de98d45baa1ea0ad58e0687ad6aaf5d391d7bbae3dd762de6ebd |
| H04 | reg-name + U+0020 @81 | PASS 198/198 | 0 | 15/15 | survived | 620333250501917a15d4246a99f34e7f5387fe1f4202c83f711b889acdf9164e |
| Q01 | query + U+007C @84 | PASS 198/198 | 0 | 15/15 | survived | e799d06c300c2f6b1ff32aee08e6d928ee97435c295b88ebee51a95d8e5820db |
| Q02 | query + U+0020 @84 | PASS 198/198 | 0 | 15/15 | survived | a7bb394e1301e44ae79361862ea9e257941fb3093680dbd57b57a60e8f6c30b0 |
| Q03 | query - U+003F @84 | PASS 198/198 | 0 | 15/15 | survived | faaa60ed7dbbdb2db922b1636228e3a3a289f2f7f289b0d68c06c19851bf235b |
| Q04 | query - U+002F @84 | PASS 198/198 | 0 | 15/15 | survived | a414f1147ef991a88867ca5f636ede62fb719adeae7f0b50d4932e8792dd76b6 |
| F01 | fragment + U+007C @85 | PASS 198/198 | 0 | 15/15 | survived | e0fd68b47c08273dafb80bbe378d80a991a0bc6d7872f3a90101f7ba002c2c15 |
| F02 | fragment + U+0020 @85 | PASS 198/198 | 0 | 15/15 | survived | 2b5bf85903bda19ef0cca1d812e3f19a47695c38b2a7ac070ddcb70ef93e2090 |
| F04 | fragment - U+003F @85 | PASS 198/198 | 0 | 15/15 | survived | cfe121919252a97d3b86c6b2076e059babbb474920d5a7749a3d1aeac4de74fd |
| F05 | fragment - U+002F @85 | PASS 198/198 | 0 | 15/15 | survived | cbb7f4a89c23b541f94382a31e506e7cb5fe8fa65145c3468a6ba6bb35237e10 |
| U03 | userinfo + U+0040 @79 | PASS 197/198 | 1 | 14/15 | killed | d8f4d947f8b18832319dca62297b60d9ce9207e24dca737116bf20d9ace7b0a5 |
| U04 | userinfo - U+003A @79 | PASS 197/198 | 1 | 14/15 | killed | 39229e954c3fff39e0cea09f443dadca6cb06bfeca5d4b415fec905b979a8f34 |
| F03 | fragment + U+0023 @85 | PASS 197/198 | 1 | 14/15 | killed | 4869e837e44ca450cae890d0c8705257ccf40ec74f3eef4c2555bb8fb24d13a9 |
Killed outputs: U03: FAIL r41_loc_userinfo_second_at; U04: FAIL r41_loc_userinfo_with_colon; F03: FAIL r41_loc_fragment_second_hash; each prints PASS 197/198 and exits 1.
U03/F03 actual mismatch: tool exit 0 != 1, clean != failed-policy, findings [] != [(loc_not_absolute, 1)]. U04 reverses those expectations. Full literal outputs: R/results/mutated/{U03,U04,F03}.stdout.
Witnesses: all 17 change _parse_url output on their recorded URL (all witness commands exit 0). Additions turn rejection into acceptance; deletions turn acceptance into rejection; none are equivalent/masked mutants.
Examples: U02 http://us er@example.com/a changes null to [http,example.com,80,/a]; Q03 http://example.com/a?q=x?y changes [http,example.com,80,/a] to null; both still print PASS 198/198.
Complete per-mutant before/mutated/restored hashes, witness URLs/outputs, detector results and restoration evidence: R/final-evidence.json; exact recipes: R/recipes.json; raw phase receipts: R/{baseline,mutated,restored}.json.
Bounds: two detector workers; at most eight workload processes including timeout supervisors/driver/children; 4 GB address-space limits; 60 MB per-file limit; one temporary fixture per worker (largest 52,428,801 bytes), removed by the unchanged suite. Every started subprocess group was reaped and killpg-cleaned; no persistent process or network request.
Tool installs/updates: none. No contract change, integration, round verdict, or broader pristine-build conformance verdict made.
