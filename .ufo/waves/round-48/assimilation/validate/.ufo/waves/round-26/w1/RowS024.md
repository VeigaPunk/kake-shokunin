# Row S024 — freshness recheck (round 26, C1)

```json
{"id":"S024","verdict":"HOLD","fetchIndex":1,"quote":"If there are multiple base elements with href attributes, all but the first are ignored.","anchorObserved":"§4.2.3 The base element, note paragraph on multiple base href (text-view char offsets 10160-10248; §4.2.3 heading at offset 8390; raw <h4 id=the-base-element><span class=secno>4.2.3</span>)","reason":"The re-fetched Living Standard (Last-Modified 20 Oct 2026 12:58:32 GMT) still carries §4.2.3 with the multiple-base-href sentence verbatim, and the same section's frozen-base-URL prose still defines the first base element with href in tree order; scope, anchor, and teaches hold with no drift, and the page's Last-Modified date equals the row's 2026-10-20 access date.","correction":null}
```

## Caveats (7)

1. Provenance: fetched/manifest.json row=S024, index=1, status 200, bytes=333092, sha256=fd9ae4b6…2db959, fetchedAt=2026-10-21T15:10:46Z; Last-Modified header 20 Oct 2026 12:58:32 GMT, content-type text/html charset=utf-8.
2. The text view is one line (96,598 bytes, 96,469 chars), so anchorObserved uses character offsets; quote is at 10160-10248 and is contiguous and word-bounded in fetched/text/S024-1.txt.
3. Fragment resolves: raw HTML offset 33390 has `<h4 id=the-base-element>` with `<span class=secno>4.2.3</span>`, so the URL fragment #the-base-element still lands on this section.
4. Sentence sits in a `<p class=note>` in the raw HTML (non-normative restatement); normative support is “There must be no more than one base element per document.” (text offset 9783) plus the frozen-base-URL definition of the first base element with an href content attribute in a document tree (raw offset 46382). The row's teaches is unchanged either way.
5. Living-standard pin: citation is date-anchored, not immutable; access date (2026-10-20) equals the current Last-Modified date, so no drift is detectable since opening. Row line checked at corpus/SOURCES.md:32.
6. corpus/lessons/round-22.md:47 already quotes the identical sentence, so no lesson text needs correction; no status/recheck/used-by cell change is warranted.
7. No tools installed or updated; no host changes; only the round-26 retained bytes and the row/lesson text were read. Remaining unknown: none; verdict is decidable from retained bytes.
