CONTROL REACHES 1434/1434 — a charset proxy plus three delimiter-count rules, with no component grammar, meets the predicate on 8/8 seeds. The C1 counter is too weak as written.

Built (Python 3 stdlib only, one gate inserted into base.py `_parse_url`; sandbox /fast/scratch/hyaku/kake-r41w1/CtlCharsetProxy/)
- charset_plain.py — sha256 0bbf59740e17b76e3529eb70c0f02154b742354ff8814c526e6fcac0d67c20ca — base + repertoire rejection (charset_plain.py:71-82).
- charset_pct.py — sha256 c2e1f14d5298a9fe484438f853b64d946e46cdce4683f045aeb5ec8fd909181a — + a "%" not starting two hex digits is rejected (charset_pct.py:75,78-84).
- charset_pct_rules.py — sha256 f5d433a06c665eb8e068186c6d0087106fdf2de7b97d8554e8152f0b9ebeaf6e — + three count proxies, still no component grammar (charset_pct_rules.py:87-109): at most one "#"; at most one "@" before the authority ends; one balanced "[".."]" pair inside the authority.
- probe/matrix.py — 27 hand values, labels from the counter's own oracle (c1_count.load_oracle), tool verdicts from each module's `_parse_url`.

Commands (all: `timeout 900 python3 -B .ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <tool> [--seed N] --label <l> --out <json>`; counter sha256 2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4)
- charset_plain, EXIT 1 · charset_pct seeds random/41/777/101, EXIT 1 · charset_pct_rules seeds random/41/777/101/202/303/404/505, EXIT 0 · ref_fix seed 101, EXIT 0 · base seeds random/101, EXIT 1 · probe/matrix.py, EXIT 0.

Counter results (byComponent order: fragment/host/path/port/query/userinfo; receipts in out/*.json)
| tool | seed | passed | loc | sitemapUrl | byComponent | met |
| base.py | 101 | 1037 | 503/630 | 534/804 | 156,159,161,237,161,163 of 239 | no |
| base.py | 90146066088948 | 1065 | 516/630 | 549/804 | 161,167,166,239,166,166 | no |
| charset_plain | random | 1295 | 562/630 | 733/804 | 205,216,214,238,211,211 | no |
| charset_plain | 101 | 1292 | 558/630 | 734/804 | 207,210,212,237,212,214 | no |
| charset_pct | random | 1417 | 621/630 | 796/804 | 233,239,235,239,235,236 | no |
| charset_pct | 41 | 1416 | 620/630 | 796/804 | 234,238,235,238,234,237 | no |
| charset_pct | 777 | 1413 | 619/630 | 794/804 | 233,237,235,238,236,234 | no |
| charset_pct | 101 | 1414 | 619/630 | 795/804 | 233,237,234,237,237,236 | no |
| charset_pct_rules | random,41,777,101,202,303,404,505 | 1434 (all 8) | 630/630 | 804/804 | 239 each | yes |
| ref_fix | 101 | 1434 | 630/630 | 804/804 | 239 each | yes |

What each tool skips, and the cases that caught it
- base.py: skips every judgment past urlsplit; 397 cases (seed 101) catch it — the 43 chars outside the RFC 3986 repertoire (space, `" < > \ ^ ` { | } DEL`, C0) mid-value, bad/truncated `%` triplets, and a letter or sign inserted between a "%" and its two hex digits. base.py:67-72 (shared copy) rejects only a leading space/control plus tab/CR/LF.
- charset_plain: skips the pct-encoded rule; 142 cases (seed 101) catch it — `%`, `%2`, `%4G`, `%G4` and any char that splits an existing triplet (`%m41`).
- charset_pct: skips per-component placement of gen-delims. Every run generates 12 `[`/`]`-in-path/query/fragment cases, 2 `"@"`-in-userinfo cases and 2 second-`"#"`-in-fragment cases, none of which a repertoire/triplet test can see (only an insertion that splits an existing `%XX` triplet hides one). Seed extras: `#` in host/port/userinfo when a fragment already exists, and `]`/`?` in userinfo when an IPv6 host puts a bracket pair in the netloc. Measured 17/18/20/21 misses (1417/1416/1414/1413), so it cannot reach 1434.
- charset_pct_rules: nothing on the counter, so 1434. It still skips host IP-literal grammar (`http://[fe80::1%25eth0]/x`: oracle false, ref_fix false, rules true) and raw non-ASCII (`http://h.example/café`: oracle false, every tool incl. ref_fix true) — no generated case exercises either.

Findings
- c1_count.py:45-47,117-119,176-183 — the case space is one interior insertion of one ASCII char or pct sequence per component; no multi-character construct and no code point above U+007F.
- c1_count.py:252-272 — `judge` reads only `loc_not_absolute` and `check_invalid`, so a tool that rejects broadly/shallowly is measured only where a single character lands.
- c1_count.py:364-365 — `met` is exactly 1434/1434, no margin, so one structural miss class decides the predicate.
- ref_fix.py:89 — accepts U+0080+ as IRI characters; the oracle labels them invalid, so the 1434 predicate holds only because the generator is ASCII-only, not because the repair is grammar-complete.

Statement checks
- "1434 cases per run, 630 loc + 804 sitemapUrl" — holds (receipt byField totals; c1_count.py:177-178).
- "one inserted ASCII character or percent sequence in one of six components" — holds, restricted to a single interior insertion (c1_count.py:117-119).
- "base tool scores 1049" — overstated: seed-dependent, measured 1065 and 1037 on two seeds; 1049 is one instance, not a property.
- "ref_fix scores 1434" — holds on seed 101.
- "the predicate separates a correct repair from cheaper tools" — wrong: charset_pct_rules has no component grammar, accepts a value ref_fix rejects, and meets the predicate on 8/8 seeds.

Risks
- charset_pct_rules is not a pure repertoire test: it adds three delimiter-count proxies. If the L1 classes it out, the measured ladder is still 1292 → 1414 → 1434, and charset+pct stays below 1434 because its residual misses are all delimiter-placement classes it cannot see (best observed 1417; 1413-1417 over four seeds).
- base/plain/pct scores move with the seed (base 1037-1065, pct 1413-1417); any published floor should name its seed or a range.

Blockers: none. No subagent spawn key is present in this seat, so all work was done in-seat. Tool installs: none.
