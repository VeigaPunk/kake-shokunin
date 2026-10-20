# Boundary URL identity review

## Axis and scope

- **Axis:** operability — the public offline CLI must compare canonical URLs consistently across authority normalization, query preservation, percent escapes, and dot-segment resolution, while returning the declared policy result and exit status.
- **Candidate:** `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (observed repository `HEAD`). Against frozen base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`, the reviewed production diff adds `scripts/canonical_audit.py` (877 lines).
- **LSP:** no `lsp` device was mounted (`xd://lsp` returned “No such tool”), so an LSP status/references/definition/diagnostics sequence was unavailable. Literal search only located candidate normalizer call sites (`normalize_http_url` at lines 408, 559, 580, 636–637); this is not semantic-reference proof. I read the normalizer and its `audit_manifest` caller (lines 620–654) and CLI entrypoint (lines 862–873) directly.
- All probe files were created under temporary local fixture trees and invoked through the public CLI. No production/lane source was edited; no tool was installed.

## Findings by severity

**No actionable finding in the assigned URL-identity boundary.** The reviewed implementation normalizes scheme/host and default ports in `normalize_http_url` (`scripts/canonical_audit.py:408–454`; authority parsing at `:320–381`), removes literal and WHATWG-style percent-encoded dot segments (`:384–405`), and preserves query spelling/order and existing escapes during serialization (`:445–453`). The caller compares normalized actual and expected strings without sorting query parameters (`:579–586`).

### Bounded public-CLI controls

Each row used a one-page manifest and explicit `<head><link rel=canonical ...></head>` HTML in a temporary fixture. Invocation shape was `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest <temporary-case>/manifest.json --json`. All stderr values were exactly empty. The `stdout` values below are the exact captured strings (including the final newline).

| Control and input relationship | Exit | Exact stdout |
|---|---:|---|
| **Positive — default ports, ASCII host case, document dot segment, query order:** document `https://EXAMPLE.test:00443/x/../p?b=2&a=1`, expected `https://example.test/p?b=2&a=1`, canonical `https://EXAMPLE.test:443/p?b=2&a=1` | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` |
| **Negative control — query order differs:** expected `https://example.test/p?a=1&b=2`, canonical `https://example.test/p?b=2&a=1` | 1 | `{"findings":[{"id":"canonical_mismatch","page":"https://example.test/p?a=1&b=2"}],"pagesChecked":1,"verdict":"failed-policy"}\n` |
| **Positive — first relative base, dot segments, repeated query keys/order:** document `https://EXAMPLE.test:443/a/index.html?old=1`, first base `../b/`, expected `https://example.test/b/page.html?a=1&a=2&flag`, canonical `./x/../page.html?a=1&a=2&flag` | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` |
| **Positive — encoded dot segment:** expected `/a/b`, canonical `/a/%2e/b` on `https://example.test` | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` |
| **Positive — literal dot segment:** expected `/a/b`, canonical `/a/c/../b` | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` |
| **Positive — encoded-dot variant `.%2E`:** expected `/b`, canonical `/a/.%2E/b` | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` |
| **Positive — same lowercase `%2f` escape spelling retained:** expected and canonical `/a/%2f/file` | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` |
| **Negative — escape hex case is not rewritten:** expected `/a/%2f/file`, canonical `/a/%2F/file` | 1 | `{"findings":[{"id":"canonical_mismatch","page":"https://example.test/a/%2f/file"}],"pagesChecked":1,"verdict":"failed-policy"}\n` |
| **Negative control — encoded slash is not decoded into a path separator:** expected `/a/b`, canonical `/a%2Fb` | 1 | `{"findings":[{"id":"canonical_mismatch","page":"https://example.test/a/b"}],"pagesChecked":1,"verdict":"failed-policy"}\n` |
| **Positive — empty query delimiter preserved:** expected and canonical `https://example.test/p?` | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` |
| **Negative — empty query delimiter differs from no delimiter:** expected `https://example.test/p?`, canonical `https://example.test/p` | 1 | `{"findings":[{"id":"canonical_mismatch","page":"https://example.test/p?"}],"pagesChecked":1,"verdict":"failed-policy"}\n` |
| **Negative control — different path:** expected `/a/b`, canonical `/a/c` | 1 | `{"findings":[{"id":"canonical_mismatch","page":"https://example.test/a/b"}],"pagesChecked":1,"verdict":"failed-policy"}\n` |

The observed exit 0/1 and JSON contract match `audit_manifest` and `main` (`:649–654`, `:871–873`). As an auxiliary local URL-serialization spot-check, Node's built-in `URL` retained `%2f` versus `%2F`, retained `%2F` rather than decoding it to `/`, and serialized the final `?`; the CLI controls above independently exercised its own behavior.

## Residual risk and verification gaps

- This is a scoped review, not proof of complete WHATWG URL conformance. The candidate explicitly describes a conservative RFC-style subset and limits hosts/markup in `usage()` (`scripts/canonical_audit.py:76–91`); the checked-in candidate also disclaims browser parsing, redirects, network freshness, and search-engine selection. Those limitations are not represented here as defects.
- The controls exercise selected ASCII HTTP(S) identity cases and public exit/output behavior only. No full selftest, matrix, build, lint, or other suite was run, per the bounded falsification scope.
- Semantic LSP checks could not be performed because no LSP device/server was available; source-level caller review and literal call-site enumeration are the available evidence.