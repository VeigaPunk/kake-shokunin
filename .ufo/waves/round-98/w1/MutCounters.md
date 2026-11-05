# MutCounters — mutation-test of the round-98 counters' own batteries (C1 + C2)

Seat: MutCounters (leaf, no subagents). Round: kake 98, hyaku run 15 attempt 1, one v1 wave.
Lane tip at run: `7838981e4e40280176085e8aa1f6827eb7133a69`. Freeze `c3eace8b…`, instruments
`2db76835…`, fleet pin `f8674006…`, base `e51328b6…` — all as tasked.

## Scope and method

Target: the two frozen instruments `.ufo/waves/round-98/c98_captable.py` (C1) and
`c98_stale.py` (C2) — attack their batteries, not the claims; no repair, no lane byte touched
outside my `w1/MutCounters/` files.

1. Digest check first: `sha256sum -c controls/instrument-sha256.txt` in the wave dir → all 11
   lines OK (captable `efd59857…`, stale `e0331e56…`).
2. Pristine copies hashed equal, then 13 captable + 19 stale single-point mutants, each an
   asserted-exactly-once textual substitution on a predicate-bearing line (cut list, prefix
   floor, first/last int, word floor, existence quantifier, containment scope, matching
   algorithm, round cap, admitted filter, met threshold; parse_cc first-occurrence/empty-name,
   delta quoted/clamp, prohibition terms, shared gate, rule order, swr/sie boundaries, sie
   precedence, error range, unknown-key refusal, judge key-set/type/stderr/rc, seed cut).
3. Battery (same bounded detector for pristine and every mutant):
   - captable: `--selftest`; base-c1 and instr-c1 against the lane; the three forgery
     fixtures (namesonly / mega / junkprose) rebuilt in my own scratch clone exactly per
     `controls.sh` (clone `--shared`, `checkout -f --detach 2db76835…`, toplevel asserted,
     identity via `-c` only, builders verbatim, `gen_cap_rows` import as in the committed
     script). Expected lines are the committed receipts' line-1 prefixes + exit codes
     (46/85/45/0 mismatches, exits 1/1/1/1/0); pristine reproduced all five exactly.
   - stale: `--selftest`; base-c2/instr-c2 (absent); the seven slot subjects (pos-oracle +
     six negations) on reproduced fixture commits. `hand=` counts, `met`, and exit are
     seed-independent and must equal the committed receipts (60/60, 14/60, 60/60, 52/60,
     56/60, 57/60, 56/60); `generated=/refusals=/seed=` depend on the fixture commit hash,
     so they are compared against the pristine run on the SAME fixture revision, plus a
     doc-contract check that the printed default seed equals `int(sha256(<rev>)[:8],16)`.
   - Pristine baseline passed every check before any mutant ran (inconclusive otherwise).
4. Survivor follow-ups: each survivor got an executed killing fixture/recipe, or equivalence
   evidence (details in `survivors.md`, raw in `survivor-recipes.json`).

## Result

**captable 7/13 killed, stale 12/19 killed** (32 mutants, none inconclusive; pristine
baseline green). Full table: `mutants.tsv`.

| killed by | captable | stale |
|---|---|---|
| selftest (oracle vs hand) | M02 M03 M08 M11 M12 | S01 S03 S05 S06 S08 S09 S15 S16 S18 S19 |
| committed control line/exit | M03 M05 M07 M12 | — |
| pos-oracle slot (mutant oracle vs correct candidate, generated space) | — | S05 S06 S07 S15 S16 S19 |
| neg-lookup count drift (same fixture rev vs pristine) | — | S01 S06 S08 S14 S15 S16 S19 |
| seed-doc derivation check | — | S14 |

Survivors and their executed killing recipes (one line each; full detail in `survivors.md`):

- M01 cut list `"; "` — row "sources-registry; gate flavor": pristine 45 / mutant 47 mismatches.
- M04 first-vs-last int — round cell "20 (recount 21)": 45 / 47.
- M06 word floor band 4–7 words — 5-word row: 47 / 45.
- M09 containment line→evidence-cell — r88 row with script path only in the what-cell: 45 / 47.
- M10 greedy matcher — **equivalent-mutant suspect**: 200000 random bipartite cases under the
  ≥3-word-prefix compat relation produced 0 greedy≠max counterexamples; no reachable fixture.
- M13 met threshold `<=1` — junkprose fixture minus one row (`mismatches=1`): pristine exit 1
  met=false / mutant exit 0 met=true.
- S02 empty directive name — `response_cc "a=1, =2"`: pristine REFUSE / mutant decided; the
  correct candidate refuses, so a hand case would kill.
- S04 clamp dropped — `L=0, A=3e9, swr=99999999999`: pristine/candidate revalidate, mutant
  serve-stale-revalidate (no battery case ever exceeds staleness 2^31: hand A≤1800, generator
  A≤~3700).
- S10 judge key-set — **equivalent mutant**: dict equality already rejects extra keys, so the
  single-point loosening is dead code; a second single-point variant S10b (line 2 loosened to
  `all(o.get(k)==v)`) also survived (line-1 guard still rejects). Accepting extra keys needs
  both judge guards changed — not a single-point defect.
- S11 staleness float — recipe candidate emitting `15.0`: pristine met=false / mutant met=true.
- S12 refusal stderr — recipe candidate writing `rejected: …`: pristine met=false / mutant met=true.
- S13 refusal exit code — recipe candidate exiting 2: pristine met=false / mutant met=true.
- S17 error range 100–199 — `error=150`: pristine/candidate not-an-error, mutant REFUSE.

## Coverage findings for the L1 (routes, not repairs)

1. The stale judge's output contract is unguarded against candidates that violate it in ways
   frozen subjects never do: float `staleness` (S11), foreign refusal stderr (S12), refusal
   exit ≠1 (S13). One violating subject in the slot set would close all three.
2. The stale generator's reachable space never exercises: empty directive names (S02), error
   statuses 100–199 (S17), staleness > 2^31 (S04). The hand set covers none of these either.
3. S07 shows a blind spot class: rule-order mutants with no dedicated hand case are caught
   only indirectly (pos-oracle slot, generated space) — hand cases for "invalid error class +
   fresh age" would make it structural.
4. Captable: the met threshold has no near-boundary control (nothing lands at mismatches=1,
   M13); the 4–7-word prose band is unpopulated (M06); no battery name cuts at `"; "` (M01);
   no round cell carries a second integer (M04); no row carries the entry's script path
   outside the evidence cell (M09). Two survivors (M10 greedy, S10 judge) are equivalent
   mutants — evidence recorded, not coverage gaps.
5. Declared-limit confirmation: the C1 junk-prose limit and the C2 exclusive-boundary /
   request-sie generated-population limits reproduce exactly as frozen.

## Bound compliance

- Writes: only `w1/MutCounters*` in the lane + `/fast/scratch/hyaku/kake-r98/MutCounters/`
  (scratch deleted after receipt copy; only my own seat dir removed). One live clone, rebuilt
  fixtures only in it, `rev-parse --show-toplevel` asserted before first commit, identity via
  `-c user.name=MutCounters -c user.email=MutCounters@example.invalid` only.
- No mutating git/jj in LANE or the fleet repo; both only read via `/usr/bin/git`
  (`GIT_NO_REPLACE_OBJECTS=1`). No sysctl touched. No pacman; no tools installed
  (python3 + git only). TMPDIR set to my scratch for every counter run.
- Instrument digests verified before attacking; a mismatch would have been reported, none
  found. My seat scratch tree is NOT on disk at yield (deleted, receipts copied first).
- At seat end the lane working tree carried uncommitted modifications to two tracked files,
  `SCORECARD.md` and `corpus/knowledge/revalidation-exchange.md` — sibling executors'
  in-flight round work (C1 repair rows / R98-D1), not this seat's: every lane byte this seat
  touched went through `git show`/`cat-file` object access, and all counter runs with
  fixture writes used the scratch clone only.

## Files

`mutants.tsv` (32 rows), `survivors.md`, `baseline-and-mutant-results.json` (pristine
baseline + per-mutant checks with observed outputs), `survivor-recipes.json` (executed
recipes incl. fixture revisions and candidate-file runs), `battery-driver.py`,
`followup-driver.py` (the exact drivers). Fixture revisions used: c1-namesonly
`362dda9a…`, c1-mega `f486acf6…`, c1-junk `2244cd93…`, c2-pos-oracle `52ebf56f…`,
c2-neg-constant `adc4819e…`, c2-neg-lookup `9f7243da…`, c2-neg-noprohibit `455f3889…`,
c2-neg-exclusive `0834e96d…`, c2-neg-respsie `24cc7b94…`, c2-neg-lenient `ea5993b1…`.

MUT-COUNTERS captable_killed=7/13 stale_killed=12/19
