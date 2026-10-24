# CtlGeneratorShape — the counter DOES score a generator-template recognizer at 1434/1434
FINDING FIRST: `v1_shape.py` reaches **1434/1434, met=true** while doing no RFC 3986 path/query/fragment grammar work. It does not repair URL judgment; it recognises the counter's own `make_url` template. The counter therefore cannot separate the claimed repair from this cheaper tool on the generator's distribution.
Axes: operability measured (counter behaviour); freshness unchanged, unmeasured. No round verdict.
Sandbox S = `/fast/scratch/hyaku/kake-r41w1/CtlGeneratorShape`. Counter sha256 `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4`; base `4de35f8c…460e`; ref_fix `6d7c2dd4…010a`.

## Tools (all standard-library only, derived from `shared/base.py` by replacing `_parse_url` only)
- `/fast/scratch/hyaku/kake-r41w1/CtlGeneratorShape/v1_shape.py` sha256 `a26808695f09a20d6e7888065bb76cd02161e18c7e5a6347bb1b5735a9b769ee` — the shape route.
- `v0_flat.py` sha256 `5744bfa8acf501c588741ac0bad449bbde81a0d7e0ba444cdfb5a4811821ef3f` — flat ablation, no authority model.
- `v1_noport.py` sha256 `83a93d8976730d304b8ce824c71994282bd20e9f11ff49900f6237f8d4ce47b8` — v1 minus the digit-only port rule.
- `v1_noipv6.py` sha256 `0175d6adbe82f822693058b6d282137e433865185d094e759154134e0478fd75` — v1 minus the `[2001:db8::hex]` host template.

## What `v1_shape.py` judges on (paths relative to S)
`v1_shape.py:67-82` declares the skip: the generator's six-component single-insert template. `:81-149` is the whole judgment: scheme marker, every `%` must open a triplet (`:97-102`), a global character repertoire `_SHAPE` (`:76`, `:103-105`), at most one `#` (`:95-96`), authority split at one `@` with a userinfo repertoire (`:114-121`), then either the literal `_IPV6_HOST` regex (`:125-131`) or `host[:digits]` (`:133-141`). No path, query or fragment production is validated; no IP-literal other than `2001:db8::` is understood; an empty port is rejected.

## Exact detector commands and results (each `cd S`, `timeout 900 prlimit --as=4000000000 python3 -B …/c1_count.py --root …/kake-shokunin --tool-file S/<tool> --seed <seed> --label <l> --out S/<receipt>`)
| Tool | Seed | Exit | passed | byField loc/sitemapUrl | byComponent frag/host/path/port/query/userinfo | met |
|---|---:|---:|---:|---|---|---|
| v1_shape | 41001 | 0 | 1434/1434 | 630/630, 804/804 | 239,239,239,239,239,239 (all /239) | true |
| v1_shape | random | 0 | 1434/1434 | 630/630, 804/804 | all 239/239 | true |
| v0_flat | 41001 | 1 | 1269/1434 | 546/630, 723/804 | 236,233,236,93,237,234 | false |
| v1_noport | 41001 | 1 | 1305/1434 | 564/630, 741/804 | 239,237,239,112,239,239 | false |
| v1_noipv6 | 41001 | 1 | 1375/1434 | 601/630, 774/804 | 224,239,229,237,220,226 | false |
Receipts: `v1_shape-s41001.json`, `v1_shape-random.json`, `v0_flat-s41001.json`, `v1_noport-s41001.json`, `v1_noipv6-s41001.json`. All report `toolExit=2` (generated manifests contain invalid `sitemapUrl` checks → `check_invalid` → the audited tool's `EXIT_CANNOT`); counter exit is the table's Exit column.
Stability (unseeded draws, same command, `--seed` omitted): `v1.json` and seeds 1–5 all 1434/1434, byField 630/630 + 804/804, met=true (receipts `v1.json`, `v1-s1..s5.json`). Offline cross-check over the generator's distribution: 40 seeds × 1434 = 57,360 cases, `c1_count.generate` vs vendored oracle vs `v1_shape._parse_url`, **0 disagreements** (timeout 600, exit 0).

## Which cases caught which tool
- `v1_shape.py` — skips path/query/fragment grammar, real IP-literals and empty ports. **No case caught it (1434/1434).**
- `v0_flat.py` — skips the whole authority skeleton. Caught by 165 cases on seed 41001 (`v0_flat-s41001.json` `misses`, complete at 165): port 146 (every non-digit unit except the pct ones its `%` rule already rejects, e.g. `Https://2r7WJQ=9s.com:4u0/…` port `u`, `HTTP://fuozr%0c.test:7%414/…` port `%41`), 20 brackets across port/host/path/query/fragment/userinfo (`HTTP://4[2Kq%3ex$NZp.example/…` host `[`), host `:` 2, userinfo `@` 1.
- `v1_noport.py` — skips the port grammar. Caught by 129: 127 port, 2 host (port/bracket interaction).
- `v1_noipv6.py` — skips IP-literal hosts. Caught by 59, spread across fragment 15, query 19, userinfo 13, path 10, port 2, host 0 — every otherwise-valid case whose host is the generator's IPv6 template.

## Checked statements
- WRONG (as a separation claim): "the counter separates a correct URL-validation repair from cheaper tools". A template recogniser that never judges path/query/fragment grammar scores 1434/1434 on every seed tried.
- HOLDS: the counter is not vacuous — it kills the flat recogniser (1269) and both ablations (1305, 1375); the port bucket alone contributes 146 misses for `v0_flat.py`.
- HOLDS: `v1_shape.py` is not an RFC 3986 judge, measured against the same oracle. It accepts RFC-invalid `https://[2001:db8::00000]/x` (5-hex group) and `https://[2001:db8::12345]/x`, and rejects RFC-valid `https://host:/x` and `https://[::1]/x`.
- HOLDS: the counter reads only the invalid/valid bit (`c1_count.py` `judge`), so shape-matching and grammar-judging are indistinguishable to it wherever they agree.
- Cause, with path:line — `c1_count.py:120-163` (`make_url`/`insert`) splices exactly one unit at an interior position of one component, so the un-inserted value is always generator-valid and every case is decidable from the one unit plus `c1_count.py:47-56` repertoires; `c1_count.py:157-160` fixes the IPv6 host to `[2001:db8::hex]`.
- Note for L1: `v1_shape.py:99-102` re-checks pct-triplet adjacency from the string, not from a table; that one rule is what makes `%`/`%2`/`%4G`/`%G4` land correctly in the port and host shifts.

## Risks / bounds
Risks: `v1_shape.py` is tuned to this generator (IPv6 template, interior insert, ASCII repertoire); a generator change that admits real-world URL shapes breaks it, and `v1_noipv6` shows sensitivity. Its returned `host`/`port`/`path` are shape-derived, so non-judged findings such as `loc_out_of_scope` can differ from a real repair even where the invalid/valid bit agrees (`v1_shape.py:142-149`); the counter never reads them. A control that reaches the target means the round-41 claim as worded ("agrees with the RFC 3986 URI oracle on 1434 of 1434 generated cases") is satisfiable without the named work; the L1 decides redesign vs exploratory.
No lane, jj or shared-file writes; read-only `git`/wheel use only. No network, no installs, no subagents, no background jobs left running. Only `chmod u+w` on my own copies (the copied `base.py` is read-only, first edit hit EACCES).
