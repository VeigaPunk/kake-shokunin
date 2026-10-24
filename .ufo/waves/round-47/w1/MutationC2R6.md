# MutationC2R6 — independent falsification of the R6 withdrawal / rerun-label repair

Axis: **freshness** (C2, routed defect R6; no C1 and no re-score of the r46 capability rows).
Seat: `MutationC2R6`, round-47 wave 1, leaf. Lane repo read-only; every mutation ran in a
disposable local clone. No subagent dispatch, no network, no tool installs, no sibling repo or
fleet-root access, no mutating jj/git command in the lane checkout.

Claim challenged: SCORECARD.md:3976 (C2 routed-record repairs) — "outstanding R3–R6 4/4 → 0/4"
at `714e707`, with R6 closed by an explicit LOG.md withdrawal plus a committed
`.ufo/waves/round-47/verification/offline-sweep-r47-rerun.txt` labelled
`R47 rerun only; not contemporaneous r46 verdict-time evidence`, recording `--offline` exit=0 and
explicitly not retroactive. Expected-failure mode if the counter is a paper check: either marker
can be deleted while the counter still prints `outstanding=0/4 C2_MET`.

## Setup

- Lane (read-only): `/home/vgpnk/Projects/shokunin/kake-shokunin`, worktree HEAD
  `766f4610b64f35a0f402b37eb1d8be2d4d634c0f`; declared measured revision
  `714e7074110469a9ed2a3594677197baa0890905`; frozen base
  `cd42e3c310ba442e89dde638ba6401adaefaf3e8`.
- Sandbox: `/fast/scratch/hyaku/kake-r47/MutationC2R6/sandbox`, from
  `git clone --no-hardlinks --local /home/vgpnk/Projects/shokunin/kake-shokunin`, then
  `git checkout -q 714e7074110469a9ed2a3594677197baa0890905`. Clean worktree before and after the
  probes; only local branches `mut-r6-withdraw`, `mut-r6-label`, `ctl-neutral-log` were created.
  Nothing was pushed (the only remote is the lane path; no push was issued).
- Detector, executed from the sandbox worktree at the base revision bytes:
  `python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision <REV> --json`.
  The detector derives R6 from two conjuncts (`c47_routed_count.py`, main): on one LOG.md line,
  `"[r47-correction R6 withdrawal]"`, `round-46` (case-folded) and `withdrawn` (case-folded); and
  in a receipt file named exactly `offline-sweep-r47-rerun.txt`, the literal
  `R47 rerun only; not contemporaneous r46 verdict-time evidence`, plus `exit=0` or `OFFLINE_EXIT=0`,
  plus `--offline`. A mutant can flip R6 only by breaking a conjunct, not by editing the detector.

## Pristine baselines (same detector bytes, sha256 `9be35ef2452aaff0757a0c2839c17cb58e08a7a59f6a217a3489598c19a8359e`)

| Root | Revision | stdout | exit |
|---|---|---|---|
| sandbox clone | `714e707…` | `outstanding=0/4 C2_MET`, `fixed {R3:t,R4:t,R5:t,R6:t}` | 0 |
| lane (read-only) | `714e707…` | `outstanding=0/4 C2_MET` | 0 |
| lane (read-only) | `766f461…` (tip) | `outstanding=0/4 C2_MET` | 0 |
| lane (read-only) | `cd42e3c…` (frozen base) | `outstanding=4/4 C2_NOT_MET` | 1 |

Counter bytes are identical at the pristine and both mutant revisions
(`git show <rev>:.ufo/waves/round-47/c47_routed_count.py` → `9be35ef2…359e` for
`714e707`, `007c4f4`, `d4b6ee8`), so only the mutated data bytes move the verdict.

## Mutants

Both mutants are single-conjunct deletions of committed bytes in the clone, committed on top of
`714e707`, so the detector reads committed blobs exactly as it does for the claim.

| # | File (line in `714e707` blob) | Bytes removed | Mutant commit | Pristine sha256 | Mutant sha256 | Detector stdout | exit |
|---|---|---|---|---|---|---|---|
| M1 | `LOG.md`:1814 | `[r47-correction R6 withdrawal]` (30 B) | `007c4f4142852f8bae2a8dabe78fe693517475f4` | `3f81fb4f24d249baba159d1656d26529631bcec488066b7b2c48cbcbed70b91c` | `eb0e3b4ea3f07b4dbb4ad6a4e80895f6b6baf46aa589c1c9348876cc5cff7753` | `outstanding=1/4 C2_NOT_MET`; `fixed {R3:t,R4:t,R5:t,R6:false}` | 1 |
| M2 | `.ufo/waves/round-47/verification/offline-sweep-r47-rerun.txt`:1 | `R47 rerun only; not contemporaneous r46 verdict-time evidence` (61 B) | `d4b6ee883ade510bc59d2a059f292eae47964a85` | `b86bc45992aa4f93c2c6d55d972a7d1a84ac0ffb46bedb7a674afd4a9822a717` | `8f7329fe70cc467d16e725f1924b594770cfa8b1bcd4fe4b30dffb79703ec24f` | `outstanding=1/4 C2_NOT_MET`; `fixed {R3:t,R4:t,R5:t,R6:false}` | 1 |

Observed isolation: in both mutants R3, R4 and R5 remain `true` and only R6 flips, so the outcome
is attributable to the R6 conjunct rather than to any collateral change. M1 leaves the line's
other text (`... claim is withdrawn ... round-46 ...`) intact, so the marker is the sole failing
conjunct; M2 leaves the receipt's `command: node scripts/freshness-sweep.mjs --offline`, the
`stdout:` block and its `OFFLINE`/exit evidence intact.

**Verdict: 2/2 killed, 0 survived, 0 inconclusive.** Either mutant leaves R6 outstanding and the
C2 claim un-met, exactly as the frozen predicate requires.

Positive control (method check, not a defect claim): a behaviour-free two-line prose insertion
before `## Round 47` in `LOG.md` (commit `8e54a71467320a4948453ac1cb027687264c9107`, sha256
`09743040523b2dbf686384c73f2b76f5e718f679f1c0324bf817be985f0d1050`) still returned
`outstanding=0/4 C2_MET`, exit 0. The detector is not rejecting arbitrary commits, and the two
kills are not a commit-count artifact. Determinism: each mutant counter was run twice with
identical stdout and exit 1.

## Exact commands and outputs

Baseline and probes, cwd `…/MutationC2R6/sandbox`:

```
git clone --no-hardlinks --local /home/vgpnk/Projects/shokunin/kake-shokunin sandbox   # exit 0
git checkout -q 714e7074110469a9ed2a3594677197baa0890905                              # exit 0, clean
python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision 714e707… --json
  → outstanding=0/4 C2_MET, exit 0
# M1
git checkout -q -B mut-r6-withdraw 714e707…                                            # exit 0
sha256sum LOG.md                                   # 3f81fb4f…b91c before
python: LOG.md bytes.replace(b"[r47-correction R6 withdrawal]", b"", 1)               # 1 occurrence
sha256sum LOG.md                                   # eb0e3b4e…7753 after
git commit -qam 'mutant mut-r6-withdraw'                                               # 007c4f4…, 1 file, +1/-1
python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision 007c4f4… --json
  → outstanding=1/4 C2_NOT_MET, R6=false, exit 1
git checkout -q 714e707… -- LOG.md ; sha256sum LOG.md   # 3f81fb4f…b91c, identical
# M2
git checkout -q -B mut-r6-label 714e707…
sha256sum .ufo/waves/round-47/verification/offline-sweep-r47-rerun.txt   # b86bc459…a717 before
python: receipt bytes.replace(b"R47 rerun only; not contemporaneous r46 verdict-time evidence", b"", 1)
sha256sum …/offline-sweep-r47-rerun.txt                                  # 8f7329fe…c24f after
git commit -qam 'mutant mut-r6-label'                                                  # d4b6ee8…, +1/-1
python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision d4b6ee8… --json
  → outstanding=1/4 C2_NOT_MET, R6=false, exit 1
git checkout -q 714e707… -- .ufo/waves/round-47/verification/offline-sweep-r47-rerun.txt
  → sha256 b86bc459…a717, identical
```

Lane read-only runs (`--root .` at the lane root, `git show`/`git ls-tree` only) reproduced the
baseline table above; no lane file, `.jj`, index, ref or bookmark was written.

## Restoration and containment evidence

- M1 restored `LOG.md` sha256 `3f81fb4f24d249baba159d1656d26529631bcec488066b7b2c48cbcbed70b91c`
  (identical to pristine); M2 restored the receipt sha256
  `b86bc45992aa4f93c2c6d55d972a7d1a84ac0ffb46bedb7a674afd4a9822a717` (identical to pristine and
  to the sha256 SCORECARD.md:3976 declares). Both verified by recomputed sha256 after
  `git checkout 714e707 -- <path>`.
- Sandbox ended clean: `git status --porcelain` empty, detached HEAD back at `714e707…`; restored
  baseline rerun `outstanding=0/4 C2_MET`, exit 0.
- Lane unchanged: worktree HEAD still `766f4610b64f35a0f402b37eb1d8be2d4d634c0f`; `LOG.md` worktree
  sha256 `16d1085b91ff1153fff6eaccedf94e8d67c85a64d8d9b8d6c721cf0a06a9999c` equals the
  `766f461:LOG.md` blob (it differs from the `714e707` blob only because the later verifier
  spot-check commit appended LOG content); receipt worktree sha256 `b86bc459…a717` equals both
  blobs. The lane status entries ` M .ufo/waves/round-47/w1/swarm-registry.json`,
  `?? .ufo/waves/round-46/residual/` were present before this seat started;
  `?? .ufo/waves/round-47/w1/MutationC1Receipt.md` is a sibling seat's report.
- Only writes by this seat: this report and `/fast/scratch/hyaku/kake-r47/MutationC2R6/`
  (40 MB disposable clone; retained as evidence, no services left running).

## Finding

Adversarial result: the R6 closure is **instrument-sensitive, not prose-only**. Deleting the
30-byte withdrawal marker from LOG.md (M1) or the 61-byte mandated label from the rerun receipt
(M2) each flips R6 to `false` and drops the counter to `outstanding=1/4 C2_NOT_MET`, exit 1, while
R3/R4/R5 stay `true`. The claim survives both assigned falsifiers, and the frozen base still reads
`4/4` outstanding.

Bounded coverage notes (static reading of the detector; no mutant was run for these, and none is
a request to change the contract):

- The receipt test is substring containment of the mandated phrase. The sentence tail
  `and not a retroactive receipt for it.` is not independently required; the frozen predicate
  quotes only the mandated phrase, so this matches the contract rather than under-running it.
- The withdrawal test is a three-token same-line conjunction on `LOG.md`; the surrounding
  claim text (for example the `cannot retroactively prove it` wording or the receipt path) is not
  checked, and restatements of the r46 `--offline exit 0` claim outside `LOG.md` are outside the
  predicate's population. C2 freshness here certifies record repair at the named revision, not a
  global absence of the withdrawn wording.

Nothing was installed or updated (no pacman, uv, npm or cargo transaction). No build, linter,
general repository test or sibling runtime was run.
