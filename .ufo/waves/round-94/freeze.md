# Round 94 freeze — kake (hyaku run 15, attempt 1)

Frozen before any wave seat scored and before any repair landed. Base (lane tip at
round open, `master`): `0f7d9bbcdd6a9ed36f5bc62b2116ddd040e871a8`. Round 93 landed at
`75effe7b` (report), then lane tip `0f7d9bbc`. Every counter, predicate, target and kill
rule below is final for this round; a rule changed after any seat has scored is not the
claim's rule.

Instrument digests (`controls/instrument-sha256.txt`):
- `c94_selfassess.py` 58028584f1aab19a294d24147854f56a703b2442f5af2d32fed69a5a87a8306a
- `c94_conditional.py` 357d8cd1c2dd04f609518e785616c4f9e54e348b954266a137078dd1ed2a750a
- `frozen/c1-surfaces.json` b911321d780c2c6815eb2d235c10626812491f21a0fd00f6a1e7b7a6cd6e4e6e

## Claims (2, distinct axes; C1 on the lowest owned non-retired axis)

**C1 — calibration (score 2, HOLD): the lane's machine-checkable self-assessment matches the
repo state it describes, under the strict successor counter.**
Predicate (one sentence, the same in the plan, the counter's `met` and this receipt label):
`met <=> pins ok (identity + cardinality) AND zero mismatches across classes E1–E5 AND battery
refused 8/8 AND the frozen round-93 counter admits at least 2 of its 7 fixture routes`.
Counting command: `python3 -B .ufo/waves/round-94/c94_selfassess.py --root <lane> --revision <REV>`.
Before (do-nothing control = the base, `controls/base-c1.txt`): `mismatches=15 E1=0 E2=0
E3=0 E4=0 E5=15 pins=ok battery=8/8 predecessor_admits=7/7 met=false`, exit 1.
Target: `mismatches=0 … met=true`, exit 0 at a committed revision. The 15 base findings are
all E5 "names a tree, not a blob" (directory references in SKILL.md table rows). A repair must
name a concrete non-empty blob the row's entry actually describes, keep the row (identity pins
refuse deletion), and not annotate a present path as absent.
Kill rule: any residual mismatch, any identity or cardinality shortfall, any battery route
admitted by this counter, or fewer than 2 predecessor admissions is an honest unmet. Score stays 2
unless the verdict says otherwise; the counter is not repaired after scoring and the target is
not narrowed.

**C2 — freshness (score 10, HOLD), instrument capability: the conditional-request counter's
frozen population kills the nine mutant classes the round-93 population let survive.**
Counting command: `python3 -B .ufo/waves/round-94/c94_conditional.py --root <clone> --revision
<mutant> --work <scratch>` over the 40 single-clause mutants of `scripts/conditional_eval.py`
(patch list: `.ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json`,
re-used unchanged), scored by the v1 counter (`.ufo/waves/round-93/c93_conditional.py`) and by
the v2 counter. The candidate is not changed by this claim.
Before (v1, do-nothing control, measured on this host): `killed=31/40`; surviving classes M11,
M18, M19, M24, M28, M29, M32, M37, M40 (round-93 receipts; re-measured in this round).
After (v2): target `killed=40/40`. v2 = v1 hand cases (44) + nine new hand cases, one per
surviving class; population digests and forgery subjects unchanged.
Kill rule: any mutant that v2 admits (survives) is an honest unmet count; the target is not
narrowed. The base candidate scores `met=true` under both counters (`controls/base-c2-v1.txt`,
`controls/base-c2-v2.txt`): the claim is about instrument sensitivity, not candidate correctness.

Both claims are causally separable: C1 reads committed prose and SKILL bytes only; C2 reads
`scripts/conditional_eval.py` mutants and the frozen counter files only.

## Out of scope this round (routed, not claimed)

- R93-8 (positive control refuses a legal quoted-comma opaque-tag; non-UTF-8 stdin): needs a
  reference/contract change = contract v2; not claimed.
- R93-9, R93-10 (contract v2 decisions), R93-11 (`__future__` allowlist): not claimed.
- R93-1..R93-6 are addressed in the C1 successor by construction (see the counter docstring),
  and each is a battery route or an identity pin. R93-6 predicate-level vacuity is decided here as
  "vacuous Gate and vacuous source line are findings".

## Controls executed before the freeze (receipts under `controls/`)

| Control | Command | Result |
|---|---|---|
| C1 do-nothing | `c94_selfassess.py --root . --revision 0f7d9bbc…` | mismatches=15 (E5=15), battery 8/8, predecessor 7/7, met=false, exit 1 (`controls/base-c1.txt`) |
| C1 instrument | `c94_selfassess.py --selftest` | 9/9 planted, exit 1 planted / exit 0 repaired (`controls/ctl-c1-selftest.txt`) |
| C2 v1 do-nothing | `c93_conditional.py --revision 0f7d9bbc…` | candidate present, hand 44/44, met=true (`controls/base-c2-v1.txt`) |
| C2 v2 base | `c94_conditional.py --revision 0f7d9bbc…` | hand 53/53, generated 120/120, met=true (`controls/base-c2-v2.txt`) |
| C2 instrument | `c94_conditional.py --selftest` | 7/7 fixtures as declared, drifted reference 4 cases (`controls/ctl-c2-selftest.txt`) |

Ledger of the strict C1 audit: its surface pins are `frozen/c1-surfaces.json` (lessons 88,
entries 81, criteria 39, SKILL first cells 255, Mistakes carriers 73); an identity loss or a
count shrink is refused whatever the mismatch count.

## Round shape

ONE v1 wave `w1`, 11 seats (band 8–16): planner held by the L1 (validator refuses `planner`);
executors 3 (ExecC1Repair, ExecC2Mutants, ExecSourceRows), scout 1 (ScoutRFC), scribe 1
(ScribeEntry), reviewer 2 (ReviewC1, ReviewC2), critic 1 (CriticClaims), mutation-tester 1
(MutC1), sentinel 1 (SentinelScope), connector 1 (ConnectorScope). Attack seats 5/11 = 45 %
(≥ 25 %); connectors 1 (≤ 2). No wave 2 unless the wave yields ≥ 32 attack items (it will not;
the residual check is the L1's own).

## Sources (frontier step)

The C2 v2 expectations for M37 (method case-sensitivity) and M40 (HTAB around list members)
rest on RFC 9110 §9.1 and §5.6.1 — rows S477 and S478 are new and must be opened this round
(scout receipts, access date recorded in the lesson Gate). Existing RFC 9110 §13 rows S471–S476
are re-opened too, so the claim cites a row opened this round.
