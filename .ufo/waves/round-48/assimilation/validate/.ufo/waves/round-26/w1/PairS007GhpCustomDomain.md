# Pair S007 × ghp-custom-domain — round-26 freshness recheck

- Milestone: r26-recheck-build · Axis: freshness · Seat: knowledge pair (leaf, no delegation)
- Entry: `corpus/knowledge/ghp-custom-domain.md` (58 lines)
- Row: S007 — https://docs.github.com/en/rest/pages/pages (`corpus/SOURCES.md:15`). Row teaches: "The Pages API exposes build_type, cname, and protected_domain_state as distinct fields".
- Re-fetch identity: fetchIndex 1 (`fetched/manifest.json`, row S007), file `fetched/S007-1.raw.gz`, fetchedAt 2026-10-21T15:09:35.741177+00:00, HTTP 200, finalUrl equal to url, 453447 bytes. The manifest sha256 `4f4449ba997276df8acfb9a04aad7dc31c8f95b263ef56c6c7a4aac892097ce0` equals the sha256 of the decompressed body (`zcat`). The gz file's own hash (`1179bd16…`) is not the manifest value.
- Text view: `fetched/text/S007-1.txt` (35495 bytes, one line).
- Result: 20 decided statements, 20 HOLD, 0 STALE. 1 statement UNVERIFIABLE and not counted. 2 date-superseded flags. No correction required.

## Method
1. Listed every entry statement that cites or relies on S007, lines 1–58. This covers the header, the Claim, the r20 correction at base cb807bc (L13–15), Source checks (L17–27), Falsifier (L29–32), Named debt (L34–39), the "How it clears" section (L43–48), and the post-review r20 erratum (L50–58).
2. Judged each statement against the 2026-10-21 bytes. Every quote below is copied from `fetched/text/S007-1.txt` and matched exactly once with `grep -o -F`.
3. Where nullability or `required` membership matters, checked the raw HTML with `zcat fetched/S007-1.raw.gz | grep -b -o -E …`. Offsets below are decompressed-byte offsets. The text view drops `<script>` content (`source_text.py` SKIP set), so these qualifiers do not appear in the text file.

## Verdict table

| # | Entry lines | Statement (abridged) | Verdict | Verbatim quote (S007-1.txt) | anchorObserved | Note |
|---|---|---|---|---|---|---|
| 1 | L1 | Source list includes S007 | HOLD | REST API endpoints for GitHub Pages - GitHub Docs Skip to main content | Page title; sections Get / Create / Update a GitHub Pages site | Attribution holds. L1's URL and anchor (§Configuring an apex domain) belong to S005. S007's own URL is not on that line (it is in SOURCES.md:15). |
| 2 | L2 | verified-at 2026-10-19; "REST API opened 2026-10-19" | HOLD · SUPERSEDED-DATE | API Version: 2026-03-10 (latest) Quickstart About the REST API | Page header | Superseded as the latest verification by the 2026-10-21 re-fetch. The round-26 fetched set holds no 2026-10-19 bytes, so that date cannot be re-decided; content is unaffected. The entry cites no API version. |
| 3 | L9–10 | Pages API exposes cname separately from build_type; build_type distinguishes workflow from legacy | HOLD | The process by which the GitHub Pages site will be built. workflow means that the site is built by a custom GitHub Actions workflow. | §Update information → Body parameters; §Get → embedded response schema (raw 369853 cname, 370449 build_type) | Separate fields confirmed in the response schema and the body schemas. |
| 4 | L10–11 | "does not establish the current mode or configured domain of any lane property" | HOLD | Use the REST API to interact with GitHub Pages sites and builds. | REST API endpoints for GitHub Pages, intro | Documentation cannot establish lane state. Still true. |
| 5 | L13–15 | r20 base: "documented mechanism depends on Pages publishing mode" (S007 share only) | HOLD | legacy means that the site is built by GitHub when changes are pushed to a specific branch. | §Update → build_type body parameter | S007 supplies only the build-mode vocabulary. The mechanism claim rests on S003/S005, which are not judged here. |
| 6 | L17 | Heading "Source checks (quotes reopened 2026-10-19)" over the S007 bullet | HOLD · SUPERSEDED-DATE | Get a GitHub Pages site Gets information about a GitHub Pages site. | §Get a GitHub Pages site (overview) | Reopening date superseded by the 2026-10-21 re-fetch. The L25–27 bullet is a paraphrase without quotation marks, not a quotation. No content change. |
| 7 | L25 | `cname` is string-or-null | HOLD | cname string or null Specify a custom domain for the repository. | §Get → embedded response schema (raw 369853, type ["string","null"]); rendered row under §Update → Body parameters | Get-section nullability exists only in embedded JSON. The text view shows "string or null" only under Update. |
| 8 | L25–26 | `build_type` is legacy, workflow, or null | HOLD (null raw-decided) | Can be one of: legacy, workflow source object Update the source for the repository. | §Get → embedded schema (raw 370449; enum ["legacy","workflow",null] at 370549) | The "or null" appears only in raw bytes. The text view lists legacy and workflow without null. |
| 9 | L26–27 | Update endpoint accepts both fields | HOLD | build_type string The process by which the GitHub Pages site will be built. | §Update information → Body parameters (cname raw 378454; build_type raw 379031) | Both fields are listed as update body parameters. |
| 10 | L27 | "No API call was made" | HOLD | Get a GitHub Pages site Gets information about a GitHub Pages site. | Manifest index 1 URL (docs.github.com) | The retained artifact is a public documentation GET (HTML, HTTP 200), not an api.github.com response. |
| 11 | L29–30 | Falsifier: GET /repos/{owner}/{repo}/pages returning build_type: legacy | HOLD | Request example get /repos /{owner} /{repo} /pages cURL JavaScript GitHub CLI | §Get → Request example; embedded 200 schema (raw 370449) | The text-view GET example omits build_type. The typed 200 schema includes it (raw only). |
| 12 | L35–36 | Current API build_type unavailable after prune (S007 part: API exposes build_type) | HOLD | build_type string The process in which the Page will be built. | §Create → Body parameters (raw 372746); Create 201 schema (raw 376011) | The 2026-10-12 prune and unavailability are lane state and are not judged. |
| 13 | L37–39 | Retain only the relevant response fields; current build_type remains unknown | HOLD | Response schema Status: 200 | §Get → Response schema (200) | The 200 schema defines build_type (raw 370449). "Unknown" is lane state. |
| 14 | L44 | Replayable claim gives the authoritative docs | HOLD (indirect) | Use the REST API to interact with GitHub Pages sites and builds. | S007 intro | Official docs.github.com page, HTTP 200. The entry's recheck argv (L3) covers S005 only; see observation 2. |
| 15 | L45 | Current build mode remains debt with an owner | HOLD (indirect) | build_type string The process by which the GitHub Pages site will be built. | §Update → build_type | S007 names build_type as the build-mode field. The debt itself is lane state. |
| 16 | L46 | Official Pages docs and API schema support the distinction | HOLD | cname string or null Specify a custom domain for the repository. | §Update rendered row; §Get and §Create embedded schemas (raw 369853, 370449, 375415, 376011) | Docs and typed schemas both separate cname from build_type. |
| 17 | L48 | Shape-only probe environment; no API request or credential material retained | HOLD (indirect) | Use the REST API to interact with GitHub Pages sites and builds. | S007 intro; manifest index 1 | The retained S007 bytes are a single docs GET. The manifest records status and response headers only. The raw HTML carries the docs' sample OIDC JWT in the deployment example; that is public documentation sample text, not lane credential material. |
| 18 | L52–54 | Erratum: "cname: required, string or null" is a transcription; the rendered page reads "cname string or null" | HOLD | cname string or null Specify a custom domain for the repository. | §Update rendered row. "required" appears only in embedded `required` lists: raw 371686 (Get 200) and 377248 (Create 201). | The classification holds: "required" is not rendered prose. The embedded schema does list cname as required, which the erratum does not deny. |
| 19 | L56 | Those representations must not be presented as an identical quote | HOLD | cname string or null Specify a custom domain for the repository. | Rendered text: no "required" token beside cname | The normative caution still holds. An identical quote with "required" would not match the rendered prose. |
| 20 | L57–58 | Field claim supported by S007 §Get a GitHub Pages site, response schema; no API request was made | HOLD | `"status": "built", "cname": "developer.github.com", "custom_404": false` | §Get → Response schema (heading present; example JSON); embedded schema raw 369853, 369935 | Anchor resolves and field presence holds. Typed nullability and the required list sit in the embedded schema, not the example. |

## Not decided (UNVERIFIABLE, not counted in JSON)
- L54–55: "The Markdown representation fetched by the L1 exposes `cname`: required, string or null." The L1 artifact is not retained in round 26; only HTML bytes are. Its qualifiers match the current embedded schema (raw 371686 required; 369853 string/null), but that does not decide what the artifact exposed.

## Excluded (no S007 reliance)
- L3 recheck argv (targets the S005 page). L7–8 (S005/S003 claim). L17–24 S005 and S003 bullets. L31–32 second half (S005 root CNAME). L34–35 lane-map label. L41 "Recheck (2026-10-19)" result (S005 argv). L47 citation-local absence. Headings L43 and L50.

## Superseded flags (date / anchor)
- L2 `verified-at: 2026-10-19` and L17 `quotes reopened 2026-10-19`: superseded by the 2026-10-21T15:09:35Z re-fetch (manifest index 1). Content holds, so these are HOLD with a flag, not STALE. STALE is reserved for content, teaching, anchor, or version changes.
- L1 anchor §Configuring an apex domain belongs to S005. It is not superseded, but it is not S007's anchor.
- SOURCES.md:15 S007 row cell "fetched 2026-10-19" is superseded. L1 may log the recheck in the allowed recheck cell. SOURCES.md was not edited here.
- Not superseded: the r20 erratum date (L50), base cb807bc (L13), and anchor §Get a GitHub Pages site, response schema (L57). Both the heading and "Response schema Status: 200" are present in the re-fetched text. The entry cites no API version; the page shows API Version 2026-03-10 (latest), which is not cited.

## Corrections
None. There are zero STALE verdicts, so no append-only STALE block is required.

Optional append (L1 discretion; not a STALE correction; not counted):
```
[r26-recheck S007 HOLD] Re-fetched 2026-10-21 (manifest index 1; decompressed sha256 4f4449ba997276df8acfb9a04aad7dc31c8f95b263ef56c6c7a4aac892097ce0). Statements citing S007 hold against those bytes. The cname and build_type nullability and the cname required list are in the embedded response schema, not in the rendered prose.
```

## Observations for L1 (non-verdict)
1. Text-view gap. `source_text.py` skips `<script>`. The S007 typed schema sits in one `<script type="application/json">` block (raw 367747–453424), so the text file lacks the `null` types, the `required` lists, and the protected_domain_state type. Rows 7, 8, 11, 16, and 18–20 rely partly on raw bytes for those qualifiers. Other rows whose schema lives in script JSON may be affected the same way.
2. No replayable S007 recheck in the entry. The header recheck (L3) greps only the S005 page. Candidate for L1: `curl -fsSL 'https://docs.github.com/en/rest/pages/pages' | grep -cF '"required":["url","status","cname","custom_404","public"]'`. On the retained bytes, `zcat fetched/S007-1.raw.gz | grep -c -F '<same string>'` returns 1. This seat did not run it against the live page.
3. Coverage. The SOURCES row teaches protected_domain_state, which the entry never uses. This is not staleness, and no correction is required.
4. Row 1 cites one URL and one anchor for three sources. S007 is unanchored on that line.

## Raw-byte locators (decompressed offsets, `zcat fetched/S007-1.raw.gz | grep -b -o -E …`)

| Offset | Content |
|---|---|
| 367747 | `<script type="application/json">` opens; closes at 453424. The text view drops it. |
| 369853 | Get-200 schema: "cname" type ["string","null"] |
| 369935 | Get-200 schema: protected_domain_state type ["string","null"] |
| 370449 | Get-200 schema: build_type type ["string","null"], enum ["legacy","workflow",null] |
| 371686 | Get-200 schema: required ["url","status","cname","custom_404","public"] |
| 375415 / 375497 / 376011 / 377248 | Same cname / protected_domain_state / build_type / required in the Create-201 schema |
| 378454 | Update body: cname, type "string or null" |
| 379031 | Update body: build_type, enum legacy and workflow |

## Tooling
No tools installed, upgraded, or updated. Used host `grep`, `zcat`, `sha256sum`, `wc`, `sort`, and `uniq`, all already present.

## Machine-readable summary
```json
{"pair":"S007xghp-custom-domain","statements":20,"hold":20,"stale":0,"corrections":[]}
```
