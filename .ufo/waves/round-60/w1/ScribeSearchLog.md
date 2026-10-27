# ScribeSearchLog

Seat: scribe, round-60 w1, lane `kake-shokunin` at base `97cdc122379711c2b02a8970752c8782da3ac81d`.
Access date 2026-10-27 (UTC). Read-only seat: no lane mutation beyond this file, no git/jj mutation, no counter or
tool run, no network fetch. Every figure below was observed with the command printed beside it in `COMMANDS:`.
Target of the draft: `corpus/lessons/round-60.md` → `## Search log (rule 5)` (that file does not exist yet:
`ls corpus/lessons/round-60.md` → "No such file or directory"); `corpus/SOURCES.md`'s own `## Search log`
still ends at its round-53 note (line 226), and round-59's rule-5 note sits at
`corpus/lessons/round-59.md:130` — so the lesson is where the round note has lived for rounds 54–59.

## SEARCH LOG:

Draft paragraph, one bounded search, prose note, lane count vocabulary kept (`Identified / screened / included /
excluded`, `Stop`) with the doctrine's exclusion reasons and stop label:

Round 60, robots.txt posture and limits per Google crawler category (assimilation theme from `merge/kake/`).
Question: what does Google's own documentation state as the robots.txt posture — obey, ignore or conditional —
of each of its three crawler categories, and what limits does it put on the robots.txt file itself? Where: the
staged package `/home/vgpnk/Projects/shokuknow/merge/kake` — `SOURCES.append.md` (129 staged rows; 28 carry
`robots`; 12 of those are Google-published; 5 of those name a crawler: S323, S327, S337, S398, S415) and
`MERGE-REPORT.md` (20 lines matching `google|robots`; its two theme entries are
`common-crawlers-japanese.md`, line 51, and `google-robots-txt-limits.md`, line 122). The lane's held ground:
55 knowledge entries, 23 mentioning robots, `googlebot-verification.md` the only entry mentioning user-triggered
fetchers or special-case crawlers (8 lines); a 164-row registry of which 25 rows mention robots and no entry
carries `generally ignore`; base row S425, whose `scope` cell claims "the three crawler categories and their
robots.txt posture" and whose `teaches` rests on the verify-requests page (round-59 S426). Then the pages opened
directly: the S425 URL re-opened (retained `sources/S427.html`, HTTP 200, 74,477 bytes, sha256 `d70ce6f5aa51…`,
fetched 2026-10-27T04:03:36Z, title `Google Crawler (User Agent) Overview`, `Last updated 2026-06-12 UTC`) and,
through the third row of the held S426 category table, `google-user-triggered-fetchers` (retained
`sources/S428.html`, 76,197 bytes, sha256 `0f296b8636d5…`, 04:03:37Z, `Last updated 2026-08-19 UTC`) — a
lane-found route, not a staged row: the held entry itself records the gap (`googlebot-verification.md:134` says
it does not carry the three category pages the table links), and the table's third cell is the link followed.
Included 3: S427, the S425 URL re-opened by document with a scope that records the posture per category
("They always respect robots.txt rules for automatic crawls." for common crawlers, the product-agreement
conditional for special-case crawlers) instead of the flat claim; S428, the user-triggered page, which states
the posture the older table states unqualified ("these fetchers generally ignore robots.txt rules"); S429, the
staged S415 `google-robots-txt-limits.md` re-grounded and renumbered by document, where the file's limits sit
("The instructions in robots.txt files cannot enforce crawler behavior" — its limits sentence). Excluded 1:
staged `common-crawlers-japanese.md` (staged S337, `google-common-crawlers?hl=ja`) — screened and refused on
theme, not on the quote rule: its two claims (one `User-agent:` token per rule, and a `Googlebot` block reaching
several products) are crawler-addressability claims, not posture or limits, and its evidence is a translated
edition only (no English-edition body was opened or retained, so the row would rest on `?hl=ja`); its quoted
sentence measures 68 characters and 7 whitespace tokens, inside the round's 6..25 / ≤160 window, so the quote
rule is not the reason. Same title-level screening, recorded not counted: staged S398 is the already-registered
S425 document (round 59), and staged S323 (crawl-error troubleshooting) and S327 (Japanese robots.txt blog post)
are off-theme. Stop: bounded by design — one theme per round, C3 caps the round at two new rows plus one
append-only correction tail, and each of the three categories in the held table is now closed: common crawlers
on S427, special-case crawlers on the held S426 quote "may or may not respect robots.txt rules",
user-triggered fetchers on S428; the file's limits land on S429, and the correction tail is owed because S426
(`Last updated 2026-03-20 UTC`) states the user-triggered posture unqualified while S428 (`2026-08-19 UTC`)
qualifies it. Surfaces left open, named as leads and not rows: the English `google-common-crawlers` and
`google-special-case-crawlers` pages the held entry lists as its own gap.

## COMMANDS:

Every count above, with the command as run (cwd `kake-shokunin` unless the staged path is named):

| figure | command | observed |
|---|---|---|
| 129 staged rows | `grep -cE '^\| S[0-9]+ \|' /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` | 129 |
| 28 rows carrying robots | `grep -cE '^\| S[0-9]+ \|.*robots' …/merge/kake/SOURCES.append.md` | 28 |
| 12 Google-published of those | `grep -E '^\| S[0-9]+ \|.*developers\.google\.com.*robots' …/SOURCES.append.md \| wc -l` | 12 |
| 5 naming a crawler | same pipe + `grep -ic crawler`; ids via `cut -d'\|' -f2` | 5 (`S323 S327 S337 S398 S415`) |
| 20 MERGE-REPORT lines | `grep -ciE 'google\|robots' /home/vgpnk/Projects/shokuknow/merge/kake/MERGE-REPORT.md` | 20 |
| 2 theme entries | `grep -nE 'google-robots-txt-limits\|common-crawlers-japanese' MERGE-REPORT.md` | lines 51, 122 |
| 55 knowledge entries | `ls corpus/knowledge/*.md \| wc -l` | 55 |
| 23 robots-mentioning | `grep -rl -i robots corpus/knowledge/*.md \| wc -l` | 23 |
| 8 user-triggered/special-case lines, 1 file | `grep -rn -i -E 'user-triggered\|special-case' corpus/knowledge/ \| wc -l`; `grep -rli …` | 8; `googlebot-verification.md` |
| 164-row registry | `git show 97cdc12…:corpus/SOURCES.md \| grep -cE '^\| S[0-9]+ \|'` | 164 |
| 25 robots rows | `git show 97cdc12…:corpus/SOURCES.md \| grep -E '^\| S[0-9]+ \|' \| grep -c -i robots` | 25 |
| S425 overstatement present | `git show 97cdc12…:corpus/SOURCES.md \| grep -c 'the three crawler categories and their robots.txt posture'` | 1 |
| 0 `generally ignore` in held entries | `grep -rc 'generally ignore' corpus/knowledge/ \| grep -v ':0' \| wc -l` | 0 |
| S427/S428/S429 absent at base | `git show 97cdc12…:corpus/SOURCES.md \| grep -cE '^\| S42[789] '` | 0 |
| S426 categories | `grep -o -E '>Common crawlers<\|>Special-case crawlers<\|>User-triggered fetchers<' .ufo/waves/round-59/sources/S426.html \| sort -u \| wc -l` | 3 |
| S426 category-page link | `grep -o 'href="/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers"' .ufo/waves/round-59/sources/S426.html \| wc -l` | 2 |
| S426 qualification | python: article-block text of `S426.html` (article block only) → `count('generally')`, `count('ignore robots.txt')` | 0; 1 |
| S428 qualification | same over `round-60/sources/S428.html` | 1; 1 |
| quote sizes | python `len(q), len(q.split())` on the three spans quoted above | 58/8; 92/14; 119/20 tokens |
| S337 quote size | python over the staged entry's quoted sentence | 68 chars, 7 whitespace tokens |
| titles / `Last updated` / receipts | python `re.search` over each retained body; `sources/receipts.json` | titles and dates as quoted; bytes 74,477 / 76,197 / 178,797 |
| 4 identified / 4 screened / 3 included / 1 excluded | set arithmetic over the four candidate sources named in the note (S415, S337, S427 re-open, S428); S426 is held base, not a candidate | as stated |

Surface articles were read as the article block only (`class="devsite-article-body` … `<devsite-content-footer`),
whitespace-collapsed, for S426/S427/S428/S429, matching the round's quote-rule extraction.

## Notes and limits

- No tool installed or upgraded this round (nothing needed); no network fetch by this seat; the three bodies and
  their receipts are the wave's retained artifacts.
- The quote forms in the draft are inside the frozen 6..25-whitespace-token / ≤160-character window as measured
  above, but this seat does not certify `c60_quote_truth.py` (C5) — that counter is built elsewhere this wave and
  no after-state exists yet. Every statement about the three entries' own `source:`/`verified-at:` headers,
  their used-by cells, the correction tail's landed bytes and the Gate lines is therefore left to their seats and
  is **[INFERENCE]** here, not observation.
- The exclusion of staged S337 is reported as the contract assigns it (screen-reject, Japanese edition) and is
  grounded on the two observed facts above (theme = addressability; edition = `?hl=ja` only); its quote is
  inside the token window, so no token-rule reason is claimed.
- Scratch dir `/fast/scratch/hyaku/kake-r60/ScribeSearchLog` was created empty and removed at exit; nothing was
  copied into a `.files/` directory because this report carries no code or artifact.

VERDICT: search-log paragraph drafted with every count command-backed (129 staged rows → 12 Google robots → 5 crawler-naming → 2 theme candidates; 55/23/8 held ground; 4 identified, 4 screened, 3 included, 1 excluded), stop labelled bounded-by-design; no counter run, no after-state claimed.
