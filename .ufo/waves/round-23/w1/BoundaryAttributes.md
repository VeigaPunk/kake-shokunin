## Verdict

Recommendation: no actionable P0–P3 defect found in the assigned attribute probes; this is not an independent admission. The tested file matches the candidate commit's `scripts/canonical_audit.py` blob: lane `HEAD` was `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`; `git rev-parse 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc:scripts/canonical_audit.py` and `git rev-parse HEAD:scripts/canonical_audit.py` both returned `2c40d71d0c7cd9a03c142b4e5c1d7535fa6c7ca7`; candidate-vs-lane file diff exit was `0`.

## Findings

None (P0–P3) for the tested duplicate-attribute, `rel` whitespace, or `hreflang`/`media`/`type` cases. No fix recommended from these probes.

## Checked and held

The probes used private fixtures under `/tmp/kake-r23-BoundaryAttributes-FrCt/` and the public CLI. Python was `Python 3.14.8`. Exact command:

```sh
for d in /tmp/kake-r23-BoundaryAttributes-FrCt/*; do printf '%s ' "${d##*/}"; python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest "$d/manifest.json" --json; result=$?; printf 'exit=%s\n' "$result"; done
```

Exact observed output:

```text
canonical-all-hints {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
canonical-hreflang {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
canonical-media {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
canonical-type {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
duplicate-href-match-first {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
duplicate-href-mismatch-first {"findings":[{"id":"canonical_mismatch","page":"https://example.test/duplicate-href-mismatch-first.html"}],"pagesChecked":1,"verdict":"failed-policy"}
exit=1
duplicate-rel-alternate-first {"findings":[{"id":"canonical_missing","page":"https://example.test/duplicate-rel-alternate-first.html"}],"pagesChecked":1,"verdict":"failed-policy"}
exit=1
duplicate-rel-canonical-first {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
negative-baseline {"findings":[{"id":"canonical_missing","page":"https://example.test/negative-baseline.html"}],"pagesChecked":1,"verdict":"failed-policy"}
exit=1
positive-baseline {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
rel-ascii-space {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
rel-ascii-tab {"findings":[],"pagesChecked":1,"verdict":"clean"}
exit=0
rel-unicode-emspace {"findings":[{"id":"canonical_missing","page":"https://example.test/rel-unicode-emspace.html"}],"pagesChecked":1,"verdict":"failed-policy"}
exit=1
rel-unicode-nbsp {"findings":[{"id":"canonical_missing","page":"https://example.test/rel-unicode-nbsp.html"}],"pagesChecked":1,"verdict":"failed-policy"}
exit=1
unsupported-noscript {"findings":[{"id":"html_unsupported","page":"https://example.test/unsupported-noscript.html"}],"pagesChecked":1,"verdict":"could-not-evaluate"}
exit=2
```

Interpretation tied to the program's documented static-source scope:

- The positive control (matching canonical) is `clean`, exit `0`; the negative control (only `rel=alternate`) is `failed-policy` with `canonical_missing`, exit `1`.
- Duplicate `rel` and `href` attributes produce first-value behavior in both directions: canonical/matching first values pass; alternate/wrong first values fail. This matches the implementation at `scripts/canonical_audit.py:145-154`, where `attrs_first_wins` uses `setdefault` on ASCII-lowercased names.
- ASCII space and tab delimit `rel` tokens and pass; NBSP and EM SPACE do not delimit the token `canonical`, so they yield `canonical_missing` (policy failure, not unsupported). The implementation's delimiter is explicitly `[ \\t\\n\\r\\f]+` at lines 141-154.
- `hreflang`, `media`, and `type`, separately and together, did not change the canonical result. The checker recognizes the `rel` token and checks `href`; it does not validate these extra attributes. This is consistent with its stated source-signal-only policy and is not evidence about crawler interpretation.
- Unsupported is distinct from clean: the noscript canonical returned `could-not-evaluate` with `html_unsupported`, exit `2`, not `clean`.

The additional command `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --selftest` exited `0`; its JSON result had `"passed": true`, including the built-in duplicate-attribute, non-ASCII-rel-separator, and unsupported-markup cases.

## Limits

The LSP device was unavailable: attempting `read xd://lsp` returned `No such tool: xd://lsp` and listed mounted devices without `lsp`. A literal fallback search found textual references, but does not establish semantic callers; no references/definition/diagnostics result is claimed. No live URL, HTTP behavior, browser parsing, search-engine selection, publishing readiness, or optional-attribute conformance was evaluated. No production source was edited and no tools were installed; probes were offline.