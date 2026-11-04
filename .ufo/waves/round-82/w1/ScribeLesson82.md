# ScribeLesson82 — round 82 wave w1

Seat: scribe, leaf (no subagent dispatch). Write scope used: `corpus/lessons/round-82.md` (the
only production file) plus this report and `.ufo/waves/round-82/w1/ScribeLesson82/`. No VCS
mutation, no network, no tool install, nothing written in the fleet repo or a sibling lane.

## What landed

`corpus/lessons/round-82.md` (207 lines) with the required sections in order — opening paragraph
(base `419866015b1f58e01f061cde9a77d490653d3c76`, freeze
`082b7dd39053e5f96ca6c463da47a3e4d83d4580`, one v1 wave, 13 seats, both claim axes), `## Claims`
(C1 and C2 in the contract's words, predicates and counting commands, marked author-side),
`## Corrections` (one single-line row for each of `D1` … `D8`), `## Gate` (S455 admit with URL,
access date and a 24-word raw-substring quote; one reject), `## Mistakes` (three rows, each fix
naming a check that can fail), `## Limits`, and `## Settlement` naming the two items that were
still absent at write time.

## Commands run, with exit codes

| command | exit | receipt |
|---|---|---|
| `python3 -B .ufo/waves/round-82/c82_defect_queue.py --root . --work <scratch>/probe` | 1 (`items=8 open=1 closed=7 met=false`) | `ScribeLesson82/counter-probe.txt` |
| `…/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` | 0 (`W04=22`, `ok` on the lane file) | `ScribeLesson82/census.txt` |
| `git -C /home/vgpnk/Projects/shokunin rev-parse 7678247a 7678247a^` | 0 | `ScribeLesson82/d3-blob-pair.txt` |
| `git -C /home/vgpnk/Projects/shokunin diff --stat 7678247a^ 7678247a -- .ufo/reports/round-81/kake.md` | 0 (`12 insertions(+), 5 deletions(-)`) | `ScribeLesson82/d3-blob-pair.txt` |
| quote verification (three retained RFC 9110 copies, three spans, `raw`/line/word count) | 0 | `ScribeLesson82/quote-check.txt` |
| `test -e` on both round-81 dead receipt paths / `test -f` on the live one | 1 / 1 / 0 | transcript below |

Dead/live path probe (D5's state conjunct, re-derived rather than quoted):

```
$ test -e .ufo/waves/round-81/controls/after-c81-defect-queue.txt   # exit=1 (absent)
$ test -e .ufo/waves/round-81/controls/after-c81-capture-audit.txt  # exit=1 (absent)
$ test -f .ufo/waves/round-81/controls/after-c1-final.txt           # exit=0 (present)
```

## Verdict

**The lesson is authored and C1's row conjuncts are satisfied: `D2`–`D8` read closed on both
state and row conjuncts when the frozen counter is run over the worktree; `D1` reads `open`
because the `S433` registry cells had not landed when I wrote, and the counter's summary is
`items=8 open=1 closed=7 met=false`.** No condition was written from memory: `D2`'s token was read
out of `after-c1-final.txt`, `D4`'s integer out of `seat-failures.json`, `D5`'s paths out of `test
-e`/`test -f`, `D6`'s tally out of `c81-selftest-c2.txt`, `D7`'s receipt out of
`controls/after-c1-ledger-gate.txt`, `D8`'s in-lane row out of `corpus/lessons/round-80.md:221`
and `D3`'s commit out of the fleet repo's blob pair.

## Findings (routed, not repaired)

1. **`line_with` is line-scoped — a wrapped row silently loses its conjuncts.** My first draft
   wrapped every correction paragraph at ~92 columns; the probe returned `log=no` for `D1`, `D2`,
   `D3`, `D4`, `D5`, `D7`, `D8` even though each paragraph carried the tokens. `D3` was the
   diagnostic one: it found the line (so `erratum` matched) but read "D3 line names no commit
   token", because the token sat on the following line. Rewriting each row as one physical line
   flipped all seven to `log=yes`/closed. The counter is right and the convention was unstated:
   row conjuncts must be one row, one line. Worth one line in the lesson convention or the
   counter's docstring; I did not edit either.
2. **C2's selftest count reads two ways.** `controls/c82-selftest-c2.txt` ends
   `selftest: 9/9 passed` over nine named fixtures, while the identical-capture control's counter
   line prints `selftest 14/14` (`controls/ctl-c82-identical-capture.txt`), and the contract's
   `selftest_ok` says ">= 12 cases". Both readings are green, but they count different things
   (fixtures vs internal cases) and the contract names one word for both. Routed to the closure;
   the lesson states the predicate and does not adjudicate the count.
3. **`D6`'s row conjunct cannot live in this file.** The contract's row cell points at
   `corpus/QUALITY.md`, and the counter's `item_d6` ignores the lesson argument entirely. It is
   satisfied by `corpus/QUALITY.md:1695` (`22/22`, `supersedes`, `round-81` on one line), which
   `ScribeRecord` owns and landed. My `D6` row records the correction and points at that line; no
   file outside my scope was edited.
4. **`D8`'s fleet half is outside this round's write scope.** The in-lane half landed as the
   appended `[r82-correction 2026-11-04]` row at `corpus/lessons/round-80.md:221` (names
   `corpus/SOURCES.md:200`, says the original is not rewritten); `.ufo/reports/round-80/kake.md`
   still reads `corpus/SOURCES.md:201` at fleet line 158, and the lesson says its erratum rides
   the round-82 report.

## Split ownership observed

| item | row text | state |
|---|---|---|
| D1 | this lesson | `ExecRegistry` (S433 cells) — pending at write time |
| D5 | this lesson | already satisfied (`test -e`/`test -f`) |
| D7 | this lesson | `ExecRegistry` — receipt landed green before I wrote |
| D6 | `ScribeRecord` (`QUALITY.md:1695`) | satisfied |
| D8 | `ScribeRecord` (`round-80.md:221`) | satisfied in-lane; fleet report out of scope |
| C2 data | `ExecCapture` / `ExecDelta` | capture B and delta record absent at write time |

## Out of scope, untouched

No publish, deploy, DNS, account or browser action; no socket opened by this seat; no `git`/`jj`
mutation; no `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/QUALITY.md`,
`corpus/SOURCES.md` edit; no tool installed or upgraded (nothing needed); `pacman` untouched.

## Artifacts

- `corpus/lessons/round-82.md`
- `.ufo/waves/round-82/w1/ScribeLesson82.md`
- `.ufo/waves/round-82/w1/ScribeLesson82/counter-probe.txt`
- `.ufo/waves/round-82/w1/ScribeLesson82/census.txt`
- `.ufo/waves/round-82/w1/ScribeLesson82/d3-blob-pair.txt`
- `.ufo/waves/round-82/w1/ScribeLesson82/quote-check.txt`

Scratch `/fast/scratch/hyaku/kake-r82/ScribeLesson82/` removed after the receipts were copied.
