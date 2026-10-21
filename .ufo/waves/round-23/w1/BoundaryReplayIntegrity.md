## Verdict

**PASS for the requested historical replay controls; HOLD for any current-tip claim based on that replay.** The b539cc1 archive replays its frozen oracle and rejects a changed digest-pinned input. The same replay does not evaluate the 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc validator: it stops at input verification with `could-not-evaluate`. This is an author-side recommendation, not independent admission.

## Findings

### P2 — Round-22 replay cannot establish current-tip validator behavior (operability)

**Exact commands and observations** (run from temporary Git archives under `/tmp/kake-r23-BoundaryReplayIntegrity-lcvgyn4w`; archive commits were `b539cc17c25e5f42fe8803e2aa42b4574c4b44c6` and `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`):

1. Positive control, unmodified b539cc1 tree:

```text
/usr/bin/python /tmp/kake-r23-BoundaryReplayIntegrity-lcvgyn4w/b539cc1/.ufo/waves/round-22/replay.py --root /tmp/kake-r23-BoundaryReplayIntegrity-lcvgyn4w/b539cc1
exit: 0
stdout (faithfully abbreviated; the `actual.results` 32-row array is omitted):
{
  "verdict": "clean",
  "id": "frozen_replay_match",
  "inputsVerified": 69,
  "casesCompared": 32,
  "perCaseMismatches": [],
  "expected": {"exit": 0, "accepted": 32, "total": 32},
  "actualExit": 0,
  "actual": {"selection": "all", "accepted": 32, "total": 32, "executed": 32, "discrepancies": 0, "toolMissing": false, "results": [omitted]},
  "stderr": ""
}
```

2. Negative control, same b539cc1 archive copied to `/tmp/.../b539cc1_tampered`, with one newline byte appended only to `.ufo/waves/round-22/cases.json`:

```text
/usr/bin/python /tmp/kake-r23-BoundaryReplayIntegrity-lcvgyn4w/b539cc1_tampered/.ufo/waves/round-22/replay.py --root /tmp/kake-r23-BoundaryReplayIntegrity-lcvgyn4w/b539cc1_tampered
exit: 2
stdout: {"verdict": "could-not-evaluate", "id": "snapshot_tampered", "error": "snapshot member digest mismatch"}
stderr: (empty)
```

3. Current-tip applicability probe, unmodified 4d95d2e9 archive:

```text
/usr/bin/python /tmp/kake-r23-BoundaryReplayIntegrity-lcvgyn4w/tip-4d95d2e9/.ufo/waves/round-22/replay.py --root /tmp/kake-r23-BoundaryReplayIntegrity-lcvgyn4w/tip-4d95d2e9
exit: 2
stdout: {"verdict": "could-not-evaluate", "id": "snapshot_tampered", "error": "snapshot member digest mismatch"}
stderr: (empty)
```

The exact pinned validator SHA-256 in `.ufo/waves/round-22/frozen/expected.json` is `5de32200ea409349659180ab93d02d273c113008596d93834da94ef1c04a1c15`; the b539cc1 archive has that digest. The candidate-tip `scripts/canonical_audit.py` digest is `d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac`. `replay.py` verifies all pinned input digests before it invokes `matrix.py`, so the tip run exits before executing the matrix. The tip output's `snapshot_tampered` identifier reports a pinned-input digest mismatch here; it is not evidence of malicious tampering, a clean result, or a semantic audit failure.

**Impact / claim:** the historical replay proves that the 69 pinned b539cc1 inputs match their recorded digests and that the 32 historical matrix cases match the frozen per-case oracle and aggregate. It proves no behavior of the changed 4d95d2e9 validator. In particular, its top-level `verdict: clean` means *frozen replay matched*, not that every case is parser-clean: its `missing_head` row is `status=PASS`, `actualExit=2`, `actualFindings=["html_unsupported"]`, as expected by that oracle.

As a separate current-tip check, the public CLI `/usr/bin/python /tmp/kake-r23-BoundaryReplayIntegrity-lcvgyn4w/tip-4d95d2e9/scripts/canonical_audit.py --selftest` returned exit `0`, empty stderr, and `{"caseCount":70,"failedCount":0,"passed":true,"tool":"canonical_audit.py"}`. Selected exact records were:

```text
body_svg_after_head={"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"body_svg_after_head","ok":true}
body_math_after_head={"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"body_math_after_head","ok":true}
body_void_selfclose={"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"body_void_selfclose","ok":true}
body_svg_selfclose_link={"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"body_svg_selfclose_link","ok":true}
head_svg={"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"head_svg","ok":true}
body_nonvoid_selfclose={"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"body_nonvoid_selfclose","ok":true}
```

This selftest is separate evidence for those current-tip CLI cases, not evidence supplied by the round-22 replay and not a substitute for a versioned current-tip frozen replay.

**Smallest fix:** keep the round-22 replay and its b539cc1 oracle immutable and clearly labeled historical. If round-23 acceptance needs replay-based evidence for the changed validator, add a separately versioned current-tip oracle/replay with the candidate digest and explicit changed-behavior plus unsupported-boundary cases; do not treat this historical replay's exit 2 as a pass.

## Checked and held

- Read `replay.py`, the frozen input digest manifest, the matrix runner, and the validator diff between b539cc1 and 4d95d2e9.
- Executed the b539cc1 positive control and digest-tamper negative control through the public replay CLI; executed the current-tip applicability probe and the candidate's named `--selftest` through public CLIs.
- Confirmed the candidate selftest distinguishes supported body SVG/MathML and self-closed void-tag inputs (exit 0, no finding) from unsupported SVG/MathML placement/link cases and non-void self-closing markup (exit 2, `html_unsupported`).
- No lane production file was changed; only this report was written. No tools were installed, and no publishing/network actions were taken.

## Limits

This assignment establishes replay and local CLI behavior only; it does not establish live web freshness or round-23 C1/C2 acceptance. No `lsp` device was exposed in the available tool routes, so caller/definition/diagnostics checks were unavailable; no grep output is presented as semantic proof. No build, lint, formatter, or broader test suite was run.