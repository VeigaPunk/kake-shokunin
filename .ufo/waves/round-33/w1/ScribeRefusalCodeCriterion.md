# ScribeRefusalCodeCriterion — round 33 wave 1 (operability)

Built a round-33 QUALITY criterion that turns round-32 routed item 2 into a
standing rule: a hostile spec that pins which layer refused must name the
runner's structured refusal `code`, never only message text. Draft with the
full criterion text, check contract and limits:
`/fast/scratch/hyaku/kake-r33/w1/ScribeRefusalCodeCriterion/criterion.md`.
Check script: `.../ScribeRefusalCodeCriterion/criterion_check.py` (proposed
committed home `.ufo/waves/round-33/w1/criterion_check.py`). Neither is
committed; the lane was not written except this report.

## Commands and exits (sandbox, TMPDIR set, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset)

1. `python3 -B criterion_check.py --root clone --rev bc6c4a8d435473f3c30903210be30d9d6e3ef750`
   → exit 1, met 1/5. Failing: S1 (12 spec cases, 1 `reason_contains` without
   `reason_code`: `scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json:23`
   case `h6`), S2 (`scripts/citing_set_hostile_selftest.py:84` CASE_KEYS has no
   `reason_code`), S3 (no `==`/`!=` on a code-named value), S4
   (`scripts/citing_set_selftest.py:528-536` refusal row has no `code`). S5
   vacuously true (no spec names a code).
2. `... --rev b1752a2480aa86fc27536dd6e7d27a91b52bed12` → exit 0, met 5/5.
   Repair bytes: P6 keeps only `reason_code: setup_commit_before_init`;
   `scripts/citing_set_hostile_selftest.py:230-234` compares codes; runner
   emits `code` at `scripts/citing_set_selftest.py:332,563,595,757`.
3. Same two commands with `--root /home/vgpnk/Projects/shokunin/kake-shokunin`
   (read-only `git show`) → exit 1 at `bc6c4a8`, exit 0 at `b1752a2`.
4. `python3 -B mutants.py` → exit 0; seven one-replacement sandbox commits.
5. `criterion_check.py` on each mutant:

| mutant | change | exit | met | killed |
|---|---|---|---|---|
| m1_p6_text_only `2836a3d` | P6 drops `reason_code`, restores `reason_contains` | 1 | 4/5 | S1 |
| m2_p6_typo_code `fb4f9b6` | P6 code `setup_commit_before_ini` | 1 | 4/5 | S5 |
| m3_keys_drop_code `00f3a47` | CASE_KEYS drops `reason_code` | 1 | 4/5 | S2 |
| m4_runner_no_code_full `74b974b` | runner drops row/failure `code` | 1 | 4/5 | S4 |
| m5_no_compare `4069396` | selftest drops the code comparison | 1 | 4/5 | S3 |
| m6_both_keys `8e53e00` | P6 keeps `reason_contains` beside `reason_code` | 0 | 5/5 | admitted |
| m7_reworded_message `0a20ed7` | guard message reworded, code kept | 0 | 5/5 | premise holds |

Every violation check has a killing mutant; two shape variants that should not
fail stay green. The command therefore is not a refuse-everything constant.

## Proposed integration

Append a `## Round-33 criteria` section to `corpus/QUALITY.md`, superseding
only the pin mechanism of the round-32 bullet at `corpus/QUALITY.md:555-561`
(its "Layer refuses first" reading stays; its `reason_contains` check is
replaced). Commit `criterion_check.py` at the proposed home and update the
observed values if the criterion is appended at a later revision. Criterion
text is in `criterion.md` (admit/reject/check/limit, grounded on
`corpus/lessons/round-32-verifier-spotcheck.md:127-130`).

## Findings and limits (advisory)

- At `bc6c4a8` the rule fails for four independent reasons, the primary being
  P6 at line 23 keyed on "needs an earlier 'git_init'". The repair commit
  `b1752a2` passes the rule; I measured committed bytes only.
- S3 is a source-shape proxy: it shows a code-named comparison exists, not
  that the case's `reason_code` flows into it. An unrelated `==` on a
  code-named value would satisfy it. S1 checks key presence, not per-layer
  code distinctness.
- I did not run `scripts/citing_set_hostile_selftest.py`, `c1_code_probe.py`
  or any gate behaviourally, so C1's `met 4` and mutant kill remain the L1's
  receipts, not mine. `m7` shows only that the static pin ignores message
  text; it is not behavioural proof that P6 passes with a reworded guard.
- No installs or upgrades were made. No lane Git/jj state, tracked lane file,
  sibling lane or fleet repo was touched. Evidence came from committed
  revisions; the check never reads a working tree.

## Artifacts (sandbox `/fast/scratch/hyaku/kake-r33/w1/ScribeRefusalCodeCriterion/`)

`criterion.md` bffc6701…254e; `criterion_check.py` 2c556ea2…c240;
`mutants.py` 56915643…2fa7; `mutants.json` 2058cd67…e0bc;
`base.json` 735c68f0…17e4; `repair.json` b13d7939…8f0b;
`mutant-results.json`, `lane-base.json`, `lane-repair.json`; clone at
`bc6c4a8` with object `b1752a2` fetched from the lane.
