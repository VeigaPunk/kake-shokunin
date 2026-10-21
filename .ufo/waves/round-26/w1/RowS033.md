# RowS033 — round 26 freshness recheck

Seat: `KakeR25.RowS033-6`. Row: `corpus/SOURCES.md:41` (S033, tier A, kind spec, cadence 365d).
Source re-fetched this round: `#1 https://www.rfc-editor.org/rfc/rfc9110.txt` — HTTP 200, fetchedAt `2026-10-21T15:10:52Z`, body 502,941 B, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`; text view `fetched/text/S033-1.txt` 457,337 B, sha256 `93a20ab9e35d1a59d3d370ed9fc89d2b4a62c45a4a7d5560218bc532c2757853`, complete through Authors' Addresses.

```json
{"id":"S033","verdict":"HOLD","fetchIndex":1,"quote":"media-type = type \"/\" subtype parameters type = token subtype = token","anchorObserved":"§8.3.1 \"Media Type\", first ABNF block (single-line text view); §8.3, §5.6.2 \"Tokens\" and §5.6.6 \"Parameters\" all present at their cited numbers","reason":"Published RFC 9110 (STD 97, June 2022) is immutable; today's 200 body sha256 21c1cdce...232a is identical to the digest recorded for this row in corpus/lessons/round-24.md:32, and all four cited sections retain their numbers and substance. §8.3.1 still defines media-type as token type/subtype plus optional parameters, §5.6.6 still defines name/value parameters, and §8.3 still says an absent Content-Type lets the recipient assume application/octet-stream. scripts/receipt_replay.py still distinguishes absent or present-null contentType from malformed values (parse_media_type:210-227; validation branch:395-415). Scope remains disjoint from S010 (§8.8 validators) and S028 (§4.2 http/https schemes).","correction":null}
```

Caveats (≤10 lines):

- Text view is whitespace-collapsed to one line; the quote was checked as a contiguous 12-word substring with word boundaries in that file.
- Raw bytes were re-verified from `S033-1.raw.gz`; length and sha256 match `fetched/manifest.json` exactly and the same digest is recorded in `corpus/lessons/round-24.md:32`, so no content drift since the row was opened.
- The living `.txt` endpoint serves an immutable standards-track RFC: no `Updated by` header and no obsoletion notice (the two `Obsoleted by` hits are §1.4's table heading/TOC entry), so the "June 2022" pin cannot go stale in place.
- §8.3 supports only the omitted-header fallback (`recipient MAY either assume a media type of "application/octet-stream" or examine the data`); the omitted-versus-malformed distinction is, as the row states, receipt-schema policy, and the reader still implements it.
- Reader inspection was read-only corroboration; no builds, tests or linters were run per assignment.
- No correction block is required and no row cell was changed; only this report was written.
- No tools were installed or updated.
