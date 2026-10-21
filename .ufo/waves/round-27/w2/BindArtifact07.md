# BindArtifact07 — S005 × corpus/knowledge/sitemap-orphan-audit.md (artifact record), r27 w2 fresh falsification

Seat: KakeR27.BindArtifact07 (leaf, read-only). Axis: freshness. Milestone: r27-fresh-falsification.
Scope: artifact identity/coordinates only (no semantic re-judgement of the S005 verdict; no live fetch).
Candidate frozen: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`. All reads used the explicit full hash.
No source/live/registry edits; scratch only under `/fast/scratch/hyaku/kake-r27/BindArtifact07/`.
No tool installs (none needed).

## Attacked item

`.ufo/waves/round-27/pairs.json` L79-89 — row `S005`, file `corpus/knowledge/sitemap-orphan-audit.md`,
kind `artifact`, verdict `STALE`, evidence `.ufo/round-20/resume/citation-disposition.json`,
contains `"supersededClaim": "Each deployment snapshots the entire checked-out tree."`.

## Independent measurements (declared before each run, then executed)

| # | Expected (declared) | Command | Actual | Exit |
|---|---|---|---|---|
| P1 | evidence blob exists at candidate; hash stable base→declarations→candidate | `git show ac46a74:…` \| `sha256sum` | `d3f33e0b75ba63dde82b0d685bb2b97e5d7f07c14a7bf89ad998dd487c8c56b6`, 17190 B; identical at `83528f7`, `be375d9`, `ac46a74`; `git diff --stat` empty on all three transitions | 0 |
| P2 | `contains` occurs exactly once in the evidence and binds to the sitemap-orphan-audit record, not another source's boilerplate | json scan | count=1 → `platformCorrections` record `location: corpus/knowledge/sitemap-orphan-audit.md:21`, `currentLine 21`, `sources [S001,S002,S004,S006]`; near-neighbour `corpus/lessons/round-7.md:22` has different claim text | 0 |
| P3 | all 8 r20 records of this file omit S005 (supports the reason text) | json scan | 8/8 records `sitemap-orphan-audit.md:{14,18,21,25,28,32,38,112}`; sources ⊂ {S001,S002,S004,S006}; union = {S001,S002,S004,S006}; S005 occurrences in the whole evidence file = 4, all in SKILL.md:16 / publish-channels.md:9,12 / ghp-subpath-spotcheck.md:83 (other entries) | 0 |
| P4 | historical date/base/retry/evidence-filename assertions hold | blob compares | evidence `"base":"cb807bc"`; cb807bc is an ancestor of candidate (2026-10-17); citing-file L1-L3 byte-identical to base (diff: 1 hunk, 0 deletions, 25 EOF insertions; candidate L1-149 == base L1-149); line2 = `…r20 S001-S006 quote corrections 2026-10-19, base cb807bc` unchanged; `retry` occurrences inside the evidence file = 0; no retry claim made for this row | 0 |
| P5 | cited reviewer reports actually contain the dissent the record/ledger says they contain | `grep -c` on `w1/Pair07A.md`, `w1/Pair07B.md` | **FAILS** — see F1 | 0 |
| P6 | ledger is machine-valid at candidate | `python3 -B count_c1.py --root . --revision ac46a74` | `citingPairs 58 / reviewed 58 / decided 55 / knownUnverifiableUnits 7 / 3 pairs`; findings = only the 3 carried-UNVERIFIABLE pairs; outcome for S005×sitemap: `verdict STALE, valid true` | 1 (carried unknowns only) |
| P7 | the `contains` pin is sensitive to the fact it is used to attest | mutation probes on scratch copies | **WEAK** — see F2 | 0 |

## Findings

### F1 — MEDIUM: "min/max-band alternative … in both reviewers' reports" is false for reviewer B (committed source + ledger)

`corpus/knowledge/sitemap-orphan-audit.md:169` (candidate) — "The min/max-band alternative is preserved in
both reviewers' reports" — and `pairs.json:88` — "Both reviewers propose STALE while disclosing a min/max-band
alternative." Evidence read at candidate:

* `w1/Pair07A.md:91-108` §7 does disclose the **min–max interval** reading of provenance bands, with a
  HOLD-branch record at §8a (`:129-132`).
* `w1/Pair07B.md` contains **zero** occurrences of `band`, `min`, `max`, `interval`, `endpoints`
  (`grep -c`: band 0, `min` 0, `max` 0, interval 0, endpoints 0; the only "min" hit is inside "Denominator"
  at L128). Its sole alternative (§"Alternative reading considered", `:77-86`) is a *different* one: reading
  `S001-S006` as "the r20 batch of SOURCES rows opened 2026-10-19" → HOLD at a weaker scope. It also contains
  no HOLD-branch ledger record (`"verdict":"HOLD"` count 0).

The two disclosed alternatives are not the same argument and have opposite implications for whether S005 is
attributed at all (A: band bounds exclude S005 ⇒ the pair arguably should not exist; B: opened-rows band
includes S005 ⇒ attribution literal, HOLD at weaker scope). The committed text therefore names a dissent
document in B's report that is not there, and mis-describes the dissent actually preserved. Both reviewers
did propose STALE, so the verdict's support (P3) is unaffected; the dissent disclosure is not.
Fix would be to attribute the min/max reading to Pair07A and the opened-rows reading to Pair07B separately.

### F2 — LOW: the `contains` pin cannot detect the mutation it is meant to attest (no hash pin in the ledger)

`pairs.json:87` pins only the `supersededClaim` text of the `:21` record; it omits that record's `location`
and `sources`. `count_c1.py`'s artifact check is a bare substring test
(`p['contains'] not in blob(p['evidence']).decode()`). Scratch probes against the candidate evidence blob:

* MUT-E: add `"S005"` to that record's `sources` → pin still present, count_c1 artifact_support still passes.
* MUT-F: repoint that record's `location` to `corpus/knowledge/publish-channels.md:21` → pin still present,
  count_c1 still passes.
* MUT-D control: mutate the `:14` record's `sources` → the reviewer-A-style pin
  (location+currentLine+supersededClaim+sources, `w1/Pair07A.md:140`) *does* fail. So the adopted pin is
  strictly weaker than the reviewer proposal on this axis, and neither pin detects MUT-E/MUT-F.

No sha256 of the evidence is pinned in `pairs.json`; `d3f33e0b…c56b6` appears only in a reviewer report
(`w1/Pair07A.md:50`), and `count_c1.py` pins a sha only for carry-errata items. In practice the evidence file
is byte-stable across base→declarations→candidate (P1), so nothing is currently wrong; this is a verification
gap, not a false statement. Suggested hardening: pin the evidence sha256 (and/or a location+sources-bearing
substring) in the ledger row so P1 stays machine-checkable.

### F3 — LOW / consistency note: same band defect, opposite treatment of S003 vs S005 (both outside {S001,S002,S004,S006})

`pairs.json:80-88` judges S005 STALE ("the band over-attributes S005") while the S003 row for the same file
(`pairs.json:71-77`) is HOLD on a "historical batch/context reading" of the same line-2 band; the candidate
text resolves the split by A2's membership (`corpus/lessons/round-20.md:261` C3 = S001/S002/S003/S004/S006/S008,
i.e. S003 present, S005 absent; A2's pointer does name this file, `sitemap-orphan-audit.md:20-24`), and
`round-20.md:262` A3 = S003/S005/S007 for *other* entries (publish-channels.md:9, SKILL.md:16) — verified.
The split is therefore checkable and holds on the artifact; noted only because the same reasoning could be
read as inconsistent (a range that is "context" for S003 but "over-attribution" for S005). Referred to the
semantic reviewer; not re-judged here.

## Verified clean (no finding)

* `contains` is exact, unique (1×) in the evidence file and lands in the correct record of the correct file —
  not another source's boilerplate (P2); the r20 evidence file is byte-frozen across three revisions (P1).
* Reason text "all8 r20 correction records use S001/S004 or S001/S002/S004/S006" is factually exact (P3).
* Historical date `2026-10-19`, base `cb807bc`, and the evidence filename are as asserted and unmodified;
  no retry fact is asserted for this row and the evidence file contains no retry record (P4).
* No self-citation to `pairs/knowledge` as proof: ledger evidence is the r20 disposition ledger, not the citing
  file; the citing file's Evidence trailer (`:172-175`) names the r20 ledger and `round-20.md:261–262` — both
  verified to exist and say what is claimed (A2 at 261, A3 at 262). Pair07B's *suggested* record would have
  self-cited the citing file; L1 did not adopt it.
* STALE marker `[r27-recheck S005 STALE]` present exactly once; ledger row machine-valid at candidate (P6);
  citing file append-only from base (0 deletions).

## Residual risk / verification gaps

* F1 is a prose-level misdescription inside committed source; the machine gate cannot see it (only the marker
  substring is checked). No automated check of "dissent preserved in both reports" exists.
* P3 verified the 8 r20 records; I did not re-derive S003/S005 source *content* (out of lane) nor re-fetch
  S005's URL (no external fetch required or implied by this record).
* The `:14` vs `:21` distinction is immaterial to P2/P3 (both are this file's records and both omit S005), but
  the pin's ambiguity (F2) means a re-pointed or source-mutated record would still validate.

All measurements are against frozen candidate blobs; no new current-source observation is implied.
