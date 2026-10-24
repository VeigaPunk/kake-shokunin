# ReviewBuildVsIndependent — round 41 wave 2 (falsify, operability)

Target: agreement of `scripts/sitemap_audit.py:_parse_url` (build, eae5ae2) with the
wave-1 independent build `/fast/scratch/hyaku/kake-r41w1/ExecIndependentBuild/indep.py`,
with the abnf-2.9.1 RFC 3986 `URI`-with-authority oracle (counter's own `load_oracle`,
wheel sha256 verified cdcac127…60917) as third vote.

## Commands
- `timeout 600 prlimit --as=4000000000 python3 -B compare.py` — exit 0, 20 s.
  Harness: /fast/scratch/hyaku/kake-r41w2/ReviewBuildVsIndependent/compare.py;
  full rows: result.json (same dir).
- Values: `generate()` of c1_count.py (seeds 101-103) + c1_count_v2.py (seeds
  201-204 → 201-203) + 107 hand edge cases; loc values judged after sentence-21
  strip, sitemapUrl raw. 8,711 unique values (≥5,000 required: met).

## Result
All three agree on 8,689 / 8,711 (99.7%). Zero exceptions in any implementation.
When build and indep both accept, returned tuples are always identical (0 tuple
mismatches). 22 values disagree:

### build vs indep — 15 mismatches (the target)
Kind A — build ACCEPTS, indep+oracle REJECT (12 values):
- IP-literal with `%` inside (4): `http://[fe80::1%25eth0]/`, `http://[fe80::1%eth0]/`,
  `http://[v1.%41]/`, `http://[v1.%]/`. Build regex `[^\]]*` (sitemap_audit.py:80)
  passes any bracket body; urlsplit's own check tolerates `%`, so unescaped zones
  (invalid even under RFC 6874) and pct-soup IPvFutures are accepted. Severity: low-med.
- `@` inside a bracket span (1): `http://[ku$.%6F:ga%dfi1bQ@[2001:db8::]/y9i5w5%f5%Acwy`.
  Build's userinfo fails on `[`, so the whole `[…@[…::]` span matches the lax
  IP-literal; urlsplit then re-derives host `2001:db8::`. Grammar-invalid twice
  over, still accepted. Severity: medium (only counter-v2-class userinfo fuzz hits it).
- Non-ASCII outside ucschar (8): U+0080, U+009F, U+E000 (private use), U+FFFE
  (noncharacter), U+D800 (surrogate), U+E0001, U+F0000, U+10FFFF — build's
  `\u0080-\U0010ffff` class accepts all; indep's ucschar and the oracle reject.
  Documented build choice (comment lines 69-72); severity: low.

Kind B — build REJECTS, indep+oracle ACCEPT (3 values):
- Port digits > 65535 (3): `http://h:65536/`, `http://h:99999999999/`,
  `https://h:99999999999999999999/` (also `http://[::1]:99999/`). Grammar
  `port = *DIGIT` is unbounded; build rejects via `urlsplit`'s .port ValueError
  → `loc_not_absolute`/`check_invalid` on grammar-valid URIs. Documented at
  line 72, still a divergence from "judged as written against URI grammar".
  Severity: low-med.

### indep vs oracle — 7 mismatches
All ucschar-IRI accepts (`/xä`, `hä`, U+00AD, U+0378, U+20000, U+D7FF, `uä@`):
indep deliberately adds RFC 3987 iunreserved (its comment lines 83-85); the pure
3986 oracle rejects. On all-ASCII inputs indep matches the oracle 100% (0 diffs
in ~8,690 ASCII values) — the independent build is a faithful grammar oracle.
build vs oracle = 22 (union of the two lists above).

## Statement checks
- "Build ≈ independent build": overstated — 15/8,711 diverge (0.17%); every
  divergence traces to build's documented lax reading, but two classes (`%`/`@`
  inside IP-literals) are invalid under any reading and are not the documented
  ucschar/port exceptions.
- Counter v1's 15/141 met-receipts: consistent — v1 units never generate
  bracket-junk, non-ASCII, or 5+-digit ports, so v1 could not see these diffs.
- No installs; no repo mutation. Residual risk: probe coverage of `loc` fields
  stops at strip(); XML-entity edge cases in `_value_text` out of scope.
