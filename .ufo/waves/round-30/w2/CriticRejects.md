# CriticRejects — round 30, wave 2 (falsify): screened rows S053, S054 (rejected) and S055 (queued)
Seat: KakeR30.CriticRejects (leaf critic, axis freshness). Attacked item: wave-1 seat ScreenRenderCandidates'
decisions, as landed at corpus/SOURCES.md:61-63 and corpus/lessons/round-30.md:55-57 (commit 451e98f).
Only lane write: this report. Sandbox: /fast/scratch/hyaku/kake-r30/w2/CriticRejects/ (get/, vt.py, tmp/).

## Verdict per row
| row | decision | tier | reason as written | flip condition |
|---|---|---|---|---|
| S053 | agree (rejected) | agree (C) | disagree in part | disagree: probably already met |
| S054 | agree (rejected) | agree (C) | agree literally, but incomplete | weak: may already be met; points at the wrong page |
| S055 | agree (queued) | agree (A, scoped) | agree, with one omission | disagree: missing from the row and aimed at the wrong evidence |

## Is S054's address claim really absent from S049-S052? Yes, within those four pages.
`216.24.57` occurs 0 times in the full retained HTML bodies of S049-S052, inline scripts and Next.js payload
included, not only in the visible text that wave 1 checked. `ALIAS` and `ANAME` also occur 0 times. The body
sha256 values match receipts.json (S052 59469467…e094c543, 371923 bytes).
Counterexample: the absence is a property of S052's overview page, not of Render's documentation. The DNS step
on S052 is a tab set whose "All other providers" tab is only a link, `href="/docs/configure-other-dns"` (found in
S052.html.gz next to configure-cloudflare-dns and configure-namecheap-dns). Nobody opened that page this round.
[INFERENCE, from memory, not opened] it is where Render states apex records, possibly the ALIAS/ANAME option
and an A-record address. So "no opened Render primary states" is true, but the row's "S052 … publishes no
address" reads as if Render publishes none.

## Evidence wave 1 had and left out
Wave 1 fetched C8, https://raw.githubusercontent.com/render-oss/render-pi-plugin/main/skills/render-domains/SKILL.md
(HTTP 200, body sha256 f1e306a2…0bd55; retained at /fast/scratch/hyaku/kake-r30/w1/ScreenRenderCandidates/sources/C8.html.gz).
It sits in Render's own GitHub org and carries `metadata: author: Render`. Its line 26 reads "Configuring
**DNS records** (CNAME, A, or ALIAS) with a provider". Line 55 reads "| **Apex** on other providers | A | `@` | Use
Render-provided IP (see Dashboard) |". Lines 60-62 link the same three provider pages. The wave-1 report does not
mention C8 in the reasons for S053 or S054.

## S053 (dev.to tutorial, 2023)
- Agree with rejected and tier C. Its only route fix, Source /* to Destination /index.html with action Rewrite, is
  in S050 ("/* /index.html All requests → /index.html"). As a 2023 third-party post it adds nothing durable.
- Disagree with "superseded by S052 … never names an ALIAS record". S052 names no record type for an ordinary
  domain at all, because it hands that step to the provider pages, so its silence says nothing about ALIAS.
  Render-authored C8 does name ALIAS. The www/root auto-redirect fact does not supersede a DNS record step. The
  tutorial's dashboard flow ("click Settings and scroll down … Enter your custom domain name and click Save")
  matches S052's current flow ("Settings page and scroll down to the Custom Domains section … Click Save"), so
  "superseded" is the wrong reason.
- Flip "a current tier-A Render page names the ALIAS record": C8 already names it, if a Render-authored GitHub
  skill counts as tier A. [INFERENCE] /docs/configure-other-dns may name it too.
- Smallest correction: give the reason as "duplicate of S050 for the rewrite; DNS record values belong to
  Render's provider pages, not to a 2023 tutorial". Drop "superseded by S052 … never names an ALIAS record".

## S054 (NameSilo blog, dated 7/8/2026)
- Agree with rejected and tier C (a registrar's marketing post). Further reasons the row could give: it says
  Let's Encrypt only, while S052's CAA section names both Let's Encrypt and Google Trust Services (pki.goog). It
  also says "Cloudflare does not support A records when proxying is enabled for Render", which no opened Render
  page states. The footer says ©2009-2025 next to a 2026 post date.
- Render-authored C8 points the other way from the blog's fixed value: it says "Use Render-provided IP (see
  Dashboard)" and pins no address. That backs keeping 216.24.57.1 out of the corpus.
- The flip condition may already be met on a page one link from S052 that nobody opened. A 90-day recheck
  without that page is the wrong target. Smallest correction: change the reason to "no opened Render page states
  it; /docs/configure-other-dns, linked from S052, was not opened", and make the flip "a GET of that page states
  the address and it matches". KakeR30.ReopenS051S052 declined to open that page (13:23Z) because its item
  names only the S051 and S052 URLs. My item allows only the three candidate URLs, so no seat in this wave
  holds it. Routed to the L1: a seat whose item names https://render.com/docs/configure-other-dns, one GET,
  settles the S053 and S054 flips.

## S055 (Astro docs recipe)
- Agree with queued and tier A scoped to Astro's own recipe. The "no revision date" anchor holds: the body has no
  last-updated marker.
- The flip condition lives only in the Gate line (lessons:57). The row (SOURCES:63) has none, unlike S053 and S054.
  The Gate's flip ("a current tier-A Render page states the same build and publish values for an Astro site")
  asks Render to confirm Astro's own output folder. Render is not the authority for that, and S049's list of
  framework deploy guides (deploy-create-react-app, docusaurus, gatsby, hugo, jekyll, nextjs-app, svelte, vue-js)
  has no Astro guide. Correction: put a flip in the row, tied to use (a kake entry cites it), or to the Astro page
  changing its values.
- Omission: the teaches cell repeats "or dist/client when pages are rendered on demand" without a caveat. S049
  says "Deploying a dynamic site, such as a Rails app? Create a web service instead of a static site." On a
  static site, on-demand pages cannot run. Add "on-demand pages need a Render web service (S049)" so the row is
  not read as Render behavior.

## Freshness recheck (one GET each, curl -sS -L --compressed, 2026-10-22T13:21:17Z-13:21:18Z, all exit 0)
| id | HTTP | live body sha256 | equals retained body | visible text sha256, lane rule | equals retained text |
|---|---|---|---|---|---|
| C1 | 200 | 5dd4eaaa…8b5 (87528 B) | no (same length) | f5ce1670…2704 | yes |
| C2 | 200 | 6e8970a0…45 (290201 B, was 290346) | no | ff717649…41d9 | yes |
| C3 | 200 | 4bcbde3e…7c27 (158829 B) | yes | b793f9e7…dd4 | yes |
The visible text of all three is unchanged since the wave-1 fetch (about 75 minutes earlier), so every quote
still holds. C2 still has `216.24.57.1` 12 times in its body.

## Commands (exit codes)
- rg/zcat scans of sources/S049-S052.html.gz and the screened C1-C3 text and bodies for 216.24.57, ALIAS, ANAME,
  A record, CNAME and the S052 tab hrefs: exit 0. Hits as reported above.
- sha256sum of decompressed bodies against receipts.json: all 7 match.
- curl GET of the three candidate URLs: exit 0 each. `python3 -B vt.py` (fetch_sources.py visible_text rule): exit 0.
  Word-level `diff` of live and retained text: empty for C1, C2 and C3.
- Read-only scan of the wave-1 sandbox bodies C1-C15: exit 1 from the loop's last test. Hits in C3 (NameSilo),
  C8 (render-domains) and C11 (dev.to) only.
- Message to KakeR30.ReopenS051S052: delivered. Reply: out of its bounds, not fetched.

## Not verified
- I did not open /docs/configure-other-dns, so whether it states 216.24.57.1 or ALIAS/ANAME is [INFERENCE].
- I did not decide whether a render-oss GitHub skill counts as tier A. That is the L1's call.
- I ran no counters (c1_reason_count, c2_quote_truth, reject_path_check) and no census.
- No request went to any owned property. I ran no freshness-sweep, probe-delta or live_snapshot. I installed nothing.
