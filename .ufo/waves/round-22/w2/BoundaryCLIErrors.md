# BoundaryCLIErrors — CLI argument and output boundary (round 22, wave 2)

Seat: `KakeR22.BoundaryCLIErrors` (leaf falsifier; author-side, not independent non-author closure).

Measured candidate: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`. Private clone `/tmp/kake-r22-BoundaryCLIErrors` observed this as HEAD. Reviewed source digest: `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` (`scripts/canonical_audit.py`). Production files were not edited; probe files were confined to `/tmp/kake-r22-cli-boundary-9pl6m84x/`. No tools were installed and no package transactions or network access occurred.

Axes exercised: (1) usage/argument shape maps to the declared exit code, (2) manifest outcomes expose the promised JSON result on stdout, and (3) unsupported/input errors cannot become a clean verdict.

## Findings (by severity)

### [P2] Usage failures return no stdout JSON despite the declared output contract

The frozen interface declares stdout as a JSON object with `verdict`, `pagesChecked`, and `findings`, and its exit map includes usage exit `64` (`contract.json`, line 4). The CLI's own `usage()` text says “Output is always one JSON object” (`scripts/canonical_audit.py:95-96`). But the `UsageError` branch in `main()` only prints human-readable text to stderr and returns `64`; it never writes a JSON object to stdout (`scripts/canonical_audit.py:862-873`). Consequently an automation consumer following the declared output contract cannot parse a result for an ordinary invalid invocation.

Exact public-CLI probe, from the private integrated-candidate clone:

```
python3 /tmp/kake-r22-BoundaryCLIErrors/scripts/canonical_audit.py \
  --manifest /tmp/kake-r22-cli-boundary-9pl6m84x/clean/manifest.json --bogus
```

Exit: `64`

stdout (exact): empty.

stderr (exact):

```text
canonical_audit.py: unrecognized arguments: --bogus
usage: canonical_audit.py --manifest PATH [--json] | --selftest
--help prints standard CLI help, exits 0, and emits no publishing verdict.

Read UTF-8 JSON manifest v1 and bounded local UTF-8 HTML only. The
manifest limit is 1 MiB; each HTML file is limited to 2 MiB.
HTML files are relative to the manifest directory; absolute paths,
traversal, symlinks, and non-regular files are rejected. No network
access or writes occur in manifest mode.

URLs use this tool's conservative HTTP(S) normalization: lowercase ASCII
scheme/host, accept ASCII DNS labels, strict dotted IPv4, or bracketed
IPv6, remove default ports and dot segments, and serialize empty paths
as '/'. Non-ASCII path/query text is UTF-8 percent-escaped; existing
escapes and legal ASCII query spelling, including a final empty '?', persist.
Credentials, fragments, backslashes, whitespace, and malformed
authorities are rejected. The first head base[href] resolves relative
links; invalid first base is base_url_invalid, not browser fallback.
This is a conservative RFC-style subset, not a WHATWG URL implementation.

HTMLParser is not an HTML5 tree builder. It does not perform browser
encoding sniffing or implied-element repair; only explicit, properly
closed head markup with supported head children is evaluated. Comments,
raw-text elements, and template descendants do not contribute links.
Any SVG/Math markup, and canonical/base inside noscript, is unsupported.
Oversize, non-UTF-8, or structurally ambiguous HTML is unsupported.
This compares publisher policy only, not Google or other search-engine
canonical selection. It does not assess readiness or HTTP responses.

Output is always one JSON object: verdict, pagesChecked, findings.
Exit: 0 clean; 1 policy finding; 2 input/unsupported; 64 usage.
```

The same empty-stdout/exit-64 behavior was observed for no mode (`[]`; stderr begins `canonical_audit.py: one of the arguments --manifest --selftest is required`), missing manifest value (`--manifest`; begins `canonical_audit.py: argument --manifest: expected one argument`), incompatible `--selftest --json` (begins `canonical_audit.py: --json is only valid with --manifest`), and an unknown flag after a valid manifest. Each emits the same usage-text suffix to stderr. `--not-a-flag` without a mode also exits `64` with empty stdout, but reports the missing required mode rather than the unknown flag. The documented `--help` exception behaved as described: exit `0`, help text on stdout, no verdict, empty stderr.

### [P2] Repeated `--manifest` silently selects the last path

The mutually-exclusive group in `parse_cli()` prevents combining `--manifest` and `--selftest`, but does not reject a repeated `--manifest` (`scripts/canonical_audit.py:100-114`). `argparse` retains the last value; `main()` evaluates only `args.manifest` (`scripts/canonical_audit.py:871-873`). Thus an ambiguous invocation can silently ignore an earlier invalid or policy-failing manifest and return clean based solely on the later path. The published CLI shape names one manifest argument (`contract.json`, line 4); the repeated-option behavior is not documented.

Own local fixtures: `mismatch/manifest.json` points to a page whose canonical is `https://example.test/wrong.html` while expected is `https://example.test/a.html`; `clean/manifest.json` points to an exact-match page. Exact runs and outputs:

```text
python3 /tmp/kake-r22-BoundaryCLIErrors/scripts/canonical_audit.py \
  --manifest /tmp/kake-r22-cli-boundary-9pl6m84x/mismatch/manifest.json \
  --manifest /tmp/kake-r22-cli-boundary-9pl6m84x/clean/manifest.json
stdout: {"findings":[],"pagesChecked":1,"verdict":"clean"}\n
exit: 0; stderr: empty.

python3 /tmp/kake-r22-BoundaryCLIErrors/scripts/canonical_audit.py \
  --manifest /tmp/kake-r22-cli-boundary-9pl6m84x/clean/manifest.json \
  --manifest /tmp/kake-r22-cli-boundary-9pl6m84x/mismatch/manifest.json
stdout: {"findings":[{"id":"canonical_mismatch","page":"https://example.test/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}\n
exit: 1; stderr: empty.

python3 /tmp/kake-r22-BoundaryCLIErrors/scripts/canonical_audit.py \
  --manifest /tmp/kake-r22-cli-boundary-9pl6m84x/does-not-exist.json \
  --manifest /tmp/kake-r22-cli-boundary-9pl6m84x/clean/manifest.json
stdout: {"findings":[],"pagesChecked":1,"verdict":"clean"}\n
exit: 0; stderr: empty.
```

A duplicated `--json` was harmless (exit `0`, clean JSON). `--selftest --selftest` was also accepted and returned `0`; because this is the selftest mode it ran the built-in selftest once. These observations do not remove the ambiguity of repeated manifest paths.

## Positive, negative, and could-not-evaluate controls

The controls confirm ordinary manifest-mode JSON/exits are distinct and that unsupported HTML is not reported clean. Each probe used the public CLI and an isolated local manifest/page under `/tmp/kake-r22-cli-boundary-9pl6m84x/`.

| Control | Exit | Exact stdout | stderr |
|---|---:|---|---|
| Exact canonical match (`clean/manifest.json`) | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` | empty |
| Canonical mismatch (`mismatch/manifest.json`) | 1 | `{"findings":[{"id":"canonical_mismatch","page":"https://example.test/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}\n` | empty |
| Empty-pages manifest or nonexistent manifest path | 2 | `{"findings":[{"id":"input_invalid","page":null}],"pagesChecked":0,"verdict":"could-not-evaluate"}\n` | empty |
| HTML with a canonical link but no explicit head | 2 | `{"findings":[{"id":"html_unsupported","page":"https://example.test/a.html"}],"pagesChecked":1,"verdict":"could-not-evaluate"}\n` | empty |

The unsupported-shape result is `could-not-evaluate` with `html_unsupported`, not `clean`; that part of the contract survived this probe.

## Review and verification limits

- Direct source review covered `usage()`, `parse_cli()`, `audit_manifest()`/`public_result()`, and `main()` at the cited lines; dynamic probes above exercise the public entrypoint.
- The `lsp` device is not mounted in this session. Attempting `xd://lsp` returned “No such tool” and listed mounted devices without LSP. Therefore `lsp` status, references, definition, and diagnostics could not be run. No grep result is offered as semantic proof; the only grep use was locating function line numbers.
- No matrix/measure rerun, build, lint, or formatter was run. The `--selftest --selftest` probe intentionally exercised duplicate-mode argument parsing and consequently invoked the CLI's built-in selftest once; it is not a full independent suite run.

Report: `.ufo/waves/round-22/w2/BoundaryCLIErrors.md`
