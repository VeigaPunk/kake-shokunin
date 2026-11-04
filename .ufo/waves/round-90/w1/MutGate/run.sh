#!/bin/bash
S=/fast/scratch/hyaku/kake-r90/MutGate; D=$S/fx.g5QC
n=$1; rev=$2
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/c90_gate.py --root $D --revision $rev --work $S/work/$n --jobs 4 > $S/runs/$n.out 2> $S/runs/$n.err
echo "rc=$?" >> $S/runs/$n.out
