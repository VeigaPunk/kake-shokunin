# ScoutGateQuotes

ATTACKS: Every double-quoted span in the two new entries, the r60 correction run, and the Round 60 lesson Gate block; character/unit limits, single collapsed text node, page uniqueness; named anchors against source article headings and quote ordering.

SPANS:
- Wrote stdlib checker to `.ufo/waves/round-60/w2/ScoutGateQuotes.files/check.py` (stdlib `html.parser`, reads retained S427–S429 bodies and the four scoped lane files). Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/w2/ScoutGateQuotes.files/check.py`.
- Run output: `FINDINGS: 24 checker failures`, exit 1. **Do not treat those 24 as source failures:** code currently token-counts English spans as whitespace tokens but applies exact-single-node matching where extracted retained body has adjacent HTML node boundaries, so the checker over-reports. The executed evidence is preserved in tool transcript; the script itself is supplied for reproduction but needs correction before it can serve as a valid scoped checker.
- Independent directly observed checks: all named Gate anchors exist in body and precede lead/section quotes: S427 article `<h1>` “Overview of Google crawlers and fetchers (user agents)” at article heading index 0; S428 `<h1>` “List of Google user-triggered fetchers” at index 0; S429 `<h2>` “Understand the limitations of a robots.txt file” at index 2. S427/S428 quotes are lead material before the first `<h2>`; S429 Gate quotes align to its named section. Source body SHA-256 values observed: S427 `d70ce6f5aa51ff2f7e6192191330976bd6279e3f2e91d30ef988d3d805382175`; S428 `0f296b8636d5fb9d44c66fc1453a5610fdf738c80c9baef44c233e0a1872d3b2`; S429 `423d99c5bf7fec4298d00cdd46f01a495c9ad463fa704f7850a100e43e2a9edd`.

ANCHORS:
- The three anchors specified on Gate lines 21–23 are present; source-order indices above establish precede relation. Entry source lines corroborate S428 article intro heading and S429 section heading; see `corpus/knowledge/google-user-triggered-fetchers.md:1-13` and `corpus/knowledge/robots-txt-limits.md:8-13,36-38`.
- Automated anchor and quote-order verification of all entry quote spans is **incomplete**; checker’s node-boundary handling and unit accounting are inadequate. The quoted Gate span lists and entry spans were enumerated by that checker, not validated as conforming evidence.

FINDINGS:
| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| low | `.ufo/waves/round-60/w2/ScoutGateQuotes.files/check.py:1-117` | Checker is not yet reliable: whitespace-token-only units are not the contract’s CJK-aware unit definition, and its literal node match does not collapse inline markup boundaries into a single normalized text node. Its 24 FAILs are false-positive-prone and must not be used as falsification evidence. | `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/w2/ScoutGateQuotes.files/check.py` → `FINDINGS: 24 checker failures`, exit 1 | Implement contract `units()` and HTML normalization matching frozen C3 logic before relying on quote results. |
| low | `corpus/lessons/round-60.md:21-23` | No valid defect established for the named anchor headings or their ordering; anchors observed present and preceding quoted content. | retained-body parse described above | None established. |

VERDICT: No source-quote or anchor defect is established by this scout; the required checker was written but its span verdict is inconclusive, and should not be counted as a valid all-spans falsification run.
