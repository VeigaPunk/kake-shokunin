# Knowledge07 — ghp-custom-domain.md provenance audit (round 21, w1)

## Behavior / gate result
- Target `corpus/knowledge/ghp-custom-domain.md` already opens with the provenance trio (`source:`, `verified-at:`, `recheck:`) followed by one blank line. Per assignment, **left unchanged**.
- No file edits. No commits. No rechecks or network reads run. No credential or auth files read.
- Target sha256 `95fb13e245d9e4debbfa12fcb4b152675d02a1fec6356b7502e83c344ce262a6` is identical to `.ufo/waves/round-21/frozen/before/corpus/knowledge/ghp-custom-domain.md`. The trio was present at the round-21 base.
- Prefix measurement (existing, not added this round): lines 1-4 = **540 bytes** (lines 1-3 = 539 bytes; the blank line is byte 540). File is 58 lines.
- Tools installed or updated: none.

## Field truth audit

| Field | Status | Evidence |
|---|---|---|
| `source:` IDs S003, S005, S007 | Supported. Registry rows exist in `corpus/SOURCES.md` (S003 line 11, S005 line 13, S007 line 15), each "fetched 2026-10-19". | `corpus/SOURCES.md`; `.ufo/round-20/resume/sources-gate.md` S005 location "Configuring an apex domain," step 4 |
| `source:` URL | Partial. The line gives only the S005 URL. S003 and S007 URLs are not in the line; they are only in SOURCES.md. | `corpus/SOURCES.md` rows S003, S007 |
| `verified-at:` date 2026-10-19 | Supported as the original evidence date. Matches SOURCES.md "fetched 2026-10-19" and gate "Accessed: 2026-10-19". Not today; not a live recheck. | `corpus/SOURCES.md`; `sources-gate.md` |
| `verified-at:` wording | **Deficient.** No "historical-not-live-reverified" token, which the S019 metadata contract requires. "REST API opened" is ambiguous: body says "No API call was made" for S007, so it refers to the docs page only. | Entry body line 27 |
| `recheck:` command | Concrete and public, no credentials. Phrase `any existing \`CNAME\` file is ignored` matches the recorded S005 gate quote. **Not local**: it is a live `curl` of public docs; no local snapshot of the S005 page exists. It covers **only S005**; it has no check for the S003 or S007 claims. No restore-or-retire requirement. Not run (assignment). The `.md` URL suffix is untested. | Entry line 3; `sources-gate.md` S005 |
| S005 body quote "no `CNAME` file is created, and any existing `CNAME` file is ignored" | **Not in the gate.** Recorded quote is "any existing `CNAME` file is ignored and is not required." Body paraphrases "branch publishing ... creates a root file" and "recommends domain verification and warns against wildcard DNS" have no recorded quote or location. | Entry lines 18-21; `sources-gate.md` S005 |
| S003 body quote "A CNAME file in your repository file does not automatically add or remove a custom domain." | **Not in the gate.** The recorded S003 quote is "You can publish your site when changes are pushed ..." (location "About publishing sources"). The custom-workflow NOTE quote has no local record. | Entry lines 22-24; `sources-gate.md` S003 |
| S007 "`build_type` is `legacy`, `workflow`, or null"; "update endpoint accepts both fields" | **Not in the gate.** The recorded quote is only "`build_type`: string or null". The enumeration and the update-endpoint claim have no recorded quote. The cname "string-or-null" claim matches the recorded schema quote and the round-20 erratum. | Entry lines 25-27; `sources-gate.md` S007; entry erratum lines 52-58 |
| Cross-refs `publish-channels.md:9`, `SKILL.md:16` | Supported. Line 9 contains "`CNAME` file pins `ds4cc.com`"; SKILL.md:16 contains the ds4cc `CNAME` = ds4cc.com line with r20-correction. | `corpus/knowledge/publish-channels.md:9`; `SKILL.md:16` |
| Absence flags (`build_type` unknown; 2026-10-12 prune; operator/webzites owner) | Preserved. Consistent with SKILL.md:16 comment and SCORECARD named checks. | Entry lines 34-39 |
| S019 metadata contract | **Unresolvable now.** S019 is absent from `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`; no `corpus/CORPUS.md` exists. L1 registration is pending. | glob of `corpus/`; grep for S019 |

## Findings (not fixed; target preservation rule)
1. Three body quotes (S003 NOTE, S005 "no `CNAME` file is created", S007 build_type enumeration) are not recorded in any round-20/21 gate artifact. They are unverified locally. They need an operator-authorized or lane-owned re-open in a future round, which this seat is not permitted to do.
2. `recheck:` covers one of three sources and is network-bound, not local. Source has not been observed vanished, so the conditional restore-or-retire clause is not triggered; the gap is coverage and locality.
3. `verified-at:` lacks the historical-not-live-reverified token required by S019 (once registered).
4. `source:` gives one URL for three IDs.

## Out of scope / handoff
- Field-count coverage: L1 job (not counted here).
- Did not edit SCORECARD, LOG, QUALITY, SOURCES, README, SKILL, or any sibling entry.
- Main to verify: none assigned to this seat. Suggested for main: re-confirm the three unrecorded quotes in the next gate round, and register S019 in CORPUS.md.
