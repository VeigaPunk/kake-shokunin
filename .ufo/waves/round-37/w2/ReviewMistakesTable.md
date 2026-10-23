# Kake R37 W2 — ReviewMistakesTable

Target: `corpus/lessons/round-37.md:152-158` `## Mistakes` at tip 79d3c780 — can each row's fix be shown to fail?
Axes: operability (the gate must be able to go red and green when rerun) and freshness (the receipt must still match the committed bytes).
Sandbox: /fast/scratch/hyaku/kake-r37w2/ReviewMistakesTable/ (clone at 79d3c780; GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE unset; TMPDIR in the sandbox). No tools installed. No lane writes except this file. I did not read /fast/scratch/hyaku/kake-r37/. No processes left running.
Row numbers: row 1 = junk control, row 2 = C2 fixture-set counter, row 3 = control sandboxes beside the key.

## Row 1: unrun junk control reported as failed. Fix: `criteria/junk_control_receipt_check.py`
- The committed checker's sha256 is `be94c6c6…cefcd8`. It equals the hash in `w1/ScribeMistakeMine.md` and was added in 528a6d02.
- Reran `timeout 300 python3 -B .ufo/waves/round-37/criteria/junk_control_receipt_check.py --root <clone> --revision R`:
  - 1a16b8e3 → exit 1, "FAIL: no later correction says the round-36 junk control was untested". The round-36 claim is present, so this red comes from the correction check, which is the intended reason.
  - 4b089da6 → exit 0, "PASS: … (0/28, met=false, exit=1)".
  - 79d3c780 → exit 0.
- Mutation test: I made 12 single-edit commits on top of 4b089da6 in `$S/mut`. They removed the receipt, removed the exit file, set passed 25, set met true, set exit 0, changed toolFile, broke the JSON, removed the receipt link, removed the correction sentence, removed the round-36 claim, set cases 27, and set target 24. The checker exits 1 on all 12. On the unmodified base it exits 0.
- I checked the receipt independently too. The retained `retained/controls/CtlC1Junk-source_recheck_junk.py` has sha256 `4c23062f…cb33e`, which equals `toolSha256` in the receipt. I reran `timeout 600 python3 -B .ufo/waves/round-36/sealed_count.py --root <clone> --tool-file <retained junk tool> --key-revision fd1fb723…`. It exits 1 with cases 28, passed 0, met false. Its perCase is identical to `verification/control-r36-junk.json` (sha256 `b5535cc3…`, which matches `ctl/CtlC1Junk.md:13`).
- Limit: the checker hard-codes the round-36 sentence, the correction sentence and the receipt path. It gates this one instance. It would not catch the same kind of mistake in a later round, for example a control reported as failed with no receipt.
- Verdict: **holds**. Red and green reproduce and every mutant goes red. The "Fix" column is accurate for the instance only; nothing gates the class (minor overstatement if read as a class fix). "Captured-by: none before the closure" matches `round-36.md:105-109` and `:143`.

## Row 2: fixture-set counter declared before a recorded-oracle set was scored. Fix: C2 withdrawn; QUALITY (h); red receipt `c2-snapshot.json`
- The committed receipt has sha256 `2a363842…a904`, which equals the hash in `ctl/CtlC2FixtureSets.md:26`. The retained `selftest-snapshot.py` has sha256 `73239541…7e54`, which equals `selftestSha256` in the receipt.
- To rebuild the snapshot variant, I copied the retained selftest over `scripts/source_recheck_selftest.py` on top of 202d625a (the variant's recorded parent). That gave commit 4460d29c. I reran `timeout 900 python3 -B .ufo/waves/round-37/c2_mutkill.py --root <c2 clone> --revision 4460d29c --jobs 6`. It exits 0 with fixtures 400, validFixtures 398, killed 32 of 32, met true, counter sha256 `d72e232e…`. This matches the committed receipt; only the commit id differs.
- So the red receipt reproduces: the recorded-oracle set meets the C2 counter. C2's withdrawal is in 4b089da6, which comes before the build commits 528a6d02 and 9dbc88bb, so "withdrawn before data" holds.
- Gap: criterion (h) has only ever been seen red. No counter has been shown to reject a recorded-oracle set, so nobody has seen (h) pass. Its "Check:" is a past receipt, not a check script that can be rerun.
- Verdict: **holds**. The red reproduces and the receipt is fresh. Calling (h) a fix that can fail is right on the red side only; the green side is **unverifiable**. "Captured-by: the pre-freeze control call" matches `SCORECARD.md:1900-1904`.

## Row 3: control sandboxes beside the sealed key. Fix: QUALITY (i); wave-1 moved; "No check yet."
- The evidence matches `w1/ReviewRoutedDisposition.md:29` and `:61` (G2) and `verification/score_control.sh:10-11`, which reads `kake-r37/ctl/$N` and `kake-r37/private/cases.json`. QUALITY (i) says "Check: none yet" (`corpus/QUALITY.md` "Round-37 criteria" (i)).
- /fast/scratch/hyaku/kake-r37w1/ exists and holds 27 wave-1 seat directories, so the "moved" claim holds. The control seats themselves were not moved, and they had already run.
- I tested whether the existing gate could catch this. I built a fake seat directory `$S/fake/ctl/Seat/` with the key at `$S/fake/private/cases.json` beside it, then ran `control_tree_check.py` (v2) on it:
  - On a listing of the seat directory, with `--pattern <key> --tree <seat>`: exit 0, PASS.
  - Without `--pattern`: exit 0.
  - Only when the report lists the parent directory: exit 1.
- So no committed gate catches a key in a sibling directory, and "No check yet" is an honest statement. The fix is not shown able to fail. Moving directories changes which directory is next to the key, not who can read it [INFERENCE: every seat runs as the same user; I did not check permissions because the bounds forbid reading kake-r37/].
- Verdict: **holds**. The row honestly says there is no check, and I confirmed the existing gate is blind to this case. The fix is **not shown able to fail**.

## Residual risk
- Row 1 guards only its instance. Row 2's (h) has never been seen green. Row 3 has no gate; the remedy G2 proposed (`ReviewRoutedDisposition.md:61`, extend control_tree_check to the seat's parent directory) did not land.
- Not run: the round-37 C1 counter, which is out of scope.

Report: .ufo/waves/round-37/w2/ReviewMistakesTable.md
