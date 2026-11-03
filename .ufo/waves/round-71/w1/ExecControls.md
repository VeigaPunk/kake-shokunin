# Round 71 W1 — ExecControls (executor): junk controls J1–J3

Base `cc6b4e0b8c35e72dfb02c6184b847f68c1262153`. Scratch `/fast/scratch/hyaku/kake-r71/ExecControls`
(`git clone --shared`, deleted before yield; commits `-c user.name=kake-seat -c user.email=seat@fixture`;
`git rev-parse --show-toplevel` = `/fast/scratch/hyaku/kake-r71/ExecControls/clone` before first commit).
Counters extracted from freeze commit `04557e17`, sha256 identical to lane working tree:
`ae317667335b76df4507dc6c6620926628ce257308884158159bdb6a82b0fd51 c71_calibration.py`,
`9037746bdf17bae71b04f88a8e28048b4254df5e34c8e5ebc341dd07b64da32a c71_tmp.py`.
Base population: `## Planned` at SCORECARD 21, 3990; `/tmp/` at SKILL 27 95 227 356 359 463 464; round-70 14 seats, 3 strict attack.

## Base do-nothing controls — verdict: both red, exit 1
```
$ cd /fast/scratch/hyaku/kake-r71/ExecControls
$ python3 -B ./c71_calibration.py --lane "$S/clone" --revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153
C1 revision=cc6b4e0b8c35e72dfb02c6184b847f68c1262153 stale_planned=2 stale_at=[21, 3990] attack_stated=4/14 attack_strict=3/14 attack_mismatch=1 guard=ok mismatches=3 met=False
exit=1
$ python3 -B ./c71_tmp.py --lane "$S/clone" --revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153
C2 revision=cc6b4e0b8c35e72dfb02c6184b847f68c1262153 tokens_total=7 unannotated_tokens=7 unannotated_lines=[27, 95, 227, 356, 359, 463, 464] removed=0 added=0 guard=ok met=False
exit=1
```
Reproduces `controls/c1-base.txt` (mismatches=3) and `controls/c2-base.txt` (7/7), exit 1 each.

## J1 — delete the two `## Planned` headings, keep bodies — verdict: red, exit 1
```
$ python3 -B ./mk_controls.py j1
J1rev=3db1e32b1e87afc5da04ab40ee8a605db22565d1
$ python3 -B ./c71_calibration.py --lane "$S/clone" --revision 3db1e32b1e87afc5da04ab40ee8a605db22565d1
C1 revision=3db1e32b1e87afc5da04ab40ee8a605db22565d1 stale_planned=0 stale_at=[] attack_stated=4/14 attack_strict=3/14 attack_mismatch=1 guard=fail mismatches=1 met=False
exit=1
```
Commit diff `SCORECARD.md | 2 --`; `guard=fail`: heading deletion without `## Superseded plan — round R` is
caught (attack_mismatch=1 is the unrepaired base value, not this control's trigger).

## J2 — delete the seven `/tmp`-bearing lines — verdict: red, exit 1
```
$ python3 -B ./mk_controls.py j2
J2rev=c38fff31e8e9e74f96861e02781997ebc77569df
$ python3 -B ./c71_tmp.py --lane "$S/clone" --revision c38fff31e8e9e74f96861e02781997ebc77569df
C2 revision=c38fff31e8e9e74f96861e02781997ebc77569df tokens_total=0 unannotated_tokens=0 unannotated_lines=[] removed=7 added=0 guard=fail met=False
exit=1
```
Commit diff `SKILL.md | 7 -------`; `guard=fail` via removed=7 added=0 (deletion without replacement).

## J3 — line 95 kept, phrase appended only (no `mktemp`), six others annotated — exit as found
Branch `j3` off base, commit `5b37014e0479e31ec23295a7c81996118ddaf483` (`SKILL.md | 7 +++++++-------`).
Line 95 tip ends `…cp` back; not an executable instruction` with its `/tmp/probe-latest.backup.json` token intact.
```
$ python3 -B ./c71_tmp.py --lane "$S/clone" --revision 5b37014e0479e31ec23295a7c81996118ddaf483
C2 revision=5b37014e0479e31ec23295a7c81996118ddaf483 tokens_total=7 unannotated_tokens=0 unannotated_lines=[] removed=7 added=7 guard=ok met=True
exit=0
```
Verdict as found: **exit 0, met=True**, recorded as the named residual probe, not a pass. Factual observation:
the C2 added-line guard is phrase-or-`mktemp`, so it does not encode the contract kill rule "an annotation on
an imperative command"; J3 and a rule-compliant repoint are indistinguishable to this counter.

Tooling: none installed/upgraded. Lane tracked bytes untouched (`git status --untracked-files=no` empty; no
mutating git outside the scratch clone). Scratch removed after writing this file (`rm -rf`).

Report: .ufo/waves/round-71/w1/ExecControls.md
