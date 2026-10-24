# ReviewBlankRevision — C1 repair, `--revision` dispatch hunk (r28a3 wave 1)

Scope: `git diff 22c1669c1fec83d1a0769de6b9ce686c75657e66 b5d423fc02057f67a6f3a255808313ce40d29069 -- scripts/citing_set.py`
(60+/13-), focused on the None-comparison change and the revision-path hunks it feeds.
Base = 22c1669 (`if arguments.revision:`, citing_set_base.py:650), fix = b5d423f
(`if arguments.revision is not None:`, citing_set_fix.py:697). Line numbers below are at b5d423f unless marked base.

## Verdict

The hunk does what C1 claims for the blank-revision family, and I found no over-rejection
of legitimate input on any path I exercised. Three findings sit on adjacent hunks of the
same repair; one is a genuine false-rejection (MEDIUM), two are LOW judgment calls.

## Findings

### F1 MEDIUM — ambient `GIT_WORK_TREE` falsely rejects a valid `--revision` run
- `_require_top_level` (citing_set_fix.py:295-310) runs `git rev-parse --show-toplevel`
  with the inherited `os.environ`. `--show-toplevel` honors `GIT_WORK_TREE`, so any stale
  exported value rejects a root+revision pair that is in fact correct.
- Evidence (same invocation, valid fixture `full` at its own top level):
  - base: exit 1, verdict `failed`, c=0 l=1 (env shifted the worktree, but the run processed)
  - fix: exit 2, `could-not-evaluate`, `input_invalid:root_not_repository_top_level`
- Benign `GIT_DIR=<root>/.git` passes the check (exit 0 clean), so the hazard is
  `GIT_WORK_TREE` (and any env that moves `--show-toplevel`).
- The lane counter cannot see this: `.ufo/waves/round-28/c1_interface_count.py` strips
  `GIT_*` via `GIT_ENV` before every run. An operator wrapper that exports `GIT_WORK_TREE`
  (or a hook context that sets it) gets exit 2 on every `--revision` run.
- Recommendation: pass a scrubbed env (drop `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`,
  `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_COMMON_DIR`) to the
  three git subprocess sites in `GitSource`, mirroring the counter's own `GIT_ENV`.

### F2 LOW — bare repository + `--revision` is now rejected (over-rejection candidate)
- `git clone --bare full bare.git`, then `--revision HEAD`:
  - base: exit 0 `clean`, c=1 l=1 — a bare clone serves blobs fine
  - fix: exit 2 `could-not-evaluate`, `input_invalid:root_not_repository_top_level`
- The rejection is a side effect of `rev-parse --show-toplevel` failing on a bare repo
  ("must be run in a work tree"), not a deliberate bare rule. The only contract cover is
  the new docstring line "a `--revision` root that is not the top level of its Git
  repository" (citing_set_fix.py:64-66 region, Findings section).
- The counter has no bare case, so this behavior is scorecard-invisible. L1 judgment:
  declare bare out of contract explicitly, or accept it (`rev-parse --is-bare-repository`
  true and `--git-dir` resolving to root).

### F3 LOW — the new root-identity guarantee checks worktree identity, not object-store identity
- With ambient `GIT_DIR` naming a second repository, `_resolve` (:313-325) and `_git`
  (:327-338) read that repository's objects while `_require_top_level` still passes
  (`--show-toplevel` derives the worktree from cwd under `-C root`).
- Probes: hostile `GIT_DIR` to a same-shaped repo → exit 0 `clean` c=1 l=1 (evaluated the
  wrong object store, indistinguishable verdict); hostile `GIT_DIR` to a repo without
  corpus/docs → exit 2 `git_command_failed`; working-tree mode with hostile `GIT_DIR` →
  exit 0 clean (no git involved, correct).
- Identical in base and fix — pre-existing, not a regression, and the observed outcomes
  were safe — but the docstring guarantee reads stronger than the check enforces.

## Confirmed behaviors — the hunk in scope (fixture `full`: clean worktree, corpus cites S001, ledger pairs S001)

| case | base | fix |
|---|---|---|
| `--revision ""` | exit 0 `clean` c=1 l=1 (silently measured the working tree — the routed defect shape) | exit 2 `could-not-evaluate`, c=0 l=0, `input_invalid:revision_not_found` |
| `--revision=` | exit 0 `clean` c=1 l=1 | exit 2, same finding |
| `--revision "   "` | exit 2 `revision_not_found` (citing_set_base.py:274 — already handled) | exit 2, unchanged |
| `--revision <40 zeros>` | exit 2 `revision_not_found` | exit 2, unchanged |
| no `--revision` (worktree) | exit 0 `clean` c=1 l=1 | exit 0 `clean` c=1 l=1 — no over-rejection |
| `--revision HEAD` / `<sha>` | exit 0 `clean` c=1 l=1 | exit 0 `clean` c=1 l=1 — no over-rejection |
| `--revision` (no value) | exit 64 usage JSON (EXIT_USAGE, citing_set_fix.py:103) | exit 64, unchanged, out of hunk |

The fix's rejection path emits the contracted JSON (verdict, citingPairs, ledgerPairs,
findings all present and parsed by my harness) and exits 2. This is exactly the C1
contract: unusable input yields the JSON report + exit 2, never a silent clean.

## Revision + working-tree-only (the fourth assigned case)

- Corpus only untracked in the worktree, committed tree lacks `corpus/knowledge`:
  - base + empty ledger: exit 0 **`clean` c=0 l=0** — the vacuous-clean defect, confirmed at base
  - base + pair ledger: exit 1 `failed` (misleading verdict, not clean)
  - fix, both ledgers: exit 2 `could-not-evaluate`, `input_invalid:corpus_directory_missing` (:365)
- Documents only untracked (population/ledger absent from the pinned tree), corpus committed:
  both base and fix exit 2 `git_command_failed` — revision semantics require the documents
  in the pinned tree; correct, not an over-rejection.

## Adjacent repair hunks exercised (supporting evidence)

- `corpus/knowledge` stored as a regular file in the pinned tree: base exit 0 `clean`
  (scanned the file as a zero-citation corpus document); fix exit 2 `not_a_directory`
  (:358-359). Closed a vacuous-clean.
- Empty working-tree `corpus/knowledge`: base exit 0 `clean`; fix exit 2 `corpus_empty`
  (:258-260).
- Nested root (`--root` inside a repo whose top is the parent) + `--revision HEAD`:
  base exit 0 `clean` c=1 l=1 but measured the parent level's documents (entry cites S001
  while `--root` named `inner/`, whose own ledger is S002) — a real level-hijack; fix
  exit 2 `root_not_repository_top_level`. Worktree mode at the nested root: exit 0 clean
  on both revisions — working-tree users are not over-rejected.

## Commands and exit codes

- `git -C <lane> diff 22c1669.. b5d423f -- scripts/citing_set.py` → exit 0
- `git show <rev>:scripts/citing_set.py` extractions to scratch → exit 0
- `python3 -B run_cases.py` (15 cases × 2 revisions, `timeout 20` per gate run) → exit 0, no run timed out
- `python3 -B probe_extra.py` (corpus-as-file, empty corpus, GIT_DIR variants) → exit 0
- hostile-GIT_DIR discrimination probe (heredoc) → exit 0
- No installs performed (tooling directive: none needed; pacman untouched). Nothing in the
  lane repo mutated; all fixtures and gate copies under
  `/fast/scratch/hyaku/kake-r28a3/w1/ReviewBlankRevision/` with `TMPDIR=./tmp`.
  Harness: `run_cases.py`, `probe_extra.py` in that directory.

## Residual risk and verification gaps

- I did not rerun the lane counter `c1_interface_count.py`; the 15/15 claim at b5d423f is
  the planner's. My probes verify the hunk's behavior directly, not the counter's coverage.
- `--revision " HEAD "` (padded real rev) untested; `_resolve` passes the unstripped string
  to `rev-parse` (:317-325), expected `revision_not_found`.
- gitlink (mode 160000) at `corpus/knowledge`, non-UTF8 corpus blobs: not exercised
  (out of hunk scope; code-read only).
- F1/F2 are invisible to the lane counter by construction (`GIT_ENV` stripping, no bare or
  env fixtures). Making them scorecard-visible needs new counter cases — L1 decision.
