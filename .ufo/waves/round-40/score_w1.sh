#!/bin/sh
# Round-40: the L1 re-scores every control tool a wave-1 seat returned, with the frozen counter.
# Usage: score_w1.sh <Seat> <tool-path>...   (copies each tool into controls/w1/<Seat>/ first)
set -u
L=/home/vgpnk/Projects/shokunin/kake-shokunin
W=$L/.ufo/waves/round-40
seat=$1; shift
mkdir -p "$W/controls/w1/$seat" "$W/verification/w1"
for t in "$@"; do
  base=$(basename "$t" .py)
  cp "$t" "$W/controls/w1/$seat/$base.py"
  timeout 1500 python3 -B "$W/c1_count.py" --root "$L" --tool-file "$W/controls/w1/$seat/$base.py" \
    --label "w1-$seat-$base" --out "$W/verification/w1/${seat}__${base}.json"
  echo "exit=$? $seat $base"
done
