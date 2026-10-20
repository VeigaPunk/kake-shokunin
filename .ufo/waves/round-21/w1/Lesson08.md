# Lesson08 — round-20 gate review (round-21 wave 1)

## Result

- **Target:** `corpus/lessons/round-20.md`
- **Action:** none. The file already has an exact `## Gate` heading (line 41), so the instruction was to leave it unchanged and review gate completeness.
- **Line count:** 455 before and after. Zero lines appended.
- **Bytes:** `sha256sum` = `5f62ef0bce7492f094b8a08982087c2fad116f01a3bd96abdebd98266723a22a`. This is identical to the base blob at `5009ecaa1cce10b895617a585ddd3f7c7c923a84`. `git diff --quiet` reports the file clean.
- **Files written:** this report only.
- **Tools installed or updated:** none.
- **Verification run:** none beyond the reads, greps, and hashes listed below. No live-state re-verification.

## Gate completeness (existing gates in round-20.md)

Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 18-20 require each `lessons/round-<N>.md` to carry `## Gate` with candidates, admitted, rejected with reasons, and spot-check result. SOURCES rule 1 (lines 112-115) requires each new row's URL, access date, and a ≤25-word quote with location.

| Gate | Lines | Candidates | Admitted | Rejected | Spot-check | Assessment |
|---|---|---|---|---|---|---|
| `## Gate` (2026-10-15 citation-locality attempt) | 41-60 | yes (3 bullets) | locally admitted, with qualification | yes, with reasons | "unavailable" (line 58-60) | Complete for its date. No SOURCES rows were added in this attempt, so no row metadata is owed. |
| `## Gate — round-20 resume` | 182-196 | not a separate list | yes (4 knowledge entries, 7 QUALITY criteria, C2 checker) | S017, S018, plus named non-claims | "still owed" (lines 194-196) | Complete for its date. Superseded for spot-check by the evidence below. |

Findings:

1. **Heading mismatch.** The resume gate is `## Gate — round-20 resume`, not exact `## Gate`. An exact-heading search, which is how the round-21 wave found this file, returns only line 41. The resume gate's admissions and rejections are reachable only by heading text. This is recorded here and not repaired, because the file is a lane-owned append-only record.
2. **Row metadata.** The resume gate table lists S001-S018, and all 18 IDs match the base registry (`5009eca:corpus/SOURCES.md` has 18 `S0xx` rows). The "accessed 2026-10-19" in the table header applies to every row. Quote word counts were not checked mechanically.
3. **Status consistency.** In the working-tree `corpus/SOURCES.md`, S014 is `mined` (used-by includes `round-20.md`), S015 and S016 are `queued`, and S017 and S018 are `rejected`. This matches the gate's admitted and rejected decisions. S015 and S016 are cited in the gate but never admitted, which is consistent with `queued`.

## Outside spot-check: existing independent evidence

- **Cited:** `corpus/lessons/round-20-verifier-spotcheck.md`, added in commit `7e17c66` (17 insertions). It is an integrator-written file, as CORPUS.md requires for outside reviews.
- **Content:** admit of `crawl-scope-per-host`, where the reviewer re-opened 18 of 18 rows and agreed. Reject of S017 and S018, where the reviewer agreed. "3/3 sampled gate decisions agree." The file names fresh agents dispatched by the orchestrator, reviewer `W3ReviewKake`.
- **Scope limit:** this covers only the resume gate's decisions. It does not cover the 2026-10-15 citation-locality gate at line 41, which remains "unavailable".
- **Not opened by me:** the full reports it names, `.ufo/waves/kaika-w3/kake-review.md` and `kake-critic.md` in the fleet repo.

## S019 metadata/gate contract

- **Base:** `5009eca` has zero `S019` rows. The registry at base has 18 rows, S001-S018.
- **Working tree:** `corpus/SOURCES.md` (uncommitted, sha256 `da458be3a2cf7eb54e8baab6433bfbf194a5bcfe86ad52c288a452f32e07fb7a`) contains an S019 own-work row. It is opened 2026-10-20, tier A, status `mined`, used-by `corpus/lessons/round-21.md`.
- **Discrepancy:** S019's canonical input is cited as `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`. The main-repo contract read for this report is `/home/vgpnk/Projects/shokunin/CORPUS.md`. The two were not compared.
- **Not verified:** the S019 row and the `scripts/corpus-contract.mjs` it names. The row is a working-tree claim and was not used as evidence for any gate decision here.
- **Round-21 lesson:** `corpus/lessons/round-21.md` does not exist at base or in the working tree. It is not cited as evidence.

## Decision for main

- The assignment asked for a new `## Gate` section labelled as round-21 retrospective reconstruction. That was not appended because the exact heading already exists.
- If a round-21 retrospective gate is wanted, it must go in a new file. CORPUS.md says corrections are new entries and lanes own `round-<N>.md`. Writing it inside `round-20.md` would violate that.
- Main should decide where to place the retrospective.

## Checks for main (not run by me)

- Confirm `corpus/lessons/round-20.md` sha256 still equals `5f62ef0b…` after integration.
- Decide the retrospective location (see above).
- Reconcile the S019 anchor path with `/home/vgpnk/Projects/shokunin/CORPUS.md` once L1 commits `corpus/SOURCES.md`.
