# Round 51 — lesson shape audit (`corpus/lessons/round-51.md`)

Scribe seat: `L1Kake51.ScribeLessonShape-2`. Judged axis: freshness. Read-only; no product
file was modified. Tools installed or upgraded: none.

## Subject

- Path: `corpus/lessons/round-51.md` in `/home/vgpnk/Projects/shokunin/kake-shokunin`.
- Measured revision: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (`git log --oneline -3`, tip).
  `git ls-tree -r 9d13768 -- corpus/lessons` lists the file; `git diff --stat HEAD --
  corpus/lessons/round-51.md` is empty, so worktree bytes equal the measured commit.
- Size/shape: 116 lines, 7 `##` sections, one `#` title (line 1). Headings:

| Line | Heading |
|---|---|
| 6 | `## Gate` |
| 18 | `## Admitted entries` |
| 32 | `## Refused entries (reason and flip)` |
| 49 | `## Stripped staged prose` |
| 60 | `## Id collision check` |
| 69 | `## Quarantine` |
| 76 | `## Mistakes` |

## Contract provisions applied

- `/home/vgpnk/Projects/shokunin/LEARNING.md:69-71` — a lane round lesson "carries a `## Gate`
  section: candidates considered, admitted, rejected (with reasons), and the spot-check
  result; a round that mines mistakes adds `## Mistakes`".
- `/home/vgpnk/Projects/shokunin/LEARNING.md:26` — "The three trends — one verdict each, every
  round"; `:35` makes the discernment verdict depend on the outside spot-check;
  `:40-45` — a non-author (fresh reviewer or operator) spot-checks at least one admit and one
  reject and records `agree`/`disagree` with a reason **in the round's lesson**.
- `/home/vgpnk/Projects/shokunin/CORPUS.md:19-20` — same Gate contract sentence (candidates,
  admitted, rejected with reasons, spot-check result).
- `CORPUS.md:113-117` — the round lesson's `## Gate` records, per new row, URL, access date
  and a ≤25-word quote with location; every in-place `status`/`recheck`/`used-by` change is
  logged old→new in the round lesson.
- `CORPUS.md:171-177` — `## Mistakes` rows carry class · evidence pointer · captured-by ·
  fix, classes drawn from the `mistakes.md` §5 vocabulary.

## Required parts — present / absent / empty

### Absent

1. **Spot-check result — entirely absent.** No non-author review is recorded anywhere in the
   116 lines: `grep -n 'spot-check\|agree\|disagree' corpus/lessons/round-51.md` returns only
   line 96, the clause "they disagree" inside a `## Mistakes` fix description of a counter, not
   a spot-check verdict. No `agree`/`disagree` token, no reviewer identity, no reason, no
   sampled admit, no sampled reject. No companion file exists either:
   `ls corpus/lessons/ | grep -i 51` prints only `round-51.md` (contrast rounds 21/22/28-32,
   which carry `corpus/lessons/round-<N>-verifier-spotcheck.md` with the three trend verdicts).
   Consequence: the discernment trend has no verdict of record for round 51, and
   `LEARNING.md:42-45` is unmet by the lesson itself. The lesson is lane-authored (`line 3:
   "Author: Kimi fresh L1 (this session)"`), so self-attestation would not satisfy it.
2. **`## Gate` carries no reject with a reason.** `## Gate` spans lines 6–16 (body ends before
   the line 18 heading). It holds only the two admitted row bullets (lines 8, 9) and the
   re-grounding prose (lines 11–16). The two rejects live under a separate heading,
   `## Refused entries (reason and flip)` (line 32; rows at lines 34–41 and 42–47). See the
   direct answer below.
3. **Candidates considered — not stated as a set.** The lesson enumerates four candidate
   entries: two admitted (`corpus/knowledge/canonical-selection.md`, `…/crawler-identity.md`,
   lines 20–26) and two refused (`…/engine-crawl-contracts.md`, `…/crux-eligibility-route.md`,
   lines 34–47). Nothing declares that four is the full candidate set, and `## Gate` (6–16)
   does not carry the candidate list at all. The contract word is "candidates considered"
   inside Gate.
4. **Old→new change log for `status` and `used-by` — absent** (`CORPUS.md:117`). Line 51–58
   records only the `recheck` normalisation, and even that as prose ("the admitted rows carry
   the normalized `180d` cadence") plus the staged cell verbatim; `opened` (campaign
   `2026-10-23` → `2026-10-24` in prior rounds' practice) is likewise unlogged. The committed
   rows (`corpus/SOURCES.md:152-153`) carry final values only: `mined | 2026-10-24 | 180d |
   corpus/knowledge/{canonical-selection,crawler-identity}.md`. No "status old … to new" and
   no "used-by old … to new" sentence exists in the lesson.
5. **Three trend verdicts — absent.** No `expansion:`/`quality:`/`discernment:` line in the
   file, and no verifier-spotcheck companion to carry them. Required every round
   (`LEARNING.md:26`).

### Present and non-empty (no empty sections)

Every heading has a non-empty body; no heading is immediately followed by another heading, and
the file ends mid-content at line 116 (`the count is reported as it stands.`). **Empty
sections: none.**

- `## Gate` (6) — non-empty but incomplete: 2 of its 4 required parts present (admitted rows;
  per-row URL/access date/quote/location), 2 absent (rejects with reasons inside Gate;
  spot-check result).
- `## Admitted entries` (18) — 2 entries, lines 20–26, plus coverage-map claim 28–30.
- `## Refused entries (reason and flip)` (32) — 2 rejects with `Reason:` and `Flip:`, lines
  34–41 and 42–47.
- `## Stripped staged prose` (49) — lines 50–58.
- `## Id collision check` (60) — lines 61–67.
- `## Quarantine` (69) — lines 70–74.
- `## Mistakes` (76) — 5 rows, lines 78–89, 90–96, 97–102, 103–109, 110–116; each carries
  `class`, `evidence`, `captured-by`, `fix`.

## Direct answer: does `## Gate` carry ≥1 admit and ≥1 reject with reason and flip?

- **Admit: yes.** Two, at lines 8–9 (`- S262 …`, `- S263 …`), each with URL, `accessed
  2026-10-24`, section anchor + doc revision, and a quoted span. Word counts 10 and 9 — inside
  the ≤25-word bound of `CORPUS.md:113-114`.
- **Reject with reason and flip, inside `## Gate`: no.** Zero rejects in 6–16.
- **Reject with reason and flip, file-wide: yes.** `## Refused entries (reason and flip)`,
  lines 34–41 (reason: S137 duplicate URL → census E04, plus un-opened Baidu sources; flip:
  open both Baidu pages, cite own S137) and 42–47 (reason: covered ground, held
  `field-performance-cwv.md` S038/S039; flip: supersede the held entry in place). So the
  substance the assignment asks about exists, but the contract places it in `## Gate` and the
  lesson places it under a sibling heading.

## Freshness re-derivation (my judged axis)

Read-only checks, all reproducible from committed bytes plus the on-disk retained bodies:

- Retained bodies reproduce the lesson's line 8–9 pins exactly:
  `sha256sum .ufo/waves/round-51/sources/S262.html` →
  `792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b`, `174926` bytes;
  `S263.html` → `6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de`,
  `175561` bytes. Both match lesson lines 8–9 and `.ufo/waves/round-51/sources/receipts.json`
  (`httpStatus` 200, `bytes == declaredBytes`).
- `receipts.json` `fetchedAt` is `2026-10-24T23:16:49-03:00`, matching the lesson's "2026-10-24,
  23:16 -03:00" (line 11).
- `python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768c…` re-run:
  `C2 quote-truth 8/8 met=True`, exit 0; `C5_gate_quote_truth pass` — the two Gate quotes are
  raw substrings of the retained bodies (so Gate lines 8–9 are load-bearing for C2).
- The lesson's claim that every non-Gate quote is class-marked holds: `canonical-selection.md`
  lines 17, 24, 30, 42, 44, 47 and `crawler-identity.md` lines 12, 19, 24 all carry
  `(collapsed-only quote…)`, matching line 13–16's "each entry marks the class of every other
  quote it carries".
- Row cadence: `opened 2026-10-24`, `recheck 180d` → next re-verification due 2027-04-22;
  doc revisions `2026-08-20` (S262) and `2026-02-03` (S263) both predate the access date.
- Header prose (lines 3–4) resolves: `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`
  lines 89–90 set `waveMinLanes: 32`, `waveMaxLanes: 64`, and 48 sits inside that band. The
  cited path is fleet-root-relative; it does not exist under the lane root
  (`ls scripts/hyaku/` in the lane: no such directory), same convention as prior lessons'
  `scripts/hyaku/jj-lane.sh` citations.

## Attack surface / repair constraints

1. **C2 is coupled to the Gate shape.** `c51_quote_truth.py:103-117` (`gate_quote`) sets
   `in_gate` only while the heading is exactly `## Gate` and matches bullets by
   `line.strip().startswith(f"- {sid} ")`, taking the last quoted string on the line. A repair
   that retitles `## Gate`, moves the two row bullets into a reject/admit sub-list with a
   different prefix, or appends a trailing quoted phrase to those bullets would break
   `C5_gate_quote_truth` and drop C2 below 8/8. Adding rejects and the spot-check to Gate is
   safe only if lines 8–9 stay bullet-prefixed and keep their single trailing quote.
2. **Unverifiable forward reference.** Line 107 names
   `.ufo/waves/round-51/round-time-accounting.json` as the L3 evidence; that file is absent
   (`ls` → no such file). This is the expected pre-settlement state (C1 is 0/3 at dispatch and
   the L1 writes wave evidence after settlement), but at revision `9d13768` the sentence has no
   committed backing and C2 does not test it.
3. **`## Mistakes` class vocabulary drift.** The five class labels are free prose
   ("staged quote mis-transcribed as a source quote", "a wave's seat-report count stated in
   prose and not re-derivable", "a route substitution recorded in prose only", "no aggregate
   round-overrun figure derivable", "inherited artifacts swept to make a count look clean").
   None uses the `mistakes.md` §5 token (`vacuous`, `survivor`, `stale-premise`,
   `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`, `provider`) that
   `CORPUS.md:174-175` requires. Fields themselves are complete on all five rows.

## Limits

- This seat judges lesson shape and the freshness provenance of the Gate rows; it did not
  re-fetch either URL (no network access performed) and did not score C1 (0/3 at dispatch, by
  design) or recompute the wave ledger.
- No authoritative outside spot-check exists in the tree for round 51 to compare the gate
  against; the absence in finding 1 is a missing-record finding, not a disagreement.
