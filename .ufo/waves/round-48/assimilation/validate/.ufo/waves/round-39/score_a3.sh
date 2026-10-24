#!/bin/sh
# Round-39 attempt-3 L1 scorer: scores each returned control/mutant tool with the frozen counter
# (key-file mode; key path private to the L1). Usage: score_a3.sh <seat-sandbox-root> <wave-tag> [Seat...]
# Control copies: .ufo/waves/round-39/a3-controls/<wave-tag>/<Seat>.py (committed with the receipts).
# Mutant copies (near-copies of the private reference): <private>/mutants/<wave-tag>/<Seat>__<M>.py, committed to
#   .ufo/waves/round-39/a3-controls/<wave-tag>-mutants/ only after the build is scored (keeps the reference out of the build seat's reach).
# Receipts: .ufo/waves/round-39/verification/a3/<wave-tag>-<Seat>[__<M>].json
set -u
L=/home/vgpnk/Projects/shokunin/kake-shokunin
SB=$1; TAG=$2; shift 2
PRIV=$(cat "$HOME/.cache/kake-r39a3-priv.path"); KEY=$PRIV/key/cases.json
E=$L/.ufo/waves/round-39/a3-controls/$TAG; M=$PRIV/mutants/$TAG; V=$L/.ufo/waves/round-39/verification/a3
mkdir -p "$E" "$M" "$V"
LST=$(mktemp)
if [ $# -gt 0 ]; then SEATS="$*"; else SEATS=$(cd "$SB" && ls -d */ | tr -d /); fi
for n in $SEATS; do
  d=$SB/$n; [ "$n" = shared ] && continue
  if [ -f "$d/control.py" ]; then cp "$d/control.py" "$E/$n.py"; echo "$TAG-$n $E/$n.py" >> "$LST"; fi
  for m in "$d"/mutants/M*.py; do
    [ -f "$m" ] || continue
    b=$(basename "$m" .py); cp "$m" "$M/${n}__$b.py"; echo "$TAG-${n}__$b $M/${n}__$b.py" >> "$LST"
  done
done
cd "$L" || exit 2
while read -r label f; do
  r=$V/$label.json
  if [ -f "$r" ] && [ "$(jq -r .toolSha256 "$r")" = "$(sha256sum < "$f" | cut -c1-64)" ]; then continue; fi
  echo "$label $f"
done < "$LST" | timeout 3000 xargs -P 8 -L1 sh -c 'python3 -B .ufo/waves/round-39/sealed_count.py --root . --tool-file "$1" --label "$0" --key-file '"$KEY"' --out '"$V"'/"$0".json >/dev/null 2>&1; true'
rm -f "$LST"
for f in "$V"/"$TAG"-*.json; do jq -r '[.label,.passed,.met]|@tsv' "$f"; done | sort -k2 -n -r
