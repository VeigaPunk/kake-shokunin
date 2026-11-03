# ConnOverlap — kake round 70, W1 connector (read-only)

Base ``e5f6fd9e4c243d092160bc74e8bea24256087173``; contract commit ``908b20b0``; lane HEAD at measurement ``d76ae926``. Every command, output and exit code:
``.ufo/waves/round-70/w1/ConnOverlap/receipts.txt``. No lane tracked file modified (the 17:10–17:12 edits are the L1's). No tool installed; pacman untouched. Scratch removed on exit.

## (a) Overlap — each claim verifiable without the other landed

C1 (``SCORECARD.md`` appended section, ``.ufo/waves/round-70/c70_pointer_audit.py``, ``corpus/QUALITY.md`` end-of-file, ``corpus/lessons/round-70.md``, ``LOG.md``) → ``python3 -B
.ufo/waves/round-70/c70_pointer_audit.py --root <lane> --revision <rev> [--base <rev>]``. C2 (``corpus/knowledge/crus-bigquery-origin-membership.md``, ``corpus/SOURCES.md`` one row,
``corpus/lessons/round-70.md`` Gate, ``LOG.md``, ``SCORECARD.md`` round section) → ``bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake``.
Proofs: deleting ``corpus/`` entirely leaves the counter's summary byte-identical (``pointers=348 dangling=17 annotated=0 unannotated=17 met=false``); the census script has **0** occurrences of
``SCORECARD|QUALITY|lessons`` — it reads only ``corpus/SOURCES.md`` plus ``test -e`` on used-by paths. The counters do not read each other's files.

**But the claims are coupled through SCORECARD.md, and the L1's current table is host-dependent.**

1. **C1's population is the whole SCORECARD.md, so C2's paths enter C1's measurement.** The L1's round section names ``.ufo/waves/round-70/c70_pointer_audit.py``,
committed together → ``unannotated=0 met=true`` exit 0; absent at the measured revision each becomes an unannotated dangler → exit 1. *Move: commit C2's entry, the retained body and the counter in the same commit as the round section* — **adopted by the L1 in ``50ec1446``**, which carries all four (plus the retained ``S438-crux-bigquery.html``) in one commit.
met=true`` exit 0; absent at the measured revision each becomes an unannotated dangler → exit 1. *Move: commit C2's entry, the retained body and the counter in the same commit as the round section.

2. **The L1's table is calibrated to *this* host.** Base dangling = 17 here only because ``/tmp/kake-r16`` resolves (a W1 seat's own ``freshness-sweep --selftest`` fixture, dir created 2026-11-03 18:50Z); the table has **no ``/tmp/kake-r16`` row**.
Against the L1's real integration commit ``50ec1446`` the tip prints ``pointers=351 dangling=17 annotated=17 unannotated=0 met=true`` exit 0 **on this host only**; clone that commit with the token renamed to an absent path (same bytes otherwise) → ``pointers=351 dangling=18 annotated=17 unannotated=1 met=false`` **exit 1** (``tmp unannotated line=91``).
``controls/c1-base-v2.txt`` (``dangling=17``) is host-dependent for the same reason. *Move: add one ``/tmp/kake-r16`` row (17→18).* Verified: same clone with that row → ``unannotated=0 met=true`` exit 0.
3. **A row can launder a
live-but-uncommitted artifact.** A row whose first cell is the exact token of a path absent from the revision annotates it away: fixture → ``annotated=1 unannotated=0 append_only=true met=true`` exit 0 for
a file in no revision; ``append_only=true`` does not detect it. Same channel: a row whose prose cites an absent lesson (``corpus/lessons/round-11.md``) *manufactures* a pointer (``pointers=2 dangling=2
annotated=1 unannotated=1`` exit 1) unless that token is also annotated. *Move: no row's prose names a repo-relative path, and no row names a path expected to exist at the tip.*

Independently confirmed (already in the L1's Amendment 1): the contract's "staged id S352 collides with the lane registry's S352" is **false** — the lane registry holds no S352 (0 hits, 175 rows, max
S437); the 8 real collisions are S312 S329 S367 S372 S373 S374 S390 S409. The adopted id stays **S438** by the next-unused rule. E03 duplicate-id is intra-lane only (two lanes each holding S900 → both
``ok``, 0 E03); S438 already names different sources in kotodama (Colorado Dept of Agriculture) and revenger (OWASP MASTG).

## (b) Sibling scan — no sibling owns CrUX or field-performance ground

Grep of all 19 sibling ``PROVINCE.md`` for ``crux|core web vital|\bCWV\b|field.?data|real.?user|\bRUM\b|lighthouse|bigquery|web.?vitals|page.?speed|user experience`` → **0 in every sibling**; grep of every
sibling ``corpus/knowledge/`` for ``developer.chrome.com/docs/crux|CrUX (eligibility|API|methodology)|Chrome UX Report`` → no hits. kake's own claim: ``kake-shokunin/PROVINCE.md:24`` "Field performance
(Core Web Vitals, CrUX eligibility) — first entry". Adjacency lines checked — all give *web properties* to kake, none claim field performance: ``kengaku/PROVINCE.md:34``, ``kasegi/PROVINCE.md:49``,
``tabi/PROVINCE.md:16``, ``kama/PROVINCE.md:43``, ``kotodama/PROVINCE.md:20``, ``kotoba/PROVINCE.md:65``, ``kagi/PROVINCE.md:64``. ``tabi/PROVINCE.md:33,39-42`` name Chrome only as a browser/CDP surface;
``kagi/PROVINCE.md:64`` is the the-musketeer profile lease (contested kagi/tabi/kake) — not field-performance ground. **No sibling contests.**

## (c) considerthese — newest-first, one unimplemented proposal

``ls -lt --time-style=long-iso kake-shokunin/considerthese/``: ``2026-10-26.md 09:05`` · ``2026-10-25.md 09:21`` · ``2026-10-24.md 21:10`` · ``2026-10-23.md 09:05`` · ``2026-10-22.md 09:14`` ·
``2026-10-21.md 09:11`` · ``2026-10-20.md 10:18`` · ``2026-10-19.md 22:08``. Read ``2026-10-26.md`` (newest). **Proposal 4 — the gate-agreement ledger — is still unimplemented in the lane.** Key-term check
at base: ``git show e5f6fd9e:LOG.md | grep -c -i 'gate-agreement'`` → **0**; ``git grep -l -i 'gate-agreement' e5f6fd9e -- corpus/`` → round-58/59/60/62.md + round-62-verifier-spotcheck.md
(rejection/evaluation records only, no artifact); ``git grep -l -i 'gate-agreement' e5f6fd9e -- corpus/knowledge/ scripts/`` → **0**. Implemented instead: 1 (``scripts/id_resolver.py``,
``scripts/landed_check.py``), 3 (r59 routed-item queue), 5 (``corpus/knowledge/gate-status-ledger.md``, r66). Proposal 2 refused as redundant bookkeeping (r63, r67).

## (d) Cross-source — the BigQuery URL is new to every lane registry

``for f in */corpus/SOURCES.md; do grep -c -i bigquery $f; done`` → **0 in every lane**. The only ``developer.chrome.com/docs/crux*`` URLs fleet-wide are kake's own S038 (``/crux/methodology``) and S039
(``/crux/api``); ``grep -rn 'crux/bigquery' --include=*.md .`` hits only the round-70 contract. So no lane-held row already covers ``developer.chrome.com/docs/crux/bigquery``; the staged row is the first
lane-held row for it and the W04 duplicate-URL class does not apply.

## Non-obvious move — make C1's table host-independent and its population closed

**Evidence.** §a.1 (C2's paths enter C1's population), §a.2 (the 17-row table passes only on a host where ``/tmp/kake-r16`` happens to exist; a simulated other host gives ``unannotated=1`` exit 1), §a.3 (a
row can launder a not-yet-committed artifact; prose can manufacture pointers). **Affected axes.** calibration (C1, HOLD 2) and freshness (C2, HOLD 10) — no score movement; an evidence-quality move touching
no C2 file and no registry row.

**Proposed move (one, bounded).** Commit C2's entry, the retained body and the counter **in the same commit** as the SCORECARD round section naming them, and make the calibration table a **host-independent
superset**: one row per dangling token under the *union* of host states (add ``/tmp/kake-r16``), with no prose naming a repo-relative path.

**Risks.** (r1) The table grows one row and one token that does not dangle here — ``pointers`` rises by 1 on this host; inert for the predicate (only ``unannotated`` matters) but the report's count must
match the run. (r2) A row for a path that resolves is inert (verified). (r3) Committing the 110 KB retained HTML follows the round-69 precedent (``.ufo/waves/round-69/w1/ScoutSources/sources/*.html`` are
tracked) but adds a large blob. (r4) The C1 tip must be measured *after* integration, never inferred from the pre-integration simulation.

**Verification (exercised).** At the L1's real integration commit ``50ec1446``: ``python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root . --revision 50ec1446`` → ``pointers=351 dangling=17 annotated=17 unannotated=0 met=true`` exit 0 (this host); the same clone with one token made absent → ``unannotated=1 met=false`` exit 1, and → ``unannotated=0 met=true`` exit 0 once a row for it is added. Cross-checks:
dangling=17 annotated=17 unannotated=0 append_only=true met=true`` exit 0; with the ``/tmp/kake-r16`` row added → met=true exit 0 on a host without it. Cross-checks: ``bash
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md`` → exit 0, ``file ok``, 16 known W04 warnings only, on the L1's integrated registry; ``python3 -B
scripts/id_resolver.py --root . --revision e5f6fd9e --fleet /home/vgpnk/Projects/shokunin`` → exit 0, ``ids_cited=117 ids_resolved=117 dangling=0``.






