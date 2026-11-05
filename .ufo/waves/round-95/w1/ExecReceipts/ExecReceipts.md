# ExecReceipts — round-95 receipt debt (R94-8 erratum + landed-tip receipt plan)

Seat copy of `.ufo/waves/round-95/w1/ExecReceipts.md` (the Report trailer
path). Content identical; kept beside the receipts for one-directory closure.

## Deliverables in this directory

- `erratum-r94-8.md` — R94-8 erratum: pointer claimed vs absent, measured
  bytes, two-sentence lesson correction, unrecoverable-from-this-lane marker.
- `run-final-receipts.sh` — landed-tip receipt script (bash, set -euo
  pipefail; takes REVISION as $1; scratch-clean via trap; counter rcs and
  instrument digest checks on stderr; receipts = revision line + counter
  stdout).
- `dryrun-c1.txt` / `dryrun-c2.txt` — dry-run receipts against the freeze
  commit `8f638b591e739e1863f5fa22334d5e15178189ed` (script rc 0; c1_rc=1,
  c2_rc=1 — met=false by design; outputs produced to scratch, copied here).

Full report: `../../ExecReceipts.md` relative to this directory, i.e.
`.ufo/waves/round-95/w1/ExecReceipts.md`.

Verdict: `RECEIPTS erratum=ready script-dryrun=rc=0`
