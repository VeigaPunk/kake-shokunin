# Round 89 — round-88 routed defects, C1 closure record

Base `76225160d0dff8d2042fbcd037bd08b0971d5e07`. Freeze commit `08ab46a1` (first
adds `.ufo/waves/round-89/c89_key.py`; committer time `1793826745`) precedes the
dispatch commit `2e700b9a` (first adds `.ufo/waves/round-89/w1.ready`; committer
time `1793826784`). Freeze is an ancestor of dispatch, so the round-88 R88-E
order holds for this round.

This file carries the C1 record: the six routed round-88 defects, each closed by
an edit to committed bytes and each re-derivable by a command. The C2 section and
the round-level verdicts are added by the integrating agent.

## C1 — routed round-88 defects (calibration, lowest owned axis, 2 HOLD)

Predicate (frozen in `.ufo/waves/round-89/freeze.md`): `C1v1 ... items=6 open=0
closed=6 met=true`, exit 0 at the carrier. Base receipt
`.ufo/waves/round-89/controls/base-c1.txt`: `open=6 closed=0 met=false`, exit 1.

Counting command: `TMPDIR=$(mktemp -d) python3 -B .ufo/waves/round-89/c89_defect_queue.py --root . --revision <REV> --work "$TMPDIR/work"`.

Closures, one per routed defect (`corpus/lessons/round-88-verifier-spotcheck.md`,
section "Routed defects"):

- **R88-A, stale integrated-selftest number.** The receipt
  `.ufo/waves/round-88/controls/integrated-selftests.txt` prints
  `selftest: 35/35 passed`, not `22/22`. Each stale line in the round-88 section
  and move-log of `SCORECARD.md`, and line 265 of `corpus/lessons/round-88.md`,
  carries an `[r89-correction …]` tag. The round-89 section of `SCORECARD.md`
  states `integrated-selftest: 35/35`.
- **R88-B, Gate sample counts.** The round-88 `## Gate` table carries two
  `**admit**` decisions and two `**reject**` decisions, not one admit and three
  rejects. The round-88 report's Gate summary (cited by the outside spot-check)
  is corrected by the marker below; the report bytes are not rewritten.
- **R88-C, unbacked re-run claim.** The sentence "re-run at `edcb2980`" has no
  committed receipt and its `--work` path is under `/fast/scratch`. It is
  retracted below; no receipt is cited for it.
- **R88-D, unpinned count.** The round-88 `1,577` count names no revision. It is
  exact at `f60a852a`; at `76225160` the count of tracked paths containing
  `/controls/` is `1590`, pinned below.
- **R88-E, freeze after dispatch.** Closed by commit order, measured on this
  round's own commits: `08ab46a1` is an ancestor of `2e700b9a` with an earlier
  committer time.
- **R88-F, lesson shape.** The four rows of `## L1 mistakes` in round-88 are
  carried as rows of `## Mistakes` below, each with its witness; round-88 points
  here with a tagged line.

Markers read by the counter:

gate-sample: admits=2 rejects=2

r88-gate-summary-correction: admits=2 rejects=2

r88-c-rerun: retracted

controls-count: 1590@76225160d0dff8d2042fbcd037bd08b0971d5e07

## Mistakes

Rows: the three round-88 routed defects with a mechanical witness, and the four
round-88 L1 mistakes (`corpus/lessons/round-88.md` `## L1 mistakes`), carried
here with the witness that would redden each fix. Rows with "manual" have no
counter; the witness is a re-read named in the row.

| Class | Evidence pointer | Captured-by criterion | Fix | Fix can fail — the witness that reddens it |
|---|---|---|---|---|
| Stale integrated-selftest count (R88-A) | `corpus/lessons/round-88.md:265`; `SCORECARD.md` round-88 section (two stale lines); `.ufo/waves/round-88/controls/integrated-selftests.txt` prints 35/35 | outside spot-check; C1 item A | tagged correction on each stale line; `integrated-selftest: 35/35` marker | an untagged `22/22` left in either file, or a marker that differs from the tool's printed count |
| Gate summary miscount (R88-B) | round-88 report Gate summary "one admit and three rejects"; `corpus/lessons/round-88.md` `## Gate` carries 2 admit and 2 reject | outside spot-check; C1 item B | `gate-sample` and `r88-gate-summary-correction` markers with the parsed counts | any edit to a `## Gate` decision cell that changes the parsed counts while the markers stay |
| Unbacked re-run claim (R88-C) | "re-run at `edcb2980`" in the round-88 report and spot-check; no committed receipt | outside spot-check; C1 item C | `r88-c-rerun: retracted` | a `receipt=` value naming a path absent at the revision, or a `r88-c-rerun` marker that is missing or duplicated |
| Unpinned controls count (R88-D) | `1,577` named with no revision in the round-88 report | outside spot-check; C1 item D | `controls-count: 1590@76225160…` | a count that differs from `git ls-tree -r --name-only 76225160 \| grep -c '/controls/'` |
| Freeze after dispatch (R88-E) | v3 `52e41d2d` landed 15:58:05, after dispatch 15:52:15 in round 88 | outside spot-check; C1 item E | this round's freeze `08ab46a1` precedes dispatch `2e700b9a` | dispatch committed before the freeze, or the two in one commit |
| Lesson shape (R88-F) | round-88 `## L1 mistakes` heading with no `## Mistakes` section for the round | outside spot-check; C1 item F | `## Mistakes` table with the five columns below, plus the tagged pointer in round-88 | removal of `## Mistakes`, a missing column, or the round-88 pointer line |
| Mid-write candidate scored (round-88 L1 mistake 1) | round-88 `## L1 mistakes` row 1: a tally read at 16:02 while the seat was live | L1 in `proc://` | score only after the results file names the seat | manual: a receipt whose revision predates the seat's results file |
| Subject copied from previous round (round-88 L1 mistake 2) | round-88 `## L1 mistakes` row 2: `add7e49b` says twelve seats for fourteen | report assembly | subjects written from the current wave's counts | manual: a commit subject whose seat count differs from `w1-spec.json` |
| Freeze amended while live (round-88 L1 mistake 3) | round-88 `## L1 mistakes` row 3: `52e41d2d` moved three seeded labels | seats `ScribeLedger`, `ScribeLesson` | freeze before dispatch, or dispatch after freeze, never interleaved | C1 item E on this round's commits |
| LF-accepting fallback (round-88 L1 mistake 4) | round-88 `## L1 mistakes` row 4: `w1/L1/vary_match.py:22` regex accepted `Vary: "*\n"` | `ReviewReader` §4b | fallback not shipped; integrated tool refuses LF | the integrated tool's selftest must refuse a trailing-LF member; manual until the C2 section |
