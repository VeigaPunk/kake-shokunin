# ExecIndependentOracle — libxml2 as an oracle for round-40 C1 (seed 40001)
Built: materialised the frozen counter's 30 witnesses with `random.Random(40001)` and asked `/usr/bin/xmllint` for well-formedness and sitemaps.org-XSD validity per file. No control tool built, no `c1_count.py` run (this seat is the oracle, not a scored control), so counter results are N/A.
Harness `/fast/scratch/hyaku/kake-r40w1/ExecIndependentOracle/oracle.py` sha256 `b77b77a443197814db226050b9d87367e0ef7f6c45961b6d5812bb90abf59480`; `derived_run.py` sha256 `50a0531d87387fcdfa472d452a5ce3ee7169cf7ee3d13480b82b3cc070cc0daf`; `derived_urlset.xsd` sha256 `cc0ca3494fc30f5911fda72e43e82d0ac1ec47d20c9147d0d356fa34c41ec5c0`; `oracle.json` sha256 `81c7eba5e2f57bf6e2b6ee672689b0e1c2e7f4e4af7f259d6b9e8a025bfdb98b`.
Commands: `timeout 300 python3 -B oracle.py` exit 0; `timeout 600 python3 -B derived_run.py` exit 0; `sha256sum -c .ufo/waves/round-39/verification/realrun/inputs.sha256` exit 0 (7 OK). Env: xmllint sha256 `1bd8970f25d14ecaa8982e1a6c3904add9a00e58dc3bc82fc4f55d5187e7d8f1`, libxml 21504-GITv2.15.4; retained `sitemap.xsd` `fbec77e8…` and `siteindex.xsd` `68d166ae…`, both equal round-39 `sources/SHA256SUMS`. No installs.

## Per-witness table (contract = counter expect; A=agree, A*=vacuous agree, C=contradict, B=oracle-blind, S=oracle-stricter)
| witness | contract outcome | WF | XSD | agree? |
|---|---|---|---|---|
| E1 | findings: xml_malformed | Y | Y | C |
| E2 | findings: xml_malformed | Y | Y | C |
| E3 | findings: xml_malformed | N | N | A |
| E4 | findings: xml_malformed | N | N | A |
| E5 | findings: xml_malformed | Y | Y | C |
| E6 | clean | Y | Y | A* |
| E7 | clean | Y | Y | A* |
| E8 | findings: encoding_invalid | Y | Y | B |
| E9 | findings: encoding_invalid | Y | Y | B |
| U1 | findings: loc_not_absolute | Y | Y | B |
| U2 | findings: loc_not_absolute | Y | Y | B |
| U3 | findings: loc_not_absolute | Y | Y | B |
| U4 | findings: loc_not_absolute | Y | Y | B |
| U5 | findings: loc_not_absolute | Y | Y | B |
| U6 | findings: loc_not_absolute | Y | Y (siteindex) | B |
| U7 | error: check_invalid | Y | Y | B |
| U8 | error: check_invalid | Y | Y | B |
| U9 | error: check_invalid | Y | Y | B |
| U10 | error: check_invalid | Y | Y | B |
| U11 | clean | Y | Y | A* |
| U12 | clean | Y | Y | A* |
| U13 | clean | Y | N | S |
| R1 | check_invalid, check_invalid | Y | Y | B |
| R2 | check_invalid, check_invalid | Y | Y | B |
| R3 | check_invalid, check_invalid | Y | Y | B |
| R4 | check_invalid, check_invalid | Y | Y | B |
| R5 | clean, check_invalid, check_invalid | Y | Y | B |
| R6 | check_invalid, clean | Y | Y | B |
| R7 | check_invalid, clean | Y | Y | B |
| R8 | check_invalid, clean | Y | Y | B |

Tally: A 2, A* 4 (6 agreements, 4 vacuous), C 3, B 20, S 1. E: 4 agree / 3 contradict / 2 blind. U: 2 vacuous / 10 blind / 1 stricter / 0 contradict. R: 8 blind (manifest-level).
Real-run (stock XSD, contract = r39 reference receipt, inputs hash-verified): rfc-editor clean Y/Y A; mdn clean Y/Y A; ruby-lang clean Y/Y A; fsf loc_out_of_scope Y/Y B (URL rule); postgresql clean Y/N S; nodejs loc_out_of_scope Y/N S.

## Five-line summary — what an oracle-backed measured claim could count
1. Well-formedness: only 2 of 5 `xml_malformed` witnesses (E3, E4 — the two with no XML declaration) are independently reproduced; E1/E2/E5 are well-formed to libxml2, which re-decodes them as UTF-16 (warning `Encoding 'UTF-8' doesn't match auto-detected 'UTF-16LE'`), so a WF claim can count at most 2/5 unless the oracle is pinned to a strict-UTF-8 reading.
2. Encoding: libxml2 cannot adjudicate sentence 6 at all — it accepts E8/E9 (`encoding_invalid` per contract) and re-decodes E1/E2/E5; the UTF-8-only rule is measurable only by an explicit decode (`iconv -f UTF-8`: E1–E7 decode, E8 and E9 fail).
3. Core XSD on real-run inputs: the stock schema validates 4/6; postgresql and nodejs fail only on the two declared lane readings — 28,312/29,600 postgresql entries are ordered `loc,priority,lastmod` (sentence 18) and nodejs carries `xhtml:link` under `processContents="strict"` (sentence 14).
4. With the derived order-insensitive + lax-wildcard schema all four urlset real-run files validate and U13 turns valid, so "core content is schema-valid" is countable only against a derived schema; that run adds no evidence for any E/U value rule.
5. URL form (class U): zero libxml2 leverage — `xsd:anyURI` collapses XML whitespace and has no absoluteness test, so U1–U6 validate; both independent parsers tried (Python `urlsplit`, Node WHATWG `URL`) strip tab/CR/LF, i.e. agree with each other and against the contract, so U claims need an RFC 3986 absolute-URI oracle, not an XML one.

## Findings
- `kake-shokunin/.ufo/waves/round-39/sources/sitemap.xsd:35-39` — tUrl is a sequence `loc, lastmod, changefreq, priority` then a `processContents="strict"` `##other` wildcard; those two facts cause every schema failure seen here, both declared as contract readings.
- `kake-shokunin/.ufo/waves/round-39/c1-contract.md:34,38` (sentence 6 UTF-8-only, sentence 8 WF), `:47` (sentence 14 extension namespaces ignored), `:55` (sentence 18 child order not checked) — the four disagreements trace to these four sentences, not to tool bugs.
- `kake-shokunin/.ufo/waves/round-40/c1_count.py:83,91,96,102,108` — witness definitions; E1/E2/E5 differ from E3/E4 only by carrying an XML declaration, which is exactly the trigger for libxml2's UTF-16 sniff.
- `kake-shokunin/.ufo/waves/round-39/verification/realrun/reference-663e051e.json` + `resid/ReviewRealRun.md:1-20` — the real-run contract outcomes used above; the six input files match `inputs.sha256`, so the receipt applies to these bytes.

## Attacked statements
- "libxml2 agrees with the contract on the E witnesses" — **overstated**: 4/9 agree (two only on clean files), 3 contradict (E1, E2, E5), 2 blind (E8, E9).
- "libxml2 agrees with the contract on the U witnesses" — **wrong**: 0 contradictions but 10/13 blind, 1 stricter (U13) and 2 vacuous; xmllint never inspects URL form.
- "libxml2 agrees with the contract on the real-run inputs" — **holds only modulo the two declared readings**: 4/6 stock, 6/6 with order-insensitivity and lax extension namespaces (the two index files already validated).
- "xmllint can serve as an oracle for C1's predicate" — **wrong as stated**: it can count well-formedness only under a strict-UTF-8 decode, and core XSD only under a derived schema; the E and U classes as written are not oracle-checkable with libxml2.
