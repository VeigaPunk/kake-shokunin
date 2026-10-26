# SentinelRound

Security review of the round-57 new executable surface, read-only, exploit work confined to my own `mktemp -d` fixtures
(`git init` + `-c user.name=selftest`); the lane was read-only — I wrote only this report and no tool was installed (none needed).
**Revision read: `4b8c73050470ada9e6583f3b12d659d1bed6a17f`** (lane HEAD is `51921b9`, but all five reviewed files are byte-identical to
`4b8c730`: `git show 4b8c730:<path> | diff - <working tree>` = 0 lines for each). Reviewer of the *code*, not of the claims.

## FINDINGS:

### F1 (MEDIUM) the gate runs revision-controlled Python with the operator's HOME, an unrestricted network stack and the live lane path
- **file:line** `.ufo/waves/round-57/c57_idresolver_gate.py:99-101` (`run_tool` env + exec), `:88-96` (`sandbox_clone`),
  `:327`/`:331` (G4/G5 pass `root`, the real lane, as the tool's `--root`).
- **input** the measured revision's `scripts/id_resolver.py` (CLI `--revision`); nothing else required.
- **command that shows it** (confirmed by running) — imported the shipped gate module and called its own `sandbox_clone`+`run_tool`
  on a scratch repo whose `scripts/id_resolver.py` prints `os.environ["HOME"]` and connects to `127.0.0.1:1`:
  `stdout: ["HOME=/home/vgpnk net=ConnectionRefusedError envkeys=['HOME','LC_ALL','PATH','PYTHONHASHSEED']", "ids_cited=0 …"]`.
- **effect** the measured code gets the operator's home (`-B` disables bytecode only; no `-I`/`-s`, so
  `~/.local/lib/python3.*/site-packages` is importable and a `sitecustomize.py` there would run before the tool) and a working
  socket syscall (no network namespace, no seccomp). In G4/G5 it is also handed the live lane directory, so "the tool writes
  nothing" is convention, not enforcement. This is the class round-56 `w2/SentinelRound.md` S2 demonstrated by writing
  `$HOME/.sent-r56-home-write`; round 57 narrows the env to 4 keys but keeps HOME + network. `stdin` is inherited and the
  `timeout=300` (`:98`) kills only the direct child, so a spawned grandchild survives the gate.
- **fix** `HOME=<fresh mkdtemp>`, `[sys.executable, "-I", "-B", …]`, `stdin=subprocess.DEVNULL`, `start_new_session=True` +
  `killpg` on timeout, and wrap the run in `bwrap --unshare-net --ro-bind / / --tmpfs /home …` (or `unshare -n`); hand G4/G5 a
  read-only clone of the lane instead of `root`.

### F2 (MEDIUM) every selftest writes into whatever repository `GIT_DIR` names — its toplevel guard is defeated by it
- **file:line** `scripts/id_resolver.py:299-303` (`_repo`: `git init`, then `rev-parse --show-toplevel` compare) + `:307-313`
  (`_commit`: `add -A`, `commit`); `.ufo/waves/round-57/c57_receipt_pins.py:327-334` (`Sandbox.__init__`, guard is
  `assert realpath(top) == realpath(self.d)` at `:332`) + `:340-352` (`commit`); `c57_quote_truth.py:712-733` (`_build`: mkdtemp,
  `git init`, same toplevel check, three commits).
- **input** an inherited `GIT_DIR` (and/or `GIT_WORK_TREE`, `GIT_INDEX_FILE`). Every git call is `subprocess.run([...])` with no
  `env=`, so git honours it; `git -C <mktemp> rev-parse --show-toplevel` then prints `<mktemp>` (verified: returns the `-C` dir),
  the equality check passes, and `git -C <mktemp> add -A` + `commit` act on `GIT_DIR`'s repository.
- **command that shows it** (confirmed by running, all in scratch repos):
  `GIT_DIR=$S/repo/.git python3 -B scripts/id_resolver.py --selftest` → the scratch repo's HEAD moved `f3031b6`→`59c4acc`, its
  index was rewritten (`git status`: ` D corpus/SOURCES.md`, ` D corpus/knowledge/a.md`), and `selftest: 28/33` (3 url-match cases
  then read the *wrong* `HEAD:corpus/SOURCES.md`, i.e. silent degradation instead of a loud failure);
  `GIT_DIR=$D/repo/.git` + `c57_receipt_pins.Sandbox().commit({"x.txt": …})` → commit `0e10ce5 c` added to the scratch repo;
  `GIT_DIR=$S/repo/.git` + `c57_quote_truth._build(...)` → commits `pre-append evidence` and `append` added (count 1 → 4).
- **effect** a seat or gate run with `GIT_DIR` exported (git hooks, `git submodule`/`worktree` wrappers, some CI shells) mutates an
  unrelated repository: if that repository is the lane, the selftest rewrites the lane index and *adds commits to the lane branch* —
  a lane mutation from a tool documented as writing only under `mkdtemp`, which would also violate C1's "a receipt is never
  rewritten". The gate itself is not affected (it passes a 4-key env), so G2/G5 are not contaminated; direct invocation is.
- **fix** strip `GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_COMMON_DIR` in the `_spawn`/`subprocess.run` helper
  (or pass `env={…}` without them), and strengthen the guard to compare `git rev-parse --absolute-git-dir` against
  `<path>/.git` **and** the toplevel; the same helper should be used by `Sandbox` and `_build`.

### F3 (LOW) the resolver's worktree mode reads through symlinks out of the lane
- **file:line** `scripts/id_resolver.py:152-174` (`knowledge_bodies`, working-tree branch: `os.walk(base)`, `open(full, "rb")`);
  the gate's reference has the same behaviour (`c57_idresolver_gate.py:157-165`), so G3's differential test cannot catch it.
- **input** a committed `corpus/knowledge/x.md` symlink (or `corpus/knowledge` itself as a symlink), used when `--revision` is omitted.
- **command that shows it** (confirmed by running) lane with `corpus/knowledge/ext.md -> $D/outside.md` (file outside the repo):
  `DANGLING S777 cited-by=corpus/knowledge/ext.md owners=- url-match=-`; lane with `corpus/knowledge -> $D/extern`:
  `DANGLING S888 cited-by=corpus/knowledge/x.md …`. The same lane with `--revision HEAD` → `unevaluable: no knowledge file` (blobs only).
- **effect** content from outside the fleet is counted as a lane citation, so a checkout can steer the capability's plain-CLI report;
  a checkout can also make the tool read any operator-readable file (only matched ids, owner names and repo-relative paths are
  printed, and `url-match` is a boolean — no content channel). Revision mode (the measured mode) is immune.
- **fix** in the walk, skip any entry whose `os.path.realpath` is not under `os.path.realpath(root)` (or exit 2 on a symlinked
  knowledge dir/file); add a fixture with a symlinked `.md` to the resolver selftest and to the gate's reference.

### F4 (LOW) `fetch_sources.py` overwrites the sha256-pinned bodies in place and ignores curl's outcome
- **file:line** `.ufo/waves/round-57/fetch_sources.py:8-14` (`-o {sys.argv[1]}/{sid}.html`, then `open(..., "rb")`,
  `json.dump(..., open(..., "w"))`; `p.returncode` never read).
- **input** a re-run (`python3 fetch_sources.py <dir>`), or any curl failure (DNS/4xx/5xx/timeout).
- **command that shows it** (confirmed by running) `python3 -B fetch_sources.py` (no argument) → `IndexError: list index out of
  range`, exit 1 instead of a usage error; the no-returncode-check branch is [INFERENCE] from the lines above (I did not re-fetch
  the live pages).
- **effect** the retained bodies C3 pins by digest (`c57_quote_truth.py:95 BODY_SHA256`) are replaced in place and `receipts.json`
  truncated by any re-run; a failed fetch leaves a truncated/empty `S421.html`/`S422.html` with no receipt. C3 fails closed on a
  digest mismatch, but the retained copy — the round's evidence — is destroyed.
- **fix** require the directory argument (exit 64) and `sys.argv`-validate it; refuse when `receipts.json` exists (or write
  `<sid>.<utc>.html`); check `p.returncode == 0` and `httpStatus == 200` before writing the receipt; write via a temp file +
  `os.replace`.

### F5 (LOW) failure paths leave `c57-*` temp trees (full repo copies) behind
- **file:line** `c57_quote_truth.py:714-716` (mkdtemp before any `try`), `c57_receipt_pins.py:327-334`, `c57_idresolver_gate.py:229-231`
  (a fixture dir is added to `tmp` only after `build_fixture` returns, so a raise inside it leaks).
- **command that shows it** (confirmed by running) `c57_quote_truth._build({…, "corpus/SOURCES.md/x": …})` raised
  `FileExistsError` and left `/tmp/c57-qt-groam0li`; `c57_receipt_pins.Sandbox().commit({"bad\0name": …})` raised `ValueError` and
  left `/tmp/c57-pins-4hfdwth_` (both removed by me).
- **effect** repeated failing runs litter /tmp with copies of a commit history; nothing in the lane breaks.
- **fix** create the tree inside a context manager (`try/except: rmtree; raise`); register the dir with `atexit` before writing.
  Related latent hazard: `Sandbox.commit` does `os.path.join(self.d, p)` on a caller-supplied key, so an absolute key would write
  outside the sandbox — assert `commonpath` (fixture keys are literals today, so not reachable).

## EXECUTION SURFACE:

| artifact | executes revision code? | with what |
|---|---|---|
| `c57_idresolver_gate.py` | **yes** — `sandbox_clone` (:88-96) clones+checks out the measured revision, then `run_tool` (:98-103) runs `<clone>/scripts/id_resolver.py` for G2 (`--selftest`), G3 (fixtures), G4 (`3994101`) and G5 (measured rev) | env `{PATH, HOME, LC_ALL, PYTHONHASHSEED}`, `cwd=clone`, caller's `sys.executable`, inherited `stdin`, no netns/seccomp; real lane path passed as `--root` in G4/G5 |
| `scripts/id_resolver.py` | no (measurement path) — `git rev-parse/ls-tree/show` + file reads, blobs decoded as text; `--selftest` runs `git init/add/commit` under `mkdtemp` | inherits the caller's full env (incl. `GIT_DIR`, `HOME`), no `env=` |
| `c57_receipt_pins.py` | no — `git log --name-status -M --format=@@%H`, `show`, `ls-tree`, `rev-parse`, `merge-base` (read-only); selftest builds repos in `mkdtemp` | inherits env; its `cli()` selftest re-invokes itself with `{**os.environ, KAKE_R57_PINS_TEST_BASE}` |
| `c57_quote_truth.py` | no — `git show` only (bodies/entries/registry read as data); selftest builds repos in `mkdtemp` | inherits env |
| `fetch_sources.py` | no — one `curl` per page, UA `kake-shokunin-round57`, no cookies/auth/credentials | caller's network and `argv[1]` |

## NO-DEFECT CHECKS:

1. **No shell anywhere.** `shell=True|os.system|os.popen|eval(|exec(|shlex` → 0 hits in all five files (unlike round 56, no
   `shlex` cell parser exists here), so there is no cell/text-to-argv path. *(confirmed by running grep)*
2. **A revision string cannot inject an option.** `git rev-parse --verify --help^{commit}`, `--output=/tmp/x^{commit}`,
   `-n^{commit}` all → `fatal: Needed a single revision` *(confirmed by running)*. The `=`-form does reach the counters
   (`--revision=--output=/tmp/pwn-r57c|d|e`): resolver exit 2, C1 exit 2, C3 exit 2, and no file exists at the injected path;
   the bare form is refused by argparse (exit 64). Downstream `rev:{path}` uses the resolved 40-hex SHA in C1/resolver; C3 keeps
   the raw string but only after the same rev-parse gate. *(confirmed by running)*
3. **Commit text cannot forge the C1 history walk.** `--format=@@%H` prints no message body; a relabel commit whose message is
   `@@<40 hex>` still yields `relabels_in_history=1 undisclosed_relabels=1` and the raw log shows only the two real headers.
   *(confirmed by running the counter on a scratch repo)*
4. **File names do not reach argv unsafely.** Blob paths come from `ls-tree`/`name-status` and are always the tail of
   `<sha>:<path>`; git quotes names containing newlines/tabs, so a weirdly named receipt silently leaves the population instead of
   splitting a record. *(by reading; the quoting behaviour is git's documented `core.quotePath`)*
5. **The measurement paths write nothing.** No `open(…, "w")`, `os.replace`, `shutil` or `makedirs` outside the `--selftest`
   branches of the resolver/counters; my runs against fixture lanes and a scratch repo left those trees unchanged.
   *(confirmed by running)*
6. **Revision mode is symlink-proof.** `--revision HEAD` over the symlinked knowledge dir → `unevaluable: no knowledge file at …`
   (git blobs only), so F3 is a working-tree-only defect. *(confirmed by running)*
7. **Gate fixture writes stay inside `mkdtemp`** (`build_fixture` prefix `c57-fixture-`, lane inside the fleet dir; cleaned in
   `evaluate`'s `finally`), and `read_lane`/`read_siblings` open files read-only. *(by reading; no fixture dir of mine remained)*
8. **No secret is read or emitted.** No `op://`, no env-token/`.ssh`/`netrc` read in any of the five; `receipts.json` carries only
   `url/httpStatus/bytes/sha256/fetchedAt/userAgent`; the only token-shaped string in the retained bodies is the publisher's own
   public chat-widget parameter (`S421.html`/`S422.html`: `…/roulette/in?id=16606&token=i7md…&domain…`) plus the widget's own
   `b.cookie=…` JS — both served to the anonymous fetch (no cookies or auth were sent). *(confirmed by running grep)*
9. **`_repo`/`Sandbox`/`_build` do build their repos in `mkdtemp` and compare toplevels** — correct against a plain inherited
   cwd; defeated only by `GIT_DIR` (F2), which the gate's 4-key env cannot supply.
10. **Not run by this seat:** the gate's five conditions end-to-end and `fetch_sources.py` against the live pages (no claim is
    scored here); all gate statements above come from calling its shipped `sandbox_clone`/`run_tool` directly.

VERDICT: no shell or shell-equivalent path exists and every CLI revision input fails closed, but the C2 gate executes the measured revision's Python with the operator's `$HOME`, an open network stack and the live lane path (F1), and all three selftests will commit into whatever repository an inherited `GIT_DIR` names — including the lane (F2); F3-F5 are low-severity integrity/cleanup defects; no credential material is read or retained.
