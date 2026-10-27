## Round-60 criteria

- **A gate's status label is re-derived from a run at the revision being measured, and a round that
  reddens a live gate relabels it with its pin before the counter scores.** The registry's `Kind` cell
  is a claim about when the row may be red, so it is read against observed exits and not remembered
  from the round that registered the counter. At the round-60 base the claim does not hold for much of
  the population: 12 of the 28 members of the round 48–59 population carry no row at all
  (`unregistered`: c48 ×2, c49 ×2, c50 ×2, c51 ×2, `c52_gate_registry`, `c52_mutation_ladder`, c54 ×2),
  `c53_gate_truth.py` carries `live` and exits 1, and `c57_idresolver_gate.py` carries `live` and exits
  2 without `--fleet` — three reds a reader of the registry cannot see, and one class the registry had
  no word for, a gate that has never been green (`never met`, written with a space because the parse
  is a substring of the `Kind` cell; `never-met` reads as `live`). A label a later round invalidates is
  re-derived, not renamed after the fact: round 59's C9 insertion reddened the live
  `readme-index-counter` (`index_mismatches=1 … head_changed=1: crawler-identity.md`), wave 1 had
  predicted it, and the row was marked `historical` only once the no-harm reviewer ran the gate, so the
  relabel is the trade's only record. The duty is therefore prospective: before the contract freezes,
  every non-`historical` row runs on a scratch draft of the after-state, and a gate the claim must
  redden is named in the contract with its disposition — `historical` with the first 40-hex revision of
  its `Kind` cell as a pin that is an ancestor of the measured revision, or the claim reshaped — with
  the contract saying why when neither; a relabel made after the counter has scored is a second defect.
  Round 60's own instance: rows S427–S429 grow the registry from 164 to 167 while the live round-59
  `crawler-identity-quote-truth-counter` requires `registry rows == mirror rows + 2` (162 + 2), so it
  goes `historical` at its measured revision before the after-state is measured. Grounding:
  `corpus/lessons/round-60.md` §Mistakes (gate-collision; status label); `corpus/lessons/round-59.md:175`
  (the gate-collision row) and `corpus/QUALITY.md` round 59 ("A frozen claim never silently turns a
  standing gate red"); `corpus/lessons/round-59-verifier-spotcheck.md` §6 R59-D1;
  `considerthese/2026-10-26.md:33` (proposal 5, the historical-gate list); `SKILL.md` § Round 60
  gate-status ledger. Falsifier: `python3 -B .ufo/waves/round-60/c60_gate_status.py --root . --revision
  <rev>` must print `members=28 mismatches=0 scores_held=3 met=True`; at the round-60 base it exits 1
  with the 12 `unregistered` members and the two live reds, and the selftest's score-only mutant
  (calibration 2 → 10, nothing else) must fail `scores_held`. Example that fails it: a `Kind` cell
  reading `never-met` with a hyphen — the row parses as `live`, and a gate that has never been green is
  advertised as a standing promise; or a `historical` row whose pin is a later commit, which fails
  `pin_not_ancestor`.
