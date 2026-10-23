# ReviewCounterV2 — sealed_count.py (v2, rule of record for C1) vs round-37 counter

No sealed-tree access. No real-key use: all runs are sandbox copies with my own dummy keys
(KEY_SHA256 edited); lane repo untouched. Artifacts: `/fast/scratch/hyaku/kake-r38w1/ReviewCounterV2/work/`
(stub.py sha256 `32783d4f…12f2c`, counter_wellformed.py `c7d54c69…e7453`, keys `key_*.json` hashed below,
outputs `out_*.txt`/`err_*.txt`).

## Diff vs `.ufo/waves/round-37/sealed_count.py` (28+/15-)
Only: docstring, constants (KEY_PATH/KEY_SHA256/CASES 20/TARGET 19/PREDICATE, tmp prefix), `import re`,
and the `rawTemplate` block in `materialize` (lines 120-129). Jail, fresh-id/file materialization,
pin-and-refuse, judge are byte-identical to r37 — the docstring's "same jail, same judge" claim is true.
Consistency: PREDICATE "passed >= 19 of 20" (:55) matches C1's declared sentence in SCORECARD at
2dab7f3 ("met: passed >= 19 of 20"; 20-of-20 is v3/C2, a different file). Working-tree file is
byte-identical to the declared commit blob: both sha256 `52daff55a2b897ba814eed134cd6bfe0de28305bf4ab82e87a5c6d1ae7096e7b`
= the declared "counter sha256 at this declaration". No `.ufo/waves/round-38/sealed/` in the lane tree
at 2dab7f3 or in the worktree. Leak check: counter carries only public constants; zero `/fast/scratch`
references; jail unchanged (binds /usr + scratch only, `--unshare-all --clearenv`, :185-194); git env
stripped (:43-45); tool gets `env={}` (:235).

## Findings

**R1 — MEDIUM: malformed `@FILE:` tokens crash the entire count, no receipt, exit 1 ≡ "not met".**
`sealed_count.py:125-126` does `names[token[6:-1]]` with no validation; `main` (:227-247) has no
per-case error handling, so one bad token aborts all cases before the receipt prints (:248-253).
Three reproducible triggers (all: stdout 0 bytes, KeyError traceback, exit 1; declared contract is
exit 2 = "cannot evaluate"):
- `@FILE:nope.txt@` not in `files` → `KeyError: 'nope.txt'`
- `@FILE:sub/robots.txt@` with `files {"sub/robots.txt"}` → `KeyError: 'sub/robots.txt'` (names keyed by
  basename only, :118; the manifest path handles directories at :136-140, rawTemplate does not)
- a stray `@FILE:` with no closing `@` before the real token → `KeyError: ' docs", "robots": "'` (R2)
Repro: `cd $S/work && TMPDIR=$S/tmp python3 -B counter_bad{1,2,3}.py --tool-file stub.py --key-file key_bad{1,2,3}.py`
(keys sha256 `b7aabe44…f1b6`/`ec3fea73…6691`/`22360bc6…5cee`). Same no-receipt class as routed F2
(MutCounterV2), but a distinct, unlisted trigger (materialize input validation). Risk with the real
key: one L1-authoring slip in any of the 20 templates turns the whole count into an un-debuggable
"not met". Suggested shape: wrap per-run materialize, emit an exit-2 receipt naming the case.

**R2 — MEDIUM: `@FILE:[^@]+@` is not string-bounded; a stray `@FILE:` swallows arbitrary JSON.**
:125 — `[^@]+` crosses quotes/colons/braces/newlines up to the next `@`. bad3's match spanned two
members (`@FILE: docs", "robots": "@`). If `files` happened to hold the absurd key, substitution would
silently corrupt the manifest instead of crashing. `@ID:[A-Za-z0-9_]+@` (:122) is tight and cannot
cross string boundaries — only the FILE regex is affected.

**R3 — MEDIUM (routed F1 class, now confirmed on the rawTemplate path): literal-token alias
acceptance.** A stub that ignores the manifest and emits the literal token `@ID:alpha@` passes:
`project` (:100) leaves observed ids not in the inverse map unchanged, and `judge` (:167-170) compares
them against expect's tokens — so expected tokens are valid findings for a tool that never reads the
manifest ids. Repro: wellformed run below, case `t9-literal-token-alias` passed. Routed as F1 by
MutCounterV2; SCORECARD says v3 fixes it. Advisory for v2 only (v3 is C2's scoring counter), but v2
stays C1's rule of record, so any re-scoring of C1 inherits it.

**R4 — LOW: expect-side asymmetry.** Expected findings may name ids by tokens but get no `@FILE`
substitution and reasons are compared raw (:170: `project(exp["findings"], {})`) — a case can never
assert a reason containing the fresh robots file name, and expect tokens must include the delimiters
(`@ID:x@`, not `x`) or never match. Matches the docstring's wording; a key-authoring constraint only.

**R5 — INFO: `rawTemplate` silently beats `raw` when both are present** (:120 before :130); verified
(t8: raw manifest `{"checks":[]}` ignored, template used). L1-authored keys only.

**R6 — INFO: inherited r37 warts, unchanged, not round-38 regressions.** `../`-prefixed file rels are
written to `work.parent` (:115) but referenced bare in the manifest → dangling reference if a case
used one; duplicate basenames across different rels overwrite `names[base]` (:118); non-string
`rawTemplate` would TypeError-crash (same class as R1, [INFERENCE] — not run).

## Verified good (dummy-key exercise, 5 runs, exit codes shown)
`TMPDIR=$S/tmp python3 -B counter_<v>.py --tool-file stub.py --key-file key_<v>.py`:
- wellformed (key `1820a8ad…2e78`): **6/6, met=true, exit 0** — repeat token shares one fresh id while
  distinct tokens differ (t1, ids `c`+hex, no `@`); `@FILE` substitution resolves to a fresh existing
  name ≠ original (t2); check-id round trip through the inverse map matches expect tokens (t2);
  a token inside a robots file body is NOT substituted (t6 — files are written before templating);
  id substitution inside an unrelated string field happens, while a plain `a@b.c` literal survives
  (t7); expected-findings mapping is enforced — neg run (key `54bd0198…530c`, wrong token in expect):
  0/1, met=false, exit 1.
- No leak observed in any run: tool saw only the scratch dir (jail held; stub reads nothing outside
  `--manifest`).

## Residual risk / not verified
Real sealed cases unopened (no key — by design); v3 counter out of scope; lone-surrogate-in-template
crash inferred, not run; the 64 MiB / 20 s bound not exercised. KEY_SHA256/CASES/TARGET edits in my
copies are test-only adaptations, disclosed above; logic otherwise pristine (diff vs lane file on request).
No tool installs or updates were made.
