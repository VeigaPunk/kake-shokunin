# CriticC1Predicate — C1 frozen-predicate attack

## Axes and result

- **Operability:** whether a counted class witness establishes class-run observation, or improperly claims incremental detection over v4.
- **Freshness:** whether the stated interpretation matches the frozen amendments and the actual claim receipt. No C2 audit was performed.
- **Named attack: FAIL against the frozen, amended class-observation capability.** A concrete mixed row exists and passes the per-control witness clause, but its class divergence is genuine. It defeats the stronger reading “every counted control is newly detectable only because of v5,” not the stated capability “a shortcut class is inside its differential counter's observation set.” The pre-freeze amendment expressly withdrew universal v4 blindness. Treating that withdrawn premise as still required would manufacture a different claim.
- **Concrete limit established:** the observed `23/27` class witnesses consist of **22 class-only rows and one mixed row**, not 23 demonstrations of incremental v4-blind-spot closure. The summary's `ok=false` remains as observed; this review does not adjudicate C1 or the round.

## Work performed and evidence

Read `git diff -- SCORECARD.md`, especially amendment A and correction 2; inspected the frozen auditor's classifier and the counter's run ordering; exhaustively partitioned the named receipt by `classCaught`/`legacyCaught`; inspected the mixed row's underlying recorded semantic divergences. No counter, class module, build, control, receipt, or ledger was changed or executed.

### Frozen text, read through the requested diff

Command, from `/home/vgpnk/Projects/shokunin/kake-shokunin`:

```sh
git diff -- SCORECARD.md
```

Decisive verbatim diff excerpt (`SCORECARD.md:3562–3568` in the inspected worktree):

```diff
+**Predicate reading frozen now, before data (removes the ambiguity in C1's sentence).** The clause
+"and no v4-corpus run does" is read as *a v4-corpus divergence is never a class witness*, not as *a
+control may not diverge on any v4 run*: the 27 controls' v4 behaviour is seed-dependent (attempt-1
+calibration found 2/27 diverging on fresh unseeded v4 runs), so a universal v4-blindness requirement
+would be a claim about a seed, not about the corpus. The before-state remains the placebo counter (a
+byte-copy of v5 whose ten class modules all delegate to `cases_f`): it cannot witness by construction,
+and the measured k/27 it reaches is reported, not targeted. Attempt-1 receipts
```

The actual capability row is at `SCORECARD.md:3460–3462`: proving that a shortcut class is inside the differential counter's observation set. Amendment A at `3510–3523` replaces the 27/27-blind baseline with the measured placebo baseline. Neither says that each counted control must be detected exclusively by the new runs.

### Strongest local counterexample candidate

Exact command:

```sh
jq -r '.rows[] | select((.classCaught|length)>0 and (.legacyCaught|length)>0) | "name=\(.name) met=\(.met) seed=\(.seed) error=\(.error)\nclassCaught=\(.classCaught|tojson)\nlegacyCaught=\(.legacyCaught|tojson)\ncaughtBy=\(.caughtBy|tojson)\nclassWitness=\(.met == false and (.classCaught|length)>0)\nclassOnlyWitness=\(.met == false and (.classCaught|length)>0 and (.legacyCaught|length)==0)\nreceipt=\(.receipt)"' .ufo/waves/round-44/verification/claim/after-v5.json
```

Verbatim output:

```text
name=repeat-len-band met=false seed=187179068777863 error=null
classCaught=["G7"]
legacyCaught=["C","T5"]
caughtBy=["C","G7","T5"]
classWitness=true
classOnlyWitness=false
receipt=tools/repeat-len-band.json
```

`classOnlyWitness` is an explicitly stronger diagnostic computed by this command, **not** a field or requirement of the frozen predicate.

Exact command inspecting the referenced receipt:

```sh
jq '{seed,classesMode,toolSha256,C:(.runs.C|{equal,ref41Exit,candExit,ref41OutSha256,candOutSha256}),G7:(.runs.G7|{equal,ref41Exit,candExit,ref41OutSha256,candOutSha256}),T5:(.runs.T5|{equal,ref41Exit,candExit})}' .ufo/waves/round-44/verification/claim/tools/repeat-len-band.json
```

Verbatim JSON output:

```json
{
  "seed": 187179068777863,
  "classesMode": "v5",
  "toolSha256": "c3a8770e5d76a8a7e218f56a2e9776fa03746770745d78a00f65dd6382df83ec",
  "C": {
    "equal": false,
    "ref41Exit": 2,
    "candExit": 2,
    "ref41OutSha256": "2f05378586d9ff9a4bf687aa6dcc867dc5ee86b21aa9c09fbc4a72aea20cfa84",
    "candOutSha256": "9a021248ef14f7925e7b1a409daf408886e464eded8618be5f3f17eb390e62c7"
  },
  "G7": {
    "equal": false,
    "ref41Exit": 1,
    "candExit": 1,
    "ref41OutSha256": "8aad13c98e814d35b6ce3896759828e1683a2811b137cc17dfbd7f2fbf81acc0",
    "candOutSha256": "1b86aa92fe5d47994a316494bcf90ad7b03506a18dc7b11e115276c80c840132"
  },
  "T5": {
    "equal": false,
    "ref41Exit": 2,
    "candExit": 2
  }
}
```

Both C and G7 have unequal stdout hashes, so G7 is not being credited merely because C fails, nor because of a timing ratio. `c44_audit.py:153–156` obtains `caughtBy` only from `run.equal is False`; `63–66` requires `met is False` and at least one actual class key. The class result survives deleting C and T5 from the witness list.

[INFERENCE] With the same seed and inputs, C would also catch this control in v4 mode: the counter initializes the same local RNG and executes A–F before inserting any class run (`c44_count_v5.py:1036–1065`). This is not a claim that a separately unseeded v4 run must catch it. No v4 replay was run. T5 is after the inserted class runs, so its same-seed v4 identity must not be inferred from this receipt alone.

### Exhaustive row-field case analysis

Exact command:

```sh
jq -r '.rows as $r | "classCaught>0\tlegacyCaught>0\trows\tsemanticWitnesses", ([false,true][] as $c | [false,true][] as $l | ($r | map(select((((.classCaught|length)>0)==$c) and (((.legacyCaught|length)>0)==$l)))) as $b | [$c,$l,($b|length),($b|map(select(.met == false and (.classCaught|length)>0))|length)] | @tsv)' .ufo/waves/round-44/verification/claim/after-v5.json
```

Verbatim output:

```text
classCaught>0	legacyCaught>0	rows	semanticWitnesses
false	false	4	0
false	true	0	0
true	false	22	22
true	true	1	1
```

Interpretation of all four cases (with the auditor's separate `met=false` requirement):

1. Neither: no class witness; a timing-only failure would remain ineligible. Here these are the four passing casememo controls.
2. Legacy only: no class witness, irrespective of how many legacy runs fail. No such row occurs in this receipt.
3. Class only: a class witness; 22 observed.
4. Mixed: a class witness because the class run independently differs; one observed. Legacy detections neither create nor invalidate that class evidence. This cannot establish incremental detection over v4, but incremental detection is not the amended per-row predicate.

## Smallest safe correction / exact sentence boundary

**No change to the frozen predicate is required for the stated observation-set capability.** Do not restore the old `all(caughtBy keys are class keys)` classifier: that would discard genuine class evidence and contradict correction 2.

The smallest safe reporting clarification is: **“Class-witness counts include mixed legacy/class detections; they do not count controls newly detectable over v4. In the inspected receipt, 23 class witnesses = 22 class-only + 1 mixed.”** This is a measurement clarification, not a new scoring rule. This seat did not append it to lane history.

If the intended capability instead means **every control represents a newly closed v4 blind spot**, the exact sentence that must change is correction 2's sentence beginning at `SCORECARD.md:3562`, “The clause ‘and no v4-corpus run does’ is read as …”, ending at `3566`, “… not about the corpus.” A future declaration would need, for example: **“For each counted newly closed control, a class run must differ semantically and a paired v4-mode replay at the recorded seed must have no semantic divergence; mixed detections are reported as class witnesses but do not count as newly closed v4 blind spots.”** That is a stronger, different claim requiring a new freeze and matching instrument, not a permissible post-receipt repair to this round. The present mixed row defeats that stronger reading. Canonical judgment is left to the designated judge.

## Other exact shell commands executed

Created the required isolated directory; no output and no temporary files created:

```sh
mkdir -p /fast/scratch/hyaku/kake-r44/CriticC1Predicate
```

Also enumerated every row before the concise case partition:

```sh
jq -r '"controls=\(.controls) witnessed=\(.witnessed) ok=\(.ok)", "name\tmet\tclassCaught\tlegacyCaught\tclassWitness\tclassOnlyWitness", (.rows[] | [.name, (.met|tostring), (.classCaught|join(",")), (.legacyCaught|join(",")), ((.met == false and (.classCaught|length) > 0)|tostring), ((.met == false and (.classCaught|length) > 0 and (.legacyCaught|length) == 0)|tostring)] | @tsv), "buckets(C,L):", (.rows | group_by([((.classCaught|length)>0),((.legacyCaught|length)>0)])[] | {classCaught:(.[0].classCaught|length>0),legacyCaught:(.[0].legacyCaught|length>0),count:length,names:map(.name)} | tojson)' .ufo/waves/round-44/verification/claim/after-v5.json
```

Its first output line was:

```text
controls=27 witnessed=23 ok=false
```

Read-only tooling additionally inspected the named SCORECARD, auditor, counter, claim summary and claim directory, plus Godspeed/Shokunin skill material. No source-editing tool, model/runtime invocation, installation, git write, or network command was used.

## Files written, checks, blockers

- **Only file written:** `.ufo/waves/round-44/w2/CriticC1Predicate.md` (this report).
- **Directory created:** `/fast/scratch/hyaku/kake-r44/CriticC1Predicate/`; no files inside.
- **Unrun:** counter/auditor execution, selftests, same-seed v4 replay, placebo measurement, held-build runs, canary runs, C2 checker, tests/build/lint. The report analyzes existing receipts; it does not present any of these as exercised.
- **Blockers:** none to this assigned static/receipt review.
- **Tools installed/updated:** none.
