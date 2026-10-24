# W1 ReviewCounterC2Code — C2 counter code review (round 29)

Axes: operability, freshness. Seat: leaf reviewer. Reviewed
`.ufo/waves/round-29/c2_matrix_count.py` (176 lines) and the frozen
`c2-matrix.json` (30 cases) for bugs that change the count.

## Canonical run — claim C2 "before" state CONFIRMED

```
cd clone && TMPDIR=$SANDBOX/tmp python3 -B .ufo/waves/round-29/c2_matrix_count.py \
  --root . --revision fe1805cf32a7aadf4574637a3a8912354cee2c7b
# exit=1, 0.97s wall; JSON: toolPresent=false, toolSha256=null, passed 0/30,
# byKind control 0/7, defect 0/14, input 0/8, usage 0/1
# constantGatesPassed: constant-clean 7/30, constant-failed-empty 0/30,
#                      constant-refuse 7/30; constantGatesAllRejected=true
# stderr: "C2 0/30 at fe1805c..."
```
All 30 rows fail with `tool absent or timed out`; the three constant gates each
fail at least one case (7/0/7), so `rejected` holds and the counter exits 1.
Matches the declared claim exactly.

## Findings by severity

### F1 (medium-low, live): non-UTF-8 tool output crashes the whole counter
`run_matrix` uses `subprocess.run(..., capture_output=True, text=True)`; decode
is strict and happens inside `communicate()`, before `judge`'s
`json.loads(ValueError)` guard. One invalid byte on tool stdout/stderr raises
uncaught `UnicodeDecodeError`: no JSON report, and exit 1 — the same code a
legitimate "matrix failed" run uses. A weird-but-observable tool behavior
destroys all 30 rows instead of judging one case "stdout is not JSON".
Repro: sandbox clone2 @ abe94d5 (stub writing `b"\xff\xfe not-json"`), run at
HEAD → traceback through c2_matrix_count.py:111 → `_translate_newlines`,
stdout 0 bytes, EXIT=1.

### F2 (low, latent): finding projection is stricter than the frozen contract
`project()` takes `keys = union over the case's expected findings`, pads absent
keys with `"None"`. The matrix's declared comparison (c2-matrix.json
"comparison") selects keys per expected finding ("reason, and
element/attribute/value when given"). On a case mixing a reason-only finding
with a keyed finding, the counter rejects a contract-conforming tool: expected
`('outside_base_path','None')` vs observed `('outside_base_path','/a.css')`.
Repro: sandbox clone3, stub printing two findings that satisfy the per-finding
comparison → counter reports `passed 0/1`, detail
`findings [('outside_base_path','/a.css'), ('outside_base_path','/x.css')] != [('outside_base_path','/x.css'), ('outside_base_path','None')]`.
Not count-changing today: I verified all 30 frozen cases have one homogeneous
expected-key set per case ({reason} ×8, {reason,element,attribute,value} ×18
finding keys; no finding carries `id`, so tool-assigned ids are never compared).
Union can only add constraints (false-reject), never mask a mismatch.

### F3 (low, latent): case materialization collision crashes uncaught
`materialize()` does `work = base/case["id"]; work.mkdir(parents=True)` with no
exist_ok and no id validation. Duplicate ids, an id nested under another id
("a" + "a/b"), or traversal-style ids crash with FileExistsError/…, traceback,
exit 1, no report. Frozen matrix verified safe: 30 unique ids, no `/`, `..`,
or leading-dot ids, no within-case file-path shadowing or absolute/`..` rel
paths, every case carries files/expect/kind. Repro: clone3 with a two-case
same-id matrix → `FileExistsError: .../base_path_audit/DUP` at line 54.

## Verified clean (with what I ran)

- Environment leakage into the tool: tool env is exactly
  `['HOME','LC_ALL','PATH','PYTHONDONTWRITEBYTECODE']` — probed with an
  env-dump stub while poisoning the parent with GIT_DIR, PYTHONPATH,
  PYTHONHASHSEED (clone3, r5.env.json). No leakage; tool output can't depend
  on ambient PYTHONPATH/GIT_*/hash seed.
- GIT_ variables on the counter's own git calls: `git_show`/`resolve` strip
  `GIT_*`. Hostile-env rerun (GIT_DIR=/nonexistent GIT_WORK_TREE=…
  GIT_CONFIG_COUNT=1 …) still produced the identical canonical result while
  the same env breaks plain git (exit 128) — filtering does real work.
- Timeout handling: sleep-25 stub with TIMEOUT=20 (clone3, single-case
  matrix): child killed at 20.08s wall, row judged failed
  (`tool absent or timed out`), counter completes exit 1, no hang.
- Exit-64 path (code read): exit equality checked first; expected 64 returns
  ok without JSON — matches interface "exit 64 needs no JSON"; expected 0/1/2
  with a 64-exiting tool fails on the exit check. U1 argv case runs `[]` with
  cwd=case dir.
- Constant-gate logic: `rejected = all(v < len(cases))` per gate, each gate
  reruns all 30 cases under its own scratch stem (no dir collisions with the
  real tool run); observed 7/0/7, rejected=true. Gate values derived
  independently from the matrix (clean 7 cases with empty expected findings;
  refuse 7 reason-only input_invalid exit-2 cases; failed-empty 0) — match.
- Digest pinning: working-tree matrix sha256 75c08f64… equals MATRIX_SHA256;
  tool blob is taken from `git show <revision>:` and reported as toolSha256 —
  the counter tests the revision, not the working tree.
- Comparison mechanics: sorted-list multiset compare counts duplicates;
  verdict and findings-list type checked; exit 2 requires all finding tuples
  match (I5 page_outside_base_path included). Sound.

## Residual risk / observations (no count impact shown)

- `detail` string conflates "tool absent" and "timed out"; `toolPresent`
  disambiguates only globally.
- Tool subprocess env has no TMPDIR: if the integrated tool ever uses
  tempfile, it hits /tmp, not the operator's sandbox TMPDIR (deterministic,
  but the L1's sandbox policy won't propagate).
- No stdout size cap: TIMEOUT bounds runtime, not captured bytes.
- `str()` coercion on observed values would mask a type-deviant tool
  (e.g. numeric value) as a string match.
- A tool that spawns a grandchild holding the stdout pipe could outlive
  TimeoutExpired's kill; untested, tool contract makes it unlikely.
- No installs performed; no pacman/uv/network use.

## Commands and exit codes (all in /fast/scratch/hyaku/kake-r29/w1/ReviewCounterC2Code)

1. `git clone -q <lane> clone` — OK; HEAD e58b66c; counter+matrix byte-identical
   to lane working tree (diff -q). `scripts/base_path_audit.py` absent at HEAD.
2. Canonical counter run at fe1805c… — exit 1 (expected), output `canonical.json`,
   stderr `canonical.err`. Repeated under hostile GIT_* env — identical.
3. clone2 @ abe94d5 UTF-8 stub run — exit 1 via UnicodeDecodeError traceback
   (`r1.err`), stdout 0 bytes.
4. clone3 env-dump stub run — exit 1 (rows fail honestly); `r5.env.json` shows
   the 4-key env.
5. clone3 R2 sleep stub (matrix digest 741eb5cb…) — exit 1, 20.08s wall.
6. clone3 R3 union-keys stub (digest b19ade21…) — 0/1 with the false-reject
   detail above.
7. clone3 R4 dup-id run (digest f5c812d9…) — exit 1, FileExistsError traceback
   (`r4.err`), stdout 0 bytes.

## Verification gaps

- The real `scripts/base_path_audit.py` does not exist yet, so the counter's
  pass path against a conforming tool is unexercised end-to-end; F2's
  false-reject risk becomes live the moment a future case mixes expected key
  sets. All stub reproducers were run against sandbox clones
  (clone2/clone3); the lane repo, its index and jj state were not touched.
