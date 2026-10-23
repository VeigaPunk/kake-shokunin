#!/bin/sh
# Round-41: the L1 re-scores control tools with the frozen counter.
# Usage: score.sh <set> <Seat> <tool-path>...   (copies each tool into controls/<set>/<Seat>/ first;
# receipts go to verification/<set>/<Seat>__<tool>.json). Dead seats are never scored.
set -u
L=/home/vgpnk/Projects/shokunin/kake-shokunin
W=$L/.ufo/waves/round-41
set_=$1; seat=$2; shift 2
mkdir -p "$W/controls/$set_/$seat" "$W/verification/$set_"
for t in "$@"; do
  base=$(basename "$t" .py)
  [ "$t" = "$W/controls/$set_/$seat/$base.py" ] || cp "$t" "$W/controls/$set_/$seat/$base.py"
  timeout 900 python3 -B "$W/c1_count.py" --root "$L" --tool-file "$W/controls/$set_/$seat/$base.py" \
    --label "$set_-$seat-$base" --out "$W/verification/$set_/${seat}__${base}.json"
  echo "exit=$? $seat $base"
done
