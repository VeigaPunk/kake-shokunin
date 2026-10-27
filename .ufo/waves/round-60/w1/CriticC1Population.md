# CriticC1Population

POPULATION:

- Census at `97cdc122…` verified byte-exact: `git ls-tree -r --name-only <rev> -- .ufo/waves` (17,779 paths) → the same-N regex
  `^\.ufo/waves/round-(N)/(?:[a-z0-9-]+/)?c(N)_[a-z0-9_]+\.py$` matches 45 files lane-wide; 28 with `48 <= N <= 59`
  (c48 ×2, c49 ×2, c50 ×2, c51 ×2, c52 ×4, c53 ×1 under `exec-quality-gate/`, c54 ×2, c55 ×2, c56 ×2, c57 ×3, c58 ×3, c59 ×3) —
  the contract's own enumeration is correct.
- The excluded same-shape set is real, not hypothetical: **17 counters at rounds 42–47** (r42 ×4 incl. `draft1/c42_count_draft1.py`,
  r43 ×1, r44 ×4 incl. `c44_placebo.py`, r45 ×4, r46 ×1, r47 ×3). None has a SKILL.md `Entry command` row at base — `c42_count_v3.py`
  (prose L1185), `c46_matrix.py` (inside a *Pinned values* cell, not an Entry command), `c47_registry_count.py` (prose L1193) are
  mentions, not registrations. Under the claim's own row rule, including the range `42 <= N` would add **17 `unregistered`
  mismatches** — the same class the claim already measures, not a new structural class.
- Disclosure defect (fixable): the parenthetical "Rounds 40–47 counters are outside the population (not claimed)" conflates two
  exclusion mechanisms and understates the tail. Rounds 40–41 counter files exist (`c1_count.py`, `c1_count_v2.py`,
  `oracle_crosscheck.py`) but fall out by the *same-N* rule, not the range; rounds 1–41 `c1_`/`c2_`-era counters (r24 `c1_selftest.py`,
  r28–34, r37 `c2_mutkill.py`, …) are also unclaimed and unnamed anywhere. The regex is the frozen predicate, so the boundary is
  honest as a *rule*; the *prose* should name the excluded set precisely ("rounds 42–47 same-N counters: 17 files, all
  unregistered, unclaimed").
- Cherry-pick test (strongest available): the documented defect origin sits just outside the bound — SKILL.md L1188–1193
  ("Round 47 gate registry additions (r46 closure routed defect R1) — Neither round-46 tool carried a registry row at landing")
  shows the registry-omission defect was born at r46/r47, and r47's fix registered the *tools* while its counters
  (`c46_matrix.py`, `c47_registry_count.py`…) stayed unregistered. A claim auditing registry-label honesty whose population begins
  one round after the motivating defect looks favorable-shaped. Mitigation that keeps the verdict honest: exclusion only cuts
  toward *more* required work (more `unregistered` mismatches), the bound is declared pre-data, and the in-range set still
  contains 12 unregistered members — the lane did not fence out a class it would fail on while claiming green inside.
- `never-met` is a latent class: zero members carry it at base, and every `never-met`-shaped counter (e.g. `c44_placebo.py`,
  `c44_probe.py`) lives in the excluded rounds. Latent rules are fine, but w2 should probe a never-met-labelled member.
- Observed exits at base (shared clone detached at `97cdc1`, env scrubbed, TMPDIR=scratch): live members — `c52_wave_ledger` 0,
  `c56_selftally` 0 (all rows OK), `c57_idresolver_gate --fleet /home/vgpnk/Projects/shokunin` **0 (5/5)**,
  `c58_receipt_rewrites` 0, `c58_resolver_cases` 0 (14/14), `c59_axis_evidence` 0, `c59_resolver_cases` 0, `c59_quote_truth` 0;
  `c53_gate_truth` **exit 1** (2/7: L1/L2/L3/R1/R2 red) → `live_not_green` = 1. Historical check: `c52_quote_truth` green at pin
  `1ae8de5d`, red at base (C8 mirror 164≠148) — label honest. All 7 pins are ancestors of base (`merge-base --is-ancestor` ×5).
  `git log -S` shows the 12 unregistered members were *never* registered (registry omission, not rot).
- **Before-note inconsistency (flag to counter builders):** the contract predicts "`c57_idresolver_gate.py` labelled live, exit 2
  without `--fleet`". The claim's own command rule substitutes `<fleet root>` → the fleet root, and the registered command string
  carries `[--fleet <fleet root>]`; run that way the gate exits **0** (verified). Under the frozen substitution rule the expected
  base is exactly 13 mismatches (12 unregistered + c53), not the implied 14 — the `>= 13` do-nothing control still holds, but
  builders must substitute placeholders literally and must NOT drop `--fleet`. Residual fragility: c57's gate reads *live* sibling
  registries (`git show HEAD:`) at run time, so `e_T` can drift with sibling lanes between freeze and measurement — the version-1
  receipt should record the observed fleet state.

AXIS:

- Correctly assigned. AXES.md: calibration = "Self-assessment quality: gaps named honestly… SHONEN.md/SCORECARD entries match
  observed repo state". The Kind-cell status labels are self-assessment claims about gate liveness, and the counter measures
  label-vs-observed-exit mismatches — the same shape as round 56's admitted C1 (SKILL.md tally cells vs observed selftest
  tallies; the r56 spot-check admitted it as calibration while holding the score). Round-56 precedent + the AXES.md letter both
  support the calibration filing.
- Caveat, not defect: a `live` label is also an operability instruction (a live gate is what the lane runs now), so a wrong label
  is simultaneously a calibration failure and an operability gap; r56 §3 and this contract both leave calibration-vs-operability
  ownership to the operator (still open, L0 row of r59). If the operator rules it operability, the claim re-files without losing
  the measurement — operability sits at 10/saturated while calibration is the lane's lowest non-retired axis (2), so the
  lowest-axis obligation is served either way.

R59-D2:

- Real fix, not vacuous. R59-D2 verbatim: "C1's calibration score cell is unchecked; add the owned-axis score to the next
  axis-evidence counter and show it able to fail." c59 code confirms the gap — `HELD = ("operability","freshness")`, predicate
  `scores_held == 2`; calibration was read for mismatches but never held. c60 requires `scores_held == 3` over the three named
  rows at base values (10/10/2) — the cheapest cheat (fix labels, quietly bump calibration 2→10) now fails the predicate.
- Precondition verified, so the guard is satisfiable: base `SCORECARD.md` axis-table rows carry exactly operability 10 /
  freshness 10 / calibration 2 → `scores_held == 3` is met at base, i.e. the term binds a true state, not an impossible one.
- Residual weaknesses for w2/mutation seats: (a) the spec sentence must be implemented as a name→score binding; a score-multiset
  check ({10,10,2} among any three rows) would pass a row-rename cheat — the required mutant (move only the calibration score)
  does not cover that case; (b) `scores_held` hard-codes base values — correct for a frozen "no score change" declaration, but any
  post-data re-pin in version 2 is a loosening that must be named per the contract's Counter versions rule; (c) the guard proves
  the score didn't move, not that 2 is honest — score honesty stays operator/L0 territory.

VERDICT: Population count is exact and the cut is disclosed, but the r42–47 tail (17 same-shape unregistered counters, including the defect's birthplace) needs naming rather than "(not claimed)"; calibration is the right axis per AXES.md + r56 precedent; `scores_held == 3` is a real, satisfiable R59-D2 fix — and the contract's c57 "exit 2 without --fleet" before-note is wrong under its own `<fleet root>` substitution (verified green), so the counter must substitute placeholders literally and expect exactly 13 base mismatches.
