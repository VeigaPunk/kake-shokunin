# ScoutRejectAmendment

Scope: screen staged `/home/vgpnk/Projects/shokuknow/merge/kake/amendments/corpus/knowledge/crawler-identity.md` (MERGE-REPORT.md line 25: "amendment | round2 | ... | target already exists in the lane - append, do not replace") against lane `corpus/knowledge/crawler-identity.md` and row S263. Read-only; scratch deleted after.

## COMPARISON:
Both files are the same entry on the same URL (`.../search/docs/crawling-indexing/googlebot`), the same section, the same revision line ("Last updated 2026-02-03 UTC"). Staged cites it as S300 (package id); the lane already holds it as S263 (SOURCES.md line 153; `grep S300` in lane SOURCES.md = 0 rows). Same URL under a second id is a duplicate row, not a new source. (CriticIds in round 51 already mapped S300<->S263.)

Sentence-level (staged -> lane), measured by normalised-substring test plus a read:
- Heading `# "Googlebot" is a family name, not one crawler`: identical.
- Metadata: staged source/verified-at 2026-10-23, recheck `180d` + curl command; lane 2026-10-24 (later, retained body), recheck `180d`. Lane is the later, retained-body-backed version. Staged adds only the curl one-liner (`grep -c 'generic name for two types of'` -> 1); lane's S263 staged recheck command is the same string (lessons/round-51.md line 58).
- Quote "Googlebot Smartphone: a mobile crawler that simulates a user on a mobile device.": lane holds the same sentence as a rendered quote (`Googlebot Smartphone : a mobile crawler ...`, no trailing period) plus the Desktop twin, the "identify the subtype ... HTTP user-agent request header" quote and the robots product-token quote. Staged has fewer quotes (one) and states the same subtype-from-user-agent point in prose. Nothing the staged quote says is missing from the lane.
- Bullet 1 "A user-agent string is the only thing a server log records about the crawler.": verbatim the lane's line 31 - the stale sentence C3 corrects append-only. Appending would re-state it verbatim, uncorrected.
- Bullet 2 "The same page can be crawled twice by the same engine under two names.": identical.
- Bullet 3 (staged: S096 parser-not-crawler): identical to the lane's bullet 4 except the staged tail "...the first is S096" vs lane "This row answers the second question."
- "What this entry does not establish": crawl rate/scheduling, non-Google bots, specific crawler on a specific property - all three present in lane; only the staged "(see CANNOT-ANSWER.md)" pointer differs, and that file is a package artifact not in the lane.
- Lane-only content absent from staged: the robots product-token bullet (both types obey one token, so robots.txt cannot target a subtype; ties to S011/S095), the Desktop quote, the "identify subtype" quote, the "Quote classes (round-51 correction)" section.
- Staged-only content: none that is knowledge. The only staged-only sentences are the S300 id, the 2026-10-23 dates, the CANNOT-ANSWER pointer.
Result: staged = a strict subset of the lane entry, 2 days older, under a duplicate id. The staged header's claim that "the lane's current text is the superseded reading" is false: the lane text is the later and fuller one.

## SOURCE CHECK:
- `curl -fsSL` of the URL on 2026-10-27: HTTP 200, 175561 bytes (== retained S263.html byte count). sha256 differs from the retained body (`efa3261f...` vs `6afbdc82...`): `cmp` first differs at byte 51658 and the diff is attribute ordering (`data-category`, `aria-label` lines swapped); whitespace-collapsed text content identical. So the page is unchanged in substance; no live drift found.
- Revision line "Last updated 2026-02-03 UTC": 2 occurrences in both live and retained. Unchanged.
- Staged recheck `grep -c 'generic name for two types of'`: raw hit count 1 in live and retained [grep -c counts lines; I counted occurrences after whitespace collapse: 1]. Reproduces.
- Staged quote "Googlebot Smartphone: a mobile crawler that simulates a user on a mobile device." (13 tokens, 80 chars):
  - raw (whitespace-collapsed HTML): 0 hits in live and retained - markup sits inside: `Googlebot Smartphone</b></a>: a mobile crawler ... device.`
  - tag-stripped rendered text: 1 hit (so the words are on the page, as a rendering).
  - single article text node, per the C3 quote rule: 0 hits. It spans two text nodes: `Googlebot Smartphone` (inside `<b>`/`<a>`) and `: a mobile crawler that simulates a user on a mobile device.`. Under the round-59 rule it would fail the "substring of ONE text node" test, the same defect class as the round-51 lane's rendered quotes.
  - the lane's `Googlebot Smartphone : a ...` (inserted space) is 0 in all forms, as the lane's own round-51 correction already says.
- Heading quote "Googlebot is the generic name for two types of web crawlers used by Google Search": 0 raw hits (markup between "types of" and "web"), 1 rendered hit. The 9-word prefix used as the lane's Gate quote is a raw hit (1).
- "identify the subtype of Googlebot": 1 raw hit (lane quote, supports the amendment's prose).
- Not checked: tag-level text-node positions for the other staged claims (no other staged quotes); span_tools.py handles only S425/S426, so the node test above is my own script (regex tag split over `devsite-article-body`..`<devsite-content-footer`).

## DECISION LINE:
REJECT - do not append the staged crawler-identity amendment: it is a strict subset of the lane's existing S263 entry under a duplicate id (S300 vs S263), repeats the stale "only thing a server log records" sentence verbatim, and its one quote spans two text nodes; FLIP to admit if it carries a sentence not already in the lane (none found) or if the lane entry is deleted/loses S263, in which case re-stage only with a one-text-node quote and the S263 id.
Observed vs inference: the subset result and quote-node counts are measured; the claim that "no other package context could add knowledge" is [INFERENCE] (I read only this file and MERGE-REPORT).

VERDICT: REJECT - staged amendment is a duplicate/subset of lane S263 entry (no new knowledge, reintroduces the stale line-31 sentence); source unchanged live.
