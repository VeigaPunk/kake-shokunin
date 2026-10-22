# KakeR30.CriticFrontierWording — round-30 frontier wording, falsify seat

Target: the round-30 sections of `corpus/README.md` (273-286), `PROVINCE.md` (94-106), `SKILL.md`
(727-808) and `corpus/knowledge/publish-channels.md` "Round-30 Render recheck" (86-108), all at tip
`451e98fc8415edf10f41b2aad656318e7edc84ca` (working tree clean for these four files). Axis judged: freshness.
Read-only throughout. No network, no installs, no sandbox writes were needed (sandbox dir created, left empty).

## Summary

No sentence in these sections claims a live measurement, Core ground, or a gate that did not land; each
section says "no gate", "knowledge only" or "not Core". I found two real overstatements (findings 1 and 2) and
three smaller ones. The publish-channels recheck is accurate about `render.yaml`. Its only flaw is a line
range that leaves out the env-var lines it describes.

## Findings

1. MEDIUM, premature saturation: the "no owned Render static site" claim is stated as an absolute.
   - `corpus/README.md:276`: "no owned Render static site exists".
   - `PROVINCE.md:100-101`: "no owned property is a Render static site".
   - Evidence: the only grounding is wave-1 `.ufo/waves/round-30/w1/ScoutLocalRenderUse.md:9-10`
     ("No local checkout of an operator property deploys a Render static site"), and that same file at
     :175-176 keeps the residual: "a Render service configured only in the web dashboard, with no local file,
     would not be visible here."
   - Counterexample: S049 itself documents a dashboard-only creation path ("After you link your site's Git
     repo", "click Create Static Site"; `.ufo/waves/round-30/sources/S049.txt`). Nothing about that path
     appears in any local tree, and no Render account or dashboard inventory was read this round.
   - The entry itself is correctly scoped: `corpus/knowledge/render-static-sites.md:4` says it "asserts
     nothing about any owned site". The README and PROVINCE sentences go further than the evidence.
   - Smallest correction: "no owned property recorded in local checkouts or this lane's corpus is a Render
     static site (a dashboard-only site would not be visible)".

2. MEDIUM, dropped condition (contradicts the lane's own SKILL row): `corpus/README.md:276` says "every push
   to the deployed branch rebuilds the site atomically and invalidates the CDN caches".
   - S049 makes invalidation conditional: "As soon as a build succeeds, we deploy it and immediately
     invalidate our CDN caches" (S049.txt, "Immediate cache invalidation" section).
   - `SKILL.md:740` keeps that condition ("a build that succeeds is published whole") and tells the reader
     to treat a failed build as a build failure. The README line reads as if every push invalidates the
     cache, which is exactly the misreading that SKILL row warns against.
   - Smallest correction: "...rebuilds the site atomically; a successful build is deployed and invalidates
     the CDN caches".

3. LOW, identity stated stronger than `render.yaml` shows:
   - `corpus/README.md:280-281`: "the lane's one Render property, `app.ds4cc.com`, is a Docker web service".
   - `PROVINCE.md:102`: "(the `app.ds4cc.com` Docker service)".
   - The lane's own recheck says the Blueprint has no `domains` key, so `render.yaml` does not attach
     `app.ds4cc.com` (`publish-channels.md:100-101`, inference-tagged). In `render.yaml` the host appears
     only as the `APP_ORIGIN` value (`ds4cc-marketplace` blob `d17ab7e5`, line 10).
   - The link from host to service rests on other evidence: the round-23 live `/health` HOLD dated
     2026-10-21 (`publish-channels.md:71`) and the host allowlist in `apps-sdk/src/server.ts:15-20`, which
     adds the `APP_ORIGIN` hostname. "One" inherits the same dashboard-only blind spot as finding 1.
   - `SKILL.md:756-757` is scoped ("in this playbook") and is acceptable.
   - Smallest correction: "the lane's recorded Render service, `ds4cc-marketplace-app` (Docker, `APP_ORIGIN`
     `https://app.ds4cc.com`)".

4. LOW, the SKILL header row goes beyond S051: `SKILL.md:746` says "A header missing on one host but present
   on another is a path-scope question, not a per-domain question".
   - S051 says a header path is "matched with all custom domains attached to your site". It is silent on
     the `onrender.com` host, which is not a custom domain. So "present on onrender, missing on the custom
     domain" (or the reverse) is not settled by the source.
   - In the same row, "lower-case form" is read off the S051 example; the text only says "normalized".
   - Correction: tag both clauses `[INFERENCE]`, or limit the first to "across custom domains".

5. LOW, a categorical clause ahead of its tag: `SKILL.md:740` says "Render's own invalidation is not the
   cause". S049 says the platform invalidates; it does not prove invalidation never fails. The cell ends
   with `[INFERENCE]`, but this clause reads as fact. Correction: "is unlikely to be the cause".

6. LOW, citation range in the publish-channels recheck: `publish-channels.md:93-96` says "lines 2-7 still
   declare..." and then lists `APP_ORIGIN` and `ALLOWED_ORIGINS`. Those values sit at lines 9-10 and 13-14
   of the blob, not inside lines 2-7. Correction: "lines 2-7 and 9-14".

## Checked and holding (no overstatement)

- Recheck vs `render.yaml`:
  - Checkout `1fbdb8ed…`, blob `d17ab7e5…` and clean status all match.
  - `ALLOWED_HOSTS` is at lines 11-12, and lines 15-20 hold `OPENAI_APPS_CHALLENGE` (with `sync: false`),
    `MAX_UNAUTHENTICATED_SESSIONS` and `MCP_SESSION_IDLE_TIMEOUT_MS`.
  - There is no `domains` key and no `renderSubdomainPolicy`.
  - The S052 quote "Services with a custom domain also keep their onrender.com subdomain." is verbatim in
    S052.txt.
  - "HOLD" here is a local read: `main` equals the local `origin/main` ref `1fbdb8e` (committed 2026-10-21),
    with no fetch; the section says so ("Nothing live was fetched").
  - `server.ts:15-20` lists both `app.ds4cc.com` and the onrender host, which supports the recheck's
    inference.
- README rule-order, TLS and dashboard-header wording:
  - S050 has "Apply the first matching rule (starting from the top of the list) Return 404 Not Found".
  - S052 has "automatically creates and renews TLS certificates for all custom domains" and the HTTPS
    redirect.
  - S051 defines headers "in the Render Dashboard".
  - `render.yaml` and Blueprint appear in S050, S051 and S052 only in the navigation text, so README:283
    correctly lists the Blueprint fields as open.
  - README:284-285 "retained them as leads, not registry rows" holds: SOURCES S053-S056 are not Blueprint
    pages.
- SKILL citing-set registry: "41 cases" matches 41 fixture directories, and "(12)" uncovered codes matches
  (25 codes the gate can emit, 13 named by fixtures; my computed uncovered list equals SKILL:800-803).
  - "abbreviations included" is backed by the gate docstring at `scripts/citing_set.py:69-72,807`.
  - "overflowing numbers" is backed by `:529-534`.
  - The `O_NOCTTY` flag is at `:283-289`.
  - PROVINCE:104-106's "round-27 input families" matches SCORECARD.md:689,702.
- No section claims Core, a live measurement, or a Render gate.

## Commands (all exit 0)

- `git rev-parse HEAD; git rev-parse HEAD:render.yaml; git status --porcelain -- render.yaml; git cat-file -p d17ab7e5… | cat -n`
  in `~/Projects/ds4cc-marketplace`
- `git branch -vv; git for-each-ref refs/remotes; git grep -n ALLOWED_HOSTS HEAD; git show HEAD:apps-sdk/src/server.ts`
  in the same checkout
- `ls scripts/fixtures/citing-set | wc -l` → 41; a read-only Python pass comparing the gate's reason codes
  with the reasons named in `expected.json`; keyword-in-context Python over `.ufo/waves/round-30/sources/S049-S052.txt`
- `git rev-parse HEAD` (lane) → `451e98f…`; `git status --porcelain` on the four target files → empty

## Not verified

- I ran neither the gate nor the self-test, and no counters (other seats own those).
- No live state was checked for any Render host, and no dashboard was read.
- I did not re-fetch any source; the retained S049-S052 text was taken as given.
