source: S011, S095, S096, S034, S098, S099, S100 (corpus/SOURCES.md; S034, S098–S100 added round 38) — S011 RFC 9309, §§1–3; S095 Google, “How Google Interprets the robots.txt Specification”, named sections below; S096 google/robotstxt, README “Quickstart” and “Notes”
verified-at: 2026-10-23 (S011, S095 and S096 retained round-37 retrievals; `.ufo/waves/round-37/sources/receipts.json`)
recheck: 90d, or on an RFC 9309 revision/erratum, Google documentation update, or google/robotstxt parser change; re-open the cited anchors and compare the retained source receipts

# Offline robots.txt rules

## Scope

The Robots Exclusion Protocol is a crawler-access convention, not authorization; a disallow rule does not secure the named resource (S011 §1, §3).

This entry describes the lane's offline expectation check, not a statement that a particular crawler will fetch or obey a file (lane reading: `SCORECARD.md`, “Round 37 — declared claims”, C1 contract, “Usage” and “Limits”; S011 §2.3.1).

## Establish the file and access result

A service publishes its rules at the lowercase `/robots.txt` path in the service's top-level path, with the protocol, authority and port determining the scope (S011 §2.3; S095 “File location and range of validity”).

A robots file at a subdirectory does not set the rules for the service root, and a file for one scheme, host or port does not set rules for another (S011 §2.3; S095 “File location and range of validity”).

When the robots file is successfully retrieved, a crawler MUST follow its parseable rules; an HTTP 4xx “unavailable” response means crawlers MAY access server resources, while an unreachable file due to server or network errors requires a crawler to assume complete disallow (S011 §§2.3.1.1, 2.3.1.3–2.3.1.4).

RFC 9309 permits a crawler, after the file stays undefined (unreachable) for a reasonably long time (for example, 30 days), to treat it as unavailable or continue using a cached copy (S011 §2.3.1.4).

**Lane reading:** this check maps every 2xx status to parsing the named local file, every 400–499 status to allow regardless of file contents, and every 500–599 status to disallow regardless of file contents, including `/robots.txt`; it does not apply the RFC's long-outage allowance (S011 §§2.3.1.1, 2.3.1.3–2.3.1.4; `SCORECARD.md`, C1 contract, “(a) Access result”).

Google documents its own status handling, including a 429 exception among 4xx responses and cache-dependent 5xx behavior; those Google-specific details are not substituted for the lane reading (S095 “Handling of errors and HTTP status codes”; `SCORECARD.md`, C1 contract, “(a) Access result”).

## Read lines and groups

RFC 9309 requires UTF-8 plain text and says parsers MUST try each line and use parseable rules; it sets a minimum parsing limit of 500 KiB (S011 §§2.3, 2.3.1.5, 2.5).

**Lane reading:** the parser consumes exactly the first 512000 bytes, drops an initial UTF-8 BOM, replacement-decodes invalid UTF-8, splits on CR, LF or CRLF, removes text from the first `#` on each line, ignores lines without `:`, and trims spaces/tabs around the key and value (S011 §§2.2, 2.3, 2.5; `SCORECARD.md`, C1 contract, “(b) Lines”).

`user-agent`, `allow` and `disallow` are the records used here; RFC 9309 permits other records but says they MUST NOT interfere with parsing the defined records (S011 §§2.2.1–2.2.4). Google states that field names are case-insensitive (S095 “Syntax”); the lane reading compares keys ASCII case-insensitively.

**Lane reading:** every other key (including `sitemap` and `crawl-delay`) is ignored without ending a group, and `allow`/`disallow` records before the first `user-agent` are ignored (S011 §§2.2.2, 2.2.4; `SCORECARD.md`, C1 contract, “(b) Lines”).

Google's documentation lists `sitemap` as a supported field (for sitemap discovery) while it, like the lane check, does not let a `sitemap` line affect group parsing (S095 “Syntax”, “Grouping of lines and rules”; `SCORECARD.md`, C1 contract, “(b) Lines”).

RFC 9309 matches a crawler's product token case-insensitively, combines the rules of every group that matches it, and falls back to the `*` group only when no group matches the token (S011 §2.2.1).

**Lane reading:** the check accepts product tokens made of ASCII letters, `_` or `-`, compares a supplied token to group names by case-insensitive equality, combines every equal-name group, and if none match combines all `*` groups; if neither exists, no rules apply and URLs are allowed (S011 §2.2.1; `SCORECARD.md`, C1 contract, manifest and “(c) Groups”).

**Lane reading:** consecutive `user-agent` records belong to one group, while a later `user-agent` starts a new group unless the prior record was also `user-agent`; blank, comment and ignored records do not break that adjacency (S011 §2.2.1; `SCORECARD.md`, C1 contract, “(c) Groups”).

Google's documentation chooses one most-specific user-agent group and says specific groups and the global `*` group are not combined; therefore the lane's explicit equality/fallback reading is not a claim about Google's group selection (S095 “Order of precedence for user agents”; `SCORECARD.md`, C1 contract, “(c) Groups”).

## Match rules to a URL

An `allow` or `disallow` path is matched from the first octet of the path; the most specific match (the one with the most octets) is used, if an `allow` and a `disallow` rule are equivalent the `allow` SHOULD be used, and no matching rule means allowed (S011 §2.2.2).

The special character `*` matches zero or more characters, `$` marks the end of a match, and `#` begins a comment (S011 §2.2.3).

**Lane reading:** an empty rule value never matches, only a final `$` anchors at the end (a non-final `$` is literal), and path patterns are case-sensitive (S011 §§2.2.2–2.2.3; `SCORECARD.md`, C1 contract, “(d) Rules”).

**Lane reading:** choose the longest matching normalized rule value measured in octets, counting `*` and a terminal `$`; an `allow` wins a same-length tie with `disallow` (S011 §2.2.2; `SCORECARD.md`, C1 contract, “(d) Rules”).

RFC 9309 says “The /robots.txt URI is implicitly allowed.” (S011 §2.2.2). **Lane reading:** this applies only when the file decides access (status 2xx); under 500–599 every URL, `/robots.txt` included, is disallowed (`SCORECARD.md`, C1 contract, “(a) Access result”, “(e) Path to match and normalization”).

**Lane reading:** construct the comparison target from the URL path (use `/` when empty), append `?` and a non-empty query, and omit the fragment (S011 §2.2.2; `SCORECARD.md`, C1 contract, “(e) Path to match and normalization”).

RFC 9309 says octets outside ASCII and those "in the reserved range" MUST be percent-encoded before comparison, and that a percent-encoded ASCII octet in the URI MUST be decoded unless it is reserved or outside the unreserved range; its Figure 4 shows `/foo/bar?baz=quz` compared unencoded and `%62%61%7A` compared as `baz` (S011 §2.2.2).

**Lane reading:** percent-encode non-ASCII characters as UTF-8 octets with uppercase hex, decode `%XX` escapes only for unreserved ASCII letters, digits, `-`, `.`, `_` and `~`, and uppercase the hex of other escapes; reserved characters are never encoded or decoded, so `%2F` and `/` remain distinct (S011 §2.2.2; `SCORECARD.md`, C1 contract, “(e) Path to match and normalization”). This follows Figure 4's first and last rows and departs both from the literal reserved-range sentence, which would make `%2F` and `/` equal (round-37 wave-1 `ScoutReopenS011` D1), and from Figure 4's row that encodes `https://foo.bar` in a query as `https%3A%2F%2Ffoo.bar`: a rule written with `%3A` does not match a raw `:` in the URL under this reading (round-37 wave-2 `ReviewKnowledgeEntry`). Google's parser decodes no unreserved escape (it percent-escapes raw high-bit bytes in allow/disallow values and uppercases hex) and leaves path normalization to the caller (S096 README “Notes”; its `robots.cc` and `robots.h` at master `22b355ff`, read by round-37 wave-1 `ScoutReopenS096` K1; the code files are not retained by the lane).

## Using the offline expectation check

For each intended URL and crawler product token, write one check `{"id", "robotsStatus", "userAgent", "url", "expect"}` (plus `robots` for 2xx: a relative path to a regular file inside the manifest directory) in a manifest `{"version": 1, "checks": [...]}`, with an absolute http(s) URL and an `expect` of `allow` or `disallow`, and run `python3 scripts/robots_audit.py --manifest PATH` (lane contract: `SCORECARD.md`, Round 37 C1 contract, “Usage”, “Manifest” and “(a) Access result”; S011 §§2.3.1.1, 2.3.1.3–2.3.1.4).

**Lane contract:** when the computed decision disagrees with the expectation, an expected-allow/actual-disallow mismatch is `blocked` and an expected-disallow/actual-allow mismatch is `exposed` (SCORECARD.md, Round 37 C1 contract, “Findings per evaluated check”; S011 §2.2.2).

**Lane contract:** malformed manifest/check input is a failure to evaluate, not a clean policy result (SCORECARD.md, Round 37 C1 contract, “(f) Check faults”, “(g) Manifest faults” and “Verdict”).

S096's README describes a local single-URL/user-agent command for the Google parser and says supplied URIs must already follow RFC 3986 because the library does not perform full URI normalization (S096 README “Quickstart” and “Notes”).

## Limits

This audit reads local input only; it does not fetch a robots file, follow redirects, or model caching (lane reading: `SCORECARD.md`, C1 contract, “Usage” and “Limits”; S011 §§2.3.1.2, 2.4).

Robots rules do not grant or deny authorization, and listing a path makes that path discoverable; protect private content with an application-layer security mechanism (S011 §1, §3).

This entry infers no behavior for any particular crawler; S095 describes Google's interpretation only, and S096 explicitly excludes crawler implementation logic outside parsing and matching (S095 opening “How Google Interprets the robots.txt Specification”; S096 README “Notes”). One lane reading matches a Google-specific choice rather than the RFC: dropping a leading UTF-8 BOM (S011 is silent; Google's parser calls it a Google-specific optimization, `robots.cc:435` per wave-1 `ScoutReopenS096`).

**Evidence boundary:** the described C1 rules are a public lane contract, not evidence that an implementation passed any check; the sealed synthetic cases are not live fetches (SCORECARD.md, Round 37 C1 contract, “Frozen predicate” and “Limits”).

## Round 38 amendments — lane readings (appended)

Lane readings of the offline audit, added in round 38 (`SCORECARD.md` "Round 38 — C2 declared",
rules (h), (i), (k)). They describe this lane's checker, not what any crawler does. Sources opened
2026-10-23: S034, S098, S099, S100 (`corpus/SOURCES.md`; Gate lines in `corpus/lessons/round-38.md`).

**(h) JSON numbers, lane reading.** RFC 8259 says numeric values such as Infinity and NaN "are not
permitted" (S034 §6), so a manifest holding `NaN`, `Infinity` or `-Infinity` outside a string is not
JSON and gets one `input_invalid` finding with nothing evaluated. Python's json module accepts all
three by default and offers `parse_constant` to raise on them (S100, "Infinite and NaN Number
Values", `parse_constant`); the round-37 tool used the default and let them through. RFC 8259 lets
an implementation limit the range and precision of numbers (S034 §§6, 9), so the next sentence is
the lane's choice, not an RFC requirement: an integer of any length parses, an out-of-range
`robotsStatus` of any length is `check_invalid` for that check, and a long number in a field the
contract does not read changes nothing. Python's default 4300-digit conversion limit would make a
5000-digit integer an `input_invalid` manifest instead (S100 points to that limit).

**(i) URL characters, lane reading.** RFC 3986 builds URIs from unreserved characters, reserved
delimiters and percent-encoding (S098 §§2.1–2.3). The audit therefore rejects (`check_invalid`) a
`url` that holds any other ASCII character: space, a C0 control, DEL, `"`, `<`, `>`, `\`, `^`,
`` ` ``, `{`, `|` or `}`, wherever it sits (leading, trailing, path, query, fragment, host). The
characters are judged as written, before parsing. Non-ASCII characters are kept (rule (e) encodes
them), and a `%` without two hex digits passes this rule. It checks the character set only, not
the full URI grammar. The WHATWG URL parser and Python's `urlsplit` strip or drop some of these
characters instead of rejecting them (round-38 wave-1 `ScoutWhatwgUrl`, `ProbeUrlsplit`; WHATWG
registry row S101 rejected as this contract's source). A publisher-side audit flags them rather than
guessing what a crawler's parser would do.

**(k) Implicit `/robots.txt` allow on the normalized path, lane reading.** "The /robots.txt URI is
implicitly allowed" (S099 §2.2.2), and the same section unencodes percent-encoded unreserved octets
before comparison. So when the file decides (status 2xx), the path to match is normalized by rule
(e) before it is compared with `/robots.txt`: `/robots%2Etxt` and `/%72obots.txt` are allowed.
`/robots.txt?x=1` (non-empty query), `/ROBOTS.TXT` (case) and `/robots%2Ftxt` (kept reserved escape)
are decided by the rules. `/robots.txt?` has an empty query and is allowed. Dot segments are not
removed (`/a/../robots.txt` is decided by the rules). This replaces the round-37 tool's raw-path
comparison. The sentence above about 500–599 still holds: under 5xx every URL is disallowed.
Google differs: its parser has no implicit allow and does not decode the path, so under
`Disallow: /` it blocks `/robots%2Etxt` (round-38 wave-1 `ScoutGoogleImplicit`, S096 `robots.cc`
at `22b355ff`, lines 537–546).
