## Verdict

**Agree** with S023's quote location, tier/scope, historical access-date treatment, and its sole listed `used-by` path. The live WHATWG text retrieved on 2026-10-21 matches the Gate quote. I found no S023-derived overclaim in `corpus/knowledge/static-canonical-preflight.md`; that entry does not cite S023. No correction to the historical row or Gate quote is indicated.

## Findings

- **P3 — Quote location and text: AGREE.**
  - **Exact command/surface:** `read("https://html.spec.whatwg.org/multipage/links.html#link-type-canonical")`; `read("/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md:41-47")`.
  - **Exact observed output:** Web reader metadata: `URL: https://html.spec.whatwg.org/multipage/links.html#link-type-canonical`, `Content-Type: text/html`, `Method: native`, `title: HTML Standard`. At heading `##### 4.6.8.4 Link type "*\`canonical\`*"`, the page says: “The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document.” The round-22 Gate at line 46 quotes the same words and identifies Section 4.6.8.4. The quote is 19 words, within the stated 25-word limit.
  - **Impacted claim/axis:** S023 exact anchor; freshness.
  - **Smallest fix:** None.

- **P3 — Access date/version: AGREE as historical metadata; current reopen is 2026-10-21.**
  - **Exact command/surface:** `read("/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md:25-35")`; `read("/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md:36-55")`; live URL above.
  - **Exact observed output:** S023 records `Living Standard accessed 2026-10-20` and `opened | 2026-10-20`; round-22 says `Sources opened for C1 (2026-10-20)` and “Living Standard citations are date-anchored, not immutable revision pins.” The live page read on 2026-10-21 returned `title: HTML Standard` and no fixed edition/version identifier in its reader metadata.
  - **Impacted claim/axis:** S023 access-date/version provenance; freshness.
  - **Smallest fix:** None to the historic `opened` date. Retain the date-anchored Living Standard description; this report records the new 2026-10-21 re-open without rewriting the historical observation.

- **P3 — Tier and scope: AGREE.**
  - **Exact command/surface:** `read("/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md:25-35")`; live URL above.
  - **Exact observed output:** S023 is `spec | A | HTML link-type keyword semantics` and anchors sections 4.6.8 and 4.6.8.4. The live Section 4.6.8 says “Keywords are always ASCII case-insensitive, and must be compared as such”; Section 4.6.8.4 gives the preferred-URL meaning. This primary HTML Standard material covers both claims in the row's `teaches` cell.
  - **Impacted claim/axis:** S023 authority and scope; freshness.
  - **Smallest fix:** None.

- **P3 — Used-by and knowledge overclaim: AGREE; no S023 overclaim found.**
  - **Exact command/surface:** Bash command `for f in /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md; do if test -e "$f"; then printf '%s exists\n' "$f"; else printf '%s missing\n' "$f"; fi; done`; `functions.grep` with `path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md"`, `pattern="S023"`, `case=false`, `gitignore=false`, `skip=0`; reads of the S023 registry row, Gate lines 41-57, and knowledge lines 1-30 and 67-88.
  - **Exact observed output:** `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md exists`; `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md exists`; knowledge grep: `No matches found`. The registry's only listed `used-by` path is `corpus/lessons/round-22.md`; the resolved file exists and Gate line 46 contains `S023` and its URL/quote. Gate line 55 identifies the knowledge entry's citations as `S020/S021/S026/S027`; its `source:` line separately lists S020, S021, S026, S027, S028, and S029, not S023. The knowledge text attributes preferred-IRI semantics to RFC 6596, Google processing/selection limits to Google sources, and stricter checks to local policy; it does not claim that a static declaration proves reachability, duplication, or Google selection.
  - **Impacted claim/axis:** S023 `used-by` accuracy and the knowledge entry's source-bound claims; freshness.
  - **Smallest fix:** None. Do not add the knowledge entry to S023's `used-by` unless it begins citing S023.

## Checked and held

- S023 registry row and its Gate quote in `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md`.
- Section 4.6.8 keyword semantics and Section 4.6.8.4 canonical definition at the public WHATWG URL.
- Existence and literal citation of the row's listed `used-by` path; existence and S023 non-citation of `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md`.
- This is a scoped source review, not independent admission. No files other than this report were written; no tools were installed.

## Limits

- The HTML Standard is a changing Living Standard; this read confirms the live text on 2026-10-21, not the exact historical bytes served on 2026-10-20.
- No LSP device is exposed in the available tool inventory. The path and citation checks here are literal file evidence, not LSP semantic-reference results; no exported code contract was evaluated.
- `static-canonical-preflight.md` is not a unit in the frozen `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/c1-population.json`, so this source-row review does not claim a C1 population receipt.