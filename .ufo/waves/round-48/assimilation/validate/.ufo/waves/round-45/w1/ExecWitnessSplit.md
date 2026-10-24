# ExecWitnessSplit — witness split re-derivation

Axes: operability, freshness.

## Result

Ran the assigned jq re-derivation against the specified round-44 final claim receipt. The measured split is 26 class-only, 1 mixed, 0 met, and 0 other (27 total). **Fail against the item's expected 22/1/4/0 split**: the designated receipt does not reproduce the expected classification. I preserved the measured output rather than substituting the expected values.

## Exact evidence

Command:
```sh
jq -r '.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length, mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length, met: map(select(.met==true))|length, other: map(select(.met==false and (.classCaught|length)==0))|length}' .ufo/waves/round-44/verification/claim/after-final/after-v5.json
```

Verbatim decisive output:
```json
{
  "class_only": 26,
  "mixed": 1,
  "met": 0,
  "other": 0
}
```

Receipt hash command:
```sh
sha256sum .ufo/waves/round-44/verification/claim/after-final/after-v5.json
```

Verbatim output:
```text
9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1  .ufo/waves/round-44/verification/claim/after-final/after-v5.json
```

The receipt itself records `witnessed: 27`, `notMet: 27`, and `metNames: []` (source lines 21, 148, and 178); that is consistent with the observed zero `met` rows. This is the relevant blocker to filing the expected C2(c) split as stated.

## Files written

- `.ufo/waves/round-45/verification/witness-split/split.json` — command, receipt path/hash, and jq output preserved verbatim.
- `.ufo/waves/round-45/verification/witness-split/split.txt` — human-readable summary and output.
- `.ufo/waves/round-45/drafts/witness-split-sentence.md` — one-sentence SCORECARD draft naming the command and measured values.
- `.ufo/waves/round-45/w1/ExecWitnessSplit.md` — this report.

No build, test, lint, or formatter was run; no tools were installed. Scratch directory created: `/fast/scratch/hyaku/kake-r45/ExecWitnessSplit/`.
