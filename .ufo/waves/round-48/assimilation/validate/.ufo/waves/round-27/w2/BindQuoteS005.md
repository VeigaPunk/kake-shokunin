# KakeR27.BindQuoteS005 — r27 fresh falsification, S005 source binding

Axes: freshness + operability (this seat = freshness of the S005 source-binding chain).
Candidate frozen at ac46a7472d945a6d7ff135e4d7f07b0b6913d835 (explicit-hash Git reads only).
Read-only seat; scratch /fast/scratch/hyaku/kake-r27/BindQuoteS005 (TMPDIR set); no source edits, no /tmp, no raw HTML persisted.

## 1. Frozen-input identity (expected: all working files == candidate blobs)
- Working HEAD = ac46a747 (observed via rev-parse before any read).
- `sha256sum f` vs `git cat-file -p ac46a747:f` for:
  - .ufo/waves/round-27/fetched/manifest.json → 33d650cd…aeb1d6 = 33d650cd…aeb1d6 MATCH (equals frozen-candidate sourceFiles)
  - .ufo/waves/round-27/fetched/S005-1.public.txt.gz → 4e5b58eb…083a077 = 4e5b58eb…083a077 MATCH
  - .ufo/waves/round-27/fetched/text/S005-1.txt → 854c3466…a264515 = 854c3466…a264515 MATCH
  - .ufo/waves/round-27/pairs.json → f1fa20ca…b376a6a = f1fa20ca…b376a6a MATCH
  - .ufo/waves/round-26/source_text.py → 55ae7abc…f57b7d6 = 55ae7abc…f57b7d6 MATCH (extractor unchanged)
All 28 frozen inputs untouched on my lane; nothing rewritten.

## 2. Manifest slots for S005 (expected: enumerate every slot)
- Exactly 1 slot (manifest is a list of 8; one `"row": "S005"`, index 1):
  url https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
  status 200, fetchedAt 2026-10-21T19:59:56.085676+00:00,
  retained: file S005-1.public.txt.gz, text text/S005-1.txt, sha256 854c3466…, bytes 14700,
  receivedSha256 6f3d1ad2…79e6be4, receivedBytes 240439,
  retainedRepresentation: kind public_visible_text, derivation source_text.text_of(receivedBody, contentType),
  rawHttpBodyRetained:false, htmlAttributesRetained:false, scriptBodiesRetained:false, formFieldValuesRetained:false,
  replacedFile S005-1.raw.gz. prepared-source-binding.json confirms the earlier raw-slot digests
  (S005-1.raw.gz 71f21dfe…, text b2a7d47d…) were replaced by the privacy-filtered retention; current bytes are the authority.

## 3. Retained representation re-hash (expected: decompressed == manifest sha256 == text file)
- gunzip-in-memory: gz container 4e5b58eb… → decompressed 854c3466…a264515, 14700 bytes
  == manifest sha256 == text/S005-1.txt (14700 bytes). PASS.
- Distinguish: receivedSha256 6f3d1ad2… (240439 B, raw HTTP body observed at fetch; NOT retained, unreconstructable by the manifest's own note) vs retained digest sha256 854c3466… (14700 B, filtered public_visible_text). Distinct, as declared. Original received HTML digest cannot be derived from filtered bytes — not attempted, per contract.

## 4. Fresh public GET (declared expectation BEFORE run: status 200; received digest and visible text computed in memory only; zero disk persistence of body)
- Command: python3 urllib GET, UA Firefox/128.0 Linux, timeout 60, single request, no cookies/auth.
- Expected: HTTP 200; fresh received sha256 comparable to 6f3d1ad2…; fresh text_of view == retained 854c3466….
- Actual: status 200, finalUrl == declared url, content-type text/html.
  - Fresh received sha256 719a9794…5fdc88c600, 240439 bytes ≠ manifest 6f3d1ad2… at IDENTICAL length 240439 → RAW DRIFT (see §7).
  - Fresh visible text via r26 source_text.text_of: sha256 854c3466…a264515, 14700 bytes == retained digest EXACTLY, zero divergence. TEXT: NO DRIFT.
- Raw drift vs text drift reported separately per instruction: raw body bytes changed since fetch; public visible text unchanged.

## 5. pairs.json quote verification (S005, kind=source, fetchIndex 1)
- Quote: "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created"
  → 15 words, 15 alphanumeric tokens (≤25 words PASS, ≥6 tokens PASS), non-boilerplate (body sentence on CNAME handling, not nav/footer) PASS.
- Retained view: exactly 2 occurrences, absolute offsets 3258 and 8563.
  - Anchor "Configuring an apex domain": occurrences at 1493 (TOC), 2596 (section), 5990, 12347 (cross-refs); quote 3258 sits 662 chars after section head 2596 → inside apex section. PASS.
  - Anchor "Configuring a subdomain": 1520 (TOC), 6940 (cross-ref), 7885 (section); quote 8563 sits 678 chars after section head 7885 → inside subdomain section. PASS.
  - Exact words, byte-identical context in both places ("…click Save. … this will create a commit that adds a CNAME file directly to the root of your source branch." preceding; ", and any existing CNAME file is ignored and is not required." following).
- Fresh view: same 2 occurrences at identical offsets 3258/8563; identical anchor offsets. Quote is fresh, not just retained-fossil. PASS.
- Anchor nuance (disclosure, not refutation): literal "step 4" numbering is absent from the derived text — docs.github.com renders <ol> counters via CSS ::marker, which text_of (text-node HTMLParser) drops. The sentence directly follows the section's instruction sequence ending "click Save", i.e. it is the visually 4th step, but item index is not provable from filtered bytes. Per oracle-implementation-corrections: anchor/location judgment is human-review scope; shape checks cannot prove anchors. No semantic PASS claimed here.

## 6. Status/time vs declaration (expected: 200 and fetchedAt ≥ declaration instant)
- Declaration be375d90 committed 2026-10-21T16:59:37-03:00 = 19:59:37Z; S005 fetch 19:59:56.085676Z → +19s ≥ declaration PASS; status 200 PASS.

## 7. Raw vs text drift finding (freshness)
- Raw received digest drift: 6f3d1ad2… (fetch-time) vs 719a9794… (today), same 240439-byte length, identical derived visible text. Equal length + unchanged text_of view confines drift to non-text regions (attributes/scripts), but the changed values are NOT retained anywhere and cannot be attributed from this wave's evidence — the manifest's stated limitation, honestly kept. No raw bytes, attribute, or header values were saved or printed. This is a normal raw-digest change, not prose drift; the S005 source binding rests on the visible text, which is byte-stable.

## 8. Overrides / corrections for S005 (expected: enumerate any new override)
- None new. git show of correction commit 08014ce ("enforce unchanged oracle targets…") and strict commit 9ba102d4 ("preserve strict C1 unknowns…") contain no S005 hunks; discovered-pairs.json adds only S013; w2-attack-design.json has no S005 entry; strict-c1-disposition.json has no S005 override. The row's durable r27 adjudications remain the two pairs.json STALE entries.
- [r27-recheck S005 STALE] markers verified present at candidate:
  - corpus/knowledge/static-canonical-preflight.md:235 (+ table row :232 restating the quote with curly quotes, "Configuring an apex domain, step4")
  - corpus/knowledge/sitemap-orphan-audit.md:163-165.

## 9. Remaining S005 pairs
- Artifact pair (sitemap-orphan-audit.md → .ufo/round-20/resume/citation-disposition.json): candidate blob contains '"supersededClaim": "Each deployment snapshots the entire checked-out tree."' exactly once. Binding PASS; semantics stay with the separate reviewers.
- Ledger census (observation, no verdict): pairs.json has 10 distinct rows, no range rows covering S005; S005 carries exactly the 2 adjudicated pairs above. complete-ledger.json lists 5 S005 citing files; the other 3 (ghp-custom-domain.md, ghp-subpath-spotcheck.md, publish-channels.md) cite S005 via r20 corrections/r26 recheck prose whose statement pairs live in .ufo/waves/round-26/statements.json — inherited-population territory, outside this seat's pairs.json mandate. Flagged for the C1 counter owners, not adjudicated here.

## Discrepancies / uncertainties
1. Raw received digest drift (§7): expected-class observation, cause unattributable from retained evidence by design.
2. "step4" anchor index not literally present in filtered bytes (§5): CSS-generated list markers; positional support only.
3. No refusal, no policy stop, no mutation seat touched; single fresh GET performed; no other URL reopened.
No semantic PASS is claimed from digests or substrings; all semantic verdicts remain with the independent reviewer seats.
