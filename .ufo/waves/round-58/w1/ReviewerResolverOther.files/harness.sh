#!/usr/bin/env bash
# ReviewerResolverOther — C2 breadth fixtures. No git mutation except the two
# revision-mode fixtures, which assert toplevel and commit with selftest identity.
set -u
S=/fast/scratch/hyaku/kake-r58/ReviewerResolverOther
SNAP="$S/id_resolver.snapshot.py"
BASE="$S/cases"
rm -rf "$BASE"
mkdir -p "$BASE"

new_lane() { # $1 case
  mkdir -p "$BASE/$1/lane/corpus/knowledge" "$BASE/$1/lane/docs"
  : > "$BASE/$1/.stamp"
}

wreg() { # $1 case, $2 registry text
  printf '%s' "$2" > "$BASE/$1/lane/corpus/SOURCES.md"
}

wk() { # $1 case, $2 knowledge text
  printf '%s' "$2" > "$BASE/$1/lane/corpus/knowledge/a.md"
}

CONTROL_REG='# Sources

## Registry

| ID | Source |
| --- | --- |
| S001 | https://e.example/1 |

## Notes

plain tail
'

run_case() { # $1 case, extra args after
  local c="$1"; shift
  local d="$BASE/$c/lane"
  local out rc last flags
  out=$(python3 -B "$SNAP" --root "$d" --fleet "$BASE/$c" "$@" 2>&1); rc=$?
  last=$(printf '%s\n' "$out" | grep -E '^ids_cited=' | tail -1)
  flags=$(printf '%s\n' "$out" | grep -E '^DANGLING ' | sed 's/ cited-by.*//;s/^DANGLING //' | paste -sd, -)
  printf 'CASE %s exit=%s | %s | flags=[%s]\n' "$c" "$rc" "${last:-<no-summary>}" "${flags:-}"
}

# c01 multiline HTML comment hiding a registry row (row line starts with |)
new_lane c01
wreg c01 '# Sources

## Registry

| ID | Source |
| --- | --- |
| S001 | https://e.example/1 |

<!--
| S900 | https://e.example/9 |
-->

## Notes
'
wk c01 'Cites S001 and S900.
'
run_case c01

# c02 single-line HTML comment (seat's literal example)
new_lane c02
wreg c02 "$CONTROL_REG
<!-- | S900 | https://e.example/9 | -->
"
wk c02 'Cites S001 and S900.
'
run_case c02

# c03 row inside a blockquote
new_lane c03
wreg c03 "$CONTROL_REG
> | S900 | https://e.example/9 |
"
wk c03 'Cites S001 and S900.
'
run_case c03

# c04 citation inside a blockquote (knowledge side)
new_lane c04
wreg c04 "$CONTROL_REG"
printf '> Cites S900.\nCites S001.\n' > "$BASE/c04/lane/corpus/knowledge/a.md"
run_case c04

# c05 setext heading AS the registry heading
new_lane c05
wreg c05 'Sources

Registry
---

| S001 | https://e.example/1 |
| S900 | https://e.example/9 |
'
wk c05 'Cites S001 and S900.
'
run_case c05

# c06 setext heading INSIDE the registry section (markdown ends section, tool does not)
new_lane c06
wreg c06 '# Sources

## Registry

| ID | Source |
| --- | --- |
| S001 | https://e.example/1 |

Subsection
---

| S900 | https://e.example/9 |
'
wk c06 'Cites S001 and S900.
'
run_case c06

# c07a citation reachable only through a symlinked directory (target inside the lane)
new_lane c07a
wreg c07a "$CONTROL_REG"
mkdir -p "$BASE/c07a/lane/notes_store"
printf 'Cites S900.\n' > "$BASE/c07a/lane/notes_store/hidden.md"
printf 'Cites S001.\n' > "$BASE/c07a/lane/corpus/knowledge/a.md"
ln -s ../../notes_store "$BASE/c07a/lane/corpus/knowledge/linked"
run_case c07a

# c07b citation through a symlinked FILE (target inside the lane) — contrast
new_lane c07b
wreg c07b "$CONTROL_REG"
mkdir -p "$BASE/c07b/lane/notes_store"
printf 'Cites S900.\n' > "$BASE/c07b/lane/notes_store/hidden.md"
printf 'Cites S001.\n' > "$BASE/c07b/lane/corpus/knowledge/a.md"
ln -s ../../notes_store/hidden.md "$BASE/c07b/lane/corpus/knowledge/link.md"
run_case c07b

# c08 non-.md markdown extensions (.markdown and .MD)
new_lane c08
wreg c08 "$CONTROL_REG"
printf 'Cites S900.\n' > "$BASE/c08/lane/corpus/knowledge/b.markdown"
printf 'Cites S901.\n' > "$BASE/c08/lane/corpus/knowledge/c.MD"
printf 'Cites S001.\n' > "$BASE/c08/lane/corpus/knowledge/a.md"
run_case c08

# c09 registry file with UTF-8 BOM
new_lane c09
printf '\xef\xbb\xbf' > "$BASE/c09/lane/corpus/SOURCES.md"
printf '%s' "$CONTROL_REG" >> "$BASE/c09/lane/corpus/SOURCES.md"
printf '%s' "$CONTROL_REG" | sed 's/S001/S900/; s|e.example/1|e.example/9|' > "$BASE/c09/alt.reg"
wk c09 'Cites S001 and S900.
'
run_case c09

# c09b UTF-8 BOM directly before the `## Registry` heading (file starts with the section)
new_lane c09b
printf '\xef\xbb\xbf## Registry\n\n| ID | Source |\n| --- | --- |\n| S001 | https://e.example/1 |\n| S900 | https://e.example/9 |\n' > "$BASE/c09b/lane/corpus/SOURCES.md"
wk c09b 'Cites S001 and S900.
'
run_case c09b

# c10 citation id split by a zero-width space (U+200B)
new_lane c10
wreg c10 "$CONTROL_REG"
printf 'Cites S\xe2\x80\x8b900.\nCites S001.\n' > "$BASE/c10/lane/corpus/knowledge/a.md"
run_case c10

# c11 citation in markdown outside corpus/knowledge
new_lane c11
wreg c11 "$CONTROL_REG"
printf 'Cites S900.\n' > "$BASE/c11/lane/docs/notes.md"
printf 'Cites S001.\n' > "$BASE/c11/lane/corpus/knowledge/a.md"
run_case c11

# --- revision-mode spot checks (c01 and c09 committed in their own fixture repos) ---
rev_fixture() { # $1 src-case, $2 dest-case
  local D="$BASE/$2/lane"
  mkdir -p "$BASE/$2"
  cp -a "$BASE/$1/lane" "$D"
  top=$(git -C "$D" rev-parse --show-toplevel 2>/dev/null || true)
  if [ "$top" != "$D" ]; then
    git -C "$D" init -q
    top=$(git -C "$D" rev-parse --show-toplevel)
    if [ "$top" != "$D" ]; then echo "REV-FIXTURE $2 ABORT: toplevel=$top"; return 1; fi
  fi
  git -C "$D" add -A
  git -C "$D" -c user.name=selftest -c user.email=selftest@local commit -qm selftest
}
if rev_fixture c01 r01; then run_case r01 --revision HEAD; fi
if rev_fixture c09 r09; then run_case r09 --revision HEAD; fi
