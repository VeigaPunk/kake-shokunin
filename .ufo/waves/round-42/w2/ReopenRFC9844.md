OVERSTATED: S124's quotes and hash hold, but it does not ground the declared zone-id filter. S125's obsolescence holds; "cannot ground that behaviour" does not.

Commands (all exit 0), files under /fast/scratch/hyaku/kake-r42w2/ReopenRFC9844/:
- `timeout 60 curl -fsSL -D rfc9844.hdr -o rfc9844.txt https://www.rfc-editor.org/rfc/rfc9844.txt` → HTTP 200, 19,292 bytes, sha256 `7585b9a9ed2e6d350ac4e79d0bbb722e5ab3d22c93fb2a40ad03d832cdb4b135`. Equal to the S124 row (`7585b9a9…c4b135`), to `.ufo/waves/round-42/sources/SHA256SUMS`, and byte-equal to the retained copy. Leading BOM `EF BB BF`. No form feeds. 418 newline-lines.
- `timeout 60 curl -fsSL -D rfc6874.hdr -o rfc6874.txt https://www.rfc-editor.org/rfc/rfc6874.txt` → HTTP 200, 19,361 bytes, sha256 `5f54b04f2035eb12f9a444bc6c2389582b9400c3df64a90965f9409c939380d5`. Equal to the S125 row (`5f54b04f…9380d5`), to SHA256SUMS, and byte-equal to the retained copy. 10 form feeds; 563 newline-lines. `str.splitlines()` mis-numbers this file because it splits on form feed; counts below are `\n` only.
- `timeout 60 curl -fsSL -D info6874.hdr -o info6874.html https://www.rfc-editor.org/info/rfc6874` → HTTP 301 to `/info/rfc6874/`, then HTTP 200, 180,056 bytes, sha256 `da71b06fea53cc15fe4ff3330419bf196b94ec82747eafe0ad45994030fa00a7`. Visible text: "This RFC is now obsolete, see RFC 9844"; "Obsoleted by (1) RFC 9844: Entering IPv6 Zone Identifiers in User Interfaces"; date published February 2013.

Quotes, found verbatim:
- S124 and Gate line: "This document completely obsoletes [RFC6874]" at rfc9844.txt:192 (the sentence goes on ", which implementors of web browsers have determined is impracticable to support"). Holds.
- "reverts the change that it made to the URI syntax" across rfc9844.txt:195-196, then "so [RFC3986] is no longer updated by [RFC6874]" (196-197). Holds. August 2025 is line 9. Header line 7 is "Obsoletes: 6874".
- S125 and Gate line: `ZoneID = 1*( unreserved / pct-encoded )` at rfc6874.txt:200. Holds.
- `IPv6addrz = IPv6address "%25" ZoneID` at rfc6874.txt:202, inside the cited 198–202 span (line 198 is the `IP-literal` replacement). Holds. February 2013 is line 13. Header line 9 is "Updates: 3986".

S125 rejection reason (SOURCES.md row teaches; Gate at corpus/lessons/round-42.md:21 and :42):
- "obsoleted by RFC 9844": holds (rfc9844.txt:7, :20-21, :192-194; info page above).
- "which reverts its URI-syntax change": holds (rfc9844.txt:195-197).
- "`%25` ZoneID grammar is not current URI syntax": holds.
- "cannot ground the declared zone-id behaviour": wrong. That behaviour, as stated at corpus/lessons/round-42.md:50-51, scripts/sitemap_audit.py:71-73 and SCORECARD.md:2916-2919, is rejecting a zone id that contains a raw non-ASCII character or raw `|`. RFC 6874 already requires that: ZoneID is `1*( unreserved / pct-encoded )` (line 200), a zone id "SHOULD contain only ASCII characters classified as unreserved", and any other character "MUST be represented using percent encoding" (lines 175-183). The Gate's shorter "cannot ground current URI syntax" holds. The row's stronger clause does not.
- What 6874 cannot ground is the claim that `%25eth0` is not URI syntax. Line 202 makes `IPv6address "%25" ZoneID` the normative form. The tool accepts it (below). Bare `%eth0` is only the non-normative suggestion at rfc6874.txt:254-259, not the grammar.

S124 against the SCORECARD and the tool comment:
- Scope ("current standing … whether a `%` zone suffix belongs to RFC 3986 IP-literal syntax; not a user-interface rule"): supported. Section 5 (rfc9844.txt:216-255) is a UI requirement and "do not apply to URIs fetched by web browsers" (254-255). The URI-syntax point is the revert at 195-197.
- Teaches, first clause (an IP literal is again RFC 3986, so a `%` zone suffix is not URI syntax): supported. Retained rfc3986.txt:1043 and :2722: `IP-literal = "[" ( IPv6address / IPvFuture ) "]"`, no zone id and no `%`.
- Teaches, audit clause, and Gate "grounds the declared zone-id behaviour" (round-42.md:20): overstated. S124 withdraws every zone suffix, including the suffixes the tool still accepts. It does not say "reject only non-ASCII and `|`".
- Witness, host Python 3.14.8, `scripts/sitemap_audit.py` `_uri_ok` / `_parse_url`: `http://[fe80::1%eth0]/a` and `http://[fe80::1%25eth0]/a` both parse; `http://[fe80::1%7Ceth0]/a` parses (percent-encoded `|`, host `fe80::1%7ceth0`); `http://[fe80::1%|eth0]/a` and `http://[fe80::1%é]/a` fail in `_uri_ok`. So "acceptance of `%25eth0`/`%eth0` is legacy laxity" is a fair inference from the revert, not a sentence of RFC 9844. SCORECARD.md:2917-2919 ("so a zone id with a non-ASCII character or `|` is rejected (RFC 3986 has no zone id)") and the comment at sitemap_audit.py:71-73 cite that fact for a class that still admits `%` (`_IP_LITERAL_ASCII`, line 124), which is how a zone id is spelled.
- rfc9844.txt:197-198 says the revert "will have no significant impact on non-browser deployments of URIs", which cuts against using S124 to justify a tighter sitemap bracket class. rfc9844.txt:272-273 says RFC 4007 does not restrict the zone-id character set; that sentence is in the UI section, outside the row's own scope.

Unchecked: S124's "info page: Obsoletes RFC 6874, no Obsoleted-by". `https://www.rfc-editor.org/info/rfc9844` was not in the named URL set. The txt header supports "Obsoletes: 6874" only.

No tool installed.
