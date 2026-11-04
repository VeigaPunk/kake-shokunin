#!/usr/bin/env bash
# Round-91 pre-freeze controls: do-nothing, junk and forgery controls for the two
# frozen counters (c91_defects.py, c91_reuse.py), plus one reachability control.
# Every fixture commit happens in a scratch clone ($D), never in the lane.
# Receipts land in .ufo/waves/round-91/controls/. Last line: `controls ok PASS/TOTAL`.
set -u
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kake-shokunin}
R91=$LANE/.ufo/waves/round-91
OUT=$R91/controls
BASE=5b20af16661040f383e9e84f85b838619857cb14
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kake-r91/L1/controls-$$
rm -rf "$SCR"; mkdir -p "$SCR"
PASS=0; TOTAL=0
check() {
  TOTAL=$((TOTAL + 1))
  if [ "$2" = "$3" ]; then PASS=$((PASS + 1)); else echo "MISMATCH $1 want=$2 got=$3"; fi
}
reading() { head -1 "$1" | grep -oE 'met=(true|false)'; }  # first line only: the JSON detail quotes per-subject lines
D=$SCR/fx
git clone -q --shared "$LANE" "$D" || { echo "controls fail: clone"; exit 9; }
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "controls fail: toplevel"; exit 9; }
git -C "$D" checkout -q --detach "$BASE"
G() { git -C "$D" -c user.name=fixture -c user.email=fixture@scratch.invalid "$@"; }
RC=0
C1() { local f=$1; shift; python3 -B "$R91/c91_defects.py" --root "$1" --revision "$2" --work "$SCR/w" > "$f" 2>&1; RC=$?; }
C2() { local f=$1; shift; python3 -B "$R91/c91_reuse.py" --root "$1" --revision "$2" --candidate "$3" --work "$SCR/w" --seed 91091 > "$f" 2>&1; RC=$?; }

{
  echo "## c1-do-nothing (lane at base: no successor counter, no mutation receipt, old script)"
  C1 "$SCR/o1" "$LANE" "$BASE"
  cat "$SCR/o1"
  check c1-do-nothing met=false "$(reading "$SCR/o1")"
  check c1-do-nothing-exit 1 "$RC"

  echo "## c1-junk (frozen bytes committed, junk receipt, junk script, no execution)"
  mkdir -p "$D/.ufo/waves/round-91"
  cp -r "$R91/frozen" "$R91/c91_defects.py" "$R91/c91_reuse.py" "$R91/c2-contract.md" "$D/.ufo/waves/round-91/"
  mkdir -p "$D/.ufo/waves/round-91/integration"
  printf 'gate_sha256=%064d mutants=21 killed=20 survivors=1 met=true\n' 0 > "$D/.ufo/waves/round-91/integration/mutation-tip.txt"
  printf '#!/usr/bin/env bash\nLANE=${LANE:-.}\necho "controls ok 9/9"\nexit 0\n' > "$D/.ufo/waves/round-90/controls/run_controls.sh"
  G add -A && G commit -qm "fx junk"
  JUNK=$(git -C "$D" rev-parse HEAD)
  C1 "$SCR/o2" "$D" "$JUNK"
  cat "$SCR/o2"
  check c1-junk met=false "$(reading "$SCR/o2")"
  check c1-junk-exit 1 "$RC"
} > "$OUT/ctl-c1.txt" 2>&1

{
  echo "## c2-do-nothing (lane at base: no candidate tool)"
  C2 "$SCR/c2-do-nothing" "$LANE" "$BASE" scripts/stored_reuse.py
  cat "$SCR/c2-do-nothing"
  check c2-do-nothing met=false "$(reading "$SCR/c2-do-nothing")"
  check c2-do-nothing-exit 1 "$RC"

  echo "## c2-forgeries (each frozen forgery subject scored as the candidate)"
  for f in neg-pin-reader neg-allowlist neg-blanket-refuse neg-blanket-admit neg-hash-table; do
    C2 "$SCR/o4" "$D" "$JUNK" ".ufo/waves/round-91/frozen/$f.py"
    echo "--- $f"; cat "$SCR/o4"
    check "c2-$f" met=false "$(reading "$SCR/o4")"
    check "c2-$f-exit" 1 "$RC"
  done

  echo "## c2-reachability (the counter's own reference, wrapped; a control, not the shipped tool)"
  mkdir -p "$D/.ufo/waves/round-91/controls"
  cp "$R91/controls/reference-candidate.py" "$D/.ufo/waves/round-91/controls/reference-candidate.py"
  G add -A && G commit -qm "fx reference candidate"
  REF=$(git -C "$D" rev-parse HEAD)
  C2 "$SCR/o5" "$D" "$REF" ".ufo/waves/round-91/controls/reference-candidate.py"
  cat "$SCR/o5"
  check c2-reachability met=true "$(reading "$SCR/o5")"
  check c2-reachability-exit 0 "$RC"
} > "$OUT/ctl-c2.txt" 2>&1

rm -rf "$SCR"
echo "controls ok $PASS/$TOTAL"
[ "$PASS" = "$TOTAL" ]
