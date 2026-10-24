# MutReasonCheckGate — can the round-32 C1 repair fail?

Seat `KakeR32.MutReasonCheckGate` (mutation tester, wave 1, r32-build). Axis: operability. Target: the new `reason_contains` reason check in the hostile selftest.

## Verdict

The C1 repair is **load-bearing and sound as landed**: every mutant that removes the reason pin (or the code that enforces it) makes mutant m3 survive again, and the unmutated runner still passes the hostile selftest with 45/45 benign fixtures clean. Two secondary findings (F2, F3) are advisory only; neither falsifies a declared claim.

## Method

Clone of the lane repo at `285abcad632e3c1c57bb402232e7d218054db383`, one sandbox clone per mutant, each mutant committed in its own clone. Counter run in every clone (all exited 0):

    cd /fast/scratch/hyaku/kake-r32/w1/MutReasonCheckGate/clone_X
    export TMPDIR=/fast/scratch/hyaku/kake-r32/w1/MutReasonCheckGate/tmp
    python3 -B .ufo/waves/round-32/c1_m3_probe.py --repo . --rev HEAD

`killed=1` = the m3 mutant (load-time guard deleted) was caught; a kill counts only when `guard_ok` is true (pristine hostile run exit 0, benign run exit 0).

## Results

| id | mutation | killed | guard_ok | m3 |
|----|----------|--------|----------|----|
| base | none (285abca) | 1 | true | killed |
| a | drop `and all(detail["reasonChecks"].values())` from `passed` | **0** | true | **survives** |
| b | `detail["reasonChecks"] = {n: True for n in wanted}` | **0** | true | **survives** |
| c | remove `reason_contains` from the P6 spec | **0** | true | **survives** |
| d | P6 setup = `git_commit` only (same as P3) | 1 | true | killed |
| e | P6 `reason_contains` loosened to `git_init` | **0** | true | **survives** |
| f | delete the P6 spec entirely | **0** | true | **survives** |
| g | P6 = P3 shape, no pin | **0** | true | **survives** |
| h | delete P6, put the pin on the existing P3 instead | 1 | true | killed |
| i | reword the runner guard message | 1 | **false** | pristine fails; kill does not count |

Assignees a, b, c behave as the acceptance requires: **m3 survives again** in each, so the reason check is what kills m3, not the fixture's mere existence. e, f, g confirm the same from the spec side. Benign fixtures: `{"exit": 0, "cases": 45, "failed": 0}` in all nine runs — no baseline failure.

## Mechanism

Runner layers in `scripts/citing_set_selftest.py`: L1 load-time guard at lines 362-363 (`raise ValueError("%s setup op 'git_commit' needs an earlier 'git_init'" ...)`) and L2 apply-time re-check at lines 489-490 (`raise RuntimeError("git_commit needs the repository created by git_init")`). Observed reason for case `h6` (export of the base clone; probe reported `guard matches: 1`): pristine runner → `case.json setup op 'git_commit' needs an earlier 'git_init'`, contains the pin, `reasonChecks {'h6': True}`, P6 passes; m3 mutant (L1 deleted) → `case setup failed: git_commit needs the repository created by git_init`, does **not** contain the pin, `reasonChecks {'h6': False}`, P6 fails and the hostile selftest exits 1. The pin separates L1 from L2, and that specificity is load-bearing: mutant e replaces it with the bare word `git_init`, which both messages contain, and m3 survives again.

## Findings

**F1 (supporting C1).** The repair kills m3 only through the reason pin; mutants a, b, c, e, f, g each restore m3's survival while the pristine hostile run stays green and the benign run stays clean. The declared claim "the repair is the thing that kills m3" holds, and the counter fields match `.ufo/waves/round-32/verification/c1-after-2f2f12d.json` (killed 1, guard_ok true) and `c1-before-a0b0dff.json` (killed 0, guard_ok true).

**F2 (coverage / redundancy, advisory).** The distinctive part of the P6 fixture does not carry the kill. Mutant d rewrites P6's setup to `git_commit` only — the shape P3 already has — and m3 is still killed, because the load-time guard fires on the first `git_commit` step whether or not a later `git_init` exists. Mutant h deletes P6 altogether and puts the pin on the existing P3 spec: m3 is still killed (killed=1, P3 fails, guard_ok true). The `git_commit`-before-`git_init` ordering in `P6-commit-before-init` is therefore decorative — the `reason_contains` pin alone suffices and could have been added to P3. P6 as landed is a duplicate shape carrying a duplicate pin. This contradicts no declared claim: the claim names the pin and the P6 spec, both of which exist and both of which work.

**F3 (operability coupling, advisory).** The pin couples the spec text to the runner's exact wording. Mutant i rewords only the runner's L1 message (`setup op git_commit requires git_init first`): the pristine hostile run then exits 1 because P6's pin no longer matches, so `guard_ok` is false and `killed=1` does not count. Any future edit to that error text breaks the selftest loudly (good), but it reads as "the selftest is broken" rather than "the spec text needs updating". Worth a note in either docstring that the two are pinned together.

## Restoration evidence

Nothing was mutated in the lane; all mutation happened in per-mutant sandbox clones under `/fast/scratch/hyaku/kake-r32/w1/MutReasonCheckGate/`. Post-run hashes — lane `scripts/citing_set_hostile_selftest.py` sha256 `1d326e16…4a32a95`, lane P6 spec sha256 `a5ba69da…13156736`, lane `scripts/citing_set_selftest.py` sha256 `7c95a18e…88b8969` — each identical to the base clone. `git diff --stat -- scripts/ corpus/` in the lane: empty; base clone `git status --porcelain`: empty, HEAD still `285abcad632e3c1c57bb402232e7d218054db383`; probe `runnerSha256` was `7c95a18e…88b8969` in every run. Artefacts: `/fast/scratch/hyaku/kake-r32/w1/MutReasonCheckGate/out_{base,a,b,c,d,e,f,g,h,i}.json`; clone dirs `clone_base`, `clone_a` … `clone_i`; mutant commits `3e2e481`, `f6cf6dd`, `b1ff77d`, `79d35ac`, `be5b6f7`, `275d483`, `69e982d` (h and i in `clone_h`, `clone_i`).

## Not verified

C2 counter and freshness claims (not re-run); mutants of the runner's L2 layer, the Git pins or the benign fixture set (attributed in `.ufo/waves/round-31/a2-w2/MutRunnerGuards.md`); any rewording of the L1 error other than mutant i's; no network access and no owned web property contacted; no tools installed or updated for this seat.
