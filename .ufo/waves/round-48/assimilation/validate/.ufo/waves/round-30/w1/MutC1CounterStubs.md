# Round 30 wave 1 — mutation test of the C1 counter (seat MutC1CounterStubs)

## What I attacked

The C1 counter (`.ufo/waves/round-30/c1_reason_count.py`, sha256 `be2a1287ab7f2abdca8695d8274504d14b9e1c6b0afe95e940c890bfb8bcc53e`,
unchanged at HEAD `04637bd`) grades 14 checks (R01-R08, F01-F06) over the `scripts/` tree exported
from a commit. I built five near-miss gate/runner mutants, one behavioural defect each, and ran the
counter on every mutant through a local commit.

## Trees used

* T0 lane base `4580c78`: **0/14** — baseline failure, so mutants there are inconclusive, not kills.
* T1 my own conforming repair (gate + runner + ten reason-naming fixtures): 14/14, scaffolding.
* T2 executor gate bytes + my runner and fixtures: 14/14, scaffolding.
* **T3 (authoritative)** executor gate + executor runner + both fixture sets: **14/14**, 41 cases,
  runner baseline 0 failed. T3 = gate seat bytes (`scripts/citing_set.py` sha256
  `dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02`, ExecGateFamilies commit
  `1ebdc06`) + runner seat bytes (`scripts/citing_set_selftest.py` sha256
  `0fc87d5b8134c841b02d0db33d8a3262fb774d0c8aacaefc6b6811f190b6530a`, ExecRunnerReasonFixtures
  commit `9bf6896`) + the runner seat's fixtures 13-16 and 30-37 + the gate seat's 38-41, on lane
  base `4580c78`; T3 commit `a1b3ce91f086c3d3968eb195f5377fbec65c367d` in my sandbox clone.
  `diff -r` against the lane's current `scripts/` working tree: **identical**, so this ledger is
  about the bytes now in the lane, not a reconstruction.

## Mutant ledger (T3, authoritative). Check order R01..R08 F01..F06, T3 baseline all pass.

| id | defect | targeted | score | failed check ids | count cross-check | verdict |
|----|--------|----------|-------|------------------|--------------------|---------|
| W1 | gate returns the right finding id with the wrong reason (`F_DUPLICATE_KEY` value `document_duplicate_key` → `document_not_json`) | F01 behaviour; compared of all ten code checks | 4/14 | R01 R02 R03 R04 R05 R06 R07 R08 F01 F02 (F01 behaviour False, 9 compared False) | 14−10=4 | KILLED |
| W2b | runner compares ids only while the fixtures name reasons (both sides reduced to `(id, None)`) | compared of R01-R08, F01, F02 | 4/14 | R01 R02 R03 R04 R05 R06 R07 R08 F01 F02 (all compared False) | 14−10=4 | KILLED |
| W3 | runner compares reasons but skips the setup cases | compared of the codes whose fixture uses a setup step | 10/14 | R01 R04 R07 R08 (compared False); survived R02 R03 R05 R06 F01 F02, whose fixtures are plain files | 14−4=10 | KILLED (partial) |
| W4 | gate exits 64 on every input | every behaviour check | 1/14 | R01 R02 R03 R04 R05 R06 R07 R08 F01 F02 F03 F05 F06 (F04 passes, controls K1-K3 break) | 14−13=1 | KILLED |
| W5 | gate walk silently skips deep directories (>32 path separators) | F05 | 13/14 | F05 (observed exit 2, could-not-evaluate, `[['input_invalid','corpus_empty']]`, want exit 1, failed, one `unadjudicated_citing_pair`) | 14−1=13 | KILLED |

Commits: W1 `e894af663f1e419336b1410c7b1ce39e23dd1cb5`, W2b `3131d0e529aec742d9b966732c360adbed695cba`,
W3 `1cacbfe7f1049b5f69abd40de0d6d5197a7f8c48`, W4 `fe0c37720571c32b133e3dc29cff8671458990a3`,
W5 `5310a1e199fff7b7408627c240f3566edec8754d`. Counters exited 1, 1, 1, 2, 1 (W4 exits 2 because the
controls break, not because a check failed).

Causal check (gate renamed by hand, runner run by hand): on T3 renaming `document_not_json` fails
exactly fixtures 15 and 31 and renaming `corpus_empty` fails exactly 33; on W2b either rename leaves
the runner at exit 0; on W3 renaming `document_not_json` still fails 15 and 31 while renaming
`corpus_empty` leaves the runner at exit 0. Every compared verdict is caused by the renamed reason.
The same five defects on the scaffolding trees give the same verdicts (T1 and T2: 4, 4, 4, 1, 13 of
14), so the detection does not depend on my scaffolding.

## Commands (all inside the seat sandbox; exit codes as observed)

```
git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r30/w1/MutC1CounterStubs/clone
git -C clone checkout -q 4580c78cca1185d059efa6970722bbcf2f9c1b0f
python3 -B .ufo/waves/round-30/c1_reason_count.py --root <clone> --revision 4580c78... --scratch <sb>/scratch-pristine
    -> exit 1, "C1 0/14 ... (controls True, constant gates rejected True)"
python3 build_wave3.py        # merges the two executor byte sets, then the five mutants
python3 -B .ufo/waves/round-30/c1_reason_count.py --root <clone> --revision a1b3ce91... --scratch <sb>/scratch-FULL
    -> exit 0, "C1 14/14 ... (controls True, constant gates rejected True)"
python3 -B .ufo/waves/round-30/c1_reason_count.py --root <clone> --revision <mutant sha> --scratch <sb>/scratch-W<n>
    -> W1 exit 1 (4/14), W2b exit 1 (4/14), W3 exit 1 (10/14), W4 exit 2 (1/14), W5 exit 1 (13/14)
```

## Evidence pointers

* Sandbox clone with T0, T1, T2, T3 and every mutant: `/fast/scratch/hyaku/kake-r30/w1/MutC1CounterStubs/clone`
* Builders: `build_reference.py`, `build_mutants.py`, `build_mutants_hybrid.py`, `build_wave3.py`, `build_w2b.py`, `mutants*.json`
* Counter output: `pristine-4580c78.json` (0/14), `reference2.json` (14/14), `results/FULL.json` (14/14), `results/W1.json`, `results/W2b.json`, `results/W3.json`, `results/W4.json`, `results/W5.json`, plus `results/M*.json`, `results/H*.json`
* Lane repository read only; my only lane write is this report. (`corpus/SOURCES.md` and `scripts/`
  carry other seats' changes, not mine.)

## Findings for the L1 (advisory, not verdicts)

1. **The compared condition can be satisfied by an unrelated runner failure.** With a fixture whose
   setup step was not idempotent, the baseline runner run left the tree dirty and the renamed run
   failed on that setup instead of on the reason code; the reason-blind runner then scored a false
   14/14. The counter requires only "the runner exits non-zero after the rename" and does not require
   the failure to mention the renamed reason. The runner seat's per-case copy avoids the dirty tree;
   the counter would be stronger if it inspected the failure text.
2. **A fixture that creates a FIFO inside the exported tree crashes the counter.** `shutil.copytree`
   in `mutated_runner` raises on a named pipe and the counter dies with a traceback before printing
   its JSON. By the tameshi precedent that run is SETUP, not judged, so I excluded it from the kill
   denominator; the runner seat's per-case copy keeps the FIFO out of the exported tree.
3. **One gate defect kills ten checks.** Every code check's compared part depends on the single
   runner baseline exit, so one wrong reason (W1) drops the score from 14 to 4. The score is coarse;
   the per-check ids in this ledger are the finer signal.
4. **The compared condition only bites for codes whose fixture uses a setup step.** W3 killed 4 of 14
   (R01, R04, R07, R08); the six codes with plain fixtures (R02, R03, R05, R06, F01, F02) survived a
   runner that never runs those cases.
5. **The rate is a self-consistency measure**: these scores come from the counter's own table, so
   they measure the counter's detection power on these five defects, not the absolute gate strength.

## Not verified

* I merged the two executor byte sets myself; the merge now in the lane working tree is byte identical
  to my T3, but I did not run the counter against a lane commit (the lane has not committed `scripts/`).
* My first W2 build changed the comparison for both expectation modes and crashed on legacy
  expectations; that is a broken runner, not a blind one. Row W2b is the corrected, passing-but-blind
  runner; both builds were killed, only W2b is the requested defect shape.
* No request left the machine (no live web property, pinned repository or network resource) and no
  tool was installed or upgraded for this seat.

Report: .ufo/waves/round-30/w1/MutC1CounterStubs.md
