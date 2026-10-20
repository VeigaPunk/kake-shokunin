# Attack32 — `symlink_html`

## Findings by severity

**No actionable finding.** The frozen final-file symlink case and a nearest-neighbor symlinked-parent case both reject the HTML input as required. The integrated candidate reported by `git rev-parse HEAD` was `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`.

## Independent expected result

Before execution, the frozen contract's file-resolution rule (`.ufo/waves/round-22/contract.json`) requires regular HTML files and rejects symlinks; its exit map assigns `2` to input/unsupported cases. The `symlink_html` record in `cases.json` specifies a symlink HTML input and expects exit `2` with `input_invalid`. The fixture manifest names `linked.html`; `matrix.py` creates that runtime symlink to `target.html` (lines 70–75), whose contents are otherwise a valid matching-canonical page. Therefore following the link would incorrectly make this control clean, while rejecting the link predicts `2` / `input_invalid`.

## Frozen case

Exact command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case symlink_html
```

Matrix process exit: `0`.

Exact stdout:

```text
PASS caseId=symlink_html exit=2 findings=input_invalid
SUMMARY selection=symlink_html accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

The matrix accepted the expected child-CLI result: exit `2`, finding `input_invalid`.

## Nearest-neighbor probe

Constructed an isolated `/tmp/kake-r22-attack32-wv7pmnw5` fixture with a valid regular file `real/page.html`, a directory symlink `via -> real`, and a manifest referring to `via/page.html`; the canonical and expected canonical were both `https://example.test/project/a.html`. This changes only the path component that is a symlink, exercising the same no-follow input policy beyond the frozen final-component symlink.

Exact public CLI command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack32-wv7pmnw5/manifest.json --json
```

Exit: `2`.

Exact stdout:

```text
{"findings":[{"id":"input_invalid","page":"https://example.test/project/a.html"}],"pagesChecked":0,"verdict":"could-not-evaluate"}
```

The public CLI rejects the symlinked parent path. This agrees with `canonical_audit.py`'s per-component `O_NOFOLLOW` directory opens and `O_NOFOLLOW` final-file open (lines 500–524).

## Claim, residual risk, and verification gaps

The claim survives these checks: both the frozen symlink-to-file and nearest symlinked-directory inputs are rejected as `input_invalid`, while the frozen target file is valid HTML that would otherwise pass. This result is limited to the symlink input boundary; it does not establish the entire 32-case capability or broader publishing readiness.

No LSP device/server is mounted in this session (`read xd://lsp` returned “No such tool”), so no LSP status, references, definition, or diagnostics queries were available. The checks above are direct CLI observations; source line references are supporting context, not semantic LSP proof. No build, lint, formatter, or broader test suite was run.