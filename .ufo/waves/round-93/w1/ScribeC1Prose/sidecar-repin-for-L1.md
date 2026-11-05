Sidecar re-pin needed from your E1/E2/E4 scribe (ScribeC1Prose).

My repairs append 87 lines (0 deletions) to corpus/QUALITY.md and corpus/lessons/round-{29,33,54,85,92}.md. Three freshness-sidecar entries are line-bound and their pinned lines moved, so `freshness-sweep.mjs --offline --section=paths` now throws `Error: paths sidecar binding invalid: corpus/lessons/round-29.md:200` and exits 2 in the worktree. The re-pin is three "line"-field updates (lineSha256 unchanged — the pinned line content moved, not modified):

  corpus/QUALITY.md            649 -> 651  (token ~/Projects/shokunin/.ufo/reports/round-33/kake.md)
  corpus/lessons/round-29.md   128 -> 131  (token ~/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md)
  corpus/lessons/round-29.md   200 -> 203  (token ~/.local/bin/time)

Verified in a scratch clone: after this re-pin the sweep exits 1 with the same pre-existing drift it has at master (1 unannotated miss, ~/projects at round-90.md:82) and no sidecar error; the frozen counter at the same scratch fixture commit reads E1=0 E2=0 E4=0 (my classes) with E3=1 remaining (the C2 knowledge entry's S471-S476 ids are unresolved in SOURCES.md — C2 seat's scope, not mine).

Full spec + verification recipe: `.ufo/waves/round-93/w1/ScribeC1Prose/sidecar-repin-for-L1.json`. My full report: `.ufo/waves/round-93/w1/ScribeC1Prose/ScribeC1Prose.md` (also mirrored at `.ufo/waves/round-93/w1/ScribeC1Prose.md`). I did not edit the sidecar myself — it is outside my named write scope; it is yours to land with the corpus edits.
