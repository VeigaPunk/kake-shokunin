# CriticC1FollowUp: attack on C1 follow-up 8ecbefe (top-level check by `--show-prefix`)

Seat: KakeR28a3.CriticC1FollowUp (leaf critic, advisory). Axis attacked: operability.
Scratch: /fast/scratch/hyaku/kake-r28a3/res/CriticC1FollowUp (TMPDIR set there). Sandbox clone at 8ecbefe31b81462239c572fbe23d21404442a177.
Tools: git 2.56.0, Python 3.14.8. No installs, no network, no lane writes other than this report.

## Counter and selftest
- `cd kake-shokunin && python3 -B .ufo/waves/round-28/c1_interface_count.py --root . --revision 8ecbefe31b81462239c572fbe23d21404442a177 --scratch <S>/counter` exit 0: passed 15/15 (defects 11/11, controls 4/4); A7 nested root refused with `root_not_repository_top_level`. Output: <S>/counter-8ecbefe.json.
- The same counter at b5d423fc02057f67a6f3a255808313ce40d29069, exit 0, gave 15/15. The per-case observed outcomes are identical to 8ecbefe (`diff` exit 0).
- `cd <S>/clone && python3 -B scripts/citing_set_selftest.py --root . --tmpdir <S>/selftest-tmp` exit 0: verdict clean, 29 cases, 0 failed; gateSha256 6b83299d…7869 (= `git show 8ecbefe:scripts/citing_set.py`).

## Case table (every case runs `--revision HEAD`; columns: base 22c1669, b5d423f, 8ecbefe)
Harness: <S>/cases.py, which ran exit 0; raw results in <S>/cases.json. Gates were taken from `git -C kake-shokunin show <rev>:scripts/citing_set.py`. The nested fixtures follow A7: the top-level tree reads clean, while the nested tree cites S001 with no ledger pair, so a correct read of the nested tree is failed. Reading the top-level tree instead is a wrong-surface clean. "refuse" means exit 2 with root_not_repository_top_level, except R1 and E4, which are exit 2 with revision_not_found.

| Case | Want | 22c1669 | b5d423f | 8ecbefe |
|---|---|---|---|---|
| N1 `<repo>/sub` | refuse | 0 clean (false) | refuse | refuse |
| N2, K1, K2 top-level controls | 0 / 0 / 1 | as wanted | as wanted | as wanted |
| B1 bare repo, content clean | 0 clean | 0 clean | refuse (over) | 0 clean |
| B2 bare repo, content failed | 1 failed | 1 failed | refuse (over) | 1 failed |
| B3 `<bare>/refs` | refuse or 1 | 1 failed | refuse | 1 failed |
| T1 top level named `space ` | 1 failed | 1 failed | refuse (over) | 1 failed |
| T2 `<'spacenest '>/sub` | refuse | 0 clean (false) | refuse | refuse |
| T3 top level name ends in newline | 1 failed | 1 failed | refuse (over) | 1 failed |
| T4 `<repo>/'x\n'` nested | refuse | 0 clean (false) | refuse | refuse |
| L1 symlink to top level | 1 failed | 1 failed | 1 failed | 1 failed |
| L2 symlink to `<repo>/sub` | refuse | 0 clean (false) | refuse | refuse |
| L3 `<symlink to repo>/sub` | refuse | 0 clean (false) | refuse | refuse |
| W1 linked worktree top level (its HEAD failed, main HEAD clean) | 1 failed | 1 failed | 1 failed | 1 failed |
| W2 `<worktree>/sub` | refuse | 1 failed | refuse | refuse |
| G1 `<repo>/.git` (HEAD failed) | refuse or 1 | 1 failed | refuse | 1 failed |
| G2 `<repo>/.git/refs` | refuse or 1 | 1 failed | refuse | 1 failed |
| G3 `<nested repo>/.git` (top tree clean) | refuse or 0 | 0 clean | refuse | 0 clean |
| R1 directory that is not a repository | refuse | refuse | refuse | refuse |
| E1 GIT_DIR=`<repo>/.git`, root `<repo>/sub` | refuse | 0 clean (false) | 0 clean (false) | 0 clean (false) |
| E2 GIT_WORK_TREE=`<repo>/sub`, root `<repo>/sub` | refuse | 0 clean (false) | 0 clean (false) | 0 clean (false) |
| E3 GIT_DIR and GIT_WORK_TREE set, root `<repo>/sub` | refuse | 0 clean (false) | 0 clean (false) | 0 clean (false) |
| E4 GIT_DIR=`<other clean repo>/.git`, root is not a repository (its own content failed) | refuse | 0 clean (false) | 0 clean (false) | 0 clean (false) |
| E5 GIT_WORK_TREE=`<repo>`, root `<repo>/sub` | refuse | 0 clean (false) | refuse | refuse |
| E6, E7 GIT_DIR or GIT_WORK_TREE pointing at the root's own repo (controls) | 1 failed | 1 failed | 1 failed | 1 failed |

## Findings
1. **No new false clean comes from 8ecbefe.** Every case where 8ecbefe differs from b5d423f (B1–B3, T1, T3, G1–G3) reads the same tree that `--root <repo>` reads: the repository's own HEAD. The verdict matches that tree's content in every such case. Every nested case (N1, T2, T4, L2, L3, W2, E5) is still refused. The over-rejections of bare roots and of roots whose names end in a space or newline are fixed.
2. **Tradeoff, not a defect:** 8ecbefe now accepts the interior of a Git directory (`<repo>/.git`, `<repo>/.git/refs`, `<bare>/refs`). In each case it measures that repository's HEAD tree, which is the same surface as the repository itself, so I found no false clean. This acceptance is not mentioned in the new docstring at scripts/citing_set.py:298-304. If the contract is "work-tree top level or bare repository", the docstring should name this case or the gate should refuse it.
3. **Counterexample, a false clean that predates this commit:** E1–E4 return exit 0 `clean` at all three revisions. The gate passes the inherited environment to `git -C <root>` (scripts/citing_set.py:306-310, 320-325, 333-338 at 8ecbefe). So GIT_DIR or GIT_WORK_TREE overrides how Git finds the repository: `--show-prefix` prints empty, and `git show HEAD:population.json` reads the top-level tree, or in E4 a different repository altogether. 8ecbefe did not cause this; b5d423f's `--show-toplevel` check is fooled the same way. It is still an open way for C1's "nested or unreachable surface must not be clean" claim to give a false clean. [INFERENCE] Git hooks export GIT_DIR and GIT_INDEX_FILE, so running the gate from a hook against another root is a realistic way to trigger it.
   - Smallest safe correction (prototype at <S>/gates/gate-envfix.py, sha256 50e1ea5b…bd3bd): drop the variables that `git rev-parse --local-env-vars` lists (GIT_DIR, GIT_WORK_TREE, GIT_COMMON_DIR, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES, GIT_CONFIG*, GIT_PREFIX, and the rest) from the environment, then pass that environment as `env=` to the three Git subprocess calls in GitSource. Observed result: E1–E3 are refused with root_not_repository_top_level and E4 with revision_not_found, every other case gives the same result as 8ecbefe (E6 and E7 stay 1 failed), and the selftest in a copy of my clone exits 0 with 29 cases and 0 failed.
   - Impacted axis: operability (correctness of the C1 surface claim). Freshness is not affected.

## Not verified
- The counter was not run on the envfix prototype, because it only exports committed revisions. The prototype was checked with the case table and the selftest only.
- Not tested: submodule roots, `core.worktree` config, GIT_CEILING_DIRECTORIES, `safe.directory` ownership refusal, Windows paths, and non-UTF-8 root names.
- I did not check whether any lane caller (QUALITY or SKILL procedures) runs the gate with GIT_* variables set.
