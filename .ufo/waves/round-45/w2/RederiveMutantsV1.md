# RederiveMutantsV1 — round 45, wave 2 (C2(a) before-state attack)

Seat: `kake-r45.RederiveMutantsV1` (independent leaf). Lane: `kake-shokunin`.
Axes: **operability** (primary), **freshness** (secondary).
Lane root: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Scratch: `/fast/scratch/hyaku/kake-r45/RederiveMutantsV1/` (all scratch artifacts there).
No tool installs were needed (python3.14 and uv-provided 3.10–3.15 already present; no pacman invoked).

## Verdict on the named attack

**CONFIRMED — the C2(a) before-state reproduces exactly as declared; this attack does not falsify it.**

- `m1` exit 1, `m2` exit 0, `m3` exit 1, `m4` exit 0 → **2/4 killed**, and the two kills are
  targeted `AssertionError`s on the very asserts the mutations break (lines 94 and 95), not crashes.
- Each v1 mutant differs from the frozen v1 driver (`round-44/c44_audit.py`, sha256
  `8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75`, byte-identical to the
  `HEAD` blob) by **one diff hunk touching only `semantic_witness()`**:
  m1/m2/m3 are 1 insertion + 1 deletion; m4 is 2 insertions + 0 deletions (one inserted
  conditional, `if row.get("error"): return True`). Literal "one-line" is exact for m1/m2/m3 and
  loose for m4, which matches `MutClassGate.md`'s own two-line m4 snippet.
- All four mutations match the `MutClassGate.md` definitions **exactly at the behavioural level**:
  1,260-case exhaustive equivalence, 0 mismatches (details in §3). m2/m3 inline the key tuples
  instead of the documented module-level `TIMING_KEYS`/`V4_RUN_KEYS` constants; that is a textual,
  not behavioural, deviation.

Findings below are about the **instrument and evidence provenance**, not the 2/4 count.

## 1. Baseline integrity (frozen driver and mutants)

```
$ sha256sum .ufo/waves/round-44/c44_audit.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75
$ git show HEAD:.ufo/waves/round-44/c44_audit.py | sha256sum
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75
$ git status --porcelain -- .ufo/waves/round-44/c44_audit.py .ufo/waves/round-45/mutants/m{1,2,3,4}.py
(empty)

m1 9816de74ea89c00dfa324509bfa1cf8f3c788d36fa6d1c0cd9cfa9c2bf2e9511
m2 d6e2a3b25c09cb6a5858b98bc8013e6aa0feffab505124bb00a177a388f45a1b
m3 0ecd960db4af22fd0c7b114aa350b7734a78c023069b0d47cff4cd995beb1646
m4 7bf8a4ce593065ade360ae4e6c44a6445f504d6455cbeae65101dbbd5ea43ae9
```

The frozen driver is unmodified versus `HEAD`, and the four mutants are tracked and clean, so the
before-state is measured against the committed v1 instrument, not a worktree drift.

## 2. Decisive run — the 2/4 count

```
$ for n in 1 2 3 4; do python3 -B .ufo/waves/round-45/mutants/m$n.py --selftest; echo "m$n EXIT=$?"; done
```

Verbatim output (stdout+stderr, interpreter `Python 3.14.8`):

```
m1 EXIT=1
Traceback (most recent call last):
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m1.py", line 226, in <module>
    main()
    ~~~~^^
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m1.py", line 122, in main
    selftest()
    ~~~~~~~~^^
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m1.py", line 94, in selftest
    assert semantic_witness(mixed_divergence, keys)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
m2 EXIT=0
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
m3 EXIT=1
Traceback (most recent call last):
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m3.py", line 226, in <module>
    main()
    ~~~~^^
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m3.py", line 122, in main
    selftest()
    ~~~~~~~~^^
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m3.py", line 95, in selftest
    assert not semantic_witness(v4_divergence, keys)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
m4 EXIT=0
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
```

The shipped receipts reproduce: `diff -q` of my assembled transcript against
`verification/selftest-coverage/before/m{1,2,4}.txt` is byte-identical; `before/m3.txt` matches
except for the caret-glyph line (finding F2). The trailers in the shipped files are
`SELFTEST_EXIT=1|0`, matching the exits above.

Why exactly these two die (mechanism, not just exit codes):

```
fixture replay (frozen,m1,m2,m3,m4):
  passing                     [False, False, False, False, False]
  class_divergence            [True,  True,  True,  True,  True ]
  v4_divergence               [False, False, False, True,  False]
  mixed_divergence            [True,  False, True,  True,  True ]
  legacy_divergence           [False, False, False, True,  False]
  class_divergence_emptykeys  [False, False, False, False, False]
fixtures containing a T* key: []
fixtures carrying an 'error' key: []
```

- m1 (`any`→`all`) flips `mixed_divergence ["D","G3"]` from True to False → `assert semantic_witness(mixed_divergence, keys)` (line 94) fails.
- m3 (accepts A–F) flips `v4_divergence ["D"]` from False to True → `assert not semantic_witness(v4_divergence, keys)` (line 95) fails.
- m2 (accepts T1–T5) and m4 (`error` ⇒ witness) change **no fixture's** value, because the frozen
  selftest has neither a timing-key row nor an error-key row. Their survival is a genuine fixture
  gap, not a no-op mutation.

## 3. Mutation fidelity — one hunk each, definitions exact

```
$ for n in 1 2 3 4; do diff -u .ufo/waves/round-44/c44_audit.py .ufo/waves/round-45/mutants/m$n.py; done
```

| mutant | numstat vs frozen | hunks | mutation |
|---|---|---|---|
| m1 | 1 ins / 1 del | 1 | `any(... key in class_keys ...)` → `all(...)` in `semantic_witness` |
| m2 | 1 ins / 1 del | 1 | adds `or key in ("T1","T2","T3","T4","T5")` inline |
| m3 | 1 ins / 1 del | 1 | adds `or key in ("A","B","C","D","E","F")` inline |
| m4 | 2 ins / 0 del | 1 | inserts `if row.get("error"): return True` before the class-key test |

Exact diffs (from `diff -u`, only these lines):

```
m1: -            any(isinstance(key, str) and key in class_keys for key in caught))
    +            all(isinstance(key, str) and key in class_keys for key in caught))
m2: -            any(isinstance(key, str) and key in class_keys for key in caught))
    +            any(isinstance(key, str) and (key in class_keys or key in ("T1", "T2", "T3", "T4", "T5")) for key in caught))
m3: -            any(isinstance(key, str) and key in class_keys for key in caught))
    +            any(isinstance(key, str) and (key in class_keys or key in ("A", "B", "C", "D", "E", "F")) for key in caught))
m4: +    if row.get("error"):
    +        return True
```

The `selftest()` body is untouched in every mutant — the sole hunk is inside `semantic_witness()`.
So the before-leg measures *the frozen v1 selftest against the mutations*, which is the claimed
baseline.

Behavioural equivalence harness (`/fast/scratch/.../equiv.py`, imports each module via
`importlib` and compares against a literal reference implementation of each `MutClassGate`
definition over 21 `caughtBy` shapes × 3 `met` values × 10 `error` shapes × 2 class-key sets):

```
rows x keysets = 1260
definition mismatches (mutant vs documented ref): {1: 0, 2: 0, 3: 0, 4: 0}
behavioural delta vs frozen (non-vacuity): {1: 50, 2: 70, 3: 120, 4: 472}
```

0 mismatches proves each mutant implements *exactly* its documented definition and nothing else;
non-zero deltas prove none is a no-op. The constant-vs-inline deviation is therefore cosmetic.

## 4. Findings by severity

### F1 — MEDIUM (operability): the C2(a) kill counter scores any non-zero exit as a kill

`c45_freshness.py:34-37` returns only `proc.returncode`; `:64-69` increments a kill when
`run_selftest(...) != 0`. Running the counter's own function on four paths:

```
pristine m1 (true kill)      rc=1  counted_as_kill=True
m2 (true survivor)           rc=0  counted_as_kill=False
syntax-broken m1 copy        rc=1  counted_as_kill=True
nonexistent mutant           rc=2  counted_as_kill=True
```

A mutant that fails to parse, or whose file is missing, is counted as **killed**. Today's numbers
are not corrupted by this (the two before-kills are verbatim `AssertionError` tracebacks at
lines 94/95, and all four after-mutants likewise fail with targeted `AssertionError`s on
`timing_only`, `v4_divergence`, `errored_class_witness`), but the instrument would print **4/4**
from broken or absent mutants. Additionally the pass gate is
`ok = (v4_before is not None and v4_after is not None and split is not None and
before_kills + after_kills > 0)` (`c45_freshness.py:94-95`): a 0/4 + 1/4 run still exits 0, so
the named counting command cannot fail the claim it prints. Repair direction: require
`AssertionError` in the captured stderr (the function currently discards it) or a per-mutant
sentinel, and gate `ok` on the specific expected tuple.

### F2 — LOW (evidence provenance): `before/m3.txt`'s caret line is not reproducible by any installed CPython

`before/m1.txt`, `before/m2.txt`, `before/m4.txt` reproduce byte-for-byte with my assembled
transcripts; all four `after/m*.txt` reproduce with every traceback byte identical and only my
trailer label differing (`SELFTEST_EXIT=` versus the file's `EXIT=`).
`before/m3.txt` differs in exactly one line — the underline under
`assert not semantic_witness(v4_divergence, keys)`:

```
shipped before/m3.txt : 19 tildes + 21 carets (40 columns)
3.11.17 / 3.12.15 / 3.13.16 / 3.14.8 / 3.15.0 : 0 tildes + 41 carets (41 columns)
```

Every installed interpreter (3.11–3.15) renders all carets for `assert not <call>`; 3.10 lacks
fine-grained carets entirely. The semantic content of `before/m3.txt` (frames, line 95, source
line, `AssertionError`, exit 1) reproduces exactly, so the verdict is unaffected; but at least one
transcript was not produced by the interpreter now on `PATH`, or was edited after capture. Strict
byte-reproducibility of the before evidence set holds 3/4, not 4/4.

### F3 — LOW (wording fidelity): "one-line mutation" is literal for m1/m2/m3 only

- m4 is a two-line insertion (the `MutClassGate.md` snippet is also two lines; its prose
  "one-line behavioural mutation" is the loose part, and the shipped file follows the snippet).
- m2/m3 inline `("T1",…)` / `("A",…)` where `MutClassGate.md`'s diff adds module-level
  `TIMING_KEYS` / `V4_RUN_KEYS`. Proven behaviourally identical (§3), so this is a documentation
  mismatch only; anyone diffing a transcript against `MutClassGate.md` literally will see it.

### F4 — INFO (lane state): `after/` evidence is uncommitted, and appeared during this run

At first observation (`~00:57`) `verification/selftest-coverage/after/` was empty; at `01:00` it
held `m1..m4.txt` (mtime `00:58`), untracked. `git ls-tree HEAD` contains only
`selftest-coverage/before/m{1..4}.txt`. The four after transcripts reproduce from
`mutants/m{1..4}_v2.py` (which differ from the committed driver `c45_audit.py`, sha
`f3c3171b…`, by exactly one line each: m1 `any`→`all`, m2/m3 key-tuple inline, m4
`return False`→`return True` in the `error` branch), so after=4/4 is independently confirmed —
but the scorecard's `after/` pointer resolves only in the worktree at this moment, not at `HEAD`.

### F5 — INFO (shared worktree): the live `c45_audit.py` changed under this seat

During this run (mtime `00:59:29`) `.ufo/waves/round-45/c45_audit.py` gained **+28 lines** versus
`HEAD` (`git diff --stat HEAD` → `1 file changed, 28 insertions(+)`): an `if not __debug__:`
assert-disabled guard plus bad-build cohort checks. This was not my write (my only write is this
report). The committed driver remains `f3c3171b…`; the v1 baseline is unaffected (frozen driver and
m1–m4 clean before and after). Any seat measuring the v2 driver must pin the `HEAD` blob rather
than the worktree.

## 5. Residual risk

- **2/4 is mutant-specific, not the selftest's total discriminating power.** A broader scratch
  mutant that drops the class-key test entirely (`return (row.get("met") is False and bool(caught))`)
  is killed by the same frozen selftest at line 95:
  `File "/fast/scratch/hyaku/kake-r45/RederiveMutantsV1/broad_m.py", line 94, in selftest` /
  `assert not semantic_witness(v4_divergence, keys)` / `AssertionError`. `2/4` must not be read as
  "v1 catches half of all plausible mutations".
- **The metric is assert-based.** Under `PYTHONOPTIMIZE=1` all four v1 mutants exit 0 (0/4):
  `m1..m4 under PYTHONOPTIMIZE=1 EXIT=0`. The counter does not set that environment, but it inherits
  whatever the caller has; the committed v2 driver has no `if not __debug__` guard (the guard seen
  in F5 is still uncommitted).
- **F1's weak gate** means the counting command's exit status is not evidence for 4/4; only the
  per-mutant transcripts are.
- The 2/4 result depends on the mutants embedding the frozen v1 selftest unchanged; this is proved
  by the single-hunk diffs, so it is not a live risk, only a precondition to re-check if the
  mutants are ever regenerated.

## 6. Verification gaps (explicitly unrun)

- I did **not** run `python3 -B .ufo/waves/round-45/c45_freshness.py` in the tree: it writes
  `verification/freshness/freshness.json`, outside this seat's write path. I reproduced both of its
  input loops exactly (same four commands, same `sys.executable`), read its aggregation
  (`:34-37`, `:62-70`, `:94-95`), and confirmed `verification/freshness/freshness.json` records
  `before=2, after=4`; the number is re-derived, the writer was not re-executed.
- No `lsp` device is exposed in this seat's toolset; semantic claims here rest on execution,
  byte diffs and AST extraction, not text grep (grep was used only for file discovery).
- I could not identify which interpreter build produced `before/m3.txt`'s caret line — 3.10–3.15
  are all installed and none reproduces it; a pre-release/patch build not present on this host
  remains a possible explanation.
- The after-leg's mutation fidelity was cross-checked against the `HEAD` driver, but the after-state
  attack itself is `RederiveMutantsV2`'s seat; I did not duplicate its full scope.

## 7. Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2/RederiveMutantsV1.md` (this report — the only lane write)
- `/fast/scratch/hyaku/kake-r45/RederiveMutantsV1/equiv.py` (equivalence harness)
- `/fast/scratch/hyaku/kake-r45/RederiveMutantsV1/broad_m.py` (broader-mutant control)
- `/fast/scratch/hyaku/kake-r45/RederiveMutantsV1/broken_syntax.py` (crash-count control)
- `/fast/scratch/hyaku/kake-r45/RederiveMutantsV1/c45_audit_HEAD.py` (pinned HEAD blob for after-leg diffs)
- `/fast/scratch/hyaku/kake-r45/RederiveMutantsV1/repro/m{1..4}.{txt,out,err}` (transcript reproductions)

No commits, no pushes, no edits to any committed lane file, no `agent://all`.
