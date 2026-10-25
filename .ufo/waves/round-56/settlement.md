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

Wave 2 (falsify, v1 policy): 41 seats dispatched against lane tip `a450e43e696d`; 41 committed reports in `w2/`
(`ls .ufo/waves/round-56/w2/*.md | wc -l`), 0 dead or misdirected seats. Roles: executor 20, critic 7, reviewer 5, mutation-tester 3,
scout 2, sentinel 1, connector 1, revenger 1, simplifier 1. Wave 2 was written to the orchestrator after wave 1 settled
(all 43 seats), so no wave was handed off while a seat was unsettled. Findings acted on: 3 entries re-cut (modal on the deleted-URL
title and outcome, a false negative about the page's own robots meta tag, "third surface" miscount, のほかに gloss, S420 condition/verb,
sweeps with commands), S419 row hedge, PROVINCE check-vs-set wording, lesson counts, C1 counter 2.1 (command ambiguity, exact pin per row,
fixture trees), C2 selftest 67 -> 86 (19 dual-edit fixtures from `MutC2Selftest`), QUALITY falsifier lines, two stale SKILL.md statements outside C1.
Not acted on (disclosed): `used-by` cells of five reused held rows are not extended (extending them breaks C8 append-only; the
cross-citations are not mirrored); the C1 counter and C2 selftests execute revision-controlled code with the caller's HOME and network
(`SentinelRound` S2) and a self-serving revision can still add modules or fixtures outside the pinned directories (S3); seven C2 mutants
are structurally masked by the fixture builder (`MutC2Selftest`); the C2 counter certifies quote truth, not support (`CriticJunkC2v2`:
a 3-file junk tree reaches 8/8); `landed_check.py` suppresses a hash on a line naming a digest algorithm; C1 does not cover the two new
registry rows or other tallies outside the ten (`ExecSkillCells`).
Round total: 84 seats (43 + 41), no residual call. Never replaced a dead seat; there were none.
