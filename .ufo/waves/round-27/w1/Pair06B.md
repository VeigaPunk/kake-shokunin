# Pair06B — critic: (S004, corpus/knowledge/static-canonical-preflight.md)

Seat: KakeR27.Pair06B (read-only critic, leaf). Axis judged: freshness. Milestone: r27-full-citing-set.
The A-seat report for this pair was not read. Peer author-side evidence only; L1 judges.
Tool installs: none.

## Verdict (suggested)

**HOLD at S004's contributing scope.** The grouped line-54 recommendation is a local synthesis. S004 alone does
not say that a checkout differs from the served set. What S004 does supply is narrower: for Actions-published sites
the deployable unit is an uploaded, workflow-produced artifact with its own shape constraints. No attribution in
this file overstates S004, so no `[r27-recheck S004 STALE]` correction is required. One clarification note is
suggested below; it is optional.

## Citing set for this pair

- `rg -n "S0\d\d"` over the file finds **one** citing line for S001–S006: line 54. It uses the en-dash range
  `S001–S006`, which `count_c1.py` RANGE expands to S001..S006 and so covers S004. No literal `S004` appears anywhere
  in the file. Lines 1-2 (`source:`, `verified-at:`) list only S020–S029. Line 184 (r26 EOF prose) lists S020–S034
  and does not name S004. **Pair count for S004 in this file is 1, at line 54.** No new citing pair was discovered.
- Measured file: HEAD `be375d9` blob sha256 `833b28f2…a5c531bc`, which is byte-identical to the frozen base `83528f7`.
  Line 54 was introduced by `c0fd6d5` (2026-10-20).
- This pair is **not** in `.ufo/waves/round-26/statements.json`; S004 **is** in the r26 population. So this is a
  genuine r27 obligation, not a carried r26 adjudication.

## Claim (lines 52-56, read whole)

> "Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout
> served set (S001–S006, `ghp-served-set.md`). No production artifact was available or claimed as tested in round22"

The claim has two parts. (a) This is an operational recommendation to audit the deployable artifact. (b) It asserts
that a "checkout served set" is only an *assumption*. The citation `ghp-served-set.md` points at the local synthesis;
the six rows are its sources.

## Source re-open (r27 retained bytes)

| field | value |
|---|---|
| fetchIndex | 1 (`.ufo/waves/round-27/fetched/manifest.json`, row S004) |
| URL / final | https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages (status 200, no redirect) |
| fetchedAt | 2026-10-21T19:59:55.714609Z |
| raw sha256 (decompressed, 141818 B) | `9ee0766a2fb78e5af104bbc97dfe32ba09ebd8f2d68df1ed2d49efc081a5f53a`, which matches the manifest (I recomputed it with `zcat \| sha256sum`) |
| gz file sha256 | `5820c74b…cae7d`; text file `text/S004-1.txt` sha256 `f24e4f82…ceab7d` |
| drift vs r26 | The r26 raw is `5c15ef2d…6a385` (decompressed) and differs bytewise. The extracted text is **word-identical** (`diff` over word tokens is empty). The HTML-only churn does not change the content. |
| page date | No revision date. Footer reads "© 2026". The `fetched 2026-10-19` anchor in `SOURCES.md:12` is a source-date stamp; it is not a stale premise. |

Exact quotes (each is a whitespace-normalized unique substring of `text/S004-1.txt`, ≤25 words; checked with the
same normalization as `count_c1.py`):

1. Q1, recommended for the ledger (15 words): "The GitHub Pages artifact should be a compressed gzip archive containing a single tar file."
   Anchor: "Configuring the upload-pages-artifact action".
2. Q2 (18 words): "The tar file must be under 10GB in size and should not contain any symbolic or hard links." Same anchor.
3. Q3 (15 words): "Custom workflows allow GitHub Pages sites to be built via the use of GitHub Actions." Anchor: "About custom workflows".

## S004's specific contribution vs. the synthesis

- **Contributes:** Q3 says Actions builds the site. Q1 says the deployable is an uploaded gzip/tar artifact. The
  "Linking separate build and deploy jobs" example builds with `jekyll-build-pages` into `destination:./_site` and
  then uploads that artifact. Together these support claim (a): the thing that gets deployed is the artifact, which
  can be a build output rather than the checkout.
- **Contributes, weakly, to (b):** Q2 says the tar "should not contain any symbolic or hard links". A checkout
  containing links therefore cannot be shipped verbatim. This is a SHOULD, though, so it does not prove that links
  are dropped.
- **Does NOT contribute:**
  - Dotfile exclusion comes from S001 and S002.
  - `/` versus `/docs` source folders come from S003.
  - The Jekyll `_`/`.`/`#`/`~` skips come from S006.
  - Custom-domain behaviour comes from S005.
  - S004 never says that a checkout differs from the published set. The inferential step "checkout ≠ served set" is
    L1/corpus synthesis across the rows plus `ghp-served-set.md`.

## Strongest counterexample tested

The S004 page itself shows a "Single deploy job no building" variant: "upload entire directory path: '.'" (5 words,
unique). In that variant the deployable artifact *is* the checkout directory, uploaded with no build.

- **Does it falsify line 54?** No. Line 54 is conditional ("when that artifact exists") and does not claim that the
  checkout always diverges.
- **Can S004 alone rebut the counterexample?** No. Only S001/S002, which document `upload-pages-artifact` v4
  excluding dotfiles from `path: .`, show that even this variant diverges.
- **Consequence for the ledger:** the S004 row must not be written as though it entails divergence. That would be
  unsupported scope.

## Stale premise vs. date stamp vs. boilerplate

- Line 55, "No production artifact was available … in round22", is a round-scoped historical statement. It is not
  sourced from S004 and is not a stale premise.
- `SOURCES.md` "fetched 2026-10-19" is a source-date stamp. The r27 text is unchanged, so S004 is fresh.
- Line 184, "S008 via `manifest-retry.json`", is **irrelevant retry boilerplate** in this file: S008 is not cited
  anywhere in `static-canonical-preflight.md`. It does not concern S004 and needs no S004 correction.
- Lines 1-2 list sources and verified dates for S020–S029 only. S001–S006 are cited in the body but absent from the
  header. This is a provenance-completeness gap, not a stale attribution.

## Suggested C1 ledger record

```json
{"row":"S004","file":"corpus/knowledge/static-canonical-preflight.md","kind":"source","verdict":"HOLD","fetchIndex":1,
 "quote":"The GitHub Pages artifact should be a compressed gzip archive containing a single tar file.",
 "anchor":"Configuring the upload-pages-artifact action",
 "reason":"Line 54 (range S001–S006) is a grouped local synthesis. S004 contributes only that Actions-published Pages deploy an uploaded workflow-built gzip/tar artifact (no links), supporting 'audit the deployable artifact'; it does not itself state checkout≠served set (that step rests on S001/S002 dotfile exclusion, S003, S006, via ghp-served-set.md). r27 bytes sha256 9ee0766a…; text word-identical to r26."}
```

## Optional appended note (not a STALE correction)

`- [r27-recheck S004 HOLD-note] Line 54's range S001–S006 is a grouped synthesis. S004 (2026-10-21 re-fetch, unchanged text) supports only that Actions deploys an uploaded workflow-built artifact ("The GitHub Pages artifact should be a compressed gzip archive containing a single tar file."); the checkout-versus-artifact divergence rests on S001/S002 and S006 via ghp-served-set.md. S004's own no-build example uploads path '.'.`

## Side finding outside this pair (for the owner of (S004, ghp-served-set.md); r26 carried, not relabelled)

`ghp-served-set.md:29` says "S004 steps 4-5 upload static files and deploy the artifact". The phrase "static files"
**does not occur** in `text/S004-1.txt` (0 matches), and S004's article has no numbered list. S003 r27 fetch #1 does:
its five-item `<ol>` has item 4, "Use the actions/upload-pages-artifact action to upload the static files as an
artifact.", and item 5, "…use the actions/deploy-pages action to deploy the artifact."

The r26 `PairS004GhpServedSet.md` row 3 reached HOLD only through an `[INFERENCE]` cross-job step count. The likelier
reading is an S003→S004 anchor mislabel. The content is still true under S004's section prose, so the impact is on
attribution provenance and the content holds. Suggest that L1 add this as a discovered review item for
(S004, ghp-served-set.md) or (S003, ghp-served-set.md). I issue no verdict here.

## Uncertainties

- The verdict is HOLD only at the contribution scope stated above. I make no claim that S004 entails the whole
  grouped recommendation.
- I did not judge S001–S003, S005 or S006 for this file.
- Commands run, all read-only: rg, sed, sha256sum, zcat, diff, git show/log, and python3 checks of quote
  normalization, r26 ledger membership and the S003 `<ol>` census. No count/gate/test runs.
