#!/usr/bin/env bash
# ReviewC1 (round 90) forgery driver. Usage: forge.sh <fixture-clone> <scratch-work>
# Each case branches from the freeze 4ee62b18 (counter + retained RFC bodies, NO fix),
# applies only forgeries (no real D89-1..3 fix), commits, and runs the frozen C1 counter.
set -u
D=$1; W=$2
FREEZE=4ee62b18fec15af45654a9c8f8d5e7938d2bb796
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
CTR=$LANE/.ufo/waves/round-90/c90_defects.py
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch"; exit 2; }
G() { git -C "$D" -c user.name=fixture -c user.email=fixture@scratch.invalid "$@"; }
INH=$LANE/.ufo/waves/round-90/inherited/baseclean.out
NOTE='S467 row'

reset_case() {  # $1 branch
  G checkout -q -f --detach "$FREEZE"
  G clean -q -fdx
  : > "$D/.git/info/exclude"
  G checkout -q -B "$1"
}

forge_d2() {  # $1 = correction line (appended to both ledgers)
  printf '\n%s\n' "$1" >> "$D/SCORECARD.md"
  printf '\n%s\n' "$1" >> "$D/LOG.md"
}

forge_d3() {  # $1 = scope cell, $2 = Gate line
  local row="| S467 | RFC 9111: HTTP Caching — https://www.rfc-editor.org/rfc/rfc9111.txt | spec | A | $1 | fixture anchor | supersedes S463 — fixture note | mined | 2026-11-04 | 180d | corpus/knowledge/cache-key-construction.md |"
  python3 - "$D/corpus/SOURCES.md" "$row" <<'PY'
import sys
p, row = sys.argv[1], sys.argv[2]
lines = open(p, encoding="utf-8").read().split("\n")
idx = max(i for i, l in enumerate(lines) if l.startswith("| S465 "))
lines.insert(idx + 1, row)
open(p, "w", encoding="utf-8").write("\n".join(lines))
PY
  mkdir -p "$D/corpus/lessons"
  printf '# fixture\n\n## Gate\n\n%s\n\n## Registry\n\nnone\n' "$2" > "$D/corpus/lessons/round-90.md"
}

relocate_copy() {
  mkdir -p "$D/.ufo/waves/round-90/inherited"
  cp -p "$INH" "$D/.ufo/waves/round-90/inherited/baseclean.out"
}

measure() {  # $1 label, $2 revision
  echo "## $1"
  ( cd "$W" && TMPDIR="$W" python3 -B "$CTR" --root "$D" --revision "$2" --work "$W" ); echo "exit=$?"
  echo "live-root-files: $(cd "$D" && ls -A | grep -vx -e .git | grep -x -e baseclean.out -e __pycache__ -e scratch.pyc | tr '\n' ' ')"
}

# Common forged D2/D3 payloads (no f62e7954 measurement; contradiction re-affirmed;
# superseding scope repeats the defect; Gate quote grounds nothing).
D2_TIP='- D89-2 correction: the round-89 C1 statement at f62e7954 stands with items B, C, D, E, F closed, receipted by `.ufo/waves/round-89/controls/final2-c1-at-tip.txt` at 93475f7e2fea29c287b5c677b80c43244f2024e0 reading open=1 closed=5'
D3_SCOPE='Not cache-key construction, storage, revalidation or serving'
D3_GATE='- S467 admit, A: "Internet Engineering Task Force (IETF)" (5 words).'

# F1: D1 live bypass via .git/info/exclude
reset_case f1-exclude
relocate_copy; forge_d2 "$D2_TIP"; forge_d3 "$D3_SCOPE" "$D3_GATE"
G add -A; G commit -q -m "F1 forged"
cp -p "$INH" "$D/baseclean.out"; echo baseclean.out >> "$D/.git/info/exclude"
measure "F1 root baseclean.out hidden by .git/info/exclude; D2 cites tip receipt (no f62e7954 measure, re-affirms B-F closed); D3 scope 'Not cache-key construction', Gate quote = IETF boilerplate" "$(G rev-parse HEAD)"

# F2: D1 bypass via committed .gitignore (+ root __pycache__ scratch, ignored by the lane's own .gitignore)
reset_case f2-gitignore
relocate_copy; printf '/baseclean.out\n' >> "$D/.gitignore"
forge_d2 '- D89-2 correction: f62e7954 superseded; base reading `.ufo/waves/round-89/controls/base-c1.txt` 76225160d0dff8d2042fbcd037bd08b0971d5e07 open=6 closed=0'
forge_d3 'not cache key construction, storage or serving' '- S467 (supersedes S463): "the cache MUST NOT use" — fixture.'
G add -A; G commit -q -m "F2 forged"
cp -p "$INH" "$D/baseclean.out"; mkdir -p "$D/__pycache__"; echo x > "$D/__pycache__/scratch.pyc"; echo x > "$D/scratch.pyc"
measure "F2 root baseclean.out ignored by committed .gitignore, root __pycache__/ and scratch.pyc ignored by lane .gitignore; D2 cites round-89 BASE receipt; D3 scope 'not cache key construction' (no hyphen)" "$(G rev-parse HEAD)"

# F3: root file staged (git add) but not committed
reset_case f3-staged
relocate_copy; forge_d2 "$D2_TIP"; forge_d3 "$D3_SCOPE" "$D3_GATE"
G add -A; G commit -q -m "F3 forged"
cp -p "$INH" "$D/baseclean.out"; G add baseclean.out
measure "F3 root baseclean.out staged in index, not committed" "$(G rev-parse HEAD)"

# F4: HEAD tracks root baseclean.out; measured revision is a side commit without it
reset_case f4-side
relocate_copy; forge_d2 "$D2_TIP"; forge_d3 "$D3_SCOPE" "$D3_GATE"
G add -A; G commit -q -m "F4 measured side commit"
SIDE=$(G rev-parse HEAD)
cp -p "$INH" "$D/baseclean.out"; G add baseclean.out; G commit -q -m "F4 HEAD keeps root scratch tracked"
measure "F4 HEAD tracks root baseclean.out; counter measures side commit $SIDE" "$SIDE"

# F0 control: same as F1 without the exclude (must stay open on D1 live)
reset_case f0-control
relocate_copy; forge_d2 "$D2_TIP"; forge_d3 "$D3_SCOPE" "$D3_GATE"
G add -A; G commit -q -m "F0 control"
cp -p "$INH" "$D/baseclean.out"
measure "F0 control: F1 without exclude (root file visible)" "$(G rev-parse HEAD)"

G checkout -q -f --detach "$FREEZE"; G clean -q -fdx; : > "$D/.git/info/exclude"
