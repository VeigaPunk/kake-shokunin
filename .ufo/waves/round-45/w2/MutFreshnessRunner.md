# MutFreshnessRunner — c45_freshness.py able-to-fail (round-45 w2, freshness)

Timestamp: 2026-10-24 00:57-01:00 -0300. No tool installs; no lane writes outside this report.
Scratch: `/fast/scratch/hyaku/kake-r45/MutFreshnessRunner/`.

## Target

`c45_freshness.py` (lane sha256 `46e6a89c5221b5c4877baeb0b23da6aa0b85d9b7a9e1706c736b177b692a3186`)
re-derives three C2 legs from committed bytes. Attacked point: its three *input selectors* — every
leg reads a hard-coded receipt path, and the script's success gate checks only that each leg returned
non-`None`/non-zero counts (`ok = v4_before is not None and v4_after is not None and split is not None
and before_kills + after_kills > 0`), never *which* bytes were read. The written receipt
(`verification/freshness/freshness.json`) records values but no source path and no source sha256
(`jq -c 'keys'` = `["ran_at_ns","selftest_kills","v4_predicate_names_class_runs","witness_split"]`;
`grep -c 'after-v5\|counter-v4\|source\|sha'` = 0).

**Hypothesis (the defect under test):** the runner cannot fail when any leg points at the wrong
receipt/mutant set; it prints the wrong values and still emits `FRESHNESS_RAN_OK`, exit 0.

## Harness (isolated replica)

`LANE = Path(__file__).resolve().parents[3]`, so a byte copy of the script was run inside a mirrored
tree under scratch (`lane/.ufo/waves/{round-44,round-45}/...`) holding byte copies of exactly the
receipts/mutants the honest script reads. No lane file was touched.

```
S=/fast/scratch/hyaku/kake-r45/MutFreshnessRunner
mkdir -p $S/lane/.ufo/waves/round-45/{mutants,verification/v6v4,verification/freshness} \
         $S/lane/.ufo/waves/round-44/verification/claim/{v4-final,after-final}
cp .ufo/waves/round-45/c45_freshness.py                 $S/lane/.ufo/waves/round-45/
cp .ufo/waves/round-45/mutants/m[1-4].py                $S/lane/.ufo/waves/round-45/mutants/
cp .ufo/waves/round-45/mutants/m[1-4]_v2.py             $S/lane/.ufo/waves/round-45/mutants/
cp .ufo/waves/round-44/verification/claim/v4-final/v4.json \
   $S/lane/.ufo/waves/round-44/verification/claim/v4-final/
cp .ufo/waves/round-44/verification/claim/after-final/after-v5.json \
   $S/lane/.ufo/waves/round-44/verification/claim/after-final/
cp .ufo/waves/round-44/verification/claim/after-v5.json $S/lane/.ufo/waves/round-44/verification/claim/
cp .ufo/waves/round-45/verification/v6v4/counter-v4.json \
   $S/lane/.ufo/waves/round-45/verification/v6v4/
cp $S/lane/.ufo/waves/round-45/c45_freshness.py $S/pristine.py
```

Baseline, pristine bytes in the replica (`cd $S/lane/.ufo/waves/round-45 && python3 -B c45_freshness.py`):

```
selftest_kills before=2/4 after=4/4
v4_predicate_names_class_runs before=true after=false
witness_split class_only=26 mixed=1 met=0
FRESHNESS_RAN_OK
exit=0
```

Identical to the lane's own run at tip (same output, lane `verification/freshness/freshness.json`
values 2/4, 4/4, true, false, 26/1/0). Baseline passes; mutants are interpretable.

Inputs the honest script reads, and the two *near-miss* receipts available on disk:

| leg | honest source | sha256 | decoy used by mutant |
|---|---|---|---|
| split | `round-44/verification/claim/after-final/after-v5.json` | `9dead4d7…c076d1` | `round-44/verification/claim/after-v5.json` (`2383efae…ce0902`, the pre-G6 23-witness receipt) |
| v4_before | `round-44/verification/claim/v4-final/v4.json` | `6673d988…60af` | — |
| v4_after | `round-45/verification/v6v4/counter-v4.json` | `887bb25b…30ca` | the committed r44 v4.json above |
| after-kills | `mutants/m{1..4}_v2.py` | `8901a8ed…`, `ea5fd625…`, `5eb13bcf…`, `9c717c13…` | `mutants/m{1..4}.py` (v1 set) |

## Mutants (one behavioural point each; diff vs pristine in `$S/m*.diff`)

```
M1  76c:  "claim" / "after-final" / "after-v5.json"  ->  "claim" / "after-v5.json"
M2  73c:  WAVE / "verification" / "v6v4" / "counter-v4.json"
          ->  WAVE.parent / "round-44" / "verification" / "claim" / "v4-final" / "v4.json"
M3  68c:  WAVE / "mutants" / ("m%d_v2.py" % n)  ->  WAVE / "mutants" / ("m%d.py" % n)
M4  = all three of the above simultaneously (degenerate runner)
```

Commands: `cd $S/lane/.ufo/waves/round-45 && python3 -B c45_freshness_m<N>.py`.

### Decisive output (verbatim)

```
===== M1 (expected: 22/1/4) =====
selftest_kills before=2/4 after=4/4
v4_predicate_names_class_runs before=true after=false
witness_split class_only=22 mixed=1 met=4
FRESHNESS_RAN_OK
exit=0
===== M2 (expected: after=true) =====
selftest_kills before=2/4 after=4/4
v4_predicate_names_class_runs before=true after=true
witness_split class_only=26 mixed=1 met=0
FRESHNESS_RAN_OK
exit=0
===== M3 (expected: after=2/4) =====
selftest_kills before=2/4 after=2/4
v4_predicate_names_class_runs before=true after=false
witness_split class_only=26 mixed=1 met=0
FRESHNESS_RAN_OK
exit=0
===== M4 (composite: all three wrong) =====
selftest_kills before=2/4 after=2/4
v4_predicate_names_class_runs before=true after=true
witness_split class_only=22 mixed=1 met=4
FRESHNESS_RAN_OK
exit=0
```

Mutant receipts (`receipt-m<N>.json`) differ from the honest receipt only in the substituted values;
M1 vs honest, `diff <(jq 'del(.ran_at_ns)' honest) <(jq 'del(.ran_at_ns)' receipt-m1.json)`:

```
   "witness_split": {
-    "class_only": 26,
+    "class_only": 22,
     "mixed": 1,
-    "met": 0
+    "met": 4
```

No source path or digest distinguishes the two receipts, so a consumer cannot tell the honest
measurement from the substituted one.

Supporting exit-code tally of the selftest sets (direct run on the lane's mutant bytes):
`m1.py=1 m2.py=0 m3.py=1 m4.py=0` (2/4), `m1_v2.py=1 m2_v2.py=1 m3_v2.py=1 m4_v2.py=1` (4/4),
`v2/m1..m4.py = 1,1,1,1`.

## Verdicts

| named attack | expected detector | actual | verdict |
|---|---|---|---|
| (1) split read from `verification/claim/after-v5.json` | prints 22/1/4 *and* the runner rejects/refuses (non-zero or mismatch marker) | prints `class_only=22 mixed=1 met=4` **and** `FRESHNESS_RAN_OK`, exit 0 | **SURVIVED** (expected wrong-values reproduced; no failure signal) |
| (2) v4_after read from committed r44 v4.json | prints `after=true` *and* fails | prints `after=true`, `FRESHNESS_RAN_OK`, exit 0 | **SURVIVED** |
| (3) after-kills run from the v1 mutant set | prints `after=2/4` *and* fails | prints `before=2/4 after=2/4`, `FRESHNESS_RAN_OK`, exit 0 | **SURVIVED** |
| (4, extra) all three substituted at once | runner cannot certify freshness | prints 2/4, true, 22/1/4, exit 0 | **SURVIVED** |

All four wrong-value predictions matched exactly, so the substitutions were behaviour-bearing; none
was detected. **The script is not able to fail on its own input selectors**: "able to fail" here
reduces to "each leg returned a value". The C2 legs' *truth* is therefore established only by the
committed receipt paths being what the wave-1 record says they are, not by this runner.
This is a coverage finding, not a claim that the tip measurement (26/1/0, 2/4→4/4, true→false) is
wrong: the honest run reproduces it byte-for-byte, both from the lane and from the replica.

Related, already-recorded overlap: `w1/CriticC2Scope.md:20` notes `make_w1_spec.py` points its jq at
`after-final/after-v5.json` while expecting 22/1/4 — M1 shows that expectation is exactly what the
sibling receipt `claim/after-v5.json` yields silently.

## Restoration evidence

- All probed lane inputs unchanged: `sha256sum -c hashes-pre.txt` over `c45_freshness.py`, the eight
  mutant files, both `after-v5.json`, `v4.json`, `counter-v4.json` → all `OK` after the probes;
  `git status --porcelain` over the same paths empty.
- **Lane-write disclosure (one, restored):** the initial baseline call ran the wave's documented
  counting command *in the lane* (`python3 -B .ufo/waves/round-45/c45_freshness.py`), which rewrites
  `.ufo/waves/round-45/verification/freshness/freshness.json`. That write changed only `ran_at_ns`
  (00:56:55); every measured value was identical (`jq -c 'del(.ran_at_ns)'` equal to `HEAD` at
  `4c53844`). I restored the committed bytes
  (`d47b4ac6d9cdba03dd4a2e1b41cf2b0ee6700a8f3ec037cef6c7e93db5715541`); `git status --porcelain`
  for that path is now empty. All mutant probes ran only against the scratch replica, where the
  receipt is written under `$S/lane/...`. If the wave wants a fresh timestamp on that receipt, seat
  `ReRunFreshness` must re-run it at the end.
- Scratch mutants restored to pristine bytes after the probes:
  `m1.py m2.py m3.py m4.py pristine.py` all `46e6a89c5221b5c4877baeb0b23da6aa0b85d9b7a9e1706c736b177b692a3186`.
- Post-restore honest run in the replica reproduced `2/4 4/4 / true false / 26/1/0 / FRESHNESS_RAN_OK`.
- Mutant copies `c45_freshness_m*.py` removed from the replica wave dir; diffs/traces/receipts kept
  as evidence under `$S/`.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2/MutFreshnessRunner.md` (this report)
- Scratch only: `$S/pristine.py`, `$S/m{1..4}.py`, `$S/m{1..4}.diff`, `$S/out-m{1..4}.txt`,
  `$S/out-pristine-post.txt`, `$S/receipt-m{1..4}.json`, `$S/hashes-pre.txt`, `$S/lane/**`.
