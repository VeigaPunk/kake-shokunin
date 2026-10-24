# CriticLearningClaim — round 31 wave 1 (critic, freshness)

Seat `KakeR31.CriticLearningClaim`. Read-only attack on C2 as the learning claim, on drift, and on C1 scope.
Lane HEAD `a16602a`; ds4cc-marketplace read only through `git show 1fbdb8ed:<path>`. No network, no
owned-site request, no lane mutation. The only file written is this report. Nothing was installed.

## Verdicts

1. **C2 is uncovered PROVINCE ground: yes.** `PROVINCE.md:100-103` lists "Render web service deploys (the Docker
   service recorded for `app.ds4cc.com`) and the Blueprint file" as open. No knowledge entry holds Blueprint field
   semantics, port binding, Docker build behaviour or health-check behaviour. Searching `corpus/knowledge` and
   `corpus/lessons` for `web service|render.yaml|Blueprint` finds only the property record
   (`publish-channels.md:24-28, 86-109`), the round-1 audit row and the round-30 lesson/spot-check.
2. **C2 changes what kake knows: yes, but only if the entry does the property check (point 4 below).** Unlike round 30
   (where no owned property is a static site: `render-static-sites.md:137-139`), this is the platform of the lane's one
   Render property. The sources cover every key in `render.yaml`: the S057 text has `dockerfilePath` and `dockerContext`
   twice each, `healthCheckPath` twice (twice more in S060), `envVars` 16 times and `sync : false` 6 times, plus
   `type : web` and `runtime : docker`.
3. **C2 repeats round 30's surface: partly. This is a fixable defect, not grounds for rejection.** It overlaps the
   held material in three places, so the entry must cross-reference these and not count them again:
   - Web-service custom domains and the kept onrender.com host are already quoted from S052
     (`render-static-sites.md:56-57, 64-65`).
   - TLS issuance is already held (`:58-61`).
   - The `render.yaml` key read and the missing-`domains` inference are already done
     (`publish-channels.md:88-109`).

   The method repeats too: the counter is round 30's counter with new ids (`c2_quote_truth.py:3-6`), and it is the
   same vendor and the same four-page shape. Drift note: three Render-docs rounds in a row would be saturation,
   because accessibility conformance (`PROVINCE.md:104`) and crawl/JS canonical (`:22-23`) stay open. Round 31 is
   justified because it touches the owned property. A round 32 on Render should need a new reason.
4. **What the entry must contain to count.** The counter checks only sourcing (`SCORECARD.md:877-878`; check b needs
   just the id word below line 8, `c2_quote_truth.py:105`). The closure should therefore require:
   - a) **Key-by-key check of `render.yaml`** at blob `d17ab7e5`, lines 1-20. Each key must map to its S057 field
     text: `type: web`, `name`, `runtime: docker`, `dockerfilePath: ./apps-sdk/Dockerfile`, `dockerContext: .`,
     `healthCheckPath: /health`, and `envVars` with `key`/`value`/`sync: false`.
   - b) **Omitted keys with their documented new-service defaults**, each marked *new service only*. S057 says:
     "Render uses 0.5c-512mb for a new web service" (plan); "oregon (default for non- workflow services) … You can't
     modify this value after creation" (region); autoDeployTrigger "Render uses commit for a new service"; and
     renderSubdomainPolicy "Render uses enabled for a new service". **Counterexample:** every default is paired
     with "Render retains the current value for an existing service". The entry must not infer the live service's
     region, plan or deploy trigger from the file. `name` matters for identity: "If you add the name of an existing
     service to your Blueprint file, Render attempts to apply the Blueprint's configuration to that existing service."
   - c) **`sync: false` caveat for `OPENAI_APPS_CHALLENGE`** (render.yaml:15-16). Render prompts "only during the
     initial Blueprint creation … When you update an existing Blueprint, Render ignores any environment variables
     with sync: false" (S057).
   - d) **Port.** S058: "must bind to a port on host 0.0.0.0" and "The default value of PORT is 10000". The service
     reads `PORT ?? "3000"` (`apps-sdk/src/server.ts:14`) and listens on 0.0.0.0 (`:272`). `EXPOSE 3000`
     (Dockerfile:15) does not decide the port. [INFERENCE] Under Render it binds 10000.
   - e) **Health.** A `/health` route exists (`server.ts:193`, JSON response). S060 counts a check as successful on
     "a 2xx or 3xx status code within five seconds". Traffic stops after 15 s of failures and the instance restarts
     after 60 s. A deploy is cancelled when the check is not met "within 15 minutes". This is a static read only;
     it is not proof that the service is live.
   - f) **Docker build.** S059 translates env vars into build args and copies secret files into the build-context
     root. The repo's `.dockerignore` at 1fbdb8ed is `*` plus `!apps-sdk/…` and `!marketplace/…`, and the
     Dockerfile has no `ARG`. [INFERENCE] Neither the secret files nor `OPENAI_APPS_CHALLENGE` reach the image.
   - g) **Reconcile the S057 conflict.** The `domains` field says "Internet-accessible services are always reachable
     at their onrender.com subdomain". The next field, `renderSubdomainPolicy`, says `disabled` gives a 404 and
     "requires the service to have at least one custom domain" (this matches the held S052 quote at
     `render-static-sites.md:65`). The entry must not quote the "always reachable" sentence unqualified.
   - h) **Settle round-30 open leads only with explicit cross-reference.** S057 has a `domains` field (closes
     `render-static-sites.md:108-110` and `publish-channels.md:101-102` for the Blueprint side) and
     `staticPublishPath` (3 hits; closes `render-static-sites.md:129-132`). Record these as appended corrections,
     not as C2 count.
   - i) **Gate quotes should be prose, not YAML examples.** A 6-25 word span such as "key : ANTHROPIC_API_KEY sync :
     false # Prompt for a value in the Render Dashboard" passes check c but proves nothing.
   - j) **What the entry does not establish:** deploy state, the live host, a dashboard-attached `app.ds4cc.com`,
     and the actual region and plan.
5. **S061 must stay out of C2.** It is routed defect 4 (`round-30-verifier-spotcheck.md:277-280`). If the entry cites
   it, that is extra ground beyond the four declared ids and must not be credited to C2. Routed defect 3
   (`:271-276`, `render-static-sites.md` lines 26 and 53) is also outside C1 and C2. If it lands, report it
   separately.
6. **C1 is confined to the routed sandbox repair: yes.** The claim lists exactly N1, N2, N3, N5 and N6 from
   `round-30-verifier-spotcheck.md:250-262`. There is no N4 in that list, so nothing is dropped. The interface
   touches only the runner, the new hostile selftest and the `citing-set-hostile/` specs, not the gate
   `citing_set.py`. It does not reach routed item 2 (`:263-270`).

   The argv allowlist matches the gate parser: `citing_set.py:821-830` defines root, revision, population, ledger,
   json and selftest. The committed argv tokens are `--revision`, `--population`, `--ledger=`, `--roo` and `--rev`
   (cases 36, 37, 42-45), and all fall inside the allowlist, so control K1 stays reachable. `--r` (root or
   revision) is allowed by the contract and argparse rejects it as ambiguous, which is harmless.

   The `.git` rule ("any depth, before any copy") is compatible with cases 36, 37 and 45, which create `.git` only
   at run time through `git_init`. [INFERENCE] One residual risk: case 37 (root not the repository top level) must
   still pass when `--git-dir/--work-tree` are pinned to the work directory.

## Commands run (cwd `/home/vgpnk/Projects/shokunin/kake-shokunin` unless noted)

- `python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision a16602a…` → exit 1, stderr
  `C2 0/4 at a16602a…`. This matches the declared before value.
- `grep -o -F <key> .ufo/waves/round-31/sources/S05{7..9,60,61}.txt | wc -l` for the render.yaml keys → all exit 0.
  The counts are quoted above. `ALLOWED_HOSTS` has 0 hits in the sources (it is an app variable).
- Context extracts from S057, S058, S059 and S060 → exit 0. All quotes above are copied from that output.
- `git -C /home/vgpnk/Projects/ds4cc-marketplace show 1fbdb8ed:{render.yaml,apps-sdk/Dockerfile,.dockerignore}`
  and `git grep … 1fbdb8ed -- apps-sdk` → exit 0.
- `grep -n add_argument scripts/citing_set.py` and a stdlib listing of the 8 fixture `case.json` argv and setup
  entries → exit 0.

## Not verified

- No entry draft exists yet: `render-web-services.md` is absent at HEAD, and no `render-web-services*` turned up in
  the `/fast/scratch/hyaku/kake-r31/w1` seat directories. These verdicts are therefore preconditions, not a review
  of entry sentences.
- The C1 counter and the hostile selftest were not run, because no implementation exists yet. Case 37's behaviour
  under pinned git paths is unrun.
- Whether the Render service is deployed, its live plan, region and domains, and S057 completeness beyond the
  retained visible text. The 1.43 MB body reduces to 8,223 words of text, and the retained text holds the field
  table and examples used above.
