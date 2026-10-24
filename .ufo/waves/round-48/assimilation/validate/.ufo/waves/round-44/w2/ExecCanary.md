# ExecCanary — round-44 canary control re-production

Axis: operability. Item: re-produce the five-row canary control and attack it with
"the five-row canary (4 r42 controls + junk) must be notMet 5/5".

No source file was edited. This seat ran the frozen audit driver against the frozen canary
manifest and the frozen v5 counter, then re-ran the same audit a second time into scratch to
test determinism.

## Verdict

**PASS** against the item's named attack.

`notMet = 5` of 5 canary rows (`ok=True`, `verdict="witnessed 3/5 notMet=5"`, `errors=[]`,
`metNames=[]`), audit exit status **0**. The `--expect not-met` gate in `c44_audit.py`
(`expectation_ok`) holds only when every control row is non-error and `met is False`, so a
0 exit is the machine-checked form of "notMet 5/5".

Second independent run reproduced the same verdict (`exit=0`, `notMet=5`, `witnessed=3`,
`errors=[]`).

## Decisive command output (verbatim)

Command (exactly the item's command, run from `/home/vgpnk/Projects/shokunin/kake-shokunin`):

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-canary.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes v5 --expect not-met --workers 2 --out .ufo/waves/round-44/verification/claim/canary.json > .ufo/waves/round-44/verification/claim/canary.txt 2>&1; echo exit=$?
```

Console output:

```
exit=0
```

Contents of `.ufo/waves/round-44/verification/claim/canary.txt` (verbatim, the driver printed
this to the redirected stdout):

```
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=3/5 notMet=5 build_met=0/0 ok=True counter=5cedaa3b9f91
  r42ctl-M8-port-five-digits R42        met=False caught=F,G1,G3,G9,G10,T3      
  r42ctl-v1_casefold   R42        met=False caught=F,T2                   
  r42ctl-v2_prefix32   R42        met=False caught=A,F,G1,G5,G7,G9,G10,T2,T3 
  r42ctl-v4_hosttable  R42        met=False caught=F,T3                   
  r44ctl-junk-constant JUNK       met=False caught=A,B,C,D,E,F,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,T1,T2,T3,T4,T5 
  witnessed-by-class r42ctl-M8-port-five-digits caughtBy=F,G1,G3,G9,G10,T3
  witnessed-by-class r42ctl-v2_prefix32 caughtBy=A,F,G1,G5,G7,G9,G10,T2,T3
  witnessed-by-class r44ctl-junk-constant caughtBy=A,B,C,D,E,F,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,T1,T2,T3,T4,T5
```

### Second run (determinism check, output redirected into scratch, not the claim dir)

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-canary.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes v5 --expect not-met --workers 2 --out /fast/scratch/hyaku/kake-r44/ExecCanary/canary-rerun.json > /fast/scratch/hyaku/kake-r44/ExecCanary/canary-rerun.txt 2>&1; echo exit=$?
```

```
exit=0
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=3/5 notMet=5 build_met=0/0 ok=True counter=5cedaa3b9f91
  r42ctl-M8-port-five-digits R42        met=False caught=F,G1,G3,G9,G10,T3      
  r42ctl-v1_casefold   R42        met=False caught=F,T2                   
  r42ctl-v2_prefix32   R42        met=False caught=F,G1,G5,G7,G9,G10,T2,T3 
  r42ctl-v4_hosttable  R42        met=False caught=F,T3                   
  r44ctl-junk-constant JUNK       met=False caught=A,B,C,D,E,F,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,T1,T2,T3,T4,T5 
  witnessed-by-class r42ctl-M8-port-five-digits caughtBy=F,G1,G3,G9,G10,T3
  witnessed-by-class r42ctl-v2_prefix32 caughtBy=F,G1,G5,G7,G9,G10,T2,T3
  witnessed-by-class r44ctl-junk-constant caughtBy=A,B,C,D,E,F,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,T1,T2,T3,T4,T5
```

## Per-row state (from `.ufo/waves/round-44/verification/claim/canary.json`)

`witnessed` = `met is False` AND `caughtBy` contains at least one v5 class key
(`G1..G10`). `legacyCaught` = caught keys that are **not** class keys (`A..F`, `T1..T5`);
these never witness under `--classes v5`.

| row | class | met | witnessed? | classCaught | legacyCaught | equalRuns | exit | error |
|---|---|---|---|---|---|---|---|---|
| r42ctl-M8-port-five-digits | R42 | False | **yes** | G1, G3, G9, G10 | F, T3 | 15/21 | 1 | none |
| r42ctl-v1_casefold | R42 | False | no | — | F, T2 | 19/21 | 1 | none |
| r42ctl-v2_prefix32 | R42 | False | **yes** | G1, G5, G7, G9, G10 | A, F, T2, T3 | 12/21 | 1 | none |
| r42ctl-v4_hosttable | R42 | False | no | — | F, T3 | 19/21 | 1 | none |
| r44ctl-junk-constant | JUNK | False | **yes** | G1..G10 (all ten) | A, B, C, D, E, F, T1, T2, T3, T4, T5 | 0/21 | 1 | none |

Summary fields read from the receipt:

```
controls = 5   witnessed = 3   notMet = 5   ok = True
verdict = "witnessed 3/5 notMet=5"
errors = []
metNames = []
classesMode = v5   expect = not-met
classKeys = ['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10']
counterSha256 = 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
predicate = met: the tool's exit code and output equal the round-41 tool's on every generated
            run (the eleven v4 runs and the ten class runs), and its median CPU time on each
            of the five timing shapes is at most 2.0 times the round-40 tool's
```

Note on `witnessed 3/5`: the canary gate under `--expect not-met` does **not** require a class
witness on every row — it requires `met == false` on every row with no errors. The two r42
rows without a class witness (`v1_casefold`, `v4_hosttable`) are still correctly scored
`met=False` because their divergence is caught on legacy v4/timing runs only. The junk row is
the strongest witness: it diverges on all 21 runs.

## Canary controls inspected (exact paths)

Manifest `.ufo/waves/round-44/controls-canary.tsv` (5 data rows + 1 comment header), each
file read and its sha256 verified against the manifest column — **all five matched**, so no
row was scored against a stale or missing tool:

| row | control file (repo-relative, path as named in the manifest) | manifest sha256 | on-disk sha256 |
|---|---|---|---|
| r42ctl-M8-port-five-digits | `.ufo/waves/round-43/controls-r42/M8-port-five-digits.py` | 391608309640431acfc873d48e33189cf71a399faaa410ce6d65b910282bbb1f | identical (391608309640431a…) |
| r42ctl-v1_casefold | `.ufo/waves/round-43/controls-r42/v1_casefold.py` | 9993b842427d1592713309420626e46e42f1e56defab28b2f5349e6391cf4bc4 | identical (9993b842427d1592…) |
| r42ctl-v2_prefix32 | `.ufo/waves/round-43/controls-r42/v2_prefix32.py` | eadf5df4b5c26059429a5dbffd2d87bcdbca6f460ba982c81360736e6856aa0f | identical (eadf5df4b5c26059…) |
| r42ctl-v4_hosttable | `.ufo/waves/round-43/controls-r42/v4_hosttable.py` | dc8b6ecdcc638d20d34f66aaeadd8aa8ba798f5307c2fa8d80a876d2ae16ece7 | identical (dc8b6ecdcc638d20…) |
| r44ctl-junk-constant | `.ufo/waves/round-43/controls-r42/junk_constant.py` | e1cf856673f57ef4ed65dcb903d198011cfaf17f3696139a3cea14ac0aa91c60 | identical (e1cf856673f57ef4…) |

`junk_constant.py` is the 4-line trivial junk tool (`print("CLEAN 0 findings"); sys.exit(0)`);
the four r42 controls are the 659–691-line round-39 offline sitemap audit tools, all of which
carry the same "Offline sitemap / sitemap-index audit (round 39, claim C1)" header.

## Frozen-artifact integrity observed

```
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
93de42331287a072f26869fd722bd26c34a72d9db225cfcbb4264b3d06225bde  .ufo/waves/round-44/controls-canary.tsv
```

The counter's sha256 equals the value pinned in `.ufo/waves/round-44/w2-spec.json` and in the
sibling receipts (`.ufo/waves/round-44/verification/claim/after-v5.json`,
`build-1..3.json`, `verification/freeze/control-v4blind.json`), i.e. the same frozen bytes
the round's other audits used. The audit driver sha256 also matches the wave-2 pin
(`8ee2c8bf…`). Nothing frozen was modified by this seat.

## Observation (not a failure of the item's attack)

The canary verdict is stable across the two runs, but one row's *caught key set* is not
byte-stable: `r42ctl-v2_prefix32` scored `equalRuns` 12/21 in run 1 vs 13/21 in run 2, and
run 1 additionally caught legacy key `A` (run 2 did not). The class-witness set for that row
was identical in both runs (`G1, G5, G7, G9, G10`), and every other row was identical apart
from the per-run `seed`. This is seed-driven (`seed` differs per run: 139695556290297 vs
165794543518171) nondeterminism in the v4 legacy runs, not a verdict flip: `met`, `notMet`,
`witnessed`, `ok` and `errors` were byte-identical across the two runs. Recorded as a factual
observation for the L1; it does not change the canary result.

## Files written by this seat

In the lane repo `/home/vgpnk/Projects/shokunin/kake-shokunin`:

1. `.ufo/waves/round-44/verification/claim/canary.json` — the audit summary receipt named by
   the item's command.
2. `.ufo/waves/round-44/verification/claim/canary.txt` — the redirected driver stdout named by
   the item's command.
3. `.ufo/waves/round-44/verification/claim/tools/r42ctl-M8-port-five-digits.json`
4. `.ufo/waves/round-44/verification/claim/tools/r42ctl-v1_casefold.json`
5. `.ufo/waves/round-44/verification/claim/tools/r42ctl-v2_prefix32.json`
6. `.ufo/waves/round-44/verification/claim/tools/r42ctl-v4_hosttable.json`
7. `.ufo/waves/round-44/verification/claim/tools/r44ctl-junk-constant.json`

   (items 3–7 are the per-control counter receipts the frozen driver writes under
   `<out-dir>/tools/`; they carry the five canary row names and do not collide with the
   `controls-27.tsv` receipt names already present in that directory.)
8. `.ufo/waves/round-44/w2/ExecCanary.md` — this report.

In scratch `/fast/scratch/hyaku/kake-r44/ExecCanary/`:

9. `canary-rerun.json`
10. `canary-rerun.txt`
11. `tools/` (the rerun's five per-control receipts)

No source file, frozen artifact, class module, control, manifest, `LOG.md`, `SCORECARD.md`,
`MANIFEST.json`, template, fleet script or route table was read-modified or written. No git,
jj or push operation was performed. No tool was installed for this item (none was needed; the
item is a re-run of an existing frozen command with the stock `python3`).

## Unrun checks

None for this item — the item's single named command and its determinism re-run were both
executed. No build, lint, test-suite or formatter gate was run; per the wave rules the parent
owns the post-integration gate.
