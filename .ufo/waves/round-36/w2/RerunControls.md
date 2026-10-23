# RerunControls — re-score every control with the frozen counter

Attacked: committed control receipts `verification/control-*.json` and
`independent-selftest-reference.json` could be fabricated, stale, or non-reproducible.
Re-scored each retained control head and the independent tool file with the frozen v3 counter
(`sealed_count.py`, sha256 `88ec5914…ff8e`, matching every receipt's `counterSha256`), key
revision `fd1fb723624b742a00a6e8e908f3b42901d627f8` (cases.json sha256 `44c94838…ef1d` = pin).

## Method (sandbox `/fast/scratch/hyaku/kake-r36w2/RerunControls/`)

1. `git clone -q <lane> clone && git checkout -q f3a38bf8e68f6cee386125d34b5e95ac9b2df66e`.
2. `git fetch <bundle> 'refs/heads/*:refs/heads/ctl/*'` for each of the 5
   `retained/r36-control-*.bundle`. Each head's parent is `9d81c75c…` (the stated prerequisite).
3. `timeout 290 python3 -B sealed_count.py --root clone --revision <rev> --key-revision fd1fb723…`
   for the 5 control heads + `b720d799…` (base) + `3555f63f…` (declaration) + `9d81c75c…`
   (counter-v2-commit); `--tool-file retained/independent/selftest-seat-reference.py` for the
   independent reference. All outputs in `../out/*.json`; all `.err` files empty.

## Table: committed vs re-run (identical on every field incl. perCase)

| Control (head sha / receipt rev) | committed passed/met | re-run passed/met | diff |
|---|---|---|---|
| CtlAllFalse `e4592f01` | 0/28, false | 0/28, false | none |
| CtlConstantClean `e0852950` | 0/28, false | 0/28, false | none |
| CtlNaiveReader `d9b29a44` | 12/28, false | 12/28, false | none |
| CtlNoReader `657956e4` | 8/28, false | 8/28, false | none |
| CtlShortcut `f06b0e15` | 9/28, false | 9/28, false | none |
| base `b720d799` | 0/28, false (toolPresent false) | same | none |
| declaration `3555f63f` | 0/28, false (toolPresent false) | same | none |
| counter-v2-commit `9d81c75c` | 0/28, false (toolPresent false) | same | none |
| independent selftest reference (toolFile) | 28/28, true | 28/28, true | `toolFile` path string only (`…/kake-r36w1/ExecSelftest/reference.py` vs the retained copy); `toolSha256` `a5176fee…221f` identical |

Committed `.exit` files equal observed exits (1 for all controls; independent re-run exit 0).
CtlShortcut and CtlNaiveReader were each scored a second time: 9 and 12 again, perCase
bit-identical — the counter is deterministic across fresh random ids/filenames.
Won-case sets: NoReader k01–k08; NaiveReader k01–k08+k25–k28; Shortcut k01–k08+k12.

## Tool bytes vs `ctl/<Name>.md` description

Each head's `scripts/source_recheck.py` sha256 equals the receipt's `toolSha256` and the byte
count in the report's key-blindness `ls -la` listing: CtlAllFalse 1634 B `20432773…`,
CtlConstantClean 461 B `81cb0f6f…`, CtlNaiveReader 7158 B `4cfeda8c…`, CtlNoReader 7878 B
`b5e9f6b1…`, CtlShortcut 8351 B `f6cb0aa4…`. Source inspection matches the described defect:
ConstantClean prints one fixed clean report without opening the manifest; AllFalse parses the
manifest, emits `quote_missing` per check, never opens a body; NoReader stats/resolves body
paths (`valid_body_path`, source line ~113) but never opens/decodes; NaiveReader's only body op
is `raw.decode("utf-8", errors="replace")` + `quote not in` (line ~181); Shortcut never opens
bodies and guesses from label regexes (`guess_bom`, `guess_missing`, "secret/ghost/hidden/
script only/mismatch/bom" wordlists, lines 123–198) exactly as described.

## Cross-check supporting the v3 key bump

`verification/v2/control-CtlShortcut.json` (counter `1bf16734…`, key v1) scored 17; the v3
receipt scores 9. Consistent with `sealed_count.py:34-41`: key v2 added `quote_missing`-correct
cases a label-guesser fails. No anomaly.

## Findings

None. Every committed control receipt is byte-for-byte reproducible under the frozen counter
on this host (bwrap `/usr/bin/bwrap`, Python 3.14.x, fresh TMPDIR). No control secretly met the
predicate; no receipt overstated a control's defeat; the independent reference still passes
28/28 from the retained bytes.

## Not verified / residual risk

- v2-receipt reproducibility under `sealed_count_v2.py` (frozen counter is v3; v2 receipts are
  historical context, not claimed v3 output).
- Ablation receipts (`verification/ablations/`) and `c1-*` claim receipts — outside this item.
- Receipts encode environment sensitivity only via bwrap+jail; a different OS/py3 minor could
  theoretically flip a case, but two draws here were identical.

Deliverables: `/fast/scratch/hyaku/kake-r36w2/RerunControls/out/*.json` (10 receipts incl. two
second-draw runs), `clone/` (f3a38bf8 + ctl/* refs), `tools/*.py`. No installs; bwrap present.
Report: .ufo/waves/round-36/w2/RerunControls.md
