CONFORMANT — C2 annotation repair (two annotation rows + pins entries) verified at freeze b49cba9.

Checks (all run this wave, ~19:53Z):

1. `cd /home/vgpnk/Projects/shokunin/kake-shokunin && node scripts/freshness-sweep.mjs --section=paths`
   exit 0, trailer "VERDICT: OK (exit 0)". Output lists both targets under declaredAbsent citing the
   annotation lines: `~/Projects/shokunin/.ufo/waves/round-29/w2/FieldsAndCounts.md  corpus/lessons/round-29.md:102 (+1)`
   and `~/Projects/shokunin/.ufo/waves/round-33/w2/ScoutPinsFlagAccuracy.md  corpus/lessons/round-33.md:43 (+1)`;
   missSet 65, drift 0. holds.

2. Annotation proximity + content (read corpus/lessons/round-29.md:94-105, round-33.md:38-45):
   - round-29.md:104 annotates the misroot citation at :102 (offset +2, within +/-2). holds.
   - round-33.md:45 annotates the citation at :43 (offset +2, within +/-2). holds.
   - Each row names the exact missing target (absolute fleet-root path), a dated event
     ("r43 re-census 2026-10-23"; the removal is attributed to "the round-29/33 misroot sweep"),
     the surviving lane copy (`.ufo/waves/round-{29,33}/w2/…md`), and states "Historical incident
     record, not an executable path." holds. Nuance: the removal event is named by round, not
     calendar-dated; the dated element present is the re-census annotation date. If the predicate
     demanded a calendar date on the removal itself, this would be overstated — as read, it holds.

3. Ground truth of absence/survival (test -e):
   - `/home/vgpnk/Projects/shokunin/.ufo/waves/round-29/w2/FieldsAndCounts.md` ABSENT (fleet root). holds.
   - `/home/vgpnk/Projects/shokunin/.ufo/waves/round-33/w2/ScoutPinsFlagAccuracy.md` ABSENT. holds.
   - Lane copies `.ufo/waves/round-29/w2/FieldsAndCounts.md` and `…/round-33/w2/ScoutPinsFlagAccuracy.md`
     under kake-shokunin both EXIST. holds.

4. Pins entries (`corpus/knowledge/freshness-pins.json`):
   - `python3 -c "import json; …"` parses cleanly; `pins.pathsMissSet` has 65 entries, all unique;
     metadata round 43, updated 2026-10-23.
   - Both tokens present verbatim: `~/Projects/shokunin/.ufo/waves/round-29/w2/FieldsAndCounts.md`,
     `~/Projects/shokunin/.ufo/waves/round-33/w2/ScoutPinsFlagAccuracy.md`. holds.
   - Note: key lives at `pins.pathsMissSet`, not top level — the C2 claim "pathsMissSet 63->65" is
     consistent with the file's `pins` envelope.

Residual risk: none found in scope. Byte-exactness of lane copies vs the deleted fleet copies was
not re-verified (fleet copies are gone; the `cmp` claim is from the round-33 citation text).

Tooling: no installs or upgrades performed; stock node v24.21.0 and python3 sufficed.
Report: .ufo/waves/round-43/w1/ReviewC2A.md
