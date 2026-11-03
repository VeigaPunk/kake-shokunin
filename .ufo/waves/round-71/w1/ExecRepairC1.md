# ExecRepairC1 — round 71, wave w1 (executor, C1 repair)

Scope: apply contract §C1 "Repair" items 1–4 to `SCORECARD.md` in a scratch clone at base
`cc6b4e0b8c35e72dfb02c6184b847f68c1262153`; counter red at base, green at the repair tip.
Lane tree untouched; no commit outside the scratch clone; `S=/fast/scratch/hyaku/kake-r71/ExecRepairC1`.

## Repair applied (scratch commit `d10fa5e31bf178f5b60858db2a744c6394d386f9`)
- item 1: line 21 `## Planned` → `## Superseded plan — round 21 (historical record)` (in place).
- item 2: line 3990 `## Planned — round 48` → `## Superseded plan — round 48 (historical record)` (in place).
- item 3: appended one 259-char line, byte-equal to the contract's item-3 code span after joining its
  wrapped whitespace: `Correction (round 71): the round-70 wave W1 attack share 3/14 (21.4 %), not 4/14: the strict list (reviewer, critic, mutation-tester, labrat) counts 3 of 14 seats in .ufo/waves/round-70/w1-results.json; the revenger seat is not an attack role under that list.`
- item 4: appended `## Planned — next round` as the last line, no body, no declared claims.
- diffstat `SCORECARD.md | 8 ++++++--` = 6 insertions, 2 deletions, exactly 3 hunks; no other line touched.

## Strict roster recomputation (source of the correction numbers)
`git show cc6b4e0b…:.ufo/waves/round-70/w1-results.json` → 14 results, agents
`[scout,scout,scout,executor,executor,scribe,scribe,reviewer,critic,mutation-tester,executor,connector,revenger,sentinel]`;
strict set {reviewer,critic,mutation-tester,labrat} = 3; 3/14 = 21.4 %. Matches contract 3/14 and `controls/c1-base.txt`.

## Commands, outputs, exit codes (all exercised)
1. `git clone --shared …/kake-shokunin $S/clone && git -C $S/clone checkout -q cc6b4e0b…`;
   `rev-parse --show-toplevel` → `$S/clone`; `rev-parse HEAD` → `cc6b4e0b…`; `status --porcelain` empty.
2. `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-71/c71_calibration.py --lane $S/clone --revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153`
   → `C1 revision=cc6b4e0b… stale_planned=2 stale_at=[21, 3990] attack_stated=4/14 attack_strict=3/14 attack_mismatch=1 guard=ok mismatches=3 met=False`; **exit 1** (identical to committed base control).
3. `git -c user.name=kake-seat -c user.email=seat@fixture commit -q -a -m "C1 repair (round 71): …"` → `d10fa5e3…`; `status --porcelain` 0 lines.
4. same counter `--lane $S/clone --revision d10fa5e31bf178f5b60858db2a744c6394d386f9`
   → `stale_planned=0 stale_at=[] attack_stated=4/14 attack_strict=3/14 attack_mismatch=0 guard=ok mismatches=0 met=True`; **exit 0**.
5. same counter `--lane $S/clone --revision cc6b4e0b…` (same clone, post-commit) → same red line as (2); **exit 1**.
6. `git -C $S/clone diff cc6b4e0b… HEAD -- SCORECARD.md` → artifact; `git apply --check -R <artifact>` against the tip → **exit 0**.
7. Lane untouched: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain -- SCORECARD.md` → empty;
   `git -C <lane> diff --stat cc6b4e0b… -- SCORECARD.md` → empty.

## Artifacts
- `.ufo/waves/round-71/w1/ExecRepairC1/SCORECARD.repair.diff` (4554 B), sha256
  `837cdc63bcef76fba486ab440bda97436f7b0538b6e8fe2c435d009bb9d4e310`; `sha256sum -c` → OK.
- `.ufo/waves/round-71/w1/ExecRepairC1/SCORECARD.repair.diff.sha256`
- `.ufo/waves/round-71/w1/ExecRepairC1/counter-tip.txt`, `counter-base.txt` (raw output plus exit codes above).
- Prefixes `i/`,`w/` come from the lane's `diff.mnemonicprefix=true`; `-p1` still applies cleanly.

## Attacks
None assigned — executor seat; junk controls J1–J3 belong to ExecControls. Adversarial checks exercised on my
own output: base-red control (2) against the committed base receipt, char-equality of the item-3 line with the
contract span (259/259), heading equality for items 1–2, reverse-apply of the saved diff, lane-worktree
cleanliness. The counter was executed only (`python3 -B`), never edited; no lane tracked file was written.

## Risks / limits
- `## Planned — next round` does not match the counter's `PLANNED_RE` (needs `round <digits>`), so the counter
  cannot see or assert it: item 4 is verified by string equality with the contract, not by the counter. If
  round 72 opens without rewriting that section it remains an invisible, unasserted placeholder.
- The guard compares line multisets and constrains removals only; a pure append with no heading rename would
  also pass it. My diff shows 3 hunks and both removals are exactly the two planned headings.
- The correction value depends on `.ufo/waves/round-70/w1-results.json` staying fixed; any later edit moves `attack_strict`.
- Scratch `/fast/scratch/hyaku/kake-r71/ExecRepairC1` deleted before yield; commit `d10fa5e3` is ephemeral (diff retained above).

## Tooling
No installs or upgrades (python3 3.14.8, git 2.56.0 already present); pacman/uv/npx not invoked.
