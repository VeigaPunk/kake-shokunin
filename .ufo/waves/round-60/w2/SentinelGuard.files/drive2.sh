#!/bin/bash
# mutation + hostile-name + perf probes
S=/fast/scratch/hyaku/kake-r60/SentinelGuard
export TMPDIR=$S
G=$S/lane/scripts/append_guard.py
run() { python3 -B "$G" "$@"; echo "  rc=$?"; }

echo "=== M1 selftest at B1 ==="
python3 -B "$G" --selftest 2>&1 | tail -4

echo "=== M2 real-lane tag is load-bearing (mutate one tag token in a scratch clone) ==="
C=$S/clone1
rm -rf "$C"
git clone -q --shared "$S/lane" "$C"
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$(realpath "$C")" ] && echo "toplevel ok: $C"
git -C "$C" checkout -q fd6303ce5c14b3f892dec586297a942ab6e4193b
git -C "$C" checkout -q 8b33fd248d126b48d838af5c38bc175850f41a09 -- corpus/knowledge/crawler-identity.md
python3 - "$C/corpus/knowledge/crawler-identity.md" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text()
assert t.count("[r59-correction 2026-10-27]") == 1, t.count("[r59-correction 2026-10-27]")
p.write_text(t.replace("[r59-correction 2026-10-27]", "correction 2026-10-27"))
PY
git -C "$C" add -A
git -C "$C" -c user.name=selftest -c user.email=selftest@local commit -qm "mutant: tag token removed"
MR=$(git -C "$C" rev-parse HEAD)
echo "--- guard fd6303ce -> mutant (expect untagged_insertion) ---"
run --root "$C" --base fd6303ce5c14b3f892dec586297a942ab6e4193b --revision "$MR"
echo "--- control: guard fd6303ce -> B1 (expect clean) ---"
run --root "$C" --base fd6303ce5c14b3f892dec586297a942ab6e4193b --revision 8b33fd248d126b48d838af5c38bc175850f41a09

echo "=== M3 non-UTF-8 bytes in a finding path + C locale stdout ==="
D=$S/fx/hostile
rm -rf "$D"; mkdir -p "$D/corpus/knowledge"; git -C "$D" init -q
printf 'a\nb\nc\n' > "$D/corpus/knowledge/nl.md"
printf 'x\n' > "$D/corpus/knowledge/naïve.md"
git -C "$D" add -A; git -C "$D" -c user.name=selftest -c user.email=selftest@local commit -qm base
B=$(git -C "$D" rev-parse HEAD)
printf 'zzz\n' > "$D/corpus/knowledge/naïve.md"; git -C "$D" add -A
git -C "$D" -c user.name=selftest -c user.email=selftest@local commit -qm rewrite
R=$(git -C "$D" rev-parse HEAD)
H=$S/fx/homeqp; rm -rf "$H"; mkdir -p "$H"; printf '[core]\n\tquotePath = false\n' > "$H/.gitconfig"
echo "--- quotePath=false + LANG=C.UTF-8 ---"
HOME="$H" LANG=C.UTF-8 run --root "$D" --base "$B" --revision "$R"
echo "--- quotePath=false + LANG=C, locale coercion off ---"
HOME="$H" LANG=C LC_ALL=C PYTHONCOERCECLOCALE=0 PYTHONUTF8=0 run --root "$D" --base "$B" --revision "$R"

echo "=== M4 --root shapes ==="
run --root "$D/corpus/knowledge/nl.md" --base "$B" --revision "$R"
run --root "" --base "$B" --revision "$R"
run --root "$D/" --base "$B" --revision "$R"

echo "=== M5 tag-dense DP worst case (states widen only when tags exist) ==="
python3 -B - "$S" <<'PY'
import importlib.util, os, sys, time
spec = importlib.util.spec_from_file_location(
    "ag", "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/append_guard.py")
ag = importlib.util.module_from_spec(spec); spec.loader.exec_module(ag)
TAG = b"[r60-correction 2026-10-27]"
def probe(n, tag_every):
    base = [b"x"] * n
    rev = []
    for i in range(n):
        if tag_every and i % tag_every == 0:
            rev.append(TAG)
        rev.append(b"x")
    t0 = time.monotonic(); ok = ag.any_clean_alignment(base, rev, [True if r == TAG else False for r in rev])
    return ok, time.monotonic() - t0
for n, every in ((500, 0), (500, 2), (1000, 2), (2000, 2)):
    ok, dt = probe(n, every)
    print(f"n={n} tag_every={every or '-'}: clean={ok} wall={dt:.3f}s")
PY
