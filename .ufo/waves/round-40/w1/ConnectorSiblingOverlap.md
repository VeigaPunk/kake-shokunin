# ConnectorSiblingOverlap — Kake R40 wave 1

Axes: operability, freshness. Scope: sibling lanes `*-shokunin` (read-only), excluding `.ufo`, venvs, live corpus.

Method (grep, text files <2MB, excluding binary): searched for `sitemap`, `urlsplit`, `UTF-16`, `BOM`, `RFC 3986`, `sitemapUrl`, `xml_malformed`, `loc_not_absolute`, `check_invalid`, `S110`/`S111`. No sibling ships a sitemap audit tool or uses kake's error vocabulary.

## Overlaps with kake C1 (S110 XML 1.0 Char no U+0000; S111 urlsplit stripping)

| path:line | relation | note |
|---|---|---|
| `kotodama-shokunin/tools/harness/r8_checks.py:79-88` | agrees | `url()` rejects any whitespace (`not any(c.isspace() for c in value)`) before `urlsplit`, matching S111's TAB/CR/LF invalidity. |
| `kagi-shokunin/corpus/release-clock.py:176,214,233,243,301,306` | conflicts | `urlsplit` consumed with no whitespace/C0 guard; S111 stripping can hide TAB/CR/LF/C0/space. |
| `kotoba-shokunin/verifiers/check_agent_definitions.py:379` | conflicts | same unguarded `urlsplit` pattern. |
| `kotoba-shokunin/verifiers/check_command_files.py:500` | conflicts | same. |
| `kotoba-shokunin/verifiers/check_plugin_manifests.py:467` | conflicts | same. |
| `chousa-shokunin/tools/quote-reopen.py:214` | conflicts | same. |
| `kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json:396,1786-1787` | duplicates | cross-lane citation to `kake-shokunin/corpus/knowledge/sitemap-orphan-audit.md`; not a contract overlap. |
| `mori-shokunin/corpus/evidence/sources-r32/S175.src:480` | agrees (weak) | generic RFC 3986 pointer in curl manpage; no XML/encoding claim. |
| `tsukuroi-shokunin/LOG.md:1167` | none | passing mention of a "sitemap note", unrelated to C1. |

## S110/S111 duplicate rows
None found in sibling lanes: no sibling SOURCES row or knowledge entry restates the XML 1.0 §2.2 `[2] Char` production or the `urlsplit` stripping quote. BOM/UTF-16 mentions in sibling corpora (e.g. `chousa-shokunin/corpus/lessons/round-27.md:225`, `kaidoku-shokunin/corpus/knowledge/*`) concern registry/BOM handling, not XML decoding; no conflict with E.

## Conclusion
No sibling tool or corpus entry duplicates or contradicts S110/S111's substance; the only concrete overlap is the shared `urllib.parse.urlsplit` primitive, where siblings that do not pre-validate whitespace inherit the S111 stripping hazard (conflicts), while `kotodama-shokunin/tools/harness/r8_checks.py` already guards it (agrees). No action required on sibling lanes; kake's C1 repair is lane-local.
"""