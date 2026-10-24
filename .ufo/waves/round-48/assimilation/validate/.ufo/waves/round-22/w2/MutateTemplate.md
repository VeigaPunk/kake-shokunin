# MutateTemplate — bounded template-inertness mutation probe

## Scope and axes

- Axes: inert-template policy correctness; frozen-detector sensitivity; private-copy isolation and byte-exact restoration.
- Author-side mutation evidence only; no admission, integration, or shipping decision.
- Read the frozen contract at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json`.
- Created `/tmp/kake-r22-w2-MutateTemplate` with `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r22-w2-MutateTemplate`.
- Observed private `HEAD` and `master`: both `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (the integrated candidate, not the earlier contract base).
- Before the probe, all 68 relevant source/contract/detector/case/fixture files matched the lane byte-for-byte. No uncommitted source copy was required.

## Mutant and expected detector

Mutant `MT-template-descendants-count`: in `/tmp/kake-r22-w2-MutateTemplate/scripts/canonical_audit.py`, line 173, exempt `link` start tags from the template-depth early return. This plausible guard defect lets inert template canonical descendants enter the active head canonical list. All other source/oracle/fixture bytes were unchanged.

Exact one-line patch:

```diff
--- /tmp/kake-r22-w2-MutateTemplate/scripts/canonical_audit.py (captured pristine)
+++ /tmp/kake-r22-w2-MutateTemplate/scripts/canonical_audit.py (mutated)
@@ -170,7 +170,7 @@
 
     def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
         tag = ascii_lower(tag)
-        if self.template_depth:
+        if self.template_depth and tag != "link":
             if tag == "template":
                 self._enter_template()
             return
```

Expected detector: frozen `template_decoy`, which expects CLI exit `0` and the matrix sentinel `clean`. Its unchanged fixture contains a wrong-host canonical inside `<template>` followed by the correct active canonical. Counting both should produce CLI exit `1`, stable finding ID `canonical_multiple`, and a matrix discrepancy.

## Commands and bounds

Ran these identical commands on pristine, mutated, and restored bytes, always the selected case first and then the whole matrix:

```text
python3 /tmp/kake-r22-w2-MutateTemplate/.ufo/waves/round-22/matrix.py --root /tmp/kake-r22-w2-MutateTemplate --case template_decoy --json
python3 /tmp/kake-r22-w2-MutateTemplate/.ufo/waves/round-22/matrix.py --root /tmp/kake-r22-w2-MutateTemplate --json
```

Each detector invocation had an outer 180-second timeout. The unchanged frozen matrix bounds each public CLI subprocess at 60 seconds. All six detector invocations completed without timeout; all detector and underlying case stderr values were empty. No builds, linters, formatters, selftests, other runtimes, installs, host services, or package transactions were invoked.

## Actual outputs

| Source state | Selected-case detector exit | Selected case accepted | CLI exit / finding | Whole-matrix detector exit | Matrix accepted | Executed | Discrepancies |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| Pristine | 0 | 1/1 | 0 / `clean` | 0 | 32/32 | 32 | 0 |
| Mutated | 1 | 0/1 | 1 / `canonical_multiple` | 1 | 31/32 | 32 | 1 |
| Restored | 0 | 1/1 | 0 / `clean` | 0 | 32/32 | 32 | 0 |

The sole mutated matrix discrepancy was `caseId=template_decoy`: expected exit `0`, expected findings `["clean"]`; actual exit `1`, actual findings `["canonical_multiple"]`, status `FAIL`. The other 31 frozen cases remained accepted.

Exact public-CLI stdout for `template_decoy` (identical between its selected-case and whole-matrix executions within each state):

Pristine and restored:

```json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

Mutated:

```json
{"findings":[{"id":"canonical_multiple","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

The `clean` value is the frozen matrix's sentinel for an empty findings array, not a finding emitted by the CLI.

## Verdict

**KILLED.** Both the selected frozen case and the whole matrix detect the one-line mutation. The pristine controls passed and the byte-restored controls passed, so this is not a baseline failure or an inconclusive probe. This establishes sensitivity to this specific template-link guard defect; it does not establish complete template/parser coverage or independently admit the capability.

## Restoration and integrity evidence

The original source was captured before mutation at `/tmp/kake-r22-w2-MutateTemplate/scripts/canonical_audit.py.original`. A `finally` block restored the complete captured file immediately after the mutated detector runs, before either restored detector ran. Direct byte comparison returned `true`.

| Source state | SHA-256 |
| --- | --- |
| Original private source and lane source | `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` |
| Mutated private source | `c4a6a53522da3a7557a5905915a7849614b62f3db02bee5ad3bfa79c174d31d2` |
| Restored private source | `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` |

Before/after comparison covered 68 relevant frozen files: the canonical source, contract, matrix instrument, case definitions, and fixture files. Private differences after restoration: `[]`. Live-lane differences: `[]`. The SHA-256 of each sorted compact JSON path-to-file-hash map (private before, private after, lane after) was identical:

```text
153506b05602e7d1abe9200bf7d7e9ebf9cc76fb222b8d6d33d221490b886687
```

Complete commands, detector exit codes, raw stdout/stderr for all six invocations, every matrix result, exact patch, and per-file hashes are retained at `/tmp/kake-r22-w2-MutateTemplate/mutation-evidence.json` (SHA-256 `7fd58363cd26ebad2e39f700bdc6a3721f063705071c5f7551beb48aa36dba3f`).

No live production, oracle, fixture, historical corpus, verifier, aggregator, sibling source, lane Git/JJ state, or lane index was modified. The only live-lane write was this assigned report. No tools were installed or updated.

Report: .ufo/waves/round-22/w2/MutateTemplate.md
