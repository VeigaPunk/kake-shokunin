# ReviewLessonNumbers — round 38 wave 2

Axes: operability; freshness (source registry). Target: every number and pointer in `corpus/lessons/round-38.md` at `adab4c7e9ec2178657395f49346f18800ff4796f`.

## Findings

1. **Medium — overstated (`corpus/lessons/round-38.md:91-92`).** “Every round-38 harm receipt” has `toolSha256` and `toolRevision` is false for two of six files in `verification/harm/`. The C1 robots counter receipt `r37-counter-on-3ed8e15c-tool.json:2-11` and round-36 counter receipt `r36-counter-on-145a6468-tool.json:2-11` have `toolSha256`, but no `toolRevision` (both JSON files end at line 126). Four pinned selftest receipts do have both fields. Qualify this to the pinned selftest receipts or pin revisions in the two counter receipts.
   - `timeout 30s jq -s '{count:length,missingToolRevision:(map(select(has("toolRevision")|not))|length),missingToolSha256:(map(select(has("toolSha256")|not))|length)}' .ufo/waves/round-38/verification/harm/*.json` — exit 0; count 6, missing revision 2, missing SHA 0.

2. **Medium — unsubstantiated negative (`corpus/lessons/round-38.md:109-111`).** The committed evidence does not establish “No dead seats and no refusals” for wave 1. `w1-dispatch.json` records 32 spawns and 32 registry members; its `RevengerExemption` task requests `.ufo/waves/round-38/w1/RevengerExemption.md` (`w1-dispatch.json:508-510`), but that report is absent from the committed `w1/` directory. The registry member has no result/status field. This is a missing return record, not proof that the seat died or refused; mark the blanket claim unverified absent that report.
   - `timeout 30s jq '{spawn:.counts.spawn,total:.counts.total,registryMembers:(.registry.members|length)}' .ufo/waves/round-38/w1-dispatch.json && timeout 30s jq '{members:(.members|length),revenger:.members.RevengerExemption}' .ufo/waves/round-38/w1/swarm-registry.json` — exit 0; 32/32 and RevengerExemption is a spawn with no outcome field.
   - `timeout 30s git ls-tree -r --name-only adab4c7e9ec2178657395f49346f18800ff4796f -- .ufo/waves/round-38/w1/RevengerExemption.md` — exit 0, no path emitted.

3. **Low — population overbroad (`corpus/lessons/round-38.md:67-68`).** “Every control of the named classes scored at most 16” holds for the pre-declaration v3 batch, but is unqualified. The post-freeze `CtlExampleK` probe is a partial-(k) control in the named class-(6) territory (`SCORECARD.md:2243-2251, 2284-2286`) and scored 19/20 under the same v3 counter (`verification/w1attack/CtlExampleK.json:2-11`). State the pre-freeze population explicitly; the 19/20 probe did not meet C2's 20/20 predicate.
   - `timeout 30s jq '{claim,predicate,passed,met,counterSha256,toolSha256}' .ufo/waves/round-38/verification/w1attack/CtlExampleK.json` — exit 0; 19, `met:false`.

## Holds

- `timeout 30s git log --format='%H %s' af43a50fa399881eead9381d835b78a015e277a6..adab4c7e9ec2178657395f49346f18800ff4796f` — exit 0; confirms the C1 declaration/withdrawal, C2 build, reveal, non-claim repair and tip sequence (`b0ab7f6` → `2dab7f3` → `3ed8e15c` → `99357694` → `145a6468` → `adab4c7e`).
- `timeout 30s jq -s '{count:length,met:(map(select(.met==true))|length),passed20:(map(select(.passed==20))|length),min:(map(.passed)|min),max:(map(.passed)|max)}' .ufo/waves/round-38/verification/mutref/M*.json` — exit 0; 42 C1 mutants, 29 met, 13 passed 20, scores 16–20. The lesson correctly calls out the scorecard's stale “28” as a historical miscount; the correction is at `SCORECARD.md:2282-2283` (original table still says 28 at :2194/:2199).
- `timeout 30s jq -s '{count:length,met:(map(select(.met==true))|length),min:(map(.passed)|min),max:(map(.passed)|max)}' .ufo/waves/round-38/verification/v3/mutref-M*.json && timeout 30s jq -s '{count:length,min:(map(.passed)|min),max:(map(.passed)|max)}' .ufo/waves/round-38/verification/v3/A[1-8]-*.json` — exit 0; 42 mutants scored 16–19, none met; 8 ablations scored 16–18.
- C2 receipts (`verification/c2-at-af43a50f.json`, `c2-at-3ed8e15c.json`, `c2-keyrev-at-99357694.json`) match 8/20 base, 20/20 at the build, and reveal-revision refusal. The build/reveal IDs and predicates in lesson lines 16-21 match `SCORECARD.md:2263-2274` and receipts.
- `timeout 30s jq '{passed,met,predicate,revision,toolSha256}' .ufo/waves/round-38/verification/c2-at-af43a50f.json .ufo/waves/round-38/verification/c2-at-3ed8e15c.json .ufo/waves/round-38/verification/c2-keyrev-at-99357694.json` — exit 0; emitted 8/20, 20/20, and null fields for the reveal revision (scorecard records the reveal measurement refusal as exit 2).
- Source dates, HTTP statuses, abbreviated hashes, section citations, and the 85 allowed / 43 excluded / 0 mismatch character audit match the wave-1 source reports and `corpus/SOURCES.md:42,106-109`; `SCORECARD.md` diff shows the S034 used-by append and S098-S101 rows. Source and report pointers cited in the lesson resolve, including S096's commit `22b355ff` and round-37 line references.
- Other audited counts hold: seven control seats (`SCORECARD.md:2176-2193`); control timing 58 s early and round-37 timing 435 s late (`criteria/receipts/timeline-r38.txt`, `timeline-r37.txt`); consequence checks 1/0/0 and 10/10 selftest (`ccc-*.txt`); postfix 137/137 on `944d2f51…d3e5`; source-recheck g33-g35, 106/106 and 28/28; robots selftest 137→194, base fails 45 and shortcut 44 (`verification/harm/`, `w1/ExecRecheckCaps.md`, `w1/ExecRobotsSelftest.md`). `git diff --unified=0` confirms the two capability-row edits described at lesson lines 86-87.
- `timeout 30s jq '[.cases[].runs[]] | {runs:length,missing:(map(select(.expect|has("checksEvaluated")|not))|length)}' .ufo/waves/round-38/sealed/cases_v3.json` — exit 0; 22 expected runs, zero missing `checksEvaluated`. The counter still checks that field conditionally (`sealed_count_v3.py:178-180`), not as an enforced universal.

## Residual risk / verification gaps

No round-38 counter, selftest, build, or network fetch was run here; verdicts above use committed receipts/reports and read-only Git. LSP is unavailable (`read xd://lsp` returned “No such tool”; only `ast_edit` and `debug` are mounted), so no semantic references/definition check was possible. No tools installed or updated.

Report: .ufo/waves/round-38/w2/ReviewLessonNumbers.md
