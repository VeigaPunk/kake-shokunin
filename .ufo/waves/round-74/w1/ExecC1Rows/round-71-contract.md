# Round 71 — frozen contract (kake, attempt 1)

Frozen before any seat scored data. Predicates, counters and kill rules below are fixed;
an amendment is a new numbered file, never an edit here. Base revision for every measurement:
`cc6b4e0b8c35e72dfb02c6184b847f68c1262153` (master). Counters read committed bytes only.

## Claims (2 — one per distinct axis; C1 works the lowest-scoring owned axis)

### C1 — calibration (score 2, HOLD 2 on success) — lowest owned axis

Move: the SCORECARD self-assessment statements that a committed artifact contradicts.
Counter: `python3 -B .ufo/waves/round-71/c71_calibration.py --revision <rev>`.

Predicate (one sentence, same in this file, the counter and the receipt label):
`C1 met iff mismatches == 0 and the append-only guard holds, where mismatches = stale_planned +
attack_share_mismatch.`

- stale_planned: active `## Planned` headings in SCORECARD.md naming a round < 72 (base: 2 —
  line 21 names round 21 in its body, line 3990 is `## Planned — round 48`).
- attack_share_mismatch: the stated `attack share K/N` (base: 4/14, line 4770, round-70 block)
  differs from the strict count over `.ufo/waves/round-70/w1-results.json` (agent in reviewer,
  critic, mutation-tester, labrat → base: 3/14), unless the revision carries a line starting
  `Correction (round 71):` naming the recomputed `attack share 3/14`. Base: 1.
- guard: each removed base line is a `## Planned` heading replaced by `## Superseded plan — round
  R` in the tip; no other base line is removed.

Base receipt (do-nothing control, committed): `controls/c1-base.txt` →
`stale_planned=2 attack_mismatch=1 mismatches=3 met=False`, exit 1.
Junk control (scored by the labrat seat only, never by the lane): deleting the two planned headings
must fail the guard.

Target after-state: `mismatches=0 guard=ok met=True`, exit 0, at the landed tip.
Kill rule: a guard failure, a correction whose number differs from the recomputed value, or any
counter edit after the first seat scored → C1 is `unprovable`, reported, not narrowed.
Sourced: C1 rests on `S132` (kama-shokunin `corpus/knowledge/self-assessment-at-writing.md`,
"Checking self-assessment statements at writing", re-opened in-round by ScoutCalib; located quote
recorded in the lesson Gate).

Repair (exact content rule; the executor writes the strings, the counter checks the rule):
1. SCORECARD.md line 21 `## Planned` → `## Superseded plan — round 21 (historical record)`.
2. SCORECARD.md line 3990 `## Planned — round 48` → `## Superseded plan — round 48 (historical record)`.
3. Append a line starting `Correction (round 71): the round-70 wave W1 attack share 3/14 (21.4 %), not
   4/14: the strict list (reviewer, critic, mutation-tester, labrat) counts 3 of 14 seats in
   .ufo/waves/round-70/w1-results.json; the revenger seat is not an attack role under that list.`
   with the numbers exactly as recomputed.
4. Append `## Planned — next round` with no declared claims (round 72 declares its own at open).

### C2 — freshness (score 10, HOLD 10 on success) — stale `/tmp` citations in SKILL.md

Move: every `/tmp/` path token in the lane playbook is either repointed to a scratch recipe or
annotated as a dated historical record that is not an executable instruction (the QUALITY
absence-annotation rule). This is the SHONEN box-3 residual named in round 70.
Counter: `python3 -B .ufo/waves/round-71/c71_tmp.py --revision <rev>`.

Predicate: `C2 met iff unannotated_tokens == 0 and the replacement guard holds.` Annotated = the line
carries `not an executable instruction`; a repointed recipe line must carry `mktemp` and no `/tmp`
token.

- Base receipt (`controls/c2-base.txt`): `tokens_total=7 unannotated_tokens=7 met=False`, exit 1
  (lines 27, 95, 227, 356, 359, 463, 464).
- Guard: removed lines all carry a `/tmp` token; added lines carry the phrase or `mktemp`; removed
  and added line counts are equal (a deletion without replacement fails).
- Target: `unannotated_tokens=0 guard=ok met=True`, exit 0.
- Kill rule: a deleted line, an annotation on an imperative command (QUALITY criterion "Absence
  annotation content"), or any counter edit after the first seat scored → C2 `unprovable`.
- Repair rule: line 95 is a runnable recipe, so its token is repointed to `$(mktemp -d)`; the other
  six lines are annotated with the exact missing path, the dated absence (`test -e` exit recorded),
  and the words `historical record, not an executable instruction`. No table is split.

## Frontier step (child-lane, section 2b)

- Sourced claim: C1 rests on S132 (above). Its Gate records URL, access date 2026-11-03, located
  quote of 25 words or fewer.
- Mistakes (round 70, mined into `corpus/lessons/round-71.md ## Mistakes`):
  - M1 number-drift — round-70 SCORECARD line 4770 and report state attack share 4/14; the strict
    roster count is 3/14. Evidence: `.ufo/waves/round-70/w1-results.json`; spot-check routed item 1
    (`corpus/lessons/round-70-verifier-spotcheck.md`). Captured-by: none. Fix: C1 attack-share
    conjunct plus the Correction line; able-to-fail: base receipt red.
  - M2 stale-premise — two active `## Planned` sections name rounds 21 and 48 while the lane is at
    round 71. Evidence: SCORECARD.md lines 21 and 3990 at base. Captured-by: none (the freshness
    sweep does not scan SCORECARD plan sections). Fix: C1 stale_planned conjunct; able-to-fail: base
    receipt red.
- Census before→after: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  (exit 0 at base; re-run at tip).

## Wave shape (one v1 wave, band 8–16, one `.ready`)

`w1`, 11 seats, `reportDir .ufo/waves/round-71/w1`:

| Seat | Role | Route | Item |
| --- | --- | --- | --- |
| ScoutCalib | scout | scout route | re-open S132; enumerate SCORECARD planned/attack population at base |
| ScoutTmp | scout | scout route | enumerate the seven SKILL.md tokens; classify recipe vs historical; `test -e` each target |
| ScoutConsider | scout | scout route | read the latest `considerthese/` file; report one unimplemented fitting proposal or none |
| ExecRepairC1 | executor | executor route | apply C1 repair in a scratch clone; counter red at base, green after |
| ExecRepairC2 | executor | executor route | apply C2 repair in a scratch clone; counter red at base, green after |
| LabratControls | labrat | executor route | junk controls (delete planned headings; delete /tmp lines) must fail the guard |
| ReviewContract | reviewer | reviewer route | attack predicates, guards, kill rules, population assumptions |
| CriticClaims | critic | reviewer route | attack falsifiability, axis harm, do-nothing reachability |
| MutCounters | mutation-tester | executor route | mutate both counters in scratch; survivors reported |
| ConnOverlap | connector | connector route | sibling-overlap scan (other lanes touching SCORECARD / SKILL.md / SOURCES.md) |
| ScribeLesson | scribe | connector route | drafts `## Mistakes` and `## Gate` skeleton into the wave dir |
| SentinelPaths | sentinel | connector route | scans counters for /tmp literals, credential material, git writes |

Attack seats: reviewer, critic, mutation-tester, labrat = 4 of 11 (36.4 %, ≥25 %). Attack share
is defined by this list; the round-70 correction uses the same definition. No seat may mutate the
lane tree or the fleet repo; every writer uses a scratch clone under `/fast/scratch/hyaku/kake-r71/<seat>/`.
At most two connector seats (one here). No planner seat (the L1 holds the planner role).

## Honest limits (named before data)

- The counters check named populations at one revision; they do not prove the seats' prose.
- C1's calibration is a self-assessment instrument, so its score (2) stays HOLD even on success.
- `freshness-sweep --offline` is red before this round (one unannotated miss on the
  lowercase `~/projects` path, pre-existing L0 question); its base receipt is `controls/sweep-offline-base.txt`.
  No new red is allowed; a difference from base is recorded.
