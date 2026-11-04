# Round 82 — lessons (kake, attempt 1)

Lane kake-shokunin, base measured revision `419866015b1f58e01f061cde9a77d490653d3c76` (lane
`master` tip at round open, 2026-11-04), round freeze `082b7dd39053e5f96ca6c463da47a3e4d83d4580`
— the commit that carries this round's contract, both counters, the drift tool, the junk and
identical-capture builders, the frozen population and the base and control receipts. One v1 wave,
**13 seats** inside the run-15 band 8–16 (scout 2, executor 3, scribe 3, reviewer 2, critic 1,
mutation-tester 1, connector 1; requested attack share 4/13 = 30.8 % over the four directive roles,
the L1 holding the planner seat). Two claim axes are worked and both are **held**: `calibration`
(2, the lowest non-retired axis) carries C1, and `freshness` (10, held) carries C2. A claim moves
evidence this round, not a scalar. Everything below is author-side: admission belongs to the
non-author closure, which is not this seat.

## Claims

**C1 — calibration: the round-81 routed-defect queue closes.** Population: the eight items `D1` …
`D8` filed by the non-author round-81 closure at
`corpus/lessons/round-81-verifier-spotcheck.md` §7; none added or dropped after the freeze. Frozen
predicate:

    met <=> open == 0

decided from bytes by

    python3 -B .ufo/waves/round-82/c82_defect_queue.py --root <tree> [--revision <rev>] [--fleet <dir>]

which reads the measured lane tree (or an exported revision in `--revision` mode) and the fleet
repo read-only. No item is decided by a word that merely says "closed": each carries a state
conjunct re-derived from a non-lesson file — the `S433` registry cells, a receipt's own
`revision=` token, a fleet commit's blob pair, `seat-failures.json`'s numbers, path presence, a
selftest tally, a gate receipt's fields, or the round-80 lesson bytes — and a row conjunct that
only prose can carry. Controls, all committed before the after-state:
`controls/base-c82-defect-queue.txt` reads `items=8 open=8 closed=0 met=false`, exit 1;
`controls/ctl-c82-junk-queue.txt`, a tree whose lesson asserts all eight items closed in prose,
reads `open=8 met=false`, exit 1; `controls/c82-selftest-c1.txt` ends `selftest: 11/11 passed`,
exit 0 over eleven cases — one green all-eight-closed fixture, one junk-prose fixture, one mutant
per item (eight, `d1-registry-cell-unchanged` … `d8-no-round80-correction`), and a missing-tree
fixture.

**C2 — freshness: a second dated capture feeds a capture-to-capture drift gate.** Declared
surfaces: the three ids and urls frozen at `.ufo/waves/round-81/capture-expectations.json`
(`ds4cc-primary` `https://ds4cc.com/`, `ds4cc-robots` `https://ds4cc.com/robots.txt`,
`ds4cc-sitemap` `https://ds4cc.com/sitemap.xml`). Capture A is the round-81 tree; capture B is a
fresh GET-only capture of the same declared surfaces under `.ufo/waves/round-82/capture/`. Frozen
predicate:

    met <=> declared == 3
        and surfaces_a == 3 and surfaces_b == 3
        and the round-82 manifest declares exactly the declared ids and urls (same order)
        and receipts_ok   (method GET, integer status 100..599, integer byte count equal to the
                          retained body length, body sha256 equal to the receipt digest,
                          truncated false, RFC 3339 fetchedAt, in both trees)
        and order_ok      (every round-82 instant strictly after its round-81 instant)
        and floor_ok      (every round-82 instant on or after 2026-11-04T12:42:00Z)
        and record_equal  (the committed record equals a fresh run's stdout, one trailing
                          newline stripped per side)
        and determinism   (two fresh runs print identical bytes)
        and selftest_ok   (the tool's selftest exits 0 with >= 12 cases)

decided by

    python3 -B .ufo/waves/round-82/c82_capture_delta.py --root <tree> [--revision <rev>]

which re-implements receipt verification independently of `scripts/capture_delta.py` (the offline
drift tool: no socket call exists in the file; exit 0 record, 1 receipt/manifest fault, 2 tree
missing, 64 usage). The committed record is `controls/after-c2-delta.txt`, the tool's stdout with
no command line. Controls, committed before the after-state:
`controls/base-c82-capture-delta.txt` reads `surfaces_b=0 … met=false`, exit 1;
`controls/ctl-c82-identical-capture.txt` (capture B replaced by a byte copy of capture A) reads
`order_ok=0 floor_ok=0 met=false`, exit 1; `controls/ctl-c82-tampered-capture.txt` is **post-data**
— the real capture B with one byte of one retained body flipped — and must read
`receipts_ok=0 met=false`, exit 1; `controls/c82-selftest-c2.txt` ends `selftest: 9/9 passed`,
exit 0 over nine fixtures (green, base, record drift, record absent, order, floor, dropped
surface, tampered body, tool absent), so the counter's power to see a flipped body is proven
before any data.

## Corrections

The eight routed defects of the round-81 non-author closure are corrected here, one line each.
None of round-81's own bytes is rewritten: the rows are appended pointers to the measured file.

**D1 — registry cells.** `corpus/SOURCES.md`'s `S433` row is corrected in place on the two cells SOURCES rule 2 permits: `recheck` `180d` → `2027-05-03` (old → new), and `used-by` gains `corpus/lessons/round-81.md`; the row keeps its line and its eleven cells, and the counter re-derives both cells rather than reading this sentence (base control: `D1 open recheck='180d' used-by='corpus/knowledge/response-header-expectations.md'`).

**D2 — measured revision label.** `.ufo/waves/round-81/controls/after-c1-final.txt` records its own `revision=498a0969499f70830b7c992eb36ea364672f1a1b`; the round-81 before→after rows cited `2b46f5c4`, which only adds the carrier receipts, so that citation is `superseded` and the receipt's own token is the measured revision the counter now compares against.

**D3 — filed-report erratum.** `.ufo/reports/round-81/kake.md` was rewritten in place at `7678247a3c13b1dc03ed1cb8f80d2dba603ee0ca` in four statements (lane-tip line, wave bullet, landed-changes row, claim row), against a report that was already a record; this erratum names the four superseded statements and leaves the original text where PROTOCOL says a filed report's bytes stay. The counter resolves the named commit in the fleet repo, resolves its parent, and requires the two report blobs to differ.

**D4 — disclosure arithmetic.** `.ufo/waves/round-81/seat-failures.json` records `output_bytes` 3801 for the mutation-tester seat (`MutC`, status `reported`); the superseded figure in round-81's prose was not re-derived from that record and is withdrawn, so the record is the only number this lane carries for that seat's output.

**D5 — receipt paths.** `corpus/lessons/round-81.md` §Settlement named `.ufo/waves/round-81/controls/after-c81-defect-queue.txt` and `.ufo/waves/round-81/controls/after-c81-capture-audit.txt`, neither of which exists at any revision; the committed receipts are `.ufo/waves/round-81/controls/after-c1-final.txt` (present, revision-bearing) alongside `after-c1.txt`, `after-c2-carrier.txt` and `after-c2-final.txt`, and the counter re-tests both dead paths and the live one on the measured tree.

**D6 — stale selftest tally.** `.ufo/waves/round-81/controls/c81-selftest-c2.txt` ends `selftest: 22/22 passed`; `corpus/QUALITY.md`'s round-81 criterion cited `18/18`. The appended criterion row at `corpus/QUALITY.md:1695` carries `22/22` and `supersedes` and `round-81` on one line and names the superseded text; the counter re-derives the tally from the receipt, not from the row.

**D7 — ledger-gate receipt.** The standing round-79 receipt ledger is re-run at the freeze and committed as `.ufo/waves/round-82/controls/after-c1-ledger-gate.txt`, whose own line is `C1v2 revision=082b7dd39053e5f96ca6c463da47a3e4d83d4580 events=40 undisclosed=0 phantom=0 malformed=0 wrong_kind=0 unpointed=0 symlinks=0 round_rewritten=0 met=true`, exit 0; the counter requires that receipt to be present and to print `undisclosed=0` and `met=true`, so a red gate reopens the item instead of being narrated green.

**D8 — routed pointer.** `corpus/lessons/round-80.md` now carries an appended `[r82-correction 2026-11-04]` row naming `corpus/SOURCES.md:200` (the `S453` row; `:201` is the blank line after it) and stating that the original sentence is not rewritten; the fleet report `.ufo/reports/round-80/kake.md` still reads `corpus/SOURCES.md:201` and its erratum rides the round-82 report, because that fleet file is outside this round's write scope.

## Gate

**Admit S455** — RFC 9110, *HTTP Semantics*, §8.8.1 *Weak versus Strong* and §8.8.3 *ETag*,
`https://www.rfc-editor.org/rfc/rfc9110.txt`. The landed row's `opened` cell is `2026-11-04` and
its anchor cites `.ufo/waves/round-81/w1/ScoutSources/rfc9110.txt` (502,941 B, sha256
`21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, fetched 2026-11-04T10:44:53Z,
HTTP 200). This round's sources seat re-opened the same URL exactly once, GET-only, at
2026-11-04T12:51:57Z: HTTP/2 200, final URL identical to the request URL, the same 502,941 bytes
and the same digest, `cmp -s` exit 0 against the lane's retained
`corpus/lessons/round-81-gate/rfc9110.txt` — so the row's quote is located in bytes three
independent fetches share. Retained bytes and quote check:
`.ufo/waves/round-82/w1/ScoutSources/rfc9110.txt` and
`…/ScoutSources/receipts/quote_check.{py,txt}`.

Admission quote, retained text `:3572-3574`, **24 words**, match class **raw-substring** (`raw=True`
in the quote check; verified again here against the retained bytes):

> The "ETag" field in a response provides the current entity tag for
>    the selected representation, as determined at the conclusion of
>    handling the request.

Two supporting spans, both raw substrings and both under the cap: the strong-validator definition
fragment, 16 words at `:3403-3404` — "representation metadata that changes value whenever a change
occurs to the representation data that would be" — and the weak-validator definition, 17 words at
`:3438-3439` — "a "weak validator" is representation metadata that might not change for every
change to the representation data." The full strong-validator sentence (`:3403-3405`) is 31 words
and **collapsed-only** (the 72-column wrap inserts `\n   ` between "value" and "whenever"); it is
recorded as collapsed, not passed off as raw.

Tier A: Standards Track document, definitional semantics. Scope: what a strong validator guarantees
about a change in the representation data and what a weak one does not guarantee — *not* cache
freshness, *not* conditional-request evaluation, *not* the ETag trailer placement, *not* any lane
capture, digest or drift property. The row landed at `corpus/SOURCES.md:202`, immediately after
`S454` (line 201), so no earlier row moves, and
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
exits 0 with the S455 `W04` duplicate-URL warning (`W04=22`, one more than the 21 in
`controls/census-before.txt`) and no `E04`, `E12` or `E01`–`E10`. Sharpest
overlap, stated not hidden: `S010` already holds §8.8.1 + §8.8.3 on the `.html` form; S455 is the
plain-text row narrowed to the representation-data direction and the weak non-guarantee, and it is
the row to withdraw if a later census treats section overlap as fatal.

**Reject — the §8.8.3 trailer paragraph and §8.8.3.1 *Generation* as anchors for that row.**
Located at `:3614-3617` ("A sender MAY send the ETag field in a trailer section … unless the entity
tag is generated while sending the content") and `:3619-3641` (only the service author knows the
implementation well enough to select a validation mechanism). Both exist in the retained bytes and
both are readable, but the first is field placement and the second is mechanism selection: neither
states what a validator guarantees, and the proposed row's own scope cell excludes trailer
placement, so admitting either span would make the anchor wider than the reading. Rejected, and
the row cites §8.8.1's two definitions and §8.8.3's definition/strong-default spans
(`:3607-3612`) instead.

## Mistakes

Rows are `class · evidence pointer · captured-by · fix`; each fix names the check that can fail.

- **receipt-shape** · `.ufo/waves/round-82/w1/L1/faulty-receipt.txt` carries two `^exit=` lines for
  one run, while the committed `controls/after-c1-ledger-gate.txt` carries one; the counter prints
  its own line (`c79_receipt_ledger.py:152`) and the wrapper appended a second ·
  **captured-by:** the L1, in this wave, before the receipt was committed ·
  **fix:** the receipt was rewritten with only the counter's own line, and the check
  `grep -c '^exit=' <receipt>` is shown able to fail — 2 on the faulty bytes versus 1 on the
  committed receipt (`.ufo/waves/round-82/w1/L1/duplicate-exit-repro.txt` records both, and the
  repro file's own three matches are one clean receipt plus the faulty pair).
- **stale-tally** · `corpus/QUALITY.md`'s round-81 criterion cited `18/18` while
  `.ufo/waves/round-81/controls/c81-selftest-c2.txt` ends `selftest: 22/22 passed` ·
  **captured-by:** the non-author round-81 closure (spotcheck §7, D6) ·
  **fix:** `c82_defect_queue.py`'s `item_d6` re-derives the tally from the receipt and requires a
  one-line superseding QUALITY row; it is shown able to fail by the base control
  (`D6 open criterion=no receipt22=yes`, exit 1) and by the `d6-stale-tally` mutant in
  `controls/c82-selftest-c1.txt`.
- **claim-vs-bytes** · the round-81 report and scorecard said the `S433` cells had moved while the
  row was byte-identical to base (`recheck` still `180d`) ·
  **captured-by:** the non-author round-81 closure (D1) ·
  **fix:** `item_d1` reads the two cells from the registry and never a sentence; the base control
  (`D1 open recheck='180d'`, exit 1) and the `d1-registry-cell-unchanged` mutant show the check
  failing on the stale row and green only after the cells move.

## Limits

- **Capture provenance.** C2 proves two dated captures and a reproducible, offline delta over
  committed bytes; it does not prove a socket produced either tree. A well-formed fabrication with
  real digests passes, so provenance stays the capture transcript's claim
  (`.ufo/waves/round-82/w1/ExecCapture.md` and its receipts), not the counter's.
- **Property conformance.** The delta reports identical/changed/added/removed bytes per surface; it
  is not a verdict that any surface meets the frozen expectations, and a change after capture B
  would only be seen by a third capture. C2 decides the chain, not the property.
- **C1's record-closure class.** The row conjuncts are textual by necessity. A records-only tree
  whose numbers are arithmetically correct can reach `open=0`; the non-author closure is what
  catches a transcription. This is round-81's own F2 limit, inherited unchanged.
- **Author-side.** This file is the author-side evidence file; every verdict here is provisional
  until the non-author closure re-derives it.

## Settlement (appended 2026-11-04)

Written while the wave was still landing; two things were absent at this writing and are named
rather than assumed.

- **D1's state conjunct.** At probe time `corpus/SOURCES.md`'s `S433` row still read
  `recheck='180d'`, `used-by='corpus/knowledge/response-header-expectations.md'`, so the counter
  printed `D1 open` and `C1v1 … items=8 open=1 closed=7 met=false`
  (`.ufo/waves/round-82/w1/ScribeLesson82/counter-probe.txt`). Those two cells are `ExecRegistry`'s
  production target in this wave; the `D1` row above is the correction it lands, and the counter
  re-derives the cells, so this note can only go stale in the direction of turning green.
- **C2's data half.** `.ufo/waves/round-82/capture/` and `.ufo/waves/round-82/controls/after-c2-delta.txt`
  did not exist at this writing, so no capture-B instant, surface count or delta result is stated
  anywhere in this file; `ExecCapture` and `ExecDelta` own them, and
  `controls/base-c82-capture-delta.txt` records the base reading (`surfaces_b=0 … met=false`).

Everything else in `## Corrections` and `## Gate` was re-derived from committed bytes at probe
time: the counter read `D2`–`D8` closed on their state and row conjuncts.

## Assimilation (appended 2026-11-04 by the L1, on ConnectorC's re-derivation)

Assimilation: none. At base `419866015b1f58e01f061cde9a77d490653d3c76` (registry blob
`1ffc61f1…435f`) the `merge/kake` package (`/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md`,
sha256 `5f0cd4c4…f0cc`, last touched 2026-10-24 by `ba6779f0`) holds 129 staged rows against the
lane's 192: **8 ids collide** and carry the identical source cell (S312, S329, S367, S372, S373,
S374, S390, S409), **19 further staged rows** stage a source the lane already holds under another
id (S287→S137, S288→S138, S289→S139, S296→S080, S299→S262, S300→S263, S310→S273, S311→S274,
S323→S286, S352→S438, S375→S419, S376→S420, S380→S418, S395→S423, S398→S425/S427, S399→S249,
S403→S421, S408→S422, S415→S429), and the remaining **102 are unscreened** in a package 11 days
stale — so no staged row is both unheld and screened, and none was adopted. Full evidence:
`.ufo/waves/round-82/w1/ConnectorC.md` §2 and `…/ConnectorC/evidence.txt` §D; the package was read
only (nothing written into `/home/vgpnk/Projects/shokuknow`).

## considerthese mining (one proposal, held for round 83)

`considerthese/2026-10-26.md` Part 2 was re-read this round. Proposal #2 (receipt-rewrite watch) and
#5 (historical-gate list) are already implemented and registered (`SKILL.md:1293`, `:1493`,
`:1509`; `corpus/knowledge/gate-status-ledger.md`). Proposal **#4, the gate-agreement ledger, is the
single still-unimplemented proposal** and the one that fits this round, because C1's limit makes the
non-author closure load-bearing and nothing in the lane counts whether that closure has ever
disagreed. It is **recorded, not landed**: the exact QUALITY criterion row it should land as next
round is in `.ufo/waves/round-82/w1/ConnectorC.md` §3, and round 82's own closure becomes its first
data point. Landing a new criterion mid-round would be scope drift against the frozen contract.

## Appended note — what the delta's verdict can and cannot say

**[r82-note 2026-11-04]** The `## Limits` bullet above that calls the delta a report of
"identical/changed/added/removed **bytes** per surface" is imprecise; this note corrects it by append.
`identical` conjoins status, body sha256, body length **and the whole header mapping**, and the tool has
no header skip list, so on this property `identical=0 changed=3` is structural rather than a finding:
the three capture-A receipts, all fetched at `2026-11-04T12:05:06Z`, already disagree on
`x-github-request-id`, `x-fastly-request-id`, `x-timer`, `x-served-by`, `x-cache` and `expires`, i.e.
those fields track the request instant, not the resource. Read `body=` and `status=` for content; read
`verdict=` as "any recorded facet differed". `field=etag` is redundant with `last-modified` plus
`content-length` (`corpus/knowledge/ghp-etag-anatomy.md`). And both trees must come from the same
client: `scripts/response_snapshot.py` records `userAgent` per receipt, but `capture_delta.py` never
compares it across trees, so a UA bump between rounds would compare two representations and print
`body=changed` — under mori's `Vary` rule (S594, RFC 9111 §4.1) exactly the case that is not content
drift. Round-83 follow-on, not this round: make the tool fault on a per-surface `userAgent` mismatch.
Evidence: `.ufo/waves/round-82/w1/ConnectorC.md` §5 and `…/ConnectorC/evidence.txt` §E–§F. This note
moves no predicate, target, kill rule, control or tool byte.

## Author-side mutation probe (appended 2026-11-04 by the L1; not a seat)

After both claims were measured, the L1 mutated copies of both counters in scratch and scored each
mutant against the counter's own selftest. This is author-side evidence, offered to the closure; it
moves no predicate and repairs nothing.

**C1 (`c82_defect_queue.py`), 5 mutants, 3 killed.**

| Mutant | Change | Result |
|---|---|---|
| m1 | last item dropped from the evaluated list | `selftest: 9/11`, killed |
| m2 | D1's exact cell compare replaced by a substring test that also accepts `180d` | `10/11`, killed |
| m3 | D4's derived number replaced by the constant `3801` | **`11/11`, survived** |
| m4 | row-conjunct matcher made token-OR instead of token-AND | `9/11`, killed |
| m5 | D7's `met=true` requirement dropped | **`11/11`, survived** |

m3 survives because the green fixture's `seat-failures.json` records `output_bytes` 3801 — the same
number as the live record — so a constant is indistinguishable from a derivation; the killer fixture
is a fixture record with a different byte count. m5 survives because no fixture carries a receipt with
`undisclosed=0` and `met=false`; the existing `d7-red-gate-receipt` mutant flips `undisclosed`, which
the other conjunct catches.

**C2 (`c82_capture_delta.py`), 5 mutants, 1 killed, 1 equivalent, 3 survived.**

| Mutant | Change | Result |
|---|---|---|
| m1 | `record_equal` replaced by a first-line comparison | `8/9`, killed |
| m2 | order conjunct made non-strict (`>=`) | **`9/9`, survived** |
| m3 | body-length check removed | **`9/9`, equivalent mutant** — sha256 equality already implies equal length |
| m4 | `selftest_ok` hard-coded to 1 | **`9/9`, survived** |
| m5 | `surfaces_a == 3` conjunct dropped | **`9/9`, survived** |

m2 survives because no fixture pair has equal instants (the order-violation fixture is an *earlier*
instant, which both forms reject); m4 survives because the tool-absent fixture also fails
`determinism` and `record_equal`, so `met` stays false and the hard-coded bit is invisible; m5
survives because no fixture has a dropped capture-A surface.

**Probe defect, disclosed.** The first C2 mutant run scored every mutant red for the wrong reason:
the counter's selftest resolves the tool as `Path(__file__).resolve().parents[3] / TOOL`, and the
mutant copies sat three levels below the scratch root, so the tool was absent and every fixture failed
on that, not on the mutation. Those readings were discarded and the probe re-ran with each mutant at
`<scratch>/<mutant>/.ufo/waves/round-82/` and a copy of the tool at `<scratch>/<mutant>/scripts/`; the
table above is the corrected run. Class: *a mutant scored against a harness whose path resolution
moves with the mutant*. Captured-by: none. Fix: the corrected layout, shown able to fail (m1 dies
`8/9` in the same run, so the harness does exercise mutations).

**Routed, not repaired.** The counters are frozen and were measured at the carrier; changing a fixture
after the after-state would break the correspondence between the receipts and the committed bytes. The
round-83 repair is the four killer fixtures named above (C1: a non-3801 seat record, an
`undisclosed=0 met=false` receipt; C2: equal instants, a green tree with a broken tool, a dropped A
surface), then the same mutants re-run.

## Appended erratum — the delta's `body=same` compares stored objects (ConnectorC §6)

**[r82-erratum 2026-11-04]** The `[r82-note]` above says the six differing fields "track the request
instant, not the resource". That is too broad for two of them, and the correction matters for how C2
may be read. `x-github-request-id`'s trailing hex is a Unix epoch (the **cache-fill** instant) and
`expires` is that epoch plus the 600-second `max-age`, so both are invariant across A→B on every
surface — primary `…6AEB18EA` = `2026-11-04T11:37:14Z` with `expires` `11:47:14Z`; robots and sitemap
`…6AEB1F72` = `2026-11-04T12:05:06Z` with `expires` `12:15:06Z`. Four of the six
(`x-fastly-request-id`, `x-timer`, `x-served-by`, `x-cache`) are per-request; the other two are
cache-fill-bound. Verified: `python3 -B .ufo/waves/round-82/w1/ConnectorC/cachefill.py` exits 0,
printing `expires − fill = 600` on all six rows and `A.ghr == B.ghr` `True` on all three surfaces
(`…/ConnectorC/cachefill.txt`).

**Consequence.** Both captures observed the **same stored objects** — robots and sitemap as a HIT on
the entry capture A's own MISS created, primary on an entry filled at `11:37:14Z`, 28 minutes before
A. `body=same` therefore says the edge served identical bytes at two instants; it does **not** say the
property's origin was read twice 55 minutes apart. `Age: 0` in B with `expires` already 45–133
minutes past shows a revalidation, not a re-fill. This is mori's cache-selection rule (S594, RFC 9111
§4.1) and kumitate's age rule (S237, §4.2.3) instantiated on kake's own property — reported as
adjacency, not absorbed. Round 83's instrument change, cheaper than the UA check the note asks for:
compare `x-github-request-id` per surface across the two trees, where equality means B may not have
re-read origin — a fact the current record cannot express.
