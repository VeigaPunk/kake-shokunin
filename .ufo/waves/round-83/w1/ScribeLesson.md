# ScribeLesson — round 83 wave w1

Seat scope: author `corpus/lessons/round-83.md` — the round's lesson and C1's row file. That is the
only production file this seat wrote. Nothing else in the lane was touched, no VCS command that
mutates state was run, and no network call was made (this seat's item names no URL).

Base read: `826b0061f233ce1dffb9bd6874abc1342a864247`. Freeze read: `64b71992` (contract, both
counters, the classifier, the junk and control-pair builders, base and control receipts). The lesson
names both, and it names the wave shape the contract freezes: one v1 wave, 14 seats, requested attack
share 5/14 = 35.7 %, axes `calibration` (C1, 2) and `freshness` (C2, 10, held).

## Commands and exit codes

| # | Command (cwd `/home/vgpnk/Projects/shokunin/kake-shokunin` unless stated) | Exit |
|---|---|---|
| 1 | `git log --format='%H %ad %s' -- .ufo/reports/round-81/kake.md` (fleet repo) | 0 |
| 2 | `git -C /home/vgpnk/Projects/shokunin diff cb02b705 7678247a -- .ufo/reports/round-81/kake.md` | 0 |
| 3 | `sed -n '120,260p' .ufo/waves/round-83/c83_defect_queue.py` (read the six evaluators) | 0 |
| 4 | `sed -n '285,460p' .ufo/waves/round-83/c83_defect_queue.py` (read `line_with`, `write_fixture`, selftest) | 0 |
| 5 | `sed -n '320,450p' .ufo/waves/round-83/c83_drift_class.py` (selftest, `parents[3] / TOOL`) | 0 |
| 6 | shallow copy of the frozen counter under `<scratch>/shallow/.ufo/waves/round-83/`, `--selftest` | 1 |
| 7 | same bytes at `<scratch>/fixed/.ufo/waves/round-83/` with the tool under `<scratch>/fixed/scripts/`, `--selftest` | 0 |
| 8 | mutated copy (`tool_offline` conjunct dropped from `met`), fixed layout, `--selftest` | 1 |
| 9 | `sha256sum .ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` | 0 |
| 10 | `awk 'NR>=583 && NR<=585' …/rfc9111.txt` and the three other cited spans | 0 |
| 11 | `python3 -B .ufo/waves/round-83/killers/run_killers.py --check` | 0 |
| 12 | `python3 -B .ufo/waves/round-83/c83_defect_queue.py --root $L --fleet …` (worktree, after writing the lesson) | 1 |
| 13 | same counter again after the last edits | 1 |
| 14 | `python3 -B <scratch>/verify_rows.py` (imports the frozen counter's own `line_with` and `git`) | 0 |
| 15 | `python3 -B <scratch>/quote_check.py` (whitespace-normalized substring test, Gate quotes) | 0 |

Rows 6–8, 14 and 15 ran entirely under `/fast/scratch/hyaku/kake-r83/ScribeLesson/`, which was
removed after the receipts were copied into `w1/ScribeLesson/`: the scripts are not retained, the
outputs are, and the three harness runs are re-runnable from the command forms above on any copy of
the frozen files.

## What the file carries

Section order is exactly the item's: title, opening paragraph, `## Claims`, `## Corrections`
(`D1`…`D6`, one physical line each), `## Erratum`, `## Gate`, `## Mistakes`, `## Dead seats`,
`## Wave`; `## Verdict` closes it. 255 lines, 20,057 bytes.

`## Corrections` carries the tokens the contract requires, each verified by importing the frozen
counter's own matcher rather than by reading:

    D1 MATCH ['0/7', 'settled_attack=']                     D4 MATCH ['7678247a', 'erratum']
    D2 MATCH ['UTF-8', 'w1-accounting.json']                D5 MATCH ['distinguished=5/5', 'C1-m3',
    D3 MATCH ['after-c83-instrument-check.txt', '--check']      'C1-m5', 'C2-m2', 'C2-m4', 'C2-m5']
    D6 MATCH ['§Gate', 'corpus/QUALITY.md']                 ROW_CONJUNCTS PASS   exit 0

The D4 predicate was re-run the same way: fleet history for `.ufo/reports/round-81/kake.md` has
`7678247a` on top with `cb02b705` beneath, the diff removes 5 lines longer than 40 characters, and
**5 of 5** are raw substrings of the lesson (need ≥ 4). `.ufo/waves/round-83/w1/ScribeLesson/row-conjuncts.txt`.

## Findings

1. **C1 reads `open=2 closed=4` at this writing** (`C1v1 revision=worktree items=6 open=2 closed=4
   met=false`, exit 1, 2026-11-04T13:36:45Z). `D3`, `D5` and `D6` close from their own files — the
   instrument receipt prints `C2v1 revision=64b71992… population=30 bound=30 mismatches=0 met=true`;
   the killer suite prints `distinguished=5/5` with four `killed` rows and `C2-m5 equivalent` carrying
   guard line `c82_capture_delta.py:239`; `corpus/QUALITY.md:1701` carries the Gate-provenance
   criterion. `D1` and `D2` read `open spec or results absent/unreadable` because their state
   conjuncts need `w1-results.json` and `w1-accounting.json`, which WAVE-DONE produces. The lesson
   states this measured state rather than claiming the closure.
2. **The round-82 probe defect reproduces on this round's files, and so does its fix.** The unmodified
   `c83_drift_class.py` at three levels under the scratch root exits 1 with `FAIL no tool at
   …/shallow/scripts/header_change_class.py` before any fixture runs; the identical bytes with the
   tool under `scripts/` print `selftest: 9/9 passed`, exit 0; and the same file with `tool_offline`
   dropped from `met` prints `FAIL tool-network-import — met=True expect=False`, `selftest: 8/9
   passed`, exit 1. That is the `## Mistakes` row's "fix shown able to fail" evidence and it was
   observed, not asserted. `.ufo/waves/round-83/w1/ScribeLesson/harness-path-repro.txt` (three runs,
   exits 1/0/1).
3. **The D3 receipt discloses a non-fatal mismatch rather than hiding it**: `revision_match=false`
   because the committed receipt pins subject `70c8241b`, an ancestor of the measured carrier. The
   lesson's D3 row names it; `w1/ExecInstrument.md` explains it. This is a disclosure, not a defect I
   found independently.
4. **The Gate is honest about being unresolved.** `corpus/knowledge/header-change-classes.md` landed
   citing `S456` and the retained bytes, but `grep -n 'S456' corpus/SOURCES.md` returned no match at
   this writing, so `## Gate` records a candidate with a pending registry row, not an admission. Its
   four quoted spans were checked as whitespace-normalized substrings of the retained file (word
   counts 14 / 23 / 21 / 48) and the retained digest recomputes to
   `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` at 84,477 bytes
   (`w1/ScribeLesson/gate-quote-check.txt`, exit 0). The 65-word and ETag anchors are rejected with
   reasons, not omitted.
5. **`## Dead seats` and `## Wave` are placeholders with no invented rows.** No seat result and no
   byte count is stated anywhere in the lesson; both tables carry `<<…>>` markers for the L1.

## Limits

- The lesson is author-side. `D1`/`D2` cannot be closed by this file; they close when WAVE-DONE writes
  the results and accounting records and the counter re-derives them. My measured note can only go
  stale in the direction of turning green, and the after receipt is the reading of record.
- The D4 row depends on fleet history: the counter takes the two most recent commits touching
  `.ufo/reports/round-81/kake.md`. It read `7678247a` over `cb02b705` at 13:36Z. A later fleet commit
  to that file would move the pair; I did not write to the fleet repo.
- `C2-m5` is an `equivalent` mutant, not a kill. The contract allows it only with the guarding source
  line and a one-line proof; both are printed. I record it as equivalence, not as a kill.
- No tool was installed or upgraded; no scratch tree survives (removed after the receipts were copied).

## Verdict

**Delivered.** `corpus/lessons/round-83.md` exists with the required section order, all six C1 row
conjuncts match under the frozen counter's own matcher (exit 0), the D4 erratum quotes 5 of 5 removed
lines verbatim (need ≥ 4), and the Gate's four spans verify against the retained RFC 9111 bytes. C1
itself is **not** closed by this seat: it reads `open=2 closed=4` pending the WAVE-DONE records, and
that is what the lesson says.
