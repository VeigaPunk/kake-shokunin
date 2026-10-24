# JudgePair06 — (S004, corpus/knowledge/static-canonical-preflight.md), HOLD kind=source

Seat: KakeR27.JudgePair06 (read-only reviewer, leaf, no dispatch). Axis judged: **freshness**.
Milestone: r27-fresh-falsification. Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`
(base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`, declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`).
Read-only: no source/ledger/state edit, no commit, no build/lint/test, no tool installed.
Scratch: `/fast/scratch/hyaku/kake-r27/JudgePair06/` only. Author-side evidence, not admission.

## 1. Attacked item (exact)

`.ufo/waves/round-27/pairs.json` row:
`{"row":"S004","file":"corpus/knowledge/static-canonical-preflight.md","kind":"source","verdict":"HOLD",
"fetchIndex":1,"quote":"The GitHub Pages artifact should be a compressed gzip archive containing a single tar file.",
"anchor":"Configuring the upload-pages-artifact action","reason":"Defines the packaged deployment artifact;
does not alone prove checkout divergence or prescribe a canonical manifest. Combined recommendation is local synthesis."}`

Citing sentence (`corpus/knowledge/static-canonical-preflight.md:53-54`, unchanged at the candidate):
"Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed
checkout served set (S001–S006, `ghp-served-set.md`)."
S004 enters only through the en-dash range (no literal `S004` token in the body; the literal tokens at
lines 231/240 are inside the r27 appended adjudication block, appended after the claim).

## 2. Verdict on the attack

**CONFIRM HOLD at S004's own stated scope.** The row is honest, row-specific, anchor-accurate and fresh.
The ledger reason labels the inferential step ("does not alone prove checkout divergence", "local synthesis"),
which is what the contract requires of a grouped-range member. No STALE marker is required for HOLD, and the
citing file correctly contains **no** `[r27-recheck S004 STALE]` marker (grep count 0 at the candidate).

## 3. Probes — expected result declared before running, then actual

**P1 (quote membership + row specificity).** Expected: quote present exactly once in S004's view, absent from
every other fetched row (gate rule `quote_not_row_specific`). Actual: S004 text `S004-1.txt` count **1**;
S001/S002/S003/S005/S006 counts **0**. Anchor `Configuring the upload-pages-artifact action` present twice
(nav + body heading at 2617); quote index **2741**, i.e. between the body H2 at 2617 and the next H2
"Deploying GitHub Pages artifacts" at 3134 → quote sits under the named section. ✔

**P2 (anchor reality vs. the S004-ghp dissent).** Expected: if "steps 4-5 upload static files and deploy the
artifact" really is S004's, S004's view contains "static files" and a numbered list; if it is S003's, S004 has
neither and S003's flow is numbered. Actual: S004 view contains **0** occurrences of "static files" and **0**
numbered list markers; S003 view contains the 5-item flow (1 Trigger, 2 checkout, 3 "build any static site
files", 4 "upload the static files as an artifact", 5 "deploy the artifact"). ⇒ the sibling
`(S004, ghp-served-set.md)` STALE override (locator corrected to S003) is correct, and it does **not** touch
this row: this row's quote is S004's own unnumbered artifact-configuration section. ✔ no cross-row contradiction.

**P3 (live freshness).** Expected before the GET: the anchor sentence and its section still present; visible
prose unchanged (raw HTML may drift by build id). Actual: one public GET (no auth/cookie/browser) of the
S004 URL → **HTTP 200**, 141818 bytes, raw body sha256 `c39eeec7418844e1cc0375de4b08e1500df5c225b42d5e577194c30f69f95e2a`;
decoded visible text (r26 `source_text.py` helper) len 6051 chars, sha256
`3f3c983ed36237b1a4e3154166562912f03b0824495bc5344ea360039efbc33d`; quote count **1**, anchor count **2**,
"static files" count **0**. The live visible-text hash equals the **committed** r27 retained text hash
`3f3c983e…` (`git show ac46a74:.ufo/waves/round-27/fetched/text/S004-1.txt` → 6052 bytes, sha256 `3f3c983e…`).
⇒ content fresh; no drift. Raw-body hash differs from the manifest's recorded `receivedSha256` `9ee0766a…`
(same length) — Next.js build/chunk churn only, prose identical. ✔

**P4 (gate re-measure at the candidate).** Expected: my row validates; overall exit stays 1 with 55/58 decided
and 3 carried UNVERIFIABLE pairs (matching the frozen `strictC1: UNPROVABLE`). Actual:
`python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a747…` → exit **1**, citingPairs 58,
reviewed 58, decided 55, knownUnverifiableUnits 7 / pairs 3, `unreviewed: []`, and in `outcomes`:
`{"row":"S004","file":"corpus/knowledge/static-canonical-preflight.md","verdict":"HOLD","valid":true}`. ✔
(Note: this is the author-side rerun; L1's recorded 29/29 gate remains the authority.)

**P5 (source-scope semantics, independent of any reviewer).** Expected: S004's registry scope
("Artifact shape and deployment requirements for custom workflows") supports the sentence's *artifact* premise
but not its *divergence* premise. Actual: S004 view has 0 occurrences of "html" and 0 of "manifest"; it supplies
"the deployment artifact is a packaged unit" and the upload/deploy workflow example (jekyll-build-pages →
`destination:./_site` → upload-pages-artifact@v4 → deploy-pages@v4); its "Single deploy job no building"
variant uploads `path: '.'` (whole checkout), i.e. S004 alone can never prove checkout≠artifact. That is
exactly what the ledger reason states, and it is why S004 is HOLD-at-limited-premise while sibling S005 is
STALE (S005 is off-subject: CNAME/domain configuration). ✔ principled asymmetry, not a carve-out.

**P6 (dissent coverage).** S005-preflight STALE: marker present at line 235 and the range re-read as "local
synthesis supported by the scoped premises from S001, S002, S003, S004 and S006" — S004 is explicitly retained
as a scoped premise, so the S005 STALE does not undercut the S004 HOLD. ✔ S005/S003-sitemap: S003 HOLD
(artifact `corpus/lessons/round-20.md`, `contains` substring present ✔); S005 STALE marker present at
`sitemap-orphan-audit.md:163` ✔. S004-ghp-steps: see P2 ✔.

## 4. Findings (author-side, ranked; none overturns HOLD)

1. **MEDIUM — W1 evidence citations describe a pre-migration retention state, not the candidate's.**
   `w1/Pair06A.md` and `w1/SourceOpenS004.md` cite `.ufo/waves/round-27/fetched/S004-1.raw.gz`, raw sha
   `9ee0766a…`, and "text 6053 bytes sha f24e4f82…", and assert the live bytes are "byte-identical to the r27
   retained body" and that the visible text is "byte-identical across r26 → r27 → live (f24e4f82… in all three)".
   At the candidate the retained representation is `S004-1.public.txt.gz` (file sha `b0cc6a78…`, decompressed
   `3f3c983e…`, 6052 bytes) plus `text/S004-1.txt` (`3f3c983e…`); the manifest records `9ee0766a…` as
   `receivedSha256` with `rawHttpBodyRetained:false`. Measured: r26 text = 6053 B `f24e4f82…`, r27 retained =
   6052 B `3f3c983e…`, differing only by the trailing newline (r26[:-1] == r27); live visible text =
   `3f3c983e…` (≠ `f24e4f82…`); live raw body `c39eeec7…` ≠ `9ee0766a…` (same length, build churn).
   ⇒ the W1 "byte-identical in all three" claim is false as written (byte-identity of the text views across
   rounds; raw-body identity with the retained copy), and the live raw-body identity asserted at 20:01–20:04Z
   no longer holds after the page rebuild. **Impact: none on this ledger row** (the row carries no hashes and
   the quote is present in both retained and live text). Consumers citing the W1 digests as the candidate's
   retained digests will be wrong. Non-blocking; recommend an L1 note that the retained-vs-received distinction
   governs any digest cited for this pair.
2. **LOW — ledger reason is thinner than the contract's "label the inferential step and each source's
   contribution" for a grouped member.** It does not name the citing line (54) nor state that the divergence
   premise is carried by S001/S002/S006/S008 while S004 contributes only "the deployment artifact is a
   packaged unit". The citing file's appended table supplies that scoping (row S004: "HOLD, limited premise:
   the deployment artifact is a packaged unit; this alone does not prove checkout divergence"), so the corpus
   text is correct; the ledger row alone reads slightly unlabelled. Minimal append-only clarification
   available; no verdict change.
3. **LOW (adjacent row, not mine) — the `(S004, ghp-served-set.md)` STALE row carries the artifact-shape quote
   as its `quote`.** That sentence is not the misattributed locator text and cannot itself evidence the defect
   (the misattributed phrase occurs 0× in S004). The STALE is correct (P2) but better evidenced by S003's
   numbered flow; the row's `reason` says so in prose. Flag for the owning seat; no effect on this row.
4. **RESIDUAL — "built/deployable HTML" is not S004's vocabulary** (0 occurrences of "html"/"manifest" in its
   view). S004 supports the artifact unit; HTML-ness of the build output comes from S003/S006. Consistent with
   the recorded reason; noted so a later reader does not widen S004's leg.

## 5. Verification gaps / limits

- One live re-open only (2026-10-21, status 200); no second independent network observation for S004 this
  round beyond the retained r27 capture and the sibling W1 openers' receipts.
- W1 A/B reports were read as author-side evidence only; their claims were re-derived from committed blobs and
  one live GET rather than accepted (P1–P5 are independent).
- Counters/measurements quoted from my own rerun of `count_c1.py` are author-side; L1's recorded 29/29 run and
  the frozen `strictC1: UNPROVABLE` status remain the authority (55/58 decided, 7 units / 3 pairs UNVERIFIABLE
  remain — no pair was promoted to "decided" by this review).

## 6. Recommendation

Admit the `(S004, corpus/knowledge/static-canonical-preflight.md)` HOLD source row as written (fresh, row-specific,
anchor-accurate, scoped). Take finding 1 as an L1 note on retained-vs-received digests for this pair and
finding 2 as an optional append-only scoping clarification. No STALE marker, no ledger rewrite.
