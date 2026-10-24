# MutationC2R3 — C2 R3 correction-line removal (round 47, wave 1)

Seat: mutation-tester. Claim under test: **C2** (freshness — r46 routed defects R3–R6
repaired append-only).
Verdict: **KILLED** — removing the single R3 correction line flips the C2 counter to
`C2_NOT_MET` with `fixed.R3=false` while R4/R5/R6 stay true. R3 is confirmed outstanding
in the mutant, and the pristine after-state is confirmed at both HEAD and the declared
after commit.

## Detector

```
python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision <rev> [--json <path>]
```

(exit 0 = `C2_MET`, 1 = `C2_NOT_MET`, 2 = could-not-evaluate, 64 = usage.)

R3 leg, `.ufo/waves/round-47/c47_routed_count.py:134`:

```python
r3_fixed = any("R3" in line and "20 data rows" in line for line in log_lines)
```

with `log_lines` derived solely from `LOG.md` at the revision (`:121`,
`log = git_show(args.root, args.revision, "LOG.md")`). `SCORECARD.md` is never read by
this predicate.

## Sandbox

- Scratch root `/fast/scratch/hyaku/kake-r47/MutationC2R3/` (local, no push path).
- Built from committed bytes only:
  `git clone --no-hardlinks --branch master --single-branch <lane> lane-copy`, then
  `git remote remove origin` (verified `git remote` empty; nothing pushed).
- Clone HEAD = `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` = lane HEAD = lane `master`.
- Byte identity with the lane before mutating:
  `git show HEAD:LOG.md | sha256sum` = `16d1085b91ff1153fff6eaccedf94e8d67c85a64d8d9b8d6c721cf0a06a9999c`
  (identical to the lane's live `LOG.md`), and the counter blob
  `9be35ef2452aaff0757a0c2839c17cb58e08a7a59f6a217a3489598c19a8359e` is identical to the
  lane's `.ufo/waves/round-47/c47_routed_count.py`.

## Mutant

`LOG.md` line 1793 (the only line in `LOG.md` carrying both `R3` and `20 data rows`),
deleted verbatim:

```diff
--- a/LOG.md
+++ b/LOG.md
@@ -1790,7 +1790,6 @@
   audit), not as build output; residual attack seats prepared under
   `.ufo/waves/round-46/residual-spec.json` for orchestrator dispatch (host mapping:
   this seat prepares waves; the orchestrator dispatches).
-- [r47-correction R3] The adjudication ledger's population is **20 data rows**
   (12 naming LOG.md + 8 naming SCORECARD.md), not the "12 rows" written in this
   entry and the round-46 report; the correction is append-only per the
   round-20 post-review ruling. Same correction appended to SCORECARD.md's
```

`git diff --stat 766f461 HEAD` → `LOG.md | 1 -` (1 file, 1 deletion). LOG.md blob
`4f4b11d` → `a60ce2f`; content sha256 `16d1085b…a9999c` → `9933af3f10d5c1eb49d7bf7e58cb71b4192eb34366aad09cde377b39d41a075b`.
Mutant commit `f6ae3499f3ab2a1729b79512597c857e6f3b1ab6` (only `LOG.md` changed; the
counter blob is byte-identical to pristine, `git diff --name-only` lists `LOG.md` alone).

Exactly one physical line was removed; the four wrapped continuation lines (old
1794–1797) remain. Post-mutation scan of the mutant blob: `grep -c '20 data rows'` = 0
and no `r47-correction R3` marker remains, so nothing residual satisfies the predicate.

## Runs

| state | revision | output | exit |
|---|---|---|---|
| pristine @ lane HEAD | `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` | `outstanding=0/4 C2_MET`; R3/R4/R5/R6 all true | 0 |
| pristine @ declared C2-after | `714e7074110469a9ed2a3594677197baa0890905` | `outstanding=0/4 C2_MET`; all four true | 0 |
| base (context) | `cd42e3c310ba442e89dde638ba6401adaefaf3e8` | `outstanding=4/4 C2_NOT_MET`; all four false | 1 |
| **mutant** | `f6ae3499f3ab2a1729b79512597c857e6f3b1ab6` | `outstanding=1/4 C2_NOT_MET`; `fixed={"R3": false, "R4": true, "R5": true, "R6": true}` | 1 |
| restored | `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` | `outstanding=0/4 C2_MET`; all four true | 0 |

Interpretation: the R3 predicate is load-bearing and isolated — the single-line deletion
turns R3 false without disturbing R4/R5/R6, and the composite flips to `C2_NOT_MET`
(exit 1). The declared r47 after-state (`714e707`) reproduces `C2_MET` from committed
bytes at a fresh clone. R3 is confirmed outstanding under the mutant.

## Restoration

- `git reset --hard 766f4610b64f35a0f402b37eb1d8be2d4d634c0f` in the scratch clone.
- Worktree and blob `LOG.md` sha256 both back to
  `16d1085b91ff1153fff6eaccedf94e8d67c85a64d8d9b8d6c721cf0a06a9999c` — identical to the
  lane's committed blob and live file.
- `git diff --stat 766f461 HEAD` empty; `git status --porcelain` empty; `git remote` empty;
  no push attempted or possible from the scratch clone.
- Restored detector run = `outstanding=0/4 C2_MET`, exit 0.
- Lane checkout untouched: HEAD still `766f4610…`, `LOG.md` sha256 unchanged
  (`16d1085b…a9999c`), counter sha256 unchanged (`9be35ef2…9a8359e`). Lane status shows
  only pre-existing/sibling artifacts (`M .ufo/waves/round-47/w1/swarm-registry.json`,
  untracked `.ufo/waves/round-46/residual/`, sibling `MutationC1Receipt.md`); no mutating
  git/jj command ran in the lane.

## Adversarial notes (static, not exercised)

- **SCORECARD half is uncounted.** The claim text says the same R3 correction is appended
  to `SCORECARD.md` (`SCORECARD.md:3947`, "an R3 correction line naming the 20 data
  rows"), but the counter reads only `LOG.md:121`. A defect confined to the SCORECARD copy
  would leave the counter at `C2_MET`.
- **Trigger is one physical line, not the block.** Because the predicate is a per-line
  substring test, deleting only the four continuation lines and keeping line 1793 would
  still report `R3: true`; likewise any line that merely contains `R3` and `20 data rows`
  satisfies it regardless of meaning. Not exercised here (single assigned probe).
- **Committed-bytes semantics.** `git show <rev>:LOG.md` means worktree edits never affect
  the measurement; the counter's trust boundary is the revision argument, which is
  caller-supplied (pristine runs were pinned to full hashes and to `HEAD`).

## Not done

No live-lane mutation, no second mutant variant, no re-derivation of R4/R5/R6 evidence, no
inspection of sibling repos or fleet-root files. Detector exercised at five revision/state
combinations only.
