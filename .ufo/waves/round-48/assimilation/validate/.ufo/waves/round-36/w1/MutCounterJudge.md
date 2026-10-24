# MutCounterJudge — synthetic counter mutation probe
Axes: operability (judge discrimination, projection invariance, faithful materialization, exact restoration). Freshness was not measured.
Sandbox S = `/fast/scratch/hyaku/kake-r36w1/MutCounterJudge` (all evidence paths below are absolute after expanding S).
Attacked only sandbox copies of public `sealed_count.py`; 12 invented cases, four toy tools, 18 independent one-line mutations. No sealed tree access, real key access, counter main/load_key invocation, network, Git/JJ changes, or source-tool changes.
Result: **15 killed, 3 survived, 0 inconclusive**; zero detector exceptions. This is not a result on the 28 sealed cases or an admission judgment.

## Detector and tools
`S/detector.py:21-54` directly calls materialize/jail/judge, using the unchanged public bubblewrap jail and 3-second tool deadlines. Each mutation gets independent pristine, mutated, restored executions with fresh random materialization each time.
Expected detector: any changed case pass/fail in any of four tools kills a mutant, provided correct-tool pristine = 12/12 and restored behavior/hashes match. Every killed mutant also changed at least one aggregate pass count.
Pristine and restored counts for every mutant, ordered C/F/S/B: **12/7/1/8** out of 12.
C = `S/tools/correct.py`: contract-correct for these synthetic cases only; reverses finding order and includes ignored non-moved targets/extra fields. Not a full C1 implementation.
F = `S/tools/wrong_fields.py`: independently corrupts exit, verdict, reason, moved target, or check on S01/S02/S03/S04/S06 respectively.
S = `S/tools/wrong_shape.py`: empty-object findings on S01, extra non-object findings on S07/S08, duplicate findings elsewhere when nonempty.
B = `S/tools/wrong_bindings.py`: assumes literal `body.txt` on S01/S05/S06/S09 and emits original ids on S02/S03/S07.
Implementations: `S/tools/toy_core.py:70-102`; wrappers select modes. Inputs/expectations: `S/make_cases.py:30-52`, materialized key `S/synthetic_key.json` (12 cases).
Cases cover clean, 404, 503, permanent/temporary redirects, missing quote, ignored non-moved target, order, multiplicity, escaping body, bad version, invalid entries/null checks.

## Mutation table
Counts are mutated C/F/S/B; K = killed, S = survived. L is the original public-counter line. SHA is the mutated-byte SHA-256 prefix; full hashes and changed cases are retained in each result JSON.
| Mutant | Single mutation (L) | Counts /12 | Result | SHA-256 prefix |
|---|---|---|---|---|
| M01 | Omit moved target (108) | 12/8/1/8 | K | 7305e39691fa |
| M02 | Compare target for every reason (108) | 3/1/1/1 | K | 391c081e2aa2 |
| M03 | Skip inverse id mapping (110) | 3/2/1/4 | K | 9f41a18deab9 |
| M04 | Preserve order instead of sorting (111) | 9/4/1/6 | K | 47c9a4277374 |
| M05 | Set instead of multiset (111) | 12/7/9/8 | K | 252d367e095e |
| M06 | Ignore verdict (151) | 12/8/1/8 | K | 0e0e8e16658f |
| M07 | Ignore exit (145) | 12/8/1/8 | K | 602f8c7834fb |
| M08 | Coerce non-list findings to list (155) | 12/7/2/8 | K | 1f97c7e4edb3 |
| M09 | Omit reason comparison (110) | 12/8/1/8 | K | ff2e7b398c24 |
| M10 | Omit check comparison (110) | 12/8/1/8 | K | 587b6ec17c1d |
| M11 | Discard non-object findings (105 deleted) | 12/7/3/8 | K | 055fbaeb8e74 |
| M12 | Write base64 text, not decoded bytes (118) | 9/6/0/7 | K | 79f89881f71a |
| M13 | Skip body-name rewrite (135) | 7/5/0/7 | K | 5143f1e6299e |
| M14 | Keep original check ids (132) | 12/7/1/8 | S | 43d55eb226f4 |
| M15 | Keep original body basenames (119) | 12/7/1/12 | K | acb7a7ab91d1 |
| M16 | Place escaping files inside work (120) | 11/6/1/7 | K | fa206312c281 |
| M17 | Accept malformed JSON output (150) | 12/7/1/8 | S | 56970c190f93 |
| M18 | Remove no-process guard (145) | 12/7/1/8 | S | 6e9e041dd1f0 |

## Coverage findings
M14 survives: these outputs do not enforce fresh-id use. Pristine B already passes S02/S03/S07 with original ids because project uses `idmap.get(check, check)`; S02 recorded idmap `two -> c2f211e481799`, output check `two`, exit 1, passed true (`S/evidence/baseline.json`, wrong_bindings/S02). This is a synthetic identity-discrimination gap, not evidence about sealed-case reachability.
M17 survives because all four tools emit JSON; M18 survives because no run times out or has an absent process. Those branches have no detecting observation in this suite. Survivors do not authorize changing the public contract.
M05 shows why a correct tool alone is insufficient: it stays 12/12 while duplicate-emitting S rises 1 -> 9. M15 similarly leaves C unchanged while the filename-dependent B rises 8 -> 12.

## Exact execution and restoration evidence
Commands ran with cwd S; setup `timeout 10s mkdir -p S/tmp S/tools S/evidence && timeout 10s cp /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-36/sealed_count.py S/sealed_count.py` exited 0 (S denotes the absolute sandbox above).
`timeout 20s /usr/bin/python3 -B prepare.py` exited 0; `timeout 20s /usr/bin/python3 -B make_cases.py && timeout 120s /usr/bin/python3 -B detector.py --baseline` exited 0, output 12 cases and baseline 12/7/1/8.
For each exact id M01,M02,M03,M04,M05,M06,M07,M08,M09,M10,M11,M12,M13,M14,M15,M16,M17,M18: `timeout 120s /usr/bin/python3 -B detector.py --mutant ID` exited 0. Four concurrent command batches held disjoint copies (M01-M05, M06-M10, M11-M14, M15-M18), sequential within each batch; outer deadlines 300 seconds.
`timeout 20s /usr/bin/python3 -B summarize.py` exited 0; output: `{"syntheticCases":12,"mutants":18,"killed":15,"survived":3,"inconclusive":0,"allRestored":true,"detectorExceptions":0}`.
Pristine lane/copy hash recorded before mutation, and all 18 restored-copy hashes: `88ec59140258ce759107b7472fdd07a005b7c1bb8b3ba5218347e4518342ff8e`.
Restoration runs in finally (`S/detector.py:79-90`); every restored C/F/S/B case vector equals pristine. Archival mutated snapshots are intentionally retained separately as evidence; working `S/mutants/M01/counter.py` through M18 are restored.
Full raw stdout/stderr/exit/idmaps/manifests and three-stage verdicts/hashes: `S/evidence/M01/result.json` through `S/evidence/M18/result.json`; exact mutant bytes: corresponding `mutated_counter.py`. Aggregate: `S/evidence/summary.json:1-8`.
Synthetic-key SHA-256: `8daadbbf28e2c997ae428177bb4f60c23178cacd33eb702850fe31f640a2c015`; summary SHA-256: `c8730690526359c11d34ec5b2f2fae263d247967fbbb1afdd4f6ac44157c068f`. Additional artifact hashes: `S/evidence/artifact_hashes.json:2-5`.
Tools used: Python 3.14.8 and bubblewrap 0.13.1 already installed; no installs/updates. All started commands/tool children finished; no service left running.
Not verified: real sealed coverage/count, frozen 25/28 predicate, key-pin loading, Git extraction, full C1 tool behavior, live-source freshness. No counter/contract fix was made.
