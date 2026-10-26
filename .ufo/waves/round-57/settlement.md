# Round 57 — seat settlement (L1, from `w1-results.json` and committed reports)

Wave 1 (build + pre-data attacks, v1 policy): 40 seats dispatched, 40 settled in `w1-results.json`, 40 committed seat reports in `w1/`
(`ls .ufo/waves/round-57/w1/*.md | wc -l`), 0 dead or misdirected seats (every report's first line is its own seat name and ends in a
`VERDICT:` line: checked with a loop over `w1/*.md`). Roles: executor 12, scout 9, critic 8, scribe 4, reviewer 4, connector 2,
mutation-tester 1. Planner seat: the L1 (the validator rejects `planner`; the data walk rode scouts and connectors).

Counter attacks acted on before any claim was measured: C1 version 2 (`CriticC1Counter`, `CritCheatC1`, `ReviewerPinsCode`, `MutC1Pins`,
`ExecPinsIndependent`), C2 version 2 (`CriticC2Gate`, `CritCheatC2`, `ReviewerGateCode`), C3 version 2 (`CriticC3Counter`, `CritCheatC3`,
`ExecC3Selftest`), contract sizing (`CriticControlsSizing`); contract amendment `contract.md` § Counter versions. Build inputs taken from
the scribes and executors: the two entries (`EntryDeadLinkTypes`, `EntrySpiderModel`, edited by the L1), the id resolver candidate
(`ExecResolverBuild`, 33-check selftest, with `ExecResolverAlt` kept as the differential oracle for wave 2), the receipt errata
(`ExecErrataBuild`), the README/PROVINCE/lesson/QUALITY text (`ScribeGroundMap`, `ScribeLessonMistakes`), the quarantine verdicts
(`ScoutQuarantineA`–`D`).
Not acted on (disclosed): see `contract.md` § Counter versions, "Not acted on".
