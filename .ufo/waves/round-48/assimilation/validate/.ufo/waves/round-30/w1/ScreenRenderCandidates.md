# ScreenRenderCandidates — round 30, wave 1: screened-and-rejected Render candidates (S053-S055)
Seat: KakeR30.ScreenRenderCandidates (leaf, axis freshness). Lane: /home/vgpnk/Projects/shokunin/kake-shokunin.
Draft only: nothing landed in the lane except this report. Sandbox: /fast/scratch/hyaku/kake-r30/w1/ScreenRenderCandidates/.
## What I built
Three non-primary candidates on Render static sites, opened once each by ordinary GET (python urllib, one request
per URL, no browser, no challenge bypass), each screened to `rejected` or `queued` with a reason, a flip condition
and one located quote of at most 25 words; the matching `corpus/SOURCES.md` rows S053-S055 (11 cells) and the
matching `## Gate` lines for `corpus/lessons/round-30.md`. This is the round-28 routed defect 4 step: the reject
sample comes from the round's own source gate, not from outside it.

## Candidates opened (one GET each) and outcome
| id | URL | HTTP | body sha256 | text sha256 | outcome |
|---|---|---|---|---|---|
| C1 | https://dev.to/stephengade/how-to-deploy-static-website-for-free-on-render-with-custom-domain-4efo | 200 | 3116e46976a94540d739e079eceee5b0a965f0bcf2302d42db9ba62c9cb0ee24 | f5ce16708c5d768bd6c75b85779ed0e8d19743e99c492dcbd65bb1834c782704 | S053 rejected |
| C2 | https://www.namesilo.com/blog/en/dns/how-to-connect-a-custom-domain-to-rendercom | 200 | 8e8015af9c4e971760dc6204000f7f526a57ec2c313b8efe65e076a510db3984 | ff717649deb3caa25a419d9843509ad6a4e5746682c0fdbb6460a7506c6341d9 | S054 rejected |
| C3 | https://docs.astro.build/en/guides/deploy/render/ | 200 | 4bcbde3ec28ce9efa8d8ffd61c7b694c873164ee6560cab90a49919b133b7c27 | b793f9e7ae55c9253c13b3066216e934c1700c999526966e4ea5eff53b424dd4 | S055 queued |
| — | https://stackoverflow.com/questions/74223164/i-cant-go-directly-to-a-url-on-my-site-after-deploying-to-render | 403 | 33529917c396f494 | 56b19218bc8f | not opened (bot challenge), no row |
Requested 2026-10-22T12:06:47Z-12:08:30Z. The Stack Overflow body is a Cloudflare "Just a moment..." challenge page,
not the question; it was not opened by any other means and has no row, as in round 29. Everything below is a draft.

## Drafted registry rows (append after the S048 row)

```
| S053 | DEV Community: How to Deploy Static Website for FREE on Render with Custom Domain — https://dev.to/stephengade/how-to-deploy-static-website-for-free-on-render-with-custom-domain-4efo | community | C | A 2023 third-party tutorial of the Render static-site dashboard flow | How to Connect Custom Domain Name to Render section; post dated Aug 5, 2023; opened 2026-10-22 | REJECTED: the tutorial's one durable point, the catch-all rewrite to /index.html, is already carried by S050, and its custom-domain step is superseded by S052, which says Render automatically adds the corresponding www subdomain and redirects it to the root domain and never names an ALIAS record; flip: a current tier-A Render page names the ALIAS record the tutorial tells the reader to create, or the tutorial is refreshed to the current dashboard flow | rejected | 2026-10-22 | 90d | — |
| S054 | NameSilo blog: How to Connect a Custom Domain to Render.com — https://www.namesilo.com/blog/en/dns/how-to-connect-a-custom-domain-to-rendercom | community | C | Apex and www DNS record values for a Render custom domain, as one registrar states them | Step 2 Configure DNS at NameSilo section and the opening summary; page dated 7/8/2026; opened 2026-10-22 | REJECTED: the post pins an apex A-record address, 216.24.57.1, that no opened Render primary states; S052 routes DNS setup through per-provider guidance and publishes no address, so the value would enter the corpus from a registrar blog alone; flip: a current tier-A Render page publishes that apex address and the post matches it | rejected | 2026-10-22 | 90d | — |
| S055 | Astro Docs: Deploy your Astro Site to Render — https://docs.astro.build/en/guides/deploy/render/ | docs | A | Astro's own build command and publish directory for deploying an Astro site to Render; not Render platform semantics | How to deploy section, Build Command and Publish Directory lines; opened 2026-10-22, the page shows no revision date | Astro's own recipe for a Render static site is build command npm run build with publish directory dist, or dist/client when pages are rendered on demand | queued | 2026-10-22 | 90d | — |
```

## Drafted Gate lines (inside `## Gate` of corpus/lessons/round-30.md)

```
- S053 (C1) — https://dev.to/stephengade/how-to-deploy-static-website-for-free-on-render-with-custom-domain-4efo — accessed 2026-10-22, HTTP 200 — **rejected**: its one durable point, the catch-all rewrite to /index.html, is already carried by S050, and its custom-domain step names an ALIAS record that S052 does not; quote “Grab your CNAME and ALIAS to add to your domain name”.
- S054 (C2) — https://www.namesilo.com/blog/en/dns/how-to-connect-a-custom-domain-to-rendercom — accessed 2026-10-22, HTTP 200 — **rejected**: it pins an apex A-record address, 216.24.57.1, that no opened Render primary states; quote “Add an A record: Type: A Host: @ Value: 216.24.57.1 TTL: 3600”.
- S055 (C3) — https://docs.astro.build/en/guides/deploy/render/ — accessed 2026-10-22, HTTP 200 — queued, tier A scoped to Astro's own recipe, so the flip condition is that a current tier-A Render page states the same build and publish values for an Astro site; quote “Build Command: npm run build Publish Directory: dist , for static sites”.
```

Quote word counts: S053 11, S054 12, S055 12 (limit 25). Each is an exact substring of that candidate's own retained
text under the lane's text rule; the S055 quote carries the tag-removal artifact "dist , for static sites".

## Commands run and observed output
1. Fetch, one GET per URL, TMPDIR inside the sandbox: `TMPDIR=<sandbox> python3 -B fetch.py` (plus fetch2-5.py).
   Exit 0 each. 15 requests: 12 HTTP 200, 2 HTTP 403 (Stack Overflow, reddit), 1 HTTP 404 (a freeCodeCamp URL variant
   that does not exist). Quote verification over the retained texts: exit 0, `S053 11 True`, `S054 12 True`,
   `S055 12 True` (words, exact substring), control quotes also True.
2. Rehearsal in a sandbox clone of the lane with the three drafted rows, stub S049-S052 rows, a stub entry and
   the drafted lesson:
   `python3 -B .ufo/waves/round-29/verification/reject-path/reject_path_check.py --registry corpus/SOURCES.md
   --lesson corpus/lessons/round-30.md --entry corpus/knowledge/render-static-sites.md --screened-dir
   <sandbox>/screened --primary-dir .ufo/waves/round-30/sources` -> exit 0, `screenedCandidates 3`,
   `rejectedScreenedCandidates 2`, `passed 3`, no problems on any row. Five mutations of that check each exit 1: no
   flip clause on S053; S053 status `queued` while the lesson marks it rejected; S054 citing S047 (not tier-A
   mined) instead of S052; one letter changed in the S053 quote; the S053 URL pasted into the entry. Restored
   baseline exit 0 again.
3. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md --today
   2026-10-22` on the rehearsal registry -> exit 0, only `W04` (pre-existing S033 duplicate URL). No freshness-sweep,
   probe-delta or live_snapshot run in any mode.
4. `python3 -B .ufo/waves/round-30/c2_quote_truth.py --root . --revision HEAD` on the rehearsal commit -> exit 0,
   `passed 4 / 4`, `controlBroken false`; with one letter of the S052 Gate quote changed it drops to `3/4`, exit 1,
   and returns to 4/4 when restored.

## Gates, evidence, touched surfaces
- Screened receipts with sha256 of body and text: .../screened/receipts.json; retained bodies and texts
  .../screened/C{1,2,3}.html.gz and C{1,2,3}.txt; sha256 of each copied file equals its receipt (checked True). All 15
  raw request receipts, including the 403 and 404 cases: .../sources/receipts.json. Draft rows
  .../deliverable/rows.md (sha256 bbc1a23cccd54c0...), registry with stubs .../deliverable/SOURCES-draft.md, checks
  .../deliverable/reject-path-check.json and .../deliverable/c2-counter-on-draft.json.
- Reason check against the primaries: the S052 retained text (10,157 bytes) has `216.24` 0 times, `ALIAS` 0 times
  and `load balancer` 0 times; it states Render uses IPv4 and asks for AAAA records to be removed. The S050 text has
  `index.html` 4 times, so the catch-all rewrite S053 repeats is already primary ground. Owned-property check: the
  only pinned host in corpus/knowledge/freshness-pins.json is veigapunk.github.io; none of the requested hosts
  matches it or any owned domain.
- Lane: only this report file; the other lane modifications in `git status` (PROVINCE.md, SKILL.md, corpus/SOURCES.md
  and friends) are other seats' work. No edit to corpus/SOURCES.md, corpus/lessons/round-30.md or
  corpus/knowledge/render-static-sites.md; no git or jj command in the lane; no request to any owned property.
- Out of scope: landing the rows and Gate lines (L1 integrates; the S049-S052 rows and Gate lines in my rehearsal
  files are stubs for the check only, sibling seats own the real ones); creating corpus/knowledge/
  render-static-sites.md and corpus/lessons/round-30.md, both absent from the lane tree, so the C2 counter cannot
  pass until the L1 creates them; the other candidate URLs I opened while searching (Cloudflare for Platforms, three
  render-oss skill files, the UMD course page, tldops, community.render.com, render.com/docs/community, reddit, two
  freeCodeCamp URLs), whose receipts are in sources/receipts.json.

## Findings for the L1
1. The reject-path witness reads candidate text from `<screened-dir>/C<N>.txt`, N from the `(C1)` marker in the Gate
   line. If the L1 lands S053-S055, put the texts at .ufo/waves/round-30/sources/screened/C1.txt, C2.txt and C3.txt
   with the receipts beside them, or the witness reports "no retained text for candidate".
2. S053's reject cites S050 and S052 in its teaches cell. The witness requires every cited primary to be a tier-A
   mined row with retained text, so S050 and S052 must land as `mined` tier A, not `queued`.
3. S055 is queued with tier A scoped to Astro's own recipe. Round 29's S048 (Hugo docs) went the same way but the L1
   set that tier; tier C here is a one-cell edit if the L1 prefers it.
4. The dev.to post is dated Aug 5, 2023 and the NameSilo post 7/8/2026; both dates sit in the anchor cell, so each
   rejection's freshness is checkable without reopening.
5. A Render forum thread cannot be the source: the old forum is retired, https://community.render.com/ returns a
   redirect page to render.com/docs/community, whose retained text says the community moved to Discord. That is
   why no forum row exists and the Stack Overflow question is the only unopened candidate. The Astro guide shows no
   revision date, so its anchor names the opened date and the two build lines only.

## Artifacts
All under /fast/scratch/hyaku/kake-r30/w1/ScreenRenderCandidates/: screened/ (C1-C3 bodies, texts, receipts.json),
sources/ (all 15 raw request receipts and bodies), deliverable/ (rows.md, lesson-draft.md, SOURCES-draft.md,
reject-path-check.json, c2-counter-on-draft.json). This report: /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-30/w1/ScreenRenderCandidates.md. Tooling: none installed or upgraded this seat.