#!/bin/bash
set -e
S=/fast/scratch/hyaku/kake-r95/ReviewC1; F=$S/fixtures
build() { DDR=$1; rm -rf "$DDR"; mkdir -p "$DDR/lane/corpus/lessons" "$DDR/lane/corpus/knowledge"; D="$DDR/lane"; git -C "$D" init -q; git -C "$D" config user.email reviewc1@example.invalid; git -C "$D" config user.name reviewc1; T=$(cd "$D" && git rev-parse --show-toplevel); M=$(readlink -f "$D"); [ "$T" = "$M" ] || { echo FAIL; exit 1; }; }
commit() { git -C "$D" add -A; git -C "$D" commit -q -m x; echo "[$1] $(git -C "$D" rev-parse HEAD | head -c 12)"; }

# G9a NG08: Gate heading as `## Gate  admit …  reject …` on same line but with body junk (decoration only in heading, junk body)
build "$F/NG08"
cat > "$D/corpus/lessons/round-95.md" <<'EOF'
# r95

## Gate — admit everything, reject nothing

lorem ipsum dolor sit amet.
consectetur adipiscing elit sed do eiusmod tempor.

## Mistakes

| # | Class |
|---|---|
| 1 | a |
EOF
writebase() {
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
mkdir -p "$D/scripts"; printf "print('t')\n" > "$D/scripts/t.py"
}
writebase; commit NG08

# G9b NG09: dual source: where the SECOND source: line is itself clean but a third one carries junk; or first is a good id and second has
# none of S-id, but the /tmp-token regex hits only the third so counter sees it through the "first 2 source lines" rule
build "$F/NG09"
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
source: scripts/evil2.py
source: /tmp/scratch/artifact.md
verified-at: 2026-11-05
recheck: 90d

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
printf "print('evil2')\n" > "$D/scripts/evil2.py"
printf "print('topic')\n" > "$D/scripts/topic.md"
printf "print('t')\n" > "$D/scripts/t.py"
commit NG09

echo "NG89 build done"
