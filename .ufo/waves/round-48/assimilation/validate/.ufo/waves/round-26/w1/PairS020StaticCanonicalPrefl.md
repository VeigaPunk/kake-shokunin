# Pair S020 × static-canonical-preflight: round 26 freshness recheck

Seat: KakeR25.PairS020StaticCanonicalPrefl-6 · Milestone r26-recheck-build · Axis: freshness · Entry: `corpus/knowledge/static-canonical-preflight.md` (read tag #8B13, 178 lines) · Source: S020, RFC 6596 §3.

## Basis
- Retained bytes `fetched/S020-1.raw.gz`. Manifest row S020: fetchIndex 1; url = finalUrl `https://www.rfc-editor.org/rfc/rfc6596.html`; HTTP 200; no redirect; fetchedAt `2026-10-21T15:10:43.158633+00:00`; bytes 18428; sha256 `87a13951ce93195e9a52915e6d170eebd4c48260576b637407bb96ea8c47f5e4`. Re-derived locally: `gzip -dc` gives 18428 bytes and a matching sha256. S020 has no retry entry; `manifest-retry.json` holds S008 only.
- Quote source `fetched/text/S020-1.txt`: one line, sha256 `bd0283930f510c3a2047f95d2b988fd69ced2d8b0658e1367b9b852b2da80054`. Anchors are RFC section numbers, because the text view has no usable line numbers.
- Live supplements (not the verdict basis, read 2026-10-21): the RFC Editor info page header shows Informational with no obsoleted-by or updated-by entry; the errata search at `errata.rfc-editor.org/search/?rfc_number=6596` returns "No matching errata found."
- Static operability only (grep, not executed): `scripts/canonical_audit.py` defines `--selftest` (line 129); `.ufo/waves/round-22/matrix.py` requires `--root` (line 212).
- Coverage: `grep S020` matches lines 1–2 only. `grep r20` matches nothing, so the entry has **no r20-correction tails**. Its only correction tails are `[r23-correction]` at lines 140–146, which cite S021 and S025. Later sections (Round 23, lines 96–155; Round 24, lines 157–180) carry one S020-dependent statement (line 117). The Round 24 text was read only as entry text; no round-24 artifact or counter was opened or run.
- Tooling: nothing installed or upgraded. Used only the base `gzip`, `wc` and `sha256sum`.

## Verdicts

| # | line | statement (abridged) | verdict | verbatim quote (S020-1.txt) | anchor observed | reason |
|---|---|---|---|---|---|---|
| R1 | 1 | header: "S020 RFC 6596 section 3 https://www.rfc-editor.org/rfc/rfc6596.html" | HOLD | "3. The Canonical Link Relation The target (canonical) IRI MUST identify content that is either duplicative" | §3 heading; manifest url = finalUrl | Section, title and URL are intact. Retained bytes match the manifest sha256. |
| R2 | 2 | "verified-at: 2026-10-20 (S020-S027) … documentation opened this round" | STALE (date only; content HOLD) | "Internet Engineering Task Force (IETF) M. Ohye Request for Comments: 6596 J. Kupke Category: Informational April 2012 ISSN: 2070-1721" | RFC header block | Same RFC and version. The S020 verification date is superseded by fetchedAt 2026-10-21T15:10:43Z (fetchIndex 1). The correction below appends the newer verification. |
| R3 | 3 | "recheck: Reopen the cited sections; canonical_audit.py --selftest; round-22/matrix.py --root ." | HOLD | "3. The Canonical Link Relation The target (canonical) IRI MUST identify content" | §3 present | The cited section exists. Both commands exist and expose the named flags (static grep only; not executed, per bounds). |
| R4 | 13 | "RFC 6596 section 3 defines a preferred IRI for duplicated or superset content." | HOLD (precision note F3) | "The target (canonical) IRI MUST identify content that is either duplicative or a superset of the content at the context (referring) IRI." | §3 MUST | §3 supplies the duplicative-or-superset condition. The "preferred IRI" wording is from §1 ("specifies the preferred IRI from resources with duplicative content") and the Abstract. The teaching holds, so this is not counted as stale. |
| R5 | 14 | "A relative IRI … may be valid." | HOLD | "Specify a relative IRI (see [RFC3986], Section 4.2)." | §3, "The target (canonical) IRI MAY:" bullet 1 | Stated as MAY. |
| R6 | 14 | "… self-reference … may be valid." | HOLD | "Be self-referential (context IRI identical to target IRI)." | §3 MAY bullet 2 | Stated as MAY. |
| R7 | 14 | "… a different hostname may be valid." | HOLD | "Exist on a different hostname or domain." | §3 MAY bullet 3 | Stated as MAY. |
| R8 | 15 | "Its single-canonical guidance is not proof that a target is reachable or duplicate." | HOLD | "verification of the following is RECOMMENDED: 1. The content of the context IRI is duplicated within the content of the target (canonical) IRI." | §5 Recommendations; §3 "administrators ought to consider the following guidelines" | The one-canonical item is advisory ("ought to consider"). §5 makes verifying duplication a recommended publisher step, so a declaration is not proof. The §3 avoid-list (error codes, redirects) is also advisory, so reachability is not established either. |
| R9 | 16 | "The offline tool cannot establish either condition." | HOLD (local claim; premise from R8) | "Before adding the canonical link relation, verification of the following is RECOMMENDED" | §5 | The tool's scope is the entry's own (lines 74–78 and 90–94). S020 supplies only the premise that duplication must be verified. |
| R10 | 25 | "Cross-domain canonical is likewise not intrinsically invalid." | HOLD (S020 part; S021 attribution) | "Exist on a different hostname or domain." | §3 MAY bullet 3 | RFC 6596 supports "not intrinsically invalid" through its MAY. The word "likewise" ties the sentence to the S021 paragraph (lines 22–24), which S021 must judge. |
| R11 | 27–28 | "stricter local policy: one canonical signal" | HOLD | "Specify only one canonical link relation for a resource." | §3 guideline list | The RFC states this as a guideline. Enforcing it as a policy failure is the stricter local policy the entry names. The fragment, credential and HTTP(S) rules are local, not S020. |
| R12 | 30 | "A mismatch is policy failure, not a claim that the URL violates RFC 6596." | HOLD | "The target (canonical) IRI MUST identify content that is either duplicative or a superset of the content at the context (referring) IRI." | §3 MUST | The MUST is a content condition. A string comparison with expectedCanonical cannot test it, so a mismatch makes no RFC-violation claim. |
| R13 | 117 | "…and would change a relative canonical." (Round 23; implicit) | HOLD | "Specify a relative IRI (see [RFC3986], Section 4.2)." | §3 MAY bullet 1 | The premise that a relative canonical is a permitted target is S020's. Base precedence (S024) is outside this pair. |

## Flags: cited version, date or anchor superseded?
- **F1 (line 2, S020 date):** superseded by the 2026-10-21 re-fetch. Handled as R2 (STALE, date only).
- **F2 (line 2, "documentation opened this round"):** for S020, "this round" means round 22. Covered by the R2 correction.
- **F3 (line 13, anchor precision):** "preferred IRI" comes from §1 and the Abstract; §3 supplies the duplicative-or-superset MUST. The verdict stays HOLD. Optional append-only clarifier, not counted: `- [r26-note] The "preferred IRI" wording at line 13 comes from RFC 6596 section 1 and the Abstract; section 3 supplies the duplicative-or-superset MUST.`
- **F4 (RFC 6596 itself):** not superseded in the observed sources. Category Informational, April 2012; §3 intact; no erratum found.
- **F5 [INFERENCE, not checked on this seat]:** RFC 6596 §3 and §4 cite RFC 2616 and RFC 5988, which later RFCs replaced. No entry statement cites or depends on them.

## Scanned and not attributed to S020 (excluded)
- Lines 5–11: scope note, no S020 claim.
- Lines 18–24: S021 Google statements, including the "Absence of a declaration…" sentence.
- Lines 32–56: local input and handoff rules.
- Lines 58–63: policy table. "violates local policy" is consistent with R11 and R12, with no separate S020 claim.
- Lines 65–78: parser and URL-module boundaries (S026, S027).
- Lines 80–88: `//` empty-authority rejection, grounded in S028 and S029. S020 is silent on empty authority.
- Lines 90–94: local tool operation.
- Lines 98–111 and 121–123: HTML, WHATWG and S024/S026/S030/S031 material, plus local rules.
- Lines 125–136: local live-snapshot handoff. Lines 134–135 mention search-engine selection (S022).
- Lines 140–146: corrections (S021, S025).
- Lines 151 and 153: S030 caveat, and meta-refresh text. Line 153's "declared canonical href/base" refers to the HTML link element, not an RFC 6596 claim.
- Lines 159–180: Round 24 receipt rules (S032–S034).
- Outside this entry, not judged: `corpus/SOURCES.md:51` (reading-order note) and row S020 (line 28) also rely on S020.

## Cross-seat note
The sibling `RowS020.md` (fetchIndex 1) reaches HOLD on the same §3 text and treats the SOURCES "opened 2026-10-20" as unchanged metadata. That is consistent: F1 concerns this entry's header date, not the SOURCES row. I read it after forming the verdicts above; it changed none of them.

## Corrections (append-only)
Append as a bullet at the end of "### Corrections to earlier text in this entry", after the r23 bullets. Do not edit lines 1–2.

```
- [r26-correction] Line 2's S020 verification date is superseded: RFC 6596 was re-fetched 2026-10-21T15:10:43Z (fetchIndex 1; https://www.rfc-editor.org/rfc/rfc6596.html; HTTP 200; sha256 87a13951ce93195e9a52915e6d170eebd4c48260576b637407bb96ea8c47f5e4). In line 2, 'this round' means round 22; 2026-10-20 is the round-22 open date. Content verdicts for the S020-sourced statements at lines 1, 3, 13-16, 25, 27-30 and 117 are unchanged (HOLD) against those bytes (r26 pair S020xstatic-canonical-preflight).
```

## Machine summary
```json
{"pair":"S020xstatic-canonical-preflight","statements":13,"hold":12,"stale":1,"corrections":["- [r26-correction] Line 2's S020 verification date is superseded: RFC 6596 was re-fetched 2026-10-21T15:10:43Z (fetchIndex 1; https://www.rfc-editor.org/rfc/rfc6596.html; HTTP 200; sha256 87a13951ce93195e9a52915e6d170eebd4c48260576b637407bb96ea8c47f5e4). In line 2, 'this round' means round 22; 2026-10-20 is the round-22 open date. Content verdicts for the S020-sourced statements at lines 1, 3, 13-16, 25, 27-30 and 117 are unchanged (HOLD) against those bytes (r26 pair S020xstatic-canonical-preflight)."]}
```
