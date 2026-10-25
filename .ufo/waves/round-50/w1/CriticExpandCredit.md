# CriticExpandCredit — does the crawl-error-status ground earn expansion credit?

Seat: critic, axis judged: calibration. Scoped question: test the expansion-credit
rule against this round's plan — read the coverage map in `corpus/README.md` and
the held entries it names, and decide whether the crawl-error-status ground (what
an error status does to crawling) is ground the lane did NOT already hold.

## Verdict

**EXPANSION CREDIT HOLDS — the ground is new.** With one bounded overlap
disclosed, not a denial: the adjacent "status → crawler action" consequence
already sits in `js-rendering-queue.md` (non-200 may skip the render pass) and
in `robots-txt-rules.md` (status classes on the robots fetch itself). Both stop
at different verbs; neither claims the scale-back consequence S286 carries.

## What the plan claims

LOG.md "Round 50" assimilation bullet: "Theme: the crawl-error status layer. One
entry, `corpus/knowledge/crawl-error-status-table.md`, grounded on S286 only."
The new entry declares its ground explicitly:
`corpus/knowledge/crawl-error-status-table.md:4` — "per-host crawl hygiene —
what an error status does to crawling, which robots directives and crawl-budget
levers do not state"; and line 10 admits exactly one sentence: "Googlebot will
scale back its crawling if it detects that your servers are having trouble"
(S286). PROVINCE.md Frontier opens "Crawl hygiene per host (robots.txt, sitemap
scope, canonical signals)" as the lane's frontier bucket.

## Coverage-map rows read

From `corpus/README.md` "Coverage map" (line numbers at current tip):

- Line 42, "Crawl scope per host (r20) → `knowledge/crawl-scope-per-host.md`" —
  the closest pre-existing row. Read the entry: its claim is about WHERE rules
  live (host-root robots, sitemap path scope). Its one status consequence is
  robots-fetch-specific: 4xx → MAY access, 5xx/unreachable → MUST assume
  complete disallow (S011 §2.3.1.3–2.3.1.4). That is what an error status does
  to the *robots fetch decision*, not what an error status does to *crawling
  the site's pages*. Different layer.
- Lines 370–373, round-37/38 rows → `scripts/robots_audit.py` and
  `knowledge/robots-txt-rules.md`. Read the entry: every status rule maps a
  *robots response* status to an allow/disallow decision (2xx parse, 400–499
  allow, 500–599 disallow, lane reading at line 23). S095's "Handling of errors
  and HTTP status codes" section was cited for Google's robots-status handling
  only (line 25). Nothing about error statuses on ordinary page fetches, and
  nothing about rate consequences.
- No coverage-map row names `crawl-budget-consequences.md` or
  `crawl-error-status-table.md` — both are too new for the map at tip. I read
  both entries directly.
- No row names `js-rendering-queue.md`; read it because S137 (opened
  2026-10-24, same round window) is the only held row with a status→consequence
  rule for ordinary pages: 200 → render queue, non-200 → rendering might be
  skipped. That is a render-queue rule, not a crawl-rate rule.

## Held entries checked

- `corpus/knowledge/crawl-scope-per-host.md` — robots/sitemap scoping only.
- `corpus/knowledge/robots-txt-rules.md` — robots-fetch status semantics only;
  Google-specific status handling recorded as "not substituted" (line 25).
- `corpus/knowledge/crawl-budget-consequences.md` — the round-49 sibling. S273:
  robots blocking does not reallocate spared budget unless the capacity limit
  is already hit. S274: the emergency backoff reduces crawl rate across the
  whole hostname — and the entry itself flags (line 13) that the checked quote
  "does not itself name the status codes that trigger that backoff." The S286
  sentence is the missing link: error statuses *are* a trigger for a
  scale-back, stated by the vendor. Complement, not duplicate.
- `corpus/knowledge/js-rendering-queue.md` — bounded overlap, disclosed above:
  status → render-queue admission, not status → crawl rate.
- `corpus/SOURCES.md` line 103 (S095 row) — confirms the held anchor set covers
  Google's robots-status interpretation only. The S286 row itself is not yet in
  the live registry (pre-append state; the mirror at
  `.ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md` carries it).

## The sharpest attack I can run, and why it fails

Attack: the lane already holds "error status → crawler action" twice (render
skip, robots disallow), so the new entry adds only a third instance of an
already-held class and the claim "which robots directives and crawl-budget
levers do not state" is an author-written strawman.

Why it fails: the expansion rule is about *ground* — the named consequence
relation — not about a syntactic class. Each held consequence binds a different
antecedent to a different consequent: (robots-fetch status → allow/disallow),
(page status → render-queue admission), (robots block → budget not shifted),
(throttle request → hostname-wide backoff). S286 binds a new pair: (server
error statuses → crawler-initiated crawl scale-back). No held entry asserts
that pair; the crawl-budget entry explicitly names the status-trigger gap in
its own S274 record. The strawman attack fails on the entries' own text, which
the new entry cites correctly.

## Calibration note for the verdict line

Round-49 non-author precedent (`corpus/lessons/round-49-verifier-spotcheck.md`)
recorded "expansion: improved" for exactly this shape: one new knowledge entry
on crawl-budget ground the coverage map did not hold, citing newly mined rows.
The S286 step is the same shape one layer over. Recommended expansion verdict:
**improved** — one new knowledge entry on the crawl-error-status layer, ground
the map did not hold, citing one row opened this round. Not "improved on two
entries": S273/S274 stay the round-49 rows whose classes this round only
measures.

## Instrument state (observed, not reasoned)

- C1 at base `9619af6`: `classed 0/3 met=False`, exit 1.
- C1 at pre-append `33eec7f`: `classed 0/3 met=False`, exit 1 (lesson absent,
  no live registry row — expected: the append commit is later).
- C2 at base `9619af6`: `durable 0/1 met=False`, exit 1.

The counters red at both frozen revisions as designed; expansion is judged on
ground, not on the counters having gone green yet.
