# ProbeAlignment

ALGORITHM:
- Prototype: `.ufo/waves/round-60/w1/ProbeAlignment.files/align.py` (`min_untagged(B, R)`), driver `run_probe.py`, clean-RSS check `rss_check.py` (same dir). Stdlib only, bytes throughout.
- Objective: minimum number of non-EOF insertion runs whose first line lacks a visible `[rNN-correction YYYY-MM-DD]` tag, over ALL alignments of base B as an ordered subsequence of revision R. Returns 0 iff some alignment is clean (the contract's existential rule); `None` when B is not a subsequence (guard reports `changed`). Trailing run after the last matched base line is the free EOF append.
- Method: DP `D[j]` = min bad runs for an alignment whose last matched pair is (B[i-1], R[j]). Transition: previous match at k — empty gap (k = j-1) costs D[k]; non-empty gap R[k+1:j] costs D[k] + (0 if tag[k+1] else 1). Prefix minima over `D[k]+pen(k)` on the previous line's occurrence list give O(1) per candidate j.
- Cost: O(m + Σ_i |occ(B[i-1])| + |occ(B[i])|) time, O(m) space. Linear when lines are distinct; O(n·m) worst case when one line value repeats everywhere (blank lines, repeated tag lines).
- Tag visibility per contract: `\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]` outside HTML comments and backtick code spans. Choices made (documented in file): comment `<!--`/`-->` state carries across lines; bytes inside comments/code spans masked to NUL so a tag can never span one; code spans masked per line BEFORE comment scanning (a backtick run binds tighter, so `<!--` inside a span is literal); a run of k backticks closes at the next same-length run on that line, else literal. Multi-line code-fence state is NOT tracked — contract fixtures put the tag on the run's first physical line; flag for the tool builder.
- Edge choices: empty B → 0 (whole revision is one EOF append; "after the last matched base line" holds vacuously). Run before the first matched line must be tagged like any mid-file run (contract: only post-last-match runs are EOF appends).
- Validation: DP == exhaustive brute-force oracle on 12,720 generated cases (0 misses). Contract-shape checks: K15 `a,"",b` → `a,TAG,"","",b` gives min 0 but leftmost-greedy 1 (the contract's "an alignment exists" clause is load-bearing); K16 `a,b,c` → `a,b,b,c` gives 1; K2 tagged run gives 0; K3 untagged run gives 1.

COST:
- Largest knowledge file: `corpus/knowledge/free-read-verbs.md` (503 newline lines, 38,347 B; worktree sha256 `5464ae6dee18b147…` == HEAD blob at `b3b9e29`). Revision = +50 inserted lines in 7 mid-file runs, alternating tagged/untagged heads → min_untagged = 3 as expected: 0.0125 s wall, 8.6 KB tracemalloc peak.
- Synthetic 5,000-line base (distinct lines) → 5,100-line revision (25 tagged 2-line runs mid-file + 50-line EOF append): 0.99 s, 42 KB peak, min = 0.
- Pathological bound (not measured in spec but bounding the DP): identical 5,000-line B and R → 5.7 s, 968 KB peak, min = 0. Real corpus files are ~500 lines with mostly distinct content, so guard-relevant inputs sit far below this bound.
- Memory note: `ru_maxrss` is broken on this host — three fresh processes each report an identical 3,756,564 KB; only tracemalloc peaks are meaningful. [INFERENCE: shared/arena page accounting.]
- Verdict on cost: the existential check is cheap enough for the guard (≈12 ms on the real corpus's worst file; ~1 s at 5k lines even fully distinct; only an adversarial all-identical-lines file pushes to seconds).

GREEDY DISAGREEMENTS:
- 200 seeded fixtures (seed 20261027, dup-prone alphabet incl. tag line and blank line, 25% injected non-subsequence): 53 changed (excluded — subsequence fails, `changed` path), 147 comparable. Leftmost: 40/147 count disagreements (27%), of which 6 are verdict disagreements (greedy >0, min = 0 → false `untagged_insertion`). Rightmost: 41/147 (28%), 6 verdict. Both greedies only ever overcount vs the optimum (never undercount): 92/147 identical.
- Minimal verdict disagreement, leftmost (found by exhaustive ascending scan; smallest in (n,m) order):
  B = [a, U]; R = [TAG, a, a, U] (TAG = `[r60-correction 2026-10-27]`). Leftmost matches a→idx1, U→idx3: run [a] at idx2 starts untagged → 1. Optimal matches a→idx2: run [TAG,a] at idx0..1 starts tagged → 0.
- Minimal verdict disagreement, rightmost:
  B = [a]; R = [a, a]. Rightmost matches a→idx1: run [a] at idx0 untagged → 1. Leftmost/optimal match a→idx0: the idx1 line becomes the free EOF append → 0.
- Minimal count disagreement, leftmost:
  B = [U, a]; R = [a, U, U, a]. Greedy 2 vs min 1.
- Mechanism: a run always starts at previous_match+1 but its emptiness/end depend on the NEXT match; greedy fixes each match at an extreme, so any base line that recurs in R (K15's `""`, K16's `b`, blank lines, repeated correction-tag lines) can shift a run's head off a tagged line or make a run non-empty. Contract K15 already proves a leftmost-greedy implementation fails a required-0 case; rightmost fails its mirror.

VERDICT: The C2 existential rule needs the DP (or equivalent min-cost alignment): both greedies produce false `untagged_insertion` verdicts on duplicate-heavy real files (~4% verdict disagreement on seeded fixtures, K15 is a live example); DP is exact vs brute oracle, ~12 ms and <10 KB on the corpus's largest file, ~1 s at 5k distinct lines, ~6 s only on adversarial all-identical input — adopt it for `append_guard.py`.
