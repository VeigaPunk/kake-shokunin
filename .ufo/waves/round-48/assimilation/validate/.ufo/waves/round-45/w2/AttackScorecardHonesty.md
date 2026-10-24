# AttackScorecardHonesty — round 45 wave 2

## Named attack and result

**Attack:** cross-surface overstatement / honest-stop wording: a bounded green measurement must not become a passed/admitted frozen claim, conceal either falsification, or omit C1's named provenance hole.

**Result: FAIL for the combined surface.** One fixable disclosure defect remains in lesson Mistake 14. The inspected SCORECARD and LOG round-45 sections **PASS this wording attack**: both explicitly retain the two NOT-MET verdicts, and both name the C1 residual. This is a scoped textual review, not a canonical admission judgment or a newly demonstrated runtime bypass.

Axes: **operability, freshness** (assigned lane axes); **calibration** is this review's evaluation lens, not an added lane axis. No scores or round state are re-declared.

## Finding — lesson 14 suggests run-binding closure without its residual

**Location:** `corpus/lessons/round-45.md:33-48`, especially `:36`.

The lesson describes the unchecked *run*-binding problem, then says the validity gate was needed "to actually close it," followed by the fix and green fixture counts. It never records C1's NOT-MET verdict or the named limitation: mtime plus a public, self-reported counter SHA cannot establish which executable bytes wrote the receipt. The full 68-line lesson was read; a targeted residual/negative-verdict sweep returned no matches. Mistake 15 honestly records C2(c)'s falsification, but does not supply the missing C1 caveat.

**Strongest counterexample from local evidence:** two writer histories yield identical gate inputs: the invoked counter writes a receipt, or different bytes write the same JSON during the accepted window with the expected `counterSha256`, a seed, an allowed exit and no `tool absent` note. Current `receipt_validity()` (`.ufo/waves/round-45/c45_audit.py:68-87`, read snapshot `CAC4`) checks only those observable fields and time bounds, not writer identity. `[INFERENCE]` Those identical inputs cannot distinguish the histories. SCORECARD already states exactly this residual, and `w1/CriticC1Predicate.md:8-26` explicitly limits its evidence to a model rather than an observed v2 exploit. I did not execute that model or any bypass.

**Impact:** calibration is directly affected by inconsistent self-assessment across surfaces. Freshness is affected because the training lesson omits the standing correction. Operability risk is `[INFERENCE]`: a reader using the lesson alone may mistake the fixture repair for causal run attestation; no new operational harm was measured.

**Calibration / alternative reading:** "close it" might be intended to mean only the three fixture regressions. That charitable reading does not remove the explicit assignment's residual-disclosure requirement. The demonstrated defect is an unqualified closure summary plus a missing caveat, not evidence of intentional deception, a failed bounded repair, or an already-admitted round.

**Smallest safe correction:** L1 appends a clarification explicitly superseding Mistake 14's unqualified closure reading, for example:

> Mistake 14's "actually close it" applies only to the three tested receipt classes under a trusted-local-counter boundary. C1 remains NOT MET as declared: run-window mtime and a self-reported counter SHA do not prove that the invoked counter bytes wrote the receipt; different writer histories can present identical gate inputs. The causal/universal clause remains with the operator, as recorded in SCORECARD's round-45 measurement append.

Do not rewrite a frozen declaration, replace either negative verdict, or turn this documentation correction into admission. This is a fixable documentation defect; the underlying universal-provenance assertion remains for the canonical judge/operator, not this seat.

## Other inspected surfaces

| Surface | Wording-attack result | Evidence / distinction |
|---|---|---|
| `SCORECARD.md:3628-3775` | PASS | C1 explicitly NOT MET at `:3734`, with the causal hole at `:3735-3743`; C2 explicitly FALSIFIED/NOT MET at `:3759-3767`; round verdict says both NOT MET at `:3771`. `MATRIX_*_PASS` and "bounded MET condition" are distinguished from claim success in the same measured section. |
| `LOG.md:1716-1747` | PASS | `:1737-1739` names mtime + self-reported-SHA insufficiency; `:1741-1743` records the wrong-receipt tuple and both NOT-MET verdicts. S133 "admitted" at `:1745` is a source admission, not claim or round admission. |
| Lesson Mistake 15 (`:50-68`) | PASS | Explicitly identifies the wrong receipt, correct split, and C2(c)'s falsified-as-declared status. |
| Lesson Mistake 14 (`:18-48`) | FAIL | Unqualified closure wording and omitted C1 residual, as above. |

The original false tuple in the frozen declarations is historical declaration data, not a new measured success assertion. No observed progression after an honest stop is claimed here. The existing HOLD/saturation wording is not independently re-graded by this review.

## Exact commands / tool invocations and decisive output

The repository was read-only. File searches used the required `grep` tool rather than shell grep. Paths below are the exact inspected paths; outputs are verbatim decisive excerpts where labeled.

### 1. Scoped inflation sweep

```text
functions.grep({"i":"Sweeping scoped inflation keywords","pattern":"(?i)PASS|\\bMET\\b|admi|falsif|residu|unfalsif|causal|clos|harm","path":"/home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md:3628-3775;/home/vgpnk/Projects/shokunin/kake-shokunin/LOG.md:1716-1747;/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-45.md","case":false,"gitignore":false,"skip":null})
```

Verbatim decisive output excerpt:

```text
*36:    inputs") and needed the validity gate to actually close it. Fix: driver v2
```

Full round-45 sections were also read directly. The grep response omitted matching SCORECARD tail lines, so it was not treated as an exhaustive absence proof; the tail was read explicitly. Tool-output inconsistencies were reported to `xd://report_issue`.

### 2. Lesson residual / negative-verdict sweep

```text
functions.grep({"i":"Testing lesson residual omission","pattern":"(?i)NOT MET|unfalsif|residual|self[- ]reported|trusted[- ]local|different bytes|causal|honest stop|halt progression","path":"/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-45.md","case":false,"gitignore":false,"skip":null})
```

Verbatim output:

```text
No matches found
```

### 3. Lesson closure context

```text
functions.read({"i":"Capturing decisive lesson wording","path":"/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-45.md:33-48:raw"})
```

Verbatim decisive output excerpt:

```text
    ("receipts re-derive at recorded seeds") certified *seed*-binding while leaving *run*-binding
    unchecked — it constrained what a receipt may be cited for, not which invocation wrote it; the
    round-45 C1 kill rule (2) repeats the class ("re-derives from committed bytes at its recorded
    inputs") and needed the validity gate to actually close it. Fix: driver v2
    `.ufo/waves/round-45/c45_audit.py` applies one `receipt_validity()` gate (`:68-86`) through
    shared row builders (`build_control_row :98`, `build_build_row :122`): exit ∈ {0,1} else
    `counter_error`; `note != "tool absent"` else `tool_absent`; counter-sha binding, seed presence
    and a run-window mtime check else `stale_receipt`; invalid rows earn no witness or not-met
    credit; build count pinned; cohort dir self-created and refused non-empty; run-manifest written
```

### 4. Contradicting limitation already present in SCORECARD

```text
functions.read({"i":"Capturing decisive scorecard boundary","path":"/home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md:3727-3743:raw"})
```

Verbatim decisive output excerpt:

```text
- **Verdict: NOT MET as declared.** The frozen predicate sentence asserts refusal for "any
  control whose receipt ... was not written inside the driver's own run window **over the invoked
  counter bytes**"; the implemented checks (exit set, note, counter-sha self-report, run-window
  mtime with 1 s wall-clock tolerance, seed) cannot establish that causal clause — a receipt
  written during the window by different bytes carrying the expected sha is indistinguishable
  (`w1/CriticC1Predicate.md`, claim-breaking for the literal reading; a model demonstrates
  identical gate inputs for both writer histories). The bounded three-fixture claim with an
  explicit trusted-local-counter boundary is verified above; the causal/universal reading is
  routed to the operator (`.ufo/l0-questions.md`). No post-hoc narrowing: this append records
  the falsification, the verified bounded repair, and the named residual hole.
```

### 5. Final round wording, not a claim-admission assertion

```text
functions.read({"i":"Capturing final negative verdict","path":"/home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md:3771-3775:raw"})
```

Verbatim output:

```text
**Round verdict.** Both claims NOT MET as declared; every falsified element is corrected
append-only with re-derivable evidence, the bounded repairs verify, and no owned axis is harmed
(ledger gate green at 3 figures / 0 mismatches after all edits — `python3 -B
scripts/ledger_latest_check.py --root .` exit 0; frozen round-43/44 bytes byte-identical).
Admission is the operator's call; per the honesty rules nothing here is rerolled.
```

### 6. Scratch setup

```sh
mkdir -p /fast/scratch/hyaku/kake-r45/AttackScorecardHonesty
```

Exit 0; no output. No scratch files were created.

## Execution limits and written files

- Static inspection only. Existing matrix/freshness receipts were read as retained evidence, not represented as checks executed by this seat.
- **Unrun:** both matrix stages, freshness runner, driver selftest, ledger gate, source census, mutation tests, live provenance attack, canonical judge. No separate runtime was invoked.
- No implementation, lesson, SCORECARD, LOG, frozen file, fleet file, history, commit, or push was changed. No subagents dispatched. No tools installed or updated.
- **Only file written:** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2/AttackScorecardHonesty.md` (this report). The scratch directory above was created; the internal issue-report device was notified.
- No missing-artifact blocker. Review complete; L1 owns any correction and canonical disposition.
