# ConnOverlap — kake round 70, W1 connector (read-only)

Base revision `e5f6fd9e4c243d092160bc74e8bea24256087173`; bytes read with `git show e5f6fd9e:<path>`.
Receipts: `.ufo/waves/round-70/w1/ConnOverlap/receipts.txt`. No lane tracked file modified.
Tools installed/upgraded: none (pacman untouched). Scratch `/fast/scratch/hyaku/kake-r70/ConnOverlap` removed on exit.

## (a) Overlap — each claim is verifiable without the other landed

| Claim | Files touched | Verification command (does not read the other claim's files) |
|---|---|---|
| C1 | `SCORECARD.md` (appended section), `.ufo/waves/round-70/c70_pointer_audit.py`, `corpus/QUALITY.md` (end-of-file), `corpus/lessons/round-70.md`, `LOG.md` | `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <lane> --revision <rev>` |
| C2 | `corpus/knowledge/crux-bigquery-origin-membership.md`, `corpus/SOURCES.md` (one row), `corpus/lessons/round-70.md` (Gate), `LOG.md`, `SCORECARD.md` (round section) | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` |

Read-set proofs (receipts `[a]`): with `corpus/` deleted from a clone, the C1 counter still prints
`pointers=348 dangling=17 annotated=0 unannotated=17 met=false` — byte-identical to the intact lane.
The census script contains **0** occurrences of `SCORECARD|QUALITY|lessons`; it reads only
`corpus/SOURCES.md` per lane and `test -e` on used-by paths. So the counters do not read each other's files.

**Two couplings the contract's "causally separable" does not cover** (both exercised on git fixtures):

1. **The shared SCORECARD round section is C1's population.** C1 enumerates path-like tokens from the
   *whole* SCORECARD.md, so the L1's round section — which names C2's entry and C2's retained body —
   enters C1's population. Fixture: SCORECARD naming `.ufo/waves/round-70/c70_pointer_audit.py`,
   `.ufo/waves/round-70/w1/ScoutSources/sources/S438-crux-bigquery.html` and
   `corpus/knowledge/crux-bigquery-origin-membership.md` gives `dangling=3 unannotated=3` before those
   artifacts are committed and `dangling=1` after. C1's verdict therefore depends on **when** C2's
   artifacts are committed, not only on C1's own bytes.
2. **The C1 counter can launder a not-yet-committed artifact.** An annotation row whose first cell is
   the exact token of a live-but-uncommitted path annotates it away: fixture gives
   `dangling=1 annotated=1 unannotated=0 append_only=true met=true` exit 0 for a file absent from the
   revision. `append_only=true` does not detect it. Same channel: a calibration row whose prose cites an
   absent lesson (`corpus/lessons/round-11.md`) *creates* a new dangling pointer
   (`pointers=2 dangling=2 annotated=1 unannotated=1` exit 1) unless that token is also annotated.

Also measured: the contract's "staged id S352 collides with the lane registry's S352" is **false** —
the lane registry holds no S352 (0 hits, 175 rows, max S437). The 8 staged collisions are
S312 S329 S367 S372 S373 S374 S390 S409. The adopted id remains **S438** by the next-unused rule.
E03 duplicate-id is intra-lane only (two lanes each holding S900 → both `ok`, 0 E03).

## (b) Sibling scan — no sibling owns CrUX or field-performance ground

Grep of all 19 sibling `PROVINCE.md` for `crux|core web vital|\bCWV\b|field.?data|real.?user|\bRUM\b|lighthouse|bigquery|web.?vitals|page.?speed|user experience` → **0 in every sibling**.
Grep of every sibling `corpus/knowledge/` for `developer.chrome.com/docs/crux|CrUX (eligibility|API|methodology)|Chrome UX Report` → no hits.
kake's own claim: `kake-shokunin/PROVINCE.md:24` — "Field performance (Core Web Vitals, CrUX eligibility) — first entry".
Adjacency lines checked (all assign *web properties* to kake, none claim field performance):
`kengaku/PROVINCE.md:34`, `kasegi/PROVINCE.md:49`, `tabi/PROVINCE.md:16`, `kama/PROVINCE.md:43`,
`kotodama/PROVINCE.md:20`, `kotoba/PROVINCE.md:65`, `kagi/PROVINCE.md:64`.
`tabi/PROVINCE.md:33,39-42` mention Chrome only as a browser/CDP surface; `kagi/PROVINCE.md:64` is the
the-musketeer profile lease (contested kagi/tabi/kake) — not field-performance ground. **No sibling contests.**

## (c) considerthese — newest-first, and one unimplemented proposal

`ls -lt --time-style=long-iso kake-shokunin/considerthese/`:
`2026-10-26.md 09:05` · `2026-10-25.md 09:21` · `2026-10-24.md 21:10` · `2026-10-23.md 09:05` ·
`2026-10-22.md 09:14` · `2026-10-21.md 09:11` · `2026-10-20.md 10:18` · `2026-10-19.md 22:08`.
Read `2026-10-26.md` (newest; unchanged since — round-68 lesson records the same).

**Proposal 4 — the gate-agreement ledger — is still unimplemented in the lane.** Key-term check at base:
`git show e5f6fd9e:LOG.md | grep -c -i 'gate-agreement'` → **0**;
`git grep -l -i 'gate-agreement' e5f6fd9e -- corpus/` → round-58/59/60/62.md + round-62-verifier-spotcheck.md
(all rejection/evaluation records, no artifact);
`git grep -l -i 'gate-agreement' e5f6fd9e -- corpus/knowledge/ scripts/` → **0** (no implementing artifact).
The other four are implemented: 1 → `scripts/id_resolver.py`, `scripts/landed_check.py`; 3 → the r59
routed-item queue; 5 → `corpus/knowledge/gate-status-ledger.md` (adopted r66). Proposal 4 stays refused
(r62 flip: "repeated verifier/gate comparisons show a durable need"; r67: verifier-side data, not lane-ownable).

## (d) Cross-source — the BigQuery URL is new to every lane registry

`for f in */corpus/SOURCES.md; do grep -c -i bigquery $f; done` → **0 in every lane**.
The only `developer.chrome.com/docs/crux*` URLs fleet-wide are kake's own S038 (`/crux/methodology`)
and S039 (`/crux/api`). `grep -rn 'crux/bigquery' --include=*.md .` hits only the round-70 contract.
So no lane-held row already covers `developer.chrome.com/docs/crux/bigquery`; the staged row is the first
lane-held row for it, and the W04 duplicate-URL class does not apply to it.

## Non-obvious move — make C1's population honest about *what it measures*

**Evidence.** C1's counter derives its population from the whole SCORECARD.md, so the L1's shared round
section injects C2's paths into C1's measurement (§a.1), and any token can be annotated away with a
self-referential row (§a.2). Both are order- and prose-dependent, not evidence-dependent.

**Affected axes.** calibration (C1, HOLD 2) and freshness (C2, HOLD 10) — both untouched in score; the
move is a measurement-honesty move, not a score move.

**Proposed move (one, bounded).** Before the L1 writes the round-70 SCORECARD section, have it (i) commit
C2's `corpus/knowledge/crux-bigquery-origin-membership.md` and the retained body
`.ufo/waves/round-70/w1/ScoutSources/sources/S438-crux-bigquery.html` **in the same commit** as the
SCORECARD section that names them, so C1's population sees resolved paths rather than dangling ones;
(ii) write the `## Pointer calibration (round 70)` rows with **no prose that names a repo-relative path**
(otherwise the row manufactures a pointer — §a.2), naming the event class and the LOG row instead; and
(iii) treat any calibration row whose first cell is a path that is *expected to exist at the tip* as a
defect, since the counter cannot distinguish "historical" from "not yet committed" (§a.2).

**Risks.** (r1) C1's population shifts when C2's artifacts commit — the tip measurement must be run
after integration, never inferred from a pre-C2 simulation; the L1's `after-sim.txt` for the *counter*
is scratch-only and cannot stand in for the lane after-state. (r2) Committing the retained HTML into the
lane tree is the round-69 precedent (`.ufo/waves/round-69/w1/ScoutSources/sources/*.html` are tracked),
so it is a precedent-supported step, but it adds a 110 KB binary-ish blob to the lane tree. (r3) Restricting
calibration prose to non-path forms weakens the reviewer's ability to cross-check the record; the LOG row
number plus the dated event class still carries the same information.

**Verification (exercised).** `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <lane> --revision <tip>`
after integration must print `unannotated=0` and exit 0 with the calibration section present, and the
population count must equal the base count plus only the tokens the section's *first cells* introduce.
Cross-checks run: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kake` exits 0 with the 16 known W04 warnings and no E-row on a full-lane
mirror carrying the normalized S438 row (receipts `[d]`, `[id]`); `python3 -B scripts/id_resolver.py --root .
--revision e5f6fd9e --fleet /home/vgpnk/Projects/shokunin` exits 0 with `ids_cited=117 ids_resolved=117
dangling=0`.

## Unimplemented-proposal note

Only proposal 4 of `considerthese/2026-10-26.md` remains unimplemented in the lane (checks above);
proposals 1, 3, 5 are implemented and proposal 2 is refused as redundant bookkeeping (r63, r67).
