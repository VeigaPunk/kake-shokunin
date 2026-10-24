# Review: GitSource._require_top_level (C1 hunk, b5d423fc02 vs 22c1669c1f)

Reviewer: KakeR28a3.ReviewGitTopLevel (leaf, w1a3). Scope: the `GitSource.__init__` /
`_require_top_level` hunk in scripts/citing_set.py. Axis: operability.
Diagnostics note: no LSP device is available in this seat (no `lsp` tool in inventory), so
caller/definition checks used `git grep` at the pinned revision plus behavioral probes; grep
output below is presented as caller evidence, not semantic proof.

## The hunk under review (b5d423f, scripts/citing_set.py:292-311)

- `__init__` calls `self.revision = self._resolve(root, revision)` (:294) then
  `self._require_top_level(root)` (:295).
- `_require_top_level` (:297-311): `git -C <root> rev-parse --show-toplevel`; OSError ->
  `git_unavailable`; nonzero rc, empty output, or `realpath(top) != realpath(root)` ->
  `InputInvalid("root_not_repository_top_level", root, "root")`.
- Sole caller of `GitSource`: `main` at :698 (`--revision` is not None); introspected at :590.
  No other caller; `git grep` at b5d423f over `scripts/` returned only :287/:295/:298/:310/:590/:698.

## Verdict

The hunk does what C1 claims for the canonical cases, with one environment-gated bypass and
one narrow over-rejection. Counter rerun at b5d423f: 15/15 (11/11 defect, 4/4 control), exit 0.

## Findings

### F1 — MEDIUM — ambient GIT_DIR/GIT_WORK_TREE defeat both directions of the check

`sandbox/cases.sh` lines `env-bypass-root-not-repo` and `env-false-reject-gitdir-dot`:

- False clean: root = plain directory with no `.git` anywhere above it, caller exports
  `GIT_DIR=<repo>/.git GIT_WORK_TREE=<root>` -> gate exits 0, verdict `clean`. A root that is
  not a repository measured clean, because `rev-parse --show-toplevel` reports
  `$GIT_WORK_TREE` and the realpath equality then holds against an env-chosen value. All
  content (`show`, `ls-tree`) likewise comes from `$GIT_DIR`, so the measurement is of a
  different surface than the named root — the exact wrong-surface false-green class A7 exists
  to kill, reachable without touching the arguments.
- False rejection: caller with `GIT_DIR=.` (git hooks, some CI wrappers) on a valid top-level
  root -> exit 2 `revision_not_found`. `-C root` chdirs first, so `.` resolves inside the root
  and discovery is poisoned.

Both stem from inheriting `os.environ` in the `subprocess.run` calls (:301-305, :315-321).
Suggested direction (not applied): run the probes with `GIT_DIR`/`GIT_WORK_TREE`/
`GIT_INDEX_FILE`/`GIT_CEILING_DIRECTORIES`/`GIT_CONFIG_*` stripped from the child env.
No observed fleet invocation sets these (the counter's GIT_ENV only sets identity/config
variables), so this is robustness, not a live mis-measurement; severity reflects that the
declared mechanism "root must equal `git rev-parse --show-toplevel`" is only true modulo env.

### F2 — LOW — bare-repository root now refused (capability regression vs base)

`bare-repo-repair`: `--root bare.git --revision HEAD` -> exit 2
`root_not_repository_top_level` because `--show-toplevel` fails in a bare repo
(probe: `fatal: this operation must be run in a work tree`, rc=128). `bare-repo-base` on the
identical case at 22c1669c: exit 0 `clean`. Every GitSource read (`rev-parse --verify`,
`ls-tree -rz`, `show rev:path`) works from a bare root, and the code's own rationale ("Git
paths are top-relative") holds there, so the implementation is narrower than its rationale.
Harmless if no fleet caller ever passes a bare repo (none observed); recorded as honest
over-rejection of otherwise-legitimate input, the failure mode this review was asked to rule out.

### F3 — INFO — ordering: `_resolve` before `_require_top_level`

For a non-repo root (`nonrepo-root-repair`) and for a nested root with an unknown revision
(`subdir-root-badrev-repair`), the reported reason is `revision_not_found`, not
`root_not_repository_top_level`; the top-level check never runs. Exit (2), verdict
(`could-not-evaluate`), and finding id (`input_invalid`) are identical, and the counter's
`judge` checks only those (c1_interface_count.py:128-156), so the contracted observable is
unaffected and A6/A7 still pass. Diagnostics-only nit: a non-repo root answers "revision HEAD
not found", which can mislead. No change requested.

### F4 — INFO — `os.fsdecode(done.stdout).strip()` (:307)

`--show-toplevel` output is whitespace-stripped; a repository whose top-level path ends in a
space or newline would be falsely rejected via realpath mismatch. Pathological; not exercised.
`-z` framing is not offered for `--show-toplevel`, so strip is the pragmatic choice; noted for
completeness, no change requested.

## Cases that must NOT over-reject — all clean, exit 0

`git-clean-repo-top`, `git-clean-symlink-root` (1 symlink), `git-clean-symlink2-root` (symlink
chain), `git-clean-worktree-gitfile` (linked worktree, `.git` is a file — handled with no
special parsing), `git-clean-trailing-slash`, `git-clean-relative-root` (`./repo-top`), plus
base sanity `base-sanity-repo-top`. Mechanism probe: `git -C link-top rev-parse
--show-toplevel` prints the physical path (`/fast/scratch/.../cases/repo-top`), and
`realpath(root)` normalizes the symlinked argument to the same string — the realpath
comparison is what makes symlinked roots accept.

## Cases that must reject — all exit 2, `could-not-evaluate`, `input_invalid`

`subdir-root-repair` -> `root_not_repository_top_level` (full JSON probe captured; scope
`root`); identical case at base (`subdir-root-base`) returned exit 0 `clean`, demonstrating the
wrong-surface false green this hunk fixes; `gitdir-as-root-repair` (root = repo/.git) ->
`root_not_repository_top_level`; `symlink-subdir-root` (symlink into a subdirectory) ->
`root_not_repository_top_level`; `nonrepo-root-repair` -> `revision_not_found` (see F3), never
clean.

## Commands and exit codes (all run in sandbox, TMPDIR under sandbox)

- `git -C <lane> diff 22c1669c1f b5d423fc02 -- scripts/citing_set.py` — exit 0.
- `git -C <lane> show <rev>:scripts/citing_set.py > sandbox/citing_set_{base,b5d423f}.py` — exit 0;
  working-tree drift check `git diff --stat b5d423fc02 -- scripts/citing_set.py` — empty.
- `bash sandbox/cases.sh` — exit 0; 17 labeled outcomes + 4 probes as quoted above.
- `python3 -B <lane>/.ufo/waves/round-28/c1_interface_count.py --root <lane> --revision
  b5d423fc02 --scratch sandbox/counter-scratch` — exit 0; `15/15`, `defect 11/11`,
  `control 4/4`, no failing case ids (`sandbox/counter-b5d423f.json`).
- `git grep -n "GitSource|_require_top_level|root_not_repository_top_level" b5d423fc02 -- scripts/` — exit 0 (caller evidence above).
- Lane untouched except this report; no git/jj mutation; no pacman transaction; no installs
  (none needed; git 2.56.0, python3 as shipped).

## Residual risk and verification gaps

- F1 is environment-gated: I did not find any current fleet caller that exports GIT_DIR /
  GIT_WORK_TREE, so I cannot demonstrate live impact — the finding is about the reachable
  bypass, not an observed mis-run.
- Fixture gap: no fixture in `scripts/fixtures/citing-set` pins `root_not_repository_top_level`
  (grep at b5d423f shows the reason only at :310); the counter's A7 is the sole automated check
  and does not pin the reason code, so a future refactor could silently change the reason while
  keeping 15/15.
- Not verified: Windows/unusual-filesystem behavior, root paths with trailing whitespace or
  newline, `core.worktree` configurations, dubious-ownership repositories (base behaves the
  same, so no regression claim either way), and I did not fuzz `--revision` values beyond the
  blank/unknown cases already covered by A6 and the counter.

Evidence: sandbox root /fast/scratch/hyaku/kake-r28a3/w1/ReviewGitTopLevel/ (cases.sh,
cases/, counter-b5d423f.json, citing_set_b5d423f.py, citing_set_base.py).
