# PairS003GhpServedSet — S003 × corpus/knowledge/ghp-served-set.md (round 26, freshness)

- Seat: knowledge pair (leaf). Axis: freshness. Milestone: r26-recheck-build. Checked: 2026-10-21.
- Entry: `corpus/knowledge/ghp-served-set.md` (79 lines, read in full).
- Row: S003, GitHub Docs "Configuring a publishing source for your GitHub Pages site" (tier A). Teaches: "GitHub Pages can publish from a selected branch or from a GitHub Actions workflow".
- Bytes judged: `fetched/S003-1.raw.gz` decompresses to 154,136 bytes, sha256 `aa758b4a…fdf1ac`, matching `manifest.json` and `population.json`. Status 200; fetchedAt 2026-10-21T15:09:34Z; no ETag or Last-Modified; finalUrl equals url. Text view `fetched/text/S003-1.txt`: one line, 8,312 bytes, sha256 `0a510dac…a643`.
- Row verdict for S003 is HOLD, consistent with `w1/RowS003.md`. The STALE verdicts below are statement-level. SOURCES.md is untouched.

## Verdicts

| # | file:line | statement | reliance | verdict | verbatim S003 quote (≤25 words) | anchor observed now | reason and flags |
|---|---|---|---|---|---|---|---|
| K1 | :1, :3 | Header lists S003 as a source. Recheck line covers only action releases and workflow changes. | explicit (name) | HOLD | “You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.” (25) | "About publishing sources", first paragraph | Attribution still holds. Coverage gap, not a verdict: :3 never triggers on S003, whose SOURCES.md:11 recheck is 90d. |
| K2 | :2 | "verified-at: 2026-10-19" applies to the S003 quotes. | explicit (date) | HOLD; DATE SUPERSEDED | “About publishing sources You can publish your site” (8) | same section | 2026-10-19 is superseded for S003 by the 2026-10-21T15:09:34Z fetch. Anchor and teaching unchanged. No correction for HOLD. |
| K3 | :7–12 | Premise: an Actions workflow publishes Pages via upload-pages-artifact (the claim concerns that action's exclusion behavior). | implicit (premise, uncited) | HOLD | “Use the actions/upload-pages-artifact action to upload the static files as an artifact.” (12) | "Creating a custom GitHub Actions workflow to publish your site", general-flow list | Premise still stated. The exclusion facts rest on S001, S002 and S004 and are not judged here. |
| K4 | :14–18 (pointer :17–18) | r20 tail: "corpus/knowledge/publish-channels.md:5-14 distinguishes Actions from branch publishing." | implicit (S003 teaching plus a local pointer) | STALE (anchor) | “You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.” (25) | S003 teaching holds. Local pointer fails: publish-channels.md:5–14 has no branch-publishing text (lines 9–15 describe two Actions workflows); the file's only "branch" is line 59. | Correction C1. Scope caveat from S003: “Your GitHub Pages site will always be deployed with a GitHub Actions workflow run” (14). The distinction concerns the publishing source, not whether an Actions run executes. |
| K5 | :20 | Heading "Source checks (quotes reopened 2026-10-19)" covers the S003 bullet. | explicit (date) | HOLD; DATE SUPERSEDED | “About publishing sources You can publish your site” (8) | same section | 2026-10-19 is superseded by the 2026-10-21 fetch. The bullet's wording is judged at K6. No S003 copy from before 2026-10-21 is retained in the tree, and round-20.md:205 records a different S003 sentence, so the 2026-10-19 reopen cannot be replayed. |
| K6 | :28–29 | S003 bullet quotes "the source folder can either be the root of the repository (`/`) or a `/docs` folder." | explicit (quote) | STALE (quote fidelity; teaching HOLD) | “the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch.” (24) | "About publishing sources", second paragraph | The quoted wording is not in the text view or the raw HTML. "on the source branch" is dropped twice with no ellipsis; backticks are markup only. Root-or-/docs substance is unchanged. The identical wording sits at `.ufo/waves/round-21/frozen/before/corpus/knowledge/ghp-served-set.md:28-29`, so it predates round 26. [INFERENCE] Docs wording drift cannot be excluded, since no earlier S003 bytes are retained; the verdict does not depend on it. Correction C2. |
| K7 | :67 | "Admission authority: action, platform docs, and GNU tar manual are cited at their scoped sources." | implicit (S003 is one of the platform docs) | HOLD; DATE SUPERSEDED (dated-doc basis) | “Configuring a publishing source for your GitHub Pages site” (9) | page title and "In this article" nav | QUALITY.md's platform-mechanism bar needs a pinned or dated doc. S003's dated basis, 2026-10-19 (SOURCES.md:11; population.json), is superseded by the 2026-10-21 fetch. |

Totals: statements 7 · HOLD 5 · STALE 2 · UNVERIFIABLE 0.

## Coverage of S003 reliance in the entry

- Explicit: :1 (K1), :28–29 (K6). Dated S003 references: :2 (K2), :20 (K5).
- Implicit: :7–12 (K3), :14–18 (K4), :67 (K7).
- Reviewed with no S003 reliance: :3 command (action only; flagged under K1); :5–6; :21–27 (S001, S002); :29–33 (S004 and S006 bullets; the "S004 steps 4-5" clause is S004); :34–36 (S008); :38–62 (rechecks, tar repro, named debt; :60–62 CNAME prediction does not rely on S003's CNAME note, which bears on ghp-custom-domain.md); :64–66 and :68–69 (QUALITY mapping); :71–79 (r20 S008 erratum, the only later appended section, with no S003 reference).

## Corrections (append-only EOF blocks for `corpus/knowledge/ghp-served-set.md`; not written by this seat, for L1 to apply)

C1 (K4):
```
[r26-recheck S003 STALE] Anchor correction for the r20-correction tail (lines 14-18): the Actions-versus-branch distinction is S003’s, “About publishing sources”: “You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.” corpus/knowledge/publish-channels.md:5-14 does not state that distinction (those lines describe two Actions workflows); its only branch-publishing mention is the r20 tail at line 59. S003 also states “Your GitHub Pages site will always be deployed with a GitHub Actions workflow run”, so the distinction concerns the publishing source, not whether an Actions run executes.
```

C2 (K6):
```
[r26-recheck S003 STALE] Quote correction for the S003 bullet (lines 28-29): the quoted sentence is not verbatim in the 2026-10-21 re-fetch of S003, “About publishing sources”. Verbatim: “the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch.” The root-or-/docs substance is unchanged; the earlier wording dropped “on the source branch” twice.
```

## Checks performed

- Gunzipped `fetched/S003-1.raw.gz` in memory: 154,136 bytes, sha256 `aa758b4a…`, equal to the manifest and population values and to content-length.
- Every quote used is a whitespace-normalized substring of `fetched/text/S003-1.txt`, between 6 and 25 words (longest 25). The K6 quote in the entry is not a substring of the text view, with or without backticks, nor of the raw HTML. The raw HTML carries `<code>/</code>` and "on the source branch" twice.
- `publish-channels.md` searched for "branch": the only match is line 59.
- Corpus and `.ufo` searched for the S003 sentence: current entry, round-21 frozen snapshot, round-26 text. No other S003 byte copy was found.
- `contract.json`: STALE requires an EOF block tagged `[r26-recheck S0NN STALE]` in the citing file; SOURCES row cells are append-only.
- No builds, tests, linters, browsers or live-property probes. The only write is this report.

## Out-of-pair observations (no verdict)

- `ghp-custom-domain.md:22-24` quotes S003's CNAME note. It is verbatim in the text view ("A CNAME file in your repository file does not automatically add or remove a custom domain."). That entry belongs to its own pair.
- `publish-channels.md:59` and `:61` (r20 tails) also cite S003. Not judged here.
- `corpus/SOURCES.md:11` S003 row: "fetched 2026-10-19" and "opened 2026-10-19" are superseded by the 2026-10-21 fetch. Only status, recheck and used-by cells may change.
- Row S003 stays HOLD. K6 is a statement-level quote correction with no row action, consistent with RowS003.md note 4.

## Tooling

None installed, upgraded or removed. No pacman, uv, npm or cargo use.

## Machine-readable summary

```json
{"pair":"S003xghp-served-set","statements":7,"hold":5,"stale":2,"corrections":["[r26-recheck S003 STALE] Anchor correction for the r20-correction tail (lines 14-18): the Actions-versus-branch distinction is S003’s, “About publishing sources”: “You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.” corpus/knowledge/publish-channels.md:5-14 does not state that distinction (those lines describe two Actions workflows); its only branch-publishing mention is the r20 tail at line 59. S003 also states “Your GitHub Pages site will always be deployed with a GitHub Actions workflow run”, so the distinction concerns the publishing source, not whether an Actions run executes.","[r26-recheck S003 STALE] Quote correction for the S003 bullet (lines 28-29): the quoted sentence is not verbatim in the 2026-10-21 re-fetch of S003, “About publishing sources”. Verbatim: “the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch.” The root-or-/docs substance is unchanged; the earlier wording dropped “on the source branch” twice."]}
```
