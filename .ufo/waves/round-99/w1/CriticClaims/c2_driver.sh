#!/usr/bin/env bash
# CriticClaims C2 escape driver. Candidates and outputs live ONLY in scratch.
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
COUNTER="$LANE/.ufo/waves/round-99/c99_fresh304.py"
W=/fast/scratch/hyaku/kake-r99/CriticClaims
CAND=$W/cand
OUT=$W/out
mkdir -p "$CAND" "$OUT" "$W/work2"
TIP=7f5b1b7b8dbfdae74dfe6d487bbf5406c478b916

run() { # name file extra-args...
  local name="$1" file="$2"; shift 2
  local o1 o2
  o1=$(python3 -B "$COUNTER" --root "$LANE" --candidate-file "$file" --work "$W/work2" 2>&1); r1=$?
  o2=$(python3 -B "$COUNTER" --root "$LANE" --candidate-file "$file" --revision "$TIP" --work "$W/work2" 2>&1); r2=$?
  {
    echo "# candidate $name  file=$file"
    echo "# mode=default(candidate-file, seed 99099) rc=$r1"
    echo "$o1"
    echo "# mode=revision=$TIP rc=$r2"
    echo "$o2"
  } > "$OUT/c2-$name.txt"
  echo "$name rc1=$r1 rc2=$r2 :: $(echo "$o1" | grep -E '^candidate=' | head -1) :: $(echo "$o2" | grep -E '^candidate=' | head -1)"
}

for c in e1-storedhopstrip e2-lazyetag e3-lmspacetrim e4-wsstdout e5-badjsoncrash e6-ageexcl honest-strict; do
  run "$c" "$CAND/$c.py"
done
