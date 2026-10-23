# KakeR36.ExecProbeQuoteMatch — does rule (c)+(d) find each Gate quote in its own source?

Hypothesis: on real retained sources, (c)+(d) finds each Gate quote in its own source and gives no hold for a quote in an unrelated source. **First half holds (22/22, correct media type); second half does not** — 1 cross-source false hold (S071 in S073), and rule (d)'s whitespace *deletion* accepts 85.2% of single-space corruptions of a quote (0% under the older collapsing rule).

Sandbox `/fast/scratch/hyaku/kake-r36w1/ExecProbeQuoteMatch/`. I did not touch `/fast/scratch/hyaku/kake-r36/` or any sealed path, ran no counter, made no network request, installed no tool, and wrote nothing in the lane but this report.

## Inputs (read-only)
- Quotes: `corpus/lessons/round-34.md:34-44` (S067-S077) and `round-35.md:44-54` (S078-S087, S006) — 22, extracted by `extract.py` from `quote “…”` on `- S0NN —` lines.
- Bodies: `.ufo/waves/round-34/sources/S067..S077.html.gz`, `.ufo/waves/round-35/sources/S006,S078..S087.html.gz`, plus 7 cross-only extras `.ufo/waves/round-36/sources/S088..S094`.
- Older rule compared: `.ufo/waves/round-35/fetch_sources.py:45-50 visible_text` (whitespace collapsed, not deleted).

## Commands (all `cd /fast/scratch/hyaku/kake-r36w1/ExecProbeQuoteMatch && export TMPDIR=$PWD/tmp`)
1. `python3 -B extract.py` → exit 0, `bodies 22 checks 22`.
2. `python3 -B analyze.py round-34 round-35 round-36` → exit 0, `bodies 29 quotes 22  own holds: contract 22/22  old 22/22`; `cross holds (contract c+d): 1`; `(old visible_text): 1` (`analyze.txt`).
3. `python3 -B typography.py` → exit 0: all 22 `ws-insensitive equal: True`; no quote contains a non-ASCII character; no source region differs from its quote except whitespace (`typography.txt`).
4. `python3 -B permissive.py` → exit 0: `1891 total` variants; `accepted under rule (d) delete-whitespace: 1612 (85.2%)`; `collapse: 0 (0.0%)`; D (delete space) 279/279, I (split word) 1333/1333, S (space→`-`) 0/279.
5. `python3 -B ablate.py` → exit 0: tag removal load-bearing for 11 of 18 HTML quotes; comment, script and template removal load-bearing for **none**; `style` only for S087.
6. `python3 -B final_probe.py` → exit 0: the S078 sentence crossing the RFC soft wrap (`/.well-\n   known/security.txt`) has `hold_d=True hold_c=False literal=False`.
7. `python3 -B discriminate.py` → exit 0: 638 pairs, 23 holds under (d), 23 under collapse, 0 disagreeing; only `S071@round-34` holds in a second body.

## Own-source holds and misses
22/22 hold under (c)+(d) and 22/22 under the old rule. **Zero misses**, with two caveats.
- **Media type, not the quote rule, is the risk.** Receipts record no `contentType`, so the probe sniffs it (markup prefix → html/xhtml, else text/plain). My first run typed S081 (`en.wikipedia.org/wiki/Security.txt`, a Wikipedia *article*) as `text/plain` and it **missed** (longest normalized prefix 36/142 chars; divergence at `<a rel="mw:WikiLink" …>`). 11 of 22 quotes (S068, S069, S071, S077, S079, S080, S081, S083, S086, S087, S006) miss if their HTML body is read as `text/plain`. A tool inferring media type from the URL suffix is wrong on 1/22.
- **Rule (d) hides the RFC's line-wrap hyphenation.** The round-35 scribe shortened S078 because `quote in text` failed across `.well-\n   known` (`w1/ScribeGateLines.md` finding 1); under (d) the full sentence holds (`literal=False`), because deleting whitespace glues `-` to `known`, so a quote that mis-transcribes a hyphenated wrap as one token is accepted. Typography is otherwise clean: no curly-vs-straight quote, NBSP or dash divergence in the 22 quotes.

## Cross-source false holds
1/462 foreign pairs (rounds 34+35; 1/638 with round-36 added): `S071@round-34` (`Fetch the complete documentation index at: /llms.txt Use this file to discover all available pages`, from developer.x.com → docs.x.com/overview, record *reject*) also holds in **S073 (docs.discord.com, an unrelated *admit*)** at the page-head banner `Documentation Index  Fetch the complete documentation index at: /llms.txt …`. Both are Intercom-hosted docs shells (`llms.txt` count 2 in S071, 1 in S073); it holds under the old rule too, so this is a property of the sources, not of (d). Reverse (S073 in S071) does not hold. Prefix sweep: 3-word fragments cross-hold 6/588 pairs (`If you want` S006→S068), 5 words 1/588 — false holds live at short length, and the contract sets no minimum quote length.

## Rule (d) is whitespace-blind — sharpest defect
Deleting every whitespace character makes word boundaries irrelevant: 1,612 of 1,891 single-space corruptions still hold (85.2%), vs 0 under collapse. Verbatim: `T he four required properties for every page are` holds (S067); `W ithout these Open Graph tags, …` holds (S068); all 279 space merges hold. Faithful to the contract as written, so this is a **contract** finding to route, not a tool bug: a row's quote can be re-spaced arbitrarily and still "hold". (d) as specified cannot bound transcription error; the older collapse rule can. Rule (c) is barely exercised here: only tag removal is load-bearing (11/18 HTML bodies); comments 429, templates 33 (S068 6, S077 4, S094 23), scripts 566 — none load-bearing. A tags-only tool scores 22/22 on this corpus.

## Gate-line defect found in passing
`corpus/lessons/round-35.md:53` says the S087 quote is `11 words`; it is **12** (`404`,`-`,`GitHub`,`Docs`,`GitHub`,`Docs`,`Page`,`not`,`found.`,`Return`,`to`,`home.`), and the lesson's own pointer at `:194` says "12 words, not 11" — the correction never reached the Gate line. Also S087's source returned HTTP 404, so rule (a) runs no quote check for it: 1/22 real Gate quotes sits on a non-200 source and can never be re-verified by the C1 tool.

## Not verified
No sealed case, no counter run (no key), no verdict on the round. Rules (a),(b),(e),(f),(g) not implemented (out of scope). `contentType` is inferred from the body, not observed; no live fetches.

## Artifacts (sha256, sandbox `/fast/scratch/hyaku/kake-r36w1/ExecProbeQuoteMatch/`)
`match.py` `4a400a09…65a4ba` · `extract.py` `978ba027…44ebb10` · `analyze.py` `9c566df9…73f50d33` · `permissive.py` `d0a67deb…bfc90f` · `ablate.py` `b5d0b5fa…f565fd7` · `typography.py` `fef101dd…00d2d4` · `discriminate.py` `7f150b8e…3f2ecc96` · `final_probe.py` `3a4e6fd4…4d0fe8` · `manifest.json` `6bd5c0c3…e1c58c74`. Transcripts: `analyze.txt` `afe19633…f945d861`, `permissive.txt` `43337174…9b4f43b5`, `ablate.txt` `85375978…f8b163ee`, `final_probe.txt` `da756248…59d556c107`, `discriminate.txt` `1cd13de6…2794d458ab`.
