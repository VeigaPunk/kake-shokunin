# ExecTrial — round 87 w1

## Axes and bounded outcome

Calibration: lowest axis 2 HOLD; freshness: 10 HOLD. This seat supplies an actual-property observation plus offline arithmetic comparison, not a score change, source admission, closure decision, or publication approval.

Trigger → action → outcome: frozen C2 requested one owned-property GET → performed one Python urllib GET to https://ds4cc.com/, retained sanitized public response and capped body, then invoked the announced ExecAge candidate offline → HTTP 200, no redirect, valid aware GMT Date and digits-only Age, all six independent arithmetic outputs matched; runner and candidate exited 0.

## Observation

- Requested/final URL: https://ds4cc.com/; status 200.
- Date: `Wed, 04 Nov 2026 18:24:35 GMT`; parsed with `email.utils.parsedate_to_datetime`, timezone-aware epoch 1793816675.
- Age: `0`, accepted by ASCII `[0-9]+` full match. Absent Age maps to zero; a present invalid Age or missing/invalid/naive Date produces could-not-evaluate without invented inputs.
- Cache-Control: `max-age=600`, retained only, not interpreted.
- Observed request_time=1793816675; response_time=1793816675 immediately after reading body. Fixed trial_now=max(response_time,int(time.time()))=1793816675, captured before offline invocation.
- Body retained: 78897 bytes, below 2097152-byte cap; SHA256 `f2c5d2b3ab34e8e1dd6d08566147664e4dc7d21a5b01acd7943fd719e8342e93`.
- Independent expected fields apparent_age, response_delay, corrected_age_value, corrected_initial_age, resident_time, current_age: all exactly integer 0. Candidate emitted exactly those six integer fields with no stderr.
- Candidate SHA256 before/after invocation: `d1b09ae17a54728a3b967cdc7436f19b62fc98e4304aab64324ee8969454331a`.

## Exact exercised commands / exits

Capture (cwd `/fast/scratch/hyaku/kake-r87/ExecTrial-2`):

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecTrial/capture_trial.py; echo "exit=$?"
```

Capture supervised process exit 0; one invocation only, no retry. The capture receipt's shortened command string is descriptive; the command above is the actual absolute-path invocation.

Offline retained trial (same cwd):

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecTrial/retained_trial.py --record /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecTrial/trial-record.json --tool /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge/cache_current_age.py
```

Runner exit 0; candidate exit 0; verdict `match`; both stderr streams empty. Exact argv, stdout, hashes, Python version and exits retained in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecTrial/trial-run.json`. Python 3.14.8; stdlib only; no installs.

Cleanup:

```sh
rmdir /fast/scratch/hyaku/kake-r87/ExecTrial-2
```

Exit 0; scratch absent afterward; zero clones. Receipt: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecTrial/cleanup.json`.

## Retained files / handoff

All new artifacts are under `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecTrial/`:

- `capture_trial.py`: executed one-shot capture provenance; **do not rerun**, because this assignment authorizes one GET.
- `trial-record.json`: sanitized response, parsed Date/Age, fixed trial_now and observed tool input. SHA256 `6775cdf6abe9c8c036ba8e83f22a167ce0732692236a56310aa896e18d45d608`.
- `receipt.json`: response/capture/body receipt; no cookies, authentication, or other response headers retained.
- `body.html`: bounded public response body, useful capture evidence only; no source-repository modification.
- `retained_trial.py`: reusable offline runner accepting required absolute `--tool`; defaults `--record` to its adjacent retained JSON; independently computes the six arithmetic fields, rejects wrong output shape/types (including bool), and preserves fixed recorded now. Runner SHA256 at execution `af3aa6a25c03892bb8eaa09b7905a554d27ea5f004aced911a1732f6d12e62e0`.
- `trial-run.json`: exact candidate invocation/outcome and digest pin.
- `cleanup.json`: disposal receipt.

L1 can replay the offline command above with its integrated absolute tool path; no network or fresh clock is needed for comparison. That post-integration replay was not performed here. No production file or frozen predicate/case/target changed.

## Honest limitations and defects

1. The real observation is all-zero at integer-second resolution. Constant-zero and Age-only shortcuts could pass this trial. It does not replace the frozen 17-case battery or independent nonzero tests, neither of which this seat ran.
2. Fixed trial_now is the capture-time clock, not the later runner invocation time (1793816762). Thus resident_time zero is intentional and not a claim about the response's age at replay.
3. Capture request_time precedes local Request construction as well as urlopen, rather than being literally the adjacent statement before urlopen. This small local setup is included in the observed interval; no timestamps were rewritten and no second GET was performed. response_time is the statement immediately after body read.
4. The first mkdir attempt specified a not-yet-existing cwd and failed before execution (no exit code supplied by tool). Retried from the existing fleet cwd, writing only authorized directories; exit 0. Scratch used the runtime identity suffix `ExecTrial-2`, while retained artifacts use assigned seat `ExecTrial`; it is fully removed.
5. Finite capture cannot establish freshness lifetime, permission to store/reuse, browser behavior, universal correctness, or independent admission. Missing-Date and invalid-Age paths are implemented but were not exercised by this real response.
6. Named bash invocations were interpreted as supervised processes by the tool; both exited 0 and none was left running. No deliberate background work, services, restart, provider probe, git mutation, clone, delegate, build, lint or formatter was used.
7. No LSP interface is available in the supplied tool inventory; no supported-symbol refactor was needed. No new dependency or installation.

No blocking prerequisite remains for this scoped trial. Reviewer findings and this report remain lane-internal.

## Self-evaluation (not admission)

Accuracy 4: observed values and candidate/runner hashes retained; request setup timing caveat above. Completeness 4: capture, runner, actual candidate comparison and cleanup complete; real response cannot exercise nonzero arithmetic. Clarity 4: absolute replay and limits explicit; receipt has an abbreviated historical command. Actionability 4: L1 can replay offline against integrated tool but integration gate remains its responsibility. Conciseness 3: evidence detail is long; compact result is HTTP200 → offline match with all-zero discrimination limitation. Overall 3.8/5. Highest-impact improvements: use the independent nonzero battery for discrimination, and place future captures' request_time immediately before urlopen. Would the user agree? Evidence and limitations are explicit; no closure or publication claim is made.
