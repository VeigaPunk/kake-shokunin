# Pair08B — critic: (S005, corpus/knowledge/static-canonical-preflight.md)

Seat: KakeR27.Pair08B (critic, read-only). Axis: freshness. Milestone: r27-full-citing-set.
Pair08A's report was not read. No ledger, source or corpus edits were made, nothing was installed, and no live network fetch was made (retained r27 bytes were used).
Measured tree: HEAD `be375d90afc6fc7aca369ab3cf5247bf460aeed2`. The cited file is identical at base `83528f7` (line 54 is unchanged; there is no knowledge-file diff between base and HEAD).

## Verdict (proposed): STALE — the attribution of S005 is wrong at its own stated scope

## 1. Citing line (range expanded)

The only S005 citation in the file is a range. There is no literal `S005`. `count_c1.py:4` uses the RANGE regex `S(\d{3,})\s*(?:[-–—]|\.\.|to|through)\s*S(\d{3,})`, which expands the en-dash range to S001…S006, so the pair is in the frozen set (`c1-before.json:34`, `c2-oracle.json:29`).

- `corpus/knowledge/static-canonical-preflight.md:52-54`: "Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set (S001–S006, `ghp-served-set.md`)."
- Blame: lines 53-56 come from `c0fd6d5` (round-22, 2026-10-20, "offline canonical publishing preflight").
- No other line of the file cites S005, by literal, range or list. The metadata header (line 1, `source:`) lists only S020/S021/S026–S029. The round-26 EOF prose (lines 184-203) names S020–S034 and the boilerplate "S008 via `manifest-retry.json`", which is not an S005 cite. No additional citing pair was discovered.

## 2. Claim scope

This is a grouped local-synthesis recommendation. The canonical-audit manifest should list the HTML that is actually built or deployed, not files assumed to be served because they exist in the checkout. The parenthetical sends readers to `ghp-served-set.md` as the authority for "checkout ≠ served set", and the range lists that entry's sources.

## 3. Counterexample (strongest local evidence)

**`ghp-served-set.md` has never cited S005.**

- Its `source:` line reads "S001, S002, S003, S004, S006, S008 (corpus/SOURCES.md)". The line is identical in every commit touching the file (`02b6dd0`, `9639ec7`, `e28312b`, `b44daed`) and at `c0fd6d5`, the commit that wrote line 54.
- `02b6dd0` (round-20, 2026-10-19) is an ancestor of `c0fd6d5`. The served-set entry's source list was therefore fixed before line 54 was written, so this is not stale drift. The range was imprecise when it was authored.
- `corpus/SOURCES.md` S005 `usedBy` is `corpus/knowledge/ghp-custom-domain.md` only. The `usedBy` field of S001, S002, S004, S006 and S008 names `ghp-served-set.md`; S005's does not.
- The range also silently omits S008 (GNU tar pattern matching), which `ghp-served-set.md` does use for its exclusion semantics. The range is a compact approximation of the referenced entry's sources: it over-includes S005 and under-includes S008.

## 4. What S005 actually says (r27 retained bytes)

- Manifest: `.ufo/waves/round-27/fetched/manifest.json`, row S005, fetchIndex 1.
  - URL = finalUrl = `https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site`, status 200.
  - fetchedAt `2026-10-21T19:59:56.085676+00:00`, 240439 bytes.
  - Decompressed sha256 `6f3d1ad215c9ad1917638c69d60732861dbc1ee758642976c8b1ce08c79e6be4`, recomputed and matching the manifest.
  - gz file sha256 `71f21dfefec0594129e76a6a3a0443e9f0cea4f9e7e07e44d36c9af6106be3cf`; text `text/S005-1.txt` sha256 `b2a7d47d7193dd2f3d8303d32e7d2379b14e7908f26208115516237f6fd8d2ba`.
- Quote (21 words), located twice in the text and in the raw bytes (as `<code>CNAME</code>`), under the anchors "Configuring an apex domain" step 4 and "Configuring a subdomain" step 4:
  > "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored and is not required."
- Also present: "If you use a static site generator to build your site locally and push the generated files to GitHub, pull the commit that added the CNAME file". This is branch-mode CNAME housekeeping, not served-set membership.
- The text contains no `html`, `canonical` or `manifest` token (rg count 0). S005 says nothing about which HTML pages are built, archived or served.

**S005's specific contribution, stated as strongly as the evidence allows.** S005 shows that a checkout file (CNAME) can be inert for domain configuration under Actions publishing. That is a related "checkout ≠ effective publication state" illustration. It is about domain configuration, not page membership. It does not establish whether `/CNAME` or any HTML file is served: `ghp-subpath-spotcheck.md:95,111` keeps "whether Actions serves /CNAME" as an unverified prediction. The served-set premise is carried by:
- S001/S002: artifact exclusions.
- S003: root-or-/docs publishing source.
- S004: the workflow uploads and deploys an artifact.
- S006: Jekyll skip rules.
- S008: tar matching.

Inferential step (local synthesis): "the served set is the deployed artifact, so audit the artifact" is the lane's own conclusion from those rows. S005 is not a premise of it.

## 5. Freshness and stale-premise separation

- **Not source drift.** The r26 bytes (`round-26/fetched/S005-1.raw.gz`, decompressed sha `dc89eecd…0cee9`, the sha pinned in `frozen/population.json`) and the r27 bytes (sha `6f3d1ad2…6be4`) both contain the quote exactly twice. The hash change is page chrome; the relied-on content is unchanged.
- **Not source-date boilerplate.** SOURCES anchor "fetched 2026-10-19" and the header `verified-at` (S020–S029 only) are historical stamps. They are not a wrong claim about S005.
- **Not retry boilerplate.** "S008 via `manifest-retry.json`" (line 184) is the round-26 retry note, not this pair.
- **The defect is an attribution-scope error present since authoring (`c0fd6d5`).** It is neither a premise invalidated by time nor a source-date issue. Under contract C1 "STALE means wrong/unsupported attribution at its own stated scope", so it is STALE rather than HOLD. It is not UNVERIFIABLE because the source bytes were opened and decide it.
- **Metadata gap (finding only, not counted as S005 STALE).** The header `source:`/`recheck:` lines omit S001–S006 entirely, although line 54 relies on them. A future recheck driven by the header would never reopen them.

## 6. Durability caveat

`.ufo/waves/round-27/fetched/` is untracked (`git status` shows `?? .ufo/waves/round-27/fetched/`). A ledger row pointing at fetchIndex 1 is reproducible only once L1 commits these bytes with the manifest.

## 7. Impacted axes

- **Freshness (C1):** this pair must be recorded STALE with a correction appended. A HOLD would certify a source-to-claim link that the source does not make.
- **Operability:** none. C2 detection is unaffected, because this pair is one of the frozen 16 regardless of verdict.
- **Fixable vs. judge-reject:** this is a fixable defect, closed by an append-only correction. It is not a tradeoff the Rust judge must reject. A row-level HOLD for S005 here would be a false-provenance acceptance that the judge should reject.

## 8. Suggested C1 ledger record

```json
{"row":"S005","file":"corpus/knowledge/static-canonical-preflight.md","kind":"source","verdict":"STALE","fetchIndex":1,"quote":"If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored and is not required.","anchor":"Configuring an apex domain step 4; Configuring a subdomain step 4","sha256":"6f3d1ad215c9ad1917638c69d60732861dbc1ee758642976c8b1ce08c79e6be4","reason":"Line 54 range S001–S006 attributes the checkout-vs-served-set premise to ghp-served-set.md's sources, but that entry cites S001-S004, S006, S008, never S005 (unchanged since 02b6dd0, before line 54's c0fd6d5). S005 covers custom-domain CNAME handling only; no HTML/served-membership statement. Attribution wrong at stated scope since authoring; quote stable r26->r27.","report":"w1/Pair08B.md"}
```

## 9. Necessary appended correction (append-only, after line 203)

```text
- [r27-recheck S005 STALE] Line 54's range “S001–S006, `ghp-served-set.md`” sweeps in S005, which `ghp-served-set.md` does not cite (its sources are S001, S002, S003, S004, S006 and S008). The 2026-10-21 S005 bytes concern custom-domain configuration: under a custom Actions workflow “any existing CNAME file is ignored and is not required”. They say nothing about which HTML files are built or served. Read the served-set premise as S001–S004, S006 and S008 via `ghp-served-set.md`; the recommendation to audit built/deployable HTML is this entry's local synthesis. Evidence: w1/Pair08B.md.
```

Optional precision note (not required for C1): the header `source:`/`recheck:` lines do not list the served-set rows that line 54 relies on.

## Uncertainties

- **Reading of the parenthetical.** A reader could take "(S001–S006, `ghp-served-set.md`)" as listing related registry rows rather than the served-set entry's sources. Even under that reading, S005 contributes only the CNAME-inertness analogy, not the stated served-set premise. The verdict stands at the line's stated scope. If the judge accepts "related rows" as the scope, the fallback is HOLD with a precision note recording that S005's contribution is the analogy only. It must not be an unqualified HOLD.
- **No live re-fetch.** The verdict rests on the retained r27 bytes, whose manifest sha was verified.
- **Tool installs:** none.
