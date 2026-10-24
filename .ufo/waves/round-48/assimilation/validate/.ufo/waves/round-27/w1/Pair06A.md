# Pair06A — S004 × corpus/knowledge/static-canonical-preflight.md (r27, C1 freshness)

Axes: freshness (assigned). Operability: preserved only — no gate, ledger, or corpus edit made by this seat.
Milestone: r27-full-citing-set. Read-only findings; author-side evidence, not admission.

## Verdict

**HOLD** — grouped local synthesis. S004 supports the citing line at its own stated scope
(artifact shape / deployment requirements for custom workflows); it does **not** individually entail
the line's checkout-vs-artifact membership claim, which is carried by S001/S002/S003/S006 (+S008 in
the pointed-to entry). No `[r27-recheck S004 STALE]` marker is required; no appended correction is
needed. No new citing pair discovered (denominator stays 57).

## Locating the citing occurrence (ranges expanded)

`corpus/knowledge/static-canonical-preflight.md` contains **no literal `S004` token**. The only
citing form is an expanded range on **line 54**:

```
54: an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production
```

En-dash range `S001–S006` → **S001, S002, S003, S004, S005, S006**. S004 enters the denominator
only through that range (confirmed by the frozen enumerator: 57 pairs at revision be375d9).

Full claim, `corpus/knowledge/static-canonical-preflight.md:52-56`:

> Prepare the manifest over actual built/deployable HTML when that artifact exists, not over
> an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production artifact was
> available or claimed as tested in round22; its fixtures are local, authorized publisher examples.

S004's contribution inside the group (labelled inferential step, per C1 `sourceVerdict`):

- **S004 alone establishes only that "the built/deployable artifact" is a real, defined unit**
  (a packaged artifact distinct from a checkout tree) and its shape constraints.
- **The membership divergence** (artifact omits checkout paths: hidden/dot paths, `.git`,
  `.github`, Jekyll defaults) is **not** S004's contribution — it comes from S001/S002 (action
  exclusions), S003 (publishing-source selection) and S006 (Jekyll defaults) as recorded in
  `corpus/knowledge/ghp-served-set.md`.
- The line is therefore a **local synthesis** whose cited range names where the evidence lives
  (`ghp-served-set.md`, whose own header lists S001, S002, S003, S004, S006, S008). It is not six
  sources each independently entailing the whole sentence.

## Source re-opened this round

- URL (SOURCES.md:12): `https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages`
- r27 retained bytes: `.ufo/waves/round-27/fetched/S004-1.raw.gz`, **fetchIndex 1**, status 200,
  141,818 bytes decompressed, **sha256 `9ee0766a2fb78e5af104bbc97dfe32ba09ebd8f2d68df1ed2d49efc081a5f53a`**,
  fetchedAt `2026-10-21T19:59:55.714609+00:00`.
- Text view `.ufo/waves/round-27/fetched/text/S004-1.txt`: 6,053 bytes, one line,
  sha256 `f24e4f82d67ed9f617cf62893f0fd4c51b89b6ccc1911d0f335acdf565ceab7d`.
- **Independent re-open by this seat** (single public GET, no account/cookie/browser):
  `2026-10-21T20:04:11Z`, HTTP 200, 141,818 bytes, sha256 `9ee0766a…5f53a` — **byte-identical to the
  r27 retained bytes** (scratch copy `/fast/scratch/hyaku/kake-r27/Pair06A/S004-live.html`).
- r26 retained bytes sha256 `5c15ef2d916a57a9877f75518968df2d644799f08630f9beb5ed8d699206a385`
  differ from r27 raw bytes only in Next.js build-id / chunk-name hashes; the **visible text is
  byte-identical across r26 → r27 → live** (text sha256 `f24e4f82…` in all three). That churn is
  build boilerplate, not source-content change, and is irrelevant to the row's scope.
- The r26 `manifest-retry.json` retry applies to **S008 only**; no retry was performed or needed
  for S004. Not applicable boilerplate for this pair.

## Exact quotes (≤25 words each, verified present once in the r27 text view)

1. `The GitHub Pages artifact should be a compressed gzip archive containing a single tar file.`
   (15 words) — anchor: H2 **"Configuring the upload-pages-artifact action"** (SOURCES.md:12 anchor).
2. `The tar file must be under 10GB in size and should not contain any symbolic or hard links.`
   (18 words) — same H2; this is the r26 receipt quote, retained for continuity.

## Scope test / counterexample attempted

Falsification attempted: read `(S001–S006)` as "all six sources entail the sentence", then S004's
artifact-shape scope would not support the checkout-divergence clause ⇒ STALE. Rejected: the
parenthetical is a pointer to a companion entry that distributes the six sources across distinct
claims (`ghp-served-set.md:1` header lists S001, S002, S003, S004, S006, S008; `:29-30` uses S004
only for "S004 steps 4-5 upload static files and deploy the artifact"). Under this reading the
attribution is accurate at each source's stated scope.

Second falsification: treat the range as stale because `SOURCES.md:12` records `fetched 2026-10-19`
and recheck `90d`. Rejected: the anchor sentence is verbatim present in bytes fetched and
independently re-fetched 2026-10-21; a historical fetch date is provenance, not a stale premise.

Third: treat the raw-HTML sha change r26→r27 as source drift. Rejected: difference is confined to
20 chunk-hash token edits; the text view is byte-identical.

Residual precision (not STALE, out of this pair's citing file): `SOURCES.md:12` `teaches` says
"gzip-compressed tar files under 10GB" while the source says the artifact is "a compressed gzip
archive containing a single tar file" and the 10GB bound attaches to the tar inside it — already
recorded as a caveat in `.ufo/waves/round-26/w1/RowS004.md`. `SOURCES.md` is not this pair's citing
file, so no correction is proposed here.

## Suggested C1 ledger record (contract C1 `pairs.json`, top-level `pairs`)

```json
{
  "row": "S004",
  "file": "corpus/knowledge/static-canonical-preflight.md",
  "kind": "source",
  "verdict": "HOLD",
  "fetchIndex": 1,
  "quote": "The GitHub Pages artifact should be a compressed gzip archive containing a single tar file.",
  "anchor": "H2 \"Configuring the upload-pages-artifact action\" (SOURCES.md:12 anchor); .ufo/waves/round-27/fetched/text/S004-1.txt",
  "reason": "Line 54 cites the expanded range S001-S006 (en dash) as a grouped local synthesis: prepare the manifest over the actual built/deployable artifact, not over an assumed checkout served set. S004's contribution at its own scope (artifact shape and deployment requirements for custom workflows) is that the Pages artifact is a real packaged unit, a gzip archive containing a single tar file under 10GB with no symbolic or hard links; that anchors 'that artifact exists' in the sentence. The membership divergence from a checkout is not S004's claim and is carried by S001/S002/S003/S006 (S008 in the pointed-to entry ghp-served-set.md). Anchor sentence verbatim in the 2026-10-21 bytes (sha256 9ee0766a2fb78e5af104bbc97dfe32ba09ebd8f2d68df1ed2d49efc081a5f53a), re-opened independently by this seat at 2026-10-21T20:04:11Z with identical bytes; no stale premise and no correction required."
}
```

## Appended correction wording

**None required.** HOLD requires no `[r27-recheck S004 STALE]` marker in the citing file. No text in
`corpus/knowledge/static-canonical-preflight.md` was changed, and no ledger/source edit was made by
this seat.

## Evidence hashes and limits

- `corpus/knowledge/static-canonical-preflight.md` (working tree, unmodified):
  `833b28f26fa7309f7e31398275bae2f704969d8e6f095bc5bb96250da5c531bc` — identical to
  `.ufo/waves/round-27/frozen/expected.json` entry for that path, i.e. the citing file still matches
  the frozen snapshot.
- `corpus/SOURCES.md`: `5001eadee20c65c5df364a88430b6b0e76a99940afc282d72fecdd6d7c6be62d`.
- `.ufo/waves/round-27/fetched/manifest.json`: `d3b0b1ca215bfa6d89edf639b2b87475d668fdf73cbf0ddf089c87e11d043781`.
- `.ufo/waves/round-27/fetched/text/S004-1.txt`: `f24e4f82d67ed9f617cf62893f0fd4c51b89b6ccc1911d0f335acdf565ceab7d`.
- `.ufo/waves/round-27/fetched/S004-1.raw.gz` (file bytes): `5820c74b55a4303ac940dd38f821888093f77431f7b0ae36de8d8ee1e4e990b9`;
  decompressed sha256 as in the manifest.
- `.ufo/waves/round-26/rechecks/S004.json` (prior-round receipt, r26 HOLD):
  `81233a452aac4393230e3678a6d628a91e328c59c7a6ae83f8f7fed9bb23aa5a`.
- Live re-open raw sha256 equals the r27 retained decompressed sha256 exactly.

Limits / uncertainties:

- Freshness evidence covers the **S004 anchor sentence only**. The r26 receipt's snippet-level pins
  (`upload-pages-artifact@v4`, `deploy-pages@v4`, `configure-pages@v5`, `checkout@v6`) live in this
  unpinned living document and were **not** re-verified as current versions here; S004 pins no action
  version, so this does not affect the row's scope.
- The text view is a single line; "anchor" is a heading, not a line number.
- No tool was installed or updated for this seat (curl + Python stdlib only).
- **Integration dependency for the L1 (not a defect of this pair):** `count_c1.py` reads
  `.ufo/waves/round-27/fetched/manifest.json`, `fetched/<raw.gz>` and `fetched/text/S004-1.txt`
  as **git blobs at the measured revision**. Those paths are currently untracked in the working tree
  (`git status` shows `?? .ufo/waves/round-27/fetched/`), so a `kind: source` ledger row can only be
  counted once the r27 fetched directory is committed. Flagging for the integrator; no action taken
  here.

## Denominator effect

Enumerated pairs at revision `be375d90afc6fc7aca369ab3cf5247bf460aeed2` = **57** (unchanged). S004
pairs at that revision: `ghp-served-set.md` (r26 decided), `sitemap-orphan-audit.md` (r26 decided),
`speedrun-pipeline.md` (r26 decided), `publish-channels.md` (r27 gap, Pair05B),
`static-canonical-preflight.md` (r27 gap, this seat). **No additional citing pair discovered**; the
monotone `discovered-pairs.json` obligation is unchanged by this seat.

## Independent corroboration within this round

`.ufo/waves/round-27/w1/SourceOpenS004.md` (sibling source-open seat) independently reports the same
live decode sha256 `9ee0766a…5f53a`, byte-identical to the r27 manifest entry, with the same
conclusion: **no prose drift** (raw-HTML difference confined to Next.js buildId / webpack chunk
hashes; text view identical r26 → r27 → live). It judges the page's contribution to this citing
line as **indirect and premise-only** — "the page never mentions a manifest and never states the
served set differs from the checkout". This agrees with the scope test above: S004 supports "that
artifact exists" (the artifact-as-deployable premise) and nothing about checkout membership.

That seat's preferred test quote is the version-pinned code line under H2 "Linking separate build
and deploy jobs":

`- name: Build with Jekyll uses: actions/jekyll-build-pages@v1 with: source:./ destination:./_site - name: Upload artifact uses: actions/upload-pages-artifact@v4`

(16 words; exact member of `fetched/text/S004-1.txt`). I did **not** adopt it as the ledger quote:
it pins live action versions (`jekyll-build-pages@v1`, `upload-pages-artifact@v4`) that this
unpinned living document can change, whereas the sentence I recorded ("The GitHub Pages artifact
should be a compressed gzip archive containing a single tar file.") is the prose that carries S004's
own recorded scope in `SOURCES.md:12` (artifact shape) and is what the row's `teaches` cell rests
on. Both quotes satisfy the C1 ≤25-word/membership test; the choice affects only which sentence
anchors the record, not the verdict.

Cross-seat note for the parent: the shared range `S001–S006` at line 54 also names **S005**, whose
row's `usedBy` is `ghp-custom-domain.md` and which is absent from `ghp-served-set.md`'s source
header (that header lists S001, S002, S003, S004, S006, S008). That is a range-composition question
belonging to the **S005 × static-canonical-preflight.md** pair, not to S004; it does not change this
verdict.
