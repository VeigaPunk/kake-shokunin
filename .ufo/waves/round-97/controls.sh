#!/usr/bin/env bash
# Round-97 pre-freeze controls. Usage: controls.sh <instruments-rev>
# Every run goes through the counters' public CLI on committed revisions.
# Scratch under $HYAKU_SCRATCH/kake-r97/controls; receipts into controls/.
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
W=$LANE/.ufo/waves/round-97
C=$W/controls
REV=${1:?instruments revision}
BASE=36d148f5c60100021304903c30e5663207c72f4f
R96BASE=bde9869144f69c5a459c0d2c93f5135922fe3a8d
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kake-r97/controls
rm -rf -- "$S"; mkdir -p "$S" "$C"
trap 'rm -rf -- "$S"' EXIT
export TMPDIR=$S
G=/usr/bin/git
rec() { # name cmd...
  local n=$1; shift
  { echo "# cmd: $*"; "$@"; echo "exit=$?"; } > "$C/$n.txt" 2>&1
}
# fixture clone with one commit applying a change script; prints new rev
fixture() { # dir change-fn
  local D=$S/$1
  $G clone -q --shared "$LANE" "$D"
  $G -C "$D" checkout -q --detach "$REV"
  [ "$($G -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch"; exit 9; }
  ( cd "$D" && "$2" )
  $G -C "$D" add -A
  $G -C "$D" -c user.name=c97-fixture -c user.email=fixture@c97.invalid commit -qm "control $1"
  $G -C "$D" rev-parse HEAD
}

# ---------------- C1
rec ctl-c1-selftest python3 -B "$W/c97_index.py" --selftest --work "$S"
rec base-c1 python3 -B "$W/c97_index.py" --root "$LANE" --revision "$BASE" --work "$S"
rec instr-c1 python3 -B "$W/c97_index.py" --root "$LANE" --revision "$REV" --work "$S"
UNIDX=$(python3 -B "$W/c97_index.py" --root "$LANE" --revision "$REV" --work "$S" | sed -n 2p \
  | python3 -c 'import sys,json;print(" ".join(json.load(sys.stdin)["unindexed"]))')
c1_pathonly() { { echo; echo "| Area | Entry | Coverage |"; echo "|---|---|---|";
  for e in $UNIDX; do echo "| x | \`knowledge/$e\` | y |"; done; } >> corpus/README.md; }
c1_fenced() { { echo; echo '```'; echo "| Area | Entry | Coverage |"; echo "|---|---|---|";
  for e in $UNIDX; do ids=$(sed -n '1,15{/^source:/p}' "corpus/knowledge/$e" | grep -oE 'S[0-9]{3,}' | sort -u | tr '\n' ' ');
    echo "| Index | \`knowledge/$e\` ($ids) | $(tr -cs 'A-Za-z' ' ' < corpus/knowledge/$e | tr 'A-Z' 'a-z' | tr ' ' '\n' | awk 'length>=6' | sort -u | head -8 | tr '\n' ' ') |"; done; echo '```'; } >> corpus/README.md; }
c1_shuffle() { { echo; echo "| Area | Entry | Coverage |"; echo "|---|---|---|";
  for e in $UNIDX; do ids=$(sed -n '1,15{/^source:/p}' "corpus/knowledge/$e" | grep -oE 'S[0-9]{3,}[–-]?S?[0-9]*' | sort -u | tr '\n' ' ');
    echo "| Index | \`knowledge/$e\` ($ids) | $(tr -cs 'A-Za-z' ' ' < corpus/knowledge/$e | tr 'A-Z' 'a-z' | tr ' ' '\n' | awk 'length>=6' | sort -u | head -8 | tr '\n' ' ') |"; done; } >> corpus/README.md; }
for f in pathonly fenced shuffle; do
  R=$(fixture c1-$f c1_$f)
  rec ctl-c1-forgery-$f python3 -B "$W/c97_index.py" --root "$S/c1-$f" --revision "$R" --work "$S"
done

# ---------------- C2
# do-nothing instrument: the frozen round-96 counter on the instruments revision
rec c2-predecessor-at-instr python3 -B "$LANE/.ufo/waves/round-96/c96_reval.py" --root "$LANE" --revision "$REV" --work "$S/p96"
rec c2-predecessor-at-base python3 -B "$LANE/.ufo/waves/round-96/c96_reval.py" --root "$LANE" --revision "$BASE" --work "$S/p96b"
# successor at the round-96 base (candidate absent; round-97 forgery absent -> population drift, fail closed)
rec c2-successor-at-r96base python3 -B "$W/c97_reval.py" --root "$LANE" --revision "$R96BASE" --work "$S/r96b"
rec ctl-c2-selftest python3 -B "$W/c97_reval.py" --selftest --work "$S/sel"
# main-path proofs (R96-A): frozen subjects placed in the candidate slot, committed
c2_pos() { cp .ufo/waves/round-96/frozen/pos-good-reval.py scripts/reval_exchange.py; }
c2_table() { cp .ufo/waves/round-97/frozen/neg-lookup-table.py scripts/reval_exchange.py; }
c2_oracle() { cp .ufo/waves/round-96/frozen/neg-oracle-import.py scripts/reval_exchange.py; }
c2_absent() { rm -f scripts/reval_exchange.py; }
for f in pos table oracle absent; do
  R=$(fixture c2-$f c2_$f)
  rec ctl-c2-slot-$f python3 -B "$W/c97_reval.py" --root "$S/c2-$f" --revision "$R" --work "$S/w-$f" &
done
wait
sha256sum "$W/c97_index.py" "$W/c97_reval.py" "$W/frozen/neg-lookup-table.py" "$W/build_lookup.py" "$W/controls.sh" \
  | sed "s#$LANE/##" > "$C/instrument-sha256.txt"
echo "controls done at instruments revision $REV"
