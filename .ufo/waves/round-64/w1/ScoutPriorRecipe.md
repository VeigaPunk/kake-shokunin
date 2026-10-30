# ScoutPriorRecipe — round-63 repair recipe mapped onto round-64 code

Seat: ScoutPriorRecipe (scout, leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`
(read-only; no git mutation; no lane file written). Measured T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`;
base `1a48131577ba82c967650561be34e8dba909432a`. Scratch `/fast/scratch/hyaku/kake-r64/ScoutPriorRecipe/`
(deleted before yield). Tools installed: none (python3 + git only).

## Verdict (one paragraph)

Every clause of the round-63 routed recipe has committed code, and the T0 greens reproduce. Three clauses
are **not** fully implemented as routed: (1) the spot-check verdict is bound to the lesson Gate only,
never to the spot-check file's actual verdict line, so the outside verdict can be rewritten and C1 still
prints `met=true`; (2) the C2 JSON guard misses the `by_id` build (unhashable `id` still tracebacks;
unreachable with the sha-pinned frozen tool, defense-in-depth gap only); (3) the prose components are
substring checks scoped to a block, not semantic checks. Attack (1) reproduces a digest-consistent green
on a tree whose pins all match; under the C1 kill-rule wording ("any wave attack reproduces a …
digest-consistent-fabrication green") that is a kill-rule hit. Verdict is the lead's to rule; I report
the reproduction.

## Clause map

| # | Routed clause (source) | Code (line numbers as in files) | Status | Evidence |
|---|---|---|---|---|
| 1 | Pin ledger + both blob shas as constants (round-63 lesson §Routed item 1) | `c64_calibration.py` 66–69 (RAW/TEXT/LEDGER/RECIPE_SHA), 90–95 (PIN_SHAS), 200 (blob reads at rev), 206–214 (drift/absent → `pins`), 221 (pins gate the ledger parse, recipe exec, class) | implemented | T0 `pins=1 pin_drift=none`; base same |
| 2 | Re-execute `extract_text.py` in-counter (kills circular text blob) | 122–131 `load_recipe` (recipe blob from rev, never worktree), 225–231 exec + output must equal pinned text bytes and TEXT_SHA, 229 `recipe_rederive=1` | implemented | T0 `recipe_rederive=1`; marker/fab fixtures `recipe_rederive=1` with real blobs (correct: the real recipe reproduces) |
| 3 | Gate disagreements/unresolved without masking | 267 `unresolved = max(disagreements - (1 if lesson_gate else 0), 0)`, 268–270 `met` requires `disagreements>=1 and unresolved==0`. Contrast c63 165 `unresolved = disagreements if not resolved else 0` (masks) | implemented (count arithmetic, see gap B) | 2-disagree fixture: c64 `unresolved=1 met=false` (exit 1); c63 same tree `met=true` exit 0 |
| 4 | Wire frozen shas into kill rules (contract §C1/§C2) | Contract C1 kill rule (`contract.md` 56–63: "any pinned sha differs ⇒ unprovable") enforced by 208/221; C2 kill rule (`contract.md` 81–84) enforced by 153–157 | implemented | T0 runs; stub control `tool_sha=mismatch` |
| 5a | Bind prose components block-level — `quote_correction` | 157–160 `correction_block`, 248 (frozen quote + ledger path inside the `[r63-correction` block) | implemented, substring-in-block | fabrication/marker controls `quote_correction=0` |
| 5b | — `criterion` | 151–155 `section`, 249–251 (CRITERION_SENTENCE + 3 PURPOSE_TERMS inside `## Round-62 criteria`) | implemented, substring-in-block | marker `criterion=0`; T0 `criterion=1` |
| 5c | — `lesson_gate` (lesson Gate must quote the spot-check's actual verdict line) | 252–259: `## Gate` block must contain SPOT_VERDICT_SPAN (256) — the constant, **not** the spot-check file | **partial — the spot leg is not bound** (gap A) | fx-spotdrift: verdict reason rewritten in spot file, `met=true` |
| 6 | Bind `locatedRawLines` against raw bytes (M5 survivor 6150–6156) | 163–182 `derive_located` (minimal range from pinned raw via recipe, window 6100–6200, span ≤15), 240–243 equality with ledger and EXPECTED_LOCATED | implemented; **M5 is killed by the ledger pin (207–208), not by 241** — 241 is unreachable when pins fail (221) and is a constant at fixed shas (see gap C) | ledger-mut `pins=0 pin_drift=drift:ledger located=unevaluable`; fx-ledgermut same |
| 7a | C2: guard JSON parsing | 119–127 `safe_json` (parse + not_object guarded), 190–194 (val None → token), 195–199 (`cases` not list → shape_invalid) | implemented for parse and shape | selftest fixtures (round-64 `selftest-c2.txt` 11/11) |
| 7b | — guard the case-row walk | 200 `by_id = {c.get("id"): c for c in cases if isinstance(c, dict)}` — **unguarded**: unhashable `id` raises (gap B2) | **not implemented** (defense-in-depth) | harness unhashable_id: `TypeError: cannot use 'list' as a dict key` line 200, exit 1 |
| 8 | Pin selftest fixtures to the measured revision | 159–166 (blobs read at rev, FIXTURE_RELS), 168–172 (materialize into tempdir, env restricted: PATH/HOME/TMPDIR/LANG only), 174–178 (run from materialized tree with `cwd=work`) | implemented; fixture bytes are not sha-pinned (gap D) | stub never reaches this path (sha mismatch first) |
| 9 | Define stub as "tool sha ≠ frozen sha" | 55 `FROZEN_TOOL_SHA`, 153–157 (`tool_sha=mismatch`, exit 1, before any execution) | implemented | `stub-c64.txt` reproduced; my fixture `stub-repo` 5dcb2988: `tool_sha=mismatch met=false` exit 1; c63 on same stub `met=true` exit 0 (defect reproduced) |

Also present, not a routed clause: C1 selftest (`c64_calibration.py` 327–425) uses BASE blobs, not the
measured revision (counter-internal, acceptable); C1 class is inlined (113–119), never gated on
`scripts/quote_class.py`, preserving separability.

## Gaps (named, with reproductions)

### Gap A — spot-check verdict is not bound to the spot-check file (clause 5c). NOT implemented.
The counter reads the spot-check file only to count S432/Disagree lines (`c64_calibration.py` 197–198).
The verdict span is compared only against the lesson Gate block (256). Nothing checks that the spot-check
row still carries that span. The spot file is not in PIN_SHAS.

Reproduction 1 (reason rewritten, every pin still matches):
```
$ python3 mutate_spot.py corpus/lessons/round-61-verifier-spotcheck.md drift
  # replaces "is only a generic lead-in, not substantive evidence for a response-header expectation"
  # with "is a generic lead-in and nothing more, per the review"
$ grep -c "is only a generic lead-in, not substantive evidence" fx-spotdrift/corpus/lessons/round-61-verifier-spotcheck.md
0
$ grep -c "is only a generic lead-in, not substantive evidence" fx-spotdrift/corpus/lessons/round-64.md
1
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root fx-spotdrift --revision 9ffee64940b526fa2fb96454421a4681bb0e718e
revision=9ffee649… disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```
Reproduction 2 (whole S432 row replaced with a fabricated Reject/Disagree row):
```
| S432 / Fetch | Reject | (fabricated row) | Disagree | no lead-in language at all |
revision=6cf433a8… disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ... class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```
Consequence: the lesson quotes an outside verdict that the committed spot-check no longer says, and C1
prints `met=true`. The spot-check file is an unpinned committed artifact, so the change is not caught.

Fix (for the round that repairs it, not me): pin the spot-check file's sha, or require the verdict span
(with `Disagree`) on the S432 row of the spot-check file (`in` check on the same line), and bind
`disagreements` to that identified row, not to any S432+Disagree line.

### Gap B — unresolved is arithmetic, not identity (clause 3). Partial.
`c64_calibration.py` 267: `unresolved = max(disagreements - (1 if lesson_gate else 0), 0)`. One boolean
"resolves" exactly one disagreement, whichever row it is. The two-disagreement case is gated correctly
(verified: c64 `unresolved=1 met=false`), so masking is gone. But combined with gap A, the single counted
row can be any S432/Disagree line. Reproduction (2 S432/Disagree lines, c64 vs c63):
```
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root fx-2disagree --revision 43caa312…
revision=43caa312… disagreements=2 pins=1 ... unresolved=1 met=false
exit=1
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root fx-2disagree --revision 43caa312…
revision=43caa312… disagreements=2 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```
c63's `unresolved = disagreements if not resolved else 0` (c63_calibration.py 165) is the masking shape
the routed defect named; c64 line 267 fixes it.

### Gap B2 — C2 case-row walk unguarded (clause 7b). Not implemented.
`c64_quote_tool.py` 200 builds `by_id` with `c.get("id")` as the dict key. An unhashable id raises
`TypeError` out of `evaluate` (traceback, exit 1 — not a `met=false` report). Reproduced with a harness
that replaces only the selftest stdout (git calls pass through; the real frozen tool sha is at T0):
```
$ python3 -B harness_c2_json.py <lane> 4c8295fa… unhashable_id
  File ".../c64_quote_tool.py", line 200, in evaluate
    by_id = {c.get("id"): c for c in cases if isinstance(c, dict)}
TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
```
Other hostile shapes were handled: a non-dict case list (`cases: [5,"s",None]`) prints `frozen_cases=missing met=false` exit 1; `ok: 1` prints `met=false` exit 1; a non-list `cases` prints `shape_invalid` (line 196–199).
Reachability: the frozen tool (sha-pinned at 153–157) cannot emit hostile JSON, so production does not reach 200 with adversarial output. This is a defense-in-depth gap, not a false green. Fix: validate `id` is `str` before keying, or key only dict rows with string ids.

### Gap C — M5 is killed by the pin, not the located re-derivation (clause 6). Partial.
With the ledger pinned (207–208), `pins=0` gates off the located derivation (221). In the ledger-mutation
fixture the kill is `pin_drift=drift:ledger`, and `located=unevaluable`. At fixed shas, `derive_located`
(163–182) is a deterministic constant `6150-6154`, so 241 can only fail if the pin is also gone. The M5
survivor is therefore dead, but by the sha pin. The located-range derivation adds no independent kill under
the frozen pins. Acceptable as belt-and-braces; not evidence that located lines are bound independently.
Reproduction (fx-ledgermut: `locatedRawLines` 6150-6154 → 6150-6156, committed):
```
revision=f09e9ba9… disagreements=1 pins=0 pin_drift=drift:ledger recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
exit=1
```

### Gap D — C2 selftest fixture bytes are revision-pinned, not sha-pinned (clause 8). Partial.
`c64_quote_tool.py` 159–166 reads the four fixture blobs and the two S432 blobs at the revision; none
is sha-pinned. The only guards are the frozen expected classes (`FROZEN_CASES`, 65–94) and the rederive
check (209–220). A revision whose fixtures change so that the frozen expected class still holds is not
caught. Not reachable as a false green on the C2 predicate (`tool_sha` pins the tool), so this is noted,
not counted as a kill.

### Clauses judged NOT implemented in full
- Gap A (spot-verdict identity) — not implemented as routed (round-63 routed defect 1: "the lesson Gate must quote the spot-check's actual verdict line").
- Gap B2 (C2 case-row guard) — not implemented as routed (round-63 routed defect 2: "guard the counter's JSON parsing"; guard present for parse/shape, missing for keying).
- Prose components (`criterion`, `quote_correction`, `lesson_gate`) are block-scoped substring checks, not semantic checks. This is what the routed text asked ("block-level evidence"), so I count it implemented-as-specified, with the caveat that a block can contain any copied string.

## Attacks run and results

| Attack | Target | Result |
|---|---|---|
| Re-run T0 c64_calibration + c64_quote_tool; base C1 | Clause 1–9 | green at T0 (exit 0 each); base `met=false` exit 1 |
| Rebuild the 4 fixtures with `build_fixtures.py <scratch> --lane <lane>` | Controls | stub `5dcb2988`, marker `501b7904`, fabrication `a303380f`, junk `c621e8e0`; all as committed (stub mismatch; marker/fab `met=false`, junk `pins=0`) |
| Stub differential | Clause 9 | c64 `tool_sha=mismatch met=false` exit 1; c63 `met=true` exit 0 (defect reproduced) |
| Spot-verdict reason rewritten (drift) | Gap A | **`met=true` exit 0** — kill-rule shape |
| Spot S432 row replaced by fabricated Reject/Disagree | Gap A | **`met=true` exit 0** |
| Second S432/Disagree line | Gap B | c64 `met=false` (correct); c63 `met=true` (masked) |
| ledger locatedRawLines 6150-6156 (M5) | Gap C | killed by pin, `met=false` exit 1 |
| Hostile selftest stdout, unhashable id | Gap B2 | TypeError, exit 1 (unreachable via frozen tool) |
| Hostile selftest stdout, non-dict cases / truthy ok | B2 | `met=false` exit 1 (guarded) |

Frozen sha256 re-derived at the lane tree (matches contract):
```
5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf  .ufo/waves/round-64/c64_calibration.py
96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b  .ufo/waves/round-64/c64_quote_tool.py
7fbd8cbc67c17264096e44474a698b3f0d7702c3e1cc23f0b5bdaa26ee0271d3  .ufo/waves/round-64/fixtures/build_fixtures.py
7c78a05df78703044f8fe8fa02793a63b580f6353f58e8ebcee836038762edde  .ufo/waves/round-64/fixtures/stub_tool.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
```

## Notes for the lead

- Kill-rule relevance: contract §C1 kill rule says a wave attack reproducing a "digest-consistent-fabrication green" makes C1 `unprovable`. Gap A's reproduction has all pinned shas matching and a rewritten outside verdict. That is the lead's call; I am reporting the reproduction, not ruling.
- The round-63 counter-family routed items 1–2 are otherwise covered in code. Clause-level line numbers above are the mapping asked for.
- No C3 (freshness) analysis in this seat; out of item scope.
- Installed: nothing. Written: this report only. Scratch deleted at yield.
