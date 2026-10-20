# NoWrites — surgical design review

**Axis:** operability. **Disposition:** no implementation verdict; review is blocked on the absent candidate, not a pass.

## Evidence and scope

The frozen contract at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json:4–5` requires an offline, read-only validator, manifest-relative regular HTML files, rejection of symlinks and traversal, and stable findings from its listed set. The required entry point is `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py`; the matrix and revision-bound counter are also part of the acceptance path (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/w1-spec.json:17–24`).

At the inspected worktree snapshot, `git status --short` showed only `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md` modified and `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/` plus `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md` untracked. The required `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py`, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py`, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/measure.py`, and `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/cases.json` were not present in the lane; the prescribed `/tmp/kake-r22-*/scripts/canonical_audit.py` search found no candidate either. The observed QUALITY addition limits the claim to declared-policy comparison and explicitly excludes Google selection, rendering, headers, redirects, freshness, and publishing readiness; it does not establish implementation behavior.

No builds or tests were run. `xd://lsp` is not mounted (`No such tool`), and there is no implementation source here for caller/definition/diagnostic analysis. The grep search used only to locate the NoWrites assignment, not as semantic proof.

## Frozen runtime IDs to preserve

The matrix prompt requests an expected exit and finding ID for each case, while the contract lists error IDs but no per-case oracle. Treat `clean` as a **matrix expectation sentinel only**: exit 0 with `findings: []`; do not emit a new `clean` finding or expand the frozen ID set. The matrix must independently pin each case’s expected result. Contract-derived ID expectations are:

| Frozen case(s) | Expected result |
|---|---|
| `absolute_match`, `relative_same_dir`, `relative_parent`, `root_relative`, `scheme_relative`, `first_base`, `second_base_ignored`, `rel_token_list`, `rel_uppercase`, `attr_uppercase`, `entity_href`, `query_preserved` | `clean` sentinel: exit 0, no findings, assuming each fixture resolves to its declared expected URL. |
| `missing_link`; `comment_decoy`, `script_decoy`, `template_decoy` when the fixture has only the decoy | `canonical_missing`, exit 1. Decoys must not satisfy the declaration. |
| `duplicate_same`, `duplicate_different` | `canonical_multiple`, exit 1. |
| `body_link` | `canonical_outside_head`, exit 1. |
| `href_absent` | `canonical_href_missing`, exit 1. |
| `href_empty`, `invalid_url`, `javascript_url`, `data_url` | `canonical_url_invalid`, exit 1. |
| `fragment_url` | `canonical_fragment`, exit 1. |
| `wrong_host`, `wrong_path`, `wrong_query` | `canonical_mismatch`, exit 1; these are failures against local `expectedCanonical` policy, not a claim that cross-host URLs violate RFC 6596. |
| `base_invalid` | `base_url_invalid`; the frozen exit map does not bind this ID to an exit. Freeze the intended exit in `cases.json` (2 is the conservative result if resolution cannot be evaluated; do not silently fall through to a later base). |
| `missing_head` | `html_unsupported`, exit 2. |
| `manifest_traversal`, `symlink_html` | `input_invalid`, exit 2. |

The contract’s exit map is 0 clean, 1 policy failure, 2 input/unsupported shape, and 64 usage. `base_invalid` is the material unpinned ID-to-exit edge case; the frozen matrix must resolve it before its result can count toward acceptance.

## Conditional failure modes to falsify (not observed in code)

### High — path escape or symlink acceptance (`input_invalid` expected)

A `pages[].file` of `../outside.html`, an absolute path, a final symlink, or a symlinked intermediate directory could let the validator read outside the manifest tree or violate the explicit no-symlinks rule. Checking only the resolved target can also wrongly accept an in-tree symlink. The frozen contract explicitly prohibits traversal and symlinks, but the prescribed matrix names only traversal and a symlink HTML case; it does not establish intermediate-symlink behavior. Require exit 2 / `input_invalid` for traversal and every symlink path; do not echo file contents or raw exceptions. This is a conditional risk, not a finding against unseen code.

### High — normal mode writes or performs network activity

A temp/cache/log file, mutation of the manifest/HTML, URL fetch, browser launch, or HTML-driven resource load violates the offline/read-only contract. A local `<img src>`, `<iframe src>`, refresh tag, or URL-looking `href` must remain inert data. A clean exit and unchanged input hashes alone do not prove no network attempt or no writes elsewhere.

### High — flat tokenizer misclassifies document structure

`HTMLParser` is a tokenizer, not an HTML5 tree builder; it does not validate matching end tags or synthesize an explicit head (source scout report, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/w1/PythonParser.md:32–49`). A parser that scans tokens without tracking explicit head/body and template nesting can count `body_link` or `template_decoy` as a head canonical, or treat a missing head as a clean parse. Require `body_link` → `canonical_outside_head`; `missing_head` → `html_unsupported`; a template-only decoy → `canonical_missing`. Comments and script raw text must not create links. For `rel`, match the ASCII-case-insensitive token `canonical`, not an exact lowercase whole-string comparison or substring; parser-normalized attribute names do not lowercase the attribute value.

### Medium — parser is mistaken for URL validation or loses comparison components

`urllib.parse` explicitly does not validate arbitrary URLs, and `urljoin` accepts absolute/scheme-relative targets that retain their own authority (source scout report, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/w1/PythonURL.md:30–48`). Require explicit HTTP(S), authority/host, credential, and fragment checks, then compare the normalized scheme, authority, path, and query. Do not drop query data: `wrong_query` must yield `canonical_mismatch`; `javascript_url`/`data_url` must yield `canonical_url_invalid`; `fragment_url` must yield `canonical_fragment`. Use only the first applicable head `<base href>`; do not skip an invalid first base and adopt the second.

### Medium — “bounded” input has no frozen numeric ceiling

The implementation brief requires bounded serialized HTML, but neither the frozen contract nor case list gives byte/page limits. An unlimited JSON or HTML read can consume unbounded memory/CPU in an automated preflight. The implementation should document and enforce a finite limit, return a contract-consistent could-not-evaluate result on overflow, and include a boundary check in later validation. No particular numeric ceiling is frozen here, so this is residual design risk rather than a reproduced defect.

## Minimum acceptance/rejection pair

Use separate manifests in a fresh temporary tree; both name `pages/a.html` relative to the manifest and run from an unrelated current directory.

1. **Accept:** manifest URL and expected URL are `https://example.test/project/a.html?x=1&y=2`; HTML has an explicit head containing `<link rel="alternate CANONICAL" href="./a.html?x=1&amp;y=2">`. Expect exit 0, `pagesChecked: 1`, and an empty `findings` array. This checks relative resolution, token-list/case handling, and one-pass entity decoding.
2. **Reject:** same manifest URL and expected URL, but the canonical `href` query is `?x=2&amp;y=2`. Expect exit 1 and a page finding with ID `canonical_mismatch`.

These are minimum policy controls, not substitutes for the complete frozen 32-case matrix. The implementation is accepted only when the independent matrix’s expected exits and IDs all match; a baseline with missing artifacts remains unavailable/0 accepted, not observed incorrect behavior.

## Bounded falsification recipe for the read-only claim

After the candidate and fixture artifacts land (do not run this review as a test now):

1. Create only the two manifests/pages under a fresh `/tmp/kake-r22-nowrites/` tree (the manifest’s `file` value is `pages/a.html`, relative to that manifest as the contract requires) plus `/tmp/kake-r22-nowrites/outside.html` as a canary; snapshot the complete input path list, file hashes, and metadata. Run each manifest once from `/` using the absolute script path and `--json`.
2. Add one traversal manifest (`../outside.html`) and final/intermediate symlink cases. Each must fail closed with exit 2 / `input_invalid`; neither stdout nor stderr may contain the canary. Do not add live URLs or open any external target.
3. If an existing `strace` is available, capture only these invocations (`-f`, file and network syscalls). Reject any network syscall or normal-mode file open for writing/creation/truncation, rename, or unlink (apart from the tracer’s own log). Do not install tools for this recipe. Compare the input path/hash snapshot after every run; it must be identical. If syscall tracing is unavailable, the snapshot is only a partial no-write check and must not be reported as proof of no network/write attempts.
4. Stop after these bounded controls plus the full frozen matrix; no live-property probes, browser, or publishing action.

## Residual risk and verification gap

No runtime behavior has been exercised or reviewed because the implementation and matrix are absent from the inspected lane. The file-boundary, no-network/no-write, parser-state, URL-normalization, and limit requirements above remain unverified. This report is not admission or promotion authority; after integration, L1 should run `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/measure.py` and the non-author closure must make the admission decision.

Report: `.ufo/waves/round-22/w1/NoWrites.md`
