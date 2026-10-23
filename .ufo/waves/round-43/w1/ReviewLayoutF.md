CONFORMANT: c43_count_v4 layout_f's scope claim matches the round-41 tool's actual scope rule — under a fold pair's segment-cased sitemapUrl the round-41 tool flags the all-lower second member `loc_out_of_scope` (exit 1), and the v1_casefold control answers it in-scope (exit 0). Empirically demonstrated on the exact pinned reference blob.

Axes: operability (this item), freshness (untested here).

## What was checked
layout_f (c43_count_v4.py:507-562) claims for a foldpair: "the round-41 tool flags the second
member out_of_scope (case-sensitive first-segment compare), a case-fold cache answers it
in-scope". Static read:
- round-41 tool (1ef7a0e9:scripts/sitemap_audit.py): `_parse_url` returns
  (scheme, host.lower(), port, path) — path case-preserved (r41:89-103); scope check is
  case-sensitive `parsed[3].startswith(_directory_of(sitemap_url[3]))` (r41:306-318).
- v1_casefold control: same scan/scope logic, but `_parse_url` memoizes on
  `value.translate(_FOLD_TABLE)` (v1:295-328, 526-536) — a/b collide on the folded key, so b
  is answered from a's parse.

## Witness (two-value fold pair, both orders)
Dir /fast/scratch/hyaku/kake-r43/ReviewLayoutF/witness/. pairAB.xml urlset:
loc1 a = https://hostw1.example.invalid/kxqZwvtm/prtm
loc2 b = https://hostw1.example.invalid/kxqzwvtm/prtm  (one upper letter in first segment vs all-lower)
m_upper.json: sitemapUrl = segment_smu(a) = https://hostw1.example.invalid/kxqZwvtm/sitemap.xml
m_lower.json: sitemapUrl = segment_smu(b) = https://hostw1.example.invalid/kxqzwvtm/sitemap.xml

Commands: `python3 -B r41_sitemap_audit.py --manifest m_upper.json` (and ctl / m_lower), cwd witness/.

r41 + m_upper: exit 1
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "cpA", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 2}]}]}
v1_casefold + m_upper: exit 0
{"version": 1, "verdict": "clean", "checks": [{"id": "cpA", "status": "clean", "error": null, "findings": []}]}
r41 + m_lower: exit 1
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "cpB", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}
v1_casefold + m_lower: exit 1
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "cpB", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}, {"code": "loc_out_of_scope", "entry": 2}]}]}

The flip is exactly as layout_f docstrings: r41 flags entry 2 (b) out_of_scope and keeps entry 1
clean under a's casing (and the reverse under b's casing — per-entry case sensitivity both ways);
the case-fold cache control answers b from a's memo → clean/exit 0 under a's casing, and doubles
the finding under b's casing.

## Identity anchors (all hold)
- Counter pins REF41_REV 1ef7a0e95f68..., REF41_SHA 50287ac6de56... and re-verifies the blob sha
  before every evaluation (c43_count_v4.py:84-85, 972-976). My extracted copy sha256 =
  50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d — the exact witnessed runtime.
- Working tree == freeze tip b49cba9: counter sha 1c3b9661... and v1_casefold sha 9993b842...
  identical in both (git show verified). No seat-score-predating-freeze evidence found in scope.
- Freeze-tip scripts/sitemap_audit.py (blob 21553d19) keeps the same case-sensitive scope logic
  (lines 511-516) — no scope-rule drift.
- SCORECARD.md:3119 already records CtlFreshCache/v1_casefold (sha 9993b842...) 10/10 met with
  "answered from case-folded memo; CLI entry flips" — consistent with this witness.

## Per-statement verdicts
- "round-41 tool flags the second member out_of_scope under a's segment-cased sitemapUrl" — holds (exit 1, entry 2, m_upper).
- "case-fold cache answers it in-scope" — holds (v1_casefold exit 0 clean, m_upper).
- segment_smu derives the sitemapUrl from `a` for foldpairs (c43_count_v4.py:555) — holds.
- v1_casefold sha 9993b842... matches SCORECARD-documented control — holds.

## Findings
None in scope. Minor note (not a defect): git HEAD of the lane is 7c070797, not the freeze tip
b49cba9; the frozen files compared above are identical, so no conformance impact observed, but
report readers should cite b49cba9 blobs, not HEAD.

## Residual risk / gaps
- Witness covers one fold pair shape (clean values, https, tail segment); fold_pair also randomizes
  scheme case, tail presence, and query suffix — all orthogonal to the case-sensitive prefix
  compare confirmed in code, but not each individually re-run.
- I did not rerun the full counter on any tool (out of my item's scope; L1 receipts cover it).
No tool installs performed (tooling directive: nothing to record).
