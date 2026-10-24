# AttackKnowledgeEntry — falsify wave 2, attack on `corpus/knowledge/receipt-integrity.md`

Seat: `kake-r45.AttackKnowledgeEntry` (leaf, no subagent dispatch).
Axis: **freshness** (provenance and citation fidelity of the durable knowledge entry).
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Scratch: `/fast/scratch/hyaku/kake-r45/AttackKnowledgeEntry/`.
No lane file was edited; no commit, no gate mutation in the tree.

Target under attack: `corpus/knowledge/receipt-integrity.md`
(115 lines, sha256 `c53b37a88bd8fcacb9f4853240cd354d52db68fe303d8cf57956e475dd1a7d21`).

**File drift observed mid-attack (not caused by this seat).** `c45_audit.py` was
`f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076` (= HEAD `e545525`) when I
measured it and ran the probe; at 00:59:19 a sibling added an uncommitted `bad-build` selftest
fixture (+26 lines, worktree sha256
`b61447e6…4156660`). I re-ran the F1 probe against the drifted bytes: identical credit. Citations
below give the f3c3171b anchors (the version the entry documents, and the version `after.json`
records) with the drifted anchor in parentheses where it moved.

## Verdict per named attack

| # | Named attack | Verdict | Decisive point |
|---|---|---|---|
| 1 | Provenance trio present (source / verified-at / recheck) | **PASS** | All three lines at head; `verified-at` claims re-derived below |
| 2 | Every count carries its command | **PASS** | All five count clauses carry a command; each re-ran to the stated value |
| 3 | Opinion marked as opinion | **PASS (formal) / FAIL (substance)** | Marked “Opinion (marked as opinion)”, but its load-bearing claim is false — see F1 |
| 4 | Named residual limit faithfully represented | **FAIL** | Two independent defects: F1 (omitted sibling-invocation hole) and F2 (remedy contradicts the cited source) |
| 5 | Quoted v2 sha256 matches committed bytes | **PASS** | `f3c3171b658abccd…0a076` is a correctly elided prefix/suffix of the actual digest |

## Findings

### F1 — HIGH — the residual-limit section omits the cohort-wide-window hole, and the opinion asserts the opposite of measured behavior

The entry states:

> *Opinion (marked as opinion):* the run window is the load-bearing clause. … only the window
> makes it evidence of *this* invocation; a gate with exit+note+sha alone still accepts a
> byte-valid receipt left over from a previous run.

and represents the residual limit as only:

> a receipt written during the window by different bytes carrying the expected sha is
> indistinguishable from an honest one, and mtime is mutable metadata.

The shipped driver's window is **cohort-wide on the lower bound**, not per-invocation: `started_ns`
is taken once per cohort and shared by every control (`c45_audit.py:356` at `f3c3171b` / `:384` in
the drifted worktree, passed to every row at `:376` / `:404`), while `finish_ns` is per child
(`:54`, unchanged). Therefore a receipt written by an **earlier
sibling control in the same cohort** — same counter bytes, same self-reported sha, a `seed`
present, mtime inside this row's window — is credited to the later row. That is precisely the
ambiguity `w1/CriticC1Predicate.md` names and the entry omits: “A cohort-wide start also does not
bind a receipt to its particular control invocation.” The entry's opinion (“evidence of *this*
invocation”) is falsified at per-invocation granularity by the shipped bytes themselves.

Decisive probe (scratch fake counter; `--workers 1`; ctl2 copies ctl1's receipt instead of
writing its own):

```text
$ python3 -B .ufo/waves/round-45/c45_audit.py --root root --controls controls.tsv \
    --counter root/counter.py --classes v5 --expect not-met --workers 1 --out out/summary.json
AUDIT kake-r45 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=2/2 notMet=2 build_met=0/0 ok=True counter=aceb71f3b601
  ctl1                 cls        met=False caught=G2
  ctl2                 cls        met=False caught=G2
  witnessed-by-class ctl1 caughtBy=G2
  witnessed-by-class ctl2 caughtBy=G2
EXIT=0
```

Summary rows (both valid, no error):

```text
[{'name': 'ctl1', 'exit': 1, 'met': False, 'seed': 111, 'error': None, 'receipt': 'tools/ctl1.json'},
 {'name': 'ctl2', 'exit': 1, 'met': False, 'seed': 111, 'error': None, 'receipt': 'tools/ctl2.json'}]
```

ctl2's receipt is ctl1's, byte-for-byte plus a provenance marker:

```json
{"counterSha256": "aceb71f3b601274a26eb5e8e2df20d08781355181b7d190a28ea0c3032b33bd5", "seed": 111, "note": null, "met": false, "runs": {"G2": {"equal": false}}, "produced_by": "ctl1.py", "copied_from": "ctl1"}
```

Scope of the claim: this proves the **gate's acceptance**, not that a real counter does this. The
manifest `nonce` (`c45_audit.py:359`) is never read anywhere in the driver and is never passed to
the counter, so no driver-side artifact distinguishes sibling receipts. The entry is the durable
artifact a future implementer will follow; presenting the window as evidence of *this* invocation,
with the sibling case absent from the residual limit, is a documentation defect on the freshness
axis even though the bounded three-fixture claim still holds.

### F2 — MEDIUM-HIGH — the stated remedy contradicts the residual-limit document it cites

Entry:

> Closing that hole needs counter-side cooperation (a driver-issued nonce echoed into the receipt)
> or an explicit trusted-local-counter boundary

`w1/CriticC1Predicate.md` says the opposite about the nonce:

> For an implementation intended to support the causal reading, the missing mechanism is a stable
> execution-byte identity plus independently driver-associated per-invocation output; **adding
> another receipt field or an echoed public nonce alone is not that mechanism.**

The entry converts “nonce alone is not that mechanism” into a one-of remedy (“needs … a nonce …
**or** a boundary”). The only faithful rendering is that the nonce clause is insufficient without
the trusted-local-counter boundary, not an alternative to it. A reader following the entry would
implement the very construction the cited critique rejects. The `nonce` field is in fact written
and never verified (`grep -n nonce` → `c45_audit.py:359` only), which is consistent with the
critic's warning and inconsistent with the entry's phrasing.

### F3 — LOW — one quoted sentence is attributed to the wrong `subprocess` object

Entry:

> `subprocess` documents `returncode` as "Exit status of the child process", with "A negative
> value `-N` indicates that the child was terminated by signal `N` (POSIX only)"
> (`Popen.returncode`, …)

Retained source `.ufo/waves/round-45/sources/subprocess.html` (208,624 bytes) attributes the two
phrases to different objects:

- `CompletedProcess.returncode`: “Exit status of the child process. Typically, an exit status of 0
  indicates that it ran successfully. A negative value `-N` indicates that the child was
  terminated by signal `N` (POSIX only).”
- `Popen.returncode`: “The child return code. Initially `None`, … A `None` value indicates that the
  process hadn't yet terminated at the time of the last method call. A negative value `-N`
  indicates that the child was terminated by signal `N` (POSIX only).”

So the first quote is `CompletedProcess.returncode`, not `Popen.returncode`; the negative-signal
quote is genuinely Popen's. Both statements are doctrinally correct and the same page is cited, so
this is attribution precision, not a false claim. `corpus/SOURCES.md:141` scopes S133 to
“§Popen Objects → Popen.returncode, paragraphs 2-3”, which is accurate for the negative-value
paragraph but not for the “Exit status” sentence.

### F4 — LOW — “every control row” is not literally true

The entry says every control row is built through `build_control_row()` (`:98-119`). The
control-sha mismatch branch returns a row directly (`c45_audit.py:371-373`), bypassing
`build_control_row`; it sets `_valid=False`, so it cannot be credited and the safety property
holds. The prose “Every control row” is an overstatement, and a mutant that kept that early return
would still not be caught by the stated invariant.

### F5 — LOW — line ranges and self-citation norm

- `receipt_validity()` cited `:68-86`; the success `return True, None` is line **87**. Off by one.
  (`build_control_row` `:98-119` and `build_build_row` `:122-137` are right at 98-119 and high by
  five at 122-**132**.)
- The entry states a citation norm — “a citation of ‘the round-44 claim receipt’ must name which
  one (path + sha256)” — but its own two citations supply paths only; the sha256s live in
  `corpus/lessons/round-45.md` entry 15 (`9dead4d7…c076d1`, `2383efae…ce0902`). Defensible by
  reference, but it violates the norm it declares in the same paragraph.
- `verification/matrix/after.json` is cited without the `.ufo/waves/round-45/` prefix used for
  every other path in the entry.

### F6 — LOW — the “routed to the operator” clause has no artifact in the lane at attack time

Entry: “the claim text that asserted the stronger reading is recorded as falsified in `SCORECARD.md`
(round 45), and the trust-boundary question is routed to the operator.”

The falsification record is real: `SCORECARD.md:3734-3743` says **NOT MET as declared**, “the
causal/universal reading is routed to the operator (`.ufo/l0-questions.md`)”. But
`.ufo/l0-questions.md` does not exist anywhere in the lane:

```text
$ find . -name "l0-questions*" -o -name "*l0*question*"
(no output)
$ ls .ufo/
interactive-sessions  reports  round-20  waves
```

The entry's own wording (“routed to the operator”) is weaker than SCORECARD's filename citation, so
this is not a proven falsehood in the entry — routing may happen at wave close through a channel I
cannot see. It is recorded as an unverified claim with a missing citation target. A fresh reader
following the entry cannot find the routed question. Adjacent to a parallel wave-2 seat
(`AttackScorecardHonesty`); I did not coordinate with it.

### Residual observation on cited evidence (not an entry falsehood)

`.ufo/waves/round-45/verification/matrix/after.json` labels the `stale-planted` leg
`"fixture": "stale-backdate"`. `c45_matrix.py:76,44` does this deliberately (`AFTER_STALE_FIXTURE`
substitutes the backdating twin for the after stage), so the entry's claim of “three distinct
named rejection classes” still re-derives. But a reader auditing the cited artifact cannot tell
which fixture the stale leg ran; the evidence naming is weaker than the entry implies. Report as
lane hygiene, not a knowledge defect.

## Claims that survived attack (re-derived, not trusted)

All commands run from `/home/vgpnk/Projects/shokunin/kake-shokunin`.

1. **v2 sha256 quote.** `sha256sum .ufo/waves/round-45/c45_audit.py` →
   `f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076` (= HEAD `e545525`).
   Entry quotes `f3c3171b658abccd…0a076`, correctly elided. **PASS as “at landing”.**
   Caveat: the worktree file is now `b61447e6…4156660` (see drift note), so a fresh
   `c45_matrix.py --stage after` would run bytes that no longer match the `driver_sha256`
   recorded in `after.json`; the recheck command therefore no longer reproduces its own receipt
   without a re-land.

2. **Frozen hashes in `source:`.** `sha256sum` of `.ufo/waves/round-44/c44_audit.py` →
   `8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75` and
   `.ufo/waves/round-44/c44_count_v5.py` →
   `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc`. Both exact. **PASS.**

3. **Class count.** `grep -cE '^\*\*\([abc]\) ' .ufo/waves/round-44/w2/ReviewCounterContract.md`
   → `3`. Labels confirmed at lines 41/57/73 as `(a)`/`(b)`/`(c)`. **PASS.**

4. **Fixture count.** `ls .ufo/waves/round-45/fixtures` →
   `counter-error  honest  stale-backdate  stale-planted  tool-absent`. **PASS.**

5. **27 controls.** `ls .ufo/waves/round-44/verification/claim/after-final/tools/ | wc -l` → `27`.
   **PASS.**

6. **Witness split.** The entry's exact one-liner over each receipt:

```text
--- .ufo/waves/round-44/verification/claim/after-v5.json
22 1 4
2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902
--- .ufo/waves/round-44/verification/claim/after-final/after-v5.json
26 1 0
9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1
```

Both tuples and both sha256 values match the entry and lesson 15. **PASS.**

7. **`verified-at` selftest claim (exit 0).** Re-ran the shipped selftest from scratch cwd:

```text
$ python3 -B .ufo/waves/round-45/c45_audit.py --selftest
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
EXIT=0
```

**PASS.**

8. **“Mutants m{1..4}_v2.py all die against the shipped selftest”.**

```text
m1_v2 EXIT=1 :: AssertionError
m2_v2 EXIT=1 :: AssertionError
m3_v2 EXIT=1 :: AssertionError
m4_v2 EXIT=1 :: AssertionError
```

**PASS** (each exits nonzero; the claimed direction holds).

9. **Matrix after evidence.** `.ufo/waves/round-45/verification/matrix/after.json`:
   `invalid_accepted: 0`, `rejections_named: 3`, named classes `counter_error`, `tool_absent`,
   `stale_receipt`; `honest: {exit: 0, valid: true, witnessed: 27, build_met: 3, problems: []}`.
   Run log: `stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3`.
   **PASS.**

10. **Counter/v1 line citations.** `c44_count_v5.py:1114-1119` covers both `finish(2)` sites
    (1116, 1119); `:1108` is exactly `rec["runs"][key] = entry` (class entries recorded before the
    exit-2 path); `:1031-1034` contains `cand = None`; `:1078-1080` contains `candExit =
    "tool absent"`; `:1113` is the `note = "tool absent"` assignment. `c44_audit.py:54-61` opens
    the receipt regardless of returncode, `:157` is `exit=code`, `semantic_witness` starts at 63,
    `expectation_ok` at 69, and neither reads the exit. **PASS.**

11. **CLI/field parity claim.** `add_argument` sets are identical between `c44_audit.py` and
    `c45_audit.py` (11 options); summary rows carry the same fields. **PASS.**

12. **Falsification record.** `SCORECARD.md:3734-3743` records the C1 verdict as “NOT MET as
    declared”, names `w1/CriticC1Predicate.md`, and keeps the bounded repair separate from the
    causal reading. The entry's summary of that record is accurate; only its routing tail is
    unverifiable (F6). **PASS** on the falsification clause.

## What I did not run / residual risk

- I did not run `c45_matrix.py --stage before|after` (the entry's recheck command) — the committed
  `after.json` and `run-log.txt` were inspected instead. The recheck is the entry's own instruction,
  and I am not asserting it fails; it was simply out of this seat's time box.
- F1's probe is a scratch fake counter. It establishes gate acceptance, not that any committed
  counter or the honest cohort is affected. The 27/27 honest cohort is unaffected by construction
  (one receipt per row, written by that row's invocation).
- The `stale-planted`/`stale-backdate` labeling in `after.json` was observed but not traced into the
  fixture directories.
- The driver drifted mid-seat (`f3c3171b` → `b61447e6`, uncommitted, sibling `bad-build` fixture).
  F1's probe was run against both byte versions with identical results; the selftest exit-0 run and
  the `after.json` cross-check belong to `f3c3171b`.
- S133's remote availability was not re-fetched; the retained 208,624-byte HTML was used, matching
  the size and scope recorded in `corpus/SOURCES.md:141`.
- No tool installs or updates were needed; nothing was installed.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2/AttackKnowledgeEntry.md`
  (this report).
- Scratch only: `/fast/scratch/hyaku/kake-r45/AttackKnowledgeEntry/probe/{controls.tsv,root/ctl1.py,
  root/ctl2.py,root/counter.py,out/…}`.
