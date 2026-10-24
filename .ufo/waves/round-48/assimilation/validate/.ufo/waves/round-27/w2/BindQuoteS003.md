# W2 BindQuoteS003 — S003 technical source-binding (r27 fresh falsification)

Axes: freshness + operability. Scope: S003 only. No subagents; no installs.
Frozen authority: HEAD = `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (`git rev-parse HEAD` = candidate, verified before any source read). Declaration `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (2026-10-21T16:59:37-03:00).

## 1. Candidate-blob equality (precondition)
All files read below verified `git hash-object` == `git rev-parse ac46a74...:<path>` (EQ):
static-canonical-preflight.md, ghp-served-set.md, ghp-custom-domain.md, publish-channels.md, sitemap-orphan-audit.md, corpus/lessons/round-20.md, pairs.json, fetched/manifest.json, fetched/S003-1.public.txt.gz, fetched/text/S003-1.txt, r26 source_text.py.

## 2. r27 manifest slots for S003
Exactly 1 slot (`grep -c '"row": "S003"' fetched/manifest.json` → 1): S003-1, url/finalUrl `docs.github.com/.../configuring-a-publishing-source-for-your-github-pages-site`, status 200, error null, fetchedAt 2026-10-21T19:59:55.678521+00:00, bytes 8311, sha256 e9f3dbd93e957e09796b508735436aa70c71baff7c3f8e2ef2f4c553db3a1892, file S003-1.public.txt.gz, receivedSha256 f42d48b59277843e489896f52f97bb9c62e68970f0c3bebb3021b586ba62a3f5, receivedBytes 154136. retainedRepresentation: kind public_visible_text, derivation `source_text.text_of(receivedBody, contentType)`, rawHttpBodyRetained false, replacedFile S003-1.raw.gz (removed by retention-migration: 8 records, offline).
Time/status vs declaration: 19:59:55Z ≥ declaration 19:59:37Z (+18.7s), HTTP 200. PASS.

## 3. Retained representation re-hash (independent)
- `sha256sum fetched/S003-1.public.txt.gz` → 974ad104801e061f9421c50121f133334c78465604779f847d7e92a5867e520f == frozen-candidate.json sourceFiles.
- `gunzip -c` piped sha256 → e9f3dbd93e957e09796b508735436aa70c71baff7c3f8e2ef2f4c553db3a1892 == manifest sha256 == retainedSha256 (retention-shape-after.json) == `sha256sum fetched/text/S003-1.txt`.
- `cmp` gunzip vs text/S003-1.txt → IDENTICAL.
Digest distinction observed: .gz container hash 974ad1… ≠ retained text digest e9f3dbd… ≠ historical receivedSha256 f42d48b5… (original HTML body, unretained). No conflation.

## 4. pairs.json quote verification (S003 × static-canonical-preflight.md, kind source, HOLD, fetchIndex 1)
Quote: "If required by your site, build any static site files. Use the actions/upload-pages-artifact action to upload the static files as an artifact."
- Independent count before check: words=22 (≤25 PASS), tokens ≥6 PASS, non-boilerplate (operational GitHub Actions instruction) PASS.
- Exact substring in retained S003-1.txt: 1 occurrence; in all 8 r27 text files: only S003-1 (uniqueness PASS).
- Anchor "Creating a custom GitHub Actions workflow to publish your site, general workflow flow steps3–4": heading present (count 2, TOC+section); the quote is the 3rd+4th list items after "The general flow of a workflow is to:" (1 occurrence). HTML `li` markers are CSS-rendered so "3."/"4." never appear in text view; positional match confirmed via preceding/following item text. PASS with positional note.

## 5. Fresh public GET (one reopen, expectations declared before fetch)
EXPECTED: E1 200 text/html; E2 text_of(body,ctype) == retained text (e9f3dbd…) ⇒ no prose drift; E3 raw digest may differ (not prose evidence); E4 quote verbatim both views; E5 items 3–5 locatable.
ACTUAL: status 200, Content-Type text/html; charset=utf-8; receivedBytes 154136; receivedSha256 ced216363c08f7093bfad0eae4c9d20ef7d7ac6c195373ea376e281ae745a9fd; derivedTextSha256 e9f3dbd… IDENTICAL to retained (no prose drift); quote present in fresh derived text; words/tokens as above.
RAW vs TEXT drift, reported separately: raw-layer drift observed — receivedSha256 ced21636… ≠ recorded f42d48b5… at identical receivedBytes 154136; derived visible text byte-identical. Raw digest change is not prose drift; no content of the delta inferred (old body unretained).
E5 locator: immediately after the quote the S003 page reads "If the workflow was triggered by a push to the default branch, use the actions/deploy-pages action to deploy the artifact." — supports the override's claim that upload+deploy general-flow items are S003 page content (my earlier case-sensitive probe `Use the actions/deploy-pages` was a probe artifact; actual text is lowercase "use").

## 6. Override touching this row (quote, as instructed)
pairs.json tail entry (row S004, file corpus/knowledge/ghp-served-set.md, kind source, verdict STALE, carriedPairOverrideReviews=1), quote: "The GitHub Pages artifact should be a compressed gzip archive containing a single tar file." anchor "Configuring the upload-pages-artifact action" (verified 1 occurrence in S004-1.txt). S003-relevant reason, verbatim: "The numbered general-flow items4–5 are in S003, not S004's unnumbered artifact configuration section. Substance remains true; append explicit S003 attribution and retain old r26 review/units without rewriting it." Item-4/5 text confirmed in S003 fresh+retained view (§5); the S004-1.txt anchor heading also present. Locator-correction binding holds textually.

## 7. Other S003-pair bindings checked
- Artifact pair S003 × sitemap-orphan-audit.md: `grep -cF 'C3: S001/S002/S003/S004/S006/S008 rows plus \`ghp-served-set\`; annotate \`round-7.md\` append-only' corpus/lessons/round-20.md` → 1. PASS (presence only; semantics not judged here).
- served-set S003 bullet (lines 28–30, non-verbatim per r26 STALE): knowledge file still reads "the source folder can either be the root of the repository (`/`) or a `/docs` folder." while fresh S003 text reads "the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch." — recorded [r26-recheck S003 STALE] quote confirmed against today's bytes; no new drift beyond it.
- "About publishing sources" heading and "You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site." present in fresh+retained view (supports the Actions-vs-branch distinction attributed to S003 in publish-channels/ghp-served-set recheck prose).

## 8. Retention transformation + stated limitation
Reproduced derivation independently with r26 `source_text.text_of` (blob-EQ at candidate) on today's body → identical retained digest; HTML attributes/script bodies not emitted by the parser. As stated: filtered bytes cannot and do not reconstruct receivedSha256 f42d48b5… (nor today's ced21636…); r27 received HTML remains unretained. Historical raw digests in prepared-source-binding.json (S003-1.raw.gz 0c7f3643…, received f42d48b5…) treated as observations only.

## Discrepancies / uncertainties
1. receivedSha256 drift at equal byte length (f42d48b5→ced21636): raw-layer only; per-body delta content unknowable from repo. No prose impact (digest-identical text view).
2. pairs.json anchor names list markers ("steps3–4") that never appear in text view (CSS markers); positional verification used; semantics untouched.
3. Original r27 raw body absent by design: f42d48b5… unverifiable from any retained bytes — accepted, not resolved.
No PASS inferred from digest/substring alone for semantic support; semantic review remains separate. No edits outside this report; no raw HTML/token/header values persisted; scratch TMPDIR=/fast/scratch/hyaku/kake-r27/BindQuoteS003 (unused, created). No tool installs.
