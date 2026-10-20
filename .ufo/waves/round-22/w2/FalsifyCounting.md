# FalsifyCounting — round-22 wave-2 (author-side falsifier, read-only on lane)

Seat: `KakeR22.FalsifyCounting` · Claim: **C1 operability — offline static
canonical publishing preflight** · Measured revision: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`
· Frozen base: `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Scope: revision counter denominator, baseline absence, source commit/blob hashes.

Axes: **operability** (does the count command reproduce the claim),
**verifiability** (can the number be re-derived without trusting it),
**honesty** (can the counter emit a success verdict that the data contradicts).

Report written to `.ufo/waves/round-22/w2/FalsifyCounting.md`; all probes ran
against a scratch clone `/tmp/kake-r22-falsify-counting` (git clone
--no-hardlinks of the lane; one throwaway probe commit `3a712e1` exists only
there) or were read-only git/sha256 queries. No production bytes touched; no
builds, lints, or formatters; no installs.

## Counter-example 1 — the numerator is trusted, not recomputed (demonstrated)

`measure.py:546` copies `matrix_result["accepted"]` into the top-level result and
`measure.py:603` derives the process verdict (`accepted != total` → exit 1) from
that declared number. It validates the **population** (32-name set equality on
`cases.json` and on result `caseId`s, `population_error` at :179, and
`total == len(results) == 32` at :573) but never recomputes acceptance from the
per-case rows it reports and never cross-checks `executed`, `discrepancies`, or
`matrixExitCode` consistency (a matrix may declare `discrepancies: 0` while
emitting 32 FAIL rows — the two are never reconciled).

**Demonstration** (`/tmp/kake-r22-falsify-counting`, probe commit
`3a712e162164124aa2f2a42baa4b8a375afadf5d`): replaced `matrix.py` with a stub
that never invokes `scripts/canonical_audit.py`, emits 32 results all marked
`status: "FAIL"`, `actualExit: 99`, `executed: 0`, but declares
`"accepted": 32, "total": 32` and exits 0. Then ran the real counter:

```
python3 .ufo/waves/round-22/measure.py --root /tmp/kake-r22-falsify-counting \
    --revision 3a712e162164124aa2f2a42baa4b8a375afadf5d
→ exit 0; JSON: accepted=32, total=32, available=true, unavailable=false,
  matrixExitCode=0 — while results[] contains 32 rows of status=FAIL,
  actualExit=99.
```

The counter's own success signal (exit 0 + `accepted/total`) therefore carries
no independent authority; on this probe revision it asserted "32/32" for a
validator that was never executed. The per-case rows expose the lie, but only a
consumer who re-audits them sees it.

**Impacted axis:** operability/verifiability of the `count` command for any
`--revision` whose instrument is not additionally digest-pinned by
`frozen/expected.json` + `replay.py`. Wave-1's `FrozenReplay.md` F5 warned of
"count-only oracle"; the landed counter is one. This does **not** falsify C1 at
`c0fd6d5` — the committed `matrix.py` there computes `accepted` by incrementing
on real per-case PASS (`matrix.py:282`), its bytes are pinned
(`a0cc66f7bc8ab4069d95f7b1b43cf71b2fd80615`, sha256 `d7de62…`) and the
instrument digests match `frozen/expected.json` — but it means the count
command certifies only the *population* of a measured revision, not the
*outcome* declared by that revision's instrument.

**Smallest safe correction (author-side, additive):** in `measure.py`, after the
existing shape checks, recompute `accepted` as the count of rows with
`status == "PASS"` (or of rows where `actualExit == expectedExit` and
`actualFindings == expectedFindings` against the pinned `cases.json` already in
`measured_blobs`), require it to equal `matrix_result["accepted"]`, and require
`executed == total`, `discrepancies == executed - accepted`, and
`matrixExitCode == 0`; otherwise return `invalid_population_result` (exit 1).
Equivalent bounded acceptance: require `replay.py` digest-verification of the
instrument before treating `accepted` as authoritative. Either restores the
counter's verdict as derived evidence.

## Counter-example 2 — baseline path exits 0 when the baseline could not be measured (demonstrated)

`measure.py` special-cases `revision == BASE_REVISION` to exit 0 on absence of
the validator so the documented "before" run is green. But two of the three
baseline-absence branches also return **exit 0** when the instrument itself
could not be validated:

- :429–441 — validator absent *and* no complete instrument and no
  `--cases-root` → `unavailable_result` + `instrumentValidated=false`, `return
  result, 0`.
- :447–458 — validator absent *and* `--cases-root` instrument incomplete →
  `instrumentValidated=false`, `return result, 0`.

**Demonstration:**

```
python3 .ufo/waves/round-22/measure.py --root /tmp/kake-r22-falsify-counting \
    --revision 7c61c8cc791bde36dd5e3688bdfea2678d90146c     # no --cases-root
→ exit 0; available=false, unavailable=true, accepted=0, total=32,
  instrumentValidated=false,
  error="baseline validator missing and no complete instrument; …",
  missingInstrumentPaths=[matrix.py, cases.json, fixtures/, fixtures/escape.html]
```

A consumer gating on exit 0 (or on `accepted=0, total=32, unavailable=true`)
cannot distinguish "the frozen baseline demonstrably has no validator" — the
C1 before-state — from "the baseline run could not even assemble an
instrument". Both exit 0. The committed `measure-before.json` is the good case
(`instrumentValidated=true`, `--cases-root` supplied, all 66 instrument blobs
sha256-pinned with `source: working-tree`), so the recorded C1 before-state is
sound; the defect is that the *failure* mode is indistinguishable by exit code.

**Impacted axis:** honesty/verifiability of the baseline-absence evidence.
**Smallest safe correction:** return a nonzero exit (e.g. 2) or a distinct
`unavailable` sub-code when `instrumentValidated` is false — i.e., exit 0 on the
baseline path only after `instrument_complete(...)` and the cases-population
check pass (:476–484 already does exactly that and is the only baseline branch
that should stay green). Alternatively, declare in L1's report that consumers
MUST inspect `instrumentValidated`, not exit code.

## Verified (what survives the attack)

All checks run read-only against the lane repo; no re-runs of the full matrix
were needed beyond the bounded probes above.

- **Baseline absence is real.** `git ls-tree
  7c61c8cc791bde36dd5e3688bdfea2678d90146c -- scripts/` shows only
  `corpus-contract.mjs`, `freshness-sweep.mjs`, `probe-delta.mjs` — no
  `canonical_audit.py` anywhere in the base tree; `ls-tree -r` on
  `.ufo/waves/round-22` at base is empty (nothing committed). `measure-before.json`
  records `available:false, unavailable:true, accepted:0, total:32,
  instrumentValidated:true, instrumentRevision:"working-tree"`, matching
  wave-1's U4 design ("no baseline instrument exists; only baseline-target
  absence"). Caveat for the record: absence is proven for the *named* entry
  `scripts/canonical_audit.py`, not for any possible capability spelling —
  contract-shaped and acceptable.
- **Denominator is frozen correctly.** `EXPECTED_CASES` in `measure.py:20-53`
  and `FROZEN_CASE_NAMES` in `matrix.py:18-51` are identical copies of the
  contract's 32 `matrixCases`; `population_error` enforces set-equality with
  duplicate/missing/extra naming on both `cases.json` and emitted results;
  `total == len(results) == 32` is hard-checked before `accepted` is reported.
- **Instrument identity before == after.** The 66 `working-tree`-sourced blob
  sha256s in `measure-before.json` equal, path-for-path, the 66 git-sourced
  instrument pins in `measure-after.json` (only `scripts/canonical_audit.py`
  added, as designed); the baseline comparison held the instrument fixed.
- **Every pin verifies.** All 67 `blobs` entries in `measure-after.json` run 0
  were rechecked against `git ls-tree -r c0fd6d5…` (gitObject + gitMode match,
  0 mismatches) and `git cat-file blob | sha256sum` (0 mismatches). Every
  `frozen/expected.json` input digest that measure also pins matches; the two
  extra replay inputs (`domain-snapshot/index.html`, `manifest.json`) are
  outside the counter's scope by design.
- **Source commit/blob hashes are accurate.** `domain-snapshot/provenance.json`
  claims `/home/vgpnk/Projects/ufo-fsd-alpha` @
  `31c465f15669f744848bd9f5d56191c5085670f7`,
  `docs/charter-ufo-fsd/index.html`. Verified: that commit resolves, and
  `git show <commit>:docs/charter-ufo-fsd/index.html | sha256sum` =
  `43d321f91cf018dc75d6f0052a573e3f198b0c1a159e0615574f8e0eecc5296b` = sha256 of
  the archived `domain-snapshot/index.html`. No false provenance.
- **Replay pin set is correct.** `frozen/expected.json` `inputs` (69 entries)
  covers matrix.py, cases.json, all 64 fixture members, the validator, and the
  two domain-snapshot files; `replay-integrated.json` reports `frozen_replay_match`,
  `inputsVerified: 69`; live worktree digests of `matrix.py`/`cases.json`/
  `canonical_audit.py` match (`d7de62…`, `28a490…`, `35433e…`).
- **Determinism evidence is real.** `measure-after.json.runs[0]` and `runs[1]`
  are byte-identical parsed JSON (including embedded matrix stdout/stderr);
  `instrumentRevision` == `revision` == `c0fd6d5…` == live `master` tip
  (`git rev-parse master`).

## Bounded acceptance / residual limits (not defects requiring correction)

- **Duplicate authority, kept consistent.** The 32-name set lives twice
  (`measure.py` + `matrix.py`) and expectations live in `cases.json` —
  author-side oracle by design (U5). The judge must read the count as
  "conforms to the committed frozen expectation table at the pinned
  instrument digest", not "independently adjudicated", matching wave-1's own
  wording rule.
- **Runner bytes unpinned in the record.** `frozen/expected.json` pins
  `matrix.py`/`cases.json`/`canonical_audit.py` but not `measure.py` or
  `replay.py`; `measure-after.json` records no runner digest (live
  `measure.py` sha256 `329f45b6…` = committed blob `359c7350…` at c0fd6d5,
  verified here). The count executes whatever `measure.py` sits in the
  invocation checkout; FrozenReplay's P0 already prescribed runner-digest
  equality, so this is a documented gap the L1 recipe covers, not new evidence
  debt. Recording the runner sha256 in the result would make P0 cheaper.
- **Baseline `--cases-root` trust.** The before-run instrument came from the
  candidate lane working tree; pins + `instrumentRevision` disclose it, and
  byte-identity with the committed c0fd6d5 instrument (verified above) removes
  any actual divergence.

## Disposition

Two fixable defects, neither fatal to C1 as evidenced at `c0fd6d5`: (1) the
counter parrots a declared numerator instead of deriving it — demonstrated to
emit `accepted=32`/exit 0 on an instrument that never ran the validator;
(2) the baseline path exits 0 even when the instrument is unvalidated,
conflating "proven absent" with "unmeasurable". Smallest safe correction for
(1) is recomputing `accepted` from the per-case rows already pinned in the
result; for (2) gating the baseline exit 0 on `instrumentValidated`. If L1 does
not patch, bounded acceptance is possible only if admission requires the
`replay.py`/`frozen/expected.json` digest verification alongside the bare
`count` exit, and the report states the counter verifies population, not
declared totals.
