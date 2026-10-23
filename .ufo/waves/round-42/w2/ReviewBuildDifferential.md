# ReviewBuildDifferential — round 42 wave 2 (falsify)

Verdict: no divergence found. Build (scripts/sitemap_audit.py) and round-41
tool (tip41.py) agreed on every value compared: 1,380,000 gate checks and
1,380,000 `_parse_url` comparisons, zero mismatches.

## Item
Attack "keeps the round-41 tool's judgments" with a generator unrelated to the
counter's (c42_count_v3.py) unit-at-position scheme.

## Method
Differential harness `/fast/scratch/hyaku/kake-r42w2/ReviewBuildDifferential/diffgen.py`
(sha256 28e820c6dbf3a9d25b4677495bbefbe6ccf40035dd9fe41f3ea460c2bf6d7dba)
loads both tools via importlib (guards present; no execution side effects),
compares `_uri_ok(v)` vs tip41 `_URI_RE.match(v)` and the full `_parse_url(v)`
results. Harness detection validated: patched build._parse_url -> mismatch
count 200/200; patched tip41 gate -> mismatch count 21/50.

Tools under test:
- build scripts/sitemap_audit.py sha256 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021 (round-42, 020bc457)
- tip41.py sha256 50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d

## Runs (all exit code 0; `timeout 900 prlimit --as=8000000000 -- python3 -B diffgen.py --family F --n N --seed S --out O`)
  grammar   n= 120000 seed=424201 gate_mm=0 parse_mm=0
  unicode   n= 140000 seed=424202 gate_mm=0 parse_mm=0
  extremes  n= 160000 seed=424203 gate_mm=0 parse_mm=0
  fuzz      n= 220000 seed=424204 gate_mm=0 parse_mm=0
  bitflip   n= 120000 seed=424205 gate_mm=0 parse_mm=0
  valid     n= 200000 seed=424206 gate_mm=0 parse_mm=0
  httpvalid n= 240000 seed=424207 gate_mm=0 parse_mm=0
  nearvalid n= 180000 seed=424208 gate_mm=0 parse_mm=0
plus a handpicked suite of 296 edge strings (empty/partial values, IPvFuture,
zone ids, malformed %-triplets, huge ports, bracket abuse, multi-@ userinfo,
http/https case variants, ports past 65535, control chars): 0 mismatches.

Total: 1,380,000 gate comparisons, 1,380,000 `_parse_url` comparisons,
0 mismatches overall. Families cover: valid http/https URLs (live urlsplit
paths), near-valid corruptions, RFC 3986-shaped random URIs, Unicode-heavy
values (non-ASCII unreserved, surrogates, controls, NBSP/BOM/RTL/ZWJ,
noncharacters), byte-level fuzz over hostile alphabet, lengths 0..~1e5,
surgical bitflips of valid URLs.

## Findings
None. Statement checked — "keeps round-41 judgments": HOLDS on every generated
value tested (1.38M) and every handpicked edge string. No witness value exists
in this sample; per kill rule 2, no control was found.

## Residual risk / verification gaps
- Judgment space is infinite; this seat sampled 1.38M values + 296 edge cases,
  not all strings. Cost ratio, selftest fixtures, H4/H5, real-run byte-equality
  are other seats' checks; not run here (not in scope of this item).
- `_parse_url` is identical past the gate in both tools (verified textually), so
  gate equality implies full judgment equality; both layers were compared anyway.
- No tools installed; no network used; nothing mutated outside sandbox and this report.

Report: .ufo/waves/round-42/w2/ReviewBuildDifferential.md
