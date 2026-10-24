# MutateMismatch — bounded author-side mutation probe

## Scope and axes

- Assigned axis: **operability**; frozen claim C1, offline static canonical publishing preflight.
- Probe controls: single-point mutation, unchanged frozen detector/fixtures, meaningful pristine and restored controls, and byte-exact restoration. These are controls, not additional capability claims.
- Author-side falsification only; no independent admission, integration, shipping, or global correctness judgment.
- Lane and private-clone `master`/`HEAD` were observed at `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`. The earlier contract base `7c61c8cc791bde36dd5e3688bdfea2678d90146c` was not used as the candidate.
- Private clone: `/tmp/kake-r22-w2-MutateMismatch`, created with `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r22-w2-MutateMismatch`.
- The captured private audit source matched the live lane SHA-256. No uncommitted source/oracle/fixture copying was required. Only the private `scripts/canonical_audit.py` was mutated; live-lane source, fixtures, oracles, index, and jj state were not written.

## Mutant and expected detector

Disable the normalized canonical-versus-`expectedCanonical` equality check in `evaluate_page`, at source line 585. Valid but wrong host/path/query URLs then fall through as clean. This is one fail-open comparison mutation.

```diff
--- a/scripts/canonical_audit.py
+++ b/scripts/canonical_audit.py
@@ -582,7 +582,7 @@
         return "canonical_fragment"
     except ValueError:
         return "canonical_url_invalid"
-    if actual_url != expected_url:
+    if False and actual_url != expected_url:
         return "canonical_mismatch"
     return None
 
```

Expected kill: the frozen `wrong_path` case requires validator exit **1** and stable finding ID **`canonical_mismatch`**. With equality disabled, validator exit **0** / no findings must make the unchanged matrix detector fail. The full matrix should also detect `wrong_host` and `wrong_query`.

## Commands and bounds

The identical commands were run against pristine, mutated, and restored bytes, in the private clone. Direct CLI and selected-case controls completed before the whole matrix in each phase. Direct/selected runs had 20-second outer bounds; whole-matrix runs had a 120-second outer bound. The unmodified matrix launches the public CLI for each case.

```sh
python3 /tmp/kake-r22-w2-MutateMismatch/scripts/canonical_audit.py --manifest /tmp/kake-r22-w2-MutateMismatch/.ufo/waves/round-22/fixtures/wrong_path/manifest.json --json
python3 /tmp/kake-r22-w2-MutateMismatch/.ufo/waves/round-22/matrix.py --root /tmp/kake-r22-w2-MutateMismatch --case wrong_path --json
python3 /tmp/kake-r22-w2-MutateMismatch/.ufo/waves/round-22/matrix.py --root /tmp/kake-r22-w2-MutateMismatch --json
```

## Actual results

| Phase | Direct `wrong_path` exit / finding | Selected detector exit; accepted | Whole-matrix detector exit; accepted | Discrepancies |
|---|---|---|---|---|
| pristine | 1 / `canonical_mismatch` | 0; 1/1 | 0; 32/32 | 0 |
| mutated | 0 / `clean (empty findings)` | 1; 0/1 | 1; 29/32 | 3 |
| restored | 1 / `canonical_mismatch` | 0; 1/1 | 0; 32/32 | 0 |

Every matrix phase executed all 32 cases. All captured stderr streams were empty; there were no timeouts or probe exceptions.

### Exact public-CLI stdout

**pristine**, process exit `1`:
```json
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

**mutated**, process exit `0`:
```json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

**restored**, process exit `1`:
```json
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

### Exact selected-case detector stdout

**pristine**, detector exit `0`:
```json
{"selection": "wrong_path", "accepted": 1, "total": 1, "executed": 1, "discrepancies": 0, "toolMissing": false, "results": [{"caseId": "wrong_path", "status": "PASS", "expectedExit": 1, "actualExit": 1, "expectedFindings": ["canonical_mismatch"], "actualFindings": ["canonical_mismatch"], "stdout": "{\"findings\":[{\"id\":\"canonical_mismatch\",\"page\":\"https://example.test/project/a.html\"}],\"pagesChecked\":1,\"verdict\":\"failed-policy\"}\n", "stderr": ""}]}
```

**mutated**, detector exit `1`:
```json
{"selection": "wrong_path", "accepted": 0, "total": 1, "executed": 1, "discrepancies": 1, "toolMissing": false, "results": [{"caseId": "wrong_path", "status": "FAIL", "expectedExit": 1, "actualExit": 0, "expectedFindings": ["canonical_mismatch"], "actualFindings": ["clean"], "stdout": "{\"findings\":[],\"pagesChecked\":1,\"verdict\":\"clean\"}\n", "stderr": ""}]}
```

**restored**, detector exit `0`:
```json
{"selection": "wrong_path", "accepted": 1, "total": 1, "executed": 1, "discrepancies": 0, "toolMissing": false, "results": [{"caseId": "wrong_path", "status": "PASS", "expectedExit": 1, "actualExit": 1, "expectedFindings": ["canonical_mismatch"], "actualFindings": ["canonical_mismatch"], "stdout": "{\"findings\":[{\"id\":\"canonical_mismatch\",\"page\":\"https://example.test/project/a.html\"}],\"pagesChecked\":1,\"verdict\":\"failed-policy\"}\n", "stderr": ""}]}
```

### Complete matrix classifications

Each cell records actual validator exit, finding ID(s), and frozen-detector status. `clean` denotes the detector's representation of an empty findings array.

| Stable case ID | Expected exit / finding | Pristine | Mutated | Restored |
|---|---|---|---|---|
| `absolute_match` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `relative_same_dir` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `relative_parent` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `root_relative` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `scheme_relative` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `first_base` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `second_base_ignored` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `rel_token_list` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `rel_uppercase` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `attr_uppercase` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `entity_href` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `query_preserved` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `missing_link` | 1 / canonical_missing | 1 / canonical_missing / PASS | 1 / canonical_missing / PASS | 1 / canonical_missing / PASS |
| `duplicate_same` | 1 / canonical_multiple | 1 / canonical_multiple / PASS | 1 / canonical_multiple / PASS | 1 / canonical_multiple / PASS |
| `duplicate_different` | 1 / canonical_multiple | 1 / canonical_multiple / PASS | 1 / canonical_multiple / PASS | 1 / canonical_multiple / PASS |
| `body_link` | 1 / canonical_outside_head | 1 / canonical_outside_head / PASS | 1 / canonical_outside_head / PASS | 1 / canonical_outside_head / PASS |
| `href_absent` | 1 / canonical_href_missing | 1 / canonical_href_missing / PASS | 1 / canonical_href_missing / PASS | 1 / canonical_href_missing / PASS |
| `href_empty` | 1 / canonical_href_missing | 1 / canonical_href_missing / PASS | 1 / canonical_href_missing / PASS | 1 / canonical_href_missing / PASS |
| `invalid_url` | 1 / canonical_url_invalid | 1 / canonical_url_invalid / PASS | 1 / canonical_url_invalid / PASS | 1 / canonical_url_invalid / PASS |
| `javascript_url` | 1 / canonical_url_invalid | 1 / canonical_url_invalid / PASS | 1 / canonical_url_invalid / PASS | 1 / canonical_url_invalid / PASS |
| `data_url` | 1 / canonical_url_invalid | 1 / canonical_url_invalid / PASS | 1 / canonical_url_invalid / PASS | 1 / canonical_url_invalid / PASS |
| `fragment_url` | 1 / canonical_fragment | 1 / canonical_fragment / PASS | 1 / canonical_fragment / PASS | 1 / canonical_fragment / PASS |
| `wrong_host` | 1 / canonical_mismatch | 1 / canonical_mismatch / PASS | 0 / clean / FAIL | 1 / canonical_mismatch / PASS |
| `wrong_path` | 1 / canonical_mismatch | 1 / canonical_mismatch / PASS | 0 / clean / FAIL | 1 / canonical_mismatch / PASS |
| `wrong_query` | 1 / canonical_mismatch | 1 / canonical_mismatch / PASS | 0 / clean / FAIL | 1 / canonical_mismatch / PASS |
| `base_invalid` | 1 / base_url_invalid | 1 / base_url_invalid / PASS | 1 / base_url_invalid / PASS | 1 / base_url_invalid / PASS |
| `comment_decoy` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `script_decoy` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `template_decoy` | 0 / clean | 0 / clean / PASS | 0 / clean / PASS | 0 / clean / PASS |
| `missing_head` | 2 / html_unsupported | 2 / html_unsupported / PASS | 2 / html_unsupported / PASS | 2 / html_unsupported / PASS |
| `manifest_traversal` | 2 / input_invalid | 2 / input_invalid / PASS | 2 / input_invalid / PASS | 2 / input_invalid / PASS |
| `symlink_html` | 2 / input_invalid | 2 / input_invalid / PASS | 2 / input_invalid / PASS | 2 / input_invalid / PASS |

**Verdict: KILLED.** The pristine baseline passed (32/32), the comparison-disabled mutant failed the selected detector and the full matrix, and restored bytes passed again (32/32). The three rejecting cases were exactly `wrong_host`, `wrong_path`, and `wrong_query`: each changed from expected exit 1 / `canonical_mismatch` to actual exit 0 / clean. The other 29 cases, including every clean positive control, retained their classifications. No surviving-mutant coverage finding is asserted for this probe.

## Restoration and integrity evidence

The original file was captured before mutation at `/tmp/kake-r22-w2-MutateMismatch.original.py` and in memory. Restoration used those captured original bytes in a `finally` block before running restored controls.

| Source stage | SHA-256 |
|---|---|
| Pristine private source and live-lane source | `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` |
| Mutated private source | `b2b8b698d37fd37dbd612e14262a449fd22a55ad1ae360dc671040f02219bb5c` |
| Restored private source | `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` |

- 70 protected file hashes were captured before and after the probe: private source, live-lane source, frozen matrix/cases/contract/expected oracle, and every private frozen fixture regular file. **Zero changed after restoration.**
- Pristine and restored results matched exactly for all three commands: return codes, stdout, stderr, and timeout fields, including the entire matrix JSON output.
- Frozen matrix SHA-256: `d7de622cf149c4a7a0d3152b3d6c0560fadcc4c0c784c764502d0a2110bf4aab`.
- Frozen cases SHA-256: `28a49013d3aaf72b0e1c3801fd5359592602e079408d9a71c99f2df03d1cbeb6`.
- Required contract SHA-256: `f9a65a8ade6acb77f013104c60dcd2cfc7b63a0f65e855e710036f26ab746fe4`.
- Frozen expected oracle SHA-256: `2040cbd01933f403fab97a6b0339138f1ae78c4d4a4651a4453cc756848c43cd`.

## Retained raw evidence

- Full commands, all nine actual process outputs/exit codes, exact patch, and complete before/after hash maps: `/tmp/kake-r22-w2-MutateMismatch.evidence.json`.
- Evidence JSON SHA-256: `d90c91042239b2e8ff02d58b61b98bf489fbcf642f2ac773ca8f194ea508e441`.
- Captured original source: `/tmp/kake-r22-w2-MutateMismatch.original.py`.
- No tools installed or updated. No builds, linters, formatters, services, package transactions, network properties, or additional runtimes were invoked. Only the explicitly assigned bounded Python public-CLI/matrix mutation probe was exercised.
- No production change is proposed or integrated by this leaf report.
