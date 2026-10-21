# Pair03B — critic: (S003, corpus/knowledge/sitemap-orphan-audit.md)

Seat: KakeR27.Pair03B (critic, leaf, read-only). Axis: freshness. Milestone: r27-full-citing-set.
Independence: Pair03A's report was not read; no other Pair report was read.
Tools: none installed or updated. No network fetch, no r24 material read or retried.

## Verdict: STALE (artifact kind) — the S003 attribution is unsupported at the line's own stated scope

## Citing set for this pair
- File hash (worktree = be375d9 = 83528f7 blob): `553ad1006e9e5800668afb033cd655b5d938fe1736b769dd9d82a3019268a0ec`, 149 lines.
- No literal `S003` anywhere in the file. The only citing form is the **range on line 2** (the `verified-at:` metadata), which `count_c1.py` RANGE expands to S001..S006:
  `verified-at: 2026-09-28 (orphan-check baseline ~20:20Z; r16 re-read 2026-09-29T02:2xZ as recorded; r20 S001-S006 quote corrections 2026-10-19, base cb807bc) — historical-not-live-reverified; ...`
- All S-tokens in the file (grep `S\d{3,}`) are on lines 1, 2, 120–127 and 149; none is S003 except via the range. No other citing form exists (no `..`/`to`/`through`/dash variant elsewhere). **No new pair discovered.**

## The claim at its own scope
Line 2 dates this entry's evidence and says round 20 made "quote corrections" for rows S001–S006 on 2026-10-19 at base cb807bc. For S003 this implies S003 backed an r20 quote or correction that applies to this entry.

## Evidence
1. **Line 1 of the same file contradicts the range.** It names exactly the four sources:
   - path `corpus/knowledge/sitemap-orphan-audit.md`, contains `S001, S002, S004, S006 (corpus/SOURCES.md) for the r20 artifact-membership corrections`
2. **The r20 dispositions for this file never use S003.** `.ufo/round-20/resume/citation-disposition.json` (sha256 `d3f33e0b…c56b6`, `"base": "cb807bc"`) has 8 `platformCorrections` at `sitemap-orphan-audit.md:14,18,21,25,28,32,38,112`. Their sources are only {S001,S004} or {S001,S002,S004,S006}. S003 appears in that file only for `SKILL.md:16` and `publish-channels.md:9,12`, the custom-domain corrections.
3. **No revision of this entry ever cited S003 itself.** Per-revision S-token census:
   - `cb807bc`: none.
   - `02b6dd0` and `9639ec7` (both r20): only S001, S002, S004 and S006.
   - `df6196b` (r21, 2026-10-20): first appearance of `S001-S006`.
   - Unchanged through `83098b5`, `3d07733`, `b44daed` and `be375d9`.
4. **The range was written in round 21, not round 20, and it mirrors rows read, not rows used.**
   - `.ufo/waves/round-21/w1/Knowledge19.md` (sha256 `66f6b749…f01ff18`) contains `Source lines cite only S001/S002/S004/S006`.
   - The same file also contains `checked SOURCES rows S001-S006 and S017-S018`.
   - Its own description of the field has no range: `r20 quote corrections 2026-10-19 with base \`cb807bc\``.
5. **Round 20 made no S003 quote "correction".** `.ufo/round-20/resume/sources-gate.md` (sha256 `dcc7a18d…7f0371eb`) records S003's first opened quote, accessed 2026-10-19: "You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site." That file's "Post-review corrections — 2026-10-19" cover only S007 and S008.
6. **The registry does not tie S003 to this entry.** The `corpus/SOURCES.md:11` S003 used-by column lists only `ghp-custom-domain.md, ghp-served-set.md`. `grep sitemap-orphan-audit corpus/SOURCES.md` returns no match.
7. **The round-26 end-of-file note (line 149) already excludes S003 from this entry.**
   - path `corpus/knowledge/sitemap-orphan-audit.md`, contains `The round-20 correction lines in this entry cite S001, S002, S004 and S006 (lines 120-127)`
   - The r26 ledger (`.ufo/waves/round-26/statements.json`) carries S001, S002, S004 and S006 for this file and has no S003 row. That matches c1-before.json listing `(S003, sitemap-orphan-audit.md)` as missing.
   - The r26 recheck receipt `.ufo/waves/round-26/rechecks/S003.json` (HOLD) concerns S003's own row anchors, not this entry.

## Strongest counterexample to STALE (tested, rejected)
- *"It is a historical batch label: S001–S006 are the GHP rows quoted on 2026-10-19 at base cb807bc."*
  - The **dates hold**. S003 was registered (`02b6dd0`, `fetched 2026-10-19`) and quoted on 2026-10-19, and cb807bc is the r20 base (citation-disposition.json and post-review-anchors.json `baseCommit` `cb807bc8d8bc…`).
  - The **attribution fails**: the line ties the range to this entry's provenance, and no S003-backed r20 content exists in this entry.
  - This is a stale premise (over-wide range), not a wrong source date and not irrelevant retry text.
- *"S003 supports body line ~112 ('non-workflow Pages deploy (branch deploy)')."*
  - [INFERENCE] S003 would entail branch-versus-Actions publishing, and the r27 fetch confirms the text is still present (see below).
  - But line 112 dates from r16 and cites no source. Its r20 correction (line 127) cites only S001 and S004.
  - Support that could have been cited is not the same as an attribution actually made, so this does not rescue the range.
- r27 fresh-source check (for contrast only; this pair's kind is artifact, not source):
  - `.ufo/waves/round-27/fetched/S003-1.raw.gz` decompresses to sha256 `f42d48b59277843e489896f52f97bb9c62e68970f0c3bebb3021b586ba62a3f5`, which matches manifest index 1.
  - `text/S003-1.txt` contains `or you can write a GitHub Actions workflow to publish your site` (1 hit).
  - So S003's own row is fresh. Only its attribution to this entry is stale.

## Impacted axes
- freshness (C1): one obligation. It is not decidable as HOLD and needs an appended `[r27-recheck S003 STALE]` correction before `count_c1.py` accepts a STALE row (`correction_missing` otherwise).
- operability (C2): none. This pair was already counted in the 57 frozen pairs, so the denominator is unchanged.

## Suggested C1 ledger record (`.ufo/waves/round-27/pairs.json` → `pairs[]`)
```json
{"row":"S003","file":"corpus/knowledge/sitemap-orphan-audit.md","kind":"artifact","verdict":"STALE","reason":"Only citing form is line-2 verified-at range 'r20 S001-S006 quote corrections 2026-10-19, base cb807bc' (written r21 df6196b). No revision ever cited S003; r20 corrections here (lines 120-127, citation-disposition.json :14..:112) use only S001/S002/S004/S006, matching line 1 and the r26 EOF note. Date and base hold; S003 attribution unsupported.","evidence":"corpus/knowledge/sitemap-orphan-audit.md","contains":"S001, S002, S004, S006 (corpus/SOURCES.md) for the r20 artifact-membership corrections"}
```
Alternate evidence with an equivalent independent substring: `.ufo/waves/round-21/w1/Knowledge19.md` contains `Source lines cite only S001/S002/S004/S006`. Both paths are tracked at be375d9; the substrings were checked with `git show be375d9:<path> | grep -c` (each returned 1).

## Required appended correction (append-only; line 2 left unchanged; preserve historical dates)
Append a new end-of-file section to `corpus/knowledge/sitemap-orphan-audit.md`, for L1 to author:
```markdown
## Round-27 citation recheck

- [r27-recheck S003 STALE] (2026-10-21, append-only; line 2 unchanged). The `verified-at` range "r20 S001-S006 quote corrections" over-attributes: the round-20 corrections in this entry cite only S001, S002, S004 and S006 (lines 120-127; `.ufo/round-20/resume/citation-disposition.json`), and no revision of this entry has cited S003. S003 (publishing source: branch or Actions workflow) was quoted 2026-10-19 for other entries, not used here. Read the range as S001, S002, S004, S006; the 2026-10-19 date and base `cb807bc` stand.
```
If the S005 seat reaches STALE, the same root cause applies. Either use one shared bullet carrying both `[r27-recheck S003 STALE]` and `[r27-recheck S005 STALE]` markers, or keep separate bullets. Never fold S005 in without its own marker.

## Uncertainties and side findings (not decided here)
- **Sibling pair (S005, same file)** is already in the frozen 57 and has the identical defect. S005 (custom-domain CNAME) appears in no revision of this entry. Its owning seat should judge it independently.
- **"quote corrections" wording.** The S001/S002/S004/S006 quotes were first-recorded, not corrected, in r20 (the post-review corrections are S007/S008 only). This label inaccuracy affects the line as a whole, not only S003.
  - The r26-carried S001/S002/S004/S006 pairs for this file show statement counts 8/2/8/2, which match lines 120-127, not line 2. [INFERENCE] r26 did not judge line 2's range.
  - Do not relabel those r26 pairs. Flag this for L1 only.
- I did not observe the live S003 page this round; I relied on the r27 seat-fetched bytes listed above.

## Checks for L1 after integration
- `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision <commit>`: this row should be valid, with no `artifact_support` or `correction_missing` errors, once the correction bullet lands.
