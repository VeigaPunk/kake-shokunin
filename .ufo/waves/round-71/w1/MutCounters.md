# MutCounters — round 71 mutation probe (kake, attempt 1)

Scope: 24 mutants of the two frozen counters, run against base `cc6b4e0b8c35e72dfb02c6184b847f68c1262153` and two repaired fixtures built from freeze `04557e17`. Frozen bytes: `c71_calibration.py` sha256 `ae317667335b76df4507dc6c6620926628ce257308884158159bdb6a82b0fd51`, `c71_tmp.py` `9037746bdf17bae71b04f88a8e28048b4254df5e34c8e5ebc341dd07b64da32a`. Scratch clone `/fast/scratch/hyaku/kake-r71/MutCounters/clone` (toplevel asserted equal before every commit); fixtures are children of the freeze commit, not of base. Sibling outputs were not read.

## Repaired fixtures (applied independently)
- F-C1 `2473255da6d9…`: SCORECARD line 21 → `## Superseded plan — round 21 (historical record)`, line 3990 → round-48 equivalent, `Correction (round 71):` line with `attack share 3/14`, `## Planned — next round` appended. Frozen receipt: `stale_planned=0 stale_at=[] attack_stated=4/14 attack_strict=3/14 attack_mismatch=0 guard=ok mismatches=0 met=True`, exit 0.
- F-C2 `2219d90a0a19…`: SKILL.md line 95 → `D=$(mktemp -d) && cp state/probe-latest.json "$D/probe-latest.backup.json"`; the six token lines 27/227/356/359/463/464 annotated with the exact missing path, `test -e` exit 1 (recorded 2026-11-03) and `historical record, not an executable instruction`. Frozen receipt: `tokens_total=12 unannotated_tokens=0 unannotated_lines=[] removed=7 added=7 guard=ok met=True`, exit 0.
- Controls: base C1 `stale_planned=2 stale_at=[21, 3990] attack_stated=4/14 attack_strict=3/14 attack_mismatch=1 guard=ok mismatches=3 met=False` exit 1; base C2 `tokens_total=7 unannotated_tokens=7 unannotated_lines=[27, 95, 227, 356, 359, 463, 464] removed=0 added=0 guard=ok met=False` exit 1. Cross-input: C1 on F-C2 is red, C2 on F-C1 is red (unchanged from base).

## Mutants — verdict per seat rule (killed iff exit or stdout differs on base/F-C1/F-C2)
| # | mutant | defect | verdict / observed contrast |
| --- | --- | --- | --- |
| 1 | c1_m1_drop_correction | correction conjunct forced False | KILLED F-C1: attack_mismatch 0→1, mismatches 0→1, exit 0→1 |
| 2 | c1_m2_next_round_48 | NEXT_ROUND 72→48 | KILLED base: stale_planned 2→1 (round 48 escapes) |
| 3 | c1_m3_bare_planned_fresh | bare `## Planned` parsed as fresh (999) | KILLED base: stale_planned 2→1 (line 21 escapes) |
| 4 | c1_m4_bare_planned_always_stale | body scan returns 0 | KILLED F-C1: guard ok→fail, met True→False (the guard re-derives the removed heading's round) |
| 5 | c1_m5_guard_noop | guard loop over empty set | SURVIVED (see S1) |
| 6 | c1_m6_guard_accept_deletion | guard passes any planned removal | SURVIVED (see S1) |
| 7 | c1_m7_roles_add_executor | executor added to STRICT_ROLES | KILLED base: attack_strict 3/14→6/14 |
| 8 | c1_m8_roles_drop_labrat | labrat removed from STRICT_ROLES | SURVIVED (see S2) |
| 9 | c1_m9_superseded_as_stale | superseded headings rescanned as planned | KILLED F-C1: stale_planned 0→2 |
| 10 | c1_m10_count_correction_line | correction line also counted as stated share | KILLED F-C1: population 2 → exit 2 `C1 unevaluable: stated attack-share population is 2` |
| 11 | c1_m11_stale_boundary_le | `< 72` weakened to `<= 72` | SURVIVED (see S3) |
| 12 | c1_m12_guard_any_superseded | guard accepts any superseded round | SURVIVED (see S4) |
| 13 | c2_m1_no_annotation_check | annotation test forced False | KILLED base: unannotated_tokens 7→0, exit 1→0 |
| 14 | c2_m2_first_token_only | one token counted per line | KILLED F-C2: tokens_total 12→6 |
| 15 | c2_m3_phrase_case_insensitive | phrase matched case-folded | SURVIVED (see S5) |
| 16 | c2_m4_mktemp_guard_loose | mktemp accepted with a /tmp token present | SURVIVED (see S6) |
| 17 | c2_m5_guard_no_count | removed/added count equality dropped | SURVIVED (see S7) |
| 18 | c2_m6_token_scope_kake | token regex scoped to `kake-` | KILLED base: tokens_total 7→6 (`/tmp/probe-latest.backup.json` missed) |
| 19 | c2_m7_annotation_window_80 | phrase searched only in first 80 chars | KILLED F-C2: unannotated_tokens 0→10 |
| 20 | c2_m8_phrase_anywhere_global | phrase found anywhere in the file annotates every line | KILLED base: pre-existing r20 citations (lines 309/311/312) make unannotated_tokens 7→0, exit 1→0 |
| 21 | c2_m9_removed_check_off | removed lines no longer checked for /tmp | SURVIVED (see S8) |
| 22 | c2_m10_guard_any_added | added-line `all` weakened to `any` | KILLED base: empty added set → guard ok→fail |
| 23 | c2_m11_exit_zero | always exit 0 | KILLED base: exit 1→0, stdout identical |
| 24 | c2_m12_mktemp_annotates | `mktemp` on a token line suppresses the count | SURVIVED (see S9) |

## Survivors under the frozen triple — reason, and supplementary probe that kills each
- S1 (#5,#6) guard mutants: base and both repaired fixtures carry `guard=ok`, so no guard-breaking revision exists in the frozen triple; outputs are byte-identical. Probe J1 (delete both superseded headings, correction kept): frozen `guard=fail` exit 1 vs mutants `guard=ok met=True` exit 0 → mutation is a real defect the frozen fixtures cannot reach; the contract junk control must be a separate seat's input.
- S2 (#8 labrat): round-70 results have no labrat row, so dropping it cannot change k=3/14. Probe J4 (append a labrat row, 15 rows): frozen attack_strict 4/15 vs mutant 3/15.
- S3 (#11 `<=`): F-C1's `## Planned — next round` does not match the counter's `## Planned — round N` regex, so no parseable round-72 heading exists; base rounds 21/48 are stale under both operators. Probe J5 (append `## Planned — round 72`): frozen green exit 0 vs mutant stale_planned 1 exit 1. Note for the lane: repair item 4's heading is invisible to the stale parser.
- S4 (#12 round-agnostic guard): F-C1 supplies the correct round on both superseded lines. Probe J3 (superseded says round 22 for the round-21 heading): frozen `guard=fail` exit 1 vs mutant `guard=ok met=True` exit 0.
- S5 (#15 case-folded phrase): every repaired token line carries the exact-case phrase, so folding changes nothing. Probe J7 (uppercase the phrase on line 27 only): frozen unannotated_tokens 2 vs mutant 0.
- S6 (#16 mktemp guard): F-C2's mktemp line carries no /tmp token, so the dropped exclusion is inert. Probe J2b (mktemp line that also keeps `/tmp/probe-latest.backup.json`): frozen `guard=fail` vs mutant `guard=ok` on the same 1 unannotated token.
- S7 (#17 no count equality): F-C2 removes 7 and adds 7. Probe J2 (delete the six annotated lines, keep the mktemp edit): frozen `guard=fail` exit 1 vs mutant `guard=ok met=True` exit 0.
- S8 (#21 removed check off): every removed line in F-C2 carries a /tmp token. Probe J11 (replace a non-/tmp line with a mktemp line): frozen `guard=fail` vs mutant `guard=ok`.
- S9 (#24 mktemp suppression): no token-bearing line in F-C2 contains `mktemp`. Probe J8 (line 356 phrase replaced by `run under mktemp`): frozen unannotated_tokens 2 vs mutant 0.
Killed 14/24 on the frozen triple; 10 survivors, all killed by a supplementary probe; 0 mutants with no distinguishing input among the 11 probes. Probe revisions and full stdout are in `MutCounters/results.json`; each mutant diff is `MutCounters/<name>.diff`.

## Restoration, hygiene, tooling
- Frozen copies were never edited: re-hashed after all runs equal the freeze blob hashes above; mutants are separate files under the report dir and scratch. Clone worktree clean (`git status --porcelain` empty) after the probe commits; no writes to the lane's tracked files (`git status` shows only the six pre-existing untracked round-71 wave entries, none ours).
- No tool installed or upgraded; pacman not invoked. Scratch `/fast/scratch/hyaku/kake-r71/MutCounters` deleted before yield.
- Honest limits: verdicts hold only for the three frozen inputs named by the seat rule; junk probes are supplementary evidence, not scope expansion of the frozen criterion. Counters read committed bytes only; this probe says nothing about seat prose or the other counters.
