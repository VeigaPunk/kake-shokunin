NOT MET: no sibling tool copies the round-41 `_URI_RE` (`\u0080-\U0010ffff`) or its cost.

Axes: operability (shared URL check?) and freshness (regex still live outside tip41?). Text search only; no language server. No tools installed.

Commands: per-repo grep of every `*-shokunin` except kake for `0010ffff|_URI_RE` — no matches (gitignore on, includes tracked corpus). Byte walk of sibling `*.py`/`*.mjs`/`*.js` outside `corpus/`, `.ufo/`, `reports/`, `.git` — `scanned 474 skipped_big 0 hits 0`. `sha256sum` of the two kake tools below completed. A full sibling-tree byte walk (including corpus) was interrupted at 120s and is not evidence.

Round-41 regex (only copy found): `/fast/scratch/hyaku/kake-r42/shared/tip41.py` sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`, `_UNRESERVED` line 73, `_URI_RE` lines 77–86, match before `urlsplit` at 92–95. Live kake tool `scripts/sitemap_audit.py` sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` does not compile `_URI_RE`; lines 76–78 name that class as the thing replaced; lines 105–134 are byte tables. The substring `0010ffff` there is a comment, not a class.

`scripts/` exists only on kake (24), kumitate (13 `.mjs`), tabi (20 `.mjs`). The other 18 lanes have no `scripts/`.

Pointers (one line):

- `kumitate-shokunin/scripts/`: no `_URI_RE`, no `0010ffff`, no `urlsplit`. `gate-mutants.mjs:853` is `new URL` of a local file, not a validator.
- `tabi-shokunin/scripts/check-round-contract.mjs:629` and `check-user-round-contract.mjs:665`: WHATWG `URL`, http(s), reject loopback. No RFC class.
- `tabi-shokunin/scripts/webmcp-validation-round19.mjs:789`: WHATWG `URL`, `http:` + `127.0.0.1` + empty userinfo.
- `tabi-shokunin/scripts/webmcp-invoke-round17.mjs:439`, `webmcp-invoke-round18.mjs:937`, `webmcp-invoke-round19.mjs:1095`, `webmcp-loopback-round16.mjs:410`: parse-or-null, not the regex.
- `chousa-shokunin/tools/quote-reopen.py:214`: `urlsplit` scheme/userinfo/host/port; no C0 or whitespace pre-check. Not under `scripts/`.
- `kagi-shokunin/corpus/release-clock.py:176`: `urlsplit`, https-only public URL. No `_URI_RE`.
- `kotoba-shokunin/verifiers/check_agent_definitions.py:379` (same pattern in `check_command_files.py:500`, `check_hook_files.py:534`, `check_plugin_manifests.py:467`, `check_scoped_rules.py:566`): `urlsplit` host / path. No character-class grammar.
- `kotodama-shokunin/tools/harness/r8_checks.py:84`: reject whitespace, then `urlsplit`. `tools/reopen-row.py:343`: `urlsplit` hostname. Neither is the round-41 regex.
- `mori`, `souji`, `tameshi`, `tsukuroi` `tools/`: no `urlsplit`, no `_URI_RE`, no `0010ffff`.

Checked statements: “a sibling already copied the round-41 regex and its cost” — wrong. “sibling `urlsplit` checks are that grammar” — overstated; they are `urlsplit` or WHATWG `URL` and do not pay the `\u0080-\U0010ffff` match. “the live kake tool still compiles that regex” — wrong. Gap: gitignored blobs under sibling `corpus/` were not byte-scanned after the 120s interrupt; tracked trees were grepped and had no hit.
