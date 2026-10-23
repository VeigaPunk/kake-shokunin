# ConnectorSiblingOverlap — kake R41 wave 1

Axes: operability (sole axis for this seat). Read-only survey; no edits, no tools scored.

## Method
- `grep -rn "urlsplit\|urlparse" /home/vgpnk/Projects/shokunin/*-shokunin/scripts/` (exit 0; 20 urlsplit hits, all in kake-shokunin).
- Sibling lanes: kumitate-shokunin/scripts (no urlsplit), tabi-shokunin/scripts (JS `new URL` only, routing, not URL validity).
- Inspected each kake call site plus its docstring/contract for intended validity standard.

## Table: URL validity decided by urlsplit/urlparse acceptance

| file:line | what is judged | shares C1 defect? | owning lane |
|---|---|---|---|
| kake-shokunin/scripts/sitemap_audit.py:73 | `loc` and manifest `sitemapUrl` absolute http(s) URL with host | YES (the C1 target) | kake |
| kake-shokunin/scripts/robots_audit.py:520 | check `url` (page URL) absolute http(s) URL with host | NO — contract explicitly judges only scheme+host; port/userinfo/host syntax not judged | kake |
| kake-shokunin/scripts/link_preview_audit.py:151 | `og:url` / page URL absolute http(s) URL with host | NO — lane policy "absolute HTTP(S) URL with a host" (same loose standard) | kake |
| kake-shokunin/scripts/live_snapshot.py:37 | redirect target safety (http(s), host, no userinfo) | NO — safety guard, not a URL-validity claim | kake |
| kake-shokunin/scripts/receipt_replay.py:385 | redirect/final URL safety in fetch records | NO — receipt validation guard | kake |
| kake-shokunin/scripts/source_snapshot.py:80 | seed URL validity (http(s), host, no userinfo) | NO — fetch-time guard | kake |
| kake-shokunin/scripts/source_snapshot.py:171 | redirect target scheme http(s) | NO — fetch-time guard | kake |
| kake-shokunin/scripts/base_path_audit.py:376 | absolute reference parse (browser-like) | NO — browser-like/WHATWG-ish standard | kake |
| kake-shokunin/scripts/base_path_audit.py:421 | base URL scheme extraction | NO — browser-like resolution | kake |
| kake-shokunin/scripts/canonical_audit.py:482,494 | conservative HTTP(S) URL normalization | NO — stricter host/port validation via `_host_and_port` | kake |
| kake-shokunin/scripts/source_recheck.py:516-523 (no urlsplit) | check `url` absolute http(s) with host via RFC 3986 App. B regex | NO — different parser (App. B, always matches); analogous looseness, not urlsplit acceptance | kake |

## Sibling lanes
No `urlsplit`/`urlparse` URL-validity judgments in `*-shokunin/scripts/`. tabi-shokunin/scripts uses JS `new URL` for request routing (tabi lane), not RFC 3986 URI validity; kumitate-shokunin/scripts has none. None share the C1 defect.

## Out of scope note
Broader scan (timed out at 300s) also shows urlsplit/urlparse in sibling non-scripts paths: kengaku-shokunin/plans/fixtures/.../evaluators.py, kengaku plans/benchmark_spec_audit.py, kotoba-shokunin/verifiers/*.py, kagi-shokunin/corpus/release-clock.py, tabi-shokunin/corpus/evidence/w9-tabi-b91/server.py. These belong to their lanes and were not examined (outside scripts/ scope).

## Findings
- Only `sitemap_audit.py:73` shares the defect C1 repairs (RFC 3986 URI grammar vs urlsplit acceptance). All other kake urlsplit sites are either contractually loose by design (robots, link_preview) or safety/fetch guards (live_snapshot, receipt_replay, source_snapshot) or browser-like/conservative (base_path_audit, canonical_audit).
- `source_recheck.py` does not use urlsplit; its App. B regex is non-validating, so its `url` validity (lines 516-523) is comparably loose but via a different parser — worth a separate claim if desired, not C1.

## Counter results
No tools scored (read-only connector seat); no counter runs.

## Per-statement verdict
- "Other tools that judge URLs with urlsplit" list in task prompt: partially accurate — source_recheck.py does not use urlsplit (overstated); all others listed do.
- "shares the defect" for sitemap_audit: holds.
- "belong to another lane" for sibling scripts: holds (none in sibling lanes use urlsplit).