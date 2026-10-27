# MutationCriterion — round 62

## Probe

Assigned mutant: remove the substantive-quote QUALITY criterion together with its verifier pointer. The frozen counter's criterion clause is `criterion = int(CRITERION in data["quality"] and "round-61-verifier-spotcheck.md" in data["quality"])` (`.ufo/waves/round-62/c62_calibration.py:35`); its expected detector is `criterion=0` and overall `met=false` when that criterion/pointer is absent. The counter reads only committed blobs at the frozen base revision, which predates the requested correction. Therefore an output on this base cannot establish whether a post-change criterion-removal mutant is killed. No post-change candidate revision was provided/available in this probe, so no substantive criterion mutation was made to a source fixture; I did not alter the frozen counter or lane data.

## Actual detector output

Command (pristine frozen counter):
`python3 -B .ufo/waves/round-62/c62_calibration.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`

Output:
`revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false`
Exit: `1`.

This matches the stated base control; it is not a mutant-kill result. Mutated/restored detector runs were not applicable because no post-change revision/fixture existed to mutate and the counter is frozen.

## Hash/restoration evidence

Pristine counter SHA-256: `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`.
Private scratch copy SHA-256 before/after: `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d` (unchanged). No lane source, counter, Git/jj/index, or source tree was modified. Verdict: **inconclusive** (base control only; mutant survival/killing not tested).
