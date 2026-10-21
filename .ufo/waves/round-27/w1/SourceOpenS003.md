# SourceOpenS003 — S003 live reopen and the preflight inference

Seat: KakeR27.SourceOpenS003 (read-only leaf, no dispatch). Axis judged: freshness.
Milestone: r27-full-citing-set.
Scope: reopen every public URL in `corpus/SOURCES.md` row S003, compare against the
round-27 retained capture, and test the grouped inference at
`corpus/knowledge/static-canonical-preflight.md:53-54`. Row S003 lists exactly one
public URL; no second S003 URL exists in the row.

## Source row apparatus (verbatim from SOURCES.md)

- S003 — GitHub Docs: Configuring a publishing source for your GitHub Pages site.
- URL: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- Tier A, docs, scope: GitHub Pages publishing modes and repository source selection.
- Anchor: "About publishing sources" and the note under "Creating a custom GitHub
  Actions workflow".
- Teaching cell: "GitHub Pages can publish from a selected branch or from a GitHub
  Actions workflow".

## Live reopen

- One public GET, no credentials/cookies; status 200; finalUrl identical to the row URL.
  Response `Date: Wed, 21 Oct 2026 20:02:01 GMT`; curl start 2026-10-21T20:02:01.053Z.
- Live decoded body: 154136 bytes, sha256
  `ced216363c08f7093bfad0eae4c9d20ef7d7ac6c195373ea376e281ae745a9fd`
  (sha256 over the decoded body, matching the manifest convention: decompressed
  round-27 raw hashes to its manifest sha256).
- Round-27 retained: fetch index 1, fetchedAt 2026-10-21T19:59:55.678521+00:00,
  154136 bytes, sha256 `f42d48b59277843e489896f52f97bb9c62e68970f0c3bebb3021b586ba62a3f5`,
  text `fetched/text/S003-1.txt`.
- Round-26 retained: fetchedAt 2026-10-21T15:09:34.198990+00:00, 154136 bytes,
  sha256 `aa758b4a543f792f3afa1ea37edf4042581719510a479a3f45ce3ace58fdf1ac`.
- Scratch copies: `/fast/scratch/hyaku/kake-r27/SourceOpenS003/S003-live.html`,
  `headers.txt`, `access-time.txt`, `S003-retained.html`, `S003-r26.html`.
- Byte comparison: 107 differing bytes r27-retained vs live; 109 r26 vs r27. Every
  difference is a Next.js asset reference (`webpack-*.js`, `2137-*.js`, `4982-*.js`
  chunk hashes, `_buildManifest.js`/`_ssgManifest.js`, `buildId`). Article prose:
  no byte changed.
- Tag-stripped article text: 8335 chars, sha256
  `497a6c08f11585455ae49613b82ddbe0695683838e851ba0e3a19c22b44258d7`
  identical for r26, r27-retained and live. Content freshness: current; r27 capture
  was already current and the live reopen confirms no drift.

## Teaching verdict

HOLD at row scope. Live bytes still read (25 words, "About publishing sources"):
"You can publish your site when changes are pushed to a specific branch, or you can
write a GitHub Actions workflow to publish your site." The second anchor limb also
persists: "A CNAME file in your repository file does not automatically add or remove
a custom domain." No status, recheck or used-by cell is changed.

Caveat carried forward: the ghp-served-set.md line-28 bullet is still non-verbatim
(live text reads "the root of the repository (/) on the source branch or a /docs
folder on the source branch"). The existing `[r26-recheck S003 STALE]` note at
`ghp-served-set.md:87` remains accurate; it is not reopened or duplicated here.

## Inference test — static-canonical-preflight.md:53-54

Target inference (grouped citation S001-S006): "Prepare the manifest over actual
built/deployable HTML when that artifact exists, not over an assumed checkout
served set."

Retained quote (22 words; verified as a normalized-whitespace substring of
`fetched/text/S003-1.txt`, so it satisfies the count_c1 source-quote rule):

> If required by your site, build any static site files. Use the
> actions/upload-pages-artifact action to upload the static files as an artifact.

Anchor: heading "Creating a custom GitHub Actions workflow to publish your site",
then the "The general flow of a workflow is to:" ordered list, steps 3-4 (after
`actions/checkout`, before `actions/deploy-pages` deploys the artifact). Live raw
HTML confirms the two steps are adjacent `<li>` items; the raw bytes split the
sentence across `<li>`/`<a><code>` markup, and the retained text rendering joins it.
Fetch index 1.

Classification: indirect contribution.

- Direct support for one sub-premise only: deployment consumes an uploaded artifact,
  and a build step may sit between checkout and that upload, so the deployable set is
  not necessarily the checkout's served files. The following list item deploys "the
  artifact", not the repository tree.
- Not direct support for the recommendation itself: S003 never mentions canonical
  manifests, HTML preflight, or targeting build output. "Prepare the manifest over
  it" is the lane's local operational step; the ledger must label it as synthesis.
- Not a contradiction. The branch-mode text is consistent: only the selected source
  folder is published, so a whole-checkout assumption is also wrong there.
- Secondary context (not the ledger quote; 24 words): "the source folder can either
  be the root of the repository (/) on the source branch or a /docs folder on the
  source branch". This supports "checkout is not the served set" for branch
  publishing but carries no build/artifact implication.
- Grouped-scope caveat: S003 alone does not entail the 53-54 sentence. With S001/S002
  (artifact exclusions), S004 (artifact shape), S006 (Jekyll exclusions) the six
  jointly motivate the advice. The S003 pair can be HOLD at grouped scope with the
  inferential step named; it must not be cited as proof that a manifest over build
  output was tested.

## Uncertainties and gaps

- S003 does not say the uploaded static files are HTML, nor that served bytes equal
  uploaded bytes; Pages processing between artifact and response is not described.
- The build step is conditional ("If required by your site"), so the artifact can
  equal checkout contents for a no-build site. The supported claim is "artifact, not
  checkout", not "always built".
- The page is a client-hydrated Next.js document; only tag-stripped text was proven
  equal. BuildId rotation between captures is [INFERENCE] edge-cache/deploy
  variation, not content change.
- This report judges only the S003 x static-canonical-preflight.md pair. S003 x
  sitemap-orphan-audit.md also appears in `c2-oracle.json` `expectedPairs`, enumerated
  through that file's metadata range "S001-S006" (line 2); it is not adjudicated here
  and not dropped — denominator unchanged, owned elsewhere.
- No source row addition, no broad download, no corpus edit by this seat.

## Reproducible commands (scratch-only writes)

```sh
cd /fast/scratch/hyaku/kake-r27/SourceOpenS003
date -u +%Y-%m-%dT%H:%M:%S.%NZ > access-time.txt
curl -sS -L --compressed --max-time 30 \
  -A 'kake-source-reopen/1.0 (public docs freshness check)' \
  -D headers.txt -o S003-live.html -w 'http_code=%{http_code} size=%{size_download}\n' \
  'https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site'
sha256sum S003-live.html
gzip -dc /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-27/fetched/S003-1.raw.gz | sha256sum
```

Checks were not run on the lane (L1 runs integration checks). No tool installs; no
pacman, upgrade or service operation was performed.

Report: `.ufo/waves/round-27/w1/SourceOpenS003.md`
