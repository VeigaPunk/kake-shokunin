# ConnectClosurePrecedent — kake C1 (wave 1, control wave)

Axes: operability, freshness.

| lane | round | pointer | ruling | applies to kake C1 |
|---|---|---|---|---|
| kake | 22 | `corpus/lessons/round-22-verifier-spotcheck.md` | C1 admitted: 0/32→32/32 re-derived against pinned `cases.json` oracle; counter reconciles rows; controls before data; no axis harm | C1 must reconcile every case against the sealed key and freeze controls before data |
| kake | 34 | `corpus/lessons/round-34-verifier-spotcheck.md` | C1/C2 not admitted: lookup/hollow controls reach 28/28 and 5/5; named non-author reviewer marks operability/freshness `unprovable-but-better`, admission `rejected-honest-stop` | sealed-key score alone is insufficient; add held-out/perturbed inputs and prove controls below target |
| kake | 35 | `corpus/lessons/round-35-verifier-spotcheck.md` | C1 verified (14→24; controls 7/24); C2 not verified (all-false/no-primary-text controls meet target); axis `unprovable-but-better` | C1 must keep target slack closed (22 reachable skipping bullet (c)) and no do-nothing control may reach |
| kake | 36 | `corpus/lessons/round-36-verifier-spotcheck.md` | C1 verified 0→28/28 under counters v1–v3 frozen before data; capability admitted | re-running the sealed key across counter versions is acceptable only if frozen before data |
| kake | 37 | `corpus/lessons/round-37-verifier-spotcheck.md` | C1 not admitted: stdlib shortcut reaches 28/28 sealed; QUALITY (j) forbids reclassifying controls after scores | a control that meets the predicate must trigger counter/target redesign or withdrawal, never relabel |
| kake | 38 | `corpus/lessons/round-38-verifier-spotcheck.md` | C1 withdrawn before build (controls met predicate); C2 not admitted: control-class text written after full-rule tools scored 20/20 | freeze control classes before any tool is scored; do not relabel after data |
| kaidoku | 30 | `corpus/lessons/round-30-verifier-spotcheck.md` | C1 admitted only where independent oracle agrees 16/16 and pre-data controls score 0–1/16 | independent oracle agreement plus pre-data controls is the admission pattern |
| tsukuroi | 31 | `corpus/lessons/round-31-verifier-spotcheck.md` | C1 not verified: work-skipping control meets target; key holder edited a counted row to pass sealed key | never let key holder edit counted rows; target must fail for work-skipping controls |

Findings:
- No fleet precedent admits an exploratory claim merely because a named non-author reviewer marks it `unprovable-but-better`; kake r34/r35/r37/r38 all end `rejected-honest-stop` unless exploratory was declared before data.
- For kake C1, the sealed key must be scored by controls committed before data, and any control reaching the predicate requires counter/target redesign or withdrawal, not relabel.
- kake C1's own prior slack (r35: 22/24 reachable with bullet (c) skipped) means the sealed set must include cases that exercise every contract bullet.

Report: .ufo/waves/round-39/w1a3/ConnectClosurePrecedent.md
path: /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/w1a3/ConnectClosurePrecedent.md