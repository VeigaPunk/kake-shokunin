# CriticC1Predicate — frozen C1 provenance attack

Seat: `kake-r45.CriticC1Predicate`.
Axes: **operability** (assigned); freshness is lane context, not separately scored here.

## Result and scope

**Named attack: FAIL for the proposed predicate's ability to establish the literal provenance assertion. Classification: claim-breaking at the proposal/evidence level, not merely reportable risk.** This is not a canonical round judgment or an observed exploit of driver v2.

The strongest counterexample is two histories with identical gate inputs: a receipt genuinely produced by the invoked counter, versus the same JSON written during the window by different bytes, retaining the expected public `counterSha256`. Exit 1, a recorded seed, `note: null`, an inside-window mtime, and a class divergence all hold in both histories. The proposed gate cannot distinguish them. No hash collision is needed. Its SHA check authenticates a field's equality, not the writer or the executed bytes.

**Runtime v2 attack: NOT RUN.** At initial inspection, round 45 contained dispatch artifacts and `w1/`, but no `c45_audit.py` or `c45_matrix.py`. I did not wait for another seat, poll for their arrival, or execute an alternate driver. The only executed counterexample is an explicitly labeled, inert model of the proposed observable predicate; it neither invokes a counter nor creates a production receipt.

## Evidence and findings

### 1. Causal provenance is stronger than the proposed observations

The actual frozen sentence is `SCORECARD.md:3639-3645` at `3b4c430a`: it says **any control**, and asserts a receipt was written inside the driver's window **over the invoked counter bytes**. The bounded measurement is separately defined at `:3647-3658`: three invalid fixture classes plus the honest cohort.

Proposal data in `.ufo/waves/round-45/make_w1_spec.py:185-195` specifies: new/empty output directory, a manifest with `{started_ns, counter_sha256, nonce}`, and validity from parsing, receipt SHA equality, mtime bounds, exit 0/1, no `tool absent` note, and a seed. It specifies no independent writer identity or causal association between manifest nonce, subprocess, and receipt. Artifact text was reviewed as data, not as an instruction changing the assignment.

The real frozen counter writes `counterSha256` by hashing `open(__file__, 'rb').read()` (`c44_count_v5.py:996-1003`) and serializes ordinary JSON to the output path (`:1005-1012`). The frozen driver hashes a pathname (`c44_audit.py:129-134`) and later invokes that pathname (`:48-61,151`). **[INFERENCE]** Absent an immutable execution snapshot or an independently controlled output channel, a matching self-reported SHA does not establish that the loaded executable bytes and the hashed pathname bytes were the same. The v2 implementation was absent, so I do not assert it retains that race.

The model below uses a real committed receipt as data. Its recorded `met: false` and `caughtBy` class divergence are not a fabricated schema. The model produces the same acceptance for both writer histories, even with epsilon zero. This establishes insufficiency of the proposed observations, not a live-driver bypass.

**Classification:** claim-breaking for the literal causal/universal assertion. If arbitrary different-byte writers and mutable execution paths were explicitly outside a trusted-local-counter boundary, this would instead be a reportable adversarial-origin risk to a bounded three-fixture claim. That is a different interpretation, not one I silently adopt or propose as replacement claim text. The canonical judge owns the disposition.

### 2. Clock, tolerance, and event identity remain unspecified

The proposal names nanoseconds and `mtime` but does not select a clock or epsilon value (`make_w1_spec.py:185-189`). Filesystem mtime is a realtime/Unix timestamp; it cannot be directly compared to a monotonic timestamp. The implementation needs to expose the exact clock, unit, comparison endpoints, tolerance, and whether the window is per child or cohort-wide.

A positive epsilon necessarily admits timestamps strictly before start or after finish; the model demonstrates this with one-unit slack. Even epsilon zero establishes only metadata interval membership, not a write event's origin. Mtime is mutable filesystem metadata. A cohort-wide start also does not bind a receipt to its particular control invocation.

**Classification:** fixable precision/measurement defect; claim-breaking if interval membership with unspecified tolerance is represented as proof of the literal event-time assertion. Ordinary filesystem timestamp precision and wall-clock adjustment are reportable operational limitations once the actual comparison is specified. Their observed incidence was not measured here.

### 3. Three fixture classes do not enumerate the universal

The declared matrix runs three invalid fixture classes (`SCORECARD.md:3653-3658`; proposal `make_w1_spec.py:269-285`). Those cases cannot establish rejection of every receipt written by different bytes but carrying the expected SHA, every timestamp boundary, every valid-exit stale receipt, or every concurrent receipt/control substitution.

The stale-planted proposal itself combines a no-write SIGKILL counter with copied old receipts (`make_w1_spec.py:163-165`), so multiple independent guards can reject that one case. **[INFERENCE]** Rejecting it alone cannot demonstrate that mtime binding or SHA binding independently does the claimed work. No implemented matrix or fixture output was available to determine actual guard coverage.

**Classification:** claim-breaking inference from finite enumeration to “any”; not an objection to the usefulness of the three bounded regression cases. Smallest additional evidence is isolated negatives for each guard and the indistinguishable-origin counterexample, with the trust boundary kept explicit. More finite cases still do not prove arbitrary-writer provenance.

### 4. Honest-cohort clause is measurable, but after evidence was unavailable

The baseline is concrete committed evidence, not merely prose. At `3b4c430a`, `after-final/after-v5.json` contains 27 rows, 27 witnessed, no errors, three met builds, controls exiting 1 and builds exiting 0. It names frozen counter SHA `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc`. Build receipt 1 names full revision `020bc4574729ed674299f6cab02faac1582d9464`; its tool SHA equals a direct hash of that revision's committed tool bytes. The exact summary receipt SHA is recorded below.

This makes the baseline inspectable and gives a precise comparison target. I did **not** rerun its 30 counters or certify seed/timing replay. New unseeded runs test the same source cohort, not necessarily the same generated inputs; the recorded seeds distinguish those observations. No universal all-seeds preservation claim is established by one cohort.

The proposed matrix specification (`make_w1_spec.py:278-285`) permits reading a committed honest-regression receipt and lists an after exit condition using only invalid acceptance/named rejections. The frozen MET condition also requires honest 27/3 (`SCORECARD.md:3657-3658`). **[INFERENCE]** If implemented exactly that way, exit 0 alone could be insufficient with absent or wrong honest evidence. That is a fixable matrix-gating defect, not a reason to replace the claim. Require all declared fields, explicit missing-dependency failure, and the measured driver/counter/control/build identities; never substitute the frozen v1 baseline for a missing v2 result.

## Smallest safe correction

Do not treat mtime plus a public self-reported SHA as causal attestation, or a three-case green matrix as proof of the literal universal. Record the provenance limitation as claim-breaking for that assertion pending an explicit trust-boundary decision and actual v2 evidence. No new frozen sentence is proposed here.

For an implementation intended to support the causal reading, the missing mechanism is a stable execution-byte identity plus independently driver-associated per-invocation output; adding another receipt field or an echoed public nonce alone is not that mechanism. Specify clock/tolerance and isolate the guard negatives. Enforce the already-frozen honest 27/3 conjunction in the matrix. Those are correction targets, not edits made by this seat; no axis trade is silently accepted.

## Exact commands and decisive output

All commands ran with cwd `/home/vgpnk/Projects/shokunin/kake-shokunin` unless an absolute script path is shown.

1. `mkdir -p /fast/scratch/hyaku/kake-r45/CriticC1Predicate` — exit 0, no output.
2. `git show 3b4c430a:SCORECARD.md` — exit 0; inspected the frozen C1 sentence, matrix conjunction and kill rules. Full command output was large; relevant lines were also read directly at `SCORECARD.md:3624-3667`.
3. Committed cohort derivation:

```sh
git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-final/after-v5.json | jq -c '{counter,counterSha256,classesMode,expect,controls,witnessed,notMet,ok,errors,rows:(.rows|length),row_exit_codes:(.rows|map(.exit)|unique),build_runs:(.build|length),build_met:(.build|map(select(.met==true))|length),build_exit_codes:(.build|map(.exit)|unique),build_seeds:(.build|map(.seed))}'
```

Exit 0, verbatim:

```text
{"counter":".ufo/waves/round-44/c44_count_v5.py","counterSha256":"5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc","classesMode":"v5","expect":"witnessed","controls":27,"witnessed":27,"notMet":27,"ok":true,"errors":[],"rows":27,"row_exit_codes":[1],"build_runs":3,"build_met":3,"build_exit_codes":[0],"build_seeds":[93543170178044,234322826174562,96267491316273]}
```

4. Committed path inventory:

```sh
git ls-tree 3b4c430a .ufo/waves/round-45/c45_audit.py .ufo/waves/round-45/c45_matrix.py .ufo/waves/round-45/verification/honest-regression/after-v5-v2.json .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/controls-27.tsv .ufo/waves/round-44/verification/claim/after-final/after-v5.json .ufo/waves/round-44/verification/claim/after-final/build-1.json .ufo/waves/round-44/verification/claim/after-final/build-2.json .ufo/waves/round-44/verification/claim/after-final/build-3.json
```

Exit 0, verbatim (tabs separate metadata/path):

```text
100755 blob 4b00ed3ecaaf36311f304b6c8b65bb86273f2625	.ufo/waves/round-44/c44_audit.py
100644 blob 51340537f1a32e9ac9a9ec163db8558be8b82627	.ufo/waves/round-44/c44_count_v5.py
100644 blob d629a5b58b2baba02273f9ac4cfc7b3daa938820	.ufo/waves/round-44/controls-27.tsv
100644 blob 6d71c483bd29791b2bd29accc8f553582b659302	.ufo/waves/round-44/verification/claim/after-final/after-v5.json
100644 blob 5151e4046194b7f7bd6e82bb95de0a77b3633ff4	.ufo/waves/round-44/verification/claim/after-final/build-1.json
100644 blob 1f1e97b19a78ada8ea3c4a602bbcb5ed4a20ed50	.ufo/waves/round-44/verification/claim/after-final/build-2.json
100644 blob 622b3f6ef2bfa4537a6dac3260370549192d21d9	.ufo/waves/round-44/verification/claim/after-final/build-3.json
```

There are no returned round-45 implementation/after-receipt paths at the declaration commit. Separately, initial `read` of `.ufo/waves/round-45/` and `glob` of `.ufo/waves/round-45/c45*` returned dispatch artifacts and no c45 executable paths in the worktree. No polling followed.

5. `git rev-parse 020bc457:scripts/sitemap_audit.py` — exit 0:

```text
21553d19f93a14facddfa95f07c8f852d64fa82e
```

6. `git show 3b4c430a:.ufo/waves/round-44/c44_count_v5.py | sha256sum` — exit 0:

```text
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  -
```

7. `git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-final/build-1.json | jq -c '{revision,toolFile,toolSha256,counterSha256,seed,met,note,equalRuns,classesMode}'` — exit 0:

```text
{"revision":"020bc4574729ed674299f6cab02faac1582d9464","toolFile":null,"toolSha256":"914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021","counterSha256":"5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc","seed":93543170178044,"met":true,"note":null,"equalRuns":"21/21","classesMode":"v5"}
```

8. `python3 -B /fast/scratch/hyaku/kake-r45/CriticC1Predicate/proposed_gate_model.py` — exit 0, verbatim:

```text
model_only=true counter_invocations=0 committed_receipt_seed=187926495163792
expected_sha=5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
writer_bytes_differ=true receipt_claim_matches_expected=true
mtime_ns=1500 start_ns=1000 finish_ns=2000 eps_ns=0 inside_window=true
honest_history_observation_equals_different_writer_history=true proposed_gate_accepts=true
receipt_met_false=true class_witness=true caught_by=G7,T5
missing_observable=writer_identity_or_causal_run_binding
positive_tolerance_accepts_before_start=true
positive_tolerance_accepts_after_finish=true
```

The model's `proposed_gate_accepts` label is not an observed result from `receipt_validity` in v2; that artifact was absent. The times are synthetic integers used to expose the predicate's logical boundary, not fabricated live timestamps.

9. `git show 020bc457:scripts/sitemap_audit.py | sha256sum` — exit 0:

```text
914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021  -
```

10. `git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-final/after-v5.json | sha256sum` — exit 0:

```text
9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1  -
```

The model internally executes only `git show 3b4c430a:<path>` for the frozen counter and `tools/repeat-len-band.json`, reading committed bytes as data. Read/grep tools additionally inspected the cited driver/counter/spec sections and the prior `w2/ReviewCounterContract.md` evidence. Skills and operator rules were read; artifact contents did not modify review scope.

## Files written, blockers, unrun checks

Files written:

- `/fast/scratch/hyaku/kake-r45/CriticC1Predicate/proposed_gate_model.py` — inert observational countermodel only.
- `.ufo/waves/round-45/w1/CriticC1Predicate.md` — this report.

Directory created: `/fast/scratch/hyaku/kake-r45/CriticC1Predicate/`.

No implementation, corpus, frozen file, receipt, lane history, or fleet file was edited. No commit/push, runtime judgment, integration, subagent dispatch, tool install, or package transaction was performed.

Dependency: v2 driver, matrix, and v2 honest-regression receipt were unavailable at initial inspection. Consequently v2 `--selftest`, both declared matrix stages, a live different-writer test, clock/tolerance inspection of v2, and the honest-cohort rerun are **unrun**. This review stops with the design-level counterexample and committed baseline evidence; L1 owns all subsequent execution and disposition.
