## Verdict

C1 (freshness) and C2 (operability) are distinct by the lane’s axis definitions: C1 re-verifies path claims against the current filesystem; C2 makes the receipt-replay artifact reject invalid inputs safely. The round’s stated axes therefore make sense. The stronger claim of causal separability is only partially supported: C2’s mutation matrix is designed to use a fixed round-23 fixture base, so C1’s corpus annotations should not make C2 pass; however, C1’s counter runs the full paths sweep over the candidate revision, including C2’s documentation edits. The contract needs a cross-claim invariance check before claiming strict independence.

The C2 “before” names the real round-23 replay runners and their actual weaknesses, so it is not inherently a strawman. It is not yet a fair *measured comparison*, though: the frozen C2 case population and per-case observations are absent from the checked round-24 tree. A further concrete semantic mismatch is that the proposed `contentType` hardening rejects `null`, although the existing snapshot producer permits it as an absent HTTP header and the old replay treats it as not-served.

## Findings

### P2 — C1 is mechanically exposed to C2-owned corpus edits

**Evidence / exact inspected output.** The C1 counter assignment in `.ufo/waves/round-24/w1-spec.json:242` directs it to `git archive REV` and to run `node scripts/freshness-sweep.mjs --section=paths --json` over that complete tree. `scripts/freshness-sweep.mjs:234-239,346-352` recursively enumerates Markdown files under `corpus/` and scans them. `paths-before.json` reports `filesScanned: 55` and includes both `corpus/SOURCES.md` and `corpus/knowledge/static-canonical-preflight.md`. The C2 scribe assignment at `w1-spec.json:544` edits that same `static-canonical-preflight.md`; the C2 source-row task at `:527` edits `corpus/SOURCES.md`.

The contract’s line 33 says C1 and C2 “each counter reads only its own population and outputs,” but C1’s sweep input is the whole corpus at `REV`, not only its 19-target population. An absolute `PATH_RE` citation added by C2’s pointer can introduce a new miss or unannotated drift and make C1 fail. Conversely, the exact C2 documentation prompt currently asks for the relative command `python3 scripts/receipt_replay.py ...`; that `.py` relative path is outside the current path scanner’s gated path grammar, so I found no evidence that the prescribed C2 text itself changes the gate. This is a coupling risk, not an observed cross-claim pass.

**Could one claim make the other pass?** Under the prescribed work, C1 cannot satisfy C2’s malformed-case matrix: the matrix prompt resets each case to `fixtureBase=f7de3ab4e9f030a15a857a5a08631bd8e690f436` and changes one receipt field, while selecting the replay implementation from `REV` (`w1-spec.json:258`). C2 also cannot supply C1’s 19 receipts, filesystem observations, sidecar annotations, or pin update. But the C1 verdict can still change when C2 edits a scanned Markdown file, so the asserted “without the others having landed” property is not proven from the ownership sentence alone.

**Smallest safe correction / falsifier.** Add a C1 counterfactual invariant: run the archived paths sweep on a C1-only revision and on the combined revision, and compare exit plus `drift`, `setDelta.newMissing`, and `setDelta.recovered`. State that C2-owned documentation must not introduce or reclassify any gated path token. Falsify separability by adding a deliberately nonexistent absolute path to the C2 knowledge pointer in a throwaway revision and observing whether C1’s sweep changes; this is a sensitivity test, not a proposed production edit. Also compare the C2 matrix on C2-only and combined revisions with identical frozen case digest and runner bytes; any outcome change attributable only to C1 edits falsifies the other direction.

### P2 — C2’s required string-only media-type rule rejects a producer-legal absence

**Evidence / exact inspected output.** `scripts/live_snapshot.py:77-85,97-100` initializes `content_type` to `None`, reads the HTTP `Content-Type` header (which may be absent), stores that value in `fetch.json`, and classifies the response with `served()`. Its re-audit check at `:172-173` explicitly accepts `contentType` as “a string or null.” Both `live_snapshot.py:67-69` and round-23 `measure_c2.py:36-39` map a falsey/missing content type to `""`, which is not served. The C2 port prompt at `w1-spec.json:250` instead requires `contentType` to be a string and says a non-string is “recorded as a problem.”

A one-field mutation of a valid non-served response to `contentType: null` is therefore a static counterexample [INFERENCE; not executed]: the existing producer’s schema allows it, and the old replay’s not-served path does not need to parse it; the proposed new rule would turn it into a replay problem. The existing 12 round-23 fetch receipts I inspected all have string `contentType` values, including the HTTP 404 controls, so the stated 12/12 unmodified-control count does not cover this producer-legal case.

**Impacted claim/axis.** C2 / operability: a replay can reject a valid receipt produced by the lane’s own snapshot tool when the response has no `Content-Type` header. This is a regression risk separate from rejecting non-string values such as a truthy integer or array.

**Smallest safe correction / falsifier.** Specify `contentType` as `string | null`; permit `null` only for the existing not-served/no-page path, and reject other non-string values and malformed media types. Add a C2 `expect: accept` control that changes a valid 404 fixture’s content type to `null`, plus reject controls for a truthy integer and a non-string array on a 2xx response. The old runner should accept the null control and the new runner should preserve that result while rejecting the malformed controls.

### P2 — The “before” runner is authentic, but its malformed-case denominator is not frozen here

**Evidence / exact inspected output.** `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD && git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --short` returned:

```text
f7de3ab4e9f030a15a857a5a08631bd8e690f436
?? .ufo/waves/round-24/
```

A read of `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/c2-population.json` returned exactly:

```text
Path '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/c2-population.json' not found
```

The round-24 directory listing contains `c1-population.json`, `paths-before.json`, and `contract.json`, but no `c2-population.json` or round-24 counters. Meanwhile contract line 26 calls the C2 population “frozen”; line 27 only says the old runner rejects “some” malformed cases. The executor spec at `w1-spec.json:258` still calls for a *provisional* population with “at least 6 cases” and a digest placeholder for L1 to fill. Those are not the same as a case list and digest frozen by this contract.

The baseline executable is the right historical instrument, not an invented strawman. At `round-23/measure_c1.py:55-56` and `measure_c2.py:56-57`, timestamps are compared only by a 10-character lexical prefix; at `measure_c2.py:36-39`, a truthy non-string `contentType` reaches `.split()` and can raise. These are the actual files the round-23 lesson identifies as the counters. But the contract’s qualitative “only some” claim is not yet an auditable before measurement without a fixed denominator and per-case results. The `17/17` and `12/12` values in C2’s after clause are unmodified acceptance controls, not counts of malformed cases rejected before versus after.

**Impacted claim/axis.** C2 / operability and the before→after attribution. A late-selected malformed population could make the baseline look arbitrarily weak or omit a regression; that would undermine the C2 measure, not invalidate the round-23 runner as a baseline.

**Smallest safe correction / falsifier.** Freeze and digest-pin the complete C2 case list before judging the implementation. For every case, record the actual round-23 result from a disposable clone at `f7de3ab4e9f030a15a857a5a08631bd8e690f436`, with the one-field mutation, exact exit, traceback flag, and stdout tail; then apply those same cases to the new runner. Keep unmodified C1/C2 controls and the producer-legal null control. The baseline is falsified as a fair comparator if a case is not a one-field mutation of a valid frozen receipt, if the old runner’s observed behavior is not recorded, or if controls do not stay accepted.

## Checked and held

- Read `contract.json`, the round-24 task specification and C1/C2 counter prompts, the round-23 replay scripts and lesson, the path-sweep scanner, the producer schema, the C2 fetch fixtures, `AXES.md`, and `SCORECARD.md`.
- Axis assignment is semantically coherent: `AXES.md:13-14` defines operability as runnable artifacts and freshness as drift detection; the round-24 contract assigns C2 to operability and C1 to freshness. `AXES.md:31-32` still requires the claims to be causally separable, not just differently named.
- No build, test, counter, mutation case, or runtime was executed. In particular, `r23Observed` outputs are not claimed here; the falsifiers above remain unrun.

## Limits

This is a static critique of the frozen contract and currently visible round-24 build tree. The proposed C2 documentation may ultimately contain only relative references and leave the paths sweep unchanged; no actual C2 landing was available to compare. The null-content-type case is reasoned from the producer/replay code and is explicitly marked unexecuted. I did not assess admission or make changes outside this report.
