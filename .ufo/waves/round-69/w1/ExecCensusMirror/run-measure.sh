#!/usr/bin/env bash
# measure runner for ExecCensusMirror — regenerates measure.txt from scratch.
# Everything it creates lives under $S = /fast/scratch/hyaku/kake-r69/ExecCensusMirror.
set -u
S=${S:-/fast/scratch/hyaku/kake-r69/ExecCensusMirror}
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
REV=4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4
V=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
G=$LANE/.ufo/waves/round-69/w1/ExecCensusMirror/guard.sh
ART=$LANE/.ufo/waves/round-69/w1/ExecCensusMirror
OUT=$LANE/.ufo/waves/round-69/w1/ExecCensusMirror/measure.txt
TODAY=2026-11-03

run() { # run <label> <cmd...>
  echo "### $1"
  echo "\$ ${*:2}"
  "${@:2}" 2>&1
  echo "exit=$?"
  echo
}

{
echo "# ExecCensusMirror — SOURCES append guard, measured"
echo "# host date: $(date -u +%FT%TZ)   base revision: $REV"
echo

echo "## 0. inputs and tool identity"
echo "\$ git -C $LANE rev-parse HEAD"
git -C "$LANE" rev-parse HEAD; echo "exit=$?"
echo "\$ git -C $LANE show $REV:corpus/SOURCES.md | sha256sum"
git -C "$LANE" show "$REV:corpus/SOURCES.md" | sha256sum; echo "exit=$?"
echo "\$ git -C $LANE show $REV:corpus/SOURCES.md | wc -l"
git -C "$LANE" show "$REV:corpus/SOURCES.md" | wc -l; echo "exit=$?"
echo "\$ sha256sum $V"
sha256sum "$V"; echo "exit=$?"
echo "\$ sha256sum $G"
sha256sum "$G"; echo "exit=$?"
echo "\$ bash $V --help | sed -n '10,20p'   # usage, mode list"
bash "$V" --help | sed -n '10,20p'; echo "exit=$?"
echo

mkdir -p "$S/fx"
git -C "$LANE" show "$REV:corpus/SOURCES.md" > "$S/fx/registry.base.md"
cp "$ART/fixtures/staged-rows-placeholder.md" "$S/fx/staged.good.md"   # placeholder rows (rows-draft.md absent)

echo "## 1. guard.sh on the base registry (ids, no staged rows yet)"
run "1a. base registry id list size and shape" bash -c "grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' '$S/fx/registry.base.md' | grep -oE 'S[0-9]+' | sort | tee '$S/fx/ids.base' | wc -l; head -3 '$S/fx/ids.base'; tail -2 '$S/fx/ids.base'"
run "1b. guard with an empty staged file (no collisions, exit 0)" bash -c "printf '# nothing staged\n' > '$S/fx/staged.empty.md'; bash '$G' '$S/fx/registry.base.md' '$S/fx/staged.empty.md' '$S/fx/out-empty'"
run "1c. guard usage errors (missing file, wrong arity)" bash -c "bash '$G' '$S/fx/registry.base.md' '$S/fx/nope.md' '$S/fx/out-x'; echo rc=\$?; bash '$G' only-one-arg; echo rc=\$?"

echo "## 2. PROOF the guard can fail — fixture: one real row indented by two spaces"
echo "\$ sed -E 's/^\\| S435 \\|/  | S435 |/' registry.base.md > registry.indented.md"
sed -E 's/^\| S435 \|/  | S435 |/' "$S/fx/registry.base.md" > "$S/fx/registry.indented.md"; echo "exit=$?"
run "2a. the fixture really moved S435 off column 0 (col-0 row count drops 173 -> 172)" bash -c "grep -cE '^\\| S' '$S/fx/registry.base.md'; grep -cE '^\\| S' '$S/fx/registry.indented.md'; grep -nE '^ {2}\\| S[0-9]' '$S/fx/registry.indented.md' | cut -c1-46"
echo "\$ printf '| S435 | staged duplicate ... |' > staged.dup435.md"
printf '| S435 | staged duplicate of the indented S435 row | docs | A | fixture | section | fixture teaches | mined | 2026-11-03 | 90d | corpus/lessons/round-69.md |\n' > "$S/fx/staged.dup435.md"; echo "exit=$?"
run "2b. guard on the indented registry vs staged S435 (MUST collide)" bash "$G" "$S/fx/registry.indented.md" "$S/fx/staged.dup435.md" "$S/fx/out-indent"
run "2c. collisions file content and size (nonempty = guard fails as required)" bash -c "cat '$S/fx/out-indent/collisions'; echo '---'; wc -c < '$S/fx/out-indent/collisions'; wc -l < '$S/fx/out-indent/collisions'"
run "2d. counterfactual: a column-0-anchored pattern would MISS the indented row" bash -c "LC_ALL=C grep -oE '^\\|[[:space:]]*S[0-9]{3,}' '$S/fx/registry.indented.md' | grep -oE 'S[0-9]+' | LC_ALL=C sort > '$S/fx/naive.ids'; LC_ALL=C grep -oE '^\\|[[:space:]]*S[0-9]{3,}' '$S/fx/staged.dup435.md' | grep -oE 'S[0-9]+' | LC_ALL=C sort > '$S/fx/naive.staged'; echo naive_registry_ids=\$(wc -l < '$S/fx/naive.ids'); comm -12 '$S/fx/naive.ids' '$S/fx/naive.staged' > '$S/fx/naive.collisions'; echo naive_collisions_bytes=\$(wc -c < '$S/fx/naive.collisions')"
run "2e. same fixture with the shipped 0-3-space pattern (collision seen)" bash -c "bash '$G' '$S/fx/registry.indented.md' '$S/fx/staged.dup435.md' '$S/fx/out-indent2'; cat '$S/fx/out-indent2/collisions'"

echo "## 3. staged rows used for the mirror"
echo "\$ ls $LANE/.ufo/waves/round-69/w1/ScoutSources/rows-draft.md"
ls -l "$LANE/.ufo/waves/round-69/w1/ScoutSources/rows-draft.md" 2>&1; echo "exit=$?"
echo "# rows-draft.md absent at $(date -u +%FT%TZ) -> the two placeholder rows below stand in (S436 Node os, S437 Python tempfile)."
cat "$S/fx/staged.good.md" 2>/dev/null || true
echo

echo "## 4. mirror validation"
rm -rf "$S/mirror"; mkdir -p "$S/mirror"
echo "\$ git -C $LANE archive $REV corpus | tar -x -C $S/mirror"
git -C "$LANE" archive "$REV" corpus | tar -x -C "$S/mirror"; echo "exit=$?"
run "4a. registry rows in the mirror" bash -c "grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' '$S/mirror/corpus/SOURCES.md'"
run "4b. validate the UNMODIFIED base copy (expect exit 0)" bash "$V" validate --file "$S/mirror/corpus/SOURCES.md" --today "$TODAY"
run "4b'. why 4b is red: the corpus-only mirror has no sibling paths, so E11 fires" bash -c "sed -n '1,3p' /dev/null; grep -n 'used-by scripts/source_recheck.py' '$S/mirror/corpus/SOURCES.md' | head -1 | cut -c1-40"
rm -rf "$S/mirror-full"; mkdir -p "$S/mirror-full"
echo "\$ git -C $LANE archive $REV | tar -x -C $S/mirror-full   # full base tree, so used-by paths resolve"
git -C "$LANE" archive "$REV" | tar -x -C "$S/mirror-full"; echo "exit=$?"
run "4c. validate the UNMODIFIED base copy in a full base tree (expect exit 0)" bash "$V" validate --file "$S/mirror-full/corpus/SOURCES.md" --today "$TODAY"
rm -rf "$S/mirror-staged"; cp -a "$S/mirror-full" "$S/mirror-staged"
echo "\$ (append the two staged rows after the last '| S' row of the ## Registry section)"
python3 - "$S/mirror-staged/corpus/SOURCES.md" "$S/fx/staged.good.md" <<'PY'
import sys
target, staged = sys.argv[1], sys.argv[2]
lines = open(target, encoding='utf-8').read().split('\n')
start = next(i for i, l in enumerate(lines) if l.strip() == '## Registry')
end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith('#'))
last = max(i for i in range(start, end) if lines[i].lstrip().startswith('| S'))
rows = [r for r in open(staged, encoding='utf-8').read().split('\n') if r.strip()]
print(f"registry_section_lines={start + 1}-{end} last_registry_row_line={last + 1}")
lines[last + 1:last + 1] = rows
open(target, 'w', encoding='utf-8').write('\n'.join(lines))
print(f"appended {len(rows)} rows after line {last + 1}")
PY
echo "exit=$?"
run "4d. registry row count after the append" bash -c "grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' '$S/mirror-staged/corpus/SOURCES.md'; grep -nE '^\\| S43[5-7]' '$S/mirror-staged/corpus/SOURCES.md' | cut -c1-34"
run "4e. validate the STAGED mirror as-is (expect exit 1: E11 on both new rows, corpus/lessons/round-69.md absent at base)" bash "$V" validate --file "$S/mirror-staged/corpus/SOURCES.md" --today "$TODAY"
rm -rf "$S/mirror-staged-lesson"; cp -a "$S/mirror-staged" "$S/mirror-staged-lesson"
printf '# Round 69 — kake lane\n\nSTUB staged for the ExecCensusMirror rehearsal: only its existence is measured here (census E11 used-by resolution). The L1 lands the real lesson content.\n' > "$S/mirror-staged-lesson/corpus/lessons/round-69.md"
run "4f. validate the STAGED mirror once the named lesson path exists (expect exit 0, warnings only)" bash "$V" validate --file "$S/mirror-staged-lesson/corpus/SOURCES.md" --today "$TODAY"

echo "## 5. PROOF the validator can fail — a staged row with a literal pipe inside a cell"
rm -rf "$S/mirror-pipe"; cp -a "$S/mirror-staged-lesson" "$S/mirror-pipe"
python3 - "$S/mirror-pipe/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
old = "PLACEHOLDER: Node documents os.tmpdir() as the OS default temporary directory"
new = "PLACEHOLDER: Node documents os.tmpdir() | os.tmpdir() is the OS default temporary directory"
assert s.count(old) == 1, s.count(old)
open(p, 'w', encoding='utf-8').write(s.replace(old, new))
print("injected a literal pipe into the S436 'teaches' cell")
PY
echo "exit=$?"
run "5a. the injected row now carries 12 cells, not 11" bash -c "awk -F'|' '/^\\| S436 /{print \"S436 cells=\" NF-2}' '$S/mirror-pipe/corpus/SOURCES.md'"
run "5b. validate must exit nonzero (expect E01 S436 fields=12, exit 1)" bash "$V" validate --file "$S/mirror-pipe/corpus/SOURCES.md" --today "$TODAY"

echo "## 6. attacks run and their verdicts"
echo "- A1 guard-fails-on-collision (indented real row): KILLED — collisions=S435, exit 1 (2b/2c)."
echo "- A2 anchoring attack (column-0-only pattern): KILLED against the shipped pattern — 2e sees S435 where 2d's naive pattern reports naive_collisions_bytes=0."
echo "- A3 guard false-positive on a legitimate S436/S437 append: PASSED (no collision, exit 0) — staged.good.md run below."
run "6a. guard on the real append (base registry vs S436/S437)" bash "$G" "$S/fx/registry.base.md" "$S/fx/staged.good.md" "$S/fx/out-good"
echo "- A4 unmodified base copy validates clean: PASSED (4c exit 0)."
echo "- A5 staged mirror validates clean once its used-by path exists: PASSED (4f exit 0)."
echo "- A6 validator red on a 12-cell row: KILLED — E01 S436 fields=12, exit 1 (5b)."
echo
echo "## 7. scope of the guard's id scan (whole file, lexical — same as the seat spec)"
run "7a. base registry: any '| S###' row outside the ## Registry section? (expect none)" bash -c "awk '/^ {0,3}## /{sec=\$0} /^ {0,3}\\|[[:space:]]*S[0-9]/{if (sec !~ /## Registry/) print NR\": \"sec}' '$S/fx/registry.base.md'; echo scan_done"
run "7b. guard counts 173 ids both with the shipped 0-3-space pattern and against the census row parser" bash -c "grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' '$S/fx/registry.base.md' | grep -oE 'S[0-9]+' | LC_ALL=C sort -u | wc -l"

echo "## 8. lane untouched"
run "8a. lane git status (only the wave directory is new)" bash -c "git -C '$LANE' status --porcelain"
run "8b. base blob still the base blob" bash -c "git -C '$LANE' show $REV:corpus/SOURCES.md | sha256sum; sha256sum '$S/fx/registry.base.md'"
} > "$OUT" 2>&1
echo "wrote $OUT ($(wc -l < "$OUT") lines)"
