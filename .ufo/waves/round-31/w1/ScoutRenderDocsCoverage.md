# Scout — retained Render text coverage for C2 (round 31, wave 1)

Worked from `.ufo/waves/round-31/sources/*.txt` only; no network, no live Render page.
All five texts hash to the `textSha256` values in `sources/receipts.json`
(`sha256sum S05*.txt` exit 0; S057 `ca8179f2…`, S058 `983a792d…`, S059 `f8e60da0…`,
S060 `1f934877…`, S061 `aa904927…`). `corpus/knowledge/render-web-services.md` does not
exist at `a16602a` (`git cat-file -e` → fatal), so this is pre-write input, not review.

Commands: `sha256sum` (exit 0); sandbox scripts
`/fast/scratch/hyaku/kake-r31/w1/ScoutRenderDocsCoverage/verify_quotes.py` (exit 0, 49/49
quotes exact, machine check in `quotes.json`); absence probes with `re.findall` (exit 0).

## Page shape (heading tags, H6 = Blueprint field names)
- S057 `Blueprint YAML Reference`: H2 Example file / Validating / Root-level / Service fields /
  Database fields / Inbound IP rules / Projects and environments / Setting environment variables;
  H3 Essential, Docker, Scaling, Build, Disks, Static sites, Render Key Value, Environment variables,
  and under env: Referencing properties, secret values, random secrets, Environment groups,
  Variable interpolation, Preview environments. 79 H6 field headings (list in sandbox `s057-fields.txt`).
- S058 `Web Services`: Deploy a template, Deploy your own code, Port binding, Connect, Additional features.
- S059 `Docker on Render`: deployment methods (registry pull, Dockerfile build), Docker or native
  runtime, Docker-specific features (env var translation, image builds, image caching), popular images.
- S060 `Health Checks`: HTTP checks (web services only), Setup, Success criteria, Handling failures.
- S061 `Configuring DNS Providers`: root domains (ANAME/ALIAS, A record), www and other subdomains.

## Covered, with exact quotes (source@byte offset, 6–25 words)
| Topic | Retained statement | Quote |
|---|---|---|
| Docker runtime | runtime values and Docker-only fields | S057@18248 “Workflow services do not currently support these Docker-specific fields.” |
| | field defaults | S057@18654 “If omitted, Render uses ./Dockerfile .” / S057@18856 “If omitted, Render uses the repo root.” |
| | method | S059@2682 “Build from a Dockerfile or pull from a container registry.” |
| | env→build args | S059@6477 “Render automatically translates those values to Docker build arguments that are available during your image's build process.” |
| | build context | S059@7119 “Render omits files and directories from your build context based on your .dockerignore file.” |
| Health checks | default probe | S060@3276 “By default, health checks are TCP socket probes to one of your service's open ports.” |
| | HTTP enablement | S060@4768 “add the healthCheckPath field to your web service's definition” |
| | success rule | S060@5001 “Render considers a check successful if the instance responds with a 2xx or 3xx status code within five seconds.” |
| | running-instance failure | S060@5934 “If a running service instance fails consecutive health checks for 15 seconds” |
| | deploy failure | S060@5689 “If this condition is not met within 15 minutes, Render cancels the deploy” |
| | Host header | S060@4007 “If your service has any verified custom domains , Render sets one of those domains as the value of the Host header” |
| Env vars / sync | Blueprint writes | S057@31952 “A Blueprint can create new environment variables or modify the values of existing ones.” |
| | preservation | S057@32040 “Render preserves existing environment variables, even if you omit them from the Blueprint file.” |
| | sync: false limit | S057@35996 “Render ignores any environment variables with sync: false .” (also S057@35876 “Render prompts you for these values only during the initial Blueprint creation .”) |
| | generated secrets | S057@36626 “If the environment variable doesn't already exist, Render adds it and sets its value to a randomized, base64-encoded, 256-bit value” |
| | per-preview value | S057@37537 “Use the previewValue field to override environment variable values for web and private services in preview environments” |
| Custom domains | Blueprint key | S057@15391 “A list of custom domains for the service.” |
| | auto www | S057@15550 “Render automatically adds a www. subdomain that redirects to the root domain.” |
| | subdomain policy | S057@16101 “Disabling a service's onrender.com subdomain requires the service to have at least one custom domain.” |
| | DNS mechanics | S061@3566 “you can use ANAME or ALIAS records if your DNS provider supports them”; S061@5455 “you should always add a CNAME record pointing to your app's Render subdomain” |
| Preview environments | root switch | S057@7178 “If you omit this field, preview environments are disabled for any linked Blueprints.” |
| | retention | S057@7465 “The number of days to retain a preview environment that receives no updates.” |
| | inherited resources | S057@11755 “If you omit this subfield, preview instances use the same number of instances as the base service.” / S057@12120 “If you omit this subfield, preview instances use the same compute plan as the base service.” |
| | secrets gap | S057@36124 “Render does not include sync: false environment variables in preview environments .” |
| autoDeploy | trigger values | S057@14657 “autoDeployTrigger Sets the automatic deploy behavior for a Git-based service.” |
| | deprecation | S057@15041 “This field replaces the deprecated autoDeploy field.” / S057@15094 “If you include both, autoDeployTrigger takes precedence.” |
| | default | S057@15251 “Render uses commit for a new service.” |
| | image services | S057@15151 “This field has no effect for services that deploy a prebuilt Docker image .” / S058@8616 “Services deployed from prebuilt images don't support auto-deploys .” |
| region | values/default | S057@13504 “oregon (default for non- workflow services) ohio virginia frankfurt singapore”; S057@13716 “If omitted for other service types, the default value is oregon .” |
| | immutability | S057@8716 “You can't modify this value after creation.” |
| plan | key + ids | S057@9343 “The service's compute plan , such as free or 1c-2g .”; S057@9444 “Show service compute plans Web Service Web Service Private Service” (plan id table follows) |
| | existing service | S057@10868 “Render retains the current compute plan for an existing service.” |

## Not stated by the retained texts — mark open, do not guess
1. Health check cadence/config: `interval`, `timeout`, `retry`, `healthCheckPort` occur zero times in
   all five texts; only S060@2750 “Every few seconds, Render sends health checks to each running web service and private service instance”.
   No configurable interval, per-check timeout, retry count, or health-check port is documented.
2. Custom-domain verification and TLS for domains: the phrase `verified custom domains` is presupposed (S060@4007)
   but no verification flow, certificate issuance or renewal is described (`renew` = 0); TLS and wildcard
   domains appear only in the capability list, S058@10651 “Free, fully managed TLS certificates Custom domains (including wildcards)”.
   S061 covers DNS records only, and only for the dashboard flow
   (S061@2756 “This guide assumes you've added a custom domain to your service in the Render Dashboard.”).
3. Wildcard custom domains in YAML: no `domains` syntax is given; the only mention is the capability list above.
4. Env var precedence: `overwrit` = 0; nothing states whether a changed `value` replaces a Dashboard-edited
   value on the next sync, nor what happens when a key is removed from render.yaml.
5. Plan default and price: the only web-service default is a comment inside the example file,
   S057@38996 “plan : 1c - 2g # Default: 0.5c-512mb”; prose gives no default. `price`/`billing`/`$`-cost = 0,
   so no cost figures; also unstated whether a plan change redeploys (`redeploy` occurs, but never about plan).
6. Region constraints: no per-plan availability, latency or multi-region guidance (`multi-region`, `latency` = 0).
7. Preview environments: no statement of preview cost beyond S057@7561 “Render automatically deprovisions the preview environment to help reduce your compute costs.”; no preview region, no preview-env var set beyond
   `previewValue`, no statement that previews need a paid workspace.
8. autoDeploy: only the equivalence and default above; no detail on what `checksPass` accepts (CI provider,
   timeout) and no statement of the deprecated boolean's behaviour beyond equivalence.
9. Docker: no cache-invalidation rule for `dockerContext`, no digest-pinning statement (`digest` = 0).

## Extraction caveat that limits what can be quoted
All code blocks survive into the `.txt`, but the extractor split syntax-highlight tokens, so code
arrives with spaces inserted around punctuation: `services : - type : web`, `healthCheckPath : /health`,
`const express = require ( 'express' )`. The YAML schemas for `registryCredential`, `image`, `scaling`,
`buildFilter`, `disk`, `headers`, `routes`, `envVarGroups`, `envVars` and `projects` are quotable only
in that tokenized form. `c2_quote_truth.py:110-115` requires an exact collapsed-whitespace substring of
the `.txt`, so Gate quotes must come from prose; any snippet quote must reproduce the inserted spacing.
One field's own format block (`registryCredential`) is absent at its point of use, so its exact schema
is not visible there (only the trailing example's `registryCredential : # Default: No credential`).

## Not verified
I did not run the C2 counter, did not write the entry, and did not check S061/round-30 defect 4; this report
states only what the retained texts do and do not say. No tools installed.
