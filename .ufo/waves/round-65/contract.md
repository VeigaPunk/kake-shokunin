# Round-65 contract (predicate freeze before any wave data, 2026-10-30)

Base revision: `d3a4e40228c307954fa6ced6cab03654faac1ffa` (round-64 wrap-up tip).
Round shape: ONE v1 wave `w1` of 32 seats (live validator band 32–48 after the
run-13 mid-run amendment "also make concurrency 32-48"; the round-65 prompt
snapshot still says 16–32 — the policy file is the validator authority and the
amendment is recorded in its `sighting.dispatch.swarm.note`).

Two-phase freeze: THIS file freezes predicates, kill rules, targets, fixture
definitions and control classes before any seat runs (commit 1, base tree).
Instrument sha256 pins are recorded in `## Instrument freeze` below after the
build items land and before any after-state receipt is taken (commit 2) — a
counter, control or predicate changed after a seat has scored is not this
round's rule; a kill-rule breach lands the affected claim `unprovable`.

Census before: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, 171 rows, 16 W04 (`.ufo/waves/round-65/controls/census-before.txt`).

## Round-65 routed inputs (from corpus/lessons/round-64-verifier-spotcheck.md)

- Defect 1: retain the C1 honest stop; before the next freeze reject
  token/contradictory prose and hidden-comment criteria; authenticate the
  outside-verdict source rather than only copying its text into the lesson.
- Defect 2: ship reproducible ledger/fixture construction and honest control
  provenance (the round-64 ledger-mut control receipt has no committed builder).
- Defect 3: reconcile proposal-5 flip and c56 live selftally red through the
  existing gate registry, with paired base/after evidence (work item, not a claim).
- Defect 4: append correction of expansion attribution (a working unchanged
  classifier is not new frontier capability) — SCORECARD/LOG append, not a claim.
- Defect 5: resolve the untracked `.ufo/waves/round-64/sources/S432.live.html`
  durability debt in lane scope — C2 below.

## C1 — calibration (lowest owned non-retired axis, 2/10): kill-rule classes counter-enforced for the S432 outside-disagreement resolution

Rounds 62–64 each landed a calibration counter whose green the wave then
showed did not bind semantics: r63 marker-prose greens; r64 contradictory Gate
prose greens (`w1/ReviewerC1Prose.md`), a QUALITY criterion hidden in an HTML
comment (`w1/MutC1Prose.md` Q3x), and one-sided outside-verdict binding
(`w1/ScoutSpotSpan.md` A1: a one-line verdict replacement stays green with all
source pins intact). Round-64's QUALITY addendum already rules "block-scoped
token presence is not semantic resolution" — so this claim does NOT assert
semantic proof. It asserts the narrower, falsifiable repair the closure routed:
the four known green classes are now counter-enforced controls, the
outside-verdict artifact is authenticated against committed bytes, and every
attack fixture is reproducible from a committed builder with honest provenance.

Frozen predicate (identical sentence in this contract, the counter docstring
and the receipt labels): **at the measured revision,
`python3 -B .ufo/waves/round-65/c65_semantics.py --root . --revision <measured>`
prints `met=true` (exit 0); at the base `d3a4e402` it prints `met=false`
(exit 1); and against each of the four committed attack fixtures A1 marker-only
prose, A2 contradictory Gate prose, A3 hidden-comment criterion, A4
outside-verdict tamper, it prints `met=false` (exit 1) naming the failed
component — and each fixture is rebuilt by the committed
`.ufo/waves/round-65/fixtures/build_attack_fixtures.py` with its build receipt
committed.**

Counter design (build item; the L1 pins its sha256 in `## Instrument freeze`
before after-receipts):

- Reads committed bytes only (`git show <revision>:<path>`), never the
  worktree.
- Components (each prints `name=0/1`, all must be 1 for `met=true`):
  `pins` (frozen sha256 constants for: round-61 spot-check file, round-64
  lesson, round-64 QUALITY append region, S432 retained blob, frozen quote
  span, frozen attribution span), `disagreements` (the spot file carries
  exactly one S432/Disagree line — the ≥1 disagreement input stays live),
  `spot_auth` (spot file sha matches pin AND the lesson Gate quotes the frozen
  verdict span verbatim AND the Gate names the spot file as the span's source —
  attribution, not copied text), `criterion_visible` (the semantic criterion
  exists in QUALITY outside HTML comments and names its grounding lesson),
  `gate_noncontradictory` (the Gate's admission block contains the frozen
  admission span and none of the frozen contradiction spans), `quote_class`
  (the ledger class for the frozen quote re-derives collapsed-only inline from
  the pinned blob via the committed extract recipe — never gating on
  `scripts/quote_class.py`), `unresolved` (≥1 disagreement never masked:
  `unresolved = max(disagreements - (1 if admission else 0), 0)` must be 0 only
  when the admission block is fully green).
- Kill rule: if the after receipt does not print `met=true` at the measured
  commit, or any pin differs at the measured revision, or any of A1–A4 prints
  `met=true`, or the counter crashes (traceback) on adversarial input, or any
  wave seat reproduces any green class (marker-only, contradiction,
  hidden-comment, tamper, sha-collision aside) against the frozen counter, C1
  is `unprovable` (honest stop), no calibration credit. Score stays 2 either
  way unless the non-author closure rules otherwise; a measured met is recorded
  as calibration 2→2 (HOLD), the move being "the four routed green classes are
  counter-enforced and the outside verdict is byte-authenticated".
- Counting command:
  `python3 -B .ufo/waves/round-65/c65_semantics.py --root . --revision <commit>`
- §9 do-nothing control: the base tree (no round-65 work) must print
  `met=false`; a tree carrying only copied lesson text without authenticated
  spot bytes must print `met=false`; a constant `met=true` mutant of the
  counter fails the counter's own selftest. Receipts: `controls/base-c1.txt`,
  `controls/donothing-c1-{base,copied}.txt`, `controls/selftest-c1.txt`.

Fixture definitions (built by the committed builder, revisions recorded in
`controls/fixture-builds.txt`):

- A1 marker-only: real spot/lesson bytes at base plus a lesson Gate extended
  with marker sentences (frozen ids/digests only, no verdict span, no
  attribution) — `spot_auth` must fail.
- A2 contradictory: real bytes plus a Gate that quotes the verdict span AND
  carries a frozen contradiction span ("withhold semantic-counter credit"
  outside the historical-settlement block) — `gate_noncontradictory` must fail.
- A3 hidden-criterion: real bytes with the semantic criterion moved inside an
  HTML comment in QUALITY — `criterion_visible` must fail.
- A4 tamper: real bytes with the spot file's S432/Disagree line flipped to
  Agree (sha no longer matches pin) — `pins`/`disagreements` must fail.

## C2 — freshness (HOLD 10): the S432 retained live re-open body is committed (routed defect 5)

The round-64 closure measured `.ufo/waves/round-64/sources/S432.live.html` as
an untracked lane-authored file — reaper-exposed (`/tmp` class risk per the
scratch-discipline rule; anything a report points at must be in the lane tree)
and a durability defect: "retained round-64 bytes and the committed receipt
remain accessible" only while the file survives.

Frozen predicate (identical sentence in this contract, the receipt labels and
the lesson §Mistakes): **at the measured revision,
`git ls-tree -r --name-only <measured> -- .ufo/waves/round-64/sources` prints
exactly `.ufo/waves/round-64/sources/S432.live.html`, and
`git show <measured>:.ufo/waves/round-64/sources/S432.live.html | sha256sum`
prints `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`,
while at the base `d3a4e402` the ls-tree output is empty; and on the measured
tree `node scripts/freshness-sweep.mjs --offline` still exits 0 (no-harm).**

- The pinned sha equals the round-61 retained body
  (`.ufo/waves/round-61/sources/S432.html`, sha256
  `63b0a018…911b`, byte-identical at base) — the claim commits the exact
  already-retained bytes; no live fetch is part of the predicate. The live
  re-open (scout seat, ONE GET) is the §2b sourced-claim evidence and records
  currency, not a predicate input.
- Kill rule: if the after receipt's ls-tree lists anything else or the sha
  differs, or the sweep exits non-zero on the measured tree, or the commit
  carrying the file changed any byte of it, C2 is `unprovable`.
- Counting command:
  `git ls-tree -r --name-only <commit> -- .ufo/waves/round-64/sources && git show <commit>:.ufo/waves/round-64/sources/S432.live.html | sha256sum`

## Separability

C1 touches only `.ufo/waves/round-65/` instruments, fixture trees (scratch +
receipts) and receipts; C2 touches only `.ufo/waves/round-64/sources/S432.live.html`
(tracked) plus receipts. C1 verifies on a tree where C2's file is untracked
(the counter never reads it); C2 verifies with no c65 instrument present.
Neither edits `corpus/SOURCES.md` (C2's claim evidence cites existing row
S432, re-opened this round — §2b sourced claim; no new row this round).

## No-harm

Append-only edits to `corpus/QUALITY.md`, `LOG.md`, `SCORECARD.md`,
`corpus/lessons/round-65.md` (new). `SKILL.md`, the sidecar, the registry, the
sweep script and all round-64 bytes stay untouched (no gate-registry rows are
added this round, so the round-64 sidecar pins cannot drift). After-receipts:
`controls/after-c1.txt`, `controls/after-c2.txt`, `controls/sweep-after.txt`,
`controls/census-after.txt`, integrated `controls/after-final.txt`.

## Instrument freeze

(To be filled by the L1 after build items land, before any after-state
receipt; commit 2 records the pins.)

- `.ufo/waves/round-65/c65_semantics.py` — sha256 `PENDING-BUILD`
- `.ufo/waves/round-65/fixtures/build_attack_fixtures.py` — sha256 `PENDING-BUILD`
