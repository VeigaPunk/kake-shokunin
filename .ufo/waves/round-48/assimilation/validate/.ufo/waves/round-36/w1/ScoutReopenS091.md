# ScoutReopenS091 — S091 (UAX #15) re-opened live, independently

No sealed-key tree touched; no lane file mutated; only this report written in the lane.

## What I did
Fresh GET (ordinary means, UA `kake-r36-scout/1.0 (source recheck; contact lane KakeR36)`), sandbox
`/fast/scratch/hyaku/kake-r36w1/ScoutReopenS091/`.

```
curl -sS -L --max-time 100 -o tr15-live.html -w 'http=%{http_code} size=%{size_download} final=%{url_effective} type=%{content_type}'
  https://www.unicode.org/reports/tr15/
```
Observed: `http=200 size=141588 final=https://www.unicode.org/reports/tr15/ type=text/html; charset=UTF-8` (curl exit 0), at `2026-10-23T01:35:39Z`.
Headers (HEAD, exit 0): `last-modified: Wed, 12 Aug 2026 17:33:14 GMT`, `server: cloudflare`, no ETag. No redirect.
Body sha256 `efcf19da85342bd87fb93b590975ca422597243f2e19c6cb46e941d0d2d48d73`.

## Revision and version (observed)
- `Version Unicode 18.0.0`, `Date 2026-08-12`, `This Version .../tr15/tr15-58.html`, `Previous Version .../tr15-57.html`, `Revision 58` — live text offsets 96–470 and the Modifications section (`Revision 58 [KW]`).
- Retained copy says the same: S091.txt offsets 119 (`Unicode 18.0.0`), 221 (`tr15-58.html`), 428 (`Revision 58`).

## Definitions (verbatim, from the live page; S091.txt is byte-identical)
§1.1 Canonical and Compatibility Equivalence:
> "Canonical equivalence is a fundamental equivalency between characters or sequences of characters which represent the same abstract character, and which when correctly displayed should always have the same visual appearance and behavior." (S091.txt [3940:4060]…[4460])
> "Compatibility equivalence is a weaker type of equivalence between characters or sequences of characters which represent the same abstract character (or sequence of abstract characters), but which may have distinct visual appearances or behaviors." (S091.txt [4460:4740], continues to ~5170)

§1.2 Normalization Forms, Table 1 (S091.txt ~[7040:7160]):
> "Normalization Form KC (NFKC) — Compatibility Decomposition, followed by Canonical Composition"
and prose: "Normalization Form KC additionally folds the differences between compatibility-equivalent characters that are inappropriately distinguished in many circumstances. For example, the halfwidth and fullwidth katakana characters will normalize to the same strings, as will Roman numerals and their letter equivalents." (S091.txt [10600:11020])

## Examples present (all in the live page, all in the retained text)
- Ligatures: §1.2 Figure 6 prose "The 'fi' ligature changes into its components 'f' and 'i'…"; Table 7/8 rows l,m: `"Ä\uFB03n"` → NFKC `"Äffin"`, note "The ffi_ligature (U+FB03) is not decomposed [in NFC]… is decomposed in NFKC". (S091.txt [36600:37000], [37600:38000])
- Fullwidth/width: §1.1 Figure 2 "Width variants ｶ → カ"; §1.2 halfwidth+fullwidth katakana sentence above.
- Circled digits: §1.1 Figure 2 "Circled variants ① → 1" (S091.txt [5819:5850]).
- Roman numerals: §1.2 sentence above; Table 7 row n "the ROMAN NUMERAL IV (U+2163) is not decomposed"; Table 8 row o′ `"Henry \u2163"` → NFKC `"Henry IV"` (S091.txt [37162], [37800:37960]).
- Also: superscripts/subscripts, squared characters, fractions, NBSP→SPACE, font variants (Figure 2).

## Comparison with the retained copy — identical, not merely similar
1. Retained body vs live body: `gunzip -c .ufo/waves/round-36/sources/S091.html.gz | sha256sum` = `efcf19da…d2d48d73` = live body sha (byte-identical, 141588 bytes). Receipt agrees: `receipts.json["S091"].bodySha256` = `efcf19da…`, `bodyBytes` 141588, `accessedUtc` `2026-10-23T01:08:59Z`.
2. Retained text vs text regenerated from the live body with `fetch_sources.py::visible_text` (script/style and comments dropped, tags removed, entities decoded, whitespace collapsed): both 84656 bytes, `equal True`, sha256 `517c1892ef8f657b4d240d5779404e660753b1c713dcee0138d05f9ec8d23e96`; equals `receipts.json["S091"].textSha256`. So the retained .txt is exactly what its body yields under the documented rule; no extractor drift.
3. No content drift between 01:08:59Z and 01:35:39Z (≈27 min, same day); page's own `last-modified` is 2026-08-12, older than both fetches. Nothing in this source changed under the round; S091 is not a moving target this round.

## Falsifier-relevant notes for C1 (advisory, not a claim about whether C1 is right)
- The page serves `\uFB03`/`\u2163` **as literal escaped text** in Table 7/8 cells (visible text contains the six characters `\uFB03`), while Figure 2 cells show the real characters (`①`, `ｶ`, `Ω`). A registry quote copied from a rendering that shows the character (e.g. "ï¬ƒ") will NOT match S091's text; a quote of the escape text will. Quote-normalisation must not unescape `\uXXXX` in source text, only in the quote side (or not at all) — otherwise it fabricates matches.
- The draft-status paragraph exists only inside an HTML comment (`<!-- NOT YET APPROVED … END NOT YET APPROVED -->`); comment-stripping (as in `visible_text`) correctly keeps the approved paragraph. A checker that strips only tags would make the text contain a sentence the live page does not display — a real divergence path for "HTML text" (contract bullet c).
- The text is a single 84656-byte line (whitespace collapsed). Any quote matcher that relies on newlines/sentence boundaries for this source will see one line; offsets and byte sizes above give ground truth.

## Sandbox artifacts (absolute)
- `/fast/scratch/hyaku/kake-r36w1/ScoutReopenS091/tr15-live.html` (141588 B, sha efcf19da…)
- `/fast/scratch/hyaku/kake-r36w1/ScoutReopenS091/S091-live.txt` (84656 B, sha 517c1892…)
- `/fast/scratch/hyaku/kake-r36w1/ScoutReopenS091/sec1-1-live.txt`, `sec1-2-live.txt`, `sec6-live.txt` (section extracts)
- `/fast/scratch/hyaku/kake-r36w1/ScoutReopenS091/retained.html` (decompressed retained body, same sha)

## Not verified / residual unknowns
- Did not verify Unicode 18.0.0 against the Unicode Standard's own version registry, nor that `tr15-58.html` is still the *Latest* (the page states it; I did not fetch `/versions/`).
- Did not check whether the S093 (Wikipedia) reject candidate or any other source shows a different NFKC wording; out of this ticket's scope.
- No tool installed or upgraded; nothing to record. No network fetch beyond the single GET + one HEAD (exit 0) to `unicode.org`, which is not an owned site. No processes left running.
