# Kake round 30 wave 2 — ReviewSkillRenderTable

Axes: lane operability + freshness; my judged axis: freshness.
Target: SKILL.md section "Render static-site triage — round 30" (SKILL.md:727-791 at 451e98fc8415edf10f41b2aad656318e7edc84ca), attacked row by row.

## Method
- Sandbox clone /fast/scratch/hyaku/kake-r30/w2/ReviewSkillRenderTable/clone (git clone of the lane, HEAD 451e98f). No file inside the lane written except this report.
- Extracted every "…" quoted span in the section — preamble, 8 rows x Check/Action/Cited-ids columns, and the "What this table does not settle" bullets (41 spans) — whitespace-normalized (the SKILL hard-wraps; the retained texts are single-line), then tested exact substring membership in the cited .txt, attributing each span to the nearest S0xx mention (before the span, or the trailing "(S0xx)").
- Read the full retained bodies S049.txt-S052.txt to judge whether each Action follows from the sources.
- Verified each S0xx.txt sha256 against receipts.json textSha256 (integrity of the text I quote-checked against).
- No network requests, no owned-site contact, no installs (none needed). Judged against retained text only, per bounds.

## Command record (all in the sandbox clone)
- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone` — exit 0
- python quote-census script over the section vs S049-S052 — exit 0, 41 spans, 41 exact, 0 failures
- `for s in S049 S050 S051 S052; do sha256sum ...; done` vs receipts.json — exit 0, 4/4 OK
  - S049 3604f8f5…d6f7, S050 1c413643…c5ed, S051 e98982ce…a27d, S052 6c1616f8…f769 — all match textSha256

## Per-row verdict
- Preamble — holds. "Render automatically updates your site with every push to your specified branch" and "Each site receives a unique onrender.com URL" are exact in S049; "custom domain can sit in front" matches S049/S052.
- Row 1 stale after push — holds. Both quotes exact in S049; "published whole" follows from "each build is fully atomic. As soon as a build succeeds, we deploy it…". The stale-cause instruction is marked [INFERENCE — no source here names a cause…], and indeed no source names one, so the marker is honest. Nit: "Read the deploy status of that build first" is dashboard practice, not stated in S049; harmless, contradicted by nothing.
- Row 2 HTTP→HTTPS — holds. Both quotes exact (S049, S052); S049 places the redirect statement inside its "Redirects and rewrites" feature, supporting "do not spend a rule on the upgrade"; remainder marked [INFERENCE].
- Row 3 rule shadowed by file — holds. Both quotes exact in S050; "the file wins" is the source's "Render simply serves the resource at that path… protects against overwriting valid paths".
- Row 4 domain root — holds, one nit. Both quotes exact in S050. The source sentence continues "(such as /blog , or even / )", which the quote truncates; nothing the row asserts is reversed (root rules rejected; Source needs a path component), but the truncation hides that "/" is offered as a syntactically valid Source example — a reader could be surprised.
- Row 5 SPA deep links — holds. All three quotes exact in S050; the action is a verbatim source example: "Specify /* to match all paths" with example "/* → /index.html — All requests → /index.html"; redirect-for-moves and the 301 sentence exact; "Return 404 Not Found" is the real final step of the source's matching flow.
- Row 6 custom headers — holds. All four quotes exact in S051; the example `cache-control: public, max-age=86400` is verbatim from S051's normalized-response list. Nit: "normalized lower-case" — the source says "normalized" and shows lowercase examples; "lower-case" is read off the examples, not stated.
- Row 7 502 / verification — holds. Both quotes exact in S052; "Wait a few minutes and try again." is verbatim after each quote, supporting "treat as provisioning… wait". Nit: the row's "press Verify again" matches the verification half ("Click the Verify button"); for the 502 half the source's retry is revisiting the domain ("Try visiting your custom domain in a browser… try again"), not pressing Verify. Substance sourced, wording conflates the two retries. "confirm that DNS points at Render" is step 2 of the source's procedure.
- Row 8 onrender.com 404 — holds. Both quotes and the token renderSubdomainPolicy exact in S052 (yaml snippet "renderSubdomainPolicy: disabled", API field serviceDetails.renderSubdomainPolicy); the three re-enable channels in the action (Dashboard toggle / Blueprint render.yaml / Render API) are verbatim the source's configuration channels, and "You can re-enable the subdomain at any time" supports the action.
- "What this table does not settle" — holds. "opened once each at 2026-10-22T11:49Z (HTTP 200)" matches receipts.json (S049/S050 11:49:44Z, S051/S052 11:49:45Z, all status 200, finalUrl = the four declared render.com/docs URLs); the Rails-app quote is exact in S049; app.ds4cc.com as an existing web-service surface is grounded in corpus/knowledge/publish-channels.md (6 occurrences).

Quote census: 41/41 exact substrings with correct source attribution, 0 defects. The single initial "FAIL" in my script was its attributor mis-reading the range "S049–S052" in the preamble as citing S052; the SKILL cites (S049), which contains the span — script artifact, not a defect.

## Verdict
No row tells the reader anything the retained sources do not support or contradict; the two rows flagged as likely targets (502 and verification) are supported by verbatim wait-and-retry language. Findings are the four nits above (rows 1, 4, 6, 7), all cosmetic; none is a defect under the stated acceptance criterion.

## Residual risk / not verified
- Live-page freshness: not verified. Bounds forbid fetches this round; the reopen seat (ReopenS051S052) owns that. My verdicts are against retained text only.
- Retained text integrity verified by sha256 against receipts.json, not by re-deriving the text from S0xx.html.gz (the C2 counter seat owns that path).
- "Read the deploy status" (row 1) and "normalized lower-case" (row 6) rest on dashboard practice / source examples, not verbatim source words.
- I did not diff the SKILL table against corpus/knowledge/render-static-sites.md (other seats own that entry; my scope was the SKILL section).

Report: .ufo/waves/round-30/w2/ReviewSkillRenderTable.md
