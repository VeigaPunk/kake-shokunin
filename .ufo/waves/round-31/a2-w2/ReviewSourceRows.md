# KakeR31a2.ReviewSourceRows — C2 rows S057–S061 vs retained text

Sandbox: /fast/scratch/hyaku/kake-r31/a2-w2/ReviewSourceRows/clone @ fde133ab48086bb9a06911b4ab045e2ad9086347 (cloned from the lane, checked out read-only; no lane mutation). Retained texts: .ufo/waves/round-31/sources/ (each file is a single whitespace-collapsed line, so checks were phrase-window greps, not heading greps).

## Row | issue

- S057 | PASS — all six anchors present in retained text: "Essential fields" table has name ("name Required. The service's name."), type ("type Required. The type of service. One of the following: web …"), runtime ("runtime Required unless type is keyvalue or redis …"); "Building from a Dockerfile" table has dockerCommand ("If omitted, Render uses the CMD defined in the Dockerfile"), dockerfilePath ("relative to the repo root … Render uses ./Dockerfile"), dockerContext ("relative to the repo root … Render uses the repo root"); healthCheckPath ("This value always starts with a / character"); domains and renderSubdomainPolicy rows both present; "Setting environment variables" and "Prompting for secret values" sections present. Teaches supported: "By default, this file has the name render.yaml and resides in your Git repository's root directory (you can customize this during setup)"; sync:false — "Render prompts you for these values only during the initial Blueprint creation … When you update an existing Blueprint, Render ignores any environment variables with sync: false"; omitted-field retention — "Render retains the current value for an existing service" occurs 5× plus "Render preserves existing environment variables, even if you omit them from the Blueprint file". Scope honest (no other host, no live service).
- S058 | PASS — anchor (opening section) verified: opening paragraphs carry "Render builds and deploys your code with every push to your linked Git branch", "Every Render web service gets a unique onrender.com subdomain", "must bind to a port on host 0.0.0.0 to receive HTTP requests from the public internet", "The default expected port is 10000". Teaches cell restates those four verbatim-faithfully. Scope honest ("not … static sites or any other host"; page's port section even says a private service is the alternative).
- S059 | MINOR FINDING — anchor cell names section "Environment variables and build arguments", which appears nowhere in the retained text (grep count of "and build arguments" in S059.txt = 0). The actual retained section title is "Environment variable translation" ("Docker-specific features Environment variable translation If you set environment variables for a Docker-based service, Render automatically translates those values to Docker build arguments …"). The taught facts are all supported by retained text: opening list ("Pull and run a prebuilt image …, or Build their own image at deploy time based on the Dockerfile in your project repo"), CMD-vs-Docker Command ("instead of using the CMD instruction in your Dockerfile … specify it in the Docker Command field under Advanced"), build args → secret files ("do not reference any build arguments that contain sensitive values … use a secret file instead"), .dockerignore ("Render omits files and directories from your build context based on your .dockerignore file"), zero-downtime present. Defect is the anchor label only; suggested fix: rename anchor to "Environment variable translation". Scope honest ("not a general Docker reference").
- S060 | PASS — anchors exact: "HTTP health checks (web services only)", "Success criteria", "Handling failures" all appear as section titles; Host-header answer present ("If your service has any verified custom domains, Render sets one of those domains as the value of the Host header … Otherwise, Render uses the service's onrender.com subdomain"). Teaches supported: 2xx/3xx within five seconds; all new instances pass together → deploy successful, "If this condition is not met within 15 minutes, Render cancels the deploy"; "fails consecutive health checks for 15 seconds, Render temporarily stops routing"; "60 seconds, Render automatically restarts the instance". Scope honest.
- S061 | PASS — anchors present: "Configuring root domains", "Using an ANAME or ALIAS record", "Using an A record" with 216.24.57.1 ("you can use 216.24.57.1 to point your root domain to Render's load balancer IP"), AAAA warning ("Remove any AAAA records from your domain … Render uses IPv4"). Teaches matches; note the teaches says "points at the onrender.com subdomain" where the page says "point to your app's Render subdomain" — same referent, no defect. Scope honest and correctly narrower than the Cloudflare/Namecheap pages (page itself routes dedicated providers elsewhere); no claim about owned domains.

## Integrity checks (all pass)

- sha256 of retained text files matches receipts.json textSha256 for all five: S057 ca8179f2…, S058 983a792d…, S059 f8e60da0…, S060 1f934877…, S061 aa904927….
- sha256 of gunzipped .html.gz bodies matches receipts.json bodySha256 for all five: S057 650ed15d…, S058 eaa1f028…, S059 d3ce93a7…, S060 70954862…, S061 bb75fe4b….
- Receipts: HTTP 200, one GET each, 2026-10-22T15:41:23Z (S057), 15:41:26Z (S058, S059), 15:41:28Z (S060), 15:41:29Z (S061) — matches the declared open times.
- used-by paths exist at the review commit: corpus/knowledge/render-web-services.md (used-by of S057–S060; its header cites S057–S060 and its quotes lines 20-22, 27-31, 35 match retained text spot-checks) and corpus/knowledge/render-static-sites.md (used-by of S061; "Round-31 corrections" at line 141 quotes S061 verbatim at lines 158-160). corpus/lessons/round-31.md exists.

## Census output (read-only, exact)

Command: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake → exit 0

```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```

The single W04 warning is pre-existing row S033 (not a C2 row); rows S057–S061 raise no census finding.

## Not verified / residual

- No live refetch of render.com: this seat was not authorized to open URLs, and the assigned target is "cells against the retained text"; so anchors/teaches are judged against the retained bodies only (receipts pin those bodies by hash).
- Column conventions (tier A, status mined, opened 2026-10-22, recheck 90d) match neighbouring registry rows; I did not re-derive QUALITY.md admission rules beyond that.
- No installs or upgrades were needed; no tooling changes to record.
