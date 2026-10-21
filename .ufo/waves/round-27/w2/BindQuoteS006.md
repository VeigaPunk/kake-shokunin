# BindQuoteS006 — r27 fresh falsification, technical source-binding attack (S006)

Axes: freshness + operability. Frozen candidate ac46a7472d945a6d7ff135e4d7f07b0b6913d835 (tree check: commit).
All reads below were made only after `git cat-file -p <candidate>:<f>` == working-tree sha256 (7/7 MATCH:
corpus/SOURCES.md, publish-channels.md, static-canonical-preflight.md, fetched/manifest.json,
fetched/S006-1.public.txt.gz, fetched/text/S006-1.txt, pairs.json). Independent sourceFiles cross-check: 7/7 OK.

## 1. Manifest slots (r27 fetched/manifest.json, 8 entries)
Exactly one S006 slot: index 7, fetchIndex 1 — pairs.json fetchIndex 1 matches.
- url == finalUrl = https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll
- status 200, error null, fetchedAt 2026-10-21T19:59:56.112484+00:00
- retained: sha256 535e55d0fb1154f0fb86de1d070abebc49c75c2e8f7845c547f8d61626806910, bytes 7676, file S006-1.public.txt.gz, text text/S006-1.txt
- receivedSha256 f0318abe7e63ecded4e7294484bd8cb68721e920b46d0b85399acb2a187742b6, receivedBytes 138096
- retainedRepresentation: kind public_visible_text, derivation source_text.text_of(receivedBody, contentType),
  rawHttpBodyRetained false, htmlAttributesRetained false, scriptBodiesRetained false, formFieldValuesRetained false,
  replacedFile S006-1.raw.gz. Note field: sha256/bytes = retained representation; receivedSha256/receivedBytes =
  observed HTTP body; original received HTML not reconstructable from filtered bytes.

## 2. Retention chain re-hash (declared expected stated before running: gz sha == sourceFiles 91327c46…; decompressed == text file == manifest sha256/bytes)
- fetched/S006-1.public.txt.gz sha256 = 91327c464630bbd7cf2b096b5f37d55d93501b4a0d5466cb142de7c2d20c975e (== sourceFiles entry)
- gunzip in memory -> sha256 535e55d0…, 7676 bytes (== manifest sha256/bytes; == fetched/text/S006-1.txt, byte-identical)
- receivedSha256 f0318abe… != retained 535e55d0… (expected: privacy-filtered transformation, not reconstructable — not claimed)
- S006-1.raw.gz absent from fetched/ (grep -c raw = 0): raw body not retained, per manifest.

## 3. Fresh public GET (one reopen, 2026-10-21, in-memory only; no raw HTML/form/header values persisted or printed)
Expected declared before run: text_of(fresh) either byte-equals retained 535e55d0… or differs (drift reported); raw digest compared to f0318abe….
- status 200, content-type text/html (prefix only).
- RAW DRIFT: fresh received sha256 d2bb9c7769328ab3ab90b5526864bab6ab1601dc689846e6064f5fe63dc99200,
  138096 bytes vs manifest receivedSha256 f0318abe…, 138096 bytes -> digest CHANGED, size identical (markup churn, same length).
- TEXT DRIFT: text_of(fresh body, ct) -> sha256 535e55d0…, 7676 bytes -> byte-identical to retained view. NONE.
- Retention transformation independently reproduced from today's live body (urllib GET + round-26 source_text.text_of).
- Similarity diff: not needed (digests equal). A raw digest change is not prose drift; observed raw and text drift are reported separately.

## 4. Quote verification (pairs.json S006/static-canonical-preflight.md, kind source, fetchIndex 1, verdict HOLD)
Quote: "By default, Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor"
- 18 words (<=25 ✓), 18 tokens (>=6 ✓), non-boilerplate ✓ (specific Jekyll default-exclusion behavior).
- Present verbatim in retained view ✓ and in fresh visible-text view ✓ (identical bytes, so both).
- Anchor "Configuring Jekyll in your GitHub Pages site, default exclusions paragraph": the phrase occurs twice —
  offset 1312 (left-nav TOC entry) and offset 2302 (article heading "…Pages site. Configuring Jekyll in your GitHub Pages site
  You can configure most Jekyll settings…"). Quote at offset 2782, i.e. 480 chars after the article-body heading, directly
  after the defaults config listing ("lsi: false safe: true … syntax_highlighter: rouge") and immediately before the
  exclusion list ("Start with _,., or # End with ~ Are excluded by the exclude setting…"). Anchor description accurate.
- Note: quote concatenates the paragraph lead-in with the first list item; exact words in order in the visible-text view,
  which concatenates list items. No PASS on semantics inferred — judges decide support.

## 5. Artifact pair binding (pairs.json S006/publish-channels.md, kind artifact, evidence corpus/SOURCES.md, verdict HOLD)
- contains-substring present verbatim in corpus/SOURCES.md ✓ (full row incl. URL == manifest url, "fetched 2026-10-19",
  "mined 2026-10-19", "90d"; paraphrase "skips paths starting with underscore, dot, or hash, paths ending in tilde,
  node_modules, and vendor" matches live text; omits the exclude-setting leg — summary-level, adds nothing false).
- ATTACK FINDING (author-side, binding layer only): corpus/knowledge/publish-channels.md contains zero "S006" tokens;
  its only SOURCES.md citations enumerate "S001, S002, S003, S005 and S007" (line 1; repeated line 84); and the file has
  no Jekyll/vendor/node_modules/exclusion content at all (grep -i over those terms: 0 lines). No visible syntactic or
  content binding from this knowledge file to row S006. This is the pair pairs.json scope calls "plus 1 conservatively
  added embedded artifact reference". Pair presence != semantic support; whether the attribution is supported at stated
  scope is for C1 review, not this seat.
- Other complete-ledger S006 bindings verified present: ghp-served-set.md line 1 "source: S001, S002, S003, S004, S006,
  S008 (corpus/SOURCES.md)" + line 30 "S006's Jekyll defaults skip" (real content reliance); sitemap-orphan-audit.md
  literal S006 (lines 1, 149, 167) and range "S001-S006" (line 2); static-canonical-preflight.md 4 S006 mentions incl.
  line 233 r27 recheck table quoting this exact quote and line 214 "All six members of the original S001–S006 range…".

## 6. Status/time vs declaration
- Manifest status 200 @ 2026-10-21T19:59:56Z; fresh GET today 200. No error field.
- SOURCES row "fetched 2026-10-19" is historical opened-date metadata (publish-channels.md line 2: "round-20 corrections
  2026-10-19 (S001-S007 opened that day)"); manifest fetchedAt is the r27 capture — distinct events, consistent with
  pairs.json reason treating the date as historical-only, not a fresh r27 source observation.

## 7. New overrides for S006
None found: 0 S006 mentions in oracle-implementation-corrections.json, carry-errata.json, discovered-pairs.json,
strict-c1-disposition.json. w1-outcomes.json mentions are seat bookkeeping only (SourceOpenS006, agentId, report path).
frozen/ledger.json S006 rows: ghp-served-set.md stale 0 / seatStale 0 / seatUnverifiable 0; sitemap-orphan-audit.md
stale 0 / seatStale 0 / seatUnverifiable 0 (addedBy "w2 adjudication", report "L1 KakeR26-2") — S006 is not among the
7 known-unknown units / 3 partial-UNVERIFIABLE pairs.

## 8. Discrepancies / uncertainties
- publish-channels.md S006 linkage absent (finding, §5) — semantic disposition left to C1 review; no rescoping here.
- Fresh received digest differs from manifest receivedSha256 with identical byte count — raw-only drift, prose unchanged;
  original received digest remains non-reconstructable from filtered bytes (manifest states this; confirmed by design).
- Only one fetch slot exists for S006; "every slot" = this one. No second fetchIndex declared anywhere for the row.
- No raw HTML, token, form, or header values persisted; scratch limited to /fast/scratch/hyaku/kake-r27/BindQuoteS006/
  (probe_fresh_s006.py only). No source/docs/registry edits, no commits, no installs (none needed), no subagents.
