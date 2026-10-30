# ExecCounterStress — round 64

## Scope and verdict

Attacked frozen C1 and C2 counters only; no lane claim files/counters/receipts were edited. Axes: fail-closed input handling, pin enforcement, and behavior on malformed/non-file spot-check inputs. Revision arguments and C1 hostile-ledger cases behaved safely. **Found a counter cross-scope result:** C2 returned `met=true` on every altered-ledger and altered-spot fixture, because its evaluator does not read those files; this is consistent with the C2 contract's defined inputs, but is not a whole-repository-integrity check. C1 returned `met=false` without traceback on all these cases.

## Reproduction

Scratch harness command:

```sh
python3 -B /fast/scratch/hyaku/kake-r64/ExecCounterStress/attack.py
```

Counter commands executed by the harness:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py --root <fixture-or-lane-root> --revision <arg>
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py --root <fixture-or-lane-root> --revision <arg>
```

Fixtures were separate scratch clones. Before any fixture commit, the harness asserted `git -C <fixture> rev-parse --show-toplevel` resolved exactly to that fixture directory. The `HEAD` for the four malformed-ledger fixtures respectively was `46bd12f950c4960f2c4843e0b901ed53b6676926` (deep nesting), `32bfa692cdb37642d8df658f3bbc26f8137d2f7d` (large string), `09f88a3392e16e919e848800b8c7e74148271843` (NaN), and `c490fa82ec410b48c5e3c4a37fcfdeb30620b7d` (duplicate keys). Located-line variants used valid modified ledger JSON. SPOT variants were a directory tree entry and binary bytes `ff 00 fe 80`.

## Result matrix

Every invocation returned only 0/1/2 and stderr had no `Traceback` (all reported `false` in the harness). `C1` means `c64_calibration.py`; `C2` means `c64_quote_tool.py`.

| Input / fixture | C1 exit; exact result | C2 exit; exact result |
|---|---|---|
| nonexistent ref `refs/heads/missing-r64` | 2; stderr `could-not-evaluate: revision refs/heads/missing-r64 unreadable` | 2; same stderr |
| empty revision `''` | 2; stderr `could-not-evaluate: revision  unreadable` | 2; same stderr |
| 41-hex `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | 2; stderr `could-not-evaluate: revision aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa unreadable` | 2; same stderr |
| `HEAD~99999` | 2; stderr `could-not-evaluate: revision HEAD~99999 unreadable` | 2; same stderr |
| ledger deep nesting (5000 levels) | 1; `pins=0 pin_drift=drift:ledger ... met=false` | 0; `present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true` |
| ledger 2,000,000-character string | 1; `pins=0 pin_drift=drift:ledger ... met=false` | 0; same `met=true` result |
| ledger `NaN` | 1; `pins=0 pin_drift=drift:ledger ... met=false` | 0; same `met=true` result |
| ledger duplicate JSON keys | 1; `pins=0 pin_drift=drift:ledger ... met=false` | 0; same `met=true` result |
| `locatedRawLines='6150'` | 1; `pins=0 pin_drift=drift:ledger ... met=false` | — |
| `locatedRawLines='6150-6155'` | 1; `pins=0 pin_drift=drift:ledger ... met=false` | — |
| `locatedRawLines='6000-7000'` | 1; `pins=0 pin_drift=drift:ledger ... met=false` | — |
| SPOT path is directory | 1; `disagreements=0 pins=1 pin_drift=none ... unresolved=0 met=false` | 0; `present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true` |
| SPOT is binary `ff 00 fe 80` | 1; `disagreements=0 pins=1 pin_drift=none ... unresolved=0 met=false` | 0; same `met=true` result |

The `...` elision above is only table compression; full C1 hostile-ledger outputs included `recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0`. Located-line rows had identical remaining C1 fields. The spot-path outputs included `recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1`.

## Source evidence

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:185-191` verifies revision args and emits exit 2 on unreadable revisions; `:200-214` detects missing/drifted pins and names `drift:ledger`; `:220-245` only parses/re-executes after pins pass; `:193-198` reads the spot blob and decodes with replacement.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py:139-145` has the same safe revision-argument exit; `:147-157` checks the frozen tool sha; `:159-229` consumes tool plus fixture blobs and computes result without reading the calibration ledger or SPOT path.
- Run output also showed hostile-ledger C2 `met=true`, not a crash or an asserted pin failure. The test harness's initial final assertion expected pin-drift output from both counters and consequently ended with `AssertionError`; that assertion was overbroad because C2 does not consume the ledger. All matrix rows had already been emitted and the observed results are recorded above. No corrective rerun was made.

No tools installed or updated. Scratch harness and fixture repositories were removed after retaining these findings; no blocker.