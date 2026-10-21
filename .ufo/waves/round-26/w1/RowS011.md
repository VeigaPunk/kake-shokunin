# Row S011 — RFC 9309 freshness recheck (round 26)

```json
{"id":"S011","verdict":"HOLD","fetchIndex":1,"quote":"the robots.txt file is unreachable due to server or network errors, this means the robots.txt file is undefined and the crawler MUST assume complete disallow","anchorObserved":"Section 2.3.1.4 \"Unreachable\" Status, body heading at char 14630 (quote at 14663, text-view line 1); Section 2.3 Access Method heading at char 12993 (TOC 2212); \"Published: September 2022\" at char 213","reason":"Section 2.3 still requires the rules in \"/robots.txt\" (all lowercase) in the top-level path of the service with URI scheme:[//authority]/robots.txt, so the host/service-root scope holds; Section 2.3.1.4 still says an unreachable robots.txt is undefined and the crawler MUST assume complete disallow (with the 30-day outage MAY). Only typographic drift: the heading now quotes \"Unreachable\" and Section 2.3.1 is titled \"Access Results\"; numbering and September 2022 publication are unchanged. The citing knowledge entry's quotes (\"in the top-level path of the service\"; \"MAY access any resources on the server\"; \"MUST assume complete disallow\" with 30-day allowance) all still match verbatim, so row teaches/anchor/used-by remain valid.","correction":null}
```

- Fetch: https://www.rfc-editor.org/rfc/rfc9309.html, status 200, sha256 bbaa280636d3e38f0a1a130a5ce40e9753db1ed18c860945b0bf795ff8dc1a87, fetchedAt 2026-10-21T15:10:38Z (manifest.json).
- RFC 9309 is an immutable published standard; drift risk is availability + anchor, and both hold. No version/date supersession notice appears in the fetched text (only the generic errata/info boilerplate); errata content itself was not separately fetched.
- Scope note: RFC wording is per-service/per-authority (`scheme:[//authority]/robots.txt`), which supports the row's "Host-root scope" for the HTTP(S) lane sites; no correction needed.
- Knowledge entry `corpus/knowledge/crawl-scope-per-host.md` lines 12-22 and 33-40 re-checked against the same text; no stale statement found, so no append-only correction required from this row.
- No tools installed or upgraded; no files outside this report touched.
