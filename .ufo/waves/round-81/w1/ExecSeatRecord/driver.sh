#!/usr/bin/env bash
# ExecSeatRecord scratch driver — every write lands under $S; the lane is only read.
set -u
S=/fast/scratch/hyaku/kake-r81/ExecSeatRecord
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
REC=$LANE/scripts/wave_seat_record.py
LOG=$S/run.log
: > "$LOG"
run(){ printf '$ %s\n' "$*" >> "$LOG"; "$@" >> "$LOG" 2>&1; printf 'rc=%d\n' "$?" >> "$LOG"; }

echo "== ExecSeatRecord $(date -u +%Y-%m-%dT%H:%M:%SZ) recorder=$(sha256sum "$REC" | cut -d' ' -f1)" >> "$LOG"

# fixtures
run python3 -B "$S/make_cases.py"
run python3 -B "$S/reorder.py"

# check 1 — cross-round fixture (round-80 prescribed; round-79 because the named facts live there)
run python3 -B "$REC" --results "$LANE/.ufo/waves/round-80/w1-results.json" --spec "$LANE/.ufo/waves/round-80/w1-spec.json" --out "$S/r80.json"
run python3 -B "$REC" --results "$LANE/.ufo/waves/round-79/w1-results.json" --spec "$LANE/.ufo/waves/round-79/w1-spec.json" --out "$S/r79.json"

# check 2 — class boundary: all "x" / one "" / one "   \n"
for c in a b c; do
  run python3 -B "$REC" --results "$S/cases/$c-results.json" --spec "$S/cases/spec.json" --out "$S/cases/$c-record.json"
done

# check 3 — determinism (two runs, different paths) and reordering
run python3 -B "$REC" --results "$LANE/.ufo/waves/round-80/w1-results.json" --spec "$LANE/.ufo/waves/round-80/w1-spec.json" --out "$S/r80-again.json"
run cmp "$S/r80.json" "$S/r80-again.json"
run python3 -B "$REC" --results "$S/cases/r80-reordered.json" --spec "$LANE/.ufo/waves/round-80/w1-spec.json" --out "$S/r80-reordered-record.json"
run cmp "$S/r80.json" "$S/r80-reordered-record.json"
run sha256sum "$S/r80.json" "$S/r80-again.json" "$S/r80-reordered-record.json" "$S/r79.json"

# check 4 — schema honesty + independent ground-truth cross-checks
run python3 -B "$S/analyze.py"

# counter consistency: embedded RECORDER copy vs the committed script
run python3 -c '
import ast, pathlib, sys
tree = ast.parse(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "RECORDER" for t in node.targets):
        pathlib.Path(sys.argv[2]).write_text(node.value.value, encoding="utf-8")
        print("extracted embedded RECORDER from", sys.argv[1])
' "$LANE/.ufo/waves/round-81/c81_defect_queue.py" "$S/embedded-recorder.py"
run diff -u "$S/embedded-recorder.py" "$REC"

echo "== driver done $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
