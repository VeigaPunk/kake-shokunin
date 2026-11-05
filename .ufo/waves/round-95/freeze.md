# Round 95 — claim freeze (declared before data)

Lane: kake, round 95 (hyaku run 15, attempt 1). Round base (round open):
`fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3` (branch tip at round open, remote
equal). Instruments commit: `43cdd9fc899a2613d8ba7b55edf820825e57b4d1`. This
freeze is committed before any wave seat scores a claim; the counters, 
predicates, kill rules and targets below are final. The routing is
`task.agentModelOverrides` in `~/.omp/agent/config.yml`; no model is named here.

Fresh-start duty (Amendment 27 authorizes kake's resume): the round-94 closure
(`corpus/lessons/round-94-verifier-spotcheck.md`, verdict
`rejected-honest-stop`, both claims unmet as frozen) and the round-94 lesson
`## Mistakes`/`## Routed` were read before declaration; every routed item
R94-1, R94-2, R94-3, R94-4, R94-5, R94-6, R94-7, R94-8, R94-9 plus the closure's
routed items are addressed by C1, C2 or the round's non-claim work below. The
do-nothing controls (a control that skips the claimed work) are part of each
claim's falsification surface and were executed before this freeze: a lane that
changes nothing stays at `mismatches=18 met=false` (C1) and
`hand<66 met=false` (C2), so neither target is reachable without the claimed
work.

## Instruments (frozen; digests at `controls/instrument-sha256.txt`)

- `c95_selfassess.py` — C1 counter (strict self-assessment conformance,
  successor to `c94_selfassess.py`, implementing routed R94-1, R94-2, R94-3,
  R94-7 and the round-94 closure's `--skip-battery` finding). Identity surface
  `frozen/c1-surfaces.json` (content-pinned: per-lesson blob digests, per-entry
  head-8-line digests, criteria headings, SKILL-row first cells with path-token
  counts, exact-`## Mistakes` carriers; no `--surfaces-file` flag exists).
- `c95_conditional.py` — C2 counter (conditional request evaluation, contract
  v2; successor to `c94_conditional.py`, implementing R94-6, R93-10, R94-4 and
  the explicit population-base pin of the round-94 closure item 5 / R94-8).
  Contract: `c2-contract-v2.md`. Population pins: `frozen/c2-population.sha256`.
  Positive control `frozen/pos-good-v2.py`; forgeries: the six round-93 frozen
  `neg-*.py` subjects plus `frozen/neg-refuse-empty-member.py`. Equivalence
  receipts: `frozen/c2-equiv-receipts.json` (empty — see the equivalence check
  below).

## Claim C1 — calibration (score 2, HOLD; lowest owned axis)

**Predicate (one sentence, same in plan, counter and receipt):** at the
measured revision, `c95_selfassess.py` reports `pins=ok`, zero mismatches
(E1=E2=E3=E4=E5=0), `battery=20/20`, `admit=5/5`, `shadow=absent`,
`predecessor_admits>=4`, `self_pin=ok` and `met=true` with exit 0.

- **Target:** mismatches 18 → 0 at the round's landed tip (base control:
  `controls/base-c1.txt`, revision `fdd5fdbe…`: `mismatches=18 E1=0 E2=0
  E3=3 E4=0 E5=15 pins=ok battery=20/20 admit=5/5 shadow=absent
  predecessor_admits=10/19 floor=4 met=false`, exit 1).
- **Counting command (frozen):**
  `python3 -B .ufo/waves/round-95/c95_selfassess.py --root . --revision <REV>`
  (`--work <scratch>` accepted; the battery needs a writable TMPDIR).
- **Kill rule (declared before data):** the claim fails if any counter run at
  the landed tip reports a mismatch, an identity or cardinality pin, a battery
  route admitted, the shadow effect present, a predecessor admission below
  floor 4, or exit != 0. Repairs may only edit the surfaces the counter audits:
  the 13 SKILL.md directory rows (each repaired row names a concrete committed
  non-empty blob path, R94-5, reviewed row-by-row by a non-author wave seat),
  the three dual-`source:`/`/tmp` knowledge entries (each repair an in-file
  correction carrying a `[r95-correction 2026-11-05]` tag per the
  append-guard contract), and the five gate-registry rows R94-9 adds to
  SKILL.md's `### Owned freshness gate registry` (new rows carry resolvable
  counter paths). The round-94 gaming routes are closed by the counter itself:
  de-backticking a repaired row fails the pinned path-token count (R94-3), a
  canned wrapper lacks the true `counter=` digest, `--verdict-only` can never
  print `met=true`, and no `--surfaces-file` flag exists (R18; the selftest
  asserts the CLI refuses it).
- **E1 scope note:** the Gate decision-vocabulary rule (/admit/i and /reject/i
  in the Gate heading or body) applies to lessons of rounds >= 95 only;
  earlier lessons are append-only history the corpus contract forbids
  rewriting, and the counter flags no E1 finding on them (base E1=0).

## Claim C2 — freshness (score 10, HOLD), capability acquisition

**Predicate (one sentence):** at the measured revision, `c95_conditional.py`
reports `candidate=present`, `population=ok` (pins digest and every pinned
fixture digest), `anti_table=ok`, all 66 hand cases decided as declared
(including the two raw duplicate-key refusals), all 120 generated cases decided
as the reference, `forgeries_refused=7/7`, `positive=admitted`,
`mutants=40/40` with no unreceipted survivor, and `met=true` with exit 0.

- **Target:** `scripts/conditional_eval.py` implements contract v2 (clauses
  C1-C5 of `c2-contract-v2.md`) and passes the frozen population at the round's
  landed tip. Base control (`controls/base-c2.txt`, at the instruments commit
  `43cdd9fc…`, where the candidate is still the round-93 v1 tool): `met=false`,
  exit 1, `hand=57/66 generated=79/120 forgeries_refused=7/7 positive=admitted
  mutants=40/40` — the nine hand failures and 41 generated failures are exactly
  the v2 acceptance clauses the v1 tool refuses (empty members first), so the
  target is unreachable without the claimed work.
- **Counting command (frozen):**
  `python3 -B .ufo/waves/round-95/c95_conditional.py --root . --revision <REV>
  --work <scratch>`.
- **Kill rule (declared before data):** the claim fails if any hand or
  generated case disagrees with the reference, any forgery is admitted, the
  positive control is refused, the population drifts (any pinned digest
  mismatch), an anti-table hit is recorded, or a population mutant survives
  without a digest-pinned equivalence receipt in
  `frozen/c2-equiv-receipts.json` (R94-4). The candidate must refuse raw
  duplicate-key inputs through its real stdin path.
- **Equivalence check (R94-4), executed before this freeze:** the 40-mutant
  population was scored against the v2 reference on 2026-11-05
  (`controls/mutant-scan-v2.txt`, `controls/mutant-scan-v2-result.json`):
  40/40 killed, zero survivors, including M11 — the round-94 survivor is
  killed by the v2 empty-member cases, so the kill target is 40/40 and the
  receipts file is empty. The receipts mechanism stays the declared rule for
  any future re-score.
- **Population base (pinned explicitly; round-94 closure item 5 / R94-8):** the
  40 mutants patch the frozen round-93 positive-control bytes
  (`.ufo/waves/round-93/frozen/pos-good.py`), not the scored candidate; the
  population's `base_rev` pointer `191dd0ed…` names an uncommitted worktree
  state absent from the lane and is not used by this counter (erratum drafted
  for the round lesson).

## Score deltas

Both owned axes sit at their legacy ceilings; neither claim claims a numeric
rise: C1 is a bounded evidenced calibration move at HOLD 2 (the score changes
only if the non-author closure re-derives it), C2 is a capability-acquisition
instrument move at HOLD 10 (`conditional_eval.py` contract v2; the Capabilities
table row updates only on a demonstrated run this round).

## Sourced-claim requirement

C2's knowledge entry rests on a source row opened this round: the RFC Editor
errata page for RFC 9110 (new row, drafted by the wave's scout and admitted
only through the round gate). The v2 clauses ground in S478 (empty elements),
S455 (etagc obs-text, re-read this round against the retained body), S034
(JSON duplicate members) and S473/S474 (method filter), all previously opened
rows re-read this round.

## Non-claim round work (inside the 1-3 claim cap)

- R94-9: registry rows for `c93_conditional.py`, `c94_selfassess.py`,
  `c94_conditional.py`, `c95_selfassess.py`, `c95_conditional.py` in SKILL.md's
  `### Owned freshness gate registry` (closure item 1).
- R94-8 erratum + the landed-tip receipts of both counters committed under
  `controls/` at the round's final revision (closure item 2).
- SOURCES census before/after (`controls/census-before.txt` exit 0; after
  receipt lands with the round's integration commit); mistake mining into
  `corpus/lessons/round-95.md`; assimilation: none (the merge/kake package
  still collides on 8 ids — `assimilation/collisions`, re-derived this round);
  considerthese mined only if a proposal fits a frozen claim's surface.
