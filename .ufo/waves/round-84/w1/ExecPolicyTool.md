# ExecPolicyTool — round 84 wave w1

## Axes
- Freshness: classify policy values using the frozen value-level classes.
- Calibration: preserve the sibling header table and exact receipt validation.
- Operability: deterministic stdout, explicit exit codes, offline input handling.

## Implementation
- Added scripts/policy_value_class.py; no existing production file changed.
- Imports POLICY, header_class, canonical, load_surface and declared_surfaces from the sibling through its resolved script-directory sys.path entry.
- Emits sorted change rows before declaration-ordered surface rows and one summary.
- Uses directive multisets, directive-name sets and a single changed numeric parameter to select the frozen classes.
- Implements all eight classes and decisive unclassified verdict propagation.
- Implements --selftest with retained-body fixtures, all classes, repeated directives, parameter-presence and multiple-numeric changes, reordered-only output, canonicalization and a receipt fault.
- Documents grammar, offline construction and exit codes in the production module docstring.
- LSP unavailable: no LSP definitions/references/refactoring tool is exposed in this seat; inspected sibling definitions directly.

## Executed commands and byte-exact stdout
Data runs explicitly requested by the assignment were executed; no build, lint, formatter, counter, or selftest was run.
Each stdout file below contains only stdout bytes; adjacent .exit.txt and .stderr.txt files retain status and stderr separately.

### real-pair
`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/policy_value_class.py --a /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-81/capture --b /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-82/capture --declared /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-81/capture-expectations.json`
Exit code: 0. Stderr: ''.
Receipt: .ufo/waves/round-84/w1/ExecPolicyTool/tool-real-pair.txt
```text
surface=ds4cc-primary changed=0 reordered=0 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-unchanged
surface=ds4cc-robots changed=0 reordered=0 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-unchanged
surface=ds4cc-sitemap changed=0 reordered=0 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-unchanged
summary surfaces=3 changed=0 reordered=0 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-unchanged
```

### ctl-control
`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/policy_value_class.py --a /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/capture-control/control/a --b /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/capture-control/control/b --declared /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-81/capture-expectations.json`
Exit code: 0. Stderr: ''.
Receipt: .ufo/waves/round-84/w1/ExecPolicyTool/tool-ctl-control.txt
```text
change surface=ds4cc-primary header=cache-control class=numeric_parameter
change surface=ds4cc-robots header=x-frame-options class=header_added
change surface=ds4cc-sitemap header=referrer-policy class=reordered
surface=ds4cc-primary changed=1 reordered=0 numeric_parameter=1 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-changed
surface=ds4cc-robots changed=1 reordered=0 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=1 header_removed=0 unclassified=0 verdict=policy-changed
surface=ds4cc-sitemap changed=1 reordered=1 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-rewritten-equivalent
summary surfaces=3 changed=3 reordered=1 numeric_parameter=1 directive_added=0 directive_removed=0 directive_changed=0 header_added=1 header_removed=0 unclassified=0 verdict=policy-changed
```

### ctl-equivalent
`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/policy_value_class.py --a /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/capture-control/equivalent/a --b /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/capture-control/equivalent/b --declared /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-81/capture-expectations.json`
Exit code: 0. Stderr: ''.
Receipt: .ufo/waves/round-84/w1/ExecPolicyTool/tool-ctl-equivalent.txt
```text
change surface=ds4cc-sitemap header=referrer-policy class=reordered
surface=ds4cc-primary changed=0 reordered=0 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-unchanged
surface=ds4cc-robots changed=0 reordered=0 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-unchanged
surface=ds4cc-sitemap changed=1 reordered=1 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-rewritten-equivalent
summary surfaces=3 changed=1 reordered=1 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-rewritten-equivalent
```

## Frozen expectations comparison
- Real pair: no changed policy headers; summary policy-unchanged, changed=0.
- control ds4cc-primary/cache-control: numeric_parameter, matches frozen expected numeric_parameter.
- control ds4cc-robots/x-frame-options: header_added, matches frozen expected header_added.
- control ds4cc-sitemap/referrer-policy: reordered, matches frozen expected reordered.
- equivalent ds4cc-sitemap/referrer-policy: reordered, matches frozen expected reordered.
- Control summary policy-changed and equivalent summary policy-rewritten-equivalent match the expectation document.

## Retained evidence and restrictions
- All three assigned data commands returned exit 0; their stdout is reproduced in full above.
- No credentials, session material, network, VCS mutation, external substrate, installation or background work was used.
- No scratch directory was created; therefore no scratch tree remains.
- Frozen controls/* was not written: the requested destination conflicts with hard rule 4 and the higher-priority write boundary. Main was notified; parent must promote retained receipts if authorized.
- tool-selftest.txt was not manufactured: developer wave rules reserve tests and post-integration gates for the parent.
- Parent checks: run the tool --selftest --work /fast/scratch/hyaku/kake-r84/<parent-seat>/tool-selftest, retain stdout/status, then run the frozen C2 counter after authorized real-record placement.
- Full C2 admission is not claimed; record_equal and selftest_ok are not measured by this seat.

## Self-evaluation
- Accuracy 4/5: the three observed data runs match frozen expected rows; selftest remains unexecuted.
- Completeness 3/5: implementation and all data evidence complete; frozen-path conflict and wave test restriction prevent requested destination/selftest receipts.
- Clarity 4/5: exact commands, rows and conflicts retained; parent must distinguish advisory receipt paths from frozen record path.
- Actionability 4/5: parent has the exact stdout to promote and named deferred gate; promotion is outside seat scope.
- Conciseness 4/5: full stdout intentionally repeats counter keys to satisfy evidence requirement.
- Overall 3.8/5. Improvements by impact: parent executes selftest; parent resolves frozen-record destination authorization.
- User agreement check: partial verification is explicitly separated from production implementation.

## Verdict
Scoped production implementation complete. Three assigned data runs exit 0 and match frozen expectations. Selftest execution and frozen controls record placement are deferred to the parent under higher-priority wave/write restrictions; no C2 gate verdict asserted.
