# KakeR36.RevengerGateRule — Gate quote rule vs C1 contract (c)+(d)

## The rule rounds 34–35 used (reconstructed)

`visible_text` is identical in `.ufo/waves/round-34/fetch_sources.py:45-50` and
`.ufo/waves/round-35/fetch_sources.py:45-50` (round 35 is a copy; docstring + receipts
`textRule` agree). Order on the raw decoded body:

1. remove `<script|style\b>...</script|style\s*>` (ASCII-case-insensitive; end tag must be `</name` + spaces + `>` — attributes or `/` break it);
2. remove `<!--` to next `-->`;
3. remove every `<[^>]+>` (any char after `<`; `<%`, `<?`, `<3 >` all gone; `<x` with no `>` kept);
4. `html.unescape` (all named/decimal/hex refs);
5. `\s+` → single space, `.strip()`, trailing `\n`.

`template` is NOT a special element — its contents survive. Media type is never read:
one pipeline for every body, and receipts record no contentType (`fetch_sources.py:64-73`).

Quote check: **substring, nothing else**. Three implementations:
- `ScribeGateLines/verify_quotes.py`: `ok = q in t` — literal, not even collapsed.
- `ScribeSourcesRows/quotes.py:11-18`: `collapse(q) in collapse(t)`.
- `c2_source_census.py:88-89,222,228`: `collapse(quote) in collapse(text)` + flip-letter control.
- Lesson: `corpus/lessons/round-35.md:40-42` "verified as exact substrings".
No NFKC anywhere. Quote chosen by a human from the .txt (6-25 words, one curly-quoted span;
`c2_source_census.py:223`, `check_gate.py` `quote_exact`).

## Differences from C1 (c)+(d), each with a disagreement input

Emulated C1 = comments → script/style/template contents → `<`+ASCII letter/`/`/`!` to `>` →
`html.unescape` → NFKC + delete-isspace substring. Verified against real retained bodies.

1. **Whitespace**: Gate collapses, C1 deletes all `isspace()` chars after NFKC.
   Real input (S078.txt): `.well-\nknown` → `.well- known`. Quote
   `e.g., https://example.com/.well-known/security.txt as per [RFC8615]`: Gate MISS, C1 HOLD
   (measured). This is the quote ScribeGateLines found unmatchable (w1/ScribeGateLines.md:43-46).
2. **NFKC**: Gate has none, C1 normalizes both sides. `ofﬁce` text vs `office` quote: Gate MISS, C1 HOLD.
3. **template**: Gate keeps contents, C1 removes them. `x<template>SECRET</template>` quote `SECRET`:
   Gate HOLD, C1 `quote_missing`.
4. **Comment/script order**: Gate strips script/style before comments; C1 comments first.
   `<script>SECRET<!--</script>-->TAIL`: Gate text `x -->TAIL y` (SECRET gone, `-->TAIL` kept);
   C1 keeps `SECRET` (comment ate the closer; unclosed script kept) and drops `-->TAIL` —
   flips in both directions (measured).
5. **End-tag strictness**: Gate needs `</name\s*>`; C1 "next end tag of the same name" matches
   `</script foo>`. `<script>hidden</script foo><p>tail</p>` quote `hidden`: Gate HOLD, C1 MISS
   (measured under the `[^>]*>` reading; contract is ambiguous here).
6. **Tag rule breadth**: Gate `<[^>]+>` vs C1 `<`+letter/`/`/`!`. `a <?xml v?> b c` quote
   `xml v?> b c`: Gate MISS, C1 HOLD (measured). Also `<%…%>`, `a <3 > b`.
7. **Media type**: Gate's pipeline ran on `text/plain` too — on real S078 it ate the ABNF
   productions: `date-time = < imported from Section 5.6 of [RFC3339] >` is absent from S078.txt,
   present in the body. C1(e) keeps plain text as-is → that quote flips Gate MISS → C1 HOLD
   (measured). Entities likewise: `R&D;` in plain text decodes under Gate only.
8. **Two Gate variants disagree internally**: literal `q in t` vs `collapse(q)`: a quote
   containing NBSP (or any run of whitespace) misses the seat script but passes the counter.
   C1 agrees with neither.
9. **Status scope**: Gate verified quotes on non-200 bodies — S087's quote is on a 404 page
   (lesson :53). C1 evaluates no quote check unless the last hop is 200.
10. **Quote provenance**: Gate constrains the quote (6-25 words, chosen from the extracted text);
    C1 takes whatever string the manifest gives. Under C1 a whitespace-free or NFKC-folded
    paraphrase of the text passes — the Gate rejected exactly such a paraphrase.

## Which Gate quotes change verdict

All 22 landed Gate quotes (11 round-34 + 10 round-35 + S006 re-open) re-tested against the
retained bodies: **HOLD under Gate and HOLD under the C1 emulation — no landed quote flips**.
But the direction of risk is asymmetric: C1 is *looser* on (d) (whitespace deletion, NFKC) —
the one real Gate rejection observed (S078 wrap quote) flips to clean, so C1 can certify a
row's quote as present where the Gate would report drift. Conversely, (c) differences let C1
drop text the Gate kept (`template`, `</script x>` end tags, comments inside scripts): a
re-check of S068/S077 (both bodies contain `<template>`) could report `quote_missing` for a
quote the Gate verified. C1 also cannot express a quote on a non-200 body (S087 pattern).

## Evidence

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-3{4,5}/fetch_sources.py:45-50`
- `/.ufo/waves/round-34/c2_source_census.py:88-89,222-230`
- `/fast/scratch/hyaku/kake-r35/w1/ScribeGateLines/verify_quotes.py` (`ok = q in t`)
- `/fast/scratch/hyaku/kake-r34/w1/ScribeSourcesRows/quotes.py:11-18`
- `corpus/lessons/round-35.md:40-54,124-127`; `w1/ScribeGateLines.md:23-28,43-46`
- Contract: `git show cd3212796cab7a2afa03b638dbfafe7194df9629:SCORECARD.md` bullets (c),(d),(e)
- Differential script run in `/fast/scratch/hyaku/kake-r36w1/RevengerGateRule/` (python3 3.14,
  read-only on the lane, exit 0). No tools installed (pacman paused; stdlib sufficed).

## Not verified

The real tool does not exist yet, so C1 behaviour above is an emulation of the contract text,
not the shipped code. Unclosed script/style/template and unclosed comments are undecided by
the contract (diffs 4-5 assume the `[^>]*>` end-tag reading). Gate quotes for S071/S087 use
redirect/404 bodies; Gate never recorded Content-Type, so diff 7's per-body effect was
inferred from serving conventions, not receipts.
