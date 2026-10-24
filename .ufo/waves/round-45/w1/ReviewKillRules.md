# ReviewKillRules — C1/C2 kill-rule gap audit (round 45, wave 1)

Seat: `kake-r45.ReviewKillRules` (reviewer, operability). Read-only review of the frozen
declarations at `SCORECARD.md` §"Round 45 — C1 and C2 declared" (base `35b35f4`), the frozen
round-44 bytes, and the round-45 artifacts that had landed at review time
(`c45_audit.py`, `c45_count.py`, `c45_matrix.py`, `fixtures/*`, `mutants/*`, `v6diff/`).
No counter, driver, or matrix run was executed by this seat; no file outside this report was
written. Scratch: `/fast/scratch/hyaku/kake-r45/ReviewKillRules/` (spec prompts extracted from
`.ufo/waves/round-45/w1-spec.json` for reading). No tool installs.

Verdicts up front:

- **C1 kill rules 2, 3, 4, 5 fail as *rules* — none is enforced by any command in the frozen
  counting path; the after-stage verdict does not gate the honest leg at all (S1-1).**
- **The landed `--stage after` cannot reach the declared after-state: `stale_receipt` is never
  named (S1-2).**
- **C2(c) is not derivable from the receipt it names (S1-3).**
- **C2 kill rule 1 has already been defeated by its own fixture: a semantic + API change
  (`PREDICATE` deleted) rode inside an allowed "predicate-text" hunk (S1-4).**

---

## S1-1 — C1 kill rule 4 (honest-cohort verdict equality): the frozen counting command does not measure it

The claim: "Claim MET iff … the after receipt records `invalid_accepted=0`, `rejections_named=3`,
`honest_witnessed=27`, `honest_build_met=3`." The landed matrix's pass condition omits the last
two:

`.ufo/waves/round-45/c45_matrix.py` (verbatim):

```
        passed = (complete_fixture_runs and all_fixture_runs_rejected and invalid_accepted == 0
                  and all_rejected and rejections_named == 3 and honest_control_ok)
```

`honest_witnessed` / `honest_build_met` are written into the receipt and printed, but are not in
`passed`, and the honest regression is opt-in:

```
    parser.add_argument("--with-honest", action="store_true",
                        help="read the committed honest-regression receipt; never launch the heavy run")
```

`honest_metrics` with `requested=False` returns `witnessed=0, build_met=0` without reading
anything. So the cheapest control that satisfies the frozen command while the honest leg is
unmeasured is the frozen command's **default invocation**:

```
python3 -B .ufo/waves/round-45/c45_matrix.py --stage after
# prints ... honest_witnessed=0 honest_build_met=0, exit 0 if the three fixtures are rejected
```

Even with `--with-honest`, provenance is unchecked — `honest_metrics` takes only
`summary["witnessed"]`, `summary["build"][*]["met"]` and `summary["ok"]`; it never checks
`counterSha256`, `controls == 27`, `classKeys`, `errors`, or exit. Cheapest violating control:
`cp .ufo/waves/round-44/verification/claim/after-final/after-v5.json \
.ufo/waves/round-45/verification/honest-regression/after-v5-v2.json` → the matrix prints
`honest_witnessed=27 honest_build_met=3` with v2 never having run the cohort. That is precisely
"verdict on the same inputs equals v1's" satisfied by using v1's own receipt.

## S1-2 — C1 after-stage is unreachable: `stale_receipt` is never named

`c45_matrix.py` plants the stale receipts **only in the before stage**:

```
            plant_from = None
            if args.stage == "before" and fixture_name == "stale-planted":
                plant_from, match_count = planted_receipt_dir(fixture)
```

In `--stage after` the `stale-planted` fake counter runs with no planted receipt and does what
its bytes say (`fixtures/stale-planted/fake_counter.py`, verbatim):

```
    ap.parse_args()
    os.kill(os.getpid(), signal.SIGKILL)
```

The driver's gate classifies by exit code **first** (`c45_audit.py:70-71`, verbatim):

```
    if exit_code not in (0, 1):
        return False, "counter_error"
```

A SIGKILLed child has `returncode -9`, so the stale-planted row is named `counter_error` — the
same class the `counter-error` fixture produces. `rejection_names` is a set of class strings, so
`rejections_named` tops out at 2 (`counter_error`, `tool_absent`), `passed` requires
`rejections_named == 3`, and the frozen after stage exits 1. The declared after-state
(`invalid_accepted=0`, `rejections_named=3`) cannot be produced by the landed counting command.
Two independent repairs are needed: plant in both stages (the fixture's on-disk
`tools/ctl1.json` exists and is unused in `after`), and classify "no receipt written" separately
from a stale receipt so the class names what was actually observed.

## S1-3 — C2(c) split re-derives only from a superseded *failed* receipt

SCORECARD C2(c): "the round-44 claim receipt's 27 witnessed controls re-derive as 22 class-only
+ 1 mixed + 4 met". Decisive scan of every committed round-44 receipt carrying `rows`:

```
$ python3 - <<'PY'   # class_only/mixed/metrows/neither per receipt
...
verification/claim/after-v5.json            n=27 witnessed=23 met=23 ok=False | class_only=22 mixed=1 metrows=4 neither=0
verification/claim/after-final/after-v5.json n=27 witnessed=27 met=27 ok=True | class_only=26 mixed=1 metrows=0 neither=0
verification/claim/after-v5-wave2-baseline.json n=27 witnessed=23 ok=False | class_only=21 mixed=2 metrows=4
verification/claim/w2-baseline/run1/…       n=27 witnessed=23 ok=False | class_only=21 mixed=2 metrows=4
verification/claim/w2-baseline/run2/…       n=27 witnessed=23 ok=False | class_only=23 mixed=0 metrows=4
```

Exactly one committed receipt yields `22/1/4/0`: `verification/claim/after-v5.json`, an
`--expect witnessed` run with `ok=False`, timestamped 22:46 — i.e. **before**
`classes/g6_fold_pairs.py` was fixed at 23:29 (SCORECARD §"Round 44 — C1 measurement" names that
fix). The receipt the round-44 claim actually cites
(`verification/claim/after-final/after-v5.json`, C1 kill rule 4's reference) is `26/1/0`.
The claim sentence is also internally impossible: a receipt with 27 witnessed controls cannot
have 4 met rows. The 4 "met" rows are `casememo-v3/v4/v7/v8`, met **because the G6 class was
pre-fix**, not witness-less controls:

```
casememo-v3 a: True [] 37611002469796  b: False ['G6'] 51991230635285
casememo-v4 a: True [] 147120660939040 b: False ['G6'] 66763655055034
casememo-v7 a: True [] 123595050640513 b: False ['G6'] 149260863541903
casememo-v8 a: True [] 82003496704499  b: False ['G6'] 22899741442922
```

So `c45_freshness.py` can print `witness_split class_only=22 mixed=1 met=4` only by reading the
pre-fix failed baseline while calling it "the claim receipt". Independently corroborated by
`.ufo/waves/round-45/verification/witness-split/split.txt` (ExecWitnessSplit), which prints the
final receipt as `26/1/0/0` and states it "does not reproduce the stated 22/1/4/0 split".
Claim-breaking unless the counted receipt path and its `ok=False` status are named in the frozen
text (L1 decision).

## S1-4 — C2 kill rule 1 has already been defeated by the landed v6 diff

`v6diff/v5-v6.diff` contains three hunks. The third is receipt construction:

```
-    rec = {"predicate": PREDICATE, "met": False, "ratioLimit": RATIO_LIMIT, "reps": REPS,
+    rec = {"predicate": PREDICATE_V5 if a.classes == "v5" else PREDICATE_V4, "met": False, "ratioLimit": RATIO_LIMIT, "reps": REPS,
```

Answers to the assigned attack:

1. **A semantic + API change did hide in the predicate-text hunk.** v6 deletes module-level
   `PREDICATE`; both drivers read it from the counter module
   (`c44_audit.py:189`, `c45_audit.py:292` — `"predicate": counter_mod.PREDICATE,`). Demonstrated:

   ```
   $ python3 -c "import importlib.util; s=importlib.util.spec_from_file_location('c','.ufo/waves/round-45/c45_count.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print([a for a in dir(m) if a.startswith('PREDICATE')]); m.PREDICATE"
   c45_count module attrs with PREDICATE: ['PREDICATE_V4', 'PREDICATE_V5']
   ATTRIBUTEERROR: module 'c' has no attribute 'PREDICATE'
   ```

   The round's own two instruments are now mutually incompatible at their documented seam
   (driver v2 + counter v6 → AttributeError). The hunk classification "predicate-text" allowed
   it, because the allowlist is about *lines containing PREDICATE*, not about symbol survival.
2. **The ratio limit can be smuggled on the same source line** — the changed line already carries
   `"ratioLimit": RATIO_LIMIT, "reps": REPS, "met": False`. A `2.0 → 2.5` edit is one token in
   the same line; `PREDICATE_V5` byte-identity does not protect `RATIO_LIMIT`, and `RATIO_LIMIT`
   is a *context* line of the predicate hunk (` RATIO_LIMIT = 2.0`), so a definition edit lands in
   the same "predicate-text" hunk too. `RATIO_LIMIT` is load-bearing (`c44_count_v5.py:1111`).
3. **The run-order / run-count smuggle is impossible** — confirmed by `c44_count_v5.py:1047-1050`:
   v4 runs are exactly A–F (6) + T1–T5 (5) = eleven; the PREDICATE_V4 text is truthful.
4. **The mode conditional itself is unmeasured.** Nothing in the frozen MET condition inspects a
   *v5-mode* receipt from v6. `rec = {"predicate": PREDICATE_V4, ...}` (unconditional) is a
   smaller diff than the landed one, passes the v4 leg, passes any "predicate-text" classifier,
   and silently makes v6's v5-mode receipts lie. Cheapest control: one line.

**Recommendation for the rule**: replace hunk-class classification with symbol+behavior checks:
allowlist `{PREDICATE_V5, PREDICATE_V4, docstring line}` and require (a) `PREDICATE`
still present and equal to `PREDICATE_V5`, (b) `RATIO_LIMIT == 2.0`, `REPS == 5`, run lists
byte-identical, (c) a v5-mode equivalence receipt (same seed, same tool as a v5 receipt, identical
`runs`/`met`/`equalRuns`, differing only in `predicate` and `counterSha256`).

---

## Per-kill-rule table (cheapest violating control, or why none exists)

### C1

| # | Rule (frozen) | Cheapest violating control while the claim reads MET | Enforcement today |
|---|---|---|---|
| 1 | frozen round-44 bytes untouched — sha guard | **Edit `classes/g6_fold_pairs.py`** after the snapshot: it is not in the claim's guard enumeration, yet its 23:29 edit flipped exactly 4 of 27 rows (S1-3 seeds). Claim still reads 27/27. Also `build_v5.py` is in the round's frozen list but has **0 entries** in `verification/sha-guard/before.sha256`. | Partial: `before.sha256` (483 entries, 447 = commit blobs at `35b35f4`, 36 = `__pycache__/*.pyc`, 0 = `build_v5.py`; `classes/` 19, `classes-placebo/` 10, `controls-r43/` 54). SentinelFrozen re-runs it at *its own* seat end; no integration-time re-run is assigned. pytest bytecode churn will false-positive the 36 `.pyc` rows. |
| 2 | receipts re-derive at recorded inputs | Cite the seeds without re-deriving them: **no frozen command re-derives a row**, the driver has no `--seed` passthrough (`c44_audit.py:49-53` builds argv with `--root/--classes/--out/--tool-file/--revision` only), and the counter draws `os.urandom(6)` (`c44_count_v5.py:995`). Kill rule 5 then *collides*: the stale-planted receipt records a real v5 seed over a different tool and can never re-derive under the invoked fixture counter. | None commanded; round-44 satisfied it with a hand-written per-row loop. Needs an explicit exemption line for fixture receipts and a replay loop in the matrix. |
| 3 | v2 reads no control file beyond v1's | Import/execute the control module in-process (not a "read"), or read any sibling file — invisible. The rule's wording targets *reads*, but the driver already reads the tool file for sha (`score()`), and already imports the **counter** in-process and trusts its `CLASS_MODULES`/`PREDICATE` — which is why every fixture's `fake_counter.py` defines its own class key set. | None. Feasible: `strace -f -e trace=openat` diff v1 vs v2 on one control, plus forbid import/exec. |
| 4 | v2's honest-cohort verdict on the same inputs equals v1's | See S1-1: run with default `--with-honest` off, or drop v1's receipt at the after path. Inputs are also **not pinned**: seeds are OS entropy; the class bytes that flip 4 rows are outside the claim's guard list; the counter's `--build-rev 020bc457` is content-addressed but CPU-time medians for the 5 timing shapes are host-load dependent. | None. `passed` excludes both honest fields. |
| 5 | fixtures match a real v1-observable receipt shape; a strawman voids the leg | Assemble a chimera (runs from receipt A, note/exit from receipt B): no field-schema check can exclude it, and "voids that leg" has no representation in `c45_matrix.py`. No strawman is *required* — the real path exists: class-run divergence at `c44_count_v5.py:1077-1079` can be followed by `CannotEvaluate("round-40 tool gave no CPU time …")` at `1098` → exit 2 (`1114-1116`) with a class divergence already in `runs`. | Prose-only (CriticFixtures, same wave). Also: all three fixtures are tested with `--classes v5` and a `--expect witnessed` summary; the matrix never checks that the *rejection class* of a fixture is its own (S1-2 shows the collision). |
| (iii) window leg specifically | The stale fixture's planted `tools/ctl1.json` carries `counterSha256 = 5cedaa3b…` (the **real** v5 counter) while the invoked counter is the fixture's own file — the sha check rejects it before mtime is consulted, so **the mtime window is never exercised end-to-end**. | To exercise it, the planted receipt must be an earlier run *of the same fixture counter* (its own sha), written before `started_ns`; only then does mtime decide. `MTIME_EPS_NS = 1_000_000_000` (1 s) is fixed in code but absent from the claim sentence — the claim has no tolerance, the mechanism has one. |

### C2

| # | Rule (frozen) | Cheapest violating control while the claim reads MET | Enforcement today |
|---|---|---|---|
| 1 | v6 differs only in mode-conditional predicate text + docstring header; hunk-classified diff; v5 string byte-identical | **Already violated** (S1-4): `PREDICATE` deleted inside an allowed hunk; `ratioLimit`/`reps` on the changed line; unconditional `PREDICATE_V4` passes every measured check. | The landed diff itself is three hunks, one of which (receipt construction) is not in the allowlist as written — the rule is simultaneously too narrow (fails the intended change) and too permissive (admits the smuggle). |
| 2 | v6 v4 receipt re-derives from committed bytes (`classRuns` empty, no G-runs) | **Frozen v5 already satisfies it**: `c44_count_v5.py:1001` writes `classRuns` `[]` in v4 mode (unchanged by the diff), and committed v4 receipts prove it (`verification/claim/v4-final/tools/*.json` → `classRuns= []`, predicate names class runs: `True`). The clause cannot distinguish v5 from v6. | Non-discriminating. Must add `counterSha256 == sha256(c45_count.py)` and exact v4 run-key set `{A..F,T1..T5}`; `c45_freshness.py` is absent at review time so this is a spec-level judgement. |
| 3 | m1–m4 are reconstructions of MutClassGate's four mutants, each documented with its source-line target | Rebuild the after-leg mutants from v2 with a *broader* mutation: the seat's own fallback instruction permits "derive minimal mutants by class"; e.g. an m2 that returns witness for any `caughtBy` key is killed by any assertion, giving 4/4 without the timing fixture the claim credits. Also a naming collision: round-44's delivered `m1–m4` all exit 1 under their hardened selftest (`MutClassGate.md:43-46`), while round-45's `mutants/m1–m4` are f-style (mutant + frozen v1 selftest) and exit 1/0/1/0 (`verification/selftest-coverage/before/m{1..4}.txt`). "Same m1–m4 mutants" therefore names two different artifact classes. | Prose-only; after-leg bytes do not exist yet. Needs: mutation text diffed against the before mutants, and the `f`-variant named explicitly. |
| 4 | no frozen byte edited (same sha guard as C1) | Same as C1 #1 (`classes/g6_fold_pairs.py` outside the claim's enumeration; `build_v5.py` unguarded; no integration-time re-run). | Partial. |

---

## Named attacks — pass/fail

| Attack | Result |
|---|---|
| Kill rule 5 enforceability: who proves fixtures non-strawman, when | **FAIL.** Prose critic in the same wave, no command, no integration gate; schema-level fidelity admits chimeras; the landed stale fixture's sha makes the window leg unreachable. |
| Regression equality scope: are the *inputs* pinned? | **FAIL.** Seeds unpinned (`os.urandom(6)`, no `--seed` passthrough); class bytes and `build_v5.py` outside the claim's guard; timing medians host-dependent. And the honest leg is not gated at all (S1-1). |
| v6 diff-audit: can a semantic change hide in a "predicate-text" hunk? | **FAIL — it already did** (S1-4: `PREDICATE` deletion breaking `c45_audit.py:292`). Ratio/reps smuggle is a one-token edit on the changed line; the run-order/count smuggle is genuinely impossible (11 = A–F + T1–T5). |
| C1 (i) exit gate exercised end-to-end | **PASS** — counter-error fixture's fake counter writes the receipt itself, so sha matches and only exit ±2 rejects it. |
| C1 (ii) note gate exercised end-to-end | **PASS** — tool-absent fake counter self-hashes and sets `note="tool absent"`. |
| C1 (iii) window gate exercised end-to-end | **FAIL** — rejected by sha binding first (planted receipt carries `5cedaa3b…`); no fixture can name `stale_receipt` in the after stage (S1-2). |

## Residual risk

- All judgements above are static (bytes + committed receipts); no fixture, driver, matrix or
  counter was executed by this seat. S1-2 is a code-path argument that a 30-minute matrix run
  will confirm or refute; if ExecMatrixRunner's run already shows `rejections_named=2`, it is
  confirmed.
- The pre-fix/post-fix split comparison assumes `classes/g6_fold_pairs.py` is the only delta
  between `after-v5.json` and `after-final/after-v5.json`; tool sha256 and row names are
  identical across the two (checked), and the two receipts bracket the 23:29 edit.
- `c45_freshness.py` is absent; every C2 judgement about the counting command is against the
  frozen command *name* and the claim's printed fields, not its bytes.

## Verification gaps / dependencies

- `c45_freshness.py` absent at review time → C2(a)/(b)/(c) cannot be checked against a command.
- `mutants/m{1..4}_v2.py` and `verification/selftest-coverage/after/` absent → C2(a) after-leg
  unmeasured.
- `verification/honest-regression/after-v5-v2.json` absent → C1 kill rule 4 unmeasured (and, per
  S1-1, would be ungated even when present).
- No `.pyc`-free guard rerun after this wave; SentinelFrozen's window closes before integration.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w1/ReviewKillRules.md` (this report)
- `/fast/scratch/hyaku/kake-r45/ReviewKillRules/*.prompt.md` (scratch: 32 item prompts extracted
  from `w1-spec.json` for reading; no repo effect)
