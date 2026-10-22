# Round-30 routed defect 5 — which wave-2 reports are partial

Scout: KakeR31.ScoutR30PartialReports. Read-only. Answer: of the 20 committed
`.ufo/waves/round-30/w2/*.md` reports, **15 are complete (seat returned) and 5 are partial
(seat cancelled)**. 14 of the 34 wave-2 seats left no report at all.

## Counts

| Measure | Value | Source |
|---|---|---|
| Wave-2 seats dispatched | 34 | `round-30/w2/swarm-registry.json` members (34), `w2-dispatch.json` counts.spawn=34, `w2-spec.json` items=34 |
| Committed `.md` reports | 20 | `ls round-30/w2/*.md` |
| Complete (seat returned) | 15 | published result + final assistant message |
| Partial (seat cancelled) | 5 | no published result; transcript ends on a tool call |
| Seats that left no report | 14 | 15+19=34 vs 20 files |
| L1's own count | "15 returned; 19 cancelled" at `history://KakeR30:926` and `.ufo/reports/round-30/kake.md:64` | agrees exactly |

## Method and evidence

Two independent signals per seat, agreeing on all 34:

1. **Published result.** `agent://KakeR30.<seat>` returns the seat's completed output. All 15
   complete seats return non-empty text; all 19 others return an empty `text` field (one line,
   no published output).
2. **Transcript ending.** `history://KakeR30.<seat>:raw` (dict `text` field). Every complete
   seat ends on a final assistant message; every partial seat ends on a tool call with no
   closing message. Final lines were read programmatically, not inferred from prose.
3. Corroboration for 8 complete seats: the L1 transcript records an explicit delivery,
   `[async-result] KakeR30.<seat>`, at `history://KakeR30` lines 732, 764, 770, 808, 818, 832,
   842, 852. Every one is classified complete below; none is a partial.
4. Report authorship: each seat's dispatch prompt names its own path
   (`Report: write your scoped findings to .ufo/waves/round-30/w2/<Seat>.md`, `w2-spec.json`)
   and each seat's transcript shows the `write`/`edit` call to that same path, so the file to
   seat mapping is observed, not just name-matched.

## JSON (20 entries)

```json
[
{"report":"AfterMutantLedger.md","seat":"KakeR30.AfterMutantLedger","role":"mutation-tester","status":"partial","evidence":{"published_result":false,"transcript_ends_on":"write(...w2/AfterMutantLedger.md) -> ok, 1 line; no closing message after the report was written"}},
{"report":"CriticC1Scope.md","seat":"KakeR30.CriticC1Scope","role":"critic","status":"complete","evidence":{"published_result":true,"final_message":"named its exported gates and residual limits","async_result_line":"history://KakeR30:764"}},
{"report":"CriticEntryContrast.md","seat":"KakeR30.CriticEntryContrast","role":"critic","status":"complete","evidence":{"published_result":true,"final_message":"points at the report with offsets, hashes and exit codes"}},
{"report":"CriticFrontierWording.md","seat":"KakeR30.CriticFrontierWording","role":"critic","status":"complete","evidence":{"published_result":true,"final_message":"states what it did not run, fetch or check"}},
{"report":"CriticMeasurementLimits.md","seat":"KakeR30.CriticMeasurementLimits","role":"critic","status":"complete","evidence":{"published_result":true,"final_message":"evidence, receipts, smallest safe corrections","async_result_line":"history://KakeR30:770"}},
{"report":"CriticQualityCriteria.md","seat":"KakeR30.CriticQualityCriteria","role":"critic","status":"complete","evidence":{"published_result":true,"final_message":"defers the unrun sweep to the report"}},
{"report":"CriticRejects.md","seat":"KakeR30.CriticRejects","role":"critic","status":"complete","evidence":{"published_result":true,"final_message":"verdicts unchanged with corrected reasons","async_result_line":"history://KakeR30:732"}},
{"report":"CriticStrictChecker.md","seat":"KakeR30.CriticStrictChecker","role":"critic","status":"complete","evidence":{"published_result":true,"final_message":"four checker holes plus stub locations"}},
{"report":"MutGateRepeatsWalkTty.md","seat":"KakeR30.MutGateRepeatsWalkTty","role":"mutation-tester","status":"complete","evidence":{"published_result":true,"final_message":"answer: all four repairs lack a committed fixture"}},
{"report":"MutRunnerCompare.md","seat":"KakeR30.MutRunnerCompare","role":"mutation-tester","status":"complete","evidence":{"published_result":true,"final_message":"not-verified list on the mutant ledger"}},
{"report":"MutWitnesses.md","seat":"KakeR30.MutWitnesses","role":"mutation-tester","status":"partial","evidence":{"published_result":false,"transcript_ends_on":"write(...w2/MutWitnesses.md) -> ok, 1 line; 'all four ledgers are complete' then the write, no closing message"}},
{"report":"ReopenS051S052.md","seat":"KakeR30.ReopenS051S052","role":"reviewer","status":"partial","evidence":{"published_result":false,"transcript_ends_on":"bash(git --no-pager -C $L diff --stat 451e98f...) while rechecking rows at a newer HEAD; no closing message"}},
{"report":"RerunC1Strict.md","seat":"KakeR30.RerunC1Strict","role":"reviewer","status":"complete","evidence":{"published_result":true,"final_message":"Verdict: HOLDS, with residual risk","async_result_line":"history://KakeR30:832"}},
{"report":"RerunC2Counter.md","seat":"KakeR30.RerunC2Counter","role":"reviewer","status":"complete","evidence":{"published_result":true,"final_message":"C2 holds, closure checks F1-F3 partial fail","async_result_line":"history://KakeR30:842"}},
{"report":"ReviewEntryBuildRules.md","seat":"KakeR30.ReviewEntryBuildRules","role":"reviewer","status":"complete","evidence":{"published_result":true,"final_message":"residual risk low, one medium wording overreach","async_result_line":"history://KakeR30:818"}},
{"report":"ReviewEntryHeadersDomains.md","seat":"KakeR30.ReviewEntryHeadersDomains","role":"reviewer","status":"partial","evidence":{"published_result":false,"transcript_ends_on":"eval(py) listing year tokens from saved sources; no closing message"}},
{"report":"ReviewPublishChannelsRecheck.md","seat":"KakeR30.ReviewPublishChannelsRecheck","role":"reviewer","status":"partial","evidence":{"published_result":false,"transcript_ends_on":"edit([...ReviewPublishChannelsRecheck.md#6693]) mid-correction; no closing message"}},
{"report":"ReviewSkillRenderTable.md","seat":"KakeR30.ReviewSkillRenderTable","role":"reviewer","status":"complete","evidence":{"published_result":true,"final_message":"full report pointer, findings advisory","async_result_line":"history://KakeR30:852"}},
{"report":"ScoutNoHarmDiff.md","seat":"KakeR30.ScoutNoHarmDiff","role":"scout","status":"complete","evidence":{"published_result":true,"final_message":"no installs, no network; report is the only lane write","async_result_line":"history://KakeR30:808"}},
{"report":"SentinelRunnerSetup.md","seat":"KakeR30.SentinelRunnerSetup","role":"sentinel","status":"complete","evidence":{"published_result":true,"final_message":"probes confirmed four setup harms; no source changes"}}
]
```

Role split: complete = 7 critic, 4 reviewer, 2 mutation-tester, 1 scout, 1 sentinel. Partial =
3 reviewer, 2 mutation-tester. The 14 report-less seats are all cancelled; none left a file.

## Operability consequence (the part that matters downstream)

- **The 5 partial reports read as finished.** All have a title, findings, numbers and a
  "not verified" section; `wc -l` runs 67-139. Nothing in the bytes marks them as unreturned,
  so a later round reading only the directory would treat them as returned evidence. This is
  the routed defect: the wave directory does not record seat status.
- **They did not leak into admitted evidence.** A lane-wide search for the 5 filenames found
  them only in `w2-spec.json`, `w2-dispatch.json`, `w2-assignments.json` and
  `swarm-registry.json`. No file under `corpus/`, and neither `SCORECARD.md` nor `LOG.md`,
  cites any of them. The public report `.ufo/reports/round-30/kake.md:64` says "their partial
  reports, where present, are unverified" and cites only complete seats
  (`w2/ScoutNoHarmDiff.md`, `w2/SentinelRunnerSetup.md`, `w2/ReviewSkillRenderTable.md`).
  The single near-hit, `w2/CriticRejects.md:56`, records ReopenS051S052's live refusal to open
  a page, not its report's content.
- **A cancelled report can carry facts the L1 never counted.** `AfterMutantLedger.md` (partial)
  records `jsonschema` 4.26.0 installed into its sandbox venv via `uv pip install`; the L1's
  report says "no seat reported an install". Both are true because the seat never returned, but
  it shows a cancelled report's tooling facts are outside the L1's accounting.
- **Cheap fix for the L1.** The status is recoverable only from `agent://`/`history://` today.
  A `status` field per seat in `swarm-registry.json` (or a suffix on the filename) would make
  the directory self-describing.

## Not verified

- I did not read the raw session store on disk; the two signals above both come through the
  harness (`agent://`, `history://`), and they agree, but neither is the on-disk terminal
  record of the `task` call.
- The `[async-result]` confirmations cover 8 of the 15 complete seats only; the L1 transcript
  rendering collapses batched `wait({})` deliveries, so the other 7 rest on signals 1 and 2.
- I did not re-run any seat's commands, so I make no claim about whether a complete report's
  numbers are right, nor about whether a partial report's findings would have held.
- I did not check wave 1 (all 34 returned per `history://KakeR30:925`).
