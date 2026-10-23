#!/bin/bash
# Score the private reference and each of its 34 ablations with the frozen C1 counter.
set -u
P=/fast/scratch/hyaku/kake-r37/private
L=/home/vgpnk/Projects/shokunin/kake-shokunin
V=$L/.ufo/waves/round-37/verification/ablations
ABLS=$(python3 -c "import json;print(' '.join(json.load(open('$P/ablation-pre.json'))))")
run() {
  a=$1
  sed "s/^ABL = set(filter(None, os.environ.get(\"KAKE_ABLATE\", \"\").split(\",\")))/ABL = {\"$a\"}/" $P/ref.py > $P/abl/ref-$a.py
  timeout 900 python3 -B $L/.ufo/waves/round-37/sealed_count.py --root $L --tool-file $P/abl/ref-$a.py --key-file $P/cases.json > $V/ablation-$a.json; echo $? > $V/ablation-$a.exit
}
export -f run; export P L V
printf '%s\n' $ABLS | xargs -P 8 -I{} bash -c 'run {}'
timeout 900 python3 -B $L/.ufo/waves/round-37/sealed_count.py --root $L --tool-file $P/ref.py --key-file $P/cases.json > $V/reference.json; echo $? > $V/reference.exit
