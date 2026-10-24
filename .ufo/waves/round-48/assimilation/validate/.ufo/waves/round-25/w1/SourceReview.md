# SourceReview — round25 C1 source population vs pinned WCAG 2.2

Seat: `KakeR25.SourceReview` · Date: 2026-10-21 · Milestone: r25-build-accessibility-packet
Axes (godspeed): **operability** (population completeness is what the packet/counter stand on), **freshness** (pinned-snapshot identity re-verified today).
Scope: pinned `.ufo/waves/round-25/population.json` vs the dated Recommendation `https://www.w3.org/TR/2024/REC-WCAG22-20241212/` only. No live-site work, no latest-version comparison, no r24 material, no capability execution, no lane mutation beyond this file.

## Verdict

**COMPLETE — no errors found.** The finalized population (sha256 `4751dc24db2e3698c2b276bb81bff57412c8fbf6c1c0a62f1aa2ad9e0f903058`, re-hashed this seat after integration) contains exactly the 55 active Level A/AA success criteria of the pinned WCAG 2.2 Recommendation: **31 A + 24 AA = 55**, zero duplicates, zero missing, zero extra, 4.1.1 absent, all 31 AAA absent. Every id, title, level, and anchor matches the pinned document byte-verified via its hash.

## Source identity (freshness evidence)

Three independent copies are byte-identical, sha256 `6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057`:

1. lane snapshot `.ufo/waves/round-25/source-wcag22.html` (512,457 bytes),
2. fresh fetch of the pinned URL this seat (2026-10-21 13:27 UTC, HTTP 200, `content-location: Overview.html`, `last-modified: Thu, 12 Dec 2024 10:36:22 GMT`),
3. `sourceSha256` embedded in `population.json`.

Source metadata, quoted from the snapshot front matter (lines 204, 211–253):

- Title: `Web Content Accessibility Guidelines (WCAG) 2.2`
- State: `W3C Recommendation` — `12 December 2024` (`publishDate: "2024-12-12"`); this is the errata republication of the 05 October 2023 original — changes section: "2024-12-12: Republished WCAG 2.2, incorporating the following errata" (line 4176). Bounded to this dated Recommendation; no latest-version claim made or needed.
- This version: `https://www.w3.org/TR/2024/REC-WCAG22-20241212/` · Latest published: `https://www.w3.org/TR/WCAG22/` · Editor's draft: `https://w3c.github.io/wcag/guidelines/22/` · History: `https://www.w3.org/standards/history/WCAG22/` · Implementation report: `https://www.w3.org/WAI/WCAG22/implementation-report/` · Errata: `https://www.w3.org/WAI/WCAG22/errata/` ("Errata exists").
- Editors: Alastair Campbell (Nomensa), Chuck Adams (Oracle), Rachael Bradley Montgomery (Library of Congress), Michael Cooper (W3C), Andrew Kirkpatrick (Adobe).

## Coverage census (extracted from the pinned snapshot)

- 87 `Success Criterion` sections in the document; **86 active** (carry a level): A 31, AA 24, AAA 31; plus **1 level-less stub**: heading `Success Criterion 4.1.1 Parsing (Obsolete and removed)` (line 2118).
- Population ∩ doc-active A/AA: 55/55; set difference both directions empty. Titles, levels, anchors, and `source` = pinned-URL + `#anchor` all match; no criterion headings outside those sets other than the 31 AAA (1.2.6–1.2.9, 1.3.6, 1.4.6–1.4.9, 2.1.3, 2.2.3–2.2.6, 2.3.2, 2.3.3, 2.4.8–2.4.10, 2.4.12, 2.4.13, 2.5.5, 2.5.6, 3.1.3–3.1.6, 3.2.5, 3.3.5, 3.3.6, 3.3.9) and the 4.1.1 stub.
- Verified A/AA registry — A (31): 1.1.1, 1.2.1, 1.2.2, 1.2.3, 1.3.1, 1.3.2, 1.3.3, 1.4.1, 1.4.2, 2.1.1, 2.1.2, 2.1.4, 2.2.1, 2.2.2, 2.3.1, 2.4.1, 2.4.2, 2.4.3, 2.4.4, 2.5.1, 2.5.2, 2.5.3, 2.5.4, 3.1.1, 3.2.1, 3.2.2, 3.2.6, 3.3.1, 3.3.2, 3.3.7, 4.1.2 — AA (24): 1.2.4, 1.2.5, 1.3.4, 1.3.5, 1.4.3, 1.4.4, 1.4.5, 1.4.10, 1.4.11, 1.4.12, 1.4.13, 2.4.5, 2.4.6, 2.4.7, 2.4.11, 2.5.7, 2.5.8, 3.1.2, 3.2.3, 3.2.4, 3.3.3, 3.3.4, 3.3.8, 4.1.3.
- No `"New"` badge residue remains in the finalized population (checked).

## Removed 4.1.1 — quoted handling in the pinned source

- Introduction (line 394): "WCAG 2.2 has removed one success criterion, 4.1.1 Parsing. Authors that are required by policy to conform with WCAG 2.0 or 2.1 will be able to update content to WCAG 2.2, but may need to continue to test and report 4.1.1."
- Stub note (line 2122): "This criterion was originally adopted to address problems that assistive technology had directly parsing HTML. Assistive technology no longer has any need to directly parse HTML. Consequently, these problems either no longer exist or are addressed by other criteria. This criterion no longer has utility and is removed."

The stub is retained non-normatively in the document; population correctly excludes it.

## Quoted conformance limits (exact, from pinned snapshot)

- §5.2 preamble: "In order for a web page to conform to WCAG 2.2, all of the following conformance requirements must be satisfied:"
- §5.2.1 Conformance Level: "One of the following levels of conformance is met in full."
  - "For Level A conformance (the minimum level of conformance), the web page satisfies all the Level A success criteria, or a conforming alternate version is provided."
  - "For Level AA conformance, the web page satisfies all the Level A and Level AA success criteria, or a Level AA conforming alternate version is provided."
  - "For Level AAA conformance, the web page satisfies all the Level A, Level AA and Level AAA success criteria, or a Level AAA conforming alternate version is provided."
  - Note 1: "Although conformance can only be achieved at the stated levels, authors are encouraged to report (in their claim) any progress toward meeting success criteria from all levels beyond the achieved level of conformance."
  - Note 2: "It is not recommended that Level AAA conformance be required as a general policy for entire sites because it is not possible to satisfy all Level AAA success criteria for some content."
- §5.2.2 Full pages: "Conformance (and conformance level) is for full web page(s) only, and cannot be achieved if part of a web page is excluded."
- §5.2.3 Complete processes: "When a web page is one of a series of web pages presenting a process (i.e., a sequence of steps that need to be completed in order to accomplish an activity), all web pages in the process conform at the specified level or better. (Conformance is not possible at a particular level if any page in the process does not conform at that level or better.)"
- §5.2.4: "Only accessibility-supported ways of using technologies are relied upon to satisfy the success criteria."
- §5.3.1: "Conformance claims are not required. Authors can conform to WCAG 2.2 without making a claim."

Packet framing is consistent with these limits: the packet is readiness-only and never asserts site conformance (population status remains not-assessed; §5.3.1 makes claims optional; §5.2.1 fixes what A/AA coverage must mean here — the full Level A and Level AA sets, which is what the 55 ids are).

## Findings by severity

- **Blocking: none.** No membership, duplication, level, title, anchor, or source-URL defect found in the finalized population.
- **Major: none.**
- **Minor: none.**
- Informational: (1) the pinned URL serves the 2024-12-12 errata republication, not the 2023-10-05 original — downstream citations should keep the dated URI (they do). (2) Each population card still carries both `text` (page blob) and `normativeText`; membership and metadata are unaffected — only `normativeText` should back `sourceQuote` validation. (3) A served-via-CDN fetch could in theory be cache-poisoned, but lane snapshot, live fetch, and population pin agree byte-for-byte, so identity is not in doubt.

## Residual risk and verification gaps

- This seat verified **identity, membership, counts, levels, titles, anchors**. It did **not** diff per-card `normativeText` strings against criterion bodies, and did not apply the ≤25-word `sourceQuote` rule — that is the quote-validation lane's scope; the shared interface and counter already re-derive per-card validity from the same pinned population.
- Freshness is anchored to the dated Recommendation as instructed; no comparison to `/TR/WCAG22/` head or future errata was performed or is required.

## Method note

Static text comparison only: one read-only fetch of the pinned URL plus grep/Python text processing over `/tmp` copies; the lane's own `source-wcag22.html` was hashed, not modified. No builds, tests, linters, counters, or r24 material touched. No tools installed or updated (existing `curl`/`grep`/`python3` sufficed — nothing to record under the tooling directive).
