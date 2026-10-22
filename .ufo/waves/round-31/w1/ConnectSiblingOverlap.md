# ConnectSiblingOverlap — round 31, wave 1 (leaf, connector)

Seat KakeR31.ConnectSiblingOverlap. Read-only scan of 20 sibling lanes under
/home/vgpnk/Projects/shokunin/*-shokunin (corpus/knowledge, SKILL.md, PROVINCE.md).
Kake read at a16602a961da5d6e75cfa09a1118a416ad01225b, base runner at f1ffb81 (blob sha256 9f2d1ecb…e14d3).
Sibling HEADs read: souji 4edb25d, kagi 899c50b, kumitate a58b7f7, tabi e3cf4e0, mori dd4dbb2, tameshi 06b59b9, kama 1560e4d.
Axes: operability (C1), freshness (C2). No installs. No network. No lane writes other than this file.

## (a) Render / render.yaml / Blueprint / Docker web service / health check — no overlap

- No sibling file contains `render.com`, `render.yaml`, `onrender.com` or `healthCheckPath` anywhere in its repository (`rg -l` over all sibling repos, exit 0 and empty output). Kake is the only lane with Render knowledge, so C2 has no sibling source to cite. **Ignore.**
- Name-only false matches, all **ignored**: game-dev-3d `corpus/knowledge/unreal-mcp/executability/blueprints.md` (Unreal Blueprints); kotodama `synthesis/conlang-blueprint-template.md`; kotoba `sibling-description-rewrites-round8.md:191-199` and `sibling-overlap-census-round49.md:75` (these describe kake's own domain line, not Render).
- Near miss, **ignore**: kama `corpus/knowledge/runtime-health-surface-matrix.md:8` ("One `/health` URL shape does not carry one portable readiness meaning"). It covers local inference servers (llama.cpp, vLLM, SGLang), not Render. Render's health-check meaning has to come from S060 alone. Citing kama here would import a different system's semantics.

## (b) Fixture-runner sandboxing — overlaps by contract item

| Item | Sibling evidence (path:line) | Disposition | Why |
|---|---|---|---|
| N5 expected.json | kumitate `corpus/knowledge/route-resolution.md:32-34`: "`O_NOFOLLOW` + fstat size pin + post-read size check, ≤1 MiB (`MAX_CONFIG_FILE_BYTES` = 1_048_576…)"; kumitate `SKILL.md:297` same | **cite** (C1 docs) | Same 1048576 ceiling and the same three-step shape. The contract omits one step this source has: a post-read length check (read `max+1`, refuse if longer). It is cheap and closes the case where a file grows between fstat and read. |
| N5 contrast | kumitate `corpus/knowledge/local-ship.md:131,226`: `O_NONBLOCK`, "O_NOFOLLOW is deliberately absent so symlinked contract files still read" | **ignore** | Opposite design choice for trusted contract files. Do not cite it as support. |
| N5 FIFO | kagi `SKILL.md:731-732`: "readers open nonblocking, then reject non-regular descriptors. A FIFO timeout is not a successful refusal." | **cite** (hostile selftest P4) | P4 must count as passing only when the runner names expected.json. A case that fails with `gate timed out` must count as a P4 failure. |
| N5/N6 classify, never open | mori `corpus/knowledge/surfaces-r8.md:154` (a FIFO entry is classified `non-regular` and never opened, 418 ms) and `:228-236` (a writer-less FIFO input hangs until an external cap, rc 124) | **defer** | Same lesson as kagi, from a watchdog rather than a fixture runner. One citation (kagi) is enough. |
| N6 symlinked case | tabi `SKILL.md:2142`: "Case/fixture files must be regular, not symlinks."; `:1586`: reads "refuse symlinked/non-regular inputs and open files with `O_NOFOLLOW`" | **defer** | Matches N6 but adds no mechanism. Cite it only if the C1 docs want a fleet precedent. |
| N2 .git | souji `SKILL.md:114` and `corpus/knowledge/jj-colocation-receipts.md:62-69`: a directory holding any `.git` (even an empty stub) is a nested repository to jj, its files read as `D`, and a directory pathspec commits phantom deletions | **cite** (hostile-spec rule) | Gives the second-order reason behind the contract's "no .git committed" rule for `scripts/fixtures/citing-set-hostile/`. The lane is jj-colocated, so a committed `.git` in a spec dir corrupts the L1's own commit, not just the runner. Building the `.git` pointer at run time under --tmpdir is the right call. |
| N2 stub | souji `SKILL.md:161`: "a nested empty `.git` directory is not a repo" (to git) | **defer** | Supports N2 refusing `.git` by name at any depth rather than probing whether it works. |
| N3 ceiling | tameshi `corpus/knowledge/mutation-case-kumitate-sources-check.md:27`: `env -i PATH HOME=$h/home TMPDIR=$h/tmp LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES=$h` | **defer** | Fleet precedent for the ceiling. It also sets `GIT_CONFIG_NOSYSTEM=1`, which base `git_env()` (runner :336-341) does not: it strips `GIT_*` but leaves system and global config, such as `core.fsmonitor` and `core.attributesFile`, live. That is outside C1's declared N-set, so it is advisory only. |
| N1 argv | kagi `corpus/knowledge/claim-ledger.md:363-368`: the allowlist and the refusals "shrink the surface … they do not close it. The control is that the ledger is a reviewed, committed file." | **cite** (C1 residual wording) | Fits the N1 prefix allowlist exactly. It blocks reaching `--selftest`, but the gate still runs on fixture-supplied data. C1 docs should say the allowlist shrinks the surface and should not claim the runner is safe on hostile input. |
| N1 contrast | tabi `corpus/knowledge/harness-hardening-round-18.md:62` ("Not covered by this hardening: argv allowlist" for Chromium flags) | **ignore** | Different program and threat. |
| Gate timeout | souji `SKILL.md:117`: "`subprocess.run(timeout=)` kills the direct child; the census and its git grandchild stay blocked on a FIFO" | **cite**, routed as a defect, not a C1 claim | See the proposed move. |
| Git on FIFO | souji `SKILL.md:116` (git opens `.gitattributes`/`.gitignore` and `info/attributes` with blocking `open(2)`); kama `SKILL.md:807` (git call >20 s on a FIFO config/include/ref) | **cite** | Ground for the probe below. |

## Proposed move (one, bounded): the runner's own `fifo` op can stall its `git_commit`

Evidence: base runner `fifo` op `scripts/citing_set_selftest.py:368-372` (mkfifo at any in-copy path) and `git_commit` `:377-380` (`git add -A`). Per souji `SKILL.md:116`, git opens a work-tree `.gitattributes` FIFO with a blocking open. Probe in my sandbox, using the N3 contract's flags:

`cd /fast/scratch/hyaku/kake-r31/w1/ConnectSiblingOverlap/fifo-attr && … git --git-dir=$W/.git --work-tree=$W init -q && mkfifo .gitattributes && timeout -k 1 5 env GIT_CEILING_DIRECTORIES=$S git -c core.hooksPath=/dev/null --git-dir=$W/.git --work-tree=$W add -A` gave **rc=124 after 5.04 s wall time** on git 2.56.0, with no leftover processes. So `--git-dir/--work-tree` plus the ceiling (N3) does not stop it.

- Move: in `load_case_setup`, refuse a `fifo` step whose path basename is `.gitattributes` or `.gitignore`, or whose path is under `.git/`. Alternatively, in `apply_setup`, refuse any non-regular file at those names before `git add`. The case fails fast with a reason, not after a full `--timeout`.
- Axes: operability improves (fast refusal, no per-case wait for the full timeout). Freshness is unaffected. The 45 committed cases are not harmed [INFERENCE: not checked that no committed case places a FIFO at those names; `01-…` uses `population.json`, runner :43].
- Second-order effect [INFERENCE, not run]: the gate runs git with no timeout of its own (`scripts/citing_set.py:394-428` at a16602a). The runner's gate `subprocess.run(timeout=)` (`:466-474`) kills only the gate, so a git grandchild stuck on a FIFO would survive the timeout, as in souji `:117`. The hostile selftest's no-harm check (canary, victim HEAD and refs) would not see a leaked process. A cheap addition is to run the gate with `start_new_session=True` and `killpg` on timeout.
- Risk: this is outside the declared N1-N6 set. The L1 should route it as a new open defect, not widen C1 mid-round.
- Verification: add a hostile case `[git_init, fifo .gitattributes, git_commit]`. The expected result is failure with a reason naming the FIFO in under 1 s, against a 5 s `--timeout`.

## S056 (tameshi `mte-report-interop.md` at f4e8f7d8): **defer**; not citable by any current round-31 output

- Pin holds: `git show f4e8f7d8:…` sha256 `b173e3e549d0227e0d37df92956b652084290955bdcb6a0a7cbf2a9ad29c0fac`, which matches `corpus/SOURCES.md:64`. The quote at line 21, "`score` is a sanity check that holds by construction.", is present.
- Freshness: tameshi HEAD 06b59b9 differs (sha256 `6e10d010…27f9`, commit 40a12bf, round 26). The changes are a `verified-at` line and an appended "Round 26 append — nine legs" section. Quoted lines 10-22 and the decision table (158-164) are byte-unchanged, but line 22's "exactly the eight ledger legs" now reads "nine". Any kake citation must keep the f4e8f7d8 pin or say nine.
- Why defer: S056's scope (SOURCES.md:64) is the record shape of a mutation ledger, and it is "not a primary source for any fact about kake's citing-set gate". Its quote is about mutation ledgers, so it does not reach the declared round-31 outputs: the C1 runner, the hostile selftest, the C1 counter, `render-web-services.md` and the C2 counter. The only round-31 seats that would produce a per-mutant ledger, MutBaseProbeSensitivity (5x5 patch-to-probe matrix) and MutC2CounterStub (mutant killed/survived table), both died at spawn (`.ufo/waves/round-31/w1/dead-seats.json`). They are not yet a used-by.
- Condition to cite: if the L1 does MutC2CounterStub's work and lands its table in a kake knowledge entry or QUALITY row that uses the per-id verdict plus aggregate-count shape, S056 becomes used-by for that row only, kind docs tier B, pinned at f4e8f7d8.

## Commands and exit codes
- `rg` scans over the 20 sibling lanes: exit 0 (Render, health, sandboxing) and exit 1 (one loop, last lane had no match; output present).
- `git -C tameshi-shokunin show f4e8f7d8:… | sha256sum`, `git diff f4e8f7d8 HEAD -- …`, `merge-base --is-ancestor` (exit 0).
- `git show f1ffb81:scripts/citing_set_selftest.py`, `git show a16602a:scripts/citing_set.py` (read only).
- FIFO probe above: inner `timeout` rc 124. Sandbox: /fast/scratch/hyaku/kake-r31/w1/ConnectSiblingOverlap/fifo-attr (TMPDIR in sandbox).

## Not verified
- Gate-side git grandchild survival after a gate timeout: inferred from code and souji, not run.
- Whether any committed case already places a FIFO at `.gitattributes` or `.gitignore`.
- None of the C1 or C2 counters were run. This seat claims nothing about them.
