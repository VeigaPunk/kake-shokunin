# KakeR29.ReviewSourcesReopen — C1 source truth: independent re-open of S040–S043

Seat: leaf reviewer, wave 1, judged axis freshness. One ordinary GET per declared URL
(urllib, no browser), visible text derived with the same rule as
`.ufo/waves/round-29/fetch_sources.py` (its `visible_text` copied verbatim into my
script), then compared byte-for-byte with the retained `sources/S0xx.txt`.

## Result: 4/4 identical

Every fresh body sha256 equals the retained `receipts.json` `bodySha256` and every
fresh visible-text sha256 equals the retained `.txt` sha256 — the raw HTTP bodies
were byte-identical, not only the derived text.

| Source | URL (→ final) | Status | UTC | Body bytes | Text sha256 (first 16) | Equal |
|---|---|---|---|---|---|---|
| S040 | docs.github.com/en/pages/…/about-github-pages → …/what-is-github-pages (redirect, same landing as original fetch) | 200 | 2026-10-22T10:33:42Z | 94214 | `625f2b0783a129d2` | yes |
| S041 | jekyllrb.com/docs/github-pages/ (no redirect) | 200 | 2026-10-22T10:33:42Z | 21840 | `86a77ee24f7e01d5` | yes |
| S042 | jekyllrb.com/docs/liquid/filters/ (no redirect) | 200 | 2026-10-22T10:33:42Z | 40985 | `b66fefc15f2b1ba5` | yes |
| S043 | vite.dev/guide/static-deploy.html (no redirect) | 200 | 2026-10-22T10:33:42Z | 13360 B text / 93983 B body | `d665dd23b193b0a4` | yes |

Full digests in `/fast/scratch/hyaku/kake-r29/w1/ReviewSourcesReopen/reopen_receipts.json`;
body sha256 S040 `fac40d86c4907bee…`, S041 `1e3149a8c51871c6…`, S042 `610d127b38f9c976…`,
S043 `be274bde3c2b6b09…` — each identical to `sources/receipts.json` of the original
fetch at 2026-10-22T10:29:37Z (my GETs ~4 min later).

## Commands run (exit codes)

1. `mkdir -p /fast/scratch/hyaku/kake-r29/w1/ReviewSourcesReopen/tmp` → exit 0 (sandbox; TMPDIR inside sandbox).
2. `sha256sum S04{0,1,2,3}.txt` + `wc -c` on retained texts → hashes match `receipts.json` `textSha256` (baseline intact).
3. `TMPDIR=/fast/scratch/hyaku/kake-r29/w1/ReviewSourcesReopen/tmp python3 -B reopen_sources.py` → exit 0; printed `S040 200 94214 equal`, `S041 200 21840 equal`, `S042 200 40985 equal`, `S043 200 93983 equal`.
4. Context greps over the fresh gzip bodies (attribution of dates, exit 0).

Script: `/fast/scratch/hyaku/kake-r29/w1/ReviewSourcesReopen/reopen_sources.py`
(5323 bytes). No tool installs (none needed).

## Last-updated / redirect notes per source

- **S040** (docs.github.com): 302-style redirect `about-github-pages` → `what-is-github-pages`, identical landing URL to the original fetch (`finalUrl` matches receipts). No `Last-Modified` header, no visible last-updated date; the ISO dates in the body (`2022-11-28`, `2026-03-10`, `2026-10-16`) are docs-platform `apiVersions`/`nextDeprecationDate` metadata inside an inline script, not page dates. All absent from visible text after the script-strip rule.
- **S041** (jekyllrb github-pages): no redirect. `Last-Modified: Tue, 13 Oct 2026 18:44:50 GMT`, ETag `"6ace7c22-5550"`, Server `GitHub.com`; JSON-LD `dateModified 2026-10-13T11:44:21-07:00` (≈ header, same site build).
- **S042** (jekyllrb liquid filters): no redirect. Same build stamp as S041 (Last-Modified 2026-10-13T18:44:50Z, ETag `"6ace7c22-a019"`). Visible `2008-11-07T13:07:54-08:00` is the doc's own example output of `{{ site.time | date_to_xmlschema }}` — content, not a page date.
- **S043** (vite.dev static-deploy): no redirect. Server `Netlify`, no `Last-Modified`, no date-like strings anywhere in the body; docs version in nav is `v8.3.4` (in HTML, matches the retained body).

## Observations on the C1 chain (not defects)

- `corpus/knowledge/pages-base-path.md` is absent from the working copy at e58b66c and from every ref (`git cat-file -e d18bbf30…:corpus/knowledge/pages-base-path.md` → exit 128; `git log --all -- <path>` → empty). This is the expected mid-build state: w1-dispatch assigns its drafting to a scribe seat ("C1 entry draft: corpus/knowledge/pages-base-path.md"), and the sibling connector report says the same for the SOURCES.md rows. Flagging so the L1 knows source truth is green but entry integration is still pending.
- Because the entry file is absent, I could not cross-check its quotes against the fresh text; the retained texts they will quote from are proven live-identical as of 10:33:42Z today, which is the part my seat owns.

## Residual risk / not verified

- Freshness claim covers a single GET per URL at 2026-10-22T10:33:42Z, 4 minutes after the original fetch; identical bytes over a 4-minute window, not over days. Recheck cadence is the SOURCES.md recheck field's job, not this probe.
- I did not re-run the C1 quote counter or the C2 counter (other seats own them); no mutation of the lane was performed anywhere (only reads; my sole lane write is this report file).
- S040's redirect was followed by urllib both times; I did not probe whether the old URL is a permanent (301) or temporary redirect — only that both fetches land on the same page with identical bytes.
