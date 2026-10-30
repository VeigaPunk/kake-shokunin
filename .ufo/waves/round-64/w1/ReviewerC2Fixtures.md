# ReviewerC2Fixtures — C2 revision-materialization review

## Recommendation

No actionable defect found in the frozen C2 production path for the assigned attacks. This is a scoped recommendation, not an admission or a claim of attack saturation. Axes: path containment, revision-byte isolation, fixture coverage, and honest missing-input status.

## Findings by severity

**Informational / latent helper hazard:** `materialize()` accepts `../` and absolute keys without containment checks. A controlled direct call demonstrated both escapes, entirely inside this seat's scratch tree. This does **not** demonstrate an attack on the frozen counter: its sole production caller constructs the keys from `TOOL_REL` and `FIXTURE_RELS`, all fixed, relative, traversal-free constants. Revision blob contents cannot replace those keys. Changing those constants would change the frozen instrument, outside the assigned attack.

Evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py:54-63,130-136,159-170`. The other helper `_fixture()` is used by the instrument selftest, not `evaluate()`; its filename input is not a production revision-controlled path.

## Caller and behavioral review

- Production `main()` calls `evaluate()` at counter lines 357-370. `evaluate()` obtains the pinned tool blob first (147-157), reads exactly six fixed fixture paths with `git show` (159-166), creates a fresh directory and writes ordinary files (168-170). Git symlink modes are not reproduced: `git_show()` returns blob content, and `materialize()` writes it using `open(..., 'wb')`, not `symlink()`.
- Tool `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py:24,40-73,76-100` binds `LANE_ROOT = Path.cwd()` and its selftest reads only the paths in `FIXTURE_CASES`. Counter lines 174-178 launch that pinned script with `cwd=work`. All fixture paths remain inside that fresh work directory. Its CLI `classify` arbitrary-path branch (127-140) is not selected by this invocation. No fixture-data execution or fixture-derived pathname was found.
- The frozen case tables match exactly, including IDs, quotes, expected classes and both paths. `FIXTURE_RELS` equals the union of all case raw/text paths: six unique files for four cases, with no omissions or extras.
- Each missing fixture returns `(2, "")`, prints `could-not-evaluate: fixture absent at revision: <path>` to stderr, and emits no `met=true` or other stdout. This precedes scratch creation and tool execution (161-165). `main()` propagates the exit code (367-370). This differs intentionally from the missing-tool case (147-151), which is exit 1 / `met=false`.

## Exact inspection commands

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:scripts/quote_class.py
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- .ufo/waves/round-64/c64_quote_tool.py scripts/quote_class.py
```

The diff adds the 374-line counter; the tool has no diff. Frozen sources for the executed probes were obtained through `subprocess.run(['git','-C',lane,'show',f'{rev}:{rel}'],check=True,stdout=subprocess.PIPE).stdout`, where `lane` is the absolute lane above and `rev` is T0 above. They were compiled into Python module namespaces with non-main names, not imported from mutable worktree files. SHA outputs:

```
counter_sha256=96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b
tool_sha256=431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14
```

## Executed attacks and exact outputs

Python Eval probe, using frozen counter module `m`, frozen tool module `t`, and `seat='/fast/scratch/hyaku/kake-r64/ReviewerC2Fixtures'`:

```python
table={c['id']:{k:str(v) if k in ('raw','text') else v for k,v in c.items() if k!='id'} for c in t.FIXTURE_CASES}
paths={c[k] for c in table.values() for k in ('raw','text')}
# Compare table to m.FROZEN_CASES and paths to set(m.FIXTURE_RELS).
root=seat+'/root'; os.makedirs(root)
m.materialize({'../escaped.txt':b'controlled escape',seat+'/absolute.txt':b'controlled absolute'},root)
```

```
case_tables_equal=True
missing_fixture_rels=[]
extra_fixture_rels=[]
fixed_paths_contained=True
helper_parent_escape=True
helper_absolute_escape=True
```

For each of the six missing-file probes, only `git_show` was patched; revision verification and all preceding tool retrieval/hash checks remained real. Exact executed loop core:

```python
real_git_show=m.git_show
for missing in m.FIXTURE_RELS:
    def altered(root,revision,rel,missing=missing):
        return None if rel==missing else real_git_show(root,revision,rel)
    out,err=io.StringIO(),io.StringIO()
    with patch.object(m,'git_show',altered),contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        code,_=m.evaluate(lane,rev)
```

Exact outputs (unit fault injection, **not** newly committed fixture revisions):

```
missing=scripts/fixtures/quote-class/inline.raw.html return=2 stdout='' stderr='could-not-evaluate: fixture absent at revision: scripts/fixtures/quote-class/inline.raw.html\n'
missing=scripts/fixtures/quote-class/inline.txt return=2 stdout='' stderr='could-not-evaluate: fixture absent at revision: scripts/fixtures/quote-class/inline.txt\n'
missing=scripts/fixtures/quote-class/markup.raw.html return=2 stdout='' stderr='could-not-evaluate: fixture absent at revision: scripts/fixtures/quote-class/markup.raw.html\n'
missing=scripts/fixtures/quote-class/markup.txt return=2 stdout='' stderr='could-not-evaluate: fixture absent at revision: scripts/fixtures/quote-class/markup.txt\n'
missing=.ufo/waves/round-61/sources/S432.html return=2 stdout='' stderr='could-not-evaluate: fixture absent at revision: .ufo/waves/round-61/sources/S432.html\n'
missing=.ufo/waves/round-63/quote-class/S432.txt return=2 stdout='' stderr='could-not-evaluate: fixture absent at revision: .ufo/waves/round-63/quote-class/S432.txt\n'
```

Finally, executed `m.evaluate(lane,rev)` with real revision blobs and no result/input substitution. Only `tempfile.mkdtemp` was wrapped to pass explicit `dir=seat`, enforcing the seat scratch bound; all other arguments were preserved. Output:

```
T0 return=0 stdout='revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true\n' stderr=''
scratch_removed=True
```

## Residual risk and verification gaps

- LSP unavailable: reading `xd://lsp` returned `No such tool: xd://lsp`. Therefore references/definition/diagnostics could not be obtained; caller conclusions above are source review and controlled execution, not semantic-index proof. No grep result is offered as semantic proof.
- This is fixture-byte isolation, not an OS sandbox: Python and its standard library necessarily remain external execution dependencies. No claim is made about a compromised interpreter, Git executable, host filesystem race, or malicious same-UID process. The fixed path tables and fresh ordinary-file materialization prevent the assigned revision-controlled traversal/symlink attacks.
- Missing-fixture behavior was tested by six unit-level read failures, not six committed repositories, because this leaf may not run mutating Git commands anywhere. The frozen early-return logic is cited above.
- No C1/C3, resume continuity, routing, or fleet saturation judgment is made; these are outside this seat's assignment. No stub or false-green was found through the assigned fixture attacks.
- No installations, upgrades, Git mutations, commits, source changes, or runtime/orchestrator invocation. Scratch removed in `finally`; only this report persists.

Self-evaluation: accuracy 4/5 (source/behavior evidence, no LSP); completeness 4/5 (all assigned paths, missing cases use injected read faults); clarity 4/5 (explicit helper-vs-production distinction, long evidence); actionability 4/5 (line anchors and probe cores, no committed fixture repro permitted); conciseness 4/5 (verbatim outputs retained for audit). Overall 4.0. Highest-impact improvement for an authorized integrator: committed missing-file fixture coverage. Would the user agree? The explicit distinction between latent helper escape and reachable counter behavior is central to that assessment.
