## Verdict

S021 is live and date-current on the reopened Google Search Central page. Agree with the recorded quote location, date anchor, tier/scope, and both used-by paths. Disagree with one overstrong word in the knowledge entry: “rejects” fragment canonicals is firmer than the source’s “generally doesn't support” wording. The local tool’s stricter fragment policy is separately and correctly identified as local policy, not Google conformance.

## Findings

- **P3 — Knowledge wording overstates S021.**
  - **Command:** `functions.read(path="https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls")`
  - **Exact observed output:** “Don't specify a URL fragment as canonical, as Google generally doesn't support URL fragments.”
  - **Impacted claim/axis:** `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md:21`; freshness/source-faithfulness.
  - **Disagree:** “Its ‘Best practices’ rejects fragment canonicals” can be read as an unconditional processing outcome; S021 advises against them and says Google generally does not support them, not that every such declaration is always rejected.
  - **Smallest fix:** Replace “rejects fragment canonicals” with “advises against fragment canonicals because Google generally doesn’t support URL fragments.” The adjacent statement that the local tool rejects fragments remains correctly scoped as local policy at lines 27–30.

## Checked and held

- **Exact quote and location — AGREE.** The round-22 Gate entry at `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md:44` identifies “The rel=canonical link element.” On the reopened page, the exact location is `Use rel="canonical" link annotations` → `The rel="canonical" link element` → paragraph after the HTML examples. The exact quoted substring is “Even though relative paths are supported by Google, they can cause problems in the long run” (16 words, within the 25-word limit). The page also says the element is accepted only in `<head>` and recommends absolute paths while supporting relative paths.
  - **Command:** `functions.read(path="https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls")`
  - **Exact observed output:** “Use absolute paths rather than relative paths with the `rel="canonical"` `link` element. Even though relative paths are supported by Google, they can cause problems in the long run … and thus we don't recommend them.”
  - **Smallest fix:** None.
- **Access date/version — AGREE, date-anchored rather than immutable-revision-pinned.** `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md:29` records `updated 2026-07-10, opened 2026-10-20`; the Gate heading at `round-22.md:36` dates that source-opening batch to 2026-10-20. The present reopen is 2026-10-21. The page exposes no immutable revision ID; it does expose the same update date.
  - **Command:** same public-page read above.
  - **Exact observed output:** `Last updated 2026-07-10 UTC.`
  - **Smallest fix:** None to the historical `opened` field; this report records the new reopen date.
- **Tier and scope — AGREE.** The row says `docs | A | Google's documented HTML canonical signals and limitations`; `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md:3` says tiers are scoped to the row’s stated topic. This first-party documentation supports claims about Google’s documented recommendations and signals, not guaranteed selection for a site. The live page describes canonical methods as signals and says they increase the chance of a preferred canonical appearing; the knowledge entry also explicitly denies a selection guarantee.
  - **Command:** `functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md:29")` and the public-page read above.
  - **Exact observed output:** `| S021 | ... | docs | A | Google's documented HTML canonical signals and limitations | ... | Head placement matters; absolute URLs are recommended while relatives work; the signal is not a selection guarantee | mined | 2026-10-20 | 90d | ... |`
  - **Smallest fix:** None.
- **Used-by paths — AGREE.** The row names `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md` and `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md`; both exist and actually cite S021. The knowledge file’s `source:` line names `S021 Google canonical guidance` and its URL; the lesson’s table row begins `| S021 |` and gives the same URL and quoted passage.
  - **Exact existence command:** `for f in corpus/knowledge/static-canonical-preflight.md corpus/lessons/round-22.md; do if test -e "/home/vgpnk/Projects/shokunin/kake-shokunin/$f"; then printf '%s: exists\n' "$f"; else printf '%s: MISSING\n' "$f"; fi; done`
  - **Exact observed output:** `corpus/knowledge/static-canonical-preflight.md: exists` and `corpus/lessons/round-22.md: exists`.
  - **Citation observations:** `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md:1` contains `S021 Google canonical guidance https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls`; `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md:44` begins with S021 and the same URL.
  - **Smallest fix:** None.
- **Other S021-derived statements — AGREE.** The reopened source supports the knowledge entry’s head placement, absolute-URL recommendation with relative support, ignored `hreflang`/`lang`/`media`/`type` canonical annotations, and JavaScript guidance. Its signal language does not guarantee Google will select the publisher’s preference.

No corpus production file was changed; this report is the only written file.

## Limits

The public page read exposed its content and “Last updated” date but no immutable revision identifier or response-header evidence. This review establishes what Google currently documents, not actual crawler processing, a particular site’s canonical selection, HTML conformance, or runtime/browser behavior. No build, lint, formatter, or test was run; no tool was installed.