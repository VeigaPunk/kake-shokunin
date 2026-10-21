# S017 — FRESHNESS recheck (round 26)

Row: `corpus/SOURCES.md:25` · tier C · kind docs · status rejected · scope "Whether public/CNAME sets a custom domain under Actions publishing" · anchor "Change your GitHub URL to a custom domain, step 2; fetched 2026-10-19" · used-by `—`.

Fetched #1: `https://docs.astro.build/en/guides/deploy/github/` → HTTP 200, 187320 bytes, sha256 `89cb471d…736075`, etag `"802f3028ac2648e5c61ab4b4f5b5c6db"`, `last-modified: null`, fetched 2026-10-21T15:10:41Z; text view `fetched/text/S017-1.txt` (10964 chars, single line).

```json
{"id":"S017","verdict":"HOLD","fetchIndex":1,"quote":"This will deploy your site at your custom domain instead of user.github.io.","anchorObserved":"Change your GitHub URL to a custom domain\" heading, step 2 'Add a ./public/CNAME record to your project.' (text view renders the inline link as 'Add a./public/CNAME'); quoted sentence immediately follows 'public/CNAME sub. example. com'","reason":"The page still tells readers to 'Choose GitHub Actions as the Source of your site' and then presents the public/CNAME file as the thing that sets the domain, so the contradicted claim survives verbatim at the same anchor. GitHub's custom-domain page re-fetched this round still says 'If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored and is not required.' The flip condition ('GitHub docs say the CNAME file is honored under Actions') is not met; if anything the guidance is firmer, so the rejection and its scope hold.","correction":null}
```

Caveats:
- Living, unpinned docs page: no version/tag pin and no HTTP `Last-Modified` (null), so drift is decided from present content, not a diff; only this round's bytes are retained for S017, no 2026-10-19 snapshot exists to compare (etag/sha256 now recorded).
- Anchor did not move: heading text and step order (1 DNS, 2 CNAME, 3 Astro `site`) are unchanged; step 2's file body still reads `sub.example.com`.
- Corroborating GitHub wording is quoted from this round's `fetched/text/S005-1.txt` ("Managing a custom domain…"); S005's own verdict belongs to that row's seat, this row only uses it as the contradiction witness its teaches names.
- Precision note for integrators: GitHub's current wording is "ignored and is not required", i.e. the Astro step is unnecessary/misattributed rather than actively breaking the site — the rejection's substance (Astro's CNAME step does not drive the domain under Actions) still stands.
- `usedBy` is `—` and no `corpus/knowledge/` file cites S017, so no knowledge pair statement required.
- No tool installs or upgrades were performed.
