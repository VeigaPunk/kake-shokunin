# Round 28 wave 1a3 — Seat SkillTableDraft (C2 freshness leaf)

Seat: `KakeR28a3.SkillTableDraft` (leaf, no subagents). Lane: kake-shokunin.
Assignment: draft the "Field performance triage" decision table for SKILL.md, grounded only in S036 and S037; do not edit SKILL.md.

## Draft deliverable — "Field performance triage" table

| Metric | Good threshold | Poor threshold | Percentile & segmentation | What kake does |
|---|---|---|---|---|
| LCP (loading) | ≤ 2500 ms [F1][F5] | > 4000 ms [F5] | 75th percentile of page loads, segmented mobile vs desktop [F4]; same thresholds for both devices [F9] | No field data: state "no field data" and never infer from lab-only measurement. Good at p75 in a segment: record meeting target. Between good and poor ("needs improvement"): monitor. Poor (> poor threshold): hand off source-fix guidance (optimize-LCP/INP/CLS guides) and flag the owning seat. Missing segment data: say so; never average segments. |
| INP (interactivity) | ≤ 200 ms [F2][F6] | > 500 ms [F6] | same as above [F4][F9] | same policy as LCP row |
| CLS (visual stability) | ≤ 0.1 [F3][F7] | > 0.25 [F7] | same as above [F4][F9] | same policy as LCP row |

### Footnotes (every threshold cell carries S-id + verbatim quote; each ≤ 25 words)

- F1 — S036: "To provide a good user experience, LCP should occur within 2.5 seconds of when the page first starts loading." (19)
- F2 — S036: "To provide a good user experience, pages should have a INP of 200 milliseconds or less." (16)
- F3 — S036: "To provide a good user experience, pages should maintain a CLS of 0.1. or less." (15)
- F4 — S036: "a good threshold to measure is the 75th percentile of page loads, segmented across mobile and desktop devices." (18)
- F5 — S037: "Thus, we conclude that 2.5 seconds is a reasonable "good" threshold, and 4 seconds is a reasonable "poor" threshold for Largest Contentful Paint." (23)
- F6 — S037: "greater than 500 ms is a reasonable "poor" threshold." (9)
- F7 — S037: "so we concluded that 0.25 is an acceptable "poor" threshold." (10)
- F8 — S037: "if at least 75 percent of page views to a site meet the "good" threshold, the site is classified as having "good" performance" (23)
- F9 — S037: "For this reason the Core Web Vitals recommended thresholds are not segregated by device and the same threshold is used for both." (22)
- F10 — S037: "if at least 25 percent of page views meet the "poor" threshold, the site is classified as having "poor" performance." (20)

## Evidence

- S036 opened via `read https://web.dev/articles/vitals` (exit 0), title "Web Vitals", author Philip Walton, "Published: May 4, 2020, Last updated: October 31, 2024". Key statements present: LCP 2.5 s, INP 200 ms, CLS 0.1, 75th percentile segmented mobile/desktop.
- S037 opened via `read https://web.dev/articles/defining-core-web-vitals-thresholds` (exit 0; first read showed lines 1–300 of 441, continued with `:301-441`, exit 0), "Last updated: May 7, 2025". Threshold table row: LCP good ≤2500 ms / poor >4000 ms; INP ≤200 ms / >500 ms; CLS ≤0.1 / >0.25; percentile 75.
- Quote re-check vs fetched bytes (Python stdlib urllib, GET only, exit 0): fetched S036 143,742 bytes and S037 149,322 bytes, stripped tags, collapsed whitespace, then asserted each of F1–F10 verbatim (straight quotes as in source). Final run: ALL 10 PASS. First verification attempt flagged 6 false negatives in S037 quotes; diagnosed as normalization/quote-char artifacts, corrected quote slices (F8 trimmed to a contiguous ≤25-word slice) and re-verified PASS. Accepted threshold values additionally cross-checked against S037's own table (LCP ≤2500/>4000, INP ≤200/>500, CLS ≤0.1/>0.25, percentile 75).

## Findings / notes

- S036 and S037 agree on all good thresholds and the 75th percentile; S037 is the authority for poor thresholds (4000 ms / 500 ms / 0.25) and for "same thresholds across devices, both computed at 75th percentile of page loads, segmented mobile vs desktop".
- S037 documents that thresholds are an achieved balance (perception research range + CrUX achievability, 10–30% poor bucket), i.e. "good"/"poor" are thresholds of record, not a justification for lab inference.

## Out of scope / not verified

- S038 (CrUX methodology) and S039 (CrUX API) not fetched — this wave is S036+S037 only.
- Did not run `c2_source_count`; did not draft the corpus entry (L1's job); SKILL.md not edited.
- No field-data pipeline, CrUX API calls, keys, accounts, or live property probes were used (network bounds respected: only the two named URLs, GET only).
- No tool installs/updates performed (no need; standard python3 stdlib + read tool).
