# DraftRenderEntry — C2 knowledge entry draft

Seat `KakeR30.DraftRenderEntry` (leaf, wave 1, axis freshness, milestone r30-build).

**Built.** Draft of `corpus/knowledge/render-static-sites.md` in the shape of the two example entries named in the task: 8-line metadata header (lines 1-8), blank line 9, body. Sections in the requested order: publish directory and build; redirect and rewrite rule order; custom response headers; custom domains and TLS; difference from GitHub Pages behaviour already held in the corpus; what the entry does not establish. Every factual sentence carries a curly-quoted span plus its source id in parentheses; 9 sentences are marked `[INFERENCE]` (the six corpus contrasts in section 5, and the publish-directory sentence, since the retained pages name no directory field). The GitHub Pages side of each contrast cites the corpus entry that already holds it, with that entry's own source ids.

**Draft path** `/fast/scratch/hyaku/kake-r30/w1/DraftRenderEntry/render-static-sites.md` — **word count** 2218 (`wc -w`, exit 0); 110 lines, 56 curly-quoted spans, 56 left and 56 right curly quotes (balanced).

**Commands and exit codes.** `python3 -B verify_quotes.py` exit 0 -> `quotes checked: 56 bad: 0`. `python3 -B probe_quotes.py` exit 0 -> `checked 52 fail 0`. `python3 -B probe2.py` exit 0 -> 30/30 candidates matched after two non-substrings were dropped. `python3 -c` counter check (b) simulation exit 0 -> first body citation line per id: S049 19, S050 36, S051 49, S052 19, all after the 8-line header. `grep -q "^| S049" corpus/SOURCES.md` exit 1 -> no registry row for S049-S052 yet. `wc -w render-static-sites.md` exit 0 -> 2218. The substring check, one-liner form, run for every span by `verify_quotes.py`, which pairs each curly quote with the citation marker that follows it and tests `quote in collapsed(retained_text)`:

    python3 -c "import re;t=re.sub(r'\s+',' ',open('.../S049.txt').read());print('HIT' if 'QUOTE' in t else 'MISS')"

**Quote table** (56 spans, all PASS; machine-readable `.../quote_table.json`, rendered `.../quote_table.md`):

| # | line | id | check | quote (exact substring of the retained text) |
|---|---|---|---|---|
| 1 | 24 | S049 | PASS | “specify your build details (including which Git branch to deploy)” |
| 2 | 27 | S049 | PASS | “By default, Render automatically attempts to detect and install your static site's dependencies.” |
| 3 | 28 | S049 | PASS | “If you prefer to install dependencies manually, add a SKIP_INSTALL_DEPS environment variable to your site and set it to true .” |
| 4 | 28 | S049 | PASS | “You can then include your own dependency installation as part of your site's build command.” |
| 5 | 29 | S049 | PASS | “We build your site with every push to your deployed branch, and each build is fully atomic.” |
| 6 | 29 | S049 | PASS | “As soon as a build succeeds, we deploy it and immediately invalidate our CDN caches so your users always see the latest working version of your site.” |
| 7 | 30 | S049 | PASS | “Render serves your site over a blazing-fast, reliable, and secure global CDN.” |
| 8 | 30 | S049 | PASS | “We cache your content on network edges around the world, ensuring the fastest possible load times for your users.” |
| 9 | 32 | S049 | PASS | “Deploying a dynamic site, such as a Rails app? Create a web service instead of a static site.” |
| 10 | 36 | S049 | PASS | “Define redirect and rewrite rules for your site's paths directly from the Render Dashboard—no code required.” |
| 11 | 36 | S050 | PASS | “When the path of an incoming request matches a rule's Source , Render automatically redirects or rewrites the request to the corresponding Destination .” |
| 12 | 37 | S050 | PASS | “Instructs the browser (or any other client) to switch URLs to the rule's destination via a 301 Moved Permanently response code.” |
| 13 | 37 | S050 | PASS | “Does not redirect the browser. Instead, your site serves the content from the rule's destination at the original path.” |
| 14 | 37 | S050 | PASS | “The browser can't detect that content was served from a different path or URL.” |
| 15 | 39 | S050 | PASS | “Render does not apply redirect or rewrite rules to a path if a resource exists at that path.” |
| 16 | 39 | S050 | PASS | “Render simply serves the resource at that path.” |
| 17 | 40 | S050 | PASS | “Apply the first matching rule (starting from the top of the list)” |
| 18 | 40 | S050 | PASS | “Return 404 Not Found” |
| 19 | 41 | S050 | PASS | “If this process results in a redirect to another site path, the process repeats with the new path.” |
| 20 | 42 | S050 | PASS | “You can't apply redirect/rewrite rules to your domain root.” |
| 21 | 42 | S050 | PASS | “Each Source requires at least one URL path component (such as /blog , or even / ).” |
| 22 | 43 | S050 | PASS | “Source must be a path (not a full URL).” |
| 23 | 43 | S050 | PASS | “Destination can be either a path or a full, publicly accessible URL.” |
| 24 | 44 | S050 | PASS | “In Source , * matches any string that appears starting at that position in the path.” |
| 25 | 44 | S050 | PASS | “In Destination , * applies the entire string captured by the wildcard in Source .” |
| 26 | 49 | S051 | PASS | “Because static sites don't have a server-side component that can inject custom HTTP response headers , you can define response headers for your static sites in the Render Dashboard .” |
| 27 | 50 | S051 | PASS | “The header path must be a relative path without the domain.” |
| 28 | 50 | S051 | PASS | “It will be matched with all custom domains attached to your site.” |
| 29 | 51 | S051 | PASS | “You can use wildcards to match arbitrary request paths.” |
| 30 | 52 | S051 | PASS | “The name is the case-insensitive name for the header.” |
| 31 | 52 | S051 | PASS | “The value of the header is sent as-is in the response.” |
| 32 | 53 | S051 | PASS | “The header key is normalized and the value is appended to it to form the response: cache-control: public, max-age=86400 x-frame-options: DENY referrer-policy: same-origin” |
| 33 | 57 | S052 | PASS | “Only web services and static sites support custom domains.” |
| 34 | 57 | S052 | PASS | “Services with a custom domain also keep their onrender.com subdomain.” |
| 35 | 58 | S052 | PASS | “Add your domain in the Render Dashboard .” |
| 36 | 58 | S052 | PASS | “Configure DNS with your domain's provider.” |
| 37 | 58 | S052 | PASS | “Verify your domain in the Render Dashboard.” |
| 38 | 59 | S052 | PASS | “Click the Verify button next to your custom domain.” |
| 39 | 59 | S052 | PASS | “If verification succeeds, Render issues a TLS certificate for your domain and updates the verification status:” |
| 40 | 60 | S052 | PASS | “Render automatically creates and renews TLS certificates for all custom domains, including wildcard domains .” |
| 41 | 60 | S049 | PASS | “Render uses Let's Encrypt and Google Trust Services to automatically issue and renew TLS certificates for every site and service.” |
| 42 | 61 | S052 | PASS | “All HTTP traffic to a custom domain is automatically redirected to HTTPS.” |
| 43 | 62 | S052 | PASS | “Remove any AAAA records from your domain while configuring DNS. AAAA records map to an IPv6 address, and Render uses IPv4.” |
| 44 | 63 | S052 | PASS | “If you add a www subdomain (e.g., www.example.org ), Render automatically adds the corresponding root domain and redirects it to the www subdomain.” |
| 45 | 64 | S052 | PASS | “After you disable your onrender.com subdomain, all requests to it receive a 404 response.” |
| 46 | 64 | S052 | PASS | “reachable exclusively at its custom domain(s)” |
| 47 | 65 | S052 | PASS | “To use a wildcard domain, your root domain must also point to Render.” |
| 48 | 66 | S052 | PASS | “If your custom domain defines CAA records , make sure to define records for Render's certificate authorities:” |
| 49 | 74 | S050 | PASS | “Apply the first matching rule (starting from the top of the list)” |
| 50 | 79 | S050 | PASS | “Return 404 Not Found” |
| 51 | 81 | S050 | PASS | “Return 404 Not Found” |
| 52 | 84 | S050 | PASS | “Does not redirect the browser. Instead, your site serves the content from the rule's destination at the original path.” |
| 53 | 85 | S051 | PASS | “You can use wildcards to match arbitrary request paths.” |
| 54 | 86 | S052 | PASS | “Only web services and static sites support custom domains.” |
| 55 | 91 | S052 | PASS | “If you add a root domain (e.g., example.org ), Render automatically adds the corresponding www subdomain and redirects it to the root domain.” |
| 56 | 96 | S049 | PASS | “Render uses Let's Encrypt and Google Trust Services to automatically issue and renew TLS certificates for every site and service.” |

**Findings and limits.** (1) Publish directory is not in the retained sources: neither S049.txt nor S049.html.gz contains `publish directory`, `root directory` or `output directory` (grep count 0), so the entry states the absence and marks the conclusion `[INFERENCE]` rather than inventing a field name. (2) No live request of any kind was made: reads were the four retained `.txt`/`.html.gz` files, `receipts.json`, two example corpus entries and four corpus entries cited for the Pages contrast; no owned site was contacted and no freshness-sweep, probe-delta or live_snapshot script was run. (3) Counter readiness: the C2 counter also needs a `mined` registry row opened 2026-10-22 in `corpus/SOURCES.md` and a `## Gate` line in `corpus/lessons/round-30.md` per id; neither is in the tree yet and both belong to other seats, so my draft satisfies only the entry-side check (b). (4) Retained-text artefacts are preserved verbatim: spans that look odd (`Source ,` `Destination .` `set it to true .` `headers ,` `records ,`) are the tag-removal whitespace of the retained plain text, kept so every span stays an exact substring. (5) The counter proves sourcing, not entailment; whether each sentence follows from its quote is the closure's read. (6) No tools installed; none was needed.

**Artifacts**, all in `/fast/scratch/hyaku/kake-r30/w1/DraftRenderEntry/`: `render-static-sites.md` (draft), `quote_table.md`, `quote_table.json`, `verify_quotes.py`, `probe_quotes.py`, `probe2.py`. The draft is not committed anywhere; the L1 integrates it into `corpus/knowledge/render-static-sites.md`.

Report: .ufo/waves/round-30/w1/DraftRenderEntry.md
