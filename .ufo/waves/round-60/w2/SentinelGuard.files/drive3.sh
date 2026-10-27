#!/bin/bash
# M6 git-call audit via PATH shim, M7 scope regex compile, M8 blob size
S=/fast/scratch/hyaku/kake-r60/SentinelGuard
export TMPDIR=$S
G=$S/lane/scripts/append_guard.py
RUN() { echo "--- $* ---"; python3 -B "$G" "$@"; echo "  rc=$?"; }

echo "=== M6 every git subprocess the tool issues (PATH shim logs argv) ==="
SH=$S/shim; rm -rf "$SH"; mkdir -p "$SH"
cat > "$SH/git" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >> "$SHIMLOG"
exec /usr/bin/git "$@"
EOF
chmod +x "$SH/git"; export SHIMLOG=$S/gitcalls.log; : > "$SHIMLOG"
PATH="$SH:$PATH" python3 -B "$G" --root "$S/lane" --base fd6303ce5c14b3f892dec586297a942ab6e4193b --revision 8b33fd248d126b48d838af5c38bc175850f41a09
echo "  total git calls: $(wc -l < "$SHIMLOG")"
echo "  by subcommand:"; awk '{print $NF}' "$SHIMLOG" | sort | uniq -c | sort -rn | head -3
awk '{for(i=1;i<=NF;i++) if ($i=="rev-parse"||$i=="ls-tree"||$i=="cat-file"||$i=="merge-base") print $i}' "$SHIMLOG" | sort | uniq -c
echo "  any worktree-reading subcommand (show/diff/status/ls-files/--work-tree)?"
grep -cE '(^| )(show|diff|status|ls-files|checkout|grep)( |$)|--work-tree|--path-format' "$SHIMLOG" || true
echo "  cat-file invocations: $(grep -c 'cat-file' "$SHIMLOG")  (distinct oids: $(grep 'cat-file' "$SHIMLOG" | awk '{print $NF}' | sort -u | wc -l))"

echo "=== M7 scope patterns that are not valid regex after translation ==="
D=$S/fx/scope; rm -rf "$D"; mkdir -p "$D/corpus/knowledge"; git -C "$D" init -q
printf 'a\n' > "$D/corpus/knowledge/a.md"; git -C "$D" add -A
git -C "$D" -c user.name=selftest -c user.email=selftest@local commit -qm base
B=$(git -C "$D" rev-parse HEAD)
for sc in '[[:alpha:]]*' 'corpus/knowledge/[a-z].md' 'corpus/knowledge/?.md' '[!c]*' 'corpus/knowledge/[a-' '**/*.md' 'corpus/knowledge/**/../*.md'; do
  RUN --root "$D" --base "$B" --revision "$B" --scope "$sc"
done

echo "=== M8 60 MB in-scope blob: memory/time with a widened scope ==="
BIG=$S/fx/big; rm -rf "$BIG"; mkdir -p "$BIG/corpus/knowledge"; git -C "$BIG" init -q
python3 - "$BIG/corpus/knowledge/huge.md" <<'PY'
import sys
line = b"duplicate payload line for the guard probe 0123456789\n"  # 54 B
n = 60_000_000 // len(line)
open(sys.argv[1], "wb").write(line * n)
PY
git -C "$BIG" add -A; git -C "$BIG" -c user.name=selftest -c user.email=selftest@local commit -qm base
BB=$(git -C "$BIG" rev-parse HEAD)
printf 'tail\n' >> "$BIG/corpus/knowledge/huge.md"; git -C "$BIG" add -A
git -C "$BIG" -c user.name=selftest -c user.email=selftest@local commit -qm rev
BR=$(git -C "$BIG" rev-parse HEAD)
ls -l "$BIG/corpus/knowledge/huge.md" | awk '{print "  blob bytes on disk:", $5, "ascii dup ratio:", 1}'
/usr/bin/time -v python3 -B "$G" --root "$BIG" --base "$BB" --revision "$BR" \
  --scope 'corpus/knowledge/**/*.md' 2>&1 | grep -E 'files=|Maximum resident|Elapsed' | sed 's/^/  /'
