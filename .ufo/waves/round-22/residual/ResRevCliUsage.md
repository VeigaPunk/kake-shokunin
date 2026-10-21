## Verdict
**No counterexample found** against D2+D3. All 21 argparse error-path probes satisfy the stdout contract: every non-help exit is exactly one JSON object equal to `USAGE_RESULT` with rc 64; every help exit is rc 0 with pure argparse help text and no `"verdict"` substring; no path emits both a manifest verdict and usage JSON. Selftest: **62/62 passed, rc 0**.

## Findings
**P3 — `--help` usage line advertises an invalid combination (`--selftest [--json]`).**
- Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --help`
- Observed stdout first line: `usage: canonical_audit.py [-h] (--manifest PATH | --selftest) [--json]`
- But `--selftest --json` is rejected (rc 64, `canonical_audit.py: --json is only valid with --manifest`). The argparse-generated synopsis contradicts `parse_cli`'s post-parse check; the hand-written `usage()` on stderr is accurate. No stdout-contract or exit-code violation — purely a misleading help synopsis introduced by fixing D2 outside argparse's model.
- Smallest fix: pass `usage="canonical_audit.py --manifest PATH [--json] | --selftest [-h]"` to `CanonicalArgumentParser` in `parse_cli`.
- Impacted axis: CLI diagnostics accuracy, not the C1 stdout/exit contract.

## Checked and held
Probes (script `scripts/canonical_audit.py`, python3 3.14.8). All error rows: stdout exactly `{"findings":[],"pagesChecked":0,"verdict":"could-not-evaluate"}\n`, single line.

| Probe | rc | stdout | stderr first line |
|---|---|---|---|
| `[]` no args | 64 | usage JSON | `...: one of the arguments --manifest --selftest is required` |
| `--not-a-flag` | 64 | usage JSON | `...: one of the arguments --manifest --selftest is required` |
| `--manifest` | 64 | usage JSON | `...: argument --manifest: expected one argument` |
| `--manifest=a --manifest=b` | 64 | usage JSON | `...: --manifest may be given only once` |
| `--manifest a --manifest a` | 64 | usage JSON | `...: --manifest may be given only once` |
| `--manifest a --selftest` | 64 | usage JSON | `...: argument --selftest: not allowed with argument --manifest` |
| `--selftest --manifest x` | 64 | usage JSON | `...: argument --manifest: not allowed with argument --selftest` |
| `--selftest --json` | 64 | usage JSON | `...: --json is only valid with --manifest` |
| `--man x` (abbrev) | 64 | usage JSON | `...: one of the arguments --manifest --selftest is required` |
| `--manifest -- x` | 64 | usage JSON | `...: argument --manifest: expected one argument` |
| `--json --json` | 64 | usage JSON | `...: one of the arguments --manifest --selftest is required` |
| `--json` alone | 64 | usage JSON | required-group error |
| `--manifest x extra` | 64 | usage JSON | `...: unrecognized arguments: extra` |
| `--selftest=x` | 64 | usage JSON | `...: argument --selftest: ignored explicit argument 'x'` |
| `--manifest --help` | 64 | usage JSON | expected-one-argument error |
| `--manifest x --manifest y --help` | 64 | usage JSON | `--manifest may be given only once` (error wins, no double output) |
| `--selftest --manifest x -h` | 64 | usage JSON | mutual-exclusion error |
| `--help` / `-h` | 0 | argparse help, no `"verdict"`, no JSON | — |
| `--help --not-a-flag` / `--not-a-flag --help` / `--selftest -h` / `-h --manifest x --manifest y` | 0 | argparse help, verdict-free | — |

Held:
- Usage-error stderr is `canonical_audit.py: <msg>\n` + 33-line custom `usage()` ending `Exit: 0 clean; 1 policy finding; 2 input/unsupported; 64 usage.`; stdout/stderr cleanly separated, stdout single line.
- `SingleManifestAction` rejects repeat-before-help; selftest's own CLI loop (7 usage cases + help) agrees with observed behavior.
- No probe reached manifest/file I/O (all rejected at parse layer); lane untouched, no installs performed.
- Held as argparse-standard, not a defect: error-vs-help precedence is token-order dependent (unknown-flag errors are deferred to end-of-parse so trailing `--help` wins with rc 0; mid-parse action/mutual-exclusion errors win over later `--help`). Both directions keep stdout single-object.

## Limits
- Probed only the assigned D2/D3 surface; manifest-mode success/input paths (exit 0/1/2) belong to sibling reviewers.
- Single runtime observed: python3 3.14.8 (Arch); behavior of `--` handling and abbreviations is version-sensitive in principle but pinned here.
- Scratch dir `/tmp/kake-r22a2-cliusage-IKCw` created; no files written into it or the lane.