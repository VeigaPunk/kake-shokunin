# Round 29 — project-site base paths: sourced knowledge and an offline audit

## Claims

Declared before implementation in `SCORECARD.md` section "Round 29 — declared
claims" (commit `d18bbf3055f33a992fc9adc4b757172554ec9981`), with declaration
notes added before any after-measurement at `9e541a1d138158cd957c0e7b1a32050478c02dd0`.

- **C1, freshness, frontier.** Project-site base paths enter held knowledge as
  `corpus/knowledge/pages-base-path.md`, grounded in S040–S043 opened this
  round. Counter `.ufo/waves/round-29/c1_quote_truth.py`; before 0/4 at
  `fe1805cf`, declared after 4/4. It checks quote truth against retained
  source text (round-28 routed defect 3), not only quote shape.
- **C2, operability, capability.** `scripts/base_path_audit.py` audits built
  HTML of a project site against its declared base path. Counter
  `.ufo/waves/round-29/c2_matrix_count.py`; before 0/30 at `fe1805cf`,
  declared after 30/30 with all three constant gates rejected. It compares
  reason codes, not only ids (round-28 routed defect 3).

This round deliberately leaves the citing-set gate alone: rounds 27 and 28
both worked it, and a third round on that surface trips the session drift
sentinel.

## Gate

### Source openings

The L1 opened each primary page with one public GET (HTTP 200,
2026-10-22T10:29:37Z) through `.ufo/waves/round-29/fetch_sources.py`.
Received bodies, visible text (HTML minus script, style and comments, tags
removed, entities decoded, whitespace collapsed) and sha256 receipts are in
`.ufo/waves/round-29/sources/`. Wave-1 seat `ReviewSourcesReopen` re-opened all
four at 10:33:42Z: bodies and texts byte-identical to the receipts. Each quote
below is an exact substring of the retained text.

- S040 — https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages (redirects to …/what-is-github-pages) — accessed 2026-10-22, section Types of GitHub Pages sites, Default site location row: “Default site location http(s):/ / <owner>.github.io http(s):/ / <owner>.github.io/ <repositoryname>”
- S041 — https://jekyllrb.com/docs/github-pages/ — accessed 2026-10-22, section Project Pages: “will become available under a subpath of your user pages subdomain, such as username.github.io/project (unless a custom domain is specified)”
- S042 — https://jekyllrb.com/docs/liquid/filters/ — accessed 2026-10-22, Standard filters table, Relative URL row: “Prepend baseurl config value to the input to convert a URL path into a relative URL.”
- S043 — https://vite.dev/guide/static-deploy.html — accessed 2026-10-22, section GitHub Pages, Update Vite Config: “If you are deploying to https://<USERNAME>.github.io/<REPO>/ (eg. your repository is at https://github.com/<USERNAME>/<REPO> ), then set base to '/<REPO>/' .”

The S040 table cell keeps the spacing that tag removal leaves (`http(s):/ /`);
the live table reads `http(s)://<owner>.github.io/<repositoryname>`.

### Screened candidates (round-28 routed defect 4)

Wave-1 seat `ScreenRejectCandidates` ran an ordinary web search and requested
six secondary or community pages once each (10:34:12Z–10:35:40Z). Bodies, text
and receipts are in `.ufo/waves/round-29/sources/screened/` (C1–C6). Each quote
is an exact substring of that retained text.

- S044 (C1) — https://mademistakes.com/mastering-jekyll/site-url-baseurl/ — accessed 2026-10-22, HTTP 200 — **rejected**: stale version claim and raw baseurl concatenation advice; quote “GitHub Pages does not use the latest version of Jekyll to build sites. It is currently locke at 3.9.0” (S016 lists Jekyll 3.10.0).
- S045 (C3) — https://github.com/jekyll/jekyll/issues/332 — accessed 2026-10-22, HTTP 200 — **rejected**: a 2011 thread about the retired `user-name.github.com` host and a `base-url` key; quote “If you're not using a CNAME and hosting your Project Page on GitHub Pages it's served out of a "project-name" subfolder”.
- S046 (C5) — https://talk.jekyllrb.com/t/relative-url-and-baseurl/2051 — accessed 2026-10-22, HTTP 200 — **rejected**: scoped to GitLab Pages and a local `jekyll serve`, 2018–2020; quote “relative_url ensures proper links by: ensuring the url to have a single leading slash always”.
- S047 (C4) — https://michaelcurrin.github.io/dev-cheatsheets/cheatsheets/jekyll/templating/links.html — accessed 2026-10-22, HTTP 200 — queued, tier C: “Use the relative_url filter to ensure you get a GitHub Pages project prefix added.”
- S048 (C6) — https://gohugo.io/host-and-deploy/deploy-to-github-pages/ — accessed 2026-10-22, HTTP 200 — queued: “Project sites are connected to a specific project hosted on GitHub.”
- Not opened (C2) — https://stackoverflow.com/questions/30209076/ returned HTTP 403 with a bot-challenge page. It was not opened by any other means and has no row.

### Registry changes (old → new)

- S040–S043: no row → new rows, tier A, status `mined`, opened `2026-10-22`,
  recheck `90d`, used-by `corpus/knowledge/pages-base-path.md,
  corpus/lessons/round-29.md`.
- S044–S046: no row → new rows, tier C, status `rejected`, teaches starting
  `REJECTED:` with a flip condition.
- S047: no row → tier C, `queued`. S048: no row → `queued`; the screening seat
  drafted tier C, and the L1 set tier A because the row's stated scope is
  Hugo's own recipe and the page is Hugo's official documentation.
- No pre-existing row's status, recheck or used-by cell changed. One Paths
  line (Project-site base paths) and one Search log paragraph (Round 29) were
  appended.
