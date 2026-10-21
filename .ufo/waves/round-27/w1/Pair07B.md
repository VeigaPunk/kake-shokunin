# Pair07B — critic, (S005, corpus/knowledge/sitemap-orphan-audit.md)

Seat: KakeR27.Pair07B (critic, read-only). Axis: freshness. Milestone: r27-full-citing-set.
Independent judgment; the Pair07A report was not read. No ledger or source edits. No tool installs.
Measured revision: be375d90afc6fc7aca369ab3cf5247bf460aeed2 (worktree HEAD). The citing file is byte-identical
at base 83528f7c, at be375d90 and in the worktree: sha256 553ad1006e9e5800668afb033cd655b5d938fe1736b769dd9d82a3019268a0ec (149 lines).

## Verdict

**STALE (partial).** The r20 date (2026-10-19) and base `cb807bc` on line 2 hold. Including S005 in the
range `S001-S006` is an unsupported attribution at the line's own stated scope: S005 grounds none of the
round-20 corrections in this entry.

## Citing location (range expanded)

The only S005 citation in the file comes from expanding the range on line 2. A scan with the `count_c1.py`
regexes finds one range, `range 2 S001-S006`, and no literal `S005` on any line.

- `sitemap-orphan-audit.md:2` (full line):
  `verified-at: 2026-09-28 (orphan-check baseline ~20:20Z; r16 re-read 2026-09-29T02:2xZ as recorded; r20 S001-S006 quote corrections 2026-10-19, base cb807bc) — historical-not-live-reverified; no live sitemap or domain fetch this round`
- Kind: historical metadata (front-matter `verified-at:`). This is not r26 EOF prose.
- Provenance: introduced by the r21 commit `df6196b` (2026-10-20 06:08:53 -0300, "round-21: make publishing
  corpus provenance and gates inspectable"), together with line 1. The r20 commits did not write it.
  Found with `git log -S 'r20 S001-S006 quote corrections'`.
- Baseline: `.ufo/waves/round-27/c1-before.json` lists `{S005, sitemap-orphan-audit.md}` and
  `{S003, sitemap-orphan-audit.md}` as missing (57 citing pairs, 41 decided, 16 missing). r26
  `statements.json` carries only S001, S002, S004 and S006 for this file, so r26 never expanded the line-2 range.

## The claim and its scope

Read in context, the clause says: on 2026-10-19 at base `cb807bc`, round 20 corrected this entry with
quote-grounded corrections from rows S001 through S006. Because it sits in this entry's `verified-at:`,
its scope is this entry. It is not a corpus-wide statement about which SOURCES rows were opened.

## Strongest counterexample (local evidence)

1. **The r20 disposition ledger excludes S005 from every correction in this file.**
   `.ufo/round-20/resume/citation-disposition.json` `platformCorrections[8..15]` covers all 8 locations in
   this file (lines 14, 18, 21, 25, 28, 32, 38, 112). Their `sources` lists are `["S001","S004"]` or
   `["S001","S002","S004","S006"]`. The ledger has only 4 `"S005"` occurrences, and none is in a
   sitemap-orphan-audit record. The occurrence closest to this file's records (json:291) belongs to
   `"location": "corpus/knowledge/publish-channels.md:12"` (superseded claim: "The setup script's
   repository CNAME configures the Actions custom domain.").
2. **The tails themselves (lines 120-127) cite only S001, S002, S004 and S006.** There is no literal
   S005 at any of them.
3. **The same r21 commit's line 1 narrows the set:**
   `S001, S002, S004, S006 (corpus/SOURCES.md) for the r20 artifact-membership corrections`.
   The r26 EOF line 149 says the same:
   `The round-20 correction lines in this entry cite S001, S002, S004 and S006 (lines 120-127).`
4. **The subject matter does not fit.** S005's scope is "Custom-domain configuration for Actions-published Pages sites"
   (`.ufo/waves/round-26/population.json`, row S005; `corpus/SOURCES.md:13`). The citing file contains no
   `CNAME`, `custom domain` or `custom-domain` text (rg exit 1). S005 is mapped to a different
   misconception: `corpus/lessons/round-20.md:262`, A3, "C3: S003/S005/S007 rows plus `ghp-custom-domain`".
   This file's misconception is A2 (`round-20.md:261`, which cites `corpus/knowledge/sitemap-orphan-audit.md:20-24`):
   "C3: S001/S002/S003/S004/S006/S008 rows". S005 is absent there too.
5. **"Quote corrections" wording.** Round 20 recorded no quote correction to S005. The only r20 quote
   errata are for S007 ("schema wording is a transcription") and S008 ("1.35" label withdrawn)
   (`round-20.md:309-311`). "S001-S006 quote corrections" is therefore loose shorthand for corrections
   grounded in S00N quotes. Under that reading S005 is still not one of the grounding rows (points 1-3).

## Stale premise vs source date vs boilerplate

- **Source date: holds and is preserved.** S005 was opened on 2026-10-19 (`SOURCES.md:13`, `opened` column).
  The r20 resume is dated 2026-10-19 with base `cb807bc` (`round-20.md:146-149`), and the r20 source
  table row S005 reads "fetched 2026-10-19" (`round-20.md:207`). The date and base on line 2 are correct.
  `cb807bc` is itself dated 2026-10-17 because it is the base, not the correction commit, so this is consistent.
- **Stale premise: not the defect.** S005's content has not drifted. The r27 fetch
  (`.ufo/waves/round-27/fetched/S005-1.raw.gz`, fetchedAt 2026-10-21T19:59:56Z, decompressed sha256
  6f3d1ad215c9ad1917638c69d60732861dbc1ee758642976c8b1ce08c79e6be4, matching the manifest) still contains
  `any existing CNAME file is ignored and is not required` (`fetched/text/S005-1.txt`, sha256 b2a7d47d…d2ba).
  The raw bytes differ from r26's fetch (dc89eecd…), but the quote survives. Content freshness is irrelevant to this pair.
- **Boilerplate: irrelevant.** "no live sitemap or domain fetch this round" on line 2 describes r21's own
  fetch activity. It is not an S005 claim and needs no action.
- **The defect is an authoring-time over-broad range.** The r21 writer collapsed {S001, S002, S004, S006}
  into `S001-S006`, which swept in S003 and S005. It is not time-decay.

## Alternative reading considered (uncertainty)

If `S001-S006` is read only as "the r20 batch of SOURCES rows opened 2026-10-19", the clause is literally
true and the pair could be HOLD at that weaker scope. I reject that reading because:
- The clause is this entry's `verified-at:`, so it dates this entry's verification.
- The sibling line from the same commit (line 1) enumerates the grounding rows and excludes S005.
- Under the weak reading, S005 would be cited in a file it contributes nothing to. That is exactly the
  unsupported-attribution case the contract's `sourceVerdict` names.

The parent judges this. I did not round it to UNVERIFIABLE because the evidence is decisive either way.

## Suggested C1 ledger record (`.ufo/waves/round-27/pairs.json` → `pairs[]`)

The primary record is artifact kind, because the defect is historical attribution, not source content:

```json
{"row":"S005","file":"corpus/knowledge/sitemap-orphan-audit.md","kind":"artifact","verdict":"STALE",
 "evidence":"corpus/knowledge/sitemap-orphan-audit.md",
 "contains":"The round-20 correction lines in this entry cite S001, S002, S004 and S006 (lines 120-127).",
 "reason":"Only citation is line 2 range 'r20 S001-S006 quote corrections 2026-10-19, base cb807bc' (r21 df6196b historical metadata). Date/base hold, but S005 grounds none of this entry's r20 corrections: .ufo/round-20/resume/citation-disposition.json platformCorrections[8..15] list only S001/S002/S004/S006 for all 8 locations; line 1 and line 149 enumerate the same four; S005 (custom-domain CNAME) maps to misconception A3, not this file's A2. Over-broad range attribution, not source drift."}
```

Self-check against `count_c1.py`:
- `contains` is a substring of the committed blob: `rg -F` matches line 149. It also exists at be375d90,
  whose sha256 matches the worktree file.
- The `(row, file)` key is in the citing set.
- The STALE verdict requires the marker `[r27-recheck S005 STALE]` in the citing file at the measured
  revision. It is not present yet, so the L1 must append the correction below or the record fails `correction_missing`.

Alternative source-kind record (also valid; it shows S005's scope is custom domains only):
`{"kind":"source","fetchIndex":1,"quote":"any existing CNAME file is ignored and is not required","anchor":"Configuring an apex domain, step 4"}`
(the quote is 9 words, verified present in `fetched/text/S005-1.txt`), with the same verdict and reason.

## Correction wording to append (append-only EOF; line 2 unchanged)

Suggested new section at the end of `corpus/knowledge/sitemap-orphan-audit.md`:

```markdown
## Round-27 citing-set recheck

- [r27-recheck S005 STALE] Line 2's `r20 S001-S006 quote corrections` over-attributes S005. The round-20 corrections in this entry (lines 120-127) cite only S001, S002, S004 and S006 (`.ufo/round-20/resume/citation-disposition.json`, platformCorrections for this file); S005 (custom-domain configuration) grounds none of them. The 2026-10-19 date and base `cb807bc` stand. Line 2 is historical r21 metadata and stays unchanged.
```

## Sibling impact (not my row)

`{S003, sitemap-orphan-audit.md}` is the other missing pair from the same range, and the same evidence
applies to it. S003 is absent from every `platformCorrections[8..15]` source list in this file, although
round-20.md:261 (A2) does name S003 as a C3 row for this misconception. Whoever judges S003 should weigh
that A2 mention; it may change S003's outcome relative to S005's. If both end up STALE, the L1 should use
one EOF section with a separate marker per row, because `count_c1.py` checks each `[r27-recheck S0NN STALE]` independently.

## Denominator

No new citing pair found. A literal and range scan of this file at be375d90 yields S001, S002, S003, S004,
S005 and S006, all already counted (4 from r26 + 2 missing). Nothing to add to `discovered-pairs.json`.

## Checks for the L1 after integration

- `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision <commit>`: the S005/sitemap outcome should be `valid:true`.
- `rg -F '[r27-recheck S005 STALE]' corpus/knowledge/sitemap-orphan-audit.md`
- Lines 1-149 of the citing file are unchanged (append-only).
