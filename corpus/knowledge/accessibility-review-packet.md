source: S035 — https://www.w3.org/TR/2024/REC-WCAG22-20241212/ (success criteria 1.1.1–4.1.3; conformance requirements §5.2)
verified-at: 2026-10-21 — pinned Recommendation source opened; documentation packet only, no website assessed
recheck: python3 -B scripts/accessibility_packet.py --root . --json; reopen S035 on a WCAG version change

# Publisher-side accessibility review packet

This packet turns the previously unheld WCAG 2.2 frontier into explicit
publisher review work. It does **not** measure a website's accessibility.
A structurally complete packet means every selected criterion has review
instructions and evidence requirements; it never means those requirements
were satisfied by a page.

## Scope and source

The fixed population is the Level A and AA success criteria in W3C's
12 December 2024 WCAG 2.2 Recommendation. The exact population and extracted
source sections are committed at `.ufo/waves/round-25/population.json`;
`.ufo/waves/round-25/source-wcag22.html` retains the opened official bytes.
The removed 4.1.1 Parsing criterion is not a WCAG 2.2 requirement. AAA
criteria are outside this packet, not waived by a Level AA claim.
The population's `normativeText` excludes headings, Understanding/How to Meet
links, conformance labels and note wrappers: quotations must come from the
criterion body, not a convenient heading.

`accessibility-review-cards.json` contains one card per selected criterion:
identifier, exact title and level, pinned source URL, a short located quote,
a publisher check, evidence needed, a realistic failure example, and a
limitation. Each card's status is `not-assessed`. The tool cannot turn that
status into a WCAG result.

The tool pins both the population bytes and the retained official source
bytes. A source change is could-not-evaluate, not a newly trusted standard.
Quotes contain 6–25 whitespace-delimited words, are case-sensitive and start
and end at word boundaries. Quote matching collapses whitespace and removes
extractor-added whitespace before punctuation and after opening parentheses
on both sides. This normalizes extraction spacing, not the standard's words.
These are local packet-grounding rules, not additional WCAG requirements.

## Executable preparation

From this repository:

```sh
python3 -B scripts/accessibility_packet.py --root . --json
python3 -B scripts/accessibility_packet.py --selftest
python3 -B .ufo/waves/round-25/packet_selftest.py --root .
python3 -B .ufo/waves/round-25/frozen_replay.py
```

The first command validates the packet's structure and source bindings.
Its JSON distinguishes packet readiness from `websiteConformance`:
`not-assessed`. Exit 0 means only structurally clean; 1 means a packet
requirement failed; 2 means input could not be evaluated; 64 means usage.
The selftests use temporary fixtures, not a domain checkout or website.

A reviewer preparing an actual publisher work item should:

1. Name the page URLs, source revision/build, page variants, complete user
   processes and intended WCAG version/level. Do not infer a served build
   from a checkout, canonical signal or an old HTTP receipt.
2. Run the packet inventory and read the relevant card **and** its normative
   source, including exceptions and definitions. The card is a work aid,
   never a replacement for the standard or a conformance methodology.
3. Assign each card's evidence requirement to a qualified reviewer. Source
   inspection can prepare checks; rendering, keyboard interaction,
   assistive-technology observations and human judgments require separate
   authorized evaluation. Browser execution belongs with the browser owner.
4. Keep the packet `not-assessed`. Record actual evaluation evidence in a
   separate work item naming the tested build, dates, page/process scope,
   methods and limitations. A missing relevant component needs a documented
   applicability judgment, not a silently skipped criterion.
5. Hand source fixes and an evaluation request to the property operator.
   Deployment, external account operations and publishing remain gated.
   This round performs none of them.

## Decision table

| Observation | Defensible conclusion | Not established |
|---|---|---|
| Inventory is clean | Every fixed criterion has a correctly bound review card | Any criterion passes on a website |
| Source quote and title match | The card refers to the pinned criterion | Its prose fully interprets every definition/exception |
| Page source contains an alt attribute | Source evidence exists for further text-alternative review | The alternative serves the equivalent purpose |
| Automated scan reports no findings | That scanner found no issue within its scope | WCAG conformance or a complete manual evaluation |
| One page/state has evidence | Evidence applies to that named page/state/build | Other pages, responsive states or an entire process conform |

## Conformance boundaries

S035 §5.2.1 requires all A and AA criteria for Level AA (or a qualifying
conforming alternate version). Section 5.2.2 says: “Conformance (and
conformance level) is for full web page(s) only”. Section 5.2.3 requires
complete processes; §5.2.4 concerns accessibility-supported ways of using
technologies; §5.2.5 requires non-interference, including content not relied
upon for conformance. These requirements are not satisfied by inventory
coverage. No live property, source tree, browser state, accessibility tree,
user account or publication action was evaluated by creating this packet.

## Error patterns

- Treating the read tool's abstract-only WCAG response as the normative
  standard: reopen the pinned official URL in raw mode and locate the
  criterion. Round 25 retained the full source because the initial reader
  result omitted all success criteria.
- Counting repeated headings or AAA criteria as A/AA coverage: bind the exact
  id/title/level/source set and reject duplicate or missing criterion IDs.
- Substituting a heading or one-character substring for a grounding quote:
  require a 6–25-word case-sensitive word-boundary quote from normativeText,
  with the same documented spacing normalization on quote and source.
- Calling a complete checklist an accessibility audit: keep every card
  `not-assessed`; packet validation is preparation only.

Evidence of capability execution and fixed-population before/after
measurements is recorded in `corpus/lessons/round-25.md` and the fleet report.
Prior round-24 reconciliation/replay claims remain separate unadmitted debt;
this packet neither repeats their interrupted probes nor resolves their
policy-stop disposition.
