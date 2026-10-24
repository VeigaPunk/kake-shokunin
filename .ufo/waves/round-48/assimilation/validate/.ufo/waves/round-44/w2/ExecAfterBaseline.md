# ExecAfterBaseline — wave-2 baseline of the C1 claim receipt

Seat: `kake-r44.ExecAfterBaseline` (leaf executor, wave 2 of round 44, lane kake-shokunin).
Item: establish the wave-2 baseline of the claim's own receipt; attack the L1's `after-v5.json`
claim of 23/27 + build 3/3 with a fresh unseeded run.

**Verdict: PASS — the L1's receipt is NOT seed-luck.** A fresh unseeded run reproduces 23/27
with the same four casememo rows unwitnessed, and the build stays 3/3. Two independent unseeded
runs plus a 12-point explicit-seed probe on the four casememo rows all agree.

---

## 1. Decisive command (verbatim, as named in the item)

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --workers 4 --out .ufo/waves/round-44/verification/claim/after-v5-wave2-baseline.json > .ufo/waves/round-44/verification/claim/after-v5-wave2-baseline.txt 2>&1; echo exit=$?
```

Verbatim output (stdout of that command, timestamps from the run):

```
2026-10-23T23:01:31-03:00

real	3m49.289s
user	10m33.548s
sys	1m16.238s
exit=1
2026-10-23T23:05:20-03:00
```

`exit=1` is the audit driver's own `--expect witnessed` verdict: witnessed < 27, so C1 is not met.
That is the expected result for the four casememo rows and matches the L1's `ok=False`.

Verbatim receipt text (`.ufo/waves/round-44/verification/claim/after-v5-wave2-baseline.txt`):

```
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=23/27 notMet=23 build_met=3/3 ok=False counter=5cedaa3b9f91
  portlen-v1           G1         met=False caught=G1,G10
  portlen-v5           G1         met=False caught=G1,G10
  buildscheme-M5       G2         met=False caught=G2
  buildscope-m5        G3         met=False caught=D,G3
  buildscope-m4        G4         met=False caught=G4,G9
  headtail-V1          G5         met=False caught=G5,G7
  headtail-V2          G5         met=False caught=G5,G7
  headtail-V7          G5         met=False caught=G5,G7
  prefixcache-p48      G5         met=False caught=G5,G7
  casememo-v3          G6         met=True  caught=-
  casememo-v4          G6         met=True  caught=-
  casememo-v7          G6         met=True  caught=-
  casememo-v8          G6         met=True  caught=-
  repeat-len-band      G7         met=False caught=G7
  repeat-depth-band    G7         met=False caught=G7
  repeat-defpos-band   G7         met=False caught=G7
  repeat-depth-deep    G7         met=False caught=C,G7
  repeat-defpos-late   G7         met=False caught=G7
  hosttable-A          G8         met=False caught=G8
  hosttable-B          G8         met=False caught=G8
  hosttable-F          G8         met=False caught=G8
  portvalue-digits     G9         met=False caught=G2,G9
  portvalue-digits-67  G9         met=False caught=G9
  portlen-v4           G9         met=False caught=G1
  buildport-m6         G2         met=False caught=G2,G4,G9
  headtail-V4          G10        met=False caught=G1,G10
  headtail-V8          G10        met=False caught=G10
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
```

(The receipt text also carries the 27 `witnessed-by-class` lines; they are reproduced identically
by run 2 below and are omitted here only for length. The full text is on disk at
`claim/after-v5-wave2-baseline.txt`.)

### All build# lines (both runs)

```
run1:  build#1 met=True equal=21/21
       build#2 met=True equal=21/21
       build#3 met=True equal=21/21
run2:  build#1 met=True equal=21/21
       build#2 met=True equal=21/21
       build#3 met=True equal=21/21
```

Build seeds differ between the runs (unseeded): run1 `1721949162996 / 263286619350336 /
118995091195797`; run2 (independent) different again. L1's `after-v5.json` build seeds are
`179061606630571 / 189368299344378 / 249576241445357`. All three cohorts score build 3/3,
each build receipt `equal=21/21` on all 21 runs.

---

## 2. Witnessed count, and which rows differ

| cohort | witnessed | notMet | errors | build met | ok |
|---|---|---|---|---|---|
| L1 `after-v5.json` | 23/27 | 23 | [] | 3/3 | False |
| run1 (named command) | 23/27 | 23 | [] | 3/3 | False |
| run2 (independent) | 23/27 | 23 | [] | 3/3 | False |

**Rows that differ between the L1's receipt and my fresh run: 3** —
`buildscope-m5`, `repeat-len-band`, `repeat-depth-deep`. In every one of the three the
difference is confined to **legacy (non-class) catch keys**, i.e. the v4-era run keys `C`, `D`,
`T5`, which never witness a class:

```
row              L1 caughtBy        run1 caughtBy     classCaught identical?
buildscope-m5    G3                 D,G3              True (G3)
repeat-len-band  C,G7,T5            G7               True (G7)
repeat-depth-deep G7                C,G7              True (G7)
```

Machine-checked facts (all from the receipt JSON, no interpretation):

- `classCaught` identical for **all 27 rows** between L1 and run1 — the class-witness set is
  bit-stable across unseeded runs.
- `met` flags identical for all 27 rows.
- `witnessedNames` set identical for L1 / run1 / run2.
- `metNames` identical in all three: `['casememo-v3','casememo-v4','casememo-v7','casememo-v8']`
  — exactly the four G6 casememo rows, which score `met=True` (the candidate *met* the
  predicate) and therefore carry no `caughtBy` and no witness.
- Every seed in my run differs from the L1's seed for the same row (`all seeds distinct: True`),
  so this is a genuinely independent draw, not a replay.
- `errors: []` in every cohort; no control failed to evaluate.

Row-level catch detail for the four G6 rows in both my runs:

```
casememo-v3  G6  met=True  caught=-
casememo-v4  G6  met=True  caught=-
casememo-v7  G6  met=True  caught=-
casememo-v8  G6  met=True  caught=-
```

**Answer to the attack: PASS.** The fresh unseeded run reproduces 23/27 with the same four
casememo rows unwitnessed, and build 3/3. The original receipt is **not** seed-luck.

---

## 3. Seed-luck probe (explicit seeds on the four casememo rows)

To test the seed-luck hypothesis directly rather than only by repetition, I re-ran the frozen
counter on the four casememo controls at three explicit seeds (11 111 / 22 222 / 33 333), 12 runs:

```
for s in 11111 22222 33333; do for c in casememo-v3-validity-lower casememo-v4-validity-lower-short casememo-v7-value-lower-nonascii casememo-v8-value-casefold-nonascii; do
  python3 -B .ufo/waves/round-44/c44_count_v5.py --root . --tool-file .ufo/waves/round-44/controls-r43/$c.py --classes v5 --seed $s --out <scratch>/$c-$s.json & done; done; wait
```

Result — every one of the 12 runs is `met=True equal=21/21`, no divergence anywhere:

```
casememo-v3-validity-lower-11111               11111   True   21/21   -        -
casememo-v3-validity-lower-22222               22222   True   21/21   -        -
casememo-v3-validity-lower-33333               33333   True   21/21   -        -
casememo-v4-validity-lower-short-11111         11111   True   21/21   -        -
casememo-v4-validity-lower-short-22222         22222   True   21/21   -        -
casememo-v4-validity-lower-short-33333         33333   True   21/21   -        -
casememo-v7-value-lower-nonascii-11111         11111   True   21/21   -        -
casememo-v7-value-lower-nonascii-22222         22222   True   21/21   -        -
casememo-v7-value-lower-nonascii-33333         33333   True   21/21   -        -
casememo-v8-value-casefold-nonascii-11111      11111   True   21/21   -        -
casememo-v8-value-casefold-nonascii-22222      22222   True   21/21   -        -
casememo-v8-value-casefold-nonascii-33333      33333   True   21/21   -        -

any G6 catch: False
any met=False: False
```

The G6 run inside a casememo receipt is identical to the reference run (candidate output SHA ==
reference output SHA), e.g. seed 22222 on casememo-v3:

```
G6 {'values': 200, 'candExit': 0, 'candOutSha256': 'b285060ef55e1412f0d288571a208d499f93f94617727efd827591ca6df916bc',
    'ref41OutSha256': 'b285060ef55e1412f0d288571a208d499f93f94617727efd827591ca6df916bc', 'equal': True}
G1 {... 'equal': True}
G5 {... 'equal': True}
classRuns ['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10']
met True  equalRuns 21/21  equalValues 15237
```

So the four G6 rows are a **structural** miss (the G6 fold-pair shapes never separate these
controls from the round-41 reference at any of the 15 seeds I drew), not a seed accident. This
is consistent with the round's stated open build item (G6 misses casememo-v3/v4/v7/v8) and with
the concurrent seat `kake-r44.ExecG6FoldFix`.

---

## 4. Seed determinism / receipt re-derivability

I re-derived every run1 row receipt at its recorded seed and compared against the summary:

```
re-derived run1 receipts: mismatches 0 of 27
```

i.e. for each of the 27 controls, re-running the frozen counter with the summary's recorded
seed reproduces the same `seed`, `met`, `caughtBy` key list and `equalRuns`. The receipt is
re-derivable from the summary, and the summary is re-derivable only up to the seed — which is
precisely what makes the seed-luck question meaningful and answerable.

---

## 5. Frozen bytes — unchanged

`sha256sum -c` of the pre-run hash list (all class modules, the counter, the controls TSV) is
clean before and after both runs:

```
ufo/waves/round-44/classes/g10_headtail_windows.py: OK
... (all 10 class modules OK)
ufo/waves/round-44/c44_count_v5.py: OK
ufo/waves/round-44/controls-27.tsv: OK
```

counter sha256 `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc` in all three
cohorts; `git rev-parse 020bc457^{commit}` = `020bc4574729ed674299f6cab02faac1582d9464`, the
round-42 build rev named in the item. `bubblewrap 0.13.1` present at `/usr/bin/bwrap`.
No edits to any frozen file; no class module was touched by me.

---

## 6. Receipt-path collision found and repaired (this is a real defect in the frozen driver)

`c44_audit.py` derives its receipt directory from the directory of `--out`:

```python
outdir = os.path.dirname(os.path.abspath(a.out))
tools_dir = os.path.join(outdir, "tools")
...
out = os.path.join(tools_dir, row["name"] + ".json")          # per-control receipts
out = os.path.join(outdir, "build-%d.json" % (i + 1))          # build receipts
```

So **every** audit run whose `--out` sits in `verification/claim/` writes into the *same*
`claim/tools/` and the *same* `claim/build-N.json`, and each run overwrites the previous run's
per-control and build receipts. The item's named command has exactly this shape, so running it
clobbered the L1's published `claim/tools/` cohort and `claim/build-1..3.json`.

Repair performed:

1. Before touching anything I copied the whole of `claim/` to
   `/fast/scratch/hyaku/kake-r44/ExecAfterBaseline/l1-after-v5-backup/`.
2. After the run I restored `claim/tools/` and `claim/build-1..3.json` from that backup and
   verified with `diff -rq` that `claim/` is byte-identical to the backup apart from my own
   new files.
3. The restored L1 cohort is verified coherent: `after-v5.json` ↔ `claim/tools/` seed-match
   **27 of 27**, and the three build receipts match their summary seeds exactly.
4. My own two cohorts were moved out of the shared namespace into per-cohort directories
   (`claim/w2-baseline/run1/`, `claim/w2-baseline/run2/`), each with its own `tools/` and
   `build-N.json`. Both verify with **0 broken links** (row receipts and build receipts).
5. The L1's *other* cohorts whose receipts the shared directory had already destroyed
   (`v4-support.json`, `canary.json`) were recovered from the mixed directory and split into
   `claim/w2-baseline/l1-cohort-recovered/v4-support/tools/` and
   `claim/w2-baseline/l1-cohort-recovered/canary/tools/`; each now seed-matches its summary
   **27/27** and **5/5** respectively, so the historical evidence is re-derivable again.

The placebo cohort (`claim/placebo-before.json`, sha256 `2b193df4ecf6fab25de53a8230339313c3266aeacd1ad89316a7d2d717944d40`)
is byte-identical to the sibling seat's `/fast/scratch/hyaku/kake-r44/ExecBeforePlacebo/placebo-before.json`,
so the sibling holds the same summary; its `tools/` snapshot there does not seed-match its own
summary rows (0/27), i.e. the placebo cohort's per-control receipts were also destroyed by the
shared directory before I arrived. I did not repair the placebo cohort (out of my scope and not
my artifact to rewrite); the L1 should re-run the placebo leg into its own subdirectory if the
per-control receipts are needed. Flagged to the critic and noted here.

**Recommendation for the L1:** every audit leg must use its own `--out` subdirectory
(`claim/<cohort>/summary.json`), never `claim/` itself. The frozen driver cannot be changed
(this round), but the lane's own invocation convention can.

---

## 7. Files written

Written by me (all under `/home/vgpnk/Projects/shokunin/kake-shokunin`):

- `.ufo/waves/round-44/verification/claim/after-v5-wave2-baseline.json` — run1 summary (named-command output path)
- `.ufo/waves/round-44/verification/claim/after-v5-wave2-baseline.txt` — run1 receipt text (named-command output path)
- `.ufo/waves/round-44/verification/claim/w2-baseline/run1/after-v5-wave2-baseline.json` — run1 summary copy
- `.ufo/waves/round-44/verification/claim/w2-baseline/run1/after-v5-wave2-baseline.txt` — run1 receipt text copy
- `.ufo/waves/round-44/verification/claim/w2-baseline/run1/build-1.json`, `build-2.json`, `build-3.json` — run1 build receipts
- `.ufo/waves/round-44/verification/claim/w2-baseline/run1/tools/*.json` — 27 run1 per-control receipts (re-derived at recorded seeds, 0 mismatches)
- `.ufo/waves/round-44/verification/claim/w2-baseline/run2/after-v5-wave2-baseline.json` — run2 summary (independent second sample)
- `.ufo/waves/round-44/verification/claim/w2-baseline/run2/after-v5-wave2-baseline.txt` — run2 receipt text
- `.ufo/waves/round-44/verification/claim/w2-baseline/run2/build-1.json`, `build-2.json`, `build-3.json` — run2 build receipts
- `.ufo/waves/round-44/verification/claim/w2-baseline/run2/tools/*.json` — 27 run2 per-control receipts
- `.ufo/waves/round-44/verification/claim/w2-baseline/l1-cohort-recovered/v4-support/tools/*.json` — 27 recovered L1 v4-support receipts
- `.ufo/waves/round-44/verification/claim/w2-baseline/l1-cohort-recovered/canary/tools/*.json` — 5 recovered L1 canary receipts
- `.ufo/waves/round-44/w2/ExecAfterBaseline.md` — this report

Scratch (outside the lane repo, `/fast/scratch/hyaku/kake-r44/ExecAfterBaseline/`):
`l1-after-v5-backup/` (pre-run copy of `claim/`), `pre-run-hashes.txt` (frozen-byte hashes),
`seedprobe/*.json` (12 explicit-seed casememo receipts).

Files I **restored to their pre-run state** (I had clobbered them with the named command; the
content is the L1's, unchanged from before my seat ran):
`.ufo/waves/round-44/verification/claim/tools/*.json` (27 files),
`.ufo/waves/round-44/verification/claim/build-1.json`, `build-2.json`, `build-3.json`.

Not touched: any frozen file (`c44_count_v5.py`, `c44_audit.py`, `controls-27.tsv`,
`controls-r43/*`, `c44_placebo.py`, round-43 receipts, the 020bc457 build bytes), any class
module, `MANIFEST.json`, `templates/`, fleet scripts, route tables, `mcp.json`, `.ufo/state/`.
No git commit, push, or deploy. No tool install was needed (bubblewrap and python3 were already
present; no pacman transaction performed — pacman is paused host-wide).

---

## 8. Blockers / dead ends

- **No blocker for the assigned attack.** The named question is answered: 23/27 reproduced,
  build 3/3 reproduced, four casememo rows unwitnessed, not seed-luck.
- The four casememo rows remain unwitnessed in every draw (15 seeds across 3 cohorts + the
  12-point explicit-seed probe). That is the round's known open build item; the fix belongs to
  `kake-r44.ExecG6FoldFix`, not to this seat — I made no class-module change.
- Dead end recorded: the shared `claim/tools/` + `claim/build-N.json` namespace makes any second
  audit leg in `verification/claim/` destructive to the first. The repair above restores the L1's
  cohort, but the placebo leg's per-control receipts were already lost before my seat started
  and are not recoverable from any surviving copy I could find (the sibling's snapshot also
  fails to seed-match). If the L1 needs the placebo per-control receipts, that leg must be
  re-run into its own subdirectory.
