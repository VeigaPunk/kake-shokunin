# ScoutQuarantine

Scratch: /fast/scratch/hyaku/kake-r58/ScoutQuarantine (receipts below are copied inline; scratch deleted at end). Lane HEAD read: cc8da1674d6e (read-only). No lane write except this file.

## SLICE:
- Command re-run verbatim from round prompt §10 (`awk -F'|' -v l='kake' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'` over
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md), read-only.
- Result: 12 rows; `cmp` against `.ufo/waves/round-58/assimilation/quarantine-slice` = byte-identical (exit 0). Also the same file name/shape as round-57's slice.
- Rows (id, register class cell): S142 S143 S148 S156 S161 S193 S194 S195 S206 = `payload-absent`; S154 S178 S184 = "the cited source could not be fetched, so no quote was checked".
- Slice ids are in neither the lane registry (`reg-ids`, 160 ids; lane S1xx ids stop at S139, so no S142-S206 row) nor `staged-ids`: `comm -12` of slice ids against each = 0 lines. [Observation only; not a defect claim.]
- Round-57 verdicts (corpus/lessons/round-57.md § Assimilation; all 12 appear in it; none adopted, register/campaign files not edited):
  - S142 VERIFIED (claim on page; registered quote lacks the page's trailing clause = quote-form defect, truncated)
  - S143 VERIFIED (table row; registered quote a flattened join of cells = quote-form defect)
  - S148 ABSENT as registered (sentence only in a %-commented line of the e-print source; true absence)
  - S154 VERIFIED (CrUX endpoint 403 PERMISSION_DENIED body, POST; checker-payload defect)
  - S156 VERIFIED (a response header, not in HTML body; stable across two requests; method defect)
  - S161 VERIFIED (same document as held S274: duplicate-URL row if appended; method defect)
  - S178 VERIFIED (PageSpeed 429 RESOURCE_EXHAUSTED body; method defect)
  - S184 VERIFIED (CrUX 403 PERMISSION_DENIED body, POST; checker-payload defect)
  - S193 VERIFIED (own-work prose present in the lane's own cited files; not a source quote)
  - S194 VERIFIED (same as S193)
  - S195 VERIFIED (same as S193)
  - S206 ABSENT as registered (artifact reads `S187-S193`, register `S187-S199`: one-token misquote, substance verified)
  Tally: 10 VERIFIED, 2 ABSENT. Lesson's class split: 8 checker-payload/method (S154 S184 S178 S156 S161 S193 S194 S195), 2 quote-form (S142 S143), 2 true absence (S148 S206).
  Per-row grep count of each id in round-57.md lesson: 2 2 3 3 2 2 2 3 3 2 2 2 (all >= 1).

## ADOPTION CHECK:
- S395 in slice: no (0 hits). S378 in slice: no (0 hits).
- This round's adopted rows S423 (= staged S395, by document) and S424: not in slice (0 hits for S423/S424; slice ids are S142-S206 only).
- Staged S395 and S378 each present exactly once in `staged-ids` (S378 is the rejected candidate per contract.md l.85; S395 adopted as S423). Neither is a registry id (no collision).
- Contract.md l.84 claim "neither S395 nor S378 among them; nothing from the slice is adopted" = CONFIRMED.
- The slice is not adopted this round: no slice id appears as an adopted/renumbered row in contract.md (rows listed: S423, S424 only) [checked contract lines 65-66, 83-85 only; S424's staged source id was not looked up here].

## COLLISIONS:
- Pattern: `^ {0,3}\|[[:space:]]*S[0-9]{3,}` (0-3 leading spaces) over lane corpus/SOURCES.md and shokuknow merge/kake/SOURCES.append.md.
- reg-ids 160, staged-ids 129, `comm -12` = 8: S312 S329 S367 S372 S373 S374 S390 S409. Matches round-57's list.
- `cmp` of my reg-ids, staged-ids, collisions against `.ufo/waves/round-58/assimilation/{reg-ids,staged-ids,collisions}`: all identical.
- Registry top ids: ... S420 S421 S422 (S422 last). S423 and S424: 0 matches in reg-ids; `grep -nE 'S42[34]' corpus/SOURCES.md` = no output; 0 rows with 0-3-space pattern. Both unused. Neither collides with staged ids (S395/S378 not in collisions).
- Not run: guard-proof fixture (indented-row proof) — outside assignment.

VERDICT: slice re-derived byte-identical (12 rows), S395/S378/S423/S424 absent from it, 8 collisions confirmed (same ids), S423/S424 unused in lane registry.
