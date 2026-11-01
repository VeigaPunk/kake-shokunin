# Gate-status ledger — historical and host-bound gates (adopted r66)

Adopted from `considerthese/2026-10-26.md` proposal 5 ("Historical-gate list"):
a dated list of gates that go red by design on later trees or on a migrated
host, so a standing red is not misread as a fresh regression, and so a gate
that *should* be re-pinned is visible as such. Rows are derived line-for-line
from the round-66 receipts named below; nothing here is a claim that a
recorded status is correct — the receipts are the authority.

## Round-66 measurement (host: Windows, python 3.13.15, the c66 v2 counter)

Before this round the 28-member registry could not be adjudicated on this
host at all: `.ufo/waves/round-65/controls/c60-paired-thishost.txt` and the
round-66 re-run at base (`.ufo/waves/round-66/controls/c60-v1-base-r66.txt`)
both print `members=28 mismatches=28`, every observation dying of the
environment (exit 2, outside the family verdict alphabet). The round-66 v2
counter (`.ufo/waves/round-66/c66_gate_status_hostportable.py`, receipt
`controls/after-c66.txt` at revision `a26fd6a57a3549a927b2e9fb589cf72813af2c24`)
makes every member produce a real family-verdict exit:
`members=28 evaluated=28 structural=0 agreement=17 met=True` (evaluability,
not agreement — 11 label mismatches are measured and reported, not forced).

| Gate | Registry label | This-host observed | Class | Ledger disposition |
|---|---|---|---|---|
| c48_lint_count | live | e_T=0 | ok | recorded green re-derives on this host |
| c48_quote_truth | live | e_T=0 | ok | recorded green re-derives on this host |
| c49_order | live | e_T=0 | ok | recorded green re-derives on this host |
| c49_quote_truth | live | e_T=0 | ok | recorded green re-derives on this host |
| c50_durable | live | e_T=0 | ok | recorded green re-derives on this host |
| c50_quote_class | live | e_T=0 | ok | recorded green re-derives on this host |
| c51_quote_truth | live | e_T=0 | ok | recorded green re-derives on this host |
| c51_wave_ledger | live | e_T=0 | ok | recorded green re-derives on this host |
| c52_gate_registry | live | e_T=0 | ok | recorded green re-derives on this host |
| c52_mutation_ladder | live | e_T=0 | ok | recorded green re-derives on this host |
| c52_quote_truth | live | e_T=0 | ok | recorded green re-derives on this host |
| c52_wave_ledger | live | e_T=0 | ok | recorded green re-derives on this host |
| c53_gate_truth | never-met | e_T=1, e_P=1 | ok | red-at-pin red-at-tip by design; re-derives |
| c54_ops_debt | live | e_T=0 | ok | recorded green re-derives on this host |
| c54_s374_calib | live | e_T=0 | ok | recorded green re-derives on this host |
| c55_quote_truth | historical | e_T=1, **e_P=1** | historical_not_green_at_pin | pin run no longer reproduces its green on this host — read as host-era, not a tip regression; not adjudicated here |
| c55_readme_index | live | e_T=0 | ok | recorded green re-derives on this host |
| c56_quote_truth | historical | e_T=1, **e_P=1** | historical_not_green_at_pin | the r55-known "6/8 on every later tree" gate (it pins 158 rows); now also not green at its own pin on this host |
| c56_selftally | live | **e_T=2** | live_not_green | the standing r64/r65 red, now a real family exit: the selftally reports an unparsable row; the frozen inner-env limit (PYTHONUTF8 does not reach c56's fixed-key child env) is the documented candidate mechanism, carried |
| c57_idresolver_gate | live | **e_T=1** | live_not_green | red at the round-66 revision; the r57/r58 differential receipts (5/5, 14/14) were taken at their own revisions; whether the delta is corpus growth or host semantics is not adjudicated here |
| c57_quote_truth | historical | e_T=1, **e_P=1** | historical_not_green_at_pin | as c55/c56 above |
| c57_receipt_pins | live | e_T=0 | ok | recorded green re-derives on this host |
| c58_quote_truth | historical | e_T=1, **e_P=1** | historical_not_green_at_pin | as c55/c56 above |
| c58_receipt_rewrites | live | **e_T=1** | live_not_green | red at the round-66 revision; same non-adjudication as c57_idresolver_gate |
| c58_resolver_cases | live | **e_T=1** | live_not_green | the r58 14/14 receipt was at its own revision `de7d96e7`; red at the round-66 revision is a delta to investigate, not a retraction of the r58 receipt |
| c59_axis_evidence | live | **e_T=1** | live_not_green | red at the round-66 revision; not adjudicated here |
| c59_quote_truth | historical | e_T=1, **e_P=1** | historical_not_green_at_pin | as c55/c56 above |
| c59_resolver_cases | live | **e_T=1** | live_not_green | red at the round-66 revision; not adjudicated here |

## Older known-historical entries (proposal 5's original list)

- `c56_quote_truth.py` — red on every tree after its pin (pins 158 registry
  rows; recorded r55). See above: now also not green at its pin on this host.
- `c53_gate_truth.py` — never-met by design (red at pin and tip); it exists to
  prove the counter catches a never-green gate.
- The three `~/Projects`-era path gates of the freshness sweep are superseded
  by the §paths sidecar mechanism (the 2026-10-30 host migration moved every
  former home tree; the r66 re-pin restored the offline gate to exit 0).

## How to use this ledger

A red row in the SKILL.md registry is "expected red" only while its receipt
chain says so; any round may re-adjudicate a row by re-running its documented
command at the revision the row names and committing the receipt. What this
ledger forbids is silent normalization: a gate that stops re-deriving must be
either re-pinned with a dated receipt or carried here with a named mechanism.
