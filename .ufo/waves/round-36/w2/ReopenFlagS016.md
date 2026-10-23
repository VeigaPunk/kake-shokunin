# W2 falsify — S016 re-opened by hand (`unsupported_type`)

Seat: ReopenFlagS016. Lane head f3a38bf8e68f6cee386125d34b5e95ac9b2df66e, base b720d799.
Sandbox: /fast/scratch/hyaku/kake-r36w2/ReopenFlagS016/. No tools installed; no lane file touched
except this report.

## What I attacked
`{"check":"S016","reason":"unsupported_type","target":null}` in
`.ufo/waves/round-36/realrun/audit.json`, over input
`.ufo/waves/round-36/realrun/input.json` S016 (`url https://pages.github.com/versions.json`, quote
`"jekyll": "3.10.0", "github-pages": "232"`, from round-20.md) and row `corpus/SOURCES.md:24`
(kind `dataset`, anchor "JSON keys jekyll and github-pages; fetched 2026-10-19").

## Commands (sandbox, TMPDIR set, each `timeout`-capped)
1. `curl -sS -D headers_nofollow.txt -o body_nofollow.bin https://pages.github.com/versions.json` → exit 0.
2. `curl -sSL -w 'final=%{url_effective} code=%{http_code} redirects=%{num_redirects} ct=%{content_type} size=%{size_download}' -o body_follow.bin <same>` → exit 0, `final=https://pages.github.com/versions.json code=200 redirects=0 ct=application/json; charset=utf-8 size=1287`.
3. `tar -xJf …/realrun/snap-bodies.tar.xz -O ./S016.body > snap_S016.body`; `cmp` → identical.
4. `python3 -B scripts/source_recheck.py --manifest trial/asis/manifest.json` (snapshot manifest fields verbatim, live body) → exit 1, `{"verdict":"failed-policy","findings":[{"check":"S016","reason":"unsupported_type","target":null}]}`: the audit finding reproduces.
5. Same tool, same live bytes, `contentType` rewritten to `text/plain; charset=utf-8` → exit 1, `quote_missing`.
6. Same tool, `text/plain`, quote `"github-pages":"232"` (one contiguous pair) → exit 0, `clean`.
7. `curl -sS -L -o versions_html.bin https://pages.github.com/versions/` → exit 0, `code=200 redirects=0 ct=text/html; charset=utf-8 size=11821`.
8. Tool on that HTML, quote `jekyll 3.10.0` → exit 0 `clean`; quote `github-pages 232` → exit 0 `clean`; quote `jekyll 3.10.0 github-pages 232` → exit 1 `quote_missing`.

## Observed facts
- Live response, verbatim: `HTTP/2 200`, `content-type: application/json; charset=utf-8`,
  `last-modified: Wed, 13 Aug 2025 12:02:55 GMT`, `content-length: 1287`, no `location` header, and
  `num_redirects=0` even with `-L`. Body sha256 `0a713bab52e15579fda7f76e71da0283e8260e217e448fd56d704801212c4542`.
- The recorded snapshot is the same bytes (command 3, identical sha256), so there is no drift
  between the 2026-10-19 fetch and today, and the origin file has not changed since 2025-08-13.
- Parsed body: `jekyll=3.10.0`, `github-pages=232`, 47 keys. Both values the row teaches are still exact.
- `unsupported_type` is exactly what the declared contract prescribes: SCORECARD.md:1637 "Any other
  media type: one `unsupported_type` finding and no quote check"; SKILL.md:1066 lists it under exit 1.
  The tool is correct per contract and its version is the landed one (sha256 `577b2d7d…0d48`).
- The Gate quote is **not** a span of the file. The body is compact (`{"jekyll":"3.10.0",…`, no
  spaces); `"jekyll":"3.10.0"` sits at byte 1 and `"github-pages":"232"` at byte 1185 — 1167 bytes
  apart with 42 intervening keys. The quote carries three spaces and joins the pairs with `, `.
  Under the tool's own normalize (NFKC, delete every `isspace`) it is still absent, hence command 5's
  `quote_missing`. A single-pair quote is found (command 6), so this is the quote, not the reader.
- Origin of the paraphrase: `corpus/lessons/round-20.md:218` writes it in backticks as
  `` `"jekyll": "3.10.0", "github-pages": "232"` ``, which reads as a verbatim JSON snippet but is a
  synthesized join. `corpus/SOURCES.md:24` itself carries no verbatim quote (anchor names the keys,
  teaches paraphrases them), so the fabricated snippet is lesson- and Gate-level, not row-level.
- Same data, HTML rendering: `https://pages.github.com/versions/` (200, no redirect) has adjacent
  cells `<a …>jekyll</a>` `3.10.0` at byte 2083 and `<a …>github-pages</a>` `232` at byte 2439; the
  existing tool returns `clean` on either single-value quote (command 8), and `quote_missing` on the
  joined paraphrase because `github-pages-health-check 1.18.2` sits between them.

## Verdict
**Tool miss (declared capability gap) plus a paraphrase in the quote; not a real drift finding.**
The reason string is honest and contract-mandated: the media type truly is `application/json`, a type
bullet (e) does not support, so no quote claim is made. But as an audit signal it says a healthy,
unchanged row is `failed-policy`, and because `application/json` can never be clean under the
contract, every re-run will re-flag S016. Independently, the Gate quote would fail as `quote_missing`
if JSON were admitted, so the real defect behind that row is a fabricated contiguous snippet, not a
stale source. The round's lesson already labels the pair "JSON endpoints" and defers them to wave 2
(`corpus/lessons/round-36.md:71-72`), so the round-level text does not overstate S016; the risk lives
in the exit-1 signal and in SKILL.md's gate table.

## What the row needs
`kind dataset`: either an `application/json` branch comparing parsed key values (a contract change,
bullet (e)), or the cheap fix that works under the frozen contract — point the row at the HTML
rendering with one contiguous quote per value and split the claim into two checks
(`jekyll 3.10.0`, `github-pages 232`), both shown `clean` here. The single check with a joined
quote cannot pass in any mode.

## Not verified
- S066, the other `unsupported_type` (api.github.com runs JSON), was not re-opened; by its row text
  it is the same class.
- One live observation only; stability argued from `last-modified`, not from repeat fetches.
- Did not implement or test a JSON mode, and did not run the sealed counter or the 101-fixture
  selftest (no claim about them here).

## Evidence
Sandbox only: `body_nofollow.bin` / `body_follow.bin` (1287 B, sha256 `0a713bab…2c4542`),
`headers_nofollow.txt`, `snap_S016.body` (sha256 `0a713bab…2c4542`), `versions_html.bin` (11821 B,
sha256 `daacecc6297ca3f837d547b17a00e28f6b196e312608214dcca7e02b3e53cfd1`), and the manifests/bodies
under `trial/{asis,asplain,contig,html_jekyll,html_ghpages,html_joined}/`, at
`/fast/scratch/hyaku/kake-r36w2/ReopenFlagS016/`.
