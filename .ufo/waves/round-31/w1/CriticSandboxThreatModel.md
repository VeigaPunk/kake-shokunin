# CriticSandboxThreatModel — C1 escape routes outside probes P1-P5 (round 31, wave 1)

Seat: KakeR31.CriticSandboxThreatModel (critic, advisory). Axis judged: operability. Milestone r31-build.
Target: the base runner at f1ffb81738c92c0537b99b30970143ab9419f990, run from a sandbox clone
(`/fast/scratch/hyaku/kake-r31/w1/CriticSandboxThreatModel/clone`, detached at f1ffb81).
Base runner sha256 9f2d1ecb…e14d3, gate sha256 dbfade45…b7f02.
Reproducer: `/fast/scratch/hyaku/kake-r31/w1/CriticSandboxThreatModel/routes.py` (sha256 1659cba7…10f57).
Command: `TMPDIR=<sandbox>/tmp python3 -B routes.py <sandbox> [route ...]`. Every run exited 0 (the harness prints
one JSON line per route). The victims are throwaway repositories in the sandbox. No lane file other than this
report was written, and no install was made.

## Headline counterexample (HIGH, the contract does not cover it)
**R1: a fixture shaped like a bare Git repository, with no entry named `.git`, redirects the gate's `--revision` read
to any repository.** The case directory holds `HEAD` (`ref: refs/heads/<branch>`) plus either
`objects/info/alternates` and `refs/heads/main`, or a single `commondir` file holding an absolute path to the
victim's `.git`. `case.json` is `{"argv": ["--revision", "HEAD"]}`. That argv passes the N1 allowlist, the case has no
`.git` so N2 passes, and the case runs no setup Git, so N3 does not apply. The gate's `git -C <root> rev-parse`
treats the root itself as an implicit bare repository. The gate's documentation accepts this by design: a bare
repository root "is accepted" (citing_set.py:104). `--show-prefix` is empty there, so `_require_top_level`
(citing_set.py:386) passes too.
- Observed, route `bare-alternates`: runner exit 0, case passed, findings `["unadjudicated_citing_pair"]`. That finding
  comes only from the victim's `corpus/knowledge/secret.md` citing S777. `dotGitEntries: []`, and the victim's HEAD,
  refs and commit count were unchanged.
- Observed, route `bare-commondir`: the same result (exit 0, passed) from two files, `HEAD` and `commondir`, with no
  SHA hard-coded. Pointed at `/home/vgpnk/Projects/shokunin/kake-shokunin/.git`, a committed fixture would measure
  the lane's live HEAD tree [INFERENCE: not run against the lane, by the bounds].
- Observed, route `bare-subroot`: setup `[git_init, git_commit]` plus `root: "x"`, where `x/` holds the bare layout.
  The result was exit 0 and passed. So the runner making its own `.git` does not protect a subdirectory root.
- Observed, route `cfgexec`: a fixture `config` with `include.path=<absolute path outside the case>` is opened by the
  gate's first `rev-parse`. strace showed `openat(... outside-include.cfg, O_RDONLY) = 4`. This is a read outside the
  case.
- Impact: it reads outside the case and touches a foreign repository. It is also a false-provenance pass: the case
  reports "passed" while measuring a tree that is not the case's.
- Smallest safe correction (runner side; the gate's bare-root acceptance stays as documented): for any case whose
  argv names `--revision`, run `git -C <gate root> rev-parse --absolute-git-dir` with the gate's environment before
  starting the gate. Fail the case unless the output equals `realpath(<work>/.git)` and that `.git` came from this
  case's `git_init`. A stronger alternative is to also refuse, before copying, any case directory that contains a file
  named `HEAD`, `commondir`, `gitdir` or `objects/info/alternates`. Add a hostile probe P6-bare-layout (commondir
  variant plus subroot variant).

## Other routes
| id | route | severity | tried | base result | does the contract cover it? |
|---|---|---|---|---|---|
| R2 | setup `mkdir x/objects`, `mkdir x/refs`, `fifo x/HEAD`; root `x`; `--revision HEAD` | MEDIUM (hang, leak) | yes, `fifo-head`, timeout 5 | the case failed with "gate timed out after 5s" (exit 1, no false pass), but the grandchild `git -C …/x rev-parse --verify --quiet HEAD^{commit}` (pid 3951752) stayed blocked on the FIFO after the run until I killed it | no. N2 sees no `.git`. The runner's gate `subprocess.run(timeout=)` (selftest:466-473) kills only the Python child. One process leaks per hostile case. |
| R3 | setup `git_init`, then `fifo .git/config` (or `.git/index`), then `git_commit` | LOW-MEDIUM (hang) | yes, `setup-fifo-config`, timeout 3 | "setup command timed out: git … add -A", exit 1. Setup aborts at the first timeout, so the cost is one timeout per case | partly. N3 still allows setup paths under `.git`. The correction is to refuse any mkdir or fifo path with a `.git` component. |
| R4 | no overall deadline: N hostile cases cost N times the timeout (default 120 s each) | LOW | partly, `many-cases`: 300 benign cases took 8.4 s, exit 0, 4.7 MB scratch | linear, no hang on its own; combined with R2 it is N times 120 s plus N leaked processes | no |
| R5 | silent skips: a dot-named case directory, a regular file and a FIFO in the fixture directory are not counted | LOW (coverage) | yes, `silent-skips` | 7 entries gave `cases: 4`. `.hidden-case` has a never-satisfiable expectation and was skipped silently | no. N6 covers only symlinks. |
| R6 | `case.json` that is a dangling symlink or a directory makes the runner ignore the setup silently (selftest:286 `is_file()`) | LOW | yes, `silent-skips` | both cases passed as plain cases. A FIFO `case.json` fails at copy ("is a named pipe") | no. The correction is lstat: if the entry exists but is not a regular file, fail the case. |
| R7 | gate Git discovers an enclosing repository (`--tmpdir` inside a victim, `--revision HEAD`, no git_init) | LOW (read of refs only) | yes, `gate-enclosing` | `_resolve` resolves the victim HEAD, then `root_not_repository_top_level`, exit 2. No tree is read | contained by gate:386. N3 pins only setup Git. |
| R8 | option-shaped revision values `--revision=--all`, `=--show-toplevel`, `=--git-dir`, `=-h`, `=--since=yesterday` (the N1 allowlist allows any value after `=`) | LOW | yes, `revision-option` | all five gave `revision_not_found`; the `^{commit}` suffix neutralises them | allowed by N1, contained by the gate |
| R9 | `GIT_DIR`, `GIT_WORK_TREE` and `GIT_CONFIG_COUNT`/`KEY`/`VALUE` (core.fsmonitor canary) in the runner's environment | LOW | yes, `envleak` | the gate ignored them (input_invalid), no canary | contained by gate GIT_LOCAL_ENV (citing_set.py:166-170) and runner `git_env` |
| R10 | `--root=/` in argv (allowed by N1) | none | yes, `symlink-inputs/S2` | gate exit 64 (StoreOnce repeat); nothing read | contained by StoreOnce |
| R11 | symlinked `population.json` pointing outside; a symlinked `root`; mkdir through a symlink that leaves the case | none | yes, S1/S3/S4 | `path_escapes_root`; "setup path escapes the case copy"; `pwnedOutside: false` | contained by `inside()` realpath and the gate's `is_inside` |
| R12 | setup `mkdir .git` (created after the N2 committed-tree scan), then `--revision HEAD` | LOW | yes, S5 | `revision_not_found`; a later `git_init` refuses because `.git` exists | contained. The contract's N2 scan never sees `.git` entries created at run time, so refusing setup paths with a `.git` component (R3) closes this as well. |
| R13 | fixture `config` keys that run code during the gate's `rev-parse`, `ls-tree` and `show` (core.fsmonitor, core.pager, core.sshCommand, gpg.program with log.showSignature, diff.external) | none observed | yes, `cfgexec`, run by hand | no canary | not applicable; R1's correction removes the surface |
| R14 | git_commit writing into a victim through a case shaped like a Git directory (`commondir`, `core.bare=false`, `core.worktree=.`) | none | yes, `gitdir-shaped-commit` | "this operation must be run in a work tree"; victim unchanged | also closed by N3 (git_init required, explicit `--git-dir`) |

## Not tried
- Huge or sparse corpus, population or ledger files (the gate reads them with no size cap): risk of memory
  exhaustion, generated fixtures only. Not run, because of the memory risk on a shared host. [INFERENCE: an unbounded
  `read()` in WorkingTreeSource.read_document]
- A fixture directory on a case-insensitive or casefold file system (a `.GIT` spelling) and hardlinked inputs
  (generated only; Git cannot commit hardlinks).
- The new hostile selftest and the post-contract runner: neither exists yet, so every result above is against the
  base. The R1, R2 and R5 claims about "after the contract" are reasoned from the contract text, not run.
- Swapping symlinks between check and use (TOCTOU) for case.json or expected.json: needs a concurrent attacker;
  out of the fixture threat model.

## Impacted axes
Operability: R1 is a false pass that leaves the case and could hide behind a clean 45/45 plus 5/5. R2 leaks
processes and can hang a run for N times 120 s. R5 and R6 are silent coverage loss. Freshness is not affected.
Priority for the L1: (1) R1 needs a runner-side check of the gate's Git directory plus a probe P6. (2) R2 needs
`start_new_session=True` on the gate and setup subprocesses and `os.killpg` on timeout, plus refusal of
FIFO or mkdir paths that form a `HEAD` file next to `objects/` and `refs/` (the R1 check covers this when
`--revision` is present). (3) R3 and R12 need setup paths with a `.git` component refused. (4) R5 and R6 need every
non-symlink entry that is not a directory, every dot-named entry, and every `case.json` that exists but is not a
regular file to count as a failure.
