# Round 29 wave 2 (falsify): no harm to existing lane gates and corpus

Seat: KakeR29.NoHarmExistingGates (leaf, no subagents). Axes: operability, freshness. Milestone: r29-falsify.
Attacked: committed bytes at 7697990cbca20291f3b0367b8ff4220e93b38b03, compared with base fe1805cf32a7aadf4574637a3a8912354cee2c7b.
Sandbox: /fast/scratch/hyaku/kake-r29/w2/NoHarmExistingGates/ with clones `base/` and `tip/` at those commits. `cf1` = base plus the two round-29 corpus files. `cf2` = tip without those two files. Raw outputs are in `out/`; exit codes are in the matching `.rc` files.
Tools: node v24.21.0, Python 3.14.8, git 2.56.0, all already installed. I installed or upgraded nothing.

## Verdict
- Holds: at tip, every existing gate in scope keeps its exit code and its findings. Only counts change.
- Every count change traces to round 29 (table). Header lines (timestamps, repo paths) were ignored.
- Limit to state: round 29 adds a host-only path to a committed lesson (finding 2).
- Process breach, disclosed: I ran one command outside my bounds (finding 1).

## Table: base vs tip (each command run in the clone at its own revision)
| Command | Base fe1805cf | Tip 7697990 | Differs | Cause |
|---|---|---|---|---|
| `node scripts/freshness-sweep.mjs --section=paths` | rc 0, OK; 66 files, 574 occurrences, 92 tokens; resolve 19, declaredAbsent 63, drift 0, unresolved 10; set-delta +10 | rc 0, OK; 68 files, 575 occ., 93 tokens; resolve 20, declaredAbsent 63, drift 0, unresolved 10; set-delta +12 | counts only | 2 new files; 1 new resolved path (finding 2); relative-form cites +13 from new files (cf1) and +13 from modified files (cf2) |
| `python3 -B scripts/canonical_audit.py --selftest` | rc 0; 11249 bytes | rc 0; 11249 bytes, byte-identical | no | none |
| `node scripts/corpus-contract.mjs --json` | rc 0; ok; knowledgeChecked 24, lessonsChecked 23, skipped 13, findings 0 | rc 0; ok; knowledgeChecked 25, lessonsChecked 24, skipped 13, findings 0 | counts only | 1 knowledge file and 1 lesson added (cf1 = tip, cf2 = base) |
| `python3 -B scripts/citing_set.py --root . --json` (as assigned) | rc 64: missing --population, --ledger | rc 64: same | no | not round 29; the command as written cannot evaluate |
| citing_set A: population `round-27/frozen/population.json`, ledger `round-27/frozen/ledger.json` | rc 1 failed; citing 59, ledger 41; 18 unadjudicated; corpusFiles 27; outsidePopulation 22 | rc 1 failed; same 59, 41, 18; corpusFiles 28; outsidePopulation 26 | counts only | new knowledge file cites S040-S043, outside the population |
| citing_set B: same population, ledger `round-27/complete-ledger.json` | rc 1 failed; citing 59, ledger 58; 1 finding: S018 in corpus/knowledge/field-performance-cwv.md | rc 1; same finding; corpusFiles 28; outsidePopulation 26 | counts only | as A |
| citing_set C: population `round-26/population.json`, complete ledger | rc 1; same finding as B | rc 1; same finding as B | counts only | as A |
| A, B, C with `--revision` set to each commit | rc 1 each; equal to the no-revision run except source and revision fields | rc 1 each; same | fields only | none |
| `python3 -B scripts/citing_set_selftest.py` (extra, existing gate) | rc 0 | rc 0 | no | none |

Notes: `--revision` does not apply to freshness-sweep, corpus-contract or canonical_audit. Their sources contain no revision flag, so they ran at each checkout. `git diff --name-status --diff-filter=MDRT` gives 7 M and no D, R or T. The unfiltered diff gives 194 A and 7 M. M files and changes: .gitignore +2; PROVINCE.md +5/-3; SCORECARD.md +36; SKILL.md +21; corpus/QUALITY.md +62; corpus/README.md +24; corpus/SOURCES.md +12 (new rows S040-S048).

## Findings, by severity
1. HIGH, process (mine). I ran `node scripts/freshness-sweep.mjs` with no section flag at base and at tip (rc 1 both; out/fresh_full_base.out, out/fresh_full_tip.out). That runs the §armed section, which sends GET requests to the lane's pinned sites (freshness-sweep.mjs:72, :77, :85; fetch at :725) and `git ls-remote origin main` on pinned repos (:744, :897). The bounds forbid live probes of owned web properties, and this command was not in my assignment. I did not repeat it. The base and tip runs differ only in the §paths lines. The DRIFT verdict (PQ-2 remote moved, ds4cc sitemap listed-live, plazir anomaly) appears at base too, so round 29 did not cause it. I did not check those live results for correctness, and I did not run the sweep's own --selftest, which writes under /tmp.
2. MEDIUM, round 29, latent. corpus/lessons/round-29.md:110 cites `/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:173`, a host file outside the repo (it exists here, 17367 bytes). The sweep counts it as resolved (resolve 19 to 20; out/paths_tip.json). On any host without that file, the same unannotated cite is a drift miss (exit 1) under the sweep's own rule (freshness-sweep.mjs:1289-1292, selftest case b). Today's OK verdict holds only on this workstation. Suggested fix for the L1: annotate it or cite a committed path.
3. LOW, round 29, content. PROVINCE.md:26-30 replaces three existing frontier lines rather than appending. It removes "Jekyll/base-path build tooling" from the open-list sentence (out/mods_U0.diff:8-20). No gate verdict changed, and freshness-pins.json is not in the diff.
4. INFO, pre-existing. The citing-set gate is already red at base under every candidate input: A has 18 unadjudicated pairs; B and C have 1 (S018). Tip matches base on findings. S040-S043 lie outside the r26 population, so the new file adds outside-population counts only (+4) and never a finding. By design, the gate cannot adjudicate round-29 citations.
5. INFO. The assigned citing_set command exits 64 at both revisions because the gate requires --population and --ledger. SCORECARD.md names no canonical pair (a search for population.json and complete-ledger found nothing), so I ran the three candidate pairs found in the tree. The round-27 contract names round-27/frozen/population.json and frozen/ledger.json as the frozen oracle, which is case A.

## Residual risk and verification gaps
- Not run: freshness-sweep --selftest (writes under /tmp by design); the C1/C2 counters and base_path_selftest.py (other seats); correctness of the live §armed results.
- The population and ledger choice is my inference from the tree (finding 5). Only three pairs were tried.
- `git status --porcelain` is empty in both clones after all gate runs (out/status_base.txt, out/status_tip.txt), so no gate wrote into either clone.
- One read-only `git diff --name-status … | head` ran in the lane before I moved all git reads to the sandbox clone. No other git or jj command ran in the lane.

## Evidence
- Exit codes: out/*.rc. Outputs: out/base_*, out/tip_*, out/cs_{base,tip}_{A,B,C}_{norev,rev}.json, out/cf1_*, out/cf2_*, out/paths_{base,tip,cf1,cf2}.json.
- Diffs: out/mods_U0.diff, out/diff_name_status_all.txt, out/diff_name_status_MDRT.txt.
- Sandbox scripts (not lane files): tmp/harness1.sh, tmp/harness2.sh, tmp/compare.py.
