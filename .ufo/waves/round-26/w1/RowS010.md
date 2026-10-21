# RowS010 — round 26 freshness recheck

Seat: `KakeR25.RowS010-6`. Row: `corpus/SOURCES.md:18` (S010, tier A, kind spec, cadence 365d).
Source re-fetched this round: `#1 https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8` — HTTP 200, fetchedAt `2026-10-21T15:10:38Z`, body sha256 `d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5` (1,187,554 B), text view `fetched/text/S010-1.txt` sha256 `c345bef6c9e101e8ee6c0971d8ff0cf002d5cfc26602249db139c8cd0fa9bc13` (450,208 B, complete through Authors' Addresses).

```json
{"id":"S010","verdict":"HOLD","fetchIndex":1,"quote":"A strong validator might change for reasons other than a change to the representation data","anchorObserved":"§8.8.1 \"Weak versus Strong\", paragraph defining a strong validator; earlier in §8.8.3 \"ETag\": \"An entity tag is an opaque validator\" (single-line text view line 1)","reason":"Both clauses of teaches are still present verbatim: §8.8.3 defines an entity tag as \"an opaque validator for differentiating between multiple representations of the same resource\", and §8.8.1 says a strong validator \"might change for reasons other than a change to the representation data, such as when a semantically significant part of the representation metadata is changed (e.g., Content-Type)\". Scope (HTTP validator semantics for entity tags) and anchor (§8.8.1 Weak versus Strong, §8.8.3 ETag, Published: June 2022 per RFC header) are unchanged; RFC 9110 is a published immutable spec, so only availability and anchor placement were at issue.","correction":null}
```

Caveats (≤10 lines):

- Immutable published RFC (STD 97, June 2022); the re-fetch tests availability and anchor placement, not content drift. The only date-sensitive element is the row's "published June 2022", confirmed by the fetched header.
- HTML is served with a weak ETag (`W/"0d9f5fb8..."`) and no `last-modified`; the digest above is over the raw HTML bytes, and the RFC's canonical text is fixed.
- Anchor text matches exactly: TOC/body read "8.8.1. Weak versus Strong" and "8.8.3. ETag"; no renumbering or heading drift.
- Row cells unchanged; no correction and no `[r26-recheck S010 STALE]` block required.
- Sibling rows S028/S033 correctly remain distinct scopes (URI schemes, media types), untouched here.
- No tools installed or updated; no builds/tests/linters run; only this report written.
