```json
{"id":"S029","verdict":"HOLD","fetchIndex":1,"quote":"When authority is not present, the path cannot begin with two slash characters","anchorObserved":"Section 3 Syntax Components, paragraph immediately after the hier-part ABNF (plain text lines 874-878, p.16), unchanged","reason":"Re-fetched raw bytes hash to the row's pinned sha256 3102dae4…b2d683 (141,811 bytes, HTTP 200); the anchor sentence is verbatim unchanged and still forbids a `//`-initial path without authority, while authority ABNF keeps all subcomponents optional so the authority may be empty.","correction":null}
```

Caveat:
- Hash check: `gzip -dc S029-1.raw.gz | sha256sum` = 3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683, 141,811 bytes — exact match to the row pin; text view (122,035 chars) is whitespace-collapsed, so its differing hash is by construction, not drift.
- Manifest: status 200, finalUrl identical to recorded URL, no redirect, content-type text/plain;charset=utf-8, fetchedAt 2026-10-21T15:10:49Z.
- RFC 3986 is immutable (January 2005, STD 66, obsoletes 2732/2396/1808); this recheck tests availability and anchor position, not living-document drift. No errata reviewed.
- "Possibly empty" rests on `authority = [ userinfo "@" ] host [ ":" port ]` (line 959) with `reg-name = *(unreserved / pct-encoded / sub-delims)` and §3.2.2 empty-host default text; §4.2 `relative-part = "//" authority path-abempty` (line 1430) routes any `//`-prefixed reference through authority.
- Independent restatement in §3.3 (lines ~1206-1208): "If a URI does not contain an authority component, then the path cannot begin with two slash characters ("//")" — teaches holds at two anchors.
- Scope, status `mined`, recheck 365d and used-by (static-canonical-preflight.md, lessons/round-22.md) remain valid; no STALE correction needed.
