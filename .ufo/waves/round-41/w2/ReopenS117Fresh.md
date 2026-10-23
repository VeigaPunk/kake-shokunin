# ReopenS117Fresh — row S117 (RFC 3986)

Axes: freshness. No tools installed. Line numbers are LF lines of the plain-text RFC (`read`/`grep`). Python `splitlines()` also breaks on the form-feeds and must not be used to re-cite these lines.

## Commands

1. `prlimit --as=4000000000 timeout 120 curl -fsSL -D headers.txt -o rfc3986.txt https://www.rfc-editor.org/rfc/rfc3986.txt` in `/fast/scratch/hyaku/kake-r41w2/ReopenS117Fresh`. Exit 0. HTTP/2 200, `date: Fri, 23 Oct 2026 10:08:42 GMT`, `content-type: text/plain;charset=utf-8`.
2. `wc -c` 141811; `sha256sum` `3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683`. Exit 0.
3. Retained `.ufo/waves/round-41/sources/rfc3986.txt` has that same digest; `cmp -s` against the fresh GET, exit 0. `wc -l` 3419. `sources/fetched-at.txt:1` is `2026-10-23T09:39:11Z`. `sources/SHA256SUMS:4` is the same digest.

## Anchors (SOURCES.md:125)

- §3, the `URI` rule, line 867 — **holds**. `rfc3986.txt:861` `3.  Syntax Components`; `:867` `URI = scheme ":" hier-part [ "?" query ] [ "#" fragment ]`.
- §3.2.3 `port = *DIGIT` — **holds**. `:1183` `3.2.3.  Port`; `:1189` `port = *DIGIT`.
- §4.3 `absolute-URI` — **holds**. `:1463` `4.3.  Absolute URI`; `:1470` `absolute-URI = scheme ":" hier-part [ "?" query ]`.
- Appendix A Collected ABNF, lines 2690–2760 — **overstated** (severity: the cited window does not hold the full grammar). Title is `:2695`. `:2690-2694` is the page-48 footer and page-49 header. Rules continue through `:2788`; Appendix B starts `:2790`. `:2760` is only the second alternative of `path` (`:2759-2763`). Outside the window: `pchar` `:2776`, `query` `:2778`, `fragment` `:2780`, `pct-encoded` `:2782`.
- RFC 3986, January 2005 — **holds** (`:8`, `:13`; running header `:60`).
- Fetched 2026-10-23T09:39:11Z, HTTP 200, 141,811 bytes, SHA256 equal to S098 — **holds**. This GET is later than the stamp and byte-identical. S098 is `SOURCES.md:106`, same full digest.

## Teaches

- A URI is scheme, ":", hier-part, then an optional "?" query and "#" fragment — **holds** (`:867`). The two brackets are independent.
- Each component has its own character repertoire — **holds** (`:699-701`: each syntax rule lists the characters allowed in that component). Precision, not a miss: `query` (`:1295`) and `fragment` (`:1319`) are the same set `*( pchar / "/" / "?" )`. Scheme `:921`, userinfo `:980`, reg-name `:2757`, port `:1189`, and pchar `:1244` differ.
- A percent sign must start a two-hex-digit triplet — **holds** (`:639-641`; `:647` `pct-encoded = "%" HEXDIG HEXDIG`). `%` is not in unreserved `:724`, gen-delims `:681`, or sub-delims `:683-684`. `:649-650`: lowercase hex is equivalent. Same sentence as S098 §2.1; that does not collapse the two scopes.
- A port is any run of digits — **holds** (`:1189` `*DIGIT`, no 65535 cap). `:1195-1197`: producers should omit an empty port; `*` still matches empty. `:963`: some schemes disallow the port subcomponent; that is outside this production.
- `absolute-URI` (§4.3) is the same without a fragment — **holds** (`:1465-1468` and `:1470` against `:867`).
- A value `urlsplit` accepts can still fail this grammar — **overstated** (severity: not this source). RFC 3986 never names `urlsplit`. Not scored as a fact about Python.

## Scope sentence (same row)

- Distinct from S098 §§2.1–2.3 — **holds** (`SOURCES.md:106` is character classes). Shared text is only the pct-encoded sentence.
- Distinct from S029's §3 authority/path reading — **holds**. S029 (`SOURCES.md:37`) is the paragraph after hier-part (`rfc3986.txt:874-878`), not the `URI` production.
- Distinct from S089 §5.2 — **holds**. S089 (`SOURCES.md:97`) is resolution and recomposition; this row does not cite it.
- "The full `URI` grammar … used to judge a URL as written" — **holds** for the component list (scheme, authority with optional userinfo and port, path, query, fragment: `:867`, `:959`, `:2715-2720`). Limit, not a miss: `:37-42` says the generic grammar is a superset and not a generative grammar; scheme specs may restrict further (`:907-909`).

Checked statements: hash, size, HTTP 200, and S098 equality **hold**; named section anchors **hold**; Appendix A lines 2690–2760 **overstated**; the `urlsplit` teaches clause **overstated**. No other lane file written.
