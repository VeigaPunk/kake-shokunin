## Verdict

On 2026-10-21, the WHATWG HTML Living Standard’s start-tag syntax permits the solidus for void or foreign elements; on void elements the solidus has no self-closing effect. Since non-void HTML elements are not foreign elements, they are outside the permitted cases. The exact 13-element void list matches `HTML_VOID_ELEMENTS` in `scripts/canonical_audit.py` with no differences.

## Findings

### P3 — WHATWG syntax and void-element inventory agree

- **Source URL(s):** <https://html.spec.whatwg.org/multipage/syntax.html#void-elements> and <https://html.spec.whatwg.org/multipage/syntax.html#start-tags>
- **Access date:** 2026-10-21
- **Located quotes** (each quote is at most 25 words; both are from `#start-tags`, step 6):
  - “if the element is one of the void elements, or if the element is a foreign element, then there may be a single U+002F SOLIDUS …” (25 words). The permitted cases are void elements and foreign elements; a non-void HTML element is not in either case.
  - “On void elements, it does not mark the start tag as self-closing but instead is unnecessary and has no effect of any kind.” (23 words).
- **Exact list at `#void-elements`:** `area`, `base`, `br`, `col`, `embed`, `hr`, `img`, `input`, `link`, `meta`, `source`, `track`, `wbr`.
- **Exact command/observed output — WHATWG:** `GET https://html.spec.whatwg.org/multipage/syntax.html#void-elements` returned the “Void elements” list shown above; `GET https://html.spec.whatwg.org/multipage/syntax.html#start-tags` returned the quoted step-6 wording.
- **Exact command/observed output — local definition:** `read /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py:38-40`:
  ```python
  HTML_VOID_ELEMENTS = {
      "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"
  }
  ```
  The names and membership are identical to the spec list; no extra or missing entries.
- **Additional local handling observed:** `read /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py:292-294` returned:
  ```python
  if tag not in HEAD_VOID_ELEMENTS and not (self._after_head() and tag in HTML_VOID_ELEMENTS):
      # HTML ignores the slash on non-void tags; do not infer a close.
      self.unsupported = True
  ```
- **Impacted claim/axis:** source-level support for the HTML self-closing-tag behavior and void-element inventory; freshness.
- **Smallest fix:** none for the element set; it exactly matches the current spec list. The local comment/unsupported handling is consistent with the syntax rule for non-void HTML tags.

## Checked and held

- Read the WHATWG `#void-elements` and `#start-tags` sections using public GET requests.
- Read the local void-element set and self-closing-tag handling in `scripts/canonical_audit.py`.
- No source files were changed; no build, test, lint, or formatter was run.

## Limits

This is a source-level comparison, not a runtime or browser-conformance test. The non-void restriction follows from the start-tag rule’s permitted cases (void or foreign); the quote itself is intentionally split into two short excerpts to keep each within the requested 25-word limit.