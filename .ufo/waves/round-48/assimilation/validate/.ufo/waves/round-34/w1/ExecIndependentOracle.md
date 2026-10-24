# Round 34 C1 — independent interface oracle

## Axes and result
- Operability: the independent `lxml.html` implementation passed all 28 matrix cases.
- Freshness: not assessed by this C1 interface audit.
- Implementation retained for wave-2 differential testing: `/fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/clone/scripts/link_preview_audit.py`.
- Parser available before this task: lxml 6.1.3 / libxml2 2.14.6. No tool was installed or updated.
- First honest implementation attempt: **28/28** at sandbox commit `7c3e7fa994c3172c4c50f8f1ac5fe371023512ab` (6/6 controls, 13/13 defects, 7/7 inputs, 2/2 usage). No case failed, so no failure-case sentence needs attribution to the case or my reading.
- Final: **28/28** at sandbox commit `61050d0ca02bcdcaaec0eadcbdb1db0ef754a73b`; the only intervening edit removed an unused import. All four constant gates were rejected.

## Interface sentences with plausible alternate readings
Matrix source: `clone/.ufo/waves/round-34/c1-matrix.json:7-12`.

1. Line 7: “stdout: one JSON object {verdict, pagesChecked, findings:[{id, reason, page, property}]} for exits 0, 1 and 2; exit 64 needs no JSON”. `page` could identify the URL or local file; `pagesChecked` could count manifest entries attempted or pages successfully read; `id` has no specified form. “needs no JSON” can mean JSON is optional or that none should be emitted.
2. Line 8: “exit 0 verdict clean (no findings); exit 1 verdict failed-policy (policy findings only); exit 2 verdict could-not-evaluate (any input finding; then only input findings are reported, reasons input_invalid or page_unreadable); exit 64 usage (missing --manifest, unknown argument)”. “Only input findings” excludes policy findings, but does not say whether to emit every input finding or just one when several inputs are invalid.
3. Line 9: “manifest v1: {version:1, pages:[{file: relative path inside the manifest directory, url: absolute http(s) page URL}]} with non-empty pages; a file path that resolves outside the manifest directory is input_invalid; a listed file that cannot be read as UTF-8 is page_unreadable”. “Resolves outside” could mean lexical path resolution or filesystem resolution through symlinks.
4. Line 10: “an Open Graph property is a <meta> element whose property attribute equals the name exactly (og:title, og:type, og:image, og:url) and whose content attribute is non-empty after stripping ASCII whitespace; name= attributes do not count”. “ASCII whitespace” could include vertical tab as general ASCII whitespace, or mean the narrower HTML whitespace set.
5. Line 11: “policy findings: og_required_missing (property = the missing one of og:title, og:type, og:image, og:url; S067), og_type_multiple (more than one og:type element; S068), og_url_not_absolute (og:url value is not an absolute http or https URL with a host), og_url_not_canonical (og:url absolute, a <link rel=canonical href> exists, and og:url differs from that href resolved against the page URL; first canonical link wins; exact string comparison after stripping ASCII whitespace; S067, S068)”. With multiple `og:url` values, “an og:url value” could mean first or each. `rel=canonical` could mean the exact rel value or a canonical token in the rel list; “first canonical link” could include a link without href or only a complete canonical link. “Absolute http or https URL with a host” leaves URL parser edge cases unspecified.

## Risks and blockers
- Runtime import requires lxml; it was present in this Python environment, but no dependency was installed or declared. Other environments lacking lxml cannot run the script.
- The ambiguous cases above were not separately exercised; the frozen matrix passed, but no build, lint, or additional test was run.
- Blockers: none after sandbox-only commits were authorized.

## Commands and retained evidence
The clone was checked out at the declared base; all Git writes/commits below were confined to the assigned sandbox clone. The first base-revision counter call was only a presence check, not a code score.

- Clone/setup: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; mkdir -p /fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/tmp && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/clone && git -C /fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/clone checkout -q a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f && git -C /fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/clone rev-parse HEAD` — exit 0; base revision printed.
- First sandbox commit: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; git add scripts/link_preview_audit.py && git -c user.name='KakeR34 ExecIndependentOracle' -c user.email='executor@example.invalid' commit -m 'Add independent link preview audit' && git rev-parse HEAD` — exit 0; `7c3e7fa994c3172c4c50f8f1ac5fe371023512ab`.
- Cleanup sandbox commit: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; git add scripts/link_preview_audit.py && git -c user.name='KakeR34 ExecIndependentOracle' -c user.email='executor@example.invalid' commit -m 'Remove unused import from link preview audit' && git rev-parse HEAD` — exit 0; `61050d0ca02bcdcaaec0eadcbdb1db0ef754a73b`.
- `python3 -c 'import importlib.util; print({name: bool(importlib.util.find_spec(name)) for name in ("lxml", "html5lib", "bs4")})' && python3 --version && uv --version` — exit 0; lxml/bs4 present, html5lib absent; Python 3.14.8, uv 0.13.0.
- `python3 -c 'import lxml; from lxml import etree; print("lxml=" + lxml.__version__); print("libxml2=" + ".".join(map(str, etree.LIBXML_VERSION)))'` — exit 0; lxml=6.1.3, libxml2=2.14.6.
- Base check: `export TMPDIR=/fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/tmp; unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; python3 -B .ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/clone --revision a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f` — exit 1, 0/28 because `toolPresent=false` at the base commit; all constant gates were rejected.
- First attempt: `export TMPDIR=/fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/tmp; unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; python3 -B .ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/clone --revision 7c3e7fa994c3172c4c50f8f1ac5fe371023512ab` — exit 0; 28/28, tool SHA-256 `40c8ec48251aaca1b45a4b95363127adc76be65c156ccf92c388ea2e026c7279`.
- Final: `export TMPDIR=/fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/tmp; unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; python3 -B .ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/clone --revision 61050d0ca02bcdcaaec0eadcbdb1db0ef754a73b` — exit 0; 28/28, tool SHA-256 `7a988883cad4d4f040e14bb6cb249eb2ebc15fbc61ccef3a59be512bfa2511ad`.
- Both scored runs used `TMPDIR=/fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/tmp` and unset `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`.
- Counter SHA-256: `fc72d855cde3656fe74ab8372ae57dca39ff2d7cebc5e5e4aced6e483b71c51e`; pinned matrix SHA-256: `246a6a3ba67a842c408f56b0240d2ad36969330c5a414b715f04b7e56fac14f7`.
- No lint, build, or additional tests were run.
