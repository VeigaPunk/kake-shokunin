# Round 40 W1 — ReviewWitnessContract: the 30 witnesses of `c1_count.py` vs the round-39 contract

Scope: sentence-by-sentence check of every witness expectation in `.ufo/waves/round-40/c1_count.py::witnesses()`
against `.ufo/waves/round-39/c1-contract.md` (rule of record) and the Round-40 declaration
(SCORECARD.md "Round 40 — C1 declared"). No edits to contract, axes, routes, or judgment; recommendation only.

## Method (commands, exit 0 unless noted)
- Read `c1_count.py` (292 ln), `c1-contract.md`, SCORECARD `:2548-2623`, `/fast/scratch/hyaku/kake-r40/shared/ref_fix.diff` (read-only).
- Empirical cross-check (fixed seed 424242): materialized all 30 witnesses in my sandbox, ran the base tool
  (`git show f171c58b…:scripts/sitemap_audit.py`; identical to tip `f043c72…` tool, sha256 `6d86c8ce…`)
  and the reference repair (`shared/ref_fix.py`) under `python3 -B`, judged with the counter's own `judge()`.
- Result: base 10/30 (E 4/9, U 3/13, R 3/8) — exactly the declaration's Before receipt; ref 30/30.
  Base fails E1–E5 (clean instead of `xml_malformed`), U1–U10 (clean instead of `loc_not_absolute`/`check_invalid`),
  R1–R5 (repeat of an earlier invalid check's id judged `clean`). Polarities E6–E9, U11–U13, R6–R8 pass at base.
  Witnesses are satisfiable and bite exactly on the three declared classes.

## 30-row table
Sentences cite c1-contract.md. "S110/S102" = sources via the declaration's readings.

| W | Deciding sentence(s) | Verdict | Reason |
|---|---|---|---|
| E1 | 6, 7(antecedent false), 8, 33, 34 | agree | UTF-16LE bytes decode as UTF-8 (NULs valid, 6 holds); NUL-interleaved text is not the lexical XML declaration so 7 is silent; U+0000 is not an XML Char → 8 `xml_malformed`, exit 1. |
| E2 | 6, 7(false), 8, 34 | agree | Same as E1, big-endian. |
| E3 | 7(no declaration), 8, 34 | agree | No declaration present at all; NULs → 8 `xml_malformed`. |
| E4 | 7, 8, 34 | agree | Same as E3, big-endian. |
| E5 | 6, 7(false), 8, 34 | agree | Intended `encoding="UTF-16"` is NUL-interleaved → no lexical XML declaration → 7 cannot fire; 8 gives `xml_malformed`. See finding F1 (the one unstated reading). |
| E6 | 6, 8, 10, 11, 15, 21–25, 34 | agree | Plain UTF-8 valid urlset, loc in scope (`/d/pXXX` under `/d/`) → clean. |
| E7 | 6 (UTF-8 BOM allowed), then E6 chain | agree | Only the UTF-8 BOM is allowed and this is it → clean. |
| E8 | 6 (failure → `encoding_invalid`, no other finding), 34 | agree | `FF FE` is not a UTF-8 BOM; bytes fail UTF-8 decode → `encoding_invalid`. |
| E9 | 6, 34 | agree | BOM-less UTF-16LE of non-ASCII text: `E9 00` is invalid UTF-8 → `encoding_invalid`. |
| U1 | 21 (interior TAB kept), 22 (+S102 RFC-3986 via declaration), 34 | agree | TAB between `a` and `b` survives the sentence-21 strip; not in the URI grammar → not absolute as written → `loc_not_absolute`. |
| U2 | 21, 22, 34 | agree | Same with interior LF. |
| U3 | 8 (parsing resolves refs), 21, 22, 34 | agree | `&#13;` parses to interior U+000D (raw CR would be EOL-normalized; a reference survives) → not absolute. Declaration's partial-repair list explicitly covers "raw characters but not character references". |
| U4 | 21, 22 | agree | TAB inside the authority; urlsplit would silently strip it — judged as written → `loc_not_absolute`. |
| U5 | 22 | agree | LF after the scheme colon → not a URI as written → `loc_not_absolute`. |
| U6 | 22 (both file kinds), 27 (relaxes scope only) | agree | sitemapindex does not relax absoluteness → `loc_not_absolute`. |
| U7 | 4, 33, 34 | agree | `sitemapUrl` carrying TAB is not an absolute http/https URL → `check_invalid`, exit 2, string id echoed. |
| U8 | 4, 33, 34 | agree | Same with CR in `sitemapUrl`. |
| U9 | 4, 33, 34 | agree | Leading space → not absolute as written → `check_invalid`. |
| U10 | 4, 33, 34 | agree | Leading C0 U+0001 → `check_invalid`. |
| U11 | 21 (strip), 22, 25, 34 | agree | Leading TAB and trailing CR/LF are exactly the stripped set; remainder is `good`, in scope → clean. Declaration refines its blanket TAB/CR/LF phrasing with "after the sentence-21 strip". |
| U12 | 21, 22, 26 (no percent-decoding), 25 | agree | `%09`/`%0A` are literal path characters; urlsplit does not alter them → clean. |
| U13 | 14 (foreign namespace ignored), 15, 25 | agree | `x:note` in `urn:…` is ignored wholesale, its TAB/LF content with it → clean. |
| R1 | 4 (c1 lacks `file`; c2 repeats string id `i1`), 33, 34 | agree | Both `check_invalid`; ids echoed; empty findings; exit 2. Declaration: an invalid check still has an id when that member is a string. |
| R2 | 4 (c1 lacks `sitemapUrl`; c2 repeats) | agree | Both `check_invalid`. |
| R3 | 4 (c1 non-string `file`; c2 repeats) | agree | Both `check_invalid`; c1 echoes id `i1` (string) per 33. |
| R4 | 4 (c1 non-string `sitemapUrl`; c2 repeats) | agree | Both `check_invalid`. |
| R5 | 4 (c2 lacks `file`; c3 repeats `i2`), 34 | agree | c1 clean, c2/c3 `check_invalid`, exit 2 (any error). |
| R6 | 4 (c1 non-string id; c2 `str(num)` ≠ integer value), 4+33 (null echo), 34 | agree | Integer id → `check_invalid` with output id `null` (composition, F2); the string `str(num)` is a different value, repeats nothing → clean. Declaration: "an integer id followed by its string stays clean". |
| R7 | 4 (c1 not an object → no members, no id), 33, 34 | agree | Non-object check → `check_invalid`, id `null`; c2 cannot repeat an id the earlier check never had → clean. Declaration: "a non-object check stays clean". |
| R8 | 4 (c1 lacks `file`; c2 id differs by case) | agree | Id comparison is exact string identity; `Q…` ≠ `q…` → c2 clean. Declaration: "a case-different id stays clean". |

All 30: **agree** — every expected outcome is what the contract decides; none is wrong.

## Findings
- **F1 (minor, unstated reading — E1–E5).** The `xml_malformed` outcome requires sentence 7's antecedent
  ("If the XML declaration has an encoding pseudo-attribute") to be read lexically on the UTF-8-decoded
  stream: NUL-interleaved bytes do not form the token `<?xml`, so no XML declaration exists and 7 is silent;
  8 fires. The contract supports only this reading (its sources are the XML lexical rules), but neither the
  contract nor the declaration states why 7 cannot fire on E5, whose bytes intend `encoding="UTF-16"`. A tool
  that locates the pseudo-attribute NUL-tolerantly, or sniffs UTF-16 before decoding, fails E1–E5. The
  witnesses force the lexical reading; that is defensible but is a reading the declaration does not spell out.
- **F2 (minor, composition — R6).** Expected output `"id": null` for the integer-id check composes sentence 4
  (only strings are ids) with sentence 33 (`<id or null>`); the declaration covers the repeat direction
  ("integer id followed by its string stays clean") but not the echo direction. Derivable; agree.
- **F3 (saturation gap, not a disagreement).** No witness repeats the id of an earlier **valid** check.
  Literal sentence 4 invalidates any repeat; the declaration's phrasing ("earlier checks that were invalid")
  is narrower. Both readings pass all 30 witnesses, so the counter cannot distinguish them: a repair that
  only handles repeat-of-invalid and drops repeat-of-valid still meets the predicate. Not fixable without
  editing the frozen counter; flagging for the L1.
- **F4 (immaterial judge note).** `norm()` compares findings as a sorted set; every witness expectation here
  is a single-finding (or empty) list, so no witness exercises multi-finding entries or order — no hiding place
  for a contract violation in this witness set.

## Attacked statements (declaration, per class)
- E ("UTF-16 without a BOM → `xml_malformed`; BOM → `encoding_invalid`"): **holds** — E1–E9 all contract-decided; ref 9/9.
- U ("TAB/CR/LF after the sentence-21 strip, or leading C0/space on `sitemapUrl` → `loc_not_absolute`/`check_invalid`; escapes, foreign-namespace TAB, and stripped values stay clean"): **holds** — U1–U13 all contract-decided; ref 13/13.
- R ("repeat of the string id of an earlier invalid check → `check_invalid`; integer/string, non-object, case-different stay clean"): **holds on every witness**, with the F3 caveat that the phrasing is narrower than sentence 4's literal rule and no witness distinguishes them.
- Counter Before totals ("10 of 30, E 4/9, U 3/13, R 3/8"): **holds** — reproduced exactly at seed 424242 with tip tool == base tool (sha `6d86c8ce…`).

Tooling: no installs needed (stock python3 + git). No lane files mutated other than this report; scratch under
/fast/scratch/hyaku/kake-r40w1/ReviewWitnessContract/ cleaned. No control built, none scored; this seat is analysis-only.
