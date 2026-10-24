# ExecBeforePlacebo — kake-r44 wave 2 (lane: kake-shokunin)

Axes: **operability** (C1's BEFORE receipt must be reproducible from frozen bytes) and
**falsifiability** (the placebo must witness strictly fewer than 27/27, otherwise the
v5 classes are not what does the work).

Role: leaf executor. No other agent spawned, no delegation, no commit/push/deploy.

---

## 1. Decisive command (the item's named command, verbatim)

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv --counter .ufo/waves/round-44/c44_placebo.py --classes v5 --expect witnessed --workers 4 --out .ufo/waves/round-44/verification/claim/placebo-before.json > .ufo/waves/round-44/verification/claim/placebo-before.txt 2>&1; echo exit=$?
```

Exit code and wall time:

```
real	3m32.219s
user	13m5.848s
sys	1m25.156s
exit=1
```

### Decisive output — `verification/claim/placebo-before.txt` (verbatim, complete)

```
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=0/27 notMet=1 build_met=0/0 ok=False counter=9ce3acd4c4c7
  portlen-v1           G1         met=True  caught=-                      
  portlen-v5           G1         met=True  caught=-                      
  buildscheme-M5       G2         met=True  caught=-                      
  buildscope-m5        G3         met=False caught=A,D                    
  buildscope-m4        G4         met=True  caught=-                      
  headtail-V1          G5         met=True  caught=-                      
  headtail-V2          G5         met=True  caught=-                      
  headtail-V7          G5         met=True  caught=-                      
  prefixcache-p48      G5         met=True  caught=-                      
  casememo-v3          G6         met=True  caught=-                      
  casememo-v4          G6         met=True  caught=-                      
  casememo-v7          G6         met=True  caught=-                      
  casememo-v8          G6         met=True  caught=-                      
  repeat-len-band      G7         met=True  caught=-                      
  repeat-depth-band    G7         met=True  caught=-                      
  repeat-defpos-band   G7         met=True  caught=-                      
  repeat-depth-deep    G7         met=True  caught=-                      
  repeat-defpos-late   G7         met=True  caught=-                      
  hosttable-A          G8         met=True  caught=-                      
  hosttable-B          G8         met=True  caught=-                      
  hosttable-F          G8         met=True  caught=-                      
  portvalue-digits     G9         met=True  caught=-                      
  portvalue-digits-67  G9         met=True  caught=-                      
  portlen-v4           G9         met=True  caught=-                      
  buildport-m6         G2         met=True  caught=-                      
  headtail-V4          G10        met=True  caught=-                      
  headtail-V8          G10        met=True  caught=-                      
```

### Answers to the item's four questions

| Question | Answer |
|---|---|
| **k** (witnessed by a class key) | **k = 0/27** (`witnessedNames: []`, `witnessedByClass: {}`) |
| **exit code** | **exit=1** (audit `ok=False`; `--expect witnessed` is *not* met — the correct/desired outcome for a placebo) |
| **equals the inherited receipt's 1/27?** | **No.** The inherited receipt (`verification/placebo/before.json`) has `witnessed=1`, `witnessedNames=["headtail-V8"]`, `witnessedByClass={"headtail-V8": ["G1"]}`. The fresh reproduction has **k=0**. The inherited 1/27 is *not* seed-stable. |
| **which row** | **headtail-V8** is the only row that ever yields a placebo witness. Inherited: `met=False caught=G1`. Fresh named run: `headtail-V8 met=True caught=-` (no divergence at all under this seed). The only fresh notMet row is **buildscope-m5** (`caught=A,D` — legacy keys, *not* a class key, hence not a witness). |

---

## 2. Pass / fail against the item's named attack

**Attack:** "placebo must witness only k<27 (k measured, not targeted); if it witnesses 27/27 the classes are not doing the work."

**PASS.** Across **7 fresh full audits** of the frozen placebo counter (the named command + 6 replicates),
k ∈ {0, 1} — never 27, never above 1:

| run | invocation | k | witnessed row (caughtBy) |
|---|---|---|---|
| named | `--workers 4`, out=claim/placebo-before.json | **0**/27 | — |
| run2 | `--workers 2`, scratch | 0/27 | — |
| run3 | `--workers 2`, scratch | 0/27 | — |
| run4 | `--workers 2`, scratch | 1/27 | headtail-V8 (`F`,`G7`) |
| run5 | `--workers 2`, scratch | 0/27 | — |
| run6 | `--workers 2`, scratch | 0/27 | — |
| clean | `--workers 4`, isolated scratch out dir | 1/27 | headtail-V8 (`G3`) |
| *inherited* | *(pre-existing receipt)* | *1/27* | *headtail-V8 (`G1`)* |

So k is **measured, not targeted**: the placebo's single possible witness is a *seed accident*, and the
inherited receipt's 1/27 is one draw of it. The classes are demonstrably what does the work:
the real v5 counter witnesses **23/27** (`verification/claim/after-v5.json`, and the wave-2
baseline `verification/claim/after-v5-wave2-baseline.json` — `witnessed 23/27 ... build met 3/3`)
while the placebo witnesses **0–1/27** on the identical harness, run set and predicate.

**Sub-verdict on the inherited 1/27 itself: it is genuine but not reproducible as a *count*.**
Re-running the inherited receipt's own recorded seeds against the frozen bytes reproduces all three of
its notMet rows exactly, including the G1 catch:

```
$ python3 -B .ufo/waves/round-44/c44_placebo.py --root . --classes v5 \
    --tool-file .ufo/waves/round-44/controls-r43/headtail-V8-longport-tail64.py \
    --seed 13424461184966 --out .../seed-headtailV8.json
seed 13424461184966 met False equalRuns 20/21
diverging: {'G1': False}          # identical to the inherited receipt's headtail-V8 caught=G1

$ ... --tool-file .../buildscope-m5-empty-path.py --seed 128848707549493
buildscope-m5 seed 128848707549493 met False equalRuns 20/21 diverging {'D': False}

$ ... --tool-file .../repeat-ctl_len_memo_band.py --seed 269612995650601
repeat-len-band seed 269612995650601 met False equalRuns 20/21 diverging {'C': False}
```

So the inherited receipt is byte-honest against the frozen counter; its `1/27` is simply the
outcome of one particular seed, and a fresh unseeded draw gives 0 (or, 2 of 7 times, 1).

---

## 3. Mechanism — why the placebo's k is 0–1 and never 27

All ten placebo class modules are byte-identical delegators to the v4 run-F generator
(`sha256 b827ec1cd2b5e2144aa6c14ae3590b7ae6ff17488e9e93a9173b4bb63aea5f54` for **all ten** files in
`.ufo/waves/round-44/classes-placebo/`):

```python
def cases(rng, h):
    return h.cases_f(rng)
```

The class runs still execute (the receipts show 21 runs per control — `A,B,C,D,E,F,G1..G10,T1..T5`,
each class run with `values=1660`), but they carry **none** of the targeted class shapes. A placebo
G-key "witness" can therefore only arise when the F-shaped corpus *coincidentally* contains a value
the control mishandles — e.g. in the isolated clean run headtail-V8 diverged under `G3` while the
plain `F` run of the same control did not. That is a coincidence of the shared rng stream, not class work.
Hence k ∈ {0,1}, never 27.

The real v5 classes under `.ufo/waves/round-44/classes/` are what move the count from 0–1 to 23/27.

---

## 4. Frozen bytes — verified unchanged before and after

```
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27  .ufo/waves/round-44/c44_placebo.py
a1f0e364dad5ff937666966a16622e6895591a2eb3db714d6ecf3f3948c31bf8  .ufo/waves/round-44/controls-27.tsv
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
```

`c44_placebo.py`'s sha256 `9ce3acd4c4c7…` equals the `counterSha256` recorded in both the inherited
receipt and my fresh receipt — same instrument in both.

**Not edited by me:** `c44_audit.py`, `c44_placebo.py`, `c44_count_v5.py`, `controls-27.tsv`,
`controls-r43/*`, `classes-placebo/*`, `classes/gN_*.py`, `build_v5.py`, `.ufo/state/`, watchdog logs,
`MANIFEST.json`, `templates/`, fleet scripts, route tables, `mcp.json`. No git/jj write, no commit, no push.

---

## 5. Operability finding the L1 should know (shared-dir collision)

`c44_audit.py` writes each per-control receipt to **`<dirname(--out)>/tools/<control>.json`**
(`outdir = dirname(abspath(--out)); tools_dir = outdir + "/tools"`). Every wave-2 seat that passes an
`--out` inside `.ufo/waves/round-44/verification/claim/` therefore writes into the **same**
`claim/tools/` directory. Observed in this wave:

* my named run wrote its 27 placebo per-control receipts into `claim/tools/` (mtimes 23:02:48–23:05:30),
* the concurrent `ExecAfterBaseline` run (`after-v5-wave2-baseline.json`, 23:05:20) and the `ExecV4Support`
  run (`v4-support.json`, 23:05:30) overwrote the same 27 filenames.

Final state of `claim/tools/*.json` (27/27) is attributed entirely to counter `5cedaa3b9f91`
(`c44_count_v5.py`, `classesMode v5`) — i.e. the sibling's baseline receipts, **not** my placebo's.
So `claim/placebo-before.json`'s per-row `receipt` pointers resolve to receipts that no longer carry
my run's data. This does not affect the summary's own numbers (they are inlined in the JSON), but it
does break per-control re-derivation of *any* receipt whose out-dir is shared.

**Consequence for the L1:** per-control receipts are only trustworthy when the run's `--out` sits in a
run-private directory. My placebo per-control receipts are preserved run-private at
`/fast/scratch/hyaku/kake-r44/ExecBeforePlacebo/clean/tools/` (27 files, provenance check: all
`counterSha256=9ce3acd4c4c7`, `classesMode=v5`) — 26 `met=True` + 1 `met=False`, matching the
isolated clean summary exactly.

---

## 6. Files written

### In the lane repo (`/home/vgpnk/Projects/shokunin/kake-shokunin`)

1. `.ufo/waves/round-44/verification/claim/placebo-before.json` — the item's named receipt (k=0/27).
2. `.ufo/waves/round-44/verification/claim/placebo-before.txt` — the item's named stdout capture (pasted verbatim above).
3. `.ufo/waves/round-44/verification/claim/tools/*.json` (27 files) — written by the audit driver as a
   side effect of the named command (`--out` in `claim/`); subsequently overwritten by concurrent
   sibling runs (see §5). No longer attributable to my run.
4. `.ufo/waves/round-44/w2/ExecBeforePlacebo.md` — this report.

### In scratch (`/fast/scratch/hyaku/kake-r44/ExecBeforePlacebo/`)

`placebo-before.json`, `placebo-before.txt` (copies of the named command's outputs), `run1-tools/`
(32 files, copied at 23:06:01 — already partly sibling-overwritten), `tools-snapshot-pre/`
(29 files, pre-run snapshot of `claim/tools/`), `tools/` (replicate per-control receipts),
`run2.json`/`run2.txt`, `run3.json`/`run3.txt`, `run4.json`/`run4.txt`, `run5.json`/`run5.txt`,
`run6.json`/`run6.txt`, `exits.txt`, `exits2.txt`, `clean/placebo-clean.json`,
`clean/placebo-clean.txt`, `clean/tools/` (27 run-private placebo per-control receipts),
`seed-headtailV8.json`/`seed-headtailV8.txt`, `seed-buildscope-m5.json`, `seed-repeat-len-band.json`.

Nothing was written anywhere else in the fleet repo.

---

## 7. Blockers / caveats

* **None blocking.** The named command ran clean (exit 1 as required for a placebo under
  `--expect witnessed`), the frozen bytes are intact, and the attack's threshold (k<27) is met with
  a large margin (k ≤ 1 over 7 fresh runs).
* The one substantive divergence from the inherited receipt — k=0 vs 1/27 — is **seed variance in the
  inherited receipt, not a defect in the reproduction**. Both numbers are reproduced exactly from
  their own recorded seeds (§2), and the inherited receipt predates the current
  `controls-27.tsv`/`c44_audit.py` mtimes (20:25:49 vs 20:40:59 / 20:40:04), i.e. it was produced
  with an earlier invocation (it carries `build met 3/3`, so it ran with `--build-rev 020bc457
  --build-runs 3`, which the item's command does not) and an earlier TSV row labelling
  (`buildport-m6` was class `G9` in the inherited receipt, `G2` in today's frozen TSV — the class
  *column* is cosmetic; witness semantics use `counter_mod.CLASS_MODULES` keys `G1..G10`, unchanged).
* No tool installs were needed or performed (no pacman, no uv/npx, no new binaries).

## 8. Checks the parent should run

* Confirm `verification/claim/placebo-before.json` parses and shows `witnessed: 0` with
  `witnessedNames: []` (already verified here).
* Re-run the named command once more if a second seed draw is wanted; expect k ∈ {0,1}.
* If per-control receipts must remain attributable, re-issue the command with a run-private `--out`
  (e.g. `--out .ufo/waves/round-44/verification/claim/placebo-before.run2.json` is *not* private —
  use a distinct directory) or accept the summary JSON alone as the evidence.
