# PairS028StaticCanonicalPrefl: S028 × static-canonical-preflight (round 26, C1 freshness)

Milestone: r26-recheck-build · Axis: freshness · Seat: knowledge pair (leaf, no delegation)

## Result

6 statements attributed to S028: 3 explicit citations, 3 implicit reliance. HOLD 6 · STALE 0 · UNVERIFIABLE 0. No correction is required, so no block was appended and the entry was not edited.

## Judged bytes

- Knowledge entry: `corpus/knowledge/static-canonical-preflight.md`, 180 lines, sha256 `192eac303fa3ba8a2aab9d545fe6b0627f3a174dff1b54472e1bab2f771fdaf7`.
- S028 raw (`fetched/S028-1.raw.gz`, decompressed): 502,941 bytes, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`. This equals the `manifest.json` S028 row and the `population.json` S028 row (fetchedAt `2026-10-21T15:10:49.556871+00:00`, HTTP 200, `text/plain;charset=utf-8`).
- S028 text view (`fetched/text/S028-1.txt`): 457,337 bytes, sha256 `93a20ab9e35d1a59d3d370ed9fc89d2b4a62c45a4a7d5560218bc532c2757853`. It is a single line; `col N` is the grep character offset into that line.

## Statement verdicts

| # | file:line | Attribution | Statement (abridged) | Verdict | Correction |
|---|---|---|---|---|---|
| 1 | static-canonical-preflight.md:1 | explicit cite | source row `S028 RFC 9110 sections 4.2.1-4.2.2 …/rfc9110.txt` | HOLD | none |
| 2 | static-canonical-preflight.md:2 | explicit date | `verified-at … 2026-10-21 (S028-S029)` | HOLD | none |
| 3 | static-canonical-preflight.md:80-81 | implicit; basis at :83-85 | a `//` reference with empty authority is rejected | HOLD (S028 clause) | none |
| 4 | static-canonical-preflight.md:83-85 | explicit cite `(S028)` at :85 | RFC 9110 §§4.2.1–4.2.2 require a recipient to reject an http(s) URI with an empty host as invalid | HOLD | none |
| 5 | static-canonical-preflight.md:85-86 | implicit contrast | Python `urljoin` silently inherits the base host, set against that requirement | HOLD (S028 clause only) | none |
| 6 | static-canonical-preflight.md:86-88 | implicit | "rejection is the conservative policy" | HOLD (S028 clause only) | none |

## Evidence

Quotes are verbatim from `fetched/text/S028-1.txt`, line 1.

**1 (:1).** Quote: "4.2.1. http URI Scheme 4.2.2. https URI Scheme 4.2.3. http(s) Normalization and Comparison" (table of contents, col 3319). Body headings: §4.2.1 at col 44184; the §4.2.2 heading follows the §4.2.1 requirement. Both section numbers and titles match the citation.

**2 (:2).** Quote: "Category: Standards Track June 2022 ISSN: 2070-1721" (RFC header, col 230). Date anchor: manifest fetchedAt 2026-10-21T15:10:49Z, the same day as the verified-at date. Precision note, not a correction: "documentation opened this round" is a relative phrase; the dated anchor carries the claim.

**3 (:80-81).** Quote: "A recipient that processes such a URI reference MUST reject it as invalid." (§4.2.1 requirement at col 44913; same sentence in §4.2.2 at col 46271). The entry links the reference's empty authority to this requirement at :83–85. The codes `canonical_url_invalid` / `base_url_invalid` describe local behavior, not S028 claims, and were not run (outside this item's scope).

**4 (:83-85).** Quotes: §4.2.1: "MUST NOT generate an "http" URI with an empty host identifier. A recipient that processes such a URI reference MUST reject it as invalid." (col 44913). §4.2.2: "MUST NOT generate an "https" URI with an empty host identifier. A recipient that processes such a URI reference MUST reject it as invalid." (col 46271). The MUST and the entry's "require" match. The paraphrase drops the RFC condition "that processes such a URI reference". No statement in the entry depends on the dropped condition, because the validator processes every reference it rejects. Precision note, not STALE.

**5 (:85-86).** Quote: "A recipient that processes such a URI reference MUST reject it as invalid." The S028 requirement the sentence contrasts with is stated correctly. The `urljoin` behavior and the w2/Attack05 receipt are not S028 claims and are not judged here (S027 pair; local receipt).

**6 (:86-88).** Quote: as in 5. Calling rejection "the conservative policy" is consistent with S028, which makes rejection a MUST for an http(s) URI reference with an empty host. The validator also rejects `//` references under any base, which is stricter than S028 requires; that extra strictness is the local policy. The WHATWG "slash-skipping" clause (:87) is uncited in the entry: no source row in its header covers WHATWG URL parsing, and S030/S031 cover HTML syntax and parsing. Not judged.

## Superseded-anchor check

- RFC 9110 version: STD 97, Internet Standard, June 2022 (retained header). The RFC Editor info page, read today, shows "Internet Standard" with no Obsoleted-by or Updated-by banner. Its metadata timestamp is 2026-10-18T22:10:11Z.
- Errata index (`errata.rfc-editor.org/search/?rfc_number=9110`, read today): verified 7138, 7306, 7419, 7105, 7109, 8268; reported 9162, 9164; rejected 7107, 7599, 7870, 8138, 8459, 7530. A grep of the full index finds no erratum citing §4.1–§4.3, and "empty host" and "userinfo" appear nowhere. The only §4.2.1/§4.2.2 mention is in reported erratum 9164 (type Technical, filed 2026-09-07, unverified; the reporter calls it editorial). It concerns the Appendix A collected-ABNF notation for `http-URI`/`https-URI`. No S028 statement quotes the ABNF, so it does not affect these statements.
- Dates and section numbers in the citing statements match the retained bytes.
- Conclusion: no cited version, date or anchor is superseded as observed today. A single snapshot cannot rule out supersession after its timestamp.

## Considered, not attributed to S028 (no verdict)

- :82 "RFC 3986 section 3 … (S029)": S029 row.
- :28 "an HTTP(S) target": local policy, no citation.
- :128 "each http(s) without userinfo" and :176 "absolute HTTP URLs without controls or userinfo": no citation. RFC 9110 §4.2.4 "Deprecation of userinfo in http(s) URIs" (table of contents, line 1) lies outside S028's anchor (§§4.2.1–4.2.2). Planner decision whether a row is needed.
- :159 "S033 (RFC9110 §8.3.1 and §5.6.6)" and :174 "under RFC9110": S033 row. Its population scope calls S033 distinct from S028's URI scope.
- :3 "Reopen the cited sections": generic instruction for all rows.

## Notes

- No `r20` tails exist: a grep of the entry for `r20` returns no matches. The only correction tails are [r23-correction] at :140–146, and neither cites S028. The Round 23 and Round 24 sections (:96–180) do not cite S028.
- Cross-file: the population `usedBy` for S028 also lists `corpus/lessons/round-22.md`. That file is outside this pair and needs its own seat.

## Tooling and boundaries

- Installed or upgraded: none. Read-only tools only: read, grep, and bash checksums (`zcat`, `sha256sum`, `wc`).
- Public documentation GETs, not retained: `https://www.rfc-editor.org/info/rfc9110` and `https://www.rfc-editor.org/errata_search.php?rfc=9110` (redirected to the errata index above).
- Wrote only this report. No corpus, fleet, lane-Git or sibling file touched. No build, test or lint run. No round-24 material read or rerun.

```json
{"pair":"S028xstatic-canonical-preflight","statements":6,"hold":6,"stale":0,"corrections":[]}
```
