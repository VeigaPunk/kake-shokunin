# Round-54 w1 — ReviewerC1Vacuity: vacuity attack on `c54_s374_calib.py` base→after predicate

Scope: C1 counter `.ufo/waves/round-54/c54_s374_calib.py` only. No edits to shared
checkout; all variants were exercised in a scratch repo at `/tmp/r54/repo` (committed
bytes fed via `git show`).

## Revisions in play (lane moved during review)

- `acae1dc` "round-54: freeze claims and calibration controls" — counter version `d043523`
  ("frozen" counter: `EN_CRAWL_RE`, comparator `pos < corr_at`, inline logic in `run_checks`).
- `8e408e0` "round-54: repair S374 calibration and settle r53 ops debt" — HEAD at report
  time. Same commit rewrote both the entry **and** the counter (`17beeb9`: shared
  `qualifier_findings()`, `NEGATIVE_CRAWL_RE`, comparator `corr_at < pos`).
- Frozen base per contract.md: `68228b2d`.
- The worktree copy of the counter mutated **three times during this review**
  (sha1 `b3a7fbe…` → broke with `NameError: CRAWL_RE`; later `81eee8d…` adds
  `CORRECTION_MARK_RE`, `BOUND_CORRECTION_RE`, mutates `PREDICATE` to end with a period).
  Mid-wave uncommitted mutation of a gate tool is itself an integrity concern, but the
  committed artifact is what counts; findings below are against committed bytes.

## Attack verdicts (landed counter @8e408e0)

| Attack | Passes? | Evidence |
|---|---|---|
| Unchanged committed bytes | **No** | Counter @8e408e0 at rev `acae1dc` and at frozen base `68228b2d` both print `mismatches=1 met=False` / `EXIT=1` (`FAIL C1.3_correction` with `block_offset: -1`, `FAIL C1.4_mismatch: mismatches=1`). Do-nothing control holds on the landed counter; matches committed receipt `controls/base-c1-s374.txt`. |
| Constant true | **No** | `met = quote_ok and corr_ok and mismatch == 0` is data-dependent; base yields `met=False`, repair yields `met=True`. Not a constant-true counter. |
| Junk correction | **Yes — predicate is lexically satisfiable without repair content** | Case 3 (base + appended `asdf qwerty zxcv 「quote」 lorem ipsum not recommend the crawl banana hammock`): `PASS C1.3_correction` `block_offset: 2815`, `mismatches=0 met=True`, `EXIT=0`. Counter lines: `mismatch = sum(1 for pos in suspects if corr_at == -1 or corr_at < pos)` plus the mark-loop `if QUOTE in window and NEGATIVE_CRAWL_RE.search(window)`. No assertion/binding check: the window just needs the substring QUOTE and the trigram `not recommend (the)? (crawl\|crawling)` within 1200 chars of the mark. |
| Contradictory correction | **Yes** | Case 4 (correction asserts "confirms the original endorsement gloss; it is false that the owner did not recommend the crawl"): `mismatches=0 met=True`, `EXIT=0`. The selftest's `correction_wrong_polarity` case claims to guard polarity, but it only checks for the *negated* trigram — any salad containing `not recommend the crawl` passes regardless of the sentence's asserted meaning. |
| Rewrite (delete suspect cell) + mark | **Yes — predicate cannot see deletion** | Case 5 (suspect `(rendered: …)` cell deleted, minimal mark appended): `suspect_cells: 0`, `mismatches=0 met=True`. The predicate is single-revision; it cannot distinguish "superseded by append" from "deleted", so the contract's "appended, never rewritten" clause is unverifiable by this counter. |
| Bare mark appended | No | Case 7 (`[r54-correction 2026-10-25]` alone): `FAIL C1.3_correction`, `mismatches=1`, `EXIT=1`. |

## Defects in the committed predicate

1. **HIGH — Counter amended in the same commit as the claim (8e408e0); "frozen" lasted one
   commit.** The contract presents the predicate as frozen *before* measurement, but the
   frozen-at-open counter **inverted supersession**: `pos < corr_at` counted every cell
   *preceding* the correction as a mismatch. Receipt: frozen counter @acae1dc on rev
   `8e408e0` → `FAIL C1.4_mismatch: mismatches=1`, `met=False` — i.e., **the frozen
   counter rejects the landed repair** (the correction is appended, offset 2876, after
   the suspect cell at 520). Under the frozen counter only a *prepended* correction
   passes (verified: prepended mark → `block_offset: 0`, `mismatches=0 met=True`), which
   is precisely the forbidden "rewrite" shape. The frozen code's own docstring
   (`C1.4 mismatch = number of suspect cells that appear BEFORE any valid correction
   block`) encodes the inversion. The comparator was flipped to `corr_at < pos` in the
   same commit that appended the repair — self-grading after the fix was authored.

2. **HIGH — Junk/contradiction pass on the landed counter.** C1.3 is lexical-window
   matching only (mark + QUOTE substring + one negated-crawl trigram within 1200 chars).
   Keyword salad (case 3) and a correction asserting the *opposite* of the repair
   (case 4) both print `mismatches=0 met=True`, `EXIT=0`. The supersession claim is never
   checked semantically.

3. **MEDIUM — Rewrite invisibility.** `mismatch` counts only suspects *after* the first
   valid mark (`corr_at < pos`). Deleting the suspect cell and appending the mark yields
   `suspect_cells: 0`, `mismatches=0`, `met=True` (case 5). The frozen sentence "not
   superseded by an r54 correction block" is satisfied by any state containing zero
   post-mark suspects, including a state where the cell was removed rather than
   superseded.

4. **MEDIUM — Suspect-cell detection is under-inclusive.** `RENDER_RE =
   \(rendered: ([^)]+)\)` truncates at the first `)`, so a cell containing any inner
   parenthesis is mis-bound; and `CRAWL_RE = crawl|巡回` means *any* crawl token in the
   cell — even "this says nothing about crawl behavior" — disqualifies it as a suspect.
   A still-wrong gloss that mentions "crawl" once escapes detection entirely.

5. **LOW — C1.1 verifies the quote is *a* substring of the body, not that the body is the
   pinned source.** Contract pins sha256 `3ad358bd…`; the counter never hashes. Any body
   file containing the quote once passes C1.1 (`occurrences: 1`).

## Findings only

- Unchanged bytes: cannot pass (do-nothing holds at `68228b2d` and `acae1dc` under the
  landed counter). ✓
- Constant true: the implementation is not constant-true; the junk/no-op distinguishability
  note in `selftest()` is honored by exit codes. ✓
- Junk correction: **passes** on the landed counter (cases 3, 4); the residual guard is
  purely lexical. ✗ — this is a real vacuity hole in the "after" predicate.
- Additionally: the frozen-at-open counter was inverted (rejects the repair, rewards a
  prepend), and the counter was edited in the same commit as the evidence it scores;
  the uncommitted worktree mutation continued during the review (no committed impact
  observed; `met=True` result at `8e408e0` reproduced identically by the committed
  counter, `block_offset: 2876`, `EXIT=0`).

Verification method: `python3 -B` runs of the committed counters extracted via
`git show <rev>:.ufo/waves/round-54/c54_s374_calib.py` against a scratch git repo in
`/tmp/r54/repo` holding committed entry/body bytes; seven committed variants tested.
No installs performed; pacman untouched.
