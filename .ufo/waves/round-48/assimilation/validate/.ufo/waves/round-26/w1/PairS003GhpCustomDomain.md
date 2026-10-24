# PairS003GhpCustomDomain: round 26 freshness (knowledge seat)

Pair: S003 × `corpus/knowledge/ghp-custom-domain.md` · Axis: freshness · Milestone: r26-recheck-build · Seat: KakeR25.PairS003GhpCustomDomain-6

**Result:** 13 statements judged: 13 HOLD, 0 STALE. Every S003-dependent statement still matches the 2026-10-21 bytes. Four flags (F1 to F4) go to L1; none changes content. No correction is required.

## Receipts
- Entry judged: `corpus/knowledge/ghp-custom-domain.md`, 58 lines, sha256 `95fb13e245d9e4debbfa12fcb4b152675d02a1fec6356b7502e83c344ce262a6`. This equals `.ufo/waves/round-21/frozen/before/expected.json:13`, so the text judged is unchanged since round 21.
- S003 raw: `fetched/S003-1.raw.gz`, 154136 bytes, sha256 `aa758b4a543f792f3afa1ea37edf4042581719510a479a3f45ce3ace58fdf1ac` (equals `manifest.json:94`). HTTP 200, `text/html`, no ETag or Last-Modified, fetchedAt `2026-10-21T15:09:34Z` (`manifest.json:85`).
- S003 text view: `fetched/text/S003-1.txt`, 8311 chars, sha256 `0a510dac7bbc93f1ea27185425cb8b53a60eec665242aebf3ab7681eb634a643`. Every quote below is an exact substring of this file (counted in-process) and has 25 words or fewer.
- Registry row: `corpus/SOURCES.md:11`. Anchor "About publishing sources and note under Creating a custom GitHub Actions workflow".
- Lane anchors: read-only `git show cb807bc:<path>` for base lines; working-tree reads for current lines.

## Statements

| # | Entry line | Statement (S003 link) | Verdict | Verbatim quote, S003-1.txt | Anchor observed · flag |
|---|---|---|---|---|---|
| 1 | :1 | Header attributes the entry to S003; S003 is the source of the NOTE at :22 | HOLD | "Configuring a publishing source for your GitHub Pages site" | Page title and in-article heading; matches SOURCES.md:11. · F4 |
| 2 | :2 | `verified-at: 2026-10-19` covers the S003 check | HOLD | "A CNAME file in your repository file does not automatically add or remove a custom domain." | Re-fetched 2026-10-21 (manifest.json:85). · F1 |
| 3 | :7-9 | Claim: under workflow publishing the custom domain is set as Pages configuration (S003 side) | HOLD | "Instead, you must configure the custom domain through your repository settings or through the API." | Section "Creating a custom GitHub Actions workflow to publish your site", Note. · "is ignored" is S005's wording, not S003's (see Excluded). |
| 4 | :13-15 | r20: "the documented mechanism depends on Pages publishing mode" (S003 side) | HOLD | "You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site." | "About publishing sources". · none |
| 5 | :13 | "Refines `corpus/knowledge/publish-channels.md:9`" | HOLD (base-scoped) | "Under "Build and deployment", under "Source", select GitHub Actions." | Base cb807bc :9 is "`CNAME` file pins `ds4cc.com`." Working tree :13 has the same text; the +4 shift is the provenance block at lines 1-4. · F2 |
| 6 | :14 | "`SKILL.md:16`: those lines attribute the domain to a repository file" | HOLD | Same as row 5 | SKILL.md:16 is the same row at cb807bc and now (`CNAME` = ds4cc.com, plus r20 tail). · none |
| 7 | :17 | "Source checks (quotes reopened 2026-10-19)" | HOLD | "A CNAME file in your repository file does not automatically add or remove a custom domain." | Quote still verbatim. · F1 |
| 8 | :22 | Label "S003, custom-workflow NOTE" and its anchor | HOLD | "Creating a custom GitHub Actions workflow to publish your site" | The NOTE follows "Managing environments for deployment." in that section. SOURCES.md:11 anchor still matches. · none |
| 9 | :22-23 | Quoted NOTE: "A CNAME file in your repository file does not automatically add or remove a custom domain." | HOLD | "A CNAME file in your repository file does not automatically add or remove a custom domain." | Verbatim in the text view (count 1, 16 words). Raw HTML wraps `CNAME` in `<code>`, so the plain string is absent there; the text view is the quote authority. · none |
| 10 | :23-24 | "It directs configuration to repository settings or the API." | HOLD | "Instead, you must configure the custom domain through your repository settings or through the API." | Faithful paraphrase. · none |
| 11 | :29-32 | Falsifier: "applying the workflow-specific conclusion to its current setup" (S003 scope) | HOLD | "A CNAME file in your repository file does not automatically add or remove a custom domain." | Workflow scope is the NOTE's section. Branch half (:32) is S005's; it is consistent with retained S005 (Excluded). · none |
| 12 | :44 | "Replayable claim: gives the authoritative docs, exact recheck argv, and count." | HOLD | "A CNAME file in your repository file does not automatically add or remove a custom domain." | The only argv (:3) checks S005's phrase; the S003 NOTE has no replay. · F3 |
| 13 | :46 | "Admission authority: official Pages docs and API schema support the distinction." | HOLD | "Publishing with a custom GitHub Actions workflow"; "Publishing from a branch" | Both mode headings are present (count 2 each). The API half is S007's. · none |

## Excluded (no S003 dependency, or another seat's row)
- :3 recheck argv (S005 seat). Its backticked string does not occur in the retained S005 text view (0 backticks in that file; the plain phrase occurs twice), so "2 matches" is not reproducible from retained bytes.
- :18-21 and :25-27 (S005 and S007 bullets): other seats.
- :34-39 Named debt: no S003 dependency. Anchors hold: SKILL.md:16 is the GH Actions row; publish-channels.md:5-9 includes the ds4cc pages.yml bullet at :9.
- :41 Recheck (2026-10-19) (S005 seat): the date is superseded by the 2026-10-21 S005 fetch.
- :50-58 S007 erratum: S007 seat.
- Retained S005 wording consistent with rows 3 and 11: "no CNAME file is created, and any existing CNAME file is ignored" (2 hits); "this will create a commit that adds a CNAME file directly to the root of your source branch." (2 hits).

## Flags (no content change; L1 decides)
- **F1 DATE-SUPERSEDED (rows 2, 7).** The 2026-10-19 check dates are older than the 2026-10-21 retrieval. The quoted sentences are present in the 2026-10-21 bytes. This round retains no 2026-10-19 S003 bytes, so a change between the dates cannot be excluded; it is only not visible now. Optional receipt A.
- **F2 ANCHOR-SCOPE (rows 5-6).** `publish-channels.md:9` is base-scoped: the entry header says "at base cb807bc", and the lane's own tails write "Base ... :9". At cb807bc, :9 is the CNAME line, so the anchor holds. In the working tree the line is :13 (+4, the provenance block). Judged HOLD. If L1 reads the anchor as a working-tree pointer, row 5 becomes STALE (9 to 13), correction B applies, and the JSON would read stale 1. Optional pointer B.
- **F3 COVERAGE (row 12).** Pre-existing gap: the replay argv covers S005 only. Optional replay C; its `.md` URL is [INFERENCE], not fetched in this lane.
- **F4 PROVENANCE (row 1).** The header names only S005's URL and anchor (§Configuring an apex domain, still present: 4 hits in S005-1.txt). S003's URL and anchor live in SOURCES.md:11. Nothing changed, so no correction.

Out of pair, not judged: `publish-channels.md:59` and `:61` and `SKILL.md:16` and `:229` carry r20 tails that cite S003. They live outside the entry.

## Optional appends (not STALE; not in corrections; append after line 58; no original line rewritten)

A (F1):
```
Round-26 recheck (appended 2026-10-21; no content change): the S003 sentences cited above are still verbatim in the publishing-source page retrieved 2026-10-21T15:09:34Z (HTTP 200; raw sha256 aa758b4a543f792f3afa1ea37edf4042581719510a479a3f45ce3ace58fdf1ac). The 2026-10-19 dates above stand for the earlier check.
```

B (F2):
```
Round-26 pointer (appended 2026-10-21): the attribution cited at line 13 as `corpus/knowledge/publish-channels.md:9` is line 9 at base cb807bc ("`CNAME` file pins `ds4cc.com`."). In the working tree that line is `corpus/knowledge/publish-channels.md:13`; lines 1-4 of that file are now the provenance block.
```

C (F3), [INFERENCE: the `.md` URL form was not fetched in this lane; L1 confirms before appending]:
```
Round-26 replay for the S003 NOTE (appended 2026-10-21): `curl -fsSL 'https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site.md' | grep -cF 'does not automatically add or remove a custom domain.'` Expected count 1 (count 1 in the retained text view).
```

## Verdict JSON

```json
{"pair":"S003xghp-custom-domain","statements":13,"hold":13,"stale":0,"corrections":[]}
```

Tools: none installed or updated. Only Python stdlib (hashing, substring counts) and read-only `git show` were used; no network. Nothing was written except this report.

Report: .ufo/waves/round-26/w1/PairS003GhpCustomDomain.md
