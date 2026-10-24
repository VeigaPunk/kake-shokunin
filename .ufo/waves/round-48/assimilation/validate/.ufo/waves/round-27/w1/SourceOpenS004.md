# SourceOpenS004 — S004 live reopen and preflight-inference test

Seat: KakeR27.SourceOpenS004 (leaf, read-only). Axes named: **freshness** (assigned) and **operability** (preserve the complete expanded citing-set obligation; no gate/implementation judgment).

Author-side evidence only. Parent/L1 judges. No production edits, no commit, no build/test/run, no install.

## Row and target

- `corpus/SOURCES.md` S004: GitHub Docs: Using custom workflows with GitHub Pages — `https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages`; kind docs, tier A; scope "Artifact shape and deployment requirements for custom workflows"; anchor "Configuring the upload-pages-artifact action; fetched 2026-10-19"; opened 2026-10-19; recheck 90d.
- Row teaches: "Pages artifacts are gzip-compressed tar files under 10GB and should contain no symbolic or hard links".
- Target inference (`corpus/knowledge/static-canonical-preflight.md:53-54`, 18 words): "Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set."
- Frozen pairs under review: (S004, `corpus/knowledge/static-canonical-preflight.md`) and (S004, `corpus/knowledge/publish-channels.md`). Other S004 citing files were already r26-decided (see pair table).

## Live reopen — one public GET, no broad download

| field | value |
|---|---|
| request window (UTC) | 2026-10-21T20:01:47Z → 2026-10-21T20:01:50Z |
| server `date` | Wed, 21 Oct 2026 20:01:50 GMT |
| URL / final URL | row URL above; no redirect (status 200, one response) |
| status | HTTP/2 200 |
| x-github-request-id | `E47E:3D48F7:C6C84F:D46C93:6AD91A2B` |
| content-encoding / decoded bytes | `br` / 141818 |
| cache | `x-cache: MISS, MISS`; `age: 0` |
| credentials | none — no cookies, auth header, or account/property operation |
| **sha256 (decoded body)** | **`9ee0766a2fb78e5af104bbc97dfe32ba09ebd8f2d68df1ed2d49efc081a5f53a`** |

Retained comparison (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-27/fetched/manifest.json`, S004 index 1): same URL/final URL, status 200, fetchedAt `2026-10-21T19:59:55.714609+00:00`, bytes 141818, sha256 `9ee0766a2fb78e5af104bbc97dfe32ba09ebd8f2d68df1ed2d49efc081a5f53a`, `file: S004-1.raw.gz`, `text: text/S004-1.txt`. **Live bytes are byte-identical to the r27 retained body.**

Retained text `fetched/text/S004-1.txt`: 6053 bytes, sha256 `f24e4f82d67ed9f617cf62893f0fd4c51b89b6ccc1911d0f335acdf565ceab7d`, one text line; it contains every quote below.

## Freshness finding

**Verdict: FRESH / content stable; row teaching holds. No drift, no staleness marker warranted.**

Observed, not inferred:

1. Live decoded body sha256 equals the r27 manifest sha256 exactly (same 141818 bytes).
2. r27 retained text sha256 `f24e4f82…` equals the **r26** retained text sha256 `f24e4f82…` byte-for-byte (both 6053 bytes) — the extracted prose is unchanged across both rounds.
3. The r26 raw body sha256 (`5c15ef2d916a57a9877f75518968df2d644799f08630f9beb5ed8d699206a385`, `.ufo/waves/round-26/population.json`) differs from live/r27. Character diff of the two decoded bodies shows the difference is **only** the Next.js `buildId` (`ndrfAHwVnt-w5Yffjl7If` → `gOeUVmJQ7z9zrUAITPynv`) plus webpack chunk filename hashes in `/_next/static/chunks/*.js`: 20 diff operations, none in prose. Both raw bodies are 141818 bytes (141775 decoded characters, equal in both); no sentence changed.

Consequence: this living page's raw-byte sha256 is build-scoped and **not** a content identity across builds. The r26→r27 hash change is not source drift; the text hash is the stable content identity here. Any r27 freshness claim should pin the text hash (`f24e4f82…`) or the quote, not raw HTML bytes.

## Located quote that best tests the inference

Recommended single ledger quote (**16 words**), located at the code lines under the heading "Linking separate build and deploy jobs" (live HTML heading line 75; code lines 89–95):

> `- name: Build with Jekyll uses: actions/jekyll-build-pages@v1 with: source:./ destination:./_site - name: Upload artifact uses: actions/upload-pages-artifact@v4`

- Anchor: heading "Linking separate build and deploy jobs", code block build job → `destination:./_site` → upload step (live HTML lines 89–95). Exact string membership in `text/S004-1.txt` verified with whitespace normalization; 16 words; ≤25.
- Format note: the retained text collapses span-boundary spaces, so the quote has `source:./` and `destination:./_site`; raw HTML has `source: ./` and `destination: ./_site`. The C1 checker matches the retained text, so the quote above is the ledger-form string.

### Relation to the inference: **indirect contribution** (not direct support, not irrelevant, not contradiction)

What the located text does establish:

- The example workflow checks out the repository, builds Jekyll from `source: ./` into `destination: ./_site`, then uploads that directory as the Pages artifact consumed by the deploy job.
- The page's deploy requirements separately state, under "Deploying GitHub Pages artifacts": "The needs parameter must be set to the id of the build step." (13 words) — the deployment is bound to a build step's artifact.
- The artifact is packaged and uploaded ("package and upload artifacts"), and should be a gzip tar (see teaching below).

What it does **not** establish (why this is not direct support):

- S004 never mentions a manifest, page enumeration, a preflight audit, or a requirement to prepare anything over the artifact.
- It never states that the served set differs from the repository checkout. Its own single-job variant shows the opposite boundary case: "In certain cases, you might choose to combine everything into a single job, especially if there is no need for a build process" and uploads `path: '.'` — exact 5-word context quote `upload entire directory path: '.'`. The doc therefore permits uploading the checkout root when no build exists; it does not equate the artifact with a build output.
- It is an example workflow, not a normative rule that built HTML must be the manifest population.

So S004 contributes the premise "the Pages deployment unit is an uploaded artifact, and a documented workflow can produce that artifact from a build destination" — the inferential step from that premise to "prepare the manifest over the artifact, not the assumed checkout" remains local synthesis, exactly as the grouped S001–S006 citation implies. S004 is not irrelevant (the artifact premise is necessary), and it does not contradict the recommendation's conditional ("when that artifact exists"): the `path: '.'` variant is the no-build case, consistent with the conditional, and is a caution against citing S004 for a blanket "checkout is never served" claim.

## Row teaching verification (HOLD at row scope)

- Heading present and matching SOURCES anchor: live HTML `<h2 id="configuring-the-upload-pages-artifact-action">` line 41, text "Configuring the upload-pages-artifact action".
- Artifact-shape quote (15 words, same paragraph): "The GitHub Pages artifact should be a compressed gzip archive containing a single tar file." — exact membership verified.
- Limits quote (18 words, same paragraph): "The tar file must be under 10GB in size and should not contain any symbolic or hard links." — exact membership verified.
- The r26 receipt's quote is the limits sentence; it remains verbatim. Result: **teaching holds; no STALE correction; no row cell change** (read-only seat). The page pins no action version; its snippets reference `upload-pages-artifact@v4`, `deploy-pages@v4`, `configure-pages@v5`, `checkout@v6`, which contradict no row cell.

Anchor-fidelity alternative if L1 requires the ledger quote to sit under the SOURCES-named anchor instead of the later build/deploy section: use the 15-word artifact-shape sentence above. It is indirect (artifact-as-deploy-unit premise only), not direct support. The build/deploy code quote is the stronger test of the built-vs-checkout clause but lies under a different heading than the stored anchor; both are the same URL, status, and row scope.

## Citing pairs and denominator

Enumeration: literal `S\d{3,}` plus ranges using hyphen/en-dash/em-dash/`..`/`to`/`through` over `corpus/knowledge/*.md`; S004 matched in five files.

| pair | status | S004's role / contribution |
|---|---|---|
| `static-canonical-preflight.md:53-54` (range S001–S006) | frozen unadjudicated (C2 missing 16) | target inference; **indirect** contribution: artifact-as-deploy-unit plus build-destination example; manifests/checkout never mentioned |
| `publish-channels.md:2` (range S001–S007) | frozen unadjudicated (C2 missing 16) | historical metadata only: "round-20 corrections 2026-10-19 (S001-S007 opened that day)". Live reopen does not establish a 2026-10-19 fetch and must not rewrite that date; consistent with SOURCES `opened` cell. Pair05B already proposes HOLD artifact-scoped |
| `ghp-served-set.md:1,29` | r26-decided (frozen ledger 41 pairs) | "S004 steps 4-5 upload static files and deploy the artifact"; artifact/deploy statement, indirect for any served-set divergence |
| `sitemap-orphan-audit.md:2,120-127` | r26-decided (w2 adjudication) | artifact/build-output comparison bits; the "checkout alone does not establish live→source" conclusions are already marked [INFERENCE] |
| `speedrun-pipeline.md:70` | r26-decided (w2 adjudication) | "S004 uploads the configured path as the artifact"; packaging premise only |

**No new citing pair discovered.** Denominator unchanged by this seat; no discovered-pairs entry added. The preflight and publish-channels pairs must remain in the denominator even though one is a metadata range.

### Suggested C1 record for the preflight pair (author-side, L1 judges)

```json
{
  "row": "S004",
  "file": "corpus/knowledge/static-canonical-preflight.md",
  "kind": "source",
  "fetchIndex": 1,
  "verdict": "HOLD",
  "quote": "- name: Build with Jekyll uses: actions/jekyll-build-pages@v1 with: source:./ destination:./_site - name: Upload artifact uses: actions/upload-pages-artifact@v4",
  "anchor": "Heading 'Linking separate build and deploy jobs', code block build job destination ./_site then upload-pages-artifact@v4; live HTML lines 75, 89-95",
  "reason": "Indirect contribution only: the documented build/deploy example builds Jekyll into destination ./_site and uploads that directory as the deployable Pages artifact, and the page binds deployment to the build step's artifact. The page never mentions a manifest or states that the served set differs from the checkout, and its single-job variant uploads path '.'. The grouped S001-S006 recommendation remains local synthesis; S004 grounds its artifact-as-deployable premise, not the full inference."
}
```

## Uncertainties and limits

- Living, unpinned docs: raw bytes change with the site build (buildId/chunk hashes). This seat observed no content drift, but hash-pinning raw HTML across rounds is invalid; pin the text hash or quote.
- No visible "last updated" date was found in the decoded page; freshness rests on the live GET, server `date`, and byte/text comparison, not on a document revision stamp.
- The recommended quote is example YAML, not normative prose. Its link to `_site` is by sequence; S004 does not itself state the upload action's default path (that is S001's action contract). Do not attribute the default to S004.
- The quote is from the "Linking separate build and deploy jobs" section, not the SOURCES anchor heading; the artifact-shape teaching under the anchor is separately verified above.
- One GET at one CDN edge (`x-served-by` cache nodes, MISS/MISS); no claim about other edges or future stability.
- The response carries `vary: x-user-version, accept, Accept-Encoding`; the sampled User-Agent produced bytes identical to the r27 retained fetch, but docs.github.com may vary presentation by user version. Content equality is established for the sampled request, not for every header combination.
- Grouped S001–S006 synthesis is not entailed by S004 alone; this report does not claim the full recommendation is proved by this row.

## Evidence hashes

- live decoded body: `9ee0766a2fb78e5af104bbc97dfe32ba09ebd8f2d68df1ed2d49efc081a5f53a` (141818 bytes)
- r27 manifest: `d3b0b1ca215bfa6d89edf639b2b87475d668fdf73cbf0ddf089c87e11d043781`
- r27 text `S004-1.txt` (and byte-identical r26 text): `f24e4f82d67ed9f617cf62893f0fd4c51b89b6ccc1911d0f335acdf565ceab7d`
- `corpus/knowledge/static-canonical-preflight.md` (observed bytes): `833b28f26fa7309f7e31398275bae2f704969d8e6f095bc5bb96250da5c531bc`
- `.ufo/waves/round-26/population.json`: `16330e1effd5ee52665f8f31738e9423c6ec387e5d4a1404c5bcc35f69d01b03`
- `.ufo/waves/round-26/statements.json`: `c2026376832ad4e4114d1bc19abeec4fcbdbd0fea3dbb102ab8a5c2eb18c95ce`
- scratch (one GET raw/decoded + headers): `/fast/scratch/hyaku/kake-r27/SourceOpenS004/{body.html,headers.txt}`

## Actions

Read contract, `count_c1.py`, `c2_count.py`, `c2-oracle.json`, frozen expected/ledger. Performed one public GET of the one S004 URL. No installs, no pacman, no builds/tests/formatters, no source/ledger/index/jj/git mutation, no r24 stopped-work access, no browser/account/property operation.
