# ReviewerC2Base — C2 no-op control cannot pass at base

Seat: ReviewerC2Base (reviewer). Scope: independently run the C2 counter
`.ufo/waves/round-54/c54_ops_debt.py` at base revision
`68228b2d74e7930ae4f07e90e382a0d03ab80c7b` and verify the no-op (do-nothing)
control fails. Findings only; no admission claimed. Read-only; the counter reads
committed bytes via `git show` and this seat made no writes other than this report.

## Executed command and verbatim output

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-54/c54_ops_debt.py --root . --revision 68228b2d74e7930ae4f07e90e382a0d03ab80c7b
registry=absent manifest=absent uncovered=4
cited=['CriticCrossLane.md', 'ReviewerProvenance.md', 'ScoutQuarantine.md', 'ScoutS329.md']
settled=[]
uncovered_names=['CriticCrossLane.md', 'ReviewerProvenance.md', 'ScoutQuarantine.md', 'ScoutS329.md']
Round-53 ops debt: registry row present, settlement manifest committed, and every cited w1 seat-report name recorded resolved or lost; met when all three hold
EXIT=1
```

Exact result: `registry=absent manifest=absent uncovered=4`, **exit 1**
(uncovered count = 4; settled = 0). Byte-identical to the committed receipt
`.ufo/waves/round-54/controls/base-c2-ops-debt.txt`. The do-nothing control
fails (met=False) exactly as the frozen contract requires — the no-op cannot pass.

## Independent verification of each predicate arm at base

Base revision verified: `git rev-parse` resolves
`68228b2d74e7930ae4f07e90e382a0d03ab80c7b` (subject "round-53 verifier
spot-check (integrator, hyaku): non-author admit/reject"), parent
`189ba6d1`; `master` contains it and sits one commit ahead
(`acae1dc` "round-54: freeze claims and calibration controls").

- **P2.1 registry row — absent.** `git show 68228b2d:SKILL.md`: the
  `### Owned freshness gate registry` table (line 208) contains only the
  `freshness-sweep` row; no line under that heading names `c53_gate_truth.py`.
  (The script itself is committed under
  `.ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py` — it is the table
  row that is missing.) The counter scans only committed bytes; the row cannot
  appear without a commit.
- **P2.2 settlement manifest — absent.**
  `git show 68228b2d:.ufo/waves/round-53/settlement.md` → fatal "exists on disk,
  but not in '68228b2d'" (exit 128). `git ls-tree -r 68228b2d --
  .ufo/waves/round-53/` lists 17 committed files (spec, exec-quality-gate,
  sources, receipts); **no `w1/` directory and no `settlement.md`** — matching
  the spotcheck's "40 spawned vs 0 committed seat reports". The on-disk
  `settlement.md` is uncommitted working-copy content; `git show` never sees it.
- **P2.3 cited-name coverage — 4 uncovered.** Extracting
  `\.ufo/waves/round-53/w1/[A-Za-z0-9_-]+\.md` from committed
  `corpus/lessons/round-53.md` yields exactly 4 names
  (CriticCrossLane, ReviewerProvenance, ScoutQuarantine, ScoutS329);
  `round-53-verifier-spotcheck.md` contributes `ReviewerProvenance.md` (already
  counted). Union = 4, settled = ∅ ⇒ `uncovered=4` is the correct, exact count.

## Contract-vs-counter consistency check

The contract says the manifest must cover "every `w1/` seat-report filename
cited by `corpus/lessons/round-53.md` **and the closure's named loss list**".
The closure (spotcheck §"Dead-seat reconciliation", committed at base) names
**7** seat reports in plain text: ReviewerProvenance, CriticCrossLane,
ScoutS329, ScoutS312, CriticLocators, ScribeGate, ScoutQuarantine. The
counter's path-anchored `cited` regex catches only the 4 prefixed spellings,
but its `REQUIRED_SEAT_NAMES` set is exactly those 7 names and is required to
be a subset of `settled` — so the manifest requirement is the strict superset:
pass requires a row `|<name>.md | resolved|lost |` for all 7 names **plus**
every path-cited name, plus the "40 spawned" / "0 committed seat reports" loss
basis. Consistent; the 7-name demand is implemented, only the uncovered-count
display shows the 4 path-cited names.

## Kill-rule and mutation notes

- Exit mapping correct: 1 at base; 0 iff `registry_present and manifest_ok`;
  2 when required committed files unreadable; 64 on usage error. Verified base
  path returns 1 via `registry_present=False`, `manifest_ok=False`.
- No exit-0 path exists at base: registry row and manifest must both come from
  `git show <rev>:<path>`; nothing uncommitted can satisfy either arm.
- Residual (out of base scope, for CriticC2Predicate/mutation seats): the
  registry check stops scanning at the next `## ` line; `### ` subsections
  under the registry heading are included in the scan. Table rows below a
  later sibling `###` would not be seen — acceptable given the frozen row
  placement convention.

## Verdict

**Control verified: the no-op cannot pass.** At base `68228b2d` the committed
counter prints `registry=absent manifest=absent uncovered=4` and exits 1,
byte-identical to the committed receipt; every predicate arm independently
confirmed against committed bytes. No defects found in scope.

Installs: none (pacman paused; no tools required).
Writes: this report only.
