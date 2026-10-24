# PairS021 × static-canonical-preflight: round-26 freshness recheck

Seat: KakeR25.PairS021StaticCanonicalPrefl-6 (knowledge pair, leaf). Milestone r26-recheck-build. Axis: freshness. Operability not exercised.

## Evidence base

- Re-fetched bytes: `fetched/manifest.json` row S021 (index 1, status 200, fetchedAt 2026-10-21T15:10:43.417148+00:00, last-modified Fri, 10 Jul 2026 10:12:15 GMT, bytes 194799).
- Digest check: decompressed `fetched/S021-1.raw.gz` = 194799 bytes, sha256 4edda778243cee4a2138fa31541226d22fc7be155a1ee385ce11a26674c7e5c5, which matches the manifest. The `.gz` file's own sha256 (c2614527…) is not the manifest value, so the manifest digest covers the decompressed body. Text view `fetched/text/S021-1.txt` sha256 1e77f15623098db427757be742464d7d244adb17e0cbcffb0503638de353b792.
- Page version: footer "Last updated 2026-07-10 UTC." and last-modified 2026-07-10. This matches the SOURCES row (`updated 2026-07-10`, SOURCES.md:29).
- Corroboration: `.ufo/waves/round-23/w1/ReopenGoogleCanonical.md` (2026-10-21) observed the same footer, the same absolute-path passage and the same fragment wording. Its P3 finding is row 6 below.
- Limit: this lane has no retained 2026-10-20 S021 copy, so byte identity with that earlier read is not proven. [INFERENCE] The 2026-07-10 last-modified date predates the 2026-10-20 opening, so that read most likely saw the same bytes.

Result: 12 statements; 9 HOLD; 3 STALE (rows 2, 6, 10).

## Verdict table

Entry = `corpus/knowledge/static-canonical-preflight.md`. Quotes are verbatim from `fetched/text/S021-1.txt`; each occurs exactly once.

| # | Entry line | Statement (entry wording) | Verdict | Anchor in re-fetch | Verbatim quote | Reason |
|---|---|---|---|---|---|---|
| 1 | 1 | `source:` header: "S021 Google canonical guidance" + URL | HOLD | Page title and breadcrumb: How to specify a canonical URL with rel="canonical" and other methods | `To specify a canonical URL for duplicate or very similar pages to Google Search, you can indicate your preference using a number of methods.` (24 words) | Same URL; finalUrl equals url; status 200. The page is the guidance the label names. |
| 2 | 2 | `verified-at: 2026-10-20 (S020-S027)`, applied to S021 | STALE (date superseded) | Footer | `Last updated 2026-07-10 UTC. LinkedIn Join us on LinkedIn` (9 words) | Version date 2026-07-10 still holds (footer and last-modified). The 2026-10-20 verification date is superseded by 2026-10-21 observations: the round-23 reopen and this round-26 re-fetch. Correction A. |
| 3 | 18-19 | Google's rel=canonical annotations "requires the HTML declaration in the head" | HOLD | "Use rel="canonical" link annotations" > "The rel="canonical" link element". The page quotes rel="canonical"; the entry drops the quote marks, which is typographic only. | `The rel="canonical" link element is only accepted if it appears in the <head> section of the HTML` (17 words) | Supported. Scope note, not a verdict change: the same section also offers an HTTP-header form ("You can provide the rel="canonical" link annotations in two ways"), which the entry does not claim is head-bound. |
| 4 | 19 | "recommends absolute URLs while supporting relatives" | HOLD | "Use absolute paths rather than relative paths with the rel="canonical" link element" | `Even though relative paths are supported by Google, they can cause problems in the long run` (16 words) | Supported. The same paragraph ends "and thus we don't recommend them." |
| 5 | 19-20 | "ignores canonical annotations carrying hreflang/lang/media/type" | HOLD | "Use rel="canonical" link annotations", first paragraph | `specifically, rel="canonical" annotations with hreflang, lang, media, and type attributes are not used for canonicalization.` (15 words) | Supported; the same paragraph says annotations that suggest alternate versions of a page "are ignored". |
| 6 | 20-21 | "Its 'Best practices' rejects fragment canonicals" | STALE (overstated; already corrected at lines 140-142) | "Best practices For all canonicalization methods" is present | `Don't specify a URL fragment as canonical, as Google generally doesn't support URL fragments.` (14 words) | Google gives advice ("Don't specify...") and says it "generally doesn't support" fragments. It does not say "rejects". Rejection is this tool's local policy (lines 27-30). Round-23 P3 found the same. Correction B. |
| 7 | 21 | "explains that JavaScript may affect the signal" | HOLD | "Best practices", client-side rendering paragraph | `make sure that JavaScript doesn't change the canonical link element` (10 words) | Supported. |
| 8 | 22-23 | "documented processing rules, not guarantees that it chooses the publisher's preference" | HOLD | Intro list: "in order of how strongly they can influence canonicalization" | `A strong signal that the specified URL should become canonical.` (10 words) | Supported: methods are graded signals. Sitemap section: `Google must still determine the associated duplicate for any canonicals that you declare in the sitemap.` (16 words). |
| 9 | 23-24 | "Absence of a declaration is not inherently a site error" (S021 basis) | HOLD | Intro paragraph | `none of them are required; your site will likely do just fine without specifying a canonical preference.` (17 words) | Supported. The clause "a failure only when the explicit local publishing policy requires one" is local policy and is not judged. |
| 10 | 25 | "Cross-domain canonical is likewise not intrinsically invalid." | STALE (attribution: S021 silent) | None. S021-1.txt has 0 hits for "cross", "Cross", "another site" and "hostname". | `Google supports explicit rel canonical link annotations as described in RFC 6596.` (12 words), the nearest passage; it defers annotation semantics to S020 | Not stated by S021. The entry's own support is the RFC 6596 sentence at line 14 ("a different hostname may be valid"). SOURCES.md:28 (S020 row) reads "Relative and cross-host targets are permitted". The round-23 reopen did not check this sentence. Correction C. |
| 11 | 27-30 | "stricter local policy: one canonical signal, no fragment or credential-bearing target, an HTTP(S) target ..." (contrast with Google) | HOLD | Intro paragraph after the list: `these methods can stack`; "Use rel="canonical" link annotations": "We recommend" | `these methods can stack and thus become more effective when combined` (11 words); `We recommend that you choose one of these and go with that` (12 words) | Supported as a contrast. Google encourages stacking, so "one canonical signal" is stricter, and it matches Google's advice to choose one rel=canonical delivery method. "No fragment" and the HTTP(S) and credential rules are local policy; S021 says only "generally doesn't support" fragments. |
| 12 | 140-142 | [r23-correction] "rejects fragment canonicals overstates S021: Google says it generally does not support fragment canonicals" | HOLD | "Best practices", fragment bullet | `Don't specify a URL fragment as canonical, as Google generally doesn't support URL fragments.` (14 words) | The correction matches the source. No new text needed. |

Totals: 12 statements; 9 HOLD (rows 1, 3, 4, 5, 7, 8, 9, 11, 12); 3 STALE (rows 2, 6, 10).

## Correction blocks

Append at end of file to `corpus/knowledge/static-canonical-preflight.md`, per the contract's EOF `[r26-recheck S0NN STALE]` rule. No existing line is rewritten.

Correction A (row 2):

```
[r26-recheck S021 STALE] The S021 verification date on line 2 (2026-10-20) is superseded. S021 was reopened 2026-10-21 in round 23 (w1/ReopenGoogleCanonical) and re-fetched 2026-10-21T15:10:43.417148+00:00 in round 26 (fetched/manifest.json row S021, index 1, status 200; decompressed body sha256 4edda778243cee4a2138fa31541226d22fc7be155a1ee385ce11a26674c7e5c5). The page footer still reads: Last updated 2026-07-10 UTC. The version date holds; lines 1-2, 18-25, 27-30 and 140-142 were re-judged in .ufo/waves/round-26/w1/PairS021StaticCanonicalPrefl.md.
```

Correction B (row 6, line 21):

```
[r26-recheck S021 STALE] Line 21's 'rejects fragment canonicals' still overstates S021 on the 2026-10-21 re-fetch. The Best practices text reads: Don't specify a URL fragment as canonical, as Google generally doesn't support URL fragments. The operative correction is [r23-correction] at lines 140-142; rejecting fragment canonicals is this tool's stricter local policy, not Google's documented wording.
```

Correction C (row 10, line 25):

```
[r26-recheck S021 STALE] Line 25's 'Cross-domain canonical is likewise not intrinsically invalid' is not stated by S021. The 2026-10-21 re-fetch (fetched/text/S021-1.txt) has no cross-domain or cross-host canonical statement and defers annotation semantics to RFC 6596. The entry's support is the RFC 6596 sentence at line 14 (S020; SOURCES.md S020 row: Relative and cross-host targets are permitted). Read line 25 as an S020 claim, not an S021 claim.
```

## Considered, not counted

- Line 3 (`recheck:` instruction) and lines 5-9 (scope): no S021 citation or reliance.
- Lines 11-16 (RFC 6596, S020 only), and the RFC 6596 clause at line 30; row 11 judges the rest of lines 27-30.
- Lines 70-72 (comments, raw script text, template descendants): parser boundary, S026 and S025 basis; no S021 citation.
- Lines 77-78 ("fragments are rejected rather than silently stripped"): local URL-policy behavior with no S021 citation. Fragment support is judged in rows 6, 11 and 12.
- Lines 80-88 (empty-authority references; S027-S029), lines 96-136 (round-23 body markup and snapshots; S024, S026, S030, S031), lines 149-155 (round-23 falsifier clarifications; S030, tool-scope statements), and lines 157-179 (round-24 receipt replay; S032-S034): none cite S021.
- Lines 143-146 ([r23-correction] on template descendants): cites S025, not S021.

## Discrepancies and routing

- The brief names "r20-correction tails". The entry has none: a case-insensitive scan finds no r20 text or tag. The only correction tails are two [r23-correction] items at lines 140 and 143; the second is S025 and is not counted.
- Round-23 P3 (w1/ReopenGoogleCanonical.md) suggested replacing line 21 outright. The entry carries an append-only tail at lines 140-142 instead, which is the policy. Correction B only re-confirms it.
- SOURCES.md:29 (S021 row) still reads `opened 2026-10-20`, `recheck 90d`. L1 may log the 2026-10-21 fetch in those allowed status/recheck cells. This seat did not edit it.
- Routing: `corpus/lessons/round-22.md` also cites S021 (population.json usedBy; round-23 cites its line 44). Not judged here; route to the lessons seat. SOURCES.md:51 (reading order) names S021 but is not a knowledge-entry statement.

## Verification exercised

- Read-only only. Digests, quote presence, word counts (9-24, all at or under 25) and a negative search were computed in memory. No files were written except this report.
- Negative search for cross-domain statements in S021-1.txt: "cross" 0 hits, "Cross" 0, "another site" 0, "hostname" 0. "domain" 3 hits, all about certificate subdomains. "other sites" 1 hit: external signals consolidate to same-site URL variants.
- Entry scan: S021 appears only at lines 1 and 140. No r20 tags. [r23-correction] appears at lines 140 and 143.
- Not run: builds, tests, linters, network GETs, browsers, probes. No round-24 assignment, probe or counter was read, run, retried or rephrased.
- Tool installs or updates: none. Stdlib Python only.

Report: .ufo/waves/round-26/w1/PairS021StaticCanonicalPrefl.md

```json
{"pair":"S021xstatic-canonical-preflight","statements":12,"hold":9,"stale":3,"corrections":["[r26-recheck S021 STALE] The S021 verification date on line 2 (2026-10-20) is superseded. S021 was reopened 2026-10-21 in round 23 (w1/ReopenGoogleCanonical) and re-fetched 2026-10-21T15:10:43.417148+00:00 in round 26 (fetched/manifest.json row S021, index 1, status 200; decompressed body sha256 4edda778243cee4a2138fa31541226d22fc7be155a1ee385ce11a26674c7e5c5). The page footer still reads: Last updated 2026-07-10 UTC. The version date holds; lines 1-2, 18-25, 27-30 and 140-142 were re-judged in .ufo/waves/round-26/w1/PairS021StaticCanonicalPrefl.md.","[r26-recheck S021 STALE] Line 21's 'rejects fragment canonicals' still overstates S021 on the 2026-10-21 re-fetch. The Best practices text reads: Don't specify a URL fragment as canonical, as Google generally doesn't support URL fragments. The operative correction is [r23-correction] at lines 140-142; rejecting fragment canonicals is this tool's stricter local policy, not Google's documented wording.","[r26-recheck S021 STALE] Line 25's 'Cross-domain canonical is likewise not intrinsically invalid' is not stated by S021. The 2026-10-21 re-fetch (fetched/text/S021-1.txt) has no cross-domain or cross-host canonical statement and defers annotation semantics to RFC 6596. The entry's support is the RFC 6596 sentence at line 14 (S020; SOURCES.md S020 row: Relative and cross-host targets are permitted). Read line 25 as an S020 claim, not an S021 claim."]}
```
