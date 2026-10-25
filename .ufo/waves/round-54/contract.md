# Kake round 54 — frozen contract (predicates declared before any data)

Lane: kake-shokunin. Base revision for controls: `68228b2d74e7930ae4f07e90e382a0d03ab80c7b`
(lane master tip at round open). This file is committed before any claim data is
measured and before any seat scores. The predicate sentence below is the same
sentence in the plan, in the counter's code, and in every receipt label.

## Claim C1 — calibration: S374 crawl-qualifier repair

Surface: the lane's self-assessment of the S374 source phrase in
`corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` — the round-53
non-author closure ruled quality harmed because the entry renders
「巡回を推奨していない」 as endorsement-only, dropping the crawl qualifier.
The calibration move is to bring the lane's rendered claim into alignment
with the retained source; the repair is appended, never rewritten.

- Before: the entry contains one rendering cell that describes the S374 phrase
  with endorsement/refusal vocabulary and without crawl vocabulary (the gloss
  `(rendered: the site owner is taken to consider the link target's page one it
  does not recommend, or a link it cannot vouch for)`), and no correction block
  supersedes it. Mismatch count = 1.
- After: that rendering cell is superseded by an appended
  `[r54-correction 2026-10-25]` block which quotes the exact source substring
  「このリンク先のウェブページの巡回を推奨していない」 and states the crawl
  qualifier with English crawl vocabulary. Mismatch count = 0.
- Counter: `python3 -B .ufo/waves/round-54/c54_s374_calib.py --root <lane> --revision <rev>`
- Predicate (frozen): **S374 qualifier: mismatches = rendered cells missing the
  crawl qualifier and not superseded by an r54 correction block; met when 0.**
- Kill rule: exit 0 iff met; exit 1 if not met; exit 2 unevaluable; 64 usage.
- Do-nothing control: run at base `68228b2d` must print `mismatches=1 met=False`
  and exit 1 (committed receipt).
- Junk control: a constant `met=True` implementation must not be the counter
  (mutation-testers attack).

## Claim C2 — operability: round-53 wave settlement + c53 gate registry row

Surface: the lane's operational artifacts — the SKILL.md "Owned freshness gate
registry" table, and round-53 dispatch/settlement evidence (40 seats spawned,
0 committed reports; seven lost report names enumerated by the non-author closure).

- Before: no registry row names `c53_gate_truth.py`; no settlement manifest
  exists; the 7 cited seat-report filenames are unresolved and unrecorded.
- After: (P2.1) the SKILL.md gate-registry table has a row for
  `c53_gate_truth.py` with kind `gate`, an entry command naming the script, a
  verdict map, a selftest spelling, a pinned/frozen proof path, a write scope
  and an owner; (P2.2) `.ufo/waves/round-53/settlement.md` is committed and
  records, per cited seat-report filename, `resolved:` or `lost:` with a
  reason; (P2.3) every `w1/` seat-report filename cited by `corpus/lessons/round-53.md`
  and the closure's named loss list is covered by the manifest.
- Counter: `python3 -B .ufo/waves/round-54/c54_ops_debt.py --root <lane> --revision <rev>`
- Predicate (frozen): **Round-53 ops debt: registry row present, settlement
  manifest committed, and every cited w1 seat-report name recorded resolved or
  lost; met when all three hold.**
- Kill rule: exit 0 iff all three hold; exit 1 otherwise; exit 2 unevaluable;
  64 usage.
- Do-nothing control: run at base `68228b2d` must print
  `registry=absent manifest=absent uncovered=4` and exit 1 (committed receipt; the 4
  are the names explicitly cited in the lane's round-53 lesson/closure file bytes).

## Maintenance item (not a claim): CJK quote-length accounting

Documented in `corpus/QUALITY.md` (appended criterion, round 54): the inherited
round-52 `units()` convention counts each CJK character as one unit and each
non-CJK whitespace token as one unit. This differs from literal “word” counting
in CORPUS.md rule 1; S367/S372/S373's 31/27/27 units do **not** prove compliance
with the ≤25-word rule. Their exact CJK word segmentation remains ambiguous;
this maintenance item records counts as units and does not claim the quotes
meet the word ceiling. The count is re-derived at the measured commit in the
report.

## Sourced claim

C1 rests on the S374 row, re-opened this round against the retained body
`.ufo/waves/round-52/sources/S374.html` (sha256
`3ad358bdbe7a74798df151c282e4b57af7475686dc405b3f8bad08f68881aecb`).
