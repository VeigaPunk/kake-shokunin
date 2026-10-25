# round-20 — non-author verification and spot-check (orchestrator, kaika)

Written by the integrator, not the lane (CORPUS.md: corrections and outside reviews are new
files; the lane owns `round-20.md`). Verifiers were fresh agents dispatched by the orchestrator
after the round landed at `9639ec7a7`; full reports are committed in the fleet repo at
`.ufo/waves/kaika-w3/kake-review.md` and `kake-critic.md`.

## Spot-check (LEARNING.md — at least one admit and one reject)

| decision | sample | verifier | result |
|---|---|---|---|
| admit | `crawl-scope-per-host` (the three project sites cannot carry their own robots.txt) — the only entry on uncovered ground; reviewer re-opened 18 of 18 rows; agree (S007 wording and S008 '1.35' label corrected by appended errata) | W3ReviewKake | agree |
| reject | S017 and S018 rejected — agree (3/3 sampled gate decisions agree) | W3ReviewKake | agree |

## Adjudication

ADMITTED after post-review fixes `9639ec7` (prior lesson/knowledge lines restored byte-identical; every correction now a pure addition; anchor-integrity proof: 728 citations, 148 moved occurrences, 942 line comparisons, 0 mismatches, old→new errata appended). Per-axis: freshness improved-bounded (unannotated locations 26→4, drift targets 7→3; `--section=paths` still exits 1 — 22/26 cleared under the gate's ±2-line rule without splitting tables; missSet 55→55: annotation, not re-verification; score held 10), operability improved (selftest 14→15; planted writes in 25 functions 0/25→25/25 caught; bounded — aliased calls, split lines and child processes unchecked; score held 10), capability `sources-registry` (18 rows, census ok), other axes unchanged. Trends: expansion improved (narrow: capability + one entry on new ground; three entries supersede covered ground), quality improved (two disproved GitHub Pages claims corrected at 27 sites), discernment improved.
