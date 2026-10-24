# PairS033 × static-canonical-preflight: round-26 freshness recheck

- Seat: KakeR25.PairS033StaticCanonicalPrefl-6 (knowledge pair, leaf, no dispatch). Milestone r26-recheck-build. Axis: freshness. Date: 2026-10-21.
- Entry: `corpus/knowledge/static-canonical-preflight.md` (tag #8B13, 180 lines).
- Source: S033 = RFC 9110 HTTP Semantics, https://www.rfc-editor.org/rfc/rfc9110.txt (SOURCES.md:41). Row teaches: «Media types have token type/subtype and optional parameters; nullable omitted headers are distinguished from malformed values by the receipt schema».
- Retained bytes: `fetched/S033-1.raw.gz`, decompressed body sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, equal to manifest.json row S033 index 1 (status 200, error null, fetchedAt 2026-10-21T15:10:52.138664+00:00). Text view `fetched/text/S033-1.txt`: 457,303 characters, one flattened line. Offsets below are character offsets into that view.
- Census note: S028 and S033 share this URL and body digest (separate GETs at 15:10:49 and 15:10:52). The census W04 duplicate-URL warning is nonfatal and inherited.

## Statements attributed to S033

S033 is cited once (line 159) and relied on in one bullet (line 174). The file has no r20-correction tail. Its only correction tails are `[r23-correction]` at lines 140 and 143, and neither cites S033. The round-24 section (lines 157-180) is the only later appended section that touches S033.

| # | Location | Statement | S033 dependency | Verdict | Quote (verbatim, S033-1.txt) | anchorObserved | Reason |
|---|---|---|---|---|---|---|---|
| 1 | L159 | "S033 (RFC9110 §8.3.1 and §5.6.6)" | cite | HOLD | `The type/subtype MAY be followed by semicolon-delimited parameters (Section 5.6.6) in the form of name/value pairs.` (16 words) | §8.3.1 "Media Type" heading @126997 (TOC @4793); sentence @127451. §5.6.6 "Parameters" heading @75771 (TOC @3997). | Both cited sections exist with the cited content. SOURCES.md:41 lists §8.3, §8.3.1, §5.6.2, §5.6.6; line 159 cites a subset, which is fine. |
| 2 | L159 | "all opened this round" | provenance | UNVERIFIABLE | none | none | The round-24 open event is not in the retained bytes. The round-26 fetch (2026-10-21T15:10:52Z) is consistent with a 2026-10-21 open but cannot decide it. Not counted. |
| 3 | L174 | "contentType permits null for an omitted header" | rely on §8.3 absence rule (not cited at L159) | HOLD | `If a Content-Type header field is not present, the recipient MAY either assume a media type of "application/octet-stream"` (18 words) | §8.3 "Content-Type" heading @124861; sentence @125677. | RFC 9110 gives an absent Content-Type a recipient-handled meaning, distinct from a malformed value. That supports the null-for-omitted distinction. The null mapping itself is local schema policy, which the bytes do not decide. |
| 4 | L174 | "(not-served)" | local label | UNVERIFIABLE | none | none | "not-served" is local receipt vocabulary (see L155). RFC 9110 has no such category. Whether a served response without Content-Type records null is local behaviour. See advisory A2. |
| 5 | L174 | "or an HTTP media-type string" | rely on §8.3.1 grammar | HOLD | `media-type = type "/" subtype parameters type = token subtype = token` (12 words) | §8.3.1 grammar block @127331. | Grammar matches. |
| 6 | L174 | "Type/subtype comparison is case-insensitive" | rely on §8.3.1 | HOLD | `The type and subtype tokens are case-insensitive.` (7 words) | §8.3.1 @127401. | Direct match. Parameter-name case-insensitivity (§5.6.6 @76166) is not claimed at L174. |
| 7 | L174 | "semicolon parameters may be empty under RFC9110" | rely on §5.6.6 grammar | HOLD | `parameters = *(OWS ";" OWS [ parameter]) parameter = parameter-name "=" parameter-value` (12 words) | §5.6.6 grammar @76013. | `[ parameter]` is optional, so empty `;`-separated elements are grammatical. The raw body spells the rule `*( OWS ";" OWS [ parameter ] )`; the text view differs in spacing only. |
| 8 | L174 | "field OWS is trimmed" | rely on §5.5 (not cited at L159) | HOLD | `A field value does not include leading or trailing whitespace.` (10 words) | §5.5 "Field Values" heading @66845; sentence @67175. | Supported. §5.5 adds that a field parser "MUST exclude such whitespace" when the HTTP version allows it. Citation gap only, so HOLD, not STALE. |
| 9 | L174 | "Other JSON types and malformed media-type strings reject cleanly." | grammar (row 5) for "malformed"; local behaviour for "reject cleanly" | UNVERIFIABLE | none | none | The grammar defines "malformed". "Reject cleanly" is validator behaviour that the retained RFC bytes cannot decide. Tests are outside this seat's bounds. Not counted. |

Teaches check (row-level, reported for L1; not a knowledge statement):
- Clause 1, "Media types have token type/subtype and optional parameters": HOLD (rows 1 and 5 quotes; "MAY be followed by" makes parameters optional).
- Clause 2, "nullable omitted headers are distinguished from malformed values by the receipt schema": the RFC separates absence (§8.3, row 3) from a grammar violation (§8.3.1). The attribution "by the receipt schema" is local design, which the bytes neither decide nor contradict. This is a row-level attribution issue for RowS033.

## Superseded check (cited version, date, anchor)

- Version: RFC 9110 (June 2022, STD 97) is not obsoleted. The RFC Editor info page (https://www.rfc-editor.org/info/rfc9110/, snapshot 2026-10-18T22:10:11Z) shows Internet Standard, STD 97, published 2022/06/06, with no obsoleted-by or updated-by entry.
- Errata: six verified errata (https://www.rfc-editor.org/errata/rfc9110): 7138 (§12.5.1), 7306 (§14.1.1), 7419 (§8.3.2), 7105 (App. B.1), 7109 (§15.4.9), 8268 (App. B.2). None touches §8.3, §8.3.1, §5.5 or §5.6.6. Reported-but-unverified 9162 (§5.2) and 9164 (App. A) do not change normative text.
- Anchors: §8.3, §8.3.1, §5.5 and §5.6.6 all exist in the retained bytes with the content the entry uses.
- Date: "opened this round" (line 159) cannot be checked from retained bytes (row 2).
- Result: no cited version, date or anchor is superseded.

## Result

- S033-attributed units: 9. Decided: 6 (HOLD 6, STALE 0). UNVERIFIABLE: 3 (rows 2, 4, 9), reported separately and not counted.
- STALE: none, so no correction is required and `corrections` is empty.

## Excluded (not S033-attributed; not counted)

- L159 "an untyped Content-Type could crash the historical counter": a local code-defect claim. No S033 text bears on it.
- L174 "Status/byte counts exclude booleans and audit comparison is recursively type-strict, so false cannot impersonate exit0 or true a count1.": local behaviour.
- L173 (S032) and L175 (S034): other sources.
- L176 "Redirect endpoints must be safe absolute HTTP URLs without controls or userinfo. A body stored for a response that cannot carry content (204/205) is rejected": RFC 9110 material outside S033's anchors and unattributed in the entry. The bytes contain §4.2.4 "Deprecation of userinfo in http(s) URIs" and §15.3.5 ("A 204 response is terminated by the end of the header section; it cannot contain content or trailers."). Route to the S028 pair or the entry owner.

## Advisory (optional; not STALE; not in `corrections`; L1 decides; this seat wrote nothing to the corpus)

- A1, append-only EOF block at L159 (citation coverage): "[r26-recheck S033 advisory] The contentType bullet (line 174) also rests on RFC 9110 §8.3 (absent Content-Type) and §5.5 (field values exclude leading or trailing whitespace), which this Sources line does not list. Verdict unchanged: HOLD."
- A2, append-only EOF block for L174 (local label): "[r26-recheck S033 advisory] RFC 9110 defines no 'not-served' category; the parenthetical on line 174 is local receipt vocabulary. RFC 9110 §8.3 treats an absent Content-Type as a recipient-handled case (assume application/octet-stream or examine the data), not as evidence that the response was not served."

## Other observations (out of pair scope; routed)

- The entry header (lines 1-2) lists S020-S029 only. S030-S034 appear only in later sections.
- SOURCES.md:41 anchors omit §5.5, which line 174 uses (RowS033).
- SOURCES.md:41 teaches attributes a local schema policy to RFC 9110 (RowS033).
- The text view normalizes ABNF spacing. Quotes are verbatim from the text view; semantics are identical.

## Verification performed

- Body digest of the decompressed S033 bytes equals the manifest sha256 (match).
- Each quote occurs exactly once in `S033-1.txt` and is 6-25 words. Rows 1, 3, 5, 6 and 8 also occur verbatim in the whitespace-normalized raw body. Row 7 differs only in ABNF spacing.
- Anchor headings present in the body: §8.3 @124861, §8.3.1 @126997, §5.5 @66845, §5.6.6 @75771.
- Supersession: public reads of the RFC Editor info and errata pages, and one web search.
- Not run: builds, tests, linters. No corpus writes. No site or property probing.

## Tooling

- No tools installed or updated. Python was used in memory only (no files written) for hashing and text search.

```json
{"pair":"S033xstatic-canonical-preflight","statements":6,"hold":6,"stale":0,"corrections":[]}
```
