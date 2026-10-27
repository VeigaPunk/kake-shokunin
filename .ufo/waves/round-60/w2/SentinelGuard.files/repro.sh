#!/bin/bash
# SentinelGuard repro — round-60 w2. Self-contained: builds its own fixtures.
# usage: bash repro.sh            (scratch under /fast/scratch/hyaku/kake-r60/SentinelGuard/repro)
set -u
S=${S:-/fast/scratch/hyaku/kake-r60/SentinelGuard/repro}
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
G=$LANE/scripts/append_guard.py
B1=8b33fd248d126b48d838af5c38bc175850f41a09
R1BASE=fd6303ce5c14b3f892dec586297a942ab6e4193b
export TMPDIR=$S
mkdir -p "$S"; rm -rf "$S"/*
run() { echo "\$ python3 -B scripts/append_guard.py $*"; python3 -B "$G" "$@"; echo "  rc=$?"; }
gc() { git -C "$1" "${@:2}"; }
commit() { git -C "$1" -c user.name=selftest -c user.email=selftest@local commit -qm "$2"; }

echo "##### F1  quoted path -> in-scope file silently unchecked (exit 0 false clean)"
D=$(mktemp -d -p "$S" f1.XXXXXX); git -C "$D" init -q
[ "$(gc "$D" rev-parse --show-toplevel)" = "$(realpath "$D")" ] || { echo FAIL TOPLEVEL; exit 9; }
mkdir -p "$D/corpus/knowledge"
printf '# note\n' > "$D/corpus/knowledge/keep.md"
printf 'x\n' > "$D/corpus/knowledge/naïve.md"
git -C "$D" add -A; commit "$D" base; B=$(gc "$D" rev-parse HEAD)
printf 'REWRITTEN\n' > "$D/corpus/knowledge/naïve.md"
git -C "$D" add -A; commit "$D" rewrite; R=$(gc "$D" rev-parse HEAD)
echo "-- ls-tree output the tool parses:"; gc "$D" ls-tree -r "$B" | sed 's/^/   /'
run --root "$D" --base "$B" --revision "$R"
H=$(mktemp -d -p "$S" home.XXXXXX); printf '[core]\n\tquotePath = false\n' > "$H/.gitconfig"
echo "-- same commit, same argv, HOME/.gitconfig core.quotePath=false:"
HOME="$H" run --root "$D" --base "$B" --revision "$R"
echo "-- and a deletion of a non-ASCII-named in-scope file:"
printf 'x\n' > "$D/corpus/knowledge/naïve.md"; git -C "$D" add -A; commit "$D" restore
B2=$(gc "$D" rev-parse HEAD); git -C "$D" rm -q "corpus/knowledge/naïve.md"; commit "$D" del
run --root "$D" --base "$B2" --revision "$(gc "$D" rev-parse HEAD)"
echo

echo "##### F3  empty effective scope -> exit 0 clean (no coverage signal)"
for sc in '' '/etc/passwd' '../**/*.md' 'corpus/knowledge/[a-'; do run --root "$D" --base "$B" --revision "$B" --scope "$sc"; done
echo

echo "##### F4  two cat-file reads per in-scope blob, even when unchanged"
SH=$S/shim; mkdir -p "$SH"
printf '#!/bin/sh\nprintf "%%s\\n" "$*" >> "$SHIMLOG"\nexec /usr/bin/git "$@"\n' > "$SH/git"; chmod +x "$SH/git"
export SHIMLOG=$S/gitcalls.log; : > "$SHIMLOG"
PATH="$SH:$PATH" python3 -B "$G" --root "$LANE" --base "$R1BASE" --revision "$B1" > /dev/null
echo "   git calls=$(wc -l < "$SHIMLOG") cat-file=$(grep -c cat-file "$SHIMLOG") distinct_oids=$(grep cat-file "$SHIMLOG" | awk '{print $NF}' | sort -u | wc -l)"
echo "   worktree subcommands=$(grep -cE '(^| )(show|diff|status|ls-files|checkout|grep)( |$)|--work-tree' "$SHIMLOG")"
echo

echo "##### F5  60 MB in-scope blob -> peak RSS"
BIG=$(mktemp -d -p "$S" big.XXXXXX); git -C "$BIG" init -q; mkdir -p "$BIG/corpus/knowledge"
python3 - "$BIG/corpus/knowledge/huge.md" <<'PY'
import sys
line = b"duplicate payload line for the guard probe 0123456789\n"
open(sys.argv[1], "wb").write(line * (60_000_000 // len(line)))
PY
git -C "$BIG" add -A; commit "$BIG" base; BB=$(gc "$BIG" rev-parse HEAD)
printf 'tail\n' >> "$BIG/corpus/knowledge/huge.md"; git -C "$BIG" add -A; commit "$BIG" rev
python3 - "$BIG" "$BB" "$(gc "$BIG" rev-parse HEAD)" "$G" <<'PY'
import resource, subprocess, sys, time
t0 = time.monotonic()
p = subprocess.run([sys.executable, "-B", sys.argv[4], "--root", sys.argv[1], "--base", sys.argv[2],
                    "--revision", sys.argv[3]], capture_output=True, text=True)
print(f"   exit={p.returncode} wall={time.monotonic()-t0:.2f}s "
      f"peak_rss={resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss/1024:.0f} MiB {p.stdout.strip()}")
PY
echo

echo "##### F6  DP cost when tags exist (states widen); cheap check is done second"
python3 - "$G" <<'PY'
import importlib.util, sys, time
spec = importlib.util.spec_from_file_location("ag", sys.argv[1])
ag = importlib.util.module_from_spec(spec); spec.loader.exec_module(ag)
TAG = b"[r60-correction 2026-10-27]"
for n in (500, 1000, 2000, 4000):
    base = [b"x"] * n
    rev = [TAG if i % 2 == 0 else b"x" for i in range(n)]
    t0 = time.monotonic(); ok = ag.any_clean_alignment(base, rev, [r == TAG for r in rev])
    print(f"   n={n} tag_every=2 clean={ok} wall={time.monotonic()-t0:.3f}s")
PY
echo

echo "##### N1  negative: the real-lane R1 pass is NOT vacuous (tag is load-bearing)"
C=$(mktemp -d -p "$S" n1.XXXXXX)
git clone -q --shared "$LANE" "$C"
gc "$C" checkout -q "$R1BASE"
gc "$C" checkout -q "$B1" -- corpus/knowledge/crawler-identity.md
python3 - "$C/corpus/knowledge/crawler-identity.md" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text()
p.write_text(t.replace("[r59-correction 2026-10-27]", "correction 2026-10-27"))
PY
git -C "$C" add -A; commit "$C" mutant
run --root "$C" --base "$R1BASE" --revision "$(gc "$C" rev-parse HEAD)"
