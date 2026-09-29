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
- **ETag literal** — one r16 sampler read `6ab49126-1365d` where the file says
  `6ab49127-1365d`; L1's 7/7 re-fetch reproduced the file's value. Lesson
  recorded instead of a correction: ETags are edge-unstable identifiers, never
  freeze metrics (the sha is).

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