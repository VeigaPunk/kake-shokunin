CONTROL REACHES 1434/1434 — a common-character allow-list plus three delimiter counts, with no RFC 3986 grammar parse, meets the predicate on 16/16 seeds. The C1 counter does not separate this control class from the reference repair.

Sandbox S = /fast/scratch/hyaku/kake-r41w1/CtlAllowList (tools, receipts, probes). Counter sha256 2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4; oracle wheel cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917 (both from receipts).
Every tool is base.py with only `_parse_url` replaced by a gate (base.py:67-93); stdlib only. Receipts in S/out/*.json, all note=null, seed 12345 unless named (v10: out/v10_seed<seed>.json, v11: out/v11_seed<seed>.json). The receipt `misses` array is capped at 200; totals below come from `passed`.

| tool | sha256 | passed | loc | sitemapUrl | byComponent f,h,p,po,q,u (of 239) | met |
|---|---|---:|---|---|---|---|
| base.py | 4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e | 1054 | 511/630 | 543/804 | 166,160,163,239,159,167 | no |
| v1_strict.py | 41a3ea1fae288ba5ee1bbbb1de611e84c4621c83f7307193ae58b7e915f9f568 | 863 | 349/630 | 514/804 | 117,138,128,224,137,119 | no |
| v2_wide.py | 5d03ac89f274d1e61f8d20fe649ed56d2cd142a2c1b9031d44b0c0c4cbfe063d | 1309 | 566/630 | 743/804 | 217,211,214,239,210,218 | no |
| v3_pct.py | 40199f84c1edcf93329d44f1659bc541451da5e4dddf34c0265f1d8ca3bf7296 | 1358 | 589/630 | 769/804 | 216,239,224,235,220,224 | no |
| v4_pct_hash.py | c54a2d6e6e40bbde228e1a10ba3bf93bd4963182fe7e9dd032328d67d27f36b0 | 1361 | 591/630 | 770/804 | 218,239,225,235,220,224 | no |
| v5_pct_hash_at.py | 56019cd428d0ce4fc968f5b6a40a40fad1172d71252c8e35903f107171fba5c2 | 1344 | 581/630 | 763/804 | 215,236,224,234,218,217 | no |
| v6_narrow_pct_hash_at.py | 07f73ac66a60e95392dff73db10c3f82679218a4eb609796c96c24df8e84ce02 | 903 | 367/630 | 536/804 | 123,149,140,224,143,124 | no |
| v7_pct_hash_brackets.py | c18a014592181fb25ec04d24d242e7f8e04788c020d9c428ba0bbc0bce1a19df | 1432 | 629/630 | 803/804 | 239,239,239,239,239,237 | no |
| v8_pct_brackets.py | 5413b876b93456fc3063fe2cdc2a4ca7311d5a1d05f7198ec4625f932b638b42 | 1429 | 627/630 | 802/804 | 237,239,238,239,239,237 | no |
| v9_pct_hash_brackets_at.py | 1b7a8572261a8e9f30b8b411614c9c65ad0cbfe5e37200a9ee66778ba13a7041 | 1432 | 628/630 | 804/804 | 238,239,239,239,238,239 | no |
| v10_charset_netloc.py | d3113b4934639067f4a4c4952100f6f280eaf9b759f0f017398e8279015e8aa2 | 1434 | 630/630 | 804/804 | 239 each | yes |
| v11_charset_netloc_brackets.py | fbfcea92a93d37f59f6d6c94bf8b965a573a9a7d3972d54882032d58f83e738e | 1434 | 630/630 | 804/804 | 239 each | yes |

Seeds: v11 1434/1434 on seeds 1-12, 777, 12345, 424242, 20261023 (exit 0 each); v10 1434 on 12345/20261023, 1433 on 777/424242 (loc 629/630; exit 1); v7 1432/1431/1432 on 12345/777/20261023; base 1049/1041/1051/1054 on seeds 1/2/3/12345; ref_fix 1434 on 1/2/777/12345 (exit 0).

What each tool skips, and the cases that caught it (units from receipt `misses`)
- base.py — skips all URL judgment past urlsplit; 380 misses (first 200 listed are all false-valid): non-repertoire characters mid-value, bad/truncated `%` triplets, characters splitting an existing triplet.
- v1_strict — skips RFC sub-delims, brackets and percent syntax; 571 misses (200 listed): `!$'()*,;` insertions (legal in every non-port component) plus every IPv6-literal sitemapUrl.
- v2_wide — skips percent syntax; 125 misses: `%`18, `%4G`10, `%G4`10, `%2`8, `[`/`]`12, and splits.
- v3_pct — skips delimiter counts and brackets; 76 misses: 71 IPv6-literal hosts plus `@`-in-userinfo and second-`#`-in-fragment.
- v4_pct_hash — as v3 with `#`≤1; 73 misses: 71 IPv6-literal hosts plus 2 `@`-in-userinfo.
- v5_pct_hash_at — blanket `@`≤1 is wrong (a second `@` is legal in path/query/fragment); 90 misses.
- v6_narrow_pct_hash_at — strict set + pct + counts; 531 misses, dominated by legal sub-delims.
- v7_pct_hash_brackets — skips only `@` placement; exactly 2 misses, both `@` inserted in userinfo (make_url's userinfo branch, c1_count.py:126-130).
- v8_pct_brackets — v7 without `#`≤1; 5 misses (3 second-`#` in fragment/path, 2 `@`-in-userinfo).
- v9_pct_hash_brackets_at — the "/"-between-`@`s heuristic; 2 misses, both legal double-`@` values where a filled path/query supplies the first `@`.
- v10_charset_netloc — skips bracket confinement to the authority; 1 miss on 2 of 4 seeds (IPv6 host pulled into path/query by an inserted `?` or `/` in userinfo).
- v11_charset_netloc_brackets — nothing on the counter: 1434 on 16/16 seeds. It still parses no grammar: fixed charset, pct triplets, `#`≤1, one bracket pair confined to urlsplit's netloc, `@`≤1 per netloc, and urlsplit for scheme/host/port/IP-literal.

Findings
- c1_count.py:44-46,117-119,122-172 — the case space is exactly one interior insertion of one ASCII char (0x00-0x7F) or one of six pct sequences into an otherwise valid URL; no multi-character construct, no code point above U+007F.
- c1_count.py:176-180 — 6x(99+6)=630 loc and 6x(128+6)=804 sitemapUrl cases; totals match every receipt.
- c1_count.py:252-272 — judge reads only `loc_not_absolute` and `check_invalid`, so the only discriminating classes are those a single inserted character can create: the port column (already rejected by base urlsplit, base.py:73-85) and the delimiter counts.
- base.py:67-93 — accepts whatever urlsplit accepts (port validated, everything else free), 1041-1054 across seeds.
- ref_fix.py:89-108 — full RFC 3986 regex; 1434 on every seed tried.
- Probe S/adversarial.py (19 hand values): mismatches vs RFC = base 8, v1 5, v7 2, v10 1, v11 0, ref_fix 0.
- Counter blind spots, not exercised: v11 accepts `http://[fe80::1%25eth0]/x` (zone id, no RFC 3986 production; ref rejects) and rejects `http://h.example/café` (ref accepts it as an IRI); generator is ASCII-only (c1_count.py:46).

Statement checks
- "counter sha256 2acc443a…" — holds (2acc443af334…); "oracle abnf 2.9.1 wheel cdcac127…" — holds.
- "1434 cases per run, 630 loc + 804 sitemapUrl" — holds (every receipt).
- "base tool scores 1049" — overstated: seed-dependent, 1041-1054 on four seeds; 1049 is one instance.
- "reference repair scores 1434" — holds on four seeds.
- "base accepts whatever urlsplit accepts" — holds, and urlsplit (3.14) also rejects port errors and non-IP bracket literals, which is why a charset gate reaches the target.
- "the counter separates a correct repair from cheaper tools" — wrong: v11 has no grammar and meets the predicate on 16/16 seeds; the purest allow-list (v7) misses by 2 cases.

Risks
- v11 is tuned (three count rules read from the generator's shape). If the L1 classes it out, the ladder still shows a pure allow-list at 1432 (v7) and 1431 on another seed — a 2-case margin that decides the predicate (c1_count.py:364-365).
- Overlap with the sibling report w1/CtlCharsetProxy.md (independent build, same conclusion, 8 seeds); this report adds the strict-set floor (863), the `@`-per-netloc rule, and 16-seed stability.
- Scores move with the seed (base 1041-1054, v10/v11 1433-1434); a published floor should name a seed or a range.

Commands (cwd S; counter exit in comment; all `timeout 900 prlimit --as=4000000000 python3 -B <counter> --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <tool> [--seed N] --label CtlAllowList-<name> --out out/<name>.json`)
v1/v2/v3/v4/v5/v6/v7/v8/v9 seed 12345 → exit 1 each; v10 seed 12345 → exit 0, seeds 777/424242 → exit 1; v11 seeds 1-12,777,12345,424242,20261023 → exit 0; base seed 12345 → exit 1; ref_fix seed 12345 → exit 0.
Probes: `python3 -B probe.py 6` exit 0 (8604 oracle parses, 8.7 s); `python3 -B adversarial.py` exit 0.
No installs, network use, subagents, or lane/jj/index writes beyond this report. All started processes exited.
