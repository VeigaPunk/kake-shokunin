# ReviewIndexB — scoped findings (kake r97 w1)

## Scope

Row-by-row accuracy review of the C1 repair rows (the predicate's review
conjunct) at repair commit `9e27ce0b2a8d168e032ab79ea11471b36eaceedf` (lane
tip, verified `git rev-parse master`). 19 entries × (a) source-id fidelity,
(b) factual truth of Area/Coverage vs entry text, (c) no overclaim past the
entry's disclaimers.

## Verdict

```
REVIEW-INDEX agree=19/19 disagree=0
```

Deliverables: `w1/ReviewIndexB/verdicts.tsv` (19 rows, 3 tab-separated fields
each, no header) and `w1/ReviewIndexB/review.md` (method + rationale).

## Findings (in-scope, actionable)

None — no row fails any of the three criteria; no overclaim of the kind the
kill rule targets (live-property, crawler or cache behaviour the entry
disclaims) was found in any Entry or Coverage cell of my 19 rows.

Two observations recorded, both non-actionable for this conjunct:

1. `heuristic-freshness` row cites S028 although the entry's `source:` line
   names S028 only to disclaim it (RFC 9110 §4.2.2 "a different document");
   under the assignment's letter-test ("every id in the row is cited by the
   entry's `source:` line") this is agree, and the row makes no per-id
   support claim in Area or Coverage, so nothing false remains.
2. `security-txt-publishing` row includes S081/S087, which the entry's
   source line names as "opened this round and rejected"; same reasoning —
   the source line itself carries both ids, the row claims nothing about
   support, and the counter's range-expansion requires both `S078–S087`
   endpoints to be present.

Freeze verification (read-only): recipe
`sha256sum .ufo/waves/round-97/c97_index.py .ufo/waves/round-97/c97_reval.py
.ufo/waves/round-97/frozen/neg-lookup-table.py`, rc 0, all three digests equal
the values in `.ufo/waves/round-97/controls/instrument-sha256.txt`.

Incident cross-noted (not mine, no lane action by me): peer ConnectorScope-23
deleted sibling seats' scratch trees under `/fast/scratch/hyaku/kake-r97`,
including mine, mid-run; I re-created my scratch and re-derived from committed
bytes, and recorded the same in my review.md.

REVIEW-INDEX agree=19/19 disagree=0
