# ReviewEntryHeadersDomains: round 30, wave 2 (falsify)

Reviewer: KakeR30.ReviewEntryHeadersDomains. Lane: /home/vgpnk/Projects/shokunin/kake-shokunin. Axis: freshness. Read-only on the lane. No network. No subagents.
Target: corpus/knowledge/render-static-sites.md lines 46–66 ("Custom response headers" and "Custom domains and TLS"). Each sentence was checked against retained S051 and S052, and against S049 for the one TLS sentence that cites it. Plan- and price-dependent statements were checked too.
Sandbox: /fast/scratch/hyaku/kake-r30/w2/ReviewEntryHeadersDomains/ (check.py to check5.py, their *.out files, retained_text_norm.json).

## Bottom line
- All 23 curly-quoted spans in the two sections are exact substrings of the cited source. None is fabricated or mis-cited.
- One claim contradicts its own quote (L64, "stops answering"). Three wordings go beyond their source (L48, L52, L53). Material omissions sit in the wildcard rules (L51, L60, L63, L65, L66).
- No sentence in lines 46–66 states a plan limit or a price as fixed. The plan allowance and the $0.25 overage are absent. That is a coverage gap, not a misstatement.

## Sentence table
Verdicts: OK = quote exact and claim matches. NARROW = true but drops a qualifier from the same page. DRIFT = wording the cited text does not state. WRONG = contradicted by its own quote. OMIT = material omission. Quotes are exact fragments; full spans are checked by check4.py.

| Line | Entry sentence (claim) | Quote (source) | Verdict |
|---|---|---|---|
| 48–49 | Static sites have no server-side component to inject headers, so headers are declared in the dashboard | S051 “you can define response headers for your static sites in the Render Dashboard .” | DRIFT, low: the page names the dashboard as a route; it has no “only” or “exclusive” (0 hits), so “declared in the dashboard” must not read as the sole route |
| 50 | A header rule is a relative path without the domain | S051 “The header path must be a relative path without the domain.” | OK |
| 50 | it applies to every custom domain on the site | S051 “It will be matched with all custom domains attached to your site.” | OK (silent on the onrender.com host; the entry does not extend to it) |
| 51 | Paths may be wildcards | S051 “You can use wildcards to match arbitrary request paths.” | OK; OMIT, medium: “/*.css Matches /tokens.css and /mode.css , but not /assets/theme.css” and “/**/*.css Matches /assets/theme.css but not /tokens.css”. Neither rule alone covers both files |
| 52 | The header name is matched case-insensitively | S051 “The name is the case-insensitive name for the header.” | DRIFT, low: the page says the name is case-insensitive; “matched” is the entry's word |
| 52 | the value is sent unchanged | S051 “The value of the header is sent as-is in the response.” | OK |
| 53 | The response carries the normalized lowercase name with the value appended | S051 “The header key is normalized and the value is appended to it to form the response: cache-control: public, max-age=86400 …” | DRIFT, low: the page says “normalized”; “lowercase” is read from its example (Cache-Control in, cache-control out). Mark [INFERENCE] or cite the example |
| 57 | Only web services and static sites take a custom domain | S052 “Only web services and static sites support custom domains.” | OK |
| 57 | a service that has one keeps its default hostname | S052 “Services with a custom domain also keep their onrender.com subdomain.” | OK (default state; the switch-off is at L64) |
| 58 | The steps are add, configure DNS, verify | S052 “Add your domain in the Render Dashboard .” / “Configure DNS with your domain's provider.” / “Verify your domain in the Render Dashboard.” | OK |
| 59 | Verification is an explicit dashboard action | S052 “Click the Verify button next to your custom domain.” | OK |
| 59 | on success the certificate is issued | S052 “If verification succeeds, Render issues a TLS certificate for your domain and updates the verification status:” | OK; OMIT, low: “If verification fails, your DNS settings might not have propagated yet.” and the 502 note (“Render might still be updating routing rules”) |
| 60 | Certificates are issued and renewed automatically, wildcards included | S052 “Render automatically creates and renews TLS certificates for all custom domains, including wildcard domains .” | OMIT, medium: S052 makes wildcard setup conditional: “This configuration requires setting all of the following CNAME DNS records with your provider:”, including _acme-challenge (“Enables Render to manage certificate issuance and renewal for your wildcard domain via Let's Encrypt.”) |
| 60 | platform-wide: Let's Encrypt and Google Trust Services | S049 “Render uses Let's Encrypt and Google Trust Services to automatically issue and renew TLS certificates for every site and service.” | OK. Freshness: snapshot-bound (2026-10-22). S049 adds “TLS certificates are always included for free.”, not quoted here; nothing here depends on it |
| 61 | Plain HTTP is redirected to HTTPS | S052 “All HTTP traffic to a custom domain is automatically redirected to HTTPS.” | OK (the paraphrase drops “to a custom domain”; the section scope holds it) |
| 62 | DNS configuration must not leave AAAA records behind | S052 “Remove any AAAA records from your domain while configuring DNS. AAAA records map to an IPv6 address, and Render uses IPv4.” | OK. Freshness: “Render uses IPv4” is a present-tense platform fact pinned to the snapshot |
| 63 | Adding one half of a domain pair adds the other with a redirect | S052 “If you add a www subdomain (e.g., www.example.org ), Render automatically adds the corresponding root domain and redirects it to the www subdomain.” | OMIT, medium: direction dropped. The host you add is the redirect target. For the root case S052 says the www host “redirects it to the root domain” (second sentence, not quoted here) |
| 64 | The default hostname can be switched off, and then it stops answering | S052 “After you disable your onrender.com subdomain, all requests to it receive a 404 response.” | WRONG, low: the host answers with a 404; “stops answering” contradicts the quote |
| 64 | can be switched off | S052 “If your service has at least one custom domain, you can disable the service's default onrender.com subdomain.” and “You can re-enable the subdomain at any time.” | OMIT, low: the precondition and the re-enable are dropped |
| 64 | leaving the service reachable exclusively at its custom domain(s) | S052 “reachable exclusively at its custom domain(s)” | OK |
| 65 | A wildcard domain needs the root domain pointing at Render too | S052 “To use a wildcard domain, your root domain must also point to Render.” | NARROW/OMIT, medium: S052 adds “If your root domain points to a non-Render destination, your wildcard configuration will fail.” and “make sure to disable proxying for your root domain (gray cloud).” (Cloudflare orange-cloud case) |
| 66 | When a domain does publish CAA records, they must name Render's authorities | S052 “If your custom domain defines CAA records , make sure to define records for Render's certificate authorities:” | NARROW/OMIT, medium: “make sure to define corresponding issuewild records for each authority.” (wildcard) is dropped. The authorities are not named; S052 names Let's Encrypt and Google Trust Services |
| 46–66 | Any plan or price stated as fixed? | none; the only search hit is “wildcards included” (L60, meaning “including”) | OK. Coverage gap, medium: S052 “Your workspace includes an amount of custom domains based on its plan:” and “Plan Included domains Hobby 2 Pro 15 Scale 25 Each custom domain you add beyond this amount costs $0.25 per month.” are absent |
| 46–53 | Plan gate on headers? | S051 states none; its nav lists “Platform features by plan” (not retained) | OK: the entry is silent. Do not add “all plans” |

## Findings by severity
1. MEDIUM, L60. “wildcards included” is unconditional. S052 makes wildcard setup depend on a CNAME set, including _acme-challenge. Suggested: add “a wildcard domain also needs the CNAME set S052 lists, including _acme-challenge.”
2. MEDIUM, L65 and L66. The wildcard failure mode (a non-Render root destination makes the wildcard fail), the Cloudflare caveat for the root record, and the issuewild records for wildcard CAA are all absent. Suggested: quote each one.
3. MEDIUM, L63. Direction dropped. Suggested: “the host you add is the redirect target; the other host redirects to it.”
4. MEDIUM, L51. S051's own examples show that neither `/*.css` nor `/**/*.css` alone covers both top-level and nested CSS. Suggested: quote both table rows.
5. MEDIUM-LOW, coverage. The plan allowance (Hobby 2, Pro 15, Scale 25) and the $0.25 overage are absent. Suggested: add to “What this entry does not establish”: “plan allowances and domain prices (S049 and S052 plan table) are not stated here.”
6. LOW-MEDIUM, L64. “stops answering” is wrong: the subdomain returns a 404. The precondition (“at least one custom domain”) and the re-enable are dropped. Suggested: “receives a 404 response; it can be switched off once the service has a custom domain.”
7. LOW, wording. L52: S051 says only that the name is case-insensitive; “matched” is not there. L53: the page says “normalized”; “lowercase” comes from its example. L48: “declared in the dashboard” reads as exclusive, and S051 has no “only” or “exclusive”.
8. LOW. L57: say “by default” (S052 later allows switching the subdomain off). L59 omits the failure path quoted above.

## Plan and price check
- Entry search for free, plan, $, Hobby, Pro, Scale, included, price and cost: one hit, L60 “wildcards included”, which means “including”. No plan or price claim is stated as fixed.
- S052 (not in the entry) gives the plan allowance and the overage quoted in the table.
- S049 (the static-sites page, which also carries the plan table) says “Add custom domains to your static site for free.” The entry does not quote it. Any later quote must keep the plan limit.
- Custom response headers: S051 states no plan gate. Its nav lists “Platform features by plan” (not retained). The entry is silent, which is correct.

## Freshness
- S049, S051 and S052 carry no revision date: the only date-like text is “© Render 2026”. The Changelog page was not retained. The entry's verified-at 2026-10-22 is the fetch date (receipts accessedUtc 11:49:44Z–11:49:45Z). Nothing dates a rule change.
- Snapshot-bound statements in the two sections: L62 “Render uses IPv4” and L60 issuers (S049). Plan facts are not in the entry. The 90-day recheck is the only control.
- Similar wording elsewhere in the lane: corpus/lessons/round-30.md:45 (“defined in the Render Dashboard”) and corpus/README.md:277 (“set per relative path in the dashboard”). Neither says “only”. Within corpus/, the flagged wordings at L52, L53 and L64 appear only in render-static-sites.md.

## Commands and exit codes (sandbox unless noted)
- sha256sum of S049–S052.txt (lane sources folder): equal to receipts textSha256, 4/4. Exit 0.
- zcat of each .html.gz, byte count and sha256: equal to receipts bodyBytes and bodySha256, 4/4. Exit 0.
- python3 -B check.py: quotes checked 23, not in cited source 0. Exit 0 (check.out).
- python3 -B check2.py and check3.py: tag-to-space derivation gives identical token sequences (983, 854, 539, 1488 words); all 23 quotes also appear in the derived HTML text. Exit 0 each.
- python3 -B check4.py: 22/22 cited omission spans are exact. Exit 0.
- python3 -B check5.py: disk text equals derived text plus one trailing newline; sha256 equals receipts, 4/4. Exit 0.
- _grep on corpus/ for the flagged wordings: only render-static-sites.md. _grep on corpus/ for “RFC 9113” and HTTP/2 lowercase: no matches. Exit not applicable.
- Not run: c2_quote_truth.py (writes receipts; not this reviewer's check); freshness-sweep.mjs, probe-delta.mjs and live_snapshot.py (forbidden this round). No network of any kind.

## Not verified and residual risk
- Live Render behaviour: not checked. The claim set is documentation only, and this reviewer may not fetch.
- HTTP/2 lowercase header-name rule: no lane source, not fetched. Keep “lowercase” as [INFERENCE] until checked against RFC 9113 §8.2.1.
- Blueprint fields (`domains`, `staticPublishPath`), the Changelog and the plan-features page: not retained. Any statement about them stays open.
- Tooling: no installs or updates. Used the existing python3, sha256sum, zcat and wc. One read-only `git status --short --branch -- .ufo/waves/round-30/w2/` in the lane; it may refresh the index stat cache. No staging, commit or other git write.
- lsp: not used. The target is markdown with no code and no language server.
