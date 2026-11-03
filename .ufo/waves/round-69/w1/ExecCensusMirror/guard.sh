#!/usr/bin/env bash
# guard.sh — SOURCES id-collision guard for an append to corpus/SOURCES.md.
#
#   guard.sh <registry.md> <staged-rows.md> <outdir>
#
# Both files are Markdown; ids are read from table rows only. The row pattern
# allows 0-3 leading ASCII spaces, matching scripts/sources-census.sh's parser
# (4+ spaces are indented code and are ignored there, so they are ignored here).
#
#   id pattern: ^ {0,3}\|[[:space:]]*S[0-9]{3,}
#
# Writes <outdir>/registry.ids, <outdir>/staged.ids, <outdir>/collisions and
# prints one summary line:
#
#   registry_ids=<n> staged_ids=<n> collisions=<n>
#
# Exit 0 when collisions=0, 1 when any staged id already exists in the
# registry, 2 on usage or missing input.
#
# Ids are sorted with LC_ALL=C sort (byte order) so comm sees consistent input;
# ids are zero-padded to >=3 digits, so byte order is also numeric order for the
# lane's S001-S999 range.

set -u

die() { echo "guard.sh: $*" >&2; exit 2; }

[ $# -eq 3 ] || die "usage: guard.sh <registry.md> <staged-rows.md> <outdir>"
REG=$1
STAGED=$2
OUTDIR=$3

[ -f "$REG" ] || die "registry not found: $REG"
[ -f "$STAGED" ] || die "staged rows not found: $STAGED"
mkdir -p -- "$OUTDIR" || die "cannot create outdir: $OUTDIR"

ID_FROM_ROWS="^ {0,3}\|[[:space:]]*S[0-9]{3,}"

LC_ALL=C grep -oE "$ID_FROM_ROWS" -- "$REG" \
  | grep -oE 'S[0-9]+' | LC_ALL=C sort > "$OUTDIR/registry.ids"
LC_ALL=C grep -oE "$ID_FROM_ROWS" -- "$STAGED" \
  | grep -oE 'S[0-9]+' | LC_ALL=C sort > "$OUTDIR/staged.ids"

# comm -12 is the set intersection: ids present in both lists.
comm -12 "$OUTDIR/registry.ids" "$OUTDIR/staged.ids" > "$OUTDIR/collisions"

reg_n=$(wc -l < "$OUTDIR/registry.ids")
staged_n=$(wc -l < "$OUTDIR/staged.ids")
col_n=$(wc -l < "$OUTDIR/collisions")

echo "registry_ids=$reg_n staged_ids=$staged_n collisions=$col_n"
[ "$col_n" -eq 0 ]
