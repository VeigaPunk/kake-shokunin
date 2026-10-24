# PairS034 × static-canonical-preflight — round 26 C1 freshness

Pair seat: KakeR25.PairS034StaticCanonicalPrefl-6 (knowledge pair, leaf, no dispatch). Checked 2026-10-21.
Result: 9 statements that cite or rely on S034 — 9 HOLD, 0 STALE. No correction blocks are required.

## Scope and provenance

- Entry: `corpus/knowledge/static-canonical-preflight.md` — 180 content lines, sha256 `192eac303fa3ba8a2aab9d545fe6b0627f3a174dff1b54472e1bab2f771fdaf7` (14,076 B). Read in full.
- Source row: `corpus/SOURCES.md:42` — S034 RFC 8259, `https://www.rfc-editor.org/rfc/rfc8259.txt`, anchor "Sections 3, 4, 6 and 9, December 2017; opened 2026-10-21", recheck 365d.
- Re-fetched bytes (`fetched/manifest.json` and `population.json`, S034 index 1): HTTP 200, `text/plain;charset=utf-8`, fetchedAt `2026-10-21T15:10:52.448786+00:00`, body 28,360 B, sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`. The decompressed `fetched/S034-1.raw.gz` matches that digest.
- Text view `fetched/text/S034-1.txt`: 23,045 B, sha256 `80a181c35a15c4108d2d2e70aaa91e7391e4f84d1b92924cd20e012841dcbc24`. One line, whitespace-collapsed, page footers inline (quotes avoid them).
- Unit counted: a distinct claim in the entry that cites S034 or depends on an S034 rule. Offsets are character positions in `S034-1.txt`.

## Verdicts (S034 statements)

| # | file:line | entry statement | S034 basis | verdict | verbatim quote from S034-1.txt (offset, words) | anchorObserved | note |
|---|---|---|---|---|---|---|---|
| 1 | :159 | "S034 (RFC8259 §3/4/6/9)" | cited section anchor | HOLD | "3. Values A JSON value MUST be an object, array, number, or string, or one of the following three literal names: false null true" (@8232, 24 w) | §3 @8232; §4 @8583; §6 @10141; §9 @16082 | Section numbers and topics match the row. Verified errata 7383 (§3 ABNF hex case) and 7600 (§6 leading-zero sentence) touch cited sections, but neither touches a sentence the entry relies on. |
| 2 | :159 | "all opened this round" (round 24, 2026-10-21) | fetch provenance | HOLD | "Request for Comments: 8259 Textuality Obsoletes: 7159 December 2017 Category: Standards Track" (@52, 12 w) | header @52 | Open date rests on SOURCES.md:42 (`opened 2026-10-21`); round-24 records were not opened. The round-26 re-fetch (2026-10-21T15:10:52Z) is a later observation of the same December 2017 document. |
| 3 | :159 | "an untyped Content-Type could crash the historical counter" | JSON value typing (implicit) | HOLD | "A JSON value MUST be an object, array, number, or string, or one of the following three literal names: false null true" (@8242, 22 w) | §3 @8242 | Describes a past defect. The premise that JSON values may be non-string still holds. |
| 4 | :174 | "Status/byte counts exclude booleans and audit comparison is recursively type-strict, so false cannot impersonate exit0 or true a count1." | boolean versus number (row scope) | HOLD | same quote as row 3 (@8242, 22 w) | §3 literal names; §6 number production | RFC 8259 makes false/true literal names, not members of the number production, so the exclusion rests on text that still holds. |
| 5 | :174 | "Other JSON types and malformed media-type strings reject cleanly." | §3 value set (implicit) | HOLD | "value = false / null / true / object / array / number / string" (@8434, 15 w) | §3 grammar @8434 | Rejecting non-string JSON values is local policy that presupposes this set. |
| 6 | :175 | "JSON duplicate names are rejected as local integrity policy" | §4 uniqueness and unpredictability | HOLD | "When the names within an object are not unique, the behavior of software that receives such an object is unpredictable." (@9176, 20 w) | §4 @9176 | The RFC attaches no requirement to rejection; it lists error reporting among observed implementation behaviors. That sentence is split by a page footer, so it is paraphrased, not quoted. Matches the row teaches. |
| 7 | :175 | "(RFC8259 says SHOULD-unique, not MUST)" | §4 normative keyword | HOLD | "The names within an object SHOULD be unique." (@8863, 8 w) | §4 @8863 | Erratum 8622 proposed replacing this sentence. Status Rejected 2025-11-01 ("Consensus is to reject"). SHOULD stands. |
| 8 | :175 | "Non-standard NaN/Infinity … reject without traceback" | §6 values; §9 extension clause | HOLD | "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted." (@10717, 18 w); "A JSON parser MAY accept non-JSON forms or extensions." (@16229, 9 w) | §6 @10717; §9 @16229 | The §9 MAY makes rejection a permitted local choice. "reject without traceback" describes the tool, not the RFC. |
| 9 | :175 | "runtime number/depth overflows reject without traceback" | §9 and §6 implementation limits | HOLD | "An implementation may set limits on the maximum depth of nesting." (@16355, 11 w); "This specification allows implementations to set limits on the range and precision of numbers accepted." (@11127, 15 w) | §9 @16355; §6 @11127 | The RFC permits such limits. The reject and no-traceback behavior is local. |

Totals: statements 9; hold 9; stale 0; corrections none.

## Not counted (no S034 reliance)

| file:line | statement | reason |
|---|---|---|
| :175 | "invalid encodings … reject without traceback" | Rule is RFC 8259 §8.1, outside the row's anchor (3/4/6/9). Retained text: "JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8 [RFC3629]." (@13910, 19 w). See advisory A3. |
| :175 | "Unknown metadata members remain allowed; valid controls are not rejected merely for extra fields." | Local policy with no S034 premise. |
| :159 | "The former lexical timestamp prefix comparison accepted malformed and future strings" | RFC 3339 premise (S032). |
| :173, :176 | timestamp, media-type, redirect clauses | S032, S033, RFC 9110 premises. |
| :140, :143 | `[r23-correction]` tails | Cite S021 and S025 only. |
| :178 | round-24 counter description (130 mutations) | Not S034-attributed in the text. Round-24 counter not opened or run (out of bounds). |

## Premise checks

- The assignment refers to "r20-correction tails". None exist in this entry: `r20` matches 0 lines. The only correction tails are `[r23-correction]` at :140 and :143, citing S021 and S025.
- Appended sections: the round-24 block (:157–:180) is the last section. Every S034 statement sits in :159–:175.

## Freshness of the cited version and anchors

- RFC 8259 is current. The rfc-editor info page (meta timestamp 2026-10-21T08:45:07Z) lists "Internet Standard", STD 90. The datatracker history's latest action is 2026-05-28 "Update from RFC Editor: added verified-errata tag", with no obsoleting action. A web search found no successor (secondary).
- Verified errata (all verified 2026-05-28): 5210 (boilerplate), 5318 (§7 ABNF), 7383 (§3 ABNF hex case), 7600 (§6 leading-zero sentence), 7603 (§1). None alters a sentence the entry relies on. The retained `.txt` predates them: it still reads "Leading zeros are not allowed." (@10443).
- Rejected, no effect: 8622 (§4 SHOULD proposal, 2025-11-01), 8874 (§6, 2026-04-13), 7617 (§6 note, 2026-05-28), 6208 (§8.1 BOM), 7307 (§3 hex), 5218 (§12), 5853 (§11), 7673 (§7).
- Held for document update: 7650 (§7), 8438 (§14.1). Reported, unverified: 9095 (§11).
- Superseded check for S034-attributed statements: none. The version (RFC 8259) is current, the cited sections exist with the row's topics, and the one date anchor is the row's open date.

## Non-S034 flags (out of pair scope; not corrected)

- F1 (superseded recheck pointer): header :3 `recheck:` cites `.ufo/waves/round-22/matrix.py`. The entry says the round-24 maintained entry point supersedes round-22/23 commands "for new structural replay" (:180). The JSON-policy claims at :173–:176 are rechecked through `scripts/receipt_replay.py` (:164–:166). The header pointer no longer covers them.
- F2 (header coverage gap): header :1–:2 list S020–S029 only. S030–S034, cited at :98–:101 and :157–:159, are absent.

## Advisories for L1 (no edits made by this seat)

- A1: SOURCES.md:42 (S034 row). Log the round-26 recheck (HOLD, 2026-10-21) in the allowed recheck and status cells.
- A2: Annotate the S034 anchor with the 2026-05-28 verified errata: 7600 changes the §6 leading-zero sentence; 7383 changes §3 ABNF hex case. The teaches cell is unaffected.
- A3: The encoding clause at :175 sits outside the row's anchor. Either extend the anchor to §8.1 or leave the clause unattributed.
- A4: The row's usedBy also lists `corpus/lessons/round-24.md`. It is not reviewed in this pair.
- A5 (context, secondary): erratum 8622 quotes ECMA-404 §6 saying name strings need not be unique. I did not verify ECMA-404 directly. The entry's claims are RFC-scoped and unaffected.

## Verification performed

- Read the entry in full. Grepped for S034, 8259, JSON, NaN, duplicate, r20, and correction tags.
- Digests: `fetched/S034-1.raw.gz` decompresses to 28,360 B, sha256 61a5378f… (matches manifest and population). The gzip file's own digest (8b9b8064…) differs by design; the manifest records the body digest.
- Quote checks: each quote is an exact substring of `S034-1.txt` with one occurrence and 6–25 words, offsets recorded. The split sentence at @9355 (page footer inside) is not quoted.
- Public documents read: rfc-editor info page and inline errata, errata pages 5318, 7600, and 7383, the errata listing, and the datatracker history. Web search for supersession.
- Tools: none installed or upgraded. In-memory Python stdlib (gzip, hashlib, re) only. No files written except this report. No builds, tests, linters, or measure.py. No round-24 assignment, probe, or counter was read or run.

```json
{"pair":"S034xstatic-canonical-preflight","statements":9,"hold":9,"stale":0,"corrections":[]}
```
