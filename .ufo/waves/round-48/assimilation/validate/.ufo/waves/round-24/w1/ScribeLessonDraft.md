# Round 24 — ScribeLessonDraft (author-side, not admitted)

Seat: `KakeR24.ScribeLessonDraft` (scribe). Lane: kake, base `f7de3ab4e9f030a15a857a5a08631bd8e690f436` (lane HEAD confirmed by `git rev-parse HEAD`). Judged on: operability, freshness. Milestone: r24-build.

The draft below is for the L1 to integrate. Nothing under `corpus/lessons/` was written. Numbers that depend on the round's counters are `<TBD>`. Sources not opened by this seat are `<URL/date/quote>` placeholders.

## Verdict

Draft sections are ready for L1 integration, with `<TBD>` where a counter must run after the C1 and C2 work lands. Two operability findings are verified by probe in this seat (F1, F2 below). F2 means the round-23 contentType fix did not reach the receipt replay counter. The C2 gap item must therefore cover `measure_c2.py`'s validation path as well as `live_snapshot.py`. Nothing here is independent admission.

## Draft: `corpus/lessons/round-24.md`

### Claims

- **C1, freshness (lowest owned axis, tied at 10).** Reconcile all 19 paths-gate targets with the current filesystem. Population: `.ufo/waves/round-24/c1-population.json` (3 drift, 12 newMissing, 4 recovered; 4 unannotated drift cites). Count: `python3 .ufo/waves/round-24/measure_c1.py --root . --revision <commit>`.
- **C2, operability (lowest owned axis, tied at 10).** The maintained replay `scripts/receipt_replay.py` rejects every frozen malformed receipt with exit 1 or 2 and no traceback, and accepts every unmodified control (c1 17/17, c2 12/12 at base). Population: `.ufo/waves/round-24/c2-population.json`. Count: `python3 .ufo/waves/round-24/measure_c2.py --root . --revision <commit>`.

Causally separable: C1 touches citation lines, the paths sidecar and freshness pins; C2 touches `scripts/receipt_replay.py` and its pointer. Round-23 runners stay byte-intact. Measured numbers are in §Measurement.

### Gate

Candidates: `<TBD>` C1 targets (19 population rows, each with a receipt) and `<TBD>` C2 malformed cases (frozen from the committed round-23 receipts) plus controls.

Admitted: `<TBD>`.

Rejected (rule-level, from the contract; outcomes `<TBD>`):
- Editing non-author files (`corpus/lessons/*aggregator*.md`, `*verifier-spotcheck*.md`). Their citations take `action: sidecar`.
- Re-pinning a target without a receipt that observes the miss this round.
- Rewriting an existing citation or receipt line. Corrections are appended only.
- Counting the 4 recovered targets as drift-free without a restoration correction on lane-authored cites.

Sources opened this round:

| Row | URL | Access | Located quote |
|---|---|---|---|
| S0xx (RFC 3339 date-time) | `<URL/date/quote>` | `<date>` | `<quote>` |
| S0xx (RFC 9110 media-type) | `<URL/date/quote>` | `<date>` | `<quote>` |

Neither row is opened by this seat. The C2 contentType rule must cite RFC 9110 only after the row is opened and its quote located.

### Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| lexical timestamp prefix check accepts malformed and future-dated receipts | `.ufo/waves/round-23/measure_c1.py:55`; `.ufo/waves/round-23/measure_c2.py:56` (`x[:10] < "2026-10-21"`); probe F1 below | round-24 contract `routedFrom` (kake r23 closure) | strict RFC 3339 date-time parse in `scripts/receipt_replay.py`, reject unparseable or future values; controls stay accepted |
| receipt validator crashes on non-string `contentType` (AttributeError, exit 1, traceback) | `.ufo/waves/round-23/measure_c2.py:37`; probe F2 below | author-side, this seat (round-23 guard exists only in the producer, `scripts/live_snapshot.py:172-173`) | type guard before `served()` in `scripts/receipt_replay.py`, exit 2 with a diagnostic, no traceback |
| fix applied to the producer, not to the validator that reads the receipt | `scripts/live_snapshot.py:172-173` (guard present); `.ufo/waves/round-23/measure_c2.py:37` (no guard); round-23 lesson lines 228-245 | author-side, this seat | C2 fix covers the replay path; a case in the C2 population exercises `measure_c2`-equivalent validation, not only the producer |
| closure overclaim: "malformed metadata returns a JSON input error" was broader than the demonstrated top-level-array case | `corpus/lessons/round-23.md` lines 221-226 (errata); round-23 recovery | RecoveryDocsAudit (round 23) | scope every "rejects malformed" statement to the frozen population, not to a class |
| citation universe expanded without pin refresh; 12 newMissing targets not in `pins.pathsMissSet` | `.ufo/waves/round-24/paths-before.json` `reasons`: `"§paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet"`; round-23 lesson lines 140-143 (missSet 55→69, pins unchanged) | round-24 freshness-sweep at round open | per-target receipt observing the miss, then re-pin; no pin without a receipt |
| pinned absence went stale silently when a domain tree reappeared | `.ufo/waves/round-24/paths-before.json` (4 recovered); contract `worldChangeAtOpen` (dir birth 2026-10-21 05:19:01 -03) | round-24 freshness-sweep at round open | appended restoration correction on lane-authored cites; prior annotations kept |

### Measurement

Before (measured or read from committed evidence):
- C1: paths section exit 1, `ok: false`, `reasons` `"§paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet"` (`paths-before.json`). Receipts: 0/19. Class counts 3 drift / 12 newMissing / 4 recovered (`c1-population.json`, recounted this seat). Unannotated cites 4 (2+1+1).
- C2: round-23 replay on malformed cases: `<TBD>` rejected correctly of `<TBD>`. Probe F1/F2 (below) were run on the round-23 functions directly, not on the full population.

After:
- C1: `<TBD>` / 19 reconciled; paths exit `<TBD>`; `pins.pathsMissSet` equals observed missSet: `<TBD>`.
- C2: `<TBD>` malformed cases rejected with exit 1 or 2 and no traceback; controls `<TBD>` accepted (c1 17/17, c2 12/12 expected from base).

Both counters: `<TBD>` runs; each run's exit and stdout tail recorded by the executor, not this seat.

## Findings (this seat)

### F1 — P1 (operability, C2). Lexical timestamp check accepts malformed and future values.

Command (run in `/tmp/kake-r24-ScribeLessonDraft-MQhT`, reading the round-23 source text):

```
python3 - <<'EOF'
for ts in ["2026-10-21", "2099-01-01", "2026-10-21garbage", "2026-13-45T99:99:99Z"]:
    print(repr(ts), 'accepted by lexical prefix test:', not (ts[:10] < "2026-10-21"))
EOF
```

Exact output:

```
'2026-10-21' accepted by lexical prefix test: True
'2099-01-01' accepted by lexical prefix test: True
'2026-10-21garbage' accepted by lexical prefix test: True
'2026-13-45T99:99:99Z' accepted by lexical prefix test: True
```

Claim impacted: C2 "before" (accepts malformed or future timestamps). Smallest fix: parse observedAt/fetchedAt as RFC 3339 date-time (`<URL/date/quote>` once opened), reject a value later than the run time, and add these four strings as malformed cases with `expect: reject`.

### F2 — P1 (operability, C2). `served()` raises on non-string `contentType`; round-23 guard is in the producer only.

Command (extracted `served()` from `.ufo/waves/round-23/measure_c2.py` verbatim via `ast`, executed in the scratch dir):

```
for ct in ["text/html", 123]:
    print(repr(ct), served({"status":200,"contentType":ct,"error":None,"truncated":False}))
```

Exact output:

```
'text/html' True
123 RAISES AttributeError 'int' object has no attribute 'split'
```

Source evidence: `.ufo/waves/round-23/measure_c2.py:37` is `status, ctype = fetch.get("status"), fetch.get("contentType") or ""` with no type check. The round-23 guard is `scripts/live_snapshot.py:172-173` (`if meta.get("contentType") is not None and not isinstance(meta["contentType"], str): raise ValueError("snapshot contentType must be a string or null")`). The round-23 lesson describes the field-shape fix as covering the snapshot path (lines 228-239). The replay counter was not covered.

Claim impacted: C2 "before" (non-string contentType crashes). Smallest fix: type guard in `scripts/receipt_replay.py` before the `served()` equivalent, returning exit 2 with `snapshot contentType must be a string or null` or an equivalent diagnostic; add a case with `contentType: 123` (`expect: reject`) to the C2 population.

### F3 — P2 (freshness, C1). Paths gate red at round open; pins do not match the observed miss set.

Evidence: `.ufo/waves/round-24/paths-before.json` (`ok: false`, `code: 1`, `reasons`: `"§paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet"`). `c1-population.json` class counts recounted this seat: drift 3 (T01 `~/Projects/plazir-15-site` 19 cites / 2 unannotated; T02 `~/Projects/webzites/bin/webzites.mjs` 16 / 1; T03 `~/Projects/webzites/scripts/kimi-surface.mjs` 28 / 1), newMissing 12 (T04–T15), recovered 4 (T16–T19, all under `~/Projects/ds4cc-marketplace`). Smallest fix: one receipt per target observing its current state; annotate unannotated cites (lane-authored inline; non-author via sidecar); re-pin only observed misses.

Note: the `paths-before.json` `pins` block lists `probeRowsFloor`, `fleetTotal`, etc. It does not show the `pathsMissSet` contents in the portion read, so the 12 "not in pins" count rests on the `reasons` line. `<TBD>` until L1 confirms the missSet diff.

### F4 — P3 (lesson accuracy). Do not carry round-23's broad malformed-metadata wording into round-24.

`corpus/lessons/round-23.md` lines 221-226 already corrected "Malformed metadata returns a JSON input error" (scoped to a top-level JSON array). The round-24 Claims must name the frozen population, not a class of malformed input.

## Checked and held

- Lane HEAD = `f7de3ab4e9f030a15a857a5a08631bd8e690f436` (`git rev-parse HEAD`), matching the contract base.
- `c1-population.json` has 19 targets; class counts 3 / 12 / 4; unannotated cites 2+1+1 = 4; matches `paths-before.json`'s "3 unannotated" count.
- `.ufo/waves/round-23/measure_c1.py:55` and `measure_c2.py:56` both use the lexical prefix form (F1).
- `measure_c2.py:37` has no type guard; `live_snapshot.py:172-173` has one (F2).
- Round-23 lesson structure (`## Claims`, `## Gate`, `## Mistakes`, `## Wave-2 integration and limits`, `## Measurement`) followed for the draft.
- Round-23 counter numbers were not re-run; they are quoted from the round-23 lesson only.

## Limits

- No counter was run for round 24. The C1 and C2 "after" numbers are `<TBD>`.
- The probes in F1 and F2 ran the round-23 source text directly, not the full C2 population or a clone with a committed receipt. They show the code path behaviour, not a counter result.
- RFC 3339 and RFC 9110 were not opened by this seat. Their rows are placeholders; no quote is claimed.
- No non-author file was read for editing or changed. No lane production file, git state, or sibling output was touched.
- No subagent was spawned; this seat is a leaf.
- Scratch: `/tmp/kake-r24-ScribeLessonDraft-MQhT` (empty apart from the probe's stdout).

## Tools

None installed or updated by this seat.
