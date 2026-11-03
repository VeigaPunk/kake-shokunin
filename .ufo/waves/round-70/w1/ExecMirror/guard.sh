#!/usr/bin/env bash
# guard.sh — registry-id collision guard (kake round 70, seat ExecMirror).
#
# usage: guard.sh <registry.md> <staged-rows.md> <outdir>
#
# Extracts candidate registry ids from both files with the census row shape
# (0–3 leading ASCII spaces, then '|', optional spaces, 'S' + 3+ digits), compares
# the two sorted id lists with comm -12, and writes <outdir>/reg-ids,
# <outdir>/staged-ids and <outdir>/collisions (one id per line).
#
# Prints registry-ids=N staged-ids=M collisions=K.
# exit 0 = no collisions (append safe) · 1 = id collision (refuse the append)
#      · 2 = usage error or missing input.
set -u

if [ "$#" -ne 3 ]; then
  echo "usage: $0 <registry.md> <staged-rows.md> <outdir>" >&2
  exit 2
fi
reg=$1
staged=$2
out=$3

for f in "$reg" "$staged"; do
  if [ ! -f "$f" ]; then
    echo "guard: missing input: $f" >&2
    exit 2
  fi
done

mkdir -p -- "$out" || exit 2

grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' -- "$reg" \
  | grep -oE 'S[0-9]+' | sort > "$out/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' -- "$staged" \
  | grep -oE 'S[0-9]+' | sort > "$out/staged-ids"
comm -12 "$out/reg-ids" "$out/staged-ids" > "$out/collisions"

reg_n=$(wc -l < "$out/reg-ids")
staged_n=$(wc -l < "$out/staged-ids")
coll_n=$(wc -l < "$out/collisions")

echo "registry-ids=$reg_n staged-ids=$staged_n collisions=$coll_n"

if [ "$coll_n" -gt 0 ]; then
  echo "COLLISION: $(tr '\n' ' ' < "$out/collisions")" >&2
  exit 1
fi
echo "guard: no id collisions"
exit 0
