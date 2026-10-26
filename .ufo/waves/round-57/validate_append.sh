#!/usr/bin/env bash
# Round-56 append-block validation (C7 receipts). Re-run after ANY edit to corpus/SOURCES.md or the
# two adopted entries: mirrors the working-tree corpus/ (registry + entries included) into assimilation/validate/ and
# gates the append on `sources-census.sh validate --file <mirror registry>` (exit 0 required).
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
cd "$LANE" || exit 64
V=.ufo/waves/round-57/assimilation/validate
rm -rf "$V"; mkdir -p "$V"
cp -r corpus "$V/corpus"   # whole-corpus mirror: the census checks that every used-by path exists
for f in SCORECARD.md SKILL.md scripts/source_recheck.py .ufo/waves/round-41/c1_count.py .ufo/waves/round-41/oracle_crosscheck.py; do
  mkdir -p "$V/$(dirname "$f")"; cp "$f" "$V/$f"   # non-corpus used-by targets named by held rows
done
ARGV="/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $V/corpus/SOURCES.md"
printf '%s\n' "$ARGV" > "$V/census-argv.txt"
$ARGV > "$V/census-stdout.txt" 2> "$V/census-stderr.txt"
echo "exit=$?" > "$V/census-exit.txt"
cat "$V/census-exit.txt"; tail -2 "$V/census-stdout.txt"
