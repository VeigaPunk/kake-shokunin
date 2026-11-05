#!/usr/bin/env bash
# Round-99 pre-freeze controls. Usage: controls.sh <lane-root> <base-rev> <repair-section.md> <scratch>
# C1 forgeries are committed in a SCRATCH clone only (fixture identity, -C "$CL" on every git call).
set -u
L=$1; BASE=$2; SEC=$3; SCR=$4
W=$L/.ufo/waves/round-99; C=$W/controls
mkdir -p "$C" "$SCR"
CL=$SCR/clone
rm -rf "$CL"
git clone -q --shared "$L" "$CL"
[ "$(git -C "$CL" rev-parse --show-toplevel)" = "$CL" ] || { echo "fixture root mismatch"; exit 2; }
c1() { # name skill-file
  git -C "$CL" checkout -q --detach "$BASE"
  cp "$2" "$CL/SKILL.md"
  git -C "$CL" -c user.name=fixture -c user.email=fixture@invalid commit -q -am "fixture $1"
  local rev; rev=$(git -C "$CL" rev-parse HEAD)
  { echo "# control $1 fixture-commit $rev (scratch clone; base $BASE)"
    python3 -B "$W/c99_registry.py" --root "$CL" --revision "$rev" --work "$SCR/w-$1"; echo "exit=$?"; } > "$C/ctl-c1-$1.txt" 2>&1
}
B=$SCR/base-skill.md; git -C "$L" show "$BASE:SKILL.md" > "$B"
{ python3 -B "$W/c99_registry.py" --root "$L" --revision "$BASE" --work "$SCR/w-base"; echo "exit=$?"; } > "$C/base-c1.txt" 2>&1
{ python3 -B "$W/c99_registry.py" --selftest --work "$SCR/w-st"; echo "exit=$?"; } > "$C/ctl-c1-selftest.txt" 2>&1
# positive: the repair section appended
cat "$B" "$SEC" > "$SCR/pos.md"; c1 pos "$SCR/pos.md"
# f1 names-only rows under a conformant header
{ cat "$B"; printf '\n| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner |\n|---|---|---|---|---|---|---|\n';
  grep -oE '^\| [A-Za-z0-9_.-]+\.(py|mjs) ' "$SEC" | sed -E 's/^\| ([^ ]+) /| scripts\/\1 | | | | | | |/'; } > "$SCR/f1.md"; c1 namesonly "$SCR/f1.md"
# f2 the real rows inside a fenced block
{ cat "$B"; echo '```'; cat "$SEC"; echo '```'; } > "$SCR/f2.md"; c1 fenced "$SCR/f2.md"
# f3 every "no self-test" cell replaced by a --selftest command the tool does not have
python3 - "$SEC" > "$SCR/f3sec.md" <<'EOF'
import re, sys
out = []
for line in open(sys.argv[1]):
    if line.startswith("| ") and "no self-test" in line:
        cells = line.split(" | ")
        name = cells[0][2:]
        line = re.sub(r"no self-test[^|]*", "`python3 -B scripts/%s --selftest` " % name, line, count=1)
    out.append(line)
sys.stdout.write("".join(out))
EOF
cat "$B" "$SCR/f3sec.md" > "$SCR/f3.md"; c1 falseselftest "$SCR/f3.md"
# f4 junk prose in well-formed rows (declared counter limit: expected met=true; only the review conjunct catches it)
python3 - "$SEC" > "$SCR/f4sec.md" <<'EOF'
import sys
out = []
for line in open(sys.argv[1]):
    if line.startswith("| ") and "| kake |" in line and not line.startswith("| Name"):
        c = line.rstrip("\n").split(" | ")
        c[1] = "lorem"; c[3] = "`0` ipsum; `1` dolor"; c[5] = "nowhere"
        line = " | ".join(c) + "\n"
    out.append(line)
sys.stdout.write("".join(out))
EOF
cat "$B" "$SCR/f4sec.md" > "$SCR/f4.md"; c1 junkprose "$SCR/f4.md"
# f5 owner forged to a sibling lane
sed -E 's/\| kake \|$/| kaidoku |/' "$SEC" > "$SCR/f5sec.md"; cat "$B" "$SCR/f5sec.md" > "$SCR/f5.md"; c1 wrongowner "$SCR/f5.md"
# C2
{ python3 -B "$W/c99_fresh304.py" --root "$L" --revision "$BASE" --work "$SCR/w2"; echo "exit=$?"; } > "$C/base-c2.txt" 2>&1
{ python3 -B "$W/c99_fresh304.py" --selftest; echo "exit=$?"; } > "$C/ctl-c2-selftest.txt" 2>&1
for f in "$W"/frozen/*.py; do n=$(basename "$f" .py)
  { python3 -B "$W/c99_fresh304.py" --root "$L" --revision "$BASE" --candidate-file "$f" --work "$SCR/w2"; echo "exit=$?"; } > "$C/ctl-c2-$n.txt" 2>&1
done
sha256sum "$W/c99_registry.py" "$W/c99_fresh304.py" "$W/fresh304-contract.md" "$W"/frozen/*.py | sed "s#$L/##" > "$C/instrument-sha256.txt"
for f in "$C"/*.txt; do printf '%s: ' "$(basename "$f")"; grep -E 'met=|exit=|selftest' "$f" | grep -vE '^(ok|fail) ' | tr '\n' ' '; echo; done
rm -rf "$CL"
