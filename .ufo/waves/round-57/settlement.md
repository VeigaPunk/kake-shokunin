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

Wave 2 (falsify, v1 policy): 37 seats dispatched against lane tip `4b8c730`, 37 settled in `w2-results.json`, 37 committed reports in `w2/` (`ls .ufo/waves/round-57/w2/*.md | wc -l`),
0 dead seats; one report (`MutC3Counter`) opens with the header `# MutC3Counter-3` (the seat's own variant of its name; content is this round's C3 mutation test). Roles: executor 10,
critic 7, reviewer 6, scout 6, mutation-tester 3, connector 2, sentinel 1, revenger 1, simplifier 1. Round total: 77 seats (40 + 37), no residual call. Never replaced a dead seat; none.
Acted on: C1 version 2.1, C2 gate version 2.1, C3 version 2.1, the tool (49 checks), both entries (sentence-level repairs), the lesson (Mistakes, Gate rejects, Trend, census), QUALITY and SKILL text
corrections, contract § Counter versions (after wave 2).
Not acted on (disclosed): `SimplifierBuild` (10 dead spots in 4 files; deletions not applied, no behavior claim rests on them); `SentinelRound` F5 (failure paths can leave `c57-*` temp trees) and the
residual F1 network exposure when bubblewrap is absent; `ExecResolverFleetRuns` shows the resolver is exact for kake's entries and noisy for other lanes' id-shaped tokens (reported, not absorbed);
`CriticAxisWave2`'s point that C1 still requires the C2 and C3 receipts to exist.
