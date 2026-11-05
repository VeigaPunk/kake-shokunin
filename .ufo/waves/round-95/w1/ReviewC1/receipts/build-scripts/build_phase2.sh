#!/bin/bash
set -e
S=/fast/scratch/hyaku/kake-r95/ReviewC1; F=$S/fixtures
build() { DDR=$1; rm -rf "$DDR"; mkdir -p "$DDR/lane/corpus/lessons" "$DDR/lane/corpus/knowledge"; D="$DDR/lane"; git -C "$D" init -q; git -C "$D" config user.email reviewc1@example.invalid; git -C "$D" config user.name reviewc1; T=$(cd "$D" && git rev-parse --show-toplevel); M=$(readlink -f "$D"); [ "$T" = "$M" ] || { echo "FAIL: not at repo root for $DDR"; exit 1; }; }
writebase() { # entry.md, QUALITY.md, SOURCES.md, SKILL.md, scripts/t.py
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
}
commit() { git -C "$D" add -A; git -C "$D" commit -q -m "fixture"; echo "[$1] $(git -C "$D" rev-parse HEAD | head -c 12)"; }

# ============ R02b: Mistakes table rows indented (separator+row lines) ============
build "$F/R02b"
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
writebase; commit R02b

# ============ R03: two source: lines, first clean, second junk ============
build "$F/R03"
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
source: S001 and scripts/topic.md
source: scripts/evil.py
verified-at: 2026-11-05
recheck: 90d

body
EOF
mkdir -p "$D/scripts"
printf "print('evil')\n" > "$D/scripts/evil.py"
printf "print('topic')\n" > "$D/scripts/topic.md"
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
commit R03

# ============ R05: SKILL path with #L42 whose blob DOES not exist (gone.py#L42) ============
build "$F/R05"
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
| u | gone | `scripts/gone.py#L42` | 0=ok |
EOF
mkdir -p "$D/scripts"
printf "print('t')\n" > "$D/scripts/t.py"
commit R05

# ============ R05b: SKILL path with :12 which DOES exist ============
build "$F/R05b"
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
| u | anchor | `scripts/t.py:12` | 0=ok |
EOF
mkdir -p "$D/scripts"
printf "print('t')\n" > "$D/scripts/t.py"
commit R05b

echo "PHASE2 build done"
