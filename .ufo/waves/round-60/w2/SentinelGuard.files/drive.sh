#!/bin/bash
# SentinelGuard attack driver — all fixtures inside $S
S=/fast/scratch/hyaku/kake-r60/SentinelGuard
export TMPDIR=$S
G=$S/lane/scripts/append_guard.py
run() { python3 -B "$G" "$@"; echo "  rc=$?"; }
g() { git -C "$D" -c user.name=selftest -c user.email=selftest@local "$@"; }

mkdir -p "$S/fx"
D=$(mktemp -d -p "$S/fx" base.XXXXXX); git -C "$D" init -q
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$(realpath "$D")" ] || { echo "TOPLEVEL MISMATCH"; exit 9; }
mkdir -p "$D/corpus/knowledge/sub"
printf '# note\n\nalpha\nbeta\ngamma\nomega\n' > "$D/corpus/knowledge/a.md"
printf '# deep\n\nx\n' > "$D/corpus/knowledge/sub/deep.md"
printf '# skill\n' > "$D/SKILL.md"
git -C "$D" add -A
g commit -qm base
B=$(git -C "$D" rev-parse HEAD)

echo "=== S1 --scope escapes (clean base/revision; nothing out of scope may be read) ==="
for sc in '../**/*.md' '/etc/passwd' '**' '../../../../**' '-x' 'corpus/knowledge/**/*.md'; do
  printf -- '--- scope=%s ---\n' "$sc"
  run --root "$D" --base "$B" --revision "$B" --scope="$sc"
done

echo "=== S2 option injection via revision/base ==="
run --root "$D" --base="$B" --revision=--output=pwn
run --root "$D" --base=--help --revision="$B"
run --root "$D" --base="$B" --revision=--upload-pack=x
ls -1 "$D/pwn" 2>&1 | sed 's/^/  side-effect: /'

echo "=== S2b tree id / tag / blob id as revision ==="
T=$(git -C "$D" rev-parse "$B^{tree}")
run --root "$D" --base "$B" --revision "$T"
g tag -a -m t v1 "$B" >/dev/null
run --root "$D" --base "$B" --revision v1
OLDB=$(git -C "$D" rev-parse "$B^{tree}")
echo "  (tree-as-base follows)"; run --root "$D" --base "$T" --revision "$B"
echo "  (abbreviated 7-char base)"; run --root "$D" --base "$(git -C "$D" rev-parse --short=7 "$B")" --revision "$B"

echo "=== S3 symlinked repo root ==="
ln -sfn "$D" "$S/fx/link"
run --root "$S/fx/link" --base "$B" --revision "$B"
ln -sfn "$D/corpus" "$S/fx/link2"
run --root "$S/fx/link2" --base "$B" --revision "$B"

echo "=== S4 GIT_* env ==="
GIT_DIR=/nonexistent GIT_WORK_TREE=/tmp GIT_OBJECT_DIRECTORY=/nonexistent \
  GIT_ALTERNATE_OBJECT_DIRECTORIES=/nonexistent GIT_INDEX_FILE=/nonexistent \
  GIT_COMMON_DIR=/nonexistent run --root "$D" --base "$B" --revision "$B"
echo "  (env pointing at ANOTHER real repo)"
GIT_DIR="$S/lane/.git" GIT_WORK_TREE="$S/lane" run --root "$D" --base "$B" --revision "$B"

echo "=== S5 path with tab / quote / backslash in name ==="
printf 'q\n' > "$D/corpus/knowledge/quo\"te.md"
printf 'b\n' > "$D/corpus/knowledge/back\\slash.md"
printf 't\n' > "$D/corpus/knowledge/tab	name.md"
git -C "$D" add -A; g commit -qm weird-names
B2=$(git -C "$D" rev-parse HEAD)
git -C "$D" ls-tree -r "$B2" | sed 's/^/  ls-tree| /'
printf 'q2\n' > "$D/corpus/knowledge/quo\"te.md"
printf 'b2\n' > "$D/corpus/knowledge/back\\slash.md"
printf 't2\n' > "$D/corpus/knowledge/tab	name.md"
git -C "$D" add -A; g commit -qm weird-rewrite
R2=$(git -C "$D" rev-parse HEAD)
echo "  --- default quotePath: three rewrites expected ---"
run --root "$D" --base "$B2" --revision "$R2"
H=$(mktemp -d -p "$S/fx" home.XXXXXX); printf '[core]\n\tquotePath = false\n' > "$H/.gitconfig"
echo "  --- same, HOME core.quotePath=false ---"
HOME="$H" run --root "$D" --base "$B2" --revision "$R2"

echo "=== S6 deletion of a non-ASCII-named in-scope file ==="
printf 'n\n' > "$D/corpus/knowledge/naïve.md"; git -C "$D" add -A; g commit -qm nonascii
B3=$(git -C "$D" rev-parse HEAD)
git -C "$D" rm -q "corpus/knowledge/naïve.md"; g commit -qm del-nonascii
R3=$(git -C "$D" rev-parse HEAD)
echo "  (expect deleted corpus/knowledge/naïve.md)"
run --root "$D" --base "$B3" --revision "$R3"

echo "DIR=$D" > "$S/fx/last.path"
