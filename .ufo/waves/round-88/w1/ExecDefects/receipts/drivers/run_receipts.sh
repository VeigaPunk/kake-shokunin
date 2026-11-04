#!/usr/bin/env bash
# Round 88 seat ExecDefects -- D2 diagnostic repair receipts. Absolute paths only.
set -u
ROOT=/fast/scratch/hyaku/kake-r88/ExecDefects
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
W=$LANE/.ufo/waves/round-88/w1/ExecDefects
BASE=$ROOT/base-cache_current_age.py
CAND=$W/cache_current_age.py
OUT=$ROOT/out
PY=$(command -v python3)
mkdir -p "$OUT" "$ROOT/tmp"
export TMPDIR=$ROOT/tmp
export PYTHONDONTWRITEBYTECODE=1

{
  echo "# provenance"
  echo "date: $(date -Is)"
  echo "cwd: $(pwd)"
  echo "python: $PY"
  "$PY" -VV
  echo "sha256 base: $(sha256sum "$BASE" | cut -d' ' -f1)"
  echo "sha256 cand: $(sha256sum "$CAND" | cut -d' ' -f1)"
  echo "bytes: base $(wc -c <"$BASE") cand $(wc -c <"$CAND")"
  echo "lines: base $(wc -l <"$BASE") cand $(wc -l <"$CAND")"
  echo "TMPDIR: $TMPDIR"
} >"$OUT/00-provenance.txt"

case_run () {
  local name=$1 tool=$2 payload=$3
  shift 3
  local f=$OUT/$name
  printf '%s' "$payload" | "$PY" -B "$tool" "$@" >"$f.stdout" 2>"$f.stderr"
  local rc=$?
  {
    echo "command: printf '%s' '$payload' | $PY -B $tool $*"
    echo "stdin: $payload"
    echo "exit: $rc"
    echo "stdout_bytes: $(wc -c <"$f.stdout")"
    echo "stderr_bytes: $(wc -c <"$f.stderr")"
    echo "--- stdout ---"
    cat "$f.stdout"
    echo "--- stderr ---"
    cat "$f.stderr"
  } >"$f.receipt"
  echo "$name exit=$rc"
}

self_run () {
  local name=$1 tool=$2
  shift 2
  local f=$OUT/$name
  "$PY" -B "$tool" "$@" </dev/null >"$f.stdout" 2>"$f.stderr"
  local rc=$?
  {
    echo "command: $PY -B $tool $* </dev/null"
    echo "exit: $rc"
    echo "stdout_bytes: $(wc -c <"$f.stdout")"
    echo "stderr_bytes: $(wc -c <"$f.stderr")"
    echo "--- stdout ---"
    cat "$f.stdout"
    echo "--- stderr ---"
    cat "$f.stderr"
  } >"$f.receipt"
  echo "$name exit=$rc"
}

diff_run () {
  local name=$1 payload=$2
  printf '%s' "$payload" | "$PY" -B "$BASE" >"$OUT/$name.base.out" 2>"$OUT/$name.base.err"
  local rb=$?
  printf '%s' "$payload" | "$PY" -B "$CAND" >"$OUT/$name.cand.out" 2>"$OUT/$name.cand.err"
  local rc=$?
  local cmpres=DIFFER
  cmp -s "$OUT/$name.base.out" "$OUT/$name.cand.out" && cmpres=IDENTICAL
  {
    echo "command(base): printf '%s' '$payload' | $PY -B $BASE"
    echo "command(cand): printf '%s' '$payload' | $PY -B $CAND"
    echo "stdin: $payload"
    echo "exit: base=$rb cand=$rc"
    echo "stdout: $cmpres"
    echo "--- base stdout ---"
    cat "$OUT/$name.base.out"
    echo "--- cand stdout ---"
    cat "$OUT/$name.cand.out"
    echo "--- base stderr ---"
    cat "$OUT/$name.base.err"
    echo "--- cand stderr ---"
    cat "$OUT/$name.cand.err"
  } >"$OUT/$name.receipt"
  echo "$name base_exit=$rb cand_exit=$rc stdout=$cmpres"
}

FLOAT='{"date_value": 7.0, "request_time": 1, "response_time": 2, "now": 3}'
BOOL='{"date_value": true, "request_time": 1, "response_time": 2, "now": 3}'
VALID='{"date_value":80,"request_time":90,"response_time":100,"now":130,"age_value":5}'
STR='{"date_value": "80", "request_time": 90, "response_time": 100, "now": 130}'
NULL='{"date_value": null, "request_time": 90, "response_time": 100, "now": 130}'
ARR='{"date_value": [], "request_time": 90, "response_time": 100, "now": 130}'
OBJ='{"date_value": {}, "request_time": 90, "response_time": 100, "now": 130}'
AGE_FLOAT='{"date_value": 80, "request_time": 90, "response_time": 100, "now": 130, "age_value": 5.0}'
REQ_STR='{"date_value": 80, "request_time": "90", "response_time": 100, "now": 130}'
MISSING='{"request_time": 90, "response_time": 100, "now": 130}'
UNKNOWN='{"date_value":80,"request_time":90,"response_time":100,"now":130,"extra":1}'
NONOBJ='[]'
ORDER='{"date_value": 80, "request_time": 100, "response_time": 90, "now": 130}'
NEG_AGE='{"date_value": 80, "request_time": 90, "response_time": 100, "now": 130, "age_value": -1}'

case_run red-base-float "$BASE" "$FLOAT"
case_run red-base-bool "$BASE" "$BOOL"
self_run base-selftest "$BASE" --selftest

case_run cand-float "$CAND" "$FLOAT"
case_run cand-bool "$CAND" "$BOOL"
case_run cand-valid "$CAND" "$VALID"
self_run cand-selftest "$CAND" --selftest
case_run cand-string "$CAND" "$STR"
case_run cand-null "$CAND" "$NULL"
case_run cand-array "$CAND" "$ARR"
case_run cand-object "$CAND" "$OBJ"
case_run cand-age-float "$CAND" "$AGE_FLOAT"
case_run cand-request-string "$CAND" "$REQ_STR"
case_run cand-missing-key "$CAND" "$MISSING"
case_run cand-unknown-key "$CAND" "$UNKNOWN"
case_run cand-nonobject "$CAND" "$NONOBJ"
case_run cand-order "$CAND" "$ORDER"
case_run cand-neg-age "$CAND" "$NEG_AGE"

diff_run arith-valid "$VALID"
diff_run arith-both-max '{"date_value": 17, "request_time": 23, "response_time": 29, "now": 40, "age_value": 2}'
diff_run arith-age-max '{"date_value": 31, "request_time": 23, "response_time": 29, "now": 40, "age_value": 13}'
diff_run arith-future-date '{"date_value": -9, "request_time": 0, "response_time": 3, "now": 8}'
diff_run arith-equal-times '{"date_value": 8, "request_time": 8, "response_time": 8, "now": 8}'
diff_run arith-omitted-age '{"date_value": -86400, "request_time": 0, "response_time": 60, "now": 120}'
diff_run arith-huge '{"date_value": -123456789012345678901234567890123456789012345678901234567890, "request_time": 0, "response_time": 1, "now": 3, "age_value": 123456789012345678901234567890123456789012345678901234567890}'

echo "--- diff -u base vs candidate ---"
diff -u "$BASE" "$CAND" >"$OUT/diff-u.txt"
echo "diff_exit=$? (1 = differing files, expected)"
cat "$OUT/diff-u.txt"

echo "--- line proof ---"
"$PY" -B "$ROOT/line_proof.py" >"$OUT/line-proof.txt" 2>&1
echo "line_proof_exit=$?"
cat "$OUT/line-proof.txt"

echo "--- predicate probe ---"
"$PY" -B "$ROOT/predicate_probe.py" >"$OUT/predicate.txt" 2>&1
echo "predicate_exit=$?"
cat "$OUT/predicate.txt"

echo "--- counter selftest ---"
"$PY" -B "$LANE/.ufo/waves/round-88/c88_defect_queue.py" --selftest >"$OUT/counter-selftest.txt" 2>&1
echo "counter_selftest_exit=$?"
cat "$OUT/counter-selftest.txt"

echo "--- scratch tree writable check ---"
find "$ROOT" -maxdepth 2 -type f | sort | sed "s|$ROOT|<scratch>|"
