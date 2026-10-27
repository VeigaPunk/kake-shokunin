# ScoutC3Rows

Round-61 C3 freshness scout (leaf). Independently re-derived the due set at base
`9f07731a873585e655a6518233ea39f5d9fb8204` from `corpus/SOURCES.md` and checked
the ten rows' cell well-formedness. Method: `git show <base>:corpus/SOURCES.md`
offline into scratch, parsed with an independent Python splitter (pipe-table,
11 columns: id | source | kind | tier | scope | anchor | teaches | status |
opened | recheck | used-by). No lane files mutated; no tools installed.

Registry facts at base: 167 rows total; status mix mined 137 / queued 8 /
rejected 22. Oldest `opened` = 2026-10-19 with 18 rows that date: 16
non-rejected (S001–S016) + 2 rejected (S017, S018). Re-derivation excluded the
2 rejected; tie-break lowest id.

DUE SET:
Re-derived (non-rejected, oldest opened 2026-10-19, ties by lowest id, lowest 10):
S001, S002, S003, S004, S005, S006, S007, S008, S009, S010.

MATCH:
Yes — re-derived set equals the contract's frozen ten exactly, in both
contract.md prose and contract.json `claims.C3.due_set`. The same re-derivation
run against the current lane worktree `corpus/SOURCES.md` returns the identical
ten (worktree file is byte-identical to base for this path as of this report;
no in-place recheck-cell edits from sibling seats yet).

CELLS:
All ten rows are well formed: exactly 11 pipe cells each, no stray pipe inside
any cell, `opened` = 2026-10-19, status `mined`. Current recheck cells,
verbatim from base (worktree agrees):

- S001 → `on-release`
- S002 → `on-release`
- S003 → `90d`
- S004 → `90d`
- S005 → `90d`
- S006 → `90d`
- S007 → `90d`
- S008 → `365d`
- S009 → `365d`
- S010 → `365d`

Full verbatim row lines (all 11 cells, unmodified) are retained at
`.ufo/waves/round-61/w1/ScoutC3Rows.files/due-set-ten-rows-verbatim.md`.

Cadence-vs-pin cross-check against the contract pin rule (opened 2026-10-19):
`on-release` → opened + 90d = 2027-01-17 (S001, S002); `90d` → 2027-01-17
(S003–S007); `365d` → 2027-10-19 (S008–S010). Matches contract.md's stated
pins. These are pre-pin base cadences; the in-place pins and lesson Gate
old→new log are produced later in this wave by the C3 build seats, not here.

No remaining unknowns for this scoped question.

VERDICT: DUE SET re-derived at base = frozen ten S001–S010 (MATCH yes); all ten rows well formed (11 cells, no internal pipe, opened 2026-10-19); recheck cells verbatim S001/S002 on-release, S003–S007 90d, S008–S010 365d.
