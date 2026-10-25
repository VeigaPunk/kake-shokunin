# CriticShape — wave-shape ruling (kake round 51, wave 1)

Ruling, two answers:

1. **YES** — one v1 build wave of 48 seats **plus one residual call of 0–8 reviewer/critic
   seats** is a conforming instance of the *default* shape, not a third shape and not the v2
   alternative: the default's wave 2 is conditional on the measured count, and the residual
   clause is the default's own named branch when that condition fails. Conditions in §4.
2. **NO** — a second 32-seat wave is **not required** when wave 1 yields fewer than 32 distinct
   attack items. Dispatching one anyway is padding and is forbidden by the same paragraph.

What is **not** yet satisfied: the lesson's declared shape line is a flat, unconditional
"one v1 wave of 48 seats" with no residual call, no round total and no measured count. As
written it is a *forecast* made before wave 1 returned, and it licenses the wrong action in
the ≥32 case (§5, counterexample A) and is not re-derivable in either case (§5, counterexample
B). Smallest safe correction in §8.

## 1. The clause (exact provenance)

The round prompt's wave-shape options are numbered item 2 of the campaign addendum:

- `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:42-62` (the copy spliced into
  the delivered L1 prompt), mirrored verbatim at
  `/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-51.md:182-206` (§6 item 2).
- Note on the citation: `kake-round-51.md` §2 (line 9) is *Claims this round* and §2b (line 42)
  is the *Frontier step*; neither contains wave-shape text. "Section 2" therefore resolves to
  numbered item 2 of the addendum, which is the same bytes in both files. No wave-shape clause
  is being smuggled in from elsewhere.

Verbatim, the load-bearing sentences (`lane-addendum.md:45-61`):

> - **Default — two v1 waves.** **Wave 1 — build (32–64):** recon, source opening, entry
>   drafting, tooling, plus first falsifiers of the round's declared claims. **Wave 2 —
>   falsify (32–64)**, dispatched after wave 1 returns and only when wave 1's output yields
>   ≥32 distinct attack items: [...] Both waves validate under policy v1 [...], band 32–64; the
>   two waves together stay ≤128 seats.
>
>   Residual checks (fewer than 32 attack items for a wave 2, or leftovers after the waves) go
>   into one ordinary `task` call of ≤8 reviewer/critic seats, counted in the round total
>   (≤128); say so in the report. Never pad: if fewer than 32 genuine items exist, the claims
>   are too thin — choose a larger frontier claim instead of adding filler seats.

And the record duty (`lane-addendum.md:75-77`):

> Record the round shape, each wave's seat count, role mix and dead seats, any residual call,
> and the round total in the report.

Session-level restatement, same reading (`/home/vgpnk/Projects/shokunin/.scratch/goal-20261025-hyaku-12h.md:28-32`):

> Default shape stands: wave 1 build (32–64), wave 2 falsify (32–64), round total ≤128;
> residual attacks ≤8 in one task call.

## 2. Why 48 + residual is the *default* shape, not a deviation

- The default's **unconditional** element is wave 1 (32–64). Its wave 2 is introduced with
  "dispatched ... **only when** wave 1's output yields ≥32 distinct attack items". A necessary
  condition on wave 2 is not a requirement that it always run; the residual clause exists
  precisely for "fewer than 32 attack items for a wave 2". A round that runs wave 1 and then
  the residual branch is the default shape instantiated with the wave-2 guard false.
- Arithmetic holds: 48 ∈ [32, 64] (`.ufo/waves/round-51/w51-taskcall.json` policy:
  `waveMinLanes 32`, `waveMaxLanes 64`, `maxLanes 48`); 48 + n, n ≤ 8, is ≤ 56, inside the
  contract's 32–128 and inside operator directive 3's "32-100 swarm round". The wave was
  dispatched as exactly **one** `task` call (`counts.spawn 48`; validator stderr
  `.ufo/waves/round-51/w51-validator.err` is 0 bytes), as the clause requires.
- Precedent in this fleet uses the same words for the same shape: `.ufo/reports/round-46/kumitate.md:107`
  ("Default: one v1 wave `build` of 38 seats, plus one residual call of 8 seats. Wave 1
  yielded fewer than 32 distinct attack items, so there was no wave 2. The round total is 46."),
  `.ufo/reports/round-40/kake.md:131`, `.ufo/reports/round-29/tameshi.md:47`,
  `.ufo/reports/round-32/kaidoku.md:141`.
- The residual call is **not a wave**: the clause calls it "one ordinary `task` call", so it is
  not validated under policy v1 and its ≤8 seats do not have to meet the 32–64 band. Trying to
  validate it as a wave would fail `too_few_lanes` and would be a category error. Keep its
  roles literally to reviewer/critic; a mutation-tester in the residual (e.g.
  `.ufo/reports/round-57/kotodama.md:56`) is outside this clause's role list.

## 3. Why no second 32-seat wave below 32 attack items

- "only when wave 1's output yields ≥32 distinct attack items" makes ≥32 necessary. Below 32,
  wave 2 is outside the default; the residual call is the prescribed outlet.
- "Never pad: if fewer than 32 genuine items exist, the claims are too thin — choose a larger
  frontier claim instead of adding filler seats." A 32-seat wave constructed from <32 genuine
  attack items is filler by definition.
- The anti-padding sentence targets **item supply**, not wave shaping: wave 1 carries 48 named,
  distinct items (`w51-spec.json` items, roles reviewer 10, critic 10, executor 9, scout 6,
  mutation-tester 5, scribe 4, connector/sentinel/revenger/simplifier 1 each). That is not "fewer
  than 32 genuine items"; 25 of the 48 seats are attack roles. The round is not claim-thin, so
  the residual branch, not a padded wave, is the correct response to a <32 wave-2 attack count.
- If ≥32 distinct attack items *do* emerge, the default's wave 2 (32–64) is the defined step and
  cannot be replaced by the ≤8-seat residual: 8 seats cannot absorb ≥32 items. Skipping it would
  be a named deviation (freeze, capacity refusal), reported as such — not a shape choice.

## 4. What the 48 + residual shape must satisfy

1. Wave 1 is 48 seats in one `task` call under policy v1 (met: `counts.spawn 48`, 0-byte
   validator stderr, `wave-grant.txt` `seats=48`).
2. Wave 2 is omitted **because the measured distinct-attack-item count is <32**, and that count
   is recorded — not asserted (§5B).
3. The residual call is ≤8 reviewer/critic seats, counted in the round total, and named in the
   report; n = 0 must be stated as "no residual call" rather than left implicit.
4. Round total = 48 + n ≤ 56, recorded; planner L1 is not a swarm seat and is not counted in it.

## 5. Counterexamples against the lesson's declared shape as committed

`corpus/lessons/round-51.md:4-5` (committed at `5591557`, ancestor of tip `9d13768`) says:

> Round shape: one v1 wave of 48 seats under `scripts/hyaku/ufo-wave-policy.json` (band 32-64).

It carries no condition, no residual, no round total, and no count. At 06:38Z there is no
`settlement.json`, no `wave-timing.json`, no `round-time-accounting.json`, and 28 of 48 seat
reports exist, so wave 1 has not returned; the line is a forecast recorded as a conclusion.

**A. The ≥32 case — the flat line licenses skipping the default's wave 2.** Wave 1 already
enumerates the falsify targets the clause names: two counting commands, two new source rows,
two claims, two entries plus the ledger and two counters (tools), the three ledger checks
(gates), the two retained bodies, the mirror receipt. If the measured list reaches ≥32 distinct
items, the default requires the 32–64 falsify wave; the flat declaration instead pre-commits to
"one wave" and the residual cap of 8 cannot cover the items. A reader then cannot tell whether
wave 2 was omitted because the guard was false (conforming) or because the shape was frozen
in advance (a deviation hidden as a declaration). This is false provenance on the operability
axis.

**B. The guard is uncounted, so the shape decision is not re-derivable.** The clause names five
classes of attack item ("re-run each counting command, re-open each new source row, attack each
claim, review each new entry or tool, mutation-test each new gate") but no granularity and no
counting command. At artifact granularity the visible wave-1 outputs are roughly 15–20 items
(2 counters, 2 entries, 2 rows, 1 lesson, settlement/timing/accounting/route-map/receipts/spec,
2 retained bodies + receipts + mirror); at property granularity the same outputs exceed 40
(3 ledger checks, 8 C2 conditions, 2 rows × 11 cells, 2 Gate quotes, 2 sha256, mirror, ancestor).
[INFERENCE] Both counts are plausible; the two readings give opposite rulings on whether wave 2
is required. A shape decision that flips on an undefined term is not evidence, and it fails the
standard the round's own C1 sets: seat accounting re-derived from committed bytes. "fewer than
32 distinct attack items" in prose is exactly the class of claim C1 replaced with a counter.

**C. Sequencing (latent, not yet violated).** C1's L1/L3 conditions read `settlement.json`,
`wave-timing.json`, `round-time-accounting.json` and the route receipts, which
`build_wave_evidence.py:7-10,88-119` writes **after** the wave settles. A residual call that
attacks those bytes must be dispatched only after they are committed; dispatched earlier, its
seats attack absent files and cannot attack anything. The clause's "after wave 1 returns" is
necessary, not sufficient.

## 6. Measured state (read-only, at 2026-10-25T06:38Z)

| Fact | Value | Evidence |
|---|---|---|
| wave | kake-r51-w1, 48 spawn, one `task` call | `.ufo/waves/round-51/w51-taskcall.json` `counts.spawn 48`; `.ufo/waves/round-51/w1/swarm-registry.json` |
| policy band | 32–64; maxLanes 48; hard ceiling 256 | `w51-taskcall.json` policy block |
| validator | stderr 0 bytes | `.ufo/waves/round-51/w51-validator.err` |
| grant | `seats=48 live=66 pending=0 cap=256` | `.ufo/waves/round-51/wave-grant.txt` |
| roles | reviewer 10, critic 10, executor 9, scout 6, mutation-tester 5, scribe 4, connector 1, sentinel 1, revenger 1, simplifier 1 | `w51-spec.json` items |
| attack seats in wave 1 | 25 of 48 (reviewer+critic+mutation-tester) | same |
| wave 1 returned? | no: 28/48 reports, no `settlement.json` | `ls .ufo/waves/round-51/w1/*.md`; `.ufo/waves/round-51/` listing |
| lesson shape line | committed, flat, pre-return | `git log -- corpus/lessons/round-51.md` → `5591557`; `git show 9d13768:corpus/lessons/round-51.md:4` |
| fleet report | absent | `ls .ufo/reports/round-51/` → kotoba, kotodama, kumitate only |

No tool was installed or upgraded for this review; only `read`/`grep`/`git`/`ls`/`python3 -c`
read-only commands ran.

## 7. Impacted axes

- **operability (primary).** Round-shape accounting is part of what a reader must re-derive. A
  flat shape line plus an uncounted "distinct attack items" guard makes the wave-2 decision
  prose, not evidence, and it pre-empts the record before the wave returns. C1's own standard is
  the counterexample: the ledger re-derives seat counts, route deviations and time, but not the
  shape decision that determined those seats.
- **freshness (secondary).** C2 (S262/S263) is the frozen claim the skipped wave would have
  attacked. If the residual carries the attack, its coverage of the eight C2 conditions and the
  two entries must be named; if ≥32 items exist and the residual alone runs, the freshness claim
  is under-attacked by construction and that must be reported, not smoothed over.

## 8. Smallest safe correction

Replace the lesson's shape line with the conditional form, and use the same sentence in the
fleet report's shape accounting, **after** the settlement exists and the attack-item list has
been counted:

> Round shape: default two-v1-wave shape. Wave 1 built and dispatched 48 seats under policy v1
> (band 32–64, one `task` call, validator stderr empty). Wave 2 falsify (32–64) is dispatched
> iff the measured distinct-attack-item list has ≥32 entries; otherwise one residual `task`
> call of ≤8 reviewer/critic seats attacks the named leftovers, dispatched only after the C1
> wave evidence is committed. Round total 48 + n (n = residual seats; n = 0 stated as "no
> residual call").

Plus, in the report or a committed file: the counting rule, the enumerated attack-item list (or
its length with a re-runnable count command), the residual role mix, the round total, and the
wave-1 dead seats. If wave 2 is skipped for a reason other than a <32 count (freeze, capacity
refusal), say so and call it a deviation.

Until the settlement exists, the lesson's line should be read as the pre-measure plan, not the
round's shape verdict; leaving it flat and unamended after the wave returns is the defect this
review flags.

Scoped to the wave-shape decision; I did not audit the counters, entries or the C1/C2
predicates, and I make no ruling on them.
