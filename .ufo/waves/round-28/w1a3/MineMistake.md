# Round 28 wave 1a3 — MineMistake (leaf seat, operability/freshness)

Seat: `KakeR28a3.MineMistake`. Task: mine one mistake row for `corpus/lessons/round-28.md` `## Mistakes`, drawn from the two consecutive honest stops (round 26, round 27).

## What I did

Read-only seat. Source reads (all `read` tool calls, exit 0, no shell commands):
- `corpus/lessons/round-27-verifier-spotcheck.md` (whole file)
- `corpus/lessons/round-26-verifier-spotcheck.md` (whole file)
- `corpus/lessons/round-27.md` (whole file)
- `.ufo/waves/round-27/unresolved-acceptance.json` (whole file)
- `.ufo/waves/round-28/c1_interface_count.py` (lines 1-335)
- `.ufo/waves/round-27/contract.json` (whole file)
- `agent://KakeR28a3.MutRefuseAllGate` (status probe: running, "Nothing produced yet")

No tool installed or updated (none needed). No lane file edited; only this report is written.

## Draft row (for round-28.md `## Mistakes`)

| Class | Evidence | Captured-by | Fix / fail-capable witness |
|---|---|---|---|
| proxy / false-green — counter verdict covered a finite surrogate of the after-clause, not the clause | r26: `corpus/lessons/round-26-verifier-spotcheck.md:11,13` (frozen C1 "is not merely the receipt count"; "Do not reduce C1 to 32 receipt files"); `.ufo/waves/round-27/contract.json:19` ("r26 measure exits0 on base despite16 missing expanded pairs"). r27: `.ufo/waves/round-27/unresolved-acceptance.json:24` ("Finite predicate alone admits constant16; real29 fixtures kill it"); `corpus/lessons/round-27-verifier-spotcheck.md:21` ("A constant therefore satisfies the frozen detection and fails the interface"); `corpus/lessons/round-27.md:105` (status conflation) | none in either counting implementation — the after-clause itself (`contract.json:10,20`) existed but was never wired into the counter verdict, so a green counter did not entail the claim | Counter verdict must derive from the full declared surface: K1/K2 require valid-clean input to return clean exit0, K3 requires a real omission to return failed exit1 with `unadjudicated_citing_pair`, U1-U4/A1-A7 require unusable/absent surfaces to return could-not-evaluate exit2 with `input_invalid`, K4 requires the 29-fixture selftest exit0 (`.ufo/waves/round-28/c1_interface_count.py:176-279`). Fail-capable witness: the round-28 MutRefuseAllGate mutation-tester (`KakeR28a3.MutRefuseAllGate`) mutates `scripts/citing_set.py` to refuse input; that mutant must fail K1/K2/K3 (and K4 if it breaks the fixture runner), proving the controls distinguish a dead gate from a live one — the r26/r27 counters had no such controls and could not fail on the constant or the missing-pair green |

## Rationale (two sentences)

Both honest stops share one shape: the counter's green verdict was produced by a finite proxy that did not entail the declared after-clause — round 26's receipt counter exited 0 with 16 missing expanded pairs (`contract.json:19`; `round-26-verifier-spotcheck.md:11,13`), and round 27's finite identity counter admitted a constant that returned the fixed 16 unconditionally (`unresolved-acceptance.json:24`; `round-27-verifier-spotcheck.md:21`). The class is measurement-proxy substitution (false-green survivor): the measured after-value must be the full declared surface, and the counter must fail on any uncovered part, which the round-28 counter enforces via K1-K3 controls (`c1_interface_count.py:247-258`), U/A defect cases (`:176-245`), and the K4 selftest (`:262-279`), with the MutRefuseAllGate refuse-mutant as the fail-capable witness.

## What I did not verify

- I did not run `c1_interface_count.py` or any counter/gate (leaf seat, read-only; no counter run is my assignment).
- `KakeR28a3.MutRefuseAllGate` had published no output at write time; the fix's fail-capability points to the seat by assignment, not by an observed mutant result.
- No source file was changed; the row is advisory input for the L1 integration into `round-28.md`.

Report: `.ufo/waves/round-28/w1a3/MineMistake.md`
