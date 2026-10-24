# R22 wave 2 — MutateDuplicates

## Result

**Mutant KILLED.** Removing the multiple-canonical guard makes both frozen duplicate cases incorrectly report `clean` with CLI exit 0. The unchanged frozen detector rejects both results: targeted detector exit 1, whole-matrix detector exit 1, 30/32 accepted. Pristine and byte-restored controls each accept 32/32, including `canonical_multiple` with CLI exit 1 for both duplicate cases. This is author-side mutation evidence only, not independent admission or a shipping decision.

- Stable probe ID: `R22-W2-MutateDuplicates-01`.
- Contract finding ID challenged: `canonical_multiple`.
- Axes: operability (duplicate-policy regression detection), isolation (private source mutation only), restoration (exact original bytes and recovered controls).
- Scope: one assigned mutation; no additional mutation or contract change.

## Frozen inputs and isolation

- Required contract read: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json`.
- Private clone created with `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r22-w2-MutateDuplicates`.
- Observed private `HEAD -> master`, `origin/master`, and `origin/HEAD`: **`c0fd6d53906a42dadfb997ddda2c8162f1adb78a`**, subject `round-22: offline canonical publishing preflight`. The contract's `7c61c8cc791bde36dd5e3688bdfea2678d90146c` is the historical BEFORE revision, not this probe's candidate.
- Read-only lane status inspection showed no uncommitted target, detector, cases, or fixture changes. Existing changes were wave-dispatch/reporting artifacts. No production overlay copy was needed; the live and private target, detector, and cases hashes matched.
- The only source mutation was in `/tmp/kake-r22-w2-MutateDuplicates/scripts/canonical_audit.py`. No lane or sibling source, index, or jj state was written.
- The detector and fixtures were read from the frozen live wave directory. No detector, oracle, or fixture bytes were edited. The sole live write by this seat is this assigned report.

Observed unchanged detector/input SHA-256 values, identical in lane and private clone:

| Input | SHA-256 |
| --- | --- |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py` | `d7de622cf149c4a7a0d3152b3d6c0560fadcc4c0c784c764502d0a2110bf4aab` |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/cases.json` | `28a49013d3aaf72b0e1c3801fd5359592602e079408d9a71c99f2df03d1cbeb6` |

## Exact mutant

Delete the two-line cardinality guard in `evaluate_page`, originally lines 563–564. This leaves the existing `parser.head_canonicals[0]` path to evaluate only the first canonical. The frozen duplicate fixtures both put a matching URL first; their second URLs respectively agree and disagree.

```diff
--- /tmp/kake-r22-w2-MutateDuplicates/scripts/canonical_audit.py
+++ /tmp/kake-r22-w2-MutateDuplicates/scripts/canonical_audit.py
@@ -563,2 +562,0 @@
-    if len(parser.head_canonicals) > 1:
-        return "canonical_multiple"
```

No selftest expectation, case expectation, fixture, or other branch was changed.

## Expected detector and commands

The fixed public-CLI detector must continue to demand exit **1** and stable finding **`canonical_multiple`** for both `duplicate_same` and `duplicate_different`. A mutant returning exit 0 or a different finding must produce detector exit 1, not an accepted case.

The same two commands were exercised on pristine, mutated, and restored source bytes. For the mutation and restoration phases, the targeted command completed before the whole matrix began. The pristine commands were independent read-only controls run concurrently against unchanged source.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /tmp/kake-r22-w2-MutateDuplicates --case duplicate_same --json
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /tmp/kake-r22-w2-MutateDuplicates --json
```

Working directory: `/tmp/kake-r22-w2-MutateDuplicates`.

The frozen detector invokes the public `python3` manifest CLI with `--json`, captures actual stdout/stderr/exit, and compares exact exit and finding IDs. Each CLI subprocess has the detector's existing 60-second timeout. Outer calls were bounded at 90 seconds for the pristine targeted call and 300 seconds for each remaining detector call. No builds, lint, formatters, network access, host services, credentials, or package transactions were used.

## Observed detector results

Detector exit and audited CLI exit are different: a correct rejection has CLI exit 1 but detector exit 0.

| Source phase | Selection | Detector exit | Accepted / total | Executed | Discrepancies | Missing tool |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Pristine | `duplicate_same` | 0 | 1 / 1 | 1 | 0 | false |
| Pristine | all frozen cases | 0 | 32 / 32 | 32 | 0 | false |
| Mutated | `duplicate_same` | 1 | 0 / 1 | 1 | 1 | false |
| Mutated | all frozen cases | 1 | 30 / 32 | 32 | 2 | false |
| Restored | `duplicate_same` | 0 | 1 / 1 | 1 | 0 | false |
| Restored | all frozen cases | 0 | 32 / 32 | 32 | 0 | false |

Exact targeted pristine detector stdout (one JSON line, followed by a newline):

```json
{"selection": "duplicate_same", "accepted": 1, "total": 1, "executed": 1, "discrepancies": 0, "toolMissing": false, "results": [{"caseId": "duplicate_same", "status": "PASS", "expectedExit": 1, "actualExit": 1, "expectedFindings": ["canonical_multiple"], "actualFindings": ["canonical_multiple"], "stdout": "{\"findings\":[{\"id\":\"canonical_multiple\",\"page\":\"https://example.test/project/a.html\"}],\"pagesChecked\":1,\"verdict\":\"failed-policy\"}\n", "stderr": ""}]}
```

The mutated targeted detector reported:

```text
FAIL caseId=duplicate_same expectedExit=1 actualExit=0 expectedFindings=canonical_multiple actualFindings=clean
```

The mutated full matrix reported these two and only these two discrepancies:

```text
FAIL caseId=duplicate_same expectedExit=1 actualExit=0 expectedFindings=canonical_multiple actualFindings=clean
FAIL caseId=duplicate_different expectedExit=1 actualExit=0 expectedFindings=canonical_multiple actualFindings=clean
```

For each duplicate case, exact observed public-CLI stdout on pristine and restored bytes was:

```json
{"findings":[{"id":"canonical_multiple","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

For each duplicate case, exact observed public-CLI stdout on mutated bytes was:

```json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

Each CLI JSON object was followed by a newline. All captured CLI stderr values in all matrix phases were empty. The mutation/restoration harness also captured empty detector stderr. `clean` in the case tables is the frozen detector's sentinel for an empty findings array, not a finding emitted by the CLI.

### Whole-matrix actual exits and stable IDs

Each cell is `actualExit / actualFindings`. Pristine and restored values matched each frozen expected value. Mutated values matched except for the two bold duplicate rows.

| Frozen case ID | Pristine | Mutated | Restored |
| --- | --- | --- | --- |
| `absolute_match` | 0 / clean | 0 / clean | 0 / clean |
| `relative_same_dir` | 0 / clean | 0 / clean | 0 / clean |
| `relative_parent` | 0 / clean | 0 / clean | 0 / clean |
| `root_relative` | 0 / clean | 0 / clean | 0 / clean |
| `scheme_relative` | 0 / clean | 0 / clean | 0 / clean |
| `first_base` | 0 / clean | 0 / clean | 0 / clean |
| `second_base_ignored` | 0 / clean | 0 / clean | 0 / clean |
| `rel_token_list` | 0 / clean | 0 / clean | 0 / clean |
| `rel_uppercase` | 0 / clean | 0 / clean | 0 / clean |
| `attr_uppercase` | 0 / clean | 0 / clean | 0 / clean |
| `entity_href` | 0 / clean | 0 / clean | 0 / clean |
| `query_preserved` | 0 / clean | 0 / clean | 0 / clean |
| `missing_link` | 1 / canonical_missing | 1 / canonical_missing | 1 / canonical_missing |
| **`duplicate_same`** | **1 / canonical_multiple** | **0 / clean** | **1 / canonical_multiple** |
| **`duplicate_different`** | **1 / canonical_multiple** | **0 / clean** | **1 / canonical_multiple** |
| `body_link` | 1 / canonical_outside_head | 1 / canonical_outside_head | 1 / canonical_outside_head |
| `href_absent` | 1 / canonical_href_missing | 1 / canonical_href_missing | 1 / canonical_href_missing |
| `href_empty` | 1 / canonical_href_missing | 1 / canonical_href_missing | 1 / canonical_href_missing |
| `invalid_url` | 1 / canonical_url_invalid | 1 / canonical_url_invalid | 1 / canonical_url_invalid |
| `javascript_url` | 1 / canonical_url_invalid | 1 / canonical_url_invalid | 1 / canonical_url_invalid |
| `data_url` | 1 / canonical_url_invalid | 1 / canonical_url_invalid | 1 / canonical_url_invalid |
| `fragment_url` | 1 / canonical_fragment | 1 / canonical_fragment | 1 / canonical_fragment |
| `wrong_host` | 1 / canonical_mismatch | 1 / canonical_mismatch | 1 / canonical_mismatch |
| `wrong_path` | 1 / canonical_mismatch | 1 / canonical_mismatch | 1 / canonical_mismatch |
| `wrong_query` | 1 / canonical_mismatch | 1 / canonical_mismatch | 1 / canonical_mismatch |
| `base_invalid` | 1 / base_url_invalid | 1 / base_url_invalid | 1 / base_url_invalid |
| `comment_decoy` | 0 / clean | 0 / clean | 0 / clean |
| `script_decoy` | 0 / clean | 0 / clean | 0 / clean |
| `template_decoy` | 0 / clean | 0 / clean | 0 / clean |
| `missing_head` | 2 / html_unsupported | 2 / html_unsupported | 2 / html_unsupported |
| `manifest_traversal` | 2 / input_invalid | 2 / input_invalid | 2 / input_invalid |
| `symlink_html` | 2 / input_invalid | 2 / input_invalid | 2 / input_invalid |

## Exact restoration evidence

Original bytes were captured before mutation at `/tmp/kake-r22-w2-MutateDuplicates.canonical_audit.original.py`. Restoration was in the mutation detector harness's `finally` block, so detector errors would still trigger restoration. It executed:

```sh
cp --preserve=mode,timestamps /tmp/kake-r22-w2-MutateDuplicates.canonical_audit.original.py /tmp/kake-r22-w2-MutateDuplicates/scripts/canonical_audit.py
cmp --silent /tmp/kake-r22-w2-MutateDuplicates.canonical_audit.original.py /tmp/kake-r22-w2-MutateDuplicates/scripts/canonical_audit.py
```

Observed copy exit: **0**. Observed byte-comparison exit: **0**.

| Byte state | SHA-256 |
| --- | --- |
| Captured original | `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` |
| Private pristine target | `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` |
| Private mutated target | `9964dd006f8dbcc93947ae69def425a8744eb6fafbf8d7828c9a34b3d33bfc34` |
| Private restored target | `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` |
| Live target before and after the probe | `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` |

After this exact-byte restoration, the same targeted detector returned 0 with `canonical_multiple`, and the same full matrix returned 0 with 32/32 accepted. The original production guard is present in the restored bytes; no mutant is left active.

## Scope of conclusion

The assigned guard-removal mutant was killed by the frozen instrument with valid pristine and recovered controls. This demonstrates sensitivity to this specific plausible duplicate-cardinality regression; it does not establish complete coverage of all duplicate parsing or broader canonical behavior. No survivor was relabeled as success, no contract was changed, and no integration/admission action was taken.

Tools installed or updated: **none**.

Report: .ufo/waves/round-22/w2/MutateDuplicates.md
