# CritClaimFit — round 27 W1 critic (claim fit, causal separability, frontier)

Seat: KakeR27.CritClaimFit (leaf critic, read-only). No admission authority; findings only.
Judged on: freshness. Milestone: r27-full-citing-set.
Read at declaration commit be375d90afc6fc7aca369ab3cf5247bf460aeed2 (base 83528f7):
- contract.json `6d2d7f51371650c2d7535c401ead613355135d18b44762c41f385d05ee7582da`
- count_c1.py `a1e46d19b438fc254689dc42f474664864b7fd7fecc6a992ad70f5d5da44a14c`
- c2_count.py `93f39b0f7187fa084abd220d8c3734ce02b11b64cd940a1953347f37fa304686`
- c2-oracle.json `1d038205473180c7cb57895c2d480a8b52debe3bf08ab0a2f58ca7b1f67bc7dd`

Probes ran only in a scratch clone at /fast/scratch/hyaku/kake-r27/CritClaimFit/clone (branch crit-probe,
TMPDIR set there). No lane, worktree, index or Git mutation. No tool installs.

## Verdict summary

Both counters can be driven green without doing the claimed work. Every probe below exited 0 or passed.

| # | Claim | Counterexample | Result | Defect or tradeoff |
|---|---|---|---|---|
| F1 | C1 | All 16 pairs adjudicated as `kind:artifact` with `evidence` = the citing file itself | count_c1 exit 0, decided 57/57, newDecided 16, no fetch used | Fixable defect |
| F2 | C1 | The 16 pairs appended to the r26 `statements.json` at the candidate revision, no r27 `pairs.json` | count_c1 exit 0, decided 57/57, newDecided 0 | Fixable defect |
| F3 | C1 | All 41 carried r26 pairs have no `verdict` field; all counted as decided | Structural (observed) | Fixable defect, needs disclosure |
| F4 | C2 | Gate that hard-codes the 16 oracle pairs and ignores its input | c2_count passed: true, detected 16/16, FP 0 | Tradeoff (one-point consumer oracle) |
| F5 | C2 | Always-clean gate plus `c2-oracle.json` rewritten at the candidate (expectedPairs [], expectedExit 0) | c2_count passed: true | Fixable defect |
| F6 | C1 | Page-chrome quote ("GitHub Docs", "Help and support") is in all of S003-1…S006-1 | Passes count_c1 quote check (line 50) | Fixable defect (QUALITY r26 rule not enforced) |
| F7 | C1/C2 | 10/16 frozen pairs are metadata or r26 boilerplate, not substantive claims | Observed | Claim-fit debt, disclose |
| F8 | C2 | Gate has no consumer path (not in the SKILL.md gate table or any runner) | Observed | Axis-fit tradeoff |
| F9 | C1 | Denominator excludes 167 population pairs in 16 non-knowledge files | Observed | Declared narrowing; name it |

Probe output hashes (scratch): probeA2 `e310be31…c9c8`, probeB `e25d59f8…4381`, probeC `05a5435e…ba994`,
probeD `7f1943c6…ea09`. probeA (literal-only `contains`) gave decided 47 because 10 pairs are cited only via ranges.
probeA2 set `contains` to the matched range text, e.g. `S001–S006`, and reached 57/57.

## C1 findings (freshness)

**F1. Self-citation satisfies artifact adjudication.** count_c1.py line 54 checks only
`p['contains'] in blob(p['evidence'])`. Nothing stops `evidence == file`, or `contains` being the citation token itself.
Contract C1 says each of the six grouped pairs is "grounded against sources opened this round". count_c1 does not
require `kind=source` for those six. probeA2 adjudicated all six grouped pairs as artifact/self and passed.
- Impacted axis: freshness. The claim "six grouped pairs grounded against sources opened this round" has no oracle.
- Smallest safe correction: in count_c1, require `kind=='source'` with a manifest `fetchIndex` for the six
  `static-canonical-preflight.md × S001–S006` pairs. Reject artifact rows where `evidence == file`, where `evidence`
  is a corpus/knowledge file, or where `contains` matches `\bS\d{3}`. Because count_c1 is frozen, the parent should
  instead apply these as judge-side review rules and disclose the counter's gap, not rewrite the counter post hoc.

**F2. The r26 carry is read at the candidate revision.** count_c1 line 31 reads `.ufo/waves/round-26/statements.json`
at `--revision`. Contract `r26Record` says the r26 ledger is "unchanged", but the counter does not enforce that.
probeB extended the r26 ledger and C1 went green with zero r27 work.
- Correction: the judge must require `git diff be375d9 <candidate> -- .ufo/waves/round-26/ .ufo/waves/round-27/{count_c1.py,c2_count.py,c2-oracle.json,frozen/,contract.json}` to be empty before trusting either counter.
  Alternatively, pin those reads to be375d9.

**F3. Carried r26 pairs are counted as decided without any verdict.** Keys in the r26 `statements.json` are
`addedBy,file,l1Disposition,reclassified,report,row,seatStale,seatUnverifiable,stale,staleAlreadyCorrected,statements,w2`.
There is no `verdict` field. Line 32 counts all 41 as decided. Two carried pairs contain UNVERIFIABLE statements:
S001×ghp-served-set (`seatUnverifiable` 3, "4 v3.0.1 statements UNVERIFIABLE") and S033×static-canonical-preflight
(`seatUnverifiable` 3). Contract C1 says "UNVERIFIABLE explicit, never counted decided" and requires a "durable HOLD or
supported STALE adjudication". At pair level, 41/57 is "has an r26 statement review", not "HOLD/STALE".
- Uncertainty: pair-level vs statement-level semantics are not defined anywhere I found. I do not claim these pairs
  are undecided. I claim the counter cannot tell the difference.
- Correction: the report must state that the 41 carried pairs are counted on r26 review existence. It must also list
  the 2 pairs that carry UNVERIFIABLE statements. Do not present them as HOLD.

**F6. Quote uniqueness is not enforced.** count_c1 line 50 checks only that the quote is a substring of the fetched text.
QUALITY.md round-26: "page chrome or any text that also occurs in a different source's bytes cannot ground a row."
Verified: "GitHub Docs" and "Help and support" occur in S003-1, S004-1, S005-1 and S006-1. A row quoting chrome would
pass the counter.
- Correction: judge-side, reject any r27 source quote that occurs in another fetched text. That takes one loop over
  `fetched/text/*`.

**F7. Freshness gain is mostly mechanical, so report the split.** Where the 16 frozen pairs come from (observed at be375d9):
- 6 substantive: static-canonical-preflight.md:54 "(S001–S006, `ghp-served-set.md`)". This is the only group where a
  fresh fetch is meaningful. Manifest: 8 GETs, all status 200, finalUrl == url.
- 4 historical verified-at metadata ranges: publish-channels.md:2 "S001-S007 opened that day" (S004, S006), and
  sitemap-orphan-audit.md:2 "r20 S001-S006 quote corrections" (S003, S005).
- 2 metadata ranges: static-canonical-preflight.md:2 "(S020-S027)" (S022, S023).
- 4 r26 EOF boilerplate: "S008 via `manifest-retry.json`" in crawl-scope-per-host.md:57, ghp-custom-domain.md:62,
  ghp-etag-anatomy.md:60 and static-canonical-preflight.md:184.

The QUALITY r26 rule says "A historical verified-at date … is not a stale claim; record it as a note." So 6 of the 16 can
only be HOLD by rule, and 4 can be settled by artifact lookup. Generic metadata-only work for those 10 is correct.
Counting them as fresh source observations would be false provenance.
- Correction: the report presents C1 as 6/16 fresh-source adjudications plus 10/16 artifact or rule adjudications, with
  separate counts. Metadata rows must cite a real external artifact (r20 receipt, round-26 `manifest-retry.json`), never
  the citing file.

**F9. Target narrowing (declared, but the milestone name overstates it).** The denominator is corpus/knowledge only. The
same regexes over the other corpus files at be375d9 find 167 population pairs in 16 files: README.md 10, QUALITY.md 3,
SOURCES.md 32, and the rest in lessons/*. SOURCES.md is the registry and lessons are historical records, so excluding
them is defensible. README.md and QUALITY.md are live documents.
- Correction: no counter change (the contract is frozen). The final report must state "full knowledge-file citing set"
  and name the 13 README/QUALITY pairs as out of scope. Do not call it the full corpus citing set.

## C2 findings (operability)

**F5. The oracle is read from the candidate revision.** c2_count.py line 9 reads `c2-oracle.json` and
`frozen/expected.json` from `--revision`. The `snapshot_tampered` check compares frozen bytes against an
`expected.json` that the candidate also controls. probeC (always-clean gate, oracle rewritten) reported passed: true.
`frozenRevision` is printed but never compared.
- Impacted: operability, plus the C1/C2 separability claim ("C2 measured against unchanged r26 ledger").
- Correction: the same pinned-diff precondition as F2, or have c2_count read the oracle and frozen files from be375d9.

**F4. Selftest vs consumer measurement.** The only consumer-side oracle is one fixed input. probeD's gate prints the
16 hard-coded pairs and passes 16/16 with 0 false positives. The contract relies on `--selftest`, at least 12 fixtures
and mutation probes to rule this out. Those are producer-authored in the same wave (BuildSelftest, BuildFixtures), so
they are not an independent consumer measurement.
- Tradeoff, not just a defect: one frozen point cannot separate a real gate from a memorized one.
- Smallest correction: L1 or the judge runs the candidate gate on at least one non-author mutation of the frozen
  snapshot. Example: delete one S001–S006 range from a copied static-canonical-preflight.md and expect 15 findings;
  add an `S008..S009` form and expect the extra pair. This must be done outside the writer-owned fixture tree. Without
  it, report the C2 capability as "selftest-attested", not "consumer-measured".

**F8. Axis fit: the operability claim has no consumer.** No runner invokes `scripts/citing_set.py`. The SKILL.md gate
table (lines ~212/387/555/568) lists freshness-sweep, corpus-contract and accessibility-packet. The gateInterface does
not require registration. The capability's only beneficiary is the freshness ledger's completeness. That makes C2 an
instrument for the freshness axis, which pushes against "distinct-axis causal separability". Both claims improve
citing-set freshness integrity: one fixes the measure, the other the measured.
- Correction: either register the gate in the SKILL.md gate table with codes 0/1/2/64, so it gives a real operator
  affordance under operability, or relabel C2 as freshness instrumentation. Two claims on one axis is still honest at
  tie 10, because no scalar moves. Scoring them as two distinct axis gains is not.

## Separability and frontier

- C1 cannot make C2 pass: C2 uses frozen/ledger.json, not `pairs.json`. Confirmed by code (c2_count copies only
  `frozen/*` and the gate). But C2's tamper resistance and C1's carry both depend on the same unenforced condition:
  "r26/r27 frozen files unchanged at candidate" (F2/F5). One judge-side diff check covers both.
- Lowest axis: SCORECARD shows operability 10 and freshness 10, and the contract states no scalar increment. The frontier
  fit is therefore about debt, not scalars. C1 addresses real freshness debt (16 undecided pairs, 6 substantive). C2
  addresses a real fail-open (r26 measure exit 0, `c2-before.json` gate_absent 16/0). Neither claim harms the other
  axis. Moves to keep: F1/F2/F5 judge preconditions and the F7 split disclosure. They harm no axis and only shrink
  false-provenance surface.

## Disagreements requiring parent decision (not decided here)

1. Should C1 PASS with self-referencing artifact rows? My position: no for the six grouped pairs, which must be
   `kind=source`. For metadata rows, PASS only if the evidence is an external artifact.
2. Should the 41 carried pairs count as "HOLD/STALE adjudicated"? My position: disclose as review-existence-carried and
   name S001×ghp-served-set and S033×static-canonical-preflight.
3. Should C2 count as operability without registration? My position: register it, or relabel it as freshness
   instrumentation.

No discovered citing pair is added by this seat. The regex forms I checked (literal, hyphen, en-dash and "to" ranges)
found no knowledge-file form outside the frozen regexes.
