# Round 51 w1 — ReviewEntryScope (province applied to the two admitted entries)

Seat: reviewer (freshness). Read-only; the only file written is this one.
Measured revision: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (lane tip at dispatch).
Base: `007d66e4e8360a5f88d29a93eeedd8066dad4434`.

**Axes named.** The round owns operability (C1, wave-evidence ledger) and freshness (C2, the two
assimilated entries). This seat is on freshness only: it asks whether the new held ground is
*kake's* ground and whether the province map that governs future ground claims reflects it.

## What I read

- `PROVINCE.md` at the tip (350 lines) and `git diff --stat 007d66e..9d13768 -- PROVINCE.md`
  (empty).
- `corpus/knowledge/canonical-selection.md` (77 lines) and `corpus/knowledge/crawler-identity.md`
  (54 lines) as committed at the tip.
- The held neighbours each entry leans on: `corpus/knowledge/static-canonical-preflight.md`,
  `corpus/knowledge/js-rendering-queue.md`, `corpus/knowledge/crawl-scope-per-host.md`,
  `corpus/knowledge/dynamic-rendering-workaround-limits.md`,
  `corpus/knowledge/crawl-error-status-table.md`, `corpus/lessons/round-51.md`.
- Sibling provinces: `tabi-shokunin/PROVINCE.md`, `chousa-shokunin/PROVINCE.md`,
  `kagi-shokunin/PROVINCE.md` (grep over all fleet `*/PROVINCE.md` for
  `robots|search engine|indexing|sitemap`: only `kake-shokunin/PROVINCE.md` matches — no sibling
  claims this ground at the province level).
- `grep -n PROVINCE .ufo/waves/round-51/c51_quote_truth.py .ufo/waves/round-51/c51_wave_ledger.py`
  → no match in either counter.

## Entry A — `corpus/knowledge/canonical-selection.md`

**Verdict: kake Frontier, held ground. Not Core. Not tabi, chousa or kagi.**

**Deciding line** — `PROVINCE.md:22-23`:

> Crawl hygiene per host (robots.txt, sitemap scope, canonical signals) — first entry
> `corpus/knowledge/crawl-scope-per-host.md`; canonical/JS rendering open.

and its round-22 gloss at `PROVINCE.md:60-61`: "The broader crawl and JS-rendered-canonical
frontier above remains open; browser execution stays tabi's adjacent province."

Why the other compartments do not take it:

- **Not Core** — Core is `PROVINCE.md:12-13` ("audits, drift checks and source-fix guidance for
  the lane's web properties") plus `14-16` (Pages/ETag serving semantics) plus `17` (the lane's
  gates). The entry audits no owned property, adds no gate, and says so itself
  (`canonical-selection.md:73-76`: "no owned property was fetched, and no engine's selection was
  observed"). Core promotion is barred by `PROVINCE.md:29-30` because no gate exists.
- **Not tabi** — `PROVINCE.md:34-35`: "`tabi` drives browsers and owns client-side crawler
  discipline", with browser execution repeated as tabi's at `PROVINCE.md:60-61`. This entry ran no
  browser and is a reading of one retained vendor page.
- **Not chousa** — `PROVINCE.md:36-37`: "`chousa` owns research method and source hierarchy; kake
  keeps only domain findings and its own `corpus/SOURCES.md` rows." The entry *is* the domain
  finding, and its row is S262 (`corpus/SOURCES.md:152`, `used-by`
  `corpus/knowledge/canonical-selection.md`). The one-GET/retained-body/quote-class method is
  chousa's craft, but the method is not what the entry records.
- **Not kagi** — `PROVINCE.md:38-39`: no secret or credential value appears in the entry.

**Is it a real frontier step?** Yes, and not covered ground. Two held entries named this exact
hole and refused to fill it: `static-canonical-preflight.md:7-9` ("this entry owns publisher-side
static-file validation, not browser crawling or search-engine canonical selection") and
`js-rendering-queue.md:71-77` ("It does not say which canonical Google selects among duplicates —
a declared canonical is a hint and the selection is the engine's decision, which the lane's own
static preflight … deliberately does not claim"). Round 51 converts that named disclaimer into
held ground for one engine. That is the opposite of the refused `crux-eligibility-route.md`
pattern in `corpus/lessons/round-51.md` ("covered ground … would not move the coverage map").

**Limits on what the verdict licenses.** The Frontier bullet enumerates *publisher-emitted*
canonical signals; this entry holds an *engine-side selection procedure*. It may be cited as
held ground for "a declared canonical is a hint and selection is the engine's" only. It does not
close the "JS-rendered canonical" half of `PROVINCE.md:23` (nothing in it addresses a canonical
injected at render time), it is not a gate, and it is not an observation about any lane property.

## Entry B — `corpus/knowledge/crawler-identity.md`

**Verdict: kake Frontier, held ground. Not Core. Not tabi, chousa or kagi.**

**Deciding line** — `PROVINCE.md:22` (head of the Frontier bullet), "Crawl hygiene per host
(robots.txt, sitemap scope, canonical signals)". The entry's load-bearing rule lands on the
enumerated `robots.txt` sub-item, not on a bare extension of the head:
`crawler-identity.md:26` — "both crawler types obey the same product token (user agent token) in
robots.txt" — which is a robots-token fact the lane's held robots ground does not answer
(`crawl-scope-per-host.md` covers discovery/scope; S095/S096 cover rule evaluation).

Why the other compartments do not take it:

- **Not tabi** — `PROVINCE.md:34-35` gives tabi *client-side* crawler discipline and kake
  "publisher-side placement (robots/sitemap at the host it serves)". The entry recognises an
  *inbound* crawler at the publisher's host (HTTP request header, server log) and performs no
  browser action and no user-agent-spoofed fetch; it fetches nothing at all
  (`crawler-identity.md:51-52`).
- **Not Core** — `PROVINCE.md:12-16` is owned-property auditing and Pages serving semantics; this
  is a vendor identity fact with no gate, so `PROVINCE.md:29-30` keeps it in Frontier.
- **Not chousa** — one finding, one row (S263, `corpus/SOURCES.md:153`, `used-by`
  `corpus/knowledge/crawler-identity.md`), per `PROVINCE.md:36-37`.
- **Not kagi** — `PROVINCE.md:38-39`; no secret material.

**Residual tension in the entry's own framing.** `crawler-identity.md:4` widens its ground to
"per-host crawl hygiene — knowing which crawler is on the wire before interpreting a crawl
log". "Crawl-log interpretation" is not one of the three enumerated sub-items, and the lane holds
no log and no artifact for it. Round-49 precedent shows how such a widening is admitted: a new
sub-item (crawl-budget consequences) entered through an appended section,
`PROVINCE.md:340` "## Round-49 crawl-budget frontier step". Round 51 has no such section (see
below), so the widening is in-province but unwitnessed by the province document.

## Frontier-step verdict (round level)

**Core-move discipline: respected.** `PROVINCE.md` is byte-identical from base to tip
(`git diff --stat 007d66e..9d13768 -- PROVINCE.md` prints nothing). No Core line was added, no
older line was rewritten, and no Core promotion was claimed — correct, because
`PROVINCE.md:29-30` requires "source-backed entries *and* a gate", and neither entry has a gate.

**The step is unrecorded — that is the actionable defect.** The province document's last dated
section is Round-49 (`PROVINCE.md:340`). There is no Round-48 section for the round-48
`js-rendering-queue.md`, and no Round-51 section for either entry. Consequence: `PROVINCE.md:22-23`
still reads "canonical/JS rendering open" and names neither of the two entries now held under it,
so the province map under-reports held ground by two rounds. A future planner reading PROVINCE
alone can re-buy ground the corpus already holds — precisely the failure mode used to refuse
`crux-eligibility-route.md` in `corpus/lessons/round-51.md`. C2 cannot catch this: neither
`c51_quote_truth.py` nor `c51_wave_ledger.py` references PROVINCE at all (grep: no match), so C2
can measure 8/8 beside a stale province map.

## Findings

- **F1 (medium, freshness) — province step unrecorded.** `PROVINCE.md` unchanged base→tip; no
  Round-51 section; `PROVINCE.md:23` still asserts "canonical/JS rendering open" without naming
  `canonical-selection.md` (S262) or `crawler-identity.md` (S263). Recommended text: a Round-51
  section naming both entries, their deciding lines (22-23 for the canonical entry; 22 plus the
  robots.txt sub-item for the crawler entry), "held Frontier, no gate, no Core line", and a
  correction of the "canonical/JS rendering open" clause for the canonical-selection half only
  (JS-rendered canonical and crawler-log interpretation remain open). Appending is the
  integrator's action; this seat is read-only.
- **F2 (low) — ground headers do not name the province line.** `canonical-selection.md:4` and
  `crawler-identity.md:4` describe their ground in prose, unlike the held precedent
  `js-rendering-queue.md:4` ("PROVINCE.md, Frontier: …"). Ground→province traceability is one hop
  weaker for exactly the entries whose province is contested by this seat's question.
- **F3 (low) — held entries still speak of one "Googlebot".** `js-rendering-queue.md:31-35`,
  `dynamic-rendering-workaround-limits.md:30` and `crawl-error-status-table.md:10` quote or
  paraphrase "Googlebot" as a single agent; `crawler-identity.md:21-26` now holds that the name
  covers Smartphone and Desktop and that the user-agent header is the discriminator. The quoted
  vendor sentences remain true, so no claim is falsified, but any *conclusion* those entries draw
  from a bare "Googlebot" is subtype-ambiguous under the new ground. No cross-reference is
  committed.
- **F4 (informational, scope guard)** — `crawler-identity.md:35` ("For a publisher running
  per-device checks") gestures at a check the entry does not run. If a later round implements it
  by fetching with a crawler user-agent, that fetch is tabi's province under `PROVINCE.md:34-35`;
  this entry stays kake's because it fetches nothing.

## Residual risk and verification gaps

- No gate exists for either entry. Both stay Frontier — correct today, but any later Core citation
  needs the gate `PROVINCE.md:29-30` demands.
- F3's list is grep-scoped (`googlebot` over `corpus/**/*.md`), not a prose review of every held
  entry. A held entry that names the crawler indirectly would not appear in that list.
- No owned property was probed, and none of these verdicts rests on one; both entries state the
  same (`canonical-selection.md:73-76`, `crawler-identity.md:51-54`).
- The worktree carries a modified `SCORECARD.md` and untracked wave files that are not this seat's;
  every verdict above is read from committed bytes at `9d13768`.
- Tooling: nothing installed or upgraded; no pacman transaction attempted.
