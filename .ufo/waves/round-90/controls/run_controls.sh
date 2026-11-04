#!/usr/bin/env bash
# Round-90 pre-freeze controls: do-nothing, forgery and positive controls for the
# C1 counter (c90_defects.py) and the C2 counter (c90_gate.py). Every fixture
# commit happens in a scratch clone ($D), never in the lane. Receipts land in
# .ufo/waves/round-90/controls/ctl-*.txt.
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
R90=$LANE/.ufo/waves/round-90
OUT=$R90/controls
BASE=209027f49959e2e2f0e16867a90a7bb38bbcd3f4
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kake-r90/L1/controls
rm -rf "$SCR"; mkdir -p "$SCR"
D=$SCR/fx
git clone -q --shared "$LANE" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "fixture toplevel mismatch"; exit 9; }
git -C "$D" checkout -q --detach "$BASE"
G() { git -C "$D" -c user.name=fixture -c user.email=fixture@scratch.invalid "$@"; }
C1() { python3 -B "$R90/c90_defects.py" --root "$1" --revision "$2" --work "$SCR/w"; echo "exit=$?"; }
C2() { python3 -B "$R90/c90_gate.py" --root "$1" --revision "$2" --work "$SCR/w" --seed 90; echo "exit=$?"; }

# freeze bytes into the fixture (counters, frozen population, retained RFC body)
mkdir -p "$D/.ufo/waves/round-90"
cp -r "$R90/frozen" "$R90/L1" "$D/.ufo/waves/round-90/"
G add -A .ufo/waves/round-90 && G commit -qm "fixture: freeze bytes"
FZ=$(git -C "$D" rev-parse HEAD)
REAL_REC=.ufo/waves/round-89/controls/final2-c1-at-tip.txt
TIP89=93475f7e2fea29c287b5c677b80c43244f2024e0
QUOTE='The "cache key" is the information a cache uses to choose a response'
QUOTE_FAKE='the cache key MUST include the request method in canonical form'
corr() { printf '\n%s\n' "- D89-2 correction: the round-89 C1 statement \`open=5 closed=1\` at f62e7954 is superseded; receipted reading \`$1\` revision $2 $3."; }
sup_row() { printf '| S467 | RFC 9111 - HTTP Caching, section 2 and 4.1 - https://www.rfc-editor.org/rfc/rfc9111.txt | spec | A | %s | sections 2 and 4.1 | supersedes S463 — fixture | mined | 2026-11-04 | 180d | corpus/knowledge/cache-key-construction.md |\n' "$1"; }
add_sup() { # $1 scope, $2 quote
  python3 - "$D/corpus/SOURCES.md" "$(sup_row "$1")" <<'PY'
import sys
p, row = sys.argv[1], sys.argv[2]
lines = open(p).read().split("\n")
idx = max(i for i, l in enumerate(lines) if l.startswith("| S46"))
lines.insert(idx + 1, row)
open(p, "w").write("\n".join(lines))
PY
  printf '# round 90\n\n## Gate\n\n- S467 admit: "%s" (rfc9111.txt line 251)\n' "$2" > "$D/corpus/lessons/round-90.md"
}
reset_fx() { G checkout -q --detach "$FZ"; G clean -qfd; rm -f "$D/baseclean.out"; }

{
echo "## c1-do-nothing (lane at base; live tree carries the inherited baseclean.out)"; C1 "$LANE" "$BASE"
reset_fx
echo "## c1-F-D1a relocated copy committed, root file left untracked"
mkdir -p "$D/.ufo/waves/round-90/inherited"; cp "$LANE/baseclean.out" "$D/.ufo/waves/round-90/inherited/"
G add .ufo/waves/round-90/inherited && G commit -qm "fx D1a"; cp "$LANE/baseclean.out" "$D/baseclean.out"
C1 "$D" HEAD
reset_fx
echo "## c1-F-D1b relocated copy with different bytes, root clean"
mkdir -p "$D/.ufo/waves/round-90/inherited"; echo junk > "$D/.ufo/waves/round-90/inherited/baseclean.out"
G add .ufo/waves/round-90/inherited && G commit -qm "fx D1b"; C1 "$D" HEAD
reset_fx
echo "## c1-F-D2a correction whose numbers disagree with the cited receipt"
corr "$REAL_REC" "$TIP89" "open=5 closed=1" | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"
G commit -qam "fx D2a"; C1 "$D" HEAD
reset_fx
echo "## c1-F-D2b fabricated receipt agreeing with its correction"
mkdir -p "$D/.ufo/waves/round-90/controls"
echo "C1v1 revision=$TIP89 items=6 open=0 closed=6 met=true" > "$D/.ufo/waves/round-90/controls/fake-c1.txt"
corr .ufo/waves/round-90/controls/fake-c1.txt "$TIP89" "open=0 closed=6" | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"
G add -A && G commit -qm "fx D2b"; C1 "$D" HEAD
reset_fx
echo "## c1-F-D2c valid correction but the filed SCORECARD row rewritten in place"
python3 - "$D/SCORECARD.md" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
s = s.replace("`open=5 closed=1 met=false`, exit 1 | `python3 -B .ufo/waves/round-89/c89_defect_queue.py",
              "`open=1 closed=5 met=false`, exit 1 | `python3 -B .ufo/waves/round-89/c89_defect_queue.py", 1)
open(p, "w").write(s)
PY
corr "$REAL_REC" "$TIP89" "open=1 closed=5" | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"
G commit -qam "fx D2c"; C1 "$D" HEAD
reset_fx
echo "## c1-F-D3a supersede row with a fabricated quote"
add_sup "Cache-key ingredients for construction" "$QUOTE_FAKE"
G add -A && G commit -qm "fx D3a"; C1 "$D" HEAD
reset_fx
echo "## c1-F-D3b supersede row valid but S463 scope rewritten in place"
python3 - "$D/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
s = s.replace("and the wildcard member; not cache-key construction, storage", "and the wildcard member; not storage", 1)
open(p, "w").write(s)
PY
add_sup "Cache-key ingredients for construction" "$QUOTE"
G add -A && G commit -qm "fx D3b"; C1 "$D" HEAD
reset_fx
echo "## c1-positive all three fixed in the fixture"
mkdir -p "$D/.ufo/waves/round-90/inherited"; cp "$LANE/baseclean.out" "$D/.ufo/waves/round-90/inherited/"
corr "$REAL_REC" "$TIP89" "open=1 closed=5" | tee -a "$D/SCORECARD.md" >> "$D/LOG.md"
add_sup "Cache-key ingredients for construction" "$QUOTE"
G add -A && G commit -qm "fx positive"; C1 "$D" HEAD
} > "$OUT/ctl-c1.txt" 2>&1

{
echo "## c2-do-nothing (lane at base: no gate)"; C2 "$LANE" "$BASE"
for kind in refuse admit hashtable nametable; do
  reset_fx
  echo "## c2-$kind gate"
  case $kind in
    refuse) printf 'import sys\nprint("cache_key_conformance met=false")\nsys.exit(1)\n' ;;
    admit) printf 'import sys\nprint("cache_key_conformance met=true")\nsys.exit(0)\n' ;;
    hashtable) cat <<'PY'
import hashlib, os, sys
cand = sys.argv[sys.argv.index("--candidate") + 1]
h = hashlib.sha256(open(cand, "rb").read()).hexdigest()
pins = os.path.join(os.path.dirname(cand), "..", "..", "..", "round-90", "frozen", "c2-population.sha256")
known = set()
for root, _, files in os.walk(os.path.dirname(os.path.abspath(cand)).split("/.ufo/")[0]):
    for f in files:
        if f == "c2-population.sha256":
            known |= {l.split()[0] for l in open(os.path.join(root, f)) if "cache_key.py" not in l}
bad = h in known
print("cache_key_conformance met=%s" % ("false" if bad else "true"))
sys.exit(1 if bad else 0)
PY
    ;;
    nametable) cat <<'PY'
import os, sys
cand = os.path.basename(sys.argv[sys.argv.index("--candidate") + 1])
bad = any(cand.startswith(p) for p in ("adv-", "ctl-", "M0", "M1", "M2", "M3", "neg-"))
print("cache_key_conformance met=%s" % ("false" if bad else "true"))
sys.exit(1 if bad else 0)
PY
    ;;
  esac > "$D/scripts/cache_key_conformance.py"
  cp "$R90/frozen/c2-population.sha256" "$D/.ufo/waves/round-90/frozen/" 2>/dev/null
  G add -A && G commit -qm "fx gate $kind"; C2 "$D" HEAD
done
} > "$OUT/ctl-c2.txt" 2>&1
rm -rf "$SCR"
