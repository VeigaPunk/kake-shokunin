#!/bin/bash
# ExecC1Dryrun — extra probes: stale ledger, incremental landing, single-commit landing.
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

echo "== P1 stale ledger after reverting the disclosure (expect undisclosed=1, met=False)"
line 6d1b7f783ef3f6ad5f0634ace483cf3b8a1476d3 p1-stale-ledger

echo "== P2 incremental landing: ledger only -> +C2 receipt -> +C3 receipt"
git -C "$C" checkout -q -B dry-inc "$PRE_T0"
python3 -B "$BL" --root "$C" --revision HEAD --note 'see {path}' --out "$C/.ufo/waves/round-58/receipt-rewrites.json" 2>/dev/null
git -C "$C" add -- .ufo/waves/round-58/receipt-rewrites.json
A=$(commit "inc: ledger only")
line "$A" p2a-ledger-only
printf 'C2 resolver-cases cases_passed=12 of 12 met=True\n' > "$C/.ufo/waves/round-58/controls/after-c2-resolver-cases.txt"
git -C "$C" add -- .ufo/waves/round-58/controls/after-c2-resolver-cases.txt
B=$(commit "inc: + C2 receipt")
line "$B" p2b-plus-c2
printf 'C3 quote-truth conditions_passed=8 of 8 met=True\n' > "$C/.ufo/waves/round-58/controls/after-c3-quote-truth.txt"
git -C "$C" add -- .ufo/waves/round-58/controls/after-c3-quote-truth.txt
D=$(commit "inc: + C3 receipt")
line "$D" p2c-plus-c3

echo "== P3 single-commit landing: ledger + all three receipts in one commit (amend)"
git -C "$C" checkout -q -B dry-one "$PRE_T0"
python3 -B "$BL" --root "$C" --revision HEAD --note 'see {path}' --out "$C/.ufo/waves/round-58/receipt-rewrites.json" 2>/dev/null
printf 'C2 resolver-cases cases_passed=12 of 12 met=True\n' > "$C/.ufo/waves/round-58/controls/after-c2-resolver-cases.txt"
printf 'C3 quote-truth conditions_passed=8 of 8 met=True\n' > "$C/.ufo/waves/round-58/controls/after-c3-quote-truth.txt"
git -C "$C" add -- .ufo/waves/round-58/receipt-rewrites.json .ufo/waves/round-58/controls/after-c2-resolver-cases.txt .ufo/waves/round-58/controls/after-c3-quote-truth.txt
E=$(commit "one: ledger + C2/C3 receipts")
line "$E" p3a-before-c1
python3 -B "$C/$CTR" --root "$C" --revision "$E" --list > /tmp/c1-run.txt 2>&1; echo "EXIT=$?" >> /tmp/c1-run.txt
cp /tmp/c1-run.txt "$C/.ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt"; rm -f /tmp/c1-run.txt
git -C "$C" add -- .ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt
git -C "$C" "${ID[@]}" commit -q --amend --no-edit
F=$(git -C "$C" rev-parse HEAD)
line "$F" p3b-amended-one-commit

echo "== P4 third after-c2-*/after-c3-* file (new_receipts becomes 3 -> not met)"
git -C "$C" checkout -q -B dry-extra "$F"
printf 'duplicate receipt\n' > "$C/.ufo/waves/round-58/controls/after-c2-resolver-cases-rerun.txt"
git -C "$C" add -- .ufo/waves/round-58/controls/after-c2-resolver-cases-rerun.txt
G=$(commit "extra: a second after-c2-* receipt")
line "$G" p4-extra-c2-receipt

echo "== P5 renaming the C1 receipt after T1 (delete+add => new_rewritten=2)"
git -C "$C" checkout -q -B dry-ren "$F"
git -C "$C" mv .ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt .ufo/waves/round-58/controls/after-c1-receipt-rewrites-v2.txt
H=$(commit "ren: renamed the C1 receipt")
line "$H" p5-renamed
