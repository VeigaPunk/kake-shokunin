# Redirect/rewrite rule semantics for static hosts

source: S050 (Render Docs: Redirects and Rewrites, opened 2026-10-22, tier A);
S135 (Cloudflare Pages redirects docs, opened 2026-10-24, tier A)
verified-at: 2026-10-24 (S135 fresh GET this round; S050 retained text re-read)
recheck: `node scripts/source_snapshot.py`-class re-GET of the two row URLs, or
`scripts/source_recheck.py` over a fresh recording; recheck by 2027-01-22 (90d)

Two static-host rule systems the lane's redirect/rewrite audit
(`scripts/redirect_audit.py`, round 46) models, and the semantic differences
that matter for an offline expectation audit.

## Render static sites (S050)

Rules are dashboard-defined per site. The documented decision process for an
incoming request path:

1. If a resource exists at the path, serve it — no rule is applied
   ("Render does not apply redirect or rewrite rules to a path if a resource
   exists at that path").
2. Otherwise the first matching rule, from the top of the list, decides
   ("Apply the first matching rule (starting from the top of the list)").
3. Otherwise the site returns 404.

Redirect sends the browser to the destination (the doc's table names a 301
Moved Permanently response); rewrite serves the destination's content at the
original path without any browser-visible change. Source must be a path (not
a full URL); destination may be a path or a full URL. A terminal `*` matches
any string from that position (`/*` matches all paths) and expands in the
destination; `:name` placeholders capture single path components and re-insert
them in the destination.

## Cloudflare Pages (S135)

Rules live in a plain-text `_redirects` file in the static asset directory.
Differences that change audit outcomes:

- "If there are multiple redirects for the same source path, the top-most
  redirect is applied" — first match wins, same as Render.
- "Redirects are always followed, regardless of whether or not an asset
  matches the incoming request" — the opposite of Render's resource
  precedence: an existing asset does NOT shadow a Cloudflare redirect rule.
- Status codes 301, 302, 303, 307, 308 are supported; 302 is the default when
  no status is declared. Splats (`/blog/*` → `https://blog.my.domain/:splat`)
  and `:placeholders` work as in Render.

## Audit consequence

An offline expectation audit must declare which precedence semantics it
audits: the manifest field `resourcePrecedence` (true = Render, false =
Cloudflare Pages) and `defaultStatus` (301 vs 302) carry that declaration.
Judging a Render-shaped rules file under Cloudflare precedence (or vice
versa) silently flips every shadowed-rule outcome. Nothing here is a live
serving claim: the audit reads a local manifest of rules, resources and
independently authored expectations, and reports decided-vs-expected
mismatches (see `scripts/redirect_audit.py` docstring for the v1 contract).
