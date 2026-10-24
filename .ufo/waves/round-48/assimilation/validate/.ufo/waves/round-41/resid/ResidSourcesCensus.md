# Residual — sources census, rows S117–S119 (KakeR41.ResidSourcesCensus, 2026-10-23)

Lane tip verified: `git rev-parse --short=12 HEAD` → `b9bf1a39362e` (expected b9bf1a39362e…). No installs made; no network used.

## 1. Census run
- `timeout 600 prlimit --as=4000000000 scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → **exit 0**, last line `ok …/corpus/SOURCES.md`.
- 11 `W04` duplicate-URL-across-scopes warnings, all informational (S033 S088 S092 S098 S099 S102 S110 S111 S115 S116 S117). S117's W04 (rfc3986.txt also in S098) is the intended split: both rows declare distinct scopes; `round-41.md` records the reject of "S098 already teaches the URI production". Script reviewed only by execution: sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`.

## 2. Registry structure
- Header (SOURCES.md:10) = 13 pipe fields = 11 columns; rows :125–:127 also 13 fields, zero empty fields. Column-by-column check below.

## 3. Rows vs retained bytes (all recomputed with sha256sum)
- Retained dir `.ufo/waves/round-41/sources/`: rfc3986.txt 141,811 B `3102dae4b68c…b2d683`; pypi-abnf.json 8,215 B `d1dab17e4879…6d10d`; pypi-rfc3987.json 9,900 B `f624f451627f…e8d2e`; fetched-at.txt `2026-10-23T09:39:11Z`. All four match `SHA256SUMS` (sha256 of the SUMS file itself `33de45de…8cba0`), the row anchors, the lessons table sizes/timestamps, and S118/S119 "retained JSON SHA256".
- **S117**: kind spec, tier A, mined, opened 2026-10-23, recheck 365d — all match lessons "admit, A, spec, mined". Anchors verified in retained text: line 867 `URI         = scheme ":" hier-part …` exact; §3.2.3 Port line 1183 and `port = *DIGIT` line 2720; §4.3 Absolute URI line 1463; Appendix A heading line 2695, URI rule line 2697 (lessons quote), ABNF block ends line 2788 (2789 blank). "(equal to S098's retained text)" holds: S098 (SOURCES.md:106) pins the identical full sha256. used-by `SCORECARD.md, corpus/lessons/round-41.md` = post-E11 form (no `"Round 41"`).
- **S118**: `info.summary` "Parsers for ABNF grammars." exact; README sentence found 1× in `info.description`; `urls[]` wheel `abnf-2.9.1-py3-none-any.whl` sha256 `cdcac127b369…0917` matches row. Vendored oracle `.ufo/waves/round-41/oracle/abnf-2.9.1-py3-none-any.whl` hashes `cdcac127b369…0917` → "byte-equal to the one PyPI publishes" **verified**. used-by files `c1_count.py`, `SCORECARD.md` exist; recheck on-release.
- **S119**: `info.summary` "Parsing and validation of URIs (RFC 3986) and IRIs (RFC 3987)" exact; wheel `rfc3987-1.3.8-py2.py3-none-any.whl` sha256 `10702b1e51e5…ce53` matches row; vendored `oracle/rfc3987-1.3.8-py2.py3-none-any.whl` hashes identically → byte-equal **verified**. used-by `oracle_crosscheck.py` exists.

## 4. Row-change log vs git
- `git diff --numstat 8eb121c8..HEAD -- corpus/SOURCES.md` → `3  0`; changed `| S` lines are exactly `+ S117, + S118, + S119`. "Row changes: S117, S118, S119 added. No `status`, `recheck` or `used-by` change to an existing row" **holds** for SOURCES.md.
- Same-round corrections (round-41.md:142–148) are all present in the final rows: S117 anchor "(lines 2695–2788)" and the lane's-observation teaches clause; S118 "valid only with an http(s) scheme and a non-empty host"; S119 "get_compiled_pattern(\"%(URI)s\").fullmatch"; all three used-by end at bare `SCORECARD.md`.

## Verdicts
- Census validate passes with exit 0: **holds** (W04 warnings informational).
- S117/S118/S119 column-by-column vs header, bytes, log: **hold** (no defect found).
- Wheel byte-equality claims: **hold** (recomputed).
- Add-only row-change claim: **holds** (git diff 3/0).

## Residual risk / gaps
- No live re-fetch (offline seat); wave-1 scout re-open results are cited, not re-executed, by me.
- The census script's internals and counter/cross-check logic are out of my scope (other seats).
