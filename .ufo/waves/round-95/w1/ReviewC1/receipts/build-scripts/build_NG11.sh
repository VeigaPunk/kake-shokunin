#!/bin/bash
set -e
S=/fast/scratch/hyaku/kake-r95/ReviewC1; F=$S/fixtures
build() { DDR=$1; rm -rf "$DDR"; mkdir -p "$DDR/lane/corpus/lessons" "$DDR/lane/corpus/knowledge"; D="$DDR/lane"; git -C "$D" init -q; git -C "$D" config user.email reviewc1@example.invalid; git -C "$D" config user.name reviewc1; T=$(cd "$D" && git rev-parse --show-toplevel); M=$(readlink -f "$D"); [ "$T" = "$M" ] || { echo FAIL; exit 1; }; }
commit() { git -C "$D" add -A; git -C "$D" commit -q -m x; echo "[$1] $(git -C "$D" rev-parse HEAD | head -c 12)"; }
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

# NG11: gate body with a bogus "admit" and "reject" appearing inside a non-decision word or code (e.g. in a prose marker "we admitta ..." and "this is a rejectable item")
build "$F/NG11"
cat > "$D/corpus/lessons/round-95.md" <<'EOF'
# r95

## Gate

Some admiralty prose that contains the substring admit as an adjective but no decision.
Reject as a noun: "this is a rejection", but no decision line. Lorem ipsum and filler here.

## Mistakes

| # | Class |
|---|---|
| 1 | a |
EOF
writebase; commit NG11

echo NG11 done
