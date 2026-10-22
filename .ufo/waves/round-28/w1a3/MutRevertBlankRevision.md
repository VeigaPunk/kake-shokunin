# MutRevertBlankRevision — C1 counter sensitivity probe (round 28, wave 1a3)

Seat: `KakeR28a3.MutRevertBlankRevision` (mutation tester, leaf). Axis: operability (C1).

## Claim under test
C1 (repair-first): unusable input documents must yield the contracted JSON report and exit 2, and an
absent or unreachable corpus surface must not return clean. Counter:
`.ufo/waves/round-28/c1_interface_count.py`. Repair commit `b5d423f` measured 15/15 (declared claims).

## Mutation (one line, smallest behavior-bearing point)
In scratch clone `scripts/citing_set.py` main(): `if arguments.revision is not None:` ->
`if arguments.revision:` (i.e. reverted the repair's blank-revision guard to the round-27
truthiness form). One mutation only; no other byte changed.

Mutated commit: `13e7c8242e1bd7241caf070c67d1a1f78ff3bbf5` (in scratch clone only).
Blob hashes of `scripts/citing_set.py`: original at `b5d423f` = `c26fcd498f1974265e6bb80dca8e102f57eb7b5f`,
mutated = `189bcccab4bf386cf27acd7db41de58b0b260630`.
Pre-commit working-tree sha256: `1df0da96dbfc023c3cd15e5b6cdb4b3426429b1fd72356d9ab9dcb59ec8636e6`.

## Commands and exit codes
1. `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r28a3/w1/MutRevertBlankRevision/clone` — exit 0; HEAD = `b5d423f`.
2. `git -c user.name=mut -c user.email=mut@invalid commit -qam mut` (in clone, after the one-line edit) — exit 0.
3. Counter on mutated HEAD:
   `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-28/c1_interface_count.py --root <clone> --revision HEAD --scratch <scratch>/count` — exit 1.
   Output JSON: `<scratch>/mut_run.json`.
4. Counter on unmutated reference (same clone):
   `--revision b5d423fc02057f67a6f3a255808313ce40d29069 --scratch <scratch>/count-ref` — exit 0.
   Output JSON: `<scratch>/ref_run.json`.

## Observed outputs
- Mutated HEAD (revision in output `13e7c824…`): passed 14/15; defect 10/11; control 4/4.
  Failing check: `A6-blank-revision` — reasons: "exit 0, want 2", "verdict 'clean', want
  'could-not-evaluate'", "no input_invalid finding" (blank `--revision ""` silently read the
  working tree again).
- Reference `b5d423f`: passed 15/15; defect 11/11; control 4/4; no failures.
- Controls K1 (valid clean working-tree), K2 (valid clean via Git), K3 (missing pair -> failed),
  K4 (fixture selftest) passed on both runs.

## Verdict
MUTANT KILLED. The counter catches the reverted blank-revision guard exactly as expected: score
drops below 15/15, the only failing check is A6, and all four controls still pass (no false
positives from the mutation). No surviving-mutant counter gap found. No conclusion about the
contract is drawn; this is a coverage/behavior probe only.

## Restoration evidence
The mutation exists only in the scratch clone (disposable per tasking); the fleet repo
`/home/vgpnk/Projects/shokunin/kake-shokunin` was not modified (no git/jj mutation, no writes
outside this report). Clone verified at mutated HEAD `13e7c824…`; reference `b5d423f` intact.
No installs performed (none needed; no pacman transaction).

## Not verified
- I did not rerun the base `22c1669` probe (declared 4/15); only the two probes above were run.
- No network fetches; no other runtime or verdict on the round.
