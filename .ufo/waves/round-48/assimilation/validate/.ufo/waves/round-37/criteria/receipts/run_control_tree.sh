#!/usr/bin/env bash
# Receipt for round-37 criterion (d) v2: control_tree_check.py in this directory.
# Every command is run under timeout; exit codes are printed after each.
set -u
B=/fast/scratch/hyaku/kake-r37w1/ExecCriteriaRepairs
L=/home/vgpnk/Projects/shokunin/kake-shokunin
C="$B/criteria/control_tree_check.py"
OLD="$L/.ufo/waves/round-36/criteria/control_tree_check.py"
export TMPDIR=$B/tmp
cd "$L" || exit 99

run() {
  echo "\$ $*"
  timeout 120 "$@"
  echo "exit=$?"
  echo
}

echo "== control_tree_check.py v2 sha256"
timeout 20 sha256sum "$C"; echo "exit=$?"; echo

echo "== RED: round-35 key-path listing report (routes defect 7, d)"
run python3 -B "$C" --report .ufo/waves/round-36/criteria/r35-0b7779dc-parent-tree-report.md --pattern .ufo/waves/round-35/sealed/

echo "== RED: constructed root listing over a tree holding a key"
run python3 -B "$C" --report "$B/fixtures/report-root-key.md" --pattern .ufo/waves/round-36/sealed/

echo "== RED: same report with the tree walked on disk"
run python3 -B "$C" --report "$B/fixtures/report-root-key.md" --pattern .ufo/waves/round-36/sealed/ --tree "$B/fixtures/tree-with-key"

echo "== RED: constructed recursive listing over a tree holding a key"
run python3 -B "$C" --report "$B/fixtures/report-recursive-key.md" --pattern .ufo/waves/round-36/sealed/

echo "== RED: root listing over the lane tree, which holds the round-37 key"
run python3 -B "$C" --report "$B/fixtures/report-lane-root.md" --pattern .ufo/waves/round-37/sealed/

echo "== RED: git ls-tree listing over the round-35 key tree"
run python3 -B "$C" --report "$B/fixtures/report-git-lstree.md" --pattern .ufo/waves/round-35/sealed/

echo "== FALSE PASS OF THE ROUND-36 CHECK (same root listing, old script)"
run python3 -B "$OLD" --report "$B/fixtures/report-root-key.md" --pattern .ufo/waves/round-36/sealed/

echo "== GREEN: round-37 ctl reports (key-free work dirs)"
run python3 -B "$C" --report .ufo/waves/round-37/ctl/CtlC1AllFalse.md --report .ufo/waves/round-37/ctl/CtlC1ConstantClean.md --report .ufo/waves/round-37/ctl/CtlC1Junk.md --report .ufo/waves/round-37/ctl/CtlC1NaiveReader.md --report .ufo/waves/round-37/ctl/CtlC1NoReader.md --report .ufo/waves/round-37/ctl/CtlC1NoReader-shortcut.md --report .ufo/waves/round-37/ctl/CtlC2FixtureSets.md --report .ufo/waves/round-37/ctl/MutRefPass.md --pattern .ufo/waves/round-37/sealed/

echo "== GREEN: round-36 ctl reports"
run python3 -B "$C" --report .ufo/waves/round-36/ctl/CtlAllFalse.md --report .ufo/waves/round-36/ctl/CtlConstantClean.md --report .ufo/waves/round-36/ctl/CtlNaiveReader.md --report .ufo/waves/round-36/ctl/CtlNoReader.md --report .ufo/waves/round-36/ctl/CtlShortcut.md --pattern .ufo/waves/round-36/sealed/

echo "== GREEN: constructed key-free tree, root listing plus disk walk"
run python3 -B "$C" --report "$B/fixtures/report-root-clean.md" --pattern .ufo/waves/round-36/sealed/ --tree "$B/fixtures/clean-tree"
