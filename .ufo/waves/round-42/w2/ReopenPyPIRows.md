HOLDS, one Gate sentence wrong: live PyPI JSON and both wheel digests equal S118/S119/S121/S122; S118/S119 cells equal `9e3c31d2` except `used-by`. `round-42.md:28` names a `used-by` value S118 and S119 do not have.

Commands (exit 0): `timeout 60 curl -fsS -D abnf.hdr -o abnf-2.9.1.json -w … https://pypi.org/pypi/abnf/2.9.1/json` and the same for `https://pypi.org/pypi/rfc3987/1.3.8/json` (2026-10-23T12:13:22Z). No packages installed.

Fetch: abnf HTTP 200, 8215 bytes, sha256 `d1dab17e48793e9e3921679ef8e2672b2a71557c024482b931eef4d934a6d10d`. rfc3987 HTTP 200, 9900 bytes, sha256 `f624f451627f0d5db519d7e32b72ab4bc8576c88247b180ee363dff8932e8d2e`. Both files are one JSON line. Retained `.ufo/waves/round-42/sources/pypi.org_pypi_{abnf_2.9.1,rfc3987_1.3.8}_json` are byte-equal to this fetch (and to `sources/SHA256SUMS`).

Vendored wheels (`.ufo/waves/round-41/oracle/`): abnf 78103 bytes `cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917`; rfc3987 13377 bytes `10702b1e51e5658843460b189b185c0366d2cf4cff716f13111b0ea9fd2dce53`. Both equal `urls[]` in the live JSON.

Quotes (verbatim):
- "Parsers for ABNF grammars." yes — abnf `info.summary` (raw line 1). Gate `round-42.md:17` holds.
- "validate a whole string against a rule (raises ParseError otherwise)" yes — abnf description line 34 (the `# ` marker is outside the quote), above `parse_all` at description line 36.
- "Parsing and validation of URIs (RFC 3986) and IRIs (RFC 3987)" yes — rfc3987 `info.summary` (raw line 1). Gate `round-42.md:18` holds.
- Gate byte counts 8215 and 9900, and sha prefixes `d1dab17e…d10d`, `f624f451…2e8d2e`, `cdcac127…0917`, `10702b1e…ce53`: hold.

Per row (sha256 of the retained JSON equals the row: yes for all four):
- S118 `corpus/SOURCES.md:126`. Quotes yes. Scope supported (ships `abnf/grammars/rfc3986.py`; not the RFC). Teaches overstated: `parse_all` does accept a whole string or raise `ParseError` (`abnf/_parser_python.py:1017-1020`; extra text raises, `ftp://example.com/a` parses), but the counter does not read every success as valid (`c1_count.py:83-93` also requires http(s) and a non-empty host).
- S119 `corpus/SOURCES.md:127`. Quote yes. Scope supported (regexes for both RFCs; authors differ: Gerber vs Yeomans). Teaches wrong: the cross-check does not call `match(value, rule="URI")`; it uses `get_compiled_pattern("%(URI)s").fullmatch` (`oracle_crosscheck.py:33-38`).
- S121 `corpus/SOURCES.md:129`. Quotes yes. Opener `supersedes S118 —` holds. Scope supported, with a stale pointer: "(S117 is)" ignores S120, which supersedes S117. Teaches supported (the S118 overstatement is the part S121 replaces; counter filter is `c1_count.py:83-93`).
- S122 `corpus/SOURCES.md:130`. Quote yes. Opener `supersedes S119 —` holds. Scope supported. Teaches supported: `match` compiles `^%(rule)s$` (`rfc3987.py:424`); `match("http://example.com/\n", rule="URI")` is true and `fullmatch` of `"%(URI)s"` on that string is false.

`9e3c31d2` (`9e3c31d2e25965d466c0d006d33684fc218b0aa6`): S118 and S119 are field-equal to that commit on id, source, kind, tier, scope, anchor, teaches, status, opened, recheck. `used-by` differs only by dropping ` "Round 41"`: now `.ufo/waves/round-41/c1_count.py, SCORECARD.md` and `.ufo/waves/round-41/oracle_crosscheck.py, SCORECARD.md`. So `round-42.md:26-27` and `:79` (restore except `used-by`) hold. `round-42.md:28` ("stays `SCORECARD.md, corpus/lessons/round-41.md`") is wrong for S118 and S119. That string is S117's current `used-by` only; at `9e3c31d2` S117's was `SCORECARD.md "Round 41", corpus/lessons/round-41.md`.

Confidence: high. Unknown: none for these four rows.
