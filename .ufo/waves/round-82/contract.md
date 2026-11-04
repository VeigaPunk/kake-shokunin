# kake round 82 — frozen contract (attempt 1)

Lane: kake-shokunin (`/home/vgpnk/Projects/shokunin/kake-shokunin`)
Round: 82 · attempt 1 · host Linux/omp · written 2026-11-04T12:5xZ
Base measured revision: `419866015b1f58e01f061cde9a77d490653d3c76` (lane `master` tip at round
open; the round-81 verifier spot-check erratum)
Frozen before any seat ran. Amended only by a dated amendment written before the after-state it
governs; a predicate, target or kill rule never moves after a seat has scored.

Scores are held this round: a claim moves evidence, not a scalar. The lowest non-retired axis is
`calibration` (2), so C1 works it; C2 works `freshness` (10, held).

## C1 — calibration: the round-81 routed-defect queue closes

Population: the eight items `D1` … `D8` filed by the non-author round-81 closure at
`corpus/lessons/round-81-verifier-spotcheck.md` §7. None added or dropped after this freeze.

Frozen predicate:

    met <=> open == 0

Decided from bytes by `python3 -B .ufo/waves/round-82/c82_defect_queue.py --root <tree>
[--revision <rev>] [--fleet <dir>]`, which reads the measured lane tree (an exported revision in
`--revision` mode) and the fleet repo read-only. No condition is decided by a sentence that merely
says "closed": each item carries a state conjunct re-derived from a non-lesson file.

| Item | State conjunct (re-derived, not quoted) | Row conjunct (`corpus/lessons/round-82.md`) |
|---|---|---|
| D1 | `corpus/SOURCES.md`'s `S433` row cells: `recheck` == `2027-05-03` and `used-by` contains `corpus/lessons/round-81.md` | a `D1` line carrying `180d` and `2027-05-03` (old → new) |
| D2 | `.ufo/waves/round-81/controls/after-c1-final.txt`'s own `revision=<40 hex>` token | a `D2` line carrying that exact token, `2b46f5c4` and `superseded` |
| D3 | the commit token named by the row resolves in the fleet repo, its parent resolves, both blobs of `.ufo/reports/round-81/kake.md` exist and differ | a `D3` line carrying `erratum` and the commit token |
| D4 | `.ufo/waves/round-81/seat-failures.json` `output_bytes` of the `mutation-tester` seat | a `D4` line carrying that integer and `superseded`; no line elsewhere in the lesson carries `3771`/`3,771` without `superseded` |
| D5 | `.ufo/waves/round-81/controls/after-c81-defect-queue.txt` and `…/after-c81-capture-audit.txt` absent at the measured revision; `…/after-c1-final.txt` present | a `D5` line naming both dead paths and the live receipt |
| D6 | `.ufo/waves/round-81/controls/c81-selftest-c2.txt` prints `selftest: 22/22 passed` | a `corpus/QUALITY.md` line carrying `22/22`, `supersedes` and `round-81` |
| D7 | `.ufo/waves/round-82/controls/after-c1-ledger-gate.txt` present and printing `undisclosed=0` and `met=true` | a `D7` line naming that receipt |
| D8 | `corpus/lessons/round-80.md` carries an `[r82-correction` line naming `corpus/SOURCES.md:200` | a `D8` line naming `.ufo/reports/round-80/kake.md` and `corpus/SOURCES.md:200` |

Controls, all committed before the after-state:
- `controls/base-c82-defect-queue.txt` — the counter over base `41986601`; must read
  `open=8 closed=0 met=false`, exit 1.
- `controls/ctl-c82-junk-queue.txt` — a tree whose lesson asserts all eight items closed in prose
  (`junk_tree_build.py`, rebuilt from `junk-tree.json`); must read `open=8`, exit 1.
- `controls/c82-selftest-c1.txt` — one green fixture per item plus one mutant per item and a
  missing-tree fixture; must end `selftest: 11/11 passed`, exit 0.

Kill rule: a base or junk control that reads `met=true` means the counter is wrong and C1 is
**not scored**. A counter whose selftest cannot run green is indistinguishable from a property
that cannot pass (round-81 mined mistake 1).

## C2 — freshness: a second dated capture feeds a capture-to-capture drift gate

Declared surfaces: the three ids and urls frozen at
`.ufo/waves/round-81/capture-expectations.json` (`ds4cc-primary` `https://ds4cc.com/`,
`ds4cc-robots` `https://ds4cc.com/robots.txt`, `ds4cc-sitemap` `https://ds4cc.com/sitemap.xml`).
Capture A is the round-81 tree; capture B is a fresh GET-only capture of the same declared surfaces
under `.ufo/waves/round-82/capture/`.

Frozen predicate:

    met <=> declared == 3
        and surfaces_a == 3 and surfaces_b == 3
        and the round-82 manifest declares exactly the declared ids and urls (same order)
        and receipts_ok   (every receipt in both trees: method GET, integer status in 100..599,
                          integer byte count equal to the retained body length, body sha256 equal
                          to the receipt digest, truncated false, RFC 3339 fetchedAt)
        and order_ok      (every round-82 instant is strictly after its round-81 instant)
        and floor_ok      (every round-82 instant is on or after 2026-11-04T12:42:00Z, the round
                          start recorded in .ufo/watchdog.log:2340)
        and record_equal  (the committed record equals a fresh run's stdout after stripping one
                          trailing newline per side)
        and determinism   (two fresh runs print identical bytes)
        and selftest_ok   (the tool's selftest exits 0 with >= 12 cases)

Counters and instruments, frozen here:
- `scripts/capture_delta.py` — the drift gate. Reads two capture trees, verifies every receipt
  against its retained body, prints one stable line per surface plus `surfaces=<n> identical=<k>
  changed=<k> added=<k> removed=<k>`. Exit 0 record, 1 receipt/manifest fault, 2 tree missing, 64
  usage. Offline by construction: no socket call exists in the file.
- `.ufo/waves/round-82/c82_capture_delta.py` — the predicate above, re-implementing receipt
  verification independently of the tool and comparing the tool's stdout to the committed record
  at a measured revision.
- `.ufo/waves/round-82/population/` — the three `fetch.json` surfaces for `response_snapshot.py`,
  frozen so capture B is one reproducible command.
- `controls/after-c2-delta.txt` — the committed record (the tool's stdout, no command line).

Controls, committed before the after-state:
- `controls/base-c82-capture-delta.txt` — the counter over base `41986601`; must read
  `surfaces_b=0 … met=false`, exit 1.
- `controls/ctl-c82-identical-capture.txt` — capture B replaced by a byte copy of capture A
  (`identical_capture_build.py`); must read `order_ok=0 floor_ok=0 met=false`, exit 1.
- `controls/ctl-c82-tampered-capture.txt` — **post-data control**: it is the real capture B with
  one byte of one retained body flipped, so it cannot exist before capture B does; it is committed
  with the carrier and disclosed as post-data. Must read `receipts_ok=0 met=false`, exit 1.
- `controls/c82-selftest-c2.txt` — nine fixtures (one green, the base control, record drift,
  record absent, order violation, floor violation, dropped surface, tampered body, tool absent);
  must end `selftest: 9/9 passed`, exit 0. The selftest's own `tampered-body` fixture is built from
  synthetic captures, so the counter's ability to see a flipped body is proven before any data.

Kill rule: a base or tampered control that reads `met=true` means the counter is wrong and C2 is
**not scored**.

## Limits stated at the freeze

- C1's row conjuncts are textual by necessity: the registry/receipt/path/record conjuncts are
  state-bound, but "a row names the fix" cannot be. A records-only tree with arithmetically
  correct numbers can reach `open=0`; the non-author closure is what catches a transcription
  (round-81's own F2 limit, inherited).
- D3 reads the fleet repo's history because the filed report is a fleet file outside this round's
  write scope; the erratum it asks for lands in the round-82 report, and the lane-side register is
  what the counter can decide.
- C2 decides the chain, not the property: it proves two dated captures and a reproducible delta
  over committed bytes, not that any surface is correct, not that a future change would be
  detected, and not that a capture came from a socket (a well-formed fabrication with real
  digests passes; provenance is the capture transcript).
- No publish, deploy, account or DNS action. GET-only reads of the three declared public
  surfaces plus source GETs by opening seats.

## Wave plan

One v1 wave, 13 requested seats inside the run-15 band 8–16 (`w1-spec.json`): scout 2, executor 3,
scribe 3, reviewer 2, critic 1, mutation-tester 1, connector 1. Attack share 4/13 = 30.8 % over
{reviewer, critic, mutation-tester, labrat}. The L1 holds the canonical planner seat (the validator
refuses `planner` as a swarm role); a bounded planning data-walk rides `ScoutRecon`.
