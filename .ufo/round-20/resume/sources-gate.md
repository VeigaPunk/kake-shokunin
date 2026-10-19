# Round 20 source gate evidence

Each row below records an opened source, the 2026-10-19 access date, a verbatim quote of at most 25 words, and its location. For S018, the Firefox 144.0 release notes were also opened as the tier-A cross-check.

## S001 — actions/upload-pages-artifact action.yml

- URL: https://raw.githubusercontent.com/actions/upload-pages-artifact/5f327015a708106f6f1b7c9a633901af30fe80cb/action.yml and https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml
- Accessed: 2026-10-19
- Quote: “Include hidden files and directories (those starting with a dot) in the artifact. Excludes .git and .github regardless.”
- Location: `inputs.include-hidden-files` description, lines 17-18; archive behavior lines 37-39; main commit `5f327015a708106f6f1b7c9a633901af30fe80cb` and v4.0.0 tag commit `7b1f4a764d45c48632c6b24a0339c27f5614fb0b`.

## S002 — actions/upload-pages-artifact releases

- URL: https://github.com/actions/upload-pages-artifact/releases/tag/v4.0.0 and https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0
- Accessed: 2026-10-19
- Quote: “Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact”; “feat: add `include-hidden-files` input”
- Location: v4.0.0 release, “What's Changed”; v5.0.0 release, “Changelog”; v4 tag commit `7b1f4a764d45c48632c6b24a0339c27f5614fb0b`, v5 tag commit `fc324d3547104276b827a68afc52ff2a11cc49c9`.

## S003 — Configuring a publishing source for your GitHub Pages site

- URL: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- Accessed: 2026-10-19
- Quote (25 words): “You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.”
- Location: “About publishing sources”; fetched 2026-10-19.

## S004 — Using custom workflows with GitHub Pages

- URL: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- Accessed: 2026-10-19
- Quote: “compressed `gzip` archive containing a single `tar` file”; “under 10GB in size and should not contain any symbolic or hard links”
- Location: “Configuring the `upload-pages-artifact` action”; first and second paragraphs; fetched 2026-10-19.

## S005 — Managing a custom domain for your GitHub Pages site

- URL: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- Accessed: 2026-10-19
- Quote: “any existing `CNAME` file is ignored and is not required.”
- Location: “Configuring an apex domain,” step 4; fetched 2026-10-19.

## S006 — About GitHub Pages and Jekyll

- URL: https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll
- Accessed: 2026-10-19
- Quote: “Are located in a folder called `/node_modules` or `/vendor`”; “Start with `_`, `.`, or `#`”; “End with `~`”
- Location: “Configuring Jekyll in your GitHub Pages site,” default exclusions; fetched 2026-10-19.

## S007 — GitHub REST API: GitHub Pages endpoints

- URL: https://docs.github.com/en/rest/pages/pages
- Accessed: 2026-10-19
- Quote: “`cname`: required, string or null”; “`protected_domain_state`: string or null”; “`build_type`: string or null”
- Location: “Get a GitHub Pages site,” response schema; fetched 2026-10-19.

## S008 — GNU tar manual: Controlling Pattern-Matching

- URL: https://cgit.git.savannah.gnu.org/cgit/tar.git/plain/doc/tar.texi?id=cfdb891bbd68c920ea75210977593f3cd08f0418
- Accessed: 2026-10-19
- Quote: “Default is `@option{--no-anchored}` for exclusion members”; “When wildcards match slash (the default for exclusion members)”
- Location: “Controlling Pattern-Matching,” anchored patterns and `--wildcards-match-slash`, lines 8478-8603; GNU tar master commit `cfdb891bbd68c920ea75210977593f3cd08f0418`.

## S009 — nginx `ngx_http_set_etag`

- URL: https://raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c
- Accessed: 2026-10-19
- Quote: `etag->value.len = ngx_sprintf(etag->value.data, "\"%xT-%xO\"", r->headers_out.last_modified_time, r->headers_out.content_length_n)`
- Location: `ngx_http_set_etag`, `src/http/ngx_http_core_module.c:1708-1710` (L1 re-verified 2026-10-19 with `grep -nF` at commit 481d28cb; the writer's 1671-1673 was wrong); release tag `release-1.28.0`, commit `481d28cb4e04c8096b9b6134856891dc52ecc68f`.

## S010 — RFC 9110 HTTP Semantics

- URL: https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8
- Accessed: 2026-10-19
- Quote: “An entity tag is an opaque validator”; “A strong validator might change for reasons other than a change to the representation data”
- Location: Section 8.8.1, “Weak versus Strong,” and 8.8.3, “ETag”; RFC 9110, June 2022.

## S011 — RFC 9309 Robots Exclusion Protocol

- URL: https://www.rfc-editor.org/rfc/rfc9309.html
- Accessed: 2026-10-19
- Quote: “The rules MUST be accessible in a file named "/robots.txt" (all lowercase) in the top-level path of the service.”; “crawler MUST assume complete disallow”
- Location: Section 2.3, “Access Method,” and Section 2.3.1.4, “Unreachable Status”; RFC 9309, September 2022.

## S012 — sitemaps.org Sitemaps XML format

- URL: https://www.sitemaps.org/protocol.html
- Accessed: 2026-10-19
- Quote: “The location of a Sitemap file determines the set of URLs that can be included in that Sitemap.”
- Location: “Sitemap file location”; fetched 2026-10-19.

## S013 — Google Search Central: Build and submit a sitemap

- URL: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Accessed: 2026-10-19
- Quote: “unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent directory.”
- Location: “Sitemap best practices”; page last updated 2026-07-08 UTC.

## S014 — own-work freshness-sweep §paths gate

- URL: `scripts/freshness-sweep.mjs`; command: `node scripts/freshness-sweep.mjs --section=paths`
- Accessed: 2026-10-19
- Quote: “Annotation window = the citing line ±2 (spec), with every *citation* on the citing line blanked”
- Location: `scripts/freshness-sweep.mjs:404-411`; command selection and §paths execution at lines 1021-1044. The opened command reported 7 unannotated missing paths and exit 1 before the citation repair landed.
- Post-repair run reported by W2RoundKake.K4xCitations: `node scripts/freshness-sweep.mjs --section=paths` returned exit 0, drift 0, missSet 55, and `set-delta miss: no new miss`; 8 unresolved placeholders/globs remain.

## S015 — GitHub Pages limits

- URL: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- Accessed: 2026-10-19
- Quote: “Published GitHub Pages sites may be no larger than 1 GB.”
- Location: “Usage limits”; fetched 2026-10-19.

## S016 — GitHub Pages dependency versions

- URL: https://pages.github.com/versions.json
- Accessed: 2026-10-19
- Quote: `"jekyll": "3.10.0", "github-pages": "232"`
- Location: JSON keys `jekyll` and `github-pages`; fetched 2026-10-19.

## S017 — Astro Docs: Deploy your Astro Site to GitHub Pages

- URL: Astro Docs https://docs.astro.build/en/guides/deploy/github/; GitHub Docs cross-check https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- Accessed: 2026-10-19
- Quote: “Add a `./public/CNAME` record to your project.”; “any existing `CNAME` file is ignored and is not required.”
- Location: Astro “Change your GitHub URL to a custom domain,” step 2; GitHub Docs “Configuring an apex domain,” step 4; fetched 2026-10-19.

## S018 — DebugBear Firefox version claim

- URL: DebugBear https://www.debugbear.com/blog/firefox-safari-web-vitals; Firefox release notes cross-check https://www.firefox.com/en-US/firefox/144.0/releasenotes/
- Accessed: 2026-10-19
- Quote (25 words): “Mozilla released version 114 of Firefox on the 14th of October 2025.”; “Firefox now supports the PerformanceEventTiming.interactionId API, allowing developers to group related input events.”
- Location: DebugBear “INP support in Firefox 114”; article updated 2026-03-19. Firefox “144.0 Firefox Release,” “Web Platform,” released 2025-10-14.


## Post-review corrections — 2026-10-19

- S007: the earlier `cname` string/null text is a schema transcription, not
  a verbatim rendered-page quote. Reviewer-opened rendered text: “cname
  string or null”; the L1-opened Markdown representation annotates it
  “required”. Authority: https://docs.github.com/en/rest/pages/pages
  §Get a GitHub Pages site, response schema (reopened 2026-10-19).
- S008: withdraw the knowledge entry's “GNU tar 1.35” label. The source is
  manual commit `cfdb891bbd68c920ea75210977593f3cd08f0418`; the source uses
  `@value{VERSION}`. Exact exclusion-default quote lines are 8587–8588 and
  8602 (non-author reviewer re-open). Both recorded containing ranges are
  broader than necessary. No SOURCES row cell changed in this correction.
