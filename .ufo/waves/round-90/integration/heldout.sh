#!/usr/bin/env bash
# Round-90 integration: score the working gate on every wave-authored subject (held out from
# the frozen population). Usage: heldout.sh <gate.py> <seed>; prints one line per subject.
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
W1=$LANE/.ufo/waves/round-90/w1
GATE=${1:-$LANE/scripts/cache_key_conformance.py}; SEED=${2:-4242}
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kake-r90/L1/heldout; rm -rf "$SCR"; mkdir -p "$SCR"
trap 'rm -rf -- "$SCR"' EXIT
pos="$LANE/scripts/cache_key.py $LANE/.ufo/waves/round-89/w1/L1/cache_key.py $LANE/.ufo/waves/round-89/w1/MutKey/mutants/M33-header-name-casefold.py $LANE/.ufo/waves/round-89/w1/MutKey/mutants/M36-duplicate-member-deduped.py $W1/ReviewGate/mine.py $W1/ReviewGate/mine_nonl.py $W1/ReviewGate/mine_strictjson.py $W1/ReviewGate/mine_tb.py"
neg="$(ls $W1/ExecStubs/stubs/*.py $W1/ExecSandbox/c*.py $W1/ScoutGround/*.py $W1/ReviewGate/forge_forkexec.py $W1/CriticClaims/probes/*.py $LANE/.ufo/waves/round-90/frozen/neg-*.py 2>/dev/null)"
run() { python3 -B "$GATE" --candidate "$1" --seed "$SEED" --work "$SCR" --jobs 8 2>&1 | tail -2 | tr '\n' ' '; }
for c in $pos; do printf 'POS %s %s\n' "${c#$LANE/}" "$(run "$c")"; done
for c in $neg; do printf 'NEG %s %s\n' "${c#$LANE/}" "$(run "$c")"; done
