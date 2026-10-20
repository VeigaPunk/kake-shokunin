# ParserScope — round 22 W1 review

**Axis:** operability. **Scope:** HTML token callbacks, canonical-link recognition, and the parser-to-policy finding boundary; not manifest/path safety, URL normalization, or CLI output plumbing.

## Review basis

The frozen interface is `.ufo/waves/round-22/contract.json` at base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`. At review time, `scripts/canonical_audit.py` was absent from the live lane; I inspected the current writer candidate `/tmp/kake-r22-Implement/scripts/canonical_audit.py` (read snapshot `9761`) and the independent matrix candidate `/tmp/kake-r22-Matrix/.ufo/waves/round-22/cases.json`. Those are not evidence of integration. I did not execute the candidate, selftest, or matrix; no statement here claims a case passes. I did only in-memory stdlib `HTMLParser` characterization: it emits a `startendtag` callback for `<link ... />`, preserves duplicate attributes in order, decodes href entities, and tokenizes template descendants unless the caller filters them.

The requested `lsp` status/references/definition/diagnostics path was unavailable: `read xd://lsp` returned “No such tool.” No source edits or installs were made.

## Findings (by severity)

### P2 — self-closing void elements are classified as unsupported

In the candidate, `handle_startendtag` unconditionally calls both `handle_starttag` and `handle_endtag` (`scripts/canonical_audit.py:225-227`). While a head is open, `handle_endtag` marks every non-text-element end tag unsupported (`:246-250`). **[INFERENCE from those branches]** A matching `<head><link rel="canonical" href="https://example.test/project/a.html" /></head>` is recorded as a head canonical, then the synthetic `end link` sets `unsupported`; `evaluate_page` consequently returns `html_unsupported`/exit 2 (`:505-506`) instead of a clean policy match. `link` is a void element, and the slash spelling is not excluded by the frozen interface. Treat the self-closing callback as one void start element (do not route it through malformed explicit-end-tag handling), or explicitly narrow and document the supported syntax before claiming the broader static HTML contract.

Expected stable result for that matching fixture: exit `0`, no findings. Candidate-derived result is inferred, not run.

## Expected stable IDs for the frozen parser-facing cases

The matrix candidate provides per-case expected outputs; the frozen contract itself enumerates the allowed IDs and case names. Keep `clean` as a matrix sentinel only, not as a finding.

| Frozen case(s) | Expected result |
|---|---|
| `rel_token_list`, `rel_uppercase`, `attr_uppercase`, `entity_href`, `query_preserved`, `comment_decoy`, `script_decoy`, `template_decoy` | Exit `0`, clean, `findings: []` |
| `missing_link` | Exit `1`, `canonical_missing` |
| `duplicate_same`, `duplicate_different` | Exit `1`, `canonical_multiple` |
| `body_link` | Exit `1`, `canonical_outside_head` |
| `href_absent`, `href_empty` | Exit `1`, `canonical_href_missing` |
| `invalid_url`, `javascript_url`, `data_url` | Exit `1`, `canonical_url_invalid` |
| `fragment_url` | Exit `1`, `canonical_fragment` |
| `wrong_host`, `wrong_path`, `wrong_query` | Exit `1`, `canonical_mismatch` |
| `base_invalid` | Exit `1`, `base_url_invalid` |
| `missing_head` | Exit `2`, `html_unsupported` |
| `manifest_traversal`, `symlink_html` | Exit `2`, `input_invalid` (adjacent input-safety boundary) |

`template_decoy` is a positive control only when the real, matching head link remains countable and the wrong template descendant is fully ignored; the matrix fixture has both. `missing_head` is explicitly an unsupported-shape case in the matrix candidate, so do not substitute `canonical_missing` or `canonical_outside_head` for its expected ID.

## Minimum acceptance/rejection pair

- **Accept — `template_decoy`:** use the matrix fixture, whose `<template>` contains a wrong-host canonical and whose explicit head also contains the correct canonical. Expected: exit `0`, clean verdict, empty findings. This catches both counting the inert descendant and comparing its URL.
- **Reject — `duplicate_different`:** two canonical links in the explicit head with different destinations. Expected: exit `1`, `canonical_multiple`, even if one destination matches the manifest.

## Bounded falsification recipe (not run)

After the candidate is integrated, use only local temporary files and at most four one-page invocations of `python3 scripts/canonical_audit.py --manifest <absolute-manifest-path> --json`:

1. Run the `template_decoy` matrix manifest; assert exit `0` and `findings == []`.
2. Run `duplicate_different`; assert exit `1` and finding ID `canonical_multiple`.
3. In the temporary directory, write one matching canonical as `<link rel="canonical" href="https://example.test/project/a.html" />`; assert exit `0` and no findings. The reviewed candidate’s callback path predicts this will instead return `html_unsupported`/2.
4. Run `missing_head`; assert exit `2` and `html_unsupported` as fixed by the matrix.

Compare structured IDs and process exit status, not just stdout text. Do not invoke a browser, fetch URLs, or write outside the temporary fixture tree. This supplement is deliberately small and does not replace the frozen 32-case matrix.

## Residual risk and verification gaps

- `HTMLParser` is a tokenizer, not an HTML5 tree builder. The candidate filters templates and rejects several unexpected head transitions, but the public module docstring does not state the supported markup boundary or explain which parser divergences become `html_unsupported`. Make that boundary explicit before calling the interface complete; no browser-DOM equivalence is claimed here.
- The candidate maps UTF-8 decode failure to `html_unsupported` (`:495-497`). The frozen exit map puts both `input_invalid` and `html_unsupported` under exit 2 but does not spell out the encoding-to-ID rule. Pin this diagnostic distinction before adding an encoding case; do not treat this as a verified matrix failure.
- Static review only: the live lane did not yet contain the candidate, and no candidate tests, matrix run, build, or runtime invocation were performed. LSP checks were unavailable as noted above.

Trailer: `.ufo/waves/round-22/w1/ParserScope.md`
