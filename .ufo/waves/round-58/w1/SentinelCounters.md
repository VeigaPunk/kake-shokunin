# SentinelCounters

Adversarial safety review of the three round-58 counters (`c58_receipt_rewrites.py`, `c58_resolver_cases.py`,
`c58_quote_truth.py`) and `scripts/id_resolver.py`, at lane HEAD `cc8da16` (tool last touched at `32754df`).
Every claim below was run in fixture repos under `/fast/scratch/hyaku/kake-r58/SentinelCounters` (git 2.56.0,
Python 3.14.8); nothing was run against the lane, siblings, jj state or the lane index. Scratch was deleted after
the receipts were copied out. Axes: argument injection, hostile `.git/config`, inherited `GIT_*`, symlinks,
write/delete containment, fixture placement.

## FINDINGS:

### F1 MEDIUM — `c58_quote_truth.py` does not scrub inherited `GIT_*`: the measured repository is env-selectable
`c58_quote_truth.py:101-102` (`git()`) and `:118-119` (`show_bytes()`) call `subprocess.run(["git", "-C", root, …])`
with the inherited environment. Every other consumer of git in this fleet scrubs it — `c58_receipt_rewrites.py:65`
(`clean_env`), `c58_resolver_cases.py:54` (`env`), `id_resolver.py:62-65` (`_spawn`) — so the omission is an outlier,
not a design choice. `GIT_DIR` overrides `-C`: the tool then evaluates one repository while printing the other's path.

Reproduction (fixtures `envA` = repo without a registry, `envB` = repo with one):
```
python3 c58_quote_truth.py --root envA --revision <B's head>            # GIT_DIR=envB/.git exported
C3 quote-truth 0/8 met=False …            # full 8-condition evaluation of envB under --root envA
python3 c58_quote_truth.py --root envA --revision <A's head>            # GIT_DIR=envB/.git exported
unevaluable: revision '…' does not resolve in '…/envA'  EXIT=2  # message blames the root, git used envB
```
Impact: with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_CONFIG_*` exported (git hooks, worktree wrappers,
`direnv`, a jj/git shim), the C3 verdict describes a repository the operator did not name; C5 body pins and C8 mirror
bytes are read through the same helper.
Fix: give `git()`/`show_bytes()`the same `env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}` filter
(or reuse `clean_env()`), and add the fixture already present in `id_resolver.py`
(`case_git_env_is_scrubbed`) as a C3 condition.

### F2 MEDIUM — `id_resolver.py --revision` reads committed symlinks as text bodies: a symlink under `corpus/knowledge/` turns red into green
`id_resolver.py:144` lists `ls-tree -r --name-only` (names only, no mode) and `:151` reads `git show rev:rel`; for a
`120000` entry git returns the **link target string**, not the linked file. The worktree path has a realpath
containment check (`:158-180`); the revision path has no symlink handling at all, and `--revision` is the mode the gates
use (C2 P7).

Reproduction (fixture `syml2`: `corpus/knowledge/linked.md -> ../notes.md`, `corpus/notes.md` cites S999, registry holds
only S001):
```
python3 id_resolver.py --root lane --fleet .            # worktree: DANGLING S999 …  ids_cited=1 dangling=1  rc=1
python3 id_resolver.py --root lane --revision HEAD --fleet .
                                                        # revision: ids_cited=0 ids_resolved=0 dangling=0  rc=0
git show HEAD:corpus/knowledge/linked.md                 # => "../notes.md"
```
The same mechanism forges citations: a symlink whose target string contains an id (`odd.md -> S777-target.md`) printed
`DANGLING S777 cited-by=corpus/knowledge/odd.md` in revision mode while the worktree run was unevaluable. A broken
symlink also only makes the worktree run exit 2.
Impact: a lane can keep every dangling citation in a file one directory above `corpus/knowledge/`, link to it, and
measure green at `--revision`; the C2 claim "F1 quoted paths closed" is silent about this neighbouring case.
Fix: switch to `ls-tree -r -z` and parse the mode, skipping `120000` (or resolving it inside the tree); when a symlink is
kept, apply the same containment rule the worktree path applies.

### F3 LOW — `c58_quote_truth.py --base` is never resolved: an empty value reads the git **index**, not a commit
`c58_quote_truth.py:621` accepts `--base` and `:283` uses it unchanged in `show(root, base_rev, REGISTRY)`, i.e.
`git show "<base>:corpus/SOURCES.md"` (`:107-119`). With an empty value the argument becomes `":corpus/SOURCES.md"`,
git's index syntax: C3's `base_rows` and C8's "mirror equals the base-revision registry" test then read staged bytes.
The CLI stays evaluable (`rc=1`, no usage error), so `--base "$BASE_REV"` with an unset variable silently downgrades
the base evidence.

Reproduction (fixture `fx8`: HEAD registry = {S001,S002}, mirror = {S001}, index staged to the mirror):
```
--base <base sha>   C8: "mirror bytes differ from the base-revision registry"
--base ''           C8: (that note absent; C3 facts base_rows 1 instead of 2)
python3 c58_quote_truth.py --root fx8 --revision <rev> --base=   → runs, EXIT=1
```
Fix: resolve `--base` through `rev-parse --verify ${base}^{commit}` exactly like `--revision` and reject empty; the
`--revision` value is resolved, the base should be too.

### F4 LOW — `c58_quote_truth.py` validates `--revision` but measures the raw string, so a symbolic name is re-resolved at every git call
`:635` passes `args.revision` (not the resolved commit) into `run_checks`, which issues ~20 separate `git show`/
`git ls-tree` calls. A ref moved by a concurrent gate/agent changes the evidence mid-run: `show(root,"movable",…)`
returned `REV-A` then `REV-B` in one process after `git branch -f movable HEAD`. `id_resolver.py` and
`c58_receipt_rewrites.py` pin the resolved object id first; C3 does not.
Fix: `rev = resolve(rev_parse(...))` once in `main()` and pass that.

### F5 LOW — the registry is read without the containment check the knowledge tree gets
`id_resolver.py:125-138`: `lane_registry` opens `root/corpus/SOURCES.md` with `open(path)` and no realpath test, while
`knowledge_bodies` (`:158-180`) explicitly refuses a symlink that leaves the lane ("a symlink must not carry a citation
in from outside the lane"). The registry is the authority that turns citations green.
Reproduction (fixture `sym2`: `lane/corpus/SOURCES.md -> ../outside/SOURCES.md`, outside file adds row S888,
`corpus/knowledge/a.md` cites only S888): `ids_cited=1 ids_resolved=1 dangling=0` — the outside row resolves the
citation. Revision mode is safe here (a symlink blob parses as the target string, no rows), so the worktree mode is the
gap. Callers who clone an untrusted lane inherit the symlink.
Fix: realpath-contain the registry path (or `os.lstat` + reject symlinks) the way knowledge files are contained.

### F6 LOW — a `--root` that is not a repository silently resolves through an ancestor repository
All three CLI tools only run `git -C root` (`id_resolver.py:118-119`, `c58_quote_truth.py:101`,
`c58_receipt_rewrites.py:69`), so a subdirectory root measures its enclosing repo. Fixture `anc/` with
`anc/lane/` (not a repo) and revision from `anc`:
```
c58_receipt_rewrites.py --root anc/lane --revision <anc head>  → "ledger: … absent (0 entries)" EXIT=1
id_resolver.py --root anc/lane --revision <anc head>           → "registry absent at <rev>" (revision accepted)
```
Not a false green by itself, but it reports a *not-met/absent* verdict for a root that is not measurable instead of
exit 2, and it measures a tree the operator did not name. The three selftests already assert
`rev-parse --show-toplevel == realpath(root)` for their own fixtures (`id_resolver.py:313`,
`c58_resolver_cases.py:81-82`) — the CLI path skips that assertion. Fix: run the same check once per `--root` before
evaluating and return 2 on mismatch.

## NON-ISSUES:

1. **`--revision` argument injection (`--output=/x`, `--upload-pack=…`, `-q`, `--`, `--all`).** Two independent guards:
   argparse refuses a separate leading-dash token (`--revision --upload-pack=/bin/echo` → exit 64, "expected one
   argument"), and the `=` form reaches git but the tool appends `^{commit}` (`id_resolver.py:119`,
   `c58_receipt_rewrites.py:374`, `c58_resolver_cases.py:209`) or a `rev:` prefix (`id_resolver.py:127,151,206`;
   `c58_quote_truth.py:119`), so `git rev-parse --verify '--upload-pack=/bin/echo^{commit}'` fails rc=128
   ("Needed a single revision"). Measured: every CLI exits 2 (`c58_quote_truth.py` prints `EXIT=2`), and no
   `PWN*` file was created for the `--output=` values. Library callers (`evaluate`, `run_checks`) are protected by the
   same suffix rule. No `shell=True` anywhere (grep: none in the four files).
2. **Hostile `.git/config` executing code (`core.fsmonitor`, `core.pager`, `diff.external`, `diff.<d>.textconv`,
   `filter.*.smudge`, `core.hooksPath`, `core.editor`, committed `.gitattributes`).** A marker script wired to all of
   them fired 0 times for every command the four tools run: `rev-parse --verify`, `show rev:path`, `ls-tree -r
   --name-only`, `ls-tree -z … --`, `cat-file -e`/`cat-file blob`, `merge-base --is-ancestor`,
   `log --diff-filter=A --format=%H`, `log --reverse --no-renames --full-history -m --first-parent -z --name-status`.
   Only `git log -p -1` fires (4 calls: textconv + fsmonitor) — and no tool uses `-p`, `--ext-diff` or `GIT_EXTERNAL_DIFF`
   (grep: none). No command in the set refreshes the index or opens a pager, so the classic vector is unreachable.
3. **Inherited `GIT_*` in the other three tools.** With `GIT_DIR=<other repo>/.git` exported, `id_resolver.py`,
   `c58_receipt_rewrites.py` and `c58_resolver_cases.py` produced the same revision and the same exit code as in a clean
   environment (their `_spawn`/`clean_env`/`env` filter). `id_resolver.py` has a selftest case for it; F1 is the only
   gap.
4. **Symlinks in fixture dirs / out of the lane (worktree mode).** A symlinked knowledge *directory* pointing outside
   the lane is not descended and its file was not counted; a symlinked `.md` pointing outside was skipped
   (`ids_cited` unchanged, both cases). The one worktree gap is the registry (F5); the revision-mode gap is F2.
5. **Writing and deleting outside scratch.** Every write and delete target is a `tempfile.mkdtemp` result:
   `id_resolver.py:330,334` (`rmtree` of `mkdtemp`), `c58_resolver_cases.py:215,219`, `c58_receipt_rewrites.py:246,348`.
   Caller-supplied `--work` / `TMPDIR` are used only as `mkdtemp` **parents**. Measured: sentinel files in `--work`
   (`c58_resolver_cases.py --work <dir>`) and in `TMPDIR` (`c58_receipt_rewrites.py --selftest`) survived both runs;
   dir contents were unchanged. `c58_quote_truth.py` writes nothing at all (read-only). The only residue is a leak of
   one `mkdtemp` dir if `_repo` raises before the caller records it (`c58_receipt_rewrites.py:245`), cosmetic.
6. **Fixture repos inside the lane.** Every `git init`/`git add`/`git commit` call site is fed a mkdtemp-derived path:
   `id_resolver.py:304-330` (selftest), `c58_resolver_cases.py:78-90` (`repo()` under `work`),
   `c58_receipt_rewrites.py:245-262` (under `TMPDIR`). Both selftests verify `rev-parse --show-toplevel` equals their
   own directory before the first commit (`id_resolver.py:313`, `c58_resolver_cases.py:79`). Neither counter ran a
   mutating git command against `--root`: the lane is read only through `show`/`ls-tree`.
7. **Untrusted record content reaching a git argv.** Registry rows, ledger notes and `ls-tree` names never become a
   bare argv element: `cat-file blob` gets an object id taken from `ls-tree` metadata, ledger note pointers go through
   `rev-parse --verify <hex>^{commit}` or `<tip>:<path>`, and `ls-tree` uses `--` before the path
   (`c58_receipt_rewrites.py:77,152,155`). Constant pathspecs (`.ufo/waves`, `corpus/SOURCES.md`) carry no `:(magic)`.
8. **`--fleet` sibling symlink out of the fleet directory.** A `beta-shokunin` symlink to a repo outside `--fleet` is
   attributed as an owner (`owners=beta-shokunin`). Read-only, no external program fires (item 2); the fleet argument
   is by definition the set of lanes to consult, so this is accepted behaviour, not a containment break.
9. **`argparse` value shapes.** `--root` is checked with `os.path.isdir` before use (`id_resolver.py:881`), `--fleet`
   must be a directory (`evaluate`), `c58_resolver_cases.py` requires `--revision` (exit 64 otherwise). Unvalidated
   remaining inputs are `--base` (F3) and the raw `--revision` string (F4).

VERDICT: no code-execution path through the four tools (argument injection, hostile `.git/config`, pathspec/record injection all closed); two MEDIUM integrity defects remain — `c58_quote_truth.py` trusts inherited `GIT_*` (F1) and `id_resolver.py --revision` turns a committed knowledge symlink into a green (F2) — plus three LOW gaps (`--base` index read, unpinned revision, registry symlink escape, ancestor-repo resolution).
