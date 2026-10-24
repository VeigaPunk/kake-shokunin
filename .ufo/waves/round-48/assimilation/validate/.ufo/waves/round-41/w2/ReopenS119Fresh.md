# ReopenS119Fresh — row S119 (rfc3987 1.3.8)

Axis: freshness. No packages installed. Sandbox: `/fast/scratch/hyaku/kake-r41w2/ReopenS119Fresh/`.

## Commands (exit codes)

1. `timeout 60 prlimit --as=4000000000 curl -fsS -D headers.txt -o pypi-rfc3987-live.json -w 'http_code=%{http_code} size=%{size_download}\n' https://pypi.org/pypi/rfc3987/1.3.8/json` — exit 0. HTTP 200, 9900 bytes. Response `Date: Fri, 23 Oct 2026 10:08:39 GMT`.
2. `sha256sum` of that file, `.ufo/waves/round-41/sources/pypi-rfc3987.json`, and `.ufo/waves/round-41/oracle/rfc3987-1.3.8-py2.py3-none-any.whl` — exit 0.

Live JSON sha256 `f624f451627f0d5db519d7e32b72ab4bc8576c88247b180ee363dff8932e8d2e` equals the retained file (SOURCES.md:127). Wheel sha256 `10702b1e51e5658843460b189b185c0366d2cf4cff716f13111b0ea9fd2dce53`.

abnf facts below are from the vendored wheel and retained `sources/pypi-abnf.json` (not re-fetched; this item names only the rfc3987 URL).

## Clauses

**Summary quote — holds.** Live `info.summary` is exactly `Parsing and validation of URIs (RFC 3986) and IRIs (RFC 3987)` (no trailing period). Same string in the wheel `rfc3987-1.3.8.dist-info/METADATA` Summary and `rfc3987.py:20` (docstring adds a period). SOURCES.md:127 anchor matches.

**Digest — holds.** Live `urls[]` wheel `rfc3987-1.3.8-py2.py3-none-any.whl` `digests.sha256` is `10702b1e51e5658843460b189b185c0366d2cf4cff716f13111b0ea9fd2dce53` (upload `2018-07-29T17:23:45.313143Z`, size 13377, not yanked). `sha256sum` of the vendored wheel is that digest. SOURCES.md:127 and SCORECARD.md:2710–2711 (`10702b1e…ce53` = PyPI digest) match. `oracle_crosscheck.py:15` pins the same digest.

**"written independently of abnf" — holds** (authors, dates, licences; inference, not a PyPI sentence).

| | rfc3987 1.3.8 | abnf 2.9.1 (S118) |
|---|---|---|
| Author | Daniel Gerber, `daniel.g.gerber@gmail.com` (JSON `info.author`; `rfc3987.py:4` "Copyright (c) 2011 Daniel Gerber.") | Charles Yeomans, `charles@declaresub.com` (retained JSON `info.author_email`; wheel METADATA Author-email) |
| Licence | `GNU GPLv3+`; classifier GPLv3+ (`rfc3987.py:6-9`) | MIT; `LICENSE.txt:1` "Copyright 2020 Charles Yeomans" |
| Date | copyright 2011; this file uploaded 2018-07-29 | copyright 2020; 2.9.1 uploaded 2026-10-21T19:34:52Z (retained JSON) |
| Home | `https://github.com/dgerber/rfc3987` | `https://github.com/declaresub/abnf` |

`rfc3987.py` has no `abnf` token (archive search, no matches) and does not import that package. Its 2011 copyright predates the abnf wheel's 2020 copyright, so 1.3.8 cannot have been written against abnf 2.9.1 or any release under that licence notice. Both still implement the same RFCs; the row's scope already says it is not a statement of either RFC.

**Adjacent, same teaches cell — wrong (low).** SOURCES.md:127 says the cross-check compares `match(value, rule="URI")`. `oracle_crosscheck.py:33-38` calls `get_compiled_pattern("%(URI)s").fullmatch` and `parse(value, rule="URI")`, and line 36 says it avoids `match` because `$` admits a trailing LF. The package does document `match` (`rfc3987.py:32`); the cross-check does not use it. SCORECARD.md:2710's `rule="URI"` is the accurate shorter form.

Confidence: high. Unknown: earlier history of the abnf *project* before the vendored 2020 copyright line was not fetched; it is not needed for the 2011-vs-2020 order.
