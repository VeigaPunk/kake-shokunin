# Pair02B — critic, (S002, corpus/knowledge/static-canonical-preflight.md)

Seat: KakeR27.Pair02B (critic, leaf, read-only). Axis: freshness. Milestone: r27-full-citing-set.
I did not read the Pair02A report. No ledger or source edits were made, and no tools were installed.

## Verdict

**HOLD at the line's stated scope, with a scoped, partial contribution.** S002 grounds one premise of the
grouped recommendation: under upload-pages-artifact v4.0.0 or later, the artifact differs from the checkout
because dotfiles are excluded by default. It does not entail the recommendation itself, which is to prepare
the canonical manifest over the built/deployable HTML. That step is local synthesis. No STALE attribution
was found, so no `[r27-recheck S002 STALE]` tag is required.

## Citing line (range expanded)

- `corpus/knowledge/static-canonical-preflight.md:52-54` at base `83528f7` and at `be375d9`. The blob is
  `d86ddec6e6acc05b3c1f60da87a97a0f2645c8bf` at both revisions, and the worktree is unchanged, with sha256
  `833b28f2…c531bc`.
  > "Prepare the manifest over actual built/deployable HTML when that artifact exists, not over
  > an assumed checkout served set (S001–S006, `ghp-served-set.md`)."
- The range is written with an en-dash (U+2013). The count_c1 RANGE pattern matches it and expands it to
  S001..S006. This is the only S002 occurrence in the file; I searched for `S00[1-6]` and found line 54 only.
- Surrounding claim, lines 54-56: "No production artifact was available or claimed as tested in round22;
  its fixtures are local, authorized publisher examples." That sentence is round-22 self-description and
  does not depend on S002.

## r27 retained bytes (manifest `.ufo/waves/round-27/fetched/manifest.json`, sha256 `d3b0b1ca…3781`)

| fetchIndex | URL | status | fetchedAt | raw sha256 (re-verified from gz) |
|---|---|---|---|---|
| 1 | …/releases/tag/v4.0.0 | 200 | 2026-10-21T19:59:53Z | `43d5e22d3d02d07e4cb8abfb1bd35b01cc29ccba819fa1d9d3883c3f278ef070` ✔ |
| 2 | …/releases/tag/v5.0.0 | 200 | 2026-10-21T19:59:55Z | `bc5d74856acfadf73123ddc235c84019ed12e43af91b1b6c030b22c3786693a0` ✔ |

The text files are `text/S002-1.txt` (sha256 `b87d66d3…143b`) and `text/S002-2.txt` (sha256 `3eab768e…230`).
I checked the quotes below with count_c1's whitespace-normalized containment test; all are found and all are
under 25 words.

- fetchIndex 1, anchor "v4.0.0 release, What's Changed" (rendered commit 7b1f4a7, relative-time 2025-08-14T19:21:06Z), 18 words:
  "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact by @tsusdere in #102"
- fetchIndex 1, same block, 22 words:
  "If you need to include dotfiles in your artifact: instead of using this action, create your own artifact according to these requirements"
- fetchIndex 1, context: "Full Changelog: v3.0.1...v4.0.0".
- fetchIndex 2, anchor "v5.0.0 release, Changelog" (rendered commit fc324d3, relative-time 2026-04-10T18:22:59Z, labelled "Latest"), 6 words:
  "feat: add include-hidden-files input @jonchurch (#137)"

## S002's specific contribution and the inferential step

1. **What S002 supplies.** For one publishing path, upload-pages-artifact v4.0.0+, the artifact excludes
   dotfiles by default. Its own remedy for including them is to build a different artifact. Together these
   show that artifact membership is decided when the artifact is built, not by the checkout tree. That is
   direct support for the negative half of line 54: do not assume the checkout is the served set.
2. **What S002 does not supply, and what is local inference.**
   - The source never mentions HTML, canonical links, manifests or preflight. "Prepare the manifest over
     built/deployable HTML" is the lane's synthesis.
   - Its scope is the Actions plus upload-pages-artifact path only. Branch publishing and Jekyll exclusions
     belong to S003 and S006. The `.git`/`.github` exclusions belong to S001. The tar mechanics and subset
     uploads belong to S004 and the `ghp-served-set.md` repro.
   - Practical reach for an HTML manifest is narrow. Only HTML under dot paths (for example
     `.well-known/*.html` or `.hidden/index.html`) is affected; `.nojekyll`-style dotfiles are not pages.
     The inference is still sound because one excluded page is enough to make a checkout-derived manifest
     wrong. **[INFERENCE]**
3. **Strongest counterexample I tested: v5 makes dotfile inclusion opt-in.** This strengthens the
   recommendation rather than weakening it, because membership now depends on a workflow input instead of
   the checkout. The r27 S001-2 main `action.yml` bytes also show `include-hidden-files` with
   `default: "false"`, so the exclusion is still the default. That fact comes from S001, not S002; S002's v5
   page states no default.
4. **Second counterexample tested: is line 54 broader than S002?** Yes. Line 54 makes a general
   publisher-practice claim. However, the citation is grouped (S001–S006 plus `ghp-served-set.md`), and the
   line does not claim that S002 alone entails it. Under the contract, a grouped synthesis is acceptable as
   long as each source's contribution is labelled. That labelling is missing in the entry, so I recommend
   a non-STALE precision note (wording below).

## Freshness

- **No stale premise.** As of 2026-10-21T19:59:55Z, v5.0.0 is still marked "Latest". No v6 appears, and
  the page shows "4 commits to main since this release".
- **Release dates are history, not staleness.** The 2025-08-14 and 2026-04-10 dates describe when each
  release was published. They do not make the premise stale.
- **The entry's dated metadata does not cover S002.**
  - Line 1 (`source:`) lists S020–S029 only, so S001–S006 are cited in the body but absent from the header.
  - Line 2's `verified-at` names S020–S027 and S028–S029 only.
  - The line-184 r26 recheck row list (S020…S034) omits S001–S006. S002 was therefore never source-rechecked
    *in this entry* before r27. It was rechecked under `ghp-served-set.md` (r26 HOLD,
    `.ufo/waves/round-26/rechecks/S002.json`).
  - This is a metadata coverage gap, not a wrong attribution, and it is not STALE.
- **Retry boilerplate is irrelevant to S002.** Line 184's "S008 via `manifest-retry.json`" names the r26
  retry of S008, which `ghp-served-set.md:95` already labels as not a source. It does not touch S002.
- **The r26 bytes differ from the r27 bytes.** The r26 S002 sha256 values `455adcec…` and `28d5566a…` differ
  from r27's `43d5e22d…` and `bc5d7485…`, which is expected for dynamic GitHub HTML. The relied-on sentences
  are unchanged.
- **Carried r26 pair versus new r27 observation.** `(S002, ghp-served-set.md)` and `(S002, publish-channels.md)`
  are r26-carried pairs. This pair is a new r27 obligation, and it is not one of the r26 41.

## Suggested C1 ledger record (pairs.json)

```json
{"row":"S002","file":"corpus/knowledge/static-canonical-preflight.md","kind":"source","verdict":"HOLD",
 "fetchIndex":1,
 "quote":"Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact by @tsusdere in #102",
 "anchor":"v4.0.0 release page, What's Changed (commit 7b1f4a7, 2025-08-14); corroborated by fetchIndex 2 v5.0.0 Changelog 'feat: add include-hidden-files input @jonchurch (#137)' (commit fc324d3, Latest at 2026-10-21T19:59:55Z)",
 "reason":"Line 54 grouped citation (S001–S006 expanded). S002 contributes only the premise that, for upload-pages-artifact v4.0.0+, the artifact excludes dotfiles by default (v5 makes inclusion opt-in), so checkout membership is not artifact membership. Preparing the canonical manifest over built/deployable HTML is local synthesis S002 does not state; scope limited to the Actions upload-pages-artifact path and dot-path HTML. r27 bytes sha256 43d5e22d…/bc5d7485… verified. Not STALE."}
```

## Suggested appended wording (not STALE; optional precision note under an r27 heading)

> - S002 note (r27, not STALE): line 54's grouped "(S001–S006, `ghp-served-set.md`)" is a local synthesis.
>   S002 contributes only that upload-pages-artifact v4.0.0+ omits dotfiles from the artifact by default
>   (v5.0.0 adds the opt-in `include-hidden-files` input). It says nothing about HTML or canonical
>   manifests; the "built/deployable HTML" step is this entry's inference. S001–S006 are not in this
>   entry's line-1 `source:` header, and S002 was not in the round-26 row list at line 184 (re-fetched
>   2026-10-21, `.ufo/waves/round-27/fetched/manifest.json` S002 indices 1–2).

## Uncertainties and risks for L1

- **The r27 source evidence is not committed.** `.ufo/waves/round-27/fetched/` is untracked (`git status`:
  `??`). count_c1 reads the manifest and text through `git show <revision>:`, so this record fails with
  `source_missing` until `fetched/` is committed at the measured revision.
- **Quote fragility.** The quote is matched against extracted text that includes GitHub page chrome.
  Containment passes on the current bytes.
- **Possible header discovery.** The header gap (S001–S006 missing from line 1) adds no new citing pair,
  because line 54 already counts. I found no other citing form for S002 in this file, so I have no new
  discovered pair to report.
