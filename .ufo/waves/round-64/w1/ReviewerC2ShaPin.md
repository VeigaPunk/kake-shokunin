# ReviewerC2ShaPin — C2 frozen-tool execution review

## Recommendation

No actionable frozen-tool SHA bypass found in the assigned scope. This is a review recommendation, not admission or settlement. Axes: byte identity, execution ordering, isolation accuracy, output integrity. Reviewed the actual base→T0 diff; the counter is new and the tool has no diff.

## Findings by severity

None against the defined claim: a revision-supplied tool with a different SHA does not reach the tool subprocess. A SHA-matching hostile replacement requires a second-preimage/collision outside the assignment's model.

### Evidence and attacked boundaries

All paths below are absolute under `/home/vgpnk/Projects/shokunin/kake-shokunin`.

- **Present → SHA → materialize → run:** `.ufo/waves/round-64/c64_quote_tool.py:139-178` first checks the revision; obtains tool bytes via `git show` (`:102-108`); rejects absent bytes at `:148-151`; rejects a different digest at `:153-157`; retains the same immutable byte value at `:159`; loads only six constant fixture paths at `:160-166`; materializes at `:168-170`; and only then executes at `:174-178`. There is no second worktree tool read between hash and execution. `materialize` at `:130-136` writes those captured bytes to ordinary files, not Git checkout symlinks. All destination names are counter constants (`:54-63`), not fixture-supplied paths.
- **Frozen tool has no execution sink for fixture content:** `scripts/quote_class.py:19-25,76-100,115-125` imports standard-library modules, reads the fixed fixture paths under the materialized cwd, decodes text, compares substrings, and emits JSON. The retained HTML/text never reaches eval, exec, import, a shell, or another subprocess. A non-frozen script in the lane worktree is not this subprocess's script.
- **Stdout/stderr cannot select files:** counter `:175-178` uses an argument vector, captures both streams into pipes, and never evaluates or opens their content. `:190-228` parses stdout as JSON and checks values; stderr is not consumed as instructions. Frozen tool output follows its constant case table, so malicious fixture strings do not become output case IDs or code. Cleanup is of the already-selected work directory (`:183-184`).
- **Counter itself:** normal evaluation has only the Git read subprocesses and the pinned Python-script subprocess (`:102-108,140-142,174-178`). Fixture bytes cannot change the counter constants or select an executable. Its separate `--selftest` entry (`:278-347,365-366`) deliberately creates Git fixtures and runs the same counter; this is not the production tool-execution path and was not invoked here.

## Residual risk: environment relocation is not a sandbox

At counter `:171-178`, HOME and TMPDIR point to work, cwd is work, PATH is inherited, and LANG is C. This prevents the frozen tool's fixed relative fixture reads from accidentally reading the lane worktree. It does **not** deny absolute filesystem reads, networking, or filesystem writes to the subprocess: there is no namespace, chroot, syscall filter, or network policy here. PATH is not set to work. The safety argument is the frozen program's inspected behavior plus trusted Python/Git/standard library, not OS confinement.

The outer counter's Git subprocesses inherit the invoking environment and resolve `git` through PATH (`:102-105,140-142`). The outer Python interpreter also starts before this module's SHA check. Compromised interpreters, ambient Python startup hooks, hostile Git configuration/replacements, same-user interference with temporary files, or mutable revision names are not disproved by hashing the tool. They are host/invocation trust assumptions, not demonstrated revision-tool bypasses. The canonical command uses the supplied immutable commit identity; no alternate runtime or identity rerouting was introduced in this review.

## Exact commands and observed evidence

1. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- .ufo/waves/round-64/c64_quote_tool.py scripts/quote_class.py`
   Output: new counter file, mode 100755, `/dev/null` → `.ufo/waves/round-64/c64_quote_tool.py`, 374 added lines; no tool diff.
2. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:scripts/quote_class.py | sha256sum`
   Output: `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  -`
3. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/c64_quote_tool.py | sha256sum`
   Output: `96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b  -`
4. `sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py`
   Output: respectively the same counter and tool hashes above, followed by those absolute filenames. Thus the line-cited working files match the measured blobs.

Existing receipt evidence, **read, not rerun**:

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/stub-c64.txt:1-3` records `python3 -B .ufo/waves/round-64/c64_quote_tool.py --root /fast/scratch/hyaku/kake-r64/l1/fixtures/stub-repo --revision 14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3`, output `revision=14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3 present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false`, `exit=1`.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/after-c2.txt:1-3` records the T0 invocation and output `revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true`, `exit=0`.

## Verification gaps and bounds

`read xd://lsp` returned `No such tool: xd://lsp`; no LSP server/status/references/definition/diagnostics device was available. Used direct line reads and literal invocation-reference search instead, not represented as semantic proof. Contract command is at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md:93-94`; the corresponding registry reference is `SKILL.md:1364`.

This is static review with digest checks and existing receipts, not an independently executed counterattack or saturation claim. No counter execution, fixture commits, runtime substitution, network probes, or mutation of claims/receipts occurred. Created the required `/fast/scratch/hyaku/kake-r64/ReviewerC2ShaPin` directory and removed it with `rmdir` before reporting; both commands exited successfully. No tools installed or updated.

Self-evaluation: accuracy 4/5 (static proof, not a runtime attack); completeness 4/5 (all assigned boundaries examined; host compromise not exercised); clarity 4/5 (explicit trust boundary and evidence); actionability 4/5 (avoid interpreting relocation as confinement); conciseness 4/5 (evidence detail retained). Overall 4.0/5. Main improvement would be independent execution by the authorized executor; review-only restrictions were respected.
