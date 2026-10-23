# ReviewScorecardR44 — SCORECARD.md round-44 internal-contradiction review

Seat: kake-r44.ReviewScorecardR44. Item: review the uncommitted `SCORECARD.md` round-44
section (`git diff SCORECARD.md`) for internal contradiction across the original C1/C2
declarations, amendment A (placebo before-state), amendment B (C2 scope), correction 2
(three instrument fixes), and the frozen predicate reading. Named checks: the quoted C2
counting command must be `--root .` with no `--spec`; placebo sha256 pins; the claim "no
receipt decided anything under the old classifier". Reviewer only — no edits, no verdict.

## Decisive commands and output

### Named check 1 — C2 counting command

The declaration's command still quotes `--spec` (SCORECARD.md:3481-3483); correction 2
item 3 (SCORECARD.md:3556-3560) supersedes it explicitly. The live checker's argparse
has no `--spec` and rejects it:

```
$ python3 -B scripts/ledger_latest_check.py --root . --spec .ufo/waves/round-44/ledger-quotes.json
usage: ledger_latest_check.py [-h] [--root ROOT] [--selftest]
ledger_latest_check.py: error: unrecognized arguments: --spec .ufo/waves/round-44/ledger-quotes.json
```

The working command (no `--spec`), run this session:

```
$ python3 -B scripts/ledger_latest_check.py --root .
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3575
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1703
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1706
ledger-quotes: 3 figures, 0 mismatches
EXIT=0
```

Matches the frozen correction-2 contract verbatim (`exit 0 met`); `ledger-after.txt` in
`verification/claim/` is byte-identical output. `--selftest`: `selftest: 2/2 passed`,
exit 0. **PASS.**

### Named check 2 — sha256 pins

```
$ sha256sum .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/c44_placebo.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  c44_count_v5.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  c44_audit.py
9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27  c44_placebo.py
```

All three pins in the text verify byte-exact (counter `5cedaa3b`, audit `8ee2c8bf`
= correction-2's "new sha256", placebo `9ce3acd4`). **PASS.**

### Named check 3 — "no receipt decided anything under the old classifier" (SCORECARD.md:3550)

Provenance by row schema: `verification/freeze/control-v4blind.json` and
`verification/placebo/before.json` rows lack `classCaught`/`legacyCaught` (old-driver
artifacts); `verification/claim/after-v5.json` and `canary.json` rows carry them
(new-driver, sha `8ee2c8bf…`). So exactly two receipts exist under the old classifier,
both the ones the text itself calls "inherited seat evidence … not the claim's
receipts". Both have classifier-independent verdicts (`caughtBy=['D']`/`['C']` and
`['G1']` only — witnessed under both `all` and `any` readings). Claim receipts are all
new-classifier. Statement is **TRUE as written**; nuance: amendment A *did* rely on the
old-classifier `control-v4blind.json` to pick the corrected before-state, so the
sentence is safe only because that receipt's verdict is classifier-independent.

## Traced-claim verification (all verified against committed bytes)

- Amendment A receipt facts verbatim vs `control-v4blind.json`: `witnessed=2, ok=false`,
  `buildscope-m5` run D seed `181346457990762`, `repeat-depth-deep` run C seed
  `5994504518804` — all match.
- "Four routed figures" (SCORECARD.md:3489) resolves: r43 spot-check §8 defects 1 (tally),
  5 (two LOG ratio figures) + 4 (wave composition) = the four; §8.7 is SOURCES-anchor
  contract work, not a figure. Consistent.
- C2 before state: `verification/ledger-before.txt` reads `3 figures, 3 mismatches`
  (18 vs 14; 4.27/8.68 vs 4.21/7.05; 1.00–1.02/1.13–1.18 vs 1.00–1.01/1.11–1.22),
  `.exit` = 1 — matches the declaration.
- Correction-2 item 1 mechanics: `c44_audit.py:63-66` `semantic_witness` uses
  `any(key in class_keys)`; selftest lines 84-97 include the mixed-key `["D","G3"]`
  fixture as described.
- Correction-2 item 2: `controls-27.tsv:26` now reads `buildport-m6  default_port  G2`;
  the named source `controls-r43/buildport-m6-default-branch.py:303-304` flips the
  default-port branch (`port = 80 if scheme == "http" else 443`) — a default_port,
  not portdigit, memo. Consistent.
- LOG.md round-44 entry (same diff) cross-references agree with the checker's
  current MATCH lines (4.21/7.05; 1.00–1.01/1.11–1.22; SCORECARD 14).

## Findings

### F1 (moderate) — placebo "cannot witness by construction" is falsified by the receipt cited two lines later

SCORECARD.md:3567-3568:

> The before-state remains the placebo counter (a byte-copy of v5 whose ten class
> modules all delegate to `cases_f`): **it cannot witness by construction**, and the
> measured k/27 it reaches is reported, not targeted. Attempt-1 receipts
> (`verification/freeze/control-v4blind.json`, `verification/placebo/*`) are inherited…

`verification/placebo/before.json` — the cited receipt, the k measurement itself —
reports `witnessed=1, verdict "witnessed 1/27 notMet=3 build met 3/3"`, with
`witnessedByClass: {"headtail-V8": ["G1"]}`. The placebo's G1 run *did* produce a
class-keyed divergence on `headtail-V8` (`caughtBy: ["G1"]`, `equalRuns 20/21`). So
"cannot witness by construction" is wrong as a statement about witness-count: k was
1, not 0. What the placebo construction guarantees is only that a class run adds no
*new* observational power (a G-run can only replay a v4-input divergence), not that
the witness counter stays at zero — a class-keyed `caughtBy` on identical-to-v4 input
still increments `witnessed`. Amendment A's own framing ("witnesses **k/27** … k is
measured, not targeted", SCORECARD.md:3518) does not promise k=0 and is consistent
with the receipt; the frozen-predicate-reading paragraph contradicts the same receipt
it names. Under the checker's semantics and the declared predicate this does not
change C1's status (k=1 < 27, `ok=false` either way), but the internal claim is
demonstrably false against the round's own committed evidence.

### F2 (minor) — amendment B "mismatches on both endpoints" is endpoint-inaccurate at the quoted precision it describes

SCORECARD.md:3528-3530 claims the exact-equality reading makes the build-ratio entry
"mismatch on both endpoints (quoted T1 1.00–1.02 vs recorded 1.004–1.009; quoted T5
1.13–1.18 vs recorded 1.105–1.215)". Endpoint-by-endpoint rounding to the quoted
2dp (the checker's `rounded_like`, verified): T1 lower 1.004→`1.00` = quoted 1.00,
**matches**; T1 upper 1.009→`1.01` ≠ 1.02; T5 lower 1.105→`1.11` ≠ 1.13; T5 upper
1.215→`1.22` ≠ 1.18. So three of four literal endpoints mismatch; the entry mismatches
on *both ranges*. The claim is true only if "endpoints" loosely means "the T1 and T5
ranges"; against the printed numbers the T1-low endpoint is a counterexample.
Residual: figure-level outcome (`3 figures, 3 mismatches`) unaffected — verified live.

## Checked and cleared (no contradiction)

- C2 counting command: declared `--spec` is superseded by correction 2 item 3; the
  section self-flags it ("superseded by this line"); the canonical command
  `--root .` exits 0 now. The predicate's mention of `ledger-quotes.json` stays
  accurate — the checker still loads it at fixed `SPEC_PATH` and validates it
  against `contract_spec()`.
- The declaration's stop rule (SCORECARD.md:3450, "if the before receipt is not
  27/27 blind, the round stops") vs `control-v4blind.json` `witnessed=2`: the rule
  did trip, and amendment A records exactly that outcome and replaces the
  before-state; the append-only convention deliberately leaves the original text
  standing. Tension by design, not a contradiction.
- Declaration's "Before: `witnessed 0/27`, `ok=true`" (SCORECARD.md:3445): falsified
  by the inherited receipt but explicitly superseded by amendment A
  (SCORECARD.md:3514 "replaces the '27/27 blind' premise"). Consistent with the
  frozen reading that v4-corpus divergences are never class witnesses — under that
  reading the claim "v4 corpus witnesses none" still holds (0 *class* witnesses by
  construction).
- Correction-2 ordering claim (`verification/claim/` empty at freeze): claim-dir
  receipts present today (`after-v5.json` 23/27 — the known open G6 build item),
  all new-classifier bytes. `claim/placebo-before.txt`, `v4-support.txt`,
  `after-v5-wave2-baseline.txt` exist but are 0 bytes — wave-2 run slots not yet
  populated; LOG.md names them as the receipt paths. No contradiction with any
  sentence in the diff.
- Predicate-reading paragraph's seed-dependence rationale: matches
  `control-v4blind.json` (2/27 diverging on fresh unseeded v4 runs).

## Verdict against the item's named attack

The named attack — internal contradiction across declaration / amendment A /
amendment B / correction 2 / frozen predicate reading — **partly lands**: two
contradictions found (F1 moderate: "cannot witness by construction" falsified by the
same paragraph's own cited placebo receipt, k=1; F2 minor: "both endpoints"
inaccurate at quoted precision). All three named checks pass: counting command
correct after supersession (`--root .`, no `--spec`, exit 0 verified live); all
sha256 pins byte-exact; "no receipt decided anything under the old classifier" true
on the deciding-vs-inherited distinction, with the noted reliance caveat.

Residual risk / verification gaps: I did not re-derive the placebo mechanism (why
G1 flagged `headtail-V8` — likely a v4-identical G1 input hitting a seed-dependent
divergence; the receipt records caughtBy only, not per-run inputs) — the finding
stands on the receipt's own `witnessed=1` regardless. The `914ebdee…` tool-sha pin
for the 020bc457 build was not re-hashed (outside the section's falsifiable text).
Zero-byte claim-receipt slots are placeholders, not evidence.

## Files written

- `.ufo/waves/round-44/w2/ReviewScorecardR44.md` (this report)
- `/fast/scratch/hyaku/kake-r44/ReviewScorecardR44/` (scratch dir, created; unused
  beyond creation — all decisive output fit inline)

No tool installs were needed (system python3, git, sha256sum sufficed).
Report: .ufo/waves/round-44/w2/ReviewScorecardR44.md
