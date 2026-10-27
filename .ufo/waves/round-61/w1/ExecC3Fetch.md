# ExecC3Fetch

C3 live fetches for the due set S001–S010 (contract § Claim C3). Ten GETs, one per row, 2026-10-27 (UTC),
all HTTP 200. Bodies: `.ufo/waves/round-61/recheck/S0xx.html` (raw response bytes, no rewriting).
Receipts: `.ufo/waves/round-61/recheck/receipts.json`, created as `{"receipts": []}` and appended one entry per
row; keys `id, url, effectiveUrl, status, sha256, bytes, fetchedAt, userAgent`. Fetcher code (retained evidence):
`.ufo/waves/round-61/w1/ExecC3Fetch.files/fetch_recheck.py`.

## FETCHES:

| id | url (as fetched) | status | bytes | sha256 (head) | effectiveUrl |
|---|---|---|---|---|---|
| S001 | raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a7…/action.yml (v4.0.0) | 200 | 2529 | 4524ed61c2fb61b4 | same (0 hops) |
| S002 | github.com/actions/upload-pages-artifact/releases/tag/v4.0.0 | 200 | 199999 | cc2473ed3e345f4b | same (0 hops) |
| S003 | docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site | 200 | 154136 | 261408c59b4476f6 | same (0 hops) |
| S004 | docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages | 200 | 141818 | 6b9e240b995d0407 | same (0 hops) |
| S005 | docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site | 200 | 240439 | 7428ff4f61f84f68 | same (0 hops) |
| S006 | docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll | 200 | 138096 | 7b63a76f5b9ebb7a | same (0 hops) |
| S007 | docs.github.com/en/rest/pages/pages | 200 | 453447 | f5f5472f8425f77a | same (0 hops) |
| S008 | cgit.git.savannah.gnu.org/cgit/tar.git/plain/doc/tar.texi?id=cfdb891… | 200 | 512359 | 93281a63cb9f94a0 | same (0 hops) |
| S009 | raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c | 200 | 147410 | c58ebede93aa6c79 | same (0 hops) |
| S010 | https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8 | 200 | 1187554 | d431760660ea44e1 | https://www.rfc-editor.org/rfc/rfc9110.html (fragment not sent on the wire) |

`fetchedAt` values (all 2026-10-27 UTC): S001 09:15:41, S002 09:15:43, S003 09:15:45, S004 09:15:46,
S005 09:15:47, S006 09:15:49, S007 09:15:50, S008 09:15:54, S009 09:15:55, S010 09:15:56
(`+00:00`). No redirect was followed (`hops=0` everywhere); no body hit the 2 MiB cap (largest 1187554 bytes),
so no retained body is truncated.

### Retained-evidence checks (run, on disk)

- `sha256sum` of each `S0xx.html` equals the receipt `sha256` and the file length equals the receipt `bytes`:
  10/10 match (`ALL_MATCH True`).
- Bodies are complete documents: S002 ends `</html>` despite its 199999-byte length (not a cap artefact);
  S001 is the full 85-line v4.0.0 `action.yml`; S008 13680 lines; S009 5367 lines; S010 19014 lines.
- Anchor material spot-probe (grep count, first line): S001 `Archive artifact` n=6 first line 24,
  `--exclude=.git` line 33, `--exclude=.github` line 34; S002 `What's Changed` line 689; S003
  `About publishing sources` line 32 / `Creating a custom GitHub Actions workflow` line 102; S004
  `Configuring the upload-pages-artifact action` line 32 and `10GB` line 42; S005 `Configuring an apex domain`
  line 32 / `Configuring a subdomain` line 32; S006 `Configuring Jekyll in your GitHub Pages site` line 32;
  S007 `Get a GitHub Pages site` line 32, `build_type` line 61, `protected_domain_state` line 49; S008
  `Controlling Pattern-Matching` line 8481 (row anchor says 8478–8617); S009 `ngx_http_set_etag` line 1682
  (row anchor exact) with the ETag `ngx_sprintf` at lines 1708–1710 (row anchor exact; format is `"%xT-%xO"`
  in release-1.28.0); S010 `8.8.1` / `Weak versus Strong` line 1667 with `ETag` material from line 1681
  (row anchor §8.8.1/§8.8.3).

## FAILURES:

None. Ten of ten rows returned HTTP 200; no transport error, no redirect chain, no timeout, no cap hit, no
non-200 status. No row is reported as fetch-failed.

## NOTES (scope facts the quote and pin seats need)

1. **Fetch ethics used** (contract § Claim C2 constraints applied in spirit, C3 text): GET only; no cookie jar,
   no credentials, no request body, no proxy config; `User-Agent: round61` and `Accept-Encoding: identity`;
   redirects followed by hand and capped at 5 (zero occurred); 20 s timeout; body cap 2 MiB with the overflow
   byte detected (nothing truncated). One request per row, 1 s spacing.
2. **Rows whose `source` cell lists two URLs** were fetched at the **primary (first-listed)** URL only, per the
   seat item ("one GET each"): S001 = v4.0.0 `action.yml`; S002 = `releases/tag/v4.0.0`. Consequence, observed
   in the retained bodies: S001's body does **not** contain `include-hidden-files` (n=0) — that input exists in
   the row's second URL, the main-commit file `5f327015a708106f6f1b7c9a633901af30fe80cb`, which was **not**
   fetched this round; the row's other half (invariant `.git`/`.github`/`.[^/]*` exclusions) is present in the
   retained body. S002's body is the v4.0.0 release page; `v5.0.0` occurs **n=0** — the v5.0.0 half lives in the
   row's second URL, **not** fetched. Both halves are therefore reported as partial, not as page changes.
3. **S010 fragment**: the row URL carries `#section-8.8`; the receipt keeps the row URL verbatim in `url` and
   records the wire/final URL in `effectiveUrl`. The retained body is the whole RFC 9110 HTML document.
4. `receipts.json` contains exactly 10 entries, ids S001–S010, no auxiliary ids and no duplicate ids.
5. Nothing outside the assigned paths was written: `corpus/SOURCES.md`, lessons and the registry were not
   touched (cell edits are ExecC3Pins' table and the L1's integration), no git/jj state was read-modified, and
   the scratch dir `/fast/scratch/hyaku/kake-r61/ExecC3Fetch` was removed at the end of the run (nothing cited
   lived there; the fetcher and bodies are in-lane).

VERDICT: All ten due rows S001–S010 re-fetched live on 2026-10-27 with HTTP 200, ten sha256-pinned bodies and ten receipts on disk; no fetch failure, no truncation, and the only coverage limit is the named second-URL half of S001/S002, which was not fetched this round.
