# CriticLearningClaimAfter — round 31 attempt 2, wave 2 (critic, freshness)

Seat `KakeR31a2.CriticLearningClaimAfter`. I attacked C2 as the learning claim now that it has landed. I compared
`corpus/knowledge/render-web-services.md` (entry) with `PROVINCE.md`, `publish-channels.md`, `render-static-sites.md`
and the wave-1 conditions in `.ufo/waves/round-31/w1/CriticLearningClaim.md` (w1). I worked in the sandbox clone
`/fast/scratch/hyaku/kake-r31/a2-w2/CriticLearningClaimAfter/clone` at `92235a0`. Content there is the same as `fde133a`.
I made no network request, contacted no owned site, and read ds4cc-marketplace only through `git show 1fbdb8ed:`.
Nothing was installed. This report is the only file I wrote in the lane.

## Verdict

C2 does change what kake knows on ground that was uncovered. `PROVINCE.md:100-103` listed Render web services and the
Blueprint as open, and `:111-120` now records the step. The new material is the health-check rules, the Docker
build-argument and secret-file rules, Blueprint identity by `name`, the "retains the current value" rule for omitted
fields, the `sync: false` behaviour, and a per-key reading of the lane's `render.yaml`.

All 40 quotes in the entry are exact substrings of the retained text. The render.yaml check is correct on every key it
covers. It has one real defect: it says a retained fact is missing (see condition d). It also leaves three wave-1
conditions short (b, h, and part of a). These are fixable defects, not grounds for rejection.

## Conditions from w1 point 4 (and points 3 and 5)

- **a) Key-by-key check: partly met.** These keys are mapped to S057 field text: `type`, `runtime`, `dockerfilePath`,
  `dockerContext`, `healthCheckPath` and `sync: false` (entry:57-64). Two items are not mapped:
  `name: ds4cc-marketplace-app` (render.yaml:3) has no bullet; the identity quote at entry:44 is not tied to line 3.
  The `envVars` bullet (entry:63) lists the variables but quotes no S057 field text for `key`/`value`.
- **b) Omitted keys and their new-service defaults: not met.** The safety half holds: entry:45 and entry:67 refuse to
  infer the live plan, region or trigger. The knowledge half is missing. The retained S057 has "Render uses 0.5c-512mb
  for a new web service", "Render uses commit for a new service.", "Render uses enabled for a new service." and, for
  region, "You can't modify this value after creation." (one hit each, checked with `grep -c -F`). None of these is in
  the entry. The fact that region cannot be changed after creation is operational and is lost.
- **c) `sync: false` caveat: met** (entry:47 and entry:64, both S057 sentences).
- **d) Port: not met, and the entry contains a false claim about its own sources.** entry:22 says "this entry did not
  retain the page that says how, so the mechanism (the PORT environment variable) is not stated from a source here."
  The retained S058 does state it: "The default value of PORT is 10000 for all Render web services.", "You can
  override this value by setting the environment variable for your service in the Render Dashboard ." and "If you
  bind your HTTP server to a different port, Render is usually able to detect and use it." As a result, entry:65 stops at "Whether Render's expected port is 10000 or 3000 … is a dashboard setting". With these
  quotes plus `server.ts:14` (`PORT ?? "3000"`), the sources support a stronger conclusion: [INFERENCE] without a
  dashboard override, the app reads PORT=10000 and binds the expected port, and `EXPOSE 3000` (Dockerfile:15) does
  not decide the port. `SKILL.md:820` already says "default 10000", so the entry and the skill differ on how much is
  sourced.
- **e) Health: met.** S060 success, cancellation, 15 s and 60 s quotes are at entry:35-38. `server.ts:193` confirms the
  `/health` route. Response time is tagged as unmeasured (entry:62).
  - Residual: entry:66 says both Host values "are in the server's list". `app.ds4cc.com` is in the list, because
    `server.ts:13,16` adds the hostname of `APP_ORIGIN`. But the live onrender host is only "a unique onrender.com
    subdomain" (S058). [INFERENCE] The file does not establish that it equals `ds4cc-marketplace-app.onrender.com`.
  - I did not verify whether the SDK's `allowedHosts` check (`server.ts:142`) also guards `/health`.
- **f) Docker build: mostly met.** The rules for build arguments, `.dockerignore` and secret files are at
  entry:29-30 and entry:61. I confirmed the COPY paths at Dockerfile:3,5,14 and the `.dockerignore` lines 1-11. The
  entry never says the Dockerfile has no `ARG`, which is the fact that keeps `OPENAI_APPS_CHALLENGE` out of the image.
- **g) "Always reachable" conflict: met** (entry:48, qualified by `renderSubdomainPolicy`). My scan flagged one quote
  as field-table text rather than prose: "disabled : The service is not reachable …". It is still a sentence.
- **h) Round-30 leads closed with cross-reference: not met.** S057 now holds three fields that settle open leads: "A list of custom domains
  for the service." (domains), "Required. The path to the directory that contains the static files to publish,
  relative to the repo root." (staticPublishPath) and "Configuration details for a static site's redirect and rewrite
  routes ." (routes). Yet three passages still call these unsettled or a lead: `render-static-sites.md:106-110` (domains), `:129-132`
  (staticPublishPath) and `:37` (whether a Blueprint can carry rules). The round-31 corrections section
  (`render-static-sites.md:141-162`) handles only routed defects 3 and 4. `publish-channels.md:101-102` is not
  cross-referenced either. The held corpus therefore contradicts what it now retains.
- **i) Gate quotes are prose: met.** The four counter quotes are prose sentences (c2_quote_truth output below).
- **j) States what it does not establish: mostly met.** See the scope line (entry:5), entry:45 and entry:67, and
  `SKILL.md:828-831`. The entry has no explicit statement that deploy state and dashboard attachment of
  `app.ds4cc.com` are not established. entry:66 assumes a verified custom domain only conditionally.
- **Point 3 (repeats): acceptable.** entry:23 repeats the onrender-plus-custom-domain fact already held from S052,
  with a cross-reference. entry:67 repeats the missing-`domains` inference from `publish-channels.md:101` without
  citing it. Neither is counted twice by the counter.
- **Point 5 (S061 kept out of C2): met.** The entry has no S061 quote; S061 appears only as a pointer at entry:23. The
  counter ids are S057-S060 only.

## Smallest safe correction (append-only, all quotes checked as exact substrings)

1. In `render-web-services.md`, supersede the inferences at entry:22 and entry:65 with the three S058 PORT sentences
   above, and state the [INFERENCE] binding conclusion from condition d.
2. Add new-service defaults, each marked *new service only*: the four S057 sentences in condition b. Map `name`
   (line 3) to entry:44. Note that the Dockerfile has no `ARG`. Optionally quote "If omitted, Render uses
   ./Dockerfile ." (S057) for the unquoted clause at entry:60.
3. In `render-static-sites.md`, add round-31 corrections that close `:37`, `:106-110` and `:129-132` with the three
   S057 field sentences in condition h, and cross-reference `publish-channels.md:101-102`. Record these as
   corrections, not as C2 count.

## Commands (cwd is the clone unless noted; TMPDIR set to the sandbox)

- `git clone -q …; git checkout -q 92235a0…`: exit 0. `git diff --stat fde133a 92235a0` shows only SCORECARD,
  receipts and the w2 spec/dispatch files.
- `python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision 92235a0…`: exit 0, `C2 4/4`; and
  `python3 -B .ufo/waves/round-31/c2_strict_checks.py --root . --revision 92235a0…`: exit 0, `C2 strict 5/5`.
- A stdlib quote scan of the entry: 40 curly quotes, 40 exact substrings, 1 field-table flag (g). The only bullet
  with no quote is entry:67.
- `grep -o/-c -F` context reads on `.ufo/waves/round-31/sources/S057-S060.txt`: exit 0. Every quote above comes from
  that output.
- In `/home/vgpnk/Projects/ds4cc-marketplace`: `git show 1fbdb8ed:{render.yaml,apps-sdk/Dockerfile,.dockerignore}`,
  `git show 1fbdb8ed:apps-sdk/src/server.ts | grep/sed`, and `git rev-parse` of the blobs. Results: render.yaml
  `d17ab7e5…`, Dockerfile `ee0b6381…`, server.ts `649726df…`, matching entry:52-54. Exit 0.

## Not verified

The live service (deploy state, port, onrender host, attached domains, plan, region; no request was made); whether
the MCP SDK host check applies to `/health` (SDK source not read); completeness of retained S057-S060 text.
