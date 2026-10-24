# ReviewOracleFidelity — r41 wave-1 oracle fidelity review

Seat: KakeR41.ReviewOracleFidelity (leaf). Scope: abnf-2.9.1 `rfc3986` (the counter's oracle) vs rfc3987-1.3.8 vs RFC 3986 Appendix A; `load_oracle` host/scheme derivation; ≥10 tricky values on both oracles.

## Artifacts (paths + sha256)
- `…round-41/oracle/abnf-2.9.1-py3-none-any.whl` sha256 `cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917` (matches `ORACLE_SHA256`, c1_count.py:41).
- `…round-41/oracle/rfc3987-1.3.8-py2.py3-none-any.whl` sha256 `10702b1e51e5658843460b189b185c0366d2cf4cff716f13111b0ea9fd2dce53`.
- Unzipped copies in `/fast/scratch/hyaku/kake-r41w1/ReviewOracleFidelity/abnf_wheel/`, `…/rfc3987_wheel/`.
- RFC 3986 text fetched `https://www.rfc-editor.org/rfc/rfc3986.txt` (sha256 `3102dae4…b2d683`); Appendix A extracted for comparison.
- Harness `…/oracle_diff.py` (exit 0): `timeout 600 python3 -B oracle_diff.py` — abnf init 0.115 s, backend `python` (no Rust ext; pure-Python `_parser_python`).

## Rule-by-rule vs Appendix A (abnf rfc3986.py:18-54)
All 19 assigned rules textually equal to Appendix A (RFC 5234 spellings): URI, hier-part, authority, userinfo, host (IP-literal/IPv4address/reg-name), port, IP-literal, IPvFuture, IPv6address, IPv4address, reg-name, path-abempty, segment, pchar, query, fragment, pct-encoded, unreserved, sub-delims — identical strings, e.g. `URI = scheme ":" hier-part [ "?" query ] [ "#" fragment ]` (rfc3986.py:18 = RFC A.1); `host = IP-literal / IPv4address / reg-name` (rfc3986.py:27).
Spelling-only deltas: `path-empty = 0pchar` (rfc3986.py:43) vs RFC `0<pchar>` — same language; `dec-octet` alternatives reordered (rfc3986.py:36) but same set 0–255; IPv6address alternatives keep RFC order (rfc3986.py:31). `IPvFuture = "v" …` lowercase literal; ABNF literals are case-insensitive (RFC 5234 §2.3; implemented via `_ascii_fold`, `_parser_python.py:27-43,539-621`), so uppercase `V` matches — verified.

## load_oracle derivation (c1_count.py:62-95)
- `Rule("URI").parse_all(value)` full-string consume; ParseError ⇒ invalid (c1_count.py:81-85).
- `find` DFS first-match; scheme node value `.lower() in ("http","https")` (86-88); authority node must exist, host node found under authority with non-empty value (89-93). Matches contract sentences 4/22. Tested: `http://:80/`, `http://user@:80/`, `http:///` all rejected (host empty); `http://example.com:` accepted (empty port is RFC-valid *DIGIT).

## Tricky values (40 run on both oracles)
39/40 agree with expected RFC verdict. Only divergence:
- `http://[V1.a]/` (IPvFuture, uppercase V): abnf oracle **True**, rfc3987 **False** (rfc3987.py:172 `"v"` literal is case-sensitive; abnf matches RFC 5234 case-insensitive literal semantics). rfc3987 is stricter than Appendix A here.
Both oracles agree on: IPv4-prefix reg-names (`1.2.3.4.5`, `1.2.3.4.in-addr.arpa`, `1.2.3.4.5:8080` — longest-match alternation works, abnf issue #232 fixed), `256.1.1.1`, `00.1.2.3` (both accepted; attribution differs: abnf reg-name, rfc3987 IPv4), lowercase hex `%2f` (accepted both), `%zz`/truncated pct rejected, `[::1]`, `[::]`, `[::ffff:1.2.3.4]`, full IPv6, `[fe80::1%25eth0]` rejected (zone ids not in RFC 3986), `HTTP://EXAMPLE.COM/` accepted, `ftp://…` rejected by scheme filter, non-ASCII rejected, leading/double dot host accepted, `http://example.com/%E0%A4%A/` rejected.
Also noted: rfc3987 `get_compiled_pattern('^%(URI)s$')` `$` anchor accepts a trailing `\n` (Python `$` quirk); strict `fullmatch`/`\Z` does not. Irrelevant to counter (uses abnf `parse_all`).

## Differential on counter-shaped cases
`c1_count.generate` (same `make_url`/units as counter) for seeds 0–5 ⇒ 8604 cases (630 loc + 804 sitemapUrl per seed, all 6 components, LOC_UNITS/URL_UNITS/PCT_UNITS). abnf oracle vs rfc3987 (strict fullmatch) disagreement: **0/8604**. `byComponent`/`byField` coverage: userinfo/host/port/path/query/fragment × loc/sitemapUrl all exercised.

## Findings (by severity; all info-level, none affect counter correctness)
1. rfc3987.py:172 IPvFuture literal `"v"` case-sensitive — deviates from RFC 5234 literal case-insensitivity; rejects `[V1.a]` that abnf accepts. (Not the counter's oracle; only cross-oracle parity note.)
2. rfc3987.py:369 `get_compiled_pattern` with `^…$` template accepts trailing newline (`$` quirk); use `fullmatch`/`\Z` for strict validation.
3. Counter oracle uses pure-Python abnf backend (no `abnf_rust`), still fast: 8604-case dual-oracle differential ≈ 19 s wall.
4. `find()` first-match DFS is unambiguous here: exactly one scheme node and one host-under-authority node per URI parse.

## Checked statements
- "abnf grammar matches RFC 3986 Appendix A rule-by-rule" — holds (36/36 rules textually equal; 19 assigned shown above, rest verified equal incl. dec-octet/path-empty equivalence).
- "load_oracle derives scheme/host per contract" — holds (verified on 40 values).
- "Both oracles agree on counter-shaped inputs" — holds (0/8604 disagreements).
- "No tool installs performed" — holds (wheels vendored; no pacman/uv/cargo changes recorded).

Report trailer: `.ufo/waves/round-41/w1/ReviewOracleFidelity.md` (this file).
