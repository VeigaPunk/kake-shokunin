# Round 71 — lessons (kake, attempt 1)

Base `cc6b4e0b8c35e72dfb02c6184b847f68c1262153` (lane master at round open). Frozen contract
`.ufo/waves/round-71/contract.md` at `04557e17`, with `amendment-1.md` (pre-data; 13-seat final shape).
Wave evidence `.ufo/waves/round-71/w1/` (13 seats, all settled, 0 dead); validated spec and dispatch at
`1240288f`. Repair commit `8102bb0b`. Two claims: C1 calibration (score 2, lowest owned axis) and C2
freshness (score 10). Outcome: **C1 unprovable** (honest stop, claim not met); **C2 met on the frozen
predicate**, with the residuals named below.

## Claims and verdicts

| Claim | Predicate (frozen) | Before (base) | After (`8102bb0b`) | Verdict |
|---|---|---|---|---|
| C1 calibration | `mismatches == 0` and guard ok, `c71_calibration.py` | `stale_planned=2 attack_mismatch=1 mismatches=3 met=False` (exit 1) | `stale_planned=0 attack_mismatch=1 mismatches=1 guard=ok met=False` (exit 1) | **unprovable** — the attack conjunct's premise is false (see M2); its correction was not landed; score stays 2 |
| C2 freshness | `unannotated_tokens == 0` and guard ok, `c71_tmp.py` | `tokens_total=7 unannotated_tokens=7 met=False` (exit 1) | `tokens_total=8 unannotated_tokens=0 removed=7 added=7 guard=ok met=True` (exit 0) | **met on the frozen predicate**; score stays 10 (HOLD); residuals below |

The contract's C1 repair item 3 (the Correction line stating 3/14 and naming the revenger seat) was
**not landed**. The record contradicts it: the round-70 attack set named in
`.ufo/waves/round-70/amendment-0-note.md:11-16` is reviewer, critic, mutation-tester and sentinel,
which is 4/14 and matches the stated SCORECARD line 4770. The wave's ConnOverlap, CriticClaims and
ReviewContract seats reached the same finding independently.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| M1 attribution — round-70 spot-check item 1 says the 4/14 count includes the revenger seat | `corpus/lessons/round-70-verifier-spotcheck.md:99-101`; `.ufo/waves/round-70/amendment-0-note.md:11-16` names sentinel; `.ufo/waves/round-70/w1-results.json` (14 seats: sentinel 1, revenger 1) | none | Corrected in the Corrections section below; the round-70 SCORECARD 4/14 is left as stated. Pre-freeze rule added: a counted population is checked against the record it cites before the counter is frozen (see M2). |
| M2 stale-premise — the C1 attack conjunct was frozen with a strict list (reviewer, critic, mutation-tester, labrat) that the record does not support: labrat is not a swarm role, and sentinel was an attack seat | `.ufo/waves/round-71/c71_calibration.py` STRICT_ROLES; `skills/swarm/SKILL.md:122-125`; CriticClaims §1; ReviewContract (b) | none (the counter was attacked only after freeze) | C1 is reported unprovable and no correction is landed. Round 72 must amend the attack-share premise by a new numbered counter file, after an operator ruling (L0 question, below). The frozen counter is not edited (kill rule). |
| M3 stale-premise — two active `## Planned` headings named rounds 21 and 48 while the lane is at round 71 | `SCORECARD.md` at base lines 21 and 3990; the counter output `stale_at=[21, 3990]` in `controls/c1-base.txt` | none (the freshness sweep does not read SCORECARD plan sections) | Renamed to `## Superseded plan — round N (historical record)` at `8102bb0b`; `controls/c1-after.txt` shows `stale_planned=0`. Able-to-fail: base red at `controls/c1-base.txt`. |
| M4 landing — the frozen C2 repair text (`$(mktemp -d)` on SKILL.md line 95) makes the backup recipe unrestorable; the counter checks text, not execution | ReviewRepair D2: restore attempts exit 1 (`cp: cannot stat …`); ExecRepairC2 repoint `652356421` | none | Line 95 repaired to a named variable recipe (`"${BK:=$(mktemp -d)}/probe-latest.backup.json` … restore with `cp "$BK/…" state/probe-latest.json`). Able-to-fail: the literal form fails its restore step; the variant restores its original bytes (scratch test, exit 0, run in the lead's scratch on this host). |
| M5 vacuous fix — the counter accepts a phrase-only annotation on an imperative command (the QUALITY criterion forbids it; the counter does not enforce it) | ExecControls J3 exit 0 (`met=True`); ReviewRepair C (`b4b54c9a9…`) exit 0 | QUALITY.md "Absence annotation content" (text only; no counter) | SKILL.md lines 95, 463 and 464 repointed to `mktemp` (no annotation left on a command); the counter gap is routed to round 72. |
| M6 reference-drift — the counter reads round-70 results at the tip revision, so a landed history rewrite can launder the attack count | ReviewContract F1 (probe commit `69836788`: `attack_stated=4/14 attack_strict=4/14 met=True`); ReviewRepair R (HIGH) | none | Routed to round 72 (counter pinned to the frozen base revision). Not fixed here: the counter is frozen. |
| M7 scope — the counters accept a crafted `--revision` that becomes a `git show` option and writes files | SentinelPaths rows 8–11 (`--output=…` writes; traversal and overwrite confirmed) | none | Routed. The verified mitigation is `git show --end-of-options <rev>:<path>` (SentinelPaths row 18: blocks the write, legitimate revisions byte-identical). Round 72 amendment; no counter edited now. |

## Corrections (append-only; old → new)

- **SCORECARD.md:21** `## Planned` (names round 21 in its body) → `## Superseded plan — round 21 (historical record)`. Body text unchanged.
- **SCORECARD.md:3990** `## Planned — round 48` → `## Superseded plan — round 48 (historical record)`. Body unchanged.
- **SCORECARD.md tail** `## Planned — next round` appended with no declared claims (contract C1 repair item 4).
- **corpus/SOURCES.md S132 used-by**: `corpus/lessons/round-44.md, SCORECARD.md` → `corpus/lessons/round-44.md, SCORECARD.md, corpus/lessons/round-71.md`. Status `mined`, recheck `on-use`, opened `2026-10-23` unchanged.
- **Round-70 spot-check item 1 (non-author routed note)** — its diagnosis is wrong: the fourth attack seat was sentinel, not revenger (see M1). The round-70 SCORECARD 4/14 statement is not contradicted by the record; the policy question is open (L0).
- **Not corrected in place**: SCORECARD line 4770 (round-70 attack share 4/14) stands. No correction line is appended because the strict premise is unresolved.

## Gate

Candidates considered this round, with decisions:

- **Admit — S132 as the sourced basis for C1**, re-opened in-round by ScoutCalib (kama
  `corpus/knowledge/self-assessment-at-writing.md`, a local own-work file, not a URL; access date
  2026-11-03; sha256 `cd6e3730085ed08ca583604390e84c352ea122e4a6386e383d261a0a0b4cf959`). Located
  quote, 18 words, line 7, first section-prose paragraph, raw substring (`grep -F -c` = 1):
  "The check then evaluates the statement against the committed tree/history at `W`, not just against the current tip." Second quote, 10 words, raw substring (1): "records a calibration error present when the statement was written". The method is S132's, and it is correct; the counter applies it to a tip revision only, so C1 cannot use S132's writing-revision rule (CriticClaims §4 is accepted).
- **Admit — C2 repairs in SKILL.md** (seven lines: 27, 95, 227, 356, 359, 463, 464). Six citations carry the exact path, the dated absence and `test -e` exit 1, and the phrase `historical record, not an executable instruction`. Lines 95, 463 and 464 are commands, repointed to `mktemp`. `git diff` shows exactly seven removed and seven added lines; the sweep (`--offline`) is unchanged from base (`controls/sweep-offline-after.txt`).
- **Reject — the C1 Correction line naming 3/14 and the revenger seat** (contract repair item 3). Reason: the record gives 4/14 with sentinel; the line would write a false count and a false cause. Flip: an operator ruling that fixes the attack set (L0 question), followed by a numbered counter amendment.
- **Reject — the contract's literal `$(mktemp -d)` repoint on line 95**. Reason: ReviewRepair D2 shows the restore fails. Replaced by the named-variable recipe (M4).
- **Reject — phrase-only annotation on line 95** (ExecControls J3, ReviewRepair C). Reason: an annotation beside an imperative command (QUALITY criterion). The counter cannot reject it; the review seats did. Flip: a counter amendment in round 72 that reads the line's command status.
- **Admit — Planned renames** (C1 repair items 1, 2, 4). Reason: they are true statements about the lane's plan state; the counter confirms `stale_planned` 2 → 0.
- **Assimilation**: none. ScoutConsider read `considerthese/2026-10-26.md` Part 2 and found no unimplemented proposal that fits C1 or C2 (its files checked and the verdict are in `.ufo/waves/round-71/w1/ScoutConsider.md`). No `merge/kake` theme was taken this round.
- **Spot-check**: the lane's own sample is 3 admits (S132, C2 repairs, Planned renames) and 3 rejects (correction line, mktemp literal, phrase-only annotation). A non-author check is owed to the hyaku closure. The attack seats' findings are recorded as routes, not admissions.

## Sourced claims

- **C1 rests on S132** (above). Its claim is unprovable, so no admitted outcome rests on it.
- **C2 rests on no web source.** The repaired citations are the lane's own `test -e` results and the QUALITY bar; no S-row is cited for the repair.

## Known residuals (named, not closed)

- The C1 counter's attack conjunct premise is false (M2); round 72 owes an operator ruling and a numbered amendment.
- The C1 counter reads `round-70/w1-results.json` at the tip revision (M6). The C1 guard checks SCORECARD lines only. A correction whose number is wrong but names another wave is accepted (ReviewRepair B).
- Both counters accept a crafted `--revision` that is read as a `git show` option (M7). Callers must pass trusted revisions until round 72 lands the mitigation.
- The C2 counter does not reject a `${TMPDIR:-/tmp}` repoint (ReviewContract F2), and it accepts phrase-only annotations on commands (M5).
- `## Planned — next round` is not parsed by the C1 counter (ExecRepairC1 risk); declared claims under it would be invisible.
- The offline sweep stays red before and after (`§paths: 1 unannotated miss`, pre-existing `~/projects`; L0 question from round 69).

## Measurements (counting commands; receipts under `.ufo/waves/round-71/controls/`)

- C1 base: `python3 -B .ufo/waves/round-71/c71_calibration.py --revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153` → exit 1 (`controls/c1-base.txt`). After: `… --revision 8102bb0b1169b8a728c6981c2d0bf4e28d840e67` → exit 1 (`controls/c1-after.txt`).
- C2 base: `python3 -B .ufo/waves/round-71/c71_tmp.py --revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153` → exit 1 (`controls/c2-base.txt`). After: `… --revision 8102bb0b…` → exit 0 (`controls/c2-after.txt`).
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0 before (`controls/census-before.txt`) and after; rows 176 → 176.
- Sweep: `node scripts/freshness-sweep.mjs --offline` → exit 1 before (`controls/sweep-offline-base.txt`) and after (`controls/sweep-offline-after.txt`): identical verdict line.
