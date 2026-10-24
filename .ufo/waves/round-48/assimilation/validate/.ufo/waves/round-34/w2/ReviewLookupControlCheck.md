# W2 ReviewLookupControlCheck — lookup_control_check.py under rerun and controls

Axes: operability (does the criterion check actually discriminate a leak?), freshness (do reruns at 24a1647 reproduce the landed receipt?).
All work in sandbox `/fast/scratch/hyaku/kake-r34/w2/ReviewLookupControlCheck/` (clone at `24a1647`, both bundles fetched). No lane file besides this report was touched. No tools installed; no network used.

## What I attacked
`.ufo/waves/round-34/criteria/lookup_control_check.py` (lane sha256 `04a2bce96654d8e9…`, byte-identical to `git show 24a1647:` of the same path) and its receipt `verification/criterion-lookup-control-c1-dcef39b.txt` (committed at `24a1647`, sha256 `622bee1062de04b2…`).

## Runs (clone cwd; `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE`; `TMPDIR=<sandbox>/tmp`)
1. `python3 -B .ufo/waves/round-34/criteria/lookup_control_check.py --counter .ufo/waves/round-34/c1_matrix_count.py --repo . --control dcef39b5f4e8373970eb74858d2c6175524cdfd0` → `{"…,"score": 28, "total": 28, "counterExit": 0,"verdict": "FAIL: control reaches the full score"}`, exit=1. Matches the landed receipt field-for-field (control sha, score/total, verdict, exit=1).
2. Same counter, `--control 5613071e0107544d825e37db1e98f0bfcfb61465` (honest tool) → identical JSON modulo the control sha, exit=1.
3. `--counter .ufo/waves/round-34/c2_source_census.py --control 0cce15f0719a4fc23e0e1e7a20bf680f5974e1ba` → `score 5, total 5, counterExit 0, "FAIL: control reaches the full score"`, exit=1. Consistent with the disclosed hollow C2.
4. `--counter /bin/false` → `no usable JSON from counter (exit 1)`, exit=2 (documented path works).
5. Fake counter printing `{"passed": 0, "total": 28}` then `sys.exit(3)` → `{"…,"counterExit": 3,"verdict": "ok: control scores below total"}`, exit=0.

## Findings (ranked)

**F1 (medium) — the check cannot tell a lookup leak from an honest pass, and neither name nor docstring says so.** Runs 1 and 2 produce the same score, verdict string, and exit code for the leak `dcef39b5` and the honest tool `5613071`. The docstring says only "Exit 1 = the control reaches total (criterion fails)", and the script prints `"FAIL: control reaches the full score"` for both — but for the honest tool, exit 1 is the *correct, expected* outcome, not a criterion failure. The name `lookup_control_check` asserts the control is a lookup table; the tool accepts any rev and never verifies that. The run is only meaningful given external knowledge of the control's provenance. Mitigation in the landed text: QUALITY.md grounds `dcef39b5`/`0cce15f0` as built by `CriticDeclarationFit` (corpus/QUALITY.md:667-669), so the pairing is documented — but the check's own contract does not make the honest-control reading clear. Fix: docstring should state exit 1 is also the expected outcome for an honest passing control, and/or the output should distinguish the two readings.

**F2 (low-medium) — a nonzero counter exit never affects the verdict.** `counterExit` is recorded but unused: run 5 shows a counter that prints valid JSON and exits 3 yields exit 0 "ok: control scores below total". The docstring covers only unusable JSON (exit 2); a crashed or partial counter can flip the verdict to "the counter discriminates". Fix: treat nonzero `counterExit` as exit 2 (or a dedicated code), or document that only the JSON is trusted.

**F3 (info) — no committed criterion receipt for the C2 pairing.** `ls-tree 24a1647 .ufo/waves/round-34/verification/` shows only `criterion-lookup-control-c1-dcef39b.txt`; the C2 counter/hollow pairing is witnessed by `c2-at-critic-hollow-0cce15f.json` (the counter's own receipt), not by this check. QUALITY.md:670-672 cites only the C1 exit-1 receipt. My run 3 fills the gap (exit 1, 5/5) but nothing committed pins it.

## QUALITY round-34 criterion (d) text vs the check
corpus/QUALITY.md:658-673 states the command, the exit-1 expectation on the frozen C1 counter with control `dcef39b5`, and the receipt path; all three match observed behavior exactly (run 1). The bullet honestly presents a criterion the round's own counters fail, with grounding and the "Limit" caveat (one control, one leak; counter hiding case names can still be transcribed). One wording nit: the Reject list ("a counter that materializes cases under directory names equal to case ids next to a published matrix") describes the C1 leak shape only; the C2 transcription shape ("rows and an entry copied from a published receipt") is in the definition sentence but not in the Reject list.

## Not verified / residual risk
- I did not audit the internals of `c1_matrix_count.py` or `c2_source_census.py` (other seats own those); my runs trust their JSON as the check does — which is exactly F2's exposure.
- I did not re-verify the wave-1 lookup/hollow commits' content (bundle heads confirmed: `lookup-c1=dcef39b5…`, `hollow-c2=0cce15f0…`).
- Exit-code probe only for crash-with-JSON; timeout path (600s) untested.
