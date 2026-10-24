## Verdict

Counterexample found.

## Findings

- **P2 — S030/S031 lesson digest prefixes appear cross-assigned (evidence-pointer operability).** `corpus/lessons/round-23.md:60-61` associates `a11dcf17…` with S030's `syntax.html` URL and `04b65bf0…` with S031's `parsing.html` URL. Re-fetched raw response bodies produced the opposite mapping:

  Exact command:
  ```sh
  T=/tmp/kake-r23w2-ReopenS030-IiJJ && curl -sS --max-time 90 https://html.spec.whatwg.org/multipage/parsing.html -o "$T/parsing.html" && sha256sum "$T/parsing.html" "$T/syntax.html" && wc -c "$T/parsing.html" "$T/syntax.html"
  ```
  Exact output:
  ```text
  a11dcf1768a76e24cdf7e16060f54bcb149c529aa8bcb9297b8d1ab633b26f13  /tmp/kake-r23w2-ReopenS030-IiJJ/parsing.html
  04b65bf0b4b5f3bb3815999ab499af980fa09b8832f02c1686c544ab8e79a52d  /tmp/kake-r23w2-ReopenS030-IiJJ/syntax.html
  826255 /tmp/kake-r23w2-ReopenS030-IiJJ/parsing.html
   89196 /tmp/kake-r23w2-ReopenS030-IiJJ/syntax.html
  ```
  The syntax response's Last Updated date is 20 October 2026, matching the lesson's stated date. **[INFERENCE]** If these `sha256` labels are response-body digests, the prefixes are swapped. Smallest fix: swap the S030/S031 digest labels, or identify the hashed object and regenerate each digest for its stated URL. The URL, date, and S030 quote themselves re-open correctly.

- **P3 — The no-effect paraphrase needs the unquoted-attribute qualifier.** `corpus/SOURCES.md:38` and `corpus/knowledge/static-canonical-preflight.md:98-99` summarize S030 as saying a slash “has no effect on void elements.” WHATWG §13.1.2.1 step 6 says the quoted sentence about not setting the self-closing flag, then immediately cautions that when the solidus directly follows an unquoted attribute value it becomes part of that value, not discarded. For example, `<link rel=canonical href=/x/>` has `href` `/x/`, not `/x`.

  Exact Python probe program and output:
  ```python
  from html.parser import HTMLParser
  class P(HTMLParser):
      def handle_starttag(self, t, a): print(t, dict(a))
      def handle_startendtag(self, t, a): print(t, dict(a), "startend")
  P().feed("<link rel=canonical href=/x/>")
  ```
  Exact output:
  ```text
  link {'rel': 'canonical', 'href': '/x/'}
  ```
  The lane parser probe was:
  ```python
  import runpy
  path='/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py'
  m=runpy.run_path(path)
  p=m['CanonicalHTMLParser']()
  p.feed('<head><link rel=canonical href=/x/></head>')
  print('head_canonicals=',p.head_canonicals)
  print('unsupported=',p.unsupported)
  ```
  Exact output:
  ```text
  head_canonicals= [{'rel': 'canonical', 'href': '/x/'}]
  unsupported= False
  ```

  So this is a documentation-scope issue, not an observed validator misparse. The lesson quote is exact and 23 whitespace-separated words, located at the cited step, but stops before this material caveat. The “Self-closed HTML void elements” wording in `static-canonical-preflight.md:110-111` is also technically imprecise: S030 says the slash does not mark a void start tag as self-closing. Smallest fix: say “void-element start tags with a separate trailing solidus,” and qualify the unquoted-value case in the row/knowledge summary; the 23-word quote can remain with that note.

## Checked and held

- Re-opened both requested fragments at `https://html.spec.whatwg.org/multipage/syntax.html#start-tags` and `#void-elements`. The source is the Living Standard dated 20 October 2026. §13.1.2.1 step 6 contains the lesson's quote verbatim; the void-elements list contains 13 names: area, base, br, col, embed, hr, img, input, link, meta, source, track, wbr.
- The S030 row's located section references (13.1.2.1 step 6; 13.1.2 void-elements list), access date 2026-10-21, kind `spec`, and tier `A` are consistent. `SOURCES.md:3` says tiers are scoped to the row's stated topic.
- Both `S030` used-by paths in the row exist and cite S030: `corpus/knowledge/static-canonical-preflight.md` and `corpus/lessons/round-23.md`.
- `scripts/canonical_audit.py`'s `HTML_VOID_ELEMENTS` set contains the same 13 names. No membership counterexample found.

## Limits

No LSP device was exposed in this session; findings use direct source reads and a targeted parser probe. I did not run the full audit selftest or an end-to-end manifest check, and I did not assess the separate S031 foreign-content claims in the knowledge section. No tools were installed.