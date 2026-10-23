SURVIVED: 2 of 6 scope/directory one-member mutants (m4 port-ignoring scope tuple, m5 empty-path default removal) survive counter v4 at 11/11 met; m1, m2, m3, m6 killed.

# Scope
Build under attack: `scripts/sitemap_audit.py@020bc4574729ed674299f6cab02faac1582d9464`, copied read-only to
`/fast/scratch/hyaku/kake-r43/MutBuildScope/build.py`, sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` (matches C1 target).
Counter: `.ufo/waves/round-43/c43_count_v4.py` sha256 `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab`. Reference `ref41.py` = `1ef7a0e95f6884dd113fe583a997c633fe330ddd:scripts/sitemap_audit.py`, sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`.
Commands (all `timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-43/c43_count_v4.py --root .../kake-shokunin --tool-file <f> --label MutBuildScope-<x> --out <x>.json`, no --seed):
base exit 0 (met 11/11, ratios T1-T5 1.028/1.218/1.321/1.258/1.156); m1 exit 1; m2 exit 1; m3 exit 1; m4 exit 0; m5 exit 0; m6 exit 1; restored exit 0 (11/11, 1.041/1.248/1.247/1.254/1.134).
Witness commands: `python3 -B <tool> --manifest w{1,2,3}/w{1,2,3}.json`, exit codes below.

# Mutants (one member each; line refs to scripts/sitemap_audit.py@020bc45)
| id | sha256 | change | receipt equalRuns/met | verdict |
|---|---|---|---|---|
| m1 | 30d423c0b17d98a49afcbe2c0416a0cc540af8cb373a440d38eaafacb3549823 | :311 `rfind("/")` -> `find("/")` (first-slash dir; leading slash makes prefix "/") | 9/11, met false | KILLED (run F + T2, candRepsEqual 0/5) |
| m2 | 38fddffe46a7c544dd043b4258114c56055e5b212f299f1319828d66804a7653 | :314 `path[: cut + 1]` -> `path[:cut]` (dir without trailing slash) | 10/11, met false | KILLED (run F only) |
| m3 | 1a49e9e4e68792f10ae77849ffb32e3ff1aea268bc559131ae36e5465199f47c | :515 case-sensitive `startswith` -> `.lower().startswith(prefix.lower())` | 9/11, met false | KILLED (run F + T2, candRepsEqual 0/5) |
| m4 | 272d02127daa0b6f35d29957b3ebb16a91a10ab01a73f3a10a3c28814de5412e | :510 `parsed[:3] != sitemap_url[:3]` -> `parsed[:2] != sitemap_url[:2]` (port dropped) | 11/11, met true | SURVIVED |
| m5 | 870ba78489282ef8966c90e1ea87ce304b507715c10959a833393917dda89f4d | :305 `path = parts.path or "/"` -> `path = parts.path` | 11/11, met true | SURVIVED |
| m6 | 8ebd6010f589ca6bb65f3765f01917408c3f42b4815d60e0f4c480a1c5760f16 | :515 `not X.startswith(prefix)` -> `X != prefix` | 3/11, met false | KILLED (A,B,C,D,E,F,T2,T4) |

Receipts: `/fast/scratch/hyaku/kake-r43/MutBuildScope/{base,m1,m2,m3,m4,m5,m6,restored}.json` (one per scored file).

# Survivor witnesses (differ from the round-41 tool)
- m4, `w1/`: loc `https://w.test:8443/page`, sitemapUrl `https://w.test/sitemap.xml`. ref41 exit 1 `loc_out_of_scope entry 1`; build exit 1 same; m4 exit 0 `clean` (port ignored).
- m5, `w2/`: loc `https://w.test` (empty path), sitemapUrl `https://w.test/`. ref41 exit 0 `clean`; build exit 0 same; m5 exit 1 `loc_out_of_scope entry 1`.

# Killed-mutant witnesses (`w3/`: 4 locs, 4 checks)
ref41 and build agree, exit 1: c1 entries 1-4, c2 1-2, c3 1-4, c4 1-2 flagged out_of_scope.
- m1 exit 0, all checks clean (prefix collapses to "/").
- m2 exit 1; c2 and c4 flag only entry 1: `/dirx/page` wrongly in scope under prefix "/dir".
- m3 exit 1; c3 flags 1-2 only: `/dir/page` wrongly in scope under "/Dir/" (case-folded compare).
- m6 exit 1; c4 flags 1-4: `/dir/page` wrongly out of scope (equality instead of prefix).

# Findings
- C1 counter coverage: port (not exercised as a scope discriminator) and empty-path locs are blind spots; 2/6 mutants survive at 11/11. Coverage finding only, not a contract change.
- C1 target claim "met on three independent os.urandom seeds": holds; a fourth fresh-seed scoring (`base.json`, 11/11) also met.
- Statement that the counter kills scope/directory mutants is overstated for m4/m5 classes.
- Conformance: `020bc45` is an ancestor of freeze tip `b49cba9` and both carry blob `21553d19...` for `scripts/sitemap_audit.py`, so the attacked build is the tip's script; all probes ran after the freeze. No seat-score-predating-freeze evidence seen.
- Restored/pristine bytes: `build.py` sha256 unchanged `914ebdee...cd021` before and after; restored scoring exit 0, 11/11 met. No files mutated in the lane; all writes under the sandbox. No tool installs.
