# CriticC1Verdict — round 33 wave 2 (falsify), seat KakeR33.CriticC1Verdict

Verdict: C1 **verifies narrowly** at `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`. The declared numbers reproduce exactly, and P6 now keys on `reason_code`, not on message text. Two doc wordings say more than the code does, and one undisclosed behaviour change came with the round-33 runner edits (findings F1 to F3). None of the three changes C1's `met`.

## What I ran (sandbox `/fast/scratch/hyaku/kake-r33/w2/CriticC1Verdict/`, clone at 0a0acfb, TMPDIR=sandbox/tmp, `--repo` = my clone)
- `python3 -B .ufo/waves/round-33/c1_code_probe.py --rev 0a0acfb1… --repo <clone>`: exit 0, **met 4/4, guard_ok true**, benign exit 0, 45 cases, 0 failed. Pristine exit 0 with no failing specs; reworded exit 0 with no failing specs; m3 exit 1, failing `[P6-commit-before-init]`; recoded exit 1, failing `[P6-commit-before-init]`. runnerSha256 `88b47f6b957d…`, hostileSha256 `70def10946ef…` (same as receipt `c1-at-1cf452e.json`). Output: `out/c1-probe-tip.json`.
- Same probe at `--rev 5777d5af…`: exit 0, **met 2/4, guard_ok true**. Reworded exit 1, failing P6; m3 killed; recoded `applicable: false`. Output: `out/c1-probe-base.json`. This matches the declared before value and the receipt `c1-before-5777d5a.json`.
- `python3 -B .ufo/waves/round-33/c1_strict_supplement.py --rev 0a0acfb1… --repo <clone>`: exit 0, **4/4** (s1 to s4 all true). Pristine h6code is `setup_commit_before_init`; the whole-message rewrite `raise CaseRefusal("setup_commit_before_init", "refused")` passes; under m3, h6code is `setup_commit_without_repo` and P6 fails. Output: `out/c1-strict-tip.json`.
- The probe was last changed at `bc6c4a8` (`git log -- c1_code_probe.py`), so it is frozen as SCORECARD says. Blob ids at the tip: probe `f4ee0e89`, runner `32091d21`, hostile selftest `ae4eda6d`.
- Receipts: c1-before-5777d5a, c1-at-bc6c4a8 (met 2), c1-after-b1752a2, c1-at-e490381 and c1-at-1cf452e (met 4, benign 45/0) all agree with SCORECARD.md:1126. There is no receipt at 0a0acfb; my run above covers it (the tip changes docs only).
- Contract check: the guard keeps its two-line shape and the raise carries both the code literal and the unchanged fragment (`scripts/citing_set_selftest.py:401-402`). The apply-time re-check uses `setup_commit_without_repo` (:529). The hostile selftest gains `reason_code` (`codeChecks`, P6 `hostile.json:23`). P6 is the only spec with a reason key (grep of `scripts/fixtures/citing-set-hostile/`), so the docstring at `citing_set_hostile_selftest.py:47` ("rewording a message cannot fail a correct runner") is true at this tip.

## Counterexample experiments (`exp/`; tip and base exported with `git archive`)
Commands: `python3 -B exp/<v>/scripts/citing_set_selftest.py --root exp/<v> --fixtures exp/<fx> --tmpdir tmp/<v>-<fx>`.
- Fixture set fxA: a benign case, a case with `case.json` `{"setup":[{"op":"bogus"}]}`, and a case with `{"argv":["--selftest"]}`.
  - Tip: exit 1; both failures have `code=None` ("names an unknown setup op 'bogus'", "argv refused: --selftest").
  - Base: exit 1; the key is absent.
- Fixture set fxB: a benign case plus a dangling symlink `02-dangling`.
  - Base: exit 1, refused per case ("symlinked case directory refused").
  - **Tip: exit 2, cases 0**, error "fixture directory contains non-directory entries: 02-dangling".

## Findings
- **F1. SKILL.md:950 and lesson round-33.md:12 overstate which refusals carry codes.** Both say the runner reports `code` "for setup refusals" and list three codes. The runner docstring at `scripts/citing_set_selftest.py:125` says the same: "the setup refusals carry codes".
  - In fact, of the load-time `case.json` refusals, only commit-before-init has a code. Every other one reports null: invalid JSON, bad argv, unknown op, bad path, a `.git` path, and so on (`:364-398`; fxA above). A "case copy failed" refusal is a plain string with no code (:550-551).
  - SCORECARD.md:1151 does say "Other refusal sites carry `code` null", but the SKILL and lesson wording reads as if all setup refusals have codes.
  - Smallest fix: "codes for the load-time commit-before-init check and for apply-time setup failures; every other refusal, including the other load-time `case.json` refusals and copy failures, reports null."
- **F2. Undisclosed behaviour change in the fixture-root edit** (`scripts/citing_set_selftest.py:738-748`, commit e490381). `not path.is_dir()` treats a dangling symlink, or a symlink to a file, as a "non-directory entry". Such an entry used to be refused per case with exit 1; now the whole run cannot be evaluated (exit 2, 0 cases), and the error text calls a symlink a "non-directory entry".
  - Symlinks to directories still go through the per-case refusal, which is how the hostile `symlink_case` works, so no current spec is affected. The pristine hostile run still passes.
  - SKILL.md:961 ("reported, not raised or skipped") and lesson :64 ("stray fixture-root entries fixed") don't mention the change. The exit-code docstring at :130-131 still lists only "gate absent, fixture directory absent/empty" for exit 2.
  - Smallest fix: check `path.is_symlink() or path.is_dir()` before the non-directory check so symlinks keep the per-case refusal, or document the new exit 2 case at :131.
- **F3. SKILL.md:959 compares counts in different units.** "0 of 4 failed after; 3 of 4 failed at base; round 32 saw 4 of 4" mixes two measurements:
  - The round-33 figures count runs out of one trial of four concurrent runs (`verification/concurrency-*.txt`).
  - Round 32's "4 of 4" counts iterations of two-run pairs, with the scratch bind-mounted (`.ufo/waves/round-32/w1/ExecBenignSuiteTip.md:37`).
  - "No longer collide" rests on one trial. The `mkdtemp` design (:820-830) makes this structurally plausible, but that part is [INFERENCE]; I did not rerun concurrency.
  - Smallest fix: name the units ("one trial of 4 concurrent runs"; "round 32: 4 of 4 pair iterations").
- Checked and not overclaimed:
  - SCORECARD.md:1126: every number matches the receipts and my runs.
  - Lesson :59, item 2 "Fixed": true for P6, which is what routed item 2 asked for (`round-32-verifier-spotcheck.md:127-130`). The limits for P1 to P5 are disclosed at SCORECARD.md:1151.
  - Lesson :60, item 3 "Fixed": `killed()` requires `guard_ok` (`c1_code_probe.py:161-163`) and `run()` turns a timeout into `timedOut: true` (:61-70). The git rev-parse and archive calls (:102, :115) still have no timeout; the lesson discloses this as a residual.
  - SKILL "a kill counts only with guard_ok": true. The hostile selftest returns exit 2 for stray or symlinked spec entries and refuses whitespace-only keys (`citing_set_hostile_selftest.py` load_spec and main): true by reading the code. I did not run these.
- Limit of the counter (disclosed in the contract, not a C1 defect): the probe's `GUARD` regex needs the raise on a single line (`c1_code_probe.py:51-53`). A line-wrapped but otherwise correct guard would make the probe exit 2 even though the hostile selftest still passes.
- Held ground: I did not argue whether a code is more trustworthy than message text, and I dropped the "apply-time layer emits the load-time code" mutant line of attack because it falls inside the held reason-trust ground.

## Not verified
- I did not rerun the concurrency runs, the QUALITY criterion check (`criteria/refusal_code_check.py`), or the hostile spec-directory stray/symlink refusals.
- C2 is out of this seat's scope.

Tools installed or updated: none. Network: none.
Sandbox deliverables: `/fast/scratch/hyaku/kake-r33/w2/CriticC1Verdict/out/{c1-probe-tip,c1-probe-base,c1-strict-tip}.json`, `/fast/scratch/hyaku/kake-r33/w2/CriticC1Verdict/exp/{base,tip}-{fxA,fxB}.json`.
