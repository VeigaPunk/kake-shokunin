# ExecGateQuoteExtractor — real-input triples for the C1 source re-check

Built `/fast/scratch/hyaku/kake-r36w1/ExecGateQuoteExtractor/gate_quotes.py` (md5
`b24c2674486ccf774a57ca191c808ea6`), which scans every `corpus/lessons/round-*.md`
for Gate lines that record a source opening and emits
`/fast/scratch/hyaku/kake-r36w1/ExecGateQuoteExtractor/gate_quotes.json` (md5
`cdfd2aa46f6f1a811e4522e25ec6add8`), a JSON list of `{id, url, quote, lesson,
line}` plus `shape`, `quote_delimiter`, `url_source`, `accessed`, `http_code`,
`quote_normalized`, `extra_urls`. These are the recorded-fetch quotes a
`source_recheck.py` audit re-checks a row's quote against.

Reproduce (one pasted command, exit 0):

```
python3 /fast/scratch/hyaku/kake-r36w1/ExecGateQuoteExtractor/gate_quotes.py
```

## Counts

- lesson files scanned: 50 (`round-*.md`)
- lines matched (records written): 132 — bullet-gate 48, table-quote-column 59,
  table-reopen 24, prose-lookahead 1
- distinct ids: 86
- SOURCES.md rows: 94
- rows with no extracted quote: S019, S088–S094 — S019 is the own-work corpus
  contract row (a local command, no URL/quote ever opened) and S088–S094 are the
  round-36 rows registered at cd321279 with no lesson line yet
- ids with no URL anywhere: S014, S056 (own-work/sibling-lane rows, not
  fetchable via HTTP — the re-check has no URL to open for them)
- fetchable triples (id with at least one URL): 84

## URL comparison (Gate line vs SOURCES row)

Comparison is verbatim first, then normalized (scheme/host lowercased, default
port and trailing slash dropped, fragment dropped).

- Gate-line first-URL equals the SOURCES first URL for every id that has a URL
  on the gate line — `url_text_differences` is empty. There is no row where the
  registered URL and the recorded open URL disagree on the primary address.
- `gate-line-names-url-not-in-sources-row` (cross-check URLs the Gate names but
  the row does not register): S017 (GitHub Docs apex-domain page), S018
  (Firefox 144.0 release notes), S054 (`render.com/docs/configure-other-dns`,
  the S061 flip source), S066 (the `apps-sdk.yml` workflow-runs URL — the row's
  source cell names it in prose but never as a URL).
- `sources-row-has-no-url`: S014 (`scripts/freshness-sweep.mjs`), S056
  (sibling-lane path) — cannot be re-checked over HTTP at all.
- Redirect/final URLs are recorded in `extra_urls` (S071 `docs.x.com/overview`,
  S084/S085 live-file notes) so the re-check can treat them as expected
  end-points, not mismatches.

## Line shapes parsed

- `- S0NN — <url> — accessed <time>, HTTP <code> — … quote “…”` (rounds 28–35;
  also `queued`/`rejected` variants and `- S040 — <url> (redirects to …)`).
- `| S0NN | <url> | … “…” |` quote-column tables (rounds 20, 22, 23, 24, 26,
  27, 28, 32, 33, 35) — the quote comes from the column whose header says
  `quote`/`located support`; URL from the `url`/`source` column.
- re-open spot-check rows `| S0NN | admit | <url>; Quote "…" | … |` (rounds
  22/26/28/30/31/32/33/34 verifier-spotcheck) — quote pulled from the source or
  reason cell when it is a `quote “…”`/`Quote "…"` span or a non-command
  backtick span.
- `S035: <url> — accessed <date>.` with the quote on the next line
  (round-25, prose-lookahead).

24 lines with an S-id but no recoverable quote are listed in
`id_lines_without_quote` — mostly spot-check rows that confirm a quote's
presence without restating it, plus registry-change bullets.

## Evidence

- extraction: `/fast/scratch/hyaku/kake-r36w1/ExecGateQuoteExtractor/gate_quotes.py`
- JSON output: `/fast/scratch/hyaku/kake-r36w1/ExecGateQuoteExtractor/gate_quotes.json`
- printed report: `/fast/scratch/hyaku/kake-r36w1/ExecGateQuoteExtractor/report.txt`
- every extracted quote is verbatim from its recorded line except S035's
  lookahead (round-25.md:22 names the line; the quote text is on line 23).
- cross-check: all 48 `- S0NN — … accessed …` bullet lines produce a record
  (grep count of that shape equals the bullet-gate count).

## Not verified / risks

- Quotes are verbatim from the lesson lines; whether each is a true substring of
  the recorded fetch is the re-check's own job (out of scope here).
- Spot-check re-open rows are informative duplicates of the row quote in some
  cases (e.g. S062 picks `- key: OPENAI_APPS_CHALLENGE`, a second backtick
  field, not the headline quote) — the JSON keeps every record, so the
  re-check should prefer the `bullet-gate`/`table-quote-column` shape for the
  canonical row quote.
- No network access used; nothing written outside the sandbox and this report.

Tooling installed: none (system python3 suffices; pacman paused per ruling).
