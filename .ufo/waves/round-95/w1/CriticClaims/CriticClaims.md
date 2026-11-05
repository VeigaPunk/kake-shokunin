# CriticClaims — round-95 seat report

Verdict line: `CLAIMS C1=falsified-as-declared C2=gaming-route-found:memorizing-candidate-passes-met`

Path note: the seat spec named `.ufo/waves/round-95/w1/CriticClaims.md`; the hard bounds confine writes to
`w1/CriticClaims/`, so the report lives here, with `verdicts.md` and flat receipts beside it.

## Findings

1. **Instrument drift in the lane worktree (integrity, urgent).** The uncommitted `c95_selfassess.py` and
   `frozen/c1-surfaces.json` were rewritten at 13:35 -0300 (sha 04be4a7d…, 9eff04c5…). The drift removes the
   knowledge-entry head-8 content identity (82 pins) and rewrites `controls/base-c1.txt` line 1 to the drifted
   digest. Committed bytes (8fd27d…, 00a04c9a…) are the only valid basis. Main was notified and relayed to KakeR95.
   Restore committed bytes before any integration.
2. **Do-nothing controls reproduce** at the freeze tree: C1 `mismatches=18 … met=false` rc 1; C2 `hand=57/66
   generated=79/120 … met=false` rc 1.
3. **C1 is unreachable as declared.** The frozen counter content-pins each of the three E3 entries' head-8 lines.
   Every E3 defect sits in those lines, so the declared in-place repairs fail `entry-content` identity (H2, X8).
   The append-guard row (`scripts/append_guard.py`) also rejects in-place edits as `changed` (H2 rc 1). The best
   reachable state under the frozen counter is mismatches=3 (E3), `met=false`. Mismatches=0 with `met=true` appears
   only with the drifted instrument (D-H2, D-X8 rc 0). The freeze's "13 directory rows" is 15 rows / 15 E5.
4. **C1 gaming routes, each refused or admitted as noted:** X0 de-backtick → identity refusal (rc 1, 100
   path-token refusals); X1 prose → identity (rc 1); X2 drop rows → `pins=short` + 15 identity (rc 1);
   X2 with lowered `--base-pins-json` → identity (rc 1); X3 canned wrapper → rc 0 with `met=true`, true digest
   absent, so only a consumer-side digest check refuses it; X4 `--verdict-only` → `met=n/a` (rc 1 failed; rc 0
   `verdict=clean` on a drifted clean fixture), never `met=true`; X5 rename pinned entry → identity (rc 1);
   X7 E5 satisfied by an unrelated blob → `E5=0` admitted (rc 1 only because E3 remains).
5. **C2 gaming route found.** A lookup-table candidate memorising the 66 hand cases and the public seed-95
   120 generated cases passes the frozen counter: `hand=66/66 generated=120/120 … anti_table=ok … met=true`,
   rc 0. The anti-table gate checks digests of hand inputs only. The mutant conjunct is candidate-independent
   (40/40 for the table candidate too).
6. **C2 reachability.** The nine hand failures map exactly to C1 (×5 empty members), C2 (×2 obs-text), C3 (×1
   `role:null`), C4 (×1 duplicate keys). C5 has zero hand failures. The 41 generated failures are all C1, C2 or
   C5 (non-GET/HEAD IM/IMS edges); none needs C3 or C4. Hand 66/66 needs only C1–C4 [INFERENCE: no candidate built].
   Full met needs C5 for generated. "66/66 needs C1–C5" overstates.
7. **C2 mutant kill rule is circular as an acceptance criterion.** Nine successor cases were authored per
   surviving mutant on the same population. M11 is equivalent to the base under v1 (round-94 receipt,
   115200/115200) and is killed only because the v2 reference moved. Five kills are refusal-vs-accept on
   v2-moved semantics (M11, M19, M20, M33, M40). Against circularity: the clauses are RFC-grounded and the
   population is digest-pinned. Verdict: circular as validation.

## Changes made
None to the lane tree. All work in scratch fixtures from `git archive 8f638b59` plus clones; no mutating git on
the lane; no tool installed; no sysctl touched.

## Deliverables (this directory)
`verdicts.md` (full tables, digests, routes, verdicts) and flat receipts (`c1-*`, `c2-*`, `instrument-drift-*`).

## Checks for the L1 to run
- `sha256sum` of `.ufo/waves/round-95/c95_selfassess.py` (expect 8fd27d…) and `frozen/c1-surfaces.json` (expect 00a04c9a…); `git status` on round-95 instruments must be clean.
- `python3 -B .ufo/waves/round-95/c95_selfassess.py --root . --revision 8f638b59…` expect rc 1, `mismatches=18`.
- Do not admit C1 on the drifted instrument; C2 must be scored as gaming-route-found until the anti-table covers generated inputs.

## Scratch
Scratch tree `/fast/scratch/hyaku/kake-r95/CriticClaims/` is removed after receipts were copied here.
