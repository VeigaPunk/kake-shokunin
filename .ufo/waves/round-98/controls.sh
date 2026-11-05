#!/usr/bin/env bash
# Round-98 pre-freeze controls. Usage: controls.sh <instruments-rev>
# Every run goes through the counters' public CLI on committed revisions.
# Scratch under $HYAKU_SCRATCH/kake-r98/controls; receipts into controls/.
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
FLEET=/home/vgpnk/Projects/shokunin
W=$LANE/.ufo/waves/round-98
C=$W/controls
REV=${1:?instruments revision}
BASE=e51328b63690c8aaa78c9c8f3b87d8735c0ccbf7
FREV=f86740064229897f53212e03ae3b6474dac66de4
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kake-r98/controls
rm -rf -- "$S"; mkdir -p "$S" "$C"
trap 'rm -rf -- "$S"' EXIT
export TMPDIR=$S
G=/usr/bin/git
rec() { # name cmd...
  local n=$1; shift
  { echo "# cmd: $*"; "$@"; echo "exit=$?"; } > "$C/$n.txt" 2>&1
}
fixture() { # dir change-fn ; prints new rev
  local D=$S/$1
  $G clone -q --shared "$LANE" "$D"
  $G -C "$D" checkout -q --detach "$REV"
  [ "$($G -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch" >&2; exit 9; }
  ( cd "$D" && "$2" )
  $G -C "$D" add -A
  $G -C "$D" -c user.name=c98-fixture -c user.email=fixture@c98.invalid commit -qm "control $1"
  $G -C "$D" rev-parse HEAD
}
CAP="python3 -B $W/c98_captable.py --fleet $FLEET --fleet-revision $FREV"

# ---------------- C1
rec ctl-c1-selftest python3 -B "$W/c98_captable.py" --selftest
rec base-c1 $CAP --root "$LANE" --revision "$BASE"
rec instr-c1 $CAP --root "$LANE" --revision "$REV"
# forgery A: the 39 repair names with their rounds but no evidence path and 3-word prose
c1_namesonly() { python3 - <<'EOF'
import re, sys
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-98")
import gen_cap_rows as g
p = "SCORECARD.md"; t = open(p).read()
i = t.index("## Capabilities"); j = t.index("\n\n", t.index("| Capability |", i))
rows = "".join(f"\n| {c} | can do it | none | {r} |" for r, c, w, e in g.ROWS)
open(p, "w").write(t[:j] + rows + t[j:])
EOF
}
D=$(fixture c1-namesonly c1_namesonly); rec ctl-c1-forgery-namesonly $CAP --root "$S/c1-namesonly" --revision "$D"
# forgery B: one mega-row carrying every repair name, round 52, real evidence path
c1_mega() { python3 - <<'EOF'
import sys
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-98")
import gen_cap_rows as g
p = "SCORECARD.md"; t = open(p).read()
i = t.index("## Capabilities"); j = t.index("\n\n", t.index("| Capability |", i))
names = "; ".join(c for r, c, w, e in g.ROWS)
paths = " ".join(f"`{x}`" for r, c, w, e in g.ROWS for x in __import__("re").findall(r"`([^`]+)`", e))
row = f"\n| two gate registry rows in SKILL.md | {names} | {paths} | 52 |"
open(p, "w").write(t[:j] + row + t[j:])
EOF
}
D=$(fixture c1-mega c1_mega); rec ctl-c1-forgery-mega $CAP --root "$S/c1-mega" --revision "$D"
# forgery C (declared known limit): right names, rounds and paths, junk 8-word prose
c1_junk() { python3 - <<'EOF'
import re, sys
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-98")
import gen_cap_rows as g
p = "SCORECARD.md"; t = open(p).read()
i = t.index("## Capabilities"); j = t.index("\n\n", t.index("| Capability |", i))
rows = "".join(f"\n| {c} | lorem ipsum dolor sit amet consectetur adipiscing elit | {e} | {r} |" for r, c, w, e in g.ROWS)
t = t[:j] + rows + t[j:]
t = t.replace("| Curated source registry |", "| Sources-registry (curated source registry) |")
for name in ("Offline link-preview (Open Graph) audit", "Link-preview audit, round-35 contract",
             "Offline robots.txt expectation audit", "Offline response-header expectation audit",
             "Standalone retained-span quote classifier (round-64 re-entry)"):
    t = re.sub(r"\n\| " + re.escape(name) + r" \|[^\n]*", "", t, count=1)
open(p, "w").write(t)
EOF
}
D=$(fixture c1-junk c1_junk); rec ctl-c1-forgery-junkprose $CAP --root "$S/c1-junk" --revision "$D"

# ---------------- C2
STALE="python3 -B $W/c98_stale.py --work $S/run"
mkdir -p "$S/run"
rec ctl-c2-selftest python3 -B "$W/c98_stale.py" --selftest
rec base-c2 $STALE --root "$LANE" --revision "$BASE"
rec instr-c2 $STALE --root "$LANE" --revision "$REV"
for subj in pos-oracle neg-constant neg-lookup neg-noprohibit neg-exclusive neg-respsie neg-lenient; do
  eval "c2_$subj() { mkdir -p scripts && cp '$W/frozen/$subj.py' scripts/stale_extensions.py; }"
  D=$(fixture "c2-$subj" "c2_$subj")
  rec "ctl-c2-slot-$subj" $STALE --root "$S/c2-$subj" --revision "$D"
done

# ---------------- digests
( cd "$W" && sha256sum c98_captable.py c98_stale.py stale-contract.md gen_cap_rows.py frozen/*.py ) > "$C/instrument-sha256.txt"
echo "controls done at instruments rev $REV"
