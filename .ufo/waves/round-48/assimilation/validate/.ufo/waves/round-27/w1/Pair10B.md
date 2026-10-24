# Pair10B — (S006, corpus/knowledge/static-canonical-preflight.md)

Seat: KakeR27.Pair10B, critic/B side, read-only. Axis: freshness. Milestone: r27-full-citing-set.
Independent: Pair10A's report was not read. No ledger, source, or corpus edits. No tool installs.
Scratch: /fast/scratch/hyaku/kake-r27/Pair10B/ (two decompressed HTML copies, used only for diffing).

## Verdict

**HOLD at stated scope — S006 contributes one leg of a local synthesis.** No STALE correction is
required. One optional precision note (not STALE) is drafted below.

## Citing location (range expanded)

- File: `corpus/knowledge/static-canonical-preflight.md`. Same SHA-256 at `be375d9` and in the
  working tree: `833b28f26fa7309f7e31398275bae2f704969d8e6f095bc5bb96250da5c531bc`
  (git blob `d86ddec6e6acc05b3c1f60da87a97a0f2645c8bf`).
- Only citing occurrence: line 54, `S001–S006` (U+2013 en-dash, bytes `E2 80 93`, which
  `count_c1.py` RANGE matches). It expands to S001, S002, S003, S004, S005, S006. There is no other
  S006 literal or range in this file.
- Claim (lines 52-54, blame `c0fd6d5`, 2026-10-20): "Prepare the manifest over actual
  built/deployable HTML when that artifact exists, not over an assumed checkout served set
  (S001–S006, `ghp-served-set.md`)."
- The parenthetical attaches only to "an assumed checkout served set" (that is, checkout ≠ served
  set). The next sentence, "No production artifact was available … in round22", is a local artifact
  claim with no source attribution. It is out of S006's scope and is not judged here.

## Source evidence (r27 retained bytes)

- Manifest: `.ufo/waves/round-27/fetched/manifest.json` (sha256 `d3b0b1ca…d043781`), row S006,
  fetchIndex 1. URL equals finalUrl:
  https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll
  Status 200, fetchedAt `2026-10-21T19:59:56.112484+00:00`, 138096 bytes.
- Raw-body hash recomputed by me: `zcat S006-1.raw.gz | sha256sum` =
  `f0318abe7e63ecded4e7294484bd8cb68721e920b46d0b85399acb2a187742b6`, which matches the manifest.
  The gzip container itself is `55c4501f…c675f4`.
- Text: `fetched/text/S006-1.txt`, sha256 `2d953b39b80cab8f7a51496dbbc627882d5b2451faa0567e0a1008e1bb5aa1f8`.
- Anchor: the raw HTML has `id="configuring-jekyll-in-your-github-pages-site"`. The exclusion list
  is a `<ul>` directly after "By default, Jekyll doesn't build files or folders that:" and before
  the "Front matter" H2.

Quotes, each checked as a substring of the whitespace-normalized text using `count_c1.py` line 50 logic:

| # | Words | Quote | Role |
|---|---|---|---|
| Q1 | 24 | "Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor Start with _,., or # End with ~" | primary support |
| Q2 | 20 | "If you want Jekyll to process any of these files, you can use the include setting in your configuration file." | the exclusions are configurable defaults |
| Q3 | 18 | "Jekyll takes Markdown and HTML files and creates a complete static website based on your choice of layouts." | built HTML is generated, not the checkout bytes |
| Q4 | 23 | "While the github-pages gem remains supported for some workflows, GitHub Actions is now the recommended approach for deploying and automating GitHub Pages sites." | freshness probe (see below) |
| Q5 | 24 | "If you are publishing from a branch, changes to your site are published automatically when the changes are merged into your site's publishing source." | the branch path is still documented |

`"GitHub Pages uses plugins that are enabled by default and cannot be disabled:"` is also present.
It lists jekyll-default-layout, jekyll-readme-index and jekyll-optional-front-matter, which are
further page-level evidence that built HTML differs from checkout HTML. Line 54 does not claim this,
so it is extra support only.

## Freshness: r26 vs r27

- The r26 retained body (`.ufo/waves/round-26/fetched/S006-1.raw.gz`, fetchedAt
  2026-10-21T15:09:35Z) has sha256 `71a69860…dfbd`, also 138096 bytes. `cmp -l` shows 105 differing
  bytes, located only in Next.js chunk hashes (`webpack-091b7f…` → `webpack-89a39c…`) and in
  `buildId` (`ndrfAHwVnt-…` → `tKruMSpttzVE…`).
- The extracted text is byte-identical between rounds (`cmp` reports equal; both `2d953b39…`).
- Conclusion: r27 is a distinct fresh GET (different body hash, timestamp 4h50m later). The document
  content is unchanged, so this is not a source-date drift.
- The r26 receipt `.ufo/waves/round-26/rechecks/S006.json` used the same Q1 quote and HOLD. That
  verdict was for `ghp-served-set.md` and does not carry over to this file's pair. The frozen r26
  ledger has S006 only for `ghp-served-set.md` and `sitemap-orphan-audit.md`.
- Order of events: the source was opened 2026-10-19 (SOURCES row), the claim was authored
  2026-10-20, and the re-fetch was 2026-10-21. No premise postdates the claim.

## Adversarial attempts

1. **Does S006 say "checkout ≠ served set"?** No. The page never mentions checkout, artifact,
   `.nojekyll` or canonical (all four absent from the normalized text). It says Jekyll does not
   *build* the listed paths (Q1). "Not built ⇒ not served" is an inference that relies on
   S003/S004 (publishing source, artifact deploy), not on S006. **[INFERENCE]**
2. **Conditional scope.** S006 applies only where a Jekyll build runs: branch publishing (Q5), or an
   Actions workflow that runs Jekyll. A custom non-Jekyll Actions workflow, or a `.nojekyll` site,
   gets nothing from S006. `ghp-served-set.md:32-33` already says "not every workflow uses that
   build path". Line 54 asserts no universality, so this narrows S006's contribution but does not
   falsify it.
3. **Stale premise via Q4?** The page now recommends GitHub Actions over the github-pages gem. That
   is advisory prose, also present in r26, and it does not remove the branch-build defaults. Line 54
   makes no claim about which path is recommended or common. Q4 is not a stale premise.
   - It is also not retry boilerplate: there was a single fetch and no retry. Note that S008's
     `manifest-retry.json` wording in the r26 paragraphs is an r26 artifact and does not concern
     this row.
4. **Does S006 support "when that artifact exists" or the round22 production-artifact sentence?**
   No. Neither is attributed to S006, and the parenthetical does not extend to it.
5. **Range lumping** (outside my pair; flagged for the L1/S005 seat). `S001–S006` includes S005
   (custom domains), which `ghp-served-set.md` does not cite. It also omits S008, which
   `ghp-served-set.md` does cite. This does not affect S006, which is cited by both the range and
   the pointer file.

## S006's specific contribution (labelled synthesis)

- **S006 entails:** GitHub Pages' Jekyll build skips, by default, `/node_modules`, `/vendor`, names
  starting `_` `.` `#`, names ending `~`, and configured `exclude` paths (Q1). `include` changes
  this (Q2). Jekyll generates the site from Markdown/HTML plus layouts (Q3).
- **Local synthesis, not S006:** "therefore the served set is the build output, so the canonical
  manifest must be prepared over built/deployable HTML rather than the checkout". The served-set leg
  needs S003/S004, and the hidden-file leg needs S001/S002. S006 alone does not entail the
  recommendation. S006 alone does show that, on the Jekyll path, a checkout-derived page list can
  include files absent from the build.

## Suggested C1 ledger record (`.ufo/waves/round-27/pairs.json`, `pairs[]`)

```json
{"row":"S006","file":"corpus/knowledge/static-canonical-preflight.md","kind":"source","verdict":"HOLD","fetchIndex":1,"quote":"Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor Start with _,., or # End with ~","anchor":"H2 'Configuring Jekyll in your GitHub Pages site' (id configuring-jekyll-in-your-github-pages-site), exclusion list before 'Front matter'","reason":"Line 54 range S001–S006 expands to S006; the parenthetical supports 'checkout ≠ served set'. S006 contributes only the Jekyll-build leg: default exclusions (and include/exclude config) mean built output can omit checkout paths. 'Not built ⇒ not served' and the built-HTML manifest recommendation are local synthesis with S003/S004/S001/S002; S006 is silent for non-Jekyll/.nojekyll workflows. r27 GET 2026-10-21T19:59:56Z, body sha256 f0318abe…; text identical to r26 (only Next.js buildId/chunk hashes differ); Actions-recommended note does not alter branch-build defaults. Fresh r27 observation, not carried from r26 ghp-served-set pair."}
```

This conforms to `count_c1.py` as I read it: row/file are in the expanded pair set, verdict and
reason are present, kind is `source`, fetchIndex 1 exists in the manifest with a matching hash, the
quote is 24 words and is a normalized substring, and the anchor is non-empty. HOLD needs no
`[r27-recheck S006 STALE]` marker.

## Optional precision note (NOT STALE; append-only, only if L1 wants scope labels)

> - S006 HOLD (r27, 2026-10-21): in line 54's `S001–S006`, S006 supports only the Jekyll-build
>   leg — GitHub Pages' Jekyll build skips `/node_modules`, `/vendor`, names starting `_`, `.`
>   or `#`, and names ending `~` unless `include` overrides them. That built output, not the
>   checkout, is served, and the built-HTML manifest recommendation is local synthesis with
>   S001–S004; S006 is silent for non-Jekyll workflows. Evidence: w1/Pair10B.md.

Do not use a `[r27-recheck S006 STALE]` marker. Nothing at line 54's stated scope is wrong.

## Uncertainties and operability flags for L1

- **U1 (blocking for counting):** `.ufo/waves/round-27/fetched/` is untracked (`git ls-files`
  count 0). `count_c1.py` reads the manifest, raw and text files through
  `git show <revision>:…`. Unless `fetched/` (manifest, `S006-1.raw.gz`, `text/S006-1.txt`) is
  committed at the measured revision, this record fails with `source_missing`, or with
  `source_hash`/`quote` if the files differ.
- **U2:** The r27 manifest drops the response `headers` that r26 recorded (content-type, date,
  content-length). The r26 last-modified/etag were null, so no source-date signal is lost, but the
  r27 GET carries no server `Date` header.
- **U3:** The `doesn't` apostrophe in the text is U+0027, decoded from `&#x27;`. Do not retype the
  quote with U+2019, or the substring check fails.
- **U4:** "Not built ⇒ not served" is unverified against any real deployed artifact, consistent with
  the entry's own "No production artifact" sentence.

## Discoveries

No new citing pair for S006. The range `S001-S006` in `sitemap-orphan-audit.md:2` (hyphen) already
appears in the frozen 16-missing set as the S003/S005 pairs, and its S006 pair is carried from r26.
The denominator is unchanged by this seat.
