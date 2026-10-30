# ReviewerC2Rederive — C2 re-derivation review

## Recommendation

No exploitable finding against the frozen C2 predicate in this seat's scope. The two case tables agree byte-for-byte on all sixteen string fields at T0. The proposed `total=4, passed=True` bypass does **not** satisfy `totals_ok`. This is a scoped review recommendation, not admission, integration, or a claim of exhaustive saturation.

Axes: frozen-table fidelity; totals/boolean correctness; malformed-case reachability; evidence reproducibility. No lane bytes, instruments, receipts, or fixtures were changed.

## Findings by severity

### Low / defense-in-depth only: malformed dictionaries are not fully guarded

Absolute source: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py:195-204` at T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`.

Line 200 drops non-dictionaries, **not** malformed dictionaries. `{}` becomes a `None` key; duplicate IDs overwrite earlier entries; `{"id": []}` and `{"id": {}}` raise `TypeError` during dictionary construction. Thus the broad docstring statement at lines 21-25 that shape-hostile output never produces a traceback is stronger than this post-parse implementation.

This is not a demonstrated C2 kill-rule breach: the canonical run at lines 147-157 checks the tool digest before execution, and lines 159-178 materialize the frozen tool and revision fixtures and invoke that tool. The frozen `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py:76-100` generates exactly one result dictionary per fixed case with string IDs, derived string values, boolean per-case flags, and integer counts. Fixture contents affect classification, not result IDs or output structure. Altering tool code to emit hostile IDs fails the digest gate first. No counterfeit runtime/output injection was treated as an actual production exploit. If the broad defensive guarantee is retained in a future instrument, reject non-string IDs before indexing; that is outside this frozen review's permitted edits.

## Attacks and evidence

All source evidence below is from committed T0 blobs, not an assumption about the current worktree.

Exact read-only commands executed:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:scripts/quote_class.py
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- .ufo/waves/round-64/c64_quote_tool.py scripts/quote_class.py
```

The diff shows the counter as a new 374-line executable and no change to `scripts/quote_class.py`.

### A. Byte-level case-table comparison

Locations:

- Counter: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py:64-94`.
- Frozen tool: `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py:40-73`.

A Python Eval cell fetched the two T0 blobs using the exact subprocess form:

```python
subprocess.check_output(['git','-C',lane,'show',f'{rev}:{path}'])
```

with `lane='/home/vgpnk/Projects/shokunin/kake-shokunin'` and `rev='4c8295fa5e3b628f1fdf3840299ae415c01849fb'`. It parsed both with `ast.parse`, used `ast.literal_eval` for `FROZEN_CASES`, and interpreted only constants, dictionary/list nodes, `Path(...)`, and the `FIXTURES / ...` path expressions for `FIXTURE_CASES`. No source module was imported or run. The tool list was indexed by `id` and that `id` removed from each value before comparison. Each of `raw`, `text`, `quote`, and `expected` was independently compared using:

```python
spec[k].encode('utf-8')==indexed[cid][k].encode('utf-8')
```

This compares semantic string bytes, not source syntax: tool paths are `Path` expressions whereas counter paths are strings. It does not normalize quote Unicode or whitespace. Canonical table bytes used this exact encoder:

```python
enc=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
```

Observed output:

```text
counter_sha256=96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b
tool_sha256=431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14
inline_raw_substring: {"expected": true, "quote": true, "raw": true, "text": true}
markup_collapsed_only: {"expected": true, "quote": true, "raw": true, "text": true}
absent_everywhere: {"expected": true, "quote": true, "raw": true, "text": true}
s432_real: {"expected": true, "quote": true, "raw": true, "text": true}
table_bytes_equal=True
canonical_table_sha256=d7fd318ce808ddf8c3988e4fc7068fa381b9823cdb77f178c533a4a3b4279068
```

Both inline classifiers also implement the same priority: raw substring, then text substring, else absent (counter lines 111-116; tool lines 32-37). Counter lines 210-220 independently decode and classify each frozen quote, require its expected result, and compare against the tool's reported derived result. Lines 201-204 already require every frozen ID's `passed is True` and `derived == expected`, so line 219's allowance of `None` cannot admit a missing result.

### B. Boolean-is-integer attack

Absolute location: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py:205-207,222-223`.

The Eval cell extracted the actual T0 AST assignment value named `totals_ok`, compiled only that expression with `compile(ast.Expression(totals), '<T0 totals_ok>', 'eval')`, and evaluated it against the parsed frozen table. Exact expression:

```python
isinstance(total, int) and isinstance(passed, int) and total == passed == len(FROZEN_CASES)
```

Observed output:

```text
total=4 passed=True totals_ok=False
total=True passed=True totals_ok=False
total=True passed=4 totals_ok=False
total=4 passed=4 totals_ok=True
total=4 passed=False totals_ok=False
```

`isinstance(True, int)` is true but `True == 4` is false. Four is fixed by the frozen table; no boolean can equal four. Therefore this specific hazard is rejected even without relying on the SHA pin, `frozen_ok`, or top-level `ok is True`. In the canonical tool, `total = len(cases)` and `passed = sum(1 for c in cases if c['passed'])` (tool lines 97-100) independently ensure honest integer counts. Counter lines 222-223 additionally require frozen flags, matching derivations, and the literal boolean `ok`.

### C. `by_id` shape and overwrite attack

The Eval cell likewise extracted the actual T0 AST assignment named `by_id`, compiled only that expression with `compile(ast.Expression(by_expr), '<T0 by_id>', 'eval')`, and supplied hostile lists. Exact expression:

```python
{c.get('id'): c for c in cases if isinstance(c, dict)}
```

Observed output:

```text
cases=[null, 3, "junk", [], {}] by_id={None: {}}
cases=[{"id": []}] error=TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
cases=[{"id": {}}] error=TypeError: cannot use 'dict' as a dict key (unhashable type: 'dict')
cases=[{"id": "x"}, {"id": "x", "passed": false}] by_id={'x': {'id': 'x', 'passed': False}}
```

Non-dictionary entries cannot supply a missing frozen ID; malformed dictionaries with absent IDs cannot satisfy the four fixed keys. Overwriting an ID is observable in isolation, but the pinned tool emits unique fixed string IDs, so fixture mutation cannot reach it.

## Residual risk and verification gaps

- `xd://lsp` was requested before textual review and returned `No such tool: xd://lsp`; no server/status/reference/definition/diagnostic device was available. AST and source inspection are the fallback, not semantic LSP proof.
- No end-to-end counter or tool selftest was invoked; this reviewer inspected the canonical run and exercised isolated table/guard expressions only. The existing green-after receipt was not independently reproduced by this seat.
- No fixture repo, commit, runtime replacement, environment attack, or SHA collision attempt was made. This report does not establish a general sandbox guarantee. Hostile output tests bypass the digest gate only as expression-level probes and are not claimed as production-reachable attacks.
- Duplicated tables are a future maintenance coupling, but both current instruments are frozen and match. No current scoring drift was found.
- A scratch directory was explicitly created at `/fast/scratch/hyaku/kake-r64/ReviewerC2Rederive/` and removed in the Eval cell's `finally`; observed final output: `scratch_removed=True`. No fixture git mutation was performed. No tools were installed or updated.

## Self-evaluation

Accuracy 4/5: byte comparisons and boolean/shape probes are observed, but no runtime receipt reproduction. Completeness 4/5: all assigned rederive/table/boolean/indexing concerns covered; environment attacks excluded. Clarity 4/5: distinguishes the defensive overclaim from production reachability. Actionability 4/5: exact source spans and probe expressions supplied; no forbidden instrument edits. Conciseness 4/5: detailed evidence retained for auditability. Overall 4.0/5. Improvement priority: a separately authorized canonical-runtime reproduction would close the stated execution gap. This assessment should match the user's scoped review expectations.
