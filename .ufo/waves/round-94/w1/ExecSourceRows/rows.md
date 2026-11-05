# ExecSourceRows — appended registry rows (corpus/SOURCES.md lines 223-224)

Appended after S476 (line 222) in the `## Registry` table. Lane diff against HEAD for this file: `2 0` (two added lines, nothing else).

```
| S477 | RFC 9110 HTTP Semantics, section 9.1 Overview of Methods — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | method token case-sensitivity | section 9.1, plain-text lines 3748-3751 (heading line 3728), RFC 9110 June 2022 revision of the fetched body (sha256 21c1cdce6ab0) | Method tokens are case-sensitive, so get and GET name different methods; standardized methods are all-uppercase by convention, so write them that way. | mined | 2026-11-05 | 180d | corpus/knowledge/http-list-and-method-grammar.md, corpus/lessons/round-94.md |
| S478 | RFC 9110 HTTP Semantics, section 5.6.1 List Syntax — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | list member syntax and whitespace around list members | section 5.6.1 List Syntax, subsection 5.6.1.2 Recipient Requirements (heading line 1693), plain-text lines 1695-1702, RFC 9110 June 2022 revision of the fetched body (sha256 21c1cdce6ab0) | A recipient MUST accept lists with empty elements and OWS around each comma, and empty elements do not count toward the number of elements present. | mined | 2026-11-05 | 180d | corpus/knowledge/http-list-and-method-grammar.md, corpus/lessons/round-94.md |
```

Quotes (scout `ScoutRFC/quotes.json`; both verified exact_substring, whitespace-normalised, against the retained body `receipts/rfc9110.txt.retained`):
- S477 (plain-text lines 3748-3749): "The method token is case-sensitive because it might be used as a gateway to object-based systems with case-sensitive method names."
- S477 teaching sentence (lines 3750-3751): "By convention, standardized methods are defined in all-uppercase US-ASCII letters."
- S478 (lines 1699-1702): "a recipient MUST accept lists that satisfy the following syntax: #element => [ element ] *( OWS \",\" OWS [ element ] )"
- S478 teaching sentence (lines 1695-1696): "Empty elements do not contribute to the count of elements present."
