# Implement — offline static canonical preflight

## Scope and files

- Implementation: `/tmp/kake-r22-Implement/scripts/canonical_audit.py` (private clone only).
- Report: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/w1/Implement.md` (this assigned report only).
- No live-lane implementation file, matrix, measure, corpus, verifier, or sibling report was changed.

## Behavior delivered

- Stdlib-only CLI: `python3 scripts/canonical_audit.py --manifest PATH [--json] | --selftest`. Manifest mode always emits the required JSON shape (`verdict`, `pagesChecked`, `findings` with `id` and `page`); exits are 0 clean, 1 policy failure, 2 input/unsupported, and 64 usage. Input/unsupported findings take precedence over policy findings while processing continues per page.
- Manifest v1 is schema-checked and non-empty. HTML paths are literal manifest-relative paths; traversal, absolute/drive paths, symlink components (including in-root links), and non-regular files are rejected. Resolution uses descriptor-relative `O_NOFOLLOW` directory walks, non-blocking opens, and `fstat` regular-file checks before bounded reads. Manifest size is capped at 1 MiB and each UTF-8 HTML file at 2 MiB. Normal mode makes no network requests and performs no writes.
- Canonical policy requires one `rel` token match in an explicit, closed head; ASCII case-insensitive tokenization and attribute names, first-attribute-wins handling, first head `<base href>` resolution, and outside-head detection are implemented. Comments, raw-text content, and template descendants do not supply candidates; canonical/base signals in `noscript` and SVG/Math markup are unsupported. An invalid first base is `base_url_invalid` (exit 1), including cases where a browser might otherwise fall back.
- URL comparison is deliberately a conservative subset, not WHATWG equivalence: HTTP(S) only; ASCII DNS, strict dotted IPv4, or bracketed IPv6 authorities; lowercase scheme/host; default-port and dot-segment normalization; empty path becomes `/`; non-ASCII path/query characters are UTF-8 percent-escaped; query spelling and a present empty `?` are preserved. Credentials, literal fragments (including a trailing empty `#`), backslashes, whitespace, malformed authorities, and unsupported schemes are rejected. The tool compares publisher policy only; it does not simulate Google/search-engine canonical selection, JS rendering, redirects, headers, network freshness, or publishing readiness.
- `--selftest` creates fixtures only under a `TemporaryDirectory`, reports expected and observed finding ID/exit for all 32 frozen matrix names plus additional edge cases (self-closing links, empty query/fragment delimiters, ASCII-only `rel` whitespace, duplicate attributes, empty manifests, noscript/foreign markup, traversal, final/intermediate symlinks, and FIFO inputs). The selftest was authored but not run in this wave.

## Retained evidence

- Read the frozen `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json`: line 2 pins base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`; line 4 defines the entry, manifest, finding IDs and exits; line 5 names the 32 matrix cases.
- Ran the required `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r22-Implement`; observed `branch=master`, `master=7c61c8cc791bde36dd5e3688bdfea2678d90146c`, `head=7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
- No dependency/tool was installed. No LSP device was available in the provided tool surface; the implementation is a new standalone file and required no existing-symbol refactor.
- No selftest, matrix, measure, build, lint, formatter, or other verification was executed by this seat, per the mid-flight gate instruction.

## Risks and handoff

- `HTMLParser` is not an HTML5 tree builder and does not sniff encodings or perform browser implied-element repair. The implementation intentionally accepts only bounded UTF-8 with explicit, properly closed head structure and fails closed for ambiguous markup. The URL rules are documented and conservative rather than browser-equivalent.
- Post-integration verification remains with L1. Recommended checks: `python3 scripts/canonical_audit.py --selftest`, then the frozen revision-bound gate `python3 .ufo/waves/round-22/measure.py --root . --revision <master-tip>` (and Matrix's case runner as appropriate).
- Blockers: none. No install record applies.
