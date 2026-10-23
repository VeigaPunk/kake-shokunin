# ReviewCounterGenerators — do the counter's generated runs match their description?

Counter `.ufo/waves/round-42/c42_count.py` sha256 `7bfc32c5e76dca9…` (verified). Probe: imported the
counter as a module (read-only, `python3 -B`, no bytecode written to the lane) and called its generator
functions with seeds 1, 2, 3 (+ dedicated seeds 7, 11 for two T1 audits), measuring counts, lengths,
defect positions, distinctness, branch/slash structure, XML well-formedness, and the T4 SHA256SUMS path.
Probe + raw JSON: `/fast/scratch/hyaku/kake-r42w1/ReviewCounterGenerators/gencheck.py`,
`gencheck-{1,2,3}.json` (full), `gencheck-{1,2,3}.full.json`. Commands: `prlimit --as=8000000000 -- timeout
900 python3 -B gencheck.py <seed> .` → EXIT:0 (all runs, 3 full + 3 layout-only after a checker fix).

## Measured table (seeds 1/2/3 unless one seed named)

| run | count (claim) | lengths (claim) | distinct | defects | XML |
|---|---|---|---|---|---|
| A | 1434 (1434) = 630 loc + 804 sitemapUrl ✓ | short URLs | 1434/1434 ✓ | inserted unit present 1434/1434 ✓ | 0 malformed, loc round-trips exactly ✓ |
| B | 1200 (1200) = 600+600 ✓ | bracket body 0–47 | **1194–1195/1200** | 0–3 bracket edits (structure 1200/1200 ✓) | loc all XML-legal ✓ |
| C | 656 (656) = 600+40+16 ✓ | 1800–2047 ✓; 2093–5985 ⊂ 2048–6000 ✓; su16 199998–200000 ✓ | 600/40/16 ✓ | 0–1 per value ✓ (353–360/600 defective, p≈0.6; ≥ path start) ✓ | 0 malformed ✓ |
| T1 | 20000, 1 check ✓ | 1998–2047 (claim 2000–2047) | 20000 ✓ | 1 per value ✓, start ≤68 from end | texts == input ✓ |
| T2 | 20000, 1 check ✓ | 1998–2047 | 20000 ✓ | 0 ✓; pct density 0.036, all triplets valid ✓ | texts == input ✓ |
| T3 | 50000, 1 check ✓ | 58–140 (claim 60–140) | 50000 ✓ | 0 ✓ | texts == input ✓ |
| T5 | 48 checks, ids unique ✓ | 199998–200000 ✓ | 48 ✓ | 40 declared: detected 40/39/40 (≤1 masked) ✓ | single XML parses ✓ |
| T4 | SHA256SUMS: 7 files (manifest + 6 sitemaps), 0 mismatches (counter check + independent recomputation), copied set == sums, manifest v1/6 checks | | | | |

## Per description sentence

- Counts 1434/1200/656 (A/B/C, receipt `runs.X.values`): **holds** (c42_count.py:206,229,275; 6×105, 2×600, 600+40+16).
- A "one inserted ASCII unit or percent sequence at any position of one component": **holds** (unit present in every value; `insert` on the target component in every branch of `make_url`).
- B "1200 IP-literal values, zero to three random edits, zone-id forms": **holds** (structure 1200/1200; `%25en1`, `%eth0` classes present via BRACKET_EDITS, c42_count.py:83).
- C "1,800–2,047 … non-ASCII included … zero or one defect at any position, plus 40 loc of 2,048–6,000 and 16 su of 200,000": **holds** (non-ASCII in 294–305/600; defect at/after path start, min +13 past head).
- T1 "one defect in the last 64 positions": **holds to within the defect's own length** — insertion index is windowed to the last 64 pre-insert positions (c42_count.py:269); post-insert start sits ≤68 from the end because the unit itself adds 1–3 code points.
- T1 "whose path, query or fragment is one long run without `/`": **wrong for ~40% of values**. Only the path branch (measured 59.9%, seed 11) is slash-free (exactly 4 slashes = head `//`+2). Query/fragment bodies draw from `FILL["query"]/["fragment"]`, which contain `/` (c42_count.py:78-80), so those values carry mean 21.8 extra slashes (min 7) — `/` roughly every 90 chars. This is the same property draft 1 was rejected for (SCORECARD: "its T1/T5 values had `/` every ~80 characters"), now diluted to the ~40% non-path branch instead of fixed. T5 likewise: slash-free only 25–36 of 48 per seed; the rest carry ~2170–2189 extra slashes. **The adversarial "one run without /" property is fully present on only ~60% (T1) / 52–75% (T5) of values.** Flagging for the freeze: may dilute the T1/T5 ratios the predicate measures; L1's call whether the description or the shape changes.
- T2 "valid long loc with percent triplets": **holds**; T3 "50,000 valid loc of 60–140": **holds with a 2-code-point dip** (min 58; `long_value` trims a partial pct triplet, docstring at :249 admits "a little less").
- T5 "48 `sitemapUrl` of 200,000 code points, 40 with a late defect": **holds** on count/defects; lengths 199998–200000 (same trim nuance); "in one run without `/`" — see T1 finding, wrong for 25–48% of values.
- T4 "retained round-39 real run (SHA256SUMS verified)": **holds** functionally (every listed file hashed, copy fail-closed via `CannotEvaluate`, c42_count.py:391-405; manifest present and well-formed). Cosmetic: docstring/SCORECARD say "round-39", the path is `.ufo/waves/round-41/realrun`.
- "Values are distinct (a random token leads every path), so caching by value cannot help": **holds for A, C, T1–T5 (100% distinct); overstated for B** — no leading token exists there and fixed short literals collide: `https://[::]` ×4, `https://[::1]` ×3, `http://[:::1]` ×2 (seed 1; 5–6 duplicate instances per seed). A value-cache could skip ≤0.5% of B's parses; equality/timing conclusions unaffected at this rate.
- XML legality: **holds** — every generated sitemap (A/B/C layouts and T1/T2/T3/T5) parsed well-formed; `xml_text`/`fast_xml` escaping round-trips exactly (decoded locs == values); loc values 0 XML-illegal chars; sitemapUrl values that do carry control chars (87–174/run) live only in manifest JSON, never in XML (by design, layout_cases:292).

## Verification gaps / residual risk

- 3 seeds per shape (T1 slash-share on 1 dedicated seed; branch mix consistent ~60/40 across seeds 1–3).
- A defect `%` followed by two hex chars is undetectable in the finished string; ~1.6–2% of defective values masked — detector can only undercount, so "exactly one defect" is verified as "≤1, ≥98% detected"; zero genuine multi-defect values in 40,096 audited.
- Multi-`%`-hit noise (T1 ~1300 values) is an artifact of adjacent `long_body` pct insertions, not second defects (audited: 0 values with ≥2 non-`%` defect chars).
- Sandbox/CPU measurement, equality scoring, and candidate tooling are out of scope here (other seats); no counter process was executed — generators only.
