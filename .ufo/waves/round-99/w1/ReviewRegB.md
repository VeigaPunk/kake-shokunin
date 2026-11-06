# ReviewRegB — report (kake round 99, wave 1)

Target: C1 row-review conjunct — judge all 26 rows of the `## Round 99 — tool registry completion`
section added by the C1 repair commit 9d341d1b46f16dbfbb41af75dd6d4966808dfa5d, every cell
(Kind, Entry command, Verdict map, Self-test, Write scope, Owner), against the tool bytes at that
commit. Deliverables: `w1/ReviewRegB/verdicts.tsv` (26 lines) and `w1/ReviewRegB/review.md`
(method, commands, rc). Full evidence in review.md; this file is the scoped-findings summary.

## Precondition checks

- Instrument digests: all 11 entries of `.ufo/waves/round-99/controls/instrument-sha256.txt`
  match both the working tree and `git show 2345e309…:<path>` — verified before attacking; no
  mismatch, no repair made.
- Environment: shared clone pinned to 9d341d1b (verified `rev-parse HEAD`), scratch
  /fast/scratch/hyaku/kake-r99/ReviewRegB/, TMPDIR redirected, no lane mutation (read-only git
  only), no tool installs.

## Findings by severity

### False cells → `disagree` (3 rows; C1 kill rule applies to each)

1. **quote_class.py — Verdict map claims `64` usage; the code cannot exit 64.**
   scripts/quote_class.py:142 `ap.error(...)` raises SystemExit(2) → the `return 64` at :143 is
   unreachable. Observed rc=2 (no args). The tool docstring itself says "2 unreadable input or
   usage fault".
2. **sitemap_audit_selftest.py — Verdict map claims `2` setup fault; the runner never exits 2.**
   Usage and tool-not-found return 64 (scripts/sitemap_audit_selftest.py:1538-1550; observed
   `--bogus` rc=64); failures return 1 (:1585). The only `return 2` sites (:1332, :1337) are
   inside the CONSTANT_CLEAN_TOOL generated-fake-tool string, not the runner.
3. **wave_seat_record.py — Verdict map claims `64` usage; argparse default exits 2.**
   scripts/wave_seat_record.py:45 plain `ap.parse_args()`, no SystemExit translation; no path
   returns 64. Observed rc=2 (no args). The row copies the tool docstring, which contradicts
   the code.

Per the frozen kill rule these are findings routed to L1, not repairs; the verdicts do not flip
if the rows are corrected later.

### Notes on `agree` rows (no false cell)

- Exit-1/exit-2 secondary meanings unmapped on header_change_class.py, ledger_latest_check.py,
  knowledge_metatext_lint.py, robots_audit_selftest.py (selftest failure = 1; argparse usage = 2).
- probe-delta.mjs: 64 also fires for invalid `--hole-hours`/`--since` values, not only unknown flag.
- source_snapshot.py write scope omits `receipts.json` (written at scripts/source_snapshot.py:297);
  all writes stay inside declared output locations.
- response_snapshot.py / live_snapshot.py defaults point inside the lane tree; run only with
  explicit args (as this review did).

## Verification performed

- All 18 Self-test-cell commands that claim a selftest executed from the pinned clone, rc=0 each,
  tallies matching the cells (45/45, 99/99, 6/6, 13/13, 14/14, 2/2, 46/46, 4/4, 10/10, 106/106,
  271/271, 113/113, tests=10). `no self-test` cells verified (0 `--selftest` refs; scorer files
  c89_key.py / c97_reval.py exist at 9d341d1b).
- Entry forms exercised live for the stdin probes and the usage/edge exits listed in review.md.

## Residual risk and gaps

- `--reaudit`, `--write`, and network-GET paths of live_snapshot.py / response_snapshot.py /
  source_snapshot.py were not executed (network/lane-write tools); their cells were judged from
  code reads (argparse, exit sites, O_EXCL/atomic-write sites). Residual risk: a runtime behavior
  of those paths not visible in code — none observed.
- wave_seat_record.py usage evidence relies on argparse's documented default exit code plus one
  observed run; other argparse-based rows' uncaught-usage exits (exit 2) are noted, not scored,
  because their rows do not claim a conflicting mapping.
- Kind cells are judged against docstrings and behavior; "round-N" provenance inside Kind cells
  was taken from the tools' own docstrings and committed contract paths, not re-derived from
  round history.
- Scratch seat directory deleted after copying receipts; no seat tree remains on disk.

REVIEW rows=26 agree=23 disagree=3
