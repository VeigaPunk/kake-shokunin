# KakeR33.CriticC1RepairScope — does C1 fully discharge round-32 routed items 2 and 3?

Seat: critic, wave 1, r33-build, axis operability. Advisory input for the L1 and the closure; no verdict.
Sandbox `/fast/scratch/hyaku/kake-r33/w1/CriticC1RepairScope/` (clone at `bc6c4a8d435473f3c30903210be30d9d6e3ef750`, TMPDIR `tmp/`).
No installs or updates. No network. The only file written in the lane is this report.

## Answer
C1 as declared delivers a **narrower slice** than items 2 and 3. Item 3 is fixed by replacing the old probe
with a new one, but the old probe stays the prescribed reviewer check in `corpus/QUALITY.md`. Item 2's
"structured field" is written down only in the dispatch prompt. The landed SCORECARD contract and the frozen
counter do not require it, and a sandbox commit with **no structured field at all** scores `met` 4 with `guard_ok` true.

## Counterexample (reproduced)
On top of `bc6c4a8` I made one sandbox commit, `489714be413c936a6d98188a80fce016c0b52ef7` (branch `cx-code-in-text`, 2 lines):
- runner `scripts/citing_set_selftest.py:366` raise line becomes `raise ValueError("setup_commit_before_init" ": %s setup op 'git_commit' needs an earlier 'git_init'" % CASE_SETUP_FILE)`,
  so the code is only a prefix of the message text;
- P6 spec keeps **`reason_contains`**, now set to `"setup_commit_before_init"`. There is no `code` field, no `reason_code` key, and no code on the apply-time re-check.

Commands (exit codes):
1. `python3 -B .ufo/waves/round-33/c1_code_probe.py --repo <clone> --rev bc6c4a8d…` → exit 0, `met 2`, `guard_ok true`;
   pristine pass, reworded fails P6, m3 killed, recoded not applicable. This matches the L1 receipt `verification/c1-at-bc6c4a8.json`. Output: `<sandbox>/probe-bc6c4a8.json`.
2. Same command with `--rev 489714be…` → exit 0, **`met 4`, `guard_ok true`**; all four expectations true; benign 45 cases, 0 failed. Output: `<sandbox>/probe-cx.json`.
3. `grep -c reason_code scripts/citing_set_hostile_selftest.py scripts/citing_set_selftest.py` at the counterexample → 0 and 0 (that grep exits 1).

Why it passes: the `reworded` variant changes only the fragment and the `recoded` variant changes only the
quoted literal, both on the guard's raise line (`c1_code_probe.py:51-57`, `:83-93`). Substring matching on the
reason text cannot tell "the code inside the text" apart from "a separate code field". The probe never reads a `code` field or a `reason_code` key.
This is about scope: the counter does not measure the field the claim names. It is not about whether codes may be trusted (held ground; not argued).

## Asked / delivered / open
| # | Asked (pointer) | Delivered by C1 as declared (pointer) | Open (pointer) |
|---|---|---|---|
| 2a | Pin the P6 refusal by a structured field, not message text (`corpus/lessons/round-32-verifier-spotcheck.md:127-130`) | The landed contract asks only for the code literal and the fragment on the guard's raise line (`SCORECARD.md:1112-1116` at bc6c4a8). The counter checks behaviour against rewording and recoding of that line. | A separate `code` field, `reason_code` and `setup_commit_without_repo` appear only in the untracked dispatch `.ufo/waves/round-33/w1-spec.json`, not in landed bytes (`grep -rl` at bc6c4a8: no hit outside `round-30/mutant-ledger`). Counterexample above: `met` 4 with text matching. |
| 2b | A reworded load-time message must not fail P6 on a correct runner (`w1/ExecBaseRunnerVsP6.md:77-78`; `w1/MutReasonCheckGate.md:46`, mutant i) | `reworded` variant must pass (`c1_code_probe.py:13-15`, `:167`) | Rewording is tested on **one fragment only**. The contract also requires that fragment to stay (`SCORECARD.md:1114-1116`), so a full rewrite of the message is never tested. |
| 2c | Tell the load-time guard apart from the apply-time re-check by something other than wording (`ExecBaseRunnerVsP6.md:54-64`; runner `:366` vs `:493`) | m3 killed only if the failing set is exactly {P6} and `guard_ok` (`c1_code_probe.py:161-163`) | The counter never checks that the apply-time site (`:493`) carries a different code. m3 is killed by any mismatch, including the old text mismatch. |
| 2d | (Implied by "per refusal" in the dispatch) refusals report codes | Only the two `git_commit` sites are named | About 25 other refusal reasons have no code (runner `:330-362`, `:407-423`, `:438`, `:468-489`, `:538-638`). P1–P5 specs check exit code and victim state, not the refusing layer (`citing_set_hostile_selftest.py:84`, `:218`; only P6 has a reason key). |
| 3a | The probe gates a kill on `guard_ok` (`spotcheck.md:131`; `w1/ReviewC1ProbeCode.md` F1) | New probe: `killed()` requires `guard_ok`, and pass expectations also require it (`c1_code_probe.py:155-169`) | Delivered in the new probe. The round-32 probe `c1_m3_probe.py` is frozen and still ungated. |
| 3b | A timeout returns a verdict, not a crash (`ReviewC1ProbeCode.md` F2) | `run()` catches `TimeoutExpired` and reports `timedOut` (`c1_code_probe.py:61-65`); a non-zero exit from `git archive` gives exit 2 (`:115-118`) | Other paths in F2's class remain: at `ac46a74~1` (no runner) and `c88b97e~1` (no hostile selftest), the probe dies with `FileNotFoundError`, **exit 1** (`:122`, `:124`). The docstring promises exit 2 when a variant cannot be judged (`:32-34`). Tar errors are not caught (`:119-120`). Low severity: every revision in scope has both files. |
| 3c | A crashed harness must not read as killed (`ReviewC1ProbeCode.md` F3) | The failing set must be exactly {P6} (`c1_code_probe.py:162-163`) | Delivered. |
| 3d | "Fix it before reusing the probe" (`spotcheck.md:132`) | C1 supersedes the old probe with a new one | `corpus/QUALITY.md:555-561` (criterion "A defence-in-depth guard is pinned by the layer that refuses first") still tells reviewers to run the unrepaired `.ufo/waves/round-32/c1_m3_probe.py` and names `reason_contains`. The declaration does not mention it. |

Adjacent, not in items 2 and 3 (do not count against C1): P3 is also refused by the same load-time guard,
and a pin on P3 kills m3 just as well (`round-32/w1/MutReasonCheckGate.md:44`, mutant h; `w1/CriticP6VsP3.md`). Routed item 1 (m3d, m3f, m3g) is excluded by the declaration (`SCORECARD.md:1116-1118`).

## Impacted axes
Operability: C1's `met` 4 can be reached with no structured field, so the claim text says more than the counter verifies. No other axis is touched.

## Smallest safe corrections
1. **Closure** (the counter is frozen; check by hand at the claimed revision):
   `git show <rev>:scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json | grep -c reason_contains` → 0 and `| grep -c reason_code` → 1;
   `git show <rev>:scripts/citing_set_hostile_selftest.py | grep -c reason_code` ≥ 1;
   the runner's raise line for the guard keeps the code outside the message argument (for example a separate argument or attribute, not `"code" ": …"`);
   `git show <rev>:scripts/citing_set_selftest.py | grep -c setup_commit_without_repo` → 1. If any of these fails, C1 discharges only the behavioural half of item 2.
2. Implementation: update `corpus/QUALITY.md:555-561` to point at `c1_code_probe.py` and `reason_code`, or C1 leaves item 3's "do not reuse" live in a reviewer criterion.
3. A future counter could add a variant that replaces the guard's entire message with a constant. My counterexample fails that variant and a field-keyed runner passes it. Also map the missing-file paths to exit 2.

## Not verified
I did not see the L1's in-progress implementation (lane working tree not read as evidence), so I did not test whether it actually adds a structured field.
I did not run P1–P5 layer mutants. I did not audit the C2 counter. The round-32 `c1_m3_probe.py` was not run.
Evidence files: `/fast/scratch/hyaku/kake-r33/w1/CriticC1RepairScope/{probe-bc6c4a8.json,probe-cx.json,c1_code_probe.py}` (probe sha256 `74bf1f80d79e830d2a5c30a711dad3172f79135af1212e998860afb653b9e047`, read from bc6c4a8);
counterexample commit `489714be413c936a6d98188a80fce016c0b52ef7` in `<sandbox>/clone`.
