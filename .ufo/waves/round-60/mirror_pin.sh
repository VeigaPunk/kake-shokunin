#!/usr/bin/env bash
# Round-60 pre-append mirror pin generator (C8 tooling).
#
# Materializes corpus/SOURCES.md at the pinned BASE revision under
# <root>/<path> and writes the pin JSON to <root>/<pin>: rows (registry table
# row count), bytes and sha256 of the mirror bytes. The pin JSON is also
# printed to stdout.
#
#   mirror_pin.sh [--root DIR] [--path REPO-REL] [--pin REPO-REL] [--base REV]
#
# Defaults reproduce the committed round-60 layout:
#   root $LANE, path .ufo/waves/round-60/assimilation/pre-append/corpus/SOURCES.md,
#   pin  .ufo/waves/round-60/assimilation/mirror-pin.json, base 97cdc12...
# With --root pointing at scratch nothing in the lane is touched (dry run).
# Exit 2 when the base blob is unreadable.
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
BASE=97cdc122379711c2b02a8970752c8782da3ac81d
ROOT=$LANE
PATH_REL=.ufo/waves/round-60/assimilation/pre-append/corpus/SOURCES.md
PIN_REL=.ufo/waves/round-60/assimilation/mirror-pin.json

while [ $# -gt 0 ]; do
  case "$1" in
    --root) [ $# -ge 2 ] || exit 64; ROOT=$2; shift 2 ;;
    --path) [ $# -ge 2 ] || exit 64; PATH_REL=$2; shift 2 ;;
    --pin)  [ $# -ge 2 ] || exit 64; PIN_REL=$2; shift 2 ;;
    --base) [ $# -ge 2 ] || exit 64; BASE=$2; shift 2 ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) echo "usage: unknown option $1" >&2; exit 64 ;;
  esac
done
case "$PATH_REL" in *..*|/*|"") echo "usage: bad --path" >&2; exit 64 ;; esac
case "$PIN_REL"  in *..*|/*|"") echo "usage: bad --pin"  >&2; exit 64 ;; esac

OUT=$ROOT/$PATH_REL
mkdir -p "$(dirname "$OUT")" "$ROOT/$(dirname "$PIN_REL")"
git -C "$LANE" show "$BASE:corpus/SOURCES.md" > "$OUT" || { echo "base blob unreadable: $BASE" >&2; rm -f "$OUT"; exit 2; }

SHA256=$(sha256sum < "$OUT"); SHA256=${SHA256%% *}
BYTES=$(wc -c < "$OUT")
ROWS=$(gawk '
  /^ {0,3}##[ \t]/ { in_reg = ($0 ~ /^ {0,3}##[ \t]*Registry/) ; next }
  /^ {0,3}#[ \t]/  { in_reg=0; next }
  in_reg && $0 ~ /^ {0,3}\|[ \t]*S[0-9]/ { n++ }
  END { print n+0 }' < "$OUT")

printf '{\n "path": "%s",\n "base": "%s",\n "sha256": "%s",\n "bytes": %d,\n "rows": %d\n}' \
  "$PATH_REL" "$BASE" "$SHA256" "$BYTES" "$ROWS" | tee "$ROOT/$PIN_REL"
printf '\n'
