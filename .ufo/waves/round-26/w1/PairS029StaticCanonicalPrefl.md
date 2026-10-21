# PairS029StaticCanonicalPrefl: round 26 C1 freshness

Pair: `corpus/knowledge/static-canonical-preflight.md` × source S029 (RFC 3986 §3).
Milestone: r26-recheck-build. Judged on: freshness. Re-verification date: 2026-10-21.
Result: 7 statements, 7 HOLD, 0 STALE, 0 UNVERIFIABLE. No corrections. The entry was not modified.

## Evidence basis

- Re-fetched bytes: `fetched/S029-1.raw.gz`. Manifest row S029, index 1, status 200, fetchedAt 2026-10-21T15:10:49+00:00, 141,811 bytes, no retry (`manifest-retry.json` lists S008 only).
- Digest: `gzip -dc fetched/S029-1.raw.gz | sha256sum` = `3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683`. This equals the manifest digest and matches the abbreviated digest (`3102dae4…b2d683`) that SOURCES.md row 37 and population row S029 record at open (2026-10-21). The content is unchanged since it was opened.
- Quotes: `fetched/text/S029-1.txt` (122,035 bytes, whitespace-normalized text view), as the contract requires. Quotes for rows 3-7 were also matched in the live RFC Editor text read 2026-10-21. The header words of rows 1-2 appear there in column-split form, not as one contiguous string.
- Status and errata: RFC Editor info pages for RFC 3986, RFC 7320 and RFC 8820, and the RFC 3986 errata records, all read 2026-10-21.

## Verdict table

| # | Entry line(s) | Statement (abridged) | Verdict | Verbatim quote from S029-1.txt (≤25 words) | Anchor observed now | Cited version/date/anchor superseded? |
|---|---|---|---|---|---|---|
| 1 | `:1` | Source row: "S029 RFC 3986 section 3 https://www.rfc-editor.org/rfc/rfc3986.txt" | HOLD | "Request for Comments: 3986 W3C/MIT STD: 66 R. Fielding Updates: 1738 Day Software" | Header block; §3 "Syntax Components" (TOC p.16) | No. Internet Standard STD 66, updated but not obsoleted (see Status) |
| 2 | `:2` | "verified-at: … 2026-10-21 (S028-S029), documentation opened this round" | HOLD | "Category: Standards Track Adobe Systems January 2005 Uniform Resource Identifier (URI): Generic Syntax" | Same header; manifest fetchedAt 2026-10-21T15:10:49+00:00; digest unchanged since open | No |
| 3 | `:80-81` | A `//` reference with an empty authority (`///project/a.html`, also as a base href) is rejected as `canonical_url_invalid` / `base_url_invalid` | HOLD (S029 clause) | "or when the registered name is empty (zero length)" | §3.2.2 Host (zero-length registered name); §3 hier-part `"//" authority` | No |
| 4 | `:82-83` | "RFC 3986 section 3 says a path without an authority cannot begin with `//` (S029), so the reference carries an empty authority" | HOLD | "When authority is not present, the path cannot begin with two slash characters ("//")." | §3 Syntax Components, paragraph after the hier-part ABNF (matches the SOURCES row anchor). Restated at §3.3 Path: "If a URI does not contain an authority component, then the path cannot begin with two slash characters ("//")." | No. RFC 8820 updates §2 only |
| 5 | `:85-88` | urljoin "inherits the base host"; WHATWG "slash-skipping"; "neither reading equals the document host, so rejection is the conservative policy" (S029 rationale only) | HOLD (S029 part) | "A relative reference that begins with two slash characters is termed a network-path reference" | §4.2 "network-path reference" (the reference-level term; the entry and SOURCES anchor §3) | No. The non-S029 parts are flagged in O1-O2 |
| 6 | `:128-129` | Live snapshot: "each http(s) without userinfo" | HOLD | "The user information, if present, is followed by a commercial at-sign ("@") that delimits it from the host." | §3.2.1 User Information (`userinfo = *(unreserved / pct-encoded / sub-delims / ":")`) | No |
| 7 | `:176` | Round-24 receipts: "Redirect endpoints must be safe absolute HTTP URLs without controls or userinfo." | HOLD | Same quote as row 6 | §3.2.1 | No |

Notes on the rows:
- Row 3's local clause (the rejection codes) is not an S029 claim. Statically, `scripts/canonical_audit.py` defines `canonical_url_invalid` (:678, fixture :799) and `base_url_invalid` (:655, fixture :831 with `<base href='///project/'>`). The names exist. Behaviour was not executed.
- Row 5's "neither reading equals the document host" is judged only on its S029 rationale; see O1.

## Statements reviewed and not counted

- `:83-84` (RFC 9110 empty-host clause): belongs to the S028 pair. Cross-reference for that pair: S029 §3.2.2 also says "whereas the "http" scheme considers a missing authority or empty host invalid."
- `:3` "Reopen the cited sections": generic recheck instruction, not an S029 content claim.
- `:76-78` (fragments and queries): RFC 3986 §3.4 and §3.5, outside the row's scope (authority versus path).
- `:140-146` [r23-correction] (S021, S025), `:151` (S030), `:153-155`, `:159-175` (S032-S034, RFC 8259): none cites or relies on S029.
- No "r20-correction" tails exist in the entry (grep found none). The only correction tails are [r23-correction] at `:140-146`.

## Status and errata (checked 2026-10-21)

- RFC 3986: Internet Standard, STD 66, January 2005. The RFC Editor page reads "This RFC was updated, see RFC 7320, RFC 8820." It is not obsoleted.
- RFC 8820 (BCP 190, June 2020): "obsoletes RFC 7320 and updates RFC 3986." Its update is advisory (§2: "This section updates RFC 3986 by advising Specifications how they should define structure and semantics within URIs"). No change to §3 text was found. Grep of RFC 8820 for "3986" hits only the abstract, the introduction, §2, §2.5 and the references.
- RFC 7320, listed by the RFC 3986 page, is itself obsolete (replaced by RFC 8820). This is an RFC Editor listing matter with no effect on the entry.
- RFC 3986 errata records, scanned for section-3 headers and grammar keywords:
  - Verified §3.1 (RFC 2718 becomes RFC 4395). Not cited by the entry.
  - Held for Document Update §3.2.2 reg-name. The proposal keeps `*( … )`, so a zero-length host is still allowed.
  - Held §3.3 path-empty notation (editorial).
  - Held §4.2 relative-part, adding path-abempty. The `"//" authority` branch is unchanged.
  - Rejected §3 (five-rule path wording, 2011) and §3.2.2 dec-octet and IPv6 (2015).
  - No erratum names the "two slash characters" sentences or the §3.2.1 userinfo text.

## Non-freshness observations (no verdict effect, no correction appended)

- O1 (wording, `:85-88`): "neither reading equals the document host" conflicts with the same paragraph's account of urljoin. Checked with `urljoin('https://example.test/project/b.html','///project/a.html')`, which returns `https://example.test/project/a.html`, the base (document) host. The planner may want the sentence reworded.
- O2 (provenance, `:87`): the WHATWG slash-skipping claim has no source row. SOURCES.md:71 records that WHATWG was deliberately not curated. This is not an S029 claim.
- O3 (anchor precision, optional): the reference-level term is §4.2 "network-path reference", and the rule is restated at §3.3. The entry and SOURCES row anchor §3. This is not STALE; the cited §3 rule is intact.
- O4 (scope): SOURCES.md row 37 and population row S029 also list `corpus/lessons/round-22.md` as an S029 consumer. It is outside this pair and was not judged.

## Corrections

None. No statement is STALE, so no append-only block was written.

## Verification gaps

- Local tool behaviour (row 3 codes, rows 6-7 implementation) was checked by static grep only. No tests or builds were run, per the assignment.
- Errata: all records were scanned for section-3 headers and for the grammar keywords (two slash, authority, reg-name, sub-delims, userinfo, network-path). The 488 lines were not read one by one.
- The quoted text is from the normalized text view, as the contract requires. Only the raw digest was compared with the manifest. Each quote's wording was cross-checked against the live RFC Editor text.
- The urljoin check (O1) is a one-line stdlib evaluation, not a test.

## Tooling

No tools were installed or updated. Read-only checks used `gzip`, `sha256sum`, `wc` and a one-line `python3` stdlib call, plus documentation GETs (RFC Editor info and errata pages).

```json
{"pair":"S029xstatic-canonical-preflight","statements":7,"hold":7,"stale":0,"corrections":[]}
```
