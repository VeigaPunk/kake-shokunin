source: S049, S050, S051, S052 (corpus/SOURCES.md) — https://render.com/docs/static-sites; https://render.com/docs/redirects-rewrites; https://render.com/docs/static-site-headers; https://render.com/docs/custom-domains
verified-at: 2026-10-22 (all four opened this round with one public GET each at 2026-10-22T11:49Z, HTTP 200; retained visible text and receipts under .ufo/waves/round-30/sources/, text sha256 S049 3604f8f5…, S050 1c413643…, S051 e98982ce…, S052 6c1616f8…)
recheck: 90d, or on a Render Docs change — re-open each page once (`.ufo/waves/round-30/fetch_sources.py` logic, in a sandbox) and compare the visible-text sha256 with `.ufo/waves/round-30/sources/receipts.json`; the counter `python3 -B .ufo/waves/round-30/c2_quote_truth.py --root . --revision <commit>` replays the retained text only and cannot see a page change
scope: Render platform documentation for static sites only. This entry makes no live request to any operator-owned property and asserts nothing about any owned site.
ground: the four retained Render Docs pages named above; every factual sentence below carries a curly-quoted span that is an exact substring of one retained text, with the source id in parentheses.
coverage: publish directory and build, redirect and rewrite rule order, custom response headers, custom domains and TLS, and the contrast with GitHub Pages behaviour already held in this corpus.
falsifier: an operator-authorized read of a Render static site's settings or a fresh fetch of the four Render Docs pages that contradicts any quoted sentence below.
counter: python3 -B .ufo/waves/round-30/c2_quote_truth.py --root . --revision <commit> — 4/4 declared ids expected at the landed commit.

# Render static sites — deploy semantics

Coverage-map ground: publishing-platform semantics for a static site hosted on
Render, so a publisher knows what Render does with a build, a path and a domain
before choosing it over the GitHub Pages channel the lane already holds. This
entry is documentation-scope only: it measures no owned property, verifies no
live Render site, and does not re-verify any GitHub Pages fact. The GitHub
Pages side of every contrast below is cited to the corpus entry that already
holds it (with that entry's own source ids); the Render side is quoted from
S049–S052; the contrast itself is an [INFERENCE] drawn from the two sides.

## Publish directory and build

- Creating a Render static site asks the dashboard for build details, and the
  branch is one of them: “specify your build details (including which Git branch to deploy)” (S049).
- The retained static-sites page names no publish-directory, root-directory or
  output-directory field at all; the only build-time setting it names besides
  the branch is dependency installation, which it opens with “By default, Render automatically attempts to detect and install your static site's dependencies.” (S049). [INFERENCE] the directory Render publishes from is configured on a page this round did not retain, so this entry cannot state how it is chosen.
- Manual installation is opted into with an environment variable: “If you prefer to install dependencies manually, add a SKIP_INSTALL_DEPS environment variable to your site and set it to true .” (S049), after which the site's own command takes over: “You can then include your own dependency installation as part of your site's build command.” (S049).
- Builds are per-push and atomic: “We build your site with every push to your deployed branch, and each build is fully atomic.” (S049), and a successful build is published and the CDN cache invalidated at once: “As soon as a build succeeds, we deploy it and immediately invalidate our CDN caches so your users always see the latest working version of your site.” (S049).
- The site is served from a global CDN: “Render serves your site over a blazing-fast, reliable, and secure global CDN.” (S049), with edge caching described as “We cache your content on network edges around the world, ensuring the fastest possible load times for your users.” (S049).
- A static site is one of several service kinds, and a dynamic site belongs
  to another: “Deploying a dynamic site, such as a Rails app? Create a web service instead of a static site.” (S049).

## Redirect and rewrite rule order

- The retained pages set rules in the dashboard, with no code in the site (whether a Blueprint file can also carry them is not settled by S049–S052): “Define redirect and rewrite rules for your site's paths directly from the Render Dashboard—no code required.” (S049), and each rule pairs a source with a destination: “When the path of an incoming request matches a rule's Source , Render automatically redirects or rewrites the request to the corresponding Destination .” (S050).
- A redirect is a client-visible 301: “Instructs the browser (or any other client) to switch URLs to the rule's destination via a 301 Moved Permanently response code.” (S050); a rewrite is not: “Does not redirect the browser. Instead, your site serves the content from the rule's destination at the original path.” (S050), so “The browser can't detect that content was served from a different path or URL.” (S050).
- An existing resource outranks any rule, which is the first branch of the
  documented matching process: “Render does not apply redirect or rewrite rules to a path if a resource exists at that path.” (S050), after which “Render simply serves the resource at that path.” (S050).
- Only then do rules apply, first match wins, and no match is a 404: “Apply the first matching rule (starting from the top of the list)” (S050) and “Return 404 Not Found” (S050).
- A redirect that lands on another path of the same site re-enters the same process: “If this process results in a redirect to another site path, the process repeats with the new path.” (S050).
- The domain root cannot carry a rule: “You can't apply redirect/rewrite rules to your domain root.” (S050), and every source path needs at least one component: “Each Source requires at least one URL path component (such as /blog , or even / ).” (S050).
- Source is a path and destination is a path or a full, publicly accessible URL: “Source must be a path (not a full URL).” (S050) and “Destination can be either a path or a full, publicly accessible URL.” (S050).
- Wildcards capture in the source and reappear in the destination: “In Source , * matches any string that appears starting at that position in the path.” (S050) and “In Destination , * applies the entire string captured by the wildcard in Source .” (S050).

## Custom response headers

- Static sites have no server-side component to inject headers, so headers are
  declared in the dashboard: “Because static sites don't have a server-side component that can inject custom HTTP response headers , you can define response headers for your static sites in the Render Dashboard .” (S051).
- A header rule is a relative path without the domain: “The header path must be a relative path without the domain.” (S051), and it applies to every custom domain on the site: “It will be matched with all custom domains attached to your site.” (S051).
- Paths may be wildcards: “You can use wildcards to match arbitrary request paths.” (S051).
- The header name is matched case-insensitively: “The name is the case-insensitive name for the header.” (S051), and the value is sent unchanged: “The value of the header is sent as-is in the response.” (S051).
- The response carries the normalized lowercase name with the value appended: “The header key is normalized and the value is appended to it to form the response: cache-control: public, max-age=86400 x-frame-options: DENY referrer-policy: same-origin” (S051).

## Custom domains and TLS

- Only web services and static sites take a custom domain: “Only web services and static sites support custom domains.” (S052), and a service that has one keeps its default hostname: “Services with a custom domain also keep their onrender.com subdomain.” (S052).
- The steps are add, configure DNS, verify: “Add your domain in the Render Dashboard .” (S052), “Configure DNS with your domain's provider.” (S052) and “Verify your domain in the Render Dashboard.” (S052).
- Verification is an explicit dashboard action: “Click the Verify button next to your custom domain.” (S052), and on success the certificate is issued: “If verification succeeds, Render issues a TLS certificate for your domain and updates the verification status:” (S052).
- Certificates are issued and renewed automatically, wildcards included: “Render automatically creates and renews TLS certificates for all custom domains, including wildcard domains .” (S052), and the platform-wide statement is “Render uses Let's Encrypt and Google Trust Services to automatically issue and renew TLS certificates for every site and service.” (S049).
- Plain HTTP is redirected to HTTPS: “All HTTP traffic to a custom domain is automatically redirected to HTTPS.” (S052).
- DNS configuration must not leave AAAA records behind: “Remove any AAAA records from your domain while configuring DNS. AAAA records map to an IPv6 address, and Render uses IPv4.” (S052).
- Adding one half of a domain pair adds the other with a redirect: “If you add a www subdomain (e.g., www.example.org ), Render automatically adds the corresponding root domain and redirects it to the www subdomain.” (S052).
- The default hostname can be switched off, and then it stops answering: “After you disable your onrender.com subdomain, all requests to it receive a 404 response.” (S052), leaving the service “reachable exclusively at its custom domain(s)” (S052).
- A wildcard domain needs the root domain pointing at Render too: “To use a wildcard domain, your root domain must also point to Render.” (S052).
- When a domain does publish CAA records, they must name Render's authorities: “If your custom domain defines CAA records , make sure to define records for Render's certificate authorities:” (S052).

## How this differs from GitHub Pages behaviour already held in this corpus

The GitHub Pages side of each contrast is cited to the lane entry that holds
it; the Render side is quoted from S049–S052. Where the corpus is silent on a
Pages mechanism, that silence is a fact about this corpus, not about GitHub
Pages. Wave-2 seat `CriticEntryContrast` corrected four contrasts in this
section on 2026-10-22.

- Redirects: GitHub Pages in this corpus redirects a slashless directory path
  to its slash form and serves `index.html` there
  (corpus/knowledge/ghp-subpath-spotcheck.md, entry-local live evidence).
  Render has two kinds of redirect: platform redirects that need no rule —
  “Render automatically redirects HTTP traffic to HTTPS” (S049), and
  “If you add a www subdomain (e.g., www.example.org ), Render automatically adds the corresponding root domain and redirects it to the www subdomain.” (S052) —
  and dashboard rules applied after the resource check and before the 404:
  “Apply the first matching rule (starting from the top of the list)” (S050).
  [INFERENCE] the slashless-directory redirect the corpus holds for Pages has
  no stated Render counterpart in S049–S052.
- Missing pages: the corpus holds that the Plazir GitHub Pages site serves its
  own root `404.html` bytes for a missing route
  (corpus/knowledge/ghp-subpath-spotcheck.md, entry-local live evidence). For
  a path with no resource and no matching rule, S050's matching flow ends:
  “Return 404 Not Found” (S050). The retained pages say nothing about a custom
  404 document, and a catch-all rewrite replaces the 404 altogether for a
  client-side-routed site: “you'll handle all requests from a single path like /index.html” (S050).
- Rewrites and client-side routing: the corpus holds no GitHub Pages
  URL-rewrite rule mechanism, and Render names one: “Does not redirect the browser. Instead, your site serves the content from the rule's destination at the original path.” (S050).
- Response headers: the corpus holds no author-defined per-path
  response-header mechanism for GitHub Pages (its header material is
  server-generated ETag anatomy, corpus/knowledge/ghp-etag-anatomy.md), and
  Render names one: “You can use wildcards to match arbitrary request paths.” (S051).
  Whether GitHub Pages has such a mechanism is not settled by this corpus.
- Custom domain authority: the corpus holds the domain as GitHub Pages
  configuration rather than a repository file under workflow publishing — an
  Actions-published site ignores a repository `CNAME` file
  (corpus/knowledge/ghp-custom-domain.md, S005, S003, S007). The retained
  Render page adds a domain in the dashboard: “Add your domain in the Render Dashboard .” (S052).
  The same page offers the Render Dashboard, a “Blueprint (render.yaml)” (S052)
  and the Render API as ways to change the onrender.com subdomain setting, so
  a repository file can carry at least some domain settings. Whether a
  Blueprint can also attach the custom domain itself is not settled by the
  retained pages (a wave-1 scout reports a `domains` field in the Blueprint
  reference, which this round did not retain).
- Base path: the corpus holds that a GitHub Pages project site is served under
  a repository-name subpath and needs a build-time base
  (corpus/knowledge/pages-base-path.md, S040, S041, S042, S043). The retained
  Render pages describe a site at its own host: “Each site receives a unique onrender.com URL” (S049),
  and name no subpath. [INFERENCE] a site whose build sets a Pages project-site
  base such as `/<REPO>/` emits references under that prefix, so before the
  same build is published on a Render host its base should be rechecked.
- TLS: the corpus holds no GitHub Pages certificate issuer or renewal
  statement at all — its custom-domain entry covers the domain as a Pages
  setting, the ignored `CNAME` file and the `cname` / `build_type` API fields
  (corpus/knowledge/ghp-custom-domain.md, S005, S003, S007) — while Render
  states its issuers and renewal directly: “Render uses Let's Encrypt and Google Trust Services to automatically issue and renew TLS certificates for every site and service.” (S049). [INFERENCE] a publisher comparing the two must add the Render-side facts from this entry; the corpus cannot supply a Pages counterpart to them.

## What this entry does not establish

- No live Render site was fetched, and no operator-owned property was
  contacted while writing it; every sentence above is a reading of four
  retained documentation pages.
- The publish directory, root directory or output path of a Render static site
  is not stated by S049–S052 and is therefore not claimed here (a wave-1 scout
  reports a `staticPublishPath` Blueprint field; that page is a lead, not a
  registry row).
- The counter above proves that each of the four ids has a registry row, a
  citation below the header and a quote that is a true substring of the
  retained text; it does not prove that each sentence of this entry follows
  from its quote. That reading is the closure's work.
- Nothing here changes the lane's property map or its publish channels: the
  Render row the lane holds is a Docker web service, not a static site
  (corpus/knowledge/publish-channels.md, `app.ds4cc.com`).
