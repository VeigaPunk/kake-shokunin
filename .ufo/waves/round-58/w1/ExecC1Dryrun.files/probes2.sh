#!/bin/bash
# ExecC1Dryrun — probe 6: sibling candidate ledger (note TODO) and ledger-built-before-build hazard.
set -u
S=/fast/scratch/hyaku/kake-r58/ExecC1Dryrun
C=$S/clone
LOG=$S/log
L=/home/vgpnk/Projects/shokunin/kake-shokunin
CTR=.ufo/waves/round-58/c58_receipt_rewrites.py
BL=$L/.ufo/waves/round-58/w1/ExecLedgerBuild.files/build_ledger.py
ID=(-c user.name=selftest -c user.email=selftest@local -c commit.gpgsign=false)
PRE_T0=cc8da1674d6e590ae2d05e1f48944ac7939e9ecd
cd "$C" || exit 1
commit() { git -C "$C" "${ID[@]}" commit -q -m "$1"; git -C "$C" rev-parse HEAD; }
line() { python3 -B "$C/$CTR" --root "$C" --revision "$1" --list > "$LOG/$2.txt" 2>&1; local rc=$?; echo "[$2] $(grep -m1 '^C1 receipt-rewrites' "$LOG/$2.txt" | sed -E 's/  \(met:.*//') exit=$rc"; }

echo "== P6 sibling candidate ledger as produced (default --note TODO)"
git -C "$C" checkout -q -B dry-todo "$PRE_T0"
cp "$L/.ufo/waves/round-58/w1/ExecLedgerBuild.files/receipt-rewrites.json" "$C/.ufo/waves/round-58/receipt-rewrites.json"
printf 'C2 resolver-cases cases_passed=12 of 12 met=True\n' > "$C/.ufo/waves/round-58/controls/after-c2-resolver-cases.txt"
printf 'C3 quote-truth conditions_passed=8 of 8 met=True\n' > "$C/.ufo/waves/round-58/controls/after-c3-quote-truth.txt"
git -C "$C" add -A -- .ufo/waves/round-58/receipt-rewrites.json .ufo/waves/round-58/controls/
X=$(commit "todo-ledger: candidate ledger with default notes + C2/C3 receipts")
line "$X" p6-todo-ledger

echo "== P7 ledger built at the pre-T0 tip, build commit also rewrites a round-56 receipt"
git -C "$C" checkout -q -B dry-buildrewrite "$PRE_T0"
python3 -B "$BL" --root "$C" --revision HEAD --note 'see {path}' --out "$C/.ufo/waves/round-58/receipt-rewrites.json" 2>/dev/null
printf 'C2 resolver-cases cases_passed=12 of 12 met=True\n' > "$C/.ufo/waves/round-58/controls/after-c2-resolver-cases.txt"
printf 'C3 quote-truth conditions_passed=8 of 8 met=True\n' > "$C/.ufo/waves/round-58/controls/after-c3-quote-truth.txt"
printf 'dry-run: build commit touched a round-56 receipt\n' >> "$C/.ufo/waves/round-56/controls/c2-selftest.txt"
git -C "$C" add -- .ufo/waves/round-58/receipt-rewrites.json .ufo/waves/round-58/controls/ .ufo/waves/round-56/controls/c2-selftest.txt
Y=$(commit "stale-ledger: ledger built before a receipt rewrite in the same commit")
line "$Y" p7-stale-ledger-in-build
echo "== P7b same tip, ledger rebuilt from the final tip"
python3 -B "$BL" --root "$C" --revision "$Y" --note 'see {path}' --out "$C/.ufo/waves/round-58/receipt-rewrites.json" 2>/dev/null
git -C "$C" add -- .ufo/waves/round-58/receipt-rewrites.json
Z=$(commit "stale-ledger: ledger rebuilt from the final tip")
line "$Z" p7b-rebuilt-ledger
