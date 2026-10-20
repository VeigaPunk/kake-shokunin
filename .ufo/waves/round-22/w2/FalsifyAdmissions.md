# FalsifyAdmissions — dead-seat credit, SHONEN authority, independent closure, trends-no-scalar

Scope: C1 evidence at integrated `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`
(base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`). Author-side falsifier; this
report is not an admission. Commands exercised: `git show/diff/log` against the
two revisions, `sha256sum` on the source blob, JSON reads of the committed
receipts and instrument files. No builds/tests; no live-lane edits.

## Verdict per attacked axis

| Axis | Result |
|---|---|
| Dead-seat credit | Defect found — wording, fixable |
| SHONEN authority | No counterexample — clean |
| Independent closure | One weak chronology nit + confirmation of correct boundary |
| Trends, no scalar | Defect found — replay match level is scalar-only (bounded fixable) |

## Finding 1 (dead-seat credit) — `round-22.md:81` implies dead seats produced work

`corpus/lessons/round-22.md:80-81` says of the four dead scribe seats
(`RegistryDraft`, `Knowledge`, `LessonDraft`, `TrendDraft`): "no output or
completion credit and no replacement. **The L1 integrates their reachable prose
work.**" The second sentence contradicts the first: `w1-deaths.json` records
`"credited": false, "replaced": false` and the seats died at provider startup
(429 before output); `ls .ufo/waves/round-22/w1/` confirms none of the four
report files exist. If any prose was integrated, it was L1-authored
backfill of the dead seats' assignments, not *their* reachable work.

- Evidence: `corpus/lessons/round-22.md:80-81`, `.ufo/waves/round-22/w1-deaths.json:2-11`,
  `git show c0fd6d5 --name-only` contains no `w1/{Knowledge,LessonDraft,RegistryDraft,TrendDraft}.md`.
- Impacted axis: operability evidence provenance (false attribution is the
  dead-seat credit this axis attacks).
- Smallest safe correction: reword to e.g. "The L1 authors the four dead
  seats' planned deliverables directly; no seat output exists." No file or
  score change; LOG.md's wording ("remain dead/uncredited… no replacement")
  is already correct and stays.

## Finding 2 (trends no scalar) — `replay.py` `frozen_replay_match` is aggregate-only

`replay.py` verifies all 69 input digests (cases.json, matrix.py,
canonical_audit.py, all fixture bytes, domain snapshot — good provenance), then
sets `matched` on three scalars only: `run.returncode == expected['exit']`,
`actual['accepted'] == expected['accepted']`, `actual['total'] ==
expected['total']` (`replay.py:34`). `frozen/expected.json` carries no
per-case results. `w1/NoCarriedRedRelabel.md:33-36` explicitly requires
"per-case verdicts, not a scalar" — exit AND finding-id set per case — and
warns a 32/32 scalar hides swapped/absent ids. The replay's own `id` is
`frozen_replay_match`, presented as frozen-expectation equality, but it would
pass any run whose aggregate counts coincide while individual case ids or
exits differ.

Mitigation (why this is bounded, not a reject): the 69 digests pin
`cases.json` (the oracle) and `matrix.py` (the per-case comparator), so a
replay pass today still implies per-case agreement through pinned bytes.
- Evidence: `git show c0fd6d5:.ufo/waves/round-22/replay.py` lines 32-38;
  `git show c0fd6d5:.ufo/waves/round-22/frozen/expected.json` keys are only
  `round, base, exit, accepted, total, inputs` (no `results`);
  `replay-integrated.json` shows `inputsVerified: 69`, `expected:
  {exit:0,accepted:32,total:32}`.
- Impacted axis: operability (trend/scalar evidence discipline).
- Smallest safe correction: either (a) word the claim precisely — SKILL.md:411
  already says "verifies input digests before comparing frozen matrix
  expectations"; make "expectations" explicit as *aggregate* exit/accepted/
  total, or (b) add per-case results into `frozen/expected.json` and compare
  them. (a) costs zero re-freeze; (b) is stronger but changes a pinned file.

## Finding 3 (independent closure) — correct boundary held; one forward-dated LOG line

The integration correctly does not self-admit: `round-22.md:28-29` — "Independent
admission and admit/reject spot-check belong to the orchestrator's non-author
closure, never this L1 or its seats." SCORECARD.md gains no capabilities row
and no round-22 self-verdict (rows "enter only through a round that
demonstrates the capability running"; absent here — consistent with
author-side status). `.ufo/reports/` still contains only `round-20`; no
non-author round-22 closure artifact exists.

Nit: `LOG.md:757-758` states in committed text that "Final measurement and
falsification receipts are recorded in the appended round22 measured entry."
At `c0fd6d5` commit time no w2 falsification receipts existed and
`measure-after.json` was not committed (it is still untracked). The receipts
do exist now in-tree (`measure-before.json` committed; `measure-after.json`
working-tree, two deterministic identical runs). Fixable by wording
("recorded under `.ufo/waves/round-22/measure-*.json` and w2 reports") at the
next admissible doc touch; not a reject.

## SHONEN authority — no counterexample

- `git diff base c0fd6d5 -- SHONEN.md` is empty; contract debts line "no
  SHONEN promotion" honored.
- `corpus/QUALITY.md` r22 addition asserts the *restriction* ("SHONEN marks do
  not advance from a local fixture/corpus repair… no promotion is claimed"),
  not a promotion. TrendDraft's own mandate ("all SHONEN boxes unchanged
  author only") is honored by the boxes being unchanged, not by TrendDraft.
- `SCORECARD.md` contains zero new `[x]`/trend lines for round 22.

## Trends no scalar — direction checks pass elsewhere

- `measure-after.json`: two runs, `stdout` byte-identical, `accepted:32` —
  determinism, not trend.
- `cases.json`: 32/32 names, exact contract order, per-case `expectedExit` +
  `expectedFindings` + `Local publisher policy:` rationale — matches
  `NoCarriedRedRelabel`'s non-scalar bar for the matrix itself.
- `matrix.py:262-267`: acceptance requires exit AND findings equality per
  case; `measure.py` embeds the frozen 32-name tuple and rejects
  missing/extra/duplicate ids.
- `capability-not-freshness` bound kept: `round-22.md:16` "No numeric score
  increase is claimed"; no freshness axis credit anywhere in the r22 diff.
- Domain positive control: `provenance.json` `expectedCanonical` sourced from
  base `SKILL.md:18` property-map row (verified: `https://veigapunk.github.io/
  charter-ufo-fsd/` is the declared canonical), not harvested from the tag;
  archived blob sha256 `43d321f9…` re-verified against source repo
  `ufo-fsd-alpha@31c465f1:docs/charter-ufo-fsd/index.html` — matches, tag at
  line 8.

## Required corrections

1. Reword `round-22.md:81` (dead seats authored nothing; L1 backfilled).
2. Declare replay's match level scalar in SKILL.md:411 wording, or extend
   `frozen/expected.json` with per-case results.
3. Optional nit: `LOG.md:757-758` forward-dates w2 receipts; point at receipt
   file paths instead.

No correction defeats the capability claim; all are documentation-precision
fixes within author-side scope for L1/closure to adjudicate.
