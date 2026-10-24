# AttackC1Sentence — C1 disposition attack

Seat: `kake-r45.AttackC1Sentence`. Axis attacked: **operability**. Freshness is lane context, not separately assessed. Read-only review apart from this report and the assigned scratch directory; no admission or canonical judgment is made here.

## Result

**Disposition sound as an honest stop on the full frozen sentence. Named attack: FAIL to overturn that disposition.** Two fixable explanation/evidence defects were found: the operator question overstates what a nonce echo establishes, and the matrix does not literally use the same stale fixture before and after. Neither turns the bounded result into causal attestation.

This is not a finding that the frozen numerical MET condition failed: **it passed.** A bounded reading was available in the original declaration, not invented after measurement. The declaration contains an ambiguity between an explicit numerical “iff” and a stronger sentence. Calling the full sentence unproved is defensible; calling the numerical condition failed, or calling a bounded reading unavailable all along, would not be. The L1 explicitly preserves the numerical success at `SCORECARD.md:3727-3728`, so I find no false failure report or concealed repair here.

### Exact sentence at issue

`SCORECARD.md:3639-3645`:

> the audit driver v2 at `.ufo/waves/round-45/c45_audit.py` refuses to count as a witness, and refuses to count as not-met, any control whose receipt (i) records a counter exit other than 0 or 1, or (ii) records the note "tool absent", or (iii) was not written inside the driver's own run window over the invoked counter bytes; and it still certifies the honest round-44 cohort (all 27 controls witnessed under `--classes v5` and three build runs met at revision `020bc457`).

The competing, equally frozen acceptance sentence at `:3655-3658` is:

> before runs the frozen v1 driver over the three fixture classes; after runs v2 over the same fixtures plus the honest regression cohort. Claim MET iff the before receipt records `invalid_accepted=3` and the after receipt records `invalid_accepted=0`, `rejections_named=3`, `honest_witnessed=27`, `honest_build_met=3`.

## Findings against the three assigned questions

### 1. Could this have meant the bounded claim all along?

**YES — attack PASS on interpretive ambiguity; FAIL on overturning the honest-stop disposition.**

The strongest counterexample to an exclusively universal reading is the declaration itself: `:3632` calls the moves bounded, `:3647` names “the three committed invalid fixture classes,” and `:3656-3658` says “Claim MET iff” followed by exactly the measured conjunction. A reasonable reader could have understood C1 as those three regression classes plus honest-cohort preservation. That interpretation is not a new numerical target.

But the specific causal phrase “over the invoked counter bytes” and “any control” in the explicitly labeled frozen sentence are not qualified by an explicit trusted-local-writer assumption. The observations in `receipt_validity` establish exit eligibility, note, reported hash equality, seed presence, and mtime interval membership—not writer identity or executed-byte identity. The old critic carefully labeled its counterexample as a model, not a live bypass, and expressly distinguished the trusted-counter interpretation (`w1/CriticC1Predicate.md:8-12,18-26,52-56`). That restraint remains correct after the implementation arrives.

**[INFERENCE] Strongest counterexample to full-sentence proof:** two writer histories with the same JSON, public hash field, exit, seed, and mtime are observationally identical to `receipt_validity`. Nothing in that function authenticates which bytes wrote the JSON. This is an evidence-sufficiency argument, not an observed attack on the landed driver. I did not construct or execute a different-writer bypass.

The L1's split disposition—numerical condition met, full causal assertion not established—therefore avoids asserting the stronger unproved claim. The canonical judge/operator must resolve the pre-existing sentence-versus-iff ambiguity; this leaf does not silently select a new claim.

### 2. Operator-owned trust boundary or punt?

**Genuine operator-owned boundary decision; attack FAIL on “punt.” A technical premise in the handoff is defective (attack PASS).**

The routed question exists at the **fleet root**, `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:132`, not under the lane's `.ufo/`. It asks whether to adopt trusted-local-counter bounded scope or require causal provenance. Deciding which frozen meaning may be admitted is not a permission the implementation author can award itself. The bounded repair has already been built and exercised, so routing is not a substitute for doing those repairs.

However, the handoff says causal provenance “requires counter-side nonce echo = a new instrument family.” That is not supported by the critic it cites: `CriticC1Predicate.md:56` explicitly says an echoed public nonce alone is **not** the missing mechanism. A nonce can help distinguish runs without authenticating the writer or loaded bytes. The implementation's manifest nonce is written at `c45_audit.py:356-363` and is not an input to `receipt_validity` (`:68-87`).

Smallest safe correction: append a clarification to the fleet question distinguishing the operator's **scope/admission choice** from the lane's **technical proof obligation**. Remove the implication that nonce echo alone supplies causal provenance or that a particular new instrument family has been proved necessary. Name the fleet-root path explicitly in the lane pointer. No new protocol, counter change, or runtime invocation is needed to correct that explanation.

### 3. Does bounded verification prove the three routed defects closed?

**PASS for the operational regression checks; FAIL if expanded to complete causal-provenance closure or a byte-identical three-fixture A/B claim.**

Evidence is stronger than merely `ok=false`: each stored after control has `witnessed=0`, `notMet=0`, and the expected row-level error. I independently ran the landed driver's existing `--selftest` with all temporary files confined to my scratch directory. Its fresh isolated summaries likewise exclude all three invalid controls from **both** counts; the honest legacy-divergence control remains credited as not-met. Thus this is not only a refusal caused by failing build rows or a reject-everything gate.

Source trace: exit and note guards are at `c45_audit.py:70-75`; SHA/seed/window guards at `:76-86`; the control path always calls the gate at `:106-119,374-377`; `valid_rows` and `not_met_rows` exclude invalid rows at `:135-144`. The empty-output-directory guard at `:333-338` independently prevents the originally routed pre-planted-directory replay before counters run. I did not freshly replay that original pre-planted-directory scenario; this last statement is a source trace, corroborated only by the historical `ReviewV1Defects.md:194-213` report, not a new runtime observation.

**Fixable evidence qualification:** the actual before fixture is `stale-planted` (old authentic receipts plus SIGKILL), whereas after uses `stale-backdate` (a new receipt, backdated five seconds, exit 0). `c45_matrix.py:43-44,75-78` and both matrix receipts expose this substitution; it is not hidden, but “same fixtures” is literally inaccurate. The latter receipt was actually written during the invocation by the invoked fake counter, then had its metadata changed (`fixtures/stale-backdate/fake_counter.py:17-25`). It tests the mtime proxy, not historical write-event origin. It also contains only a small receipt subset (`counterSha256`, `seed`, `note`, `met`, `runs`), unlike the real frozen-counter record initialized at `c44_count_v5.py:996-1003`. Consequently it must not be presented as independently satisfying frozen kill rule 5's authentic-receipt-shape requirement without a separate fidelity argument.

Also, the stored counter-error and tool-absent fixture builds all fail `stale_receipt` because the fake counters copy old build receipts. A global red summary alone would be confounded. The actual row-level exclusions and the fresh selftest counts below remove that confound for the bounded control checks; they do not retroactively repair fixture fidelity or prove causal provenance.

The honest matrix receipt records the frozen-v5 counter SHA, 27 witnessed controls, no errors, and three met builds. I inspected its first underlying build receipt, which names full revision `020bc4574729ed674299f6cab02faac1582d9464`. I did not independently rerun the 27-control/three-build cohort or replay its recorded seeds.

## Exact commands and verbatim decisive output

Cwd for shell commands: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

1. `mkdir -p /fast/scratch/hyaku/kake-r45/AttackC1Sentence`

Exit 0; no output.

2. `sha256sum .ufo/waves/round-45/c45_audit.py .ufo/waves/round-45/c45_matrix.py .ufo/waves/round-44/c44_count_v5.py`

Exit 0:

```text
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  .ufo/waves/round-45/c45_audit.py
ebcccd55dcf910f87c14be5b5f8c912731d323b78ad1695284cb4321f642c63b  .ufo/waves/round-45/c45_matrix.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
```

3. Stored-receipt reduction, not a matrix rerun:

```sh
jq -cs 'map({stage,driver_sha256,invalid_accepted,rejections_named,honest_witnessed,honest_build_met,fixture_ids:[.fixtures[]|.fixture]})' .ufo/waves/round-45/verification/matrix/before.json .ufo/waves/round-45/verification/matrix/after.json
```

Exit 0:

```text
[{"stage":"before","driver_sha256":"8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75","invalid_accepted":3,"rejections_named":0,"honest_witnessed":27,"honest_build_met":3,"fixture_ids":["counter-error","tool-absent","stale-planted"]},{"stage":"after","driver_sha256":"f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076","invalid_accepted":0,"rejections_named":3,"honest_witnessed":27,"honest_build_met":3,"fixture_ids":["counter-error","tool-absent","stale-backdate"]}]
```

4. Stored row-level credits:

```sh
jq -c '{file:input_filename,controls,witnessed,notMet,ok,row_exit:.rows[0].exit,row_error:.rows[0].error,build_errors:[.build[].error]}' .ufo/waves/round-45/verification/matrix/runs/after/counter-error-bfdcbac53c48/summary.json .ufo/waves/round-45/verification/matrix/runs/after/tool-absent-754d72a556bf/summary.json .ufo/waves/round-45/verification/matrix/runs/after/stale-planted-47bd82ade247/summary.json
```

Exit 0:

```text
{"file":".ufo/waves/round-45/verification/matrix/runs/after/counter-error-bfdcbac53c48/summary.json","controls":0,"witnessed":0,"notMet":0,"ok":false,"row_exit":2,"row_error":"counter_error","build_errors":["stale_receipt","stale_receipt","stale_receipt"]}
{"file":".ufo/waves/round-45/verification/matrix/runs/after/tool-absent-754d72a556bf/summary.json","controls":0,"witnessed":0,"notMet":0,"ok":false,"row_exit":1,"row_error":"tool_absent","build_errors":["stale_receipt","stale_receipt","stale_receipt"]}
{"file":".ufo/waves/round-45/verification/matrix/runs/after/stale-planted-47bd82ade247/summary.json","controls":0,"witnessed":0,"notMet":0,"ok":false,"row_exit":0,"row_error":"stale_receipt","build_errors":["stale_receipt","stale_receipt","stale_receipt"]}
```

5. Fresh shipped regression execution:

```sh
env TMPDIR=/fast/scratch/hyaku/kake-r45/AttackC1Sentence PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/waves/round-45/c45_audit.py --selftest
```

Exit 0:

```text
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
```

6. Fresh selftest row reductions:

```sh
jq -c '{file:input_filename,controls,witnessed,notMet,ok,row_exit:.rows[0].exit,row_error:.rows[0].error}' /fast/scratch/hyaku/kake-r45/AttackC1Sentence/kake45-audit-selftest-jbgcxs7i/out-counter-error/summary.json /fast/scratch/hyaku/kake-r45/AttackC1Sentence/kake45-audit-selftest-jbgcxs7i/out-tool-absent/summary.json /fast/scratch/hyaku/kake-r45/AttackC1Sentence/kake45-audit-selftest-jbgcxs7i/out-stale/summary.json /fast/scratch/hyaku/kake-r45/AttackC1Sentence/kake45-audit-selftest-jbgcxs7i/out-honest/summary.json
```

Exit 0:

```text
{"file":"/fast/scratch/hyaku/kake-r45/AttackC1Sentence/kake45-audit-selftest-jbgcxs7i/out-counter-error/summary.json","controls":0,"witnessed":0,"notMet":0,"ok":false,"row_exit":2,"row_error":"counter_error"}
{"file":"/fast/scratch/hyaku/kake-r45/AttackC1Sentence/kake45-audit-selftest-jbgcxs7i/out-tool-absent/summary.json","controls":0,"witnessed":0,"notMet":0,"ok":false,"row_exit":1,"row_error":"tool_absent"}
{"file":"/fast/scratch/hyaku/kake-r45/AttackC1Sentence/kake45-audit-selftest-jbgcxs7i/out-stale/summary.json","controls":0,"witnessed":0,"notMet":0,"ok":false,"row_exit":0,"row_error":"stale_receipt"}
{"file":"/fast/scratch/hyaku/kake-r45/AttackC1Sentence/kake45-audit-selftest-jbgcxs7i/out-honest/summary.json","controls":1,"witnessed":0,"notMet":1,"ok":true,"row_exit":1,"row_error":null}
```

Additional decisive read-only tool evidence:

- `read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md:3600-3790")` supplied the exact frozen and measured sentences above.
- `grep(pattern="round.45|causal|receipt.*trust|trust.*receipt|C1.*provenance", path="/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md", case=false, gitignore=false)` returned the operative handoff verbatim:

```text
kake | round-45 | C1 disposition: is the witness-gate trust boundary the bounded three-fixture reading (trusted local counter; causal-provenance hole named in SCORECARD) or must the gate prove causal provenance (requires counter-side nonce echo = a new instrument family)? CriticC1Predicate classified the literal sentence claim-breaking; adopting either reading is an operator ruling.
```

The initial lookup under the lane's `.ufo/l0-questions.md` returned `Path not found`; a scoped glob located the actual fleet-root file. This is a relative-pointer qualification, not an absent handoff or a blocker.

## Smallest safe correction / impacted axis

Operability is affected by claim interpretation and what the runnable checks actually establish. Keep the existing honest-stop disposition and measured results; append an explicit acknowledgment that the original numerical iff passed and that a bounded reading was originally available. Correct the nonce-echo premise in the operator handoff. Distinguish the two stale fixtures and qualify authenticity/mtime-proxy coverage rather than saying a causal origin property has been closed. No frozen sentence should be rewritten, no bounded success upgraded to full causal success, and no extra implementation should be smuggled into this review. Scope/admission remains for the canonical judge/operator.

## Files written and unrun checks

Only lane file written:

- `.ufo/waves/round-45/w2/AttackC1Sentence.md` — this report.

The shipped selftest wrote the following files under the common scratch prefix `/fast/scratch/hyaku/kake-r45/AttackC1Sentence/kake45-audit-selftest-jbgcxs7i/` (each entry is relative to that prefix):

```text
controls.tsv
root/ctl.py
counter-error/fake_counter.py
tool-absent/fake_counter.py
stale/fake_counter.py
honest/fake_counter.py
out-counter-error/run-manifest.json
out-counter-error/summary.json
out-counter-error/tools/ctl1.json
out-tool-absent/run-manifest.json
out-tool-absent/summary.json
out-tool-absent/tools/ctl1.json
out-stale/run-manifest.json
out-stale/summary.json
out-stale/tools/ctl1.json
out-honest/run-manifest.json
out-honest/summary.json
out-honest/tools/ctl1.json
```

No other files were written by this seat. No tool installs/updates, package transactions, mutations of lane bytes, commits, pushes, subagent dispatch, judge/admission, or other model runtime occurred. Fresh matrix before/after, real honest-cohort/seed replay, original planted-directory replay, authentic-shape reconstruction, and different-writer bypass are **unrun**. The report separates existing stored evidence, current source traces, inference, and the one freshly exercised shipped selftest.
