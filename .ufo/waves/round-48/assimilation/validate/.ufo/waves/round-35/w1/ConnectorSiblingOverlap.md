# ConnectorSiblingOverlap — round 35 wave 1
Axes: operability and freshness. Advisory investigation only; no admission, integration, tool repair or source-truth verdict.
Scope: 20 sibling default-branch tips, tracked text only; each captured HEAD equals its master/main tip. Kake evidence is the sandbox clone at 318561efa67206699fdaf259ffb86e39f2d916a8, never the integrating working tree. No sealed-directory access, network, subagents or sibling writes.
Evidence root E = /fast/scratch/hyaku/kake-r35/w1/ConnectorSiblingOverlap/. Full revisions, match coordinates/snippets and output hashes: E/scan-manifest.json; raw outputs: E/sibling-scan.json; source snapshots: E/snapshots/; complete item map: E/planning-map.json.
Commands: E/command-manifest.json records all 109 exact subprocess commands and exits: 90 exit 0; 19 exit 1, all supplemental RFC searches with no matches. These are research commands, not test results.
Scan command, instantiated for every sibling: `git -C <lane> grep -n -I -i -E 'security[._ /-]?txt|well[- _]known|sealed|held[- _]?out' <captured-hash> --`; all 20 exit 0, 11895 matching lines. Supplement: `git -C <lane> grep -n -I -i -E 'RFC[[:space:]-]*(9116|8615)' <captured-hash> --`; only kasegi matches (4 lines).
Other recorded commands: `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r35/w1/ConnectorSiblingOverlap/clone`; checkout -q 318561efa67206699fdaf259ffb86e39f2d916a8 there; per-sibling rev-parse HEAD, rev-parse --symbolic-full-name HEAD, for-each-ref --format='%(refname) %(objectname)' refs/heads; six pinned git show snapshots; sha256sum of the four assignment inputs. All exit 0. GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; TMPDIR=E/tmp; at most four subprocesses concurrent.
Input hashes: w1-spec.json 27475721cd3cce8e6cfc7f66175d492a65e89359f0bc35e66107d427cd7f2f89; w1-dispatch.json bfd87230fa6c9b51e55eeba2cf418a2c4443e95cc6c5ff96b48fc1667df02cfa; frozen SCORECARD.md a1ab8de01d6be399f78d490acca4b67e568a6380d3203e3710fb28322d95142e; round-34-verifier-spotcheck.md ec9c508f448bd60a89577c761acc7e66242cc5f023ab0260d906c46229aa232e.
## Overlaps and citation disposition
Sibling paths below include the lane name; abbreviated revisions resolve in E/scan-manifest.json. No matched sibling text supplies another GitHub Pages security.txt publishing how-to. Method overlaps belong in a lesson/QUALITY citation if used, not as RFC 9116 authority.
- kasegi @1fafde8f: corpus/knowledge/policy-access-playbook.md:12 says a security.txt stub is not scope; corpus/knowledge/vdp-disclosure-packages.md:13,23-31 records Contact intake and operator-only sending. Adjacent, not duplicate publishing knowledge; optional boundary citation only. Both entries explicitly mark their underlying evidence lost/not re-verifiable (:33-35 and :35-37); do not present them as newly verified primary sources.
- kagi @899c50b4: .ufo/waves/round-26/build/ClockS015-evidence/page.html:50,87 concerns OIDC discovery; not security.txt or Pages. No C2 citation needed.
- kotoba @58db81c4: .ufo/round-44/evidence/omp-live-18.12.2-strings.txt:563345 is OIDC; kengaku @1f3b0f1e: .ufo/waves/round-28/scratch/OpenS053/rfc8259.html:1040 is an account-login OIDC URL. Incidental retained bytes, not publisher guidance; do not cite for C2.
- tabi @e3cf4e0d: .ufo/waves/round-16/w1/SrcRejects.md:140,160 rejects a non-spec .well-known/webmcp manifest. Different protocol and a rejection, not reusable security.txt guidance.
- kaidoku @d210fb8f: SCORECARD.md:3146 distinguishes a met counter from a genuinely held-out prediction (168/230 inputs pre-seen); :3197 separately discloses author-selected public names versus blind selection. Strong methodology citation, no C2 duplication.
- mado @8e5d9369: SCORECARD.md:1450 freezes primary eligibility/normalizations and keeps supplemental cases outside its denominator; :1470 later records harm despite 35/35+17/17. Cite the bounded methodology and its contrary result together, never just the green counts.
- mori @95cd794e: corpus/lessons/round-23-verifier-spotcheck.md:36-38 preserves an explicit contradiction: the pre-seal rule demands unknown while the frozen oracle says enabled/xfs. Both bytes and 29/30 remain unchanged. Sealing is not proof that the oracle agrees with the contract.
- lore @380ef3ab: corpus/lessons/round-103.md:131-144 discloses post-results criterion wording and re-grades sealed questions, reversing one entry decision. Method-only citation; not permission to change this round's frozen target.
- souji @4edb25df: corpus/lessons/round-17-verifier-spotcheck.md:18 distinguishes synthetic held-out tables from precision on fresh transcripts; corpus/lessons/round-17.md:7,14 records the table counter. Method-only.
- audio @7a2fcd4f: SCORECARD.md:252 records 13 held-out boundary classifications; kagi @899c50b4: SKILL.md:707 and corpus/lessons/round-22.md:169 distinguish fresh qualifier attacks from tamper/setup tests. Analogous verification, not duplicated publishing work.
- kama @1560e4d8: .ufo/waves/round-17/build/advice/CriticC1Invariants.md:89,119 proposes independent held-out mutants, not an observed implementation; tsukuroi @5bbd1841: .ufo/waves/round-29/residual/ResCritVerdicts.md:30 says revised tests are no longer held-out strictness; kotoba @58db81c4: SCORECARD.md:31 retains 6/18 held-out errors separately from the declared counter. Method-only.
- Adjacent but not sealed-counter implementations: kengaku @1f3b0f1e corpus/knowledge/agent-time-horizon-and-task-validity.md:45 (blinded validity checks); kotodama @3569d244 corpus/knowledge/verification/lexicon-coverage-audit.md:81,86,96 (productivity diagnostics); kumitate @e5ffcbe7 corpus/knowledge/distill-and-l3.md:181-198 (sealed source-map integrity); tabi @e3cf4e0d .ufo/waves/round-21/selftest-c1.mjs:104 (producer resealing fixture). None duplicates C2; source-map sealing is not held-out correctness.
- tameshi @367ec0f1: .ufo/evidence/round-18/final/measure-final.json:225-226 only inventories mado's precision-heldout evidence in the matches; cite the actual mado work rather than treating this ledger as a second result.
- No relevant overlap among the matched text in chousa @6c5eb146, game-dev-2d @7753d49b, game-dev-3d @89dd182b or revenger @876630db. Matches are respectively alias-route closure, edits withheld from landing, idle-step sealing/explicitly no held-out work, and ordinary “well-known” wording. Full negative-sweep commands and positive hits remain in E.
## Planning data walk — all 36 items
R1–R6 mean the numbered defects at frozen corpus/lessons/round-34-verifier-spotcheck.md:215-246. “Mapped” means assigned, not implemented or verified. Evidence column is w1-spec.json line; dispatch count is 36 at w1-dispatch.json:16-20.
| Item | Route / concrete purpose | Spec line |
|---|---|---|
| ExecToolRepair | C1; R6 — a-c repair and fixtures | 13 |
| ExecIndependentOracle | C1; R1 — independent public-contract oracle | 21 |
| ExecDifferentialGenerator | C1; R1 — generated differential witnesses | 29 |
| ScribeEntryDraft | C2; frontier — publisher entry | 37 |
| ScoutDs4ccWellKnown | C2 — offline publishing substrate | 45 |
| ScoutPagesDotfilesSource | C2 — current build/hidden-file sources | 53 |
| ScoutSecurityTxtCandidates | C2 — extra source screening | 61 |
| ScoutRfc9116Errata | C2 — status/errata freshness | 69 |
| ScoutGithubExpiresDynamic | C2 — volatile example-date hypothesis | 77 |
| ScoutSecurityTxtCensus | C2 — observed examples, not normative rules | 85 |
| RevengerJekyllInclude | C2 — Jekyll/Pages code evidence | 93 |
| ScribeSourcesRows | C2 — rows and S006 used-by update | 101 |
| ScribeGateLines | C2 — located source-opening decisions | 109 |
| ScribeSkillRegistryRow | R3; C1 — gate registry draft | 117 |
| ScribeControlCorrection | R2 — three append-only corrections | 125 |
| ReviewS074Head | R5 — HTML/text recount and SOURCES note | 133 |
| ExecPrebuildLeakCheck | R4 — receipt target-exposure check | 141 |
| ExecControlDescriptionCheck | R2 — control-byte quotation check | 150 |
| ExecRegistryRowCheck | R3 — missing registry-row check | 158 |
| ScribeQualityCriteria | R1-R4 — criteria/check contracts and limits | 166 |
| ScribeMistakeMine | R2-R5 — closure mistake capture | 175 |
| ScribeProvinceReadme | C2; frontier — coverage and province boundary | 184 |
| CriticSealedDesign | C1+C2; R1 — skip-work controls/design attack | 192 |
| CriticC2Conditions | C2; R1; R6 analogue — new-counter copying/cites attack | 201 |
| CriticC1ContractAmbiguity | C1; R6 — rival contract readings | 209 |
| MutSealedCounter | C1+C2; R1 — fake-key mutation coverage | 217 |
| ReviewCounterCode | C1+C2; R1; R6 analogue — new-counter code review | 226 |
| ReviewControlReceipts | C1+C2; R1 — scores/bundles/hash evidence | 235 |
| ReviewDeclarationSizing | C1+C2; R1+R4 — sizing/order/separability/leaks | 244 |
| SentinelKeyExposure | C1+C2; R1 — exposure search, not key reading | 253 |
| ConnectorSiblingOverlap | C2; frontier; R1-R6 map — this scan | 262 |
| ReviewSpotcheckRouting | R1-R6 map — disposition audit, not all repairs | 271 |
| ReopenSourcesSpecs | C2 — RFC/registry reopening | 280 |
| ReopenSourcesOthers | C2 — docs/examples reopening | 288 |
| ReviewSelftestContractChange | C1; R6 — changed-behavior caller/text inventory | 296 |
| CriticHarmPlan | C1; R6 — before receipts and after-run plan | 304 |
## Gaps and contradictions, not a scalar verdict
- R1's final instruction (:221), rerunning lookup_control_check.py against the new counter with both retained controls, has no explicit execution/adaptation item. ReviewControlReceipts validates existing receipts; that is not this named rerun. The declaration/control-score prerequisites already exist at 81d9fd74 and 318561ef; they are not wave builds.
- R2-R5 each have named draft/check/review items above. R5 names a SOURCES correction, but no item explicitly names an appended correction at the old Gate sentence as well; ScribeMistakeMine/ReviewSpotcheckRouting can expose this without claiming it already fixed.
- R6's template/svg/math and unreadable-page problems are assigned to ExecToolRepair. The first-og:url-only comparison is NOT replaced: SCORECARD.md:1379-1382 explicitly keeps it and adds a duplicate finding. Mark that distinction, not an all-values comparison repair.
- R6 has no repair item for the legacy C2 counter D1-D4, Git-pin mutants, duplicated option tables, NUL-byte runner crash, freshness-pins re-pin or round-31 F1-F3. Routing review is an item, not a repair. The adjacent null-code debt is also carried at round-34.md:128-129.
- CriticC2Conditions, MutSealedCounter and ReviewCounterCode attack analogous parser/crash shapes in the NEW counter; they do not repair .ufo/waves/round-34/c2_source_census.py. D1-D4 remain specifically defined at round-34.md:136-142. No held-item investigation was pursued.
## One bounded proposed move
Make the missing R1 criterion round-35-target-aware and key-aware, synthesizing ReviewControlReceipts' pinned evidence with ScribeQualityCriteria's control-discrimination rule; leave the frozen counter, keys, declared targets and historic results unchanged. This is a proposal only, not an edit or reroute.
Evidence: legacy criteria/lookup_control_check.py:11-17,39-54 requires a counter with only --root/--revision and JSON total, and rejects controls only at full score. New sealed_count.py:174,249-263 uses cases/probes, requires c1/c2 plus a key argument, and C1's target is 22 rather than 24. Code-read incompatibility; no invocation attempted. [INFERENCE] Merely renaming cases to total would still wrongly clear a control scoring 22 or 23.
Effects [INFERENCE]: runtime verification becomes callable with the frozen interface; contract checking rejects a skip-work control at the actual target, not merely at perfection; substrate provenance reuses the existing counter-hash/revision/receipt binding. Operability evidence improves, freshness discrimination is preserved, and C1/C2 production behavior and publisher/source facts do not change.
Risks: never rewrite a historical result or lower a target to resolve an oracle disagreement (mori :38); seal/hash integrity alone does not prove truth or no harm (mado :1470). Receipt comparison is not source-semantic review. Any claimed benefit/no-harm remains unverified until the L1 exercises the proposed check.
Verification for L1, not run here: show the target-aware check clears known-control C1 score 21 and rejects 22/23/24, clears C2 met=false and rejects met=true; then rerun the frozen c1/c2 counter on dcef39b5/0cce15f0 with an authorized reveal revision, retaining outputs and exact counter hash. Keep oracle/contract disagreements separate from scores.
Not verified: sibling runtime behavior, source freshness, any peer's finished deliverable, actual sealed cases/probes, proposed criterion execution or no-harm. No build, test, linter, formatter or smoke run was performed.
Tool installs/updates: none. Tool issue recorded: glob with a trailing directory slash returned no matches while the same pattern without the slash found the lanes; directory discovery and pinned Git reads supplied the evidence instead.
