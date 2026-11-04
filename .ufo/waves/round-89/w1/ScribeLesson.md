# ScribeLesson — round 89, wave 1 (scoped findings)

Seat: `ScribeLesson` (scribe, leaf member, no subagent dispatch). Lane
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Draft lesson:
`.ufo/waves/round-89/w1/ScribeLesson/round-89.md`. No production file, commit,
push, or mutating git/jj command was run. The lane's integrated
`corpus/lessons/round-89.md` (L1's) was read, not edited.

## Verdicts on the two claims (measured, not admitted)

- **C1 calibration, six routed defects.** At lane HEAD `acc69ba5`:
  `items=6 open=1 closed=5 met=false`, exit 1. Item A (stale `22/22` selftest
  number) is the only open item: `SCORECARD.md:5469`, `SCORECARD.md:5488` and
  `corpus/lessons/round-88.md:265` carry the stale count with no `[r89-correction`
  tag. The counter's do-nothing control (`open=6`) does not reproduce at base:
  this seat measured `76225160` as `open=5 closed=1`, because item E reads the
  checked-out HEAD rather than `--revision` (defect D1 below).
- **C2 freshness, bounded capability.** Integrated candidate `9784ad54` scores
  `frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true` under both the
  frozen v1 counter and the committed v2 counter, exit 0. Base is
  `frozen=0/16 props=0/200 refuse=0/9 met=false`, exit 1. The predicate is
  satisfied, but the counter also admits shortcut and non-conforming
  constructors (defects C2-1 to C2-4 below), so this seat does not treat
  `met=true` as conformance.

## Commands and exits (this seat)

| Command (lane-relative; `--work` under scratch) | Output (verbatim) | Exit |
|---|---|---|
| `c89_defect_queue.py --revision 76225160…` | `items=6 open=5 closed=1 met=false` | 1 |
| `c89_defect_queue.py --revision 2e700b9a…` | `items=6 open=5 closed=1 met=false` | 1 |
| `c89_defect_queue.py --revision 2177058662…` | `items=6 open=5 closed=1 met=false` | 1 |
| `c89_defect_queue.py --revision acc69ba5…` | `items=6 open=1 closed=5 met=false` | 1 |
| `c89_defect_queue.py --selftest` | `selftest: 12/12 passed` | 0 |
| `c89_key.py --root . --revision 76225160… --candidate scripts/cache_key.py` | `frozen=0/16 props=0/200 refuse=0/9 controls=5/5 met=false (candidate absent)` | 1 |
| `c89_key.py --revision 9784ad54…` (v1 counter from `08ab46a1`, and v2 committed) | `frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true` | 0 (both) |
| `c89_key.py --selftest` (lane, controls beside it) | `selftest: 43/43 passed` | 0 |
| `c89_key.py --selftest` (counter file alone, no `controls/`) | `selftest: 40/43 passed` (3 FAIL: controls and oracle-import and case-table guards) | 1 |
| `c88_defect_queue.py --revision edcb2980…` | `items=3 open=0 closed=3 met=true` | 0 |
| `c88_vary.py --revision edcb2980…` | `frozen=20/20 random=200/200 met=true` | 0 |
| `scripts/vary_match.py --selftest` at HEAD (sha256 bytes from `git show`) | `selftest: 35/35 passed` | 0 |
| `git log` / `merge-base --is-ancestor` on dispatch and freeze v2 | dispatch `2e700b9a` (18:13:04 -0300) precedes freeze v2 `46a43e94` (18:16:18 -0300) | — |
| `curl -sS` `https://www.rfc-editor.org/rfc/rfc9111.txt` and `rfc9110.txt` | HTTP/2 200; 84 477 B and 502 941 B; sha256 equal to round-88 retained copies | 0 |
| counter probes `probes/probe_all.py`, `probe_1d.py`, `probe_collision.py` | see defect list; full JSON `receipts/probes-c2.json` | 0 |

Receipts are copied into `.ufo/waves/round-89/w1/ScribeLesson/receipts/`
(RFC bodies and headers, C1 and C2 outputs, probes JSON). Probe scripts are in
`.ufo/waves/round-89/w1/ScribeLesson/probes/`.

## Defects found (lane-internal; routed, not repaired)

**In the round's counters and contract (C1 and C2):**

1. **C1 item E reads HEAD, not `--revision` (RC-1, re-confirmed).** Base
   `76225160` prints `open=5`, not the predicate's `open=6`. The committed
   `controls/base-c1.txt` is not a pure base measurement.
2. **C1 item E is blind to the post-dispatch amendment (RC-2, re-confirmed).**
   `c89_key.py` was amended by `46a43e94` at 18:16:18 -0300, after dispatch
   `2e700b9a` at 18:13:04 -0300. Item E only checks the first add of each file.
   This is the R88-E class recurring in round 89.
3. **C1 item A cannot accept an appended correction.** It stays open on three
   stale round-88 lines; the append-only rule forbids editing them in place.
4. **C2 counter admits a table over its own seed population (met=true).** The
   seed `SEED = 89089` is a committed constant; a table of 421 entries built
   from `_props(random.Random(89089))` plus frozen cases and refusals scores
   `16/200/9`, guard null (`probe_all.py` case E). Round-88 R88-1 already named
   this class; round 89's freeze text says the population is generated at scoring
   time, which does not prevent a table built from the public seed.
5. **C2 textual guard accepts a runtime-built import of the committed reference.**
   Case D (`probe_all.py`) builds the module path at run time; the guard returns
   null; the candidate scores `16/200/9`.
6. **C2 counter misses the URI-escape clause.** Removing `_esc(uri)` scores
   `16/200/9`, and the mutant collides two distinct logical requests (R1 and R2
   in `probe_collision.py`). The canonical constructor keeps them apart.
7. **C2 counter misses the `%1D` escape clause.** Omitting the `%1D` entry in
   the escape table scores `16/200/9`. No frozen case or property contains
   U+001D (`probe_1d.py`).
8. **C2 counter misses the OWS set.** Trimming VT and FF and LF and CR as well as
   SP and HTAB scores `16/200/9`, though the contract names SP and HTAB only
   (case C).
9. **C2 selftest depends on a sibling `controls/` directory.** The counter file
   alone prints `40/43` and exits 1.

**In the round-88 defect set (R88-A…F), as this seat observed them:**

- R88-A (stale `22/22`): open at HEAD (defect 3 above).
- R88-B (Gate summary): closed. Round-88 `## Gate` parses `admits=2 rejects=2`
  at base and at HEAD; the tagged correction at `corpus/lessons/round-88.md`
  lines 334–337 is present. The selftest mutant "Gate table edit reopens B" is
  green (12/12), so the item does redden a changed table.
- R88-C (unbacked re-run claim): the claim's number reproduces at `edcb2980`
  (`controls` receipts `r88-c1-at-edcb2980.txt`, `r88-c2-at-edcb2980.txt`, both
  uncommitted in this seat's wave directory), but no committed receipt names
  `edcb2980`. The lesson's `r88-c-rerun:` marker is a placeholder for L1.
- R88-D (unpinned count): the lesson pins `controls-count: 1604@2177058662d8778f1d1a685613f57deccb51ef01`,
  re-counted by this seat. The round-88 count `1,577` is exact at `f60a852a` and
  `1,590` at `76225160`; the lane's HEAD is now `1,609`.
- R88-E (freeze after dispatch): recurs (defect 2).
- R88-F (lesson shape): closed. `## Mistakes` carries the five columns in the
  draft; round-88 line 329 carries a tagged pointer.

## Routing for L1 (not applied by this seat)

- L1 must replace the `r88-c-rerun:` placeholder in `round-89.md` with a committed
  receipt path, or `retracted`. Item C reads it at the revision.
- L1's integrated lesson (`corpus/lessons/round-89.md`) states the base do-nothing
  control as `open=6`. This seat measured `open=5` at the same base; the lesson's
  claim should be corrected or the counter repaired (defect 1).
- Items 1–9 above are round-90 routing candidates. Any change to a frozen claim
  needs an explicit claim decision by L1, not a silent edit.

## Tools

No tool was installed or upgraded. Present and used: `curl 8.23.0` (system) and
`Python 3.14.8`. PACMAN was not touched.

## Scratch and writes

Scratch: `/fast/scratch/hyaku/kake-r89/ScribeLesson/` (one directory, no clone).
It is deleted before this report is yielded; the cited receipts were copied to
`.ufo/waves/round-89/w1/ScribeLesson/receipts/` first. No file was written under
`/tmp`. Writes made: `.ufo/waves/round-89/w1/ScribeLesson/` (draft, receipts,
probes) and this report. Nothing else.

## Unresolved

- No storability, freshness, revalidation, reuse or serving claim is made.
- Peer seats' evidence (ReviewCounterC1/C2, CriticClaims, ExecControls, ExecKey)
  is cited only where the lane's own round-89 lesson already cites it; this seat
  did not re-run those seats' sweeps.
- The round-89 lesson draft's `r88-c-rerun` marker is intentionally not filled.
