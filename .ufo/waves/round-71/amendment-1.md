# Round 71 — amendment 1 (pre-data; written before any seat was dispatched)

The contract's wave-shape table (commit 04557e17) lists a LabratControls seat and says the attack
seats are reviewer, critic, mutation-tester and labrat (4 of 11). The swarm validator and
`skills/swarm` exclude `labrat` from swarm roles (a frozen-topology seat). This amendment makes
these changes, all before any seat was dispatched:

1. LabratControls -> ExecControls, role `executor`: the junk controls (J1-J3) are run by an
   executor seat in scratch. The J3 result is a named residual probe, not a pass.
2. One added seat, ReviewRepair (role `reviewer`): it attacks the repair rules themselves
   (contract C1 items 1-4, C2 repair rule), not the counters.

Final wave: w1, 13 seats: scout 3 (ScoutCalib, ScoutTmp, ScoutConsider), executor 3
(ExecRepairC1, ExecRepairC2, ExecControls), reviewer 2 (ReviewContract, ReviewRepair), critic 1
(CriticClaims), mutation-tester 1 (MutCounters), connector 1 (ConnOverlap), scribe 1
(ScribeLesson), sentinel 1 (SentinelPaths).
Attack seats (reviewer, critic, mutation-tester): 4 of 13 = 30.8 %, which meets the >=25 % rule.
The C1 counter's STRICT_ROLES still names labrat; no round-70 seat was a labrat, so the round-70
correction value (3/14) is unchanged.

Predicates, counters, controls, repair rules and kill rules are byte-identical to the freeze
commit 04557e17. The contract's '4 of 11' sentence is superseded by the numbers here.
