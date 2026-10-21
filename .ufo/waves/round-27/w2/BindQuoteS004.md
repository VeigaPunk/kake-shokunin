# BindQuoteS004 — r27 fresh falsification, source-binding attack (S004)

Axes: freshness (judged), operability. Leaf seat; no subagents; no source edits.
Method: every measured source read used full candidate hash
`ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (never bare HEAD); working tree was
first proven equal to candidate blobs (8/8 MATCH below). One public GET total,
all bytes processed in memory; nothing persisted to scratch (`/fast/scratch/
hyaku/kake-r27/BindQuoteS004/` created, left empty); no raw HTML, header,
token or form values written anywhere.

## 1. Frozen authority check
`git cat-file -p <C>:<f> | sha256sum` vs `sha256sum <f>` — 8/8 MATCH:
pairs.json f1fa20ca; fetched/manifest.json 33d650cd;
fetched/S004-1.public.txt.gz b0cc6a78; fetched/text/S004-1.txt 3f3c983e;
ghp-served-set.md 35fedf84; static-canonical-preflight.md 40ebd1da;
publish-channels.md 18042de4; corpus/SOURCES.md c92807d7.
Candidate commit time 2026-10-21T18:51:48-03:00 (=21:51:48Z).

## 2. Manifest slots for this row
fetched/manifest.json has 8 slots: S001×2, S002×2, S003, S004, S005, S006.
S004 has exactly ONE slot (index 1) — matches its single SOURCES.md URL.
Slot: url=docs.github.com/en/pages/getting-started-with-github-pages/
using-custom-workflows-with-github-pages, status 200, error null,
fetchedAt 2026-10-21T19:59:55.714609+00:00, bytes 6052,
sha256 3f3c983ed36237b1a4e3154166562912f03b0824495bc5344ea360039efbc33d,
file S004-1.public.txt.gz, receivedSha256 9ee0766a2fb78e5af104bbc97dfe32ba09
ebd8f2d68df1ed2d49efc081a5f53a, receivedBytes 141818, replacedFile S004-1.raw.gz.

## 3. Retained representation: decompress + re-hash
`gzip -dc` S004-1.public.txt.gz → sha256 **3f3c983e…**, 6052 bytes ==
manifest slot `sha256`/`bytes` == candidate text/S004-1.txt hash. Container
.gz bytes b0cc6a78 (2125 B) == candidate sourceFiles entry. Nuance: manifest
`sha256` names the decompressed visible-text view, not the container; the
container hash lives only in frozen-candidate.json sourceFiles. Consistent.

## 4. receivedSha256 vs retained digest — distinct, correctly labeled
received 9ee0766a…/141818 B observes the original HTTP body; retained
3f3c983e…/6052 B is the public_visible_text view. Manifest retainedRepre-
sentation: rawHttpBodyRetained/htmlAttributesRetained/scriptBodiesRetained/
formFieldValuesRetained all false; original received HTML not reconstructable
from filtered bytes. prepared-source-binding.json still declares the pre-cutover
S004-1.raw.gz (5820c74b…) — historical declaration only; no raw.gz in tree.
No conflation observed.

## 5. Fresh public GET (declared expectations BEFORE running)
Declared: (a) 200 expected; (b) if prose unchanged, derived text_of view must
equal frozen 6052-byte view byte-for-byte; (c) raw digest may differ without
prose drift. Ran frozen round-26 helpers (fetch_sources.fetch + source_text.
text_of), TMPDIR set, memory only. Actual:
- status 200; content-type text/html; charset=utf-8; content-length 141818
- receivedSha256 **9ee0766a2fb78e5af104bbc97dfe32ba09ebd8f2d68df1ed2d49efc081a5f53a**
  = manifest receivedSha256 → NO raw drift (body byte-identical to W1 observation)
- derived text_of view sha256 **3f3c983e…**, 6052 B, `derived==frozen: True`
  → NO text drift
- recheck time 2026-10-21T22:01:14Z (fetch 19:59:55Z < commit 21:51:48Z < now)
Raw drift and text drift reported separately as required; both zero.

## 6. Quote verification (actual pairs.json quote)
Quote (both source pairs): "The GitHub Pages artifact should be a compressed
gzip archive containing a single tar file." — 15 words (≤25 ok), ≥6 tokens,
non-boilerplate (specific packaging assertion). Anchor: "Configuring the
upload-pages-artifact action". In retained/fresh view: quote occurs exactly
once, 124 chars after the anchor's section-heading occurrence (2nd of 2 anchor
hits; 1st is TOC) — quote is inside the named section. Verified against BOTH
the retained view and the fresh derived view independently.

## 7. S004 pair slots in pairs.json (3)
a) artifact, publish-channels.md, HOLD: evidence corpus/SOURCES.md, `contains`
   substring verified EXACTLY present in candidate SOURCES.md (line 12). Binding
   is registry-mediated: publish-channels.md contains no literal "S004" token;
   it cites S001/S002/S003/S005/S007 and references upload-pages-artifact;
   SOURCES.md's S004 row names publish-channels.md in its citing-file list.
   Artifact shape recorded; no semantic PASS claimed from substring.
b) source, static-canonical-preflight.md, fetchIndex 1, HOLD: citing file line
   231 quotes the identical sentence verbatim at the named anchor. Syntactic
   match confirmed; semantic support is the separate review's (Pair06A/B).
c) source, ghp-served-set.md, fetchIndex 1, **STALE** (new r27 pair): override
   present at lines 99–106, old lines 29–30 retained unmodified (append-only).

## 8. New override quote for this row (candidate ghp-served-set.md:99–106)
"- [r27-recheck S004 STALE] Lines29–30 attribute "steps 4-5 upload static files
  and deploy the artifact" to S004. The numbered general workflow flow is
  in S003, under Creating a custom GitHub Actions workflow to publish your
  site: item4 uploads static files and item5 deploys the artifact. S004 has
  the unnumbered artifact-configuration section and workflow code examples.
  The publishing substance is unchanged; the numbered locator attribution
  is corrected to S003. Retained source: round27 fetched S003/S004, adjudication
  `.ufo/waves/round-27/pairs.json`, discovery `w1/Pair06B.md`."

## 9. Status/time vs declaration
Manifest: status 200, error null, fetchedAt 2026-10-21T19:59:55Z — internally
consistent with candidate commit 21:51:48Z same day. SOURCES.md row "fetched
2026-10-19 | 90d" is the r20 opened-batch historical metadata, explicitly
labeled as such in the artifact pair's reason — not contradicted by the r27
manifest timestamp; fresh GET within the 90d window and byte-identical.

## 10. Discrepancies / uncertainties
- None binding. Two labeling notes recorded (§3 manifest sha256 = plaintext
  view, not container; §4 prepared-source-binding.json keeps pre-cutover raw
  declaration by design, cross-referenced via `replacedFile`).
- Fresh-view equality used the frozen text_of derivation (declared derivation);
  independence comes from re-deriving from a fresh network response, not from
  trusting retained bytes.
- discovered-pairs.json adds only S013; no new S004 obligations.
Reviews referenced exist: w1/Pair05A/B, Pair06A/B, SourceOpenS003/S004.
No PASS verdicts issued; semantic adjudication remains with the judge pairs.
