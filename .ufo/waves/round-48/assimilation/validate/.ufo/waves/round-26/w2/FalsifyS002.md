# FalsifyS002 — round-26 C1 freshness falsification (lane: kake-shokunin)

**Target:** receipt `.ufo/waves/round-26/rechecks/S002.json` (verdict **HOLD**), row S002 in
`corpus/SOURCES.md`, anchor bytes in `.ufo/waves/round-26/fetched/S002-1.raw.gz` /
`S002-2.raw.gz`, and two plain public GETs of the row URLs compared today (2026-10-21).

**Verdict: AGREE** — the HOLD is correct on the judged (freshness) axis; no defect found that
changes the verdict. Two low-severity residual observations recorded below (version-attribution
pointer inside the v5.0.0 body; a paraphrase in the receipt's `reason`), neither of which
overturns the HOLD.

---

## 1. Did the quote really ground THIS row's teaches (not page chrome / a neighbouring clause)?

Row teaches (SOURCES.md S002 cell): “v4.0.0 excludes hidden dotfiles by default; v5.0.0 adds
the include-hidden-files input”.

- The receipt quote “Potentially breaking change: hidden files (specifically dotfiles) will not
  be included in the artifact by @tsusdere in #102” occurs exactly once in the regenerated text
  view `fetched/text/S002-1.txt`, word-bounded (boundary chars are spaces), and is character-for-
  character equal to the release-body bullet extracted from the `data-test-selector="body-content"`
  div of `S002-1.raw.gz` (raw line 701; body div starts at raw line 699, after the v4.0.0 tag
  header). So it is grounded in the release body, not in page chrome.
- It is **not** grounded in the document `<head>` meta description. The string also appears in
  `twitter:description`/`og:description` (chars ~23600, 3 occurrences of the sentence in the raw
  head area), but the receipt quote is taken from the body bullet; the head-meta occurrence would
  be the “page chrome” trap, and the receipt did not fall into it. (For the counter, the text
  view is the authoritative text; `HTMLParser` does not emit attribute values, so the text view
  has the quote exactly once.)
- The quote is the **first** bullet of v4.0.0's “What's Changed”, not a neighbouring clause
  (the neighbour bullet is “Pin actions/upload-artifact to SHA by @heavymachinery in #127” —
  not quoted). It is the exact sentence that supports the v4 half of the teaches.
- Cross-contamination check: the v5 phrase “feat: add include-hidden-files input @jonchurch
  (#137)” is absent from the v4.0.0 body, and the v4 phrase is absent from the v5.0.0 body.
  No page confusion.

**The quote grounds the v4.0.0 half.** The v5 half is not carried by the receipt `quote` field
(there is only one quote slot; fetchIndex=1); it is carried by `anchorObserved`/`reason` and is
verbatim present in `fetched/text/S002-2.txt` and in the live v5.0.0 body. This matches the
wave's own one-quote-per-row convention (cf. S001's receipt) and is accepted by the counter's
`quote_in_text`/`quote` rules.

## 2. Is the anchor observed correct in raw bytes?

Anchor cell: “v4.0.0 What's Changed and v5.0.0 Changelog; release tags
7b1f4a764d45c48632c6b24a0339c27f5614fb0b and fc324d3547104276b827a68afc52ff2a11cc49c9”.

- `S002-1.raw.gz`: exactly one `<h2>What's Changed</h2>` (body div, raw line 699); the v4.0.0
  tag header renders commit short SHA `7b1f4a7` and the full SHA `7b1f4a764d45c48632c6b24a0339c27f5614fb0b`
  appears 2× (raw line 657 commit href + hovercard). Header precedes body (char 176106 < 181243).
- `S002-2.raw.gz`: exactly one `<h1>Changelog</h1>` (body div, raw line 705); the v5.0.0 tag
  header renders commit short SHA `fc324d3` and the full SHA `fc324d3547104276b827a68afc52ff2a11cc49c9`
  appears 2× (raw line 663/666). Header precedes body (char 176501 < 181638).
- The two pages are mutually exclusive on the anchor headings (v4 has 0 `Changelog` h1; v5 has 0
  `What's Changed` h2) — the receipt did not confuse the two documents.
- “Latest” badge: v5.0.0 page carries the `Label--success ... "Latest"` badge (2 occurrences),
  v4.0.0 page carries none → v5.0.0 is the newest release as of both the retained fetch and the
  live fetch. No newer release supersedes the row's v4/v5 scope.

**Anchor observed is correct.**

## 3. Did content/version change in a way the receipt missed? (freshness)

- Live GET of both row URLs today returns **200** and the *release body text is byte-identical*
  to the retained `fetched/S002-1.raw.gz` / `S002-2.raw.gz` (v4 body 591 chars, v5 body 327
  chars, exact equality). Full normalized page text is also identical (3509 chars v4 / 3588 v5,
  0 diff hunks). The only byte differences in the raw HTML are 40 volatile hunks (GitHub asset
  hash churn: `wp-runtime-*.js`, `environment-*.js`, `fetch-nonce`, etc.) — not content.
- Release stamps identical: v4.0.0 2025-08-14T19:21:06Z, v5.0.0 2026-04-10T18:22:59Z, both in
  retained and live. “commits to main since this release” 11 (v4) / 4 (v5) unchanged.
- The text views are reproducible: `fetched/text/S002-1.txt` == `text_of(gunzip(S002-1.raw.gz),
  content-type)` + "\n" (3483 B), same for S002-2 (3559 B). So the amendment's “all 32 receipt
  quotes re-found” holds for this row.
- The row cell in `corpus/SOURCES.md` is byte-identical between base 97404de4… and candidate
  e28312b1… (sha256 757ba5aa… for both). The receipt file in the worktree is byte-identical to
  the candidate blob (sha256 7efa5f33…).
- The v5.0.0 page contains two failed-partial count “Uh oh! There was an error while loading.”
  React blankslates at raw chars 173595 and 186489, bracketing the anchor body (181638–183358).
  The cited sentences are inside the server-rendered `body-content` div, not in a failed partial —
  checked, does not affect the anchor.

## 4. Residual observations (do not change the verdict)

**R1 (version-attribution pointer inside v5.0.0 body).** The v5.0.0 release body ends with
“See details of all code changes since previous release.” linking `compare/v4.0.0...v4.0.1`
(S002-2.raw.gz line 710; present live too). This is the only occurrence of “v4.0.1” on either
retained page, and `v4.0.1` occurs **zero** times in `corpus/` (grep) and zero in the corpus
lineage. That pointer means the changelog bullets under the v5.0.0 “Changelog” heading are framed
by the page itself as the v4.0.0→v4.0.1 diff — i.e. a v4.0.1 release/tag exists between
v4.0.0 and v5.0.0 that the row's anchor and scope do not record. Consequently, whether the
include-hidden-files input *first* shipped in v5.0.0 or in v4.0.1 is **not established by the
round-26 retained bytes**. What IS established and sufficient for the row's teaches:
  - the v4.0.0 tag commit's `action.yml` (S001-1.raw.gz lines 33-35/51-53/69-71) hard-codes
    `--exclude=".[^/]*"` with no `include-hidden-files` input (the v4.0.0 page also says “instead
    of using this action, create your own artifact” → no opt-in in v4.0.0);
  - the v5.0.0 **tag commit** `fc324d3` `action.yml` carries `include-hidden-files` defaulting to
    `false` (corpus/knowledge/publish-channels.md:73, round-23 receipt c7 at base; 2895 B, same
    size as main's action.yml);
  - main (S001-2, commit 5f327015) has the input, default `false`.
  So “v5.0.0 adds the include-hidden-files input” holds at the row's stated v4-vs-v5 scope; the
  stricter “first introduced in v5.0.0 (not v4.0.1)” claim is unverified within scope. No v4.0.1
  bytes exist anywhere in the lane to resolve it, and fetching /releases/tag/v4.0.1 is outside the
  lane's allowed-GET bound (not a URL in corpus/SOURCES.md). Recorded as a verification gap, not a
  staleness.

**R2 (paraphrase in the receipt's `reason`).** The reason says the v4.0.0 page “says hidden
dotfiles are excluded by default”; the source text says they “will not be included in the
artifact” and offers no opt-in (workaround = create your own artifact), and the v4.0.0 action.yml
hard-codes the exclusion. “By default” is the corpus's established phrasing (used in README,
publish-channels, ghp-served-set), true of the current/main input's `false` default, and looser
for v4.0.0 where the exclusion is unconditional. This is a wording/attribution imprecision in the
receipt's prose, not a change the HOLD missed, and it does not affect the verdict.

## 5. Verification notes

- No tools installed/upgraded (recorded per generic-rules). No network traffic beyond two plain
  public GETs of the row's own URLs (both in corpus/SOURCES.md), compared only, nothing saved.
- I did **not** run `measure.py` (counter seat is separate; my item's commands are the receipt
  read, SOURCES row, raw-byte reads, and the optional row-URL GET). Receipt schema was verified by
  inspection against `measure.py`'s rules: keys exactly match `RECEIPT_KEYS`; verdict ∈
  {HOLD,STALE}; fetchIndex=1 is a population fetch of S002; quote 18 tokens/18 words (≥6 tokens,
  ≤25 words); quote word-bounded in the fetch-1 text; quote occurs in no other population row's
  text view (only `fetched/text/S002-1.txt`); `correction: null` is normal for HOLD.
- Row + receipt immutability base→candidate verified via `git show` (row sha256 757ba5aa…
  identical; receipt sha256 7efa5f33… identical).

---

## Summary

- **Verdict: AGREE** (HOLD correct on freshness). Agent quote grounds the v4.0.0 half; v5 half
  verbatim in the v5.0.0 body; anchor observed correctly in raw bytes (headings, tag→commit SHAs,
  Latest badge); no content/version change (live == retained body text); row and receipt unchanged
  base→candidate.
- Severity: **none** for the receipt's verdict. Two residual items (R1 version-attribution
  pointer => v4.0.1; R2 “by default” paraphrase) are documented as low-severity observations /
  verification gaps, not corrections to the verdict.

```json
{"target":".ufo/waves/round-26/rechecks/S002.json","verdict":"AGREE","severity":"none"}
```
