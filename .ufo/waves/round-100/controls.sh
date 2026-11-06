#!/usr/bin/env bash
# Round-100 pre-freeze controls. Usage: controls.sh <lane> <instruments-rev> <scratch>
# Every fixture commit lives in a scratch clone; the lane is never written except the
# receipts under .ufo/waves/round-100/controls/.
set -u
L=$1; REV=$2; S=$3
W=$L/.ufo/waves/round-100; C=$W/controls
mkdir -p "$C" "$S"
trap 'rm -rf -- "$S"' EXIT
rcpt() { # name, command...
  local n=$1; shift
  { echo "\$ $*"; "$@"; echo "exit=$?"; } > "$C/$n.txt" 2>&1
  echo "$n: $(grep -m1 -E 'met=|selftest [0-9]' "$C/$n.txt") $(tail -1 "$C/$n.txt")"
}
# ---- C1
rcpt ctl-c1-selftest python3 -B "$W/c100_registry.py" --selftest --work "$S/st"
rcpt base-c1 python3 -B "$W/c100_registry.py" --root "$L" --revision "$REV" --work "$S/b"
for mode in pos deleteall keepold everycode; do
  D=$S/fx-$mode
  git clone -q --shared "$L" "$D"
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "fixture root mismatch"; exit 2; }
  git -C "$D" checkout -q --detach "$REV"
  python3 -B "$W/c1_repair_fixture.py" "$D/SKILL.md" "$mode" || { echo "fixture $mode failed"; exit 2; }
  git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -am "fixture $mode"
  sha256sum "$D/SKILL.md" | cut -d' ' -f1 > "$C/fixture-c1-$mode-SKILL.sha256"
  rcpt ctl-c1-$mode python3 -B "$W/c100_registry.py" --root "$D" --revision HEAD --work "$S/w-$mode"
  rm -rf -- "$D"
done
# ---- C2
rcpt ctl-c2-selftest python3 -B "$W/c100_fresh304.py" --selftest
rcpt base-c2 python3 -B "$W/c100_fresh304.py" --root "$L" --revision "$REV" --work "$S/c2b"
for f in "$W"/frozen/*.py; do
  n=$(basename "$f" .py)
  rcpt ctl-c2-$n python3 -B "$W/c100_fresh304.py" --candidate-file "$f" --work "$S/c2-$n"
done
( cd "$W" && sha256sum c100_registry.py c100_fresh304.py fresh304-contract-v2.md build_frozen.py c1_repair_fixture.py controls.sh frozen/*.py ) > "$C/instrument-sha256.txt"
echo done
