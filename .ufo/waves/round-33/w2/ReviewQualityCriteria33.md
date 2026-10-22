# ReviewQualityCriteria33 — round-33 criteria and checks

Seat: KakeR33.ReviewQualityCriteria33 (wave 2, falsify). Reviewed
`corpus/QUALITY.md` "## Round-33 criteria" (:569-593) and
`.ufo/waves/round-33/criteria/{refusal_code_check.py,counter_control_check.py}`
at `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`. Lane tree never read as
evidence; all checks run on sandbox clones at
`/fast/scratch/hyaku/kake-r33/w2/ReviewQualityCriteria33/` (clone-a @
0a0acfb, clone-b @ bc6c4a8 + bundle refs). No tools installed (pacman
paused; system python3 sufficed).

## Receipts re-run — all reproduced

1. `python3 -B .ufo/waves/round-33/criteria/refusal_code_check.py --root ../clone-b --rev bc6c4a8d435473f3c30903210be30d9d6e3ef750`
   -> exit 1, met 1 of 5, unmet S1-S4, S5 vacuous (named_codes=[]). Diff vs
   committed `verification/criterion-refusal-code-at-bc6c4a8.txt`: only the
   `"revision"` field (short vs full hash). Reproduced.
2. Same check `--root . --rev 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`
   -> exit 0, met 5 of 5. Also `--rev e4903817669aa411e424006bb342b345e143ab20`
   -> exit 0, 5 of 5; diff vs committed receipt: revision field only.
3. `git bundle list-heads .ufo/waves/round-33/verification/hollow-r32-c2-6ffa03e.bundle`
   -> `6ffa03ea9c1b094f04ddcf65da46903b7cd16c82 refs/heads/hollow-r32-c2`;
   `git -C clone-b fetch <bundle> '+refs/*:refs/bundle/*'` ok. Lane clone-a
   `cat-file -t 6ffa03ea...` -> exit 128 (commit exists only via bundle).
   `git show --stat`: parent a0b0dff, "hollow C2 repair (fabricated row
   inside registry window)"; SOURCES.md +2, render-web-services.md +2,
   `scripts/fixtures/unrelated/{a,b}.txt` — same bytes at unrelated paths,
   fabricated row S099, matching the criterion's "hollow" definition.
4. `python3 -B .ufo/waves/round-33/criteria/counter_control_check.py --counter .ufo/waves/round-32/c2_retained_count.py --repo ../clone-b --before a0b0dff --after e9283ec --hollow refs/bundle/heads/hollow-r32-c2`
   -> exit 1; before=0 after=3 hollow=3; hollow detail identical to
   committed receipt (c1BlobPaths -> unrelated a/b.txt, c2RowIds ["S099"],
   c3Cites {"S099": 1}). Reproduced.
5. `git show 0a0acfb:scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json`
   -> case h6 carries `reason_code: setup_commit_before_init` and no
   `reason_contains`; runner :402 raises `CaseRefusal("setup_commit_before_init", ... "needs an earlier 'git_init'")`; selftest :228 builds `wanted_codes` from `reason_code` (graded, not tolerated).

## Wording vs check — defects (all low severity)

- F1 (low): Bullet 1 says the selftest "compares [reason_code] for equality"
  but `compares_reason_code` passes on ANY `==`/`!=` AST node whose operand
  text matches a `code` token — an unrelated `runner_code == "clean"` would
  satisfy S3. Conversely a real compare stored via a non-`code` name would
  miss. Landed selftest genuinely compares (:228), so no false verdict here;
  the structural-only limit is disclosed in the bullet.
- F2 (low): S5 only requires the spec's `reason_code` value to appear as a
  string literal ANYWHERE in the runner. A spec naming the wrong layer's
  code (e.g. `setup_commit_without_repo` for P6) still scores 5/5, so "the
  spec shows the intended guard refused first" is not falsified by this
  check alone — it leans on the C1 probe, which the bullet names as the
  behaviour oracle. Consistent with the stated limit; recorded for honesty.
- F3 (low): S4 fires on any dict/`["code"]` assignment in the runner, not
  necessarily the per-case report field. Loose.
- F4 (low): committed receipt `criterion-counter-control-r32-c2.txt` prints
  the hollow row as `hollow` — a repo-local ref name from the L1's evidence
  repo, not the bundle head (`hollow-r32-c2`) nor the sha. Verbatim
  reproduction needs a ref named `hollow`; semantics identical. Naming the
  sha would be more honest.
- F5 (low): bullet 2's "(exit 1 when the hollow commit reaches the
  after-value)" understates exit-1 conditions: the check also exits 1 when
  `before` is not strictly below `after` and on non-JSON counter output;
  argparse failure exits 2 (observed while passing a two-token --hollow
  accidentally). Minor incompleteness of the stated contract.
- F6 (info): S1 is vacuous at tip — `reason_contains_cases` is 0 (P6
  dropped `reason_contains` entirely rather than keeping it "as a secondary
  assertion"). Wording permits this ("may stay"), but S1 currently guards
  nothing; S2-S5 carry the pin. A future unpinned case is outside this
  criterion's stated reject list, so no false claim — just thin coverage.

## Duplication with earlier criteria

No verbatim duplicates. Bullet 1 descends from round-29 bullet 1
("A committed fixture asserts the reason code, not only the finding id")
at QUALITY.md:345 — different layer (hostile-spec vs gate fixture) and
uncited; it does explicitly supersede the round-32 bullet 2 mechanism
(`reason_contains`/`c1_m3_probe.py`). Bullet 2 descends from round-28
bullet 1 ("A counter must be able to reject a constant") — controls vs
hollow-commit discrimination, uncited. Two readability notes: round-32
bullet 2's reviewer check (:556-566) retains its superseded
`c1_m3_probe.py` pointer with no in-place mark (a reader of the round-32
section alone would still try it); consistent with the doc's append-only
convention (round-31 wave-2 corrections behave the same). Mild defect, not
blocking.

## Not verified

The grounding claim "at bc6c4a8 a reworded load-time message fails P6 on a
correct runner" is C1-probe behaviour (`.ufo/waves/round-33/c1_code_probe.py`),
outside these structural checks and this item's scope. Sandbox receipts:
`../tmp/rc-{bc6c4a8d…,0a0acfb1…,e4903817…}.json` under
`/fast/scratch/hyaku/kake-r33/w2/ReviewQualityCriteria33/tmp/`.

Verdict on receipts: all three named receipts reproduced byte-semantically.
Checks are honest about their limits; findings F1-F6 are wording/robustness
nits, none change the declared exit codes.
