# Pair S010 × ghp-etag-anatomy — round-26 freshness

Pair: S010 × `corpus/knowledge/ghp-etag-anatomy.md`, read at tag `#28F7` (56 lines). No corpus files were edited. `L<n>` below means line n of that file.

Source: S010 = RFC 9110 HTTP Semantics, §8.8.1 Weak versus Strong and §8.8.3 ETag. fetchIndex 1, `https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8`, fetchedAt 2026-10-21T15:10:38Z. Decompressed bytes 1,187,554, sha256 `d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5`, recomputed and equal to manifest.json and population.json. Text view: `fetched/text/S010-1.txt`.

Bottom line: 9 S010-dependent statements. 7 HOLD, 2 STALE. RFC 9110 is still an Internet Standard, the retained text matches its manifest hash, and no erratum touches §8.8. Both STALE rows are pre-existing defects in the entry (a wrong locator and an incomplete paraphrase), not source drift.

## Verdict table

| # | Line | Statement (abridged) | Verdict | Verbatim quote (source, ≤25 words) | anchorObserved | Notes |
|---|---|---|---|---|---|---|
| 1 | L1 | Header lists S010 with the nginx raw URL (`…release-1.28.0/src/http/ngx_http_core_module.c`) and `§ngx_http_set_etag` | STALE | "This document describes the overall architecture of HTTP, establishes common terminology, and defines aspects of the protocol that are shared by all versions" | text abstract, line 1 | The only URL given is S009's nginx file. S010's own locator is missing, so the header points S010 at the wrong document. Correction C1. |
| 2 | L2 | `RFC 9110 published June 2022` (S010 version and date anchor) | HOLD | "Category: Standards Track Published: June 2022 ISSN: 2070-1721" | text line 1 header | Version and date hold. RFC 9110 is not obsoleted. The `verified-at: 2026-10-19` date is superseded for S010 by the 2026-10-21 re-fetch (flag only). |
| 3 | L21 | `Source checks (reopened 2026-10-19).` heading over the S010 bullets | HOLD | "8.8.3. ETag The "ETag" field in a response provides the current entity tag for the selected representation" | §8.8.3 ETag | Anchors hold. The 2026-10-19 date is superseded by the 2026-10-21 re-fetch (flag only). |
| 4 | L24–25 | S010 §8.8.3: "An entity tag is an opaque validator for differentiating between multiple representations of the same resource." | HOLD | "An entity tag is an opaque validator for differentiating between multiple representations of the same resource" | §8.8.3 ETag | Verbatim. The source sentence continues ", regardless of whether …". The period inside the quotation marks truncates it and is not a misquote. No correction needed. |
| 5 | L25–28 | S010 §8.8.1 notes a one-second modification time "might be a weak validator" "when changed twice within that second." | STALE | "if it is possible for the representation to be modified twice during a single second and retrieved between those modifications" | §8.8.1 Weak versus Strong, paragraph "Likewise, a representation's modification time …" | The quoted clause is verbatim. The paraphrase drops the retrieval condition, so it overgeneralizes. The gap is in the paraphrase, not in the source. Correction C2. |
| 6 | L30–34 | `[INFERENCE]` same-length updates within one timestamp second can produce the same fields; recorded ETags cannot by themselves certify byte identity | HOLD | "a validator is weak if it is shared by two or more representations of a given resource at the same time" | §8.8.1, shared-validator paragraph | Labelled inference. The RFC supplies the weak-validator premise. The nginx format and its collision behaviour come from S009, not S010. |
| 7 | L51 | QUALITY mapping: "pins nginx release and RFC" | HOLD | "Category: Standards Track Published: June 2022 ISSN: 2070-1721" | text line 1 | The pinned RFC is still the current Internet Standard, STD 97 (rfc-editor info page, meta timestamp 2026-10-18). |
| 8 | L53 | QUALITY mapping: "separates nginx code facts, RFC semantics, and inference" | HOLD | "Validators come in two flavors: strong or weak." | §8.8.1 | S010 remains the RFC-semantics authority the entry relies on. |
| 9 | L56 | QUALITY mapping: "the opaque marker is not treated as a content digest" | HOLD | "An entity tag is an opaque validator for differentiating between multiple representations of the same resource" | §8.8.3 ETag | Holds. Quote verified in both the text view and the decompressed raw HTML. |

## Checks performed

- **Statement enumeration.** I read the full entry and swept it for `validator|opaque|weak|strong|RFC|HTTP|8.8|semantics|one-second|entity tag|r20|tail`. There is no r20-correction tail at `#28F7` (zero `r20` or `round-20` hits). The only appended section is "How it clears corpus/QUALITY.md" (L50–56), covered by rows 7–9. L18–19 ("the token is not a body hash") is not counted; see adjacent notes.
- **Quotes.** Each quote is present in `fetched/text/S010-1.txt`. After tag stripping and whitespace normalization, each appears once in the decompressed raw HTML.
- **Integrity.** The decompressed raw sha256 equals the manifest value (`d431…e1e5`). The gzip container hashes to `8ecfae6d…1a75`; the manifest hashes the decompressed bytes, not the `.gz`.
- **Status.** The rfc-editor info page reads "Internet Standard", STD 97, with the meta timestamp 2026-10-18. The only "Obsoleted by" strings in the raw HTML are the section title "1.4. Specifications Obsoleted by This Document", not a status line. A web search (datatracker group CSV) also lists RFC 9110 as "Internet Standard", not obsoleted.
- **Errata.** The rfc-editor errata page lists Verified (6): EIDs 7105, 7109, 7138, 7306, 7419 and 8268, all in its Verified section. It lists Reported (2), dated 2026-09-01 and 2026-09-07, both unverified. A grep over the whole page for `Section 8\.` finds only §8.3.2 and §8.6, nothing at §8.8, §8.8.1 or §8.8.3.
- **Anchors.** The raw HTML carries `section-8.8` (150 hits), `section-8.8.1` (23), `section-8.8.3` (67), `name-weak-versus-strong` and `name-etag`. The SOURCES.md anchor "Section 8.8.1 Weak versus Strong and 8.8.3 ETag" holds.
- **Row teaches.** SOURCES.md:18 and population.json:246 state "Entity tags are opaque validators, and a strong validator can change for metadata reasons without representation-data changes." It remains supported. Quotes: "A strong validator might change for reasons other than a change to the representation data" (§8.8.1) and the §8.8.3 opaque-validator sentence.
- **Superseded-flag scan.** The S010 section anchors are not superseded. The S010 date anchors on L2 and L21 (2026-10-19) are superseded by the 2026-10-21 re-fetch. That is a freshness flag, not an error. No S010 version is superseded.

## Corrections (append-only; STALE rows only)

Append these at the end of `corpus/knowledge/ghp-etag-anatomy.md`. Do not rewrite L1 or L25–28.

**C1 (row 1, L1 locator):**

```text
## Correction (r26 freshness, 2026-10-21): S010 locator
S010 is RFC 9110, https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8 (§8.8.1 Weak versus Strong; §8.8.3 ETag). The nginx URL on line 1 is the S009 source only.
```

**C2 (row 5, L25–28 paraphrase):**

```text
## Correction (r26 freshness, 2026-10-21): S010 §8.8.1 condition
RFC 9110 §8.8.1 says a one-second modification time "might be a weak validator if it is possible for the representation to be modified twice during a single second and retrieved between those modifications." Two modifications within one second are not by themselves that condition; the retrieval between them is part of it.
```

**Optional re-verification note (not a STALE correction; for the superseded dates on L2 and L21, at the integrator's discretion):**

```text
## Re-verification (r26, 2026-10-21): S010
RFC 9110 re-fetched 2026-10-21 (fetchIndex 1; decompressed sha256 d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5). Published June 2022; Internet Standard; no obsoleting RFC; no erratum cites §8.8. The 2026-10-19 dates on lines 2 and 21 are the earlier check dates.
```

## Adjacent, not counted

- **L18–19** ("the token is not a body hash, so use the recorded SHA-256"). This is grounded in the S009 nginx format (`%xT-%xO`) and carries no S010 citation. Consistent with S010 §8.8.3 if the integrator wants it counted; it would be HOLD.
- **L22–23 and L41–44.** These are S009 (nginx release-1.28.0) statements, outside this pair. The release-1.28.0 pin is a fixed tag, so it is not superseded by later nginx releases. The S009 pair judges the bytes.
- **L3 recheck trigger.** It cites no S010 date or anchor. SOURCES.md:18 has a 365d recheck from 2026-10-19, so the next check is due 2027-10-19 and nothing is overdue.

## Counts

statements 9 · hold 7 · stale 2

## Tooling

No tools installed or upgraded. Used coreutils `sha256sum`, Python stdlib (`gzip`, `hashlib`, `re`) read-only through eval, rfc-editor public pages, and web search. Nothing was written outside the report path.

## Verification gaps

- The S009 pair and the nginx line anchors (1682, 1708–1710) were not re-checked here.
- The errata verdict rests on the rfc-editor errata page as fetched. I grepped it for section mentions but did not read the two Reported entries in full.
- Datatracker status came from a search snippet. The rfc-editor info page is the primary status evidence.

```json
{
  "pair": "S010xghp-etag-anatomy",
  "statements": 9,
  "hold": 7,
  "stale": 2,
  "corrections": [
    "## Correction (r26 freshness, 2026-10-21): S010 locator\nS010 is RFC 9110, https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8 (§8.8.1 Weak versus Strong; §8.8.3 ETag). The nginx URL on line 1 is the S009 source only.",
    "## Correction (r26 freshness, 2026-10-21): S010 §8.8.1 condition\nRFC 9110 §8.8.1 says a one-second modification time \"might be a weak validator if it is possible for the representation to be modified twice during a single second and retrieved between those modifications.\" Two modifications within one second are not by themselves that condition; the retrieval between them is part of it."
  ]
}
```
