# LabratCapture — round 86 retained capture probe

## Verdict

**Hypothesis confirmed within the three explicitly assigned trees:** 9 Cache-Control field values exist; all are exactly `max-age=600`; none contains duplicate max-age. Duplicate handling is therefore exercised by synthetic frozen cases, not these retained values. This is an author-side population observation, not independent C1/C2 closure or a claim about unsearched r84/r85 trees.

Axes: extraction completeness, directive-count correctness, reproducibility, read-only safety. One bounded extraction; no production changes.

## Measurement

| Metric | Observed |
|---|---:|
| JSON files inventoried | 15 |
| Files with response headers lists | 9 |
| Cache-Control field values | 9 |
| Directive histogram: max-age | 9 |
| Other directive names | 0 |
| Duplicate-directive extra occurrences within one value | 0 |
| Duplicate-directive extra occurrences across field lines in one response | 0 |
| Duplicate max-age extra occurrences across field lines | 0 |
| s-maxage occurrences | 0 |
| no-store occurrences | 0 |
| Responses containing max-age + no-cache | 0 |
| Missing trees / parse or header-shape errors | 0 / 0 |

The population tree has three fetch-descriptor JSON files, not headers lists, and contributes zero field values. Capture contributes three; capture-control contributes six. Three manifests also lack headers lists. Values are counted per retained field occurrence, not deduplicated by content; nine occurrences represent only one distinct value.

## Exact value locations

Every following response has one `Cache-Control: max-age=600` field; directive list `[max-age=600]`, normalized name `max-age`. Header indices are zero-based.

| Absolute response path | Header index |
|---|---:|
| /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-82/capture/ds4cc-primary/response.json | 8 |
| /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-82/capture/ds4cc-robots/response.json | 8 |
| /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-82/capture/ds4cc-sitemap/response.json | 9 |
| /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-83/capture-control/a/ds4cc-primary/response.json | 8 |
| /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-83/capture-control/a/ds4cc-robots/response.json | 8 |
| /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-83/capture-control/a/ds4cc-sitemap/response.json | 9 |
| /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-83/capture-control/b/ds4cc-primary/response.json | 8 |
| /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-83/capture-control/b/ds4cc-robots/response.json | 8 |
| /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-83/capture-control/b/ds4cc-sitemap/response.json | 9 |

## Method and retained receipts

Read host rules, frozen contract and counter CASES before execution. Discovered the assigned trees using directory/glob tools. Inspected header entry shapes without emitting unrelated header values. The script recursively inventories JSON files in precisely the three assigned trees; extracts only Cache-Control from `headers` lists; splits directives on unquoted commas; normalizes directive names case-insensitively; counts duplicates both within values and across all field lines in each response. It emits input SHA-256 hashes, absolute paths, header indices, raw Cache-Control values, directive lists, summary counts and explicit errors. Other header contents are neither emitted nor copied.

Executed command (exit **0**, stderr empty):

```text
TMPDIR=/fast/scratch/hyaku/kake-r86/LabratCapture /usr/bin/python -B /fast/scratch/hyaku/kake-r86/LabratCapture/extract_cache_control.py
```

Cwd was `/fast/scratch/hyaku/kake-r86/LabratCapture`; Python 3.14.8. The extraction ran once using a synchronous subprocess. Copied script, raw output, stderr and command receipt to the exclusive deliverable directory, then removed the entire exclusive scratch directory successfully. No installs/updates, network requests, VCS mutations, production writes, counter executions, tests, builds, linters or formatters. No supported-symbol LSP tool was exposed; no production symbol lookup/refactor was needed.

Retained artifacts:

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/LabratCapture/extract_cache_control.py`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/LabratCapture/raw-output.json`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/LabratCapture/stderr.txt`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/LabratCapture/command-receipt.json`

## Limits and disposition

No extraction defects or blockers observed. Zero duplicate observations cannot validate first-occurrence semantics. The frozen counter separately specifies synthetic order witnesses at cases 5 and 15; this seat did not execute them. No live status/body observation or authorized keyless POST was performed, and these receipts must not be substituted for that assimilation probe. No corpus append or assimilation was attempted, so §10 append gates remain the integrating owner's responsibility. D84-2/3 remain retained-open; no full D84-queue closure is claimed. Parent retains all post-integration gate ownership; this seat requires no additional empirical probe.

Self-evaluation: accuracy 4/5 (bounded retained snapshot, no independent rerun); completeness 5/5 (all requested counts, values, paths, script and output retained); clarity 4/5 (absolute paths lengthen the table); actionability 5/5 (script and hash-bearing output retained); conciseness 4/5 (explicit per-file table repeats the lane prefix). Overall 4.4/5. Highest-impact improvement for future use: add a genuinely heterogeneous retained population before treating duplicate semantics as empirically supported; that expansion is outside this seat. Would the user agree: expected, given the explicit bounded verdict.

Report: .ufo/waves/round-86/w1/LabratCapture.md
