# Review: `c44_audit.py` as contract instrument — `--expect` vs SCORECARD predicates

Seat: `kake-r44.ReviewCounterContract` (wave 2). Reviewed
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/c44_audit.py`
(sha256 `8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75` — the
frozen, declared bytes) end-to-end against the SCORECARD round-44 C1 predicate,
the frozen predicate reading (`SCORECARD.md:3562-3570`), and kill rules
(`SCORECARD.md:3454-3458`). Counter under audit:
`c44_count_v5.py` sha256 `5cedaa3b9f91…7672bc` (verified on disk).

**Verdict on the named attack — FAIL (defects found).** `--expect` does not
implement the SCORECARD predicates exactly: the instrument certifies witnesses
from evidence kill rule (2) says is not a witness, trusts receipts it cannot
bind to the run it just made, and does not pin the "three unseeded runs"
count. One hole is demonstrated end-to-end below; the rest are demonstrated on
the exact row/dict shapes `score()` produces.

## Clause-by-clause trace (what is correct)

| Predicate clause | Code | Verdict |
|---|---|---|
| Unseeded scoring | `run_counter` never passes `--seed` (`:49-53`); counter falls to `int.from_bytes(os.urandom(6))` (`c44_count_v5.py:995`); seed recorded in receipt (`:997`) and mirrored into the audit row (`:159`) and build row (`:177`) | OK |
| Per-row receipts | `tools/<name>.json` under `<outdir>/tools/` (`:131-132,148`), relpath recorded (`:159`); builds at `outdir/build-N.json` (`:174`) | OK |
| Exit codes | `sys.exit(0 if ok else 1)` (`:222`); argparse errors → exit 2 | Partial — see defect 5 |
| Witness classifier = at-least-one class key | `semantic_witness` (`:63-66`): `met is False` ∧ any `caughtBy` key in `class_keys`; `class_keys` = `CLASS_MODULES` names iff `--classes v5` (`:165`) | Classifier OK in isolation; the rows fed to it are the problem (defect 1) |
| v4-mode blindness | `class_keys == []` under `--classes v4` → `not witnessed` vacuously true — "0 by construction" (`:165,210`) | OK |
| Build met = equal 21/21 ∧ ratio ≤ 2.0 | Counter: `met = (equal == len(runs)) and len(ratios) == 5 and ratios_ok` (`c44_count_v5.py:1111-1112`); v5 `len(runs)` = 21; `ratios_ok` requires 5 exact ratios each `<= RATIO_LIMIT` (`:1100-1104`) — "at most 2.0" inclusive ✓ | OK inside counter; audit trusts `rec["met"]` (see defect 1) |
| `blind` = all met ∧ witnessed 0 ∧ all 27 rows | `total == expected_rows and not errors and not witnessed and all(r["met"] is True)` (`:74-76`) | Matches docstring; exceeds the frozen reading (defect 4) |
| `witnessed` = every control class-witnessed ∧ every build met | `total == expected_rows and len(witnessed) == total and not errors and bool(build) and all(b["met"] is True)` (`:77-79`) | Structure OK; evidence trust and count-pin defects below |
| `not-met` = every control met==false | `total == expected_rows and len(not_met) == total and not errors` (`:80-81`) | Counts cannot-evaluate receipts as not-met (defect 2) |
| `semantic_witness` timing-only exclusion | Timing-only `caughtBy=[T*]` → no class key → not a witness (probe G: `False`) | OK |

## Defects

### 1. HIGH — receipts are trusted without binding; `row["exit"]` is recorded and never gated (`c44_audit.py:54-61, 63-66, 151-160, 176-182`)

Three sub-holes, one root cause: `score()` builds the row from whatever JSON is
at the receipt path plus the subprocess return code, and `semantic_witness` /
`expectation_ok` never look at `exit` (or `note`, which is dropped at `:160`).

**(a) Counter-error (exit 2) receipts witness.** The counter writes a receipt
on `CannotEvaluate`/any exception mid-loop (`c44_count_v5.py:1114-1119`) with
partial `runs` and `met: False`. `CannotEvaluate` fires inside the T branch at
`:1097-1098` (missing base40 CPU time — reachable via a 600 s tool timeout
through `Sandbox.run :957-961`, or `OSError → :962-963`), i.e. *after* all G1–G10
entries are recorded (`rec["runs"][key] = entry`, `:1108`). A flaky timing run
on an honestly-witnessing control → exit-2 receipt with `caughtBy=[G…]` →
`semantic_witness` True. Kill rule (2): "**a counter error → not a witness**" —
violated. Demonstrated:

```
== A. counter error (exit 2) AFTER a class divergence ==
semantic_witness: True
expect witnessed (build 3/3 met): True
```

**(b) "tool absent" receipts witness.** If the counter cannot read the tool
file it sets `cand=None` (`c44_count_v5.py:1031-1034`), marks every run
`equal: False` with `candExit: "tool absent"` (`:1078-1080`), exits **1** with
`note: "tool absent"`. All 21 keys land in `caughtBy` → the control is
witnessed on all ten class keys though nothing ran. Reachable via TOCTOU: the
audit sha-checks `ctl.py` (`:147`) then the counter subprocess `open()`s it
independently (`:1032`); a file replaced/unreadable between those two opens
produces exactly this receipt. `note` is never propagated (`:157-160` omits
it). Demonstrated:

```
== B. 'tool absent' receipt (exit 1, note='tool absent') ==
semantic_witness: True
expect witnessed (build 3/3 met): True
```

**(c) Stale receipts are accepted.** `run_counter` reads `out` whenever it
parses (`:56-60`), regardless of `p.returncode`. Demonstrated end-to-end: a
fake counter that SIGKILLs itself on every call (writes nothing), with receipts
planted beforehand:

```
$ python3 -B c44_audit.py --root . --controls controls.tsv --counter fake_counter.py \
    --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --out out/summary.json
AUDIT kake-r44 classes=v5 classKeys=G1,...,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=3a4b23d3d1f6
  ctl1                 G5         met=False caught=G5
  witnessed-by-class ctl1 caughtBy=G5
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
AUDIT_EXIT=0
```

The summary *records* `"exit": -9` on the control row and all three build rows
and still reports `"ok": true`. Any crash-kill (OOM, timeout kill) on a rerun
over a receipt directory that already holds files certifies yesterday's
receipts. The same trust hole means receipt-internal consistency is never
checked: `met`, `equalRuns`, `classesMode`, `counterSha256`, `toolSha256` are
taken verbatim — a receipt claiming `met: true` with `equalRuns: "18/21"` or
written by different counter bytes passes `all(b.get("met") is True)` (`:79`).

### 2. MEDIUM — `--expect not-met` counts cannot-evaluate receipts as "not met" (`:80-81`)

`len(not_met) == total` uses `r.get("met") is False` alone; an exit-2
`CannotEvaluate` receipt carries `met: False`, so a canary the counter never
evaluated satisfies "the canaries and the junk control do not meet it":

```
== C. exit-2 cannot-evaluate under --expect not-met ==
expect not-met: True
```

A measurement failure is not evidence of not-met; it should be an error row.

### 3. MEDIUM — build-run count is not pinned (`:79, 172, 181-182`)

`bool(build) and all(b.get("met") is True)` accepts any non-empty all-met build
list. `score_build` runs `range(a.build_runs)` — operator argv — so
`--build-runs 1` produces `ok=True` on one run, not the frozen claim's "three
unseeded runs". `expectation_ok` is not even told the count:

```
== D. build count not pinned: --build-runs 1 ==
expect witnessed with ONE build receipt: True
```

The claim's `--build-runs 3` lives only in the declared command; a
mis-invocation under-measures silently green.

### 4. LOW — `--expect blind` enforces the rejected universal-v4-blindness clause (`:74-76`)

`all(r.get("met") is True)` under `--classes v4` requires all 27 controls met —
i.e. no control may diverge on any v4 run. The frozen predicate reading
(`SCORECARD.md:3562-3570`) explicitly rejected that reading: "a universal
v4-blindness requirement would be a claim about a seed, not about the corpus"
(2/27 controls observed diverging seed-dependently; `classes v4` makes
`not witnessed` vacuous anyway). Direction is conservative (spurious red on
unlucky seeds, never false-green), but the instrument gates a condition the
frozen reading says is not the claim.

### 5. LOW — input errors exit 1, not 2; one bad row kills the audit

Only argparse `ap.error` yields exit 2 (`:126`). Missing `--controls` file
(`:137`), malformed TSV line (`.split("\t")` unpack at `:141` → ValueError),
unloadable `--counter` (`:133`), `os.makedirs` failure (`:132`), and
`subprocess.TimeoutExpired` from `run_counter`'s 900 s cap (`:54`, uncaught in
`score`, re-raised through `pool.map` at `:162-163`) all die on tracebacks →
exit 1, conflated with predicate failure, no summary written. Per-row: a
directory at a control path → `sha256_file` `IsADirectoryError` → same crash
(one bad control discards all 27 rows' work). Cannot produce false-green, but
the exit contract does not distinguish "claim failed" from "instrument broke".

### Nits (no gate effect)

- `witnessedByClass` (`:192`) emits the row's full `caughtBy` (class + legacy
  keys), not the class subset; `rows[].classCaught`/`legacyCaught` (`:199-200`)
  are the correctly-split fields.
- No TSV-name uniqueness check: duplicate `name` values clobber each other's
  `tools/<name>.json` receipt (unique in `controls-27.tsv` today).
- `--classes v5 --expect blind` is legal argv; coherent ("all met ∧ no class
  witness") but not a declared command.

## Sanity checks (all correct)

```
== E. sanity: honest class witness still works ==
witnessed 3/3 builds: True
== F. sanity: v4-only divergence not a witness ==
semantic_witness: False
== G. sanity: timing-only not a witness ==
semantic_witness: False
```

And the shipped selftest on the frozen bytes:

```
$ python3 -B .ufo/waves/round-44/c44_audit.py --selftest
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
SELFTEST_EXIT=0
```

## Commands run / files written

- `sha256sum` of the three frozen files (matches declared hashes above).
- `python3 -B .ufo/waves/round-44/c44_audit.py --selftest` → PASS, exit 0.
- `python3 -B classifier_probe.py` (scratch) — drives `expectation_ok` /
  `semantic_witness` on rows shaped exactly as `score()` emits them.
- End-to-end stale-receipt run (scratch): fake counter (SIGKILLs, writes no
  receipt) + planted `tools/ctl1.json`, `build-{1,2,3}.json` → `ok=True`,
  exit 0, verbatim above.
- This report: `.ufo/waves/round-44/w2/ReviewCounterContract.md`.
- Scratch (all under `/fast/scratch/hyaku/kake-r44/ReviewCounterContract/`):
  `classifier_probe.py`, `stale_probe/{fake_counter.py,ctl.py,controls.tsv,
  out/tools/ctl1.json,out/build-1..3.json,out/summary.json}`. No lane files
  modified. No tools installed (python3/coreutils already present; pacman
  paused).

## Residual risk

Probes A–D exercise `expectation_ok` on row shapes copied verbatim from
`score()` (`:157-160`); the receipt-trust hole (1c) is demonstrated end-to-end
but its organic trigger needs a counter death after a prior receipt exists.
Defect 1a's trigger — a T-run `CannotEvaluate` after a class divergence — is a
code-path trace (`c44_count_v5.py:1097-1098` inside `if key.startswith("T")`,
after `rec["runs"][key] = entry` at `:1108`), not a live run. I did not execute
the real counter (needs bwrap + git-show of the pinned revisions; expensive);
counter-side reachability of exit-2/partial receipts is by code reading. The
real 23/27 witnesses flow through normal exit-1 receipts, so these defects
affect what the gate *would* certify, not what the current claim receipts show.
