#!/bin/bash
set -e
S=/fast/scratch/hyaku/kake-r95/ReviewC1; F=$S/fixtures; rm -rf "$F/NG07"; D=$F/NG07/lane
mkdir -p "$D/corpus/lessons" "$D/corpus/knowledge" "$D/scripts"
git -C "$D" init -q
# note: don't set user config here so git uses an empty identity; integrity is not asserted
git -C "$D" config user.email reviewc1@example.invalid; git -C "$D" config user.name reviewc1
cat > "$D/corpus/lessons/round-01.md" <<'EOF'
# r1

## Gate

admit A.
reject B.

## Mistakes

| # | Class |
|---|---|
| 1 | a |
EOF
cat > "$D/corpus/lessons/round-02.md" <<'EOF'
# r2

## Gate

admit C.
reject D.

## Mistakes

| # | Class |
|---|---|
| 1 | a |
EOF
cat > "$D/corpus/knowledge/entry.md" <<'EOF'
source: S001
verified-at: 2026-11-05
recheck: 180d

body
EOF
cat > "$D/corpus/QUALITY.md" <<'EOF'
# Q

## Round-01 criterion — a thing

Grounded in `corpus/lessons/round-01.md`.
EOF
cat > "$D/corpus/SOURCES.md" <<'EOF'
# S

## Registry

| id | source |
|---|---|
| S001 | x |
EOF
# SKILL.md with only 1 row instead of the full lanes 13 rows (rows < base 255)
cat > "$D/SKILL.md" <<'EOF'
| name | kind | entry | verdict |
|---|---|---|---|
| t | gate | `scripts/t.py` | 0=ok |
EOF
printf "print('t')\n" > "$D/scripts/t.py"
git -C "$D" add -A; git -C "$D" commit -q -m "fixture"
echo "[NG07] $(git -C "$D" rev-parse HEAD | head -c 12)"
