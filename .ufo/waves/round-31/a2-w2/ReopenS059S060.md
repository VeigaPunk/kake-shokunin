# ReopenS059S060 — independent re-open of C2 sources S059 and S060

Axes: freshness (judged), fidelity of retained receipts. No defect found.

## What was attacked

Claim C2's evidence path for S059 (https://render.com/docs/docker) and
S060 (https://render.com/docs/health-checks): whether a second, independent
open of the same URLs reproduces status 200, the receipt hashes and the
lesson `## Gate` quotes, and whether the wave-1 claim "bodies differ only in
per-request trace values and build asset ids"
(`corpus/lessons/round-31.md:35-36`) is honest or understated.

## Method

Same as `.ufo/waves/round-31/fetch_sources.py`: one public GET per page,
same User-Agent (`kake-shokunin-round-31-source-opening (one GET per page)`),
same visible-text rule (HTML minus script/style and comments, tags removed,
entities decoded, whitespace collapsed). Sandbox copy:
`/fast/scratch/hyaku/kake-r31/a2-w2/ReopenS059S060/reopen.py`
(sha256 `9da68bec84ff…`). No headless browser, no challenge bypass; both
pages opened at once by ordinary urllib GET. Quotes checked: the `## Gate`
quote per id plus every curly-quoted span attributed `(S059)`/`(S060)` in
`corpus/knowledge/render-web-services.md` at fde133a
(8 quotes for S059, 10 for S060).

## Commands and results

- `python3 -B /fast/scratch/hyaku/kake-r31/a2-w2/ReopenS059S060/reopen.py`
  run at 2026-10-22T18:07:46Z, exit 0. Full JSON:
  `/fast/scratch/hyaku/kake-r31/a2-w2/ReopenS059S060/out/reopen-result.json`
  (sha256 `d104d5fe1f65…`).

### S059 — https://render.com/docs/docker
- time 2026-10-22T18:07:46Z; status 200; finalUrl unchanged.
- body 325333 bytes, sha256 `5e9561ce1c944e06…` — NOT equal to receipt
  body `d3ce93a75d29…` (327582 bytes). 8 of 269 lines differ, all
  `data-dpl-id`, `dpl=` params and Next.js chunk filenames
  (`06fjb9vnwzby-.js` -> `16x8clleqm4wh.js`); sentry-trace/baggage head block
  gone in the fresh body — a docs-site redeploy between 15:41Z and 18:07Z.
- visible text sha256 `f8e60da01b30…` — EQUAL to receipt textSha256 and to
  retained `.ufo/waves/round-31/sources/S059.txt` byte-for-byte.
- Gate quote "Render copies your service's secret files into the root of
  your build context." present in fresh text (and retained). All 8
  entry-attributed S059 quotes present in fresh text; 0 missing.

### S060 — https://render.com/docs/health-checks
- time 2026-10-22T18:07:46Z; status 200; finalUrl unchanged.
- body 458138 bytes, sha256 `8196ed2484d0…` — NOT equal to receipt body
  `70954862f322…` (458065 bytes). 8 of 225 lines differ; same class of
  diffs (new `dpl=566dc9cb5f`, new sentry-release
  `6e73712e…`, chunk-id swaps, a `<!--$--><!--/$--` React placeholder insert).
- visible text sha256 `1f934877247b…` — EQUAL to receipt textSha256 and
  retained `S060.txt` byte-for-byte.
- Gate quote "If this condition is not met within 15 minutes, Render
  cancels the deploy and continues routing traffic to your service's
  existing instances." present in fresh text (and retained). All 10
  entry-attributed S060 quotes present in fresh text; 0 missing.

## Findings

- None blocking. C2's retained material reproduces against the live pages
  ~2.5 hours after the original fetch: status, final URL and visible text
  identical; every quote the knowledge entry and lesson Gate attribute to
  S059/S060 is still an exact substring of the page text.
- Observation (not a defect): receipt `bodySha256` values are per-request
  and were already unequal at wave-1's 15:55Z re-open; mine differ again —
  Render redeployed its docs site between 15:41Z and 18:07Z (new
  `data-dpl-id`/chunk hashes, dropped sentry head meta on S059). The
  lesson's "differ only in per-request trace values and build asset ids"
  holds exactly; nothing in the diffs touches visible content.

## Not verified / residual risk

- S057, S058, S061 — not assigned to this seat; only S059/S060 re-opened.
- C2 strict counter internals and the counter re-runs at 92235a0 — sibling
  seat scope; `c2_quote_truth.py` was read only to mirror its quote rule.
- Receipts' `fetcherSha256` chain-of-custody — script read and reimplemented
  in sandbox; hash not independently re-derived.
- Pages could drift after 18:07Z; the 90-day recheck hook in the entry is
  the right guard.

Tooling: none installed (pacman paused host-wide); Python 3.14.8 urllib.
Sandbox artifacts: `/fast/scratch/hyaku/kake-r31/a2-w2/ReopenS059S060/`
(`out/S059.body`, `out/S060.body`, `out/S059.txt`, `out/S060.txt`,
`fetch/` retained-body copies for diffing, `reopen.py`,
`out/reopen-result.json`).
