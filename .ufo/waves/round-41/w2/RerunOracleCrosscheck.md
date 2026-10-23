# RerunOracleCrosscheck — r41 wave-2 (falsify), axis: operability

Claim checked: rfc3987 1.3.8 agrees with the abnf oracle on every generated case (14,340 for v1 and v2).

## Runs (fresh seeds 42001–42010; prior runs used 41001–41010 / 41101–41110)

- `prlimit --as=4000000000 timeout 900 python3 -B .ufo/waves/round-41/oracle_crosscheck.py --seeds 42001,…,42010 --out …/x1.json` → `{"totalCases": 14340, "totalDisagree": 0}`, **exit 0**.
- Same + `--counter .ufo/waves/round-41/c1_count_v2.py` → `{"totalCases": 14340, "totalDisagree": 0}`, **exit 0**.
- Counter shas in my outputs match the scorecard-cited files: v1 `2acc443a…`, v2 `53a0ec1b…`; rfc3987 wheel `10702b1e…ce53`, abnf wheel `cdcac127…` — all verified by sha256sum.

## `fullmatch` (oracle_crosscheck.py:33-37)

- `get_compiled_pattern("%(URI)s")` is an **unanchored** template; `.fullmatch` anchors it `\A…\Z`. Correct and stricter than rfc3987's own `match()` which wraps `'^%(rule)s$'` (wheel source confirmed) — `$` admits a trailing `\n`. Spot test: `second("http://a.com/x\n")` → False. Correct.
- `rfc3987.parse(rule="URI")` at :38 internally re-matches with `^…$`, so it is only reached on already-fullmatched input — the `$` newline hole is dead code here. No defect.
- Host extraction (:41-49): `rpartition("@")` strips userinfo; `[`-branch keeps the whole IP-literal; `partition(":")` splits the port. Spot tests OK: `http://u:p@a.com:80`, `http://[2001:db8::1]:81/x`, `http://[v7.aB]:80/x` all → True; `http:///x`, `http://user@/x` → False; `ftp://` → False. Matches the abnf wrapper's scheme/authority/non-empty-host checks (c1_count.py:81-93).

## loc-strip handling (oracle_crosscheck.py:55)

- `.strip(" \t\r\n")` applied iff `field == "loc"` — exactly contract sentence 21's XML whitespace set {U+0020,U+0009,U+000D,U+000A}; `sitemapUrl` unstripped, matching sentence 4 (judged as written). Correct.
- v2 parity: c1_count_v2.py:210-213 labels `valid(strip)` for loc — crosscheck applies the identical strip, so both sides judge the same string.
- v1 note (informational, not a defect): c1_count.py:183 labels `valid(value)` **unstripped** while the crosscheck feeds `second()` the stripped value. In v1's space this is harmless: `insert` (c1_count.py:117-119) uses `randint(1, len(text)-1)` — strictly interior — and every component is non-empty, so no generated value can carry boundary whitespace; strip is a no-op on all v1 cases. It means the v1 crosscheck never exercises the strip path, but no mislabel can result. v2's `insert` uses `randint(0, len(text))` (c1_count_v2.py:123), so boundary whitespace does occur (e.g. end of fragment) and both sides strip identically.

## Findings

- No defects found. One informational asymmetry above (v1 labels unstripped; inert because v1 never generates boundary whitespace).
- Spot-check script (9 edge cases incl. trailing-LF rejection, empty host, userinfo-only authority, IP-literal/IP-future) all behaved as the abnf oracle requires.

## Verdict

- "Second oracle agrees on 14,340/14,340 v1 cases": **holds** (replicated, fresh seeds, exit 0).
- "Second oracle agrees on 14,340/14,340 v2 cases": **holds** (replicated, fresh seeds, exit 0).
- Residual risk: agreement is only over the generator's unit-insertion space; oracles could still diverge on inputs outside it (none observed in 28,680 fresh cases).

No tools installed; standard library only. Outputs: /fast/scratch/hyaku/kake-r41w2/RerunOracleCrosscheck/{x1,x2}.json
