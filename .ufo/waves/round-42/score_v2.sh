#!/usr/bin/env bash
# Round 42: the L1 re-scores every returned control tool with counter v2 (frozen bytes, sha256 01d3fb8d...).
# Usage: score_v2.sh <list> [seed]   list lines: <Seat> <suffix> <absolute tool path>
# Copies each tool to controls/w1/<Seat>/<suffix>.py and writes verification/w1v2/<Seat>__<suffix>.json.
set -u
L=/home/vgpnk/Projects/shokunin/kake-shokunin
W=$L/.ufo/waves/round-42
LIST=$1
SEED=${2:-42201}
mkdir -p "$W/controls/w1" "$W/verification/w1v2"
while read -r seat suffix path; do
  [ -z "${seat:-}" ] && continue
  mkdir -p "$W/controls/w1/$seat"
  cp "$path" "$W/controls/w1/$seat/$suffix.py"
  printf '%s\t%s\n' "$seat" "$suffix"
done < "$LIST" | xargs -P 6 -L 1 bash -c '
  W='"$W"'; L='"$L"'
  timeout 1200 prlimit --as=8000000000 -- python3 -B "$W/c42_count_v2.py" --root "$L" \
    --tool-file "$W/controls/w1/$0/$1.py" --label "$0-$1" --seed '"$SEED"' \
    --out "$W/verification/w1v2/$0__$1.json" > /dev/null 2>&1
  echo "$0 $1 exit=$?"'
