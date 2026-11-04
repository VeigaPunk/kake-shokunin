# ExecCorrections — independent re-implementation of C1 R80-1/R80-2/R80-3

**Verdict:** all three items are decidable from lane bytes; the instrument
`.ufo/waves/round-81/w1/ExecCorrections/verify_corrections.py` re-derives every
expected token itself (registry line 200 for S453, `constants_failed=4/4`,
`47/48`, `const_echo 11/12`, `rfc9110.txt rows=3`, `rfc9110.html rows=3`), kills
all three of its mutants and accepts the green fixture (`met=true`, exit 0).
`corpus/lessons/round-81.md` did not exist when I finished, so the real-lane run
correctly reports `met=false` on `lesson missing`; the synthetic-lesson branch is
covered by the green fixture.

## Files written (write scope)

- `/.ufo/waves/round-81/w1/ExecCorrections/verify_corrections.py` — production target.
- `/.ufo/waves/round-81/w1/ExecCorrections/run-{green,mutant-line,mutant-arith,mutant-count,real-lane}.txt` — verbatim run transcripts with exit codes.
- This report. Nothing else in the lane was touched; no edits to `c81_defect_queue.py` or any receipt.

## The three numbers, derived independently (not from the counter)

Derived from `git show 2e11925500dd5a739376c9108c94616243af0cd4:corpus/SOURCES.md`
and the working tree — `git diff --stat` base→worktree on `corpus/SOURCES.md` and
`.ufo/waves/round-80/controls/ctl-c80-constants.txt` was empty (identical bytes),
so base-revision and worktree derivations agree:

1. **S453 registry line L = 200.** `corpus/SOURCES.md:200` is the row whose id
   cell is exactly `S453` (row: "RFC 9110: HTTP Semantics, §5.6.7 Date/Time
   Formats — https://www.rfc-editor.org/rfc/rfc9110.txt"). Same at base revision
   and working tree. Registry parses to 191 `S*` rows.
2. **Constants receipt arithmetic** (`.ufo/waves/round-80/controls/ctl-c80-constants.txt`):
   per-const rows `const_all.py 12/12`, `const_clean.py 12/12`, `const_echo.py 11/12`,
   `const_regex.py 12/12` → summed failures/slots **47/48**; ctl summary
   **`constants_failed=4/4`**; echo row → **`const_echo 11/12`**.
3. **rfc9110 source-cell census:** **`rfc9110.txt rows=3`** (S028 L36, S033 L41,
   S453 L200), **`rfc9110.html rows=3`** (S010 L18, S088 L96, S433 L179). Same at
   base revision (independent awk pass over the extracted blob).

## Token contract enforced by the instrument (exact substrings, one lesson line each)

- `R80-1` line must contain `R80-1`, `S453`, and `corpus/SOURCES.md:200`.
- `R80-2` line must contain `R80-2`, `constants_failed=4/4`, `47/48`, `const_echo 11/12`.
- `R80-3` line must contain `R80-3`, `rfc9110.txt rows=3`, `rfc9110.html rows=3`.

Note for the scribe: the contract gives literal labels for the R80-2 tokens 1 and 3
but token 2 is "the summed case-level failures `<n>/<slots>`" with no label, so the
bare fraction `47/48` must appear verbatim; and `const_echo.py 11/12` does **not**
contain `const_echo 11/12` — use the label without `.py`.

## Recorded runs (5; transcripts verbatim in receipts, sha256 over each file)

| Receipt | Fixture | Result |
|---|---|---|
| `run-green.txt` `088599cf4d3689a397868004daa005d0efc66aecb2ba89f519755463527d88c3` | scratch fixture lane = base-revision SOURCES.md + real receipt + synthetic lesson from my re-derivation | `met=true`, `exit=0` |
| `run-mutant-line.txt` `854ca67dbed5ffb338657d020712cd9efa7858b33eabee0e7b7688bfcf04cd48` | R80-1 names `corpus/SOURCES.md:201` (wrong line) | R80-1 `closed=false`, `met=false`, `exit=1` |
| `run-mutant-arith.txt` `68b9dad681742e45b7db77976cb01404ffe48e30e2ae45db167463ae84dcb5f9` | R80-2 carries `47/49` (wrong arithmetic) | R80-2 `closed=false`, `met=false`, `exit=1` |
| `run-mutant-count.txt` `8eb07977bb4ef35d7d438d12c5207a8cf951de3015537b8204c269e1a9dc939a` | R80-3 carries `rfc9110.txt rows=4` (wrong count) | R80-3 `closed=false`, `met=false`, `exit=1` |
| `run-real-lane.txt` `b10390ba9b42471ee98cb8fd46c6e4b4168abba53a446d7efe3d949a72b19106` | real lane root, checked twice (start and finish) | `lesson missing`, all three `closed=false`, `met=false`, `exit=1` |

Each mutant opens exactly its own item and leaves the other two closed — the
predicates are isolated, not confounded.

## Decidability verdict per item

- **R80-1: decidable from bytes.** L is a pure function of `corpus/SOURCES.md`
  (stable at 200 today); any insertion above the row reopens the item by design.
  The lesson row must spell the pointer `corpus/SOURCES.md:200` on the same line
  as `R80-1`.
- **R80-2: decidable from bytes.** The receipt parses deterministically; the only
  spec looseness is the unlabeled middle token (resolved here as the bare
  fraction) and the exact `const_echo` spelling. Both are stated above so the
  lesson can be written to satisfy any faithful reader.
- **R80-3: decidable from bytes.** Counts are stable integers (3/3) over source
  cells; the row must carry both literal `rows=n` tokens.

## Process notes

- Independence: `c81_defect_queue.py` was never opened; my instrument is written
  from `.ufo/waves/round-81/contract.md` ("Item conditions (frozen)") alone. If
  the lesson lands later, disagreement = my printed expected tokens vs the lesson
  rows vs the counter's carrier verdict; neither file was edited by me.
- No tool installs (pacman pause respected; nothing needed beyond python3/awk).
- Git usage read-only (`git show`, `git diff --stat`); no mutations anywhere.
- No network GETs (my item names none). Scratch
  `/fast/scratch/hyaku/kake-r81/ExecCorrections/` deleted before yield; receipts
  were written directly under the seat directory in the lane.
