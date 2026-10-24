# CriticEntryContrast — round 30, wave 2 (falsify)

Target: `corpus/knowledge/render-static-sites.md` section "How this differs from GitHub Pages behaviour already held in this corpus" (lines 68-97), as landed at 451e98f (file sha256 5371195991bd281a…). Axis judged: freshness. Leaf seat; no fetch, no subagent, no install, no lane file written except this report. Sandbox `/fast/scratch/hyaku/kake-r30/w2/CriticEntryContrast/` used only as TMPDIR; no deliverable files there.

## Verdicts

| # | Contrast | GitHub Pages side | Render side and inference | Verdict |
|---|---|---|---|---|
| 1 | Redirects | holds | overreach | overreach |
| 2 | Missing pages | holds | "plain" and the inference are overreach | overreach |
| 3 | Rewrites and client-side routing | absence holds | holds | holds |
| 4 | Response headers | absence holds | inference is overreach | overreach (inference only) |
| 5 | Custom domain authority | holds | understates the retained text; contradicts a sibling entry | overreach |
| 6 | Base path | holds | "say only" is wrong; the quote does not bear on base path | wrong (Render half) |
| 7 | TLS | absence holds | inference misses a retained Pages counterpart | holds, with gap |

All eight curly quotes in lines 68-97 are exact substrings of the retained texts S049-S052 (the script check is under Commands).

## Evidence and smallest correction per contrast

1. **Redirects.** The Pages side matches `ghp-subpath-spotcheck.md:69` (`/dir` → 301 → `/dir/`) and the round-23 HOLD at `:103`. The Render side says "Render's redirects are dashboard rules" and calls Render's mechanism "an explicit ordered rule set". The retained texts also document two automatic redirects that are not rules: S049 at offset 4479, "Render automatically redirects HTTP traffic to HTTPS", and S052 at offset 4213, where adding a root domain adds www with a redirect. The entry itself quotes the latter at lines 61, 63 and 91. No retained page says whether Render redirects `/dir` to `/dir/`. Correction: say "Render's *user-defined* redirects are dashboard rules", note the two platform redirects (S049, S052), and state that the slashless-directory case on Render is not documented in S049-S052.

2. **Missing pages.** The Pages side matches `ghp-subpath-spotcheck.md:74` and the round-23 HOLD at `:104` (c4). The quote "Return 404 Not Found" is at S050 offset 5816. "Plain 404" overreaches: the text gives only the status, not the body. Searching S049-S052 for `404` finds only that flowchart line and S052 offset 7117 (a disabled onrender subdomain). The inference "a custom 404 document on Render depends on a file in the published output" has no retained support, and it does not follow from the quote. A further counterexample: the catch-all rewrite `/* /index.html` (S050 offset 5083, "All requests → /index.html") makes a missing path serve `index.html` instead of returning 404. Correction: drop "plain", and replace the inference with "S049-S052 do not say whether Render serves a custom 404 document; a catch-all rewrite to `/index.html` (S050) replaces the 404 outcome."

3. **Rewrites.** The absence claim holds. A corpus-wide search for `rewrit` finds no Pages URL-rewrite mechanism. The hits are Kimi byte rewrites (`mirror-pitfalls.md:14`, `free-read-verbs.md:150`, `kimi-subpath-audit.md:13`), source-side href rewrites for Kimi (`publish-queue.md:60-61`, `kimi-subpath-audit.md:54`) and record-keeping uses ("not rewritten"). The parenthetical "byte rewrites on the Kimi mirrors" leaves out the href-rewrite mentions; that is precision only. The held Pages `404.html` fallback (c4) returns status 404, so it is not a rewrite, and "held here" is correctly scoped. A stronger Render quote exists: S050 offset 3894 names "a framework with client-side routing (such as react-router or Vue Router )" directly. This change is optional.

4. **Response headers.** The absence claim holds. Searching `corpus/` for `_headers|cache-control|x-frame|content-security|http-equiv|max-age|last-modified|x-github|strict-transport` finds Pages header material only in `ghp-etag-anatomy.md` and `publish-queue.md:26` (ETag and last-modified, both server-generated). The parenthetical leaves out last-modified, which is harmless. The inference "header rules are a Render-only capability among the two platforms the lane holds" overreaches in two ways. First, it turns absence from the corpus into a platform fact, and no registered source says Pages lacks custom headers. Second, the lane holds three hosting surfaces, not two (`publish-channels.md:24` Render and `:30` Kimi, besides Pages). Correction: "the corpus holds no Pages counterpart to these rules."

5. **Custom domain authority.** The Pages side matches `ghp-custom-domain.md:7-10` and `:18-23` (S005, S003, S007). The quote "Add your domain in the Render Dashboard ." is in S052. "The four retained pages describe only that dashboard path" is literally true for *adding* a domain. However, S052 offsets 6320-6712 list "Render Dashboard / Blueprint (render.yaml) / Render API" as the ways to configure the custom-domain-section setting `renderSubdomainPolicy`. So the retained page already shows that a Blueprint YAML file can carry a domain-related setting, and "`render.yaml`, not retained this round" understates the retained evidence. Separately, `publish-channels.md:100` (same commit 451e98f) concludes "The file has no `domains` key, so `app.ds4cc.com` is not attached by this Blueprint". That conclusion rests on the very `domains` field this entry calls an unretained scout report and an open question. Two entries from the same round disagree on whether that fact is held. Correction: either register and retain the Blueprint reference page, or mark `publish-channels.md:100` as an [INFERENCE] resting on an unregistered scout report. In this entry, also cite S052's Blueprint/API channel for the subdomain policy.

6. **Base path.** The Pages side matches `pages-base-path.md:11-15`, `:20` and `:40` (S040, S041, S043). "Name no subpath" holds by search: `subpath` does not occur in S049-S052. "And say only that adding a root domain adds the www subdomain with a redirect" is wrong. The pages say much more about hosts, and the quoted root/www pairing has nothing to do with base path. The retained sentence that does bear on it is S049 offset 3139: "Each site receives a unique onrender.com URL". That is a per-site host, not a shared owner host with a repository subpath. It still does not state the published root path, so the closing inference ("not settled here") can stay. Correction: replace the S052 quote with that S049 quote and delete "say only".

7. **TLS.** The absence claim holds as worded. Searching `corpus/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md` and `README.md` for `certificat|let's encrypt|TLS|ACME|enforce https|HSTS` finds only Render material (`render-static-sites.md`, `SOURCES.md` S052 row, `README.md:277`, `lessons/round-30.md:46`, `SKILL.md:741`, `PROVINCE.md:100`). The two other hits use "certificate" in an unrelated sense (`static-canonical-preflight.md:71`, `lessons/round-27-verifier-spotcheck.md:63`). The gap: S005, which this same sentence cites, has retained round-26 bytes containing a Pages HTTPS counterpart. In `.ufo/waves/round-26/fetched/text/S005-1.txt` (sha256 b2a7d47d7193dd2f…), offset 5795 reads "Optionally, to enforce HTTPS encryption for your site, select Enforce HTTPS . It can take up to 24 hours before this option is available." That passage sits outside the S005 row anchor ("step 4") and is not in corpus text, so the "cannot supply" claim is narrowly true. Still, the strongest contrast available locally (Pages HTTPS is opt-in; Render's is automatic, per S052 offset 3158) is missed. Correction: optional. Note the opt-in versus automatic contrast and cite it as S005's retained round-26 bytes outside the row anchor, or widen the S005 anchor.

## Impacted axes

Freshness (the knowledge held and its provenance): contrasts 1, 2, 4 and 6 assert more than the retained texts say; contrast 5 shows the same fact held in one entry and called open in another; contrast 7 leaves an available counterpart unused. Operability: none, since no gate or script is involved. None of these needs the canonical judge to reject a tradeoff. Each is a wording fix inside the entry, plus one wording fix in `publish-channels.md:100`.

## Commands run (cwd `/home/vgpnk/Projects/shokunin/kake-shokunin` unless noted; TMPDIR set to the sandbox)

- `ls .ufo/waves/round-30/sources/; mkdir -p <sandbox>; git log -1 --format=%H; git status --short` exited 0. HEAD is 451e98f…; untracked wave-2 files only.
- An inline `python3 -B` keyword-context scan over `.ufo/waves/round-30/sources/S049-S052.txt` exited 0 (offsets quoted above).
- An inline `python3 -B` check that every curly quote in lines 68-97 is a substring of its cited source exited 0: 8 of 8 OK.
- An inline `python3 -B` HTML-to-text scan of `.ufo/waves/round-26/fetched/S003-1.raw.gz` and `S005-1.raw.gz` for HTTPS, certificate and header exited 0.
- An inline `python3 -B` offset pin for S005-1.txt, S049, S050 and S052, plus `sha256sum`, exited 0.
- Read-only Grep and Read tool searches over `corpus/` and the top-level lane files, with the patterns named above.

## Not verified

I did not run `c2_quote_truth.py` (another seat's job). I fetched nothing, so no claim here is about live GitHub Docs or Render Docs. I did not check whether Render serves a custom `404.html` or redirects `/dir` to `/dir/` (no retained page covers either). I did not open the Blueprint reference page; it is not retained.
