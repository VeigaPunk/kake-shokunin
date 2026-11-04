# Round 85 frozen contract — kake

Base: bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7. This replaces an uncommitted, undispatched planning draft; no seat scored that draft. Freeze occurs before ready-file dispatch. Two causally separable claims; neither claims the entire D84 queue closed.

## C1 — calibration (lowest owned score 2, HOLD)

The three round-84 verdict instruments missing from the registry home acquire complete discoverable registry rows: `c84_defect_queue.py`, `c84_policy_values.py`, `policy_value_class.py`. Target: complete=3/3, missing=0, from complete=0/3. The frozen count.py C1 predicate requires one eight-cell row per instrument, nonempty cells, filename in entry command, 0=/1= verdict mapping, --selftest, persisted .ufo/waves/ proof path, owner kake. It measures registry discoverability, not full semantic or gate conformance. policy_value_class remains experimental; selftest success never grants publication approval. D84-1 is the motivating routed defect; D84-2..4 remain explicitly open except for procedural mitigations.

## C2 — freshness (10, HOLD), bounded capability

Acquire an offline Referrer-Policy effective-token decoder, `scripts/referrer_policy_effective.py`. Input: stdin JSON list of string field values in response field order. Output: exactly one JSON object {"effective": <last recognized nonempty policy token, or empty string>}; process comma-separated tokens in order with surrounding whitespace stripped. Tokens compare case-sensitively. Valid tokens: no-referrer, no-referrer-when-downgrade, same-origin, origin, strict-origin, origin-when-cross-origin, strict-origin-when-cross-origin, unsafe-url. Unsupported input must fail with nonzero. Normal invocation exits 0 for decoded data, 1 for invalid data, 64 usage. Exposes --selftest with isolated fixtures and exit-code assertions.

Source: W3C Referrer Policy §8.1, opened GET-only by L1 this round; the algorithm sets policy to each recognized token in sequence. The new source row is S458, opened again by the source seat before registration. The claim does not upgrade or rewrite the round-84 experimental general classifier, nor assert arbitrary response-field equivalence. It is a separate, field-specific decoder with no publishing authorization.

Target: all ten frozen count.py CASES match (0/10 absent at base → 10/10). The oracle is committed in the counter before implementation. In particular reversing no-referrer and strict-origin must change the effective policy. Real trial: decode Referrer-Policy fields from the retained r84 control pair and report both effective values; this trial is separate from the ten-case numerator. No live property request is required or authorized.

## Measurements, controls, kill rules

For each claim:
`python3 -B .ufo/waves/round-85/count.py --root . --revision <rev> --claim c1|c2 --work /fast/scratch/hyaku/kake-r85/L1-count`

Before freeze dispatch, commit base receipts. Do-nothing control: same counter at the base must fail both targets. Prose-only registry rows without required fields must fail C1. Constant effective-token output must fail C2 because the expected tokens differ. Preserve these receipts. If either unchanged control meets its target, the claim is unprovable. A nonzero after measurement is unprovable; never narrow the ten-case population or retrofit expectations after a seat scores. New discovered defects are disclosed, not hidden by green syntax counts.

## Wave / ownership

One v1 wave of ten seats: scout 1, executor 3, scribe 2, reviewer 2, critic 1, connector 1. Attack share 3/10. L1 holds canonical planner because the validator forbids planner; ScoutSources carries the bounded planning data-walk. This does not silently settle the outside integrator's literal L2-planner disagreement.

All seats read production bytes only and write deliverables solely under their unique round-85 w1/<Seat>/ directory plus their exact scratch directory. No concurrent production writers: L1 alone integrates candidate code, registry rows and corpus text after WAVE-DONE. No seat commits/pushes/mutates jj. One ready file, no replacements. Operative config read before dispatch: all roles @m_zfl; no model argument. Scratch roots /fast/scratch/hyaku/kake-r85/<Seat>/, removed on exit.

## Frontier and mistakes

Census before/after required. S458 grounds C2. Lesson Gate includes admit and reject, URL/date/located ≤25-word quote. Mine the r84 blanket-reorder semantic mistake with the retained opposite-order witness and a red-before decoder measurement. Considerthese/2026-10-26.md proposal 5 is considered: distinguish historical red gates from regressions by explicitly documenting the r84 instruments' frozen scope and experimental status. No bulk staged-source assimilation; report Assimilation: none. No rank/SHONEN promotion is claimed.
