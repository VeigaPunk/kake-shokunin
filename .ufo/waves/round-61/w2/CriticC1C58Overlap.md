# CriticC1C58Overlap

SAME for the motivating rewrite/pending-fill class; C1 does not demonstrate incremental calibration over c58. C1 adds a distinct population-drift check, principally `extra_member`, but that is not a new receipt-rewrite detection class and its calibration value is not established here.

## Axes
- Population / scope overlap
- Event-definition coverage and blind spots
- Marginal calibration under a c58-only control

## EVIDENCE

- **Do-nothing control (c58 only):** ran committed `.ufo/waves/round-58/c58_receipt_rewrites.py` at both its measured revision `de7d96e720522ea15fba3fd9ee3ce58c42596031` and current lane tip `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f`. Both returned `EXIT=0`, `events=19`, `undisclosed=0`, `phantom=0`, `malformed=0`, `wrong_kind=0`, `unpointed=0`, `symlinks=0`, `new_rewritten=0`, `new_receipts=2`, `met=True`. Thus the existing in-lane detector and its ledger already pass at the current measured state without C1.
- **Motivating incidents overlap exactly:** c58 ledger records the round-56 `after-c1-selftally.txt` event at `ad06cb8a1` as `pin-only`, and round-57 `after-c1-receipt-pins.txt` at `20217f23e` as `pending-fill`. C1's disclosure registry includes both same `(path, commit)` events, respectively `rewrite` and `pending_filled`. Both tools therefore cover the cited relabel and pending-fill; C1 does not add either detection.
- **Event cross-tab:** `.ufo/waves/round-58/receipt-rewrites.json` has 19 `(path, commit)` entries; `.ufo/receipt-disclosures.json` has 12. Every one of C1's 12 entries is in c58's 19; C1 contributes zero additional historical events. Seven c58 events are outside C1's event set:
  - `round-52/control/c2-quote-selftest.txt` at `a4a890cf1`
  - `round-54/controls/base-c1-s374.txt` and `base-c2-ops-debt.txt` at `a0a4fd482`
  - `round-54/controls/sources-census.txt` at `5826682b3`
  - `round-55/controls/c1-selftest-v2.txt` at `64c0ce12f`
  - `round-55/controls/c2-selftest.txt` at `955e3d7bd`
  - `round-56/controls/c2-selftest.txt` at `ad06cb8a1`
  c58's event walk detects all control-path rewrites; C1 gates detection on first-version receipt grammar and then on result-span changes (except pending-fill). C1 is therefore not a superset of c58 and misses these real rewrite events.
- **Population / the 79:** c58's `POP_RE` covers files under `round-<N>/control(s)/` at any depth. C1's rule also restricts its frozen population to control(s) paths, then recognizes only receipt-grammar files for event detection. Round-58 contract line 104 explicitly records 79 artifact rewrites outside `control(s)/`; both scopes exclude those, so they are not evidence of C1's distinctness.
- **C1 observed output:** running `scripts/receipt_lineage.py` at `9f07731a873585e655a6518233ea39f5d9fb8204` and current tip both printed `receipts=95 events=12 undisclosed=0 met=True`. This confirms the 12-event disclosed registry aligns with the above c58 subset; it does not show new detection power.

## SAME / DIFFERENT

**SAME** for the claimed calibration class: the c58-only control already detects and discloses the r56 relabel and r57 pending-fill, and C1's entire observed historical event set is contained in c58's. The definitions differ (C1's result-span/pending model and frozen-member checks versus c58's byte-level ledger), but the overlap is not merely nominal: C1's 12 events are a strict subset of c58's 19. C1's `member_changed`/`member_missing`/`extra_member` terms are a separate population-integrity surface; c58 has no frozen-list `extra_member` term, though changed/deleted existing files are already rewrite events for c58.

**Smallest safe correction:** do not award C1 distinct calibration credit for detecting undisclosed receipt rewrites on this evidence. If the claim is retained, identify and independently justify `extra_member` (or another frozen-population behavior) as the distinct calibration target, with a control showing c58 misses that behavior; otherwise fold the population guard into the existing c58 instrument rather than presenting overlapping rewrite watches as a new calibration capability.

VERDICT: SAME — c58 already covers the motivating rewrite/pending-fill class and C1's event set is a strict subset; only a separate population-drift term remains potentially distinct.
