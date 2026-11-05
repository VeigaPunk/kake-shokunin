# MutCounters survivors — kake round 98 (hyaku run 15, attempt 1)

Six c98_captable mutants and seven c98_stale mutants survived the full battery
(selftest + committed controls re-run on reproduced scratch fixtures). Every
survivor below carries an EXECUTED killing recipe (observed outputs recorded),
except M10 and S10 which are evidenced equivalent mutants. Full observations:
`survivor-recipes.json`; per-mutant battery output: `baseline-and-mutant-results.json`.

## c98_captable (6 survivors)

| id | site | why the battery misses it | one-line killing recipe (executed) | observed |
|---|---|---|---|---|
| M01 | `key()` CUTS list | no battery case cuts at `"; "` — all fixtures' names cut at `" ("` or `": "` | append row `| sources-registry; gate flavor | <9-word prose> | `corpus/SOURCES.md` | 20 |` at the instruments rev | pristine `mismatches=45 matched=9`, mutant `mismatches=47 matched=8` |
| M04 | `first_int()` | every battery round cell is a bare integer, so first==last | row round cell `20 (recount 21)` against the round-20 entry | pristine `mismatches=45`, mutant `mismatches=47` (reads 21) |
| M06 | word floor `< 8` loosened to `< 5` | all fixture prose is either ≥8 words (junkprose=8) or ≤3 words (namesonly "can do it"); the 4–7-word band is unpopulated | row with 5-word description vs entry r20 | pristine `mismatches=47`, mutant `mismatches=45` (row admitted) |
| M09 | containment scope `line`→`cells[2]` | in all battery fixtures the entry's named script path also appears in the evidence cell, so line-scan and cell-scan agree | row for the unlisted r88 entry ("Conservative Vary-match reader…scripts/vary_match.py") with the path only in the what-cell and evidence `corpus/SOURCES.md` | pristine `mismatches=45`, mutant `mismatches=47` |
| M10 | `max_match()` augmenting dropped (greedy) | probable EQUIVALENT mutant: under "equal or ≥3-word word-prefix" compatibility, the case greedy needs (E1 compat {R1,R2}, E2 compat {R1} only) appears unreachable | probe: 200000 random bipartite cases over the same relation | greedy == maximum matching in 200000/200000 cases, 0 counterexamples |
| M13 | `line1()` met threshold `==0`→`<=1` | no control lands on exactly one mismatch (base=46, namesonly=85, mega=45, junkprose=0; selftest checks mismatch counts, not `met`) | junkprose control fixture minus one row → `mismatches=1` | pristine `exit=1 met=false`, mutant `exit=0 met=true` |

## c98_stale (7 survivors)

| id | site | why the battery misses it | one-line killing recipe (executed) | observed |
|---|---|---|---|---|
| S02 | `parse_cc()` empty directive name | HAND and the generator never emit an element whose name is empty (`", =5,"` shapes absent) | hand case `response_cc="a=1, =2"` → must REFUSE | pristine `REFUSE`, mutant `{revalidate, 1}`; pos-oracle candidate rc=1 `invalid_input: bad directive name` |
| S04 | `delta()` 2^31 clamp dropped | staleness never exceeds 2^31 anywhere: hand A≤1800, generator A≤~3700; H35's huge window is still ≥ staleness both ways | hand case `swr=99999999999, L=0, A=3000000000` → must be `revalidate` (clamped W=2^31 < 3e9) | pristine `revalidate`, mutant `serve-stale-revalidate`; candidate `revalidate` |
| S10 | `judge()` key-set `==`→`<=` | EQUIVALENT by construction: dict equality on line 2 already rejects extra/missing keys, so the single-point loosening is dead code; second mutant S10b (line 2 → `all(o.get(k)==v)`) also ran: battery killers=[] (line-1 guard still rejects) | accepting a third output key requires loosening BOTH judge guards — not a single-point defect | extrakey candidate: pristine rc=1 met=false, S10b rc=1 met=false |
| S11 | `judge()` staleness type check | all frozen subjects emit int staleness; `15.0 == 15` passes dict equality, so a float-emitting candidate is invisible | recipe candidate: pos-oracle emitting `float(staleness)`; contract says "staleness (integer)" | pristine `met=false rc=1`, mutant `met=true rc=0` (--candidate-file --seed 98) |
| S12 | `judge()` refusal stderr prefix | all frozen refusals write `invalid_input:`; any-nonempty-stderr accepts foreign prefixes | recipe candidate: pos-oracle writing stderr `rejected: …` on refusal | pristine `met=false rc=1`, mutant `met=true rc=0` |
| S13 | `judge()` refusal exit code | all frozen refusals exit 1; `rcode != 0` accepts exit 2 | recipe candidate: pos-oracle exiting 2 on refusal (stderr kept) | pristine `met=false rc=1`, mutant `met=true rc=0` |
| S17 | error range `100..599`→`200..599` | no battery error status lies in 100–199 (hand uses 404/501/429/200/304 + 5xx; generator adds none) | hand case `error=150` (SE, L=600, A=900) → must be `not-an-error` | pristine `not-an-error`, mutant `REFUSE`; candidate `not-an-error` |

## Battery pattern behind the survivors

- The 60 HAND cases kill semantic oracle mutants (S01/S03/S05/S06/S08/S09/S15/S16/S18/S19 via selftest; the pos-oracle slot control additionally catches mutant-oracle vs correct-candidate disagreement in generated space, which is what killed S07 — a rule-order change with no covering hand case).
- The committed forgery controls kill threshold/boundary moves only where a fixture sits exactly on the boundary (M05 died on junkprose's 8-word prose; M06's 4–7-word band is empty and lived).
- The judge/refusal/seed guards (S10–S14) are checked only against frozen subjects that never violate them; only the seed mutant died, and only via count drift on neg-lookup plus the documented-derivation check (`seed=` printed vs `sha256(revision)[:8]`).
- Two survivors are equivalent mutants (M10, S10), not coverage gaps; a strengthening battery should not chase them.
