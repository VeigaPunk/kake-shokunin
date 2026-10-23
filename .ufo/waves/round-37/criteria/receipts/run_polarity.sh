#!/usr/bin/env bash
# Receipt for round-37 criterion (f) polarity: polarity_check.py in this directory.
set -u
B=/fast/scratch/hyaku/kake-r37w1/ExecCriteriaRepairs
L=/home/vgpnk/Projects/shokunin/kake-shokunin
C="$B/criteria/polarity_check.py"
export TMPDIR=$B/tmp
cd "$L" || exit 99

run() {
  echo "\$ $*"
  timeout 120 "$@"
  echo "exit=$?"
  echo
}

echo "== polarity_check.py sha256"
timeout 20 sha256sum "$C"; echo "exit=$?"; echo
echo "== key hashes (read as JSON only; the round-37 key is not touched)"
timeout 20 sha256sum .ufo/waves/round-36/sealed/cases-v1.json .ufo/waves/round-36/sealed/cases.json; echo "exit=$?"; echo

echo "== RED: round-36 key v1 (bullets e and f have no body-decided finding)"
run python3 -B "$C" --key .ufo/waves/round-36/sealed/cases-v1.json

echo "== GREEN: round-36 key v2"
run python3 -B "$C" --key .ufo/waves/round-36/sealed/cases.json

echo "== RED on a constructed key whose only (e) finding is metadata-decided"
run python3 -B "$C" --key "$B/fixtures/key-metadata-only.json" --body-bullets e

echo "== GREEN on a constructed key carrying a body-decided finding and hold in (e)"
run python3 -B "$C" --key "$B/fixtures/key-both-polarities.json" --body-bullets e
