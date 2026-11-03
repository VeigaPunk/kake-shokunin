#!/usr/bin/env bash
# Held-out fixture harness for c74_registry_gap.py — ReviewerC1, kake round 74 w1.
# Usage: run-against-fixtures.sh [PATH-TO-COUNTER] [WORKDIR]
# Read-only over the lane; all writes go to the per-fixture throwaway repos.
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
COUNTER=${1:-$LANE/.ufo/waves/round-74/c74_registry_gap.py}
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=${2:-$(mktemp -d)}
mkdir -p "$WORK"
trap 'rm -rf -- "$WORK"' EXIT
POP=(
  .ufo/waves/round-69/c69_recorded_counts.py
  .ufo/waves/round-69/c69_tmp_honour.py
  .ufo/waves/round-70/c70_pointer_audit.py
  .ufo/waves/round-71/c71_calibration.py
  .ufo/waves/round-71/c71_tmp.py
  .ufo/waves/round-72/c72_tmp_v2.py
  .ufo/waves/round-73/c73_tmp_v3.py
  .ufo/waves/round-73/c73_wave_pointers.py
)
if [ ! -f "$COUNTER" ]; then
  echo "NOT_RUN: counter absent: $COUNTER"
  exit 3
fi
for fx in "$HERE"/f[0-9][0-9]-*.md; do
  name=$(basename "$fx" .md)
  D=$(mktemp -d "$WORK/$name.XXXXXX")
  git -C "$D" init -q || exit 4
  top=$(git -C "$D" rev-parse --show-toplevel)
  [ "$top" = "$D" ] || { echo "FATAL: toplevel $top != $D"; exit 5; }
  cp "$fx" "$D/SKILL.md"
  for p in "${POP[@]}"; do
    mkdir -p "$D/$(dirname "$p")"
    printf '# population stub\n' > "$D/$p"
  done
  git -C "$D" add SKILL.md "${POP[@]}"
  git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -qm "fixture $name"
  rev=$(git -C "$D" rev-parse HEAD)
  echo "== $name rev=$rev"
  python3 -B "$COUNTER" --root "$D" --revision "$rev" --json
  echo "exit=$?"
done
