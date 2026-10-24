# Kake R35 w1 — ReviewS074Head (routed defect 5 of the round-34 closure)

Axes: freshness (judged here — the SOURCES.md S074 record must state only what the retained
bytes show); operability untouched by this item. Godspeed: cheap parallel counts first, kept
what reproduced, discarded nothing into the lane but the report.

## What was attacked

Routed defect 5 (`corpus/lessons/round-34-verifier-spotcheck.md`, "Routed defects" item 5):
Gate `corpus/lessons/round-34.md:41` and the SOURCES.md S074 row say "no og: occurrence". The
closure's own spot-check claims the retained page head carries 3 `og:` metas. I reproduced the
counts independently from the retained bytes only — no live request was made (none assigned;
owned-site and network bounds observed).

## Commands and observed output (all from /home/vgpnk/Projects/shokunin/kake-shokunin)

1. `zcat .ufo/waves/round-34/sources/S074.html.gz | grep -o 'og:' | wc -l` → `3`, exit 0
   (case-insensitive `grep -io` recount also 3; no other casing present).
2. `zcat .ufo/waves/round-34/sources/S074.html.gz | grep -oiE '.{0,40}og:[a-z0-9:_-]*' | sort | uniq -c | sort -rn` →
   exactly three contexts, one each: `<meta property="og:title`, `<meta property="og:image`,
   `<meta property="og:description` (exit 0). These are the only `og:` substrings in the body.
3. `grep -o 'og:' .ufo/waves/round-34/sources/S074.txt | wc -l` → `0`, exit 0.
4. `zcat .ufo/waves/round-34/sources/S074.html.gz | sha256sum` →
   `099bc4f9d7a44da589a089a8954515e3c615d4be2f3fe85b9766f1d9c9a90bbc`, exit 0 — equal to
   `.ufo/waves/round-34/sources/receipts.json` S074 `bodySha256`, `bodyBytes` 860230
   (receipts.json:86-95). So the counted bytes are the exact retained fetch.
5. Head scope, `python3 -c` with `re.search(r'<head\b[^>]*>(.*?)</head>', h, re.S|re.I)` over
   the decompressed body → `og_anywhere 3 og_in_head 3 og_after_head 0`, exit 0. The `<head>`
   spans chars 53–1351 of 857,871 and holds 6 `<meta>` tags; the three `og:` metas are
   `<meta property="og:title" content="Telegram Bot API">`, `og:image`, `og:description`
   (the Bot API page describing itself).
6. `wc -w .ufo/waves/round-34/sources/S074.txt` → `73876`; `sha256sum` →
   `9be76fdab951f0aa007fcf6c17fcebc68c70cc171f40745e701286fa046a9554` — both equal the row's
   "(73,876 words, …)" anchor cell and the receipt's `textSha256`/`textWords`
   (SOURCES.md:82; receipts.json:95-96).

## Finding — routed defect 5 confirmed, severity: accuracy defect, reject unaffected

- "No og: occurrence" is false for the retained page body (3 `og:` metas, all in `<head>`) and
  true only for the retained extracted text `S074.txt` (0 occurrences). The SOURCES.md:82
  parenthetical and round-34.md:41 overclaim by one scope word.
- The reject and its substantive reason stand: LinkPreviewOptions holds only a bot's switches
  (is_disabled, url, prefer_small_media, prefer_large_media, show_above_text) and names no page
  tag, so the page grounds no publisher-side metadata rule. The three `og:` metas are the
  Telegram page's own social-preview metadata, not a publisher-side rule; the flip condition
  (a Telegram primary naming the tags its preview reads) is still unmet.

## Deliverable

- Draft note: `/fast/scratch/hyaku/kake-r35/w1/ReviewS074Head/s074-note.md` — one-paragraph
  correction note shaped on the "Round-31 resolution note for S053 and S054" line
  (corpus/SOURCES.md:160): names the routed defect, scopes the parenthetical to the retained
  text, gives both counts, keeps the reject and its reason, ends "Status, recheck and used-by
  cells of S074 are unchanged (`rejected`, `90d`, `—`)". Placement guidance included (append
  after the Round-31 wave-2 anchor note for S059, same notes area).
- Acceptance: counts reproduced above; note drafted; I wrote nothing to SOURCES.md and no
  status, recheck or used-by cell is touched — the note corrects by append only.

## Residual risk and verification gaps

- Live page not fetched by me (bounds; not assigned). The independent live confirmation in
  `round-34-verifier-spotcheck.md` (spot-check table, S074 row: "3 og: metas") is cited as the
  closure's recorded result, not re-observed here.
- Head extraction used a regex over the decompressed body, not a full HTML parser; with the
  head span 53–1351 and og_after_head 0, placement is not in doubt for this file.
- `grep -o 'og:'` counts literal substrings; the context listing (command 2) shows all 3
  occurrences are meta properties, so no other substring source inflates the count.

Tooling: nothing installed or updated (operator directive 2026-10-19 — no tool needed).
