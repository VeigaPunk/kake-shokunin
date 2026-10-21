# Pair S030 × static-canonical-preflight — freshness recheck (round 26, C1)

Knowledge seat (leaf). Judged against retained round-26 bytes only; no network, no builds or tests, no edits to the entry, SOURCES.md, or code.

## Provenance

- Entry: `corpus/knowledge/static-canonical-preflight.md`. 180 lines, 14,076 bytes, sha256 `192eac303fa3ba8a2aab9d545fe6b0627f3a174dff1b54472e1bab2f771fdaf7`, read tag `#8B13`.
- Fetch (manifest.json, row S030, index 1; population.json record agrees): `https://html.spec.whatwg.org/multipage/syntax.html#start-tags`, status 200, `text/html; charset=utf-8`, Last-Modified `Tue, 20 Oct 2026 12:58:33 GMT`, 89,196 bytes, sha256 `04b65bf0b4b5f3bb3815999ab499af980fa09b8832f02c1686c544ab8e79a52d` (equals the decompressed `S030-1.raw.gz`), fetchedAt `2026-10-21T15:10:50.088887+00:00`. The raw HTML contains `id=start-tags`.
- Text view `fetched/text/S030-1.txt`: 31,810 bytes, one line, sha256 `c7228ee108988f11fcb9be86142018a9c6a47e06ae33970f9763b58d8d7337eb`, reads "Last Updated 20 October 2026".
- Scope of the retained bytes: `syntax.html` is section 13.1 only. Its nav links 13.2 to `parsing.html`, which is not retained. No statement in this pair depends on 13.2.
- Quote fidelity: the five distinct quotes below (rows 1–8 reuse them) all appear in the text view, whitespace-normalized, and in the raw HTML with tags removed.
- Offsets are character offsets (`@N`) in the one-line text view.

## Statements attributed to S030 (entry lines 98–99, 110–111, 151)

There are three attributed passages, which split into eight testable claims. There are no r20 tails in this entry (see below).

| # | Line | Statement as written | Verdict | Verbatim S030 quote (offset, words) | Anchor observed | Reason |
|---|---|---|---|---|---|---|
| 1 | 98–99 | "a slash is allowed only on void or foreign elements" | HOLD | "if the element is one of the void elements, or if the element is a foreign element, then there may be a single" (@9310, 23) | §13.1.2.1 Start tags (@8607); the solidus is the "step 6" of the start-tag syntax (cross-reference @12167) | The solidus is permitted under exactly that condition. S030 grants it to no other element. |
| 2 | 98–99 | "…and has no effect on void elements" | HOLD (read with line 151) | "On void elements, it does not mark the start tag as self-closing but instead is unnecessary and has no effect of any kind." (@9514, 23) | §13.1.2.1 | Supported. S030's next sentence carves out the unquoted-value case, and line 151 states that carve-out. SOURCES.md:102 records the same caveat. |
| 3 | 110 | "the 13 names in S030" | HOLD | "Void elements area, base, br, col, embed, hr, img, input, link, meta, source, track, wbr" (@4242, 15 including label) | §13.1.2 Elements (@4059) | Exactly 13 names. `scripts/canonical_audit.py:38–40` `HTML_VOID_ELEMENTS` lists the same 13. |
| 4 | 110 | "Self-closed HTML void elements (`<input />`, `<img />`, `<br/>`, …)" | **STALE** (label; substance HOLD) | "On void elements, it does not mark the start tag as self-closing but instead is unnecessary and has no effect of any kind." (@9514, 23) | §13.1.2.1 solidus sentence | S030 says a solidus on a void element "does not mark the start tag as self-closing". Self-closing is the foreign-element mark (row 5). The examples remain valid void start tags. Only the term is wrong, and line 151 already uses the correct one. Correction C-1. |
| 5 | 111 | "A self-closed non-void element (`<div/>`) stays unsupported." | **STALE** (label; outcome HOLD) | "then there may be a single U+002F SOLIDUS character (/), which on foreign elements marks the start tag as self-closing." (@9394, 20) | §13.1.2.1 step 6 | The outcome is supported: S030 permits the solidus only on void or foreign elements (row 1). The label conflicts with S030, which reserves the self-closing mark for foreign elements. Correction C-2. |
| 6 | 151 | "a separate trailing solidus has no effect on a void-element start tag" | HOLD | As row 2 (@9514) | §13.1.2.1 | "Separate" means not absorbed into an unquoted value. S030 gives "no effect of any kind" for that case. |
| 7 | 151 | "a slash immediately following an unquoted attribute is part of the value (`href=/x/>` means `/x/`)" | HOLD (precision, no correction) | "if directly preceded by an unquoted attribute value, it becomes part of the attribute value rather than being discarded by the parser." (@9717, 22) | §13.1.2.1, the sentence after the void sentence | Supported by retained 13.1 text, so the tokenizer (13.2) is not needed. S030 says "unquoted attribute value"; the entry's shorter "unquoted attribute" is looser, but the example pins the meaning. A valueless attribute (`<input disabled/>`) is not an unquoted value, so row 6 governs it. |
| 8 | 151 | "This is not an XML-style self-closing element" | HOLD | As row 2 (@9514) | §13.1.2.1 | S030 defines the void-element solidus as not marking self-closing. "XML-style" is the entry's gloss. |

Totals: 8 statements, 6 HOLD, 2 STALE. Both STALE items are wording only. The outcomes, the 13-name list, and the tool behavior are not in dispute.

## Superseded and anchor check

- Nothing cited is superseded. The text reads "Last Updated 20 October 2026" (Last-Modified 2026-10-20 12:58:33 GMT). That is the Living Standard the row and the round-23 section were opened against. There has been no drift since opening.
- The anchors hold: §13.1.2 Elements (@4059), §13.1.2.1 Start tags (@8607), the step-6 cross-reference (@12167), and `id=start-tags` in the raw HTML.
- The two STALE items predate this recheck. The round-23 precision note (SOURCES.md:102) addressed line 151 only, and lines 110–111 kept the label.
- r20 tails: none. A search for `r20`, `R20`, and `round 20`/`round-20` finds nothing. The only correction block is `### Corrections to earlier text in this entry` (lines 138–146, all tagged r23). It cites S021 and S025, not S030, so it is outside this pair.
- Later appended sections: lines 149–154 contain rows 6–8. Lines 157–180 (round 24) do not reference S030.

## Corrections (append-only; STALE rows only)

Placement: append at end of file under a new heading `### Round-26 S030 corrections`. No original line changes.

C-1 (row 4):

```
- [r26-correction] Line 110's 'Self-closed HTML void elements' misuses S030's term. S030 §13.1.2.1 says that on void elements the trailing solidus 'does not mark the start tag as self-closing', and that it marks a start tag as self-closing only on foreign elements. Read the bullet as: void-element start tags with a trailing solidus (`<input />`, `<img />`, `<br/>`, …; the 13 names in S030 §13.1.2) are evaluated after the closed head. Line 151 gives the same reading. (r26 w1/PairS030StaticCanonicalPrefl)
```

C-2 (row 5):

```
- [r26-correction] Line 111's 'A self-closed non-void element (`<div/>`) stays unsupported' has the right outcome but the wrong label. S030 §13.1.2.1 permits a trailing solidus only on void or foreign elements, and says the solidus marks a start tag as self-closing only on foreign elements. Read it as: a trailing solidus on a non-void element (`<div/>`) is outside the S030 start-tag grammar and stays unsupported. (r26 w1/PairS030StaticCanonicalPrefl)
```

## Adjacent observations (not counted; no STALE verdict)

1. **Header omission.** Header lines 1–2 (`source:`, `verified-at:`) list sources through S029 and omit S030. Optional append-only tail note: `- [r26-note] Header lines 1–2 omit S030 (WHATWG HTML syntax, syntax.html#start-tags; Last Updated 20 October 2026; re-fetched 2026-10-21). S030 is cited at lines 98–99 and 151.` S031–S034 are omitted the same way; they are outside this pair.
2. **Tool help text.** `scripts/canonical_audit.py:108` uses "self-closed HTML void elements", the same term as C-1. The code is outside this seat's write scope; flagged for L1 or the tool owner.
3. **Foreign self-closing is undescribed.** `scripts/canonical_audit.py:299–304` accepts a self-closed foreign start tag and opens nothing. S030 supports that ("in which case they must not have an end tag"). The SVG/MathML bullet (lines 106–109) and lines 113–115 do not describe this path. That is a coverage gap, not staleness.
4. **Tool void lists match.** `HTML_VOID_ELEMENTS` (`scripts/canonical_audit.py:38–40`) equals S030's 13 names. `HEAD_VOID_ELEMENTS` = {base, link, meta} (line 37) applies only inside the head (line 305), matching the entry's "after the closed head" framing.
5. **Outside this pair.** `corpus/lessons/round-23.md` also cites S030 (SOURCES row and population usedBy). It is a lesson seat and was not checked here. Lines 86–88 ("WHATWG slash-skipping") concern URL parsing, not S030.
6. **SOURCES.md S030 row (row seat, for L1).** The anchors hold: "step 6", 13 names, "last updated 20 October 2026", and opened 2026-10-21.

## Verification gaps

- Retained S030 bytes are 13.1 only. The tokenizer text (13.2, `parsing.html`) is not retained. No pair statement depends on it, because row 7 is decided by the 13.1.2.1 sentence.
- The text view is one line, so locations are given as heading text and character offsets, not line numbers.
- `scripts/canonical_audit.py --selftest` was not run. Tests are outside this item's scope.
- The `w2/ReopenS030` pointer on line 151 was not opened. It is outside the retained-bytes scope.

## Tooling

No tools were installed or updated. Checks used the host `python3` standard library (`gzip`, `hashlib`, `json`, `re`) and the read and grep tools.

```json
{"pair":"S030xstatic-canonical-preflight","statements":8,"hold":6,"stale":2,"corrections":["- [r26-correction] Line 110's 'Self-closed HTML void elements' misuses S030's term. S030 §13.1.2.1 says that on void elements the trailing solidus 'does not mark the start tag as self-closing', and that it marks a start tag as self-closing only on foreign elements. Read the bullet as: void-element start tags with a trailing solidus (`<input />`, `<img />`, `<br/>`, …; the 13 names in S030 §13.1.2) are evaluated after the closed head. Line 151 gives the same reading. (r26 w1/PairS030StaticCanonicalPrefl)","- [r26-correction] Line 111's 'A self-closed non-void element (`<div/>`) stays unsupported' has the right outcome but the wrong label. S030 §13.1.2.1 permits a trailing solidus only on void or foreign elements, and says the solidus marks a start tag as self-closing only on foreign elements. Read it as: a trailing solidus on a non-void element (`<div/>`) is outside the S030 start-tag grammar and stays unsupported. (r26 w1/PairS030StaticCanonicalPrefl)"]}
```
