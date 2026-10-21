# Reopen S025 — WHATWG template element

## Verdict

The round-22 Gate’s S025 quote and location are correct. The registered 2026-10-20 access date is consistent with the current Living Standard’s displayed update date, but it is a date anchor rather than an immutable version pin. Tier A is appropriate for S025’s stated, narrow tree-separation scope. Its only listed `used-by` path exists and cites S025. The static canonical knowledge entry stays within its declared static-only scope, but it repeats the template boundary without citing S025 in its source metadata; the broader “cannot supply” wording should be explicitly scoped to the static input tree.

## Findings

### P2 — Static canonical entry omits the S025 citation

- **Impacted claim / axis:** Freshness and source traceability for `corpus/knowledge/static-canonical-preflight.md:72`, “template descendants cannot supply a document-head canonical.” The entry’s `source:` metadata names S020, S021, S026, S027, S028, and S029, but not S025; the knowledge file contains no literal `S025` citation. The source row’s listed `used-by` path is therefore accurate as a direct-citation list, but does not record this uncited reuse.
- **Exact check:** `grep` for `S025` in `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md`.
- **Exact observed output:** `No matches found`.
- **Supporting observed text:** `corpus/knowledge/static-canonical-preflight.md:1` lists its sources without S025; line 72 states: `text and template descendants cannot supply a document-head canonical.`
- **Smallest fix:** Add S025 to the entry’s `source:` metadata and cite it on the template-boundary sentence; add the knowledge path to S025’s `used-by` field if it is intended as a direct citation.

### P3 — Qualify the canonical-link conclusion to static input

- **Impacted claim / axis:** Freshness / scope of the S025 `teaches` clause (“…do not supply document-head canonical links”) and the sentence at `static-canonical-preflight.md:72`. In this knowledge entry’s declared static-audit scope, the conclusion is sound: the entry says it does not execute JavaScript and evaluates serialized static HTML. Read as an unconditional runtime rule, however, “cannot supply” is broader than the template-tree distinction alone.
- **Exact check:** `read` of the live section’s downloaded response at `/tmp/kake-r23-ReopenHTMLTemplate-NgLq/scripting.html:1550-1610`.
- **Exact observed output:** At line 1553 the standard says, “The template contents of a template element are not children of the element itself.” Lines 1582–1585 explain that a template’s `p` is a child of the `DocumentFragment` returned by `.content`; lines 1571–1579 show a script cloning that fragment and appending it to the document body.
- **Smallest fix:** State “In the static parsed input tree, template descendants cannot supply a document-head canonical” and cite S025. Do not present this static-audit rule as a guarantee about later script-driven DOM changes.

## Checked and held

| Field | Verdict | Evidence |
|---|---|---|
| Exact quote location (≤25 words) | **AGREE** | Live GET of `https://html.spec.whatwg.org/multipage/scripting.html#the-template-element` returned HTTP 200. The response’s table of contents and heading identify §4.12.3, “The template element”; the quoted sentence is in its template-contents paragraph. The quote is 14 words and matches the Gate exactly: “The template contents of a template element are not children of the element itself.” |
| Access date / version | **AGREE on date; PARTIAL on version** | `SOURCES.md` records “Living Standard accessed 2026-10-20”; round-22.md dates the source opening 2026-10-20 and explicitly says Living Standard citations are date-anchored, not immutable revision pins. The re-opened page displays `Living Standard — Last Updated 20 October 2026`. No immutable revision identifier is recorded or exposed by this check. |
| Tier and scope | **AGREE, with the row’s scope retained** | The row is `spec | A` and its stated scope is “Template contents are separate from document children.” `SOURCES.md` says tiers are scoped to each row’s topic, and round-22.md calls these tier-A scoped primary sources. WHATWG is the primary HTML standard; this does not make the row a global claim about runtime behavior. |
| Listed `used-by` paths | **AGREE for the listed path** | The only listed path is `corpus/lessons/round-22.md`. `test -f /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md && printf 'exists\\n'` produced `exists`. The file’s S025 row contains the same URL and quote at line 48. No other path is listed. The static canonical entry has a related assertion but does not cite S025, as noted under P2. |
| Overclaim in static canonical knowledge | **DISAGREE with a universal reading; AGREE within its stated static scope** | Lines 8–9 limit the entry to publisher-side static-file validation, not browser crawling or canonical selection; lines 90–93 say no browser or JavaScript execution is involved. Thus the static-tree claim is supported by S025’s separate `DocumentFragment` model. The source does not establish an unconditional runtime prohibition: §4.12.3 itself shows template content being cloned and inserted by script. |

**Live retrieval evidence:** The exact HEAD command was `curl -sSIL --max-time 60 -o /dev/null -w 'http_code=%{http_code}\\nurl_effective=%{url_effective}\\n' https://html.spec.whatwg.org/multipage/scripting.html#the-template-element`; exact output was `http_code=200` and `url_effective=https://html.spec.whatwg.org/multipage/scripting.html#the-template-element`. The GET body saved under `/tmp/kake-r23-ReopenHTMLTemplate-NgLq/scripting.html` was 276,128 bytes with SHA-256 `5854951bbabbdca6b5ea365edd1e2f14e342bc51e77353469d21e46f859abe43`.

## Limits

A fetch on 2026-10-21 confirms the currently served text and its displayed 2026-10-20 update date; it cannot independently prove the historical fetch event on 2026-10-20 or recover an immutable revision pin. This was a read-only source and corpus review only; no production files were changed and no tools were installed or updated.
