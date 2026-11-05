#!/bin/bash
set -e
S=/fast/scratch/hyaku/kake-r95/ReviewC1; F=$S/fixtures
build() { DDR=$1; rm -rf "$DDR"; mkdir -p "$DDR/lane/corpus/lessons" "$DDR/lane/corpus/knowledge"; D="$DDR/lane"; git -C "$D" init -q; git -C "$D" config user.email reviewc1@example.invalid; git -C "$D" config user.name reviewc1; T=$(cd "$D" && git rev-parse --show-toplevel); M=$(readlink -f "$D"); [ "$T" = "$M" ] || { echo "FAIL: not at repo root"; exit 1; }; }
commit() { git -C "$D" add -A; git -C "$D" commit -q -m "fixture"; echo "[$1] $(git -C "$D" rev-parse HEAD | head -c 12)"; }

# NG01: decorated '## Gate — admit x reject y' on round-95 lesson, junk body
build "$F/NG01"
cat > "$D/corpus/lessons/round-95.md" <<'EOF'
# r95

## Gate — admit P, reject Q

completely unrelated filler words here.
more filler that has nothing to do with decisions.
a third filler line for good measure.

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

Grounded in `corpus/lessons/round-95.md`.
EOF
cat > "$D/corpus/SOURCES.md" <<'EOF'
# S

## Registry

| id | source |
|---|---|
| S001 | x |
EOF
cat > "$D/SKILL.md" <<'EOF'
| name | kind | entry | verdict |
|---|---|---|---|
| t | gate | `scripts/t.py` | 0=ok |
EOF
mkdir -p "$D/scripts"
printf "print('t')\n" > "$D/scripts/t.py"
commit NG01

# NG02: row whose first cell matches a pinned cell in a DIFFERENT table (identity displacement)
build "$F/NG02"
cat > "$D/corpus/knowledge/entry.md" <<'EOF'
source: S001
verified-at: 2026-11-05
recheck: 180d

body
EOF
cat > "$D/corpus/lessons/round-95.md" <<'EOF'
# r95

## Gate

admit A.
reject B.

## Mistakes

| # | Class |
|---|---|
| 1 | a |
EOF
cat > "$D/corpus/QUALITY.md" <<'EOF'
# Q

## Round-01 criterion — a thing

Grounded in `corpus/lessons/round-95.md`.
EOF
cat > "$D/corpus/SOURCES.md" <<'EOF'
# S

## Registry

| id | source |
|---|---|
| S001 | x |
EOF
# SKILL.md: two tables in one file; second table has first cell = "t" (same as the first table)
cat > "$D/SKILL.md" <<'EOF'
## Registry A

| name | kind | entry | verdict |
|---|---|---|---|
| t | gate | `scripts/t.py` | 0=ok |

## Registry B

| advisory | impact | pin | state |
|---|---|---|---|
| t | advisory | `scripts/evil.py` | n/a |
EOF
mkdir -p "$D/scripts"
printf "print('t')\n" > "$D/scripts/t.py"
printf "print('evil')\n" > "$D/scripts/evil.py"
commit NG02

# NG03: brace-expanded tokens that mask a tree (scripts/{a,sub}) where sub is a dir
build "$F/NG03"
cat > "$D/corpus/knowledge/entry.md" <<'EOF'
source: S001
verified-at: 2026-11-05
recheck: 180d

body
EOF
cat > "$D/corpus/lessons/round-95.md" <<'EOF'
# r95

## Gate

admit A.
reject B.

## Mistakes

| # | Class |
|---|---|
| 1 | a |
EOF
cat > "$D/corpus/QUALITY.md" <<'EOF'
# Q

## Round-01 criterion — a thing

Grounded in `corpus/lessons/round-95.md`.
EOF
cat > "$D/corpus/SOURCES.md" <<'EOF'
# S

## Registry

| id | source |
|---|---|
| S001 | x |
EOF
cat > "$D/SKILL.md" <<'EOF'
| name | kind | entry | verdict |
|---|---|---|---|
| t | gate | `scripts/t.py` | 0=ok |
| u | dir | `scripts/{x,sub}` | n/a |
EOF
mkdir -p "$D/scripts/sub"
printf "print('t')\n" > "$D/scripts/t.py"
printf "print('x')\n" > "$D/scripts/x.py"
echo "" > "$D/scripts/sub/README.md"
commit NG03

# NG04: path token with trailing dot or comma inside backticks
build "$F/NG04"
cat > "$D/corpus/knowledge/entry.md" <<'EOF'
source: S001
verified-at: 2026-11-05
recheck: 180d

body
EOF
cat > "$D/corpus/lessons/round-95.md" <<'EOF'
# r95

## Gate

admit A.
reject B.

## Mistakes

| # | Class |
|---|---|
| 1 | a |
EOF
cat > "$D/corpus/QUALITY.md" <<'EOF'
# Q

## Round-01 criterion — a thing

Grounded in `corpus/lessons/round-95.md`.
EOF
cat > "$D/corpus/SOURCES.md" <<'EOF'
# S

## Registry

| id | source |
|---|---|
| S001 | x |
EOF
cat > "$D/SKILL.md" <<'EOF'
| name | kind | entry | verdict |
|---|---|---|---|
| t | gate | `scripts/t.py` | 0=ok |
| u | punct | `scripts/missing.py,.` | 0=ok |
EOF
mkdir -p "$D/scripts"
printf "print('t')\n" > "$D/scripts/t.py"
commit NG04

echo "NG build done"
