# SentinelFixtureSafety — round-64 security review of committed instruments

Seat: SentinelFixtureSafety (leaf, no subagents). Lane: /home/vgpnk/Projects/shokunin/kake-shokunin.
Measured T0: 4c8295fa5e3b628f1fdf3840299ae415c01849fb (lane HEAD cc8add1fa740b920ea5179a71152680ab220c70c; wave/lesson tracked files are clean against HEAD).
Scope: `.ufo/waves/round-64/c64_calibration.py`, `c64_quote_tool.py`, `fixtures/build_fixtures.py`, `fixtures/stub_tool.py`, `corpus/lessons/round-64.md`, `controls/*`, plus the committed recipe and tool blobs they execute.

## Verdict

No exploit path found against the committed instruments as frozen. The three frozen instruments and the stub fixture are sha-pinned and their executed code is pinned by sha before execution. Three low-severity defects exist that are reachable only after the frozen pin is bypassed (a modified counter), plus one informational note. No finding changes a frozen predicate result. Nothing was edited, committed or pushed; the lane working tree is unchanged.

## Frozen bytes (read-only check)

```
$ sha256sum .ufo/waves/round-64/c64_calibration.py .ufo/waves/round-64/c64_quote_tool.py .ufo/waves/round-64/fixtures/build_fixtures.py .ufo/waves/round-64/fixtures/stub_tool.py
5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf  .ufo/waves/round-64/c64_calibration.py
96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b  .ufo/waves/round-64/c64_quote_tool.py
7fbd8cbc67c17264096e44474a698b3f0d7702c3e1cc23f0b5bdaa26ee0271d3  .ufo/waves/round-64/fixtures/build_fixtures.py
7c78a05df78703044f8fe8fa02793a63b580f6353f58e8ebcee836038762edde  .ufo/waves/round-64/fixtures/stub_tool.py
$ git diff --stat HEAD -- .ufo/waves/round-64 corpus/lessons/round-64.md   # (no output)
```
All four match the contract's freeze hashes. Executed recipe at base: `6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405` (matches RECIPE_SHA). Executed tool at base: `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14` (matches FROZEN_TOOL_SHA).

## Per-item verdicts

### 1. Network calls — PASS
`grep` over the scoped files for `urlopen|urllib|requests\.|socket|http\.client|ftplib|ssl` finds only `controls/census-*.txt` lines that quote a URL token `urllib.parse` as citation data. No instrument imports a network module. The only network activity in the round is the author's one S432 GET, recorded in `.ufo/waves/round-64/sources/receipts.json` (`method GET, httpStatus 200, bytes 1854393`) and performed outside the committed instruments.

### 2. eval/exec of remote bytes — PASS, with the importlib question answered
Only dynamic-code site: `c64_calibration.py:122-129` `load_recipe`, which writes the recipe blob to a fresh `tempfile.mkdtemp` directory and runs `spec.loader.exec_module`. Bound-safety analysis:
- The bytes are `git show <rev>:<RECIPE_REL>` from the `--root` object store, never the worktree (`c64_calibration.py:186-200` region, `git_show`).
- Execution is gated on the sha pin: `pins = int(not missing and not drift)` (line 208) requires all four blobs (raw, text, ledger, recipe) to hash to their constants; `load_recipe` runs only under `if pins and ledger_state == "ok":` (line 221). A recipe with any other sha is never executed.
- The same in-memory bytes that were hashed are the bytes written and executed (single read, no re-read, so no TOCTOU). The temp directory is fresh (`mkdtemp`, mode 0700) and is removed in `finally` (`shutil.rmtree`, line ~241).
- The committed recipe is stdlib only (`argparse`, `html.parser`, `sys`); import has no I/O side effects; `main()` runs only under `__main__` (verified by reading `.ufo/waves/round-63/quote-class/extract_text.py` at base).
- Selftest T7 (`c64_calibration.py:411`) execs the BASE recipe without re-checking its sha. This is bound by git content addressing: the BASE commit id fixes the blob bytes, and a missing commit yields `None` → exit 2. Acceptable; noted only.
- `c64_quote_tool.py` executes the tool only after `if tool_sha != FROZEN_TOOL_SHA:` returns (line 154). The canned stub is never executed: `controls/stub-c64.txt` prints `tool_sha=mismatch selftest=skipped ... met=false`, consistent with the code.
- No `eval`, `exec`, `pickle`, `marshal`, `__import__`, `os.system`, `os.popen` in any scoped file (recursive grep).

Conclusion: the importlib use is bound to the committed recipe blob and is gated on its sha constant before any byte is executed. Safe under the frozen pins.

### 3. Path traversal / `..` handling — PASS
- Every `os.path.join` in scope joins a module constant: `RAW_REL`, `FIXTURE_RELS`, `TOOL_REL`, `RECIPE_REL`, fixture names (`c64_calibration.py:124,285,288`; `c64_quote_tool.py:132,175,252,255`; `build_fixtures.py:36,76,79`). No relative path from user input is joined, so no `..` handling is needed and none is exposed.
- Operator-supplied values: `--root` (only as `git -C` argument), `--revision` (argv), `--selftest-work` (workdir), `build_fixtures.py <workdir>` and `--lane`. All are passed in argv form.
- `--revision` option injection (informational, see F4): a dash-prefixed value is rejected by `git rev-parse --verify` before `git show` runs.

Reproduced:
```
$ python3 -B c64_quote_tool.py --root <lane> "--revision=--output=<scratch>/viaCounter:x"
could-not-evaluate: revision --output=<scratch>/viaCounter:x unreadable
rc=2                          # no file created
$ git -C <lane> show "--output=<scratch>/outshow:.ufo/.../stub_tool.py"
fatal: could not open '<scratch>/outshow:.ufo/...' for writing: No such file or directory
rc=128                        # git does treat the arg as an option, but only if reached
```

### 4. subprocess argv / shell=True — PASS
Every `subprocess.run` in scope uses an explicit argv list (`["git","-C",...]`, `[sys.executable,"-B",...]`). `grep shell\s*=\s*True` finds nothing in scope.

### 5. Credential material — PASS
Recursive grep over `controls/`, `fixtures/`, both counters, `sources/receipts.json`, `corpus/lessons/round-64.md` and the untracked `sources/S432.live.html` for PEM private-key headers, `AKIA[0-9A-Z]{16}`, `ghp_…`, `sk-…`, `xox[bp]-`, `password=`, `Bearer `, `Authorization:`, `api_key` returned 0 secret matches. Hits for the words "credentials", "token", "Authorization" appear only as WHATWG spec prose (e.g. `S432.live.html:634`, `:1868`). Environment handling: the quote-tool child env is restricted to `PATH, HOME=<work>, TMPDIR=<work>, LANG=C` (`c64_quote_tool.py:171-172`). The calibration selftest children inherit full `os.environ` (`c64_calibration.py:334`, `c64_quote_tool.py:288`); no secret is read by either, so this is noted only.

### 6. Selftests write only under their work dirs — FAIL (minor, F2)
Reproduced with TMPDIR redirected to scratch:
```
$ TMPDIR=<scratch>/cal-tmp python3 -B c64_calibration.py --root <lane> --selftest --selftest-work <scratch>/cal-work
selftest 26/26   (rc=0)
$ ls <scratch>/cal-tmp
c64-t7-vs93h969          # left behind outside the work dir
```
The quote-tool selftest with the same redirect left nothing in TMPDIR (`ls` empty, `selftest 11/11`).

### 7. Fixture builder (`build_fixtures.py`) — PASS
Ran into scratch with `--lane <lane>`: all four fixtures created under the work argument; `git -C <dir> rev-parse --show-toplevel` equals each fixture dir; `git -C <lane> status --porcelain` identical before and after (no lane write). Tree ids reproduce the l1 receipts exactly (commit ids differ only by commit timestamps, as expected):
```
stub-repo         mine=f8271b1174dc955458fd2df8c7ba2e9ddf2b23ba l1=f8271b1174dc955458fd2df8c7ba2e9ddf2b23ba
marker-repo       mine=8cab4d289e94713f78fc87e8fe82756375bbca0d l1=8cab4d289e94713f78fc87e8fe82756375bbca0d
fabrication-repo  mine=c8dc2d141203a96e4f680e8d77af7241cc8ccd37 l1=c8dc2d141203a96e4f680e8d77af7241cc8ccd37
junk-repo         mine=fe8c1cfa9c6ebb06c1d23eb2f032b177289d6e31 l1=fe8c1cfa9c6ebb06c1d23eb2f032b177289d6e31
```
`stub_tool.py` bytes sha `7c78a05d…edde` equal the committed stub-repo `scripts/quote_class.py` blob (`git show HEAD:scripts/quote_class.py | sha256sum`). The stub is never installed as the lane tool.

### 8. Controls and lesson — PASS for scope
No credential, network or shell content. `controls/` contains receipts only; `corpus/lessons/round-64.md` is prose plus the S432 re-open record (sha `63b0a018…911b`, matches `receipts.json`).

## Findings

### F1 — Low (defense-in-depth; reachable only past the sha pin). `by_id` crash on hostile tool output
- Where: `.ufo/waves/round-64/c64_quote_tool.py:200` `by_id = {c.get("id"): c for c in cases if isinstance(c, dict)}`.
- Claim contradicted: docstring line 22 says "shape-hostile output prints met=false, never a traceback."
- Reproduced in a scratch copy whose `FROZEN_TOOL_SHA` was replaced by the sha of a hostile tool that emits `{"cases":[{"id":["unhashable"],...}]}` (scratch repo, real S432 blobs from base):
```
Traceback (most recent call last):
  File ".../c64_quote_tool_patched.py", line 367, in main
    code, out = evaluate(args.root, args.revision)
  File ".../c64_quote_tool_patched.py", line 200, in evaluate
    by_id = {c.get("id"): c for c in cases if isinstance(c, dict)}
TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
exit=1
```
- Impact: no false green. The traceback exits 1 (same code as met=false), prints no `met=true`. The only way to reach it is to change the frozen sha pin, which the frozen counter prevents. The selftest T4 covers `safe_json` only, not this line.
- Smallest remediation (not applied; frozen file): require `isinstance(c.get("id"), str)` before keying, or wrap the comprehension in `try/except TypeError` → `met=false`.

### F2 — Low. Selftest temp directory escapes its work dir
- Where: `.ufo/waves/round-64/c64_calibration.py:411` `load_recipe(real["recipe"], tempfile.mkdtemp(prefix="c64-t7-"))`.
- The directory is never removed and lives in the default TMPDIR, outside `--selftest-work` and outside the `finally` cleanup. Reproduced (`<scratch>/cal-tmp/c64-t7-vs93h969` left after a green selftest).
- Impact: an empty-ish scratch leak, plus a violation of the literal "selftests write only under their work dirs" bar. No secret or data is written there (only the recipe bytes at BASE).
- Smallest remediation: use `os.path.join(work, "t7")` and `os.makedirs` in the selftest work dir.

### F3 — Low (reachable only past the sha pin). Recipe `SystemExit` escapes the counter
- Where: `.ufo/waves/round-64/c64_calibration.py:232` `except Exception as exc:` around `load_recipe` + `mod.extract(...)` (lines 225-231).
- `SystemExit` and `KeyboardInterrupt` are `BaseException`, not caught. Reproduced in a scratch copy with `RECIPE_SHA` re-pinned to a recipe that is `import sys; sys.exit(7)`:
```
$ python3 -B cal_patched.py --root <scratch repo> --revision <rev>
exit=7        # no verdict line; the counter exits with the recipe's code
```
- The exec occurs only after the sha pin passes (line 221), so this requires a modified counter and a matching pinned recipe; it cannot occur with the frozen instruments. A pinned recipe that loops forever would also hang the counter (no timeout on the exec); the committed recipe does not do this.
- Smallest remediation: `except BaseException` for the recipe exec, or run the recipe in a child with a timeout.

### F4 — Informational. `--revision` reaches git argv in option position
- `--revision` is passed as `git rev-parse --verify <rev>` and `git show <rev>:<rel>` in argv form (no shell). Dash-prefixed values are rejected by `rev-parse` (`fatal: Needed a single revision`, counter exit 2) before any `git show` runs. Reproduced above. Operator-supplied argument only; no remote input reaches it.

## Other observations (no action)
- `c64_quote_tool.py` evaluates a fixed frozen tool after a sha check; its `RUN_TIMEOUT=120` applies. `c64_calibration.py` has no timeout on git calls; local repos make this moot.
- `build_fixtures.py` defaults `work` to a relative `fixtures-built` (cwd-relative); operator arg, no traversal.

## Tools
No tools were installed or updated. Used only `git`, `python3`, `sha256sum`, `grep`, `diff`, `rm` (cleanup). `pacman` not used (paused host-wide). `/home/vgpnk/.omp/agent/RULES.md` was not found at the path `/home/vgpn/.omp/...` (typo in my first read); the correct path was read after the retry.

## Scratch
All scratch under `/fast/scratch/hyaku/kake-r64/SentinelFixtureSafety/` (hostile repo, argv probes, recipe-exit repo, fixture build `fx/`, TMPDIR probes). Removed before yield.

## Writes
Only this file: `.ufo/waves/round-64/w1/SentinelFixtureSafety.md`. No frozen instrument, control, receipt, contract or lesson was edited. No git/jj mutation; read-only `git show/rev-parse/status/diff` only.
