#!/usr/bin/env bash
# Round 42: the L1 re-scores every returned control tool with counter v3 (frozen bytes, sha256 ce2d5a0c...).
# Usage: score_v3.sh <list>   (no --seed: each run draws its seed from os.urandom, recorded in the receipt)   list lines: <Seat> <suffix> <absolute tool path>
# Copies each tool to controls/w1/<Seat>/<suffix>.py and writes verification/w1v3/<Seat>__<suffix>.json.
set -u
L=/home/vgpnk/Projects/shokunin/kake-shokunin
W=$L/.ufo/waves/round-42
LIST=$1
SEED=urandom
mkdir -p "$W/controls/w1" "$W/verification/w1v3"
while read -r seat suffix path; do
  [ -z "${seat:-}" ] && continue
  mkdir -p "$W/controls/w1/$seat"
  cp "$path" "$W/controls/w1/$seat/$suffix.py"
  printf '%s\t%s\n' "$seat" "$suffix"
done < "$LIST" | xargs -P 6 -L 1 bash -c '
  W='"$W"'; L='"$L"'
  timeout 1200 prlimit --as=8000000000 -- python3 -B "$W/c42_count_v3.py" --root "$L" \
    --tool-file "$W/controls/w1/$0/$1.py" --label "$0-$1" \
    --out "$W/verification/w1v3/$0__$1.json" > /dev/null 2>&1
  echo "$0 $1 exit=$?"'
