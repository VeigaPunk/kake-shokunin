#!/bin/sh
# Sweep c53_gate_truth.py over EVERY commit reachable from any ref of the lane clone.
# Usage: sh c53-nevergreen-sweep.sh <clone> ; clone must be a scratch --shared clone.
L="$1"; P=.ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py
green=0
for r in $(git -C "$L" rev-list --all); do
  git -C "$L" show "$r:$P" > "$L/$P" 2>/dev/null || continue
  (cd "$L" && env -i PATH=/usr/bin:/bin HOME=/home/vgpnk TMPDIR=/fast/scratch/hyaku/kake-r60/ReviewerC1Relabels/tmpK \
    LANG=C.UTF-8 python3 -B "$P" --revision "$r" >/dev/null 2>&1)
  [ $? -eq 0 ] && { green=$((green+1)); echo "GREEN $r"; }
done
git -C "$L" show 8b33fd248d126b48d838af5c38bc175850f41a09:"$P" > "$L/$P"
echo "green_revisions=$green"
