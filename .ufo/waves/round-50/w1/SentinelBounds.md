# Sentinel bounds — round-50 counters `c50_quote_class.py` and `c50_durable.py`

Scope of this audit: the two frozen counting instruments only, their subprocess
surface, their read set, their write set, and their behaviour when the lane
root is not the kake-shokunin repository. Audited at wave-1 spawn, lane HEAD
family `9619af67…` → `33eec7f2…`. Both scripts were read in full and executed
against the two contract revisions plus a battery of hostile roots and
revisions.

## What they execute

Both counters are single-file Python 3 scripts run as
`python3 -B <script> --root <dir> --revision <rev> [--json <path>]`.

The only external process either spawns is `git`, via
`subprocess.run([...], capture_output=True)` — `shell=False`, fixed argv list,
no `PATH` search tricks beyond resolving the `git` binary itself:

- `c50_quote_class.py`: `git -C <root> show <revision>:<relpath>` only.
- `c50_durable.py`: `git -C <root> show <revision>:<relpath>` and
  `git -C <root> merge-base --is-ancestor <revA> <revB>`.

`<revision>` and `<root>` are passed as argv elements, never interpolated into
a shell string. A revision of `--all`, `--work-tree=/tmp`, or `""` is handed
to git literally; git rejects or ignores it and every read returns non-zero /
`None`. There is no shell-injection vector.

`git show <rev>:<path>` and `git merge-base` are plumbing commands. They do not
run hooks, do not invoke textconv or `filter.*` drivers, do not consult
`core.fsmonitor` or `core.pager`, and ignore `alias.show`/`alias.merge-base`.
Verified empirically: a scratch repo with `alias.show='!id'` and
`core.fsmonitor='echo pwned'` produced a normal `met=False` result with no
side output — the alias was not executed.

Because `git` is spawned in a real checkout, git's "dubious ownership"
(`safe.directory`) check applies to the lane. If the lane `.git` were owned by
a different user, every `git` call exits non-zero, every blob read returns
`None`, and the counter reports `met=False` (do-nothing). Failure direction is
fail-safe: permission errors can never produce a false `met=True`.

## Files read

All content comes from the git object store via `git show <rev>:<path>`.
No worktree file is ever opened. `COMMITTED_BYTES_ONLY = True` in
`c50_quote_class.py` is accurate.

`c50_quote_class.py` reads, per revision:

- `.ufo/waves/round-50/quote-classes.json`
- `corpus/lessons/round-50.md`
- `corpus/SOURCES.md`
- `corpus/knowledge/crawl-error-status-table.md`
- `.ufo/waves/round-49/sources/S273.txt` and `.raw.html`
- `.ufo/waves/round-49/sources/S274.txt` and `.raw.html`
- `.ufo/waves/round-50/sources/S286.txt` and `.raw.html`

`c50_durable.py` reads:

- `.ufo/waves/round-50/assimilation/order-proof.json`
- `.ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md`
- `.ufo/waves/round-50/assimilation/pre-append/census-argv.txt`
- `.ufo/waves/round-50/assimilation/pre-append/census-stdout.txt`
- `.ufo/waves/round-50/assimilation/pre-append/census-exit.txt`
- `.ufo/waves/round-50/wave-cite-proof.json`
- `.ufo/waves/round-50/wave-grant.txt`
- `.ufo/waves/round-50/dispatch-command.txt`
- `.ufo/waves/round-50/settlement.json`
- `corpus/SOURCES.md` (at `pre_rev` and at the measured revision)
- `LOG.md` (at `grant_rev` and at the measured revision)

plus `git merge-base --is-ancestor` for ancestry of `pre_rev` and `grant_rev`.

Every path is a hard-coded constant inside the lane. `git show rev:path` can
only emit bytes that are already committed to that repo's object store — it
cannot traverse `..`, cannot follow a symlink stored in the tree (it returns
the link target text), and cannot read outside the repository.

## Could they read a secret or credential path?

No path under the counters' control points anywhere near a credential. All
eleven+nine read targets are wave artifacts, `corpus/` content, `LOG.md`, and
`SOURCES.md`. The only way a counter could surface a secret is if a secret
were committed to one of those fixed paths inside the lane — at which point
`git show` would return it like any other blob, but that is a repo-hygiene
issue, not a counter defect. The scripts do not read `.env`, `~/.ssh`,
credentials files, or any path supplied by the caller; `--root` selects the
repository, never the file.

Environment inherited by `git` is the caller's. `GIT_DIR`, `GIT_WORK_TREE`,
`GIT_EXEC_PATH` are not scrubbed, but `-C <root>` pins the work tree and none
of the plumbing subcommands honour pager/editor/hook variables. A hostile
`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` could alias or set safe.directory, but
again plumbing ignores aliases and the worst outcome is reads failing →
`met=False`.

## What they write

- Stdout/stderr only, unless `--json <path>` is passed.
- With `--json`, `open(<path>, "w", encoding="utf-8")` writes the JSON result.
  The path is taken verbatim from argv — no sandboxing, no `realpath` check,
  no confinement to the lane. `--json /etc/passwd` or `--json` pointing into a
  sibling lane would happily truncate and overwrite it with the report JSON.
  This is the single writable surface and the narrowest place to clamp if a
  guard is ever added (e.g. resolve and require the path to sit under
  `--root`). Neither contract counting command uses `--json`, so in the frozen
  invocation the scripts are read-only.
- Neither script appends, creates directories, or touches the git index,
  refs, worktree, or `.jj` state.

## Behaviour when the lane path is a different repository

Empirically verified:

- `--root` pointing at an unrelated scratch repo with a different history:
  every `git show` returns non-zero → all blobs `None` → clean `met=False`,
  exit 1, reasons list the missing artifacts. No exception, no crash.
- `--root` pointing at a non-repo directory or a nonexistent path: git
  fails the same way → `met=False`, exit 1.
- `--root` pointing at a regular file (`/etc/passwd`): same → `met=False`,
  exit 1.
- `--revision` naming a commit that exists in a different repo's object store
  but is passed against the kake lane, or a garbage string: every read fails
  → `met=False`, exit 1.

So a wrong-lane or wrong-revision invocation is a **silent false-negative**,
never a false-positive and never an error. The counter answers "not met"
rather than refusing to run. Callers must therefore treat a `met=False` with
"artifact absent" reasons as ambiguous between "work not done" and "wrong
root" — the schema does echo `revision` back, but not `root`, so the receipt
cannot by itself prove which repo produced it.

## Concrete failure scenarios

1. **Silent wrong-root false-negative.** `--root` resolves (via symlink,
   mount, or caller error) to a different repo, or to no repo. Result:
   `met=False`, exit 1, "absent" reasons — indistinguishable from "work
   incomplete". Mitigation is on the caller: pin `--root` and echo it in the
   receipt.
2. **Ownership/dubious-repo fail-safe.** Lane `.git` owned by another user →
   git's safe.directory refusal → all reads `None` → `met=False`. Correct
   direction (never claims met) but can mask as "absent" rather than
   "permission denied".
3. **Missing python3 or git.** `subprocess.run` would raise
   `FileNotFoundError` inside `run()`, which `main` catches and reports as
   `{"error": ...}` exit 2 — the could-not-evaluate path. Good.
4. **Unparseable committed artifacts.** Malformed `quote-classes.json`,
   `order-proof.json`, `wave-cite-proof.json`, `settlement.json` → caught,
   recorded as an "unreadable" reason, `met=False`. Fail-safe.
5. **`--json` overwrite of an arbitrary path.** Only writable surface; the
   frozen contract commands never pass it, but any caller that does can
   clobber any file the process owner can write. Narrowest fix: constrain
   the resolved path to live under `--root`.
6. **Enormous committed blobs.** `git show` loads each blob fully into
   memory; a multi-GB artifact at one of the fixed paths could OOM the
   counter. Not a boundary violation, just a resource bound; paths are
   fixed and wave-controlled.
7. **Revision ambiguity.** `--revision` accepts any commit-ish git resolves
   (branch names, tags, `HEAD`). If a caller passes a ref that later moves,
   receipts naming only the resolved revision string stay accurate only if
   the caller recorded the 40-hex form. The contract uses full hashes, so
   this is latent, not live.
8. **`git` binary resolution.** `subprocess` resolves `git` on `PATH`. A
   hostile earlier `PATH` entry could substitute a fake `git` that emits
   crafted blob contents — the only route to a false `met=True`, and it
   requires control of the caller's environment, not anything the counter
   exposes. Worth pinning `git` to an absolute path if the instrument is
   ever run in an uncontrolled environment.

## Narrowest safe scope

- Run the counters only on a local, non-bare checkout owned by the invoking
  user, with `--root` set to the lane's real path (no symlink indirection) and
  `--revision` as a full 40-hex commit.
- Treat them as read-only: do not pass `--json`, or if used, resolve the
  target and require it to sit under `--root`.
- The trust boundary is the git object store of the repo `--root` names:
  inputs are exactly the committed bytes at the fixed paths above; outputs
  are stdout and the optional JSON file. Nothing crosses into the worktree,
  the index, `.jj`, hooks, filters, or the network.
- The one genuine hardening gap is `--json` path confinement; the one
  operational ambiguity is that a wrong root reports `met=False` rather than
  an error, so receipts should record the resolved root alongside the echoed
  revision.
