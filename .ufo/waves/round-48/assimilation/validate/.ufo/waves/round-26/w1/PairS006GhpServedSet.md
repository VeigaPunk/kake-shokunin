# PairS006GhpServedSet — round 26 C1 freshness (knowledge seat)

Pair: S006 × `corpus/knowledge/ghp-served-set.md` (79 lines). Row: `corpus/SOURCES.md:14` (GitHub Docs: About GitHub Pages and Jekyll; status A; used-by this entry). Axis: freshness.

## Re-fetched evidence (fetchIndex 1)

- Manifest `fetched/manifest.json`, row S006, index 1: status 200, error null, `url` = `finalUrl` = `https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll`, `fetchedAt` `2026-10-21T15:09:35.317006+00:00`, bytes 138096, sha256 `71a698604486380c05ca092adbc863dc653fc175eecea5a675891651cd3bdfbd`.
- Retained bytes re-verified in memory: decompressed `S006-1.raw.gz` matches the manifest sha256 and byte count. `manifest-retry.json` has no S006 row.
- Text view `fetched/text/S006-1.txt`: sha256 `847e8190cf0b9635d0e08cf5bdf26b5b6d87457cb381cefa1f67ccae5a879063`, 7,676 bytes, one line.

## Verdicts

| # | file:line | statement attributed to S006 | verdict | verbatim quote (fetched/text/S006-1.txt) | anchor observed | reason |
|---|---|---|---|---|---|---|
| S1 | `ghp-served-set.md:1` | header `source:` lists S006 as a source for this entry | HOLD | "By default, Jekyll doesn't build files or folders that:" | Same URL as SOURCES.md:14. Defaults list sits under h2 "Configuring Jekyll in your GitHub Pages site" (raw `id="configuring-jekyll-in-your-github-pages-site"`). | Row and page unchanged; the passage the entry relies on is still at its anchor. |
| S2 | `ghp-served-set.md:30-31` | "S006's Jekyll defaults skip `node_modules`, `vendor`" | HOLD | "Are located in a folder called /node_modules or /vendor" | Same h2, list item 1. | Still a default exclusion ("By default, Jekyll doesn't build …"). |
| S3 | `ghp-served-set.md:31` | "names starting `_`, `.`, or `#`" | HOLD | "Start with _,., or # End with ~" | Same h2, list item 2. | Same three prefixes. |
| S4 | `ghp-served-set.md:31-32` | "and names ending `~`" | HOLD | "Start with _,., or # End with ~" | Same h2, list item 3. | "End with ~" unchanged. |
| S5 | `ghp-served-set.md:32` | quote "Start with `_`, `.`, or `#`" attributed to S006 | HOLD | "Start with _,., or # End with ~" | Same h2. Raw page markup is `Start with <code>_</code>, <code>.</code>, or <code>#</code>` (one occurrence in raw HTML body). The entry's backticked form is that markup rendered as markdown. | Quote is faithful to the page's own markup. The text view drops code spans and the `, ` separators, so the backticked form has 0 hits in the text view. Extraction loss, not content drift. No correction. |
| S6 | `ghp-served-set.md:32-33` | "not every workflow uses that build path" | HOLD | "If you prefer, you can use other static site generators or customize your own build process locally or on another server." | "About Jekyll" section (other builds). "Building your site locally": "If you are publishing from a custom GitHub Actions workflow, changes are published whenever your workflow is triggered". | Page still separates Jekyll branch builds from custom build processes and Actions workflows. The Note above "About Jekyll" now states "GitHub Actions is now the recommended approach for deploying and automating GitHub Pages sites." That strengthens the scope. |

Totals: statements 6 · HOLD 6 · STALE 0 · UNVERIFIABLE 0.

## Superseded dates, anchors, versions (flags; none makes a statement STALE)

- F1 Date: `ghp-served-set.md:2` `verified-at: 2026-10-19` and `:20` "quotes reopened 2026-10-19" govern the S006 attribution. This round's re-fetch (2026-10-21T15:09:35Z) supersedes that date for S006. Content is unchanged, so no entry correction. L1 may log the recheck in the `SOURCES.md:14` recheck column; appendOnly permits recheck/status logging. The entry itself needs no edit.
- F2 Anchor: "Configuring Jekyll in your GitHub Pages site" still exists as the h2 id above. Not moved.
- F3 Version: the page exposes no version or last-updated field. Manifest `last-modified` and `etag` are null; the raw HTML has no `lastUpdated`, `dateModified`, or `datePublished`. The ISO dates in the raw (2022-11-28, 2026-03-10, 2026-10-16) are API-version and Enterprise Server table values, not page dates. Nothing version-like to supersede.
- F4 Row paraphrase (not an entry statement): `SOURCES.md:14` teaches reads "By default Jekyll skips paths starting with underscore, dot, or hash …". The page says "By default, Jekyll doesn't build files or folders that:". Substance matches; no change for L1.

## Scanned, not counted

- `:14-18` r20-correction: no S006 token. Points at `corpus/knowledge/publish-channels.md:5-14`, which is outside this pair.
- `:37-62` rechecks, tar repro, named debt, prediction: no S006 reliance.
- `:64-69` "How it clears corpus/QUALITY.md": `:67` "platform docs" is generic and does not name S006. If L1 counts it: HOLD (same URL and content).
- `:71-79` round-20 post-review correction: cites S008 only.
- Token scan: "S006" occurs only at `:1` and `:30`; "Jekyll" only at `:30`.
- `corpus/SOURCES.md:47` (reading path) also lists S006. Outside this entry; not judged.

## Checks run

- Every quote cited above is an exact substring of the text view, occurring once.
- Entry quote S5 checked against the text view (backticked form: 0 hits) and against retained raw HTML (`<code>` form: 1 hit).
- Anchor id, page-date absence, and manifest integrity checked against retained bytes.
- Replay:

```
zcat fetched/S006-1.raw.gz | sha256sum                                  # 71a698604486380c05ca092adbc863dc653fc175eecea5a675891651cd3bdfbd
grep -cF 'Start with _,., or #' fetched/text/S006-1.txt                 # 1
grep -cF 'Start with `_`, `.`, or `#`' fetched/text/S006-1.txt          # 0
zcat fetched/S006-1.raw.gz | grep -cF 'Start with <code>_</code>, <code>.</code>, or <code>#</code>'   # 1
```

## Observations for L1 (tooling; no action taken)

- Text-view extraction drops inline code markup and the `, ` separators: `` `_`, `.`, or `#` `` becomes `_,., or #`. A text-view-only verbatim gate will false-fail exact code-span quotes. This is a fetch-tool operability item, not a content issue.
- Tooling: no installs or updates were performed. Used built-in read/grep, `sha256sum`, `wc`, `zcat` (gzip 1.15), and in-memory Python (stdlib gzip/re). No files written except this report. No network access; retained bytes only.

## Gaps

- No prior S006 bytes were consulted, so freshness is judged against the current retained bytes and the entry's stated claims, not a byte diff against the 2026-10-19 fetch.
- All six statements are HOLD, so no STALE correction is required and `corrections` is empty.

```json
{"pair":"S006xghp-served-set","statements":6,"hold":6,"stale":0,"corrections":[]}
```

Report: .ufo/waves/round-26/w1/PairS006GhpServedSet.md
