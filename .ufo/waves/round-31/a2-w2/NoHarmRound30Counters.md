# Round 31 wave 2 — NoHarmRound30Counters (C1 no-harm)

Axis judged: operability. Scope: does the repaired round-31 runner
(citing_set_selftest.py at fde133a) still satisfy the round-30 C1 claim
as measured by the round-30 declared counters.

## Attack

Cloned the lane to /fast/scratch/hyaku/kake-r31/a2-w2/NoHarmRound30Counters/clone,
checked out fde133ab48086bb9a06911b4ab045e2ad9086347, and re-ran both round-30
C1 counters against that revision (each exports scripts/ via git archive into
its own scratch under my sandbox, so the lane checkout is untouched).

## Commands and results

  cd /fast/scratch/hyaku/kake-r31/a2-w2/NoHarmRound30Counters/clone
  python3 -B .ufo/waves/round-30/c1_reason_count.py --root . \
    --revision fde133ab48086bb9a06911b4ab045e2ad9086347 \
    --scratch /fast/scratch/hyaku/kake-r31/a2-w2/NoHarmRound30Counters/scratch/count
  -> exit 0, 18.8 s
  stderr: "C1 14/14 at fde133ab… (controls True, constant gates rejected True)"

  python3 -B .ufo/waves/round-30/c1_strict_checks.py --root . \
    --revision fde133ab48086bb9a06911b4ab045e2ad9086347 \
    --scratch /fast/scratch/hyaku/kake-r31/a2-w2/NoHarmRound30Counters/scratch/strict
  -> exit 0, 20.1 s
  stderr: "C1 strict 6/6 at fde133ab… {S1..S6 all True}"

Full JSON outputs:
  /fast/scratch/hyaku/kake-r31/a2-w2/NoHarmRound30Counters/c1-count-out.json
  /fast/scratch/hyaku/kake-r31/a2-w2/NoHarmRound30Counters/c1-strict-out.json

## Comparison with round-30 after receipts
(verification/c1-after-f80bd8f.json, verification/c1-strict-after-f80bd8f.json)

- c1_reason_count: 14/14 both runs. rPassed 8, fPassed 6. Controls K1/K2/K3
  hold. Constant gates rejected: constantClean 0/14, refuseEverything 0/14.
  runnerBaseline identical to receipt: exit 0, cases 45, failed 0 — the
  repaired runner still passes all 45 committed fixture cases with zero
  failures, so the repair caused no fixture regression.
- c1_strict_checks: 6/6 both runs; S1-S6 each True. S2 rename precision
  holds, so every committed fixture still binds its named reason code under
  the new runner.
- gateSha256 identical to receipt
  (dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02) — the
  gate bytes are unchanged; only the runner changed.
- runnerSha256: mine 5371530d93ecb218b4607fb37de810fe7b7b2db869c65c8b65988b2f04c0ce6c
  vs receipt 9f2d1ecb280b7dc314886c79264fb5461c400d8f7c762ea62bb4018fc49e14d3 —
  expected difference; this is the round-31 repaired runner under test.

## Findings

No check changed. The round-30 C1 claim (14/14 reason/family checks,
6/6 strict checks, controls hold, constant gates rejected, runner baseline
clean) still holds at fde133a with the repaired runner. No-harm confirmed.

## Not verified / gaps

- I measured at fde133a per the assignment, not at the attempt-2 lane tip
  92235a0; SCORECARD records counters passing there, and no content file
  changed between the two commits.
- I did not rerun the round-30 C2 counter (out of scope for this seat).

## Tooling

No installs or upgrades needed (python3 and git already present).
