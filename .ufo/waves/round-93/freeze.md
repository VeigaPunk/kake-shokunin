# Round 93 freeze — kake (hyaku, attempt 1)

Frozen before any seat ran and before any candidate was scored. Base
`10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5` (lane `master` tip at round open). Everything below is
committed in the same commit as this file; no counter, case, predicate, label or target is changed
after the first seat scores.

## Claims (2, distinct axes, one on the lowest owned non-retired axis)

**C1 — calibration 2 → 2 HOLD (lowest owned non-retired axis): the lane's machine-checkable
self-assessment matches the repo state it describes.**
Before: `mismatches=20 E1=1 E2=8 E3=1 E4=4 E5=6 pins=ok met=false`, exit 1 at the base.
After (target): `mismatches=0 … met=true`, exit 0 at the carrier.
Predicate and population: `.ufo/waves/round-93/c1-predicate.md`.
Counter: `.ufo/waves/round-93/c93_selfassess.py`.
Kill rule: any residual mismatch at the carrier is an honest unmet; the counter is not repaired
after scoring and the target is not narrowed.

**C2 — freshness 10 → 10 HOLD, capability acquisition on open frontier ground: a conditional
request evaluation instrument (contract v1).**
Before: `candidate=absent hand=0/44 generated=0/120 forgeries_refused=0/6 positive=refused … met=false`,
exit 1 at the base.
After (target): `candidate=present hand=44/44 generated=120/120 forgeries_refused=6/6
positive=admitted anti_table=ok population=ok met=true`, exit 0 at the carrier.
Contract: `.ufo/waves/round-93/c2-contract.md`. Counter: `.ufo/waves/round-93/c93_conditional.py`.
Candidate path: `scripts/conditional_eval.py`.
Kill rule: any admitted forgery, any hand/generated disagreement, a refused positive control, an
anti-table hit or a population drift is an honest unmet.

Both claims are causally separable: C1 scores committed prose/registry bytes only; C2 scores a new
tool file and its frozen fixture set only. Neither counter reads the other's surface.

## Controls executed before the freeze (receipts under `controls/`)

| Control | Command | Result |
|---|---|---|
| C1 do-nothing | `c93_selfassess.py --root . --revision <base>` | `mismatches=20 … met=false`, exit 1 (`controls/base-c1.txt`) |
| C1 instrument | `c93_selfassess.py --selftest` | 5/5 planted findings, exit 1 planted / exit 0 repaired (`controls/ctl-c1-selftest.txt`) |
| C2 do-nothing | `c93_conditional.py --root . --revision <base> --work <scratch>` | `candidate=absent … met=false`, exit 1 (`controls/base-c2.txt`) |
| C2 fixtures | `c93_conditional.py --selftest` | 7/7 scored as declared, drifted reference distinguished by 4 cases (`controls/ctl-c2-fixtures.txt`) |

The C2 positive control (`frozen/pos-good.py`) is an independent contract-faithful implementation
and must be **admitted**; the six `frozen/neg-*.py` forgeries must each be **refused**. The forgery
generator (`frozen/build-fixtures.py`) applies exactly one documented defect per forgery to the
positive control, so a refusal is attributable to that defect. Population digests:
`frozen/c2-population.sha256`, its own digest pinned in the counter as `PINS_SHA`.

## Round shape

ONE v1 wave of 12 seats under `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`
(band 8–16 for this run). Attack seats: reviewer ×2, critic ×1, mutation-tester ×1 = 4/12 = 33 %
(≥ 25 %); connector 1 (≤ 2). The L1 holds the canonical planner seat (`planner` is a frozen-topology
role the validator refuses); a bounded data-walk rides the connector and the scouts.

## Sources

The two RFC texts this round grounds C2 on were opened by the L1 with one public GET each and
retained under `L1/src/` (`rfc9110.txt` 502 941 B sha256 `21c1cdce…`, `rfc9111.txt` 84 477 B sha256
`aeb52adb…`; the latter is byte-identical to the round-92 retained body). Row drafting and the
Gate quotes are seat work; the census before this round is `assimilation/census-before.txt`.
