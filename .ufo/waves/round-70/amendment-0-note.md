# Round 70 — Amendment 0 (pre-dispatch, before any seat ran)

Recorded by the L1 on 2026-11-03, before the W1 `.ready` handoff. Seat-shape only; no claim
predicate, kill rule, control, or frontier term changes.

- The wave validator refused the 13-seat spec with `unknown_role`: `labrat` is a frozen-topology
  probe seat, not a swarm role (orchestrator ruling of 2026-10-19 already keeps the planner off
  the spec for the same reason).
- The census-validator probe therefore rides an **executor** seat (item renamed `ExecCensusProbe`,
  same bounded hypothesis and red/green deliverable).
- A **sentinel** seat (`SentinelAdoption`) joins the attack set: adversarial review of the two
  untrusted intake paths (staged `merge/kake` bytes into the corpus; pointer tokens into the C1
  counter's git calls, which the executor item now pins to list-form subprocess, never
  `shell=True`).
- W1 shape: one v1 wave of **14** seats — 3 scout, 3 executor, 2 scribe, 1 reviewer, 1 critic,
  1 mutation-tester, 1 connector, 1 revenger, 1 sentinel. Attack share 4/14 ≈ 28.6 % (≥25 %);
  1 connector seat. Round total 14; no residual wave planned.
- Routing unchanged (run-15 map; never pass `model`). Validator refusal evidence:
  `{"schema":"ufo-swarm-wave-error-v1","code":"unknown_role","message":"items[10].role \"labrat\"
  is not a swarm role"}` (first `run` attempt, 14:0x -03), fixed before any dispatch.
