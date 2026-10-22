# Round 28 wave 1a3 — QualityCriteriaDraft (leaf scribe)

Seat: `KakeR28a3.QualityCriteriaDraft`. Scope: round-27 routed defects 2–4
(round-27-verifier-spotcheck.md lines 69–74) → lesson-backed QUALITY.md
criteria. Defect 1 is out of scope (repaired by C1).

## Method
Read `corpus/lessons/round-27-verifier-spotcheck.md` (defects at 69–74),
read `corpus/QUALITY.md` in full, and grepped QUALITY.md/corpus for
`no-harm`, `policy-stop`, `void`, `timeout`, `overrun`, `granularity`,
`finding-id`, `multiset` to test for existing carries. No tools installed
or updated.

## Per-defect verdicts

### Defect 2 — C1 review-presence vs strict-support distinction; 7 unknown units / 3 pairs unresolved, not counted decided
**Carried by existing criteria.**
- `corpus/QUALITY.md:256-259` (round-27 section): "A pair review is not a
  universally true file or a HOLD for each statement. Preserve inherited
  UNVERIFIABLE units by identity and do not rewrite earlier units to increase a
  later tally. A syntactic completeness gate and a source adjudication ledger
  are different evidences."
- `corpus/QUALITY.md:274-280` (Strict-status refinement): "inventory carried
  UNVERIFIABLE subunits before promising all-pair HOLD/supported-STALE.
  `seatUnverifiable>0` is not erased by a durable review record... the counter's
  current-consumer selftest must reject that real input... not invent a clean
  fixture or reinterpret a review tally as supported truth." Grounding:
  round-27 lesson Strict C1 section, `strict-c1-disposition.json`.
No draft needed.

### Defect 3 — conformance exceptions visible (void stub smoke, 3600 s timeout, report overruns); fixture-oracle granularity = exit + finding-id multiset only
**Not carried.** No QUALITY.md mention of the named exceptions, empty timeout,
overrun identities, or oracle comparison granularity (grep: zero hits for
`void`/`timeout`/`overrun`/`granularity`/`finding-id`/`multiset`; closest
proxy, line 285-286 "id-only fixture tally", states an admission rule, not
the runner's comparison granularity). Draft:
> Recorded conformance exceptions stay visible and void: a prohibited
> mid-flight stub-gate smoke is VOID acceptance evidence with no credit, a
> scratch job that times out with no counter or output gains none, and
> report-length overruns are kept named by identity. State the fixture-oracle
> granularity on the record: the runner compares only process exit plus
> finding-id multiset, so finer semantic differences are outside what a
> passing comparison proves. Grounding:
> `corpus/lessons/round-27-verifier-spotcheck.md:57,73`
> (w1-outcomes.json `scopeVoidAcceptance`, w2-outcomes.json `probeTimeouts`).

### Defect 4 — preserve bounded no-harm scope, r24 policy-stop, out-of-population debt as they are
**Partially carried, partially drafted.** Carried: out-of-population debt →
`corpus/QUALITY.md:266-272` (scope disclosure: broader "every corpus statement"
policy remains open; the 18 knowledge pairs for excluded S014/S019/S035 are
recorded; "Neither a green pair count nor this clarification claims that
broader policy satisfied or retires it"). Not carried: bounded no-harm scope
and r24 policy-stop have no QUALITY.md criterion (grep: zero `no-harm` hits in
QUALITY.md; policy-stop lives only in lessons/README). Draft for the remainder:
> No-harm receipts keep the bounded scope they measured (named knowledge
> byte-prefixes, pre-existing scripts, prior wave files, logged registry
> cells) and never generalize into a universal no-harm or arbitrary CLI-safety
> proof; an unmeasured surface stays unmeasured. The round-24 L0 policy-stop
> disposition remains open, unretried and unrouted; a later round neither
> rephrases it into a green result nor silently drops it. Grounding:
> `corpus/lessons/round-27-verifier-spotcheck.md:45,61,74`.

## Notes
- Grounding paths are relative to `corpus/`; all quotes are verbatim from the
  current lane bytes (read at the committed worktree).
- The two drafts are plain English, ≤6 lines each, grounded in a lesson path
  (`round-27-verifier-spotcheck.md`).
- No other files were written; no repo state was mutated; no network access,
  no API calls, no tool installs. Defect 1 not addressed here by design.
