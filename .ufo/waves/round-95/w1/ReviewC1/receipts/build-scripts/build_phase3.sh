#!/bin/bash
set -e
S=/fast/scratch/hyaku/kake-r95/ReviewC1; F=$S/fixtures
build() { DDR=$1; rm -rf "$DDR"; mkdir -p "$DDR/lane/corpus/lessons" "$DDR/lane/corpus/knowledge"; D="$DDR/lane"; git -C "$D" init -q; git -C "$D" config user.email reviewc1@example.invalid; git -C "$D" config user.name reviewc1; T=$(cd "$D" && git rev-parse --show-toplevel); M=$(readlink -f "$D"); [ "$T" = "$M" ] || { echo "FAIL: not at repo root"; exit 1; }; }
commit() { git -C "$D" add -A; git -C "$D" commit -q -m "fixture"; echo "[$1] $(git -C "$D" rev-parse HEAD | head -c 12)"; }

# ============ R08: round-02 lesson duplicated (displaced) with same basename in different dir ============
build "$F/R08"
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
cat > "$D/corpus/lessons/round-02.md" <<'EOF'
# r2

## Gate

admit C.
reject D.

## Mistakes

| # | Class |
|---|---|
| 1 | displaced |
EOF
cat > "$D/corpus/lessons/nested-round-02.md" 2>/dev/null || true
mkdir -p "$D/corpus/lessons/nested"
cat > "$D/corpus/lessons/nested/round-02.md" <<'EOF'
# r2 twin

## Gate

admit C.
reject D.

## Mistakes

| # | Class |
|---|---|
| 1 | displaced |
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
commit R08

# ============ R09: SKILL row names a symlink (committed git mode 120000) ============
build "$F/R09"
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
mkdir -p "$D/scripts"
printf "print('t')\n" > "$D/scripts/t.py"
cat > "$D/SKILL.md" <<'EOF'
| name | kind | entry | verdict |
|---|---|---|---|
| t | gate | `scripts/t.py` | 0=ok |
| u | link | `scripts/sym.py` | n/a |
EOF
commit R09_prelink
ln -s "t.py" "$D/scripts/sym.py"
git -C "$D" add -A
git -C "$D" commit -q -m "symlink"
echo "[R09] $(git -C "$D" rev-parse HEAD | head -c 12)"

# ============ R10b: absence span with mismatched/unclosed bracket ============
build "$F/R10b"
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
| u | ghost | [r95-absence 2026-11-05: `scripts/gone2.py` absent | ok |
EOF
mkdir -p "$D/scripts"
printf "print('t')\n" > "$D/scripts/t.py"
commit R10b

# ============ R12: knowledge entry source line w/o id; locator /tmp/scratch ============
build "$F/R12"
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
cat > "$D/corpus/knowledge/entry.md" <<'EOF'
source: /tmp/scratch/anywhere.md
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
commit R12

echo "PHASE3 build done"
