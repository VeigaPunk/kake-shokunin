# CriticKeyStrength — receipt-only discrimination review
Axes: operability (attacked); freshness (not measured). No round judgment or claim re-score.
Checked 77 receipts using ONLY `{label,passed,met,toolSha256}` projections; joined all 54 mutant records to their descriptions by seat/id AND exact tool hash. No sealed paths, rows, why, counter, network, or detector execution.
**HOLDS:** 39/54 mutant records score below 24; **OVERSTATED:** 24/24 proves contract discrimination—15 known non-equivalent mutant records and the regex shortcut reach 24.
Table: S = contract sentence; N = scored records declaring exactly one sentence; 24 = those reaching 24. This is mutation discrimination, not inferred case coverage.
| S | N | 24 | S | N | 24 |
|---|---:|---:|---|---:|---:|
| 1 | 0 | 0 | 18 | 0 | 0 |
| 2 | 0 | 0 | 19 | 1 | 0 |
| 3 | 0 | 0 | 20 | 1 | 0 |
| 4 | 3 | 2 | 21 | 1 | 0 |
| 5 | 0 | 0 | 22 | 3 | 2 |
| 6 | 0 | 0 | 23 | 1 | 0 |
| 7 | 0 | 0 | 24 | 4 | 1 |
| 8 | 0 | 0 | 25 | 2 | 1 |
| 9 | 0 | 0 | 26 | 3 | 0 |
| 10 | 3 | 2 | 27 | 1 | 0 |
| 11 | 2 | 1 | 28 | 1 | 0 |
| 12 | 0 | 0 | 29 | 6 | 0 |
| 13 | 1 | 0 | 30 | 0 | 0 |
| 14 | 4 | 4 | 31 | 1 | 0 |
| 15 | 0 | 0 | 32 | 5 | 0 |
| 16 | 0 | 0 | 33 | 6 | 0 |
| 17 | 2 | 1 | 34 | 0 | 0 |
Totals: 51 single-sentence records / 14 at 24. Three multi-sentence records excluded: EntryNumbering M02 [11,33] = 24; M03 [11,33] = 23; M06 [13,33] = 22. All 15 survivors have distinct hashes.
Identity caveats: NumericBoundaries M06 and StdlibSubstitution M04 are identical bytes; S32 has 4 unique tools, not 5 (overall 53 unique tools; 50 single-sentence). Producers assign the unnumbered finding-identity preamble (contract:31–32) to S33; retain that convention explicitly, not as independent numbered-sentence provenance.
Evidently untested distinctions: S4 empty-port/fragment sitemapUrl; S10 namespace-URI slash/case; S11 child-local default binding; S14 foreign root/entry fields and empty-namespace reset; S17 nested url field; S22 userinfo/IPv6; S24 explicit port zero; S25 trailing-slash directory; combined S11/33 foreign-child ordinal shift.
**WRONG:** asserting a whole sentence is “never tested” from these totals. S14 alone has all its supplied one-sentence probes survive (4/4); this establishes four blind distinctions, not absence of every S14 case. Unprobed S1–3,5–9,12,15–16,18,30,34 remain unknown, not passed or proven absent.
Strongest existing counterexample: MutNamespaceBinding/mutants/M10_foreign_priority.py:154 treats foreign `<x:priority>2</x:priority>` as sitemap priority; its public witness is clean under S14 but the mutant emits priority_invalid/1 (w1a3/MutNamespaceBinding.md:26), yet its hash-bound receipt is 24/24. This is a fixable discriminator defect, not an acceptable contract tradeoff.
## Smallest proposed addition — UNRUN, contract-derived, no key contents
Three XML fixtures, packable into ONE three-check manifest; each check uses unique id, relative file, and sitemapUrl `https://[2001:db8::1]:/dir/#fragment`. Exact UTF-8 inputs and complete expected JSON: sandbox `proposed-cases.json` below. Compare full findings as (code,entry) sets and exit 1, not just verdict.
1. Root `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9/"/>` → root_invalid/null; predicts killing NamespaceBinding M02.
2. Root `<urlset xmlns="http://www.SITEMAPS.org/schemas/sitemap/0.9"/>` → root_invalid/null; predicts killing NamespaceBinding M03.
3. Correct-namespace root with legal Unicode prefix `é:urlset`, also binding the default sitemap namespace and x=urn:extension. Before four real entries put `<x:url/>`; explicitly redeclare the correct default namespace on entry 1.
Entry 1: loc `https://u@[2001:db8::1]/dir/a`, foreign `<x:url/>`, `<loc xmlns="">ignored</loc>`, foreign `<x:priority>2</x:priority>`; entry 2: valid same-host `/dir/ok` loc plus sitemap-namespace `<url/>`; entry 3: same-host `/outside`; entry 4: `https://[2001:db8::1]:0/dir/zero`.
Expected fixture-3 findings ONLY: element_unexpected/2, loc_out_of_scope/3, loc_out_of_scope/4. Distinct entries prevent the foreign-url and nested-url faults masking each other as identical set pairs.
Fixture 3 predicts killing NamespaceBinding M04,M07–M11; EntryNumbering M02; UrlAuthority M03–M05,M09–M10; StdlibSubstitution M09; and CtlRegexTweak. Its ASCII-only TOKEN_RE (control.py:27–33) misses legal `<é:urlset>`; scan:85–86 predicts xml_malformed instead of those findings.
[INFERENCE] Three documents are minimal for these implementations: the two root-URI normalization faults need mutually exclusive wrong namespaces, while remaining namespace faults need a valid namespace root. The Unicode-prefix witness folds the regex kill into that third document; no fourth malformed-XML fixture is necessary. If manifest is the scoring unit, the minimum is one multi-check case. No proposed kill was executed.
## Reproducible evidence
Sandbox = `/fast/scratch/hyaku/kake-r39a3w2/CriticKeyStrength/`; `receipt-analysis.json` SHA256 `a42471c01d9bb0582596ae1f8dda7378ddfef96bfe56fd20fc07220d338b5eb3`; `proposed-cases.json` SHA256 `4d4177baafd1e565770db37135f684807daa0baa003cc21ec934b9a9d6f917b7`.
Regex source `/fast/scratch/hyaku/kake-r39a3w1/CtlRegexTweak/control.py` SHA256 `2d941dab16fbd28fba438c0fcf172c696c627503ff7faf57c9b4fcc892db2af3`, matches its allowed receipt toolSha256; passed=24, met=true.
Exact shell commands, both exit 0 (only hashing; projections/aggregation used read/eval tools, not shell commands):
`timeout --signal=TERM --kill-after=2s 20s prlimit --as=4000000000 -- sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/c1-contract.md /fast/scratch/hyaku/kake-r39a3w1/MutNamespaceBinding/mutants.json /fast/scratch/hyaku/kake-r39a3w1/MutNumericBoundaries/mutants.json /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants.json /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants.json /fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants.json /fast/scratch/hyaku/kake-r39a3w1/CtlRegexTweak/control.py /fast/scratch/hyaku/kake-r39a3w2/CriticKeyStrength/receipt-analysis.json`
`timeout --signal=TERM --kill-after=2s 20s prlimit --as=4000000000 -- sha256sum /fast/scratch/hyaku/kake-r39a3w2/CriticKeyStrength/receipt-analysis.json /fast/scratch/hyaku/kake-r39a3w2/CriticKeyStrength/proposed-cases.json`
Smallest safe correction: add the proposed discriminator inputs in a future explicitly authorized key revision; retain current frozen totals and claim identity unchanged. No build/test/counter was run; no installs/updates, background processes, or writes outside sandbox and this report.
