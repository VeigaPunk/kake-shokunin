# ExecBuildIndependent — independent fast rewrite of the URL check (round 42, wave 1)

## What I built

* Tool: `/fast/scratch/hyaku/kake-r42w1/ExecBuildIndependent/sitemap_audit_fast.py`, sha256 `438afaf0a445e07f3eeb551da18912818e0f9553caa436b941e64e14591c6e8b` — a copy of `50287ac6…` (`scripts/sitemap_audit.py` at `1ef7a0e9`) with **only** the URL block changed (`diff -u tip41.py sitemap_audit_fast.py`: 225 changed lines, all in `sitemap_audit_fast.py:66-283`; `_parse_url` `:282` and below are byte-identical, so `urlsplit` still judges host, port range, IPv6 literal). Written without reading any other seat's work; only shared instruments were read (`tip41.py`, `base40.py`, the counter's source — the counter was **not run**).
* Technique (`sitemap_audit_fast.py:100-280`): one `utf-8`/`surrogatepass` encode (`:212`); each grammar class a 256-byte translation table (`_class_table` `:100`, tables `:113-128`) so `bytes.translate(t).find(b"\x01")` gives the first byte outside the class in one C pass; the percent rule one linear regex `%(?![0-9A-Fa-f]{2})` per region (`:129`); the path walked with **one** mask per region (`_path_ok` `:158`); authority/port/query/fragment scanned by index (`_scan` `:175`, `_uri_ok` `:206`).

## Differential vs tip41 `_parse_url` (full return tuple) — 0 disagreements

`difftest.py 300000 20261023` exit 0 → 300 109 values; `250000 4242` exit 0 → 250 109; `150000 5150` exit 0 → 150 109; `fuzz2.py 250000 2024` exit 0 → 250 000; `250000 31337` exit 0 → 250 000; `150000 99` exit 0 → 150 000 ⇒ **1 350 327 values, 0 disagreements**. `difftest.py` = structured URLs, one-unit insertions per component, ASCII junk, 1 800–2 047 code-point values, 2–5 % non-ASCII, 106 hand-written edge cases; `fuzz2.py` = byte-random strings weighted onto `%`, hex, `:`, `@`, `/`, `?`, `#`, `[`, `]`, non-ASCII, lone surrogates.

## CLI equivalence (not the counter)

* `python3 -B cli_check.py` exit 0: manifest case exit 2 with 5 411 stdout bytes **identical**; usage exit 64 = 64; missing-file exit 2 = 2, identical stdout.
* round-41 real run (the T4 input, read-only): `python3 -B <tool> --manifest manifest.json` in `.ufo/waves/round-41/realrun` → tip41 exit 1, rewrite exit 1, both stdout sha256 `2ffbea3a8fafa3ca8d7c759acc2c6c7df9646a74c388757800f6598e9180b22e` (`cmp` identical).

## Cost (my own measurement; the counter was not run by this seat)

`python3 -B bench.py 1` exit 0 (`results/bench.txt`); child CPU user+sys, same case dir:

| shape | r40 | r41 | rewrite | r41/r40 | **new/r40** |
|---|---|---|---|---|---|
| T1-like (defect in last 64) | 0.242 | 1.329 | 0.228 | 5.49 | **0.94** |
| T2-like (valid long) | 0.241 | 0.598 | 0.295 | 2.48 | **1.22** |
| T3-like (valid 60–140) | 0.233 | 0.347 | 0.327 | 1.49 | **1.40** |
| T5-like (sitemapUrl 200 000) | 0.208 | 1.118 | 0.200 | 5.38 | **0.96** |

µs/call (tip41 / rewrite): long valid 2000 → 48.6 / **4.3**; long defect 2000 → 150.7 / **2.8**; 200 000-char defect → 14 361 / **81.8**; short real URL → 1.93 / **2.66** (fixed overhead ~0.7 µs higher per call; on T3-like the two sit inside run-to-run noise). **No counter receipt from this seat**: `c42_count.py` was never executed (seat instruction), so `equalRuns`/`ratios`/`met` for this tool are **not measured**; the L1 must score `--tool-file /fast/scratch/hyaku/kake-r42w1/ExecBuildIndependent/sitemap_audit_fast.py`.

## Findings

1. `sitemap_audit_fast.py:113` — the round-41 cost driver is the class range `\u0080-\U0010ffff`, forcing an sre BIGCHARSET (per-character range scan). Measured `_URI_RE.match` on valid values: 22.8, 23.1, 22.4, 21.5, 21.3, 20.6, 20.8 ns/char at 500…32 000 chars — **linear, ~21 ns/char**; the rewrite is 1.0–5.5 ns/char (10–20× faster). A failed match backtracks (~3× the matched cost) but never catastrophically.
2. Round-41 behaviour worth knowing (`results/probe.txt`): inside an IP-literal a `%` needs **no** triplet — the check accepts `http://[a%zz]/x` (then `urlsplit` refuses → `None`) and `http://[fe80::1%25eth0]/x` → `('http','fe80::1%25eth0',80,'/x')`; elsewhere a malformed triplet ends the value (`http://a/%zz` → `None`). A `:` before the `@` is **userinfo**, not port: `http://a:b@c/` → `('http','c',80,'/')` while `http://a@b@c/` → `None`. U+0080…U+10FFFF are unreserved anywhere (`http://a.b/c\xa0d` → `('http','a.b',80,'/c\xa0d')`) but refused inside an IP-literal (`http://[aéb]/x` → `None`). The port range is not part of the URL rule: `http://a:65536/` passes the check and is refused by `urlsplit`; `http://a:0/` → port `0`. Only the host is case-folded (`http://EXAMPLE.com/PaTh?Q=1#F` → `('http','example.com',80,'/PaTh')`); query and fragment are dropped (`http://a.b/?` → `('http','a.b',80,'/')`).
3. My own first path implementation re-scanned the path per segment (quadratic): T2-like new/r40 = 2.70 (worse than round-41's 2.31). Fixed at `sitemap_audit_fast.py:158` (one mask per region); every number above is post-fix.

## Per checked statement

* "keeps EVERY judgment of the round-41 tool" → **holds** on 1 350 327 generated values, 106 edge cases, the round-41 real run (byte-equal) — evidence, not a proof.
* "costs at most 2.0× the round-40 tool's CPU time on five input shapes" → **holds locally** on four self-generated shapes (0.94–1.40), **unmeasured** on the counter's own shapes.
* "slow on long adversarial values (backtracking)" → **overstated**: linear ~21 ns/char from the big-range class, not catastrophic backtracking (finding 1).
* "U+0080 and above stay accepted wherever unreserved is allowed" → **holds**.

Tooling: nothing installed or updated (no pacman/uv/npx/cargo); Python 3.14.8 stdlib only. No writes outside this sandbox and this report file.
