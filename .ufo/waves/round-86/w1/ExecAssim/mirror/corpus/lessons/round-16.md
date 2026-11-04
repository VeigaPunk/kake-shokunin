# Round 16 lesson — a frozen sample cannot see the classes it never sampled

Context: `LOG.md` round 16; evidence `/tmp/kake-r16/` (12 L2 artifacts),
`scripts/freshness-sweep.mjs`, `corpus/knowledge/freshness-sweep.md`,
`corpus/knowledge/freshness-pins.json`.

## What happened

r10 measured "60/60 paths resolve" and froze it as a standing claim; r15 had
to retire it by measurement (49/58, 5 genuine danglers). Adding more path
coverage did not help that failure mode, because the failure mode was the
*frozen sample*: a claim verified once, cited forever, with no re-derivation
path a non-author can run.

r16 tested the opposite approach — **enumerate every quantified standing claim
and give each one a live command** (160 claims: counts, byte sizes, shas,
ETags, dates, marker literals, exit predicates, code-line pins, verb outcomes,
journal structure). Result: **117 HOLDS / 15 STALE / 7 UNVERIFIABLE /
21 HISTORICAL-OK**. Ten of the 15 stale rows sit in classes no earlier round
had a method to see:

- **verb-outcome literals** — `free-read-verbs.md` recorded `sync-check`'s bare
  9-row sample as `{ok:3, attention:[…6 ids…]}` and `reconcile`'s fleet sweep as
  "7 attention ids / 6 DIFF + 1 ERR". The world moved (`plazir27runs-on` flipped
  to `in-sync`), so the samples now read `{ok:4, attention:[…5…]}` and
  "6 ids / 5 DIFF + 1 ERR". Both exits still `1` — an exit-code-only re-check
  would have called this "unchanged".
- **journal structure** — `fire-journal-codes.md` listed `newVersion`,
  `preview`, `operatorNext`, `liveAfter` as journal *top-level* keys. Measured
  over all 28 journals, the union is exactly `site, mode, startedAt, steps[],
  fire, error`. The claim was wrong when written; no path sweep could see it.
- **fire counts** — `recreate plazir15 ×2 fired` was an undercount: three
  journals carry `fire:true` (codes 7, 4, 6). Meter accounting is
  operator-facing, so the undercount mattered.
- **ETag literal** — one r16 sampler read `6ab49126-1365d` where the file said
  `6ab49127-1365d`; L1's 7/7 same-round re-fetch reproduced the latter.
  r17 then observed `6ab49126-1365d` in 8/8 fetches, confirming the lesson:
  ETags are edge-unstable identifiers, never freeze metrics (the sha is).

## Two rules this round lands

1. **Pin the set, not the count.** A count freeze ("60/60") cannot distinguish
   "all still resolve" from "the base grew and the count was never updated".
   `freshness-sweep.mjs` pins `pathsMissSet` (the *set* of non-resolving
   citations) and reports new misses as drift; a recovered path is
   informational. Same shape for the history shape (set equality, not counts).
2. **A dated sample is not a standing claim.** Attention lists, ok counts and
   verdict tallies from a specific run MUST be labelled with that run's
   timestamp and re-run before being cited (`free-read-verbs.md` r16
   amendment). Counts of a file that grows on a timer (probe-history rows,
   full/spot splits, era families) are floors or dated measurements, never
   constants.

## The in-round domain catch

`plazir15-ghp` is 5 commits ahead of `origin/main`, so live serves the
pre-push tree: live sitemap 8 locs incl. `/tetris/` vs source 7, `snake/`
missing its `og:url`, `speedrun/` canonical not yet repointed to ds4cc.com —
all 8 live locs 200, so stale-not-rot, and invisible to `probe`/`reconcile`
(root `index.html` is not in the lag set). Ledgered as PQ-14; the r7 "103
locs" baseline is now written as "103 live-side / 102 source-side — the delta
IS the gate". r6 had recorded "5 ahead / 5 diffs" in a lesson but the claim in
`drift-detection.md` ("tree byte-identical to live") was never corrected —
a measurement that never reached the claim it contradicted.

## Costs

- `freshness-sweep.mjs` is ~1050 lines for three sections. It is verified
  (`--selftest` 9/9, 9 live run modes, byte-identical state guard, independent
  critic fixture attack incl. an interior-history-tamper counterexample that
  forced the exact-event pins) — but it is the largest artifact in the repo,
  and its printer verbosity is a maintenance cost worth revisiting before
  adding a fourth section.
- L2 verdicts are drafts: the r16 sentinel/reviewer/critic each caught a real
  defect (one self-cite line number, two instrument suppression paths, a stale
  internal-consistency count). L1 adjudicated each before landing.

## Gate

**Label: retrospective round-21 reconstruction, not original admission.** Written
2026-10-20 by round-21 wave 1 (Lesson04) from the recorded artifacts listed below.
No round-16 gate decision was recorded as such at the time; the outcomes here are
reconstructed from the round-16 LOG entry and the knowledge files it cites. Nothing
was re-verified live. Original sections reconstructed: "What happened" (lines 7-38),
"Two rules this round lands" (40-52), "The in-round domain catch" (54-64), "Costs"
(66-76).

Candidates and historically supported outcomes:

- **A. Pin the set, not the count** (rule 1, lines 42-46). Admitted with
  qualification. Implemented as `pathsMissSet` in `scripts/freshness-sweep.mjs`
  (LOG round-16 item 1). Qualification: the round-17 new miss (W6) was handled by
  re-pinning `pathsMissSet` 9→10 (LOG round-17 item 1), showing the pin moves with
  evidence; it does not prove completeness of the sweep.
- **B. A dated sample is not a standing claim** (rule 2, lines 47-52). Admitted with
  qualification. Applied as timestamped "re-read" labels in
  `corpus/knowledge/free-read-verbs.md` (r16 re-reads, around lines 173-176 and
  218) and row-count floors in `corpus/knowledge/ops-automation.md` (line 5).
  Qualification: no mechanical enforcement of this rule is recorded; it is
  corpus convention.
- **C. Enumerate every quantified standing claim with one live command** (lines
  15-21). Admitted with qualification. Recorded measurement: 160 claims, 117 HOLD /
  15 STALE / 7 UNVERIFIABLE / 21 HISTORICAL-OK (LOG round-16 item 2). All 15 stale
  items were fixed or re-pinned in-round. The 7 UNVERIFIABLE claims were not closed
  and were carried into round 17 (LOG round-17 item 2). The lesson's claim that ten
  of the 15 stale rows were in classes no earlier round could see is the lesson's
  own statement; it was not independently recounted here.
- **D. Journal-structure and fire-count corrections** (lines 28-34). Admitted.
  Measured corrections recorded in `corpus/knowledge/fire-journal-codes.md`: the
  top-level key union over 28 journals is `site, mode, startedAt, steps[], fire,
  error`, and `recreate plazir15` fired ×3, not ×2.
- **E. ETag as a freeze metric** (lines 35-38). Rejected as a freeze metric and
  replaced by the rule "ETags are edge-unstable identifiers; the sha is the metric".
  LOG round-16 item 2 records the candidate as refuted on re-measurement (7/7
  fetches matched the file). LOG round-17 item 2 records a later flip back to
  `6ab49126` in 8/8 fetches, supporting the rule.
- **F. In-round domain catch, PQ-14** (lines 54-64). Admitted as ledgered.
  `plazir15-ghp` is recorded as 5 commits ahead of `origin/main`; the claim in
  `corpus/knowledge/drift-detection.md` that the tree was byte-identical to live was
  corrected. Ledger entry: `corpus/knowledge/publish-queue.md` PQ-14. Classified
  stale-not-rot at round-16 measurement; not re-checked for this gate.
- **G. Freshness 9→10 move, instrument plus claim sweep** (lines 74-76 and LOG
  round-16 item 7). Admitted with qualification. The first critic ruling was
  NOT-ELIGIBLE, because the instrument alone is operability (r10 precedent) and two
  suppression paths were proven. After those paths were closed, the critic re-ruled
  MOVE-ELIGIBLE on two branches under a stated predicate. The reviewer verdict was
  `concerns` (one FAIL, the self-cite line number), fixed in-round. Qualification:
  these adjudications are in-round L2 verdicts, not outside review.
- **H. Instrument maintenance cost** (lines 68-73, "Costs"). Unverified. The
  roughly 1050-line size is the lesson's statement; no maintenance-cost measurement
  is recorded. The "revisit before a fourth section" advice is a recommendation, not
  an admitted change.

Rejected candidates (only those documented in the record):

- Exit-code-only re-check as proof that a claim is unchanged. Rejected by the
  round-16 measurement: both exits stayed 1 while counts moved (lines 22-27; LOG
  round-16 item 2).
- The initial critic ruling NOT-ELIGIBLE on the freshness move. Superseded after
  the suppression paths were closed (candidate G).
- Any other rejected candidate: not recorded.

Unverified or deferred (not admitted as fixed):

- The seven UNVERIFIABLE claims from candidate C.
- The reviewer's three low residue items, recorded as pre-r15 conventions and not
  fixed (LOG round-16 item 7).
- The instrument maintenance-cost question in candidate H.

Outside spot-check: not recorded. No non-author verifier's admit or reject sample for
round 16 exists in the repository. `corpus/lessons/round-20-verifier-spotcheck.md`
covers round 20 only. The in-round critic and reviewer verdicts (candidates G and
the reviewer item) and the round-17 re-sweep (LOG round-17 items 2 and 6) are cited
above as existing evidence, but they are in-lane or later-round author-side checks,
not outside spot-checks.

Evidence basis (historical, read in round 21, nothing run):

- `LOG.md` round-16 entry (lines 208-309) and round-17 entry (lines 311-398).
- `corpus/knowledge/freshness-sweep.md` ("Why it exists (r16)", line 30; "r16 run",
  line 78).
- `corpus/knowledge/publish-queue.md` PQ-14 (line 34) and
  `corpus/knowledge/drift-detection.md` (line 42, r16 proof at line 67).
- Raw evidence directory `/tmp/kake-r16/` is named throughout LOG round 16 but was
  absent when this gate was written. Its raw files were not re-read; the counts above
  rest on the LOG and runbook text.

Metadata contract and round-21 link: wave spec entry `Lesson04` in
`.ufo/waves/round-21/wave1-spec.json` names "S019" as the metadata and gate corpus
contract, with `CORPUS.md` as its registration point. Neither an S019 identifier nor
`corpus/CORPUS.md` was found in the repository when this gate was written, so S019
is cited by name only, not as a verified source. The round-21 lesson
(`corpus/lessons/round-21.md`) did not exist at that time and is not cited for content.
Verified-at for this gate: round-16 LOG date 2026-09-29, historical-not-live-reverified.

Recheck, not run: `node scripts/freshness-sweep.mjs --offline` (the offline mode the
round-16 LOG names; read-only there). If `/tmp/kake-r16/` is still absent, the
operator must either restore that directory from backup or retire the round-16
citations to it. This is an operator decision, not a lesson edit.