# Row S025 — freshness recheck (round 26, C1)

```json
{"id":"S025","verdict":"HOLD","fetchIndex":1,"quote":"The template contents of a template element are not children of the element itself.","anchorObserved":"§4.12.3 The template element — template contents paragraph after the shadowroot* content-attribute paragraphs; text view S025-1.txt line 1 at offset 62596; raw <p> at byte 211509 under <h4 id=the-template-element> (secno 4.12.3)","reason":"The re-fetched Living Standard (Last-Modified Tue, 20 Oct 2026 12:58:32 GMT, fetched 2026-10-21) keeps section 4.12.3 at the same number and carries the template-contents paragraph verbatim; the section's template content model is still Nothing and the contents remain a DocumentFragment owned by the inert template-contents owner document with null browsing context, so links written inside template contents sit outside the document tree and cannot supply a document-head canonical. Scope, anchor and teaches hold with no drift, and the 90d cadence remains appropriate for a living document.","correction":null}
```

## Caveats (8)

1. Fetch provenance: manifest.json row S025 index 1, status 200, bytes 276128, sha256 5854951bbabbdca6b5ea365edd1e2f14e342bc51e77353469d21e46f859abe43, fetchedAt 2026-10-21T15:10:47Z; Last-Modified 2026-10-20 12:58:32 GMT and the page banner "Last Updated 20 October 2026" equal the row's access date.
2. Living Standard, no commit pin: this recheck tests content drift at a moving URL; today's revision is the 2026-10-20 generation, so the anchor and content hold and no version re-pin is needed.
3. Quote sits at text-view line 1 offset 62596; raw HTML wraps the same sentence in inline `<a>`/`<code>` markup (raw byte 211509), so a bare-sentence substring search of the raw bytes fails by construction.
4. The second teaches clause ("do not supply document-head canonical links") is entailed, not literally stated on this page: template contents are a separate DocumentFragment whose owner document is an inert document with null browsing context; canonical-keyword semantics are S023's row.
5. The sentence cross-links syntax.html#template-syntax; that page was not fetched this round, but the statement itself is present verbatim in the retained S025 bytes.
6. Same-section corroboration: content model "Nothing (for clarification, see example)"; "Each template element has an associated DocumentFragment object that is its template contents"; inert-owner-document note "they aren't in a browsing context and thus remain inert".
7. Consistency: corpus/SOURCES.md:33 anchor/scope/teaches unchanged; corpus/lessons/round-22.md quotes the same sentence; corpus/knowledge/static-canonical-preflight.md:144 relies on it with the static-bytes-only caveat, which this source does not contradict.
8. No tools installed or updated; no host changes; only wave-retained public GET bytes and corpus reads used; no browser, property probe, account, or credential use.
