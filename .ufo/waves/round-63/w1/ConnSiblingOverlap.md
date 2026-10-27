# ConnSiblingOverlap

Sibling-overlap scan for round 63's three surfaces: quote-class machinery (C2,
`scripts/quote_class.py` + `.ufo/waves/round-63/quote-class/quote-classes.json`,
vocabulary `raw-substring` / `collapsed-only` / `absent`), calibration-counter
repair (C1, `.ufo/waves/round-63/c63_calibration.py` over kake's own SCORECARD
sub-axis), and the S432 / fetch-spec ground (`corpus/SOURCES.md:178`, WHATWG
Fetch §3.6 `X-Content-Type-Options`). Evidence is file:line, read-only, at
sibling heads as inspected 2026-10-27; no tool installs performed.

## OVERLAPS:

### 1. Quote-class machinery — no sibling holds the vocabulary or the class
- `grep -nE 'quote[-_ ]?class|collapsed-only|raw-substring'` over every
  `*/SKILL.md` and `*/PROVINCE.md` (gitignore off) hits only
  `kake-shokunin/SKILL.md:1348` — the round-50 `quote-class-counter` gate row
  (`classed == 3 of 3`, ledger `.ufo/waves/round-50/quote-classes.json`). No
  sibling SKILL/PROVINCE contains any of the three tokens.
- `find` over sibling `tools/` and `scripts/` for `*quote*` returns two
  self-scoped tools, neither a class deriver:
  - `chousa-shokunin/tools/quote-reopen.py` — live GET re-open of a located
    quote against the *live* page named in chousa's own registry, verdicts
    `VERBATIM`/`ABSENT`/`TOO_LONG`/`NO_SOURCE`/`UNREACHABLE` (header
    `:1-30`; registered `chousa/SKILL.md:88`). Presence check against live
    bytes, not a raw-vs-collapsed class against retained blobs; chousa-only
    registry inputs.
  - `kotodama-shokunin/tools/check-gate-quotes.py` — 25-word quotation cap on
    kotodama's own `## Gate` lesson rows (`:1-30`). Length lint, unrelated.
- The `collapsed-only` class semantics this round re-derives are kake's own
  round-50 rule (`kake/SKILL.md:1348`; MANIFEST capability row
  `"Quote-class ledger for cited source spans"`, fleet `MANIFEST.json` round-50
  kake entry). First use was kake round 50; no sibling adopted or duplicated it.

### 2. Calibration-counter repair — fleet axis name, lane-local counters
- `AXES.md:15` defines `calibration` fleet-wide ("Self-assessment quality:
  gaps named honestly"); every lane scores its own row. Siblings carrying a
  calibration axis per `shokunin.conf`: kaidoku `:45`, kengaku `:47`, kagi
  `:51`, kama `:52`, lore `:53`, revenger `:54`, tameshi `:55`, tabi `:58`,
  souji `:76`, audio/game-dev-2d/game-dev-3d `:81-83`.
- Sibling calibration *counters* are all lane-scoped instruments over their own
  claims files: `kaidoku-shokunin/tools/round-{25,26,32,35}/*calibration*.py`
  (capability/statement calibration vs kaidoku claims-v*.json),
  `kama-shokunin/tools/round40-calibration-audit.py` (kama digest-citation
  corrections), `mori-shokunin/tools/mori-round41-calibration.py`. None names
  kake's counter family, `c62_calibration.py`, the `resolved` components, or
  kake's SCORECARD row.
- Nearest method claim, not machinery: `tameshi` owns the verification-fixture
  *method* — a sibling's gate is probed read-only and never edited
  (`kengaku-shokunin/PROVINCE.md:340-343` restating `tameshi/PROVINCE.md:14-18`);
  `souji` censuses artifacts fleet-wide but "contested artifact ownership is
  reported to the integrator, never silently absorbed"
  (`souji/SKILL.md:2`). Neither claims authority over kake's counter semantics.
- The one open authority question is lane↔operator, not sibling↔sibling:
  `.ufo/l0-questions.md:181` (kake round-59) asks whether `calibration` stays a
  scored kake sub-axis while MISSION names kake "operability + freshness"
  (`shokunin.conf:48`, `MISSION.md:25`). Still unanswered; round-62 carried it
  (`kake-shokunin/LOG.md:2255`). This scan does not rule on it.

### 3. S432 / fetch-spec ground — one same-document adjacency, one id-string collision
- `grep -c 'fetch\.spec\.whatwg\.org'` over every `*/corpus/SOURCES.md`: two
  lanes cite the WHATWG Fetch living standard —
  - `kake-shokunin/corpus/SOURCES.md:178` = S432, §3.6 `X-Content-Type-Options`
    header, proposition: the field's one defined value is `nosniff`;
  - `mori-shokunin/corpus/SOURCES.md:231` = S225, §4.5 HTTP-redirect fetch,
    proposition: twenty-hop redirect-chain limit, feeding mori's
    `source-drift-hardening` knowledge (mori is "detection and report only",
    `shokunin.conf:63`).
  Same document, disjoint sections and propositions; registries are lane-local.
- `grep 'nosniff\|X-Content-Type-Options'` over every `*/corpus/SOURCES.md`:
  kake is the only lane with a row for the header. No sibling SKILL/PROVINCE
  mentions `nosniff`, `X-Content-Type-Options` or `fetch.spec.whatwg.org`.
- `kotodama-shokunin/corpus/SOURCES.md:461` carries a lane-local id `S432`
  (Walters Art Museum tsuba records) — an S-id *string* collision only; S-ids
  are lane-local (round-58 finding: each lane owns its registry/ID semantics —
  kama TSV, tabi E02–E04 rules, `w1/ConnSiblingOverlap.md` §2). Any cross-lane
  citation of this round's row must be qualified `kake/S432`.
- kake already declared this ground: `kake/PROVINCE.md:32-36` owns
  `corpus/knowledge/response-header-expectations.md` (S430–S433) plus
  `response_snapshot.py`/`header_audit.py`; `corpus/QUALITY.md`'s
  raw-substring/substantive-support criteria are kake's own gate corpus.

### 4. Declared boundaries covering the nearest neighbors
- tabi: `kake/PROVINCE.md:40-41` splits browser execution (tabi) from
  publisher-side placement (kake); `tabi/SKILL.md:2921` records live
  header/redirect observation is tabi's on driven pages, static declaration
  audit kake's. Round-63 work is offline committed-bytes audit — kake's side.
- chousa: `kake/PROVINCE.md:42-43` — chousa owns research method and source
  hierarchy; kake keeps domain findings and its own registry rows.
  `quote_class.py` is an in-lane self-measure, not a method claim.
- The only kake-tagged contested row anywhere is the the-musketeer Chrome
  profile lease, kagi/tabi/kake, with the integrator (`kake/PROVINCE.md:45-46`;
  `kagi/PROVINCE.md:43`) — unrelated to this round's surfaces.

## CONTESTED:

1. **None on machinery or counter repair.** No sibling claims the
   `collapsed-only`/`raw-substring` vocabulary, a quote-class deriver, the c62
   counter family, or repair authority over kake's gates.
2. **Advisory adjacency — WHATWG Fetch, mori S225.** Two lanes hold rows on
   the same living standard. If a future round treats "the Fetch spec" as one
   source (dedupe, shared mirror), mori's §4.5 proposition is not kake's §3.6
   row and must not be counted as a duplicate or as coverage of S432.
3. **Advisory adjacency — quote-verification method, chousa.** chousa's
   quote-reopen is a live-fetch presence verdict; kake's quote_class is an
   offline class deriver over retained blobs. Disjoint verdict spaces; keep it
   that way — do not frame `quote_class.py` as implementing chousa's
   claim-vs-source method, and do not cite chousa verdicts as class evidence.
4. **Carried, unresolved — L0 `calibration` sub-axis authority**
   (`.ufo/l0-questions.md:181`): whether kake may score calibration at all is
   operator-owned. C1 repairs a counter on an already-scored sub-axis; the
   repair does not presume the ruling either way.

## RECOMMENDATION:

- **Report, not absorb:** C1/C2 surfaces are in-lane ground. Constraints to
  keep while the round scores:
  1. Qualify the S432 cite as `kake/S432` in any cross-lane artifact
     (kotodama holds a same-numbered unrelated row).
  2. Keep mori's S225 fetch-spec row distinct; never count it as coverage of,
     or a duplicate of, S432.
  3. Keep `quote_class.py` verdicts (`raw-substring`/`collapsed-only`/`absent`)
     separate from chousa's (`VERBATIM`/`ABSENT`/`UNREACHABLE`) — different
     questions, different inputs.
  4. Leave the L0 calibration-ownership ruling where it is: operator channel.
- No sibling lane needs a handoff; no sibling file was touched. No tools
  installed; scratch: none beyond this report.

VERDICT: kake uniquely owns this round's ground — quote-class machinery and
the calibration counter family are kake-only across all sibling SKILL/PROVINCE
files, and the S432/nosniff proposition is kake-only across all sibling
registries; one same-document fetch-spec adjacency (mori S225 §4.5), one
lane-local S-id collision (kotodama S432), and one operator-owned
axis-authority question (L0 :181) are reported, not absorbed.
