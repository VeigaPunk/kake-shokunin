#!/usr/bin/env bash
# Round-57 C1 landing sequence (dry-run verified by ExecC1Dryrun).
# Usage: landing.sh [scratch-dir]      (default: mktemp -d)
# Env:   LANE (default /home/vgpnk/Projects/shokunin/kake-shokunin), FLEET (default /home/vgpnk/Projects/shokunin),
#        BUILD (default 4b8c73050470ada9e6583f3b12d659d1bed6a17f).
# Writes only inside the scratch clone. Prints X, T0, TIP and each counter's printed output.
set -euo pipefail

LANE=${LANE:-/home/vgpnk/Projects/shokunin/kake-shokunin}
FLEET=${FLEET:-/home/vgpnk/Projects/shokunin}
BUILD=${BUILD:-4b8c73050470ada9e6583f3b12d659d1bed6a17f}
D=${1:-$(mktemp -d)}
W=.ufo/waves/round-57
C=$W/controls

git clone -q --no-checkout "$LANE" "$D"
git -C "$D" checkout -q "$BUILD"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "refusing: $D is not a scratch toplevel" >&2; exit 1; }
G=(git -C "$D" -c user.name=selftest -c user.email=selftest@local -c commit.gpgsign=false)
echo "D=$D"

# ---- (1) stand-in content revision X -------------------------------------------------
"${G[@]}" commit -q --allow-empty -m "stand-in content revision X"
X=$(git -C "$D" rev-parse HEAD)
echo "X=$X"

# ---- (2) measure at X, write measured.json + SCORECARD pin + c2/c3 receipts, commit T0 --
mkdir -p "$D/$C"
set +e
python3 -B "$D/$W/c57_idresolver_gate.py" --root "$D" --revision "$X" --fleet "$FLEET" > "$D/.c2.out"
C2=$?
python3 -B "$D/$W/c57_quote_truth.py" --root "$D" --revision "$X" > "$D/.c3.out"
C3=$?
set -e
echo "--- C2 at X (exit $C2) ---"; cat "$D/.c2.out"
echo "--- C3 at X (exit $C3) ---"; cat "$D/.c3.out"
[ "$C2" = 0 ] && [ "$C3" = 0 ] || { echo "claim counter did not report met at X; stop" >&2; exit 1; }
{ cat "$D/.c2.out"; echo "EXIT=$C2"; } > "$D/$C/after-c2-idresolver.txt"
{ cat "$D/.c3.out"; echo "EXIT=$C3"; } > "$D/$C/after-c3-quote-truth.txt"
printf '{"revision": "%s"}\n' "$X" > "$D/$W/measured.json"
# after-c1 placeholder: pin-only content; its body is rewritten at the tip (see step 3)
printf 'revision: %s\npending: replaced at the tip with the run at T0\nEXIT=0\n' "$X" \
  > "$D/$C/after-c1-receipt-pins.txt"
printf '\n## Round 57 — declared and measured claims\n\nMeasured revision: %s\n' "$X" >> "$D/SCORECARD.md"
"${G[@]}" add -A
"${G[@]}" commit -q -m "round-57: measured revision X, c2/c3 receipts, C1 placeholder"
T0=$(git -C "$D" rev-parse HEAD)
echo "T0=$T0"

# ---- (3) the C1 receipt for T0; commit; then verify at the tip -----------------------
# A fresh after-c1 cannot pass its own body check at the commit that introduces it (its `tip:` must be a
# strict ancestor that already holds all three receipts), so C1 run at T0 prints met=False. The receipt's
# first line is the counter's own re-derivation at T0 with the body check off; the tip run must print
# exactly that line again, which is the assertion below.
set +e
python3 -B "$D/$W/c57_receipt_pins.py" --root "$D" --revision "$T0"
set -e
DERIVED=$(python3 -B - "$D" "$T0" <<'PY'
import importlib.util, sys
root, tip = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("c57_receipt_pins", root + "/.ufo/waves/round-57/c57_receipt_pins.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
v = m.measure(root, tip, check_bodies=False)
print(m.report_first_line(v))
sys.exit(0 if v["met"] else 1)
PY
)
echo "--- C1 line re-derived at T0 ---"; printf '%s\n' "$DERIVED"
{ printf '%s\n' "$DERIVED"
  printf '  tip: %s\n' "$T0"
  printf '  revision: %s\n' "$X"
  echo "EXIT=0"; } > "$D/$C/after-c1-receipt-pins.txt"
"${G[@]}" add -A
"${G[@]}" commit -q -m "round-57: C1 receipt is the run at T0"
TIP=$(git -C "$D" rev-parse HEAD)
echo "TIP=$TIP"

# ---- (4) verify at the tip -----------------------------------------------------------
set +e
OUT2=$(python3 -B "$D/$W/c57_receipt_pins.py" --root "$D" --revision "$TIP")
P2=$?
set -e
printf '%s\n' "$OUT2"
echo "C1_EXIT=$P2"
[ "$P2" = 0 ] || { echo "C1 not met at the tip" >&2; exit 1; }
[ "$(printf '%s\n' "$OUT2" | head -n 1)" = "$DERIVED" ] || { echo "tip first line differs from the receipt body line" >&2; exit 1; }
echo "LANDED X=$X T0=$T0 TIP=$TIP"
