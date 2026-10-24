#!/usr/bin/env bash
# Receipt for round-37 criterion (a) bare-id: bare_id_check.py in this directory.
set -u
B=/fast/scratch/hyaku/kake-r37w1/ExecCriteriaRepairs
L=/home/vgpnk/Projects/shokunin/kake-shokunin
C="$B/criteria/bare_id_check.py"
export TMPDIR=$B/tmp
cd "$L" || exit 99

run() {
  echo "\$ $*"
  timeout 120 "$@"
  echo "exit=$?"
  echo
}

echo "== bare_id_check.py sha256"
timeout 20 sha256sum "$C"; echo "exit=$?"; echo

echo "== RED: constructed entry citing S098 and S099 only as bare ids"
run python3 -B "$C" "$B/fixtures/bare-id-entry.md"

echo "== GREEN: a real knowledge entry (crawl-scope-per-host)"
run python3 -B "$C" corpus/knowledge/crawl-scope-per-host.md

echo "== GREEN: every knowledge entry in the lane (informational sweep)"
run python3 -B "$C" corpus/knowledge/*.md
