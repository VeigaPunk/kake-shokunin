#!/bin/bash
# mkroute.sh NAME ROUND  -- creates a fixture synthetic lane for one route.
set -e
NAME="$1"
S=/fast/scratch/hyaku/kake-r95/ReviewC1/fixtures
FX="$S/$NAME"
rm -rf "$FX"
mkdir -p "$FX/lane/corpus/lessons" "$FX/lane/corpus/knowledge"
D="$FX/lane"
git -C "$D" init -q
git -C "$D" config user.email reviewc1@example.invalid
git -C "$D" config user.name reviewc1
assert_top() { [ "$(git -C "$D" rev-parse --show-toplevel)" = "$(mkdir -p "$D"; readlink -f "$D")" ] || { echo 'FAIL: not at repo root'; exit 1; }; }
assert_top
echo "fixture $NAME ready at $D"
