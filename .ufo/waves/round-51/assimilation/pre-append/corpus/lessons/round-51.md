# Round 51 — kake

Lane: `kake-shokunin`. Author: Kimi fresh L1 (this session). Round shape: one v1 wave of
48 seats under `scripts/hyaku/ufo-wave-policy.json` (band 32-64).

## Gate

- S262 — https://developers.google.com/search/docs/crawling-indexing/canonicalization — accessed 2026-10-24 — § "What is URL canonicalization" (doc rev. Last updated 2026-08-20 UTC) — quote: "indicating a canonical preference is a hint, not a rule" (10 words; raw substring of the retained body, sha256 792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b, 174926 bytes, HTTP 200)
- S263 — https://developers.google.com/search/docs/crawling-indexing/googlebot — accessed 2026-10-24 — § "Googlebot is the generic name for two types of web crawlers used by Google Search" (doc rev. Last updated 2026-02-03 UTC) — quote: "Googlebot is the generic name for two types of" (9 words; raw substring of the retained body, sha256 6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de, 175561 bytes, HTTP 200)

Both rows are re-grounded in this round: the L1 fetched each URL once (2026-10-24,
23:16 -03:00), kept the response body under `.ufo/waves/round-51/sources/`, and pinned its
sha256 in `.ufo/waves/round-51/sources/receipts.json`. Every quote in the two admitted
entries is an exact substring of the retained body after whitespace collapse; the two
quotes above are raw substrings, and each entry marks the class of every other quote it
carries.

## Admitted entries

- `corpus/knowledge/canonical-selection.md` — grounded on S262 alone. Google's canonical
  **selection** mechanism: what a declared canonical is worth, which signals are weighed,
  and which variant classes create duplicates. This is the half the lane's held
  `corpus/knowledge/static-canonical-preflight.md` explicitly disclaims.
- `corpus/knowledge/crawler-identity.md` — grounded on S263 alone. "Googlebot" names two
  crawlers (Smartphone and Desktop); the subtype is identified from the HTTP user-agent
  request header, and both obey the same robots product token.

Both entries are new files: the coverage map in `corpus/README.md` did not hold this
ground. The lane's held canonical ground stopped at the declared value, and its held
crawl ground stopped at robots semantics and crawl-budget consequences.

## Refused entries (reason and flip)

- `corpus/knowledge/engine-crawl-contracts.md` (staged, round 1; staged ids S250, S253,
  S254) — **refused**. Reason: the entry's Google half cites
  `https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics`,
  a URL the lane already mines as S137 in the same scope, so a second row for that URL is a
  within-scope duplicate (census E04); and its two Baidu sources were not opened by this
  lane in this round, so their quotes are un-re-grounded here. Flip: adopt in a later round
  that opens both Baidu pages itself and cites the lane's own S137 for the Google half
  instead of a second row for the same URL.
- `corpus/knowledge/crux-eligibility-route.md` (staged, round 2) — **refused**. Reason:
  covered ground. The lane already holds CrUX eligibility in
  `corpus/knowledge/field-performance-cwv.md` (S038 CrUX methodology, S039 CrUX API), so
  admitting this entry would not move the coverage map; expansion credit is knowledge on
  ground the lane does not hold. Flip: admit only if the held field-performance entry is
  superseded in place, never as a second row for the same ground.

## Stripped staged prose

The staged rows carried a `recheck` cell holding a shell command and its result
(`180d — curl -fsSL '…' | grep -c 'a hint, not a rule' -> 1 (ran 2026-10-23)`). That prose
is stripped: the admitted rows carry the normalized `180d` cadence, and the commands are
recorded here instead, with their run date, so the row still parses as eleven cells and
no cell carries a literal or escaped pipe.

- S262 staged recheck command: `curl -fsSL 'https://developers.google.com/search/docs/crawling-indexing/canonicalization' | grep -c 'a hint, not a rule'` — run 2026-10-23 by the package; re-run this round against the retained body, where the phrase occurs.
- S263 staged recheck command: `curl -fsSL 'https://developers.google.com/search/docs/crawling-indexing/googlebot' | grep -c 'generic name for two types of'` — run 2026-10-23 by the package; re-run this round against the retained body, where the phrase occurs.

## Id collision check

Run in scratch before any append, with the census parser's own 0-to-3-leading-space
pattern (a column-zero-only pattern misses an indented collision). The staged ids that
overlap the lane registry are S273, S274 and S286 — none of them is adopted this round.
The adopted ids S262 and S263 are unused in the lane registry, so no citation had to be
re-pointed; the guard was proven able to fail on an indented fixture before the check was
trusted. Evidence: `.ufo/waves/round-51/assimilation/`.

## Quarantine

The lane's slice of the campaign's absent-defect register was re-derived read-only and
left unadopted: no quarantined id was hand-checked this round, so the round-48 hand-check
is not used as an adoption basis. Evidence:
`.ufo/waves/round-51/assimilation/quarantine-slice`.

## Mistakes

- **class:** staged quote mis-transcribed as a source quote. **evidence:** the staged
  `canonical-selection.md` quotes "Google chooses the most complete and useful page as the
  canonical URL", which is not in the source; the page says Google chooses the page that is
  "objectively the most complete and useful for search users". The staged
  `crawler-identity.md` quotes "Googlebot Smartphone: a mobile crawler that simulates a
  user on a mobile device", which is not a substring either; the page renders
  "Googlebot Smartphone : a mobile crawler …" with a space before the colon. Both were
  confirmed absent from the bodies this round fetched. **captured-by:** none — the round-50
  quote-class instrument derived a class for quotes the lane already held, but nothing
  re-grounded a *staged* quote before it was copied. **fix:** every admitted entry is
  re-grounded against bytes this lane fetched this round, and the C2 counter's condition
  C5 requires each Gate quote to be a raw substring of the retained body.
- **class:** a wave's seat-report count stated in prose and not re-derivable. **evidence:**
  `corpus/lessons/round-50-verifier-spotcheck.md` routed defect 1 — the round-50 report
  claimed 26 seat reports while the committed tree holds 25. **captured-by:** none —
  `c50_durable.py` proved the grant and the citation order but never counted the
  reports. **fix:** `c51_wave_ledger.py` condition L1 compares the committed report-file
  count, the settlement's `reports_written` and the payload's seat count, and fails when
  they disagree.
- **class:** a route substitution recorded in prose only. **evidence:**
  `corpus/lessons/round-50-verifier-spotcheck.md` routed defect 2 — the HTTP status codes
  behind the fallback existed only in the report. **captured-by:** none — the round-50 route
  map recorded the fallback but no receipt. **fix:** `c51_wave_ledger.py` condition L2
  requires a committed probe receipt per route with an integer HTTP status and a body
  excerpt, and refuses a failing alias used by a role.
- **class:** no aggregate round-overrun figure derivable from committed bytes. **evidence:**
  `corpus/lessons/round-50-verifier-spotcheck.md` routed defect 3 — the overrun was named
  nowhere a reader could re-derive. **captured-by:** none — the round-50 settlement receipt
  carried per-seat seconds but no aggregate and no wall clock. **fix:** the round-51
  settlement carries the wave's start and end stamps, `.ufo/waves/round-51/round-time-accounting.json`
  carries the three figures, and `c51_wave_ledger.py` condition L3 re-derives them from the
  committed bytes and requires the lane's LOG.md to name the wall-clock figure.
- **class:** inherited artifacts swept to make a count look clean. **evidence:**
  `corpus/lessons/round-50-verifier-spotcheck.md` routed defect 4 — the eight
  `.ufo/waves/round-46/residual/` reports and the nine `>1MiB` copies under
  `.ufo/waves/round-48/assimilation/validate/`. **captured-by:** the round-50 QUALITY
  criterion "Operator-owned and inherited artifacts are not swept to zero a count".
  **fix:** they stay uncommitted and untouched this round; the count is reported as it
  stands.
