#!/usr/bin/env bash
# Round-60 append-block validation (adapted from .ufo/waves/round-59/validate_append.sh) — C7 receipt.
#
# Round-60 differences vs the round-59 script:
#   * the mirror is built from the PINNED BASE REVISION (git archive), not the
#     working tree, so the census sees exactly the registry the append lands on;
#   * the 3-row append block is inserted into the `## Registry` table here,
#     before the append is committed;
#   * the admitted files are overlaid at their repo-relative paths;
#   * the non-corpus used-by targets are re-derived from the BASE registry,
#     not hardcoded.
#
# Usage (run by the L1 before the append commit):
#   validate_append.sh --rows <rows.md> [--rows <more.md> ...] \
#                      [--file <repo-rel>[=<src>] ...] \
#                      [--work <dir>] [--receipt <path>] [--today <ISO>]
#
#   --rows     file of `| SNNN | ... |` rows; files concatenate in argv order.
#   --file     path admitted this round, repo-relative; `=src` reads src instead
#              of the lane worktree (the C3 run passes the two new entries plus
#              corpus/lessons/round-60.md; the googlebot-verification correction
#              is in-file, so that file is already in the base mirror and needs
#              no --file). Missing/unreadable src is copied as absent: the census
#              then reports the E11 honestly instead of the script dying.
#   --work     scratch mirror root; default mktemp (kept iff --keep-work).
#   --receipt  receipt file; default $LANE/.ufo/waves/round-60/controls/validate-append.txt
#   --today    passed to the census (default: census's own UTC date).
#
# Mirror layout: <work>/corpus/ + the non-corpus used-by targets at BASE +
# the overlaid files; census runs `validate --file <work>/corpus/SOURCES.md`
# so its E11 check resolves used-by paths under <work>/.
# Exit: census exit code verbatim (0 clean; 1 E-findings; 2 usage/missing).
set -u
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
BASE=97cdc122379711c2b02a8970752c8782da3ac81d
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh

WORK=""; WORK_GIVEN=0; RECEIPT=""; TODAY=""
declare -a ROWFILES=() ADDED=()

while [ $# -gt 0 ]; do
  case "$1" in
    --rows)     [ $# -ge 2 ] || { echo "usage: --rows needs a path" >&2; exit 64; }
                ROWFILES+=("$2"); shift 2 ;;
    --file)     [ $# -ge 2 ] || { echo "usage: --file needs a path" >&2; exit 64; }
                ADDED+=("$2"); shift 2 ;;
    --work)     [ $# -ge 2 ] || { echo "usage: --work needs a dir" >&2; exit 64; }
                WORK=$2; WORK_GIVEN=1; shift 2 ;;
    --keep-work) KEEP_WORK=1; shift ;;
    --receipt)  [ $# -ge 2 ] || { echo "usage: --receipt needs a path" >&2; exit 64; }
                RECEIPT=$2; shift 2 ;;
    --today)    [ $# -ge 2 ] || { echo "usage: --today needs a date" >&2; exit 64; }
                TODAY=$2; shift 2 ;;
    -h|--help)  sed -n '2,33p' "$0"; exit 0 ;;
    *) echo "usage: unknown option $1" >&2; exit 64 ;;
  esac
done
[ ${#ROWFILES[@]} -gt 0 ] || { echo "usage: at least one --rows file is required" >&2; exit 64; }
RECEIPT=${RECEIPT:-$LANE/.ufo/waves/round-60/controls/validate-append.txt}

# Scratch mirror ---------------------------------------------------------------
if [ "$WORK_GIVEN" = 0 ]; then
  WORK=$(mktemp -d "${TMPDIR:-/tmp}/validate-append.XXXXXX") || exit 2
  [ "${KEEP_WORK:-0}" = 1 ] || trap 'rm -rf -- "$WORK"' EXIT
else
  mkdir -p "$WORK" || exit 2
fi
V=$(realpath -- "$WORK")
cd "$LANE" || exit 2

# corpus/ at BASE (never the worktree): git archive streams a tar of the pinned
# tree; extraction pathnames come from the repo, not from arguments.
git archive "$BASE" corpus | tar -x -C "$V" || { echo "git archive corpus failed" >&2; exit 2; }
[ -f "$V/corpus/SOURCES.md" ] || { echo "no corpus/SOURCES.md at $BASE" >&2; exit 2; }

# Non-corpus used-by targets named by MINED rows at BASE (the census E11 check
# only reads status=mined rows; "—" and "-" cells are not paths). Re-derived
# from the base registry instead of the round-59 hardcoded list.
git show "$BASE:corpus/SOURCES.md" | gawk -F'|' '
  /^ {0,3}##[ \t]/ { in_reg = ($0 ~ /^ {0,3}##[ \t]*Registry/) ; next }
  /^ {0,3}#[ \t]/  { in_reg=0; next }
  !in_reg || $0 !~ /^ {0,3}\|[ \t]*S[0-9]/ { next }
  { st=$9; gsub(/^[ \t]+|[ \t]+$/,"",st); if(st!="mined") next
    n=split($0,a,"|"); ub=a[n-1]
    gsub(/^[ \t]+|[ \t]+$/,"",ub); m=split(ub,u,",")
    for(i=1;i<=m;i++){ p=u[i]; gsub(/^[ \t]+|[ \t]+$/,"",p)
      if(p!="" && p!="—" && p!="-" && p!~/^corpus\// && p!~/\.\./ && p!~/^\//) print p } }' \
| sort -u | while IFS= read -r p; do
    mkdir -p "$V/$(dirname "$p")"
    git show "$BASE:$p" > "$V/$p" 2>/dev/null || \
      printf 'WARN: used-by target %s unreadable at %s\n' "$p" "$BASE" >&2
  done

# Admitted knowledge files at their repo-relative paths ------------------------
for spec in "${ADDED[@]}"; do
  rel=${spec%%=*}
  case "$spec" in *=*) src=${spec#*=} ;; *) src="$LANE/$rel" ;; esac
  case "$rel" in *..*|/*|"") echo "usage: bad --file path: $rel" >&2; exit 64 ;; esac
  mkdir -p "$V/$(dirname "$rel")"
  if [ -f "$src" ]; then cp "$src" "$V/$rel"
  else printf 'WARN: admitted file %s missing (src %s) — census will report E11\n' "$rel" "$src" >&2
       rm -f "$V/$rel"; fi
done

# Append block: insert the row file(s) right after the LAST registry table row
# (the Registry table is followed by `## Paths`; find the last `|`-row before
# the next `## ` heading so a trailing prose section never splits the table).
REG="$V/corpus/SOURCES.md"
NEXT=$(gawk '/^ {0,3}##[ \t]/{ if(seen){print NR; exit} ; if($0 ~ /^ {0,3}##[ \t]*Registry/) seen=1 }' "$REG")
ENDLINE=${NEXT:-$(wc -l < "$REG")}
LASTROW=$(gawk -v end="$ENDLINE" 'NR<end && $0 ~ /^ {0,3}\|/ { last=NR } END{ print last+0 }' "$REG")
[ "$LASTROW" -gt 0 ] || { echo "no registry table rows found in mirror" >&2; exit 2; }
TMPREG="$V/SOURCES.md.new"
{
  sed -n "1,${LASTROW}p" "$REG"
  cat -- "${ROWFILES[@]}"
  sed -n "$((LASTROW+1)),\$p" "$REG"
} > "$TMPREG" && mv "$TMPREG" "$REG"
NROWS=$(cat -- "${ROWFILES[@]}" | grep -cE '^\|[[:space:]]*S[0-9]')

# Census validation ------------------------------------------------------------
ARGV="$CENSUS validate --file $REG"
[ -n "$TODAY" ] && ARGV="$ARGV --today $TODAY"
printf '%s\n' "$ARGV" > "$V/census-argv.txt"
$ARGV > "$V/census-stdout.txt" 2> "$V/census-stderr.txt"
RC=$?
echo "exit=$RC" > "$V/census-exit.txt"

# Receipt ----------------------------------------------------------------------
mkdir -p "$(dirname "$RECEIPT")"
{
  echo "validate-append round-60 C7"
  echo "date-utc: $(date -u +%FT%TZ)"
  echo "lane: $LANE"
  echo "base: $BASE"
  echo "argv: $ARGV"
  echo "mirror: $V"
  echo "rows-appended: $NROWS from ${ROWFILES[*]}"
  echo "files-admitted: ${ADDED[*]:-—}"
  echo "registry-rows-after: $(grep -cE '^\|[[:space:]]*S[0-9]' "$REG")"
  echo "exit=$RC"
  echo "--- census stdout ---"; cat "$V/census-stdout.txt"
  echo "--- census stderr ---"; cat "$V/census-stderr.txt"
} > "$RECEIPT"

cat "$V/census-exit.txt"
tail -2 "$V/census-stdout.txt"
echo "receipt: $RECEIPT"
exit "$RC"
