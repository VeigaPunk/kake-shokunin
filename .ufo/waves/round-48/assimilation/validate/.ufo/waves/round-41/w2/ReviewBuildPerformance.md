# Round 41 w2 — build regex run time on long and adversarial values

Seat KakeR41.ReviewBuildPerformance (leaf). Item: time `_URI_RE`/`_parse_url` on 2,047-char backtracking `loc`
values and on 50,000-entry sitemaps. Build `scripts/sitemap_audit.py` sha256 `0b485431…13edbf`; base from
`8eb121c8` sha256 `4de35f8c…1460e` (both re-hashed in my sandbox). No install.

**Checked.** 20 shapes at 2,047 chars (`%` runs, `%41`, `%2G`, `@`, `:`, sub-delims, `[`/`]`, digits, dots, `?`,
`#`, space, userinfo/host splits) as `loc` and (several) as manifest `sitemapUrl`, incl. 200,000 chars; two
50,000-entry sitemaps (4.2 MB valid; 37 MB rotating 700-ch adversarial); a 52.4 MB and a 30 MB file at the byte
cap / one loc; the round-39 real run. Grammar correctness not inspected — other seats.

**Commands** (all `timeout ≤850 s`, `prlimit --as=4000000000`, ≤8 procs, exit 0): `git show
8eb121c8:scripts/sitemap_audit.py`; `gen.py`/`gen.py big`/`gen_worst.py`; `runner.py` (min of 7, whole process);
`inproc.py` (min of 5, CPU); `scale.py`+`probe2.py`–`probe5.py` (slopes); `onelen.py L` ×7 fresh processes;
`huge.py`; `hyperfine --shell=default --runs 3`.

| Input | base | build | × |
|---|---|---|---|
| 1 loc 2,047 ch, early reject (`%` run, `#` run, `[`) | 0.049 ms | 0.050 ms | 1.03 |
| 1 loc 2,047 ch, valid `%41` path | 0.050 ms | 0.121 ms | 2.5 |
| 1 loc 2,047 ch, worst (`/`+`a`×2045+`%`) | 0.046 ms | 0.226 ms | 4.85 |
| 1 `sitemapUrl` 200,000 ch, worst shape | 0.312 ms | 12.419 ms | 39.8 |
| 50,000 entries, ~100-ch valid locs (4.2 MB) | 287.8 ms | 250.3 ms | 0.87 |
| 50,000 entries, 700-ch adversarial (37 MB) | 248.6 ms | 759.3 ms | 3.05 |
| 37 MB file, wall, hyperfine | 0.242 s | 0.670 s | 2.8 |
| 25,327 × 2,047-ch worst, 52.4 MB (cap) | 164.2 ms | 2332.5 ms | 14.2 |
| 52.4 MB file, wall, hyperfine | 0.191 s | 2.213 s | 11.6 |
| 1 loc of 30,000,000 ch | 59.7 ms | 710.7 ms | 11.9 |
| round-39 real run (6 sitemaps) | 236.5 ms | 288.7 ms | 1.22 |

**Super-linearity: none found.** Median log₂ slope per doubling, 1 KB→64 KB, is 0.95–1.07 on all 25 shapes; the
`%`-run, `#`-run and `[`-run shapes fail at the first bad character and stay O(1) (1.2–2.2 µs at every length);
cost at 2,048 ch is 0.6–46 ns/char. One reproducible discontinuity, not growth: per-char cost steps ~3× once the subject
passes 128–192 KB and is flat to 1 MiB (fresh processes: 12.7, 12.7, 39.1, 40.2, 41.3, 42.3, 38.2 ns/char at
64 K/128 K/192 K/256 K/384 K/512 K/1 M), while `\A[a]+\Z` and `str.count` controls stay 0.12–0.23 ns/char at all
lengths. The engine is O(n) with a size-dependent constant; no shape makes it quadratic.

**Findings.**
1. `scripts/sitemap_audit.py:77-86` — `_URI_RE` linear per above. Severity: informational.
2. `scripts/sitemap_audit.py:89`, `:306-308` — `_parse_url` adds 0.003–0.18 ms per 2,047-ch value, capped at
   ≈0.23 ms by the 2048-codepoint bound. Severity: low.
3. `scripts/sitemap_audit.py:306-308` — `_audit_loc` still calls `_parse_url` after recording `loc_too_long`, so
   an oversized value is parsed at full cost: one 30 MB loc = 711 ms vs 60 ms (≈1.1 s at the 52 MB cap); the
   length finding is already reached, so a short-circuit would cap it. Severity: low (bounded, crafted).
4. `scripts/sitemap_audit.py:382` — manifest `sitemapUrl` is unbounded (`_load_manifest` reads the file
   unchecked), so the regex runs once on an unbounded value: 200,000 chars = 12.4 ms (×39.8 base), linear.
   Severity: informational.
5. Sample sizing — 50,000 × 2,047-ch locs is ≈103 MB > `MAX_BYTES` 52,428,800 (`:28`), so a worst-shape file
   holds only 25,327 such entries; the 50,000-entry runs use shorter values. Severity: informational.
6. Ordinary load — 50,000 valid ~100-ch locs: build 13% faster (base does four Python scans per value); real
   run: +52 ms (×1.22). Severity: informational.

**Per checked statement.**
- "Run time of the build's regular expression on long and adversarial values": no super-linear case; worst
  absolute 2.21 s on a crafted 52.4 MB sitemap and ≤0.23 ms per 2,047-ch value — **holds** (linear).
- Read as a repair with no operability cost — **overstated**: ×3.05 on a 50,000-entry adversarial file,
  ×11.6–14.2 on a crafted 52 MB file, ×39.8 on a 200,000-ch `sitemapUrl`. No round statement is **wrong**.

**Risk/blocker.** None: runs bounded (max 2.4 s), RSS 177 MiB at the byte cap, 120 MB written to the sandbox, no process left.
