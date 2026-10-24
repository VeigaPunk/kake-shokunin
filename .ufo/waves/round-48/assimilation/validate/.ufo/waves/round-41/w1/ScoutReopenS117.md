# ScoutReopenS117 — planned row S117 (RFC 3986 URI grammar)

Axes: freshness (judged). Operability named, not scored: this seat does not run the counter. No tools installed.

## Fetch

`prlimit --as=4000000000 timeout 120 curl -fsSL -D headers.txt -o rfc3986.txt https://www.rfc-editor.org/rfc/rfc3986.txt` (sandbox `/fast/scratch/hyaku/kake-r41w1/ScoutReopenS117/`). Exit 0. HTTP 200, `date: Fri, 23 Oct 2026 09:48:03 GMT`, `content-type: text/plain;charset=utf-8`, 141811 bytes, 3419 LF, 61 form-feeds (`\x0c` page breaks), 0 CR.

sha256 `3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683`.

Equal to all three pins:

- `.ufo/waves/round-41/sources/SHA256SUMS:4` `rfc3986.txt`
- retained `.ufo/waves/round-41/sources/rfc3986.txt` (byte-identical to the GET)
- S098 anchor, `corpus/SOURCES.md:106`, same full digest

`sources/fetched-at.txt:1` is `2026-10-23T09:39:11Z` (~9 min before this GET). Line numbers below are LF lines (`read`/`grep`). Python `splitlines()` also breaks on the 61 form-feeds and shifts later lines by up to ~48; do not cite those.

## Productions (live = retained)

| rule | §3 | Appendix A |
|---|---|---|
| `URI = scheme ":" hier-part [ "?" query ] [ "#" fragment ]` | 867 (header `3.  Syntax Components` 861) | 2697 (header `Appendix A.  Collected ABNF for URI` 2695) |
| `hier-part` | 869–872 | 2699–2702 |
| `reg-name = *( unreserved / pct-encoded / sub-delims )` | 1135 | 2757 |
| `port = *DIGIT` | 1189 (§3.2.3 at 1183) | 2720 |
| `pchar = unreserved / pct-encoded / sub-delims / ":" / "@"` | 1244 | 2776 |
| `query = *( pchar / "/" / "?" )` | 1295 (§3.4 at 1279) | 2778 |
| `fragment = *( pchar / "/" / "?" )` | 1319 (§3.5 at 1308) | 2780 |
| `absolute-URI = scheme ":" hier-part [ "?" query ]` | §4.3 header 1463, rule 1470 | 2706 |

`port = *DIGIT` has no 65535 cap. `reg-name` is `*` (empty allowed). Prose at 1137–1142: an empty registered name is zero length, and "the http scheme considers a missing authority or empty host invalid." That sentence names `http`, not `https`. `absolute-URI` drops the fragment; the planned citation is `URI`, which keeps it.

## S098 vs planned S117

S098 (`SOURCES.md:106`) anchor is §§2.1–2.3 only (headers 634, 656, 718). Scope: reserved/unreserved and percent-encoding, "distinct from S029 §3 authority/path grammar". Teaches: reserved delimiters vs unreserved characters; not browser URL normalization. It does not state the `URI` production, `hier-part`, `port`, `reg-name`, `pchar`, `query`, `fragment`, or `absolute-URI`.

Planned S117 (`SCORECARD.md:2685-2686`) is that `URI` production at §3 / Appendix A. No S117 row exists yet (registry ends at S116, `SOURCES.md:124`). Appendix A also reprints `pct-encoded` / `unreserved` / `reserved` at 2782–2788, which is S098's subject, but the planned citation is the `URI` rule, not those classes.

S098's `teaches` does not overlap the planned row. S098 does not make S117 redundant. S029 remains the `//` authority/path sentence, not this production.

## Checked statements

- Live sha256 equals `SHA256SUMS:4` and S098's retained digest — **holds**.
- Dispatch premise "S098 covers §2 only" — **holds**.
- `URI` production is at §3:867 and Appendix A:2697 — **holds**.
- `port`, `reg-name`, `pchar`, `query`, `fragment`, §4.3 `absolute-URI` are at the lines above — **holds**.
- S098 `teaches` already covers the planned URI-production row — **wrong** (no overlap).
- `SCORECARD.md:2685` "S117 … opened this round" as a registry fact — **overstated** until a row is added; the section (`2677-2678`) says it freezes nothing yet, and the bytes the row would pin are already fresh.

Unknown: none for this reopen. Non-empty host for https is not in the `URI` production (see 1141–1142); the scorecard puts that constraint on the oracle, not on the S117 citation.
