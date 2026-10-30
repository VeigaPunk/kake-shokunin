# ExecDoNothing — Round 64 §9 do-nothing controls

## Verdict

The specified do-nothing controls behave as claimed. **D1:** the frozen T0 C1 counter does not credit the unchanged base (`met=false`, exit 1); C2 returns `met=true` because the quote tool already exists at base, exactly as §C2 declares—not a stub finding or defect; freshness exits 2 with the stale sidecar binding at `SKILL.md:364`. **D2:** applying only the T0 sidecar file to the base tree leaves C1 `met=false` (`lesson_gate=0`) while the sweep exits 0. This is the intended C3 target: the repair is precisely the seven-entry sidecar re-pin, not a bypass.

## Scratch setup and exact invocations

Scratch root: `/fast/scratch/hyaku/kake-r64/ExecDoNothing/`. Both trees were cloned from the lane repository; `base` was detached at `1a48131577ba82c967650561be34e8dba909432a`. `repin` was likewise detached at base and only `corpus/knowledge/freshness-sidecar.json` was copied from T0 (`4c8295fa5e3b628f1fdf3840299ae415c01849fb`). The clone's `git rev-parse --show-toplevel` printed `/fast/scratch/hyaku/kake-r64/ExecDoNothing/repin` before this file was copied. No fixture commits were made.

Commands (T0 counters, frozen claims left untouched):

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/ExecDoNothing/base --revision 1a48131577ba82c967650561be34e8dba909432a
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py --root /fast/scratch/hyaku/kake-r64/ExecDoNothing/base --revision 1a48131577ba82c967650561be34e8dba909432a
node /fast/scratch/hyaku/kake-r64/ExecDoNothing/base/scripts/freshness-sweep.mjs --offline
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/ExecDoNothing/repin --revision 1a48131577ba82c967650561be34e8dba909432a
node /fast/scratch/hyaku/kake-r64/ExecDoNothing/repin/scripts/freshness-sweep.mjs --offline
```

## Captured output

D1 C1 (`d1-calibration.txt`):
```text
revision=1a48131577ba82c967650561be34e8dba909432a disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

D1 C2 (`d1-quote.txt`):
```text
revision=1a48131577ba82c967650561be34e8dba909432a present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true
exit=0
```

D1 C3 (`d1-sweep.txt`):
```text
freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:364
    at loadPathSidecar (file:///fast/scratch/hyaku/kake-r64/ExecDoNothing/base/scripts/freshness-sweep.mjs:386:13)
    at scanCitations (file:///fast/scratch/hyaku/kake-r64/ExecDoNothing/base/scripts/freshness-sweep.mjs:400:19)
    at runSections (file:///fast/scratch/hyaku/kake-r64/ExecDoNothing/base/scripts/freshness-sweep.mjs:1032:56)
    at main (file:///fast/scratch/hyaku/kake-r64/ExecDoNothing/base/scripts/freshness-sweep.mjs:1096:24)
    at file:///fast/scratch/hyaku/kake-r64/ExecDoNothing/base/scripts/freshness-sweep.mjs:1669:1
    at ModuleJob.run (node:internal/modules/esm/module_job:561:25)
    at async onImport.tracePromise (node:internal/modules/esm/loader:647:26)
    at async asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:101:5)
exit=2
```

D2 C1 (`d2-calibration.txt`):
```text
revision=1a48131577ba82c967650561be34e8dba909432a disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

D2 C3 (`d2-sweep.txt`, output summarized to preserve only verdict evidence):
```text
§paths  171 files · 677 occurrences · 106 unique tokens
VERDICT: OK (exit 0, partial: offline)
exit=0
```

## Evidence references and scope

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md:35-41` defines C1 including base `met=false`; lines 43-50 give pins and located span.
- The same contract `:71-79` explicitly says the base quote tool exists and base C2 can be green; `:81-92` defines the stub predicate/kill rule. Thus D1 C2's `met=true` is the expected predicate shape, not a defect reproduction.
- The same contract `:104-119` states C3's before/after and that the repair is exactly the seven-entry sidecar re-pin; `:112-115` constrains the sidecar changes.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/sidecar-repin-map.txt:1-9` records the seven old-to-new pins. The run demonstrated that applying the re-pin alone to base makes offline sweep `VERDICT: OK` and does not make C1 green.

No tools installed or updated. The only persistent write was this assigned report; scratch trees and captured output were removed before handoff.
