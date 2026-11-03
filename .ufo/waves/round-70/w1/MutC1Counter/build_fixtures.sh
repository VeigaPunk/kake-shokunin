#!/usr/bin/env bash
set -euo pipefail
S=/fast/scratch/hyaku/kake-r70/MutC1Counter
mkdir -p "$S"
G="git -C"

newrepo() {
  d=$(mktemp -d "$S/fx.XXXXXX")
  $G "$d" init -q
  top=$($G "$d" rev-parse --show-toplevel)
  if [ "$top" != "$d" ]; then echo "TOPLEVEL MISMATCH: $top != $d" >&2; exit 9; fi
  echo "$d"
}

commit() { # d msg
  $G "$1" add -A
  $G "$1" -c user.name=kake-seat -c user.email=seat@fixture commit -qm "$2"
  $G "$1" rev-parse HEAD
}

# F1 annotation-substring: dangling /tmp/kake-r10, row first cell /tmp/kake-r1
D1=$(newrepo)
cat > "$D1/SCORECARD.md" <<'EOF'
# kake-shokunin — Scorecard (fixture F1: annotation substring)

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| calibration | 2 | scratch receipt `/tmp/kake-r10` (round-10 move log row 10) | round 70 fixture |

## Pointer calibration (round 70)

| Pointer | Event |
|---|---|
| /tmp/kake-r1 | historical: scratch-discipline cleanup (2026-11-03) |
EOF
R1=$(commit "$D1" "F1 annotation-substring")

# F2 comment-out: annotation row inside an HTML comment
D2=$(newrepo)
cat > "$D2/SCORECARD.md" <<'EOF'
# kake-shokunin — Scorecard (fixture F2: commented-out annotation)

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| calibration | 2 | scratch receipt `/tmp/kake-r10` (round-10 move log row 10) | round 70 fixture |

## Pointer calibration (round 70)

<!--
| Pointer | Event |
|---|---|
| /tmp/kake-r10 | historical: scratch-discipline cleanup (2026-11-03) |
-->
EOF
R2=$(commit "$D2" "F2 comment-out")

# F3 wrong-section: row under '## Pointer calibration (round 69)'
D3=$(newrepo)
cat > "$D3/SCORECARD.md" <<'EOF'
# kake-shokunin — Scorecard (fixture F3: wrong section)

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| calibration | 2 | scratch receipt `/tmp/kake-r10` (round-10 move log row 10) | round 70 fixture |

## Pointer calibration (round 69)

| Pointer | Event |
|---|---|
| /tmp/kake-r10 | historical: scratch-discipline cleanup (2026-11-03) |
EOF
R3=$(commit "$D3" "F3 wrong-section")

# F4 honest: exact-token row in the right section; plus a resolving repo pointer
D4=$(newrepo)
mkdir -p "$D4/scripts"
printf '#!/bin/sh\necho probe\n' > "$D4/scripts/probe.sh"
cat > "$D4/SCORECARD.md" <<'EOF'
# kake-shokunin — Scorecard (fixture F4: honest annotation)

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| calibration | 2 | scratch receipt `/tmp/kake-r10` and committed probe `scripts/probe.sh` | round 70 fixture |

## Pointer calibration (round 70)

| Pointer | Event |
|---|---|
| /tmp/kake-r10 | historical: scratch-discipline cleanup (2026-11-03) |
EOF
R4=$(commit "$D4" "F4 honest")

# F5 working-tree: repo pointer dangling at the revision but present in worktree
D5=$(newrepo)
cat > "$D5/SCORECARD.md" <<'EOF'
# kake-shokunin — Scorecard (fixture F5: working-tree-only target)

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| calibration | 2 | planned receipt `.ufo/waves/round-70/ghost.md` | round 70 fixture |
EOF
R5=$(commit "$D5" "F5 working-tree")
mkdir -p "$D5/.ufo/waves/round-70"
printf 'ghost target only in the working tree\n' > "$D5/.ufo/waves/round-70/ghost.md"

cat <<EOF
F1 $D1 $R1
F2 $D2 $R2
F3 $D3 $R3
F4 $D4 $R4
F5 $D5 $R5
EOF
