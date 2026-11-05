#!/bin/bash
set -e
S=/fast/scratch/hyaku/kake-r95/ReviewC1; F=$S/fixtures; D=$F/R18/lane
rm -rf "$F/R18"; mkdir -p "$D/corpus/lessons" "$D/corpus/knowledge"
git -C "$D" init -q; git -C "$D" config user.email reviewc1@example.invalid; git -C "$D" config user.name reviewc1
# Real lane shape: round-95 small lesson + big pinned judge
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
git -C "$D" add -A; git -C "$D" commit -q -m "fixture"
echo "[R18] lane committed; now build operator surfaces.json for the --surfaces-file route"
# Operator-authored surfaces.json -- not the frozen lane surface; craft to match the R18 lane
python3 - <<'EOF'
import hashlib, json, os
D='/fast/scratch/hyaku/kake-r95/ReviewC1/fixtures/R18/lane'
files={'corpus/lessons/round-95.md':open(os.path.join(D,'corpus/lessons/round-95.md')).read(),
       'corpus/knowledge/entry.md':open(os.path.join(D,'corpus/knowledge/entry.md')).read()}
sur={'lessons':[{'path':p,'sha256':hashlib.sha256(c.encode()).hexdigest()} for p,c in files.items()],
     'entries':[{'path':'corpus/knowledge/entry.md','head8_sha256':hashlib.sha256('\n'.join(files['corpus/knowledge/entry.md'].splitlines()[:8]).encode()).hexdigest()}],
     'quality_criteria_headings':['Round-01 criterion — a thing'],
     'skill_rows':[{'cell':'t','path_tokens':1}],
     'mistakes_sections':['corpus/lessons/round-95.md']}
out='/fast/scratch/hyaku/kake-r95/ReviewC1/fixtures/R18/op_surfaces.json'
json.dump(sur,open(out,'w'),indent=1, sort_keys=True)
print('op_surfaces.json written')
EOF
echo "PHASE R18 build done"
