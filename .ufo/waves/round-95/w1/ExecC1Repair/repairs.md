# repairs.md — R94-5 row-by-row file choices (base fdd5fdbe SKILL.md)

Each row: directory token leaves backticks (prose), one concrete committed non-empty regular blob enters backticks. First cells unchanged.
Evidence commands: `git cat-file -t` / `-s` / `ls-tree` at `fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3` (read-only).

| line | row (first cell) | old token (base) | new file (backticked) | cat-file kind/size at fdd5fdbe |
|---|---|---|---|---|
| 617 | citing-set | `scripts/fixtures/citing-set/` (tree) | `scripts/fixtures/citing-set/01-single-literal-clean/expected.json` | blob 34B mode 100644 |
| 720 | The audit reports `outside_base_path` on an `<a href>` point | `.ufo/waves/round-29/real-input/out/` (tree) | `.ufo/waves/round-29/real-input/out/summary.json` | blob 950B mode 100644 |
| 726 | base-path-audit | `scripts/fixtures/base-path/` (tree) | `scripts/fixtures/base-path/D1-root-relative-stylesheet/expected.json` | blob 325B mode 100644 |
| 1046 | link-preview-audit | `scripts/fixtures/link-preview/` (tree) | `scripts/fixtures/link-preview/clean_first_canonical/expected.json` | blob 43B mode 100644 |
| 1253 | selftest-tally-counter | `scripts/fixtures` (tree) | `scripts/fixtures/quote-class/markup.txt` | blob 56B mode 100644 |
| 1254 | yahoo-crawl-handling-quote-truth-counter | `.ufo/waves/round-56/sources/` with `receipts.json` (tree) | `.ufo/waves/round-56/sources/receipts.json` | blob 1789B mode 100644 |
| 1350 | canonical-crawler-identity-quote-truth-counter | `.ufo/waves/round-51/` (tree) | `.ufo/waves/round-51/sources/receipts.json` | blob 909B mode 100644 |
| 1359 | response-snapshot | `.ufo/waves/round-61/capture/` (tree) | `.ufo/waves/round-61/capture/charter-ghp/response.json` | blob 1982B mode 100644 |
| 1431 | c73_wave_pointers.py | `.ufo/waves/round-72/` (tree) | `.ufo/waves/round-72/contract.md` | blob 5747B mode 100644 |
| 1506 | scripts/x_robots_tag_audit.py (round-80 grammar) | `.ufo/waves/round-80/cases` (tree) | `.ufo/waves/round-80/cases/c32/manifest.json` | blob 248B mode 100644 |
| 1535 | c84_defect_queue.py | `.ufo/waves/round-85/w1/ExecRegistry/` (tree) | `.ufo/waves/round-85/w1/ExecRegistry/c1-base.json` | blob 728B mode 100644 |
| 1536 | c84_policy_values.py | `.ufo/waves/round-85/w1/ExecRegistry/` (tree) | `.ufo/waves/round-85/w1/ExecRegistry/c1-base.json` | blob 728B mode 100644 |
| 1537 | policy_value_class.py | `.ufo/waves/round-85/w1/ExecRegistry/` (tree) | `.ufo/waves/round-85/w1/ExecRegistry/c1-base.json` | blob 728B mode 100644 |
| 1539 | count.py (round 85) | `.ufo/waves/round-85/controls/` (tree) | `.ufo/waves/round-85/controls/base-c1.txt` | blob 230B mode 100644 |
| 1588 | c87 finite claims | `.ufo/waves/round-87/{expected-ledger.json,age-cases.json,snapshots/}` (tree) | `.ufo/waves/round-87/expected-ledger.json` | blob 2275B mode 100644 |

Notes:
- 15 row occurrences (15 base E5 findings) across 13 distinct directory tokens; `.ufo/waves/round-85/w1/ExecRegistry/` occurs in three rows (1535, 1536, 1537), and the 13 in the freeze/seat list are distinct tokens.
- `.ufo/waves/round-85/w1/ExecRegistry/registry-rows.mjson` (named as a candidate in the seat spec) does NOT exist at fdd5fdbe; replaced by `c1-base.json` (728 B) from the same directory.
- Row 1588 brace group `{expected-ledger.json,age-cases.json,snapshots/}` counted as one backticked token; the snapshots/ directory and age-cases.json move to prose, and one blob (`expected-ledger.json`) keeps the single token, so the pinned per-row count is unchanged.
- Row 1254 keeps prose `receipts.json` (not a path token).
