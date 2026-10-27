# ScoutSourceRegistry — round 62

## Findings

- **S432 existing row:** `corpus/SOURCES.md:178` registers WHATWG Fetch at `https://fetch.spec.whatwg.org/`, kind `spec`, tier A, status `mined`, opened `2026-10-27`, recheck `180d`, used-by `corpus/knowledge/response-header-expectations.md`. Its current scope/anchor/teaches concern the X-Content-Type-Options nosniff value rule and §3.6. Do not reject or replace it: it remains applicable primary evidence.
- **Used-by:** the current knowledge entry is already listed. A correction within the same entry changes no used-by value. No observed evidence here justifies adding/deleting a used-by path.
- **Current round evidence:** the round-62 contract states S432 was reopened at the canonical URL on 2026-10-27 and points to retained body `.ufo/waves/round-61/sources/S432.html`, §3.6 lines 6151–6154, for the substantive Content-Type/destination sentence. This substantiates correcting the knowledge entry's quote/span; it does not make the registry row invalid.
- **Permissible registry operations:** under the SOURCES rule 2 reflected in `corpus/QUALITY.md:1116`, a corrected source anchor is recorded as a *superseding registry row* rather than rewriting the old row. The precedent at `corpus/SOURCES.md:223` says immutable source/tier/scope/anchor/teaching/opened cells stay unchanged, while used-by changes are logged separately. Therefore, if adjudication establishes a genuine corrected locator/scope, append a superseding row with the supported revised anchor/scope/teaching and preserve the original S432 row; keep status mined and date/recheck facts evidence-based. Any used-by adjustment is limited to actually changed entry relationships and must be separately logged old→new. Do not overwrite S432 cells or mark it rejected.
- **This round:** make no SOURCES registry cell edits. The already registered source is the same URL and source record; the correction target is the knowledge quote, not a mistaken source identity, status, or current use. The new claim's required change is the entry quote correction plus a grounded QUALITY criterion; neither warrants changing the S432 registry row absent a separately demonstrated locator correction requiring supersession.

## Evidence and commands

- `read corpus/SOURCES.md:178`: exact S432 row including all eleven cells.
- `read corpus/QUALITY.md:1115-1116`: held-source resolution and corrected-anchor superseding-row requirements.
- `read corpus/SOURCES.md:223`: precedent that immutable row cells remain unchanged and used-by changes are logged separately.
- `grep -n S432 corpus/SOURCES.md` equivalent search evidence: row at line 178, used-by points at the knowledge entry; broad literal search also found round-61 artifacts but no alternate S432 registry row.
- `contract.md:9` states the retained quote location; `S432` current row remains mined. No predicate, claim, counter, criterion or score was changed by this seat.

Confidence: high for current row/status/used-by and no-cell-change recommendation; the possibility of a formal superseding row depends on treating the §3.6 locator as a registry correction, which this evidence does not establish as necessary.