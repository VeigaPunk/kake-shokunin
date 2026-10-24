## Verdict

**S024: agree, with scope bounded to the WHATWG HTML Standard.** The live read of the cited section confirms the Gate quote verbatim. The row's Tier A classification and narrow first-`href` scope are supported; the separate HTML document-base algorithm explicitly specifies the first qualifying element in tree order. The recorded 2026-10-20 opening date remains a valid historical date; this read-only re-verification was performed 2026-10-21. No immutable HTML Standard revision is claimed (and the Gate explicitly says Living Standard citations are date-anchored, not revision-pinned).

## Findings

- **P3 — Adjacent WHATWG URL parser statement is not sourced by S024.**
  - **Probe:** Read `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md` (lines 1 and 80–88). Exact source metadata begins: `source: S020 RFC 6596 section 3 ...; S021 Google canonical guidance ...; S026 Python HTMLParser ...; S027 Python URL parsing ...; S028 RFC 9110 ...; S029 RFC 3986 ...` (no S024 or WHATWG URL Standard). The later text says: `Browsers' WHATWG slash-skipping would read the first path segment as the host; neither reading equals the document host, so rejection is the conservative policy.`
  - **Impacted claim/axis:** This sentence is a separate URL-parser claim and is not supported by S024's HTML `<base>` element section. The earlier statement that the local gate rejects an empty-authority base `href` is framed as local policy and cites RFC 3986/9110; it is not an S024 overclaim. No S024-dependent overclaim appears in the knowledge entry.
  - **Smallest fix:** If retaining the browser slash-parsing rationale as a sourced claim, cite the relevant WHATWG URL Standard parser rule (and register that source); do not attribute it to S024. This is outside the S024 row's claim.

## Checked and held

| Field | Verdict | Evidence |
|---|---|---|
| Exact quote and location | **AGREE** | Live GET via `read https://html.spec.whatwg.org/multipage/semantics.html#the-base-element` returned section **4.2.3 The `base` element** and the exact 15-word sentence: “If there are multiple base elements with href attributes, all but the first are ignored.” This is the multiple-`href` paragraph; the Gate's section and quote are exact and within 25 words. |
| First-in-tree-order scope | **AGREE** | Live GET via `read https://html.spec.whatwg.org/multipage/urls-and-fetching.html#document-base-urls` returned **2.4.3 Document base URLs**; its step 1 identifies “the first such base element in tree order” and returns its frozen base URL. The row's scope is accurate when read with that algorithm, not as a guarantee about arbitrary parsers or nonconforming static markup. |
| Access date/version | **AGREE as historical metadata** | `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md:32` records `Living Standard accessed 2026-10-20`, matching the 2026-10-20 opening date in the round-22 Gate. The live re-open here is 2026-10-21. The Gate at `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md:54` explicitly states that Living Standard citations are date-anchored, not immutable revision pins. The source row's 90-day recheck is not overdue. |
| Tier and stated scope | **AGREE** | The S024 row at `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md:32` marks the WHATWG HTML specification `A`, with scope “First base href in document tree order.” That is a primary normative source for the HTML document-base behavior above; the tier is scoped to that topic, not a claim of parser conformance. |
| Used-by path exists and cites S024 | **AGREE** | `test -f /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-22.md && printf 'exists\n'` produced exactly `exists`. The row's used-by path resolves to that file; its Gate source table at line 47 has the `S024` identifier, cited URL, section 4.2.3, and quote. |
| Overclaim in static-canonical-preflight knowledge | **AGREE: no overclaim from S024** | The knowledge file's `source:` field does not list S024. Lines 80–85 discuss the local rejection policy and cite S029/S028 for URI grammar and empty-host invalidity; they do not claim first-base selection. The line-87 URL-parser statement above is separate, not evidence supplied by S024. |

## Limits

- Evidence is a read-only live documentation fetch and source-text inspection; no browser behavior or parser execution was tested.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/c1-population.json` does not list S024 or `static-canonical-preflight.md` as a C1 unit, so this scoped source-row report does not manufacture a C1 receipt with a non-population unit name.
- No files other than this report were written; no tools were installed or updated.