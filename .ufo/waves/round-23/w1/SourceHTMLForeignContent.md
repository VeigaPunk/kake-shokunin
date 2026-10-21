## Verdict

**WHATWG result (accessed 2026-10-21):** In ordinary in-body parsing, `<svg>` and `<math>` create SVG- and MathML-namespace elements. A direct `<link>` start tag while the adjusted current node is in SVG foreign content is also inserted in the SVG namespace, not as an HTML `link`. Foreign-content breakout can reprocess a token in the current HTML insertion mode, but cannot move it into the document's actual head: a breakout `<head>` token is ignored in body mode, and in-body `link` processing does not push the head element pointer. The validator's direct foreign-link check is fail-closed and avoids treating that SVG element as an HTML canonical link; it is conservatively broader than the specification and can reject pages it could otherwise continue auditing.

## Findings

### P2 — Foreign-link rejection is safe but conservatively blocks page evaluation

- **Impacted claim/axis:** `CanonicalHTMLParser`'s foreign-content handling; operability of the canonical preflight.
- **Observed source:** `read /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py:195-205` returned:
  ```python
  if self.foreign_depth:
      # SVG/MathML content after the explicit head cannot change head
      # canonicals; a canonical-looking link inside it stays ambiguous.
      if tag in {"svg", "math"}:
          self.foreign_depth += 1
      elif tag == "link" and is_canonical_relation(attrs_first_wins(attrs)):
          self.unsupported = True
      return
  ```
  `read /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py:621-628` shows that `evaluate_page` returns `"html_unsupported"` when `finish_supported()` is false.
- **Specification evidence:** URL: <https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inbody> (accessed 2026-10-21; fetched HTML header said “Living Standard — Last Updated 20 October 2026”). In-body SVG and MathML rules respectively say: “Insert a foreign element for the token, with SVG namespace.” / “Insert a foreign element for the token, with MathML namespace.” URL: <https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inforeign> (same access date); for a non-breakout start tag the rule says: “Any other start tag” and “Insert a foreign element for the token, with the adjusted current node's namespace.” Since `link` is not a foreign breakout tag and the direct parent/current SVG node is in the SVG namespace, a direct `<svg><link rel=canonical ...>` is an SVG-namespace element, not an HTML canonical link.
- **Observed output:** The source rule sets `unsupported = True`; the downstream source rule returns `"html_unsupported"`. No runtime probe was run.
- **Judgment / smallest fix:** This is a safe refusal, not a false acceptance: the validator does not count the foreign `<link>` as a canonical link. It is more restrictive than necessary for the direct SVG case, which the standard classifies rather than leaving ambiguous. If operability requires auditing such pages, model namespace/integration-point and breakout transitions sufficiently to ignore SVG-namespace `link` elements while still checking any HTML-namespace descendants; otherwise retain this as an explicit unsupported-input boundary. No production change made.

## Checked and held

- **(a) SVG/MathML start tags in body insert foreign elements.** URL: <https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inbody>, accessed 2026-10-21. Located the separate in-body `math` and `svg` start-tag cases. Exact quotes (each under 25 words): “Insert a foreign element for the token, with MathML namespace.” “Insert a foreign element for the token, with SVG namespace.”
- **(b) A direct `<link>` inside SVG is SVG namespace, not HTML.** URL: <https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inforeign>, accessed 2026-10-21. Exact quotes (each under 25 words): “Any other start tag”; “Insert a foreign element for the token, with the adjusted current node's namespace.” Combined with (a), this makes a direct SVG child `<link>` an SVG-namespace element. This statement is specifically for ordinary SVG foreign content; integration points and breakout tags change how later tokens are handled.
- **(c) Foreign content cannot move a node into the document's head.** URL: <https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inforeign>, accessed 2026-10-21. In the foreign start-tag breakout list, the exact excerpt is “\"h6\", \"head\", \"hr\"”; the algorithm then says “Reprocess the token according to the rules given in the section corresponding to the current insertion mode in HTML content.” URL: <https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inbody>, accessed 2026-10-21. Body mode's exact `<head>` rule is “A start tag whose tag name is one of: \"caption\", \"col\", \"colgroup\", \"frame\", \"head\", \"tbody\", \"td\", \"tfoot\", \"th\", \"thead\", \"tr\"” followed by “Parse error. Ignore the token.” A body-mode `link` token is processed using in-head rules, but body mode does not push the head element pointer; those rules therefore use the current body insertion location, not the document head. In-head's ordinary `link` case inserts an HTML element and pops the current node. **Conclusion:** no foreign-content path re-enters the actual in-head insertion mode or moves the foreign element/link into the document head.
- **Validator comparison:** In `canonical_audit.py:197-203`, tracked foreign content never records a `link` as a head canonical; a canonical-looking one is rejected as unsupported. This matches the essential safety property for the direct SVG case. Its `foreign_depth` counter does not model the standard's breakout tags or HTML integration points, so its result is deliberately a bounded approximation rather than a full WHATWG parse.

## Limits

- Read the public WHATWG HTML Standard and the specified source ranges only. No code was edited; no selftest, CLI probe, or build was run.
- The conclusion concerns the HTML parser's tree-construction behavior for HTML documents, not XML parsing or arbitrary DOM mutations after parsing.
- No tools were installed or updated.
