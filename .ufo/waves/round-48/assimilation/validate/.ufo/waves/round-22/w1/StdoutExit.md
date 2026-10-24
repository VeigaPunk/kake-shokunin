# Stdout/exit review — round 22

Axis: **operability** only. Scope is the frozen `contract.json` CLI/stdout/exit interface and the future `scripts/canonical_audit.py` entrypoint; this is not admission or a claim that unseen code passes.

## Evidence and review boundary

The frozen interface (`.ufo/waves/round-22/contract.json`, interface and matrix fields) requires `python3 scripts/canonical_audit.py --manifest <path> [--json] | --selftest`, a JSON stdout object with `verdict`, `pagesChecked`, and `findings` (each finding has `id` and `page`), and exit codes 0 clean / 1 policy failure / 2 input-or-unsupported / 64 usage. Its fixed IDs are `canonical_missing`, `canonical_multiple`, `canonical_outside_head`, `canonical_href_missing`, `canonical_url_invalid`, `canonical_fragment`, `canonical_mismatch`, `base_url_invalid`, `input_invalid`, `html_unsupported`.

At review time the lane has no `scripts/canonical_audit.py` (the required path is absent), and the observed implementation workspace `/tmp/kake-r22-Implement/scripts/` also has no such file. The tracked diff observed was only `corpus/QUALITY.md`; round-22 work was untracked round metadata and a lesson, not an implementation diff. No code-level defect or pass can therefore be asserted. The LSP route is not mounted (`read xd://lsp` returned “No such tool”), so status/references/definition/diagnostics could not be requested; I did not use text search as semantic proof. No tests or commands against an implementation were run.

## Concrete falsification targets (not observed implementation findings)

| Failure mode to reject | Required stable ID | Expected class |
|---|---|---|
| Missing canonical, duplicates, body-only canonical, absent `href`, invalid canonical URL, fragment, or normalized mismatch are silently treated as clean or as unscorable input | respectively `canonical_missing`, `canonical_multiple`, `canonical_outside_head`, `canonical_href_missing`, `canonical_url_invalid`, `canonical_fragment`, `canonical_mismatch` | Exit 1; retain the offending page in the JSON findings |
| Invalid manifest/path or unsupported HTML shape is reported as a policy violation or clean | `input_invalid` / `html_unsupported` (and `base_url_invalid` when the invalid first base prevents resolving a relative canonical) | Exit 2; never present the page/result as clean |
| A wrong CLI invocation inherits `argparse`'s default status 2, or is reported as policy failure | no page-level ID for usage is specified by the frozen set | Exit 64, distinct from content/input exit 2 |
| `--json` is the only mode that emits JSON, or banners/debug/tracebacks are written to stdout around the JSON | relevant canonical ID if the policy result is wrong; otherwise no additional ID is specified | Stdout must remain one parseable JSON object for an evaluated invocation; diagnostics belong on stderr |
| A failed page is counted as checked, a policy failure returns 0, or output is omitted on a nonzero evaluation result | exact page finding ID from the cases above | `pagesChecked` must not imply unperformed evaluation; exit 0 only for a fully clean evaluated set; preserve findings in stdout on exits 1/2 |

`base_url_invalid` and aggregation behavior are not individually assigned an exit in the contract text. Treat it as exit 2 only when resolution is thereby impossible; document/implement deterministic precedence for a multi-page run that mixes an unevaluable page and a policy failure. The safe outcome must never be 0. The `--json` flag is optional while the stdout clause states JSON; the latter should govern normal mode rather than silently adding an undocumented human-output mode. Usage-envelope details and the `page` sentinel for manifest-global input errors are not fully specified; do not invent a new finding ID to fill that gap.

## Minimum acceptance/rejection pair

1. **Accept**: one regular `a.html` with an explicit head containing exactly `<link rel="canonical" href="https://example.test/project/a.html">`; manifest `url` and `expectedCanonical` are that same URL. Expect exit 0, parseable JSON on stdout, `pagesChecked: 1`, and `findings: []`.
2. **Reject**: keep the manifest and page URL/expected URL, but change only `href` to `https://example.test/project/a.html?rev=1`. Query is significant by contract. Expect exit 1, a `canonical_mismatch` finding for the page, and parseable JSON on stdout. No “clean” verdict or exit 0 is acceptable.

## Bounded falsification recipe (not executed)

In a fresh temporary directory, use one version-1 manifest and vary only the single fixture/input named per invocation. Run the CLI once per case, capture stdout, stderr, and process status separately, and parse stdout as JSON for evaluated cases:

- `absolute_match` above: `0`, clean, no findings.
- `wrong_query` above: `1`, `canonical_mismatch`.
- Replace the regular HTML file with a symlink at the manifest's `file`: `2`, `input_invalid`; no clean result.
- Invoke with a missing `--manifest` argument (and separately an unknown option only if the first returns a status): `64`, not argparse's default 2. Usage text may go to stderr; do not fabricate a page-level finding ID.

These four probes falsify the stdout/exit boundary only; they do not stand in for the frozen 32-case matrix, parser-shape coverage, read-only/no-network verification, or an end-to-end capability judgment.
