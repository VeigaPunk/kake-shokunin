# ReopenFlagS068 — re-open the `moved` + `quote_missing` finding by hand

Leaf scout (falsify). Lane read-only at `f3a38bf8`; all writes under
`/fast/scratch/hyaku/kake-r36w2/ReopenFlagS068/`. No tool installs, no pacman.

## Verdict
- **`quote_missing` = tool miss (fetch layer)**: not page drift, not extraction, not a paraphrase.
  The live page carries the Gate quote verbatim in server-rendered text; the realrun snapshot was
  served in **Portuguese** because `scripts/source_snapshot.py` sends no `Accept-Language`.
- **`moved` = true live observation, not a row defect**: one permanent hop, already declared in the
  row's anchor. `source` URL cell should not change (S071/S083 keep the requested URL too).

## Commands (all exit 0; `timeout 60`/`90`/`120`, `TMPDIR` in sandbox)
1. `curl --max-redirs 0` on `https://developers.facebook.com/docs/sharing/webmasters/` →
   `code=301 redirect=https://developers.facebook.com/documentation/sharing/webmasters size=0` (`live/h1.txt`).
2. Same final URL, no-follow → `code=200 size=729616 type=text/html; charset="utf-8"` (`live/s068.html`), **pt-BR page**.
3. Same + `-H 'Accept-Language: en-US,en;q=0.9'` → `code=200 size=723692` (`live/s068-en.html`), **English, quote present**.
4. Same + `-H 'Accept-Language: de-DE,de;q=0.9'` → `code=200 size=106181` (`live/s068-de.html`), German page.
5. Exact recorder replay (urllib, UA `kake-shokunin-round-36-source-snapshot (one GET per source)`, `Accept: */*`, no language) →
   `status 200 len 729571`, `EN quote: False`, `PT quote: True` (`live/s068-recorder-emulated.html`).
6. Tool's own extractor (`importlib` on `scripts/source_recheck.py`, `html_text`+`normalize`):
   `live-en 1095 words quote_found True` / `live-ptBR 1222 words False` / `snapshot 1222 words False`.
7. `difflib` words, round-34 `sources/S068.txt` vs live English visible text:
   `1276 / 1276 words`, `similarity 1.0`, `non-equal blocks 0`.

## Live evidence (visible text of `live/s068-en.html`)
> Without these Open Graph tags, the Facebook Crawler uses internal heuristics to make a best guess
> about the title, description, and preview image for your content. Designate this info explicitly
> with Open Graph tags to ensure the highest quality posts on Facebook.

The Gate quote is an exact **prefix** of that sentence (it stops before "for your content"). It sits
in a server-rendered `<p>` (raw offset 564970, not inside a `<script>`), so script stripping is not the
cause. The anchor's `Updated : Jun 30, 2026` also matches live (PT renders `Updated : 30 de jun de 2026`).

pt-BR served instead (`live/s068.html`), same section:

> Sem essas tags do Open Graph, o rastreador do Facebook usa técnicas heurísticas internas para
> tentar dar o melhor palpite em relação ao título, à descrição e à imagem de prévia do seu conteúdo.

## Why it is a fetch-layer miss
- The row's retained text is English and **contains the quote**: `grep -c -F` on
  `.ufo/waves/round-34/sources/S068.txt` → `1`; 1276 words; sha256 `2c9a5d3c…5baa72`, the hash the
  row cites; `round-34/sources/receipts.json` says `textWords 1276`, `bodyBytes 726758`.
- That text equals the live English page word-for-word (step 7), so **nothing changed** since round
  34; only the negotiated locale differed.
- `.ufo/waves/round-36/fetch_sources.py:59` sends `Accept-Language: en-US,en;q=0.9`;
  `scripts/source_snapshot.py:99` sends only `{"User-Agent": UA, "Accept": "*/*"}`. The realrun
  recorder diverged from the lane's own row-opening fetcher, and returns pt-BR deterministically
  (step 5), not flakily.
- Header-driven, not UA-driven: UA constant across steps 2/3/4, only `Accept-Language` varied →
  pt-BR / en / de. `Vary: Accept-Encoding` only on all three responses (no `Vary: Accept-Language`),
  so a shared cache could hand a pt-BR body to an English request; `cache-control: private, no-cache,
  no-store, must-revalidate` limits that.
- Contract check: C1 judges a **recorded** body ("it does not fetch"), so this is a recorder/realrun
  defect, not a C1 falsification. The tool honestly reports `quote_missing` for the body it was given.

## `moved` hops (`live/h1.txt`, `live/h2.txt`)

1. `GET …/docs/sharing/webmasters/` → **301**, `location: https://developers.facebook.com/documentation/sharing/webmasters`
2. `GET …/documentation/sharing/webmasters` → **200**, no further hop. Recommendation: keep the requested URL; the anchor already names the target, and the redirect is
permanent (301), matching S088. The finding is information, not a row defect.

## Saved bodies (absolute)
`/fast/scratch/hyaku/kake-r36w2/ReopenFlagS068/` —
`live/s068.html` 729,616 B `3228724d…76de1` (pt) · `live/s068-en.html` 723,692 B `1b1953ac…62b1` (en) ·
`live/s068-de.html` `378a25c9…0528` (de) · `live/s068-recorder-emulated.html` 729,571 B `0dbcb977…c45a` ·
`live/{h1,h2,h3}.txt` headers · `live/s068.text.txt`, `live/s068-en.html.visible.txt` text ·
`snap/S068.body` 729,573 B `e54b9487…a120` (the recorded snapshot: 2× `Sem essas tags do Open Graph`,
0× English quote).

## Not verified
- No sealed counter or C1 scoring run (outside this seat; locale is outside C1's predicate).
- Whether other `quote_missing` findings (S004-S008, S017, S025, S065) share this cause — not checked.
- Geo-IP influence on the headerless default untested (egress cannot be varied); en/de probes only
  prove header-driven selection.
