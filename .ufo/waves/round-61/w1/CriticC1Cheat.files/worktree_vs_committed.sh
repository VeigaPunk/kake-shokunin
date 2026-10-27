#!/bin/bash
# CHEAT DEMO (c61 cheat 2): counter that reads the WORKTREE instead of
# committed bytes at --revision. Same repo, three views of one file.
set -e
D=$(mktemp -d -p /fast/scratch/hyaku/kake-r61/CriticC1Cheat/demo)
git -C "$D" init -q
P=.ufo/waves/r90/controls/receipt-1.txt
mkdir -p "$D/$(dirname $P)"
printf '# receipt: r90\nrevision: r90-1\n' > "$D/$P"
git -C "$D" -c user.name=selftest -c user.email=selftest@local add -A
git -C "$D" -c user.name=selftest -c user.email=selftest@local commit -q -m add
BASE=$(git -C "$D" rev-parse HEAD)
printf '# receipt: r90\nrevision: r90-2\n' > "$D/$P"
git -C "$D" -c user.name=selftest -c user.email=selftest@local add -A
git -C "$D" -c user.name=selftest -c user.email=selftest@local commit -q -m rewrite
HEADC=$(git -C "$D" rev-parse HEAD)
# now dirty the worktree WITHOUT committing: revision-line r90-3
printf '# receipt: r90\nrevision: r90-3-UNCOMMITTED\n' > "$D/$P"
echo "repo: $D"
echo "base=$BASE"
echo "head=$HEADC"
echo "--- committed bytes at HEAD (cat-file) ---"
git -C "$D" cat-file blob "$HEADC:$P"
echo "--- worktree bytes (cat) ---"
cat "$D/$P"
echo "--- a counter reading worktree sees r90-3 (a rewrite event that does NOT exist in history) ---"
echo "--- a counter reading committed bytes at base sees the file absent entirely ---"
git -C "$D" cat-file -e "$BASE:$P" 2>&1 || echo "(absent at base)"
