# NoHarmK1Fixtures — C1 no-harm on the 45 committed cases (round 31, attempt 2, wave 2)

Seat: KakeR31a2.NoHarmK1Fixtures (leaf reviewer, operability axis).
Claim attacked: the round-31 runner repair (commit c88b97e, present at tip
fde133a) changed behavior on the 45 committed fixtures — any per-case exit,
verdict, findings, ok/passed, reason, case set, or failures difference between
base f1ffb81 and tip fde133a is a harm.

## Method

Sandbox: /fast/scratch/hyaku/kake-r31/a2-w2/NoHarmK1Fixtures/ (clone `clone`,
detached exports `base` @ f1ffb81, `tip` @ fde133a via `git worktree add
--detach`; TMPDIR inside sandbox; the runner's own scratch flag is `--tmpdir`,
used for both runs). Each run uses its own export's runner, gate and fixtures:

    cd <export> && TMPDIR=$S/tmp python3 -B scripts/citing_set_selftest.py \
        --root <export> --tmpdir $S/tmp/cases-<tag> --min-cases 45

## Commands and exit codes

| run | command exit | verdict | passed | cases | failed | failedCases | meetsContractMinimum |
|-----|--------------|---------|--------|-------|--------|-------------|----------------------|
| base f1ffb81 | 0 | clean | true | 45 | 0 | 0 | true |
| tip  fde133a | 0 | clean | true | 45 | 0 | 0 | true |

Both runs wrote empty stderr. `runnerSha256` differs as expected (the repair):
base 9f2d1ecb280b7dc314886c79264fb5461c400d8f7c762ea62bb4018fc49e14d3,
tip 5371530d93ecb218b4607fb37de810fe7b7b2db869c65c8b65988b2f04c0ce6c.
`gateSha256` is identical: dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02.
`git diff --stat f1ffb81 fde133a -- scripts/citing_set.py scripts/fixtures/citing-set`
is empty: gate and all 45 fixture trees are byte-identical between the commits.

## Per-case comparison

Rows compared by case name after normalizing only the export path
(`<export>` vs `<export>`) and tmpdir (`cases-base`/`cases-tip`) inside each
row's recorded `argv`. Result: **zero differences** across all 45 rows and
every row field (`case`, `ok`, `passed`, `reason`, `expected`, `actual`,
`argv`). Specifically:

- per-case `actual.exit` mismatches: none (distribution identical: exit 0 ×5,
  exit 1 ×22, exit 2 ×14, exit 64 ×4)
- per-case `actual.verdict` mismatches: none (clean ×5, failed ×22,
  could-not-evaluate ×18 — same mapping case-for-case)
- per-case `actual.findings` (sorted (id,reason) pairs / ids per expected.json
  mode): none
- per-case `ok`/`passed`/`reason`/`expected`: none
- `failures` array: `[]` in both; `caseNames` identical, all 45 discovered in
  both runs — the new containment checks did not reclassify or silently drop
  any committed case.

Post-run `git status --porcelain` in both exports: empty — neither runner
mutated a committed fixture (case copies run under `--tmpdir`).

## Findings

No harm found. The repair is behavior-preserving on the committed corpus: the
containment refusals (argv token rule, `.git` discovery, `git_commit` without
`git_init`, expected.json O_NOFOLLOW/size guard, symlinked-case refusal) fire
on zero of the 45 committed cases, and every case's recorded gate interaction
(argv modulo scratch paths) is unchanged.

Residual gaps: comparison relies on the runner's own JSON rows; gate stdout
itself is not diffed (rows capture exit/verdict/findings, which is the
acceptance surface). Fixture identity across commits is asserted by
`git diff --stat` on tracked content (empty), not by hashing every blob;
fixtures were re-read from each export at run time.

Artifacts: /fast/scratch/hyaku/kake-r31/a2-w2/NoHarmK1Fixtures/run-base.json,
run-tip.json, run-*.stderr, exports `base/` and `tip/`.
No installs or updates performed.
