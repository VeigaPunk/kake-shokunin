#!/bin/bash
# SentinelScope R94-2 effectful-shadow probes. Scratch only; counters are read from the lane and copied.
set -u
L=/home/vgpnk/Projects/shokunin/kake-shokunin
S=/fast/scratch/hyaku/kake-r95/SentinelScope
FIX=$S/fixture
REV=8f638b591e739e1863f5fa22334d5e15178189ed
SRC=$L/.ufo/waves/round-95
R=$S/shadow
rm -rf "$R"; mkdir -p "$R"

mkshadow() {
  mkdir -p "$1"
  cat > "$1/subprocess.py" <<'PY'
import os, sys
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MARK"), "a").write("ran\n")
sys.exit(7)
PY
}

runone() {  # name counter-dir-with-counter shadow-dir pythonpath(or -) interp-mode
  local name=$1 cdir=$2 sdir=$3 pp=$4 mode=$5
  local W=$R/$name/work
  mkdir -p "$W" "$W/tmp"
  local cnt=$cdir/$CNT
  local envs=(env -i PATH=/usr/bin:/bin HOME="$W" TMPDIR="$W/tmp")
  [ "$pp" != "-" ] && envs+=(PYTHONPATH="$pp")
  local args=(--root "$FIX" --revision "$REV" --work "$W/work")
  if [ "$mode" = "wrap" ]; then
    ( cd "$cdir" && "${envs[@]}" python3 -B -c "import sys; sys.path.insert(0,'.'); g={'__file__':'$CNT','__name__':'__main__'}; sys.argv=['$CNT','--root','$FIX','--revision','$REV','--work','$W/work']; exec(compile(open('$CNT').read(),'$CNT','exec'), g)" > "$W/out.txt" 2> "$W/err.txt"; echo $? > "$W/rc" )
  else
    local flag=-B; [ "$mode" = "I" ] && flag=-I
    ( cd "$W" && "${envs[@]}" python3 $flag "$cnt" "${args[@]}" > "$W/out.txt" 2> "$W/err.txt"; echo $? > "$W/rc" )
  fi
}

for CNT in c95_selfassess.py c95_conditional.py; do
  T=${CNT%.py}
  # A: counter + shadow share script dir, no PYTHONPATH, python3 -B (the frozen command form)
  d=$R/A-$T; mkdir -p "$d"; cp "$SRC/$CNT" "$d/"; mkshadow "$d"; runone "A-$T" "$d" "$d" - B &
  # B: same, plus PYTHONPATH pointing at the shadow dir
  d=$R/B-$T; mkdir -p "$d"; cp "$SRC/$CNT" "$d/"; mkshadow "$d"; runone "B-$T" "$d" "$d" "$d" B &
  # C: same as B under python3 -I (documented as excluding script dir; -I also ignores PYTHONPATH)
  d=$R/C-$T; mkdir -p "$d"; cp "$SRC/$CNT" "$d/"; mkshadow "$d"; runone "C-$T" "$d" "$d" "$d" I &
  # D: counter in its own dir, shadow only reachable via PYTHONPATH from a separate dir
  d=$R/D-$T; mkdir -p "$d"; cp "$SRC/$CNT" "$d/"; sh=$R/D-shadow-$T; mkshadow "$sh"; runone "D-$T" "$d" "$sh" "$sh" B &
  # E: python3 -c wrapper, shadow in cwd ('.' inserted on sys.path), counter exec'd with __file__ set
  d=$R/E-$T; mkdir -p "$d"; cp "$SRC/$CNT" "$d/"; mkshadow "$d"; runone "E-$T" "$d" "$d" - wrap &
done
wait

for dir in "$R"/*/; do
  n=$(basename "$dir")
  [ -d "$dir/work" ] || continue
  marker=absent; [ -e "$dir/MARK" ] && marker=present
  [ -e "$R/$n/work/../../../shadow/$n/MARK" ] && true
  rc=$(cat "$dir/work/rc" 2>/dev/null || echo NA)
  l1=$(head -n 1 "$dir/work/out.txt" 2>/dev/null | cut -c1-160)
  e1=$(tail -n 1 "$dir/work/err.txt" 2>/dev/null | cut -c1-160)
  echo "RUN $n marker=$marker rc=$rc own_line=${l1:-<none>} stderr_tail=${e1:-<none>}"
done
