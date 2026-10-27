#!/usr/bin/env bash
# Round-59 append-block validation (C7 receipts). Re-run after ANY edit to corpus/SOURCES.md or the two
# adopted entries (crawler-identity-signals.md, googlebot-verification.md): mirrors the working-tree
# corpus/ (registry + entries included) into .ufo/waves/round-59/assimilation/validate/ and gates the
# append on `sources-census.sh validate --file <mirror registry>` (exit 0 required).
#
# The non-corpus used-by targets are DERIVED at run time from the registry's own used-by cells (the
# mined rows of the `## Registry` section) — not copied from round 58's list. The census resolves every
# used-by path relative to the mirror root, so a mined row that names a target outside corpus/ makes
# that target a mirror member; a mined row naming a target that is absent from the lane leaves it
# absent from the mirror and the census reports E11 (exit 1) on its own.
#
# LANE may be overridden (env) to validate a scratch copy of the lane; it defaults to the lane.
set -u
LANE="${LANE:-/home/vgpnk/Projects/shokunin/kake-shokunin}"
CENSUS="${CENSUS:-/home/vgpnk/Projects/shokunin/scripts/sources-census.sh}"
V=".ufo/waves/round-59/assimilation/validate"
cd "$LANE" || exit 64
rm -rf "$V"; mkdir -p "$V"
cp -r corpus "$V/corpus"   # whole-corpus mirror: the census checks that every used-by path exists

# --- derive the non-corpus used-by targets from the registry's used-by cells (mined rows) ---
# Row parsing mirrors the census parser: `## Registry` section only, 0-3 leading spaces, 11 cells
# (NF==13 with the leading/trailing empty fields), status in column 9, used-by in column 12.
# A cell is a path only when it is ASCII and looks like a relative path; "—" and "-" are skipped.
# Only `mined` rows are considered: the census existence check (E11) covers mined rows only, so
# those are exactly the used-by targets the mirror has to carry outside corpus/.
gawk -F'|' '
function trim(s) { gsub(/^[ \t]+|[ \t]+$/,"",s); return s }
function pathlike(s) { return (s ~ /^[A-Za-z0-9._][A-Za-z0-9._\/-]*$/) }
{
  line=$0
  if (line ~ /^ {0,3}##[ \t]/) { sub(/^ {0,3}/,"",line); in_registry=(trim(substr(line,3))=="Registry"); next }
  if (line ~ /^ {0,3}#[ \t]/) { in_registry=0; next }
  if (!in_registry) next
  if (line !~ /^ {0,3}\|/) next
  sub(/^ {0,3}/,"",line); $0=line
  if (NF!=13) next
  if (trim($9)!="mined") next
  ub=trim($12)
  n=split(ub, cells, ",")
  for (i=1;i<=n;i++) {
    p=trim(cells[i])
    if (!pathlike(p)) continue          # "—", "-", empty and any non-path cell
    if (p ~ /^corpus\//) next           # already in the whole-corpus mirror
    print p
  }
}' corpus/SOURCES.md | sort -u > "$V/used-by-targets.txt"

missing=""
while IFS= read -r f; do
  [ -n "$f" ] || continue
  case "$f" in
    /*|../*|*/../*|*/..) missing="$missing $f"; continue ;;   # never leave the lane root
  esac
  if [ -e "$LANE/$f" ]; then
    mkdir -p "$V/$(dirname "$f")"
    cp -p "$LANE/$f" "$V/$f"
  else
    missing="$missing $f"
  fi
done < "$V/used-by-targets.txt"

ARGV="$CENSUS validate --file $V/corpus/SOURCES.md"
printf '%s\n' "$ARGV" > "$V/census-argv.txt"
$ARGV > "$V/census-stdout.txt" 2> "$V/census-stderr.txt"
rc=$?
echo "exit=$rc" > "$V/census-exit.txt"
cat "$V/census-exit.txt"; tail -1 "$V/census-stdout.txt"
[ -n "$missing" ] && echo "MISSING_USED_BY_TARGETS:$missing" >&2
exit "$rc"
