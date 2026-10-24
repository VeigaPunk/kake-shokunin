# RowS007 — freshness re-check (round 26)

```json
{"id":"S007","verdict":"HOLD","fetchIndex":1,"quote":"build_type string The process by which the GitHub Pages site will be built.","anchorObserved":"Update information about a GitHub Pages site -> Parameters for \"Update information about a GitHub Pages site\" -> Body parameters (text view line 1; the HTML-to-text view is one line)","reason":"Living unpinned docs re-fetched 2026-10-21, status 200, sha256 4f4449ba997276df8acfb9a04aad7dc31c8f95b263ef56c6c7a4aac892097ce0: build_type is still a body parameter with values legacy|workflow, cname is still defined in the Update body as string-or-null and appears in the Get 200 response example, and protected_domain_state still appears in that response example beside pending_domain_unverified_at; both named anchor sections persist under unchanged headings, so scope, anchor and teaches still hold.","correction":null}
```

## Caveat

- The page is living/unpinned: its banner now reads "API Version: 2026-03-10 (latest)" and every code sample pins `X-GitHub-Api-Version: 2026-03-10`; the row pins no API version, so this is context, not drift.
- `build_type` occurs exactly twice in the retained bytes, both as Create/Update body parameters; the Get 200 response example does not list `build_type`. The row's teaches ("API exposes ... as distinct fields") survives, but a claim that GET returns `build_type` is not supported by this capture.
- `protected_domain_state` is evidenced only by the response example (2 occurrences: Get 200 and Create 201), with no prose definition.
- `cname`'s "string or null" definition sits in the Update body parameters; the Get response example shows only a plain string.
- used-by `corpus/knowledge/ghp-custom-domain.md:25-26` attributes to the "Get a Pages site response schema" that `build_type` is "legacy, workflow, or null"; today's bytes show no `build_type` in the Get response example and say "Can be one of: legacy, workflow" with no null. Flagged for L1 / the knowledge seat; I edited nothing.
- No tools installed or updated.
