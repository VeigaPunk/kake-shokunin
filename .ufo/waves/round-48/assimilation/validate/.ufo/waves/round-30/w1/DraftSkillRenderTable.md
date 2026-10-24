# Round 30, wave 1 — DraftSkillRenderTable (scribe, freshness axis)

**Seat:** `KakeR30.DraftSkillRenderTable` (r30-build). **Deliverable:**
`/fast/scratch/hyaku/kake-r30/w1/DraftSkillRenderTable/table.md` (paste-ready
SKILL.md section + quote checks).

**What I built.** A SKILL.md decision table `## Render static-site triage —
round 30`, 8 rows, modelled on the round-29 table
(`SKILL.md:699` `## Project-site base-path triage — round 29`, columns
`| Symptom | Check | Remedy | Cited ids |`). Every row cites one or more of
S049–S052 and carries a located quote from the retained text. Insertion point
for the L1: end of `SKILL.md`, after the round-29 gate registry (file ends at
line 725 today).

**Column-head note:** the brief says “action”; the draft names the fourth
column `Action` and keeps `Symptom | Check | Cited ids` from round 29. Rename
to `Remedy` for strict round-29 parity.

**The draft (verbatim, from `table.md`):**

| Symptom | Check | Action | Cited ids |
|---|---|---|---|
| The site still serves the previous release after a push to the deployed branch | Read the deploy status of that build first. S049: “each build is fully atomic”, and “we deploy it and immediately invalidate our CDN caches so your users always see the latest working version of your site” — a build that succeeds is published whole and its CDN caches are invalidated at once | A failed build is fixed as a build failure, not as a caching problem. If the build succeeded and the old bytes are still served, Render's own invalidation is not the cause: look for a CDN, proxy or service worker in front of the site, and for a different branch serving the domain. [INFERENCE — no source here names a cause for stale content after a green build] | S049 (Immediate cache invalidation): “each build is fully atomic”; “we deploy it and immediately invalidate our CDN caches so your users always see the latest working version of your site” |
| A plain HTTP request is not upgraded to HTTPS | Both pages state this as platform behaviour: S049 “Render automatically redirects HTTP traffic to HTTPS”; S052 “All HTTP traffic to a custom domain is automatically redirected to HTTPS” | Do not spend a redirect rule on the upgrade — the platform already does it. If the upgrade does not happen, the request is probably not reaching the Render site (for a custom domain: DNS and verification status), or something in front answers first. [INFERENCE] | S049 (Redirects and rewrites): “Render automatically redirects HTTP traffic to HTTPS”; S052 (Custom Domains on Render): “All HTTP traffic to a custom domain is automatically redirected to HTTPS” |
| A redirect or rewrite rule has no effect on a path that has content | S050: “Render does not apply redirect or rewrite rules to a path if a resource exists at that path” — “Instead, Render simply serves the resource at that path” | Rename or delete the file that occupies the path, or point the rule at a path with no resource. A rule cannot shadow a file that is already deployed; the file wins | S050 (Rule matching and ordering): “Render does not apply redirect or rewrite rules to a path if a resource exists at that path”; “Instead, Render simply serves the resource at that path” |
| A rule for the site root (`/`) cannot be created, or a root rule never fires | S050: “You can't apply redirect/rewrite rules to your domain root”, and “Each Source requires at least one URL path component” | Put the wanted behaviour in the content at the root, or in a rule whose Source carries at least one path component. The domain root is out of scope for rules | S050 (Which action to use?): “You can't apply redirect/rewrite rules to your domain root”; “Each Source requires at least one URL path component” |
| Deep links in a client-side-routed app (react-router, Vue Router) answer 404 | S050 names this case: “you'll handle all requests from a single path like /index.html”; its matching flow ends “Return 404 Not Found” when no rule matches a path | Add a rewrite from `/*` to `/index.html` so every unmatched path serves the app shell. Keep the redirect action for real moves: a redirect “Instructs the browser (or any other client) to switch URLs to the rule's destination via a 301 Moved Permanently response code” (S050) | S050 (Which action to use?, Rule matching and ordering): “you'll handle all requests from a single path like /index.html”; “Return 404 Not Found”; “Instructs the browser (or any other client) to switch URLs to the rule's destination via a 301 Moved Permanently response code” |
| A custom response header is missing, or missing only on the custom domain | S051: “Because static sites don't have a server-side component that can inject custom HTTP response headers”, so headers are defined in the dashboard; “The header path must be a relative path without the domain”; “It will be matched with all custom domains attached to your site”; “The header key is normalized and the value is appended to it to form the response” | Give the header a relative path (no domain in it) so it covers the custom domain as well, and read the response in its normalized lower-case form (`cache-control: public, max-age=86400`). A header missing on one host but present on another is a path-scope question, not a per-domain question | S051 (HTTP Headers for Static Sites, Header syntax): “Because static sites don't have a server-side component that can inject custom HTTP response headers”; “The header path must be a relative path without the domain”; “It will be matched with all custom domains attached to your site”; “The header key is normalized and the value is appended to it to form the response” |
| A newly added custom domain answers 502 Bad Gateway, or verification never completes | S052: “If verification fails, your DNS settings might not have propagated yet”; “If you see a 502 Bad Gateway error, Render might still be updating routing rules for your service” | Treat both as provisioning, not as a broken site: wait a few minutes and press Verify again, and confirm that DNS points at Render. A 502 in the first minutes after adding the domain is the documented state, not a verdict | S052 (3. Verify your domain): “If verification fails, your DNS settings might not have propagated yet”; “If you see a 502 Bad Gateway error, Render might still be updating routing rules for your service” |
| The old `onrender.com` hostname now answers 404 after a custom domain was added | S052: “After you disable your onrender.com subdomain, all requests to it receive a 404 response” — “These requests do not reach your service”; the switch is `renderSubdomainPolicy: disabled` (dashboard: Render Subdomain → Disabled) | If the subdomain was disabled on purpose, the 404 is the expected result, not a fault. Re-enable it (dashboard toggle, `render.yaml` field or API) when the fallback host is wanted again | S052 (Disabling your onrender.com subdomain): “After you disable your onrender.com subdomain, all requests to it receive a 404 response”; “These requests do not reach your service”; “renderSubdomainPolicy” |

The draft also carries a preamble paragraph (Knowledge pointer, S049–S052, no
live request) and a closing `### What this table does not settle` block: the
four pages are platform docs, the fleet's Render surface (`app.ds4cc.com`,
`ds4cc-marketplace-app`) is a web service and S049 says a dynamic site belongs
on a web service, and the rows do not cover build output, the repository or the
DNS console.

**Commands run (all read-only over the lane; nothing in the lane was modified
except this report):**

| Command (cwd) | Exit | Observed |
|---|---|---|
| `python3 -B check_quotes.py` (sandbox) | 0 | `33/33 candidate quotes pass; 9/9 alternates pass` |
| `python3 -B verify_table.py` (sandbox) | 0 | `42/42 drafted quotes are exact substrings of one retained text` |
| `python3 -B check_quotes.py` (first run, before the fix) | 1 | `27/28 candidate quotes pass` — one candidate of mine read “the onrender.com subdomain”; the retained text says “your onrender.com subdomain”. Corrected, then 33/33. |

**Quote checks (details).** Rule identical to the round-30 counter
`.ufo/waves/round-30/c2_quote_truth.py`: collapse whitespace in the retained
`.txt`, collapse the quote, test exact substring; the quote must be 1–25
words. `verify_table.py` pulls every curly-quoted span straight out of the
drafted block in `table.md` (not from a hand-kept list) and reports which
source ids contain it: every one of the 42 spans is contained in exactly one
retained text, and every span is at most 25 words (longest: 21 words).
Retained-text sha256 equals `receipts.json` `textSha256` for all four ids
(S049 `3604f8f5…`, S050 `1c413643…`, S051 `e98982ce…`, S052 `6c1616f8…`).
Section headings named in the `Cited ids` cells were also checked to occur in
the same retained text.

**Coverage.** Rows use S049 (rows 1–2), S050 (rows 3–5), S051 (row 6), S052
(rows 2, 7–8). All four ids of the round are used; no row cites an id outside
S049–S052. Alternates verified but left out under the 8-row cap, for the L1 to
take if wanted: dependency install / `SKIP_INSTALL_DEPS` (S049), custom-domain
quota and plan table (S049), wildcard domain and root domain (S052), AAAA
records (S052), wildcard capture in a rule (S050), CAA records (S052), TLS
auto-issue (S049), pull-request previews (S049). They are listed with their
verified quotes at the end of `table.md`.

**Out of scope / not done.** I did not touch `corpus/knowledge/render-static-sites.md`,
`corpus/lessons/round-30.md` or `corpus/SOURCES.md` (other seats own those; the
C2 counter needs a `## Gate` line with a curly-quoted quote per id — mine are
ready to hand over). I made no live request to any site, owned or public, and
ran none of `freshness-sweep.mjs`, `probe-delta.mjs` or `live_snapshot.py`. I
did not verify the draft inside `SKILL.md` itself, because the lane file is
operator/L1-owned.

**Tooling.** No install was needed or made: no pacman, uv or npm transaction
this seat, so nothing to record in the tooling ledger.

**Artefacts.**
`/fast/scratch/hyaku/kake-r30/w1/DraftSkillRenderTable/table.md` (draft),
`…/check_quotes.py`, `…/verify_table.py`, `…/quote-check.json`,
`…/table-verify.json`.
