#!/bin/bash
# Round-58 C1 landing dry run — ExecC1Dryrun. All writes stay under $S.
set -u
S=/fast/scratch/hyaku/kake-r58/ExecC1Dryrun
C=$S/clone
LOG=$S/log
L=/home/vgpnk/Projects/shokunin/kake-shokunin
CTR=.ufo/waves/round-58/c58_receipt_rewrites.py
ID=(-c user.name=selftest -c user.email=selftest@local -c commit.gpgsign=false)
mkdir -p "$LOG"

log() { echo "### $*"; }
commit() { git -C "$C" "${ID[@]}" commit -q -m "$1"; git -C "$C" rev-parse HEAD; }
run() {  # run <rev> <label>
  local out rc
  out=$(python3 -B "$C/$CTR" --root "$C" --revision "$1" --list 2>&1); rc=$?
  printf '%s\n' "$out"
  echo "EXITCODE=$rc"
  log "counter at $2 ($1) exit=$rc"
  return $rc
}

cd "$C" || exit 1
echo "clone toplevel: $(git -C "$C" rev-parse --show-toplevel)"
git -C "$C" checkout -q -B dry || exit 1
PRE_T0=$(git -C "$C" rev-parse HEAD)
log "dry branch starts at $PRE_T0"

log "STEP 0: base-control cross-check at 0440485"
run 044048597d62f3199494b63b36e90dd57825e350 base-c1 | tee "$LOG/step0-base.txt" >/dev/null
grep -E '^C1 receipt-rewrites|EXITCODE' "$LOG/step0-base.txt"

log "STEP 0b: counter selftest in clone"
python3 -B "$C/$CTR" --selftest; echo "SELFTEST_EXIT=$?"

log "STEP 1: build ledger with sibling build_ledger.py --note 'see {path}'"
python3 -B "$L/.ufo/waves/round-58/w1/ExecLedgerBuild.files/build_ledger.py" --root "$C" \
  --revision "$PRE_T0" --note 'see {path}' --out "$C/.ufo/waves/round-58/receipt-rewrites.json"
echo "LEDGER_BUILD_EXIT=$?"
python3 - <<'PY'
import json
p="/fast/scratch/hyaku/kake-r58/ExecC1Dryrun/clone/.ufo/waves/round-58/receipt-rewrites.json"
d=json.load(open(p))
from collections import Counter
print("ledger events:", len(d["events"]), "kinds:", dict(Counter(e["kind"] for e in d["events"])))
print("notes sample:", d["events"][0]["note"])
PY

log "STEP 2: T0 commit (ledger + C2/C3 after-receipts)"
printf 'C2 resolver-cases cases_passed=12 of 12 met=True  (met: cases_passed == 12 of 12)\n  revision: %s\n  (dry-run synthetic content: C2 counter/fixtures not executed in this clone)\n' "$PRE_T0" \
  > "$C/.ufo/waves/round-58/controls/after-c2-resolver-cases.txt"
printf 'C3 quote-truth conditions_passed=8 of 8 met=True  (met: conditions_passed == 8 of 8)\n  revision: %s\n  (dry-run synthetic content: C3 counter/entries not executed in this clone)\n' "$PRE_T0" \
  > "$C/.ufo/waves/round-58/controls/after-c3-quote-truth.txt"
git -C "$C" add -- .ufo/waves/round-58/receipt-rewrites.json \
  .ufo/waves/round-58/controls/after-c2-resolver-cases.txt .ufo/waves/round-58/controls/after-c3-quote-truth.txt
T0=$(commit "round-58 dry run: T0 ledger + C2/C3 receipts")
log "T0=$T0"
run "$T0" T0 | tee "$LOG/step2-T0.txt"
log "T0 exit captured"

log "STEP 3: write C1 receipt from the T0 run, commit T1"
python3 -B "$C/$CTR" --root "$C" --revision "$T0" --list > "$C/.ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt" 2>&1
echo "EXIT=$?" >> "$C/.ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt"
git -C "$C" add -- .ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt
T1=$(commit "round-58 dry run: C1 receipt written after its run at T0")
log "T1=$T1"
run "$T1" T1 | tee "$LOG/step3-T1.txt"

log "STEP 4: SCORECARD/LOG/report edits after T1 (must not change the result)"
printf '\ndry-run edit line\n' >> "$C/SCORECARD.md"
printf '\ndry-run edit line\n' >> "$C/LOG.md"
mkdir -p "$C/.ufo/waves/round-58/w1"
printf '# ExecC1Dryrun (dry-run report placeholder)\n' > "$C/.ufo/waves/round-58/w1/ExecC1Dryrun.md"
git -C "$C" add -- SCORECARD.md LOG.md .ufo/waves/round-58/w1/ExecC1Dryrun.md
T1b=$(commit "round-58 dry run: SCORECARD/LOG/report edits after T1")
log "T1b=$T1b"
run "$T1b" T1b | tee "$LOG/step4-T1b.txt"

log "STEP 5: T2 — rewrite the C1 receipt (must fail new_rewritten=1)"
printf 'rewritten after the fact (dry run)\n' >> "$C/.ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt"
git -C "$C" add -- .ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt
T2=$(commit "round-58 dry run: T2 rewrite of the C1 receipt")
log "T2=$T2"
run "$T2" T2 | tee "$LOG/step5-T2.txt"

log "STEP 6: T3 — rewrite census-before.txt (must fail)"
printf 'dry-run census re-run line\n' >> "$C/.ufo/waves/round-58/controls/census-before.txt"
git -C "$C" add -- .ufo/waves/round-58/controls/census-before.txt
T3=$(commit "round-58 dry run: T3 rewrite of census-before.txt")
log "T3=$T3"
run "$T3" T3 | tee "$LOG/step6-T3.txt"

log "STEP 7: T4 — disclose the census rewrite in the ledger (must still fail on new_rewritten)"
python3 -B "$L/.ufo/waves/round-58/w1/ExecLedgerBuild.files/build_ledger.py" --root "$C" \
  --revision "$T3" --note 'see {path}' --out "$C/.ufo/waves/round-58/receipt-rewrites.json"
git -C "$C" add -- .ufo/waves/round-58/receipt-rewrites.json
T4=$(commit "round-58 dry run: T4 disclose the census rewrite")
log "T4=$T4"
run "$T4" T4 | tee "$LOG/step7-T4.txt"

log "STEP 8: historical (round-57) receipt rewrite, disclosed, on a branch from T1 (must stay met)"
git -C "$C" checkout -q -B dry-hist "$T1"
printf 'dry-run post-commit rewrite of a round-57 receipt\n' >> "$C/.ufo/waves/round-57/controls/after-c1-receipt-pins.txt"
git -C "$C" add -- .ufo/waves/round-57/controls/after-c1-receipt-pins.txt
T5=$(commit "round-58 dry run: rewrite a round-57 receipt")
python3 -B "$L/.ufo/waves/round-58/w1/ExecLedgerBuild.files/build_ledger.py" --root "$C" \
  --revision "$T5" --note 'see {path}' --out "$C/.ufo/waves/round-58/receipt-rewrites.json"
git -C "$C" add -- .ufo/waves/round-58/receipt-rewrites.json
T6=$(commit "round-58 dry run: ledger re-issued with the new event")
log "T5=$T5 T6=$T6"
run "$T6" T6 | tee "$LOG/step8-T6.txt"

log "STEP 9: same tree, ledger left stale (must fail undisclosed=1)"
git -C "$C" revert --no-edit -q "$T6" >/dev/null 2>&1 || git -C "$C" "${ID[@]}" commit -q --allow-empty -m noop
echo "revert head: $(git -C "$C" rev-parse HEAD)"

log "SUMMARY"
for f in step0-base step2-T0 step3-T1 step4-T1b step5-T2 step6-T3 step7-T4 step8-T6; do
  printf '%-12s %s | %s\n' "$f" "$(grep -m1 '^C1 receipt-rewrites' "$LOG/$f.txt" | sed -E 's/  \(met:.*//')" "$(grep -m1 '^EXITCODE=' "$LOG/$f.txt")"
done
git -C "$C" log --oneline -12 dry
