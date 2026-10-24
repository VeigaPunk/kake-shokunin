# MutationC2R4 — R4 reason-fidelity: pristine pass confirmed, append-only clause unenforced (round 47, wave 1)

Seat: mutation-tester. Claim under test: **C2** freshness, R4 leg — the r46 reason-cell
misattributions are repaired append-only, the committed correction block passes, and five
in-memory old-reason mutants are rejected.

Verdict: **PRISTINE PASS CONFIRMED; assigned probe SURVIVED.** The script's claim
(`base=pass mutants=5/5_rejected PASS`, exit 0) reproduces at the round-47 tip and at the
declared after-commit. But a ledger whose historical table cell is edited in place
(append-only violated, block intact) still produces the same PASS line **and** the main
counter's `C2_MET`; neither script reads the table. Coverage finding, not a live defect:
the committed ledger really is a pure append (verified by diff), so C2's append-only
clause holds in bytes while being unenforced by the detector.

## Detector

```
python3 -B .ufo/waves/round-47/c47_r4_mutation_check.py --root . --revision <commit>
```

Exit 0 = PASS, 1 = fail, 2 = could-not-evaluate, 64 = usage. It loads
`corpus/quality/citation-adjudications.md` and `.ufo/waves/round-47/c47_routed_count.py`
**at the revision** via `git show` (`c47_r4_mutation_check.py:23-30,47-52`), execs the
counter (`:54-55`), and requires `r4_reasons_fixed(ledger)` (`:56-60`). It normalizes all
whitespace (`:62`), then for each of the five `R4_EXPECTED` entries substitutes the
corrected phrase with a mutant phrase once (`:64-70`) and fails if the substitution did
not land or the mutated ledger still passes (`:71-73`).

`base=pass` at `:76` names the **committed block under test**, not the frozen base
revision: at `cd42e3c` the counter file does not exist and the script returns
`could-not-evaluate` exit 2 (observed below).

## Pristine runs (read-only; lane untouched)

| revision | subjects (blob ids) | detector output | exit |
|---|---|---|---|
| `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` (HEAD, `master`) | ledger `ef54bc6`, counter `8e6da41`, checker `130854bc` | `R4_REASON_FIDELITY base=pass mutants=5/5_rejected PASS` | 0 |
| `714e7074110469a9ed2a3594677197baa0890905` (declared C2-after) | ledger `ef54bc6`, counter `8e6da41` | same PASS line | 0 |
| `78552622baf74cc8744d0e15013e88d47c16478c` | ledger `ef54bc6`, counter `8e6da41` | same PASS line | 0 |
| `59146c9788b8d12f9053a1ada1d538d0fbf3cc7c` | ledger `ef54bc6`, counter `8e6da41` | same PASS line | 0 |
| `cd42e3c310ba442e89dde638ba6401adaefaf3e8` (frozen base) | counter file absent at revision | `could-not-evaluate: cannot read .ufo/waves/round-47/c47_routed_count.py at cd42e3c` | 2 |

Context from the main counter at the same revisions: `766f461` → `outstanding=0/4
C2_MET` exit 0; `cd42e3c` → `outstanding=4/4 C2_NOT_MET` exit 1 — R4 false at base, true
after, as claimed. The five-mutant loop is real: `R4_EXPECTED` has exactly five tokens
(`c47_routed_count.py:40-46`) and every substitution lands exactly once; otherwise the run
prints `mutant_survived=<token>` and exits 1 (`c47_r4_mutation_check.py:69-73`).

Precision notes on "five old-reason mutants":

- 4/5 are literal old-reason restorations (`charter repo commit` →
  `ds4cc-marketplace repo commit`, `c47_r4_mutation_check.py:68`).
- the `dc8e1adf` mutant only swaps the critic name and **retains the new prose**
  ("all-false entry, met true, 12 of 12"), whereas the old cell text quoted in the ledger
  is "(`CriticC2Sufficiency` re-score, 12 of 12)" (`citation-adjudications.md:49-50`;
  construction `c47_r4_mutation_check.py:65-66`). It is a wrong-critic mutant, not a
  faithful old-reason restoration — the defect class is exercised, but "old-reason
  mutants" overstates 1/5.
- Control (killed, not the assigned probe): inverting the labels of the `b74190e` entry
  in scratch — expected phrase moved into a quote without the `Corrected reason:` prefix —
  was rejected at the block gate with `R4_REASON_FIDELITY base=FAIL`, exit 1. The expected
  values all begin `Corrected reason:`, so a quote lacking that literal label cannot pass.

## No-write check

Before and after the HEAD run, SHA-256 over sorted `path size mtime` for every lane file
outside `.jj`/`.git` was identical:
`0e4138655496bdb8d21380ed31e1334ecd36980827deac6cdfc166774791b669`
(`/tmp/tree_before.txt` vs after-run recomputation). `-B` suppressed bytecode; no
`__pycache__` entry was added or touched. The later tree hash `f8840456...` differs only
because siblings created untracked reports in `.ufo/waves/round-47/w1/` during this wave;
the three subject file hashes stayed equal to their HEAD blobs.

## Assigned mutation probe — in-place cell edit (SURVIVED)

Sandbox: `/fast/scratch/hyaku/kake-r47/MutationC2R4/probe`, `git clone --no-hardlinks` of
the lane at `766f461`; origin removed (`git remote -v` empty), nothing pushed. Pristine
clone run reproduced the PASS line, exit 0; ledger sha256
`e75bc3a746539d86651f4b31f578480702fc325cbe1e1555cd76aa38d5058669`.

Mutant: `corpus/quality/citation-adjudications.md:16` (the `dc8e1adf` table row) rewritten
in place from the recorded old reason to the corrected reason; the `## Round-47
corrections` block (lines 31-54) left byte-identical. This is the most plausible botched
repair — the editor "fixes" the historical cell instead of adding the ruled append-only
line, then keeps the block. Mutant ledger sha256
`abd4efba922fc6ceb71746727069f01ed2faf2c52ee589d95c382b8bd6ffcbba`, commit
`c56142a62fd3672c515d79299401375d9d5f450f`, diff `1 file changed, 1 insertion(+),
1 deletion(-)`.

```
$ python3 -B .ufo/waves/round-47/c47_r4_mutation_check.py --root . --revision HEAD
R4_REASON_FIDELITY base=pass mutants=5/5_rejected PASS
$ echo $?
0
$ python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision HEAD
outstanding=0/4 C2_MET
$ echo $?
0
```

Expected detector: PASS on the checker and `C2_MET` on the counter, because
`r4_reasons_fixed` parses only the block (`c47_routed_count.py:100-112`) and never reads
the table. Observed: exactly that. **Verdict: SURVIVED — coverage finding.** The mutant is
internally contradictory: line 16 now carries the corrected reason while the block's quote
at lines 49-50 still claims the row says "(`CriticC2Sufficiency` re-score, 12 of 12)", and
the block's own assertion "The five table rows above stay byte-identical" (line 33) is now
false. Neither R4 arm notices.

## Artifact side of the claim (does the live build actually comply?)

Yes, independently of the detector: `diff` of the ledger at base vs HEAD is `29a30,54` —
25 added lines, zero deletions or modifications (`e6851ed2…` → `ef54bc64…`). The committed
repair is genuinely append-only; the survivor shows the automation would not have caught a
violation of that clause.

## Restoration

Scratch only: `git reset --hard 766f4610b64f35a0f402b37eb1d8be2d4d634c0f`; ledger sha256
back to `e75bc3a746539d86651f4b31f578480702fc325cbe1e1555cd76aa38d5058669` (= HEAD blob);
`git status --porcelain` empty; origin absent. Restored runs:
`R4_REASON_FIDELITY base=pass mutants=5/5_rejected PASS` exit 0 and `outstanding=0/4
C2_MET` exit 0. Lane production hashes after all probing: checker
`0c8aa7a4357e836e0011871900d0e26bbb4f4c426b91ea2634538405c482ada2` (HEAD blob
`130854bc`), counter `9be35ef2452aaff0757a0c2839c17cb58e08a7a59f6a217a3489598c19a8359e`
(HEAD blob `8e6da41`), ledger
`e75bc3a746539d86651f4b31f578480702fc325cbe1e1555cd76aa38d5058669` (HEAD blob
`ef54bc6`); lane HEAD still `766f4610`. No mutating git/jj command ran in the lane;
my only lane write is this report.

## Not done

No live-lane mutation; no mutation of the counter's `r4_reasons_fixed` implementation; no
re-derivation of R3/R5/R6; no SCORECARD arm; no sibling-repo or fleet-root reads. Detector
exercised at the five revisions above and the single scratch mutant/restore pair.
