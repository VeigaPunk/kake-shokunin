#!/bin/bash
# Retain a control seat's C1 tool in the lane and score it with the frozen C1 counter (key file outside the lane).
# Usage: score_control.sh <SeatName>
set -u
N=$1
L=/home/vgpnk/Projects/shokunin/kake-shokunin
R=$L/.ufo/waves/round-37/retained/controls
V=$L/.ufo/waves/round-37/verification
mkdir -p $R
cp /fast/scratch/hyaku/kake-r37/ctl/$N/robots_audit.py $R/$N-robots_audit.py
timeout 900 python3 -B $L/.ufo/waves/round-37/sealed_count.py --root $L --tool-file $R/$N-robots_audit.py --key-file /fast/scratch/hyaku/kake-r37/private/cases.json > $V/control-$N.json
echo $? > $V/control-$N.exit
python3 -c "import json;d=json.load(open('$V/control-$N.json'));print('$N', d.get('passed'), d.get('met'), d.get('toolSha256'), d.get('error'))"
