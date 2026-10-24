source: S130 (kama `corpus/knowledge/self-assessment-at-writing.md`, adjacency import) and the round-42 closure routed defect 1 (`corpus/lessons/round-42-verifier-spotcheck.md`)
verified-at: 2026-10-23 (kake round 43) — the r42-stated counts failed re-derivation; the r43-stated counts re-derive from committed bytes
recheck: re-derive any count filed in a report or SCORECARD row with the CORPUS.md census commands over `git show <rev>:corpus/SOURCES.md` (or `registry_count_check.py --claims <json>`) before filing; on any registry edit, re-derive before writing the next count

# Claim-count derivation discipline

Every count in a self-assessment document (SCORECARD row, report section, lesson table) is a
claim about committed bytes, not a measurement by itself. It must name the revision it was
measured over and re-derive from those bytes with a recorded command at filing time.

The round-42 defect that grounds this entry: the round-42 report and SCORECARD stated registry
"rows 128 → 131; mined +1 net of supersessions". Re-derived from the committed bytes at the two
revisions the round named (`1ef7a0e9` base, `5949e66ffe` tip), the census commands give
**119 → 128 rows; mined +7; queued +0; rejected +2** (S120–S128 added; the report's 128 was
already the tip value restated as the base). The stated counts failed re-derivation at both
ends — a calibration error present when the sentence was written, exactly the class kama's
writing-revision check extracts (S130: "records a calibration error present when the statement
was written").

Rules landed with this entry (round 43):

1. A count filed without its counting command and measured revision is a conformance defect
   (QUALITY "A count carries its command", applied to the lane's own bookkeeping).
2. A correction to a filed count is append-only: a new row or entry naming the superseded
   text, never an edit of filed bytes (protocol report rule; CORPUS.md corrections rule).
3. The able-to-fail gate is `.ufo/waves/round-43/registry_count_check.py`: it re-derives the
   rows/mined/queued/rejected at two revisions from a claims file and exits 1 on any mismatch.
   It is red on the round-42 claims (`verification/freeze/registry-count-r42-check.txt`,
   exit 1) and green on the round-43 correction (`registry-count-r43-check.txt`, exit 0).

Correction (2026-10-24, kake round 45, appended per the corrections-are-new-entries rule): the
`source:` line above names S130; S130 was superseded by S132 in round 44 under SOURCES.md contract
rule 2 (a correction is a new row whose teaches opens `supersedes S0NN —`). The writing-revision
method this entry cites is now carried by S132 (`corpus/SOURCES.md` row S132, kama round 29
adjacency import); read the `source:` line's S130 as S132 from this correction forward. Routed
defect fixed: the round-44 closure's "claim-count-derivation.md still declares source: S130".
