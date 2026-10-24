# W1 ReviewC1ProbeCode — review of `.ufo/waves/round-33/c1_code_probe.py` @ bc6c4a8

Sandbox: `/fast/scratch/hyaku/kake-r33/w1/ReviewC1ProbeCode/` (lane clone at
`bc6c4a8d435473f3c30903210be30d9d6e3ef750`, `TMPDIR` = sandbox `tmp/`). Crafted revs exist
only in the sandbox clone: `ca647be` (benign fixture corrupted), `craft-b` (runner file
removed), `7bc32ea` (guard raise split over two lines). No tools installed.

## Round-32 routed item 3 — repair check (all four attacked points)

1. **Kill gated on guard_ok — REPAIRED.** `killed(entry)` reads
   `out["guard_ok"] and entry.get("exit") == 1 and entry.get("failing") == [P6]`
   (c1_code_probe.py ~line 163). Docstring claim "a kill never counts when guard_ok is
   false" is now enforced in code.
2. **Timeout returns a verdict — REPAIRED.** `run()` catches `TimeoutExpired` →
   `{"exit": None, "timedOut": True, "summary": None}`. Unit demo: `run(["sleep","5"])`
   with `TIMEOUT=0.5` → that dict, no raise; such an entry cannot be `killed`
   (exit None != 1). Verified.
3. **Crashed harness reading as killed — substantially narrowed, one residual path (F4).**
   Exit 1 with no/invalid JSON → `failing` None → not killed. Exact-set test
   `failing == [P6]` is exact. Verified.
4. **Variant patterns — verified at bc6c4a8:** `GUARD.findall` = 1 (fail-closed exit 2
   otherwise); `replace_in_guard` confines edits to the matched block's raise line and
   requires `count(old)==1` else `applicable: false`; `m3 = GUARD.sub(count=1)`. One
   brittleness (F5). Baseline runs reproduce L1 receipts exactly: met 2, guard_ok true
   at both 5777d5a and bc6c4a8 (expectations: pristine+m3 true; reworded false since P6
   spec still keys `reason_contains`; recoded not applicable, no code literal yet).

## Findings

- **F1 LOW — git subprocesses have no timeout; a stalled git wedges the probe mid-run
  emitting nothing.** `subprocess.run(["git","-C",..., "rev-parse",...])` and
  `git archive` (~lines 103, 115) lack `timeout=`; only harness/variant runs are timed.
  Repro: `printf '#!/bin/sh\nsleep 60\n' > fakebin/git; chmod +x; PATH=fakebin:$PATH
  timeout 12 python3 -B clone/.ufo/.../c1_code_probe.py --rev bc6c4a8 --repo clone`
  → exit 124 (killed by wrapper), 0 bytes of JSON — not even the exit-2 error path.
- **F2 LOW — export failures beyond `git archive` crash with exit 1, outside the
  documented {0,2} contract.** A rev whose tree lacks `scripts/citing_set_selftest.py`
  (or the hostile script) hits `runner.read_text`/`read_bytes` → FileNotFoundError
  traceback. Repro (rev `craft-b`, `git rm scripts/citing_set_selftest.py` on bc6c4a8):
  probe exit 1, `FileNotFoundError .../export/scripts/citing_set_selftest.py`.
- **F3 LOW — pass expectations also AND `guard_ok`: a benign-fixture failure flips
  `met` to 0, conflating environment failure with claim failure.** `pristine_passes =
  passes(pristine) and out["guard_ok"]` (~line 167). Repro (rev `ca647be`, corrupted
  `01-single-literal-clean/expected.json` on bc6c4a8): probe exit 0, `guard_ok` False,
  `met` 0 — though the pristine hostile run exits 0 with all specs passing and the P6
  code-keying claim is unexercised either way. `guard_ok` itself is honestly computed
  (pristine hostile exit 0 + `failing == []` + benign runner exit 0).
- **F4 LOW — an exception-path spec failure is indistinguishable from a genuine
  refusal; the counter never inspects `detail`.** Hostile catches per-case
  `OSError/RuntimeError/SubprocessError` and emits `{"case": name, "passed": False,
  "detail": {"error": ...}}` (hostile line ~253) — exit 1, P6-only in `failing` if the
  error hits only P6 → `m3_killed: True` without the runner being evaluated. Unit demo:
  `spec_rows`/`failing` on `{"case":"P6-commit-before-init","passed":False,
  "detail":{"error":"OSError: disk full"}}` → `failing == ["P6-commit-before-init"]`.
  Narrower than round-32 F3 (needs error confined to P6) but nonzero.
- **F5 LOW — GUARD matches a multi-line raise and m3 then builds a syntactically broken
  mutant.** `raise \w+\([^\n]*\n` swallows only the first line; deleting leaves a
  dangling `"%s..." % CASE_SETUP_FILE)` → SyntaxError → all 6 specs fail → `failing` =
  all six, `m3_killed` False. Repro (rev `7bc32ea`, raise split over two lines on
  bc6c4a8): probe exit 0, `met` 1 (pristine only), m3 `failing` = [P1..P6]. Fail-closed
  and the JSON honestly shows all specs failing, but the "not killed" verdict means
  "mutant unbuildable", not "P6 passes" — and `reworded`/`recoded` also become
  inapplicable since the raise line no longer carries the fragment/literal.
- **F6 NOTE (latent) — `spec_rows` drops non-dict `cases` entries silently** — an
  overclaim direction: a malformed harness hiding a failure could let `failing ==
  [P6]` read as a clean kill. Demo: `[dict, "GARBAGE", dict(P6 fail)]` → `failing` =
  `[P6]`. Unreachable with the bc6c4a8 harness (always emits dicts, lines 251/253).

## Mechanism-attribution caveat (as round-32 F4)
`killed` = "P6 is the only failing spec"; the counter cannot tell why. After C1 lands,
m3 kills because the apply-time re-check refuses h6 with `setup_commit_without_repo`,
mismatched against the spec's expected `setup_commit_before_init` — not because the
commit escapes unrefused. The counter answers its question honestly; report wording
should not imply h6 would go undetected without the load-time guard.

## Not verified / residual
- No >900 s end-to-end hang test (unit-level only); `tarfile`/`write_text` failures
  also escape as exit-1 tracebacks (F2 class, untested). `failing` uses `passed is not
  True` — `"passed": 1` underclaims only (hostile emits booleans). Crafted revs are sandbox-only.
