# ScoutReopenS274 — round 50 wave 1

Scoped task: re-open `https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate` with one curl GET, report HTTP status, byte size, whether the frozen S274 quote is a RAW substring of the fetched body, and the derived class. Body was not written into the lane repo (kept at `/tmp/r50-s274/body.html`).

## Fetch

- URL: `https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate`
- Command: `curl -sS -o /tmp/r50-s274/body.html -w 'HTTP %{http_code}\nbytes %{size_download}\n' -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' --max-time 60 <URL>`
- HTTP status: **200**
- Byte size (size_download): **68791 bytes**
- Body sha256: `ee7107eb057f0ef9a475af9918204b325292118618bf860486c277607ac99d52`
- Fetched: 2026-10-24

## Frozen S274 quote check

Frozen quote (from `.ufo/waves/round-50/quote-classes.json` and `FROZEN_QUOTES` in `c50_quote_class.py:46`):

```
It reduces your site's crawl rate across the whole hostname
```

- RAW substring of fetched body: **YES** — found at byte offset 35527.
- Context in raw HTML: `<b>It reduces your site's crawl rate across the whole hostname</b>` (the quote sits verbatim inside a `<b>` element; straight ASCII apostrophe, not the curly variant — checked, curly variant absent).

## Derived class

`raw-substring` — identical to the class recorded in the round-50 ledger (`quote-classes.json`, S274 `matchClass: "raw-substring"`). The live page still serves the quote verbatim, so the label derived from today's fetch matches the frozen label. (For reference, the class definition in `c50_quote_class.py:101-106`: raw-substring = quote is a substring of both text and raw blobs; collapsed-only = substring of text only. The ledger's match for this id is raw-substring and the live fetch preserves that.)

## Counting commands run (per goal; not reasoned about)

- `c50_quote_class.py --revision 9619af67c52939daac502ca7a24c9d714f3f51db` (base): exit 1 — `C1 classed 0/3 met=False`; S273/S274 "class ledger absent, lesson absent"; S286 also missing retained blob, registry row, entry.
- `c50_quote_class.py --revision 33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1` (pre-append): exit 1 — `C1 classed 0/3 met=False`; all three ids "lesson absent"; S286 additionally "no live registry row, entry absent". Ledger rows and retained blobs are present at this revision (no "class ledger absent" / "retained blob absent" reasons).
- `c50_durable.py --revision 9619af67c52939daac502ca7a24c9d714f3f51db` (base): exit 1 — `C2 durable 0/1 met=False`; order proof absent, wave-cite proof absent, LOG.md does not cite the wave, settlement absent.

## Bottom line

S274 re-opens cleanly: the frozen quote remains a verbatim RAW substring of the live Google doc today, so the derived class `raw-substring` matches the ledger. The C1 counter still reports 0/3 at both revisions — the remaining gaps are the lesson sentences, plus the S286 live-registry/entry wiring — not the S274 quote class itself.
