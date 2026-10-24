# AttackV2Regression — driver-v2 interface compatibility

Seat: `kake-r45.AttackV2Regression` · critic · round 45, wave 2.

**Axes:** operability (assigned); freshness unchanged by this read-only review.

**Named-attack result: FAIL strict v1-interface preservation; counterexamples supported.** The healthy fresh-cohort JSON interface passes: all 19 summary fields, all 14 serialized control-row fields, all 8 build-row fields, and their values are unchanged in the deterministic fixture. However, v2 rejects a healthy invocation solely because the output parent contains an unrelated file; the default stdout label changes; and `_valid` is added internally but is not exported in summary rows. The output-directory change was explicitly described in the wave-1 implementation spec, so it is a disclosed design tradeoff, not an accidentally hidden implementation change. These findings do **not** independently falsify the narrower frozen kill-rule-4 assertion about the real 27-control cohort in fresh directories. No claim or admission verdict is issued here.

## Scope and method

Read frozen `.ufo/waves/round-44/c44_audit.py` and current `.ufo/waves/round-45/c45_audit.py`; compared argument declarations by AST; loaded both with bytecode writes disabled; extracted the actual in-memory selftest dictionaries and compared witness/expectation behavior; ran one deterministic scratch fixture through both drivers in fresh, occupied, and deliberately failing expectation cases. Independent runs were concurrent.

The scratch fixture has two controls taken from the selftest row shapes (`class-divergence`, `mixed-divergence`) and returns seeded, in-window, own-SHA receipts. Its three build receipts are synthetic interface fixtures, **not** executions or certification of revision `020bc457`. The revision flag is exercised, not its real build. Both shipped `--selftest` commands were also run, with `TMPDIR` confined to the assigned scratch directory.

Observed driver identities:

```text
DRIVER v1 sha256=8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75
DRIVER v2 sha256=f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076
```

## Enumerated interface and results

| Surface | v1 observable contract | v2 result |
|---|---|---|
| Flags | `-h/--help`; `--selftest`; `--root`; `--controls`; `--counter`; `--classes {v4,v5}`; `--expect {blind,witnessed,not-met}`; `--build-rev`; `--build-runs`; `--workers`; `--out`; `--label` | Argument declarations identical; same parser rejection behavior exercised. |
| Defaults | `selftest=False`, `build_runs=0`, `workers=4`, `label=""`; other arguments default `None`. Root/controls/counter/classes/expect/out required unless selftest. | Preserved. Workers still clamped to at least 1; build workers still capped at 3. |
| Summary fields | `label, classesMode, expect, counter, counterSha256, predicate, controls, classKeys, witnessed, witnessedNames, witnessedByClass, notMet, notMetNames, metNames, errors, build, rows, ok, verdict` | All 19 retained, in the same order; complete fixture values equal. Invalid-receipt counts/errors intentionally change under hardening. |
| Serialized control rows | `name, family, class, path, sha256, exit, met, equalRuns, seed, caughtBy, receipt, error, classCaught, legacyCaught` | All 14 retained and equal in both fixture rows. `error` already existed in v1. `_valid` is **not** serialized. |
| Build rows | `run, exit, met, seed, equalRuns, ratios, receipt, error` | All 8 retained and equal in all 3 fixture builds. Internal `_valid` is also omitted here. |
| In-memory rows | Selftest passing, class-only, v4-only, mixed, and legacy-only rows; v2 additionally supplies timing-only. | Witness results equal on all 6 shapes; 18 single-row expectation comparisons equal. Validity additions do not overwrite old healthy row fields. |
| `witnessedByClass` / stdout | JSON maps control name to **all** `caughtBy` keys; text is `  witnessed-by-class NAME caughtBy=COMMA_KEYS`. Mixed example retains `D,G3`, not just `G3`. | Preserved exactly. |
| Exits | Successful expectation 0; unmet expectation 1; argparse misuse 2; selftest 0. | All exercised and preserved in fresh cohorts. An occupied parent newly turns a healthy case into argparse exit 2. |
| Layout | `<out-parent>/tools/<control-name>.json`; `<out-parent>/build-1.json` through `build-N.json`; requested summary path. | Same names/relative receipt paths; additive `run-manifest.json`. New requirement: entire output parent must be empty. |
| Default stdout | Empty `--label` falls back to `AUDIT kake-r44 ...`. | Falls back to `AUDIT kake-r45 ...`; JSON `label` remains `""`. No default text byte-identity. |
| Selftest stdout | `SELFTEST PASS: ...` | Exit/prefix preserved, exact descriptive text intentionally expanded. |

Source anchors: v1 CLI `:107-126`, row creation `:145-160`, build naming `:171-182`, serialization/text `:184-222`; v2 CLI `:308-327`, output guard `:329-338`, internal validity fields `:98-132`, build naming `:389-398`, serialization/text `:400-445`.

## Strongest counterexample: unrelated file changes success into usage failure

The only extra precondition in the occupied cases is an existing `unrelated.txt` containing an unrelated log. No old receipt was planted. Both drivers use the same controls, counter, classes, expectation, revision flag, build count, and worker count.

Exact decisive commands, as executed by the retained probe:

```sh
/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/c44_audit.py --root /fast/scratch/hyaku/kake-r45/AttackV2Regression/fixture-root --controls /fast/scratch/hyaku/kake-r45/AttackV2Regression/controls.tsv --counter /fast/scratch/hyaku/kake-r45/AttackV2Regression/fixture_counter.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --workers 1 --out /fast/scratch/hyaku/kake-r45/AttackV2Regression/occupied-v1/summary.json
/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_audit.py --root /fast/scratch/hyaku/kake-r45/AttackV2Regression/fixture-root --controls /fast/scratch/hyaku/kake-r45/AttackV2Regression/controls.tsv --counter /fast/scratch/hyaku/kake-r45/AttackV2Regression/fixture_counter.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --workers 1 --out /fast/scratch/hyaku/kake-r45/AttackV2Regression/occupied-v2/summary.json
```

Verbatim decisive probe output:

```text
RUN occupied v1 exit=0
STDOUT:
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3 witnessed=2/2 notMet=2 build_met=3/3 ok=True counter=0d185b4b430a
  class-divergence     G2         met=False caught=G2                     
  mixed-divergence     G2         met=False caught=D,G3                   
  witnessed-by-class class-divergence caughtBy=G2
  witnessed-by-class mixed-divergence caughtBy=D,G3
  build#1 met=True equal=21/21 
  build#2 met=True equal=21/21 
  build#3 met=True equal=21/21
RUN occupied v2 exit=2
STDOUT:

STDERR:
usage: c45_audit.py [-h] [--selftest] [--root ROOT] [--controls CONTROLS]
                    [--counter COUNTER] [--classes {v4,v5}]
                    [--expect {blind,witnessed,not-met}]
                    [--build-rev BUILD_REV] [--build-runs BUILD_RUNS]
                    [--workers WORKERS] [--out OUT] [--label LABEL]
c45_audit.py: error: output directory must be empty: /fast/scratch/hyaku/kake-r45/AttackV2Regression/occupied-v2
```

**Impact:** operability; a wrapper that precreates a log in the output parent, writes a sibling summary there, or reuses a parent accepted by v1 cannot run unchanged. This is stronger than merely replaying old counter receipts: an unrelated file suffices.

**Smallest safe correction:** do not simply delete the fresh-cohort guard. Explicitly narrow the compatibility statement to fresh empty cohorts and migrate/document affected invocations; if full old output-parent compatibility is required, use a newly created isolated receipt cohort internally and publish requested outputs only after reading that cohort's receipts. The current guard-versus-reusable-parent tradeoff cannot honestly be described as full no-regression compatibility. Whether that tradeoff is acceptable belongs to the canonical judge, not this seat. The wave-1 spec (`make_w1_spec.py:184-185`) already declares this behavior; that fact does not make the old invocation compatible.

## Additivity and default-text findings

1. **Serialized `_valid` addition is absent.** Both new row builders return `error` and `_valid`, but summary comprehensions whitelist only the old fields (`c45_audit.py:416-422`). Thus the assigned check that published rows now carry `_valid` additively fails, while preservation of old fields passes. There is no removed v1 field: v1 already had `error`. Smallest correction if `_valid` is part of the intended public row contract: add it to the two serialization field lists without replacing any old field. Alternatively, accurately describe it as internal-only; do not claim the JSON exports it.
2. **Default stdout identity changed.** The healthy fixture stdout becomes byte-identical after changing only `kake-r44` to `kake-r45`. This is a detectable default change, not a gate regression. Restoring a false round-44 identity is not recommended merely to satisfy a byte comparator. Smallest safe correction: explicitly document this compatibility exception and pin `--label` in consumers that need stable text. The `witnessed-by-class` lines themselves are unchanged.

Verbatim decisive healthy-fixture output:

```text
RUN fresh v1 exit=0
RUN fresh v2 exit=0
SUMMARY keys_v1=label,classesMode,expect,counter,counterSha256,predicate,controls,classKeys,witnessed,witnessedNames,witnessedByClass,notMet,notMetNames,metNames,errors,build,rows,ok,verdict
SUMMARY keys_v2=label,classesMode,expect,counter,counterSha256,predicate,controls,classKeys,witnessed,witnessedNames,witnessedByClass,notMet,notMetNames,metNames,errors,build,rows,ok,verdict
SUMMARY missing=[] added=[] changed=[]
ROW 0 keys=name,family,class,path,sha256,exit,met,equalRuns,seed,caughtBy,receipt,error,classCaught,legacyCaught unchanged=True exported_error=True exported__valid=False
ROW 1 keys=name,family,class,path,sha256,exit,met,equalRuns,seed,caughtBy,receipt,error,classCaught,legacyCaught unchanged=True exported_error=True exported__valid=False
BUILD 1 keys=run,exit,met,seed,equalRuns,ratios,receipt,error unchanged=True receipt=build-1.json exported__valid=False
BUILD 2 keys=run,exit,met,seed,equalRuns,ratios,receipt,error unchanged=True receipt=build-2.json exported__valid=False
BUILD 3 keys=run,exit,met,seed,equalRuns,ratios,receipt,error unchanged=True receipt=build-3.json exported__valid=False
WITNESSED_BY_CLASS text_equal=True lines=["  witnessed-by-class class-divergence caughtBy=G2", "  witnessed-by-class mixed-divergence caughtBy=D,G3"]
STDOUT exact_equal=False normalized_default_label_equal=True
LAYOUT v1 ["build-1.json", "build-2.json", "build-3.json", "summary.json", "tools/class-divergence.json", "tools/mixed-divergence.json"]
LAYOUT v2 ["build-1.json", "build-2.json", "build-3.json", "run-manifest.json", "summary.json", "tools/class-divergence.json", "tools/mixed-divergence.json"]
INTERNAL v2 row error=None _valid=True; serialized row _valid_present=False
```

These are selected unchanged lines from the probe output, not a claim they were contiguous. Full invocation arguments/stdout/stderr are retained in scratch `evidence.txt`.

## In-memory and selftest evidence

Command:

```sh
python3 -B /fast/scratch/hyaku/kake-r45/AttackV2Regression/interface_probe.py
```

Verbatim:

```text
CLI declarations equal=True count=11 (plus argparse --help)
MEMORY pass-all witness=False/False expectations={"blind": [true, true], "not-met": [false, false], "witnessed": [false, false]}
MEMORY class-divergence witness=True/True expectations={"blind": [false, false], "not-met": [true, true], "witnessed": [true, true]}
MEMORY v4-divergence witness=False/False expectations={"blind": [false, false], "not-met": [true, true], "witnessed": [false, false]}
MEMORY mixed-divergence witness=True/True expectations={"blind": [false, false], "not-met": [true, true], "witnessed": [true, true]}
MEMORY legacy-divergence witness=False/False expectations={"blind": [false, false], "not-met": [true, true], "witnessed": [false, false]}
MEMORY timing-only witness=False/False expectations={"blind": [false, false], "not-met": [true, true], "witnessed": [false, false]}
MEMORY compatibility PASS rows=6 expectation_comparisons=18
```

The probe also executed `--help` (0), no required arguments (2), `--classes bad` (2), and `--unknown-compat-flag` (2) against each driver. Both negative fixture runs (`--expect blind` over class-divergent rows) exited 1. Exact commands and diagnostics are in `evidence.txt`.

Additional exact commands:

```sh
env TMPDIR=/fast/scratch/hyaku/kake-r45/AttackV2Regression python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/c44_audit.py --selftest
env TMPDIR=/fast/scratch/hyaku/kake-r45/AttackV2Regression python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_audit.py --selftest
```

Both exited 0. Verbatim stdout, respectively:

```text
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
```

## Limits

- Actual 27-control / real-build regression was **not rerun** by this seat; the supplied round state is not re-declared.
- No real `--classes v4` counter run, timeout/resource-failure injection, or arbitrary malformed-receipt census was run. v4/no-class semantic behavior was compared in memory; v4 choice/branch preservation was read in source.
- The occupied-parent counterexample demonstrates an interface/precondition change, not false witness credit or defeat of the receipt gate.
- The scratch probe creates new fixture directories and is not an idempotent rerun command in its already populated scratch workspace.
- No lane implementation, frozen receipt, state, route, or manifest was changed. No installs/updates; existing `python3` sufficed. No commits, pushes, subagent dispatch, or alternate judgment runtime.

## Every file written

Only lane file: `.ufo/waves/round-45/w2/AttackV2Regression.md` (this report).

All remaining files are under `/fast/scratch/hyaku/kake-r45/AttackV2Regression/`. Their individual relative names are listed in `files-created.json`; the following is the same fully enumerated set using Cartesian brace notation:

```text
interface_probe.py
fixture_counter.py
controls.tsv
evidence.txt
files-created.json
fixture-root/{class-divergence.py,mixed-divergence.py}
{fresh-v1,fresh-v2,negative-v1,negative-v2,occupied-v1}/{summary.json,build-1.json,build-2.json,build-3.json,tools/class-divergence.json,tools/mixed-divergence.json}
{fresh-v2,negative-v2}/run-manifest.json
{occupied-v1,occupied-v2}/unrelated.txt
kake45-audit-selftest-b99vi1ja/controls.tsv
kake45-audit-selftest-b99vi1ja/root/ctl.py
kake45-audit-selftest-b99vi1ja/{counter-error,tool-absent,stale,honest}/fake_counter.py
kake45-audit-selftest-b99vi1ja/{out-counter-error,out-tool-absent,out-stale,out-honest}/{summary.json,run-manifest.json,tools/ctl1.json}
```

Workspace directory creation command: `mkdir -p /fast/scratch/hyaku/kake-r45/AttackV2Regression`.
