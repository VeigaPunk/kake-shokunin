KILLED: counter v4 kills 3 of 6 single-member host-handling mutants of the round-42 build (reg-name class, userinfo class, trailing-dot host); the 3 survivors are CLI-equivalent, not detection gaps.

# MutBuildHost — round 43 wave 1 (operability lane)

Baseline: `git -C <lane> show 020bc4574729ed674299f6cab02faac1582d9464:scripts/sitemap_audit.py` (read-only) -> /fast/scratch/hyaku/kake-r43/MutBuildHost/build.py, sha256 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021 (matches frozen build / freeze receipt toolSha256). ref41 extracted from 1ef7a0e9 -> ref41.py, sha256 50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d (matches counter REF41_SHA).

## Commands (all exit codes recorded)
- pristine: `timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-43/c43_count_v4.py --root <lane> --tool-file <scratch>/build.py --label MutBuildHost-pristine --out <scratch>/pristine.json` -> exit 0, met true, equalRuns 11/11, seed 140863020759105, max ratio 1.281.
- m1..m6: same command with `--tool-file <scratch>/mN.py --label MutBuildHost-mN --out <scratch>/mN.json` (no --seed). Exit 1 for m1,m2,m5; exit 0 for m3,m4,m6.
- witness: `timeout 300 python3 -B witness.py` -> exit 0 (300 runs, <3 s).
- function probe: inline import of build.py/m3.py/m4.py/m6.py (read-only) -> exit 0.

## Mutants (one source site each; diff -u build.py mN.py has exactly one changed line)
| # | change (line) | sha256 | equalRuns | met | differing runs | verdict |
|---|---|---|---|---|---|---|
| m1 | `_REGNAME_ASCII` drops `b"%"` (121) — class member | 835412de2b47440dffaade671e4ba03965aa1af6bcbe806c66c0cdfc45e6b174 | 6/11 | false | A,D,E,F,T3 | KILLED |
| m2 | userinfo scan `_TABLE_USERINFO` -> `_TABLE_REGNAME` (275) — class member | 86bd72a3e90fdc1a90e0702720280f0a3c8fe9f63afb5d35c67b0e844cdd46cd | 8/11 | false | A,D,E | KILLED |
| m3 | `if at == host_start` -> `if at < host_start` (194) — empty reg-name boundary | 9c466c35663cf30ecda1d6d4c64a99faa452ccdf8adbc513b7bc3e0716613db0 | 11/11 | true | none | SURVIVED (masked) |
| m4 | `if not host` -> `if host is None` (298) — empty-host branch | f72d6df794d1c256bef383900879ac29d9472c60b2552747622cdf82cad11bc6 | 11/11 | true | none | SURVIVED (masked) |
| m5 | reg-name rejected when `raw[at-1] == 0x2E` (194) — trailing-dot boundary | ba783b8c55d41f17d18c99a6177cd164380c15d276158a392fff2920102259c9 | 10/11 | false | D | KILLED |
| m6 | `host.lower()` -> `host` (306) — reg-name case fold removed | 7ef56aa93c6774eaafee3eadf17b2fd8031f243f34240c46faba53c21933f0eb | 11/11 | true | none | SURVIVED (redundant) |

Receipts (one per scored mutant, seeds recorded): <scratch>/{pristine,m1,m2,m3,m4,m5,m6}.json. Seeds: m1 160084383580424, m2 42836773278835, m3 183305686870391, m4 92936064348956, m5 171472619553063, m6 196492474382206. Max timing ratio over all receipts 1.364 (< 2.0), so kill/no-kill is by output equality, not timing.

## Witness values (ref41 = build = round-41 behaviour; mutant differs)
- m1: sitemapUrl `http://ex%41mple.com/sitemap.xml` -> ref41 exit 0 `clean` (sha f42282003a504032), m1 exit 2 `could-not-evaluate`, check error `check_invalid` (sha 2fd1409a6c89d49b).
- m2: sitemapUrl `https://user:pw@example.com/sitemap.xml` -> ref41 exit 0 clean, m2 exit 2 check_invalid.
- m5: sitemapUrl `http://example.com./sitemap.xml` -> ref41 exit 0 clean, m5 exit 2 check_invalid.
- Survivors: no witness exists. m3 flips `_uri_ok` only on empty-host values (`http:///x`, `http://@/x`, `http://:80/x`, `http://u@:/x`: build False / m3 True), but every one is then rejected by the intact `if not host: return None` (m4's site), so CLI output is identical. m4's `hostname == ""` branch is unreachable once `_uri_ok` requires a non-empty reg-name (build and m4 both `_parse_url('http:///x') -> None`). m6 is equivalent because `urlsplit(...).hostname` already lowercases (`http://ExAmPle.COM/x` -> `example.com` in both) — witness `http://ExAmPle.COM/sitemap.xml` gives identical output for ref41/build/m6, so case folding is exercised but the `.lower()` call itself is dead.

## Findings, per checked statement
- C1 output-equality arm covers host handling where behaviour is observable: reg-name character class, userinfo character class and trailing-dot hosts all produce counter-visible divergence. Holds for those three.
- Trailing-dot host rejection (m5) is caught by run D alone (1/11 runs); the counter's dedicated repetition classes F and the common-host basket never emit a trailing dot. Thin, but a kill: covered.
- Empty-host and reg-name case lines are double-guarded or redundant; no counter, however generated, can distinguish them through the CLI. Not a counter weakness; the two guards (m3 site and m4 site) are behaviourally interchangeable, so one is dead weight in the frozen build. Maintenance note only, nothing about C1 changes.
- No seat-score-before-freeze evidence was touched; no conformance defect observed in the paths I read.
- Statement "build met" restated: pristine scored true with my own run (11/11, seed 140863020759105), independent of the freeze receipts.

## Restoration / bounds
- build.py never mutated: sha256 after all runs still 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021.
- No lane file written; only `git show` reads in the lane. All writes confined to /fast/scratch/hyaku/kake-r43/MutBuildHost/ (7 receipts, logs, witness dir with 6 manifests, ~1 MB total). All runs `timeout`+`prlimit --as=8000000000`; max 3 counter processes at once; no process left running.
- Tools installed/upgraded: none.
