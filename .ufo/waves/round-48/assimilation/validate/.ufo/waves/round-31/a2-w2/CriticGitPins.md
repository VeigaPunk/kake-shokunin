# CriticGitPins — C1 N2/N3, Git binding of setup and gate (round 31, attempt 2, wave 2)

Seat: KakeR31a2.CriticGitPins (critic, leaf). Axis judged: operability. Sandbox: /fast/scratch/hyaku/kake-r31/a2-w2/CriticGitPins/.
Clones: `clone` at fde133ab48086bb9a06911b4ab045e2ad9086347, `clone-base` at f1ffb81738c92c0537b99b30970143ab9419f990. TMPDIR=$S/tmp. git 2.56.0. No installs.
Gate scripts/citing_set.py is byte-identical at both commits (sha256 dbfade45...7b7f02); runner differs (base 9f2d1ecb..., landed 5371530d...).

## Verdict summary
- Fixtures 36, 37 and 45 behave exactly as at base: no regression.
- `git --git-dir=X --work-tree=Y init` creates the repository at <copy>/.git as expected, with no core.worktree, and leaves an enclosing repository untouched.
- The gate ceiling (GIT_CEILING_DIRECTORIES=cases_root) does not break legitimate cases whose root is a subdirectory, including a three-level root a/b/c.
- One fixable defect: a `:` in --tmpdir silently disables the ceiling (Git splits the variable on `:`), and the gate reads an enclosing repository again. This is the same leak that exists at base. Severity is low: the gate only reads, no fixture reaches it today, and the default tmpdir has no colon.

## 1. Full runner, base and landed (per-case results compared)
`cd clone-base && python3 -B scripts/citing_set_selftest.py --root . --tmpdir $S/run-base > $S/run-base.json` exited 0: clean, 45/45.
`cd clone && python3 -B scripts/citing_set_selftest.py --root . --tmpdir $S/run-fde > $S/run-fde.json` exited 0: clean, 45/45.
I compared the tuple (ok, reason, actual) for each of the 45 cases: 0 differ.
- 36-revision-not-found: both runs exit 2, [input_invalid, revision_not_found].
- 37-root-not-repository-top-level: both runs exit 2, [input_invalid, root_not_repository_top_level].
- 45-repeated-revision-abbreviated: both runs exit 64, findings [].
Verdict: no regression. Coverage caveat: 36 and 45 do not test the Git binding. 36 fails for any repository and 45 is an argparse usage error. 37 only shows that some commit exists at the copy root. No shipped fixture runs a positive `--revision HEAD` case, so I added synthetic ones in section 3.

## 2. Setup Git commands (git_command, git_env): probes PA, PB, PC
Script: $S/probes.sh. Output: $S/probes.out. I ran `bash $S/probes.sh` and it exited 0.
- PA: I imported the landed runner and called apply_setup([git_init, git_commit]) on $P/enc/cases/w, where $P/enc is an enclosing empty repository. The command was `git --git-dir=<w>/.git --work-tree=<w> -c core.hooksPath=/dev/null init -q` with ceiling <enc>/cases. Results:
  - <w>/.git is a directory.
  - Local config is exactly core.bare=false, core.filemode=true, core.logallrefupdates=true, core.repositoryformatversion=0. There is no core.worktree.
  - `git -C <w> rev-parse --show-toplevel` returns <w>.
  - The HEAD tree is corpus/a.md.
  - The enclosing repository has 0 commits and 0 index entries.
  - Verdict: the repository is created where expected.
- PB: apply_setup([git_commit]) with no init inside the enclosing repository raised "git_commit needs the repository created by git_init". The enclosing repository still had 0 commits and 0 index entries. The apply-time guard holds behind the load-time refusal.
- PC: I ran raw `git --git-dir=X --work-tree=Y init` two ways.
  - With Y equal to the parent of X: exit 0, no core.worktree.
  - With Y elsewhere: core.worktree=Y gets written.
  - The runner always passes Y = realpath(copy) and X = Y/.git (citing_set_selftest.py:434-438), so it is always the first form.

## 3. Gate ceiling with subdirectory roots: probe PD
I built five synthetic fixtures in $P/fixtures:
- a: fixture 01 plus git_init, git_commit and --revision HEAD.
- b: fixture 02 plus the same Git setup.
- c: fixture 01 placed under root a/b/c, git_init at the copy root, --revision HEAD.
- d: root a/b/c with no Git.
- e: root a/b/c with --revision HEAD and no git_init.

I ran each runner with `--fixtures $P/fixtures` in three environments:
- plain: tmpdir not in any repository.
- enclosing: tmpdir inside a committed repository $P/encl.
- hostile: as enclosing, plus inherited GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE and GIT_OBJECT_DIRECTORY pointing at encl, and GIT_CEILING_DIRECTORIES=/nonexistent.

Every run exited 1 with 4/5 passing. The failure is always e, and it is my own malformed expected.json (ids-only pairs). Its observed reason is what matters here.

| Case | Expected outcome | Observed (base and landed, all three environments) |
|---|---|---|
| a | exit 0, clean | pass |
| b | exit 1, unadjudicated_citing_pair | pass |
| c | root_not_repository_top_level | pass |
| d | working-tree mode, clean | pass |

So discovery from a/b/c still climbs to the copy-root .git. The ceiling breaks no legitimate subdirectory root.

Case e reasons:

| Runner | plain | enclosing | hostile |
|---|---|---|---|
| base | revision_not_found | root_not_repository_top_level | root_not_repository_top_level |
| landed | revision_not_found | revision_not_found | revision_not_found |

At base, the gate escaped the case copy and bound to $P/encl. The landed ceiling contains it.
The enclosing repository had 1 commit and index `z` before and after: nothing was written to it.
PE: the full 45-case landed runner in the hostile environment, with tmpdir $P/encl/full, exited 0: clean, 45/45. The enclosing repository was unchanged.

## 4. Counterexample: a colon in --tmpdir defeats the ceiling (probe PF)
- With GIT_CEILING_DIRECTORIES=$P/encl/co:lon/citing-set-selftest/cases, `git rev-parse --show-toplevel` from cases/nogit printed $P/encl, an escape. The control path without a colon printed "fatal: not a git repository".
- The landed runner with `--tmpdir $P/encl/co:lon2 --fixtures $P/fixtures` reported case e as root_not_repository_top_level. This is the base leak, so the landed fix is lost.
- The full 45-case run with `--tmpdir $P/encl/co:lon` exited 0: clean, 45/45. No shipped fixture reaches the gap.
- Evidence: citing_set_selftest.py:694 (gate ceiling `str(cases_root)`) and :430 (setup ceiling). The setup side is harmless because every setup command names --git-dir and --work-tree. The module docstring (citing_set_selftest.py:57-62) claims the ceiling without this limit.
- Impacted axes: operability. Wrong provenance is read-only: the gate binds to a foreign repository's blobs.
- Smallest safe correction: in main, return cannot_evaluate when `os.pathsep in str(cases_root)`, because Git has no escape for `:` in this variable. Optionally add a hostile spec for a case with --revision and no git_init. Today load_case_setup accepts that shape (case e), and only the ceiling contains it.

## Not verified
- Behaviour on a Git version other than 2.56.0.
- GIT_DISCOVERY_ACROSS_FILESYSTEM and mount boundaries.
- Inherited GIT_CONFIG_SYSTEM or GIT_CONFIG_GLOBAL reaching the gate. The gate's GIT_LOCAL_ENV list does not strip them; I did not probe them.
- I did not run the hostile selftest or the C1 counter; other seats own those.

Evidence files (sandbox): $S/probes.sh, $S/probes.out, $S/run-base.json, $S/run-fde.json, $S/probe/*.json, where S=/fast/scratch/hyaku/kake-r31/a2-w2/CriticGitPins and P=$S/probe.
