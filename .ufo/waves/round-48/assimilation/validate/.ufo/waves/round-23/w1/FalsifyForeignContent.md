## Verdict

**P1 operability hold recommended for candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`.** The validator returns `clean` for browser-parsed foreign-content cases where an HTML `<base>` changes the relative canonical URL. This is a review recommendation only, not an admission or independent judgment.

## Findings

### P1 — Foreign-content paths can hide an effective HTML `<base>` and produce false clean

**Impacted claim/axis:** C2 canonical preflight operability. A clean receipt can disagree with browser parsing of the same served HTML, so reproducing the validator does not establish the canonical policy for these pages.

**Source path/evidence:** `scripts/canonical_audit.py` lines 160–164 puts `script`, `style`, and `title` into a global `CDATA_CONTENT_ELEMENTS` set. Lines 197–204 return early throughout `foreign_depth`, only incrementing on nested `svg`/`math` and marking canonical-looking `link`; lines 285–295 return early for any self-closed tag while foreign content is active; lines 297–302 decrement a scalar depth for any `</svg>` or `</math>` without matching element names or popping nested descendants. These paths do not model HTML integration points or the browser foreign-content breakout/end-tag stack.

The HTML Standard defines SVG `foreignObject` and SVG `title` as HTML integration points, lists `head` among the foreign-content breakout start tags, and processes body-mode `base` through the in-head rules. Its document-base-URL algorithm uses the first descendant HTML `base[href]` in tree order. Therefore a `<base href="https://wrong.test/root/">` in these browser-parsed HTML positions changes the resolution of the page's relative `<link rel=canonical href="a.html">`; the validator ignores that base and resolves against the original page URL.

Standards references: [foreign-content parsing](https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inforeign), [HTML integration points](https://html.spec.whatwg.org/multipage/parsing.html#html-integration-point), [in-body parsing](https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inbody), [document base URL](https://html.spec.whatwg.org/multipage/urls-and-fetching.html#document-base-url).

**Reproduction.** The pre-run expectation record is `/tmp/kake-r23-FalsifyForeignContent-JTrt/expectations.md`; the focused manifest is `/tmp/kake-r23-FalsifyForeignContent-JTrt/base-attacks.json`. All six pages have expected canonical `https://example.test/cases/a.html`; the manifest includes `foreignobject_base.html`, `svg_second_head_base.html`, `mismatched_svg_base.html`, `svg_title_base_escape.html`, `svg_style_base_escape.html`, and `svg_script_base_escape.html`. For example, `foreignobject_base.html` is:

```html
<head><link rel=canonical href="a.html"></head><body><svg><foreignObject><base href="https://wrong.test/root/" /></foreignObject></svg></body>
```

Exact command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-FalsifyForeignContent-JTrt/base-attacks.json --json; printf 'exit=%s\n' "$?"
```

Exact observed output:

```text
{"findings":[],"pagesChecked":6,"verdict":"clean"}
exit=0
```

The six pages in that focused manifest are all reported clean, including the direct HTML integration-point base, a base following a nested `<head>` breakout, a base exposed by mismatched `</svg>`/`</math>` ends, and bases hidden by the parser's SVG `title`/`style`/`script` text modes. The mismatch case is especially clear: the browser's `</svg>` pops the nested foreign descendants before the following base; the implementation decrements its counter once, ignores that base, then reaches zero on `</math>` and accepts the page.

**Smallest fix:** Keep the clean path only when the parser can prove browser-equivalent handling of foreign-content integration points, breakout tokens, and matching foreign end tags. At minimum, detect and fail closed on browser-effective HTML base tokens in those paths, and do not apply HTML raw-text handling for SVG `title`/`style`/`script` as if they were HTML head elements. A stack of element names (rather than a depth counter) is needed to avoid treating mismatched ends as balanced.

## Checked and held

- The invoked source matches the requested candidate blob: `git rev-parse 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc:scripts/canonical_audit.py` and `git hash-object scripts/canonical_audit.py` both returned `2c40d71d0c7cd9a03c142b4e5c1d7535fa6c7ca7`. The checkout HEAD is later (`4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`), but the tested script bytes are identical to the candidate.
- The corrected 14-page CLI matrix covered nested SVG/MathML, mismatched and missing closes, ordinary `foreignObject` HTML, canonical in `foreignObject`, `base` in `foreignObject`/plain SVG/second `head`, SVG title/style/script, and CDATA. Exact command:

  ```sh
  python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-FalsifyForeignContent-JTrt/manifest.json --json; printf 'exit=%s\n' "$?"
  ```

  Exact output:

  ```text
  {"findings":[{"id":"html_unsupported","page":"https://example.test/cases/missing_svg_end.html"},{"id":"html_unsupported","page":"https://example.test/cases/foreignobject_canonical.html"},{"id":"html_unsupported","page":"https://example.test/cases/svg_cdata.html"}],"pagesChecked":14,"verdict":"could-not-evaluate"}
  exit=2
  ```

  The missing SVG end, canonical link inside `foreignObject`, and CDATA cases fail closed as expected. The properly nested pair, mismatch without a signal-changing element, ordinary `foreignObject` HTML, a plain SVG-namespace `<base>`, and a second `head` without a base have no findings. The focused six-case result above identifies the false-clean cases directly.
- The first exploratory matrix used an invalid oracle (`href=a.html` with a distinct expected canonical for each page); those `canonical_mismatch` results were discarded. The corrected expected canonical and per-case outcomes were recorded before the corrected run in `/tmp/kake-r23-FalsifyForeignContent-JTrt/expectations.md`.
- LSP status/references/definition/diagnostics could not be used: `read` returned `No such tool: xd://lsp` and listed no LSP device. The literal `grep` fallback was used only to locate parser symbols; it is not treated as semantic proof. The code-path conclusions above come from the read source and the CLI runs.
- No production files, Git/JJ state, or existing untracked round-23 work were changed; only this assigned report was written in the lane.

## Limits

- No browser engine was invoked. Browser behavior is checked against the cited WHATWG parsing/base-URL algorithms; actual execution here was limited to the candidate public CLI.
- No build, lint, formatter, or general test suite was run. No live pages were fetched; this assignment was a local validator behavior probe.
- Residual risk remains for foreign integration points and breakout/recovery sequences outside the explicit fixtures until the parser either models their browser tree construction or rejects ambiguous cases.