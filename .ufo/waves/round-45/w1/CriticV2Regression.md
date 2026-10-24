# CriticV2Regression — driver-v2 regression surface

## Axes and result

- Primary axis: **operability** (CLI compatibility, reproducible receipt navigation, honest verdicts). Related axis: **freshness** (retaining provenance and the class/legacy split needed to re-derive receipts).
- Named attack: silently remove or reinterpret a v1 interface while preserving the headline witnessed count.
- **V2 compatibility / honest-verdict-equality check: FAIL TO ESTABLISH — candidate unavailable at inspection.** The scoped round-45 directory listing contained no candidate driver; the exact `c45*.py` discovery returned `No files found matching pattern`. Per the assignment's absent-artifact branch, I did not wait for another seat. No actual v2 field deletion or runtime regression is alleged.
- **V1 `--selftest`: PASS**, exit 0. The CLI help and missing-required-flag behavior were also exercised. V2 `--selftest`, v2 source comparison, and a full honest-cohort comparison are **UNRUN** because no v2 driver was available. The full audit was not run against either version.
- This report supplies the complete source-derived baseline and the check required for each surface, not an admission or canonical judgment.

## Strongest available counterexample

The committed `repeat-len-band` row is a **mixed** witness, not a class-only witness:

```json
{
  "name": "repeat-len-band",
  "exit": 1,
  "met": false,
  "equalRuns": "19/21",
  "seed": 187926495163792,
  "caughtBy": ["G7", "T5"],
  "receipt": "tools/repeat-len-band.json",
  "error": null,
  "classCaught": ["G7"],
  "legacyCaught": ["T5"]
}
```

The referenced counter receipt independently has `runs.G7.equal=false` and `runs.T5.equal=false`. The frozen transcript contains this exact line:

```text
  witnessed-by-class repeat-len-band caughtBy=G7,T5
```

Consequently, replacing `caughtBy` or `witnessedByClass[name]` with class-only keys, removing `legacyCaught`, or printing only `G7` preserves the 27/27 headline but silently destroys an existing distinction. This is a concrete baseline counterexample to a narrowed compatibility check, **not evidence that absent v2 made that change**.

**Smallest safe correction/check:** retain all v1 fields and all caught keys in their original order; derive `classCaught` and `legacyCaught` separately from the same complete caught list and the summary's exact `classKeys`. Add this real mixed row to the eventual field-level comparison. Do not rename the JSON mapping to the stdout spelling: JSON is `witnessedByClass`, stdout is `witnessed-by-class`.

Receipt re-derivation also needs `rows[].receipt` and each `build[].receipt` to resolve relative to the summary's directory, the raw receipt files to remain at those locations, `counterSha256` to identify the counter bytes, and `seed` to identify the sampled run. `name`, `path`, and `sha256` tie the row back to the control. `equalRuns`, `exit`, `error`, `met`, and the caught-key partition must not disappear merely because the overall verdict agrees. `toolSha256` and `seat` are **not** v1 summary-row fields: v1 computes/reads them internally but its published row projection omits them. Their absence alone would not demonstrate a v2 regression.

## Enumeration and checks needed

All baseline semantics below come from the complete 228-line frozen `.ufo/waves/round-44/c44_audit.py` (SHA-256 recorded below), corroborated where stated by existing committed receipts. Except for the three CLI commands in the evidence section, these are **source-derived checks to run once v2 exists**, not checks claimed as exercised.

### CLI and defaults

| Surface | V1 observable behavior | Required v2 check |
|---|---|---|
| `-h`, `--help` | argparse help, exit 0; lists the flags below | Compare flag/choice inventory; distinguish the necessarily renamed executable in usage from any actual option change |
| `--selftest` | Boolean, default false; runs before required-field validation; exit 0 on passing assertions; no summary, `tools/`, or builds created by this branch | Run both selftests; retain every old assertion and allow the explicitly requested new rejection assertions |
| `--root ROOT` | Default `None`; required unless selftest; converted to absolute path | Compare omitted-flag error, relative/absolute roots, and counter argv |
| `--controls CONTROLS` | Default `None`; required unless selftest; opened relative to caller's cwd, not rebased under `root` | Compare the same TSV launched from a non-root cwd |
| `--counter COUNTER` | Default `None`; required unless selftest; converted to absolute path; imported and SHA-256 hashed | Compare relative/absolute counter paths and the summary's root-relative counter identifier |
| `--classes {v4,v5}` | Default `None`; required unless selftest; only these choices; forwarded unchanged | Test both modes and invalid choice; ensure v4 has no class witnesses |
| `--expect {blind,witnessed,not-met}` | Default `None`; required unless selftest; only these choices | Test all three honest outcome classes and invalid choice |
| `--build-rev BUILD_REV` | Default `None`; passed to child as `--revision` only when both build options are truthy | Compare child argv and revision selection |
| `--build-runs BUILD_RUNS` | Integer, default 0; builds run only if revision and count are truthy; positive count without revision produces no builds; no explicit nonnegative validation | Check default/no-revision/zero/positive cases; identify deliberate validation changes rather than silently attributing them to equality |
| `--workers WORKERS` | Integer, default 4; control executor uses `max(1, workers)` | Compare ordering and behavior at 0, negative, 1, and 4; do not change output ordering with completion order |
| `--out OUT` | Default `None`; required unless selftest; summary path as provided; receipt base is its absolute parent | Check path resolution, parent creation, summary basename independence, and receipt links |
| `--label LABEL` | Default empty string; summary stores it exactly; only stdout substitutes `kake-r44` for a falsey label; label is not forwarded to child counters | Compare absent/empty/custom labels, including the default stdout identity; name any intentional default-identity change |
| argparse behavior | Unknown options/bad choices/bad integer/missing required fields exit 2; required-field checks occur in root, controls, counter, classes, expect, out order | Compare rejection class and useful diagnostics; source verification should catch any added required option |
| selftest plus other flags | Required-field checks are bypassed, but argparse still parses supplied flags and choices first | Check `--selftest` without other flags and with a syntactically invalid supplied choice |

### Inputs, child invocation, errors, and receipt layout

| Surface | V1 observable behavior | Required v2 check |
|---|---|---|
| TSV format | Skips blank/whitespace-only lines and lines beginning with `#`; every other row must split into exactly six tab-separated values: name, family, class, path, sha256, seat; preserves TSV order | Use an honest multirow TSV including comments/blanks; compare selected metadata and ordering; do not silently introduce a header interpretation |
| Control identity | Tool path is `os.path.join(abs_root, row.path)`; compares actual file SHA-256 with TSV SHA before calling counter | Compare valid control and missing/mismatched file behavior |
| SHA failure row | `exit=2`, `met=null`, fixed error `control sha256 mismatch or file missing`; published `equalRuns`, `seed`, `caughtBy`, `receipt` become null; `classCaught`/`legacyCaught` are empty arrays | Compare the error row's key set, nulls, and error spelling, not merely final exit |
| Child argv | Current `sys.executable`, `-B`, absolute counter, `--root`, absolute root, `--classes`, mode, `--out`, receipt path; controls add `--tool-file`; builds add `--revision` | Capture/compare argv using an honest instrumented counter when available |
| Seed/cwd/environment | Driver passes no `--seed`, so counter chooses/records its seed; subprocess inherits caller cwd/environment and receives DEVNULL stdin | Compare protocol, not random seed values across independent runs; ensure driver does not silently pin seeds |
| Child I/O/time limit | Captures stdout/stderr; 900-second child timeout; on receipt-read/JSON failure `rec=None`; decoded UTF-8 replacement and last 2000 characters of stderr or stdout supply row error | Check failed-child/no-receipt diagnostic retention and encoding; timeouts/OSErrors currently propagate rather than becoming a successful audit |
| Existing output directory | V1 `makedirs(tools_dir, exist_ok=True)` reuses existing parents and permits overwrite of named outputs; it neither cleans nor isolates a reused cohort | Explicitly distinguish the proposed freshness hardening from compatibility; see tradeoff below |
| Per-control layout | Always `<absolute parent of --out>/tools/<name>.json`; names are not sanitized or disambiguated by v1 | Compare ordinary honest names; preserve link/layout compatibility, and identify any separately intended input-validation change |
| Build layout | Sibling files `<outdir>/build-1.json` through `build-N.json`, one-based; **not** under `tools/`; at most `min(3,N)` concurrent build workers | Check exact names, location, count, run order, and relative receipt paths for N=3 |
| Retention | Child receipts retained on disk; no success cleanup; summary does not embed the full runs/ratios for each control | Re-derive every row via its receipt path, including raw `runs` and provenance fields |
| Summary write | JSON indentation is 1, followed by newline; written before stdout and final expectation exit; not atomic in v1 | Compare serialization shape and presence on failed expectations; do not silently suppress failed-run evidence |
| Counter module contract | Imported before controls are scored; needs `PREDICATE`; v5 needs ordered `CLASS_MODULES`; v4 does not enumerate class modules | Compare module/CLI coupling and class-key order; import/hash errors currently raise rather than produce a verdict |

### Summary JSON: all 19 fields

| Field | V1 value/semantics | Required v2 check |
|---|---|---|
| `label` | Exact argument, including empty string | Same key/type/default/value |
| `classesMode` | `v4` or `v5` | Same key/mode |
| `expect` | Requested expectation | Same key/value |
| `counter` | `os.path.relpath(abs_counter, abs_root)` | Preserve identity/path semantics, allowing the explicitly selected new counter path |
| `counterSha256` | SHA-256 of invoked counter file | Match selected counter bytes; do not reuse frozen hash for new bytes |
| `predicate` | Imported module's `PREDICATE` | Retain field and provenance; counter predicate repair must not be confused with driver schema drift |
| `controls` | Number of result rows with falsey `error`, not TSV length unconditionally | Compare on honest rows and classify intended invalid-receipt changes separately |
| `classKeys` | Ordered `CLASS_MODULES` keys for v5; empty array for v4 | Same mode-dependent set and order |
| `witnessed` | Number of semantic witnesses | Honest equality, not only headline equality on invalid fixtures |
| `witnessedNames` | Witness names in TSV order | Preserve ordered membership |
| `witnessedByClass` | Mapping witness name to **complete** `caughtBy`, including legacy keys on mixed witnesses | Check `repeat-len-band` maps to `["G7","T5"]`, not just `["G7"]` |
| `notMet` | Number of rows with `met is False`, regardless of caught-key class in v1 | Honest equality; explicitly expected invalid-receipt filtering is not an honest regression |
| `notMetNames` | Those names in TSV order | Compare ordered membership |
| `metNames` | Names with `met is True`, in TSV order | Retain field and strict boolean semantics |
| `errors` | Names whose row error is truthy, in TSV order | Retain array-of-names shape; invalid fixtures may intentionally add names |
| `build` | Ordered build-row array, empty if build gate not entered | Preserve schema/order and one-based naming; intended count pin must not drop fields |
| `rows` | One projected row per input control in input order, including errors | Compare complete key set and values, not just successful rows |
| `ok` | Boolean expectation result | Compare all honest expectation scenarios and aggregate exit agreement |
| `verdict` | `witnessed W/T notMet=N`, with ` build met B/R` appended iff build array nonempty | Compare exact labels, spacing, denominator semantics, and optional suffix |

### Control-row JSON: all 14 fields

| Field | V1 value/semantics | Required v2 check |
|---|---|---|
| `name` | TSV name, not renamed receipt stem | Exact identity |
| `family` | TSV family | Preserve metadata |
| `class` | TSV declared class, not inferred catching class | Preserve distinction from caught keys |
| `path` | TSV tool path, not rewritten to absolute | Preserve identity/path spelling |
| `sha256` | TSV expected control hash | Preserve expected bytes identity |
| `exit` | Child returncode, or 2 on control SHA mismatch | Preserve raw result; invalid-returncode credit must be rejected without misreporting exit |
| `met` | Receipt `met`, else null | Preserve boolean/null distinction; invalid receipt handling must remain diagnosable |
| `equalRuns` | Receipt `equalRuns`, else null | Preserve string such as `19/21`; do not replace with a numeric count |
| `seed` | Receipt seed, else null | Retain exact recorded integer; compare shape/presence, not fresh-run random equality |
| `caughtBy` | Every receipt run whose `equal is False`, in receipt insertion order; empty array on a normal no-catch run; null on SHA failure | Preserve all run keys, exact false check, order, and error/null distinction |
| `receipt` | Path relative to summary directory, typically `tools/<name>.json`; null on SHA failure | Resolve it and compare raw receipt; do not resolve relative to repo root |
| `error` | null for a truthy parsed receipt in v1, otherwise stderr-or-stdout tail; fixed SHA error on mismatch | Preserve key and useful diagnostics; hardening is expected to add errors for invalid receipts |
| `classCaught` | `caughtBy` filtered by membership in mode's class-key set, preserving order; empty in v4 | Compare exact array, especially mixed witnesses |
| `legacyCaught` | Complementary caught keys, preserving order; includes timing and other non-class keys | Retain complement; it is necessary for class-only versus mixed classification |

### Build-row JSON: all 8 fields

| Field | V1 value/semantics | Required v2 check |
|---|---|---|
| `run` | One-based integer | `[1,2,3]` for three builds |
| `exit` | Child returncode | Preserve raw returncode independently of validity |
| `met` | Receipt met or null | Preserve boolean/null |
| `seed` | Receipt seed or null | Preserve exact recorded seed |
| `equalRuns` | Receipt equalRuns or null | Preserve ratio-like string |
| `ratios` | Receipt ratios or null | Preserve per-shape mapping/numbers; not present on control projection |
| `receipt` | `build-N.json`, relative to summary directory | Check file existence and raw receipt |
| `error` | null for truthy parsed receipt, otherwise stderr-or-stdout tail in v1 | Preserve field and diagnostics; explicitly classify intended validity errors |

### Witness predicates, expectation verdicts, stdout, and exits

| Surface | V1 observable behavior | Required v2 check |
|---|---|---|
| Semantic witness | Strict `met is False`, nonempty caughtBy, at least one string key in exact class-key set; mixed is a witness; legacy-only/timing-only is not; v4 has none | Pass, class-only, mixed, legacy-only, timing-only, empty-class cases; preserve all old selftest assertions |
| `blind` | All expected rows error-free, no witnesses, every control `met is True`; build results do not enter this v1 predicate | Compare honest v4/pass cohort; name any deliberate build-validity expansion |
| `witnessed` | All expected controls error-free and witnessed; at least one build; every build `met is True`; v1 does not pin requested build count | Compare honest class/mixed plus three builds; count pin is requested hardening, not a silent honest change |
| `not-met` | All expected controls error-free and `met is False`; does not require witnesses or builds | Include an honest legacy-only not-met row; do not accidentally require a class witness |
| Empty controls | V1 blind/not-met are vacuously true with zero rows; witnessed can be true with zero rows if a nonempty all-met build list exists | Explicit edge comparison; do not silently add a minimum cohort size under an equality claim |
| Stdout header | `AUDIT <label-or-kake-r44> classes=<mode> classKeys=<comma-keys-or-> witnessed=W/T[ v4-note] notMet=N build_met=B/R ok=<True-or-False> counter=<12 hex>` | Compare token names/order, Python boolean spelling, default label, and abbreviated hash |
| v4 note | Exact ` (no class runs; witnessed=0 by construction)` in header | Preserve mode-specific explanation |
| Row lines | `  %-20s %-10s met=%-5s caught=%-22s %s`, using name, declared class, met, comma-joined complete caughtBy or `-`, and error or empty | Compare fixed-width layout and all-caught-key reporting |
| Witness text | `  witnessed-by-class <name> caughtBy=<comma-joined complete caughtBy>`; one line per witness, input order | Preserve spelling, two leading spaces, key order, and mixed legacy keys |
| Build text | `  build#<run> met=<value> equal=<equalRuns> <error-or-empty>` after witness lines | Preserve one-based IDs and ordering |
| Audit exit | 0 iff `ok`, otherwise 1; selftest/help 0; parser errors 2; uncaught operational failures propagate rather than pretending an expectation was evaluated | Compare actual exits, JSON ok, and printed ok together; a failed parser/exception is not an honest not-met verdict |
| Invalid receipts | Frozen v1 may grant credit to bad counter exit / tool-absent / stale receipts | This is the expressly targeted behavior change, not a behavior to preserve; compare honest shape separately from malicious acceptance |

## Proposed-policy compatibility risk (not an observed implementation defect)

The inspected proposal text at `make_w1_spec.py:184-186` says v2 will refuse a nonempty output cohort. V1 instead reuses `dirname(--out)` and `tools/`. Therefore rerunning into an existing cohort, or placing `--out` in an existing populated directory, is an observable operability change even when every candidate/control is honest. This is a deliberate freshness-versus-reuse tradeoff in the proposal, not a defect demonstrated in absent v2. It must be disclosed and evaluated separately from field/CLI compatibility; a headline 27/27 equality test does not exercise it. The smallest safe treatment is to preserve the public receipt names/links and document/enforce the fresh-cohort precondition explicitly, not quietly reinterpret `--out` as a different directory layout. No attempt was made to weaken the freshness gate.

## Decisive commands and verbatim output

All shell commands ran with cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`.

### Frozen bytes

Command:

```sh
sha256sum .ufo/waves/round-44/c44_audit.py
```

Output:

```text
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
```

### V1 selftest

Command:

```sh
python3 -B .ufo/waves/round-44/c44_audit.py --selftest
```

Exit: 0. Output:

```text
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
```

### CLI inventory

Command:

```sh
python3 -B .ufo/waves/round-44/c44_audit.py --help
```

Exit: 0. Output:

```text
usage: c44_audit.py [-h] [--selftest] [--root ROOT] [--controls CONTROLS]
                    [--counter COUNTER] [--classes {v4,v5}]
                    [--expect {blind,witnessed,not-met}]
                    [--build-rev BUILD_REV] [--build-runs BUILD_RUNS]
                    [--workers WORKERS] [--out OUT] [--label LABEL]

options:
  -h, --help            show this help message and exit
  --selftest
  --root ROOT
  --controls CONTROLS
  --counter COUNTER
  --classes {v4,v5}
  --expect {blind,witnessed,not-met}
  --build-rev BUILD_REV
  --build-runs BUILD_RUNS
  --workers WORKERS
  --out OUT
  --label LABEL
```

### Missing-required-flag behavior

Command:

```sh
python3 -B .ufo/waves/round-44/c44_audit.py --root .
```

Exit: 2. Output:

```text
usage: c44_audit.py [-h] [--selftest] [--root ROOT] [--controls CONTROLS]
                    [--counter COUNTER] [--classes {v4,v5}]
                    [--expect {blind,witnessed,not-met}]
                    [--build-rev BUILD_REV] [--build-runs BUILD_RUNS]
                    [--workers WORKERS] [--out OUT] [--label LABEL]
c44_audit.py: error: --controls is required unless --selftest is used
```

### V2 discovery

Exact specialized-tool call (not a claimed shell execution):

```json
{"path":"/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45*.py","hidden":true,"gitignore":false,"limit":100}
```

Verbatim glob result:

```text
No files found matching pattern
```

### Actual published field sets

Exact `read` path/query:

```text
/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/verification/claim/after-final/after-v5.json?q={summaryKeys:keys,rowKeys:(.rows[0]|keys),buildKeys:(.build[0]|keys),label,classesMode,expect,counter,counterSha256,classKeys,controls,witnessed,notMet,metNames,errors,ok,verdict}
```

Verbatim result:

```json
{
  "summaryKeys": [
    "build",
    "classKeys",
    "classesMode",
    "controls",
    "counter",
    "counterSha256",
    "errors",
    "expect",
    "label",
    "metNames",
    "notMet",
    "notMetNames",
    "ok",
    "predicate",
    "rows",
    "verdict",
    "witnessed",
    "witnessedByClass",
    "witnessedNames"
  ],
  "rowKeys": [
    "caughtBy",
    "class",
    "classCaught",
    "equalRuns",
    "error",
    "exit",
    "family",
    "legacyCaught",
    "met",
    "name",
    "path",
    "receipt",
    "seed",
    "sha256"
  ],
  "buildKeys": [
    "equalRuns",
    "error",
    "exit",
    "met",
    "ratios",
    "receipt",
    "run",
    "seed"
  ],
  "label": "",
  "classesMode": "v5",
  "expect": "witnessed",
  "counter": ".ufo/waves/round-44/c44_count_v5.py",
  "counterSha256": "5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc",
  "classKeys": [
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
    "G6",
    "G7",
    "G8",
    "G9",
    "G10"
  ],
  "controls": 27,
  "witnessed": 27,
  "notMet": 27,
  "metNames": [],
  "errors": [],
  "ok": true,
  "verdict": "witnessed 27/27 notMet=27 build met 3/3"
}
```

This is the existing summary's content, not a fresh certification or a re-declaration of a frozen round claim. The underlying receipts must be opened to re-derive the current committed evidence.

## Remaining evidence and activity ledger

Additional inspected source/data:

- `read` of frozen `c44_audit.py:1-240` (all 228 lines returned), the round-45 directory, `.ufo/waves/round-44/verification`, `c44_count_v5.py:1-120`, and `make_w1_spec.py:177-204`.
- `read` of `verification/claim/after-final.txt:1-90` under round-44, including all 58 transcript lines.
- Exact mixed-row query on round-44 `verification/claim/after-final/after-v5.json`: `?q={mixed:(.rows|map(select((.classCaught|length)>0 and (.legacyCaught|length)>0))),firstBuild:.build[0]}`.
- Exact raw mixed-receipt query on round-44 `verification/claim/after-final/tools/repeat-len-band.json`: `?q={met,seed,equalRuns,note,runs:(.runs|with_entries(select(.value.equal==false))),keys:keys}`.
- Exact raw build-receipt query on round-44 `verification/claim/after-final/build-1.json`: `?q={met,seed,equalRuns,ratios,note,keys:keys}`. It corroborated the row's seed, `21/21`, and T1-T5 ratios.
- `grep` for `witnessedByClass|classCaught|legacyCaught|\["rows"\]|\["receipt"\]|build-%d` over round-44/round-45 `*.py` (case-sensitive, gitignore disabled); and `honest verdict|[Kk]ill rule|[Kk]ill|c45_audit.py|--selftest` over round-45 `make_w1_spec.py:100-240`.
- Read required `skill://godspeed` and `/home/vgpnk/.omp/agent/RULES.md`. No tools were installed or upgraded.
- Exact only other shell command: `mkdir -p /fast/scratch/hyaku/kake-r45/CriticV2Regression` (success, no output).

## Files written and blockers

- **Only file written:** `.ufo/waves/round-45/w1/CriticV2Regression.md` (this report).
- Created the permitted scratch directory `/fast/scratch/hyaku/kake-r45/CriticV2Regression/`; no scratch files were needed.
- No driver, counter, fixture, receipt, corpus, state, history, or frozen file was edited. No commit, push, integration, alternate runtime, or subagent dispatch was performed.
- **Exact blocker:** `.ufo/waves/round-45/c45_audit.py` was absent at inspection. This prevents source diff, candidate selftest, and observed v2 compatibility conclusions. The absent-artifact deliverable is complete; the table above names the outstanding main-agent checks without claiming they ran.
