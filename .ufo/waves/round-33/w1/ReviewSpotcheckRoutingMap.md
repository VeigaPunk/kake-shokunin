# ReviewSpotcheckRoutingMap — round-32 routed defects vs round-33 plan

Seat: KakeR33.ReviewSpotcheckRoutingMap (reviewer, wave 1). Base of the routed
list: `corpus/lessons/round-32-verifier-spotcheck.md` "Routed defects" (7 items,
checked at lane tip bc6c4a8). Plan sources: SCORECARD.md "Round 33 — declared
claims" (SCORECARD.md:1091-1120) and the 35 seat names/tasks in
`.ufo/waves/round-33/w1-dispatch.json` taskCall.tasks.
Round prompt §6.5 dispositions: fixed / lesson-backed QUALITY criterion /
explained.

## Seven-row routing table

| # | Routed defect | Handler (claim / wave item / none) | Gap |
|---|---|---|---|
| 1 | Git-pin mutants m3d, m3f, m3g survive the hostile selftest | Explained, not fixed: declaration discloses exclusion (SCORECARD.md:1116-1118, "handled outside the claims this round, see the round-33 lesson"); wave item ExecPinMutantsP7 probes whether a spec (P7) in the committed setup vocabulary can kill them | Explanation text is owed to the round-33 lesson but no seat is assigned to write it (L1 by default). If the vocabulary cannot express a kill, the item stays open into round 34. Declaration originally named m3d/m3f; m3g also covered by ExecPinMutantsP7 — good. |
| 2 | C1 kill keys on message text; a reworded guard message fails P6 on a correct runner | Claim C1: `reason_code` spec key + `setup_commit_before_init` code literal (SCORECARD.md:1109,1112-1116); ScribeRefusalCodeCriterion drafts the QUALITY criterion; CriticC1RepairScope bounds the repair | C1 repairs spec P6 only. Other hostile specs still use `reason_contains` (P3 etc.); residual is delegated to CriticC1RepairScope's findings, not fixed this round. Criterion is a draft until the L1 integrates it. |
| 3 | Probe `killed` not gated on `guard_ok`; timeout raises instead of returning a verdict | Claim C1 counter `.ufo/waves/round-33/c1_code_probe.py` (report contract requires `guard_ok` field; ReviewC1ProbeCode verifies both defects are fixed; MutC1ProbeVariants checks variant construction) | The repair lives in the new probe, not the round-32 `c1_m3_probe.py` — correct since counters are frozen. Unproven until ReviewC1ProbeCode lands; watch for a timeout path that still raises. |
| 4 | Round-32 C2 counter has seven defects; a hollow commit scores 3 | Claim C2 ships replacement counter `.ufo/waves/round-33/c2_pin_count.py` designed against the defect classes (row S065 pinned, path+mode blob check, section-anchored cite, counter re-derives numbers); ReviewC2CounterCode checks each defect fixed/still-present; MutC2HollowCommit attacks with hollow commits | Old counter is unrepaired by design (frozen evidence); risk only if anyone reuses it as a gate — flag if a caller survives. New counter's soundness is pending the review/mutation seats; no handler needed beyond them. |
| 5 | PROVINCE.md:122 "five hostile fixture shapes"; six exist after P6 | ScribeProvinceReadme drafts the append-only correction (+round-33 PROVINCE/README notes) | Confirmed stale at base: PROVINCE.md:122 says five; `scripts/fixtures/citing-set-hostile/` has P1–P6 (six dirs). Handler is draft-only; landing depends on L1 integration. ScoutProvinceLiveFetchWording covers round-31 F1/F2 wording, not this line — no overlap. |
| 6 | Concurrent `citing_set.py --selftest` runs collide on fixed scratch default | ExecScratchDefaultUnique (per-run mkdtemp patch for the runner); ExecHostileScratchCollision (checks the hostile selftest half); RevengerScratchDefaultIntent (checks whether the fixed default was intentional) | Item only named the benign suite; the wave widened it to the hostile selftest — good. All output is clone-side; integration pending. Intent check guards against breaking a documented use. |
| 7 | Round-31 item-3 lows still open: read_expected OSError escape; silent skip of non-dir fixture-root entries; duplicated option tables | ExecReadExpectedOSError; ExecFixtureRootStrayEntries; ExecDuplicatedOptionTables — one executor per sub-item | All three sub-defects have dedicated seats. Duplicated-option-tables seat may conclude "cannot unify without behaviour change" — that is an accepted explain outcome, not a miss. |

## Items with no handler

None. Every routed item maps to at least one seat or a declared explanation.
Weakest coverage: item 1 (explanation has no named writer) and item 5
(draft-only scribe; no second seat verifies the correction landed).

## Commands run (all exit 0)

- `read corpus/lessons/round-32-verifier-spotcheck.md` — 7 routed items at §"Routed defects".
- `read SCORECARD.md:1090-1160` — declaration, C1 contract, disclosed limits.
- `python3 -c <json dump of w1-dispatch.json taskCall.tasks>` — 35 seats, Target/Change text extracted (output truncated to 400 chars each; full texts in the file).
- `read PROVINCE.md:116-135` — line 122 "five hostile fixture shapes" confirmed.
- `ls scripts/fixtures/citing-set-hostile/` — P1–P6, six directories.
- `git log --oneline -3 -- PROVINCE.md` — read-only; last touched round-31.

## Not verified

- Whether any seat's patch/draft actually lands (L1 integration is in flight during this wave).
- Whether c1_code_probe.py/c2_pin_count.py are internally correct — that is ReviewC1ProbeCode/ReviewC2CounterCode's seat, not mine.
- Seat-name fidelity to assignment is assumed from task text at dispatch time; a seat that returns nothing leaves its row's handler nominal only.

Tooling: none installed. Reads only; no clone needed for this mapping.
