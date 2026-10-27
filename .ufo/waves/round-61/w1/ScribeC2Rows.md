# ScribeC2Rows

Round-61 w1 leaf seat. Drafted registry rows S430–S433 and their lesson Gate lines for claim C2
(operability / response-header expectation audit), built the append block, and ran the mirror-census
validation. Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin` (read-only for this seat outside its
own report and `.files/`). Fleet base for the mirror: `9f07731a873585e655a6518233ea39f5d9fb8204`
(round-61 base, registry = 167 rows). Access date of every row and Gate line: 2026-10-27 (UTC).

## ROWS:

Four rows, 11-cell schema, appended in id order. Full block:
`.ufo/waves/round-61/w1/ScribeC2Rows.files/rows.md` (rows also in `rows-append.md`).

- S430 — RFC 6797 HSTS — spec / A / `HSTS policy signalling (STS response header)` — anchor
  `Section 6.1 Strict-Transport-Security HTTP Response Header Field and Section 5.1 HSTS Host Declaration; RFC 6797, November 2012` — teaches: a host declares an HSTS policy by sending the
  Strict-Transport-Security field over secure transport, so a captured HTTPS response without it carries
  no declaration to audit — mined / 2026-10-27 / 180d / `corpus/knowledge/response-header-expectations.md`.
- S431 — W3C CSP Level 3 — spec / A / `Content-Security-Policy header as policy conveyance` — anchor
  `Section 3.1 The Content-Security-Policy HTTP Response Header Field; W3C Working Draft WD-CSP3-20261027, 27 October 2026` — teaches: the CSP response header field is the document's preferred
  mechanism for delivering a policy server→client, so its presence/absence is the conveyance signal an
  offline audit reads — mined / 2026-10-27 / 180d / same used-by.
- S432 — WHATWG Fetch — spec / A / `X-Content-Type-Options nosniff value rule` — anchor
  `Section 3.6 X-Content-Type-Options header and its value ABNF; WHATWG Living Standard accessed 2026-10-27` — teaches: the field has one defined value, `nosniff`, compared ASCII case-insensitively
  against the split field values — mined / 2026-10-27 / 180d / same used-by.
- S433 — RFC 9110 — spec / A / `Content-Type field semantics and HTTP field-line rules` — anchor
  `Section 8.3 Content-Type and Section 5.2 Field Lines and Combined Field Value; RFC 9110, June 2022` — teaches: Content-Type is a singleton field whose accidental repetition only looks like a list, while
  field lines combine in received order by comma concatenation — mined / 2026-10-27 / 180d / same used-by.

## GATE:

Lines as written into `rows.md` (CORPUS rule 1: URL, access date, located ≤25-unit quote; the section
name is carried after the quote, round-60 precedent). Every quote is ASCII, 6..25 units, ≤160 chars, a
substring of one whitespace-collapsed text node of the retained body at
`.ufo/waves/round-61/sources/S43N.html`, and occurs once in that page (machine check in
`ScribeC2Rows.files/quote-check.txt`).

- S430 — https://www.rfc-editor.org/rfc/rfc6797.html — opened 2026-10-27 — "The Strict-Transport-Security HTTP response header field (STS header field) indicates to a UA that it MUST enforce the HSTS Policy" (20 units; § 6.1)
- S431 — https://www.w3.org/TR/CSP3/ — opened 2026-10-27 — "HTTP response header field is the preferred mechanism for delivering a policy from a server to a client." (18 units; § 3.1)
- S432 — https://fetch.spec.whatwg.org/ — opened 2026-10-27 — "Web developers and conformance checkers must use the following" (9 units; § 3.6)
- S433 — https://www.rfc-editor.org/rfc/rfc9110.html — opened 2026-10-27 — "Although Content-Type is defined as a singleton field, it is sometimes incorrectly generated multiple times" (15 units; § 8.3)

Retained-body digests were re-checked by this seat against `sources/receipts.json` and match:
S430 `f086bfac…72c0a` 133951 B, S431 `be8f2468…144e` 1011256 B, S432 `63b0a018…911b` 1854393 B,
S433 `d4317606…e1e5` 1187554 B. The same four digests came back from this seat's own GET, so the
retained bytes are corroborated, not merely trusted.

## CENSUS:

Mirror replicated from `validate_append.sh` (round-60/59 lineage) with the round-61 base
`9f07731a` instead of the script's baked-in `97cdc122` (round-59 base): `git archive <base> corpus`,
non-corpus used-by targets re-derived from the base registry, the four rows inserted after the last
registry row, then `sources-census.sh validate --file <mirror>/corpus/SOURCES.md`.

- Without the used-by entry present: **exit 1**, 4 × E11 `missing used-by corpus/knowledge/response-header-expectations.md` (one per new row) and 16 × W04. The E11 is real at my run time: `ls` on `corpus/knowledge/response-header-expectations.md` returned absent twice in this run (before and after the report draft); ScribeC2Entry had not written it.
- With a clearly-labelled scratch stub at that path (census E11 resolution only; not an admitted entry): **exit 0**, 16 × W04, no E-findings, no W01–W03. W04 set = the 15 base warnings + `S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes` (the S088 duplicate the contract anticipates). Telegram from the contract ("census stays exit 0") is therefore reproduced once the entry lands, and my four rows add no other finding: the registry diff is exactly +4 lines (`registry-diff.txt`).

Artifacts: `census-exit1.txt`, `census-exit1-stdout.txt`, `census-stub-exit0-stdout.txt`,
`registry-diff.txt`, `base-SOURCES.md`, `rows-append.md`, `quote-check.txt`, `rows.md` — all under
`.ufo/waves/round-61/w1/ScribeC2Rows.files/`.

## Findings (verbatim contract/asset conflicts)

1. Contract § C2 S430 line reads `https://www.rfc-editor.org/rfc/rfc6790`… before naming the canonical
   `https://www.rfc-editor.org/rfc/rfc6797.html`. rfc6790 is not the HSTS RFC; the row uses 6797, which
   is what was fetched and retained.
2. Contract § C2 says "W3C CSP Level 3 REC row". The retained body of `https://www.w3.org/TR/CSP3/`
   (fetched 2026-10-27T09:14:55Z) declares itself a **Working Draft** — `This version:
   https://www.w3.org/TR/2026/WD-CSP3-20261027/`, `27 October 2026` — and its Status section says
   "published by the Web Application Security Working Group as a Working Draft using the
   Recommendation track". The row records Working Draft; tier A is kept on authority, not on REC status.
3. `.ufo/waves/round-61/validate_append.sh` is a byte-copy of the round-60 script: banner "validate-append
   round-60 C7", `BASE=97cdc122…` (round-59 base), default receipt
   `.ufo/waves/round-60/controls/validate-append.txt`, and it writes a receipt. I did not execute it as-is;
   I replicated its mirror logic with the round-61 base and wrote no receipt (seats do not commit).
4. S432's quote is a clause, not a sentence: WHATWG wraps every header name in `<code>`, so no full
   sentence of §3.6 is a single text node, and the value ABNF (`X-Content-Type-Options = "nosniff" ;
   case-insensitive`) is itself split across four nodes. The row's teaches cell states the value rule; the
   Gate quote grounds only that the value ABNF sentence exists. A wave-2 reviewer should treat this as the
   weakest of the four.
5. S431's quote begins at "HTTP response header field" for the same reason (the header name is a `<code>`
   element inside the sentence). The span is still the remainder of one sentence and one text node.

## Unrun / unverified

- ScoutC2Sources's report was not present in `w1/` when this seat finished; the anchors above are
  self-located in the retained bodies (heading scan + node index in `quote-check.txt`), not copied from
  that report. If the scout's anchors disagree, the L1 should reconcile before the lesson is assembled.
- Not run: the entry draft, the manifest, capture, counters, any scoring. An after-state was not scored.
- Nothing installed; tools used were `curl`, `git` (read-only), `gawk`, `bash`, `python3` stdlib.

## Touched surfaces

- Written: `.ufo/waves/round-61/w1/ScribeC2Rows.md`, `.ufo/waves/round-61/w1/ScribeC2Rows.files/` (7 files).
- Not written: `corpus/SOURCES.md`, `corpus/knowledge/`, any wave receipt, any counter, any jj/git state.
  Scratch `/fast/scratch/hyaku/kake-r61/ScribeC2Rows/` was deleted after the cited artifacts were copied.

VERDICT: Four tier-A `spec` rows and Gate lines drafted, quotes machine-verified against the sha-matched retained bodies, mirror census reproduces exit 1 (E11, entry pending) and exit 0 with the entry path present; two contract statements (rfc6790 URL typo, "REC" for a Working Draft) are reported verbatim and the rows record the observed state.
