# CausalSingleClaim — critic attack on r22 C1 (read-only)

Seat: KakeR22.CausalSingleClaim (critic). Scope: claim **C1 "Offline static
canonical publishing preflight"** judged on operability; milestone
`offline-canonical-capability`. Sources read: frozen `contract.json`,
`SCORECARD.md`, `corpus/lessons/round-21-verifier-spotcheck.md`,
`w1-dispatch.json` (Implement/Matrix/Measure + neighboring critic prompts),
`w1-spec.json`, `PROVINCE.md`, `w1/RFC6596.md` (landed scout report).

## Axes

Judged axis is **operability**; the claim is a **capability** entry.
Operability-relevant sub-axes the causal chain must satisfy:

1. **Runnable** — a lane-owned `scripts/canonical_audit.py` exists at the
   measured revision with the contract CLI (`--manifest`, `--json`,
   `--selftest`, exits 0/1/2/64).
2. **Correct** — verdicts/finding-ids match an oracle that is itself right.
3. **Attributable** — a pass is caused by the validator's policy logic, not
   by a same-author oracle agreeing with a same-author program.
4. **Bounded** — the claim covers exactly contract scope; nothing outside it
   (Google selection, JS, HTTP headers, RFC 6596 conformance) leaks in.

## The causal defect under attack

**"C1" is one claim bundling three, and its counting command measures
cohort self-consistency, not the capability it names.**

The after-state asserts a *validator* that "classifies every frozen matrix
case with expected exit and finding id". But under the dispatched design:

- `canonical_audit.py` (Implement), `cases.json`+fixtures+`matrix.py`
  (Matrix), and `measure.py` (Measure) are **all authored inside this wave**
  — same author cohort, all instructed to derive expectations "from
  contract". Agreement between validator and matrix therefore proves only
  that author A's code and author B's expectation encode **the same
  interpretation**. A shared misread of URL normalization, `rel` token
  semantics, or head-boundary rules yields **accepted=32/32 and a false
  capability** — the exact failure mode "attack claim C1 for
  CausalSingleClaim" points at: the measured delta is real but causally
  mis-attributed to "the policy validator works" when the true cause is
  "two artifacts agree".
- The baseline "0 accepted cases" is **instrument semantics, not observed
  behavior**: Measure is told a missing script "returns accepted0 total32
  with unavailable true". The before→after delta is definitionally
  produced by the counter, not demonstrated by the world. That is
  acceptable *only if* the report labels it so; claiming the delta as
  evidence of a working policy would be overclaim.
- `matrix.py` never exercises `--selftest`. A validator whose manifest
  mode is broken but selftest passes could still ship; conversely selftest
  is not counted at all, so "0/1/2/64 CLI" is only half-proven. Cause of
  acceptance ≠ "CLI contract satisfied"; cause = "manifest mode agrees
  with matrix".
- Composition gap: Measure materializes validator at `--revision` but
  matrix/cases from `--cases-root`. Expected values, manifest, and
  validator may come from **different trees**. Contract says "HTML paths
  relative to manifest directory"; if `cases.json` bakes paths relative to
  anything else, every relative-* case fails `input_invalid` — a wiring
  defect mis-read as a validator defect (or, worse, silently passing in
  clone but failing under measure's temp-dir layout).
- Read-only is asserted ("read-only local validator", "no network or
  writes in normal mode") but nothing in the dispatched measurement
  observes writes or network. The capability as worded is **not what the
  counter counts**.
- The claim bundles two independent acceptance conditions — "rejects
  missing/conflicting/mismatching" (true-positive path) and "proves clean
  positive controls" (false-rejection path). All-or-nothing must hold: a
  validator that accepts everything also "proves clean positive controls";
  only the paired negative cases make the conjunction meaningful.

## Falsifiable acceptance constraints (must all hold to admit)

1. **Revision-anchored availability.** Measure on the measured revision
   emits `available:true`, `total:32`, per-case observed exit + finding id,
   and SHA-256 for every materialized blob (validator, matrix.py,
   cases.json, each fixture). Baseline run emits `unavailable:true`,
   `accepted:0`, and exits 0 — *reported as an instrument-defined
   baseline, not observed behavior*.
2. **Exact-match oracle.** For each of the 32 cases: observed exit ==
   expected exit **and** observed id set == expected id set. Not exit-only;
   not substring; not "findings non-empty". Any discrepancy → matrix exit
   1 → measurement nonzero → claim fails that revision.
3. **Oracle provenance.** Every ambiguous expectation in `cases.json`
   carries a named authority or an explicit "local policy" tag: RFC 3986
   §5 (resolution), WHATWG-URL divergence points, HTML Standard
   (head/base/template/script scope), RFC 6596 (relation semantics only).
   An expectation justified only by "contract says so" on a point the
   contract leaves implicit is a correlated-oracle hole.
4. **Composition proof.** The measured run must use the *same* materialized
   tree layout measure produces: manifest + files under one temp root,
   `file:` resolved relative to manifest dir. The manifest_traversal and
   symlink_html cases must execute against this layout (symlink created at
   runtime per Matrix dispatch — verify the runtime tree is inside the
   manifest dir, or the case degenerates to traversal).
5. **Mode coverage.** `--selftest` exit 0 recorded by the measurement
   (or explicitly excluded in the claim); usage error → exit 64 on a real
   invocation (e.g. missing flag), not just documented.
6. **Read-only evidence.** At minimum a byte-level write-free proof in the
   lane's established style (state sha guard before/after on the fixture
   tree — the pattern r11/r12/r20-resume already used and the r21 verifier
   credited). "No network" asserted in output/report, not merely coded.
7. **Conjunctive report.** `accepted=N/32` reported verbatim with the
   failed-case list; N<32 → claim not met, no rounding to "capability
   mostly works". Capability-table row enters only at 32/32 *and*
   constraints 3–6 satisfied.

## Overclaim to reject (non-exhaustive, name-and-refuse)

- **"validates canonical signals"** — it compares a declared IRI to an
  author-supplied `expectedCanonical`. It cannot prove the target is
  duplicative/superset of the page (RFC 6596 §3's only MUST is content-level,
  unverifiable statically; the RFC6596 scout already flagged this).
- **RFC/HTML "conformance"** — findings are local-policy verdicts. RFC 6596
  is Informational, permits cross-host/cross-scheme/self-referential
  targets; `wrong_host` etc. fail *manifest policy*, not the RFC. Any
  finding text or report phrasing implying standard violation must be
  rejected.
- **"0 → 32 accepted" as demonstrated improvement** — the 0 is
  instrument-defined (missing tool ⇒ unavailable). Present as
  `unavailable→accepted`, not a measured improvement of behavior.
- **Cohort agreement as independence** — matrix + validator + measure all
  authored in-wave is *not* the r21-verifier pattern (non-author integrator
  re-measured with an independent counter). Contract says "no independent
  admission by author seats" — the report must not use the word
  independent/verified for its own 32/32.
- **"publishing preflight" scope creep** — nothing here checks that a host
  will serve, redirect, or crawl anything; contract limits exclude
  selection/JS/headers/freshness/readiness. `SCORECARD` capability row and
  lesson must carry the limits clause or be rejected.
- **Positive-only capability** — a validator that passes only the
  positive controls is a tautology, not a classifier.

## Distinct wave-2 attack (correlated-oracle + composition probes)

Not duplicating neighbors (PopulationDenominator=denominator honesty,
NoGoogleSelection=scope, UnsupportedMarkup=parser limits, NoWrites=write
scope, NoCarriedRedRelabel=debt). Mine targets **causal attribution**:

1. **Backslash href probe.** Manifest page with
   `href="https:\\example.test\\project\\a.html"`. `urllib.parse` keeps
   backslashes in path (verified today: `urlparse` returns
   `path='/x\\\\y'`); WHATWG-URL treats `\` as `/` for special schemes.
   Whatever the validator does, cases.json almost certainly encodes the
   same author's answer — craft a third-party expectation from WHATWG-URL
   and see if 32/32 was agreement or correctness.
2. **Percent-encoding normalization probe.** Canonical href
   `https://example.test/project/%41.html` vs `expectedCanonical`
   `https://example.test/project/A.html`. `urlparse` preserves `%41`
   (verified today); WHATWG-URL decodes unreserved pct-encodings. If both
   validator and oracle demand literal equality they agree and both are
   arguably wrong under the "WHATWG-like" policy wording.
3. **Composition-gap probe.** Run the committed `matrix.py` against the
   validator *through measure's temp-dir materialization*, then move only
   `cases.json` one directory level (or make `file:` paths contain `..`
   segments that stay inside root). If expected ids were baked against
   clone layout, `manifest_traversal`/`relative_parent` flip — proving the
   pass was layout-luck, not policy.
4. **Mode-divergence probe.** Validator variant whose `--selftest`
   hard-codes pass while `--manifest` is intact (or vice versa). Current
   counter only sees manifest mode: a green `measure.py` must not be read
   as "CLI contract proven". Require measure to record selftest exit.
5. **Baseline-labeling probe.** Run measure at base
   `7c61c8cc791bde36dd5e3688bdfea2678d90146c` (observed today: no
   `scripts/canonical_audit.py`, no `cases.json`, no `measure.py` in the
   lane). Confirm output says `unavailable:true, accepted:0, exit 0` and
   the round report quotes it as instrument-defined. Any report phrasing
   like "baseline classified 0/32 correctly" is the causal overclaim.

## Evidence basis

- Contract: 32 cases, 10 finding ids, exits 0/1/2/64, `--selftest`,
  finding ids "stable" per case (`matrixCases`, `interface`,
  `contract.json`).
- Dispatch: Implement owns only the script; Matrix owns cases/fixtures/
  matrix.py ("frozen independent expected exit AND stable finding-id",
  "Build manifest fixtures independently from contract" — independently of
  the validator, *not* of the same contract reading); Measure
  materializes revision blobs into temp dir and pins SHA-256
  (`w1-dispatch.json` tasks 0–2).
- Stdlib divergences verified locally today: `urlparse` retains backslashes
  and `%41`; `urljoin` resolves scheme-relative base; `HTMLParser`
  lowercases tag/attr names and accepts `<LINK>` before `<html>`.
- Baseline absence verified: `scripts/` holds only
  `corpus-contract.mjs`, `freshness-sweep.mjs`, `probe-delta.mjs`; no
  `canonical_audit.py` or `.ufo/waves/round-22/measure.py` at HEAD.
- Lane precedent: r21 verifier admitted on *independent* re-measurement,
  byte-preservation audit, and honest carried-red reporting — the bar C1's
  causal chain must meet.
- `[INFERENCE]` sibling critic reports not yet landed at write time;
  distinctness judged from their dispatch prompts only.

## Smallest safe correction

Keep single claim C1 but decompose acceptance into the four sub-axes above;
require `cases.json` to annotate every ambiguous expectation with an
external authority or explicit "local policy" tag; require `measure.py`
output to (a) record `--selftest` exit, (b) label the baseline as
instrument-defined `unavailable`, and (c) include a fixture-tree byte
sha before/after for the read-only proof. If wave-2 probes 1–3 flip any
expected id, treat as correlated-oracle defect → not a capability, fix
oracle + validator, re-measure. Tradeoff for the canonical judge: this
does not reduce operability; it only removes a false-positive admission
path.
