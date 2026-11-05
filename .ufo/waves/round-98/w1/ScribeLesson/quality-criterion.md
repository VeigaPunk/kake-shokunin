# QUALITY.md criterion — draft for kake round 98 (proposal 2: seat-yield ledger)

Seat: ScribeLesson (scribe, leaf member — no subagent dispatch). Draft only; the L1 integrates.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Round base `e51328b63690c8aaa78c9c8f3b87d8735c0ccbf7`;
instruments `2db768356cd081092c3abc60f76b25487ec4c535`; freeze `c3eace8b5c70453faff872c89d8443753e5d21b6`;
C1 repair `4446ce219b4f0c9f5f4fc81f7f772e3a7f24c95a`; lane tip at this seat's start
`7838981e4e40280176085e8aa1f6827eb7133a69`.

## Proposal picked, and why it is still unimplemented

`considerthese/2026-11-05.md` Part 2, **proposal 2 — "Seat-yield ledger"** (line 27 of that file):

> Count, per round, seats requested vs seats that committed a report (r91: 9/13; r92: 13/14 with an
> empty sentinel; r93: L1 died). A single line "yield 9/13, attack share 28.6 %" in the daily note
> would show whether wave quality or provider failures are the real limiter.

Status of every Part-2 proposal in the lane, checked read-only before choosing:

| proposal | implemented? | evidence |
|---|---|---|
| 1 weekly gap check on reflections | no | the 2026-10-27 → 2026-11-04 gap in `considerthese/` is still unfilled; `ls considerthese/` shows 2026-10-19 … 2026-10-26 then 2026-11-05 |
| **2 seat-yield ledger** | **no** | see below |
| 3 held-out vs frozen divergence | **yes, already** | `corpus/QUALITY.md:1848` §Round 95 → R95-D ("An instrument's frozen `met` line is reported beside an independent held-out replay, and a divergence between the two is flagged, never averaged away"), adopted from `considerthese/2026-11-05.md` Part 2 proposal 3 and cited in `corpus/lessons/round-95-verifier-spotcheck.md:59` |
| 4 open-frontier map from the Planned sections | partial, in-lesson only | frontier items are named inside individual rounds' `### Planned` blocks (e.g. `corpus/lessons/round-96.md`); no running map artifact exists |
| 5 branch triage with diffs | no | no `considerthese/2026-11-05.md` proposal-5 artifact in the lane |
| 6 operator queue freshness | no | the round-50/59 operator-queue items are still operator-side; no lane artifact |

Proposal 3 is the closest match to the seat brief but it is **already implemented** (R95-D), so
re-implementing it would duplicate a criterion. Proposal 2 is the one still-unimplemented proposal
whose surface the lane can measure without operator input, and its own worked examples are already
checkable — which is what this criterion is built to make durable.

**Overlap with the L1's landed criterion.** While this draft was being written the L1 landed
`corpus/lessons/round-98.md:90` with **R98-B**, also for `considerthese/2026-11-05.md` proposal 2:
"Every round report carries one line `seat yield: <settled with report>/<dispatched>, attack
<a>/<n>` derived from the wave results file… Shown able to fail: this round's line reads 12/13
with ReviewCapA producing no file." This draft agrees with R98-B on the proposal and on the
falsifier class, and proposes the same criterion in a fuller form (four sub-clauses, R98-Y1…Y4)
with the populations named. It is written to **extend** R98-B, not to replace it: the L1's
one-line format is kept (R98-Y1), and the additions are the population statement (R98-Y2), the
casualty-reason rule (R98-Y3) and the route-mining rule (R98-Y4). The L1 may adopt the whole
section, the parts of it, or none of it.

## What the proposal points at, and what is missing

The proposal names three rounds by number. Each was re-derived from committed bytes by this seat
(receipt `receipt-seat-yield-two-definitions.txt`):

- **r91: "9/13"** — the committed `.ufo/waves/round-91/w1-spec.json` has 13 requested seats; the
  committed wave holds 9 seat reports (4 seats — `ScoutGround`, `ScoutSources`, `ExecReuseStubs`,
  `ConnectorScope` — left none). **Reproduces exactly.**
- **r92: "13/14 with an empty sentinel"** — 14 requested; 13 reports; `SentinelQuote`'s results row
  carries output but its wave directory is empty. **Reproduces exactly.**
- **r93: "L1 died"** — `.ufo/waves/round-93/w1-results.json` does not exist at all, so r93 has
  **no results file**: requested 13, reports 8 (or 9 counting `ScribeEntry/ScribeEntry.md`, which
  lives inside the seat's own directory rather than at the wave root). **Reproduces exactly**, and
  it shows the count needs a stated rule for what a "report" is.

So the proposal's own arithmetic is right. What is missing is everything the arithmetic depends on:

1. **No artifact.** `.ufo/waves/round-<N>/w1-accounting.json` exists for rounds 81–86 only
   (`ls .ufo/waves/round-*/w1-accounting.json` → 81 82 83 84 85 86). Rounds 87–98 have none, and the
   shape changed four times inside the window it does cover: r81 counts only seats with a non-empty
   output and names an explicit `settled_definition` (`.ufo/waves/round-81/w1-accounting.json:18`),
   r82 adds a byte floor and a `schema` key, r83 calls it `kake-wave-accounting/v2`, r85/r86 drop the
   schema and rename the fields (`settled_nonempty`, `attack_share`). Six rounds, four shapes.
2. **No stated denominator.** The lane's published wave lines mix them: r96's "all 12 settled, no
   dead seats" (`LOG.md:3274`) uses *settled*, r97's "one dead seat (ReviewReval, no report)"
   (`LOG.md:3282`) uses *reports*, and r91's "nine seats reported" (`LOG.md:3156`) uses neither
   term for the denominator. The same word covers three different populations.
3. **No stated role set for the share.** The share is published as a bare fraction: "attack share
   5/12 ≈ 42 %" (fleet `.ufo/reports/round-96/kake.md:73`, lane `LOG.md:3274`). The role set it
   must use is pinned elsewhere — `.ufo/waves/round-81/w1-accounting.json:2` says the sentinel is
   not an attack role — and r96's own spec carries exactly four attack-role seats, so the strict
   figure is 4/12 = 33.3 %. The published 5/12 counts the sentinel. **This is mistake row 4 in
   `mistakes.md`; it is the concrete instance the criterion must be able to catch.**
4. **The daily note is the operator's file.** `git log --format='%an' -- considerthese/` shows the
   lane's `considerthese/` entries are authored by the operator, not by `kake-shokunin`. A lane
   criterion that requires the lane to write into the operator's daily note is a criterion the lane
   cannot satisfy and should not try to; the lane-side artifact is the thing to require.

## Criterion text (proposed for `corpus/QUALITY.md`)

Append as a new section; every earlier criterion stands unchanged, and this section adds nothing
that rewrites filed bytes.

---

## Round 98 — seat-yield is an artifact with a stated population

Grounding: `considerthese/2026-11-05.md` Part 2 proposal 2 ("Seat-yield ledger"), opened this round
(2026-11-05) — "Count, per round, seats requested vs seats that committed a report (r91: 9/13;
r92: 13/14 with an empty sentinel; r93: L1 died). A single line 'yield 9/13, attack share 28.6 %'
in the daily note would show whether wave quality or provider failures are the real limiter."
The proposal's three worked examples were re-derived from committed bytes this round and all three
reproduce (`.ufo/waves/round-91/w1-spec.json` 13 requested / 9 reports;
`.ufo/waves/round-92/w1/` 14 requested / 13 reports with `SentinelQuote` empty;
`.ufo/waves/round-93/` has no `w1-results.json` at all). The proposal's *arithmetic* is right; the
lane has never made its *population* durable.

- **R98-Y1. A round's seat yield is a committed artifact, not a sentence.** Every dispatched wave
  commits `.ufo/waves/round-<N>/w1-accounting.json`, and every round report, LOG wave line and
  lesson that states a seat count states it by pointing at that artifact's path. **Admit:** the
  artifact exists at the measured revision, the report's number re-derives from it, and the artifact
  names its own revision. **Reject:** a seat count or an attack share written only in prose in the
  report, the LOG or the lesson, with no artifact a reader can re-derive it from; and an artifact
  whose shape differs from the previous round's without the change being named.
  **Shown able to fail:** the lane's own published share is wrong by one seat on that rule —
  "attack share 5/12 ≈ 42 %" (fleet `.ufo/reports/round-96/kake.md:73`, lane `LOG.md:3274`) against
  the run-15 attack-role set pinned at `.ufo/waves/round-81/w1-accounting.json:2` ("sentinel is not
  an attack role", round-80 closure R80-4); the round-96 spec carries exactly four attack-role
  seats, so the strict figure is 4/12 = 33.3 % and the fifth seat in the published numerator is
  `SentinelScope`. Round 97 published the strict figure correctly (6/13 = 46 %, fleet
  `.ufo/reports/round-97/kake.md:169`), so round 96 is the outlier this rule catches.

- **R98-Y2. The artifact states its population in words before its numbers.** It names, on its
  face: the **requested** population (the seat names in `w1-spec.json`) and the **settled**
  population (rows in `w1-results.json`), separately; the rule that decides whether a seat counts
  as having produced a report, stated as one of two — *a committed report at the wave root
  `w1/<Seat>.md`*, or *any committed `*.md` under `w1/<Seat>/`* — and which rule this round used;
  the **attack-role set** the share is computed over, quoted from its source; and the revision the
  counts were read at. A wave with no results file says so in the artifact rather than reporting
  zero. **Admit:** each of the four is present and the report's figures re-derive under the stated
  rule. **Reject:** a count without a named population; "settled" used to mean "returned output" in
  one place and "committed a report" in another within the same lane; a share whose role set is not
  quoted; a missing results file silently counted as zero seats.
  **Shown able to fail:** the two definitions of "report" give different answers on the same
  committed bytes — under the wave-root rule rounds 95, 96 and 97 yield 7/12, 9/12 and 10/13, while
  under the seat-directory rule the same waves yield 12/12, 12/12 and 12/13 (receipt
  `receipt-seat-yield-two-definitions.txt`); **the round-98 wave itself is the live instance** —
  under the wave-root rule it reads 6/13 and under the seat-directory rule 12/13, and the L1's own
  R98-B line ("this round's line reads 12/13 with ReviewCapA producing no file") uses the
  seat-directory rule without naming it (receipt `receipt-r98-live-wave-yield.txt`); and rounds 89
  and 90 have every results row's `output` set to `null` by an orchestrator kernel restart while all
  14 and all 13 seat reports are committed, so a "settled = non-empty output" definition reads 0/14
  and 0/13 for two rounds in which every seat reported (receipt `receipt-seat-yield.txt`).

- **R98-Y3. A yield line separates wave quality from provider failure.** The artifact reports the
  yield fraction, the attack share, and the seats that produced no report **with their reason
  class** — refused, dead at spawn, provider error, kernel restart, or empty output — so a reader
  can tell a wave that was cut short by the provider from a wave whose seats chose not to report.
  A seat that reported is never counted as a casualty; a seat whose results row is `null` because
  of a kernel restart is not counted as a casualty either. **Admit:** every seat without a report is
  named with its reason class and a pointer to the bytes that show it. **Reject:** a wave line that
  lists "no dead seats" while three seats left no report; a casualty count that includes a seat
  whose report is committed; and a wave line that reports a share but no yield.
  **Shown able to fail:** rounds 89 and 90 are the instances — `w1-results.json` records every
  output as `null` with the note "orchestrator kernel restarted mid-wave; seat output was delivered
  to the orchestrator session but not retained", yet all 14 and all 13 seat reports are committed;
  a ledger keyed on non-empty output reports those two waves as total failures, and a ledger that
  reported them as total failures would send the reader looking for a provider outage that did not
  happen. The same two rounds are why the lane's own wave lines are not comparable to each other.

- **R98-Y4. A closure route the lane does not mine is recorded as not-mined, and a route the lane
  does mine leaves a rule.** Every defect a closure routes to the lane appears in the next round's
  `## Mistakes` table with its evidence pointer and fix, **or** appears in that table's
  "not mined" list with the reason it was closed in practice instead. **Admit:** both forms are
  present, and the "not mined" rows carry the reason and the practice that replaced the route.
  **Reject:** a routed defect that appears in no lesson and in no not-mined list; and a lane that
  adopts the routed practice without recording why it changed. **Shown able to fail:** the round-94
  closure routed "Landed-tip receipts uncommitted" (`corpus/lessons/round-94-verifier-spotcheck.md:118`
  — the report's "final run at `99a88dea`" outputs have no committed receipt) and the round-95
  closure routed the trend-label vocabulary defect
  (`corpus/lessons/round-95-verifier-spotcheck.md:77`); `grep -rn 'landed-tip\|99a88dea' corpus/lessons/`
  and `grep -rn 'improved-bounded' corpus/lessons/round-9[5-8].md` return no lesson row for either,
  and the rounds that followed did land tip receipts (`controls/after-c1-final.txt` @ `1fca1ad7`,
  `controls/after-c1-successor.txt` @ `1098dccd`, `controls/after-c1.txt` @ `d687cd6a`), so the
  practice changed while the corpus recorded no reason.

**Pointer:** `considerthese/2026-11-05.md` Part 2, **proposal 2** (seat-yield ledger). The other
proposals in that Part are not claimed here: proposal 3 is already implemented as
`corpus/QUALITY.md:1848` (R95-D); proposals 1, 4, 5 and 6 remain open and are not this criterion.

---

### Notes for the L1 (not part of the criterion text)

- The criterion is written so that a **round** can satisfy it without touching the operator's
  `considerthese/` file. The proposal's "daily note" is the operator's; the lane-side artifact is
  the substitutable form, and the numbers the proposal quotes are already reproducible.
- R98-Y2's report-definition rule is stated as two named alternatives rather than one chosen rule,
  because the lane has used both and this round's evidence does not settle which is right. Choosing
  one is a lane decision for the L1, not a measurement this seat can make.
- This criterion adds to `corpus/QUALITY.md`; it rewrites nothing. The filed bytes it quotes
  (fleet `.ufo/reports/round-96/kake.md:73`, lane `LOG.md:3274`, `LOG.md:3264`,
  `corpus/knowledge/revalidation-exchange.md:130`) are evidence, not targets: correcting them belongs
  to the L1 or to the fleet closure.
- No counter, contract, ledger or registry was edited by this seat, and no C1 or C2 verdict is
  asserted here.
