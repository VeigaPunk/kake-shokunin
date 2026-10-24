# ScoutReopenS092 — S092 re-opened live, S025 template sentence checked

Sealed key: never listed, read, stat'ed or searched; no path under /fast/scratch/hyaku/kake-r36/ was touched and the counter was not run (no key). Read-only git was not needed. No tool installed or upgraded.

## Commands (all exit 0 unless stated)

```
curl -sS -o syntax.html   -w '%{http_code} %{size_download} %{content_type}\n' --max-time 60 \
  -A 'Mozilla/5.0 (X11; Linux x86_64) kake-r36-recheck/1.0' https://html.spec.whatwg.org/multipage/syntax.html
  -> 200 89196 text/html; charset=utf-8
curl -sS -o scripting.html ... https://html.spec.whatwg.org/multipage/scripting.html
  -> 200 276128 text/html; charset=utf-8
curl -sSI (same two URLs, headers below)
sha256sum syntax.html scripting.html
zcat .ufo/waves/round-36/sources/S092.html.gz | sha256sum
python3 <extractor: strip script/style, strip comments, strip tags, unescape, collapse \s+>  -> syntax.text
python3 verbatim-find of the S025 row quote in scripting.text
```

## F1 — S092 body is byte-identical on re-open; no drift since the L1 fetch

| item | my fetch (2026-10-23T01:35:05Z) | retained / receipt |
|---|---|---|
| HTTP | 200 | receipt status 200 |
| bytes | 89196 | receipt bodyBytes 89196 |
| sha256 body | `0128a08f5d6a544d9c38420f9f7a9956d7da2ef499948ecc7f3488de45fb648f` | receipt bodySha256 `0128a08f…648f`; `zcat S092.html.gz` same |
| etag / last-modified | `"6ada7f53-15c6c"` / `Thu, 22 Oct 2026 21:25:39 GMT` | — |

Both fetches postdate Last-Modified by ~4 h, so the retained row would record the current revision, not a stale one. `date -u` at my run = Fri 23 Oct 2026 01:35:04 UTC, i.e. 26 min after the L1's 01:08:59Z receipt; the receipts' accessedUtc is therefore not a future timestamp (the session header's "2026-10-22" is the stale value, not the receipt).

## F2 — the retained text artifact is exactly reproducible, but only with a trailing newline

My extractor on my own body gives 5852 words (receipt textWords 5852). `sha256(syntax.text)` = `a0ffd6c19319590e8a5f294f9496dc4893d06040afd7fcc3822a579a53d0b46e`, which does **not** equal receipt textSha256 `2fb98770463f89d127d4f02bc92c9306164a530498bc78db61e8875f4496adb3`; `sha256(syntax.text + "\n")` equals it exactly, and `syntax.text == retained S092.txt.rstrip("\n")` (first-and-only diff at offset 31920, retained has one trailing `\n`).

Consequence for C1 (e): the receipt's textRule string does not state the trailing newline, yet the recorded textSha256 only reproduces with it. A re-check tool that canonicalizes text without the newline computes a different digest than the registry receipt and would flag a fresh source as changed. Pin the newline (or the absence of one) in the contract.

## F3 — quotes, with section numbers (punctuation spacing preserved as the collapse rule emits it)

- §13.1.2 Elements (`syntax.html:130`, `id=elements-2`): "There are six different kinds of elements : void elements , the template element , raw text elements , escapable raw text elements , foreign elements , and normal elements ." then the list "Void elements area , base , br , col , embed , hr , img , input , link , meta , source , track , wbr / The template element template / Raw text elements script , style / Escapable raw text elements textarea , title / Foreign elements Elements from the MathML namespace and the SVG namespace . / Normal elements All other allowed HTML elements are normal elements."
- §13.1.2.6 Restrictions on the contents of raw text and escapable raw text elements (`syntax.html:792`, `id=cdata-rcdata-restrictions`): "The text in raw text and escapable raw text elements must not contain any occurrences of the string \" </ \" (U+003C LESS-THAN SIGN, U+002F SOLIDUS) followed by characters that case-insensitively match the tag name of the element followed by one of U+0009 CHARACTER TABULATION (tab), U+000A LINE FEED (LF), U+000C FORM FEED (FF), U+000D CARRIAGE RETURN (CR), U+0020 SPACE, U+003E GREATER-THAN SIGN (>), or U+002F SOLIDUS (/)."
- §13.1.4 Character references (`syntax.html:820/827`, `id=character-references`): "Character references must start with a U+0026 AMPERSAND character (&). Following this, there are three possible kinds of character references:" — Named ("The ampersand must be followed by one of the names given in the named character references section, using the same case."), Decimal numeric ("The ampersand must be followed by a U+0023 NUMBER SIGN character (#), followed by one or more ASCII digits, …The digits must then be followed by a U+003B SEMICOLON character (;)."), Hexadecimal numeric (same, with x/X after #). Also: "An ambiguous ampersand is a U+0026 AMPERSAND character (&) that is followed by one or more ASCII alphanumerics, followed by a U+003B SEMICOLON character (;), where these characters do not match any of the names given in the named character references section."
- §13.1.6 Comments (`syntax.html:880-890`, `id=comments`): "Comments must have the following format: The string \" <!-- \". Optionally, text, with the additional restriction that the text must not start with the string \" > \", nor start with the string \" -> \", nor contain the strings \" <!-- \", \" --> \", or \" --!> \", nor end with the string \" <!- \". The string \" --> \". The text is allowed to end with the string \" <! \", as in <!--My favorite operators are > and <!-->."

## F4 — quote match on collapsed text is punctuation-hostile (falsifier for the C1 quote check)

Because the collapse rule inserts spaces around tags, punctuation that hugged a tag carries a leading space in the text artifact (`elements :`, `void elements ,`, `Raw text elements script`). A quote copied from the rendered page ("There are six different kinds of elements: void elements, the template element, …") does **not** occur verbatim in `S092.txt`; only the space-padded form does. A re-check that does plain `quote in text` on the stored text will fail correct quotes and pass padded ones. Normalize spaces around `,;:.()` on both sides, or quote from the text artifact.

## F5 — S025's stored quote is a paraphrase, not verbatim source text

My `scripting.html` = 200, 276128 bytes, sha256 `a7741016d8120b00995b438a375ddd448894035580c7801d1b4f9a89d87944b9`, etag `"6ada7f52-436a0"`, last-modified `Thu, 22 Oct 2026 21:25:38 GMT`. There is no retained S025 body in `.ufo/waves/round-36/sources/`, so this is the only copy.

- §4.12.3 The template element (`id=the-template-element`, `id=template-contents`): "The `template` element has an associated `DocumentFragment` object that is its template contents ." and "The template contents of a template element are not children of the element itself ." (`scripting.html:1600` and `:1553`).
- Row `corpus/SOURCES.md:33` quote: "Template contents are not children of the template element itself and do not supply document-head canonical links".
- Verbatim find: `"are not children of the template element itself"` -> **-1** (absent); `"do not supply document-head canonical links"` -> -1 (absent; lane-side inference). The spec says "of the element itself", not "of the template element itself".

Consequence: if C1's quote-match is applied to existing rows, S025 reports as an unmatched quote even though the source is fresh and the claim is true — a false alarm caused by the row, not the source. Do not store the S025 paraphrase as a verbatim quote, and do not use it as a clean case in any scaling.

## F6 — two wording traps for a registry row over this source

1. The spec's order is "Escapable raw text elements textarea , title" (alphabetical); the ticket text says "title, textarea". A row quoting the ticket order fails verbatim.
2. The element-kind classification is §13.1.2 (`id=elements-2`); the `</`-prohibition is its own subsubsection §13.1.2.6 (`id=cdata-rcdata-restrictions`). Citing "13.1.2" for the prohibition would misname the section.

## Not verified / gaps

- No sealed case, counter run or pass count was observed; I make no claim about C1's verdict.
- I did not compare the L1 fetcher's UA/Accept-Encoding (fetcherSha256 `215f59…`) with mine; identity of bytes makes encoding-only drift moot for this URL but is untested for S088-S091.
- I did not re-open S093/S094 (out of scope), and did not check whether the registry contract requires a row for S092 before C1 cites it.

## Artifacts (sandbox, absolute)

- `/fast/scratch/hyaku/kake-r36w1/ScoutReopenS092/syntax.html` (89196 B), `scripting.html` (276128 B)
- `syntax.text` (31920 chars, 5852 words), `scripting.text`
- `sec_raw.txt`, `sec_charref.txt`, `sec_comments.txt` (verbatim section slices)
