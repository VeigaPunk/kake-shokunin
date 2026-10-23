#!/bin/sh
# Score one control tool file with the frozen round-38 counter (L1 only; key outside the lane).
# Usage: score_control.sh NAME TOOLFILE  -> verification/control-NAME.json and .exit
set -u
L=/home/vgpnk/Projects/shokunin/kake-shokunin
V=$L/.ufo/waves/round-38/verification
cd "$L" || exit 2
python3 -B .ufo/waves/round-38/sealed_count.py --root . --tool-file "$2" \
  --key-file /fast/scratch/hyaku/kake-r38/private/cases.json > "$V/control-$1.json"
echo $? > "$V/control-$1.exit"
mkdir -p .ufo/waves/round-38/retained/controls
cp "$2" ".ufo/waves/round-38/retained/controls/$1.py"
printf '%s exit=%s passed=%s met=%s\n' "$1" "$(cat "$V/control-$1.exit")" \
  "$(jq -r .passed "$V/control-$1.json")" "$(jq -r .met "$V/control-$1.json")"
