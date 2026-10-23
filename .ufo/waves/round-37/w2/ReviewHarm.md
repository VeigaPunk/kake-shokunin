# ReviewHarm — round 37 wave 2: no-axis-harmed check

Attacked: the claim that round 37 (621fb528..79d3c780) harms no axis: deletions, SCORECARD axis rows,
every lane selftest. Sandbox: /fast/scratch/hyaku/kake-r37w2/ReviewHarm/{clone@79d3c780, base@621fb528};
TMPDIR=<sandbox>/tmp; GIT_* unset; every run wrapped in `timeout 900`; outputs in <sandbox>/out/.
621fb528 is the round-36 tip and the parent of 202d625a (the first round-37 commit). No tools installed.

## Selftests (each run in its own clone root)
| Selftest | base 621fb528 | tip 79d3c780 | Δ |
|---|---|---|---|
| scripts/base_path_selftest.py | exit 0, 45/45 | exit 0, 45/45 | identical output |
| scripts/citing_set_selftest.py | exit 0, 45 cases clean | exit 0, 45 cases clean | only temp-dir names differ |
| scripts/citing_set.py --selftest | exit 0, 45 clean | exit 0, 45 clean | only temp-dir names differ |
| scripts/citing_set_hostile_selftest.py --root R --tmpdir T | exit 0, 7 passed/0 failed | exit 0, 7/0 | only paths differ (with no args, both exit 2: usage, --root/--tmpdir required) |
| scripts/link_preview_selftest.py | exit 0, 46/46 | exit 0, 46/46 | identical output |
| scripts/source_recheck_selftest.py | exit 0, 101/101 | exit 0, 106/106 | +5 fixtures (528a6d02) |
| scripts/source_recheck_hardening_selftest.py | absent | exit 0, 6/6 | new |
| scripts/robots_audit_selftest.py | absent | exit 0, 131/131 | new |
| scripts/canonical_audit.py --selftest | exit 0, 82/82 ok | exit 0, 82/82 | identical output |
| scripts/accessibility_packet.py --selftest | exit 0, 16/16 | exit 0, 16/16 | identical output |
| scripts/receipt_replay.py --selftest | exit 0, 129 checks | exit 0, 129 checks | identical output |

Round-36 record comparison: source_recheck 101/101 (round-36-verifier-spotcheck.md:80; LOG.md@621fb528:1501),
link-preview 46/46 (LOG.md@621fb528:1485). Both reproduce at base, and the tip does not regress either.
Cross-runs (the strongest regression check for the only deleted code):
- base 101-fixture selftest `--tool` tip source_recheck.py (sha 37a8a8ef…) → exit 0, 101/101. The round-36 contract is kept.
- tip 106-fixture selftest `--tool` base source_recheck.py (sha 3e5457a9… = round-36 tip sha) → exit 0, 106/106. The new fixtures target
  mutants, not the base tool, so this matches the "kill 5 survivors" framing and is not a weakness of it.

## Deletions — `git diff --numstat 621fb528 79d3c780` (exit 0)
628 files, +118978 / −16. Only lines with deletions (`-`-only rows are 4 new binary .gz sources, no deletions):
- corpus/SOURCES.md `4 1`: the deleted line is the S011 row, re-added unchanged except for the used-by cell, which now also names
  corpus/knowledge/robots-txt-rules.md. The other +3 are S095–S097. Not harm.
- scripts/source_recheck.py `111 15`: the 15 deleted lines are a rewrite, not a removal. (1) `_RAW_START_RE` regex scan → quote-aware
  `tag_end`/`raw_tag_name` (contract (c) amendment: `<script` inside an attribute value no longer opens a raw element). (2) `body_path`
  returns the validated `real` path instead of `candidate` (symlink check-then-open race). (3) `load_manifest` (:607) replaces the plain
  `open().read()` with a stat → O_NONBLOCK open → fstat, plus a 64 MiB cap (`MAX_MANIFEST_BYTES`, :40), so FIFOs, devices and oversized
  files become "unreadable" instead of hanging or raising MemoryError. That last change is a deliberate narrowing: manifests over 64 MiB,
  previously accepted, are now refused. It is disclosed in-code and does not touch any selftest. The cross-run above shows no regression.
- SCORECARD.md `257 0`, LOG.md `18 0`, PROVINCE.md `10 0`, corpus/README.md `10 0`: insert-only.

## SCORECARD axis rows
`git diff -U0 621fb528 79d3c780 -- SCORECARD.md` has a single hunk, `@@ -1752,0 +1753,257 @@`, which is a pure append. Axis rows
operability (line 14) and freshness (line 15) are byte-identical. SCORECARD.md@79d3c780:2001-2002 states "Axis ratings unchanged (10 → 10)".

## Findings
1. LOW (wording/operability), SCORECARD.md@79d3c780:2001: "Capability row … entered `## Capabilities` below." The canonical
   `## Capabilities` table (lines 187-197) did not change, because the only hunk is the append at 1753. The row sits instead in a new
   `### Capabilities acquired in round 37` subsection at :2005/:2009. Round 36 inserted its row into the canonical table itself (:197;
   it said "entered `## Capabilities`" at :1730). Round 25 used a per-round subsection (:470), so there is precedent for both. Even so,
   anyone reading the canonical table will not see the robots capability, and "entered `## Capabilities`" is overstated.
   Fix: add the row to the table at line 187, or change the wording to "entered the round-37 capabilities subsection below".
2. INFO (pre-existing, not round 37): scripts/citing_set_selftest.py:158 `DEFAULT_TMPDIR = "/fast/scratch/hyaku/kake-r27"` ignores
   $TMPDIR when --tmpdir is not passed. My two runs (and citing_set.py --selftest) created private temp dirs there and removed them;
   afterwards `ls /fast/scratch/hyaku/kake-r27/citing-set-selftest-*` matches nothing. Byte-identical at base, so no harm from round 37,
   but sandboxed callers should pass --tmpdir.

## Verdicts
- "No deletions harm an axis": HOLDS. The 16 deleted lines are a row edit and a contract-preserving rewrite (101/101 cross-run).
- "SCORECARD axis rows unchanged": HOLDS (append-only hunk; lines 14-15 identical).
- "Every lane selftest still passes at 79d3c780": HOLDS. All 11 entry points exit 0, with counts equal to or above round 36.
- "Capability row entered `## Capabilities`": OVERSTATED (finding 1).
- Harm verdict: no axis harmed. Operability is improved (two new selftests, hardened reader), freshness is not regressed (S011 row
  only extended). One low-severity wording defect.

Residual risk: selftest outputs only. I did not mutation-test the hardening (that is SentinelHardening's/ReviewHardening's lane), and
I did not run the C1 counter (the RerunC1Sealed lane).
