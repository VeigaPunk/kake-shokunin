# Pair04A — (S003, corpus/knowledge/static-canonical-preflight.md) — freshness axis, r27

Seat: reviewer (read-only findings; no ledger/source edits). Lane: leaf, no dispatch.
Target: independently propose HOLD/STALE/UNVERIFIABLE for citing pair **S003 × corpus/knowledge/static-canonical-preflight.md**.
Base/frozen claims read: `.ufo/waves/round-27/contract.json`, `count_c1.py`, `c2-oracle.json`.
Measured revision used: `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (declarations) — corpus tree identical to frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`.

## 1. Exact citing line(s)

Only one citing form for S003 exists in this file — a grouped en-dash range, no literal `S003`:

- `corpus/knowledge/static-canonical-preflight.md:54` → `an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production`
- Claim sentence spans lines 52–54: `Prepare the` / `manifest over actual built/deployable HTML when that artifact exists, not over` / `an assumed checkout served set (S001–S006, `ghp-served-set.md`).`

Range expansion `S001–S006` yields S001…S006, hence this pair (grep for `003` in the file: no match; no other range/list/metadata form names S003). The line was added with the entry in round-22 commit `c0fd6d5` (2026-10-20) and is unchanged since — an inherited citation, not a new one.

## 2. Source re-opened this round (retained bytes, no live call needed)

- Row **S003** — GitHub Docs: *Configuring a publishing source for your GitHub Pages site* — https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- Registry anchor (`corpus/SOURCES.md` S003): “About publishing sources and note under Creating a custom GitHub Actions workflow; fetched 2026-10-19”. Scope: *GitHub Pages publishing modes and repository source selection*. Teaches: *GitHub Pages can publish from a selected branch or from a GitHub Actions workflow*. Status `mined`, recheck `90d`.
- r27 retained: `.ufo/waves/round-27/fetched/S003-1.raw.gz` and `.ufo/waves/round-27/fetched/text/S003-1.txt`; manifest `.ufo/waves/round-27/fetched/manifest.json`.
- fetchIndex **1**; status 200; finalUrl == url (no redirect); fetchedAt `2026-10-21T19:59:55.678521+00:00`; bytes 154136; **sha256 `f42d48b59277843e489896f52f97bb9c62e68970f0c3bebb3021b586ba62a3f5`** (verified by recomputing sha256 over the decompressed blob; matches manifest).
- Supporting quote (≤25 words, verified present verbatim under whitespace normalisation of the retained text): **“You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.”** (25 words; occurs at the “About publishing sources” first paragraph, immediately after the “In this article” nav).
- Corroborating retained text (not the ledger quote): “You can specify which branch and folder to use as your publishing source.” / “The source branch can be any branch in your repository, and the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch.” — and in the custom-workflow section: “Use the actions/upload-pages-artifact action to upload the static files as an artifact.” The row’s second anchor is intact: “A CNAME file in your repository file does not automatically add or remove a custom domain.”

## 3. Judgment: **HOLD** (for S003’s specific contribution to the grouped line)

- Line 54 is a **grouped local synthesis**, not a single-source claim (contract C1 “sourceVerdict”: a grouped recommendation may be local synthesis; the inferential step must be labelled and each source’s contribution identified).
- **Inferential step (explicit):** “the checkout” is an unjustified proxy for the served set *because the Pages publishing source is a selection* (which branch, which folder, or which workflow artifact), and what is served is what that selection builds/uploads.
- **S003’s specific contribution:** the *premise* that the served set is defined by a publishing-source selection — branch (any branch; root or `/docs` folder) versus a GitHub Actions workflow that uploads a static-file artifact. That is exactly the premise that makes “an assumed checkout served set” the wrong object to audit. It supports the citation at its stated scope (publishing modes and repository source selection).
- **What S003 does *not* carry:** artifact-membership rules (hidden-file/`.[^/]*` exclusions, v4/v5 dotfile default, tar shape, 10 GB limit) and Jekyll default exclusions. Those belong to S001/S002/S004 and S006 respectively; the S001–S006 grouping on line 54 is a collective citation, and no single member entails the whole sentence alone. S003’s retained text contains no statement about what the artifact contains (no “hidden”, no archive membership rules).
- **Not STALE:** the cited proposition (“publish from a selected branch or from a GitHub Actions workflow”) is still what the page says, at the row’s stated anchor, in bytes opened this round. No wrong or unsupported attribution to S003 at its own scope was found.
- **Not UNVERIFIABLE:** the source bytes are retained and hash-pinned this round; the anchor sentence is located verbatim; the claim is checkable.

### Stale premise vs. source-date vs. retry boilerplate (explicitly separated)

- **Source-date check:** SOURCES.md records S003 “opened 2026-10-19”, recheck `90d` → not due; r26 re-fetched it 2026-10-21; r27 fetched it 2026-10-21T19:59:55Z. No date-driven staleness.
- **Byte-change triage (not a premise change):** r27 raw sha `f42d48b5…a3f5` differs from r26 raw sha `aa758b4a543f792f3afa1ea37edf4042581719510a479a3f45ce3ace58fdf1ac` (both 154136 bytes), but the diff is confined to per-response Next.js hydration artefacts (`/_next/static/AZNqItOm5dutcdHoWp04P/_buildManifest.js` build-ID and chunk hashes). **Extracted text is byte-identical** (`.ufo/waves/round-26/fetched/text/S003-1.txt` == `.ufo/waves/round-27/fetched/text/S003-1.txt`, 8311 bytes each). So the raw-byte delta is deployment nonce noise, not a changed premise — the freshness axis sees no content drift.
- **Irrelevant retry boilerplate:** none inside the S003 text used as support; no retry markers, no “not found / try again” content. (r26 needed a retry for **S008**, not S003 — that is a different row and does not transfer to S003’s judgment.)

## 4. Suggested C1 ledger record (for `.ufo/waves/round-27/pairs.json`; L1 integrates — not written by me)

```json
{
  "row": "S003",
  "file": "corpus/knowledge/static-canonical-preflight.md",
  "kind": "source",
  "verdict": "HOLD",
  "fetchIndex": 1,
  "quote": "You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.",
  "anchor": "S003 'About publishing sources' section, first paragraph after the 'In this article' nav; row's second anchor (CNAME note under the custom GitHub Actions workflow section) also intact in the same retained bytes",
  "reason": "Grouped local synthesis at lines 52-54 ('Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set (S001-S006)'). S003's contribution is the premise that the Pages publishing source is a selection (any branch with root or /docs source folder, or a GitHub Actions workflow that uploads a static-file artifact), so 'the checkout' is not a self-defining served set. Re-fetched 2026-10-21 (fetchIndex 1, sha256 f42d48b59277843e489896f52f97bb9c62e68970f0c3bebb3021b586ba62a3f5, 154136 bytes, 200, no redirect): the quoted sentence is present verbatim at the row's anchor and the row's second anchor is intact. Extracted text is byte-identical to the r26 retained text; the raw-sha delta is a per-response Next.js build-ID nonce, not a premise change. Artifact-membership and Jekyll-exclusion halves of the grouped sentence are carried by S001/S002/S004 and S006, not by S003; HOLD is scoped to support at S003's stated scope, not to individual entailment of the whole synthesis."
}
```

Gate conformance check (against `count_c1.py` rules): `kind`=`source` ⇒ requires `fetchIndex` (1, present in `fetched/manifest.json`), `quote` (25 words ≤ 25; present in `fetched/text/S003-1.txt` after whitespace normalisation — verified locally), `anchor` (non-empty), `reason` (non-empty); `verdict` ∈ {HOLD,STALE,UNVERIFIABLE}; the pair is in the enumerated citing set (range expansion on line 54) so `not_cited` does not fire. **No `[r27-recheck S003 STALE]` marker is required** because the verdict is HOLD (the marker obligation is STALE-only).

## 5. Appended correction wording

**None required** for this pair: HOLD needs no appended correction in the citing file under the contract, and the r27 gate does not require one. Optional (author-side, not mine to append) — a provenance-clarity line, if the L1 wants the grouped synthesis labelled in-place:

> `[r27-recheck S003 HOLD]` Line 54's `(S001–S006)` citation is a grouped local synthesis: S003 supplies only the publishing-source premise (branch/folder source versus GitHub Actions workflow artifact); artifact-membership rules come from S001/S002/S004 and the Jekyll default exclusions from S006. S003 re-fetched 2026-10-21 (sha256 f42d48b5…a3f5), anchor text unchanged. Evidence: w1/Pair04A.md.

## 6. Observations for the L1 (findings, no edits)

1. **Denominator unchanged by me: 57 citing pairs, 41 decided, 16 missing** at `be375d9` (re-ran `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision be375d90afc6fc7aca369ab3cf5247bf460aeed2`; `findings: []`, `missing` = the frozen 16). My pair is one of those 16; I found **no additional valid citing form** for S003 in this file, so I add **no** pair to the denominator (monotone, not shrunk).
2. **This file contributes 9 of the 16 missing pairs**: S001, S002, S003, S004, S005, S006, S008 (line 54 range `S001–S006` + a literal `S008` at line 184) and **S022, S023** — the latter two arise from the *header* range `(S020-S027)` on line 2 (“verified-at: 2026-10-20 (S020-S027) …”), not from line 54. Flagging because a seat reading only line 54 would miss the S020–S027 expansion; S022/S023 are other seats’ pairs.
3. **Provenance-header gap (not an attribution error):** the entry’s `source:` line 1 and `verified-at:` line 2 enumerate only S020, S021, S026–S029 (plus S024/S025/S030–S034 in later sections). They do **not** list S001–S006, although line 54 cites that range. This is a header-completeness observation about the file, not a mis-attribution about S003’s content, so it does not move this pair off HOLD. If the L1 wants the header to name the range, that is an append-only edit outside this seat’s remit.
4. **Registry `used-by` column is not an enumeration source and is already incomplete:** SOURCES.md S003 lists `corpus/knowledge/ghp-custom-domain.md, corpus/knowledge/ghp-served-set.md` only — it does not list `static-canonical-preflight.md` (nor `publish-channels.md` / `sitemap-orphan-audit.md`, which cite S003 elsewhere). The C1 denominator is derived from citations in knowledge files (range/literal enumeration), so this column must not be used to shrink or deny a pair. Flagging for the L1’s used-by reconciliation; no edit made.
5. **C2 unaffected:** C2 is measured against the unchanged r26 ledger (`frozen/ledger.json`), so this adjudication cannot make its red detection pass; `count_c1.py` is the independent C1 measure.

## 7. Uncertainties / limits

- S003 is a **living documentation page with no version pin**; its recheck window is `90d`. HOLD is a statement about the bytes fetched 2026-10-21, not a durable guarantee; the page could change again (the r26→r27 raw-sha delta shows the wrapper regenerates per response even when prose does not change).
- The recommendation on lines 52–54 is the entry’s own local synthesis. HOLD for S003 covers **support at S003’s stated scope** (publishing modes / source selection); it does **not** assert that S003 alone entails “prepare the manifest over actual built/deployable HTML”, and I do not pretend otherwise.
- The claim “when that artifact exists” is a conditional local instruction; no artifact was available or tested in round22 and none was tested here (read-only seat; no live fetch by me — I used the round's retained bytes, hash-verified against the manifest).
- I did not adjudicate the sibling pairs of the same grouped citation (S001/S002/S004/S005/S006/S008 in this file, S003 in `sitemap-orphan-audit.md`) — those belong to other seats; my verdict here must not be read as covering them.

## 8. Evidence index (commands run, read-only)

- `git log -1 -L 54,54:corpus/knowledge/static-canonical-preflight.md` → `c0fd6d5 Tue Oct 20 18:30:55 2026 round-22: offline canonical publishing preflight`.
- `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision be375d90afc6fc7aca369ab3cf5247bf460aeed2` → population 32, citingPairs 57, decided 41, missing 16, findings [].
- sha256 recomputed over `gzip.decompress(fetched/S003-1.raw.gz)` → `f42d48b5…a3f5` (r27) vs `aa758b4a…f1ac` (r26); `fetched/text/S003-1.txt` (r27) byte-identical to `round-26/fetched/text/S003-1.txt` (8311 bytes).
- Quote presence verified in the retained text; 25 words; anchor located by offset search in the single-line text extraction.
- Raw-byte diff confined to `/_next/static/<buildID>/…` chunk hashes (per-response nonce), e.g. `AZNqItOm5dutcdHoWp04P`; no proposition-bearing prose changed.

Report path: `.ufo/waves/round-27/w1/Pair04A.md` (relative to `/home/vgpnk/Projects/shokunin/kake-shokunin`).
