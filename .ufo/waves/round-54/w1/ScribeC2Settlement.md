# ScribeC2Settlement — round-54 w1 finding

Scope: re-read `corpus/lessons/round-53-verifier-spotcheck.md` §Dead-seat
reconciliation and `.ufo/waves/round-53/settlement.md`; judge whether the
settlement honestly distinguishes "40 spawned / 0 committed reports" from
unverified individual seat deaths, and whether each of the seven lost names is
accounted. Findings only; no admission claim. Read-only; no product edits.

## Finding 1 — the 40/0 vs unverified-death distinction is honest

The settlement states the evidence-backed count and the unverifiable remainder
in separate sentences, and refuses to blur them:

- "40 spawned vs 0 committed seat reports is the evidence-backed settlement
  count; individual death outcomes are not recoverable and are **unverified**,
  not inferred from absent reports." (`settlement.md:6-9`)
- "No missing report was recreated or represented as an observed response."
  (`settlement.md:9-10`)
- "lost pointers, not as recovered agent transcripts" (`settlement.md:11`)
- "No report is classified `resolved`: the cited files were not recovered. The
  40-seat launch happened, but the individual dead-seat count remains
  unverified. This settlement records the loss without changing prior round-53
  prose or claiming a seat transcript exists." (`settlement.md:25-28`)

This mirrors the spotcheck's own ruling — "Dead-seat count remains unverified,
consistent with the L1's own admission" (spotcheck:74) — without upgrading it.
Verified against ground truth:

- `w53-spec.json`: `items` length 40, `maxLanes` 40, role mix
  `scout 14, connector 1, executor 3, scribe 6, reviewer 8, critic 8` —
  matches the settlement's declared mix exactly (re-derived, not copied).
- `.ufo/waves/round-53/w1/` is absent from the working tree (confirmed);
  spotcheck:72 records it absent from the committed tree at fleet HEAD.
- The frozen counter's loss-basis check
  (`c54_ops_debt.py` `has_loss_basis`: `40\s+spawned` and
  `0\s+(?:committed\s+)?seat reports`) matches settlement text at spans
  (121,131) and (353,377).

No dishonesty found in the distinction: it does not call absent reports
"deaths", does not fabricate transcripts, and classifies nothing `resolved`.

## Finding 2 — all seven lost names are accounted

The settlement table rows are exactly the spotcheck's enumerated loss list
(spotcheck:73) and the counter's `REQUIRED_SEAT_NAMES`
(`c54_ops_debt.py:23-26`):

| Name | Settlement row | Spotcheck list | Cited in `round-53.md` | Seat in `w53-spec.json` |
|---|---|---|---|---|
| `ReviewerProvenance.md` | lost | yes | line 11 (`w1/` path) | yes |
| `CriticCrossLane.md` | lost | yes | line 11 (`w1/` path) | yes |
| `ScoutS329.md` | lost | yes | line 13 (bare, no `.md`) | yes |
| `ScoutS312.md` | lost | yes | line 13 (bare, no `.md`) | yes |
| `CriticLocators.md` | lost | yes | line 13 (bare, no `.md`) | yes |
| `ScribeGate.md` | lost | yes | line 15 (bare, no path) | yes |
| `ScoutQuarantine.md` | lost | yes | line 29 (`w1/` path) | yes |

All seven are literal seat `name` values in the spec, so the cited filenames
are `<seat>.md` under `reportDir: .ufo/waves/round-53/w1`; with `w1/` absent,
each pointer is unresolvable and `lost` is the correct disposition. Every row
carries a reason ("non-author census found no committed `w1/` report or
lane-tree copy"). No `resolved` rows exist.

Coverage caveat observed (consistent with contract, worth noting): the frozen
counter's `NAME_RE` requires the literal prefix `.ufo/waves/round-53/w1/` in
cited bytes, so only 4 names are machine-extractable from lesson+spotcheck
(committed base receipt `controls/base-c2-ops-debt.txt` prints `uncovered=4`
listing exactly CriticCrossLane/ReviewerProvenance/ScoutQuarantine/ScoutS329 —
the names appearing with the full path in `round-53.md`). The other three names
are covered by the counter's hard-coded `REQUIRED_SEAT_NAMES` set instead. The
settlement satisfies the stricter requirement: all seven cited names appear in
its manifest rows.

## Minor nits (non-blocking, no dishonesty)

- Every row's reason says "Cited by round-53 lesson"; three of the seven are
  cited there bare (no `w1/` prefix or `.md` suffix). The full-path citations
  live in the spotcheck. The reason remains factually true.
- The settlement settles only the seven cited pointers, not all 40 seats; the
  other 33 seats' outcomes are left in the "unverified" bucket. This is exactly
  what the contract P2.3 requires and what the honest-distinction finding
  implies — it would be fabrication to name 33 more `lost` rows as confirmed
  deaths.
- Spotcheck:72 says "17 committed files under round-53 waves"; at settlement
  time the tree holds 17 committed files plus `settlement.md` itself (the 18th
  file, added round 54). No conflict — the spotcheck predates the settlement.

## Out of scope

- SKILL.md registry-row half of claim C2 (P2.1) — separate review seat.
- C1 S374 calibration — separate claim, not touched.
- Judgment of `resolved`/`lost` correctness is lane-evidence-based only; no
  seat transcripts were sought outside the lane repo (none should exist — the
  spec's seats never committed).

## Tools

None installed or updated. Read-only commands only: `ls`, `find`, `grep`,
`python3` (JSON spec parse, regex checks). No writes except this report.

## Evidence

- `.ufo/waves/round-53/settlement.md` (28 lines, read at working tree)
- `corpus/lessons/round-53-verifier-spotcheck.md` §§Conformance, Dead-seat
  reconciliation, Routed defects 1-2
- `corpus/lessons/round-53.md` lines 11, 13, 15, 29 (seven seat citations)
- `.ufo/waves/round-53/w53-spec.json` (items len 40; reportDir
  `.ufo/waves/round-53/w1`; role mix re-derived)
- `.ufo/waves/round-54/c54_ops_debt.py` (NAME_RE, MANIFEST_RE,
  REQUIRED_SEAT_NAMES, has_loss_basis)
- `.ufo/waves/round-54/controls/base-c2-ops-debt.txt` (`uncovered=4` receipt)
- `.ufo/waves/round-54/contract.md` claim C2 (P2.1-P2.3)

Verdict: the settlement honestly separates the evidence-backed 40-spawned /
0-committed count from unverified individual deaths, and all seven cited lost
report names are enumerated as `lost` with reasons — matching the spotcheck's
reconciliation and the frozen predicate without over-claim.
