# CriticC2Predicate — frozen C2 sentence vs counter PREDICATE vs operational conditions

Scope: `.ufo/waves/round-54/contract.md` Claim C2 (lines 35–58) vs
`.ufo/waves/round-54/c54_ops_debt.py` (`PREDICATE` line 33; checks lines 48–91).
Checked against committed bytes at base `68228b2d74e7930ae4f07e90e382a0d03ab80c7b`.
No edits; findings only.

## 1. Predicate label — match, not verbatim-identical

Frozen sentence (contract.md:51–53, bolded, includes trailing period inside the
bold):

> Round-53 ops debt: registry row present, settlement manifest committed, and
> every cited w1 seat-report name recorded resolved or lost; met when all three hold.

`PREDICATE` (c54_ops_debt.py:33) is character-identical through "hold" and drops
only the sentence-final period. Printed verbatim as the receipt label (line 104).
No predicate-label mismatch in substance.

## 2. Condition ledger — all three conjuncts gated; two qualifiers unenforced, two uncontracted gates added

| Contract condition | Counter mechanism | Status |
|---|---|---|
| P2.1 registry row in `### Owned freshness gate registry` | heading-scoped scan (lines 62–71), `all(token in line for REQUIRED)` | enforced; nit: `"gate"` token is satisfied vacuously — it is a substring of `c53_gate_truth.py`, so a row with no kind column still passes |
| P2.2 `.ufo/waves/round-53/settlement.md` committed, per-name `resolved:`/`lost:` **with a reason** | `manifest_raw is not None` + `MANIFEST_RE` pipe-table rows `|name|resolved|lost|` | enforced **except "with a reason"**: `MANIFEST_RE` matches a bare 2-column `| Foo.md | lost |` row — no reason column required |
| P2.3 every `w1/` name cited by lesson + closure loss list covered | `cited ⊆ settled` via `NAME_RE` on lesson+spotcheck **plus** hardcoded `REQUIRED_SEAT_NAMES ⊆ settled` | enforced; gap: `NAME_RE` only matches `.ufo/waves/round-53/w1/<name>.md` path-prefixed citations |

### Citation coverage at base (verified)

- Lesson `corpus/lessons/round-53.md` cites 4 path-prefixed names
  (ReviewerProvenance, CriticCrossLane, ScoutS329, ScoutQuarantine) and 3
  bare-filename mentions (ScoutS312, CriticLocators on line 13; ScribeGate on
  line 15).
- Spotcheck loss list (line 73) names all seven, only ReviewerProvenance
  path-prefixed.
- Union = the 4 regex-visible names; the 3 bare names are covered solely by the
  hardcoded `REQUIRED_SEAT_NAMES`. `uncovered=4` at base matches the committed
  do-nothing receipt ("the 4 … explicitly cited" = path-prefixed form).

## 3. Counterexamples

**(a) False negative — counter stricter than the frozen predicate.**
`manifest_ok` (line 81) adds `has_loss_basis`: the manifest must contain the
literal strings `40 spawned` and `0 [committed ]seat reports` (line 78–79), and
statuses must appear as lowercase pipe-table rows. A manifest that records all
seven names resolved/lost in a bullet list — e.g. `ReviewerProvenance.md — lost:
seat never wrote the file` — or phrases the basis as "zero committed reports"
satisfies every predicate conjunct yet exits 1. Similarly, a manifest phrasing
"0 committed seat reports" as "no committed seat reports" fails `has_loss_basis`.
These are met-by-contract states the counter rejects. In practice the settlement
was written to fit the counter, so no live false-negative; it is a spec gap.

**(b) False positive — P2.2's "with a reason" qualifier omitted.**
`| ScoutS312.md | lost |` with no third column matches `MANIFEST_RE` and lands in
`settled`; a seven-row reason-free manifest combined with a registry row yields
exit 0. The contract's after-state requires a reason per name; the predicate
sentence itself only says "recorded resolved or lost", so this is an
enforceable-qualifier gap between contract narrative and counter, not a sentence
mismatch.

**(c) Coverage hole — bare-filename citations invisible outside the frozen
seven.** If a future revision of the lesson cites `.ufo/waves/round-53/w1/` seat
reports by bare name only (as ScoutS312/CriticLocators/ScribeGate already are),
any *eighth* such name escapes both `NAME_RE` and `REQUIRED_SEAT_NAMES` — the
predicate conjunct "every cited name recorded" would pass unchecked. Inert at the
frozen revision; load-bearing only via the hardcoded superset.

**(d) Kill-rule nit (shared with C1 counter).** Missing `--revision` exits
argparse's 2, colliding with the "unevaluable" code and violating the contract's
`64 usage` kill rule.

## 4. Impacted axes

Correctness/faithfulness: counter is stricter than the frozen predicate in two
places (loss-basis strings, pipe-table format) and looser in one (reason
qualifier) — the predicate is still falsifiable and the do-nothing receipt is
consistent, but the counter is not the weakest faithful test of the sentence.

## 5. Smallest safe correction

1. Require a non-empty third column in `MANIFEST_RE` (`\|\s*[^|]+\|`) to restore
   the "with a reason" qualifier — one regex change, no contract edit.
2. Either codify the loss-basis line and table format into the contract's After
   clause, or drop `has_loss_basis`/format anchors from `manifest_ok` so the
   counter tests exactly the frozen conjuncts.
3. Extend `NAME_RE` to catch `w1/<name>.md` and trailing bare `X.md` mentions, or
   codify the seven-name superset as *the* citation list in the contract.
4. Parse `--revision` manually (or catch `SystemExit`) to exit 64 on usage
   errors.

Verdict: no predicate-label mismatch; no operational condition omitted — but the
counter adds an uncontracted fourth gate and drops the P2.2 reason qualifier.
Fixable defects, not a canonical-judge rejection of the approach.
