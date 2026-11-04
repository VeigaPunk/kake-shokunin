#!/bin/bash
# usage: sweep.sh <gate.py> <outdir>  -- scores every ExecSandbox candidate, one line per candidate
W=/fast/scratch/hyaku/kake-r90/ExecSandbox; C=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/w1/ExecSandbox
mkdir -p "$2"
for f in $C/c*.py; do n=$(basename $f .py)
  python3 -B "$1" --candidate "$f" --work $W/work --seed 4242 --verbose > "$2/$n.txt" 2>&1; rc=$?
  l=$(grep -E "^cache_key_conformance clauses" "$2/$n.txt" | tail -1)
  v=$(grep -m1 -A1 "^FAIL" | tr "\n" " " "$2/$n.txt")
  echo "$n rc=$rc | ${l:-NO-SUMMARY $(tail -1 $2/$n.txt)} | first_violation=${v:-none}"
done
