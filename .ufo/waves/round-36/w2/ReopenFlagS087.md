# S087 `gone` — re-opened by hand

Seat: ReopenFlagS087 (r36 wave 2, falsify). Lane head `f3a38bf8e68f6cee386125d34b5e95ac9b2df66e`, read-only.
Input: `realrun/input.json` S087, url `https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/bypassing-jekyll-with-nojekyll`,
quote `404 - GitHub Docs GitHub Docs Page not found. Return to home.` (`round-35.md`). Row `corpus/SOURCES.md:95`: grade C, REJECTED, flip "the URL serves GitHub documentation again".

## Verdict

**REAL** — the URL is gone. HTTP/2 404, no `Location`, for every ordinary request I made. The recorded
row (`corpus/SOURCES.md:95`, "HTTP 404, 502-byte body") and the tool's `gone` finding agree with the live server.
Two qualifications, both reproducible, neither a contract violation:

1. **Zero freshness delta.** The row's own fetch already recorded 404 on 2026-10-22T22:27:55Z and was rejected.
   `source_recheck.py:528-529` derives `gone` from final status alone (bullet (a)), so re-checking this row
   restates a known state. The lesson is honest about it (`corpus/lessons/round-36.md:71`, "`gone` 1 (S087, already rejected)"),
   but the count "14 findings on 13 rows" must not be read as 13 rows of drift.
2. **The row's `quote` is not a quote** — it is the 404 page's own boilerplate, captured by the wave-1
   Gate-quote extractor. That makes the row's quote permanently uncheckable and creates a soft-404
   false clean (below). Extraction defect at the data layer, not in the tool.

## What I ran (all in `/fast/scratch/hyaku/kake-r36w2/ReopenFlagS087/`, `TMPDIR=…/tmp`)

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `curl -sS -D headers-noredirect.txt -o body-noredirect.html <url>` (no `-L`) | 0 | `HTTP/2 404`, no `location:` header, `content-length: 502`, `date: Fri, 23 Oct 2026 02:03:32 GMT`, `x-github-request-id: CA9C:1267A9:…:6ADABF1F` |
| 2 | `curl -sS -L -o body-followed.html <url>` | 0 | `HTTP/2 404` only; zero hops; body sha256 identical to #1 |
| 3 | `curl … -A "Mozilla/5.0 … Chrome/130.0" -H "Accept: text/html,…"` | 0 | `HTTP/2 404`, 502 bytes, same sha256 — not a client/UA artifact |
| 4 | `curl … <url>/` (trailing slash) | 0 | `301` → `<url>` (slash-trim), i.e. redirect *into* the 404, not a recovery |
| 5 | `curl … http://docs.github.com/…` | 0 | `301` → `https://docs.github.com/…` (scheme only) |
| 6 | `python3 -B scripts/source_recheck.py --manifest only87/manifest.json` (S087's realrun check, extracted verbatim) | 1 | `{"verdict":"failed-policy","checksEvaluated":1,"findings":[{"check":"S087","reason":"gone","target":null}]}` |
| 7 | `python3 -B scripts/source_recheck.py --manifest soft404/manifest.json` (S087's quote, live 404 body, hop status flipped to **200**) | **0** | `{"verdict":"clean","checksEvaluated":1,"findings":[]}` |
| 8 | `curl https://docs.github.com/sitemap.xml` | 0 | `404`, 502 bytes — the same boilerplate is what this site serves for every unknown path |

Saved bodies: `body-noredirect.html`, `body-followed.html`, `ua-body.html` — all sha256
`979615bad4719ae23bf76385ee60de8b1b05c785ce74497dee80ecb54c69c522` (502 bytes). Headers: `headers-noredirect.txt`, `headers-followed.txt`, `ua-headers.txt`.
Manifests: `only87/manifest.json`, `soft404/manifest.json` + `soft404/S087.body`.

## Live text (exact bytes)

```
<!doctype html><html lang=en><meta charset=utf-8><title>404 - GitHub Docs</title><style>…</style><p style=font-weight:500>GitHub Docs</p><p>Page not found.</p><p><a href=/>Return to home.</a></p><small>&copy; 2026 GitHub, Inc. …
```

Run through the tool's own `html_text` (`scripts/source_recheck.py:341`):
`'404 - GitHub DocsGitHub DocsPage not found.Return to home.© 2026 GitHub, Inc. • Terms • Privacy'`;
`normalize(quote) in normalize(text)` → `True`. So the manifest quote does match the live body; it is the
error page's text, and the finding is produced only by bullet (a)'s status rule.

## Soft-404 false clean (row 7) — scope note

`soft404/manifest.json` gives S087 a `200` hop, `contentType: text/html; charset=utf-8` and the live 404 body.
The tool returns **clean**: any server that serves this error template with 200 satisfies the quote forever.
This is compliant with the declared C1 contract (bullet (a) gates the quote rules on 200 and nothing else;
SCORECARD limits already say the tool shows the contract is implemented, "not that any registry row is fresh"),
so it is a limitation of the declared capability, not a broken claim. It becomes a real hole only if a row's
quote is error-page boilerplate, which is exactly S087's case.

## Row URL / flip

No change needed. There is no live replacement of the retired `.nojekyll` page: the exact slug is 404 with no
redirect, and the rule survives on S086's page, verified live today —
`https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site` (HTTP 200):
"…disable the Jekyll build process by creating an empty file called .nojekyll in the root of your publishing source…"
(saved `s086.html`). The rejection teaches nothing new and loses nothing; the flip condition stays correct.

## Not verified

- Did not read `github/docs` history or `redirect-exceptions.txt` to prove the removal was intentional; only the
  live server, the trailing-slash 301 into the 404, and the public redirects README structure were consulted.
- The row's "retained text sha256 1d697e89…" does not reproduce from the live body under `html_text` (5e527ca0…)
  or `normalize(html_text)` (5fda646d…): a different extraction produced it. Not chased; not needed for `gone`
  (bodies match by size, content and quote). No claim about JS rendering is needed: the page is static.
- Tool installs/upgrades: none.

## Clean vs harmful

Clean on the finding itself (`gone` is true and contract-mandated). Advisory to the L1: (1) do not count S087
as a drift hit — label the real-run as 12 rows plus one known-dead row, or exclude rejected rows at input build;
(2) drop `quote` for a row recorded as non-200, or give the tool an error-page/soft-404 guard, before the real-run
findings are used as a freshness signal on other rows.
