# Round 56 — seat settlement (L1, from `w1-results.json` and committed reports)

Wave 1 (build + pre-data attacks, v1 policy): 43 seats dispatched, 43 settled in `w1-results.json`, 43 committed seat reports in
`w1/` (`ls .ufo/waves/round-56/w1/*.md | wc -l`), 0 dead or misdirected seats (each report opens with its own seat name and names this
lane's round-56 evidence; checked by reading the first lines and by the fleet-root misroot sweep recorded in the report). Roles:
executor 18, scout 7, critic 6, scribe 5, reviewer 4, connector 2, mutation-tester 1. Planner seat: the L1 (the validator rejects
`planner`; the data walk rode scouts and connectors). `labrat` and `sonic` are not swarm roles under policy v1: the two cheat
experiments and the two inventories ran as critic and executor seats.

Counter attacks acted on before any claim was measured: C1 version 2 (`CriticC1Contract`, `MutC1Counter`, `ReviewerSelftallyCode`,
`CritCheatC1`), C2 version 2 (`CriticC2Contract`, `CriticControls`, `CritCheatC2`); contract amendment `contract.md` §Counter versions.
Not acted on (disclosed): the helper pin stops at the pinned script's directory; C2's quote check cannot verify a quote that contains a
raw double quote; C7 stays a receipt check.

Wave 2: see the wave-2 section below once settled.
