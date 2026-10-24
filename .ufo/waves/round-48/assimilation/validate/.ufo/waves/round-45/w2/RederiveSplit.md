# RederiveSplit — C2(c) correction re-derivation (round-45 wave 2)

Seat: `kake-r45.RederiveSplit` (falsify wave). Target: independently re-derive the
witness split from the **named claim receipt**
`.ufo/waves/round-44/verification/claim/after-final/after-v5.json`
(sha256 `9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1`), confirm
`26 class-only + 1 mixed + 0 met`, confirm `22/1/4` comes **only** from the earlier
`verification/claim/after-v5.json` (sha256 `2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902`),
and verify the SCORECARD append names both sha256s correctly.

Read-only over the lane. Methods used: pure-Python re-derivation, the runner's exact
jq expression run read-only, a tree-wide receipt scan, an alternate-definition attack,
and execution of the frozen counting command from a scratch mirror (the runner writes
`verification/freshness/freshness.json`, so it was never run in-tree).

## Verdicts on the named attack

| # | Question | Result |
|---|---|---|
| 1 | Named receipt re-derives as 26 class-only + 1 mixed + 0 met | **PASS — confirmed** |
| 2 | 22/1/4 comes only from the earlier receipt | **PASS — confirmed** (unique derivation in tree; pre-G6 reruns move the tuple) |
| 3 | SCORECARD append names both sha256s correctly | **PASS** (named receipt full 64-hex exact; earlier receipt abbreviated `2383efae…ce0902`, prefix/suffix exact and unique — full 64-hex not printed, completeness note only) |

Net: the C2(c) falsification recorded in the SCORECARD append is correct, and the
corrected tuple is the receipt's own measurement, not a substitution.

## Decisive commands and verbatim output

### 1. Receipt identities (both match the assignment)

```
$ sha256sum .ufo/waves/round-44/verification/claim/after-final/after-v5.json \
            .ufo/waves/round-44/verification/claim/after-v5.json
9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1  .ufo/waves/round-44/verification/claim/after-final/after-v5.json
2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902  .ufo/waves/round-44/verification/claim/after-v5.json
```

### 2. Independent derivation from `rows` (not the runner's code path)

```
$ python3 -B - <<'PY'
import json,collections
for p in ('.ufo/waves/round-44/verification/claim/after-final/after-v5.json',
          '.ufo/waves/round-44/verification/claim/after-v5.json'):
    d=json.load(open(p)); c=collections.Counter()
    for r in d['rows']:
        cc=len(r.get('classCaught') or []); lc=len(r.get('legacyCaught') or [])
        if r.get('met'): c['met']+=1
        elif cc>0 and lc==0: c['class_only']+=1
        elif cc>0 and lc>0: c['mixed']+=1
        else: c['other']+=1
    print(p, dict(c), 'rows',len(d['rows']),
          'witnessed',d['witnessed'],'notMet',d['notMet'],'ok',d['ok'])
PY
.ufo/waves/round-44/verification/claim/after-final/after-v5.json {'class_only': 26, 'mixed': 1} rows 27 witnessed 27 notMet 27 ok True
.ufo/waves/round-44/verification/claim/after-v5.json {'class_only': 22, 'met': 4, 'mixed': 1} rows 27 witnessed 23 notMet 23 ok False
```

Totality per receipt (so the tuple cannot be hiding dropped rows):

```
after-final/after-v5.json  rows=27 class_only=26 mixed=1 met=0 other=0 sum=27
claim/after-v5.json        rows=27 class_only=22 mixed=1 met=4 other=0 sum=27
```

Row-type sanity: all 27 rows in the named receipt carry boolean `met` and list
`classCaught`/`legacyCaught`; `classCaught` is always a subset of `classKeys`
(G1–G10); `metNames` equals the set of rows with `met==true` in both receipts.

### 3. The runner's exact jq expression, read-only

```
$ jq -r '.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length, mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length, met: map(select(.met==true))|length}' .ufo/waves/round-44/verification/claim/after-final/after-v5.json
{
  "class_only": 26,
  "mixed": 1,
  "met": 0
}
$ jq -r '...same...' .ufo/waves/round-44/verification/claim/after-v5.json
{
  "class_only": 22,
  "mixed": 1,
  "met": 4
}
```

Identical to the committed `.ufo/waves/round-45/verification/witness-split/split.json`
(`receipt_sha256` = `9dead4d7…076d1`, `jq_output_verbatim` = `26 / 1 / 0`).

### 4. 22/1/4 exclusivity — tree-wide scan

```
$ python3 -B (scan .ufo/**/*.json + corpus/**/*.json; keep dicts with non-empty rows[0].met;
              classify exactly as above)
scanned 2384 json files, 31 receipt-shaped (rows+met)
files yielding 22/1/4:
   ('.ufo/waves/round-44/verification/claim/after-v5.json',
    '2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902',
    {'class_only': 22, 'met': 4, 'mixed': 1})
```

One hit, the earlier receipt. Other receipt-shaped artifacts do not produce it, e.g.
`after-final/after-v5.json` 26/1/0, `w2-baseline/run1` 21/2/4, `w2-baseline/run2`
23/0/4, `v4-final/v4.json` met 27, `placebo-final/placebo.json` met 26.

Same-counter confirmation (all five receipts: `counterSha256` prefix `5cedaa3b9f918979`,
controls 27): the tuple is a property of the run, not of different bytes.

### 5. Alternate-definition attack (could another plausible definition yield 22/1/4 on the named receipt?)

Classifying by `witnessedByClass` restricted to `classKeys` (T5/C treated as non-class)
instead of row `classCaught`:

```
after-final/after-v5.json  {'class_only': 26, 'mixed': 1}
claim/after-v5.json        {'class_only': 22, 'met': 4, 'mixed': 1}
```

Same tuples under both definitions. No definition tried reproduces 22/1/4 from the
named receipt.

### 6. Frozen counting command, executed from a scratch mirror (in-tree would write)

```
# scratch mirror: copy of c45_freshness.py (byte-identical, sha below), round-44 and
# mutants/v6v4 symlinked read-only, LANE redirected to /fast/scratch/hyaku/kake-r45/RederiveSplit/lane
$ cd /fast/scratch/hyaku/kake-r45/RederiveSplit/lane && python3 -B .ufo/waves/round-45/c45_freshness.py
selftest_kills before=2/4 after=4/4
v4_predicate_names_class_runs before=true after=false
witness_split class_only=26 mixed=1 met=0
FRESHNESS_RAN_OK
exit=0
$ sha256sum .ufo/waves/round-45/c45_freshness.py   # copied script
46e6a89c5221b5c4877baeb0b23da6aa0b85d9b7a9e1706c736b177b692a3186
$ sha256sum <lane>/.ufo/waves/round-45/c45_freshness.py
46e6a89c5221b5c4877baeb0b23da6aa0b85d9b7a9e1706c736b177b692a3186
```

No mutation of the lane: in-tree `verification/freshness/freshness.json` mtime
`2026-10-24 00:56:55`; scratch run wrote its own receipt at `00:58:43`. The runner
contains no literal target tuple (`grep -nE "22|26|expected|MET"` hits only the docstring,
the MET sentence, and the print format) — it cannot emit 22/1/4 unless measured.

### 7. SCORECARD append sha citations

```
$ python3 -B (parse SCORECARD.md lines 3711-3775 = the appended section)
named full sha occurrences in append: 1
earlier abbreviated token: '2383efae…ce0902'
abbrev prefix ok: True | suffix ok: True
append mentions 26 class-only: True | 1 mixed: True | 0 met: True
append mentions 22/1/4: 1 | 22 class-only: 1
3762:   `9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1`), which re-derives as
3763:   **26 class-only + 1 mixed + 0 met** (`verification/witness-split/split.json`). The 22/1/4 tuple
3765:   `2383efae…ce0902`) — found independently by four wave-1 seats. Correction filed append-only
```

Uniqueness of the abbreviation: a hash sweep over the working tree (files ≤ 8 MB, `.git`
excluded) finds exactly one file whose sha256 starts `2383efae` or ends `ce0902` — the
earlier receipt. The abbreviated citation is unambiguous. The `22/1/4` mentions in the
append are (a) quoting the frozen target and (b) naming which receipt owns it, never a
measured value.

Frozen-declaration context: the frozen C2 block's own counting command writes
`--out .ufo/waves/round-44/verification/claim/after-final/after-v5.json`
(`SCORECARD.md:3602-3611`), so "the round-44 claim receipt" is the `after-final` file;
its split is 26/1/0. This confirms the append's receipt-identity diagnosis rather than
resting on the append's own wording. The append is positionally after the frozen block
(line 3711, file ends 3775) and does not edit it.

## Findings

### No blocker or high-severity finding. The attacked correction holds.

**L1 (LOW, instrument totality) — split leg cannot detect dropped rows.**
`c45_freshness.py:48-57` emits only `class_only`, `mixed`, `met`; `main()` (`:90-97`)
accepts the leg whenever the jq call succeeds, with no `sum == len(rows)` or `other`
assertion. A receipt with a non-met row whose `classCaught` and `legacyCaught` are both
empty would silently shrink the triple and still print `FRESHNESS_RAN_OK`. Effect on
this claim: none — the named receipt's `other=0`, `26+1+0=27`; verified above. Fix (not
applied, out of my write path): have the runner also emit `other` and `rows`, and fail
the leg when they disagree.

**L2 (LOW, reproducibility) — the split leg depends on an external `jq`, which on this
host is jaq.**
`command -v jq` → `jq`; `jq --version` → `jaq 3.1.1`; `python3 --version` → `Python 3.14.8`.
Results were cross-checked with pure Python and agree exactly, so there is no observed
divergence; recording it because a different jq/jaq build is a silent input to leg (c).

**I1 (INFO, receipt data model) — `witnessedByClass` contains out-of-domain keys.**
`classKeys` is G1–G10, but `witnessedByClass` maps `repeat-len-band → ['G7','T5']` in the
named receipt and `→ ['G7','T5']` with an additional `C` key elsewhere in the earlier
receipt (`C`/`T5` in the earlier receipt's value union). A reader counting "any
witnessedByClass entry" as a class witness would count 27 class witnesses for the named
receipt, not 26, and would lose the mixed row. The split's authoritative fields are row
`classCaught`/`legacyCaught` (T5 is a timing/legacy key: `legacyCaught` union = `['T5']`
for the named receipt, `['C','T5']` for the earlier). The corrected tuple is consistent
with the authoritative fields; flagging the latent ambiguity, not a claim defect.

**I2 (INFO, supporting datum) — 22/1/4 is a single pre-G6 draw, not a stable baseline.**
Pre-G6 reruns with the same counter (`5cedaa3b…`) yield `w2-baseline/run1` 21/2/4
(sha `86c7c429…a2d0`) and `run2` 23/0/4 (sha `f6f9a5fe…694c4`); only the original
`claim/after-v5.json` yields 22/1/4. The moving element is the legacy `C` key
(`legacyCaught`), which changes `mixed` and `met` counts. This strengthens the append's
diagnosis (misattributed pre-final draw, not a reproducible property of "the round-44
claim receipt") and is not contradicted by anything in the append.

## Residual risk and verification gaps

- **Unrun in-tree by design:** the frozen counting command was executed from a
  byte-identical copy (sha `46e6a89c…3186`) with `LANE` redirected; running it in-tree
  would rewrite committed `verification/freshness/freshness.json`. In-tree mtime predates
  my run, so the lane is unmutated by this seat.
- **Revision scope:** all derivation is on working-tree bytes at the current tip. I did
  not re-execute the `git show 3b4c430a:…` check that `w1/CriticC2Scope.md` reports; the
  named receipt's sha256 matches the value `round-44/w2/CriticKillRules.md:237` recorded
  for the same path, which is consistent with no drift, but no git-history check was run
  here (bounds discourage routine git subcommands).
- **Legs (a)/(b):** my scratch execution printed `2/4 → 4/4` and `true → false`, matching
  the declaration, but I did not independently audit the mutant construction or the v6
  v4 receipt beyond that run — those are other seats' axes.
- **Scan coverage:** exclusivity rests on 2384 JSON files (`.ufo/**`, `corpus/**`, ≤ 8 MB)
  with 31 receipt-shaped; non-JSON derivations are not machine-checkable and textual
  mentions of `22/1/4` are quotes of the frozen target, not measurements.
- **Not attempted:** full 27-row replay of `c44_count_v5.py` per control (regression
  seats' scope).

## Files written

- `.ufo/waves/round-45/w2/RederiveSplit.md` (this report — the only lane write)
- `/fast/scratch/hyaku/kake-r45/RederiveSplit/lane/` scratch mirror: `c45_freshness.py`
  copy, `round-44/`, `mutants/`, `verification/v6v4/` symlinks, generated
  `verification/freshness/freshness.json`
- Tools installed/updated: none.
