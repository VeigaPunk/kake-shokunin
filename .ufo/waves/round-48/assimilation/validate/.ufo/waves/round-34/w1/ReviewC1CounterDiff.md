# KakeR34 wave1 — ReviewC1CounterDiff (leaf reviewer)

Target: `.ufo/waves/round-34/c1_matrix_count.py` (184 lines) vs parent
`.ufo/waves/round-29/c2_matrix_count.py` (176 lines). Judged axis: operability.

## What I verified
- `diff -u` the two files: exactly the declared changes, nothing else — docstring
  (+derivation note), `MATRIX` name, `MATRIX_SHA256`, `TOOL` path, `CONSTANTS`
  entries (3 old constants retargeted to the new report shape + new
  `constant-all-missing`), tmpdir/tool-file/counter/log names, and a new
  `counterSha256` output field. Judge, project, materialize, resolve,
  git_show, run_matrix, arg handling: byte-identical.
- `sha256sum c1-matrix.json` = `246a6a3b…fac14f7` = `MATRIX_SHA256` pinned in
  the counter. Counter self-reports the same digest in output.
- Counter run at declared revision a2fe31b: exit 1, `0/28`, `toolPresent=false`,
  all gates rejected. Matches `c1-at-*` before-receipts.
- Constant gates measured live (same in both runs): constant-clean 6/28,
  constant-failed-empty 0/28, constant-refuse 6/28, constant-all-missing 1/28.
  All < 28 → `constantGatesAllRejected=true`. constant-refuse misses only
  I4 (`page_unreadable` vs its fixed `input_invalid`) — consistent.

## Findings (severity-ranked)

### HIGH — counter hands the tool the oracle key in `cwd` basename; a lookup-table stub scores 28/28
`run_matrix` sets `cwd = scratch/<tool-stem>/<case["id"]>` (line ~118). The case
id is the row key of the frozen matrix, so the tool can read
`os.path.basename(os.getcwd())` and replay a canned report — no HTML, no
manifest parsing. Reproduced end-to-end:

- Built `TABLE[case_id] -> (exit, stdout)` directly from `c1-matrix.json`;
  12-line stub (`scripts/link_preview_audit.py`, sha256
  `91374902…bf880a`) committed in sandbox repo at 83f53357.
- Command: `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root
  /fast/scratch/hyaku/kake-r34/w1/ReviewC1CounterDiff/stubrepo --revision HEAD`
- Result: **counter exit 0, `passed=28/28` (6/6 control, 13/13 defect, 7/7
  input, 2/2 usage), `constantGatesAllRejected=true`** — identical verdict
  shape to a genuinely correct tool. Artifact:
  `/fast/scratch/hyaku/kake-r34/w1/ReviewC1CounterDiff/stub-run.json`.

The counter verifies "deterministic mapping on frozen inputs," not that the
tool analyzes pages. Inherent to fixed-answer test rigs, but the `cwd`-leak
removes even the need to key off input bytes. Operability note for the
claim: 28/28 alone does not evidence a real audit.

### MEDIUM — one non-UTF-8 byte on tool stdout kills the counter outright
`subprocess.run(..., text=True)` decodes tool stdout with the parent's locale;
with `LANG=C`/`LC_ALL=C` (or any non-UTF-8 environment) a single `\xff` byte
raises `UnicodeDecodeError` inside `run_matrix` — uncaught, no JSON report,
traceback + exit 1. Reproduced under both `C` and `C.UTF-8` parents on
Python 3.14.8 (the counter never sets decode `errors=`/locale for the child
read). A tool crash that happens to dump binary to stdout downgrades the
whole verdict to a Python exception.

### LOW — `judge()` accepts non-strict JSON
`json.loads` default `parse_constant` accepts `NaN`/`Infinity`/`−Infinity`.
A report `{"verdict":"clean","pagesChecked":NaN,"findings":[]}` passes a clean
case (probed: `judge` → `(True,'ok')`). Stdout containing valid JSON values
unrepresentable in strict JSON slips through.

### LOW — exit-64 path validates exit code only, stdout unchecked
`if exp["exit"] == 64: return True` — probed: exit 64 with garbage/crash
bytes on stdout judges `ok`. By design ("exit 64 needs no JSON"), but a tool
segfaulting-after-64 is indistinguishable from a clean usage error.

### LOW — findings projection ignores page, id, and extra keys
Comparison keys come only from the *expected* finding dicts (matrix never
carries `page`/`id`). Probed: a finding reporting the right reason+property
on `page:"WRONG-PAGE"` with a bogus `id` passes a defect case — for
multi-page cases (K5, D11) page attribution is unverified. Extra report keys
(`pagesChecked`, arbitrary fields) are likewise unchecked; `pagesChecked` is
never compared to manifest page count. Non-string values are `str()`-coerced
(`null` → `"None"`) — fails closed against the matrix, noted for completeness.

### LOW — stderr ignored
Crashes, warnings, and interpreter noise on stderr are invisible to the
verdict. Constants themselves rely on stdout-only checking.

## Reproduced as NOT-a-defect
- Grandchild-process fd-hold on stdout: `TimeoutExpired` still raised at
  exactly the 20 s-boundary (probed at timeout=2 vs 8 s grandchild) —
  `subprocess.run` reaps+waits correctly; timed-out tools do fail the case.
- Missing tool → `tool=None` → all rows fail, gates still run, JSON emitted,
  exit 1. Absent-tool path is honest.
- Matrix schema: all 28 cases carry `id/kind/files/expect`; no absolute or
  `..` file paths; exit-64 cases carry no JSON expectation. No crash path in
  `materialize`/`judge` from this matrix.
- `resolve`/`git_show` strip all `GIT_*` env vars; `git show` non-zero →
  `toolPresent=false`, fails closed.

## Not verified / residual risk
- A real (non-stub) tool run — tool does not exist yet at a2fe31b.
- Digest self-hash (`counterSha256`) is informational; nothing cross-checks it.
- Docstring claim "materializes … next to this file" is inaccurate (fresh
  `tempfile` dir); cosmetic.
- Constant gates run even when the tool is absent — fine, but ~112 constant
  case-runs add latency when only a 0/28 is being recorded.

## Evidence
- Sandbox: `/fast/scratch/hyaku/kake-r34/w1/ReviewC1CounterDiff/`
  (`stubrepo/` @83f53357, `stub-run.json`, `before-run.json`,
  `before-run.stderr`, `stub-run.stderr`, `probe/` repro scripts outputs).
- Counter sha256 (self-reported): `fc72d855…3b71c51e`; matrix sha256 verified.
- No tools installed; no lane mutation (counter run read-only, TMPDIR in
  sandbox); no network, no owned-property requests; report written only at
  this lane path.
