# ScoutRFC6874 — zone-id syntax (RFC 6874 → RFC 9844)
Axes: freshness of the obsoletion chain, then whether each of the six strings matches the cited grammar. No package installs. Counter not run (scout seat). Python 3.14.8. Fetches 2026-10-23; curl and the tip41 import exited 0.
## Bodies

| GET | status | bytes | sha256 |
|---|---|---|---|
| https://www.rfc-editor.org/rfc/rfc6874.txt | HTTP/2 200 | 19361 | `5f54b04f2035eb12f9a444bc6c2389582b9400c3df64a90965f9409c939380d5` |
| https://www.rfc-editor.org/info/rfc6874 (no slash) | HTTP/2 301, `Location: /info/rfc6874/` | 100 | `a5c38bb77c292eb8069157604dfb5d1deeb16c3fb1ca8e0124f9cf53d12ddf8c` |
| https://www.rfc-editor.org/info/rfc6874/ | HTTP/2 200 | 180056 | `da71b06fea53cc15fe4ff3330419bf196b94ec82747eafe0ad45994030fa00a7` |
| https://www.rfc-editor.org/rfc/rfc9844.txt | HTTP/2 200 | 19292 | `7585b9a9ed2e6d350ac4e79d0bbb722e5ab3d22c93fb2a40ad03d832cdb4b135` |
| https://www.rfc-editor.org/info/rfc9844/ | HTTP/2 200 | 276031 | `ce0da28698e622759bb94a2d43eace0640dc524c6ff277e0e458f8bc25520c2d` |

Retained under `/fast/scratch/hyaku/kake-r42w1/ScoutRFC6874/`. `rfc9844.txt` begins with UTF-8 BOM `EF BB BF` (line 1); that byte is inside the sha256. 6874 info page, static About tab: "Obsoleted by (1) RFC 9844"; the string "Updated by" does not occur. 9844 info page: "Obsoletes (1) RFC 6874"; "Obsoleted by" and "Updated by" occur zero times. Chain stops at 9844.
## Grammar

RFC 6874 (February 2013, `Updates: 3986` at line 9) replaces the RFC 3986 IP-literal rule. Quotes:

- line 198: `IP-literal = "[" ( IPv6address / IPv6addrz / IPvFuture  ) "]"`
- line 200: `ZoneID = 1*( unreserved / pct-encoded )`
- line 202: `IPv6addrz = IPv6address "%25" ZoneID`
- lines 163–164: "scoped address fe80::a%en1 would appear in a URI as http://[fe80::a%25en1]."

`unreserved` and `pct-encoded` are the RFC 3986 productions named here, not re-fetched this run: unreserved is ALPHA / DIGIT / "-" / "." / "_" / "~"; pct-encoded is "%" HEXDIG HEXDIG. Lines 236–237: "no normative statements are made in this section." Lines 252–253 only "suggest that URI parsers accept bare "%" signs".

RFC 9844 (August 2025) does not define ZoneID or IPv6addrz. Quotes:

- line 7: `Obsoletes: 6874`
- line 192: "This document completely obsoletes [RFC6874]"
- lines 195–196: "obsoleting [RFC6874] reverts the change that it made to the URI syntax"
- lines 222–223: "the UI SHOULD support the complete format specified by [RFC4007] (e.g., "fe80::1%eth0")."

That example is a UI address string, not a URI. After 9844, URI validity is RFC 3986 again, whose IP-literal has no `%`.
## Six values

`_parse_url` imported from `/fast/scratch/hyaku/kake-r42/shared/tip41.py`. IP-literal class is tip41.py:80 (ASCII, includes `%`, excludes `|` and U+0080+). `None` on value 3 is `urlsplit` → `ipaddress.ip_address`: `_split_scope_id` (`/usr/lib/python3.14/ipaddress.py:1910`) rejects a second `%`.

| value | tip41 | RFC 6874 ABNF | after RFC 9844 |
|---|---|---|---|
| `http://[fe80::1%25eth0]/` | `('http','fe80::1%25eth0',80,'/')` | valid; ZoneID `eth0` | not a URI (no IPv6addrz) |
| `http://[fe80::1%25en1]/` | `('http','fe80::1%25en1',80,'/')` | valid; matches lines 163–164 | not a URI |
| `http://[fe80::1%25%41]/` | `None` (regex hit, then ValueError) | valid; ZoneID is one pct-encoded `%41` | not a URI |
| `http://[fe80::1%eth0]/` | `('http','fe80::1%eth0',80,'/')` | not ABNF; bare `%` is the §3 suggestion only | not this URI; UI example is unwrapped `fe80::1%eth0` |
| `http://[fe80::1%é]/` (U+00E9) | `None` (regex miss) | invalid; bare `%`, U+00E9 not unreserved or pct-encoded | not a URI |
| `http://[fe80::1%en\|0]/` | `None` (regex miss on `\|`) | invalid; bare `%`, `\|` not unreserved | not a URI |

tip41 therefore disagrees with the RFC 6874 grammar on value 3 (rejects a legal pct-encoded ZoneID) and value 4 (accepts a bare `%` the ABNF excludes).

## Statements

- "RFC 6874 is obsoleted by RFC 9844 and has no Updated-by RFC on the info page." holds.
- "RFC 9844 supplies a replacement ZoneID / IPv6addrz ABNF." wrong. It reverts the URI change and states a UI requirement.
- "All six strings are valid under RFC 6874." wrong. Only the three `%25` forms match the ABNF.
- "The three `%25` forms are still valid URIs after RFC 9844." wrong. 9844 restores RFC 3986 IP-literal.
## Draft SOURCES rows (not inserted; S119 was the last registry row when read)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| draft | RFC 6874 — https://www.rfc-editor.org/rfc/rfc6874.txt | spec | A | Historical zone-id URI syntax only; obsoleted, not current URI law | Lines 198, 200, 202; February 2013; fetched 2026-10-23, HTTP 200, sha256 `5f54b04f2035eb12f9a444bc6c2389582b9400c3df64a90965f9409c939380d5`; info page Obsoleted by RFC 9844 | `IPv6addrz` is an IPv6address, the three characters `%25`, then a ZoneID of unreserved or pct-encoded; a bare `%` is not in that ABNF | queued | 2026-10-23 | 365d | — |
| draft | RFC 9844 — https://www.rfc-editor.org/rfc/rfc9844.txt | spec | A | Current status of the RFC 6874 URI change, and the UI zone-id requirement; not a URI grammar | Lines 7, 192, 195–196, 222–223; August 2025; fetched 2026-10-23, HTTP 200, sha256 `7585b9a9ed2e6d350ac4e79d0bbb722e5ab3d22c93fb2a40ad03d832cdb4b135` (body includes a leading UTF-8 BOM); info page has no Obsoleted-by or Updated-by | Obsoleting RFC 6874 reverts its edit to RFC 3986; a UI SHOULD accept an address string such as `fe80::1%eth0`, which is not a URI production | queued | 2026-10-23 | 365d | — |
