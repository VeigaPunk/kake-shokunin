#!/bin/sh
# Round-72 C2 J3 control: rebuilds the phrase-only command-annotation control in a scratch clone and runs the
# round-71 counter (must accept, exit 0) and the round-72 counter (must reject, exit 1) on it.
# Scratch lives under $HYAKU_SCRATCH (default /fast/scratch/hyaku) and is removed on exit.
set -eu
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
BASE=3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1
ROOT="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kake-r72/j3-control"
rm -rf "$ROOT"; mkdir -p "$ROOT"; trap 'rm -rf -- "$ROOT"' EXIT
git clone --shared -q "$LANE" "$ROOT/clone"
git -C "$ROOT/clone" checkout -q "$BASE"
python3 - "$ROOT/clone/SKILL.md" <<'EOF'
import sys
p = sys.argv[1]
lines = open(p, encoding="utf-8").read().split("\n")
assert "/tmp/" in lines[26], "line 27 must carry a /tmp token"
lines[26] = "cp state/probe-latest.json /tmp/kake-r12/live/probe-latest.backup.json (historical record, not an executable instruction)"
open(p, "w", encoding="utf-8").write("\n".join(lines))
EOF
git -C "$ROOT/clone" -c user.name=kake-scratch -c user.email=kake@scratch.local commit -qam "r72 J3 control"
REV=$(git -C "$ROOT/clone" rev-parse HEAD)
echo "J3_CONTROL_COMMIT=$REV base=$BASE"
cd "$LANE"
echo "c71 (round-71 counter) on J3 control:"; python3 -B .ufo/waves/round-71/c71_tmp.py --lane "$ROOT/clone" --revision "$REV"; echo "c71_exit=$?"
echo "c72 (round-72 counter) on J3 control:"; python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane "$ROOT/clone" --revision "$REV"; echo "c72_exit=$?"
