# ScribeSearchLog

Draft of the two round-59 lesson sections, `## Search log (rule 5)` and `## Trend inputs` (model
`corpus/lessons/round-58.md`), for theme `crawler identity verification signals` (assimilation from
`merge/kake/`; `contract.md` § Frontier step). Read-only: this report is the only lane file I wrote; no
git/jj mutation, no counter of this round run against the lane, no claim scored. Statements below carry
the seat that measured them; my own observations are marked (own).

## SEARCH LOG:

Round 59, crawler identity verification signals (assimilation theme from `merge/kake/`). Question: how
does Google's own crawler documentation tell a publisher to tell a genuine Google crawler request from an
impostor, and which signals does it name? Where: the staged package (staged entry
`crawler-identity-three-signals.md`, staged row S398, the same URL as S425; staged
`amendments/corpus/knowledge/crawler-identity.md`, round2; staged `yahoo-crawler-ua-carrier-survey.md`,
staged row S394), the lane's held ground (`w1/ScoutLaneCrawlerIdentity.md`: registry 162 rows with no
S425/S426 row, no entry holding Google IP or reverse-DNS material, no Yahoo DNS entry, the only
crawler-identity entry being `crawler-identity.md` on S263), then the pages opened directly:
`overview-google-crawlers` (retained `sources/S425.html`, HTTP 200, 74,477 bytes, sha256
`ff2b9fd7ed07…`, fetched 2026-10-27T01:21:22Z, userAgent `kake-shokunin-round59`) and, through its own
in-article link `Learn how to use these details to verify Google's crawlers and fetchers.` (S425.html
line 1284; the same href also sits once in the page navigation, line 720 — own), `verify-google-requests`
(retained `sources/S426.html`, 69,789 bytes, sha256 `8df9d4ade1d1…`, same fetch; `sources/receipts.json`).
Included 2: S425, from staged S398 renumbered by document to the registry's next unused id after S424;
S426, lane-found with no staged id. Excluded, each screened by a wave-1 seat:

- the staged `amendments/corpus/knowledge/crawler-identity.md` (round2) — `w1/ScoutRejectAmendment.md`:
  a strict subset of the lane's S263 entry under a duplicate id (staged S300 vs lane S263, same URL, same
  section, same `Last updated 2026-02-03 UTC`), it repeats the stale line-31 sentence verbatim, and its
  one quote spans two text nodes; the live page is unchanged in substance (HTTP 200, 175,561 bytes, byte
  diff attribute ordering only). Flip: admit if it carries a sentence not already in the lane.
- the staged `yahoo-crawler-ua-carrier-survey.md` (S394) — `w1/ScoutRejectYahooUA.md`: it cites an
  own-work count file outside the lane and outside the registry, quotes no operator page, its DNS thesis
  belongs to `archives/002855.php` which the lane does not hold (round-55 S386 refusal, round-58
  id=2855 exclusion), its recheck greps a string the sweep script itself writes, and the ads-page figures
  no longer reproduce (436,802 → 102,822 bytes live). Flip: adopt 002855 as a lane row and re-cut the
  entry on its sentences under a CJK-units quote rule.

Stop rationale: one theme per round and two entries — the contract's C3 caps the round at two new rows
plus one append-only correction tail, and S425+S426 close the identification-signal half (three signals
on S425; the reverse-then-forward DNS procedure and published IP-range lists on S426) with every quote
inside the frozen 6..25-token / ≤160-character / one-text-node rule (`span_tools.py check`). The two
refused candidates are refused for duplication and for resting on pages the lane does not hold, not for
want of searching; the Yahoo re-grounding cannot pass the token-count rule at all (a whole Japanese
operator sentence is one whitespace token — `w1/ScoutRejectYahooUA.md`), so it is deferred to a round
that widens the rule rather than forced into this one.

## TREND INPUTS:

expansion: two entries on Google's own verification signals, each citing a `mined` row opened 2026-10-27
(S425: three identification signals, "your logs may show visits from several IP addresses", US egress and
the fallback when US requests are blocked; S426: reverse DNS to `googlebot.com` / `google.com` /
`googleusercontent.com`, forward lookup matching the logged address, and the published IP-range JSON
lists). The coverage map's frontier ground held `Crawler identity (Googlebot subtypes)` (README line 97,
S263) and `Crawler identity (Baidu: UA + two-step DNS; unblocking)` (line 108, S423 S424) only; no Google
IP, reverse-DNS or published-range ground existed (`w1/ScoutLaneCrawlerIdentity.md` §7; own: README lines
53/97/108 read at base `fd6303ce`, and the two round-59 entries do not exist in `corpus/knowledge/` yet —
the index rows are drafted, not landed, by `w1/ScribeGroundMap.md` E1/E2). quality: three mined mistakes
shown able to fail on the base revision before data — routed defect D1 carried seven rounds unrepaired
(`controls/base-c3-quote-truth.txt:2`, `0/9 met=False`), axis evidence pointing at `/tmp` files and a
removed tree while the scores stayed 10 (`controls/base-c1-axis-evidence.txt:2`, `mismatches=16
unresolved=11 … met=False`), and the resolver's seven disclosed routes (`controls/base-c2-resolver-cases.txt:2`,
`13/21 met=False`); the counters are version 1 and wave 1 attacks them before any claim is measured.
discernment: one staged entry re-grounded with eight of its sentences refused as absent from S425 (0 hits
for forge/spoof/anyone can/Baidu/Yahoo), plus the "no revision printed" clause contradicted by the page
footer (`Last updated 2026-06-12 UTC`) and two quote-form refusals (29 tokens/191 chars; a tail crossing
text nodes); two staged candidates refused with decision lines and flips (duplicate/subset; own-work
source with a tautological recheck). Rule-shape input for the next round: the 6-token floor makes any
Japanese operator sentence unquotable (one whitespace token), which is what kept the Yahoo DNS ground out
of this round. Adjacency: not re-opened this round — no `Conn*`/sibling-overlap report exists under
`.ufo/waves/round-59/w1/` (own, directory listing 2026-10-26 22:49); the round-58 record stands as
carried input (DNS half unowned; tabi owns the client-side half; kumitate keeps a prose receipt-change
file), not re-measured here. The non-author discernment spot-check remains a closure duty.

### Provenance (for the lesson scribe)

- Contract: `.ufo/waves/round-59/contract.md` (§ Claim C3, § Frontier step and assimilation).
- Retained bodies and receipts: `.ufo/waves/round-59/sources/{S425.html,S426.html,receipts.json}`.
- Scout measurements used: `w1/ScoutStagedS398.md`, `w1/ScoutRejectAmendment.md`,
  `w1/ScoutRejectYahooUA.md`, `w1/ScoutLaneCrawlerIdentity.md`; index draft: `w1/ScribeGroundMap.md`.
- Own observations: `span_tools.py spans S425|S426`; `grep -n "verify-google-requests" S425.html` (lines
  720, 1284); `grep -c "Learn how to use these details" S425.html` = 1; `grep -n "Crawler identity"`
  `corpus/README.md` (lines 53, 97, 108); `grep -n "S425\|S426" corpus/SOURCES.md` = no rows;
  `ls corpus/knowledge/` = no `crawler-identity-signals.md`, no `googlebot-verification.md`; the three
  base control receipts' `met=False` lines; `ls .ufo/waves/round-59/w1/` (no Conn*/sibling report).
- Not done by this seat: no live re-fetch, no counter run against the lane, no re-verification of the
  scouts' hit counts.

VERDICT: search log and trend inputs drafted on S425+S426 with both exclusions carried from the scout seats' decision lines and flips; nothing scored, no claim measured.
