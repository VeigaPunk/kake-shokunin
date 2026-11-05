#!/usr/bin/env bash
# run-final-receipts.sh — landed-tip receipts for the round-95 frozen counters
# (kake round 95, wave w1, seat ExecReceipts).
#
# Usage:   run-final-receipts.sh <REVISION> [LANE_ROOT]
# Env:     LANE              lane root (default: derived from this script's location)
#          RECEIPTS_OUT_DIR  output dir for after-c1-final.txt / after-c2-final.txt
#                            (default: <LANE>/.ufo/waves/round-95/controls;
#                             set to a scratch dir for dry runs)
#
# Runs the two frozen round-95 counters exactly as the freeze declares:
#   cd <LANE> && python3 -B .ufo/waves/round-95/c95_selfassess.py  --root . --revision <REV> --work <scratch>
#   cd <LANE> && python3 -B .ufo/waves/round-95/c95_conditional.py --root . --revision <REV> --work <scratch>
#
# Receipt format: line 1 `revision <full-sha>`; the counter's stdout follows.
# Counter exit codes are reported on stderr (met=false exits 1 by design; that is
# a receipt, not a script failure). Instrument digests are checked against the
# freeze pin file and reported on stderr; a mismatch is reported, never repaired.
# Scratch-clean: all work dirs live under /fast/scratch/hyaku/kake-r95/ExecReceipts
# and one trap removes them on exit.
set -euo pipefail

REVISION="${1:?usage: run-final-receipts.sh <REVISION> [LANE_ROOT]}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANE="${2:-${LANE:-$(cd "$SCRIPT_DIR/../../../../../" && pwd)}}"
SCRATCH_ROOT="/fast/scratch/hyaku/kake-r95/ExecReceipts"
OUT_DIR="${RECEIPTS_OUT_DIR:-$LANE/.ufo/waves/round-95/controls}"

FULL="$(git -C "$LANE" rev-parse --verify "$REVISION^{commit}")"
SHORT="${FULL:0:12}"
WORK="$SCRATCH_ROOT/final-$SHORT-$$"
mkdir -p "$WORK/tmp" "$OUT_DIR"
trap 'rm -rf "$WORK"' EXIT
export TMPDIR="$WORK/tmp"

# Digest check against the freeze pin (stderr only).
PIN_FILE="$LANE/.ufo/waves/round-95/controls/instrument-sha256.txt"
for c in c95_selfassess.py c95_conditional.py; do
  want="$(awk -v p=".ufo/waves/round-95/$c" '$2==p {print $1}' "$PIN_FILE")"
  got="$(sha256sum "$LANE/.ufo/waves/round-95/$c" | cut -d' ' -f1)"
  if [[ -n "$want" && "$got" == "$want" ]]; then
    printf 'digest %s ok=%s\n' "$c" "$got" >&2
  else
    printf 'digest %s MISMATCH pin=%s disk=%s\n' "$c" "${want:-absent}" "$got" >&2
  fi
done

c1_rc=0
(cd "$LANE" && python3 -B .ufo/waves/round-95/c95_selfassess.py --root . --revision "$FULL" --work "$WORK/c1") \
  >"$WORK/c1.stdout" 2>"$WORK/c1.stderr" || c1_rc=$?
{ printf 'revision %s\n' "$FULL"; cat "$WORK/c1.stdout"; } >"$OUT_DIR/after-c1-final.txt"
printf 'c1_rc=%s\n' "$c1_rc" >&2

c2_rc=0
(cd "$LANE" && python3 -B .ufo/waves/round-95/c95_conditional.py --root . --revision "$FULL" --work "$WORK/c2") \
  >"$WORK/c2.stdout" 2>"$WORK/c2.stderr" || c2_rc=$?
{ printf 'revision %s\n' "$FULL"; cat "$WORK/c2.stdout"; } >"$OUT_DIR/after-c2-final.txt"
printf 'c2_rc=%s\n' "$c2_rc" >&2

if [[ -s "$OUT_DIR/after-c1-final.txt" && -s "$OUT_DIR/after-c2-final.txt" ]]; then
  printf 'receipts written: %s %s\n' "$OUT_DIR/after-c1-final.txt" "$OUT_DIR/after-c2-final.txt" >&2
else
  printf 'ERROR: a receipt file is missing or empty\n' >&2
  exit 1
fi
