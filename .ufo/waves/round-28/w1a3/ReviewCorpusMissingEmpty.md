# ReviewCorpusMissingEmpty (W1A3, round 28): C1 repair, WorkingTreeSource.corpus_files

Seat: KakeR28a3.ReviewCorpusMissingEmpty. Leaf reviewer, operability axis. Advisory input for the L1. Not a verdict on the round.

Pinned: commit b5d423fc02057f67a6f3a255808313ce40d29069, scripts/citing_set.py blob c26fcd498f1974265e6bb80dca8e102f57eb7b5f. Base 22c1669c1fec83d1a0769de6b9ce686c75657e66, blob 352a471abec08daa56a0fb7ef23fe78f2930d773.
Sandbox clone: /fast/scratch/hyaku/kake-r28a3/w1/ReviewCorpusMissingEmpty/clone (HEAD b5d423f). No lane file, index, or Git state was changed.

## Bottom line

The assigned hunk does what C1 claims. Every absent, empty, subdirectory-only, dangling-symlink, and blank-revision shape that base read as clean now exits 2 with the contracted JSON report. I found no legitimate input that the hunk over-rejects. Two defects sit next to the hunk. Neither produces a false clean.

## Findings

### F1 (Low, regression from b5d423f; in the sibling GitSource hunk, outside my assignment)

- A committed symlink at corpus/knowledge now reports `not_a_directory`. Base reported `symlink_rejected`. Exit stays 2.
- Cause: scripts/citing_set.py:357-358 tests `path == CORPUS_DIR` before the symlink test at :359-360.
- Evidence: probe2.jsonl, case G03. New gate: `["not_a_directory"]`, exit 2. Base gate: `["symlink_rejected"]`, exit 2. The working-tree twin W17 gives `symlink_rejected` in both gates.
- Nothing catches it. The selftest argv never carries `--revision` (grep of real/selftest.out, no match). The counter checks the finding id only, not the reason.
- Prototype in a scratch copy (citing_set_fix.py, not applied to the lane): swap the two checks. G03 then gives `symlink_rejected`. G04 (committed blob) still gives `not_a_directory`. See fixrun/G03-committed-symlink-knowledge.json and fixrun/G04-committed-blob-knowledge.json.

### F2 (Low, pre-existing, reachable from corpus_files, not fixed by the commit)

- A corpus nested about 990 directories deep crashes the working-tree walker. The result is an uncaught RecursionError, exit 1, and empty stdout. Base behaves the same.
- Cause: `_walk` (scripts/citing_set.py:263-284) recurses with no RecursionError handler. The commit adds one only to load_json_document (:401).
- Evidence: probe2.jsonl case W14 (depth 1100) and probe3.jsonl cases W23 at depth 995 and 1005. Each run exits 1 with stderr `RecursionError: maximum recursion depth exceeded`, in both gates. Depth 985 is clean in both gates.
- Impact: exit 1 is the "failed" code, so a caller that reads exit codes misreads a crash. No false clean results.
- Prototype: wrap the `_walk` call at :258 in try/except RecursionError, raising InputInvalid("corpus_directory_too_deep"). W14 and depth 995 then exit 2 with JSON. Depth 985 and the committed depth-1100 case (G07, Git path, no recursion) stay clean. See fixrun/*.json. The new reason label needs a docstring line.

## Claim check

| Shape (probe id) | Base | b5d423f | Result |
|---|---|---|---|
| corpus absent (W02) | clean | exit 2, corpus_directory_missing | fixed |
| corpus empty directory (W03) | clean | exit 2, corpus_empty | fixed |
| only empty subdirectories (W04); nested empty a/b/c (W05) | clean | exit 2, corpus_empty | fixed |
| corpus is a dangling symlink (W18) | clean | exit 2, corpus_directory_missing | fixed |
| absent at HEAD but present in working tree (G02) | clean | exit 2, corpus_directory_missing | fixed |
| blank --revision, absent corpus (G06; adjacent main hunk) | clean | exit 2, revision_not_found | fixed |
| committed corpus/knowledge as blob (G04) | failed, exit 1 | exit 2, not_a_directory | fixed |
| subdirectory mode 000 (W10); unreadable file (W11); directory without search (W12); corpus parent mode 000 (W22); escaping symlink (W19) | exit 2 | exit 2 | unchanged, refused |
| FIFO in corpus (W09) | exit 2, no hang | exit 2, no hang | unchanged |

Controls, all clean in both gates: W01 cited file; W06 cited in a subdirectory; W07 dotfile; W21 cited file plus empty subdirectories; W13 depth 960; W23 depth 985; G01 committed corpus; G07 committed depth 1100.

Real lane input, no over-rejection: population .ufo/waves/round-26/population.json (32 rows), ledger .ufo/waves/round-27/complete-ledger.json, 26 corpus files. Working tree of the clone, revision b5d423f, and revision 22c1669: new and base output are byte-identical (diff exit 0 for each). Verdict clean, citingPairs 58 equals ledgerPairs 58.

Official counter, run from the lane path with --root set to my clone and --scratch set to my scratch directory:
- `--revision b5d423f...`: exit 0, 15/15 (defects 11/11, controls 4/4). Matches the claim.
- `--revision 22c1669...`: exit 1, 4/15 (defects 0/11, controls 4/4). Matches the claim.

Selftest, `python3 -B scripts/citing_set_selftest.py --root .` in the clone: exit 0, all 29 fixtures ok. A fixture scan found no fixture without corpus files.

## Informational

- I1: a corpus parent that is a regular file (W15) reports corpus_directory_unreadable (ENOTDIR), not not_a_directory. Base is identical. Label nit.
- I2: a corpus holding only `.gitkeep` (W08) is clean in both gates. The rule is "at least one regular file", which matches the contract wording. Decision for the L1: state it in the docstring or tighten the rule.

## Residual risk and verification gaps

- The lsp device is not in this seat's tool inventory. Caller checks used text grep (literal fallback), not semantic proof.
- The prototype was not run through the selftest or the counter. Only the ten probe trees were run. The L1 must rerun the counter after applying any fix.
- Not probed: filesystems with unknown d_type. There, is_symlink or is_file would stat each entry and could raise an uncaught OSError inside _walk. Also not probed: non-UTF-8 files in the corpus (pre-existing) and a nested .git inside the corpus.
- Not checked: whether any recorded historical verdict used a revision with no corpus/knowledge. Such a revision would now read could-not-evaluate.
- Other hunks (population_id_unreachable, _require_top_level, the parser flag) were reviewed only through the runs above.
- The clone is pinned at b5d423f. Lane HEAD may have moved since.

## Tooling record

No installs or upgrades. Used /usr/bin/python3 3.14.8, system git, and coreutils. Read ~/.omp/agent/RULES.md. No pacman calls.

## Commands and exit codes

- `git clone -q <lane> <clone>`: exit 0, clone HEAD b5d423f.
- `python3 -B probe2.py > probe2.jsonl`: exit 0, 54 records.
- `python3 -B probe3.py > probe3.jsonl`: exit 0, 10 records.
- Real-lane runs (working tree; revision b5d423f; revision 22c1669), new and base: each exit 0, each diff exit 0.
- Official counter at b5d423f: exit 0. At 22c1669: exit 1 (the expected failing run).
- Selftest in clone: exit 0.
- Prototype runs (fixrun): as listed in F1 and F2.

Scratch evidence: /fast/scratch/hyaku/kake-r28a3/w1/ReviewCorpusMissingEmpty/ (probe2.py, probe2.jsonl, probe3.py, probe3.jsonl, real/, counter-b5d.json, counter-22c.json, real/selftest.out, citing_set_fix.py, fixrun/).
